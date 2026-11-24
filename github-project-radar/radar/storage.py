"""存储层：SQLite 表结构定义与幂等、失败安全的读写封装。

设计要点：
- 快照只增不改：按 (repository_id, captured_at) 唯一约束，重复写入被忽略。
- 所有写操作使用事务；异常时回滚，绝不留下半写入的损坏历史。
- 采集运行（collection_runs）记录查询参数、来源与时间，满足可审计性。
"""

import json
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional

from .models import Candidate, Repository, Snapshot, utc_now_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS repositories (
    repository_id   INTEGER PRIMARY KEY,
    full_name       TEXT NOT NULL,
    description     TEXT,
    language        TEXT,
    topics          TEXT,          -- JSON array
    license         TEXT,
    created_at      TEXT,
    homepage        TEXT,
    default_branch  TEXT,
    archived        INTEGER DEFAULT 0,
    first_seen_at   TEXT NOT NULL,
    source_url      TEXT,
    observed_at     TEXT,
    retrieved_at    TEXT,
    data_quality    TEXT
);

CREATE TABLE IF NOT EXISTS snapshots (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_id      INTEGER NOT NULL,
    captured_at        TEXT NOT NULL,
    stargazers_count   INTEGER NOT NULL DEFAULT 0,
    forks_count        INTEGER NOT NULL DEFAULT 0,
    watchers_count     INTEGER NOT NULL DEFAULT 0,
    open_issues_count  INTEGER NOT NULL DEFAULT 0,
    pushed_at          TEXT,
    updated_at         TEXT,
    release_info       TEXT,       -- JSON object
    source_url         TEXT,
    observed_at        TEXT,
    retrieved_at       TEXT,
    data_quality       TEXT,
    UNIQUE(repository_id, captured_at),
    FOREIGN KEY(repository_id) REFERENCES repositories(repository_id)
);

CREATE INDEX IF NOT EXISTS idx_snapshots_repo_time
    ON snapshots(repository_id, captured_at);

CREATE TABLE IF NOT EXISTS collection_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at    TEXT NOT NULL,
    query_params  TEXT,            -- JSON
    source        TEXT,
    status        TEXT NOT NULL    -- running | success | failed
);

CREATE TABLE IF NOT EXISTS candidates (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_id      INTEGER NOT NULL,
    topic              TEXT NOT NULL,
    discovery_reason   TEXT,       -- JSON
    evaluation         TEXT,       -- JSON
    review_status      TEXT NOT NULL DEFAULT 'Discovered',
    research_objective TEXT,
    created_at         TEXT NOT NULL,
    human_selected_for_research INTEGER DEFAULT 0,
    source_url         TEXT,
    observed_at        TEXT,
    retrieved_at       TEXT,
    data_quality       TEXT,
    UNIQUE(repository_id, topic),
    FOREIGN KEY(repository_id) REFERENCES repositories(repository_id)
);
"""


class Storage:
    """对 SQLite 的轻量封装。传入不同 db_path 即可用于测试（tempfile）。"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """建立全部表结构（可重复调用，幂等）；对旧库追加缺失列。"""
        with self._connect() as conn:
            conn.executescript(SCHEMA)
            # 向后兼容：旧数据库通过 ALTER 补齐增量列，不破坏既有数据。
            self._ensure_columns(conn, {
                "repositories": {
                    "source_url": "TEXT", "observed_at": "TEXT",
                    "retrieved_at": "TEXT", "data_quality": "TEXT",
                },
                "snapshots": {
                    "source_url": "TEXT", "observed_at": "TEXT",
                    "retrieved_at": "TEXT", "data_quality": "TEXT",
                },
                "candidates": {
                    "human_selected_for_research": "INTEGER DEFAULT 0",
                    "source_url": "TEXT", "observed_at": "TEXT",
                    "retrieved_at": "TEXT", "data_quality": "TEXT",
                },
            })
            conn.commit()

    @staticmethod
    def _ensure_columns(conn, columns: Dict[str, Dict[str, str]]) -> None:
        """为已存在的表追加缺失列（SQLite 不支持 IF NOT EXISTS 的列语法）。"""
        for table, specs in columns.items():
            existing = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            for name, ddl in specs.items():
                if name not in existing:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")

    # ---------- repositories ----------

    def upsert_repository(self, repo: Repository) -> None:
        """写入或更新仓库元数据。first_seen_at 一旦确定不再更改。"""
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO repositories
                        (repository_id, full_name, description, language, topics,
                         license, created_at, homepage, default_branch, archived, first_seen_at,
                         source_url, observed_at, retrieved_at, data_quality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(repository_id) DO UPDATE SET
                        full_name=excluded.full_name,
                        description=excluded.description,
                        language=excluded.language,
                        topics=excluded.topics,
                        license=excluded.license,
                        created_at=excluded.created_at,
                        homepage=excluded.homepage,
                        default_branch=excluded.default_branch,
                        archived=excluded.archived,
                        source_url=excluded.source_url,
                        observed_at=excluded.observed_at,
                        retrieved_at=excluded.retrieved_at,
                        data_quality=excluded.data_quality
                    """,
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
                        repo.source_url,
                        repo.observed_at,
                        repo.retrieved_at,
                        repo.data_quality,
                    ),
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def get_repository(self, repository_id: int) -> Optional[Repository]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM repositories WHERE repository_id = ?", (repository_id,)
            ).fetchone()
        return self._row_to_repo(row) if row else None

    def get_repository_by_name(self, full_name: str) -> Optional[Repository]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM repositories WHERE full_name = ?", (full_name,)
            ).fetchone()
        return self._row_to_repo(row) if row else None

    def list_repositories(self) -> List[Repository]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM repositories ORDER BY full_name").fetchall()
        return [self._row_to_repo(r) for r in rows]

    @staticmethod
    def _row_to_repo(row: sqlite3.Row) -> Repository:
        d = dict(row)
        d["topics"] = json.loads(d.get("topics") or "[]")
        d["archived"] = bool(d.get("archived"))
        return Repository.from_dict(d)

    # ---------- snapshots ----------

    def insert_snapshot(self, snap: Snapshot) -> bool:
        """插入快照。返回 True 表示新增，False 表示该时刻快照已存在（幂等忽略）。"""
        with self._connect() as conn:
            try:
                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO snapshots
                        (repository_id, captured_at, stargazers_count, forks_count,
                         watchers_count, open_issues_count, pushed_at, updated_at, release_info,
                         source_url, observed_at, retrieved_at, data_quality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
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
                        snap.source_url,
                        snap.observed_at,
                        snap.retrieved_at,
                        snap.data_quality,
                    ),
                )
                conn.commit()
                return cur.rowcount == 1
            except Exception:
                conn.rollback()
                raise

    def insert_snapshots(self, snaps: Iterable[Snapshot]) -> int:
        """批量插入，单事务；返回实际新增数量。"""
        added = 0
        with self._connect() as conn:
            try:
                for snap in snaps:
                    cur = conn.execute(
                        """
                        INSERT OR IGNORE INTO snapshots
                            (repository_id, captured_at, stargazers_count, forks_count,
                             watchers_count, open_issues_count, pushed_at, updated_at, release_info,
                             source_url, observed_at, retrieved_at, data_quality)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
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
                            snap.source_url,
                            snap.observed_at,
                            snap.retrieved_at,
                            snap.data_quality,
                        ),
                    )
                    added += 1 if cur.rowcount == 1 else 0
                conn.commit()
                return added
            except Exception:
                conn.rollback()
                raise

    def get_snapshots(
        self, repository_id: int, since: Optional[str] = None
    ) -> List[Snapshot]:
        with self._connect() as conn:
            if since:
                rows = conn.execute(
                    """SELECT * FROM snapshots
                       WHERE repository_id = ? AND captured_at >= ?
                       ORDER BY captured_at ASC""",
                    (repository_id, since),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT * FROM snapshots
                       WHERE repository_id = ? ORDER BY captured_at ASC""",
                    (repository_id,),
                ).fetchall()
        return [self._row_to_snap(r) for r in rows]

    @staticmethod
    def _row_to_snap(row: sqlite3.Row) -> Snapshot:
        d = dict(row)
        d["release_info"] = json.loads(d.get("release_info") or "{}")
        return Snapshot.from_dict(d)

    # ---------- collection_runs ----------

    def start_collection_run(
        self, query_params: Dict[str, Any], source: str
    ) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO collection_runs (started_at, query_params, source, status)
                   VALUES (?, ?, ?, 'running')""",
                (utc_now_iso(), json.dumps(query_params, ensure_ascii=False), source),
            )
            conn.commit()
            return cur.lastrowid

    def finish_collection_run(self, run_id: int, status: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE collection_runs SET status = ? WHERE id = ?", (status, run_id)
            )
            conn.commit()

    # ---------- candidates ----------

    def upsert_candidate(self, cand: Candidate) -> None:
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO candidates
                        (repository_id, topic, discovery_reason, evaluation,
                         review_status, research_objective, created_at,
                         human_selected_for_research, source_url, observed_at,
                         retrieved_at, data_quality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(repository_id, topic) DO UPDATE SET
                        discovery_reason=excluded.discovery_reason,
                        evaluation=excluded.evaluation,
                        review_status=excluded.review_status,
                        research_objective=excluded.research_objective,
                        human_selected_for_research=excluded.human_selected_for_research,
                        source_url=excluded.source_url,
                        observed_at=excluded.observed_at,
                        retrieved_at=excluded.retrieved_at,
                        data_quality=excluded.data_quality
                    """,
                    (
                        cand.repository_id,
                        cand.topic,
                        json.dumps(cand.discovery_reason or {}, ensure_ascii=False),
                        json.dumps(cand.evaluation or {}, ensure_ascii=False),
                        cand.review_status,
                        cand.research_objective or "",
                        cand.created_at or utc_now_iso(),
                        1 if cand.human_selected_for_research else 0,
                        cand.source_url,
                        cand.observed_at,
                        cand.retrieved_at,
                        cand.data_quality,
                    ),
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def list_candidates(
        self, review_status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            if review_status:
                rows = conn.execute(
                    """SELECT c.*, r.full_name FROM candidates c
                       JOIN repositories r ON r.repository_id = c.repository_id
                       WHERE c.review_status = ? ORDER BY c.created_at DESC""",
                    (review_status,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT c.*, r.full_name FROM candidates c
                       JOIN repositories r ON r.repository_id = c.repository_id
                       ORDER BY c.created_at DESC"""
                ).fetchall()
        result = []
        for row in rows:
            d = dict(row)
            d["discovery_reason"] = json.loads(d.get("discovery_reason") or "{}")
            d["evaluation"] = json.loads(d.get("evaluation") or "{}")
            d["human_selected_for_research"] = bool(d.get("human_selected_for_research", 0))
            result.append(d)
        return result

    def update_candidate_review(
        self,
        candidate_id: int,
        review_status: str,
        reviewer: str,
        decision: str,
        research_objective: str = "",
    ) -> None:
        """更新复核状态并记录复核人、时间、决定（追加到 evaluation.review_log）。"""
        with self._connect() as conn:
            try:
                row = conn.execute(
                    "SELECT evaluation FROM candidates WHERE id = ?", (candidate_id,)
                ).fetchone()
                if row is None:
                    raise ValueError(f"候选记录不存在: id={candidate_id}")
                evaluation = json.loads(row["evaluation"] or "{}")
                log = evaluation.setdefault("review_log", [])
                log.append(
                    {
                        "reviewer": reviewer,
                        "at": utc_now_iso(),
                        "from": evaluation.get("review_status", ""),
                        "to": review_status,
                        "decision": decision,
                    }
                )
                evaluation["review_status"] = review_status
                if research_objective:
                    evaluation["research_objective"] = research_objective
                conn.execute(
                    """UPDATE candidates SET review_status = ?, evaluation = ?,
                       research_objective = CASE WHEN ? != '' THEN ? ELSE research_objective END
                       WHERE id = ?""",
                    (
                        review_status,
                        json.dumps(evaluation, ensure_ascii=False),
                        research_objective,
                        research_objective,
                        candidate_id,
                    ),
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    def get_latest_snapshot(self, repository_id: int) -> Optional[Snapshot]:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT * FROM snapshots WHERE repository_id = ?
                   ORDER BY captured_at DESC LIMIT 1""",
                (repository_id,),
            ).fetchone()
        return self._row_to_snap(row) if row else None
