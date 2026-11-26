#!/usr/bin/env python3
"""Generate the VitePress content tree from the AI Knowledge-to-Learning Engine markdown sources.

Usage:
    python tools/build_vitepress_content.py

Outputs (all generated, git-ignored):
    site-vitepress/docs/**                  curated markdown content tree
    site-vitepress/docs/index.md            generated home page
    site-vitepress/.vitepress/sidebar.generated.json

Same source of truth as tools/build_site.py (stdlib only).

2026-11-24 强制发布边界 v2：文档集由 tools/publish-allowlist.json 决定（target="online"，
仅 public）。archive/ 的 online=forbidden（D10.4：离线站保留只读归档，不自动扩大为在线
发布）；excluded-internal（DECISIONS/CHANGELOG/WORKFLOW_STATE/课程根审核材料等）永不进入。
注册表缺失/损坏/与磁盘不一致 → 构建失败，不留下半成品站点树。
在线发布本身仍受 D02 人工授权约束；本脚本只生成镜像内容树。
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT
DOCS = ROOT / "site-vitepress" / "docs"
SIDEBAR_PATH = ROOT / "site-vitepress" / ".vitepress" / "sidebar.generated.mjs"

PUBLISH_TARGET = "online"

TOP_ORDER = [
    "00-导航与索引",
    "01-基础理论",
    "02-解码与播放链路",
    "03-图形与GPU工程",
    "04-跨平台与高性能架构",
    "05-项目实战",
    "06-面试知识库",
    "07-3D渲染与算法实现",
    "08-具身智能",
    "courses",
    "docs",
]

SECTION_LABELS = {
    "00-导航与索引": "00 · 导航与索引",
    "01-基础理论": "01 · 基础理论",
    "02-解码与播放链路": "02 · 解码与播放链路",
    "03-图形与GPU工程": "03 · 图形与 GPU 工程",
    "04-跨平台与高性能架构": "04 · 跨平台与高性能架构",
    "05-项目实战": "05 · 项目实战",
    "06-面试知识库": "06 · 面试知识库",
    "07-3D渲染与算法实现": "07 · 3D 渲染与算法实现",
    "08-具身智能": "08 · 具身智能",
    "courses": "教学课程（pilot）",
    "docs": "使用指南",
}


def clean_label(stem: str) -> str:
    """Strip a leading numeric sort prefix like '01-' from a file stem."""
    return re.sub(r"^\d+-", "", stem)


def collect_markdown() -> list[Path]:
    """在线镜像文档集 = 注册表允许进入 online 的 .md（默认拒绝；未登记资产 = 失败）。"""
    import publish_boundary as pb

    registry = pb.load_registry()  # fail closed
    audit = pb.audit_registry(registry, ROOT)
    if not audit["ok"]:
        lines = [f"  - {m}" for m in audit["errors"]]
        lines += [f"  - unregistered asset (default=deny): {p}" for p in audit["unregistered"]]
        raise pb.RegistryError("publish registry / disk mismatch:\n" + "\n".join(lines))
    files = []
    for rel in pb.scan_assets(ROOT):
        if rel.endswith(".md") and pb.is_publishable(rel, target=PUBLISH_TARGET, registry=registry):
            files.append(ROOT / rel)
    return sorted(files)


def group_label(top: str) -> str:
    if top in SECTION_LABELS:
        return SECTION_LABELS[top]
    return top


def build_sidebar(files: list[Path]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for path in files:
        rel = path.relative_to(SRC).as_posix()
        top = rel.split("/", 1)[0] if "/" in rel else ""
        link = "/" + rel[:-3]  # strip .md
        groups.setdefault(top, []).append({"text": clean_label(path.stem), "link": link})
    ordered = [t for t in TOP_ORDER if t in groups] + [t for t in groups if t not in TOP_ORDER]
    sidebar = []
    for top in ordered:
        if top == "":
            continue
        items = sorted(groups[top], key=lambda i: i["text"])
        sidebar.append({"text": group_label(top), "collapsed": True, "items": items})
    return sidebar


def write_home(files: list[Path]) -> None:
    def has(target: str) -> bool:
        return any(p.relative_to(SRC).as_posix() == target for p in files)

    actions = []
    if has("00-导航与索引/知识架构总览.md"):
        actions.append(('brand', "知识架构总览", "/00-导航与索引/知识架构总览"))
    if has("courses/video-rendering-journey/README.md"):
        actions.append(('alt', "教学课程 · 一帧视频如何从文件抵达屏幕", "/courses/video-rendering-journey/README"))
    if has("00-导航与索引/学习路径指南.md"):
        actions.append(('alt', "学习路径指南", "/00-导航与索引/学习路径指南"))
    action_lines = "\n".join(
        '    - theme: %s\n      text: %s\n      link: %s' % item
        for item in actions
    )
    features = [
        {"title": "递进式知识地图", "details": "从像素格式、时间戳到 RenderGraph、MVP，概念之间有明确的依赖与桥接。"},
        {"title": "教学课程闭环", "details": "5 篇教学样章 + 配套 quiz 与交互实验，全部回指主文档锚点，不复制正文。"},
        {"title": "断言可溯源", "details": "evidence 层给每条关键断言登记来源与置信度；AI 生成内容不自动标验证。"},
    ]
    feature_lines = "\n".join(
        "  - title: %s\n    details: %s" % (f["title"], f["details"]) for f in features
    )
    content = f"""---
layout: home

hero:
  name: AI Knowledge-to-Learning Engine
  text: 音视频与 GPU 渲染知识库
  tagline: 在线镜像站。离线主站在仓库 web/ 目录，双击 index.html 即可打开。
  actions:
{action_lines}

features:
{feature_lines}
"""
    (DOCS / "index.md").write_text(content, encoding="utf-8")


def main() -> None:
    # 先在内存中确定文档集；注册表/审计失败时不动现有站点树（不留下半成品）。
    files = collect_markdown()
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    for path in files:
        rel = path.relative_to(SRC)
        dest = DOCS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)

    write_home(files)

    sidebar = build_sidebar(files)
    SIDEBAR_PATH.parent.mkdir(parents=True, exist_ok=True)
    SIDEBAR_PATH.write_text(
        "// Generated by tools/build_vitepress_content.py — do not edit.\n"
        "export default " + json.dumps(sidebar, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    # index.md is generated too; keep it out of the sidebar duplication.
    print(f"Wrote {DOCS.relative_to(ROOT)} with {len(files)} documents + index.md")
    print(f"Wrote {SIDEBAR_PATH.relative_to(ROOT)} ({len(sidebar)} groups)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — 注册表/IO 失败 = 构建失败，非零退出
        print(f"VITEPRESS BUILD FAILED: {exc}", file=sys.stderr)
        sys.exit(2)
