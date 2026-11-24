# -*- coding: utf-8 -*-
"""治理工具包单元测试：全部使用 tempfile，不联网、不依赖真实仓库。"""

import io
import json
import os
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


if __name__ == "__main__":
    unittest.main()
