"""GitHub Project Radar 单元测试。

覆盖：快照幂等、增长计算（充足/不足历史）、可配置评分与理由、
复核状态机（含 Adopt 不自动导入）、导出字段完整性、周报 7 文件、主题配置可扩展。

全部使用 tempfile.TemporaryDirectory 隔离数据库，不发起网络请求、不执行 git 操作。
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from radar import load_config
from radar.export import EXPORT_FIELDS, build_research_task, export_research_tasks
from radar.growth import compute_growth
from radar.models import Candidate, Repository, Snapshot
from radar.reports import REPORT_FILES, generate_json_report, generate_report, generate_summary_report
from radar.research import render_from_candidate, render_research_template
from radar.review import (
    CANONICAL_STATES,
    ReviewStateMachine,
    normalize_status,
    record_transition,
    to_legacy_status,
)
from radar.scoring import DEFAULT_WEIGHTS, compare_group, evaluate, evaluate_three_scores
from radar.sources.base import SourceClient
from radar.sources.ossinsight import OSSInsightSourceClient
from radar.sources.rest import RestSourceClient
from radar.sources.trending import TrendingSourceClient
from radar.storage import Storage


def make_snapshots(repo_id, stars_by_day, start=None):
    """根据 (days_ago, stars) 列表生成快照。"""
    start = start or datetime(2026, 11, 19, tzinfo=timezone.utc)
    snaps = []
    for days_ago, stars in stars_by_day:
        captured = start - timedelta(days=days_ago)
        snaps.append(
            Snapshot(
                repository_id=repo_id,
                captured_at=captured.replace(microsecond=0).isoformat(),
                stargazers_count=stars,
                forks_count=max(0, stars // 10),
                watchers_count=stars // 20,
                pushed_at=(start - timedelta(days=2)).isoformat(),
            )
        )
    return snaps


class SnapshotStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "radar.db")
        self.storage = Storage(self.db)
        self.storage.init_db()
        self.repo = Repository(repository_id=1, full_name="org/proj", first_seen_at="2026-01-01T00:00:00+00:00")

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_insert_idempotency(self):
        self.storage.upsert_repository(self.repo)
        snap = Snapshot(repository_id=1, captured_at="2026-11-19T00:00:00+00:00", stargazers_count=100)
        self.assertTrue(self.storage.insert_snapshot(snap))
        # 同一 (repository_id, captured_at) 再次插入应被忽略
        self.assertFalse(self.storage.insert_snapshot(snap))
        snaps = self.storage.get_snapshots(1)
        self.assertEqual(len(snaps), 1)
        self.assertEqual(snaps[0].stargazers_count, 100)

    def test_snapshots_accumulate_not_overwrite(self):
        self.storage.upsert_repository(self.repo)
        self.storage.insert_snapshot(Snapshot(1, "2026-11-18T00:00:00+00:00", 90))
        self.storage.insert_snapshot(Snapshot(1, "2026-11-19T00:00:00+00:00", 100))
        snaps = self.storage.get_snapshots(1)
        self.assertEqual([s.stargazers_count for s in snaps], [90, 100])

    def test_failed_transaction_does_not_corrupt_history(self):
        from radar.collector import Collector, CollectorConfig

        self.storage.upsert_repository(self.repo)
        self.storage.insert_snapshot(Snapshot(1, "2026-11-18T00:00:00+00:00", 90))

        class ExplodingClient:
            def search_repositories(self, params):
                raise RuntimeError("simulated failure")

            def get_repository(self, full_name):
                raise RuntimeError("simulated failure")

        collector = Collector(
            self.storage,
            ExplodingClient(),
            CollectorConfig(max_retries=1, base_backoff_seconds=0, sleep_func=lambda s: None),
        )
        # 所有查询失败，但既有历史应保持不变
        result = collector.discover(load_config("topics.json"), max_queries=1)
        self.assertGreater(len(result["errors"]), 0)
        snaps = self.storage.get_snapshots(1)
        self.assertEqual(len(snaps), 1)
        self.assertEqual(snaps[0].stargazers_count, 90)


class GrowthTests(unittest.TestCase):
    def test_sufficient_history(self):
        snaps = make_snapshots(1, [(35, 100), (30, 120), (14, 200), (8, 260), (1, 300), (0, 310)])
        g = compute_growth(snaps)
        self.assertFalse(g["insufficient_history"])
        self.assertIsNotNone(g["star_growth_7d"])
        self.assertIsNotNone(g["star_growth_30d"])
        # 近 7 天：300-260? anchor=最后一个快照时间；base 在 7 天前≈day8(260) → 310-260=50
        self.assertEqual(g["star_growth_7d"], 50)
        self.assertTrue(g["activity"]["active_recently"])
        self.assertIn("acceleration", g)
        self.assertIsNotNone(g["acceleration"])

    def test_insufficient_history_no_fabricated_numbers(self):
        snaps = make_snapshots(1, [(0, 100)])  # 只有 1 个快照
        g = compute_growth(snaps)
        self.assertTrue(g["insufficient_history"])
        self.assertIsNone(g["star_growth_7d"])
        self.assertIsNone(g["star_growth_30d"])
        self.assertIsNone(g["star_growth_24h"])
        self.assertIsNone(g["fork_growth_7d"])
        self.assertIn("note", g)

    def test_empty_history(self):
        g = compute_growth([])
        self.assertTrue(g["insufficient_history"])
        self.assertIsNone(g["star_growth_7d"])


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.topics = load_config("topics.json")
        self.repo = {
            "full_name": "org/agent-forge",
            "description": "A novel multi-agent framework with memory and orchestration",
            "topics": ["agent", "framework"],
            "license": "MIT",
            "homepage": "https://example.org",
        }
        self.growth = {
            "insufficient_history": False,
            "star_growth_7d": 50,
            "star_growth_rate_7d": 0.2,
            "acceleration": {"accelerating": True},
        }

    def test_weights_configurable_and_total_matches(self):
        custom = {"innovation": 50, "relevance": 50, "engineering_maturity": 0, "reusability": 0, "growth_momentum": 0}
        ev = evaluate(self.repo, self.topics, self.growth, "ai-agent", weights=custom)
        self.assertEqual(ev["weights"], custom)
        self.assertAlmostEqual(
            ev["total"],
            (ev["dimensions"]["innovation"]["score"] * 50 + ev["dimensions"]["relevance"]["score"] * 50) / 100,
            places=2,
        )

    def test_reasons_present_for_every_dimension(self):
        ev = evaluate(self.repo, self.topics, self.growth, "ai-agent")
        for key, d in ev["dimensions"].items():
            self.assertIn("score", d, key)
            self.assertTrue(d.get("reason"), f"{key} 缺少 reason")
            self.assertIn("basis", d, key)

    def test_growth_momentum_neutral_when_insufficient(self):
        poor = {"insufficient_history": True, "snapshot_count": 1, "note": "test"}
        ev = evaluate(self.repo, self.topics, poor, "ai-agent")
        gm = ev["dimensions"]["growth_momentum"]
        self.assertEqual(gm["score"], 0.0)
        self.assertIn("中性", gm["reason"])

    def test_group_comparison_rejects_cross_group(self):
        evs = [
            {"group": "ai-agent", "total": 80},
            {"group": "mcp-tools", "total": 70},
        ]
        result = compare_group(evs)
        self.assertFalse(result["comparable"])
        self.assertEqual(result["ranking"], [])


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.storage = Storage(os.path.join(self.tmp.name, "radar.db"))
        self.storage.init_db()
        self.storage.upsert_repository(Repository(repository_id=1, full_name="org/proj"))
        self.storage.upsert_candidate(
            Candidate(repository_id=1, topic="ai-agent", review_status="Discovered", created_at="2026-11-19T00:00:00+00:00")
        )
        self.cid = self.storage.list_candidates()[0]["id"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_transition_chain(self):
        sm = ReviewStateMachine(self.storage)
        cur = "Discovered"
        for target in ["Triaged", "Watch", "Research", "Adopt"]:
            res = sm.transition(self.cid, cur, target, "alice", f"move to {target}")
            self.assertEqual(res["to"], target)
            self.assertEqual(res["auto_side_effects"], [])
            cur = target
        rows = self.storage.list_candidates()
        self.assertEqual(rows[0]["review_status"], "Adopt")

    def test_invalid_transition_rejected(self):
        sm = ReviewStateMachine(self.storage)
        with self.assertRaises(ValueError):
            sm.transition(self.cid, "Discovered", "Adopt", "alice", "skip steps")

    def test_adopt_does_not_auto_import(self):
        sm = ReviewStateMachine(self.storage)
        sm.transition(self.cid, "Discovered", "Triaged", "alice", "triage")
        sm.transition(self.cid, "Triaged", "Research", "alice", "research")
        res = sm.transition(self.cid, "Research", "Adopt", "alice", "adopt decision")
        self.assertEqual(res["auto_side_effects"], [])
        self.assertIn("不会导入", res["note"])
        # 确认除状态与审计日志外没有产生任何外部写入记录
        rows = self.storage.list_candidates()
        eval_data = rows[0]["evaluation"]
        self.assertIn("review_log", eval_data)
        self.assertEqual(eval_data["review_status"], "Adopt")

    def test_review_log_records_reviewer_time_decision(self):
        sm = ReviewStateMachine(self.storage)
        sm.transition(self.cid, "Discovered", "Triaged", "bob", "looks promising")
        log = self.storage.list_candidates()[0]["evaluation"]["review_log"][0]
        self.assertEqual(log["reviewer"], "bob")
        self.assertEqual(log["decision"], "looks promising")
        self.assertIn("at", log)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.storage = Storage(os.path.join(self.tmp.name, "radar.db"))
        self.storage.init_db()
        self.storage.upsert_repository(Repository(repository_id=1, full_name="org/proj"))
        self.storage.upsert_candidate(
            Candidate(
                repository_id=1,
                topic="ai-agent",
                evaluation={"total": 80, "dimensions": {}},
                review_status="Research",
                research_objective="研究其记忆机制",
                created_at="2026-11-19T00:00:00+00:00",
            )
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_export_field_completeness(self):
        out = os.path.join(self.tmp.name, "tasks.json")
        export_research_tasks(self.storage, out, review_status="Research", only_approved=True)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["task_count"], 1)
        task = data["tasks"][0]
        for field in EXPORT_FIELDS:
            self.assertIn(field, task, f"缺少字段 {field}")
        self.assertEqual(task["review_status"], "approved_for_research")
        self.assertEqual(task["url"], "https://github.com/org/proj")
        self.assertEqual(task["research_objective"], "研究其记忆机制")


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.storage = Storage(os.path.join(self.tmp.name, "radar.db"))
        self.storage.init_db()
        self.storage.upsert_repository(Repository(repository_id=1, full_name="org/proj"))
        self.storage.upsert_candidate(
            Candidate(repository_id=1, topic="ai-agent", review_status="Research", created_at="2026-11-19T00:00:00+00:00")
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_report_creates_all_seven_files(self):
        result = generate_report(self.storage, self.tmp.name, label="2026-W47")
        self.assertEqual(result["count"], 7)
        names = sorted(os.path.basename(p) for p in result["files"])
        self.assertEqual(names, sorted(REPORT_FILES))
        for p in result["files"]:
            self.assertTrue(os.path.exists(p))
            self.assertGreater(os.path.getsize(p), 0)
        expected_dir = os.path.join(self.tmp.name, "2026-W47")
        self.assertEqual(result["directory"], expected_dir)


class TopicConfigTests(unittest.TestCase):
    def test_add_topic_without_code_change(self):
        cfg = load_config("topics.json")
        original_count = len(cfg["topics"])
        cfg["topics"].append(
            {
                "id": "quantum-ml",
                "name": "Quantum ML",
                "keywords": ["quantum", "qubit", "hybrid"],
                "languages": ["Python"],
            }
        )
        self.assertEqual(len(cfg["topics"]), original_count + 1)
        # 评分逻辑完全由配置驱动：新主题即可参与相关性评分与分组
        repo = {"description": "a quantum qubit framework", "topics": ["quantum"], "license": "MIT"}
        ev = evaluate(repo, cfg, {"insufficient_history": True}, "quantum-ml")
        self.assertEqual(ev["group"], "quantum-ml")
        self.assertGreater(ev["dimensions"]["relevance"]["score"], 0)
        # 发现查询生成也应包含新主题关键词
        from radar.collector import Collector, CollectorConfig

        collector = Collector(storage=None, api_client=None, config=CollectorConfig())
        queries = collector.build_search_queries(cfg)
        self.assertTrue(any("quantum" in q["q"] for q in queries))


# =====================================================================
# 增量功能测试（追加，不影响上面 17 个既有测试）
# =====================================================================


class ThreeScoresTests(unittest.TestCase):
    """三维独立评分：确定性、缺字段 unknown、旧综合分不变。"""

    def setUp(self):
        self.topics = load_config("topics.json")
        self.repo = {
            "full_name": "org/agent-forge",
            "description": "A novel multi-agent framework with memory and orchestration",
            "topics": ["agent", "framework"],
            "license": "MIT",
            "homepage": "https://example.org",
            "language": "Python",
            "created_at": "2025-01-01T00:00:00Z",
            "release_info": {"tag": "v1.0"},
            "open_issues_count": 5,
        }
        self.growth = {
            "star_growth_24h": 5,
            "star_growth_7d": 50,
            "star_growth_30d": 200,
            "fork_growth_7d": 10,
            "activity": {"days_since_push": 2, "active_recently": True},
        }

    def test_three_scores_structure_and_determinism(self):
        first = evaluate_three_scores(self.repo, self.topics, self.growth, "ai-agent")
        second = evaluate_three_scores(self.repo, self.topics, self.growth, "ai-agent")
        self.assertEqual(first, second)
        self.assertEqual(set(first), {"discovery_signal", "engineering_quality", "relevance"})
        for dim, payload in first.items():
            self.assertIn("score", payload, dim)
            self.assertIn("explanation", payload, dim)
            self.assertIsInstance(payload["basis"], list, dim)
            self.assertTrue(payload["explanation"], dim)

    def test_missing_fields_yield_unknown_not_zero_or_full(self):
        result = evaluate_three_scores({"full_name": "x/y"}, self.topics, None, None)
        for dim, payload in result.items():
            self.assertEqual(payload["score"], "unknown", dim)
            self.assertIn("unknown", payload["explanation"])

    def test_higher_growth_yields_higher_discovery_signal(self):
        low_growth = dict(self.growth)
        low_growth.update(star_growth_7d=1, star_growth_30d=2, fork_growth_7d=0)
        low = evaluate_three_scores(self.repo, self.topics, low_growth, "ai-agent")["discovery_signal"]["score"]
        high = evaluate_three_scores(self.repo, self.topics, self.growth, "ai-agent")["discovery_signal"]["score"]
        self.assertLess(low, high)

    def test_old_total_weighting_unchanged(self):
        ev = evaluate(self.repo, self.topics, self.growth, "ai-agent")
        expected = sum(ev["dimensions"][k]["score"] * w / 100.0 for k, w in DEFAULT_WEIGHTS.items())
        self.assertAlmostEqual(ev["total"], expected, places=2)
        self.assertEqual(set(ev["dimensions"]), set(DEFAULT_WEIGHTS))
        self.assertNotIn("discovery_signal", ev["dimensions"])
        self.assertNotIn("engineering_quality", ev["dimensions"])

    def test_config_version_two_and_old_weights_preserved(self):
        cfg = load_config("scoring.json")
        self.assertEqual(cfg["version"], 2)
        self.assertIn("three_scores", cfg)
        self.assertEqual(cfg["weights"], DEFAULT_WEIGHTS)
        for dim in ["discovery_signal", "engineering_quality", "relevance"]:
            self.assertIn(dim, cfg["three_scores"])


class LifecycleAliasTests(unittest.TestCase):
    """canonical 生命周期与旧别名双向兼容。"""

    def test_normalize_legacy_aliases(self):
        mapping = {
            "Discovered": "discovered",
            "Triaged": "triaged",
            "Watch": "watchlist",
            "Research": "deep_dive",
            "Adopt": "adopted",
            "Ignore": "rejected",
        }
        for raw, canonical in mapping.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_status(raw), canonical)

    def test_normalize_all_canonical_values(self):
        for status in CANONICAL_STATES:
            with self.subTest(status=status):
                self.assertEqual(normalize_status(status), status)

    def test_reverse_alias_to_legacy(self):
        self.assertEqual(to_legacy_status("watchlist"), "Watch")
        self.assertEqual(to_legacy_status("deep_dive"), "Research")
        self.assertEqual(to_legacy_status("adopted"), "Adopt")
        self.assertEqual(to_legacy_status("rejected"), "Ignore")
        self.assertEqual(to_legacy_status("archived"), "archived")

    def test_unknown_value_passthrough(self):
        self.assertEqual(normalize_status("LegacyCustomValue"), "LegacyCustomValue")

    def test_record_transition_has_time_operator_reason(self):
        record = record_transition(
            "Research", "Adopt", "alice", "决定吸收", at="2026-11-19T00:00:00+00:00"
        )
        for key in ["from", "to", "operator", "reason", "at"]:
            self.assertIn(key, record)
        self.assertEqual(record["from"], "deep_dive")
        self.assertEqual(record["to"], "adopted")
        self.assertEqual(record["operator"], "alice")

    def test_legacy_fixture_value_still_readable(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        storage = Storage(os.path.join(tmp.name, "radar.db"))
        storage.init_db()
        storage.upsert_repository(Repository(repository_id=1, full_name="org/proj"))
        storage.upsert_candidate(
            Candidate(repository_id=1, topic="ai-agent", review_status="Research",
                      created_at="2026-11-19T00:00:00+00:00")
        )
        self.assertEqual(storage.list_candidates()[0]["review_status"], "Research")


class NewReportFormatTests(unittest.TestCase):
    """新增的单文件摘要与 JSON 报告（七板块 A-G）。"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.storage = Storage(os.path.join(self.tmp.name, "radar.db"))
        self.storage.init_db()
        self.storage.upsert_repository(Repository(repository_id=1, full_name="org/proj"))
        self.storage.upsert_candidate(
            Candidate(repository_id=1, topic="ai-agent", review_status="Research",
                      created_at="2026-11-19T00:00:00+00:00")
        )

    def test_summary_report_has_seven_sections(self):
        result = generate_summary_report(self.storage, self.tmp.name, label="2026-W47")
        self.assertEqual(result["sections"], list("ABCDEFG"))
        self.assertEqual(os.path.basename(result["path"]), "2026-W47.md")
        with open(result["path"], encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('doc_id: "weekly-summary-2026-W47"', text)
        for key in "ABCDEFG":
            self.assertIn(f"## {key} ·", text)

    def test_json_report_has_seven_sections(self):
        result = generate_json_report(self.storage, self.tmp.name, label="2026-W47")
        self.assertEqual(set(result["sections"]), set("ABCDEFG"))
        self.assertEqual(os.path.basename(result["path"]), "2026-W47.json")
        with open(result["path"], encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["week"], "2026-W47")
        self.assertEqual(set(data["sections"]), set("ABCDEFG"))
        for key in "ABCDEFG":
            self.assertIn("items", data["sections"][key])


class ProvenanceTests(unittest.TestCase):
    """人工选择标志与溯源字段的模型往返、存储与导出。"""

    def test_model_round_trip(self):
        repo = Repository(repository_id=1, full_name="o/r", source_url="repo-url",
                          observed_at="repo-obs", retrieved_at="repo-ret", data_quality="high")
        self.assertEqual(Repository.from_dict(repo.to_dict()).source_url, "repo-url")
        snap = Snapshot(repository_id=1, captured_at="t", source_url="snap-url",
                        observed_at="snap-obs", retrieved_at="snap-ret", data_quality="medium")
        self.assertEqual(Snapshot.from_dict(snap.to_dict()).retrieved_at, "snap-ret")
        cand = Candidate(repository_id=1, topic="ai-agent", human_selected_for_research=True,
                         source_url="cand-url", observed_at="cand-obs",
                         retrieved_at="cand-ret", data_quality="low")
        restored = Candidate.from_dict(cand.to_dict())
        self.assertTrue(restored.human_selected_for_research)
        self.assertEqual(restored.source_url, "cand-url")
        self.assertEqual(restored.data_quality, "low")

    def test_defaults_are_false_and_none(self):
        cand = Candidate(repository_id=1, topic="t")
        self.assertFalse(cand.human_selected_for_research)
        self.assertIsNone(cand.source_url)
        self.assertIsNone(cand.observed_at)
        self.assertIsNone(cand.retrieved_at)
        self.assertIsNone(cand.data_quality)

    def test_storage_and_export_round_trip(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        storage = Storage(os.path.join(tmp.name, "radar.db"))
        storage.init_db()
        storage.upsert_repository(Repository(repository_id=1, full_name="org/proj", source_url="repo-url"))
        storage.upsert_candidate(
            Candidate(
                repository_id=1, topic="ai-agent",
                evaluation={"total": 80, "dimensions": {}},
                review_status="Research", created_at="2026-11-19T00:00:00+00:00",
                human_selected_for_research=True, source_url="cand-url",
                observed_at="cand-obs", retrieved_at="cand-ret", data_quality="low",
            )
        )
        out = os.path.join(tmp.name, "tasks.json")
        export_research_tasks(storage, out, review_status="Research")
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        task = data["tasks"][0]
        self.assertTrue(task["human_selected_for_research"])
        self.assertEqual(task["source_url"], "cand-url")
        self.assertEqual(task["observed_at"], "cand-obs")
        self.assertEqual(task["retrieved_at"], "cand-ret")
        self.assertEqual(task["data_quality"], "low")

        # build_research_task 在候选缺字段时回退到仓库记录
        fallback = build_research_task({"id": 1, "topic": "t"},
                                       Repository(repository_id=1, full_name="o/r", source_url="repo-url").to_dict(),
                                       None)
        self.assertEqual(fallback["source_url"], "repo-url")
        self.assertFalse(fallback["human_selected_for_research"])


class SourceAdapterTests(unittest.TestCase):
    """source 适配器接口符合性，且绝对无网络调用。"""

    CLIENTS = [RestSourceClient, TrendingSourceClient, OSSInsightSourceClient]

    def test_clients_implement_interface(self):
        for cls in self.CLIENTS:
            with self.subTest(client=cls.__name__):
                client = cls()
                self.assertIsInstance(client, SourceClient)
                for method_name in ["fetch_repositories", "fetch_trending", "fetch_insights"]:
                    result = getattr(client, method_name)({})
                    self.assertIsInstance(result, dict)
                    self.assertIn("items", result)

    def test_no_network_calls(self):
        import socket

        def blocked(*args, **kwargs):
            raise AssertionError("source adapter 试图发起网络请求")

        original = socket.socket.connect
        socket.socket.connect = blocked
        try:
            for cls in self.CLIENTS:
                client = cls()
                for method_name in ["fetch_repositories", "fetch_trending", "fetch_insights"]:
                    getattr(client, method_name)({})
        finally:
            socket.socket.connect = original

    def test_default_client_is_fixture_not_source_stub(self):
        from fixtures.client import FixtureApiClient

        self.assertTrue(hasattr(FixtureApiClient, "search_repositories"))
        self.assertTrue(hasattr(FixtureApiClient, "get_repository"))


class ResearchPathTests(unittest.TestCase):
    """深度研究默认输出 research/owner__repo.md。"""

    def test_default_output_dir_is_research(self):
        import inspect

        self.assertEqual(inspect.signature(render_research_template).parameters["output_dir"].default, "research")
        self.assertEqual(inspect.signature(render_from_candidate).parameters["output_dir"].default, "research")

    def test_filename_and_output_override(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        result = render_research_template(
            {"full_name": "owner/repo", "description": "d"}, {"total": 80}, output_dir=tmp.name
        )
        self.assertEqual(result["filename"], "owner__repo.md")
        self.assertEqual(os.path.basename(result["path"]), "owner__repo.md")
        self.assertTrue(os.path.exists(result["path"]))
        with open(result["path"], encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn('doc_id: "research-owner__repo"', text)


if __name__ == "__main__":
    unittest.main()
