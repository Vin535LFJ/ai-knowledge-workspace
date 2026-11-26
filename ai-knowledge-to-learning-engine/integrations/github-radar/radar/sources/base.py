"""数据源客户端抽象接口（增量新增）。

SourceClient 与 radar.collector.ApiClient 协议对齐：方法接收 params 字典，
返回 dict。本接口只定义方法契约，任何实现都不得在构造或调用时发起真实网络
请求；未来接入真实 API 时令牌必须通过环境变量提供，禁止硬编码。

离线 stub 实现见 rest.py / trending.py / ossinsight.py。
默认注入客户端仍是 fixtures/client.py，本模块不参与默认采集。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class SourceClient(ABC):
    """数据源客户端抽象基类（接口契约）。

    方法签名：
        fetch_repositories(params) -> dict   仓库搜索/详情，形如 {"items": [repo_dict, ...]}
        fetch_trending(params)     -> dict   趋势列表
        fetch_insights(params)     -> dict   洞察/指标数据

    所有实现必须是离线的：本轮不允许任何真实网络调用。
    """

    @abstractmethod
    def fetch_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """按参数获取仓库数据，返回 fixture 形状的 dict。"""

    @abstractmethod
    def fetch_trending(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """按参数获取趋势数据，返回 fixture 形状的 dict。"""

    @abstractmethod
    def fetch_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """按参数获取洞察数据，返回 fixture 形状的 dict。"""
