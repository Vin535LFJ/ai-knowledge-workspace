#!/usr/bin/env python3
"""Build the offline browsing site data from the AI Knowledge-to-Learning Engine Markdown files.

Usage:
    python tools/build_site.py

The only output is web/content.js, which is consumed by web/assets/app.js.
No third-party Python packages are required.
"""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# 2026-11-24 强制发布边界 v2（用户批准）：注册表 tools/publish-allowlist.json 是唯一判定来源。
# 旧版路径排除 API（is_publishable(include_archive=...) / check_allowlist）已废除。
from publish_boundary import (  # noqa: E402
    RegistryError,
    audit_registry,
    load_registry,
    policy_for,
    require_site_data,
    scan_assets,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "web" / "content.js"
GRAPH_PATH = ROOT / "tools" / "graph.json"
PUBLISH_TARGET = "offline"  # 离线学习站；在线镜像（VitePress）用 target="online"

# Map each glossary group to a technical-index category. Groups not listed fall back to "concept".
TECH_CATEGORY_BY_GROUP = {
    "explicit-api": "api",
    "android-av": "api",
    "pipeline-resources": "api",
    "gpu-hardware": "algorithm",
    "culling-aa": "algorithm",
    "color-compression": "algorithm",
    "math-geometry": "concept",
    "sync-scheduling": "concept",
    "automotive": "topic",
    "procedural-graphics": "topic",
    "pbr-material": "topic",
}
TECH_CATEGORY_LABELS = {
    "api": "图形 / 媒体 API",
    "algorithm": "渲染 / 图像算法",
    "concept": "核心概念",
    "topic": "工程主题",
}

CATEGORY_ORDER = [
    "",
    "00-导航与索引",
    "01-基础理论",
    "02-解码与播放链路",
    "03-图形与GPU工程",
    "04-跨平台与高性能架构",
    "05-项目实战",
    "06-面试知识库",
    "07-3D渲染与算法实现",
    "archive",
]

REPO_URL = "https://github.com/Vin535LFJ/ai-knowledge-to-learning-engine"

SECTION_ENTRY = {
    "00-导航与索引": "00-导航与索引/知识架构总览.md",
    "01-基础理论": "01-基础理论/音视频基础理论.md",
    "02-解码与播放链路": "02-解码与播放链路/解码与播放链路.md",
    "03-图形与GPU工程": "03-图形与GPU工程/GPU与渲染引擎基础与链路.md",
    "04-跨平台与高性能架构": "04-跨平台与高性能架构/跨平台与高性能架构.md",
    "05-项目实战": "05-项目实战/项目实战指南.md",
    "06-面试知识库": "06-面试知识库/面试知识库.md",
    "07-3D渲染与算法实现": "07-3D渲染与算法实现/README.md",
    "archive": "archive/README.md",
}

SECTION_META = {
    "": {
        "icon": "◈",
        "summary": "仓库总览与阅读入口。",
        "question": "这套知识库解决什么问题？我该从哪里开始？",
    },
    "00-导航与索引": {
        "icon": "◈",
        "summary": "知识地图、学习路线、缺口登记与术语验真。",
        "question": "我现在该读哪一篇？这个概念属于哪一层？",
    },
    "01-基础理论": {
        "icon": "◉",
        "summary": "音视频与图形渲染的底层概念：像素格式、容器编码、时间戳、色彩。",
        "question": "视频为什么是 YUV？PTS/DTS/Stride 为什么容易出错？",
    },
    "02-解码与播放链路": {
        "icon": "▷",
        "summary": "从文件/网络到解码、纹理与播放时序的完整数据链。",
        "question": "一帧码流如何变成 GPU 可采样的纹理？ownership 在哪里切换？",
    },
    "03-图形与GPU工程": {
        "icon": "▦",
        "summary": "GPU 硬件模型、图形管线、FBO 多 Pass、带宽与移动端架构。",
        "question": "一帧怎么画出来？瓶颈为什么常在带宽而不是算力？",
    },
    "04-跨平台与高性能架构": {
        "icon": "⌗",
        "summary": "显式 API、RenderGraph、同步原语、零拷贝与智驾渲染方案。",
        "question": "如何把渲染变成可预测、可复用、可跨平台的工程系统？",
    },
    "05-项目实战": {
        "icon": "◇",
        "summary": "阶段目标、验收标准、性能数字口径与项目复盘。",
        "question": "如何把知识落成可交付、可讲述、可验证的项目经历？",
    },
    "06-面试知识库": {
        "icon": "✦",
        "summary": "车载渲染方向的高频问答、专题拆解与项目表达。",
        "question": "同一个知识点，如何讲成结论 + 原理 + 工程约束 + 反例？",
    },
    "07-3D渲染与算法实现": {
        "icon": "◐",
        "summary": "坐标变换、光照材质、阴影、图像算法与批处理实现。",
        "question": "矩阵、光照、采样与批处理如何真正落到 shader 和 Pass 上？",
    },
    "archive": {
        "icon": "▤",
        "summary": "历史手册与归档材料，保留原始脉络，不作为最新结论来源。",
        "question": "过去的资料如何追溯？哪些结论已经被主干文档取代？",
    },
}

SECTION_PREREQS = {
    "01-基础理论": [],
    "02-解码与播放链路": ["01-基础理论"],
    "03-图形与GPU工程": ["01-基础理论", "02-解码与播放链路"],
    "04-跨平台与高性能架构": ["03-图形与GPU工程"],
    "05-项目实战": ["04-跨平台与高性能架构"],
    "06-面试知识库": ["04-跨平台与高性能架构", "05-项目实战"],
    "07-3D渲染与算法实现": ["03-图形与GPU工程"],
    "archive": [],
}


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def section_key(doc_path: str) -> str:
    return doc_path.rsplit("/", 1)[0] if "/" in doc_path else ""


def top_key(doc_path: str) -> str:
    return doc_path.split("/", 1)[0] if "/" in doc_path else ""


def format_section(key: str) -> str:
    if not key:
        return "总览"
    labels = []
    for part in key.split("/"):
        match = re.match(r"^(\d{2})-(.*)$", part)
        if match:
            labels.append(f"{match.group(1)} · {match.group(2)}")
        elif part == "archive":
            labels.append("归档 · archive")
        else:
            labels.append(part)
    return " / ".join(labels)


def sort_key(doc_path: str):
    key = section_key(doc_path)
    try:
        category_index = CATEGORY_ORDER.index(key.split("/")[0])
    except ValueError:
        category_index = len(CATEGORY_ORDER)
    return (category_index, doc_path)


def truncate(text: str, limit: int = 140) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def strip_frontmatter(markdown: str) -> tuple[str, str]:
    """Split a leading YAML frontmatter block from the body.

    Returns (body, frontmatter). Body keeps everything after the closing
    ``---`` line; when no frontmatter exists, body is the original text.
    """
    match = re.match(r"\A---\s*\n.*?\n---\s*\n", markdown, re.DOTALL)
    if not match:
        return markdown, ""
    return markdown[match.end():], match.group(0)


def extract_title(markdown: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def extract_subtitle(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines[1:12]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            text = stripped.lstrip(">").strip()
            text = re.sub(r"\*\*|__|`", "", text)
            if text and not text.startswith("验证状态"):
                return truncate(text)
        if stripped.startswith("#") or stripped.startswith("---"):
            continue
        if stripped:
            text = re.sub(r"\*\*|__|`", "", stripped)
            return truncate(text)
    return ""


def plain_text(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$\n]*\$", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"^\s*[#>|]+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def glossary_url(term_name: str) -> str:
    return "#/glossary?term=" + quote(term_name, safe="")


def build_term_entries(glossary: dict) -> list[dict]:
    entries = []
    for group in glossary.get("groups", []):
        for term in group.get("terms", []):
            aliases = [term["name"], *(term.get("aliases") or [])]
            entries.append(
                {
                    "name": term["name"],
                    "aliases": aliases,
                    "short": term.get("short", ""),
                    "group": group.get("label", ""),
                }
            )
    entries.sort(key=lambda item: max(len(name) for name in item["aliases"]), reverse=True)
    return entries


def collect_term_hits(text: str, term_entries: list[dict]) -> list[tuple[dict, int]]:
    lowered = text.lower()
    hits = []
    for entry in term_entries:
        count = max(lowered.count(alias.lower()) for alias in entry["aliases"])
        if count:
            hits.append((entry, count))
    hits.sort(key=lambda item: (-item[1], item[0]["name"]))
    return hits


def relative_doc_link(current: str, target: str, label: str | None = None) -> str:
    base = posixpath.dirname(current)
    rel = posixpath.relpath(target, base) if base else target
    rel = rel.replace("\\", "/")
    text = label or Path(target).stem
    return f"[{text}]({rel})"


def build_chapter_intro(doc_path: str, hits: list[tuple[dict, int]], all_doc_ids: list[str]) -> str:
    top = top_key(doc_path)
    meta = SECTION_META.get(top, SECTION_META[""])
    lines = [
        "<!-- rn-generated-start -->",
        f"> **{meta['icon']} 章节定位** · {meta['summary']}",
        ">",
        f"> **本章核心问题**：{meta['question']}",
    ]

    architecture = "00-导航与索引/知识架构总览.md"
    if doc_path != architecture:
        lines.append(">")
        lines.append("> **知识地图**：" + relative_doc_link(doc_path, architecture, "知识架构总览"))

    prereqs = [
        SECTION_ENTRY[key]
        for key in SECTION_PREREQS.get(top, [])
        if key in SECTION_ENTRY and SECTION_ENTRY[key] != doc_path
    ]
    if prereqs:
        lines.append(">")
        lines.append("> **前置知识**：" + " · ".join(relative_doc_link(doc_path, p) for p in prereqs))

    siblings = [
        doc_id
        for doc_id in all_doc_ids
        if top_key(doc_id) == top and doc_id != doc_path and doc_id != architecture
    ][:6]
    if siblings:
        lines.append(">")
        lines.append("> **同章文档**：" + " · ".join(relative_doc_link(doc_path, s) for s in siblings))

    if hits:
        lines.append(">")
        lines.append("> **本章术语**：")
        for entry, count in hits[:8]:
            link = f"[{entry['name']}]({glossary_url(entry['name'])})"
            lines.append(f"> - {link} — {truncate(entry['short'], 64)}（出现 {count} 次）")

    lines.append("")
    return "\n".join(lines)


PROTECT_PATTERNS = [
    r"`[^`\n]*`",
    r"\[[^\]\n]*\]\([^)\n]*\)",
    r"\$\$.*?\$\$",
    r"\$[^$\n]*\$",
    r"<!--.*?-->",
]


def protected_ranges(line: str) -> list[tuple[int, int]]:
    ranges = []
    for pattern in PROTECT_PATTERNS:
        for match in re.finditer(pattern, line):
            ranges.append((match.start(), match.end()))
    return ranges


def find_free(text: str, needle: str, ranges: list[tuple[int, int]]) -> int:
    lowered = text.lower()
    target = needle.lower()
    cursor = 0
    while True:
        index = lowered.find(target, cursor)
        if index < 0:
            return -1
        end = index + len(target)
        if not any(index < stop and end > start for start, stop in ranges):
            return index
        cursor = index + 1


def inject_inline_term_links(markdown: str, selected: list[tuple[dict, int]]) -> str:
    if not selected:
        return markdown
    used: set[str] = set()
    output = []
    in_fence = False
    in_math = False

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence or stripped.startswith("<!--"):
            output.append(line)
            continue
        # 2026-11-24 公式乱码修复：$$ display 公式块（可跨行）内禁止注入术语链接。
        # 此前 PROTECT_PATTERNS 只保护单行 $...$，多行 $$ 块内的 NDC 等术语被注入
        # [NDC](#/glossary?term=NDC)，KaTeX 收到 Markdown 链接语法导致公式乱码。
        if in_math:
            output.append(line)
            if stripped.endswith("$$"):
                in_math = False
            continue
        if stripped.startswith("$$"):
            output.append(line)
            if not (stripped.endswith("$$") and len(stripped) > 2):
                in_math = True
            continue
        if stripped.startswith("#") or stripped.startswith("|") or stripped.startswith(">"):
            output.append(line)
            continue

        processed = line
        ranges = protected_ranges(processed)
        for entry, _count in selected:
            if entry["name"] in used:
                continue
            url = glossary_url(entry["name"])
            placed = False
            for alias in entry["aliases"]:
                index = find_free(processed, alias, ranges)
                if index < 0:
                    continue
                processed = (
                    processed[:index]
                    + f"[{alias}]({url})"
                    + processed[index + len(alias) :]
                )
                used.add(entry["name"])
                placed = True
                break
            if placed:
                ranges = protected_ranges(processed)
        output.append(processed)

    return "\n".join(output)


def augment_markdown(markdown: str, doc_path: str, term_entries: list[dict], all_doc_ids: list[str]) -> tuple[str, list[dict]]:
    if "<!-- rn-generated-start -->" in markdown:
        return markdown, []
    plain = plain_text(markdown)
    hits = collect_term_hits(plain, term_entries)
    enriched = inject_inline_term_links(markdown, hits[:12])
    intro = build_chapter_intro(doc_path, hits, all_doc_ids)

    lines = enriched.splitlines()
    heading_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if heading_index is None:
        lines = [intro] + lines
    else:
        lines.insert(heading_index + 1, "\n" + intro)

    term_meta = [
        {"name": entry["name"], "count": count, "group": entry["group"]}
        for entry, count in hits[:8]
    ]
    return "\n".join(lines), term_meta


def build_tech_index(glossary: dict) -> dict:
    """Derive a browsable technical index from the glossary groups (no second curated file)."""
    categories: dict[str, list] = {key: [] for key in TECH_CATEGORY_LABELS}
    for group in glossary.get("groups", []):
        category = TECH_CATEGORY_BY_GROUP.get(group.get("id", ""), "concept")
        for term in group.get("terms", []):
            name = term.get("name", "")
            if not name:
                continue
            categories[category].append({
                "name": name,
                "aliases": term.get("aliases", []) or [],
                "summary": term.get("short", ""),
                "group": group.get("label", ""),
                "route": "#/glossary?term=" + quote(name),
            })
    order = ["api", "algorithm", "concept", "topic"]
    return {
        "categories": [
            {"id": key, "label": TECH_CATEGORY_LABELS[key], "items": categories[key]}
            for key in order if categories[key]
        ]
    }


def build_payload() -> dict:
    # 强制发布边界 v2（2026-11-24）：
    #  1. 注册表缺失/损坏/不合规 → RegistryError → 构建失败（fail closed，无 advisory 回退）。
    #  2. 注册表 ↔ 磁盘审计：扫描空间内未登记资产 = 构建失败（默认拒绝，必须显式登记）。
    #  3. 文档只从注册表允许进入本 target 的资产中产生；excluded-internal 永不进入。
    registry = load_registry()
    audit = audit_registry(registry, ROOT)
    if not audit["ok"]:
        lines = [f"  - {m}" for m in audit["errors"]]
        lines += [f"  - unregistered asset (default=deny): {p}" for p in audit["unregistered"]]
        raise RegistryError("publish registry / disk mismatch:\n" + "\n".join(lines))

    def load_site_data(rel: str):
        require_site_data(rel, registry=registry)
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    markdown_files: list[Path] = []
    doc_policies: dict[str, str] = {}
    for rel in scan_assets(ROOT):  # 符号链接逃逸在此处抛错
        if not rel.endswith(".md"):
            continue
        policy = policy_for(rel, registry)
        if policy in ("public", "offline-read-only"):
            doc_policies[rel] = policy
            markdown_files.append(ROOT / rel)
    markdown_files.sort(key=lambda p: sort_key(relpath(p)))
    all_doc_ids = [relpath(path) for path in markdown_files]

    glossary = load_site_data("tools/glossary.json")
    course = load_site_data("tools/course.json")
    labs = load_site_data("tools/labs.json")
    graph = load_site_data("tools/graph.json") if GRAPH_PATH.exists() else {"nodes": [], "edges": [], "views": []}
    term_entries = build_term_entries(glossary)

    # 2026-11-25 精选数据呈现（TASK 0 收口）：注册表 policy=curated-data 的资产（证据来源注册表、
    # 知识模型）是**唯一**被授权进入站点的证据/知识数据，这里显式嵌入 payload.curated，
    # 并经 require_site_data 强制校验（未登记 / excluded-internal → 构建失败）。
    # claim-ledger.json（含未审核断言与内部验证状态）永远不在此集合中。
    curated: dict = {}
    curated_manifest: list = []
    for rel in sorted(registry["_by_path"]):
        if registry["_by_path"][rel]["policy"] == "curated-data":
            curated[rel] = load_site_data(rel)
            curated_manifest.append({
                "path": rel,
                "sha256": hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(),
            })
    # 断言编号 → 来源（只取来源注册表的 used_by_claims 反向索引；不读断言台账）。
    sources_by_claim: dict[str, list] = {}
    for source in curated.get("evidence/source-registry.json", {}).get("sources", []):
        for cid in source.get("used_by_claims") or []:
            sources_by_claim.setdefault(str(cid), []).append(source)
    # 定义文档 → 概念（知识模型只发布概念 ID/名称/路由/已登记关系）。
    concepts_by_doc: dict[str, list] = {}
    for concept in curated.get("knowledge-model/concepts.json", {}).get("concepts", []):
        concepts_by_doc.setdefault(concept.get("definition_ref"), []).append(concept)

    docs = []
    manifest_docs = []
    sections = []
    linked_term_total = 0
    for path in markdown_files:
        doc_path = relpath(path)
        key = section_key(doc_path)
        raw_bytes = path.read_bytes()  # 读取失败 = OSError = 构建失败，不静默跳过
        markdown = raw_bytes.decode("utf-8", errors="replace")
        markdown, _frontmatter = strip_frontmatter(markdown)
        fallback = path.stem
        plain = plain_text(markdown)
        enriched, term_meta = augment_markdown(markdown, doc_path, term_entries, all_doc_ids)
        linked_term_total += len(term_meta)
        # 本文引用的证据来源：正文出现的断言编号 ∩ 来源注册表。只输出引用信息（标题/链接/类型），
        # 不输出断言的验证状态（那在 claim-ledger.json，属 excluded-internal）。
        mentioned = set(re.findall(r"\bV\d{2,3}\b", markdown)) & set(sources_by_claim)
        cited: dict[str, list] = {}
        for cid in sorted(mentioned):
            for source in sources_by_claim[cid]:
                cited.setdefault(source.get("id"), []).append(cid)
        evidence = []
        for sid in sorted(cited):
            source = next(s for c in cited[sid] for s in sources_by_claim[c] if s.get("id") == sid)
            url = str(source.get("url") or "")
            evidence.append({
                "id": sid,
                "title": str(source.get("title") or sid),
                "url": url if url.startswith(("http://", "https://")) else "",
                "type": str(source.get("type") or ""),
                "claims": sorted(cited[sid]),
            })
        concepts = [
            {
                "id": str(c.get("id") or ""),
                "name": str(c.get("name") or ""),
                "route": str(c.get("route") or ""),
                "relations": [
                    {"type": str(r.get("type") or ""), "target": str(r.get("target") or ""), "source_claim": str(r.get("source_claim") or "")}
                    for r in (c.get("relations") or []) if isinstance(r, dict)
                ],
            }
            for c in concepts_by_doc.get(doc_path, [])
        ]
        doc = {
            "id": doc_path,
            "path": doc_path,
            "publishPolicy": doc_policies[doc_path],
            "title": extract_title(markdown, fallback),
            "sectionKey": key,
            "section": format_section(key),
            "subtitle": extract_subtitle(markdown),
            "words": len(plain),
            "minutes": max(1, round(len(plain) / 400)),
            "markdown": enriched,
            "plain": plain,
            "terms": term_meta,
            "evidence": evidence,
            "concepts": concepts,
        }
        docs.append(doc)
        manifest_docs.append({
            "path": doc_path,
            "policy": doc_policies[doc_path],
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        })
        if not sections or sections[-1]["key"] != key:
            sections.append(
                {
                    "key": key,
                    "label": format_section(key),
                    "items": [],
                }
            )
        sections[-1]["items"].append(doc_path)

    # 2026-11-24 多课程最小扩展（用户批准）：additive courses[] payload。
    # 主课程在首位，courses/*/course.json 依次追加；旧 UI 读 .course 不受影响。
    # 每个课程契约必须是已登记的 site-data，否则构建失败。
    courses_payload = [course]
    courses_dir = ROOT / "courses"
    if courses_dir.exists():
        for cd in sorted(p for p in courses_dir.iterdir() if p.is_dir()):
            cj = cd / "course.json"
            if cj.exists():
                cdata = load_site_data(cj.relative_to(ROOT).as_posix())
                if cdata.get("id") != course.get("id"):
                    courses_payload.append(cdata)

    payload = {
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "repo": REPO_URL,
        "docs": docs,
        "sections": sections,
        "order": [doc["id"] for doc in docs],
        "glossary": glossary,
        "course": course,
        "courses": courses_payload,
        "labs": labs,
        "graph": graph,
        "curated": curated,
        "techIndex": build_tech_index(glossary),
        "sectionMeta": SECTION_META,
        # 可追溯的最终发布清单：每篇文档的策略与源文件 SHA256（审批证据链据此比对）。
        "publishManifest": {
            "registry": "tools/publish-allowlist.json",
            "registryVersion": registry["version"],
            "target": PUBLISH_TARGET,
            "docs": manifest_docs,
            "curated": curated_manifest,
        },
    }
    return payload


def main() -> None:
    try:
        payload = build_payload()
    except (RegistryError, OSError, ValueError) as exc:
        # 构建失败：不写任何产物，已有 bundle 保持原样（不会被半成品污染）。
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        sys.exit(2)

    # Escape sequences that would otherwise terminate the inline <script> block.
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    raw = raw.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    content = "window.RENDER_NOTES = " + raw + ";\n"
    # 先写临时文件并回读校验，再原子替换正式产物；失败时正式 bundle 不变。
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT.with_name(OUTPUT.name + ".tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        check = tmp.read_text(encoding="utf-8")
        json.loads(check[len("window.RENDER_NOTES = "):].rstrip().rstrip(";"))
        os.replace(tmp, OUTPUT)
    except (OSError, ValueError) as exc:
        print(f"BUILD FAILED: cannot write {OUTPUT.relative_to(ROOT)}: {exc}", file=sys.stderr)
        sys.exit(2)

    course = payload["course"]
    glossary = payload["glossary"]
    labs = payload["labs"]
    docs = payload["docs"]
    sections = payload["sections"]
    term_count = sum(len(group["terms"]) for group in glossary["groups"])
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"  {len(docs)} documents, {len(sections)} sections (publish boundary v2: default=deny)")
    print(f"  {len(glossary['groups'])} glossary groups, {term_count} terms")
    print(f"  {len(course['units'])} course units, {len(course['lessons'])} lessons")
    print(f"  {len(labs['labs'])} interactive labs")
    print(f"  {count_term_cards(docs)} chapter term cards generated")
    print(f"  {OUTPUT.stat().st_size / 1024:.0f} KB")


def count_term_cards(docs: list[dict]) -> int:
    return sum(len(d.get("terms") or []) for d in docs)


if __name__ == "__main__":
    main()
