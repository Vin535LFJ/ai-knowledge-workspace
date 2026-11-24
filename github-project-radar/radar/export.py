"""研究任务导出：生成交给知识到学习引擎（Render_Notes）的标准研究任务 JSON。

本模块是纯输出模块：只把结果写入调用方指定的文件，绝不包含任何写入
Render_Notes 或其他项目的代码。导入由外部引擎自行决定。
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .storage import Storage

GITHUB_URL_TEMPLATE = "https://github.com/{full_name}"

# 期望导出的字段集合（用于自检）
EXPORT_FIELDS = [
    "candidate_id",
    "repository",
    "url",
    "topic",
    "discovery_reason",
    "star_metrics",
    "evaluation",
    "review_status",
    "research_objective",
    "created_at",
    # 人工选择标志 + 溯源字段（增量新增）
    "human_selected_for_research",
    "source_url",
    "observed_at",
    "retrieved_at",
    "data_quality",
]


def _provenance(row: Dict[str, Any], repo: Dict[str, Any], field: str) -> Any:
    """溯源字段优先取候选记录，其次取仓库记录；均缺失时为 None。"""
    if row.get(field) is not None:
        return row.get(field)
    return repo.get(field)


def build_research_task(row: Dict[str, Any], repo: Dict[str, Any], latest_snapshot: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """把候选记录组装为一条标准研究任务。"""
    dims = (row.get("evaluation") or {}).get("dimensions", {})
    growth_basis = dims.get("growth_momentum", {}).get("basis", {})
    return {
        "candidate_id": row.get("id"),
        "repository": repo.get("full_name"),
        "url": GITHUB_URL_TEMPLATE.format(full_name=repo.get("full_name", "")),
        "topic": row.get("topic"),
        "discovery_reason": row.get("discovery_reason", {}),
        "star_metrics": {
            "stargazers_count": latest_snapshot.get("stargazers_count") if latest_snapshot else None,
            "forks_count": latest_snapshot.get("forks_count") if latest_snapshot else None,
            "star_growth_7d": growth_basis.get("star_growth_7d"),
            "star_growth_30d": growth_basis.get("star_growth_30d"),
            "insufficient_history": (row.get("evaluation") or {}).get("insufficient_history", True),
        },
        "evaluation": row.get("evaluation", {}),
        "review_status": row.get("review_status", "Discovered"),
        "research_objective": row.get("research_objective", ""),
        "created_at": row.get("created_at"),
        "human_selected_for_research": bool(row.get("human_selected_for_research", False)),
        "source_url": _provenance(row, repo, "source_url"),
        "observed_at": _provenance(row, repo, "observed_at"),
        "retrieved_at": _provenance(row, repo, "retrieved_at"),
        "data_quality": _provenance(row, repo, "data_quality"),
    }


def validate_task(task: Dict[str, Any]) -> None:
    """导出前自检字段完整性。"""
    missing = [f for f in EXPORT_FIELDS if f not in task]
    if missing:
        raise ValueError(f"研究任务缺少字段: {missing}")


def export_research_tasks(
    storage: Storage,
    output_path: str,
    review_status: str = "Research",
    only_approved: bool = False,
) -> Dict[str, Any]:
    """导出研究任务 JSON 到指定文件。纯输出，无外部副作用。

    only_approved=True 时，review_status 设为 approved_for_research（供引擎识别）。
    """
    candidates = storage.list_candidates(review_status=review_status)
    tasks: List[Dict[str, Any]] = []
    for row in candidates:
        repo_row = storage.get_repository(row["repository_id"])
        if not repo_row:
            continue
        snap = storage.get_latest_snapshot(row["repository_id"])
        task = build_research_task(
            row,
            repo_row.to_dict(),
            snap.to_dict() if snap else None,
        )
        if only_approved:
            task["review_status"] = "approved_for_research"
        validate_task(task)
        tasks.append(task)

    payload = {
        "schema_version": 1,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "task_count": len(tasks),
        "tasks": tasks,
    }
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return {"output": output_path, "count": len(tasks), "fields": EXPORT_FIELDS}
