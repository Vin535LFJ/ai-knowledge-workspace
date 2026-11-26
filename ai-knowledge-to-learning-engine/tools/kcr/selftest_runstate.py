#!/usr/bin/env python3
"""P9 自测：run_state 轻量状态机 ↔ run-state.schema.json 对齐 + 不变量 + 真实回放。

stdlib-only（D05 原则）。运行：py -3 tools/kcr/selftest_runstate.py
覆盖：schema 正反用例 / 五条不变量（人工门/AI 不预填/未批准不应用/单写者/可追溯）/
断点恢复 / 失败重试 / 防重复写入 / 人工跳过暂停 / KCR 子状态顺序 /
kcr_impact 真实影响分析对接（SRC-RN-COLORMGMT 回放）/ CLI 退出码。
所有运行态写入临时目录，不触碰真实 .agent/runs/。
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import kcr_impact  # noqa: E402
import run_state as rs  # noqa: E402
import approval_chain  # noqa: E402
from kcr import validate_kcr  # noqa: E402

RUN_SCHEMA = validate_kcr.load_schema("run-state")


def minimal_run() -> dict:
    """手工构造最小合法 run-state（INTAKE/pending，无 gate）。"""
    now = "2026-11-20T18:00:00+08:00"
    return {
        "schema_version": 1,
        "run_id": "RUN-test-min",
        "title": "最小合法样例",
        "phase": "INTAKE",
        "status": "pending",
        "kcr_substate": None,
        "owner_agent": "qwenwork",
        "dependencies": [],
        "write_paths": [],
        "artifacts": [],
        "human_gate": None,
        "phase_records": [
            {"phase": p, "status": "active" if p == "INTAKE" else "pending",
             "entered_at": now if p == "INTAKE" else None, "completed_at": None,
             "failure_reason": None, "retry_count": 0, "next_action": rs.PHASE_INFO[p][2]}
            for p in rs.PHASES
        ],
        "transitions": [{"at": now, "operator": "qwenwork", "action": "new",
                         "detail": "INTAKE/pending", "reason": ""}],
        "resume_point": "INTAKE / pending",
        "created_at": now,
        "updated_at": now,
    }


class SchemaTests(unittest.TestCase):
    def assert_ok(self, doc: dict) -> None:
        self.assertEqual(validate_kcr.validate(doc, RUN_SCHEMA), [])
        self.assertEqual(validate_kcr.semantic_errors(doc, "run-state"), [])

    def test_minimal_valid(self):
        self.assert_ok(minimal_run())

    def test_missing_required(self):
        doc = minimal_run()
        del doc["resume_point"]
        self.assertTrue(any("resume_point" in e for e in validate_kcr.validate(doc, RUN_SCHEMA)))

    def test_bad_phase_enum(self):
        doc = minimal_run()
        doc["phase"] = "KNOWLEDGE"  # V3 旧稿阶段名，不在设计稿十阶段内
        self.assertTrue(validate_kcr.validate(doc, RUN_SCHEMA))

    def test_bad_hash_pattern(self):
        doc = minimal_run()
        doc["artifacts"] = [{"phase": "INTAKE", "path": "x.md", "hash": "abc123",
                             "kind": "file", "registered_at": "2026-11-20"}]
        self.assertTrue(any("hash" in e for e in validate_kcr.validate(doc, RUN_SCHEMA)))

    def test_gate_passed_requires_human_approver(self):
        doc = minimal_run()
        doc["human_gate"] = {"gate": "G3", "status": "passed", "approver": None, "approved_at": None}
        errs = validate_kcr.semantic_errors(doc, "run-state")
        self.assertTrue(any("approver" in e for e in errs), errs)
        doc["human_gate"]["approver"] = "user"
        doc["human_gate"]["approved_at"] = "2026-11-20T18:00:00+08:00"
        self.assertEqual(validate_kcr.semantic_errors(doc, "run-state"), [])

    def test_publish_requires_passed_gate(self):
        doc = minimal_run()
        doc["phase"] = "PUBLISH"
        errs = validate_kcr.semantic_errors(doc, "run-state")
        self.assertTrue(any("PUBLISH" in e for e in errs), errs)
        doc["human_gate"] = {"gate": "G3", "status": "open", "approver": None, "approved_at": None}
        self.assertTrue(validate_kcr.semantic_errors(doc, "run-state"))

    def test_kcr_approved_requires_human_transition(self):
        doc = minimal_run()
        doc["kcr_substate"] = "APPROVED"
        errs = validate_kcr.semantic_errors(doc, "run-state")
        self.assertTrue(any("kcr_approved" in e for e in errs), errs)
        doc["transitions"].append({"at": "2026-11-20T18:00:00+08:00", "operator": "user",
                                   "action": "kcr_approved", "detail": "REVIEWING->APPROVED", "reason": ""})
        self.assertEqual(validate_kcr.semantic_errors(doc, "run-state"), [])

    def test_done_only_at_feedback(self):
        doc = minimal_run()
        doc["status"] = "done"
        self.assertTrue(any("FEEDBACK" in e for e in validate_kcr.semantic_errors(doc, "run-state")))

    def test_infer_schema_runstate(self):
        self.assertEqual(validate_kcr.infer_schema("run-state-RUN-x.json"), "run-state")
        self.assertEqual(validate_kcr.infer_schema("RUN-x.json"), None)  # 实例文件名需 --schema 指定


class MachineTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.runs = Path(self._td.name) / "runs"
        self.files = Path(self._td.name) / "files"
        self.approvals = Path(self._td.name) / "approvals"  # TASK 4 审批记录目录（临时）
        self.files.mkdir(parents=True)
        self.addCleanup(self._td.cleanup)

    def _file(self, name: str, content: str = "artifact") -> Path:
        f = self.files / name
        f.write_text(content, encoding="utf-8")
        return f

    def _new(self, run_id: str = "RUN-t", **kw) -> dict:
        return rs.new_run(self.runs, run_id, "qwenwork", **kw)

    def test_new_and_duplicate_rejected(self):
        self._new("RUN-dup")
        with self.assertRaises(rs.RunStateError):
            self._new("RUN-dup")
        with self.assertRaises(rs.RunStateError):
            rs.new_run(self.runs, "BAD-ID", "qwenwork")

    def test_full_happy_path_to_done(self):
        rid = "RUN-happy"
        self._new(rid, gate="G3", write_paths=["tools/course.json"])
        rs.start(self.runs, rid)
        for i, phase in enumerate(rs.PHASES):
            rs.add_artifact(self.runs, rid, str(self._file(f"p{i}.md", phase)))
            if phase == "REVIEW":
                with self.assertRaises(rs.RunStateError):
                    rs.advance(self.runs, rid)  # 人工门未过
                rs.pass_gate(self.runs, rid, approver="user")
                with self.assertRaises(rs.RunStateError) as cm:  # TASK 4：gate 过了但没有审批记录
                    rs.advance(self.runs, rid, approvals_dir=self.approvals)
                self.assertIn("审批证据链", str(cm.exception))
                approval_chain.record(self.runs, rid, "G3", "user", scope="全部阶段产物",
                                      root=self.files, approvals_dir=self.approvals)
            rs.advance(self.runs, rid, reason=f"{phase} 完成", approvals_dir=self.approvals)
        state = rs.load_run(self.runs, rid)
        self.assertEqual(state["status"], "done")
        self.assertEqual(state["phase"], "FEEDBACK")
        self.assertEqual(state["write_paths"], [])  # done 自动释放单写者
        self.assertEqual(len(state["artifacts"]), 10)
        self.assertTrue(all(r["status"] == "done" for r in state["phase_records"]))
        self.assertEqual(validate_kcr.validate(state, RUN_SCHEMA), [])
        self.assertEqual(validate_kcr.semantic_errors(state, "run-state"), [])

    def test_advance_requires_artifact(self):
        rid = "RUN-noart"
        self._new(rid)
        rs.start(self.runs, rid)
        with self.assertRaises(rs.RunStateError):
            rs.advance(self.runs, rid)
        self.assertEqual(rs.load_run(self.runs, rid)["phase"], "INTAKE")

    def test_gate_ai_cannot_pass(self):
        rid = "RUN-gate"
        self._new(rid, gate="G2")
        for bad in ("", "   ", None):
            with self.assertRaises(rs.RunStateError):
                rs.pass_gate(self.runs, rid, approver=bad)
        self.assertEqual(rs.load_run(self.runs, rid)["human_gate"]["status"], "open")
        rs.pass_gate(self.runs, rid, approver="user")
        with self.assertRaises(rs.RunStateError):
            rs.pass_gate(self.runs, rid, approver="user")  # 不重复批准

    def test_pause_resume_roundtrip(self):
        rid = "RUN-pause"
        self._new(rid)
        rs.start(self.runs, rid)
        rs.add_artifact(self.runs, rid, str(self._file("intake.md")))
        rs.advance(self.runs, rid)
        before = rs.load_run(self.runs, rid)["resume_point"]
        rs.pause(self.runs, rid, reason="人工暂停", operator="user")
        self.assertEqual(rs.load_run(self.runs, rid)["status"], "paused")
        with self.assertRaises(rs.RunStateError):
            rs.advance(self.runs, rid)  # paused 不能推进
        state = rs.resume(self.runs, rid)
        self.assertEqual(state["status"], "running")
        self.assertEqual(state["resume_point"], before)  # 断点恢复：续跑点不丢

    def test_fail_retry_counts(self):
        rid = "RUN-retry"
        self._new(rid)
        rs.start(self.runs, rid)
        with self.assertRaises(rs.RunStateError):
            rs.fail(self.runs, rid, reason="")  # 失败必须留原因
        rs.fail(self.runs, rid, reason="门禁 FAIL")
        state = rs.load_run(self.runs, rid)
        self.assertEqual(state["status"], "failed")
        self.assertEqual(state["phase_records"][0]["failure_reason"], "门禁 FAIL")
        rs.retry(self.runs, rid)
        rs.fail(self.runs, rid, reason="再次失败")
        state = rs.retry(self.runs, rid)
        self.assertEqual(state["status"], "running")
        self.assertEqual(state["phase_records"][0]["retry_count"], 2)
        self.assertIsNone(state["phase_records"][0]["failure_reason"])

    def test_artifact_idempotent_and_traceable(self):
        rid = "RUN-art"
        self._new(rid)
        f = self._file("same.md", "v1")
        rs.add_artifact(self.runs, rid, str(f))
        rs.add_artifact(self.runs, rid, str(f))  # 同 path+hash 幂等
        state = rs.load_run(self.runs, rid)
        self.assertEqual(len(state["artifacts"]), 1)
        self.assertEqual(len(state["artifacts"][0]["hash"]), 64)
        f.write_text("v2", encoding="utf-8")
        state = rs.add_artifact(self.runs, rid, str(f))  # 内容演进 → 新 hash 记录
        self.assertEqual(len(state["artifacts"]), 2)
        self.assertNotEqual(state["artifacts"][0]["hash"], state["artifacts"][1]["hash"])

    def test_artifact_future_phase_rejected(self):
        rid = "RUN-future"
        self._new(rid)
        with self.assertRaises(rs.RunStateError):
            rs.add_artifact(self.runs, rid, str(self._file("x.md")), phase="PUBLISH")

    def test_single_writer_conflict_and_release(self):
        self._new("RUN-A", write_paths=["tools/course.json"])
        rs.start(self.runs, "RUN-A")
        with self.assertRaises(rs.RunStateError):
            self._new("RUN-B", write_paths=["tools/course.json"])
        rs.pause(self.runs, "RUN-A", reason="暂停仍持有")
        with self.assertRaises(rs.RunStateError):
            self._new("RUN-B", write_paths=["tools/course.json"])
        rs.release_path(self.runs, "RUN-A", "tools/course.json")
        self._new("RUN-B", write_paths=["tools/course.json"])  # 释放后可持有
        with self.assertRaises(rs.RunStateError):
            rs.claim_path(self.runs, "RUN-A", "tools/course.json")  # B 活跃，A 抢不回

    def test_skip_human_only_forward(self):
        rid = "RUN-skip"
        self._new(rid, gate="G3")
        rs.start(self.runs, rid)
        with self.assertRaises(rs.RunStateError):
            rs.skip(self.runs, rid, "WRITE", approver="", reason="AI 想跳")
        with self.assertRaises(rs.RunStateError):
            rs.skip(self.runs, rid, "WRITE", approver="user", reason="")
        state = rs.skip(self.runs, rid, "WRITE", approver="user", reason="资料已备齐")
        self.assertEqual(state["phase"], "WRITE")
        self.assertEqual(state["phase_records"][0]["status"], "skipped")
        with self.assertRaises(rs.RunStateError):
            rs.skip(self.runs, rid, "INTAKE", approver="user", reason="回跳非法")
        with self.assertRaises(rs.RunStateError):
            rs.skip(self.runs, rid, "PUBLISH", approver="user", reason="门未过")

    def test_kcr_chain_order_and_human_approval(self):
        rid = "RUN-kcr"
        self._new(rid, kcr=True)
        rs.kcr_transition(self.runs, rid, "REVIEWING")
        with self.assertRaises(rs.RunStateError):
            rs.kcr_transition(self.runs, rid, "APPROVED")  # 无人工 approver
        with self.assertRaises(rs.RunStateError):
            rs.kcr_transition(self.runs, rid, "APPLIED")  # 顺序跳跃
        rs.kcr_transition(self.runs, rid, "APPROVED", approver="user")
        rs.kcr_transition(self.runs, rid, "APPLIED")
        state = rs.kcr_transition(self.runs, rid, "VERIFIED")
        self.assertEqual(state["kcr_substate"], "VERIFIED")
        self.assertTrue(any(t["action"] == "kcr_approved" and t["operator"] == "user"
                            for t in state["transitions"]))
        self.assertEqual(validate_kcr.semantic_errors(state, "run-state"), [])
        self._new("RUN-nokcr")
        with self.assertRaises(rs.RunStateError):
            rs.kcr_transition(self.runs, "RUN-nokcr", "REVIEWING")

    def test_persistence_reload(self):
        rid = "RUN-disk"
        self._new(rid, gate="G3")
        rs.start(self.runs, rid)
        rs.add_artifact(self.runs, rid, str(self._file("d.md")))
        on_disk = json.loads((self.runs / f"{rid}.json").read_text(encoding="utf-8"))
        self.assertEqual(on_disk, rs.load_run(self.runs, rid))  # 跨进程断点恢复的事实源
        self.assertEqual(validate_kcr.validate(on_disk, RUN_SCHEMA), [])

    def test_impact_artifact_invalid_rejected(self):
        rid = "RUN-badimpact"
        self._new(rid)
        bad = self._file("impact-bad.json", json.dumps({"trigger": {}}))
        with self.assertRaises(rs.RunStateError):
            rs.add_artifact(self.runs, rid, str(bad))
        self.assertEqual(rs.load_run(self.runs, rid)["artifacts"], [])  # 失败不登记

    def test_impact_artifact_real_replay(self):
        """真实数据回放：kcr_impact 分析 SRC-RN-COLORMGMT → 登记为 RESEARCH artifact → 推进。"""
        rid = "RUN-replay"
        self._new(rid)
        rs.start(self.runs, rid)
        rs.add_artifact(self.runs, rid, str(self._file("intake.md")))
        rs.advance(self.runs, rid)  # → RESEARCH
        g = kcr_impact.load_graph()
        report = kcr_impact.analyze(g, source_id="SRC-RN-COLORMGMT")
        self.assertEqual(validate_kcr.validate(report, validate_kcr.load_schema("impact-report")), [])
        f = self._file("impact-colormgmt.json", json.dumps(report, ensure_ascii=False))
        state = rs.add_artifact(self.runs, rid, str(f))  # 文件名自动推断 impact-report 并过契约
        self.assertEqual(state["artifacts"][-1]["kind"], "impact-report")
        state = rs.advance(self.runs, rid, reason="影响分析完成")
        self.assertEqual(state["phase"], "EVIDENCE")


class CliTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.runs = Path(self._td.name)
        self.addCleanup(self._td.cleanup)
        self.cli = [sys.executable, str(ROOT / "tools" / "run_state.py"), "--runs-dir", str(self.runs)]

    def _run(self, *args):
        return subprocess.run(self.cli + list(args), capture_output=True, text=True)

    def test_cli_new_show_list(self):
        p = self._run("new", "--run-id", "RUN-cli-1", "--owner", "qwenwork", "--gate", "G3")
        self.assertEqual(p.returncode, 0, p.stderr)
        p = self._run("show", "--run-id", "RUN-cli-1")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["phase"], "INTAKE")
        p = self._run("list")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("RUN-cli-1", p.stdout)

    def test_cli_duplicate_and_gate_guard(self):
        self._run("new", "--run-id", "RUN-cli-2", "--owner", "qwenwork", "--gate", "G3")
        p = self._run("new", "--run-id", "RUN-cli-2", "--owner", "qwenwork")
        self.assertEqual(p.returncode, 1)
        p = self._run("gate", "--run-id", "RUN-cli-2", "--pass")  # 无 approver
        self.assertEqual(p.returncode, 1)
        self.assertIn("approver", p.stderr)
        p = self._run("gate", "--run-id", "RUN-cli-2", "--pass", "--approver", "user")
        self.assertEqual(p.returncode, 0, p.stderr)
        p = self._run("show", "--run-id", "RUN-missing")
        self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)