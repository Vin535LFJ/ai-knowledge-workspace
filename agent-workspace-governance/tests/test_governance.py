# -*- coding: utf-8 -*-
"""治理工具包单元测试：全部使用 tempfile，不联网、不依赖真实仓库。"""

import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT_ROOT, "cli"))

import governance as g  # noqa: E402


FULL_FM = """---
doc_id: spec-doc
type: formal-tech-doc
level: L1
status: active
owner: alice
created: 2026-11-19
updated: 2026-11-19
---

# 正文
"""


class GovernaceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def _write_json(self, filename, data):
        path = os.path.join(self.project, g.STATE_DIR, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return path

    def _write(self, rel_path, content):
        path = os.path.join(self.project, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        return path

    # 1. init 幂等
    def test_init_idempotency(self):
        first = g.init_project(self.project)
        self.assertTrue(first)
        self.assertTrue(os.path.exists(os.path.join(self.project, g.STATE_DIR, g.CONFIG_FILE)))
        self.assertTrue(os.path.exists(os.path.join(self.project, g.AGENTS_FILE)))
        second = g.init_project(self.project)
        self.assertEqual(second, [], "第二次 init 应不新建任何文件")

    # 2. frontmatter 解析
    def test_frontmatter_parsing(self):
        text = """---
doc_id: doc-1
type: test
status: active
owner: bob
created: 2026-11-19
updated: 2026-11-19
generated: true
tags: [a, b, c]
items:
  - one
  - two
---

body
"""
        fm = g.parse_frontmatter(text)
        self.assertEqual(fm["doc_id"], "doc-1")
        self.assertEqual(fm["status"], "active")
        self.assertIs(fm["generated"], True)
        self.assertEqual(fm["tags"], ["a", "b", "c"])
        self.assertEqual(fm["items"], ["one", "two"])
        self.assertEqual(g.parse_frontmatter("no frontmatter here"), {})

    # 3. 文档登记
    def test_document_registration(self):
        g.init_project(self.project)
        self._write("spec.md", FULL_FM)
        touched = g.inventory_docs(self.project)
        self.assertIn("spec-doc", touched)
        registry = g._read_json(os.path.join(self.project, g.STATE_DIR, g.REGISTRY_DOC))
        doc = next(d for d in registry["documents"] if d["document_id"] == "spec-doc")
        self.assertEqual(doc["owner"], "alice")
        self.assertEqual(doc["status"], "active")
        self.assertEqual(doc["level"], "L1")

    # 4. validate 检测缺 owner/status
    def test_validate_detects_missing_owner_status(self):
        g.init_project(self.project)
        self._write("bad.md", """---
doc_id: bad-doc
type: test
created: 2026-11-19
updated: 2026-11-19
---

# 缺 owner 与 status
""")
        report = g.validate(self.project)
        err_text = "\n".join(report["errors"])
        self.assertIn("'owner'", err_text)
        self.assertIn("'status'", err_text)

        # 补齐后应通过
        self._write("bad.md", FULL_FM)
        report2 = g.validate(self.project)
        self.assertEqual(report2["errors"], [])

    # 5. 任务状态查询
    def test_task_status_query(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_TASK, {"tasks": [
            {
                "task_id": "TASK-001",
                "title": "修复登录",
                "owner_agent": "claude-code",
                "status": "in_progress",
                "human_approval_required": True,
            },
            {
                "task_id": "TASK-002",
                "title": "写文档",
                "owner_agent": "codex",
                "status": "completed",
                "human_approval_required": False,
            },
        ]})
        result = g.task_status(self.project)
        self.assertEqual(len(result["tasks"]), 2)
        self.assertEqual(result["tasks"][0]["status"], "in_progress")
        self.assertEqual(len(result["pending_approvals"]), 1)
        self.assertEqual(result["pending_approvals"][0]["task_id"], "TASK-001")

    # 6. Agent 映射
    def test_agent_map(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_AGENT, {"agents": [
            {
                "agent_id": "a1",
                "agent_name": "Claude",
                "provider": "anthropic",
                "harness": "claude-code",
                "runtime_verification_status": "unverified",
                "supported_skills": ["research-to-learning"],
                "supported_mcp": ["filesystem"],
                "supported_tools": ["bash"],
            }
        ]})
        result = g.agent_map(self.project)
        self.assertEqual(len(result["agents"]), 1)
        self.assertEqual(result["agents"][0]["agent_id"], "a1")
        self.assertIn("research-to-learning", result["skills"])
        self.assertIn("filesystem", result["mcp"])
        self.assertIn("bash", result["tools"])

    # 7. 交接文档生成
    def test_handoff_generation(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_TASK, {"tasks": [
            {
                "task_id": "TASK-001",
                "title": "迁移模块",
                "owner_agent": "agent-a",
                "status": "in_progress",
                "read_paths": ["docs/a.md"],
                "write_paths": ["src/b.py"],
                "protected_paths": ["constitution/"],
                "dependencies": ["TASK-000"],
                "outputs": ["src/b.py"],
                "acceptance_criteria": ["测试通过"],
                "human_approval_required": False,
            }
        ]})
        path = g.generate_handoff(self.project, "TASK-001", to_agent="agent-b")
        self.assertTrue(path and os.path.exists(path))
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("TASK-001", content)
        self.assertIn("agent-b", content)
        self.assertIn("测试通过", content)
        self.assertNotIn("{{", content)

    # 8. ADR 创建与列出
    def test_adr_create_and_list(self):
        g.init_project(self.project)
        rec = g.adr_create(self.project, "采用事件溯源")
        self.assertEqual(rec["id"], "ADR-0001")
        self.assertEqual(rec["status"], "proposed")
        self.assertEqual(rec["human_approved"], False)
        adrs = g.adr_list(self.project)
        self.assertEqual(len(adrs), 1)
        self.assertTrue(os.path.exists(
            os.path.join(self.project, "docs", "adr", "ADR-0001.md")))

    # 9. 归档检查
    def test_archive_check(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_DOC, {"documents": [
            {
                "document_id": "old-superseded",
                "path": "docs/old.md",
                "type": "adr",
                "status": "superseded",
                "owner": "alice",
                "created_at": "2020-01-01",
                "updated_at": "2020-01-01",
            }
        ]})
        self._write_json(g.REGISTRY_TASK, {"tasks": [
            {"task_id": "TASK-DONE", "status": "completed"}
        ]})
        result = g.archive_check(self.project, max_age_days=30)
        kinds = {c["kind"] for c in result["archive_candidates"]}
        self.assertIn("document", kinds)
        self.assertIn("task", kinds)

    # 10. audit 孤儿检测
    def test_audit_orphan_detection(self):
        g.init_project(self.project)
        self._write("lonely.md", FULL_FM)
        g.inventory_docs(self.project)
        result = g.audit(self.project)
        self.assertIn("spec-doc", result["orphan"])

    # 11. Render_Notes 迁移映射
    def test_render_notes_migration_mapping(self):
        path = os.path.join(KIT_ROOT, "examples", "render-notes", "README.md")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        for token in [
            "KNOWLEDGE_CHANGE_REVIEW.md",
            "WORKFLOW_STATE.md",
            "Source → Claim → Concept → Lesson → Quiz → Course",
            "DECISIONS.md",
            ".agent/constitution/",
        ]:
            self.assertIn(token, content, "迁移映射缺少：" + token)

        # basic-project 无知识结构依赖
        cfg = os.path.join(KIT_ROOT, "examples", "basic-project", ".governance", "config.json")
        with open(cfg, encoding="utf-8") as fh:
            config = json.load(fh)
        self.assertEqual(config["project_id"], "basic-project")


class GovernanceIncrementTests(unittest.TestCase):
    """增量补齐：13 类枚举、doctor、index 别名、三条协作协议纯函数。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def _write_json(self, filename, data):
        path = os.path.join(self.project, g.STATE_DIR, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return path

    def _clean_doc_entry(self, **overrides):
        entry = {
            "document_id": "DOC-1",
            "path": "docs/spec.md",
            "type": "Spec",
            "status": "active",
            "owner": "alice",
            "created_at": "2026-11-19",
            "updated_at": "2026-11-19",
        }
        entry.update(overrides)
        return entry

    def _run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = g.main(list(args))
        return rc, buf.getvalue()

    # --- 13 类枚举 ---
    def test_document_types_enum_legal_and_illegal(self):
        self.assertEqual(len(g.DOCUMENT_TYPES), 13)
        self.assertIn("ADR", g.DOCUMENT_TYPES)
        self.assertIn("Session Note", g.DOCUMENT_TYPES)
        self.assertNotIn("bogus-type", g.DOCUMENT_TYPES)
        # schema 文件中确实定义了全部 13 类
        schema_path = os.path.join(KIT_ROOT, "schemas", "document.schema.json")
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
        consts = {
            item["const"]
            for item in schema["properties"]["type"]["oneOf"]
            if "const" in item
        }
        self.assertEqual(consts, set(g.DOCUMENT_TYPES))
        self.assertIs(schema["additionalProperties"], True)

    def test_task_schema_claim_fields_optional(self):
        schema_path = os.path.join(KIT_ROOT, "schemas", "task.schema.json")
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
        for field in ("claimed_at", "claim_token", "dependency_frontier"):
            self.assertIn(field, schema["properties"])
            self.assertNotIn(field, schema["required"])

    # --- doctor ---
    def test_doctor_clean_exit_zero(self):
        g.init_project(self.project)
        rc, out = self._run_cli("doctor", "--project", self.project)
        self.assertEqual(rc, 0, out)
        self.assertIn("诊断通过", out)
        self.assertEqual(g.doctor(self.project)["errors"], [])

    def test_doctor_detects_missing_owner(self):
        g.init_project(self.project)
        entry = self._clean_doc_entry()
        del entry["owner"]
        self._write_json(g.REGISTRY_DOC, {"documents": [entry]})
        report = g.doctor(self.project)
        self.assertTrue(any("'owner'" in e for e in report["errors"]))
        rc, out = self._run_cli("doctor", "--project", self.project)
        self.assertEqual(rc, 1)
        self.assertIn("缺少必填字段 'owner'", out)

    def test_doctor_detects_illegal_type(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_DOC, {"documents": [
            self._clean_doc_entry(type="bogus-type")]})
        report = g.doctor(self.project)
        self.assertTrue(any("13 类标准枚举" in e for e in report["errors"]))
        self.assertEqual(self._run_cli("doctor", "--project", self.project)[0], 1)

    def test_doctor_detects_single_writer_conflict(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_TASK, {"tasks": [
            {"task_id": "T1", "status": "in_progress", "owner_agent": "a",
             "write_paths": ["docs/shared.md"]},
            {"task_id": "T2", "status": "in_progress", "owner_agent": "b",
             "write_paths": ["docs/shared.md", "docs/other.md"]},
        ]})
        report = g.doctor(self.project)
        self.assertEqual(len(report["single_writer_conflicts"]), 1)
        self.assertTrue(any("单写者冲突" in e for e in report["errors"]))
        self.assertEqual(self._run_cli("doctor", "--project", self.project)[0], 1)

    def test_doctor_detects_dependency_cycle(self):
        g.init_project(self.project)
        self._write_json(g.REGISTRY_TASK, {"tasks": [
            {"task_id": "A", "status": "blocked", "dependencies": ["B"]},
            {"task_id": "B", "status": "blocked", "dependencies": ["A"]},
        ]})
        report = g.doctor(self.project)
        self.assertTrue(report["dependency_cycles"])
        self.assertTrue(any("依赖环" in e for e in report["errors"]))
        self.assertEqual(self._run_cli("doctor", "--project", self.project)[0], 1)

    def test_doctor_detects_broken_json(self):
        g.init_project(self.project)
        path = os.path.join(self.project, g.STATE_DIR, g.REGISTRY_TASK)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("{ not valid json")
        report = g.doctor(self.project)
        self.assertTrue(any("JSON 解析失败" in e for e in report["errors"]))
        self.assertEqual(self._run_cli("doctor", "--project", self.project)[0], 1)

    # --- index 别名 ---
    def test_index_is_alias_of_inventory(self):
        g.init_project(self.project)
        doc = """---
doc_id: alias-doc
type: Spec
status: active
owner: alice
created: 2026-11-19
updated: 2026-11-19
---

# 正文
"""
        path = os.path.join(self.project, "alias.md")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(doc)
        rc_inv, out_inv = self._run_cli("inventory", "--project", self.project)
        rc_idx, out_idx = self._run_cli("index", "--project", self.project)
        self.assertEqual(rc_inv, 0)
        self.assertEqual(rc_idx, 0)
        self.assertEqual(out_inv, out_idx, "index 与 inventory 输出应完全一致")
        self.assertIn("alias-doc", out_idx)

    # --- claim_task ---
    def test_claim_task_success_and_conflict(self):
        registry = {"tasks": [
            {"task_id": "T1", "status": "draft", "owner_agent": "",
             "write_paths": ["docs/a.md"]}]}
        updated, info = g.claim_task(registry, "T1", "agent-a",
                                     branch="feature/x", now="2026-11-19")
        self.assertTrue(info["ok"])
        self.assertTrue(info["claim_token"])
        task = updated["tasks"][0]
        self.assertEqual(task["status"], "in_progress")
        self.assertEqual(task["owner_agent"], "agent-a")
        self.assertEqual(task["claimed_at"], "2026-11-19")
        self.assertEqual(task["claim_token"], info["claim_token"])
        self.assertEqual(task["branch"], "feature/x")
        # 纯函数：入参未被修改
        self.assertEqual(registry["tasks"][0]["status"], "draft")

        # 重复认领（不同 agent）被拒绝
        updated2, info2 = g.claim_task(updated, "T1", "agent-b", now="2026-11-19")
        self.assertFalse(info2["ok"])
        self.assertIn("单写者冲突", info2["error"])
        self.assertEqual(updated2["tasks"][0]["owner_agent"], "agent-a")
        # 同一 agent 重新认领允许（幂等）
        _, info3 = g.claim_task(updated, "T1", "agent-a", now="2026-11-19")
        self.assertTrue(info3["ok"])

    def test_claim_task_missing_task(self):
        _, info = g.claim_task({"tasks": []}, "NOPE", "agent-a", now="2026-11-19")
        self.assertFalse(info["ok"])
        self.assertIn("不存在", info["error"])

    # --- check_frontier ---
    def test_check_frontier_satisfied_and_unsatisfied(self):
        registry = {"tasks": [
            {"task_id": "D1", "status": "completed"},
            {"task_id": "D2", "status": "approved"},
            {"task_id": "D3", "status": "in_progress"},
        ]}
        ready, missing = g.check_frontier(
            {"task_id": "T", "dependencies": ["D1", "D2"]}, registry)
        self.assertTrue(ready)
        self.assertEqual(missing, [])

        ready, missing = g.check_frontier(
            {"task_id": "T", "dependencies": ["D1", "D3"]}, registry)
        self.assertFalse(ready)
        self.assertEqual(missing, ["D3"])

        # dependency_frontier 对象形式
        ready, missing = g.check_frontier(
            {"task_id": "T", "dependency_frontier": [
                {"task_id": "D1", "approved": True},
                {"task_id": "D3", "approved": False},
            ]}, registry)
        self.assertFalse(ready)
        self.assertIn("D3", missing)

    # --- detect_single_writer_conflicts (纯函数) ---
    def test_detect_single_writer_conflicts_pure(self):
        registry = {"tasks": [
            {"task_id": "A", "status": "in_progress", "owner_agent": "a",
             "write_paths": ["x.py", "y.py"]},
            {"task_id": "B", "status": "in_progress", "owner_agent": "b",
             "write_paths": ["y.py"]},
            {"task_id": "C", "status": "in_progress", "owner_agent": "a",
             "write_paths": ["x.py"]},
            {"task_id": "D", "status": "completed", "owner_agent": "b",
             "write_paths": ["y.py"]},
        ]}
        conflicts = g.detect_single_writer_conflicts(registry)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual({conflicts[0]["task_a"], conflicts[0]["task_b"]}, {"A", "B"})
        self.assertEqual(conflicts[0]["paths"], ["y.py"])

    # --- detect_dependency_cycles ---
    def test_detect_dependency_cycles_pure(self):
        self.assertEqual(g.detect_dependency_cycles({"tasks": [
            {"task_id": "A", "dependencies": ["B"]},
            {"task_id": "B", "dependencies": ["C"]},
            {"task_id": "C", "status": "completed"},
        ]}), [])
        cycles = g.detect_dependency_cycles({"tasks": [
            {"task_id": "A", "dependencies": ["B"]},
            {"task_id": "B", "dependencies": ["A"]},
            {"task_id": "C", "dependencies": ["C"]},
        ]})
        self.assertEqual(len(cycles), 2)
        self.assertTrue(any(set(c) == {"A", "B"} for c in cycles))
        self.assertTrue(any(c == ["C"] for c in cycles))


class ExampleProjectTests(unittest.TestCase):
    """验收缺口闭环（2026-11-21）：examples/basic-project 此前未被测试直接引用。"""

    def _example_root(self):
        root = os.path.join(KIT_ROOT, "examples", "basic-project")
        assert os.path.isdir(root), "examples/basic-project 缺失"
        return root

    def test_basic_project_governance_state_complete(self):
        state_dir = os.path.join(self._example_root(), ".governance")
        expected = {
            "config.json", "document-registry.json", "task-registry.json",
            "agent-registry.json", "adr-index.json",
        }
        for name in expected:
            path = os.path.join(state_dir, name)
            self.assertTrue(os.path.isfile(path), f"缺 {name}")
            data = json.load(io.open(path, encoding="utf-8"))
            self.assertIsInstance(data, dict, f"{name} 应为 JSON object")

    def test_basic_project_docs_are_scannable(self):
        docs = g.scan_markdown_docs(self._example_root())
        rels = [rel for _abs, rel, _text in docs]
        self.assertTrue(any("design.md" in rel for rel in rels),
                        f"basic-project 的 docs 未被扫描到: {rels}")

    def test_scan_markdown_docs_skips_ignore_dirs(self):
        """真实项目适配修复（2026-11-21）：node_modules/vendor/dist 不再入扫描。"""
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "node_modules", "vue"))
            os.makedirs(os.path.join(tmp, "vendor", "lib"))
            os.makedirs(os.path.join(tmp, "docs"))
            for rel in (
                os.path.join("node_modules", "vue", "README.md"),
                os.path.join("vendor", "lib", "x.md"),
                os.path.join("docs", "keep.md"),
            ):
                io.open(os.path.join(tmp, rel), "w", encoding="utf-8").write("# t\n")
            rels = [rel for _abs, rel, _t in g.scan_markdown_docs(tmp)]
        self.assertEqual(rels, ["docs/keep.md"])

    # --- P0-A：示例必须自洽（2026-11-25） ---
    def test_basic_project_doctor_exit_zero(self):
        rc, out = self._run_cli("doctor", "--project", self._example_root())
        self.assertEqual(rc, 0, out)
        self.assertIn("诊断通过", out)

    def test_basic_project_types_in_enum_and_match_frontmatter(self):
        """注册表 type 必须在 13 类枚举内，且与文档 frontmatter 的 type 一致。"""
        root = self._example_root()
        with io.open(os.path.join(root, g.STATE_DIR, g.REGISTRY_DOC),
                     encoding="utf-8") as fh:
            registry = json.load(fh)
        fm_types = {
            rel: g.parse_frontmatter(text).get("type")
            for _abs, rel, text in g.scan_markdown_docs(root)
        }
        for entry in registry["documents"]:
            self.assertIn(entry["type"], g.DOCUMENT_TYPES, entry["path"])
            self.assertEqual(entry["type"], fm_types[entry["path"]], entry["path"])

    def test_basic_project_registry_reproduced_by_inventory(self):
        """示例注册表不是手写漂移的：对示例副本重跑 inventory，条目应完全一致。"""
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = os.path.join(tmp, "basic-project")
            shutil.copytree(self._example_root(), copy_root)
            g.inventory_docs(copy_root)
            regenerated = g._read_json(os.path.join(copy_root, g.STATE_DIR, g.REGISTRY_DOC))
        with io.open(os.path.join(self._example_root(), g.STATE_DIR, g.REGISTRY_DOC),
                     encoding="utf-8") as fh:
            checked_in = json.load(fh)
        self.assertEqual(regenerated["documents"], checked_in["documents"])

    def test_document_schema_accepts_optional_null_fields(self):
        """schema 与 CLI 产物一致：未声明的可选字段（如 level）登记为 null，schema 必须接受。"""
        schema_path = os.path.join(KIT_ROOT, "schemas", "document.schema.json")
        with io.open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
        props = schema["properties"]
        for field in ("level", "source_of_truth", "related_task", "related_adr",
                      "replaces", "superseded_by"):
            self.assertIn("null", props[field]["type"], field + " 应允许 null")
        self.assertNotIn("level", schema["required"])

    def _run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = g.main(list(args))
        return rc, buf.getvalue()


class InitExistingAgentsTests(unittest.TestCase):
    """P0-B：已有 AGENTS.md 的项目接入 init（2026-11-25）。

    覆盖：空白项目、已有自定义内容、重复执行幂等、原内容逐字节不变、
    带空格/中文的路径、非 UTF-8 文件不破坏。
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    USER_CONTENT = (
        "---\n"
        "doc_id: MY-AGENTS\n"
        "type: adapter\n"
        "status: active\n"
        "owner: alice\n"
        "---\n"
        "\n"
        "# 我的项目规则\n"
        "\n"
        "这是用户自己写的内容，init 不得改动。\n"
        "- 先读 `.agent/README.md`\n"
    )

    def _agents_path(self, project=None):
        return os.path.join(project or self.project, g.AGENTS_FILE)

    def _read_bytes(self, project=None):
        with open(self._agents_path(project), "rb") as fh:
            return fh.read()

    def _run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = g.main(list(args))
        return rc, buf.getvalue()

    def _state_snapshot(self, project=None):
        """读取 .governance 下全部文件的字节快照，用于幂等对比。"""
        state = os.path.join(project or self.project, g.STATE_DIR)
        snapshot = {}
        for name in sorted(os.listdir(state)):
            with open(os.path.join(state, name), "rb") as fh:
                snapshot[name] = fh.read()
        return snapshot

    def _pointer_kit_path(self, text):
        """从指针段中取出治理 CLI 路径（`{kit}/cli/governance.py` 的 {kit} 部分）。"""
        match = re.search(r"治理 CLI：`([^`]+)/cli/governance\.py`", text)
        self.assertIsNotNone(match, "指针段缺少治理 CLI 路径")
        return match.group(1)

    # 1. 空白项目 init → 有治理入口
    def test_blank_project_gets_pointer_entry(self):
        rc, out = self._run_cli("init", "--project", self.project)
        self.assertEqual(rc, 0, out)
        self.assertIn("新建文件", out)
        text = self._read_bytes().decode("utf-8")
        self.assertIn(g.POINTER_BEGIN, text)
        self.assertIn(g.POINTER_END, text)
        self.assertTrue(text.startswith("---\n"), "新建的入口应带 frontmatter")
        self.assertEqual(text.count(g.POINTER_BEGIN), 1)
        # 指针路径相对项目根解析后必须指向真实存在的工具包目录
        kit = self._pointer_kit_path(text)
        resolved = os.path.normpath(os.path.join(self.project, kit))
        self.assertEqual(os.path.normpath(KIT_ROOT), resolved)
        for rel in ("constitution/AGENT_RULES.md", "AGENTS.md", "cli/governance.py"):
            self.assertTrue(os.path.isfile(os.path.join(resolved, *rel.split("/"))), rel)
        self.assertFalse(os.path.isabs(kit) or re.match(r"^[A-Za-z]:", kit),
                         "同盘符下指针应为相对路径，不应写死盘符：" + kit)

    # 2. 已有 AGENTS.md（CRLF、无结尾换行、中文自定义内容）→ 原内容逐字节不变 + 指针
    def test_existing_agents_file_kept_byte_identical_and_pointer_appended(self):
        original = self.USER_CONTENT.replace("\n", "\r\n").rstrip("\r\n").encode("utf-8")
        with open(self._agents_path(), "wb") as fh:
            fh.write(original)

        rc, out = self._run_cli("init", "--project", self.project)
        self.assertEqual(rc, 0, out)
        self.assertIn("追加治理入口指针", out)

        after = self._read_bytes()
        self.assertTrue(after.startswith(original), "用户原有内容必须逐字节不变")
        appended = after[len(original):]
        self.assertIn(g.POINTER_BEGIN.encode("utf-8"), appended)
        self.assertIn(g.POINTER_END.encode("utf-8"), appended)
        self.assertEqual(after.count(g.POINTER_BEGIN.encode("utf-8")), 1, "不得重复追加")
        self.assertNotIn(b"created:", appended, "追加段不得再写 frontmatter")
        # 沿用原文件的换行风格，且指针段从新行开始
        self.assertTrue(appended.startswith(b"\r\n\r\n"))
        self.assertNotIn(b"\n", appended.replace(b"\r\n", b""))
        self.assertEqual(g.parse_frontmatter(original.decode("utf-8"))["doc_id"], "MY-AGENTS")

    # 3. 重复 init → 幂等（AGENTS.md 与 .governance 内容均不变）
    def test_repeated_init_is_idempotent(self):
        with open(self._agents_path(), "wb") as fh:
            fh.write(self.USER_CONTENT.encode("utf-8"))
        self._run_cli("init", "--project", self.project)
        agents_first = self._read_bytes()
        state_first = self._state_snapshot()
        created_count = len(state_first)
        self.assertEqual(created_count, 5, "应生成 5 个治理 JSON")

        rc, out = self._run_cli("init", "--project", self.project)
        self.assertEqual(rc, 0, out)
        self.assertIn("已含治理入口指针", out)
        self.assertEqual(self._read_bytes(), agents_first, "第二次 init 不得改动 AGENTS.md")
        self.assertEqual(self._state_snapshot(), state_first, "第二次 init 不得改动 .governance")
        self.assertEqual(g.init_project(self.project), [], "第三次 init 不新建任何文件")

    # 3b. 空白项目重复 init 同样幂等
    def test_repeated_init_blank_project_idempotent(self):
        self._run_cli("init", "--project", self.project)
        agents_first = self._read_bytes()
        state_first = self._state_snapshot()
        self._run_cli("init", "--project", self.project)
        self.assertEqual(self._read_bytes(), agents_first)
        self.assertEqual(self._state_snapshot(), state_first)

    # 4. 跨平台路径：带空格/中文的项目目录跑 init + doctor
    def test_init_and_doctor_in_path_with_spaces_and_chinese(self):
        project = os.path.join(self._tmp.name, "治理 示例 project", "我的 项目")
        os.makedirs(project)
        rc_init, out_init = self._run_cli("init", "--project", project)
        self.assertEqual(rc_init, 0, out_init)
        rc_doc, out_doc = self._run_cli("doctor", "--project", project)
        self.assertEqual(rc_doc, 0, out_doc)
        text = self._read_bytes(project).decode("utf-8")
        kit = self._pointer_kit_path(text)
        self.assertEqual(
            os.path.normpath(KIT_ROOT),
            os.path.normpath(os.path.join(project, kit)))
        config = g._read_json(os.path.join(project, g.STATE_DIR, g.CONFIG_FILE))
        self.assertEqual(config["project_id"], "我的 项目")

    # 5. 空的 AGENTS.md → 写入完整入口；再次 init 不重复
    def test_empty_agents_file_gets_full_entry_once(self):
        with open(self._agents_path(), "wb") as fh:
            fh.write(b"  \r\n")
        status = g.ensure_agents_pointer(self.project)
        self.assertEqual(status, "created")
        first = self._read_bytes()
        self.assertTrue(first.startswith(b"---\n"))
        self.assertEqual(g.ensure_agents_pointer(self.project), "present")
        self.assertEqual(self._read_bytes(), first)

    # 6. 非 UTF-8 的 AGENTS.md → 不修改、不静默（CLI 有明确警告）
    def test_non_utf8_agents_file_untouched_with_warning(self):
        original = "# 我的规则\n不得改动。\n".encode("gbk")
        with open(self._agents_path(), "wb") as fh:
            fh.write(original)
        self.assertEqual(g.ensure_agents_pointer(self.project), "skipped")
        rc, out = self._run_cli("init", "--project", self.project)
        self.assertEqual(rc, 0)
        self.assertIn("警告", out)
        self.assertIn("不是 UTF-8", out)
        self.assertEqual(self._read_bytes(), original)

    # 7. 项目就是工具包自身 / 位于工具包内部：相对路径为 "." 或 "../.."（只渲染，不写文件）
    def test_pointer_relative_when_project_inside_kit(self):
        self.assertEqual(g._kit_pointer_path(KIT_ROOT), ".")
        inside = os.path.join(KIT_ROOT, "examples", "basic-project")
        self.assertEqual(g._kit_pointer_path(inside), "../..")
        text = g._render_pointer_body(KIT_ROOT, appended=True)
        self.assertIn("`./constitution/`", text)
        self.assertIn("`./cli/governance.py`", text)

    # 8. 跨盘符：relpath 抛 ValueError 时退回绝对路径，不得崩溃
    @unittest.skipUnless(os.name == "nt", "跨盘符 relpath 仅 Windows 会抛 ValueError")
    def test_pointer_falls_back_to_absolute_on_cross_drive(self):
        saved = g.KIT_ROOT
        try:
            g.KIT_ROOT = r"Z:\no-such-drive\agent-workspace-governance"
            with tempfile.TemporaryDirectory() as tmp:
                text = g._render_pointer_body(tmp)
            self.assertIn("Z:/no-such-drive/agent-workspace-governance/cli/governance.py", text)
        finally:
            g.KIT_ROOT = saved


if __name__ == "__main__":
    unittest.main()
