"""周报生成：在 reports/YYYY-Www/ 下生成 7 个文件，覆盖 A–G 七个板块。

板块：
  A 每周崛起项目  B 潜力遗珠  C AI Agent 雷达  D Skills 雷达
  E MCP 雷达  F 工程雷达  G 图形与渲染雷达

所有结论基于库内快照/评分数据，数据不足的字段明确标注，不编造事实。
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from .storage import Storage


WEEK_SECTIONS = {
    "A": "每周崛起项目",
    "B": "潜力遗珠（低星标高质量）",
    "C": "AI Agent 雷达",
    "D": "Skills 雷达",
    "E": "MCP 雷达",
    "F": "工程雷达",
    "G": "图形与渲染雷达",
}

SECTION_TOPIC_MAP = {
    "C": "ai-agent",
    "D": "agent-skills",
    "E": "mcp-tools",
    "F": "knowledge-engineering",
    "G": "graphics-rendering",
}

REPORT_FILES = [
    "weekly-report.md",
    "star-growth.json",
    "rising-projects.md",
    "new-skills.md",
    "mcp-and-tools.md",
    "engineering-practices.md",
    "research-candidates.json",
]


def iso_week_label(now: Optional[datetime] = None) -> str:
    """返回 YYYY-Www 形式的周标签（ISO 周）。"""
    now = now or datetime.now(timezone.utc)
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"


def _frontmatter(doc_id: str, title: str, label: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return (
        "---\n"
        f'doc_id: "{doc_id}"\n'
        'type: "report"\n'
        'status: "generated"\n'
        'owner: "github-project-radar"\n'
        f'created: "{today}"\n'
        f'updated: "{today}"\n'
        f'title: "{title}"\n'
        f'week: "{label}"\n'
        "---\n\n"
    )


def build_report_data(storage: Storage, label: str) -> Dict[str, Any]:
    """从库中聚合生成报告所需的全部数据。"""
    candidates = storage.list_candidates()
    repos = {r.repository_id: r for r in storage.list_repositories()}

    enriched: List[Dict[str, Any]] = []
    for c in candidates:
        repo = repos.get(c["repository_id"])
        if not repo:
            continue
        latest = storage.get_latest_snapshot(c["repository_id"])
        enriched.append(
            {
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "topic": c["topic"],
                "review_status": c["review_status"],
                "evaluation": c.get("evaluation", {}),
                "discovery_reason": c.get("discovery_reason", {}),
                "stars": latest.stargazers_count if latest else 0,
                "stargrowth": (c.get("evaluation", {}).get("dimensions", {})
                               .get("growth_momentum", {})
                               .get("basis", {})
                               .get("star_growth_7d")),
            }
        )

    # A 崛起：按增长势能分排序
    rising = sorted(
        enriched,
        key=lambda e: e["evaluation"].get("dimensions", {}).get("growth_momentum", {}).get("score", 0),
        reverse=True,
    )
    # B 遗珠：低星标高总分
    hidden = sorted(
        [e for e in enriched if e["stars"] <= 500],
        key=lambda e: e["evaluation"].get("total", 0),
        reverse=True,
    )
    by_topic: Dict[str, List[Dict[str, Any]]] = {}
    for key, topic_id in SECTION_TOPIC_MAP.items():
        by_topic[key] = [e for e in enriched if e["topic"] == topic_id]

    return {
        "week": label,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": WEEK_SECTIONS,
        "rising": rising,
        "hidden_gems": hidden,
        "by_section": by_topic,
        "all": enriched,
    }


def _render_section_table(items: List[Dict[str, Any]]) -> str:
    if not items:
        return "_本周无符合条件的数据（数据不足，未编造）。_\n"
    lines = ["| 项目 | 主题 | 星标 | 总分 | 复核状态 |", "|---|---|---:|---:|---|"]
    for e in items[:15]:
        lines.append(
            f"| {e['full_name']} | {e['topic']} | {e['stars']} | "
            f"{e['evaluation'].get('total', 'N/A')} | {e['review_status']} |"
        )
    return "\n".join(lines) + "\n"


def generate_report(
    storage: Storage, reports_root: str, label: Optional[str] = None
) -> Dict[str, Any]:
    """生成整份周报目录与 7 个文件，返回生成结果。"""
    label = label or iso_week_label()
    out_dir = os.path.join(reports_root, label)
    os.makedirs(out_dir, exist_ok=True)
    data = build_report_data(storage, label)

    # 主报告（A–G）
    md = _frontmatter("weekly-report-" + label, "每周情报周报", label)
    md += f"# GitHub Project Radar 周报 · {label}\n\n"
    md += "本报告由系统基于库内快照与评分自动生成；一切结论以数据为依据，数据不足处已标注。\n\n"
    for key, title in WEEK_SECTIONS.items():
        md += f"## {key} · {title}\n\n"
        if key == "A":
            md += _render_section_table(data["rising"])
        elif key == "B":
            md += _render_section_table(data["hidden_gems"])
        else:
            md += _render_section_table(data["by_section"].get(key, []))
        md += "\n"

    # rising-projects.md
    rising_md = _frontmatter("rising-" + label, "每周崛起项目", label)
    rising_md += f"# A · 每周崛起项目（{label}）\n\n" + _render_section_table(data["rising"])

    # new-skills.md
    skills_md = _frontmatter("skills-" + label, "Skills 雷达", label)
    skills_md += f"# D · Skills 雷达（{label}）\n\n" + _render_section_table(data["by_section"].get("D", []))

    # mcp-and-tools.md
    mcp_md = _frontmatter("mcp-" + label, "MCP 与工具雷达", label)
    mcp_md += f"# E · MCP 雷达（{label}）\n\n" + _render_section_table(data["by_section"].get("E", []))

    # engineering-practices.md
    eng_md = _frontmatter("engineering-" + label, "工程雷达", label)
    eng_md += f"# F · 工程雷达（{label}）\n\n" + _render_section_table(data["by_section"].get("F", []))

    files = {
        "weekly-report.md": md,
        "rising-projects.md": rising_md,
        "new-skills.md": skills_md,
        "mcp-and-tools.md": mcp_md,
        "engineering-practices.md": eng_md,
        "star-growth.json": json.dumps(
            {
                "week": label,
                "items": [
                    {
                        "full_name": e["full_name"],
                        "stars": e["stars"],
                        "star_growth_7d": e["stargrowth"],
                        "topic": e["topic"],
                    }
                    for e in data["all"]
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "research-candidates.json": json.dumps(
            {
                "week": label,
                "candidates": [
                    {
                        "full_name": e["full_name"],
                        "topic": e["topic"],
                        "review_status": e["review_status"],
                        "total": e["evaluation"].get("total"),
                        "research_objective": e["evaluation"].get("research_objective", ""),
                    }
                    for e in data["all"]
                    if e["review_status"] in ("Research", "Adopt", "Watch")
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
    }
    written = []
    for name, content in files.items():
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content if content.endswith("\n") or name.endswith(".json") else content + "\n")
        written.append(path)
    return {"week": label, "directory": out_dir, "files": written, "count": len(written)}


# =====================================================================
# 新增报告格式（增量新增；上面的 generate_report 7 文件目录保持不变）
# ---------------------------------------------------------------------
# summary：单文件 Markdown 周报 reports_root/YYYY-Www.md，含 A–G 精简摘要。
# json    ：机器可读 reports_root/YYYY-Www.json。
# 周编号统一使用 datetime.isocalendar()，格式 YYYY-Www（零填充，如 2026-W47）。
# =====================================================================


def _sections_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """把 build_report_data 的结果整理为 A–G 七个板块的载荷。"""
    return {
        "A": {"title": WEEK_SECTIONS["A"], "items": data["rising"]},
        "B": {"title": WEEK_SECTIONS["B"], "items": data["hidden_gems"]},
        "C": {"title": WEEK_SECTIONS["C"], "items": data["by_section"].get("C", [])},
        "D": {"title": WEEK_SECTIONS["D"], "items": data["by_section"].get("D", [])},
        "E": {"title": WEEK_SECTIONS["E"], "items": data["by_section"].get("E", [])},
        "F": {"title": WEEK_SECTIONS["F"], "items": data["by_section"].get("F", [])},
        "G": {"title": WEEK_SECTIONS["G"], "items": data["by_section"].get("G", [])},
    }


def generate_summary_report(
    storage: Storage, reports_root: str, label: Optional[str] = None
) -> Dict[str, Any]:
    """生成单文件 Markdown 周报（含 A–G 七个板块的精简摘要）。"""
    label = label or iso_week_label()
    data = build_report_data(storage, label)
    sections = _sections_payload(data)

    md = _frontmatter("weekly-summary-" + label, "每周情报摘要", label)
    md += f"# GitHub Project Radar 周报摘要 · {label}\n\n"
    md += "单文件精简摘要，含 A–G 七个板块；结论基于库内快照与评分，数据不足处已标注，不编造事实。\n\n"
    for key in ["A", "B", "C", "D", "E", "F", "G"]:
        payload = sections[key]
        md += f"## {key} · {payload['title']}\n\n"
        md += _render_section_table(payload["items"])
        md += "\n"

    os.makedirs(reports_root, exist_ok=True)
    path = os.path.join(reports_root, f"{label}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(md)
    return {"week": label, "path": path, "sections": list(WEEK_SECTIONS.keys())}


def generate_json_report(
    storage: Storage, reports_root: str, label: Optional[str] = None
) -> Dict[str, Any]:
    """生成机器可读的 YYYY-Www.json 周报（含 A–G 七个板块）。"""
    label = label or iso_week_label()
    data = build_report_data(storage, label)
    sections = _sections_payload(data)
    payload = {
        "schema_version": 1,
        "week": label,
        "generated_at": data["generated_at"],
        "section_titles": WEEK_SECTIONS,
        "sections": sections,
        "candidate_count": len(data["all"]),
    }
    os.makedirs(reports_root, exist_ok=True)
    path = os.path.join(reports_root, f"{label}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return {"week": label, "path": path, "sections": list(WEEK_SECTIONS.keys())}
