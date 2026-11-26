#!/usr/bin/env python3
"""TASK 4 自测：审批证据链（approval-record 契约 + 登记 + 发布前复核 + 历史审批 + CLI）。

stdlib-only（D05 原则）。运行：py -3 tools/kcr/selftest_approval.py
覆盖：
- 契约：最小合法记录 / 缺字段 / 空 approver / 空 artifacts / 路径含 .. / record_id 不匹配 / 文件名推断
- 登记：无审批人拒绝 / 无范围拒绝 / 无产物拒绝 / 产物不存在拒绝 / 只增不改（-01、-02 并存）
- 复核：批准后文件变化 → 拦；还原 → 过；批准后新增范围内产物 → 拦；后续阶段产物不误伤
- 历史审批：gate passed 但无记录 → legacy-unverifiable（不补造）；记录被改坏 → 拦
- 与状态机联动：gate 已过仍进不了 PUBLISH；skip 到 PUBLISH 同样受限；有效记录后才放行
- git 信息：仓库内登记会记下提交号与未提交文件数（临时仓库，不触碰真实仓库）
- CLI 退出码
所有运行态、审批记录与临时 git 仓库都写在临时目录，不触碰真实 .agent/runs/ 与 reviews/approvals/。
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
import approval_chain as ac  # noqa: E402
import run_state as rs  # noqa: E402
from kcr import validate_kcr  # noqa: E402

SCHEMA = validate_kcr.load_schema("approval-record")


def minimal_record() -> dict:
    return {
        "schema_version": 1, "record_id": "RUN-x/G3-01", "run_id": "RUN-x", "gate_id": "G3",
        "approver": "user", "approved_at": "2026-11-25T18:00:00+08:00", "decision": "approved",
        "scope": "六课", "approved_at_phase": "REVIEW",
        "artifacts": [{"path": "courses/x/E01.md", "sha256": "0" * 64, "phase": "WRITE", "kind": "file"}],
        "commit": None, "dirty_files": None, "note": "",
    }


class SchemaTests(unittest.TestCase):
    def test_minimal_valid(self):
        self.assertEqual(validate_kcr.validate(minimal_record(), SCHEMA), [])
        self.assertEqual(validate_kcr.semantic_errors(minimal_record(), "approval-record"), [])

    def test_schema_rejections(self):
        doc = minimal_record(); del doc["scope"]
        self.assertTrue(any("scope" in e for e in validate_kcr.validate(doc, SCHEMA)))
        doc = minimal_record(); doc["gate_id"] = "G9"
        self.assertTrue(validate_kcr.validate(doc, SCHEMA))
        doc = minimal_record(); doc["artifacts"] = []
        self.assertTrue(any("minItems" in e for e in validate_kcr.validate(doc, SCHEMA)))
        doc = minimal_record(); doc["artifacts"][0]["sha256"] = "abc"
        self.assertTrue(validate_kcr.validate(doc, SCHEMA))
        doc = minimal_record(); doc["record_id"] = "G3-01"
        self.assertTrue(validate_kcr.validate(doc, SCHEMA))

    def test_semantic_rejections(self):
        for mutate in (
            lambda d: d.update(approver="   "),
            lambda d: d.update(approved_at=""),
            lambda d: d.update(artifacts=[]),
            lambda d: d["artifacts"][0].update(path="../../etc/passwd"),
            lambda d: d.update(record_id="RUN-y/G3-01"),
        ):
            doc = minimal_record(); mutate(doc)
            self.assertTrue(validate_kcr.semantic_errors(doc, "approval-record"), doc)

    def test_infer_schema(self):
        self.assertEqual(validate_kcr.infer_schema("approval-record-x.json"), "approval-record")
        self.assertIsNone(validate_kcr.infer_schema("G3-01.json"))  # 需 --schema 指定


class ChainTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        base = Path(self._td.name)
        self.runs, self.files, self.approvals = base / "runs", base / "files", base / "approvals"
        self.files.mkdir()
        self.addCleanup(self._td.cleanup)
        self.a = self.files / "lesson.md"
        self.a.write_text("v1", encoding="utf-8")

    def _run_to_review(self, rid: str = "RUN-c") -> str:
        rs.new_run(self.runs, rid, "qwenwork", gate="G3")
        rs.start(self.runs, rid)
        for i, phase in enumerate(rs.PHASES[:rs.PHASES.index("REVIEW") + 1]):
            f = self.files / f"p{i}.md"
            f.write_text(phase, encoding="utf-8")
            rs.add_artifact(self.runs, rid, str(f))
            if phase != "REVIEW":
                rs.advance(self.runs, rid)
        rs.pass_gate(self.runs, rid, approver="user")
        return rid

    def _record(self, rid: str, **kw):
        kw.setdefault("root", self.files)
        kw.setdefault("approvals_dir", self.approvals)
        kw.setdefault("scope", "全部产物")
        return ac.record(self.runs, rid, "G3", "user", **kw)

    def test_record_guards(self):
        rid = self._run_to_review()
        for bad in ("", "   "):
            with self.assertRaises(ac.ApprovalError):
                ac.record(self.runs, rid, "G3", bad, scope="x", root=self.files, approvals_dir=self.approvals)
        with self.assertRaises(ac.ApprovalError):
            self._record(rid, scope="  ")
        with self.assertRaises(ac.ApprovalError):
            self._record(rid, decision="maybe")
        rs.new_run(self.runs, "RUN-empty", "qwenwork")
        with self.assertRaises(ac.ApprovalError):  # 没有产物 = 没有可批准的文件版本
            ac.record(self.runs, "RUN-empty", "G3", "user", scope="x", root=self.files, approvals_dir=self.approvals)
        moved = self.files / "p0.md.bak"; (self.files / "p0.md").rename(moved)  # 批准时的产物不在了
        with self.assertRaises(ac.ApprovalError):
            self._record(rid)
        moved.rename(self.files / "p0.md")

    def test_record_append_only_and_verify_ok(self):
        rid = self._run_to_review()
        r1 = self._record(rid, note="第一次")
        self.assertEqual(r1["record_id"], f"{rid}/G3-01")
        self.assertEqual(len(r1["artifacts"]), 8)  # INTAKE…REVIEW 各 1 个
        status, problems, used = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertEqual((status, problems, used["record_id"]), ("ok", [], r1["record_id"]))
        # 改一个不在批准范围内的文件：复核放行（范围外的文件不受本次批准约束）
        self.a.write_text("范围外的改动", encoding="utf-8")
        self.assertEqual(ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)[0], "ok")
        r2 = self._record(rid, note="重新批准")
        self.assertEqual(r2["record_id"], f"{rid}/G3-02")
        self.assertTrue((self.approvals / rid / "G3-01.json").is_file())  # 旧记录原样保留
        first = json.loads((self.approvals / rid / "G3-01.json").read_text(encoding="utf-8"))
        self.assertEqual(first["note"], "第一次")
        self.assertEqual(ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)[2]["record_id"],
                         r2["record_id"])  # 复核以最新记录为准

    def test_verify_blocks_change_then_recovers(self):
        rid = self._run_to_review()
        self._record(rid)
        target = self.files / "p7.md"  # 已登记的 REVIEW 阶段产物
        original = target.read_text(encoding="utf-8")
        target.write_text("v2", encoding="utf-8")  # 批准后被改
        status, problems, _ = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertEqual(status, "failed")
        self.assertTrue(any("已变化" in p for p in problems), problems)
        target.write_text(original, encoding="utf-8")  # 逐字节还原
        self.assertEqual(ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)[0], "ok")
        hidden = self.files / "p7.hidden"
        target.rename(hidden)  # 批准时的产物被移走
        status, problems, _ = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertTrue(any("不存在" in p for p in problems))
        hidden.rename(target)

    def test_verify_blocks_out_of_scope_artifact(self):
        rid = self._run_to_review()
        self._record(rid)
        extra = self.files / "late.md"
        extra.write_text("批准后才登记", encoding="utf-8")
        rs.add_artifact(self.runs, rid, str(extra))  # 仍在 REVIEW 阶段 → 超出审批范围
        status, problems, _ = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertEqual(status, "failed")
        self.assertTrue(any("不在审批范围内" in p for p in problems), problems)
        self._record(rid)  # 重新批准后放行
        self.assertEqual(ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)[0], "ok")

    def test_later_phase_artifact_not_flagged(self):
        rid = self._run_to_review()
        self._record(rid)
        rs.advance(self.runs, rid, approvals_dir=self.approvals)  # REVIEW → PUBLISH
        pub = self.files / "publish-record.md"
        pub.write_text("发布记录", encoding="utf-8")
        rs.add_artifact(self.runs, rid, str(pub))  # PUBLISH 阶段产物：批准之后才可能产生，不误伤
        self.assertEqual(ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)[0], "ok")
        rs.advance(self.runs, rid, approvals_dir=self.approvals)  # PUBLISH → FEEDBACK

    def test_machine_blocks_publish_without_or_with_stale_record(self):
        rid = self._run_to_review()
        with self.assertRaises(rs.RunStateError) as cm:  # gate 已 passed，但没有审批记录
            rs.advance(self.runs, rid, approvals_dir=self.approvals)
        self.assertIn("审批证据链", str(cm.exception))
        with self.assertRaises(rs.RunStateError):  # 人工 skip 也绕不过
            rs.skip(self.runs, rid, "PUBLISH", approver="user", reason="想跳", approvals_dir=self.approvals)
        self._record(rid)
        target = self.files / "p7.md"
        original = target.read_text(encoding="utf-8")
        target.write_text("changed", encoding="utf-8")
        with self.assertRaises(rs.RunStateError) as cm:  # 批准后文件变化
            rs.advance(self.runs, rid, approvals_dir=self.approvals)
        self.assertIn("已变化", str(cm.exception))
        target.write_text(original, encoding="utf-8")
        state = rs.advance(self.runs, rid, approvals_dir=self.approvals)
        self.assertEqual(state["phase"], "PUBLISH")

    def test_legacy_unverifiable_not_fabricated(self):
        rid = self._run_to_review()
        status, problems, used = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertEqual(status, "legacy-unverifiable")
        self.assertIsNone(used)
        self.assertTrue(any("legacy" in p for p in problems))
        self.assertFalse((self.approvals / rid).exists())  # 不补造任何记录

    def test_tampered_record_rejected(self):
        rid = self._run_to_review()
        self._record(rid)
        f = self.approvals / rid / "G3-01.json"
        doc = json.loads(f.read_text(encoding="utf-8"))
        doc["approver"] = ""
        f.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        status, problems, _ = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertEqual(status, "failed")
        self.assertTrue(any("契约校验" in p for p in problems), problems)

    def test_extra_paths_and_rejected_decision(self):
        rid = self._run_to_review()
        extra = self.files / "course.json"
        extra.write_text("{}", encoding="utf-8")
        with self.assertRaises(ac.ApprovalError):
            self._record(rid, extra_paths=("missing.json",))
        rec = self._record(rid, extra_paths=(str(extra),))
        self.assertIn(str(extra).replace("\\", "/"), {e["path"] for e in rec["artifacts"]})
        rec = self._record(rid, decision="rejected")
        self.assertEqual(rec["decision"], "rejected")
        status, problems, _ = ac.verify(self.runs, rid, root=self.files, approvals_dir=self.approvals)
        self.assertTrue(any("不是批准" in p for p in problems))

    def test_git_info_captured_in_temp_repo(self):
        repo = self.files / "repo"
        (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "a.md").write_text("x", encoding="utf-8")
        g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=repo,
                                      capture_output=True, text=True)
        g("init", "-q")
        g("add", "-A"); self.assertEqual(g("commit", "-q", "-m", "init").returncode, 0)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
        rid = "RUN-git"
        rs.new_run(self.runs, rid, "qwenwork", gate="G3")
        rs.start(self.runs, rid)
        rs.add_artifact(self.runs, rid, str(repo / "docs" / "a.md"))
        rec = ac.record(self.runs, rid, "G3", "user", scope="a", root=repo, approvals_dir=self.approvals)
        self.assertEqual((rec["commit"], rec["dirty_files"]), (head, 0))
        (repo / "docs" / "b.md").write_text("y", encoding="utf-8")
        rec = ac.record(self.runs, rid, "G3", "user", scope="a", root=repo, approvals_dir=self.approvals)
        self.assertEqual(rec["dirty_files"], 1)  # 如实记下批准时工作树不干净


class CliTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        base = Path(self._td.name)
        self.runs, self.files, self.approvals = base / "runs", base / "files", base / "approvals"
        self.files.mkdir()
        self.addCleanup(self._td.cleanup)
        self.cli = [sys.executable, str(ROOT / "tools" / "approval_chain.py"),
                    "--runs-dir", str(self.runs), "--approvals-dir", str(self.approvals)]

    def _run(self, *args):
        return subprocess.run(self.cli + list(args), capture_output=True, text=True, encoding="utf-8", errors="replace")

    def test_cli_record_verify_show(self):
        rid = "RUN-cli"
        rs.new_run(self.runs, rid, "qwenwork", gate="G3")
        rs.start(self.runs, rid)
        f = self.files / "a.md"; f.write_text("x", encoding="utf-8")
        rs.add_artifact(self.runs, rid, str(f))
        rs.pass_gate(self.runs, rid, approver="user")
        p = self._run("record", "--run-id", rid, "--gate", "G3", "--scope", "a")  # 无 approver
        self.assertEqual(p.returncode, 2)  # argparse：--approver 必填
        p = self._run("record", "--run-id", rid, "--gate", "G3", "--approver", " ", "--scope", "a")
        self.assertEqual(p.returncode, 1); self.assertIn("approver", p.stderr)
        p = self._run("verify", "--run-id", rid)
        self.assertEqual(p.returncode, 1); self.assertIn("legacy-unverifiable", p.stdout)
        p = self._run("record", "--run-id", rid, "--gate", "G3", "--approver", "user", "--scope", "a")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(f"{rid}/G3-01", p.stdout)
        p = self._run("verify", "--run-id", rid)
        self.assertEqual(p.returncode, 0, p.stderr); self.assertIn('"ok"', p.stdout)
        p = self._run("show", "--run-id", rid)
        self.assertEqual(p.returncode, 0, p.stderr); self.assertIn("user", p.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
