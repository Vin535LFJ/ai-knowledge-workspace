"""GitHub REST 数据源客户端（两个实现并存，2026-11-21 阶段 4 解冻后落地）。

- `RestSourceClient`：**离线 stub**（保持"绝对无网络调用"测试契约，默认不参与采集）。
- `GitHubRestClient`：**真实联网客户端**（仅 CLI `--source rest` 显式启用）。

GitHubRestClient 设计要点：
- **令牌只走环境变量**：`GITHUB_TOKEN` 存在则携带 Bearer 认证；不存在则匿名
  （核心 API 60 req/h、搜索 API ~10 req/min），由内部节流（min_interval_seconds）
  与 collector 的退避重试共同兜底。
- **速率限制感知**：HTTP 403/429 抛 RateLimitError（消息含 "rate limit"，
  供 collector._call_with_retry 识别并休眠）；响应头 X-RateLimit-Remaining
  映射为 `_rate_limit_remaining`（collector 见 0 会休眠 60 秒）。
- **字段形状**：GitHub REST 返回的 repo 对象即为 collector._parse_repo /
  _parse_snapshot 消费的形状（full_name/description/topics/license/stargazers_count
  等），此处直接透传，不做二次映射。
- fetch_trending / fetch_insights：GitHub REST 无对应端点，返回空结果并注明
  （trending.py/ossinsight.py 接入后启用）。
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

from .base import SourceClient

API_BASE = "https://api.github.com"
DEFAULT_TIMEOUT_SECONDS = 30


class RateLimitError(Exception):
    """速率限制/配额类错误；消息刻意含 'rate limit' 供 collector 识别退避。"""


class RestSourceClient(SourceClient):
    """离线 REST 适配器 stub：返回 fixture 形状数据，不做任何网络 I/O。

    保持既有测试契约（SourceAdapterTests：绝对无网络调用）。真实联网采集
    请用 GitHubRestClient（CLI --source rest）。
    """

    def fetch_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}

    def fetch_trending(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}

    def fetch_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}


class GitHubRestClient(SourceClient):
    """GitHub REST v3 真实客户端：stdlib urllib，无第三方依赖（D05 原则）。

    匿名与认证共用同一实现——令牌仅通过环境变量 `GITHUB_TOKEN` 提供，
    构造参数可显式覆盖（测试注入用），禁止硬编码。
    """

    def __init__(
        self,
        token: Any = None,
        per_page: int = 30,
        min_interval_seconds: float = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ):
        if token is None:
            token = os.environ.get("GITHUB_TOKEN") or None
        self.token = token
        self.per_page = per_page
        # 匿名搜索 ~10 req/min → 7 秒间隔；带 Token 放宽到 1 秒
        if min_interval_seconds is None:
            min_interval_seconds = 1.0 if self.token else 7.0
        self.min_interval_seconds = float(min_interval_seconds)
        self.timeout_seconds = timeout_seconds
        self._last_request_monotonic = None
        self.anonymous = self.token is None

    # ---------- HTTP ----------

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ai-knowledge-radar/1.0 (stdlib urllib)",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _pace(self):
        if self._last_request_monotonic is None:
            return
        elapsed = time.monotonic() - self._last_request_monotonic
        remaining = self.min_interval_seconds - elapsed
        if remaining > 0:
            time.sleep(remaining)

    def _get(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        self._pace()
        url = API_BASE + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers=self._headers(), method="GET")
        self._last_request_monotonic = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as resp:
                body = resp.read().decode("utf-8")
                remaining = resp.headers.get("X-RateLimit-Remaining")
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                raise RateLimitError(
                    f"rate limit hit (HTTP {exc.code}) at {path}"
                ) from exc
            excerpt = (exc.read().decode("utf-8", errors="replace"))[:300]
            raise RuntimeError(f"GitHub API HTTP {exc.code} at {path}: {excerpt}") from exc
        data = json.loads(body)
        if remaining is not None:
            try:
                data["_rate_limit_remaining"] = int(remaining)
            except ValueError:
                pass
        return data

    # ---------- SourceClient / ApiClient 契约 ----------

    def fetch_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """SourceClient ABC 契约方法（base.py）：等价于 search_repositories。"""
        return self.search_repositories(params)

    def search_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = {
            "q": params.get("q", ""),
            "sort": params.get("sort", "stars"),
            "order": params.get("order", "desc"),
            "per_page": int(params.get("per_page", self.per_page)),
        }
        data = self._get("/search/repositories", query)
        return {"items": data.get("items", [])}

    def get_repository(self, full_name: str) -> Dict[str, Any]:
        safe = urllib.parse.quote(full_name, safe="/")
        return self._get(f"/repos/{safe}")

    def fetch_trending(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "GitHub REST 无 trending 端点；待 trending.py/ossinsight.py 接入"}

    def fetch_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "GitHub REST 无独立 insights 端点；待 ossinsight.py 接入"}
