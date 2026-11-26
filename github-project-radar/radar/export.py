"""研究任务导出：生成交给知识到学习引擎（Render_Notes）的标准研究任务 JSON。

本模块是纯输出模块：只把结果写入调用方指定的文件，绝不包含任何写入
Render_Notes 或其他项目的代码。导入由外部引擎自行决定。

例外（仅限本系统自己的数据库）：`--approved` 是一次人工批准动作，必须把完整批准状态
同步写入本系统 SQLite（见 storage.approve_candidate），导出内容以数据库真实状态为准，
避免「报告显示 Approved 而导出/Intake 判定未经人工批准」的不一致。
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models import utc_now_iso
from .storage import APPROVED_REVIEW_STATUS, Storage

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
    """导出前自检：字段完整性 + Research Intake 契约（类型与人工门槛）。"""
    missing = [f for f in EXPORT_FIELDS if f not in task]
    if missing:
        raise ValueError(f"研究任务缺少字段: {missing}")
    validate_intake_task(task)


def validate_intake_task(task: Dict[str, Any]) -> None:
    """按 docs/engine-interface.md 的 Research Intake 契约校验单条记录。

    - 字段类型：布尔必须是 bool，ID 必须是整数，对象字段必须是 dict，文本字段必须是 str（溯源字段允许 null）。
    - 人工门槛：review_status 为 approved_for_research 的记录，human_selected_for_research 必须为 true。
    不满足即抛 ValueError，不做任何放宽或静默修正。
    """
    problems: List[str] = []
    bool_fields = ("human_selected_for_research",)
    int_fields = ("candidate_id",)
    dict_fields = ("discovery_reason", "star_metrics", "evaluation")
    text_fields = ("repository", "url", "topic", "review_status", "research_objective", "created_at")
    nullable_text_fields = ("source_url", "observed_at", "retrieved_at", "data_quality")
    for name in bool_fields:
        if type(task.get(name)) is not bool:
            problems.append(f"{name} 必须为 bool")
    for name in int_fields:
        if type(task.get(name)) is not int:
            problems.append(f"{name} 必须为 int")
    for name in dict_fields:
        if not isinstance(task.get(name), dict):
            problems.append(f"{name} 必须为 object")
    for name in text_fields:
        if not isinstance(task.get(name), str):
            problems.append(f"{name} 必须为 string")
    for name in nullable_text_fields:
        value = task.get(name)
        if value is not None and not isinstance(value, str):
            problems.append(f"{name} 必须为 string 或 null")
    if not problems and task["url"] != GITHUB_URL_TEMPLATE.format(full_name=task["repository"]):
        problems.append("url 与 repository 不一致")
    if task.get("review_status") == APPROVED_REVIEW_STATUS and task.get("human_selected_for_research") is not True:
        problems.append("review_status=approved_for_research 但 human_selected_for_research 不为 true（未经人工批准）")
    if problems:
        raise ValueError(f"研究任务不符合 Research Intake 契约: {problems}")


def export_research_tasks(
    storage: Storage,
    output_path: str,
    review_status: str = "Research",
    only_approved: bool = False,
    approver: Optional[str] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """导出研究任务 JSON 到指定文件。对 Render_Notes 等外部系统纯输出，无外部副作用。

    only_approved=True（人工批准）：
    1. 必须提供非空 approver，否则抛 ValueError；
    2. 对所选候选在数据库写入完整人工批准状态（storage.approve_candidate）；
       重复批准为 no-op，保留首次 approver / approved_at / approval_reason；
    3. 只导出数据库中 review_status=approved_for_research 的候选，且回读数据库真实状态组装任务。
    候选范围：review_status 等于 review_status 参数的行，加上（仅 only_approved 时）此前已批准的行。
    """
    candidates = storage.list_candidates()
    selected = [
        row
        for row in candidates
        if row["review_status"] == review_status
        or (only_approved and row["review_status"] == APPROVED_REVIEW_STATUS)
    ]

    approved_rows: Dict[int, Dict[str, Any]] = {}
    if only_approved:
        approver_name = (approver or "").strip()
        if not approver_name:
            raise ValueError("--approved 必须提供非空 approver（人工批准人）")
        approved_at = utc_now_iso()
        for row in selected:
            if row["review_status"] != APPROVED_REVIEW_STATUS:
                storage.approve_candidate(
                    row["id"], approver=approver_name, approved_at=approved_at, approval_reason=reason
                )
        # 回读：导出只能基于数据库真实状态，不得在导出层「改写」状态
        approved_rows = {
            row["id"]: row
            for row in storage.list_candidates(review_status=APPROVED_REVIEW_STATUS)
        }

    tasks: List[Dict[str, Any]] = []
    for row in selected:
        if only_approved:
            candidate_id = row["id"]
            row = approved_rows.get(candidate_id)
            if row is None:
                raise ValueError(f"候选 id={candidate_id} 未处于已批准状态，拒绝导出")
        repo_row = storage.get_repository(row["repository_id"])
        if not repo_row:
            continue
        snap = storage.get_latest_snapshot(row["repository_id"])
        task = build_research_task(
            row,
            repo_row.to_dict(),
            snap.to_dict() if snap else None,
        )
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
