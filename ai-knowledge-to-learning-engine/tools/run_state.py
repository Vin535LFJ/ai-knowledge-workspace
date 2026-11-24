#!/usr/bin/env python3
"""P9 轻量工作流状态机（stdlib-only，D05 JSON 原则，扩展现有 tools/）。

设计依据：reviews/P9-orchestrator-design.md（状态机 + run-state schema + 五条不变量）
         archive/process-history/NEXT_PHASE_PLAN.md P9.2（重试/断点恢复/防重复写入/来源追踪/人工跳过暂停）
         reviews/EXECUTION_PLAN_V3.md P9（每阶段输入/输出/执行记录/完成条件）

运行态落盘 `.agent/runs/<run_id>.json`（D15：本地 only，已在 .gitignore；
摘要留痕走 CHANGELOG/archive，不提交运行态）。不引入 DB/队列/分布式组件。

不变量（程序强制，不可绕过）：
1. 人工门不可绕过：human_gate 只能经 `gate --pass --approver <人名>` 改为 passed；
   任何 API/CLI 路径都不接受空 approver，AI 不得批准。
2. AI 不预填裁决：本工具只记录关卡状态与材料 artifact，不写评分/裁决内容。
3. 未批准不应用：进入 PUBLISH/FEEDBACK 必须 gate passed；KCR 子状态到
   APPROVED 必须有人工 approver，APPLIED 只能在 APPROVED 之后。
4. 单写者：同一 write_path 同时刻只能被一个未完成 run 持有（声明即持有，
   pending/running/paused/failed 均算；done 自动释放，或显式 release-path）。
5. 可追溯：artifact 记录 path+sha256；每次状态变更追加 transitions（时间/操作者/理由）。

写盘纪律（沿用 kcr_impact.py）：每次保存前经 tools/kcr/validate_kcr.py 全量校验
（schema + semantic），失败不写文件；临时文件 + os.replace 原子替换。

用法（本机用 py -3；--runs-dir 可指向临时目录供测试）：
    py -3 tools/run_state.py new --run-id RUN-2026-11-20-demo --owner qwenwork --gate G3
    py -3 tools/run_state.py start --run-id RUN-2026-11-20-demo
    py -3 tools/run_state.py artifact --run-id ... --path reviews/kcr/impact-v14-replay.json
    py -3 tools/run_state.py advance --run-id ... --reason "研究报告完成"
    py -3 tools/run_state.py gate --run-id ... --pass --approver <人名>   # 仅人工执行
    py -3 tools/run_state.py pause|resume|fail|retry|skip|kcr|show|list ...
退出码：0 成功；1 规则拒绝（不变量/完成条件/重复保护）；2 用法/文件错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from kcr import validate_kcr  # noqa: E402

DEFAULT_RUNS_DIR = ROOT / ".agent" / "runs"

PHASES = ["INTAKE", "RESEARCH", "EVIDENCE", "ARCHITECT", "WRITE",
          "DESIGN", "PRACTICE", "REVIEW", "PUBLISH", "FEEDBACK"]
KCR_STATES = ["PROPOSED", "REVIEWING", "APPROVED", "APPLIED", "VERIFIED"]

# 每阶段：角色 / 完成条件（advance 的硬条件 = 本阶段至少 1 个 artifact；
# 进入 PUBLISH 另需 gate passed）/ 下一步动作提示（resume_point 用）。
PHASE_INFO = {
    "INTAKE":    ("Research Agent", "登记输入资料清单（来源/路径/范围）", "查已有知识，确定研究缺口"),
    "RESEARCH":  ("Research Agent", "研究报告 artifact（可挂 kcr_impact 影响分析）", "提取断言草稿与证据"),
    "EVIDENCE":  ("Evidence Analyst", "断言草稿/证据 artifact（新断言默认 open/low）", "G1 材料备齐，等人工核验；整理概念关系"),
    "ARCHITECT": ("Knowledge Architect", "concepts/知识模型变更提案 artifact", "G1 通过后落权威 JSON；规划课程结构"),
    "WRITE":     ("Documentation Writer", "教材草稿 artifact", "设计学习体验与交互"),
    "DESIGN":    ("Learning Designer", "学习设计/交互方案 artifact", "设计练习与实验"),
    "PRACTICE":  ("Practice Designer", "lab/quiz artifact", "提交独立审读，备 G2 材料"),
    "REVIEW":    ("Knowledge Reviewer", "审读记录/G2 评分材料 artifact（AI 不填分数）", "等人工 G2/G3 裁决；修订后重审"),
    "PUBLISH":   ("Knowledge Publisher", "发布记录 artifact（build/validate 输出）", "收集学习反馈"),
    "FEEDBACK":  ("Feedback Analyst", "反馈记录 artifact", "advance 收尾 → done，释放 write_paths"),
}


class RunStateError(Exception):
    """规则拒绝（不变量/完成条件/重复保护）。CLI 捕获后退出码 1。"""


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _norm_path(p: str) -> str:
    return str(PurePosixPath(p.replace("\\", "/")))


def _run_file(runs_dir: Path, run_id: str) -> Path:
    if not run_id.startswith("RUN-") or "/" in run_id or "\\" in run_id or run_id in ("RUN-", "RUN-."):
        raise RunStateError(f"run_id 非法：{run_id!r}（须匹配 ^RUN-[A-Za-z0-9._-]+$）")
    return runs_dir / f"{run_id}.json"


def load_run(runs_dir: Path, run_id: str) -> dict:
    f = _run_file(runs_dir, run_id)
    if not f.exists():
        raise RunStateError(f"run 不存在：{f}")
    return json.loads(f.read_text(encoding="utf-8"))


def _validate(state: dict) -> None:
    errors = (validate_kcr.validate(state, validate_kcr.load_schema("run-state"))
              + validate_kcr.semantic_errors(state, "run-state"))
    if errors:
        raise RunStateError("run-state 契约校验失败（不写盘）：\n  - " + "\n  - ".join(errors))


def _save(runs_dir: Path, state: dict) -> None:
    _validate(state)
    runs_dir.mkdir(parents=True, exist_ok=True)
    target = _run_file(runs_dir, state["run_id"])
    # 固定名临时文件 + os.replace 原子替换；校验先行，失败不产生 tmp。
    # 不做任何删除操作：极端写入中断遗留的 .tmp 会被下次保存覆盖（glob 只认 RUN-*.json）。
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def _log(state: dict, operator: str, action: str, detail: str, reason: str = "") -> None:
    state["transitions"].append({"at": _now(), "operator": operator,
                                 "action": action, "detail": detail, "reason": reason})
    state["updated_at"] = _now()
    _refresh_resume(state)


def _refresh_resume(state: dict) -> None:
    info = PHASE_INFO[state["phase"]]
    state["resume_point"] = f"{state['phase']} / {state['status']} / 下一步：{info[2]}"


def _record(state: dict, phase: str) -> dict:
    return next(r for r in state["phase_records"] if r["phase"] == phase)


def _iter_runs(runs_dir: Path):
    if not runs_dir.exists():
        return
    for f in sorted(runs_dir.glob("RUN-*.json")):
        try:
            yield json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue  # 损坏文件不参与单写者判定，show/list 会如实报错


def _check_write_conflict(runs_dir: Path, write_paths: list[str], exclude_run: str) -> None:
    want = {_norm_path(p) for p in write_paths}
    if not want:
        return
    for other in _iter_runs(runs_dir):
        if other.get("run_id") == exclude_run or other.get("status") == "done":
            continue
        held = {_norm_path(p) for p in other.get("write_paths", [])}
        clash = want & held
        if clash:
            raise RunStateError(f"单写者冲突：{sorted(clash)} 已由未完成 run {other['run_id']}"
                                f"（owner={other.get('owner_agent')}, status={other.get('status')}）持有；"
                                "先等其 done 或 release-path")


def new_run(runs_dir: Path, run_id: str, owner: str, *, title: str = "",
            dependencies: list[str] | None = None, write_paths: list[str] | None = None,
            gate: str | None = None, kcr: bool = False) -> dict:
    f = _run_file(runs_dir, run_id)
    if f.exists():
        raise RunStateError(f"防重复写入：run_id 已存在 {f}（断点续跑请用 resume/show，不要重建）")
    if not owner:
        raise RunStateError("owner_agent 必填（单写者约定）")
    if gate is not None and gate not in ("G1", "G2", "G3"):
        raise RunStateError(f"gate 非法：{gate}")
    deps = list(dependencies or [])
    for d in deps:
        if not _run_file(runs_dir, d).exists():
            raise RunStateError(f"依赖 run 不存在：{d}")
    paths = [_norm_path(p) for p in (write_paths or [])]
    _check_write_conflict(runs_dir, paths, run_id)
    now = _now()
    state = {
        "schema_version": 1,
        "run_id": run_id,
        "title": title or run_id,
        "phase": "INTAKE",
        "status": "pending",
        "kcr_substate": "PROPOSED" if kcr else None,
        "owner_agent": owner,
        "dependencies": deps,
        "write_paths": paths,
        "artifacts": [],
        "human_gate": ({"gate": gate, "status": "open", "approver": None, "approved_at": None}
                       if gate else None),
        "phase_records": [
            {"phase": p, "status": "active" if p == "INTAKE" else "pending",
             "entered_at": now if p == "INTAKE" else None, "completed_at": None,
             "failure_reason": None, "retry_count": 0, "next_action": PHASE_INFO[p][2]}
            for p in PHASES
        ],
        "transitions": [{"at": now, "operator": owner, "action": "new",
                         "detail": f"INTAKE/pending gate={gate} kcr={kcr}", "reason": title}],
        "resume_point": "",
        "created_at": now,
        "updated_at": now,
    }
    _refresh_resume(state)
    _save(runs_dir, state)
    return state


def _mutate(runs_dir: Path, run_id: str) -> dict:
    state = load_run(runs_dir, run_id)
    return state


def start(runs_dir: Path, run_id: str, *, reason: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] not in ("pending", "paused"):
        raise RunStateError(f"start 仅接受 pending/paused，当前 {state['status']}")
    _check_write_conflict(runs_dir, state["write_paths"], run_id)
    old = state["status"]
    state["status"] = "running"
    _log(state, state["owner_agent"], "start", f"{old}->running", reason)
    _save(runs_dir, state)
    return state


def pause(runs_dir: Path, run_id: str, *, reason: str = "", operator: str | None = None) -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] != "running":
        raise RunStateError(f"pause 仅接受 running，当前 {state['status']}")
    state["status"] = "paused"
    _log(state, operator or state["owner_agent"], "pause", "running->paused", reason)
    _save(runs_dir, state)
    return state


def resume(runs_dir: Path, run_id: str, *, reason: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] != "paused":
        raise RunStateError(f"resume 仅接受 paused，当前 {state['status']}（failed 请用 retry）")
    _check_write_conflict(runs_dir, state["write_paths"], run_id)
    state["status"] = "running"
    _log(state, state["owner_agent"], "resume", f"paused->running @ {state['resume_point']}", reason)
    _save(runs_dir, state)
    return state


def fail(runs_dir: Path, run_id: str, *, reason: str) -> dict:
    if not reason:
        raise RunStateError("fail 必须提供 --reason（失败原因留痕）")
    state = _mutate(runs_dir, run_id)
    if state["status"] not in ("running", "pending"):
        raise RunStateError(f"fail 仅接受 running/pending，当前 {state['status']}")
    state["status"] = "failed"
    rec = _record(state, state["phase"])
    rec["failure_reason"] = reason
    _log(state, state["owner_agent"], "fail", f"{state['phase']}->failed", reason)
    _save(runs_dir, state)
    return state


def retry(runs_dir: Path, run_id: str, *, reason: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] != "failed":
        raise RunStateError(f"retry 仅接受 failed，当前 {state['status']}")
    _check_write_conflict(runs_dir, state["write_paths"], run_id)
    rec = _record(state, state["phase"])
    rec["retry_count"] += 1
    rec["failure_reason"] = None
    state["status"] = "running"
    _log(state, state["owner_agent"], "retry",
         f"{state['phase']} retry#{rec['retry_count']} failed->running", reason)
    _save(runs_dir, state)
    return state


def add_artifact(runs_dir: Path, run_id: str, path: str, *, phase: str | None = None,
                 kind: str | None = None, note: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] == "done":
        raise RunStateError("run 已 done，不再接受 artifact（防重复写入）")
    src = Path(path)
    if not src.is_absolute():
        src = ROOT / path
    if not src.exists():
        raise RunStateError(f"artifact 文件不存在：{src}")
    phase = phase or state["phase"]
    if phase not in PHASES:
        raise RunStateError(f"phase 非法：{phase}")
    if PHASES.index(phase) > PHASES.index(state["phase"]):
        raise RunStateError(f"阶段跳转检查：不能为未来阶段 {phase} 登记 artifact（当前 {state['phase']}）")
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    # 与 kcr_impact 对接：impact-report 类 artifact 登记前过契约校验，失败不登记
    inferred = kind or ("impact-report" if "impact" in src.name.lower() and src.suffix == ".json" else "file")
    if inferred == "impact-report":
        try:
            doc = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RunStateError(f"impact-report 解析失败：{exc}") from exc
        errors = validate_kcr.validate(doc, validate_kcr.load_schema("impact-report"))
        if errors:
            raise RunStateError("impact-report 契约校验失败（不登记）：\n  - " + "\n  - ".join(errors))
    rel = _norm_path(str(src.relative_to(ROOT))) if src.is_relative_to(ROOT) else _norm_path(str(src))
    for a in state["artifacts"]:
        if a["phase"] == phase and a["path"] == rel and a["hash"] == digest:
            return state  # 幂等：同 phase+path+hash 不重复登记
    state["artifacts"].append({"phase": phase, "path": rel, "hash": digest,
                               "kind": inferred, "registered_at": _now(), "note": note})
    _log(state, state["owner_agent"], "artifact", f"{phase}: {rel} ({inferred})", note)
    _save(runs_dir, state)
    return state


def advance(runs_dir: Path, run_id: str, *, reason: str = "", operator: str | None = None) -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] != "running":
        raise RunStateError(f"advance 仅接受 running，当前 {state['status']}（paused→resume，failed→retry）")
    cur = state["phase"]
    if not any(a["phase"] == cur for a in state["artifacts"]):
        raise RunStateError(f"完成条件未满足：{cur} 还没有 artifact（{PHASE_INFO[cur][1]}）")
    op = operator or state["owner_agent"]
    if cur == "FEEDBACK":
        state["status"] = "done"
        _record(state, cur)["status"] = "done"
        _record(state, cur)["completed_at"] = _now()
        released = state["write_paths"]
        state["write_paths"] = []
        _log(state, op, "done", f"FEEDBACK->done，释放 write_paths={released}", reason)
        _save(runs_dir, state)
        return state
    nxt = PHASES[PHASES.index(cur) + 1]
    if nxt in ("PUBLISH", "FEEDBACK"):
        g = state["human_gate"]
        if not g or g["status"] != "passed":
            raise RunStateError(f"人工门不可绕过：进入 {nxt} 需要 gate passed"
                                f"（当前 {g['gate'] + '/' + g['status'] if g else '无 gate'}；"
                                "仅人工可执行 gate --pass --approver <人名>）")
    _record(state, cur)["status"] = "done"
    _record(state, cur)["completed_at"] = _now()
    rec = _record(state, nxt)
    rec["status"] = "active"
    rec["entered_at"] = _now()
    state["phase"] = nxt
    _log(state, op, "advance", f"{cur}->{nxt}", reason)
    _save(runs_dir, state)
    return state


def skip(runs_dir: Path, run_id: str, to_phase: str, *, approver: str, reason: str) -> dict:
    if not approver:
        raise RunStateError("人工跳过必须提供 --approver（AI 不得自行跳阶段）")
    if not reason:
        raise RunStateError("人工跳过必须提供 --reason")
    state = _mutate(runs_dir, run_id)
    if to_phase not in PHASES:
        raise RunStateError(f"目标阶段非法：{to_phase}")
    cur_i, to_i = PHASES.index(state["phase"]), PHASES.index(to_phase)
    if to_i <= cur_i:
        raise RunStateError(f"阶段跳转检查：skip 只能向前（{state['phase']} → {to_phase} 非法）")
    if to_i >= PHASES.index("PUBLISH"):
        g = state["human_gate"]
        if not g or g["status"] != "passed":
            raise RunStateError("人工门不可绕过：跳过至 PUBLISH/FEEDBACK 仍需 gate passed")
    for p in PHASES[cur_i:to_i]:
        rec = _record(state, p)
        rec["status"] = "skipped"
        rec["completed_at"] = _now()
    rec = _record(state, to_phase)
    rec["status"] = "active"
    rec["entered_at"] = _now()
    state["phase"] = to_phase
    if state["status"] in ("pending", "paused"):
        state["status"] = "running"
    _log(state, approver, "human_skip", f"{PHASES[cur_i]}->{to_phase}", reason)
    _save(runs_dir, state)
    return state


def pass_gate(runs_dir: Path, run_id: str, *, approver: str) -> dict:
    if not approver or not approver.strip():
        raise RunStateError("人工门不可绕过：--approver 必填且非空（AI 不得写入 passed）")
    state = _mutate(runs_dir, run_id)
    g = state["human_gate"]
    if not g:
        raise RunStateError("该 run 未设置 human_gate（new --gate G1|G2|G3）")
    if g["status"] == "passed":
        raise RunStateError(f"gate {g['gate']} 已由 {g['approver']} 于 {g['approved_at']} 通过，不重复批准")
    g["status"] = "passed"
    g["approver"] = approver.strip()
    g["approved_at"] = _now()
    _log(state, approver.strip(), "gate_passed", f"{g['gate']} open->passed", "人工裁决")
    _save(runs_dir, state)
    return state


def set_gate(runs_dir: Path, run_id: str, gate: str, *, reason: str = "") -> dict:
    if gate not in ("G1", "G2", "G3"):
        raise RunStateError(f"gate 非法：{gate}")
    state = _mutate(runs_dir, run_id)
    g = state["human_gate"]
    if g and g["status"] == "passed":
        raise RunStateError("已 passed 的关卡记录不可重置（可追溯）；如需新关卡请另建 run")
    state["human_gate"] = {"gate": gate, "status": "open", "approver": None, "approved_at": None}
    _log(state, state["owner_agent"], "gate_set", f"gate={gate}/open", reason)
    _save(runs_dir, state)
    return state


def kcr_transition(runs_dir: Path, run_id: str, to: str, *, approver: str | None = None,
                   reason: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    cur = state["kcr_substate"]
    if cur is None:
        raise RunStateError("该 run 未启用 KCR 子状态（new --kcr）")
    if to not in KCR_STATES:
        raise RunStateError(f"KCR 子状态非法：{to}")
    if KCR_STATES.index(to) != KCR_STATES.index(cur) + 1:
        raise RunStateError(f"KCR 顺序检查：{cur} 只能到 {KCR_STATES[KCR_STATES.index(cur) + 1] if cur != 'VERIFIED' else '（终点）'}，不能到 {to}")
    if to == "APPROVED":
        if not approver or not approver.strip():
            raise RunStateError("未批准不应用：KCR APPROVED 必须有人工 --approver（AI 不得自批）")
        op = approver.strip()
        action = "kcr_approved"
    else:
        op = state["owner_agent"]
        action = "kcr"
    state["kcr_substate"] = to
    _log(state, op, action, f"{cur}->{to}", reason)
    _save(runs_dir, state)
    return state


def claim_path(runs_dir: Path, run_id: str, path: str) -> dict:
    state = _mutate(runs_dir, run_id)
    if state["status"] == "done":
        raise RunStateError("run 已 done，不再接受 write_path")
    p = _norm_path(path)
    if p in state["write_paths"]:
        return state
    _check_write_conflict(runs_dir, [p], run_id)
    state["write_paths"].append(p)
    _log(state, state["owner_agent"], "claim_path", p)
    _save(runs_dir, state)
    return state


def release_path(runs_dir: Path, run_id: str, path: str, *, reason: str = "") -> dict:
    state = _mutate(runs_dir, run_id)
    p = _norm_path(path)
    if p not in state["write_paths"]:
        raise RunStateError(f"该 run 未持有 write_path：{p}")
    state["write_paths"].remove(p)
    _log(state, state["owner_agent"], "release_path", p, reason)
    _save(runs_dir, state)
    return state


def summary(state: dict) -> dict:
    rec = _record(state, state["phase"])
    return {
        "run_id": state["run_id"], "title": state["title"],
        "phase": state["phase"], "status": state["status"],
        "kcr_substate": state["kcr_substate"], "owner_agent": state["owner_agent"],
        "human_gate": state["human_gate"], "write_paths": state["write_paths"],
        "artifacts": len(state["artifacts"]), "retry_count": rec["retry_count"],
        "failure_reason": rec["failure_reason"], "resume_point": state["resume_point"],
        "updated_at": state["updated_at"],
    }


# ---------------------------------------------------------------- CLI

def main() -> int:
    parser = argparse.ArgumentParser(description="P9 轻量工作流状态机（stdlib-only）")
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR), help="运行态目录（默认 .agent/runs）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="创建 run（重复 run_id 拒绝）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--depends", nargs="*", default=[])
    p.add_argument("--write-path", nargs="*", default=[])
    p.add_argument("--gate", choices=["G1", "G2", "G3"])
    p.add_argument("--kcr", action="store_true", help="启用 KCR 子状态（PROPOSED 起）")

    for name, hlp in (("start", "pending/paused → running"), ("show", "查看 run 摘要与续跑点"),
                      ("pause", "人工暂停（running → paused）"), ("resume", "断点恢复（paused → running）")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("--run-id", required=True)
        if name in ("pause", "resume", "start"):
            p.add_argument("--reason", default="")
        if name == "pause":
            p.add_argument("--operator", default=None, help="暂停操作者（人工暂停时填人名）")

    p = sub.add_parser("fail", help="标记失败（必须给原因）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--reason", required=True)
    p = sub.add_parser("retry", help="失败重试（retry_count +1）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--reason", default="")

    p = sub.add_parser("artifact", help="登记阶段产物（path+sha256；impact-report 自动过契约）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--phase", choices=PHASES)
    p.add_argument("--kind", default=None)
    p.add_argument("--note", default="")

    p = sub.add_parser("advance", help="推进到下一阶段（完成条件 + 人工门检查）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--reason", default="")

    p = sub.add_parser("skip", help="人工向前跳阶段（必须 approver+reason）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--to", required=True, choices=PHASES)
    p.add_argument("--approver", required=True)
    p.add_argument("--reason", required=True)

    p = sub.add_parser("gate", help="查看/人工通过关卡（--pass 必须 --approver，仅人工执行）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--pass", dest="pass_", action="store_true")
    p.add_argument("--approver", default=None)
    p.add_argument("--set", dest="set_gate", choices=["G1", "G2", "G3"], help="设置/切换跟踪的关卡（重置为 open）")

    p = sub.add_parser("kcr", help="KCR 子状态推进（APPROVED 必须人工 approver）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--to", required=True, choices=KCR_STATES)
    p.add_argument("--approver", default=None)
    p.add_argument("--reason", default="")

    p = sub.add_parser("claim-path", help="声明单写者 write_path")
    p.add_argument("--run-id", required=True)
    p.add_argument("--path", required=True)
    p = sub.add_parser("release-path", help="释放 write_path")
    p.add_argument("--run-id", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--reason", default="")

    sub.add_parser("list", help="列出全部 run")

    args = parser.parse_args()
    runs_dir = Path(args.runs_dir)
    try:
        if args.cmd == "new":
            state = new_run(runs_dir, args.run_id, args.owner, title=args.title,
                            dependencies=args.depends, write_paths=args.write_path,
                            gate=args.gate, kcr=args.kcr)
        elif args.cmd == "start":
            state = start(runs_dir, args.run_id, reason=args.reason)
        elif args.cmd == "pause":
            state = pause(runs_dir, args.run_id, reason=args.reason, operator=args.operator)
        elif args.cmd == "resume":
            state = resume(runs_dir, args.run_id, reason=args.reason)
        elif args.cmd == "fail":
            state = fail(runs_dir, args.run_id, reason=args.reason)
        elif args.cmd == "retry":
            state = retry(runs_dir, args.run_id, reason=args.reason)
        elif args.cmd == "artifact":
            state = add_artifact(runs_dir, args.run_id, args.path, phase=args.phase,
                                 kind=args.kind, note=args.note)
        elif args.cmd == "advance":
            state = advance(runs_dir, args.run_id, reason=args.reason)
        elif args.cmd == "skip":
            state = skip(runs_dir, args.run_id, args.to, approver=args.approver, reason=args.reason)
        elif args.cmd == "gate":
            if args.pass_:
                state = pass_gate(runs_dir, args.run_id, approver=args.approver or "")
            elif args.set_gate:
                state = set_gate(runs_dir, args.run_id, args.set_gate)
            else:
                state = load_run(runs_dir, args.run_id)
                print(json.dumps(state["human_gate"], ensure_ascii=False, indent=2))
                return 0
        elif args.cmd == "kcr":
            state = kcr_transition(runs_dir, args.run_id, args.to,
                                   approver=args.approver, reason=args.reason)
        elif args.cmd == "claim-path":
            state = claim_path(runs_dir, args.run_id, args.path)
        elif args.cmd == "release-path":
            state = release_path(runs_dir, args.run_id, args.path, reason=args.reason)
        elif args.cmd == "show":
            state = load_run(runs_dir, args.run_id)
            print(json.dumps(summary(state), ensure_ascii=False, indent=2))
            return 0
        elif args.cmd == "list":
            rows = [summary(s) for s in _iter_runs(runs_dir)]
            if not rows:
                print(f"（{runs_dir} 无 run）")
                return 0
            for r in rows:
                g = r["human_gate"]
                print(f"{r['run_id']}  {r['phase']:<9} {r['status']:<8} "
                      f"gate={g['gate'] + '/' + g['status'] if g else '-':<9} "
                      f"kcr={r['kcr_substate'] or '-':<9} owner={r['owner_agent']}")
            return 0
        else:  # pragma: no cover
            raise RunStateError(f"未知命令 {args.cmd}")
    except RunStateError as exc:
        print(f"拒绝：{exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as exc:
        print(f"文件错误：{exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary(state), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())