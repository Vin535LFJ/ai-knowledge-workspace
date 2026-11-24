"""人工复核状态机：Discovered → Triaged → Watch → Research → Adopt → Ignore。

增量新增 canonical 生命周期 discovered/triaged/watchlist/deep_dive/adopted/rejected/archived，
旧状态通过别名双向兼容；详见文件末尾的 canonical 区块。

职责边界（强约束）：
- AI 负责发现、初筛、研究、评分与推荐；人类决定是否深入研究 / 采纳 / 入库。
- 任何状态转换都只记录状态与审计信息，绝不自动触发安装、导入或修改其他项目。
- 尤其 Adopt 只标记『已采纳』，不会把内容写入 Render_Notes 或任何外部知识库。
"""

from typing import Any, Dict, Optional

from .storage import Storage

STATES = ["Discovered", "Triaged", "Watch", "Research", "Adopt", "Ignore"]

ALLOWED_TRANSITIONS: Dict[str, set] = {
    "Discovered": {"Triaged", "Ignore"},
    "Triaged": {"Watch", "Research", "Ignore"},
    "Watch": {"Research", "Ignore"},
    "Research": {"Adopt", "Watch", "Ignore"},
    "Adopt": {"Ignore"},
    "Ignore": {"Triaged"},
}

# 禁止任何自动副作用：仅允许的状态写入，不触发外部动作
SIDE_EFFECT_FORBIDDEN = True


class ReviewStateMachine:
    def __init__(self, storage: Storage):
        self.storage = storage

    def allowed_targets(self, current: str) -> set:
        return set(ALLOWED_TRANSITIONS.get(current, set()))

    def validate(self, current: str, target: str) -> None:
        if current not in STATES:
            raise ValueError(f"未知当前状态: {current}")
        if target not in STATES:
            raise ValueError(f"未知目标状态: {target}")
        if target not in self.allowed_targets(current):
            raise ValueError(f"非法状态转换: {current} → {target}")

    def transition(
        self,
        candidate_id: int,
        current: str,
        target: str,
        reviewer: str,
        decision: str,
        research_objective: str = "",
    ) -> Dict[str, Any]:
        """执行一次人工复核转换；仅记录状态与审计，无外部副作用。"""
        self.validate(current, target)
        # 安全护栏：转换逻辑不得包含任何 install/import/write-external 行为。
        if SIDE_EFFECT_FORBIDDEN:
            self.storage.update_candidate_review(
                candidate_id=candidate_id,
                review_status=target,
                reviewer=reviewer,
                decision=decision,
                research_objective=research_objective,
            )
        return {
            "candidate_id": candidate_id,
            "from": current,
            "to": target,
            "reviewer": reviewer,
            "decision": decision,
            "auto_side_effects": [],
            "note": "本次转换仅记录状态与审计信息，未触发安装/导入/修改任何外部项目；"
            + ("Adopt 仅标记采纳，不会导入 Render_Notes。" if target == "Adopt" else ""),
        }


# =====================================================================
# canonical 生命周期（增量新增；与上面的旧状态机 1:1 兼容）
# ---------------------------------------------------------------------
# 新文档定义的 canonical 状态：
#   discovered → triaged → watchlist → deep_dive → adopted / rejected / archived
# 旧状态 Watch/Research/Adopt/Ignore 作为 1:1 别名保留，fixtures 中的旧值仍可读。
# 去重口径：按 repository_id 去重；rename/transfer 保留历史映射（见 docs/data-model.md）。
# =====================================================================

CANONICAL_STATES = [
    "discovered", "triaged", "watchlist", "deep_dive", "adopted", "rejected", "archived",
]

# 旧别名 → canonical（Discovered/Triaged 仅大小写差异，也纳入映射）
LEGACY_TO_CANONICAL: Dict[str, str] = {
    "Discovered": "discovered",
    "Triaged": "triaged",
    "Watch": "watchlist",
    "Research": "deep_dive",
    "Adopt": "adopted",
    "Ignore": "rejected",
}

# canonical → 旧别名（archived 无旧别名，返回自身）
CANONICAL_TO_LEGACY: Dict[str, str] = {v: k for k, v in LEGACY_TO_CANONICAL.items()}

# canonical 生命周期允许的转换（描述性定义，不在旧状态机上强制）
CANONICAL_ALLOWED_TRANSITIONS: Dict[str, set] = {
    "discovered": {"triaged"},
    "triaged": {"watchlist", "deep_dive", "rejected"},
    "watchlist": {"deep_dive", "rejected"},
    "deep_dive": {"adopted", "rejected", "watchlist"},
    "adopted": {"archived"},
    "rejected": {"archived"},
    "archived": set(),
}


def normalize_status(status: Optional[str]) -> Optional[str]:
    """把任意旧别名或 canonical 值归一化为 canonical 状态。

    - 已是 canonical（小写）→ 原样返回；
    - 旧别名（如 Research/Adopt）→ 返回对应 canonical；
    - 大小写不同的 canonical（如 WATCHLIST）→ 返回小写 canonical；
    - 未知值 → 原样返回，保证 fixtures 中的历史值仍可被读取而不报错。
    """
    if status is None:
        return None
    key = str(status).strip()
    if key in LEGACY_TO_CANONICAL:
        return LEGACY_TO_CANONICAL[key]
    if key in CANONICAL_STATES:
        return key
    if key.lower() in CANONICAL_STATES:
        return key.lower()
    # 兼容首字母大写的 canonical 写法，如 "Deep_Dive"
    lowered = key.lower()
    for canonical in CANONICAL_STATES:
        if canonical.lower() == lowered:
            return canonical
    return key


def to_legacy_status(status: Optional[str]) -> Optional[str]:
    """把 canonical 值转回旧别名；非 canonical 值原样返回（双向兼容）。"""
    if status is None:
        return None
    canonical = normalize_status(status)
    return CANONICAL_TO_LEGACY.get(canonical, status)


def record_transition(
    from_status: Optional[str],
    to_status: Optional[str],
    operator: str,
    reason: str,
    at: Optional[str] = None,
) -> Dict[str, Any]:
    """生成一条状态变更记录（时间/操作人/理由 + 归一化前后状态）。

    现有存储已有 review_log（reviewer/at/from/to/decision），此函数用于
    需要独立审计记录的调用方；不触发任何外部副作用。
    """
    from .models import utc_now_iso

    return {
        "from": normalize_status(from_status),
        "from_raw": from_status,
        "to": normalize_status(to_status),
        "to_raw": to_status,
        "operator": operator,
        "reason": reason,
        "at": at or utc_now_iso(),
    }
