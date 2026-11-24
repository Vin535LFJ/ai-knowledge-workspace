# -*- coding: utf-8 -*-
"""Agent Workspace Governance CLI.

纯 Python 标准库实现。所有命令都是本地文件操作：不联网、不执行 git。
核心逻辑为可单独测试的纯函数；argparse 仅负责参数解析与分发。
"""

from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

STATE_DIR = ".governance"                 # 状态目录（位于目标项目内）
CONFIG_FILE = "config.json"
REGISTRY_DOC = "document-registry.json"
REGISTRY_TASK = "task-registry.json"
REGISTRY_AGENT = "agent-registry.json"
REGISTRY_ADR = "adr-index.json"
AGENTS_FILE = "AGENTS.md"

# 治理工具包根目录（本文件位于 <kit>/cli/）
KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 正式文档必备的 frontmatter 字段
REQUIRED_FM = ["doc_id", "type", "status", "owner", "created", "updated"]

# ADR 合法状态与生命周期
ADR_STATUSES = {"proposed", "accepted", "deprecated", "superseded"}
ADR_DECIDED = {"accepted", "deprecated", "superseded"}

# 13 类标准文档类型（与 schemas/document.schema.json 的 oneOf 保持一致）
DOCUMENT_TYPES = [
    "ADR", "Spec", "Plan", "Task", "Runbook", "Glossary", "Architecture",
    "Skill", "Workflow", "Script", "Handoff", "Audit", "Session Note",
]

# 依赖前沿被视为「已就绪」的任务状态
FRONTIER_READY_STATUSES = {"completed", "approved"}

TODAY = datetime.date.today().isoformat()

AGENTS_POINTER_TEMPLATE = """---
doc_id: AGENTS
type: adapter-entry
status: active
owner: {owner}
created: {date}
updated: {date}
---

# AGENTS.md

本项目采用 **Agent Workspace Governance** 治理工具包。

> 本文件是指针入口，不含规则正文（由 `governance.py init` 生成，可安全重复执行）。

- 权威规则：`agent-workspace-governance/constitution/`
- 通用入口说明：`agent-workspace-governance/AGENTS.md`
- 治理 CLI：`agent-workspace-governance/cli/governance.py`
- 状态目录：`.governance/`

进入项目的 Agent 请先读取上述权威规则，并在 Agent 注册表登记身份与能力；
未验证的能力标记 `unverified`。正式文档单一权威来源，人工决策不可被 AI 替代。
"""


# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------

def _now() -> str:
    return TODAY


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def _read_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _safe_read_json(path: str):
    """只读地读取 JSON，返回 (data, error)。文件不存在视为空（error=None）。

    用于 doctor 等诊断命令：绝不写文件，且能捕获 JSON 解析错误。
    """
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh), None
    except (ValueError, UnicodeDecodeError) as exc:
        return None, "JSON 解析失败：{}".format(exc)


def _write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def _state_path(project_path: str, filename: str) -> str:
    return os.path.join(os.path.abspath(project_path), STATE_DIR, filename)


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _parse_scalar(value: str):
    """将 frontmatter 标量字符串解析为 Python 值。"""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_strip_quotes(part) for part in inner.split(",")]
    text = _strip_quotes(value)
    low = text.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none", "~"):
        return None
    if re.fullmatch(r"-?\d+", text):
        try:
            return int(text)
        except ValueError:
            pass
    if re.fullmatch(r"-?\d+\.\d+", text):
        try:
            return float(text)
        except ValueError:
            pass
    return text


def parse_frontmatter(text: str) -> dict:
    """解析文档顶部的 YAML 风格 frontmatter。

    仅依赖标准库，支持 key: value、行内列表 [a, b]、块列表 - item、
    引号字符串、布尔值、数字与 null。无 frontmatter 时返回 {}。
    """
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() in ("---", "..."):
            end = idx
            break
    if end is None:
        return {}

    data: dict = {}
    idx = 1
    while idx < end:
        line = lines[idx]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            idx += 1
            continue
        if ":" not in line:
            idx += 1
            continue

        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()

        if raw == "":
            # 可能是块列表
            items = []
            jdx = idx + 1
            while jdx < end and lines[jdx].strip().startswith("- "):
                items.append(_strip_quotes(lines[jdx].strip()[2:].strip()))
                jdx += 1
            if items:
                data[key] = items
                idx = jdx
                continue
            data[key] = ""
            idx += 1
            continue

        data[key] = _parse_scalar(raw)
        idx += 1

    return data


def _fill_template(text: str, mapping: dict, default: str = "（待补充）") -> str:
    """替换模板中的 {{KEY}} 占位符；未提供的占位符填 default。"""
    def repl(match):
        key = match.group(1).strip()
        value = mapping.get(key, default)
        if value is None:
            value = ""
        return str(value)

    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", repl, text)


IGNORE_DIRS = {
    "node_modules", "vendor", "dist", "build", "out", "target",
    "__pycache__", ".temp", ".venv", "venv",
}


def scan_markdown_docs(project_path: str):
    """扫描项目中的 Markdown 文档，返回 [(abs_path, rel_path, text)]。

    跳过 .governance、所有以 '.' 开头的目录/文件，以及常见依赖/构建目录
    （node_modules/vendor/dist 等——真实项目适配发现的缺口，2026-11-21）。
    """
    root = os.path.abspath(project_path)
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d != STATE_DIR and d not in IGNORE_DIRS
        ]
        for name in filenames:
            if not name.endswith(".md") or name.startswith("."):
                continue
            abs_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(abs_path, root).replace(os.sep, "/")
            text = _read_text(abs_path)
            results.append((abs_path, rel_path, text))
    results.sort(key=lambda item: item[1])
    return results


# ---------------------------------------------------------------------------
# 1. init
# ---------------------------------------------------------------------------

def init_project(project_path: str) -> list:
    """初始化治理配置（幂等）。返回本次新建的文件路径列表。"""
    project_path = os.path.abspath(project_path)
    state = os.path.join(project_path, STATE_DIR)
    os.makedirs(state, exist_ok=True)
    created = []

    config_path = os.path.join(state, CONFIG_FILE)
    if not os.path.exists(config_path):
        config = {
            "project_id": os.path.basename(project_path),
            "name": os.path.basename(project_path),
            "description": "由 governance.py init 初始化的治理配置。",
            "version": "0.1.0",
            "owner": "human",
            "doc_root": ".",
            "state_dir": STATE_DIR,
            "doc_levels": ["L1", "L2", "L3"],
            "lifecycles": {
                "general": ["draft", "proposed", "under_review", "approved",
                            "active", "superseded", "archived"],
                "change_proposal": ["draft", "proposed", "approved", "implementing",
                                    "verifying", "completed", "archived"],
                "adr": ["proposed", "accepted", "deprecated", "superseded"],
            },
            "registries": {
                "document": REGISTRY_DOC,
                "task": REGISTRY_TASK,
                "agent": REGISTRY_AGENT,
                "adr": REGISTRY_ADR,
            },
            "adapters": ["generic"],
            "created_at": _now(),
            "updated_at": _now(),
        }
        _write_json(config_path, config)
        created.append(config_path)

    skeletons = [
        (REGISTRY_DOC, {"documents": [], "updated_at": _now()}),
        (REGISTRY_TASK, {"tasks": [], "updated_at": _now()}),
        (REGISTRY_AGENT, {"agents": [], "updated_at": _now()}),
        (REGISTRY_ADR, {"adrs": [], "updated_at": _now()}),
    ]
    for filename, initial in skeletons:
        path = os.path.join(state, filename)
        if not os.path.exists(path):
            _write_json(path, initial)
            created.append(path)

    agents_path = os.path.join(project_path, AGENTS_FILE)
    if not os.path.exists(agents_path):
        content = AGENTS_POINTER_TEMPLATE.format(owner="human", date=_now())
        _write_text(agents_path, content)
        created.append(agents_path)

    return created


# ---------------------------------------------------------------------------
# 2. inventory
# ---------------------------------------------------------------------------

def _record_from_doc(rel_path: str, fm: dict) -> dict:
    """根据 frontmatter 构造文档注册表条目。"""
    return {
        "document_id": str(fm.get("doc_id") or os.path.splitext(rel_path)[0]),
        "path": rel_path,
        "type": str(fm.get("type") or "unknown"),
        "level": fm.get("level"),
        "status": str(fm.get("status") or "unknown"),
        "owner": str(fm.get("owner") or ""),
        "created_at": str(fm.get("created") or fm.get("created_at") or ""),
        "updated_at": str(fm.get("updated") or fm.get("updated_at") or ""),
        "source_of_truth": fm.get("source_of_truth"),
        "generated": bool(fm.get("generated", False)),
        "related_task": fm.get("related_task"),
        "related_adr": fm.get("related_adr"),
        "related_documents": fm.get("related_documents") or [],
        "replaces": fm.get("replaces"),
        "superseded_by": fm.get("superseded_by"),
        "retention_policy": str(fm.get("retention_policy") or ""),
        "title": str(fm.get("title") or ""),
    }


def inventory_docs(project_path: str) -> list:
    """扫描项目文档并登记到文档注册表（按 document_id 去重、upsert）。

    返回本次登记/更新的 document_id 列表。
    """
    registry_path = _state_path(project_path, REGISTRY_DOC)
    registry = _read_json(registry_path)
    if registry is None:
        registry = {"documents": [], "updated_at": _now()}

    documents = registry.setdefault("documents", [])
    by_id = {d.get("document_id"): d for d in documents}

    touched = []
    for abs_path, rel_path, text in scan_markdown_docs(project_path):
        fm = parse_frontmatter(text)
        record = _record_from_doc(rel_path, fm)
        doc_id = record["document_id"]
        if doc_id in by_id:
            by_id[doc_id].update(record)
        else:
            documents.append(record)
            by_id[doc_id] = record
        touched.append(doc_id)

    registry["updated_at"] = _now()
    _write_json(registry_path, registry)
    return touched


# ---------------------------------------------------------------------------
# 3. validate
# ---------------------------------------------------------------------------

def validate(project_path: str) -> dict:
    """校验 frontmatter、必填字段与引用完整性。

    返回 {'errors': [...], 'checked_docs': int, 'checked_entries': int}。
    """
    errors = []
    checked_docs = 0
    for abs_path, rel_path, text in scan_markdown_docs(project_path):
        checked_docs += 1
        fm = parse_frontmatter(text)
        if not fm:
            errors.append(f"{rel_path}: 缺少 frontmatter")
            continue
        for field in REQUIRED_FM:
            value = fm.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"{rel_path}: 缺少必填字段 '{field}'")

    # 校验注册表中的必填字段与引用
    registry_path = _state_path(project_path, REGISTRY_DOC)
    registry = _read_json(registry_path) or {"documents": []}
    documents = registry.get("documents", [])
    checked_entries = len(documents)
    ids = {d.get("document_id") for d in documents}

    for entry in documents:
        path = entry.get("path", "<未知路径>")
        for field in ("document_id", "path", "type", "status", "owner",
                      "created_at", "updated_at"):
            value = entry.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"注册表条目 {path}: 缺少必填字段 '{field}'")
        # 引用完整性
        for ref_field in ("replaces", "superseded_by", "related_adr"):
            ref = entry.get(ref_field)
            if isinstance(ref, str) and ref.strip() and ref not in ids:
                errors.append(f"注册表条目 {path}: {ref_field} 引用不存在的文档 '{ref}'")

    return {
        "errors": errors,
        "checked_docs": checked_docs,
        "checked_entries": checked_entries,
    }


# ---------------------------------------------------------------------------
# 4. status
# ---------------------------------------------------------------------------

def task_status(project_path: str) -> dict:
    """返回任务与审批状态。"""
    registry = _read_json(_state_path(project_path, REGISTRY_TASK)) or {"tasks": []}
    tasks = registry.get("tasks", [])
    pending = [
        t for t in tasks
        if t.get("human_approval_required") and t.get("status") not in ("completed", "archived")
    ]
    return {
        "tasks": [
            {
                "task_id": t.get("task_id"),
                "title": t.get("title"),
                "owner_agent": t.get("owner_agent"),
                "status": t.get("status"),
                "human_approval_required": bool(t.get("human_approval_required")),
            }
            for t in tasks
        ],
        "pending_approvals": [
            {
                "task_id": t.get("task_id"),
                "title": t.get("title"),
                "status": t.get("status"),
            }
            for t in pending
        ],
    }


# ---------------------------------------------------------------------------
# 5. map
# ---------------------------------------------------------------------------

def agent_map(project_path: str) -> dict:
    """返回 Agent / Skill / Tool / MCP 映射。"""
    registry = _read_json(_state_path(project_path, REGISTRY_AGENT)) or {"agents": []}
    agents = registry.get("agents", [])
    all_skills, all_mcp, all_tools = set(), set(), set()
    for a in agents:
        all_skills.update(a.get("supported_skills") or [])
        all_mcp.update(a.get("supported_mcp") or [])
        all_tools.update(a.get("supported_tools") or [])
    return {
        "agents": [
            {
                "agent_id": a.get("agent_id"),
                "agent_name": a.get("agent_name"),
                "provider": a.get("provider"),
                "harness": a.get("harness"),
                "model": a.get("model"),
                "invocation_mode": a.get("invocation_mode"),
                "parallel_capability": bool(a.get("parallel_capability")),
                "background_task_capability": bool(a.get("background_task_capability")),
                "runtime_verification_status": a.get("runtime_verification_status", "unverified"),
                "supported_skills": a.get("supported_skills") or [],
                "supported_mcp": a.get("supported_mcp") or [],
                "supported_tools": a.get("supported_tools") or [],
            }
            for a in agents
        ],
        "skills": sorted(all_skills),
        "mcp": sorted(all_mcp),
        "tools": sorted(all_tools),
    }


# ---------------------------------------------------------------------------
# 6. handoff
# ---------------------------------------------------------------------------

def generate_handoff(project_path: str, task_id: str, to_agent: str | None = None) -> str | None:
    """从任务注册表生成标准交接文档，返回生成文件路径；任务不存在返回 None。"""
    registry = _read_json(_state_path(project_path, REGISTRY_TASK)) or {"tasks": []}
    task = next((t for t in registry.get("tasks", []) if t.get("task_id") == task_id), None)
    if task is None:
        return None

    template = _read_text(os.path.join(KIT_ROOT, "templates", "handoff.md"))
    mapping = {
        "TASK_ID": task.get("task_id", ""),
        "TITLE": task.get("title", ""),
        "STATUS": task.get("status", ""),
        "OWNER_AGENT": task.get("owner_agent", ""),
        "TO_AGENT": to_agent or "待定",
        "DATE": _now(),
        "READ_PATHS": ", ".join(task.get("read_paths") or []) or "无",
        "WRITE_PATHS": ", ".join(task.get("write_paths") or []) or "无",
        "PROTECTED_PATHS": ", ".join(task.get("protected_paths") or []) or "无",
        "DEPENDENCIES": ", ".join(task.get("dependencies") or []) or "无",
        "OUTPUTS": "\n".join("- " + o for o in (task.get("outputs") or [])) or "无",
        "ACCEPTANCE_CRITERIA": "\n".join(
            "- " + c for c in (task.get("acceptance_criteria") or [])
        ) or "无",
        "HUMAN_APPROVAL_REQUIRED": "是" if task.get("human_approval_required") else "否",
        "HANDOFF_NOTES": task.get("handoff_doc") or "无未决事项。",
    }
    content = _fill_template(template, mapping)
    out_dir = os.path.join(os.path.abspath(project_path), STATE_DIR, "handoffs")
    out_path = os.path.join(out_dir, "handoff-{}.md".format(task_id))
    _write_text(out_path, content)
    return out_path


# ---------------------------------------------------------------------------
# 7. adr
# ---------------------------------------------------------------------------

def adr_create(project_path: str, title: str, decision_type: str = "adr") -> dict:
    """创建 ADR：写入索引并生成 Markdown 文件。返回 ADR 记录。"""
    registry_path = _state_path(project_path, REGISTRY_ADR)
    registry = _read_json(registry_path)
    if registry is None:
        registry = {"adrs": [], "updated_at": _now()}
    adrs = registry.setdefault("adrs", [])

    numbers = []
    for a in adrs:
        match = re.search(r"(\d+)$", str(a.get("id", "")))
        if match:
            numbers.append(int(match.group(1)))
    next_num = max(numbers, default=0) + 1
    adr_id = "ADR-{:04d}".format(next_num)

    record = {
        "id": adr_id,
        "title": title,
        "date": _now(),
        "status": "proposed",
        "decision_type": decision_type,
        "context": "",
        "problem": "",
        "goals": [],
        "constraints": [],
        "options": [],
        "comparison": "",
        "decision": "",
        "rationale": "",
        "consequences": "",
        "supersession": {"supersedes": None, "superseded_by": None},
        "related_docs": [],
        "owner": "human",
        "human_approved": False,
    }
    adrs.append(record)
    registry["updated_at"] = _now()
    _write_json(registry_path, registry)

    # 生成 Markdown 文件
    template = _read_text(os.path.join(KIT_ROOT, "templates", "adr-template.md"))
    mapping = {
        "ADR_ID": adr_id,
        "TITLE": title,
        "DATE": _now(),
        "OWNER": "human",
    }
    content = _fill_template(template, mapping)
    adr_dir = os.path.join(os.path.abspath(project_path), "docs", "adr")
    _write_text(os.path.join(adr_dir, "{}.md".format(adr_id)), content)
    return record


def adr_list(project_path: str) -> list:
    """列出所有 ADR 记录。"""
    registry = _read_json(_state_path(project_path, REGISTRY_ADR)) or {"adrs": []}
    return registry.get("adrs", [])


def adr_check(project_path: str) -> dict:
    """检查 ADR：状态合法性、已决定 ADR 是否经人工批准、ADR 不自动 accepted。"""
    errors = []
    warnings = []
    for adr in adr_list(project_path):
        adr_id = adr.get("id", "<未命名>")
        status = adr.get("status")
        if status not in ADR_STATUSES:
            errors.append(f"{adr_id}: 非法状态 '{status}'")
        if adr.get("decision_type") != "adr":
            warnings.append(f"{adr_id}: decision_type 不是 'adr'，请确认是否应作为 ADR")
        if status in ADR_DECIDED and not adr.get("human_approved"):
            errors.append(f"{adr_id}: 状态为 '{status}' 但未记录人工批准（ADR 不得自动 accepted）")
    return {"errors": errors, "warnings": warnings, "checked": len(adr_list(project_path))}


# ---------------------------------------------------------------------------
# 8. archive-check
# ---------------------------------------------------------------------------

def _parse_date(value: str):
    try:
        return datetime.datetime.strptime(value[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def archive_check(project_path: str, max_age_days: int = 180) -> dict:
    """检查归档条件：过旧的 superseded 文档、已完成任务。"""
    today = datetime.date.today()
    candidates = []

    reg = _read_json(_state_path(project_path, REGISTRY_DOC)) or {"documents": []}
    for doc in reg.get("documents", []):
        if doc.get("status") == "superseded":
            updated = _parse_date(str(doc.get("updated_at", "")))
            if updated and (today - updated).days > max_age_days:
                candidates.append({
                    "kind": "document",
                    "id": doc.get("document_id"),
                    "reason": "superseded 且超过 {} 天未更新".format(max_age_days),
                })

    treg = _read_json(_state_path(project_path, REGISTRY_TASK)) or {"tasks": []}
    for task in treg.get("tasks", []):
        if task.get("status") == "completed":
            candidates.append({
                "kind": "task",
                "id": task.get("task_id"),
                "reason": "任务已完成，可归档（需人工审批）",
            })

    return {"archive_candidates": candidates}


# ---------------------------------------------------------------------------
# 9. audit
# ---------------------------------------------------------------------------

def audit(project_path: str) -> dict:
    """审计文档：冗余、孤儿、冲突、过期引用、未登记。"""
    reg = _read_json(_state_path(project_path, REGISTRY_DOC)) or {"documents": []}
    documents = reg.get("documents", [])
    ids = {d.get("document_id") for d in documents}
    paths = {d.get("path") for d in documents}

    # 未登记：扫描到但不在注册表
    unregistered = []
    for abs_path, rel_path, text in scan_markdown_docs(project_path):
        if rel_path not in paths:
            unregistered.append(rel_path)

    #  outgoing / incoming 引用关系
    outgoing = {}
    incoming = {doc_id: 0 for doc_id in ids}
    for doc in documents:
        doc_id = doc.get("document_id")
        refs = set(doc.get("related_documents") or [])
        for field in ("related_adr", "replaces", "superseded_by"):
            ref = doc.get(field)
            if isinstance(ref, str) and ref.strip():
                refs.add(ref)
        outgoing[doc_id] = refs
        for ref in refs:
            if ref in incoming:
                incoming[ref] += 1

    # 孤儿：既无出边也无入边
    orphans = [
        doc.get("document_id") for doc in documents
        if not outgoing.get(doc.get("document_id")) and incoming.get(doc.get("document_id"), 0) == 0
    ]

    # 冗余：重复 document_id / 重复 source_of_truth
    redundant = []
    seen_ids = set()
    seen_sot = {}
    for doc in documents:
        doc_id = doc.get("document_id")
        if doc_id in seen_ids:
            redundant.append(f"重复 document_id: {doc_id}")
        seen_ids.add(doc_id)
        sot = doc.get("source_of_truth")
        if isinstance(sot, str) and sot.strip():
            if sot in seen_sot:
                redundant.append(f"重复 source_of_truth '{sot}': {seen_sot[sot]} 与 {doc_id}")
            else:
                seen_sot[sot] = doc_id

    # 冲突：L3 文档却处于 active 状态
    conflicting = []
    for doc in documents:
        if doc.get("level") == "L3" and doc.get("status") == "active":
            conflicting.append(
                f"{doc.get('document_id')}: L3 归档文档却标记为 active"
            )
    # 任务写路径冲突（不同 owner 写同一路径）
    treg = _read_json(_state_path(project_path, REGISTRY_TASK)) or {"tasks": []}
    write_map = {}
    for task in treg.get("tasks", []):
        for path in task.get("write_paths") or []:
            write_map.setdefault(path, []).append(task.get("owner_agent"))
    for path, owners in write_map.items():
        if len(set(owners)) > 1:
            conflicting.append(f"写路径冲突 '{path}': 多个 owner {sorted(set(owners))}")

    # 过期引用：指向不存在的文档
    expired_reference = []
    for doc in documents:
        for ref_field in ("related_adr", "replaces", "superseded_by"):
            ref = doc.get(ref_field)
            if isinstance(ref, str) and ref.strip() and ref not in ids:
                expired_reference.append(
                    f"{doc.get('document_id')}: {ref_field} -> '{ref}' 不存在"
                )
        for ref in doc.get("related_documents") or []:
            if ref not in ids:
                expired_reference.append(
                    f"{doc.get('document_id')}: related_documents -> '{ref}' 不存在"
                )

    return {
        "redundant": redundant,
        "orphan": orphans,
        "conflicting": conflicting,
        "expired_reference": expired_reference,
        "unregistered": sorted(set(unregistered)),
    }


# ---------------------------------------------------------------------------
# 10. 协作协议纯函数（Task Claim / Single Writer / Dependency Frontier）
# ---------------------------------------------------------------------------

def _dependency_ids(task):
    """从任务提取依赖任务 ID 列表。

    兼容 `dependencies`（字符串数组）与 `dependency_frontier`
    （字符串数组或对象数组，对象取 task_id/id/task/dependency 键）。
    """
    ids = []
    for dep in (task.get("dependencies") or []):
        if isinstance(dep, str) and dep.strip() and dep.strip() not in ids:
            ids.append(dep.strip())
    for dep in (task.get("dependency_frontier") or []):
        if isinstance(dep, str) and dep.strip():
            if dep.strip() not in ids:
                ids.append(dep.strip())
        elif isinstance(dep, dict):
            for key in ("task_id", "id", "task", "dependency"):
                val = dep.get(key)
                if isinstance(val, str) and val.strip():
                    if val.strip() not in ids:
                        ids.append(val.strip())
                    break
    return ids


def claim_task(task_registry, task_id, agent, branch=None, now=None):
    """认领任务（Task Claim 协议）。返回 (更新后的注册表副本, 结果信息)。

    结果信息 dict 含 ok / task_id / error / task / claim_token。
    若任务已被其他 Agent 认领（owner_agent 不同且 status=in_progress），
    拒绝认领并在 error 中返回单写者冲突说明。纯函数，不修改入参。
    """
    if now is None:
        now = _now()
    result = {"ok": False, "task_id": task_id, "error": None,
              "task": None, "claim_token": None}
    registry = copy.deepcopy(task_registry) if isinstance(task_registry, dict) else {}
    tasks = registry.setdefault("tasks", [])
    task = next((t for t in tasks if t.get("task_id") == task_id), None)
    if task is None:
        result["error"] = "任务 '{}' 不存在，无法认领".format(task_id)
        return registry, result

    owner = task.get("owner_agent")
    if owner and owner != agent and task.get("status") == "in_progress":
        result["error"] = (
            "单写者冲突：任务 '{tid}' 已由 '{owner}' 认领且处于 in_progress，"
            "'{agent}' 不得重复认领（只能提交建议或独立补丁）"
        ).format(tid=task_id, owner=owner, agent=agent)
        return registry, result

    token = "claim-" + hashlib.sha1(
        "{}|{}|{}".format(task_id, agent, now).encode("utf-8")
    ).hexdigest()[:12]
    task["owner_agent"] = agent
    task["claimed_at"] = now
    task["claim_token"] = token
    task["status"] = "in_progress"
    if branch is not None:
        task["branch"] = branch
    task["updated_at"] = now
    result["ok"] = True
    result["task"] = task
    result["claim_token"] = token
    return registry, result


def check_frontier(task, task_registry):
    """检查任务依赖前沿是否全部就绪（completed / approved）。

    返回 (ready: bool, unsatisfied: list[str])。依赖任务不存在视为未满足。
    """
    tasks = (task_registry or {}).get("tasks", []) or []
    by_id = {t.get("task_id"): t for t in tasks}
    unsatisfied = []
    for dep_id in _dependency_ids(task):
        dep_task = by_id.get(dep_id)
        if dep_task is not None and dep_task.get("status") in FRONTIER_READY_STATUSES:
            continue
        unsatisfied.append(dep_id)
    return (len(unsatisfied) == 0, unsatisfied)


def detect_single_writer_conflicts(task_registry):
    """找出 write_paths 重叠、均 in_progress、owner 不同的任务对。

    返回冲突列表，每项为 dict：task_a / task_b / owner_a / owner_b / paths。
    """
    tasks = [t for t in ((task_registry or {}).get("tasks", []) or [])
             if t.get("status") == "in_progress"]
    conflicts = []
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            a, b = tasks[i], tasks[j]
            if a.get("owner_agent") == b.get("owner_agent"):
                continue
            overlap = sorted(set(a.get("write_paths") or []) &
                             set(b.get("write_paths") or []))
            if overlap:
                conflicts.append({
                    "task_a": a.get("task_id"),
                    "task_b": b.get("task_id"),
                    "owner_a": a.get("owner_agent"),
                    "owner_b": b.get("owner_agent"),
                    "paths": overlap,
                })
    return conflicts


def detect_dependency_cycles(task_registry):
    """检测任务依赖环，返回环列表（每环为任务 ID 列表）；空列表表示无环。"""
    tasks = (task_registry or {}).get("tasks", []) or []
    known_ids = {t.get("task_id") for t in tasks}
    graph = {}
    for t in tasks:
        tid = t.get("task_id")
        if tid is None:
            continue
        graph[tid] = [d for d in _dependency_ids(t) if d in known_ids]

    cycles = []
    seen = set()
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    stack = []

    def dfs(node):
        color[node] = GRAY
        stack.append(node)
        for nxt in graph.get(node, []):
            if color.get(nxt) == WHITE:
                dfs(nxt)
            elif color.get(nxt) == GRAY and nxt in stack:
                cycle = stack[stack.index(nxt):]
                key = tuple(sorted(cycle))
                if key not in seen:
                    seen.add(key)
                    cycles.append(list(cycle))
        stack.pop()
        color[node] = BLACK

    for node in list(graph.keys()):
        if color.get(node) == WHITE:
            dfs(node)
    return cycles


# ---------------------------------------------------------------------------
# 11. doctor（只读诊断）
# ---------------------------------------------------------------------------

def doctor(project_path: str) -> dict:
    """只读诊断：JSON 可解析、必填字段、type 枚举、单写者冲突、依赖环。

    返回 {'errors': [...], 'warnings': [...], 'checked_json': int,
          'checked_docs': int, 'single_writer_conflicts': [...],
          'dependency_cycles': [...]}。不写任何文件。
    """
    errors = []
    warnings = []
    state = os.path.join(os.path.abspath(project_path), STATE_DIR)
    json_files = [CONFIG_FILE, REGISTRY_DOC, REGISTRY_TASK, REGISTRY_AGENT, REGISTRY_ADR]
    data = {}
    checked_json = 0
    for name in json_files:
        content, err = _safe_read_json(os.path.join(state, name))
        if err:
            errors.append("{}: {}".format(name, err))
            continue
        if content is None:
            continue
        checked_json += 1
        data[name] = content

    # 文档注册表：必填字段 + type 枚举
    doc_reg = data.get(REGISTRY_DOC) or {}
    documents = doc_reg.get("documents", []) if isinstance(doc_reg, dict) else []
    checked_docs = 0
    for entry in documents:
        checked_docs += 1
        path_label = entry.get("path") or entry.get("document_id") or "<未知>"
        for field in ("document_id", "path", "type", "status", "owner",
                      "created_at", "updated_at"):
            value = entry.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append("注册表条目 {}: 缺少必填字段 '{}'".format(path_label, field))
        dtype = entry.get("type")
        if isinstance(dtype, str) and dtype.strip() and dtype not in DOCUMENT_TYPES:
            errors.append(
                "注册表条目 {}: type '{}' 不在 13 类标准枚举内".format(path_label, dtype))

    # 任务注册表：单写者冲突 + 依赖环
    task_reg = data.get(REGISTRY_TASK) or {}
    conflicts = detect_single_writer_conflicts(task_reg)
    for conflict in conflicts:
        errors.append(
            "单写者冲突：任务 '{}'({}) 与 '{}'({}) 同时写 [{}]".format(
                conflict["task_a"], conflict["owner_a"],
                conflict["task_b"], conflict["owner_b"],
                ", ".join(conflict["paths"])))
    cycles = detect_dependency_cycles(task_reg)
    for cycle in cycles:
        errors.append("依赖环：" + " -> ".join(cycle + [cycle[0]]))

    return {
        "errors": errors,
        "warnings": warnings,
        "checked_json": checked_json,
        "checked_docs": checked_docs,
        "single_writer_conflicts": conflicts,
        "dependency_cycles": cycles,
    }


# ---------------------------------------------------------------------------
# 输出格式化（供 CLI 使用）
# ---------------------------------------------------------------------------

def _print_block(title: str, lines) -> None:
    print("\n== {} ==".format(title))
    for line in lines:
        print("  - " + str(line))


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def _extract_project(argv):
    """从 argv 任意位置提取 --project/-p，返回 (project, 其余 argv)。"""
    project = None
    rest = []
    idx = 0
    while idx < len(argv):
        arg = argv[idx]
        if arg in ("--project", "-p"):
            if idx + 1 < len(argv):
                project = argv[idx + 1]
                idx += 2
                continue
            idx += 1
            continue
        if arg.startswith("--project="):
            project = arg.split("=", 1)[1]
            idx += 1
            continue
        rest.append(arg)
        idx += 1
    return project, rest


def main(argv=None) -> int:
    raw = list(argv) if argv is not None else list(sys.argv[1:])
    project_arg, rest = _extract_project(raw)

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--project", default=".", help="目标项目路径（默认当前目录）")

    parser = argparse.ArgumentParser(
        prog="governance.py",
        description="Agent Workspace Governance —— 可移植 Agent 项目治理工具包"
                    "（纯本地文件操作，不联网、不执行 git）",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", parents=[parent], help="初始化治理配置（幂等）")
    sub.add_parser("inventory", parents=[parent], help="扫描项目文档并登记到文档注册表")
    sub.add_parser("index", parents=[parent],
                   help="inventory 的别名：扫描项目文档并登记到文档注册表")
    sub.add_parser("validate", parents=[parent], help="校验 frontmatter、必填字段与引用")
    sub.add_parser("status", parents=[parent], help="展示任务与审批状态")
    sub.add_parser("map", parents=[parent], help="展示 Agent/Skill/Tool/MCP 映射")
    sub.add_parser("doctor", parents=[parent],
                   help="只读诊断：JSON/必填字段/type 枚举/单写者冲突/依赖环")

    handoff_p = sub.add_parser("handoff", parents=[parent], help="从任务生成交接文档")
    handoff_p.add_argument("--task", required=True, help="任务 ID")
    handoff_p.add_argument("--to", default=None, help="接手 Agent（可选）")

    adr_p = sub.add_parser("adr", parents=[parent], help="ADR 创建/列出/检查")
    adr_sub = adr_p.add_subparsers(dest="adr_command")
    adr_create_p = adr_sub.add_parser("create", help="创建 ADR")
    adr_create_p.add_argument("--title", required=True, help="ADR 标题")
    adr_sub.add_parser("list", help="列出 ADR")
    adr_sub.add_parser("check", help="检查 ADR")

    sub.add_parser("archive-check", parents=[parent], help="检查文档与任务的归档条件")
    sub.add_parser("audit", parents=[parent], help="审计冗余/孤儿/冲突/过期引用/未登记文档")

    args = parser.parse_args(rest)
    project = project_arg or getattr(args, "project", ".") or "."

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "init":
        created = init_project(project)
        if created:
            print("初始化完成，新建文件：")
            for path in created:
                print("  - " + path)
        else:
            print("已初始化，无需变更（幂等）。")

    elif args.command in ("inventory", "index"):
        # index 是 inventory 的别名，行为完全一致（保留 inventory 名向后兼容）
        touched = inventory_docs(project)
        print("已登记 {} 个文档：".format(len(touched)))
        for doc_id in touched:
            print("  - " + str(doc_id))

    elif args.command == "doctor":
        report = doctor(project)
        print("doctor 只读诊断：检查 {} 个 JSON 文件、{} 个注册表文档条目。".format(
            report["checked_json"], report["checked_docs"]))
        if report["single_writer_conflicts"]:
            _print_block("单写者冲突", [
                "'{}'({}) 与 '{}'({}) 同时写 [{}]".format(
                    c["task_a"], c["owner_a"], c["task_b"], c["owner_b"],
                    ", ".join(c["paths"]))
                for c in report["single_writer_conflicts"]
            ])
        if report["dependency_cycles"]:
            _print_block("依赖环", [
                " -> ".join(cycle + [cycle[0]])
                for cycle in report["dependency_cycles"]
            ])
        if report["errors"]:
            _print_block("错误", report["errors"])
            print("\n诊断发现问题：共 {} 项， doctor 返回非零退出码。".format(
                len(report["errors"])))
            return 1
        print("诊断通过：未发现 JSON/必填字段/type 枚举/单写者冲突/依赖环问题。")

    elif args.command == "validate":
        report = validate(project)
        print("已校验 {} 个文档，{} 个注册表条目。".format(
            report["checked_docs"], report["checked_entries"]))
        if report["errors"]:
            _print_block("错误", report["errors"])
            print("\n校验失败：共 {} 个问题。".format(len(report["errors"])))
            return 1
        print("校验通过，未发现问题。")

    elif args.command == "status":
        result = task_status(project)
        print("任务状态：")
        for task in result["tasks"]:
            print("  - {task_id} [{status}] {title} (owner: {owner_agent}, 需审批: {approval})".format(
                task_id=task["task_id"], status=task["status"], title=task["title"],
                owner_agent=task["owner_agent"],
                approval="是" if task["human_approval_required"] else "否"))
        _print_block("待人工审批", [
            "{task_id} [{status}] {title}".format(**t) for t in result["pending_approvals"]
        ] or ["无"])

    elif args.command == "map":
        result = agent_map(project)
        print("Agent 映射：")
        for agent in result["agents"]:
            print("  - {agent_id} ({provider}/{harness}) 验证状态={status} skills={skills} "
                  "mcp={mcp} tools={tools}".format(
                      agent_id=agent["agent_id"], provider=agent["provider"],
                      harness=agent["harness"], status=agent["runtime_verification_status"],
                      skills=agent["supported_skills"], mcp=agent["supported_mcp"],
                      tools=agent["supported_tools"]))
        _print_block("全部 Skills", result["skills"] or ["无"])
        _print_block("全部 MCP", result["mcp"] or ["无"])
        _print_block("全部 Tools", result["tools"] or ["无"])

    elif args.command == "handoff":
        path = generate_handoff(project, args.task, args.to)
        if path is None:
            print("错误：未找到任务 '{}'。".format(args.task))
            return 1
        print("已生成交接文档：" + path)

    elif args.command == "adr":
        cmd = getattr(args, "adr_command", None)
        if cmd == "create":
            record = adr_create(project, args.title)
            print("已创建 {}：{}（状态 proposed，需人工推进）".format(
                record["id"], record["title"]))
        elif cmd == "list":
            adrs = adr_list(project)
            if not adrs:
                print("暂无 ADR。")
            for adr in adrs:
                print("  - {id} [{status}] {title}".format(**adr))
        elif cmd == "check":
            report = adr_check(project)
            print("已检查 {} 个 ADR。".format(report["checked"]))
            if report["errors"]:
                _print_block("错误", report["errors"])
            if report["warnings"]:
                _print_block("警告", report["warnings"])
            if report["errors"]:
                return 1
            print("ADR 检查通过。")
        else:
            adr_p.print_help()

    elif args.command == "archive-check":
        result = archive_check(project)
        candidates = result["archive_candidates"]
        if candidates:
            print("归档候选：")
            for item in candidates:
                print("  - [{kind}] {id}: {reason}".format(**item))
        else:
            print("无归档候选。")

    elif args.command == "audit":
        result = audit(project)
        for key in ("redundant", "orphan", "conflicting", "expired_reference", "unregistered"):
            _print_block(key, result[key] or ["无"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
