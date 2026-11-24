#!/usr/bin/env python3
"""P8 片一+片二自测：kcr_impact 输出 ↔ impact-report.schema.json 对齐 + 真实回放 + 程序化校验器。

stdlib-only（D05 原则）。运行：py -3 tools/kcr/selftest_impact.py
回放样本依据：D17/D18（V14 verified、K-STRIDE 改挂 V14、L01-Q2 挂 V14）；
L03 新写登记 V21–V24（SRC-RN-COLORMGMT，2026-11-20）。
片二（2026-11-20）：validate_kcr 全量校验接入 assert_shape；ValidatorTests 覆盖
三 schema 正反用例、文档化硬规则（semantic_errors）、真实样本回放与 CLI。
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import kcr_impact  # noqa: E402
from kcr import validate_kcr  # noqa: E402

REQUIRED = ["trigger", "new_sources", "affected", "conflicts", "uncovered"]
AFFECTED_REQUIRED = ["claims", "concepts", "lessons", "quizzes", "courses"]
TRIGGER_TYPES = {"new_research_report", "new_source", "source_update", "lesson_revision", "claim_status_request"}
RELATIONS = {"supports", "conflicts", "extends"}

IMPACT_SCHEMA = validate_kcr.load_schema("impact-report")

MINIMAL_IMPACT = {
    "trigger": {"type": "new_source", "ref": "SRC-X", "date": "2026-11-20"},
    "new_sources": [],
    "affected": {"claims": [], "concepts": [], "lessons": [], "quizzes": [], "courses": []},
    "conflicts": [],
    "uncovered": [],
}
MINIMAL_PROPOSAL = {
    "proposal_id": "KCR-2026-11-001",
    "impact_report": "reviews/kcr/impact-v14-replay.json",
    "items": [{
        "item_id": "I1", "action": "add",
        "target": {"layer": "claim", "id_draft": "V99"},
        "evidence": "SRC-X §1", "affected": {},
        "rationale": "测试", "version_note": "v1",
    }],
    "ai_recommendation": "仅供参考",
    "human_decision": None,
}
MINIMAL_DECISION = {
    "proposal_id": "KCR-2026-11-001",
    "reviewer": "user", "date": "2026-11-20",
    "decisions": [{"item_id": "I1", "verdict": "approve"}],
    "overall": "同意",
}
REAL_SAMPLES = ["impact-l09-p07.json", "impact-v14-replay.json", "impact-colormgmt-replay.json"]


class SchemaShape(unittest.TestCase):
    def assert_shape(self, r: dict) -> None:
        for k in REQUIRED:
            self.assertIn(k, r, f"缺契约顶层字段 {k}")
        for k in ("type", "ref", "date"):
            self.assertIn(k, r["trigger"])
        self.assertIn(r["trigger"]["type"], TRIGGER_TYPES)
        self.assertIsInstance(r["new_sources"], list)
        for k in AFFECTED_REQUIRED:
            self.assertIn(k, r["affected"])
        self.assertNotIn("website", r["affected"], "website 不得混入契约 affected")
        for c in r["affected"]["claims"]:
            self.assertIn("id", c)
            self.assertIn(c["relation"], RELATIONS)
        for k in ("concepts", "lessons", "quizzes"):
            for x in r["affected"][k]:
                self.assertIn("id", x)
        for c in r["affected"]["courses"]:
            self.assertIn("id", c)
        self.assertIsInstance(r["conflicts"], list)
        self.assertIsInstance(r["uncovered"], list)
        for u in r["uncovered"]:
            self.assertIsInstance(u, str)
        # 片二：全量程序化 schema 校验（required/type/enum/pattern/minItems）
        self.assertEqual(validate_kcr.validate(r, IMPACT_SCHEMA), [], "impact-report 契约校验未通过")


class ReplayTests(SchemaShape):
    @classmethod
    def setUpClass(cls):
        cls.g = kcr_impact.load_graph()

    def test_source_colormgmt_replay(self):
        """L03 登记过程回放：SRC-RN-COLORMGMT → V21–V24 → L03（无 quiz）。
        注：该来源后续也支撑 L14 的 V47/V48（2026-11-20），故用子集断言而非全等。"""
        r = kcr_impact.analyze(self.g, source_id="SRC-RN-COLORMGMT")
        self.assert_shape(r)
        ids = [c["id"] for c in r["affected"]["claims"]]
        self.assertTrue({"V21", "V22", "V23", "V24"} <= set(ids), ids)
        self.assertIn("L03", [l["id"] for l in r["affected"]["lessons"]])
        self.assertEqual(r["affected"]["quizzes"], [])
        self.assertTrue(all(c["relation"] == "supports" for c in r["affected"]["claims"]))
        self.assertEqual(r["uncovered"], [])

    def test_claim_v14_replay(self):
        """V14（D18 升级 verified）：K-STRIDE 概念 / L01 / L01-Q2 / 两层 course。"""
        r = kcr_impact.analyze(self.g, claim_id="V14")
        self.assert_shape(r)
        self.assertEqual([c["id"] for c in r["affected"]["claims"]], ["V14"])
        self.assertIn("K-STRIDE", [c["id"] for c in r["affected"]["concepts"]])
        self.assertIn("L01", [l["id"] for l in r["affected"]["lessons"]])
        self.assertIn("L01#L01-Q2", [q["id"] for q in r["affected"]["quizzes"]])
        self.assertEqual(len(r["affected"]["courses"]), 2)
        self.assertFalse(any(f["type"] == "unverified_claim_in_chain" for f in r["integrity_findings"]))

    def test_unverified_claim_finding(self):
        """V21（open）在链中 → integrity_findings 如实标注，不冒充契约 conflicts。"""
        r = kcr_impact.analyze(self.g, claim_id="V21")
        self.assert_shape(r)
        self.assertEqual(r["conflicts"], [])
        self.assertTrue(any(f["type"] == "unverified_claim_in_chain" and f["claim"] == "V21"
                            for f in r["integrity_findings"]))

    def test_draft_cli_schema(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "draft.json"
            p = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "kcr_impact.py"),
                 "--claim-draft", "RGBA 中间纹理的 loadOp=LOAD 在 TBDR 上代价高，应使用 CLEAR/DONT_CARE",
                 "--out", str(out)],
                capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            r = json.loads(out.read_text(encoding="utf-8"))
            self.assert_shape(r)
            self.assertEqual(r["trigger"]["type"], "claim_status_request")
            self.assertEqual(r["affected"]["claims"], [])
            self.assertIn("claim_draft_echo", r)
            self.assertTrue(r["read_only"])

    def test_unknown_seed_errors(self):
        r = kcr_impact.analyze(self.g, claim_id="V99")
        self.assertIn("error", r)


class ValidatorTests(unittest.TestCase):
    """片二：validate_kcr 正反用例 + 硬规则 + 真实样本 + CLI。"""

    def test_minimal_valid_all_three(self):
        for name, doc in (("impact-report", MINIMAL_IMPACT),
                          ("change-proposal", MINIMAL_PROPOSAL),
                          ("review-decision", MINIMAL_DECISION)):
            self.assertEqual(validate_kcr.validate(doc, validate_kcr.load_schema(name)), [], name)
            self.assertEqual(validate_kcr.semantic_errors(doc, name, stage2=True), [], name)

    def test_missing_required(self):
        doc = copy.deepcopy(MINIMAL_IMPACT)
        del doc["trigger"]["date"]
        errs = validate_kcr.validate(doc, IMPACT_SCHEMA)
        self.assertTrue(any("date" in e for e in errs), errs)

    def test_bad_enum(self):
        doc = copy.deepcopy(MINIMAL_IMPACT)
        doc["trigger"]["type"] = "unknown_mode"
        self.assertTrue(validate_kcr.validate(doc, IMPACT_SCHEMA))

    def test_bad_pattern(self):
        doc = copy.deepcopy(MINIMAL_PROPOSAL)
        doc["proposal_id"] = "KCR-26-11-1"  # 不匹配 ^KCR-\d{4}-\d{2}-\d{3}$
        self.assertTrue(validate_kcr.validate(doc, validate_kcr.load_schema("change-proposal")))
        doc2 = copy.deepcopy(MINIMAL_IMPACT)
        doc2["new_sources"] = [{"id": "REF-1", "url": "https://x", "type": "spec"}]  # id 不匹配 ^SRC-
        self.assertTrue(validate_kcr.validate(doc2, IMPACT_SCHEMA))

    def test_min_items(self):
        doc = copy.deepcopy(MINIMAL_PROPOSAL)
        doc["items"] = []
        self.assertTrue(validate_kcr.validate(doc, validate_kcr.load_schema("change-proposal")))
        doc2 = copy.deepcopy(MINIMAL_DECISION)
        doc2["decisions"] = []
        self.assertTrue(validate_kcr.validate(doc2, validate_kcr.load_schema("review-decision")))

    def test_type_union_null(self):
        schema = validate_kcr.load_schema("change-proposal")
        doc = copy.deepcopy(MINIMAL_PROPOSAL)
        doc["human_decision"] = {"reviewer": "user", "date": "2026-11-20", "decisions": [], "overall": "ok"}
        self.assertEqual(validate_kcr.validate(doc, schema), [])  # object 合法（Stage 3 回填后）
        doc["human_decision"] = "approved"  # string 非法
        self.assertTrue(validate_kcr.validate(doc, schema))

    def test_semantic_modify_requires_id(self):
        doc = copy.deepcopy(MINIMAL_PROPOSAL)
        doc["items"][0]["action"] = "deprecate"  # 无 target.id
        errs = validate_kcr.semantic_errors(doc, "change-proposal")
        self.assertTrue(any("target.id" in e for e in errs), errs)
        doc["items"][0]["target"]["id"] = "V14"
        self.assertEqual(validate_kcr.semantic_errors(doc, "change-proposal"), [])

    def test_stage2_human_decision_must_be_null(self):
        doc = copy.deepcopy(MINIMAL_PROPOSAL)
        doc["human_decision"] = {"reviewer": "ai", "date": "2026-11-20", "decisions": [], "overall": "预填"}
        errs = validate_kcr.semantic_errors(doc, "change-proposal", stage2=True)
        self.assertTrue(any("human_decision" in e for e in errs), errs)
        self.assertEqual(validate_kcr.semantic_errors(doc, "change-proposal", stage2=False), [])

    def test_unknown_keyword_guard(self):
        with self.assertRaises(ValueError):
            validate_kcr.validate({}, {"allOf": []})

    def test_real_samples_replay(self):
        for name in REAL_SAMPLES:
            doc = json.loads((ROOT / "reviews" / "kcr" / name).read_text(encoding="utf-8"))
            self.assertEqual(validate_kcr.validate(doc, IMPACT_SCHEMA), [], name)

    def test_cli_ok_and_fail(self):
        sample = ROOT / "reviews" / "kcr" / "impact-v14-replay.json"
        p = subprocess.run([sys.executable, str(ROOT / "tools" / "kcr" / "validate_kcr.py"), str(sample)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "impact-bad.json"
            bad.write_text(json.dumps({"trigger": {}}), encoding="utf-8")
            p2 = subprocess.run([sys.executable, str(ROOT / "tools" / "kcr" / "validate_kcr.py"), str(bad)],
                                capture_output=True, text=True)
            self.assertEqual(p2.returncode, 1, p2.stdout + p2.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)