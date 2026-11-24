"""核心数据模型：以 dataclass 定义系统与存储层之间流转的实体。

所有时间戳统一使用 ISO-8601 字符串（UTC），便于跨工具比对与审计。
本模块不依赖任何第三方库。
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    """返回当前的 UTC ISO-8601 时间字符串（秒级精度）。"""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Repository:
    """GitHub 仓库的元数据快照（不随时间变化的身份信息）。"""

    repository_id: int
    full_name: str
    description: str = ""
    language: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    license: Optional[str] = None
    created_at: Optional[str] = None
    homepage: Optional[str] = None
    default_branch: str = "main"
    archived: bool = False
    first_seen_at: Optional[str] = None
    # 溯源字段（增量新增，带默认值，确保 to_dict/from_dict 往返透传）
    source_url: Optional[str] = None
    observed_at: Optional[str] = None
    retrieved_at: Optional[str] = None
    data_quality: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Repository":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Snapshot:
    """仓库在某一采集时刻的指标快照。历史只增不改。"""

    repository_id: int
    captured_at: str
    stargazers_count: int = 0
    forks_count: int = 0
    watchers_count: int = 0
    open_issues_count: int = 0
    pushed_at: Optional[str] = None
    updated_at: Optional[str] = None
    release_info: Dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None
    # 溯源字段（增量新增，带默认值，确保 to_dict/from_dict 往返透传）
    source_url: Optional[str] = None
    observed_at: Optional[str] = None
    retrieved_at: Optional[str] = None
    data_quality: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Snapshot":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Candidate:
    """进入候选池的仓库及其发现依据、评分与人工复核状态。"""

    repository_id: int
    topic: str
    discovery_reason: Dict[str, Any] = field(default_factory=dict)
    evaluation: Dict[str, Any] = field(default_factory=dict)
    review_status: str = "Discovered"
    research_objective: str = ""
    created_at: Optional[str] = None
    id: Optional[int] = None
    # 人工选择标志：只有 true 才允许导入 Engine source inbox
    human_selected_for_research: bool = False
    # 溯源字段（增量新增，带默认值，确保 to_dict/from_dict 往返透传）
    source_url: Optional[str] = None
    observed_at: Optional[str] = None
    retrieved_at: Optional[str] = None
    data_quality: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candidate":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Evaluation:
    """评分结果：每个维度含分数、理由与数据依据。"""

    innovation: Dict[str, Any] = field(default_factory=dict)
    relevance: Dict[str, Any] = field(default_factory=dict)
    engineering_maturity: Dict[str, Any] = field(default_factory=dict)
    reusability: Dict[str, Any] = field(default_factory=dict)
    growth_momentum: Dict[str, Any] = field(default_factory=dict)
    total: float = 0.0
    group: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evaluation":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
