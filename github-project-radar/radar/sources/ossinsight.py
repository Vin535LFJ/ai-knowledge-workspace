"""OSSInsight 数据源客户端 stub（增量新增，离线，无网络）。

占位实现：只返回 fixture 形状的空结果，绝不调用 OSSInsight API。
未来接入时必须：
- API 令牌仅通过环境变量提供，不得硬编码；
- 遵守速率限制与数据使用条款；
- 仅在明确授权联网后才注入真实实现，默认采集仍走 fixtures/client.py。
"""

from typing import Any, Dict

from .base import SourceClient


class OSSInsightSourceClient(SourceClient):
    """离线 OSSInsight 适配器 stub：返回 fixture 形状数据，不做任何网络 I/O。"""

    def fetch_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}

    def fetch_trending(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}

    def fetch_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"items": [], "_note": "offline stub, no network"}
