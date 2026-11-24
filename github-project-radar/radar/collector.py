"""采集器：通过注入的 API 客户端获取仓库数据，自身不发起任何网络请求。

API 客户端协议（由调用方注入，测试时使用离线 fixtures）：
    search_repositories(params) -> {"items": [repo_dict, ...]}
    get_repository(full_name)   -> repo_dict

采集器负责：
- 新仓库发现、按主题/语言搜索、快速增长、最近推送、最近发布、技能/MCP 关键词发现。
- 指数退避重试与速率限制感知（配置驱动）。
- 事务性：采集失败时回滚，不破坏既有快照历史。
- 即使仓库在某次搜索结果中掉出，也继续跟踪（从库内已有仓库中补充抓取最新快照）。
"""

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol

from .models import Repository, Snapshot, utc_now_iso
from .storage import Storage


class ApiClient(Protocol):
    def search_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]: ...

    def get_repository(self, full_name: str) -> Dict[str, Any]: ...


@dataclass
class CollectorConfig:
    max_retries: int = 3
    base_backoff_seconds: float = 1.0
    rate_limit_per_minute: int = 30
    per_page: int = 50
    sleep_func: Any = time.sleep


class Collector:
    def __init__(self, storage: Storage, api_client: ApiClient, config: Optional[CollectorConfig] = None):
        self.storage = storage
        self.api = api_client
        self.config = config or CollectorConfig()

    # ---------- retry / rate-limit ----------

    def _call_with_retry(self, func, *args, **kwargs):
        """带指数退避的重试；识别常见速率限制错误。"""
        last_exc = None
        for attempt in range(self.config.max_retries):
            try:
                result = func(*args, **kwargs)
                # 尊重上报的速率限制余量（若客户端返回该信息）
                if isinstance(result, dict) and result.get("_rate_limit_remaining") == 0:
                    self.config.sleep_func(60)
                return result
            except Exception as exc:  # noqa: BLE001 - 网络层异常形态多样
                last_exc = exc
                text = str(exc).lower()
                if "rate limit" in text or "403" in text or "429" in text:
                    self.config.sleep_func(60)
                if attempt < self.config.max_retries - 1:
                    self.config.sleep_func(self.config.base_backoff_seconds * (2 ** attempt))
        raise last_exc

    # ---------- 解析 ----------

    @staticmethod
    def _parse_repo(raw: Dict[str, Any]) -> Repository:
        owner = raw.get("owner") or {}
        full_name = raw.get("full_name") or (
            f"{owner.get('login', 'unknown')}/{raw.get('name', 'unknown')}"
        )
        license_info = raw.get("license") or {}
        return Repository(
            repository_id=int(raw["id"]),
            full_name=full_name,
            description=raw.get("description") or "",
            language=raw.get("language"),
            topics=list(raw.get("topics") or []),
            license=license_info.get("spdx_id") if isinstance(license_info, dict) else None,
            created_at=raw.get("created_at"),
            homepage=raw.get("homepage") or None,
            default_branch=raw.get("default_branch") or "main",
            archived=bool(raw.get("archived", False)),
            first_seen_at=utc_now_iso(),
        )

    @staticmethod
    def _parse_snapshot(raw: Dict[str, Any], captured_at: Optional[str] = None) -> Snapshot:
        return Snapshot(
            repository_id=int(raw["id"]),
            captured_at=captured_at or utc_now_iso(),
            stargazers_count=int(raw.get("stargazers_count", 0)),
            forks_count=int(raw.get("forks_count", 0)),
            watchers_count=int(raw.get("watchers_count", 0)),
            open_issues_count=int(raw.get("open_issues_count", 0)),
            pushed_at=raw.get("pushed_at"),
            updated_at=raw.get("updated_at"),
            release_info={"tag": (raw.get("_release") or {}).get("tag_name")}
            if raw.get("_release")
            else {},
        )

    # ---------- 发现策略 ----------

    def build_search_queries(self, topics_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据外部化主题配置生成搜索查询参数（含技能/MCP 关键词发现）。"""
        queries: List[Dict[str, Any]] = []
        seen = set()
        for topic in topics_config.get("topics", []):
            for kw in topic.get("keywords", []):
                q = f'{kw} in:name,description,readme'
                if q in seen:
                    continue
                seen.add(q)
                queries.append(
                    {
                        "q": q,
                        "topic_id": topic.get("id"),
                        "sort": "stars",
                        "order": "desc",
                        "per_page": self.config.per_page,
                    }
                )
        # 显式追加技能 / MCP 定向发现
        for special in ["AGENTS.md in:readme", "model context protocol in:readme", "claude skill in:readme"]:
            queries.append({"q": special, "topic_id": "agent-skills", "sort": "updated", "order": "desc", "per_page": self.config.per_page})
        return queries

    def discover(self, topics_config: Dict[str, Any], max_queries: Optional[int] = None) -> Dict[str, Any]:
        """执行发现；返回统计信息。事务性写入：失败时整体回滚保护历史。"""
        queries = self.build_search_queries(topics_config)
        if max_queries:
            queries = queries[:max_queries]
        run_id = self.storage.start_collection_run(
            {"query_count": len(queries), "topics_version": topics_config.get("version")},
            source="collector.discover",
        )
        repos_seen: Dict[int, Repository] = {}
        snaps_seen: List[Snapshot] = []
        errors: List[str] = []
        try:
            for params in queries:
                try:
                    result = self._call_with_retry(
                        self.api.search_repositories, params
                    )
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{params.get('q')}: {exc}")
                    continue
                for raw in result.get("items", []):
                    try:
                        repo = self._parse_repo(raw)
                        snap = self._parse_snapshot(raw)
                    except Exception as exc:  # noqa: BLE001
                        errors.append(f"parse {raw.get('full_name')}: {exc}")
                        continue
                    repos_seen[repo.repository_id] = repo
                    snaps_seen.append(snap)
            self._persist(repos_seen, snaps_seen)
            status = "success" if not errors else "partial"
            self.storage.finish_collection_run(run_id, status)
        except Exception:
            self.storage.finish_collection_run(run_id, "failed")
            raise
        return {
            "run_id": run_id,
            "queries": len(queries),
            "repositories": len(repos_seen),
            "snapshots": len(snaps_seen),
            "errors": errors,
            "status": status,
        }

    def refresh_tracked(self, full_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """刷新已跟踪仓库的最新快照，确保掉出搜索结果的仓库仍被跟踪。"""
        if full_names is None:
            full_names = [r.full_name for r in self.storage.list_repositories()]
        run_id = self.storage.start_collection_run(
            {"full_names": full_names}, source="collector.refresh_tracked"
        )
        repos: Dict[int, Repository] = {}
        snaps: List[Snapshot] = []
        errors: List[str] = []
        try:
            for name in full_names:
                try:
                    raw = self._call_with_retry(self.api.get_repository, name)
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{name}: {exc}")
                    continue
                repo = self._parse_repo(raw)
                snap = self._parse_snapshot(raw)
                repos[repo.repository_id] = repo
                snaps.append(snap)
            self._persist(repos, snaps)
            self.storage.finish_collection_run(run_id, "success" if not errors else "partial")
        except Exception:
            self.storage.finish_collection_run(run_id, "failed")
            raise
        return {"run_id": run_id, "refreshed": len(repos), "errors": errors}

    def _persist(self, repos: Dict[int, Repository], snaps: List[Snapshot]) -> None:
        """在单一连接事务内写入仓库与快照；重复快照被幂等忽略。"""
        import sqlite3

        conn = sqlite3.connect(self.storage.db_path)
        try:
            for repo in repos.values():
                conn.execute(
                    """INSERT INTO repositories
                       (repository_id, full_name, description, language, topics, license,
                        created_at, homepage, default_branch, archived, first_seen_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(repository_id) DO UPDATE SET
                         full_name=excluded.full_name, description=excluded.description,
                         language=excluded.language, topics=excluded.topics,
                         license=excluded.license, created_at=excluded.created_at,
                         homepage=excluded.homepage, default_branch=excluded.default_branch,
                         archived=excluded.archived""",
                    (
                        repo.repository_id,
                        repo.full_name,
                        repo.description or "",
                        repo.language,
                        json.dumps(repo.topics, ensure_ascii=False),
                        repo.license,
                        repo.created_at,
                        repo.homepage,
                        repo.default_branch,
                        1 if repo.archived else 0,
                        repo.first_seen_at or utc_now_iso(),
                    ),
                )
            for snap in snaps:
                conn.execute(
                    """INSERT OR IGNORE INTO snapshots
                       (repository_id, captured_at, stargazers_count, forks_count,
                        watchers_count, open_issues_count, pushed_at, updated_at, release_info)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        snap.repository_id,
                        snap.captured_at,
                        snap.stargazers_count,
                        snap.forks_count,
                        snap.watchers_count,
                        snap.open_issues_count,
                        snap.pushed_at,
                        snap.updated_at,
                        json.dumps(snap.release_info or {}, ensure_ascii=False),
                    ),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
