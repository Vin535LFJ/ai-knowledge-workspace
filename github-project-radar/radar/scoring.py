"""加权评分：默认权重创新 25 / 相关性 25 / 工程成熟度 15 / 可复用性 15 / 增长势能 20。

设计要点：
- 权重来自 config/scoring.json，可配置。
- 每个维度输出 {score, reason, basis}，分数、理由与数据依据齐全。
- 增长势能直接消费 growth.compute_growth 的输出；历史不足时为 0（中性）并说明原因。
- 分组比较：不同主题组的仓库不做直接排名，compare_group 会拒绝跨组比较。
"""

from typing import Any, Dict, List, Optional

DEFAULT_WEIGHTS = {
    "innovation": 25,
    "relevance": 25,
    "engineering_maturity": 15,
    "reusability": 15,
    "growth_momentum": 20,
}

DIMENSIONS = list(DEFAULT_WEIGHTS.keys())

INNOVATION_HINTS = ["novel", "new", "framework", "engine", "protocol", "graph", "diffusion", "world model", "agent", "rag", "mcp"]


def _dim(score: float, reason: str, basis: Any) -> Dict[str, Any]:
    return {"score": round(score, 2), "reason": reason, "basis": basis}


def score_innovation(repo: Dict[str, Any], topic_group: str) -> Dict[str, Any]:
    text = (repo.get("description") or "").lower()
    topics = [str(t).lower() for t in (repo.get("topics") or [])]
    hits = [h for h in INNOVATION_HINTS if h in text or any(h in t for t in topics)]
    score = min(100.0, 40 + len(hits) * 12)
    return _dim(
        score,
        "基于描述/主题中的创新关键词命中度估计；关键词命中越多，创新信号越强（启发式，非事实断言）。"
        if hits
        else "未发现明显创新关键词，给出保守中性分（启发式）。",
        {"description": repo.get("description", ""), "topics": repo.get("topics", []), "keyword_hits": hits},
    )


def score_relevance(repo: Dict[str, Any], topic_config: Dict[str, Any], topic_group: str) -> Dict[str, Any]:
    group = next((t for t in topic_config.get("topics", []) if t.get("id") == topic_group), None)
    keywords = group.get("keywords", []) if group else []
    text = ((repo.get("description") or "") + " " + " ".join(repo.get("topics") or [])).lower()
    hits = [k for k in keywords if k.lower() in text]
    total = len(keywords) or 1
    score = min(100.0, 20 + len(hits) / total * 100)
    return _dim(
        score,
        f"与主题组『{topic_group}』关键词匹配 {len(hits)}/{total} 项。",
        {"topic_group": topic_group, "keyword_hits": hits, "keywords_total": total},
    )


def score_engineering_maturity(repo: Dict[str, Any]) -> Dict[str, Any]:
    score = 30.0
    checks = {}
    checks["has_license"] = bool(repo.get("license"))
    checks["has_homepage"] = bool(repo.get("homepage"))
    checks["has_topics"] = bool(repo.get("topics"))
    checks["has_description"] = bool(repo.get("description"))
    checks["has_recent_release"] = bool((repo.get("release_info") or {}).get("tag"))
    score += sum(10 for v in checks.values() if v)
    return _dim(
        score,
        "依据许可证、主页、主题、描述、最近发布等可观测信号评估工程成熟度。",
        checks,
    )


def score_reusability(repo: Dict[str, Any]) -> Dict[str, Any]:
    license_name = (repo.get("license") or "").upper()
    permissive = any(tag in license_name for tag in ["MIT", "APACHE", "BSD", "MPL", "ISC"])
    score = 30.0 + (30 if permissive else 0)
    score += 20 if repo.get("homepage") else 0
    score += 10 if repo.get("topics") else 0
    return _dim(
        score,
        "宽松许可证、文档主页与清晰主题提升可复用性；专有/无许可证降低可复用性。"
        if not permissive
        else "宽松许可证显著提升可复用性。",
        {
            "license": repo.get("license"),
            "permissive_license": permissive,
            "homepage": repo.get("homepage"),
        },
    )


def score_growth_momentum(growth: Dict[str, Any]) -> Dict[str, Any]:
    if growth.get("insufficient_history") or growth.get("star_growth_7d") is None:
        return _dim(
            0.0,
            "快照历史不足，增长势能记为 0（中性）；未使用或编造 7d/30d 增长数据。"
            + (" " + growth.get("note", "") if growth.get("note") else ""),
            {"insufficient_history": growth.get("insufficient_history", True), "snapshot_count": growth.get("snapshot_count", 0)},
        )
    g7 = growth.get("star_growth_7d") or 0
    rate = growth.get("star_growth_rate_7d")
    base = max(1.0, 1.0 + (rate or 0) * 10)
    score = max(0.0, min(100.0, 30 + g7 * 2 * base))
    accel = (growth.get("acceleration") or {}).get("accelerating")
    if accel:
        score = min(100.0, score + 10)
    return _dim(
        score,
        f"基于 7 日星标增长 {g7}、增长率 {rate} 与加速度 {'加速' if accel else '未加速'} 计算。",
        {"star_growth_7d": g7, "star_growth_rate_7d": rate, "acceleration": growth.get("acceleration")},
    )


def evaluate(
    repo: Dict[str, Any],
    topic_config: Dict[str, Any],
    growth: Dict[str, Any],
    topic_group: str,
    weights: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """返回完整评估：各维度明细 + 加权总分 + 分组标签。"""
    w = dict(weights or DEFAULT_WEIGHTS)
    dims = {
        "innovation": score_innovation(repo, topic_group),
        "relevance": score_relevance(repo, topic_config, topic_group),
        "engineering_maturity": score_engineering_maturity(repo),
        "reusability": score_reusability(repo),
        "growth_momentum": score_growth_momentum(growth),
    }
    total = 0.0
    weight_sum = 0.0
    for name, d in dims.items():
        weight = w.get(name, 0)
        weight_sum += weight
        total += d["score"] * weight / 100.0
    if weight_sum and abs(weight_sum - 100) > 0.01:
        total = total * 100.0 / weight_sum
    return {
        "dimensions": dims,
        "total": round(total, 2),
        "group": topic_group,
        "weights": w,
        "insufficient_history": growth.get("insufficient_history", False),
    }


def compare_group(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """仅在同组内比较排名；跨组混合时拒绝比较并说明原因。"""
    groups = {e.get("group") for e in evaluations}
    if len(groups) > 1:
        return {
            "comparable": False,
            "reason": "待比较项目属于不同主题组，不做直接排名（不同组的评分口径不可比）。",
            "groups": sorted(g for g in groups if g is not None),
            "ranking": [],
        }
    ranked = sorted(evaluations, key=lambda e: e.get("total", 0), reverse=True)
    return {
        "comparable": True,
        "reason": "同组内按加权总分排序。",
        "groups": list(groups),
        "ranking": [
            {"index": i + 1, "group": e.get("group"), "total": e.get("total")}
            for i, e in enumerate(ranked)
        ],
    }


# =====================================================================
# 三维独立评分（增量新增）
# ---------------------------------------------------------------------
# 与上面的 evaluate()/total 完全解耦：这里输出三个彼此独立的分数，
# 而不是再合成一个综合分。每个分数形如：
#   {"score": 数字或 "unknown", "explanation": 中文说明, "basis": [子信号, ...]}
# 规则完全确定性、由 config/scoring.json 的 three_scores 块驱动，可单测。
# 关键原则：字段缺失标 "unknown"，绝不默认满分或零分；只有可观测子信号
# 参与加权平均，全部缺失时整体分数才为 "unknown"。
# =====================================================================

THREE_SCORES_DEFAULTS: Dict[str, Any] = {
    "discovery_signal": {
        "dimensions": [
            "star_velocity_24h", "star_velocity_7d", "star_velocity_30d",
            "fork_growth_7d", "commit_activity", "novelty",
            "domain_attention", "contributor_change",
        ],
        "weights": {
            "star_velocity_24h": 10, "star_velocity_7d": 25,
            "star_velocity_30d": 15, "fork_growth_7d": 15,
            "commit_activity": 20, "novelty": 10,
            "domain_attention": 3, "contributor_change": 2,
        },
        "thresholds": {
            "velocity_cap_24h": 20, "velocity_cap_7d": 100,
            "velocity_cap_30d": 300, "fork_growth_cap": 30,
            "novelty_reference_date": "2026-11-19", "novelty_max_years": 3,
        },
    },
    "engineering_quality": {
        "dimensions": [
            "readme_clarity", "docs_runnable", "license", "release_activity",
            "issue_pr_maintenance", "community_activity", "testing_ci",
            "security_policy", "dependency_health", "code_structure",
            "single_maintainer_risk",
        ],
        "weights": {
            "readme_clarity": 20, "docs_runnable": 15, "license": 15,
            "release_activity": 10, "issue_pr_maintenance": 10,
            "community_activity": 15, "testing_ci": 5, "security_policy": 4,
            "dependency_health": 4, "code_structure": 2,
            "single_maintainer_risk": 0,
        },
        "thresholds": {"readme_full_length": 120, "issue_penalty_per_issue": 2},
    },
    "relevance": {
        "dimensions": ["engine", "agent_docs_governance", "radar", "web_teaching", "av_gpu"],
        "weights": {
            "engine": 25, "agent_docs_governance": 20, "radar": 20,
            "web_teaching": 20, "av_gpu": 15,
        },
        "group_match_bonus": 50,
        "dimension_keywords": {
            "engine": {
                "keywords": ["agent", "engine", "framework", "runtime", "orchestration", "memory", "harness"],
                "groups": ["ai-agent", "agent-skills"],
            },
            "agent_docs_governance": {
                "keywords": ["agents.md", "skills", "claude skill", "codex skill", "registry", "documentation", "governance"],
                "groups": ["agent-skills"],
            },
            "radar": {
                "keywords": ["rag", "knowledge graph", "graphrag", "retrieval", "research automation", "document intelligence", "radar"],
                "groups": ["knowledge-engineering"],
            },
            "web_teaching": {
                "keywords": ["tutor", "education", "interactive learning", "learning experience", "course", "teaching", "docs"],
                "groups": ["learning-education"],
            },
            "av_gpu": {
                "keywords": ["gpu", "webgpu", "vulkan", "render", "renderer", "3d", "shader", "video", "diffusion", "multimodal"],
                "groups": ["graphics-rendering", "extensions"],
            },
        },
    },
}


def _load_three_scores_config() -> Dict[str, Any]:
    """从 config/scoring.json 读取 three_scores；失败时回退到内置默认。"""
    try:
        from . import load_config

        cfg = load_config("scoring.json") or {}
        return cfg.get("three_scores") or {}
    except Exception:
        return {}


def _three_cfg() -> Dict[str, Any]:
    """内置默认与文件配置做浅合并（文件优先），保证确定性与向后兼容。"""
    merged: Dict[str, Any] = {k: dict(v) for k, v in THREE_SCORES_DEFAULTS.items()}
    for key, val in _load_three_scores_config().items():
        if isinstance(val, dict) and isinstance(merged.get(key), dict):
            sub = dict(merged[key])
            sub.update(val)
            merged[key] = sub
        else:
            merged[key] = val
    return merged


def _parse_iso_dt(value: str):
    """解析 ISO-8601（兼容 Z 后缀），无时区时按 UTC 处理。"""
    from datetime import datetime, timezone

    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _signal(name: str, status: str, value: Any = None, sub_score: Any = None, note: str = "") -> Dict[str, Any]:
    """构造一个子信号记录；status 为 ok 或 unknown。"""
    return {"name": name, "status": status, "value": value, "sub_score": sub_score, "note": note}


def _aggregate(signals: List[Dict[str, Any]], weights: Dict[str, Any]) -> Any:
    """对可观测子信号做加权平均；没有可观测子信号时返回 'unknown'。"""
    usable = [s for s in signals if s["status"] == "ok" and isinstance(s["sub_score"], (int, float))]
    if not usable:
        return "unknown"
    total_w = sum(float(weights.get(s["name"], 1)) for s in usable)
    if total_w <= 0:
        return "unknown"
    score = sum(float(s["sub_score"]) * float(weights.get(s["name"], 1)) for s in usable) / total_w
    return round(max(0.0, min(100.0, score)), 2)


def _velocity_score(delta: Any, cap: Any) -> float:
    """把增长量线性映射到 0-100（cap 对应 100 分），确定性。"""
    base = float(cap) or 1.0
    return round(max(0.0, min(100.0, float(delta) / base * 100.0)), 2)


def _novelty_score(created_at: str, reference: str, max_years: Any) -> Any:
    """基于创建时间距参考日的新颖度：越新分越高。"""
    try:
        age_days = (_parse_iso_dt(reference) - _parse_iso_dt(created_at)).days
        age_years = max(0.0, age_days / 365.25)
        return round(max(0.0, min(100.0, 100.0 - age_years / (float(max_years) or 1.0) * 100.0)), 2)
    except (ValueError, TypeError):
        return None


def _best_group(repo: Dict[str, Any], topic_config: Dict[str, Any]) -> Optional[str]:
    """按关键词命中数推断最匹配主题组；没有命中返回 None。"""
    text = ((repo.get("description") or "") + " " + " ".join(str(t) for t in (repo.get("topics") or []))
            + " " + str(repo.get("language") or "")).lower()
    best: Optional[str] = None
    best_hits = 0
    for topic in (topic_config or {}).get("topics", []):
        hits = sum(1 for k in topic.get("keywords", []) if str(k).lower() in text)
        if hits > best_hits:
            best, best_hits = topic.get("id"), hits
    return best


def _discovery_signals(repo: Dict[str, Any], growth: Optional[Dict[str, Any]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    g = growth or {}
    th = cfg.get("thresholds", {})
    signals: List[Dict[str, Any]] = []
    velocity_map = [
        ("star_growth_24h", "star_velocity_24h", "velocity_cap_24h"),
        ("star_growth_7d", "star_velocity_7d", "velocity_cap_7d"),
        ("star_growth_30d", "star_velocity_30d", "velocity_cap_30d"),
        ("fork_growth_7d", "fork_growth_7d", "fork_growth_cap"),
    ]
    for key, name, cap_key in velocity_map:
        if key in g and g[key] is not None:
            signals.append(_signal(
                name, "ok", g[key], _velocity_score(g[key], th.get(cap_key, 100)),
                f"来自 growth.{key}，按阈值 {th.get(cap_key, 100)} 映射。",
            ))
        else:
            signals.append(_signal(name, "unknown", None, None, f"缺少 growth.{key}（快照历史不足或未提供），不编造增长数据。"))

    activity = g.get("activity") or {}
    if "days_since_push" in activity and activity.get("days_since_push") is not None:
        days = float(activity["days_since_push"])
        signals.append(_signal(
            "commit_activity", "ok", days, round(max(0.0, min(100.0, 100.0 - days)), 2),
            "基于最近推送距今天数（越近越高）。",
        ))
    else:
        note = "缺少 growth.activity.days_since_push"
        if repo.get("pushed_at"):
            note += "（虽有 pushed_at，但缺少增长锚点，无法换算天数）"
        signals.append(_signal("commit_activity", "unknown", repo.get("pushed_at"), None, note + "。"))

    if repo.get("created_at"):
        sub = _novelty_score(
            repo["created_at"], th.get("novelty_reference_date", "2026-11-19"),
            th.get("novelty_max_years", 3),
        )
        if sub is None:
            signals.append(_signal("novelty", "unknown", repo.get("created_at"), None, "created_at 无法解析。"))
        else:
            signals.append(_signal("novelty", "ok", repo["created_at"], sub, "基于创建时间距参考日的新颖度。"))
    else:
        signals.append(_signal("novelty", "unknown", None, None, "缺少 created_at，无法评估相对新颖性。"))

    signals.append(_signal("domain_attention", "unknown", None, None, "当前仓库字段不含领域关注度/watcher 趋势，无法量化。"))
    signals.append(_signal("contributor_change", "unknown", None, None, "当前数据模型不含贡献者变化字段，无法量化。"))
    return signals


def _engineering_signals(repo: Dict[str, Any], growth: Optional[Dict[str, Any]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    th = cfg.get("thresholds", {})
    signals: List[Dict[str, Any]] = []

    if "description" in repo:
        length = len(str(repo.get("description") or ""))
        full = float(th.get("readme_full_length", 120)) or 120.0
        signals.append(_signal("readme_clarity", "ok", length, round(min(100.0, length / full * 100.0), 2),
                               "以描述/README 摘要长度作为清晰度代理指标。"))
    else:
        signals.append(_signal("readme_clarity", "unknown", None, None, "缺少 description，无法评估文档清晰度。"))

    if "homepage" in repo:
        signals.append(_signal("docs_runnable", "ok", repo.get("homepage"), 100.0 if repo.get("homepage") else 0.0,
                               "以是否提供可访问文档主页作为『文档可运行』代理指标。"))
    else:
        signals.append(_signal("docs_runnable", "unknown", None, None, "缺少 homepage，无法评估文档可运行性。"))

    if "license" in repo:
        lic = str(repo.get("license") or "").upper()
        permissive = any(t in lic for t in ["MIT", "APACHE", "BSD", "MPL", "ISC"])
        sub = 90.0 if permissive else (55.0 if lic else 10.0)
        signals.append(_signal("license", "ok", repo.get("license"), sub,
                               "识别许可证类型：宽松许可 90 / 有许可 55 / 无许可 10。"))
    else:
        signals.append(_signal("license", "unknown", None, None, "缺少 license 字段，无法判断许可证及类型。"))

    if "release_info" in repo:
        ri = repo.get("release_info") or {}
        tag = ri.get("tag") if isinstance(ri, dict) else ri
        signals.append(_signal("release_activity", "ok", ri, 100.0 if tag else 20.0,
                               "以是否存在最近 release 标签评估版本发布活跃度。"))
    else:
        signals.append(_signal("release_activity", "unknown", None, None, "缺少 release_info，无法评估版本发布。"))

    if "open_issues_count" in repo:
        issues = int(repo.get("open_issues_count") or 0)
        penalty = float(th.get("issue_penalty_per_issue", 2))
        signals.append(_signal("issue_pr_maintenance", "ok", issues,
                               round(max(0.0, min(100.0, 100.0 - issues * penalty)), 2),
                               "以未关闭 Issue 数量作为 Issue/PR 维护代理指标。"))
    else:
        signals.append(_signal("issue_pr_maintenance", "unknown", None, None, "缺少 open_issues_count，无法评估 Issue/PR 维护。"))

    activity = (growth or {}).get("activity") or {}
    if "active_recently" in activity:
        signals.append(_signal("community_activity", "ok", activity.get("active_recently"),
                               100.0 if activity.get("active_recently") else 30.0,
                               "基于最近推送是否活跃评估社区活跃度。"))
    else:
        signals.append(_signal("community_activity", "unknown", None, None, "缺少增长活动数据，无法评估社区活跃度。"))

    for name in ["testing_ci", "security_policy", "dependency_health", "code_structure", "single_maintainer_risk"]:
        signals.append(_signal(name, "unknown", None, None, "当前离线数据不含该维度可观测字段，标为 unknown（非 0 分）。"))
    return signals


def _relevance_signals(
    repo: Dict[str, Any], topic_config: Dict[str, Any], group: Optional[str], cfg: Dict[str, Any]
) -> List[Dict[str, Any]]:
    text = (
        (repo.get("description") or "") + " " + " ".join(str(t) for t in (repo.get("topics") or []))
        + " " + str(repo.get("language") or "")
    ).lower().strip()
    dims = cfg.get("dimensions", [])
    details = cfg.get("dimension_keywords", {})
    bonus = float(cfg.get("group_match_bonus", 50))
    signals: List[Dict[str, Any]] = []

    if not text and not group:
        for name in dims:
            signals.append(_signal(name, "unknown", None, None, "缺少描述/主题/语言且未指定主题组，无法评估对该生态维度的价值。"))
        return signals

    for name in dims:
        info = details.get(name) or {}
        keywords = info.get("keywords") or []
        if not keywords:
            signals.append(_signal(name, "unknown", None, None, "该生态维度未配置关键词。"))
            continue
        hits = [str(k) for k in keywords if str(k).lower() in text]
        base = len(hits) / len(keywords) * 100.0
        mapped = bool(group and group in (info.get("groups") or []))
        sub = round(min(100.0, base + (bonus if mapped else 0.0)), 2)
        signals.append(_signal(name, "ok", {"keyword_hits": hits, "group_mapped": mapped}, sub,
                               "关键词命中占比 + 主题组映射加权。"))
    return signals


def evaluate_three_scores(
    repo: Dict[str, Any],
    topic_config: Dict[str, Any],
    growth: Optional[Dict[str, Any]] = None,
    group: Optional[str] = None,
) -> Dict[str, Any]:
    """输出三个彼此独立的分数（Discovery / Engineering / Relevance）。

    每个分数包含 score（数字或 "unknown"）、explanation（中文说明）与
    basis（子信号列表）。缺失字段对应的子信号标 "unknown"，不默认满分/零分；
    某一维度全部子信号不可观测时，其整体 score 才为 "unknown"。
    本函数不修改也不依赖旧的 evaluate()/total 加权逻辑。
    """
    cfg = _three_cfg()
    repo = repo or {}
    if not group:
        group = _best_group(repo, topic_config)

    groups_by_dim = {
        "discovery_signal": _discovery_signals(repo, growth, cfg.get("discovery_signal", {})),
        "engineering_quality": _engineering_signals(repo, growth, cfg.get("engineering_quality", {})),
        "relevance": _relevance_signals(repo, topic_config, group, cfg.get("relevance", {})),
    }

    result: Dict[str, Any] = {}
    for dim, signals in groups_by_dim.items():
        weights = cfg.get(dim, {}).get("weights", {})
        score = _aggregate(signals, weights)
        ok_count = sum(1 for s in signals if s["status"] == "ok")
        unknown_names = [s["name"] for s in signals if s["status"] == "unknown"]
        if score == "unknown":
            explanation = (
                f"『{dim}』缺少足够可观测字段，标记为 unknown（未默认给满分或零分）。"
                f"未知子信号：{', '.join(unknown_names) or '无'}。"
            )
        else:
            explanation = (
                f"『{dim}』基于 {ok_count} 个可观测子信号按配置权重加权平均得到 {score}；"
                f"未知子信号（未参与计分）：{', '.join(unknown_names) or '无'}。"
            )
        result[dim] = {"score": score, "explanation": explanation, "basis": signals}
    return result
