"""深度研究模板渲染：为高价值项目生成结构化研究框架。

原则：模板只提供结构与可观测数据的占位，无法从库内数据验证的内容一律标注 [未验证]，
绝不把猜测当成事实陈述。研究者需逐项查证并移除标记。
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .storage import Storage

# D22 并入 Engine：默认输出锚定模块根（integrations/github-radar/research/），
# 不再依赖 CWD，避免从 Engine 根运行时把研究模板写进核心仓根目录。
MODULE_ROOT = Path(__file__).resolve().parent.parent

SECTIONS = [
    ("Executive Summary", "执行摘要"),
    ("Background", "背景"),
    ("Pain Points", "痛点"),
    ("Architecture", "架构"),
    ("Core Mechanism", "核心机制"),
    ("Key Implementation", "关键实现"),
    ("Advantages", "优势"),
    ("Disadvantages", "劣势"),
    ("Comparison", "对比"),
    ("Engineering Maturity", "工程成熟度"),
    ("Absorbable Designs", "可吸收的设计"),
    ("Further Research Decision", "进一步研究决定"),
    ("Sources", "资料来源"),
]


def render_research_template(
    repo: Dict[str, Any],
    evaluation: Dict[str, Any],
    research_objective: str = "",
    output_dir: str | None = None,
) -> Dict[str, Any]:
    """渲染单个项目的研究模板，返回 {filename, markdown, path?}。

    默认输出到模块根 research/owner__repo.md（文件名 = safe_name + '.md'）；
    传入 output_dir 可覆盖该默认路径（相对路径按 CWD 解析，调用方自行负责）。
    """
    full_name = repo.get("full_name", "unknown/unknown")
    safe_name = full_name.replace("/", "__")
    today = datetime.now(timezone.utc).date().isoformat()
    md = (
        "---\n"
        f'doc_id: "research-{safe_name}"\n'
        'type: "research"\n'
        'status: "template"\n'
        'owner: "github-project-radar"\n'
        f'created: "{today}"\n'
        f'updated: "{today}"\n'
        f'repository: "{full_name}"\n'
        "---\n\n"
    )
    md += f"# 深度研究：{full_name}\n\n"
    md += f"> 研究目标：{research_objective or '【待填写】'}  \n"
    md += f"> 评分总分：{evaluation.get('total', 'N/A')}  \n"
    md += "> 说明：所有 [未验证] 标记为待查证内容，查证后请移除标记并补充来源。\n\n"

    md += "## 可观测数据（来自库内快照 / 评分）\n\n"
    md += f"- 描述：{repo.get('description') or '[未验证]'}\n"
    md += f"- 语言：{repo.get('language') or '[未验证]'}\n"
    md += f"- 主题：{', '.join(repo.get('topics') or []) or '[未验证]'}\n"
    md += f"- 许可证：{repo.get('license') or '[未验证]'}\n"
    dims = evaluation.get("dimensions", {})
    for key, d in dims.items():
        md += f"- {key}：{d.get('score', 'N/A')} —— {d.get('reason', '[未验证]')}\n"
    md += "\n"

    for en, zh in SECTIONS:
        md += f"## {en} · {zh}\n\n"
        md += f"_【待研究】{zh}内容需查证后填写；未经证实的陈述必须保留 [未验证] 标记。_\n\n"

    filename = f"{safe_name}.md"
    result = {"filename": filename, "markdown": md, "path": None}
    if output_dir is None:
        output_dir = str(MODULE_ROOT / "research")
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(md)
        result["path"] = path
    return result


def render_from_candidate(
    storage: Storage, candidate_id: int, output_dir: str | None = None
) -> Dict[str, Any]:
    """根据候选 id 从库中组装仓库与评分数据并渲染模板。"""
    row = None
    for c in storage.list_candidates():
        if c.get("id") == candidate_id:
            row = c
            break
    if row is None:
        raise ValueError(f"候选记录不存在: id={candidate_id}")
    repo_row = storage.get_repository(row["repository_id"])
    if repo_row is None:
        raise ValueError(f"仓库不存在: id={row['repository_id']}")
    return render_research_template(
        repo_row.to_dict(),
        row.get("evaluation", {}),
        research_objective=row.get("research_objective", ""),
        output_dir=output_dir,
    )
