"""离线样例 API 客户端：实现采集器所需协议，从 fixtures/sample_data.json 读取。

供 CLI 演示与测试使用。绝不发起网络请求。
"""

import json
import os
from typing import Any, Dict

FIXTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.json")


class FixtureApiClient:
    def __init__(self, fixture_path: str = FIXTURE_PATH):
        with open(fixture_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.repositories = data.get("repositories", [])

    def search_repositories(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """简单模拟：取查询的第一个关键词，在描述/主题/全名中做子串匹配。"""
        q = str(params.get("q", "")).lower()
        keyword = q.split(" ")[0] if q else ""
        if not keyword:
            return {"items": list(self.repositories), "_note": "offline fixture"}
        items = [
            r
            for r in self.repositories
            if keyword in (r.get("description") or "").lower()
            or any(keyword in t.lower() for t in r.get("topics", []))
            or keyword in (r.get("full_name") or "").lower()
        ]
        return {"items": items, "_note": "offline fixture"}

    def get_repository(self, full_name: str) -> Dict[str, Any]:
        for r in self.repositories:
            if r.get("full_name") == full_name:
                return r
        raise KeyError(f"fixture 中不存在仓库: {full_name}")
