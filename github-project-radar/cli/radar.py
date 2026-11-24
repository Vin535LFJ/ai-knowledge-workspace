#!/usr/bin/env python3
"""GitHub Project Radar 命令行入口。

默认命令使用本地文件与离线 fixtures（无网络）；`collect --source rest` 显式启用
真实 GitHub REST 采集（radar/sources/rest.py）。令牌等敏感信息仅通过环境变量
GITHUB_TOKEN 提供，本 CLI 不读取或打印令牌内容。不执行任何 git 操作。
"""

import argparse
import json
import os
import sys

# 保证从任意工作目录运行都能导入项目内的包
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from radar import load_config
from radar.collector import Collector, CollectorConfig
from radar.export import export_research_tasks
from radar.growth import compute_growth
from radar.models import Candidate, Snapshot, utc_now_iso
from radar.reports import generate_json_report, generate_report, generate_summary_report, iso_week_label
from radar.review import ReviewStateMachine, STATES
from radar.scoring import evaluate
from radar.storage import Storage

DEFAULT_DB = os.path.join(PROJECT_ROOT, "radar.db")
DEFAULT_REPORTS = os.path.join(PROJECT_ROOT, "reports")


def _fixture_client():
    from fixtures.client import FixtureApiClient

    return FixtureApiClient()


def _rest_client():
    from radar.sources.rest import GitHubRestClient

    return GitHubRestClient()


def _resolve_topic(repo, topics_config):
    """为一个仓库推断最匹配的主题组（基于关键词命中数）。"""
    text = ((repo.description or "") + " " + " ".join(repo.topics or [])).lower()
    best_id, best_hits = "extensions", 0
    for topic in topics_config.get("topics", []):
        hits = sum(1 for k in topic.get("keywords", []) if k.lower() in text)
        if hits > best_hits:
            best_id, best_hits = topic.get("id"), hits
    return best_id, best_hits


def cmd_init_db(args):
    Storage(args.db).init_db()
    print(f"[init-db] 数据库已初始化: {args.db}")


def cmd_collect(args):
    storage = Storage(args.db)
    storage.init_db()
    topics = load_config("topics.json")
    if args.source == "rest":
        client = _rest_client()
        # 真实网络：保留 collector 的退避与限速休眠（匿名搜索 ~10 req/min）
        collector = Collector(
            storage,
            client,
            CollectorConfig(max_retries=2, base_backoff_seconds=2.0),
        )
    else:
        client = _fixture_client()
        collector = Collector(
            storage,
            client,
            CollectorConfig(max_retries=2, base_backoff_seconds=0, sleep_func=lambda s: None),
        )
    result = collector.discover(topics, max_queries=args.max_queries)
    label = "真实 GitHub REST" if args.source == "rest" else "离线 fixtures，无网络请求"
    print(f"[collect] 采集完成（{label}）:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_snapshot(args):
    storage = Storage(args.db)
    storage.init_db()
    client = _fixture_client()
    names = args.full_name or [r["full_name"] for r in client.repositories]
    captured_at = args.captured_at or utc_now_iso()
    added = 0
    for name in names:
        try:
            raw = client.get_repository(name)
        except KeyError as exc:
            print(f"[snapshot] 跳过: {exc}")
            continue
        snap = Snapshot(
            repository_id=int(raw["id"]),
            captured_at=captured_at,
            stargazers_count=int(raw.get("stargazers_count", 0)),
            forks_count=int(raw.get("forks_count", 0)),
            watchers_count=int(raw.get("watchers_count", 0)),
            open_issues_count=int(raw.get("open_issues_count", 0)),
            pushed_at=raw.get("pushed_at"),
            updated_at=raw.get("updated_at"),
        )
        # 确保仓库元数据存在
        from radar.collector import Collector

        repo = Collector._parse_repo(raw)
        storage.upsert_repository(repo)
        if storage.insert_snapshot(snap):
            added += 1
    print(f"[snapshot] 新增快照 {added} 条，采集时间: {captured_at}")


def cmd_analyze(args):
    storage = Storage(args.db)
    topics = load_config("topics.json")
    scoring_cfg = load_config("scoring.json")
    weights = scoring_cfg.get("weights")
    repos = storage.list_repositories()
    created = 0
    for repo in repos:
        snaps = storage.get_snapshots(repo.repository_id)
        growth = compute_growth(snaps)
        group, hits = _resolve_topic(repo, topics)
        ev = evaluate(repo.to_dict(), topics, growth, group, weights=weights)
        cand = Candidate(
            repository_id=repo.repository_id,
            topic=group,
            discovery_reason={
                "method": "topic-keyword-match",
                "matched_keywords": hits,
                "snapshot_count": len(snaps),
            },
            evaluation=ev,
            review_status="Discovered",
            created_at=utc_now_iso(),
        )
        storage.upsert_candidate(cand)
        created += 1
    print(f"[analyze] 已评估 {created} 个仓库并写入候选池（增长数据不足处标记为中性）。")


def cmd_candidates(args):
    storage = Storage(args.db)
    rows = storage.list_candidates(review_status=args.status)
    if not rows:
        print("[candidates] 无候选记录。")
        return
    for r in rows:
        print(
            f"- #{r['id']} {r['full_name']} | 主题={r['topic']} | "
            f"状态={r['review_status']} | 总分={r['evaluation'].get('total', 'N/A')}"
        )


def cmd_report(args):
    storage = Storage(args.db)
    report_format = getattr(args, "format", "dir")
    if report_format == "summary":
        result = generate_summary_report(storage, args.reports_root, label=args.week)
        print(f"[report] 单文件摘要周报已生成: {result['path']}")
        print(f"  含七个板块: {', '.join(result['sections'])}")
        return
    if report_format == "json":
        result = generate_json_report(storage, args.reports_root, label=args.week)
        print(f"[report] JSON 周报已生成: {result['path']}")
        print(f"  含七个板块: {', '.join(result['sections'])}")
        return
    # 默认 dir：保持旧的 YYYY-Www/ 目录 + 7 文件行为不变
    result = generate_report(storage, args.reports_root, label=args.week)
    print(f"[report] 周报已生成于 {result['directory']}，共 {result['count']} 个文件。")
    for path in result["files"]:
        print("  - " + os.path.relpath(path, PROJECT_ROOT))


def cmd_export(args):
    storage = Storage(args.db)
    result = export_research_tasks(
        storage,
        args.output,
        review_status=args.status,
        only_approved=args.approved,
    )
    print(f"[export] 已导出 {result['count']} 条研究任务到 {args.output}")
    print("  说明：本模块仅输出文件，不会写入 Render_Notes 或任何外部项目。")


def cmd_query(args):
    import sqlite3

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(args.sql).fetchall()
    except Exception as exc:
        print(f"[query] 查询失败: {exc}")
        return
    finally:
        conn.close()
    for row in rows:
        print(json.dumps(dict(row), ensure_ascii=False))


def cmd_review(args):
    storage = Storage(args.db)
    sm = ReviewStateMachine(storage)
    result = sm.transition(
        candidate_id=args.candidate_id,
        current=args.current,
        target=args.target,
        reviewer=args.reviewer,
        decision=args.decision,
        research_objective=args.objective,
    )
    print("[review] 复核完成:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="radar",
        description="GitHub Project Radar —— 开源情报与技术发现系统（离线、仅标准库）",
    )
    parser.add_argument("--db", default=DEFAULT_DB, help=f"SQLite 数据库路径（默认 {DEFAULT_DB}）")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="初始化数据库表结构").set_defaults(func=cmd_init_db)

    p = sub.add_parser("collect", help="执行发现采集（默认离线 fixtures；--source rest 为真实 GitHub REST）")
    p.add_argument("--source", choices=["fixture", "rest"], default="fixture",
                   help="数据源：fixture=离线样例（默认），rest=真实 GitHub REST（匿名或 GITHUB_TOKEN）")
    p.add_argument("--max-queries", type=int, default=None, help="限制执行的搜索查询数量")
    p.set_defaults(func=cmd_collect)

    p = sub.add_parser("snapshot", help="记录一次快照（默认全部样例仓库）")
    p.add_argument("--full-name", action="append", help="指定仓库全名，可重复")
    p.add_argument("--captured-at", help="指定采集时间（ISO-8601），用于可复现测试")
    p.set_defaults(func=cmd_snapshot)

    p = sub.add_parser("analyze", help="计算增长与评分，写入候选池")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("candidates", help="列出候选记录")
    p.add_argument("--status", choices=STATES, help="按复核状态过滤")
    p.set_defaults(func=cmd_candidates)

    p = sub.add_parser("report", help="生成周报（默认目录 7 文件；可选单文件摘要 / JSON）")
    p.add_argument("--reports-root", default=DEFAULT_REPORTS, help=f"周报根目录（默认 {DEFAULT_REPORTS}）")
    p.add_argument("--week", help="周标签 YYYY-Www（默认当前 ISO 周）")
    p.add_argument("--format", choices=["summary", "json", "dir"], default="dir",
                   help="报告格式：dir=目录 7 文件（默认），summary=单文件 Markdown，json=机器可读 JSON")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("export", help="导出研究任务 JSON（纯输出）")
    p.add_argument("--output", required=True, help="输出文件路径")
    p.add_argument("--status", default="Research", help="要导出的复核状态（默认 Research）")
    p.add_argument("--approved", action="store_true", help="将 review_status 标记为 approved_for_research")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("query", help="执行只读 SQL 查询并打印结果")
    p.add_argument("sql", help="SQL 查询语句")
    p.set_defaults(func=cmd_query)

    p = sub.add_parser("review", help="人工复核状态转换")
    p.add_argument("candidate_id", type=int, help="候选 id")
    p.add_argument("--current", required=True, choices=STATES, help="当前状态")
    p.add_argument("--target", required=True, choices=STATES, help="目标状态")
    p.add_argument("--reviewer", required=True, help="复核人")
    p.add_argument("--decision", required=True, help="复核决定说明")
    p.add_argument("--objective", default="", help="研究目标（可选）")
    p.set_defaults(func=cmd_review)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
