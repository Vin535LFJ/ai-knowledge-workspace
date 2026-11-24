"""GitHub Project Radar —— 开源情报与技术发现系统。

本包仅使用 Python 标准库，所有网络访问都通过注入的客户端完成。
"""

import json
import os
from typing import Any, Dict

# 包根目录（…/github-project-radar）
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(PACKAGE_ROOT, "config")


def load_config(filename: str) -> Dict[str, Any]:
    """从 config/ 目录加载 JSON 配置。"""
    path = filename if os.path.isabs(filename) else os.path.join(CONFIG_DIR, filename)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
