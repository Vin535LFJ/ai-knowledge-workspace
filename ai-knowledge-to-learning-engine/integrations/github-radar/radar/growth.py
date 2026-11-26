"""增长分析：基于每日快照计算 24h/7d/30d 增长、Fork 增长、活跃度与加速度。

关键约束：快照历史不足时（例如仅 1 个快照）返回 insufficient_history=true，
所有窗口指标为 None，绝不编造或外推 7d/30d 数字。
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from .models import Snapshot


def _parse_time(value: str) -> datetime:
    """解析 ISO-8601 时间（兼容 Z 后缀）。"""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _nearest_before(snaps: List[Snapshot], target: datetime) -> Optional[Snapshot]:
    """返回不晚于 target 的最近一个快照（避免未来数据污染）。"""
    candidates = [s for s in snaps if _parse_time(s.captured_at) <= target]
    if not candidates:
        return None
    return max(candidates, key=lambda s: _parse_time(s.captured_at))


def _delta(latest: Snapshot, base: Optional[Snapshot], field: str) -> Optional[int]:
    if base is None:
        return None
    return int(getattr(latest, field)) - int(getattr(base, field))


def compute_growth(snaps: List[Snapshot], now: Optional[str] = None) -> Dict[str, Any]:
    """计算增长指标。

    snaps 需按 captured_at 升序。now 默认使用最后一个快照时间，
    以保证离线测试可复现（不依赖真实当前时间）。
    """
    result: Dict[str, Any] = {
        "insufficient_history": False,
        "snapshot_count": len(snaps),
        "window_days": [1, 7, 30],
        "star_growth_24h": None,
        "star_growth_7d": None,
        "star_growth_30d": None,
        "fork_growth_7d": None,
        "star_growth_rate_7d": None,
        "activity": {},
        "acceleration": None,
        "basis": {},
        "note": "",
    }
    if not snaps:
        result["insufficient_history"] = True
        result["note"] = "没有快照数据，无法计算增长。"
        return result

    snaps = sorted(snaps, key=lambda s: _parse_time(s.captured_at))
    latest = snaps[-1]
    anchor = _parse_time(now) if now else _parse_time(latest.captured_at)
    result["basis"]["latest_captured_at"] = latest.captured_at
    result["basis"]["latest_stars"] = latest.stargazers_count

    # 历史跨度
    span_days = (anchor - _parse_time(snaps[0].captured_at)).total_seconds() / 86400.0
    result["basis"]["history_span_days"] = round(span_days, 2)

    # 至少 2 个快照才计算任何增长窗口
    if len(snaps) < 2:
        result["insufficient_history"] = True
        result["note"] = "快照数量不足（<2），无法计算增长；7d/30d 指标留空而非编造。"
        return result

    for days, key in [(1, "star_growth_24h"), (7, "star_growth_7d"), (30, "star_growth_30d")]:
        base = _nearest_before(snaps, anchor - timedelta(days=days))
        result[key] = _delta(latest, base, "stargazers_count")
        result["basis"][key + "_base_captured_at"] = base.captured_at if base else None

    base7 = _nearest_before(snaps, anchor - timedelta(days=7))
    result["fork_growth_7d"] = _delta(latest, base7, "forks_count")
    if base7 and base7.stargazers_count:
        result["star_growth_rate_7d"] = round(
            (result["star_growth_7d"] or 0) / base7.stargazers_count, 4
        )

    # 活跃度：pushed_at 距 anchor 的天数
    activity: Dict[str, Any] = {}
    if latest.pushed_at:
        try:
            pushed_age_days = (anchor - _parse_time(latest.pushed_at)).total_seconds() / 86400.0
            activity["days_since_push"] = round(pushed_age_days, 2)
            activity["active_recently"] = pushed_age_days <= 30
        except (ValueError, TypeError):
            activity["days_since_push"] = None
            activity["active_recently"] = False
    else:
        activity["days_since_push"] = None
        activity["active_recently"] = False
    result["activity"] = activity

    # 加速度：最近 7 天增长 vs 之前 7 天增长
    if result["star_growth_7d"] is not None:
        prior_end = anchor - timedelta(days=7)
        prior_start = anchor - timedelta(days=14)
        prior_base = _nearest_before(snaps, prior_start)
        prior_end_snap = _nearest_before(snaps, prior_end)
        if prior_base and prior_end_snap:
            prior_growth = (
                int(prior_end_snap.stargazers_count) - int(prior_base.stargazers_count)
            )
            recent_growth = result["star_growth_7d"]
            result["acceleration"] = {
                "recent_7d": recent_growth,
                "prior_7d": prior_growth,
                "accelerating": recent_growth > prior_growth,
            }
            result["basis"]["acceleration_prior_base"] = prior_base.captured_at
            result["basis"]["acceleration_prior_end"] = prior_end_snap.captured_at

    # 判断哪些窗口数据充分
    lacking = [k for k in ["star_growth_7d", "star_growth_30d"] if result.get(k) is None]
    if lacking:
        result["insufficient_history"] = True
        result["note"] = "以下窗口缺少足够历史，指标留空（未编造）：" + ", ".join(lacking)
    return result
