#!/usr/bin/env python3
"""发布边界 v2 回归测试（2026-11-24，用户批准的学习站发布政策；advisory 模式已废除）。

覆盖（夹具在临时目录中构造注册表与磁盘，不触碰真实课程内容）：
  A. 判定：未登记 Markdown / courses 内伪装教材的内部材料 / evidence 未授权提取记录 /
     knowledge-model 未审核中间模型 / excluded-internal / archive 非注册文件 → 一律拒绝
  B. fail closed：注册表缺失、JSON 损坏、Schema 错误、未知 policy、advisory、通配符、
     重复路径、大小写冲突、excluded-internal 无原因、offline-read-only 越出 archive
  C. 路径安全：`..`、绝对路径、盘符、反斜杠、通配、符号链接逃逸
  D. Build 行为：注册表/磁盘不一致 → 非零退出且不留下半成品；一致 → 原子替换
  E. 真实产物：bundle docs == 注册表 offline 集合；内部文件 0 泄露；archive 19/19；
     VitePress 在线树只含 online 资产且无 archive；旧 API 已移除

用法：py -3 tools/test_publish_boundary.py （E 组需先跑 build_site.py / build_vitepress_content.py）
"""

from __future__ import annotations

import inspect
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import publish_boundary as pb  # noqa: E402

REGISTRY_PATH = ROOT / "tools" / "publish-allowlist.json"

BASE_POLICIES = {
    "public": {"nav": True, "search": True, "online": "allowed"},
    "offline-read-only": {"nav": True, "search": False, "online": "forbidden"},
    "curated-data": {"nav": False, "search": False, "online": "allowed"},
    "site-data": {"nav": False, "search": False, "online": "allowed"},
    "excluded-internal": {"nav": False, "search": False, "online": "forbidden"},
}


def make_registry(assets, **overrides):
    doc = {
        "doc_id": "publish-allowlist",
        "version": 2,
        "policy": "enforce",
        "default": "deny",
        "policies": json.loads(json.dumps(BASE_POLICIES)),
        "assets": assets,
    }
    doc.update(overrides)
    return doc


def validate(doc):
    """直接走 Schema 校验（不触盘）。"""
    return pb._validate_registry(json.loads(json.dumps(doc)), REGISTRY_PATH)


class DecisionTests(unittest.TestCase):
    """A + 部分 B/C：纯判定逻辑。"""

    def setUp(self):
        self.reg = validate(make_registry([
            {"path": "README.md", "policy": "public"},
            {"path": "courses/journey/lessons/L01.md", "policy": "public"},
            {"path": "docs/USER-GUIDE.md", "policy": "public"},
            {"path": "docs/internal-plan.md", "policy": "excluded-internal", "reason": "内部计划"},
            {"path": "archive/old.md", "policy": "offline-read-only"},
            {"path": "evidence/source-registry.json", "policy": "curated-data"},
            {"path": "evidence/claim-ledger.json", "policy": "excluded-internal", "reason": "含未审核断言"},
            {"path": "knowledge-model/concepts.json", "policy": "curated-data"},
            {"path": "tools/glossary.json", "policy": "site-data"},
        ]))

    def test_unregistered_markdown_denied(self):
        for rel in ("01-基础理论/新文档.md", "notes/scratch.md"):
            self.assertIsNone(pb.policy_for(rel, self.reg))
            self.assertFalse(pb.is_publishable(rel, target="offline", registry=self.reg))
            self.assertFalse(pb.is_publishable(rel, target="online", registry=self.reg))
            with self.assertRaises(pb.RegistryError):
                pb.require_publishable(rel, target="offline", registry=self.reg)

    def test_internal_review_material_disguised_in_courses_denied(self):
        # courses/ 下未登记的"教材"——默认拒绝，父目录里有 public 教材也不会被目录规则放行。
        rel = "courses/journey/lessons/内部审核材料.md"
        self.assertFalse(pb.is_publishable(rel, target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("courses/journey/review-report.md", target="offline", registry=self.reg))
        # 即使登记为 excluded-internal，仍不可发布
        self.assertFalse(pb.is_publishable("docs/internal-plan.md", target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("docs/internal-plan.md", target="online", registry=self.reg))
        with self.assertRaises(pb.RegistryError):
            pb.require_publishable("docs/internal-plan.md", target="offline", registry=self.reg)

    def test_unauthorized_evidence_extraction_record_denied(self):
        self.assertFalse(pb.is_publishable("evidence/internal-extraction.md", target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("evidence/ research-log.json", target="offline", registry=self.reg))
        # 含未审核断言的台账：既不是文档，也不能作为数据嵌入
        self.assertFalse(pb.is_publishable("evidence/claim-ledger.json", target="offline", registry=self.reg))
        with self.assertRaises(pb.RegistryError):
            pb.require_site_data("evidence/claim-ledger.json", registry=self.reg)

    def test_unreviewed_knowledge_model_intermediate_denied(self):
        self.assertFalse(pb.is_publishable("knowledge-model/agent-state.json", target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("knowledge-model/dump.md", target="online", registry=self.reg))
        with self.assertRaises(pb.RegistryError):
            pb.require_site_data("knowledge-model/agent-state.json", registry=self.reg)

    def test_excluded_internal_overrides_any_allow(self):
        for target in pb.TARGETS:
            self.assertFalse(pb.allows_target("excluded-internal", target), target)
            self.assertFalse(pb.allows_target(None, target), target)  # 默认拒绝

    def test_archive_unregistered_file_denied_and_registered_read_only(self):
        self.assertFalse(pb.is_publishable("archive/未登记.md", target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("archive/未登记.md", target="online", registry=self.reg))
        self.assertTrue(pb.is_publishable("archive/old.md", target="offline", registry=self.reg))
        self.assertFalse(pb.is_publishable("archive/old.md", target="online", registry=self.reg), "D10.4：archive 不得自动进入在线站")

    def test_registered_assets_publish_as_expected(self):
        for rel in ("README.md", "courses/journey/lessons/L01.md", "docs/USER-GUIDE.md"):
            self.assertTrue(pb.is_publishable(rel, target="offline", registry=self.reg), rel)
            self.assertTrue(pb.is_publishable(rel, target="online", registry=self.reg), rel)
        self.assertEqual(pb.require_publishable("README.md", target="offline", registry=self.reg), "public")
        self.assertEqual(pb.require_site_data("tools/glossary.json", registry=self.reg), "site-data")
        self.assertEqual(pb.require_site_data("evidence/source-registry.json", registry=self.reg), "curated-data")
        # 文档不能当数据嵌入，数据不能当文档发布
        with self.assertRaises(pb.RegistryError):
            pb.require_site_data("README.md", registry=self.reg)
        self.assertFalse(pb.is_publishable("tools/glossary.json", target="offline", registry=self.reg))


class FailClosedTests(unittest.TestCase):
    """B：注册表缺失/损坏/不合规。"""

    def write(self, tmp, text):
        path = Path(tmp) / "publish-allowlist.json"
        path.write_text(text, encoding="utf-8")
        return path

    def test_registry_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(pb.RegistryError):
                pb.load_registry(Path(tmp) / "missing.json")

    def test_registry_corrupt_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "{not json")
            with self.assertRaises(pb.RegistryError):
                pb.load_registry(path)

    def test_schema_errors(self):
        bad = {
            "version 1": make_registry([{"path": "a.md", "policy": "public"}], version=1),
            "advisory policy": make_registry([{"path": "a.md", "policy": "public"}], policy="advisory"),
            "default allow": make_registry([{"path": "a.md", "policy": "public"}], default="allow"),
            "unknown policy": make_registry([{"path": "a.md", "policy": "whatever"}]),
            "wildcard path": make_registry([{"path": "docs/*.md", "policy": "public"}]),
            "directory glob": make_registry([{"path": "docs/**", "policy": "public"}]),
            "duplicate path": make_registry([{"path": "a.md", "policy": "public"}, {"path": "a.md", "policy": "public"}]),
            "case conflict": make_registry([{"path": "A.md", "policy": "public"}, {"path": "a.md", "policy": "public"}]),
            "excluded without reason": make_registry([{"path": "a.md", "policy": "excluded-internal"}]),
            "read-only outside archive": make_registry([{"path": "docs/x.md", "policy": "offline-read-only"}]),
            "missing asset fields": make_registry([{"policy": "public"}]),
            "empty assets": make_registry([]),
            "policies altered": make_registry([{"path": "a.md", "policy": "public"}], policies={"public": {}}),
            "archive online opened": make_registry([{"path": "archive/a.md", "policy": "offline-read-only"}], policies={
                **BASE_POLICIES, "offline-read-only": {"online": "allowed"}}),
        }
        for name, doc in bad.items():
            with self.subTest(name), self.assertRaises(pb.RegistryError):
                validate(doc)

    def test_advisory_never_falls_back(self):
        # 未知 policy 不得回退到 advisory：is_publishable 在注册表不合规时抛错而非返回 True。
        with tempfile.TemporaryDirectory() as tmp:
            self.write(tmp, json.dumps(make_registry([{"path": "a.md", "policy": "public"}], policy="advisory")))
            old = pb.ALLOWLIST_PATH
            pb.ALLOWLIST_PATH = Path(tmp) / "publish-allowlist.json"
            try:
                with self.assertRaises(pb.RegistryError):
                    pb.is_publishable("a.md", target="offline")
            finally:
                pb.ALLOWLIST_PATH = old


class PathSafetyTests(unittest.TestCase):
    """C：路径穿越 / 绝对路径 / 符号链接逃逸。"""

    def test_traversal_and_absolute_rejected(self):
        for bad in ("../x.md", "a/../../x.md", "a/../b.md", "./a.md", "a/./b.md", "a//b.md", "a/",
                    "/etc/passwd", "C:/x.md", "a\\b.md", "a/*.md", "a/[x].md", "", "x\x00y"):
            with self.subTest(bad), self.assertRaises(pb.RegistryError):
                pb.normalize_rel(bad)
        self.assertEqual(pb.normalize_rel("a/b/c.md"), "a/b/c.md")
        self.assertEqual(pb.normalize_rel("a.md"), "a.md")

    def test_traversal_cannot_reach_registry(self):
        reg = validate(make_registry([{"path": "a.md", "policy": "public"}]))
        # 即便规范化后恰好命中已登记资产，非规范输入也必须拒绝（不可信路径不解释）。
        for sneaky in ("tools/../a.md", "./a.md", "x/./../a.md"):
            with self.subTest(sneaky), self.assertRaises(pb.RegistryError):
                pb.policy_for(sneaky, reg)
        with self.assertRaises(pb.RegistryError):
            pb.is_publishable("../../outside.md", target="offline", registry=reg)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp_in, tempfile.TemporaryDirectory() as tmp_out:
            inside = Path(tmp_in) / "repo"
            (inside / "docs").mkdir(parents=True)
            (inside / "docs" / "ok.md").write_text("ok", encoding="utf-8")
            outside = Path(tmp_out) / "secret.md"
            outside.write_text("secret", encoding="utf-8")
            link = inside / "docs" / "escape.md"
            try:
                os.symlink(outside, link)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"当前系统不允许创建符号链接，跳过实链接用例: {exc}")
            # 解析后越出仓库根 → 拒绝
            with self.assertRaises(pb.RegistryError):
                pb.safe_relpath(link, inside)
            with self.assertRaises(pb.RegistryError):
                pb.scan_assets(inside)

    def test_containment_without_symlink_privilege(self):
        # 不依赖符号链接权限：仓库外文件直接按根解析也必须被拒。
        with tempfile.TemporaryDirectory() as tmp_in, tempfile.TemporaryDirectory() as tmp_out:
            inside = Path(tmp_in) / "repo"
            inside.mkdir()
            outside = Path(tmp_out) / "secret.md"
            outside.write_text("secret", encoding="utf-8")
            with self.assertRaises(pb.RegistryError):
                pb.safe_relpath(outside, inside)
            (inside / "a.md").write_text("x", encoding="utf-8")
            self.assertEqual(pb.safe_relpath(inside / "a.md", inside), "a.md")


class BuildBehaviorTests(unittest.TestCase):
    """D：build_site 在注册表/磁盘不一致时 fail closed，且不留下半成品。"""

    def make_root(self, tmp, registry_assets, extra_files=()):
        root = Path(tmp) / "repo"
        (root / "tools").mkdir(parents=True)
        (root / "tools" / "publish-allowlist.json").write_text(
            json.dumps(make_registry(registry_assets), ensure_ascii=False), encoding="utf-8")
        (root / "tools" / "glossary.json").write_text(json.dumps({"groups": [{"id": "g", "label": "G", "terms": [{"name": "T", "short": "s"}]}]}), encoding="utf-8")
        (root / "tools" / "course.json").write_text(json.dumps({"title": "c", "units": [], "lessons": []}), encoding="utf-8")
        (root / "tools" / "labs.json").write_text(json.dumps({"labs": []}), encoding="utf-8")
        for rel in extra_files:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# x\n", encoding="utf-8")
        (root / "web").mkdir()
        (root / "web" / "content.js").write_text("PREVIOUS_BUNDLE", encoding="utf-8")
        return root

    SITE = [
        {"path": "tools/glossary.json", "policy": "site-data"},
        {"path": "tools/course.json", "policy": "site-data"},
        {"path": "tools/labs.json", "policy": "site-data"},
    ]

    def run_build(self, root):
        import build_site

        old = (build_site.ROOT, build_site.OUTPUT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH)
        build_site.ROOT = root
        build_site.OUTPUT = root / "web" / "content.js"
        build_site.GRAPH_PATH = root / "tools" / "graph.json"
        pb.ALLOWLIST_PATH = root / "tools" / "publish-allowlist.json"
        try:
            build_site.main()
            return 0
        except SystemExit as exc:  # 构建失败 → sys.exit(2)
            return exc.code
        finally:
            build_site.ROOT, build_site.OUTPUT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH = old

    def test_unregistered_file_fails_build_and_keeps_previous_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, self.SITE + [{"path": "docs/ok.md", "policy": "public"}],
                                  extra_files=["docs/ok.md", "docs/ sneaky-internal.md"])
            self.assertEqual(self.run_build(root), 2)
            self.assertEqual((root / "web" / "content.js").read_text(encoding="utf-8"), "PREVIOUS_BUNDLE")
            self.assertFalse((root / "web" / "content.js.tmp").exists())

    def test_excluded_internal_never_enters_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, self.SITE + [
                {"path": "docs/ok.md", "policy": "public"},
                {"path": "docs/internal.md", "policy": "excluded-internal", "reason": "内部"},
                {"path": "archive/old.md", "policy": "offline-read-only"},
            ], extra_files=["docs/ok.md", "docs/internal.md", "archive/old.md"])
            import build_site
            old = (build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH)
            build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH = root, root / "tools" / "graph.json", root / "tools" / "publish-allowlist.json"
            try:
                payload = build_site.build_payload()
            finally:
                build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH = old
            ids = {d["id"] for d in payload["docs"]}
            self.assertEqual(ids, {"docs/ok.md", "archive/old.md"})
            self.assertEqual(next(d for d in payload["docs"] if d["id"] == "archive/old.md")["publishPolicy"], "offline-read-only")
            self.assertEqual({m["path"] for m in payload["publishManifest"]["docs"]}, ids)

    def test_registry_error_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, self.SITE)
            (root / "tools" / "publish-allowlist.json").write_text("{broken", encoding="utf-8")
            self.assertEqual(self.run_build(root), 2)
            self.assertEqual((root / "web" / "content.js").read_text(encoding="utf-8"), "PREVIOUS_BUNDLE")

    def test_consistent_root_builds_and_replaces_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, self.SITE + [{"path": "README.md", "policy": "public"}], extra_files=["README.md"])
            self.assertEqual(self.run_build(root), 0)
            text = (root / "web" / "content.js").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("window.RENDER_NOTES = "))
            self.assertFalse((root / "web" / "content.js.tmp").exists())

    @staticmethod
    def write_json(root, rel, data):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def build_payload_in(self, root):
        import build_site

        old = (build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH)
        build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH = root, root / "tools" / "graph.json", root / "tools" / "publish-allowlist.json"
        try:
            return build_site.build_payload()
        finally:
            build_site.ROOT, build_site.GRAPH_PATH, pb.ALLOWLIST_PATH = old

    def test_curated_data_is_embedded_and_internal_ledger_never_is(self):
        """2026-11-25：精选 evidence / knowledge-model 必须真正呈现；内部台账不得借道嵌入。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(
                tmp,
                self.SITE + [
                    {"path": "docs/lesson.md", "policy": "public"},
                    {"path": "docs/km.md", "policy": "public"},
                    {"path": "evidence/source-registry.json", "policy": "curated-data"},
                    {"path": "knowledge-model/concepts.json", "policy": "curated-data"},
                    {"path": "evidence/claim-ledger.json", "policy": "excluded-internal", "reason": "含未审核断言"},
                    {"path": "knowledge-model/agent-state.json", "policy": "excluded-internal", "reason": "Agent 中间状态"},
                ],
                extra_files=["docs/lesson.md", "docs/km.md"],
            )
            (root / "docs" / "lesson.md").write_text("# L\n\n结论见 V01 与 V02，另有 V99。\n", encoding="utf-8")
            (root / "docs" / "km.md").write_text("# KM\n", encoding="utf-8")
            self.write_json(root, "evidence/source-registry.json", {"sources": [
                {"id": "SRC-1", "title": "权威来源一", "url": "https://example.com/a", "type": "paper", "used_by_claims": ["V01", "V02"]},
                {"id": "SRC-2", "title": "本机路径来源", "url": "C:/internal/x.md", "type": "doc", "used_by_claims": ["V02"]},
            ]})
            self.write_json(root, "evidence/claim-ledger.json", {"claims": [{"id": "V01", "verification": {"status": "open"}}]})
            self.write_json(root, "knowledge-model/concepts.json", {"concepts": [
                {"id": "K-1", "name": "概念一", "definition_ref": "docs/km.md", "route": "#/glossary?term=概念一",
                 "relations": [{"type": "used_by", "target": "K-2", "source_claim": "V01"}]},
            ]})
            self.write_json(root, "knowledge-model/agent-state.json", {"secret": "x"})

            payload = self.build_payload_in(root)
            self.assertEqual(set(payload["curated"]), {"evidence/source-registry.json", "knowledge-model/concepts.json"})
            docs = {d["id"]: d for d in payload["docs"]}
            cited = {e["id"]: e for e in docs["docs/lesson.md"]["evidence"]}
            self.assertEqual(set(cited), {"SRC-1", "SRC-2"}, "V99 不在来源注册表中，不得产生引用")
            self.assertEqual(cited["SRC-1"]["claims"], ["V01", "V02"])
            self.assertEqual(cited["SRC-1"]["url"], "https://example.com/a")
            self.assertEqual(cited["SRC-2"]["url"], "", "非 http(s) 链接（如本机路径）不得输出为可点击链接")
            self.assertNotIn("verification", json.dumps(cited, ensure_ascii=False), "不得输出断言验证状态")
            self.assertEqual(docs["docs/km.md"]["concepts"][0]["id"], "K-1")
            self.assertEqual(docs["docs/km.md"]["concepts"][0]["relations"][0]["target"], "K-2")
            raw = json.dumps(payload, ensure_ascii=False)
            self.assertNotIn('"secret"', raw, "excluded-internal 的 JSON 不得以任何形式进入 payload")
            mf = {m["path"]: m["sha256"] for m in payload["publishManifest"]["curated"]}
            import hashlib
            self.assertEqual(set(mf), set(payload["curated"]))
            for rel, digest in mf.items():
                self.assertEqual(hashlib.sha256((root / rel).read_bytes()).hexdigest(), digest, rel)

    def test_curated_asset_without_registration_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, self.SITE + [{"path": "docs/lesson.md", "policy": "public"}], extra_files=["docs/lesson.md"])
            self.write_json(root, "evidence/source-registry.json", {"sources": []})
            self.assertEqual(self.run_build(root), 2, "evidence/ 内未登记资产 = 默认拒绝")
            self.assertEqual((root / "web" / "content.js").read_text(encoding="utf-8"), "PREVIOUS_BUNDLE")


def load_bundle_docs():
    content_js = ROOT / "web" / "content.js"
    text = content_js.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"window\.RENDER_NOTES = (\{.*\})\s*;?\s*$", text, re.S)
    return json.loads(match.group(1))


INTERNAL_CANARIES = (
    "DECISIONS.md", "CHANGELOG.md", "WORKFLOW_STATE.md", "AGENTS.md", "CLAUDE.md",
    "courses/video-rendering-journey/curriculum.md",
    "courses/video-rendering-journey/review-report.md",
    "courses/video-rendering-journey/教材质量诊断.md",
    "courses/video-rendering-journey/课程覆盖矩阵.md",
    "courses/video-rendering-journey/G2-审核材料-P6.md",
)


class RealArtifactTests(unittest.TestCase):
    """E：真实仓库产物（需要先跑 build_site.py / build_vitepress_content.py）。"""

    @classmethod
    def setUpClass(cls):
        if not (ROOT / "web" / "content.js").exists():
            raise unittest.SkipTest("web/content.js 尚未生成，请先运行 py -3 tools/build_site.py")
        cls.reg = pb.load_registry()
        cls.bundle = load_bundle_docs()
        cls.docs = {str(d.get("id")): d.get("publishPolicy") for d in cls.bundle.get("docs", [])}

    def test_old_advisory_api_removed(self):
        self.assertFalse(hasattr(pb, "check_allowlist"))
        self.assertFalse(hasattr(pb, "load_allowlist"))
        self.assertNotIn("include_archive", inspect.signature(pb.is_publishable).parameters)
        # 三个消费者都必须经 v2 API，且不再保留独立的目录排除表
        for tool in ("build_site.py", "validate_site.py", "build_vitepress_content.py"):
            src = (ROOT / "tools" / tool).read_text(encoding="utf-8")
            self.assertIn("publish_boundary", src, tool)
            self.assertNotIn("EXCLUDED_TOP_DIRS", src, tool)
        self.assertIn("load_registry", (ROOT / "tools" / "build_site.py").read_text(encoding="utf-8"))
        self.assertIn("load_registry", (ROOT / "tools" / "validate_site.py").read_text(encoding="utf-8"))

    def test_bundle_equals_registry_offline_set(self):
        expected = {rel for rel in pb.scan_assets(ROOT)
                    if rel.endswith(".md") and pb.is_publishable(rel, target="offline", registry=self.reg)}
        self.assertEqual(set(self.docs), expected, "bundle 文档集合必须恰好等于注册表 offline 允许集合")
        audit = pb.audit_registry(self.reg, ROOT)
        self.assertTrue(audit["ok"], audit["errors"])
        self.assertEqual(audit["unregistered"], [])

    def test_internal_files_never_in_bundle(self):
        leaked = [p for p in INTERNAL_CANARIES if p in self.docs]
        self.assertEqual(leaked, [], f"内部文件泄露进学习站: {leaked}")
        self.assertEqual([p for p in self.docs if p.startswith(("reviews/", ".agent/", ".governance/",
                                                                "program/", "legacy/", "integrations/"))], [])
        # D22：管理层/归档区/集成模块不是发布候选空间，扫描层面即排除
        scanned = pb.scan_assets(ROOT)
        self.assertEqual([p for p in scanned if p.startswith(("program/", "legacy/", "integrations/"))], [])
        for rel, policy in self.reg["_by_path"].items():
            if policy == "excluded-internal":
                self.assertNotIn(rel, self.docs, rel)
                self.assertTrue(str(self.reg["_by_path"][rel].get("reason", "")).strip(), rel)

    def test_archive_19_read_only(self):
        archive = {p for p, pol in self.docs.items() if pol == "offline-read-only"}
        disk_archive = {rel for rel in pb.scan_assets(ROOT) if rel.startswith("archive/") and rel.endswith(".md")}
        self.assertEqual(archive, disk_archive)
        self.assertEqual(len(archive), 19, "D10.4：archive 应为 19 篇且一一对应")
        for p in archive:
            self.assertTrue(p.startswith("archive/"))
        self.assertFalse([p for p, pol in self.docs.items() if pol == "offline-read-only" and not p.startswith("archive/")])

    def test_manifest_traceable(self):
        manifest = self.bundle["publishManifest"]
        self.assertEqual(manifest["target"], "offline")
        self.assertEqual(manifest["registryVersion"], self.reg["version"])
        import hashlib
        for m in manifest["docs"]:
            self.assertEqual(hashlib.sha256((ROOT / m["path"]).read_bytes()).hexdigest(), m["sha256"], m["path"])

    def test_site_data_registered(self):
        for rel in ("tools/glossary.json", "tools/course.json", "tools/labs.json"):
            self.assertEqual(pb.policy_for(rel, self.reg), "site-data", rel)

    def test_curated_data_actually_presented(self):
        """2026-11-25：注册为 curated-data 的资产必须真正进入站点并呈现，且内部台账不在其中。"""
        import hashlib
        curated = {rel for rel, a in self.reg["_by_path"].items() if a["policy"] == "curated-data"}
        self.assertIn("evidence/source-registry.json", curated)
        self.assertIn("knowledge-model/concepts.json", curated)
        embedded = self.bundle.get("curated") or {}
        self.assertEqual(set(embedded), curated, "payload.curated 必须恰好等于注册表的 curated-data 集合")
        for rel, a in self.reg["_by_path"].items():
            if a["policy"] == "excluded-internal":
                self.assertNotIn(rel, embedded, rel)
        mf = {m["path"]: m["sha256"] for m in self.bundle["publishManifest"]["curated"]}
        for rel in curated:
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), mf[rel], rel)
        docs = self.bundle.get("docs", [])
        with_evidence = [d for d in docs if d.get("evidence")]
        with_concepts = [d for d in docs if d.get("concepts")]
        self.assertGreaterEqual(len(with_evidence), 20, "至少主课程 19 课应呈现证据来源")
        self.assertTrue(any(d["id"].startswith("courses/embodied-loop-journey/") for d in with_evidence), "embodied 六课应呈现证据来源")
        self.assertGreaterEqual(len(with_concepts), 10, "知识文档应呈现其定义的概念")
        source_ids = {s["id"] for s in embedded["evidence/source-registry.json"]["sources"]}
        for d in docs:
            for item in d.get("evidence") or []:
                self.assertIn(item["id"], source_ids, d["id"])
                self.assertNotIn("verification", item)
        for d in docs:
            for item in d.get("concepts") or []:
                self.assertEqual(set(item), {"id", "name", "route", "relations"}, d["id"])

    def test_online_tree_excludes_archive_and_internal(self):
        vp = ROOT / "site-vitepress" / "docs"
        if not vp.exists():
            self.skipTest("VitePress docs 尚未生成")
        self.assertFalse((vp / "archive").exists(), "在线站不得包含 archive/（D10.4 online=forbidden）")
        files = [p.relative_to(vp).as_posix() for p in vp.rglob("*.md") if p.name != "index.md"]
        bad = [f for f in files if not pb.is_publishable(f, target="online", registry=self.reg)]
        self.assertEqual(bad, [], "在线树含有非 online 资产")
        self.assertEqual(sorted(files), sorted(p for p in pb.scan_assets(ROOT)
                                               if p.endswith(".md") and pb.is_publishable(p, target="online", registry=self.reg)))

    def test_knowledge_docs_still_present(self):
        self.assertIn("01-基础理论/音视频基础理论.md", self.docs)
        self.assertTrue(any(p.startswith("courses/video-rendering-journey/lessons/") for p in self.docs))
        self.assertIn("docs/USER-GUIDE.md", self.docs)

    def test_no_term_links_inside_display_math(self):
        """2026-11-24 回归门禁：$$ 公式块内不得注入术语链接（公式乱码修复）。"""
        bad = []
        for d in self.bundle["docs"]:
            if d.get("path") == "CHANGELOG.md":
                continue
            for m in re.finditer(r"\$\$[\s\S]*?\$\$", d.get("markdown") or ""):
                if "glossary?term" in m.group(0):
                    bad.append(d.get("path"))
                    break
        self.assertEqual(bad, [], f"公式块内出现术语链接（会致 KaTeX 乱码）: {bad}")

    def test_quizzes_payload_covers_disk(self):
        # D22 P0：检查点练习必须嵌入 bundle（lesson id -> quiz），键必须是已知课时
        quizzes = self.bundle.get("quizzes")
        self.assertIsInstance(quizzes, dict)
        disk = {}
        for qf in sorted((ROOT / "courses").glob("*/quizzes/*.json")):
            qd = json.loads(qf.read_text(encoding="utf-8"))
            disk[qd["lesson"]] = qd
        self.assertEqual(set(quizzes), set(disk), "quizzes payload 必须恰覆盖磁盘 quiz 文件")
        self.assertIn("E01", quizzes)
        self.assertIn("L01", quizzes)
        lesson_ids = set()
        for c in self.bundle.get("courses", []):
            lesson_ids.update(l["id"] for l in c.get("lessons", []))
        self.assertTrue(set(quizzes) <= lesson_ids, "quiz 键必须是课程契约中的课时 id")

    def test_registry_still_indexes_reviews(self):
        registry = ROOT / ".agent" / "indexes" / "document-registry.json"
        if not registry.exists():
            self.skipTest("注册表尚未生成")
        self.assertIn("reviews/", registry.read_text(encoding="utf-8", errors="replace"), "文档注册表应继续索引 reviews/ 治理文档")

    def test_pilot_course_context_navigation(self):
        """回归：pilot 复用主课程 L## id，课程上下文必须贯穿路由/下一课/返回链。

        证据：reviews/consolidation-qa-pilot-context-20261126.json（3 浏览器场景）。
        此处守住代码不变量与数据级 next 链，防止修复被意外回退。
        """
        app = (ROOT / "web" / "assets" / "app.js").read_text(encoding="utf-8")
        # 1) courseRoute 对非主课程课时链接携带 ?c=
        self.assertIn('const suffix = key && key !== "main" ? "?c=" + encodeURIComponent(key) : "";', app)
        self.assertIn('return "#/course/" + encodeURIComponent(lessonId) + suffix;', app)
        # 2) parseRoute 的 course/<id> 分支读取课程上下文
        self.assertIn('courseKey: cm ? safeDecode(cm[1]) : "main"', app)
        # 3) renderLesson 接受课程参数并经课程感知解析
        self.assertIn("function renderLesson(lessonId, courseKey)", app)
        self.assertIn("function lessonMeta(lessonId, courseKey)", app)
        # 4) 路由分发把课程上下文传入 renderLesson
        self.assertIn('renderLesson(target.lesson, target.courseKey || "main")', app)
        # 数据级：pilot 的 L02 下一课必须是 L06（精选路径），而非主课程的 L03
        pilot = next((c for c in self.bundle.get("courses", [])
                      if c.get("id") == "video-rendering-journey"), None)
        self.assertIsNotNone(pilot, "bundle 应含 video-rendering-journey 课程")
        by_id = {l["id"]: l for l in pilot.get("lessons", [])}
        self.assertEqual(by_id["L02"].get("next"), "L06", "pilot L02 的下一课必须是 L06")
        self.assertEqual([l["id"] for l in pilot["lessons"]], ["L01", "L02", "L06", "L11", "L13"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
