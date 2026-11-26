#!/usr/bin/env python3
"""审批证据链（TASK 4，stdlib-only，D05 JSON 原则，扩展现有 tools/）。

目的：让已有的人工 G1/G2/G3 批准结果对应到**具体文件版本**，并在发布前复核。
不新建审批平台、不改 run_state / KCR / 人工关卡的既有流程，只补两件事：
  1. 批准登记（record，仅人工执行）：把 run 当前全部产物冻结为
     「相对路径 + SHA256 + 所处阶段」，连同审批人、时间、决定、范围、当时的提交号
     写入 reviews/approvals/<run_id>/<gate>-NN.json。**只增不改**：没有更新或删除命令，
     重新批准会生成新的编号文件，旧记录原样保留。
  2. 发布前复核（verify；run_state.advance / skip 进入 PUBLISH / FEEDBACK 时自动调用）：
     读取最新审批记录 → 重算每个产物的 SHA256 → 与批准时比对 → 检查范围、审批人、时间。
     任何产物在批准后发生变化、或批准后新增了范围内的产物，都阻止发布，要求重新审核。

历史审批（8.3）：没有哈希绑定记录的过去批准不补造。verify 对「关卡已 passed 但没有
审批记录」的 run 报 legacy/unverifiable。历史批准的实际情况见 reviews/approvals/README.md。

已知限制（如实）：approver 仍是一个字符串，技术上无法证明它由人输入——这与
run_state gate --pass 相同；本工具增加的是「批准对应到文件版本」的可追溯性，
不是身份认证。

用法（本机用 py -3；record 仅人工执行）：
    py -3 tools/approval_chain.py record --run-id RUN-x --gate G3 --approver <人名> --scope "六课教材+测验+G1/G2 材料" [--path 额外文件 ...]
    py -3 tools/approval_chain.py verify --run-id RUN-x [--gate G3]
    py -3 tools/approval_chain.py show   --run-id RUN-x
退出码：0 通过；1 规则拒绝 / 复核未通过；2 用法或文件错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import run_state as rs  # noqa: E402
from kcr import validate_kcr  # noqa: E402

DEFAULT_APPROVALS_DIR = ROOT / "reviews" / "approvals"
GATES = ("G1", "G2", "G3")
SCHEMA = "approval-record"


class ApprovalError(Exception):
    """规则拒绝（缺少审批人 / 文件缺失 / 记录损坏）。CLI 捕获后退出码 1。"""


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _norm(p: str) -> str:
    return str(PurePosixPath(p.replace("\\", "/")))


def _resolve(path: str, root: Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else root / path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str, cwd: Path) -> str | None:
    """取不到 git 信息时返回 None（不在仓库内 / 未安装 git），不中断登记。"""
    try:
        out = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def latest_artifacts(state: dict) -> dict[str, dict]:
    """每个路径取最后一次登记（同一路径内容演进时旧哈希自然作废）。"""
    out: dict[str, dict] = {}
    for a in state.get("artifacts", []):
        out[_norm(a["path"])] = a
    return out


def record(runs_dir: Path, run_id: str, gate: str, approver: str, *, scope: str,
           note: str = "", extra_paths: tuple[str, ...] = (), decision: str = "approved",
           root: Path = ROOT, approvals_dir: Path = DEFAULT_APPROVALS_DIR) -> dict:
    """人工批准登记：冻结当前产物版本。只增不改。"""
    if gate not in GATES:
        raise ApprovalError(f"gate 非法：{gate}（可选 {GATES}）")
    if not approver or not approver.strip():
        raise ApprovalError("审批记录不可绕过：--approver 必填且非空（AI 不得代批）")
    if decision not in ("approved", "rejected"):
        raise ApprovalError(f"decision 非法：{decision}")
    if not scope or not scope.strip():
        raise ApprovalError("必须提供 --scope（本次批准覆盖什么）")
    state = rs.load_run(runs_dir, run_id)
    if state["human_gate"] and state["human_gate"]["status"] == "passed" \
            and state["human_gate"]["approver"] != approver.strip():
        raise ApprovalError(f"run 的关卡已由 {state['human_gate']['approver']} 通过，"
                            f"审批记录的 approver 必须一致（当前 {approver!r}）")
    entries = []
    for path, a in latest_artifacts(state).items():
        f = _resolve(path, root)
        if not f.is_file():
            raise ApprovalError(f"批准范围内的产物已不存在：{path}")
        entries.append({"path": path, "sha256": _sha(f), "phase": a["phase"], "kind": a["kind"]})
    for raw in extra_paths:
        path = _norm(raw)
        f = _resolve(path, root)
        if not f.is_file():
            raise ApprovalError(f"额外纳入范围的文件不存在：{path}")
        if any(e["path"] == path for e in entries):
            continue
        entries.append({"path": path, "sha256": _sha(f), "phase": "extra", "kind": "file"})
    if not entries:
        raise ApprovalError("该 run 还没有任何产物，没有可对应到文件版本的批准对象")
    dirty = _git("status", "--porcelain", cwd=root)
    rec = {
        "schema_version": 1,
        "record_id": "",
        "run_id": run_id,
        "gate_id": gate,
        "approver": approver.strip(),
        "approved_at": _now(),
        "decision": decision,
        "scope": scope.strip(),
        "approved_at_phase": state["phase"],
        "artifacts": entries,
        "commit": _git("rev-parse", "HEAD", cwd=root),
        "dirty_files": (len([x for x in dirty.splitlines() if x.strip()]) if dirty is not None else None),
        "note": note,
    }
    target_dir = approvals_dir / run_id
    target_dir.mkdir(parents=True, exist_ok=True)
    n = 1
    while (target_dir / f"{gate}-{n:02d}.json").exists():
        n += 1
    rec["record_id"] = f"{run_id}/{gate}-{n:02d}"
    errors = (validate_kcr.validate(rec, validate_kcr.load_schema(SCHEMA))
              + validate_kcr.semantic_errors(rec, SCHEMA))
    if errors:
        raise ApprovalError("审批记录未通过契约校验（不写盘）：\n  - " + "\n  - ".join(errors))
    target = target_dir / f"{gate}-{n:02d}.json"
    # 'x' 独占创建：绝不覆盖既有记录
    with open(target, "x", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
    return rec


def _load_records(run_id: str, approvals_dir: Path) -> list[dict]:
    d = approvals_dir / run_id
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.glob("*.json")):
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


def verify(runs_dir: Path | None, run_id: str, *, gate: str | None = None, state: dict | None = None,
           root: Path = ROOT, approvals_dir: Path = DEFAULT_APPROVALS_DIR) -> tuple[str, list[str], dict | None]:
    """发布前复核。返回 (状态, 问题列表, 所依据的记录)。
    状态：ok / no-record / legacy-unverifiable / failed。问题列表非空即不得发布。"""
    if state is None:
        state = rs.load_run(runs_dir, run_id)
    gate = gate or (state["human_gate"]["gate"] if state.get("human_gate") else None)
    recs = [r for r in _load_records(run_id, approvals_dir) if r.get("gate_id") == gate] if gate else []
    if not recs:
        passed = bool(state.get("human_gate")) and state["human_gate"].get("status") == "passed"
        if passed:
            return "legacy-unverifiable", [
                f"{gate} 已由 {state['human_gate'].get('approver')} 标记为 passed，但没有审批记录："
                "历史批准无法对应到具体文件版本（legacy / unverifiable，不补造）"], None
        return "no-record", [f"{gate or '关卡'} 还没有审批记录（先由人工执行 record）"], None
    rec = recs[-1]
    errors = (validate_kcr.validate(rec, validate_kcr.load_schema(SCHEMA))
              + validate_kcr.semantic_errors(rec, SCHEMA))
    problems = [f"审批记录 {rec.get('record_id')} 未通过契约校验：{e}" for e in errors]
    if errors:
        return "failed", problems, rec
    if rec["decision"] != "approved":
        problems.append(f"审批记录 {rec['record_id']} 的决定是 {rec['decision']}，不是批准")
    approved_paths = {e["path"] for e in rec["artifacts"]}
    for e in rec["artifacts"]:
        f = _resolve(e["path"], root)
        if not f.is_file():
            problems.append(f"批准时的产物已不存在：{e['path']}")
        elif _sha(f) != e["sha256"]:
            problems.append(f"产物在批准后已变化，需重新审核：{e['path']}")
    approved_idx = rs.PHASES.index(rec["approved_at_phase"]) if rec["approved_at_phase"] in rs.PHASES else len(rs.PHASES)
    for path, a in latest_artifacts(state).items():
        if path not in approved_paths and rs.PHASES.index(a["phase"]) <= approved_idx:
            problems.append(f"批准后新增的产物不在审批范围内，需重新审核：{path}（{a['phase']}）")
    return ("ok" if not problems else "failed"), problems, rec


def verify_state(state: dict, *, root: Path = ROOT,
                 approvals_dir: Path = DEFAULT_APPROVALS_DIR) -> list[str]:
    """供 run_state.advance / skip 调用：返回问题列表（空 = 通过）。"""
    gate = state["human_gate"]["gate"] if state.get("human_gate") else None
    _, problems, _ = verify(None, state["run_id"], gate=gate, state=state,
                            root=root, approvals_dir=approvals_dir)
    return problems


def show(run_id: str, approvals_dir: Path = DEFAULT_APPROVALS_DIR) -> list[dict]:
    return [{k: r.get(k) for k in ("record_id", "gate_id", "approver", "approved_at", "decision",
                                   "approved_at_phase", "commit", "dirty_files")}
            | {"artifacts": len(r.get("artifacts", []))} for r in _load_records(run_id, approvals_dir)]


def main() -> int:
    parser = argparse.ArgumentParser(description="审批证据链：批准对应到文件版本 + 发布前复核（record 仅人工执行）")
    parser.add_argument("--runs-dir", default=str(rs.DEFAULT_RUNS_DIR))
    parser.add_argument("--approvals-dir", default=str(DEFAULT_APPROVALS_DIR))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("record", help="人工批准登记（冻结产物哈希；只增不改）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--gate", required=True, choices=GATES)
    p.add_argument("--approver", required=True)
    p.add_argument("--scope", required=True, help="本次批准覆盖什么")
    p.add_argument("--note", default="")
    p.add_argument("--path", nargs="*", default=[], help="额外纳入范围的文件（相对仓库根）")

    p = sub.add_parser("verify", help="发布前复核（重算哈希、检查范围）")
    p.add_argument("--run-id", required=True)
    p.add_argument("--gate", choices=GATES)

    p = sub.add_parser("show", help="列出某 run 的全部审批记录")
    p.add_argument("--run-id", required=True)

    args = parser.parse_args()
    runs_dir, approvals_dir = Path(args.runs_dir), Path(args.approvals_dir)
    try:
        if args.cmd == "record":
            rec = record(runs_dir, args.run_id, args.gate, args.approver, scope=args.scope,
                         note=args.note, extra_paths=tuple(args.path), approvals_dir=approvals_dir)
            print(json.dumps({"record_id": rec["record_id"], "artifacts": len(rec["artifacts"]),
                              "commit": rec["commit"]}, ensure_ascii=False, indent=2))
            return 0
        if args.cmd == "verify":
            status, problems, rec = verify(runs_dir, args.run_id, gate=args.gate, approvals_dir=approvals_dir)
            print(json.dumps({"run_id": args.run_id, "status": status,
                              "record": rec["record_id"] if rec else None,
                              "problems": problems}, ensure_ascii=False, indent=2))
            return 0 if status == "ok" else 1
        print(json.dumps(show(args.run_id, approvals_dir), ensure_ascii=False, indent=2))
        return 0
    except ApprovalError as exc:
        print(f"拒绝：{exc}", file=sys.stderr)
        return 1
    except rs.RunStateError as exc:
        print(f"拒绝：{exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as exc:
        print(f"文件错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
