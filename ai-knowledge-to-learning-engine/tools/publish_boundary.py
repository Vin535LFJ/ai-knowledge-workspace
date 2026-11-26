#!/usr/bin/env python3
"""强制发布边界 v2（2026-11-24，用户批准的学习站发布政策）。

唯一判定来源：tools/publish-allowlist.json（version 2，policy=enforce，default=deny）。
build_site.py（离线站）/ build_vitepress_content.py（在线镜像）/ validate_site.py（门禁）
全部通过本模块判定，不再各自维护文件排除表。

规则（不可被调用方绕过）：
- 资产必须逐个登记；未登记 = 拒绝（default=deny），没有目录通配授权。
- excluded-internal 优先于一切允许规则：无论父目录是否被允许，都不能发布。
- 注册表缺失 / JSON 损坏 / Schema 错误 / 未知 policy / 通配符 / 重复或大小写冲突
  路径 → RegistryError（fail closed）。不存在 advisory 回退。
- 路径必须是仓库根内的规范化相对 POSIX 路径：拒绝绝对路径、`..`、反斜杠、NUL、
  符号链接逃逸。

目标类型（target）——同一注册表，不同发布规则：
- "offline"：离线学习站（web/content.js）。public + offline-read-only（archive，D10.4 只读）。
- "online" ：VitePress 在线镜像。仅 public；archive 的 online=forbidden。
"""

from __future__ import annotations

import json
import posixpath
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST_PATH = ROOT / "tools" / "publish-allowlist.json"

REGISTRY_VERSION = 2
REQUIRED_POLICY = "enforce"
REQUIRED_DEFAULT = "deny"
# 资产策略 → (进离线站文档集, 进在线站文档集)
DOC_TARGETS = {
    "public": ("offline", "online"),
    "offline-read-only": ("offline",),
    "curated-data": (),
    "site-data": (),
    "excluded-internal": (),
}
TARGETS = ("offline", "online")

# 非资产空间：工具/构建产物/智能体与客户端适配/治理审核材料。这里面的文件**不是发布候选**
# （永不进入任何 target），也不因未登记而触发失败。发布政策明令禁止的 .agent/ reviews/
# .governance/ 都在此列——它们里面的新文件再多也不可能进入 bundle。
NON_ASSET_PARTS = frozenset({
    ".git",
    "web",
    "site-vitepress",
    "node_modules",
    "__pycache__",
    ".agent",              # D14：统一智能体文档仓库
    ".workbuddy-ai",
    ".zcode",              # D12/A3
    ".gemini",             # D15：客户端适配目录
    ".cursor",             # D15
    ".github",             # D15
    ".governance",         # 2026-11-24：治理产物
    "reviews",             # 2019-11-19：治理/审核材料，不进学习站
    ".qoder-input-images", # 工具输入缓存
})
NON_ASSET_FILES = frozenset({"CLAUDE.md", "AGENTS.md"})  # D15：根适配入口是指针
# 资产扫描空间内参与扫描的扩展名：.md 全量（除非资产空间），.json 仅以下顶层目录
# （注册表 scan.json；其余 JSON 是工具/模式/运行态，由 build 显式加载的站点数据另行强制校验）。
ASSET_JSON_ROOTS = frozenset({"evidence", "knowledge-model"})
# 发布资产扫描范围内的文件扩展名。
ASSET_SUFFIXES = (".md", ".json")


class RegistryError(Exception):
    """注册表缺失/损坏/不合规，或路径非法。调用方必须视为构建失败（fail closed）。"""


def normalize_rel(rel: str) -> str:
    """规范化仓库内相对 POSIX 路径；越界/绝对/通配/非规范形式一律拒绝。

    只接受规范形式（无 `.`/`..`/空段/重复分隔符）：注册表与磁盘扫描产出的路径都是
    规范的，任何需要"规范化后才知道指向哪"的输入都按不可信处理。
    """
    if not isinstance(rel, str) or not rel or "\x00" in rel:
        raise RegistryError(f"illegal asset path: {rel!r}")
    if "\\" in rel:
        raise RegistryError(f"asset path must use '/' separators: {rel!r}")
    if rel.startswith("/") or PurePosixPath(rel).is_absolute() or (len(rel) > 1 and rel[1] == ":"):
        raise RegistryError(f"absolute asset path not allowed: {rel!r}")
    if any(ch in rel for ch in "*?["):
        raise RegistryError(f"wildcard not allowed in asset path: {rel!r}")
    parts = rel.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise RegistryError(f"non-canonical or escaping asset path: {rel!r}")
    return posixpath.normpath(rel)


def _validate_registry(data: object, source: Path) -> dict:
    if not isinstance(data, dict):
        raise RegistryError(f"{source.name}: top-level must be an object")
    if data.get("version") != REGISTRY_VERSION:
        raise RegistryError(f"{source.name}: version {data.get('version')!r} != {REGISTRY_VERSION}")
    if data.get("policy") != REQUIRED_POLICY:
        raise RegistryError(f"{source.name}: policy {data.get('policy')!r} is not {REQUIRED_POLICY!r} (advisory 模式已废除，不回退)")
    if data.get("default") != REQUIRED_DEFAULT:
        raise RegistryError(f"{source.name}: default {data.get('default')!r} != {REQUIRED_DEFAULT!r}")
    policies = data.get("policies")
    assets = data.get("assets")
    if not isinstance(policies, dict) or not isinstance(assets, list) or not assets:
        raise RegistryError(f"{source.name}: 'policies' object and non-empty 'assets' list required")
    if set(policies) != set(DOC_TARGETS):
        raise RegistryError(f"{source.name}: policies {sorted(policies)} != expected {sorted(DOC_TARGETS)}")
    if policies.get("offline-read-only", {}).get("online") != "forbidden":
        raise RegistryError(f"{source.name}: offline-read-only.online must stay 'forbidden' (D10.4：archive 不自动扩大为在线发布)")
    by_path: dict[str, dict] = {}
    folded: dict[str, str] = {}
    for asset in assets:
        if not isinstance(asset, dict) or "path" not in asset or "policy" not in asset:
            raise RegistryError(f"{source.name}: every asset needs 'path' and 'policy': {asset!r}")
        path = normalize_rel(asset["path"])
        policy = asset["policy"]
        if policy not in DOC_TARGETS:
            raise RegistryError(f"{source.name}: {path}: unknown policy {policy!r}")
        if path in by_path:
            raise RegistryError(f"{source.name}: duplicate asset path: {path}")
        if path.casefold() in folded:
            raise RegistryError(f"{source.name}: case-insensitive path conflict: {path} vs {folded[path.casefold()]}")
        if policy == "excluded-internal" and not str(asset.get("reason", "")).strip():
            raise RegistryError(f"{source.name}: excluded-internal asset needs a non-empty reason: {path}")
        if policy == "offline-read-only" and path.split("/", 1)[0] != "archive":
            raise RegistryError(f"{source.name}: offline-read-only is reserved for archive/ (D10.4): {path}")
        by_path[path] = asset
        folded[path.casefold()] = path
    data["_by_path"] = by_path
    return data


def load_registry(path: Path | None = None) -> dict:
    """加载并校验注册表。任何问题都抛 RegistryError（fail closed）。"""
    source = path or ALLOWLIST_PATH
    if not source.exists():
        raise RegistryError(f"publish registry missing: {source} (未登记资产无法判定，构建必须失败)")
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RegistryError(f"publish registry unreadable: {source}: {exc}") from exc
    return _validate_registry(data, source)


def policy_for(rel: str, registry: dict) -> str | None:
    """返回资产策略；未登记返回 None。excluded-internal 原样返回（调用方必须视为拒绝）。"""
    path = normalize_rel(rel)
    asset = registry["_by_path"].get(path)
    return asset["policy"] if asset else None


def allows_target(policy: str | None, target: str) -> bool:
    if target not in TARGETS:
        raise RegistryError(f"unknown publish target {target!r}")
    if policy is None or policy == "excluded-internal":
        return False  # 默认拒绝；excluded-internal 优先于任何允许规则
    return target in DOC_TARGETS[policy]


def is_publishable(rel_posix: str, *, target: str = "offline", registry: dict | None = None) -> bool:
    """v2 判定：资产已登记且策略允许进入 target 的文档集合。未登记 = False。"""
    reg = registry if registry is not None else load_registry()
    return allows_target(policy_for(rel_posix, reg), target)


def require_publishable(rel_posix: str, *, target: str, registry: dict) -> str:
    """强制版：未登记/被排除/目标不允许 → RegistryError。返回命中的策略。"""
    policy = policy_for(rel_posix, registry)
    if policy is None:
        raise RegistryError(f"unregistered asset cannot be published ({target}): {rel_posix} — 请先在 tools/publish-allowlist.json 逐个登记")
    if not allows_target(policy, target):
        raise RegistryError(f"asset policy {policy!r} does not allow {target}: {rel_posix}")
    return policy


def require_site_data(rel_posix: str, *, registry: dict) -> str:
    """强制版（嵌入 payload 的数据文件）：必须是已登记的 site-data / curated-data。

    excluded-internal（如 claim-ledger.json）与未登记文件一律拒绝——它们永远不能
    作为数据被嵌入 bundle，即便调用方"顺手"读进来。
    """
    policy = policy_for(rel_posix, registry)
    if policy not in ("site-data", "curated-data"):
        raise RegistryError(f"asset is not registered embeddable data (site-data/curated-data): {rel_posix} (policy={policy!r})")
    return policy


def safe_relpath(path: Path, root: Path | None = None) -> str:
    """磁盘路径 → 仓库内相对 POSIX 路径；解析后越出根目录（符号链接逃逸）即拒绝。"""
    base = (root or ROOT).resolve()
    resolved = path.resolve()
    try:
        rel = resolved.relative_to(base)
    except ValueError as exc:
        raise RegistryError(f"path escapes repository root (symlink?): {path}") from exc
    return normalize_rel(rel.as_posix())


def scan_assets(root: Path | None = None) -> list[str]:
    """枚举发布资产扫描空间内的全部 .md/.json（规范化相对路径，已排序）。

    .md：全仓，除非 asset 空间（NON_ASSET_PARTS/FILES）。.json：仅 evidence/ 与
    knowledge-model/（资产级精选登记的空间）。courses/ docs/ archive/ 08-*/ 等都在
    扫描空间内——新文件必须被显式登记（public / offline-read-only / excluded-internal），
    否则 build/validate 双双 FAIL。符号链接在此处直接抛错。
    """
    base = root or ROOT
    found: list[str] = []
    for path in base.rglob("*"):
        rel = path.relative_to(base)
        parts = rel.parts
        if any(part in NON_ASSET_PARTS for part in parts[:-1]):
            continue
        if path.is_dir() or path.suffix not in ASSET_SUFFIXES:
            continue
        if path.name in NON_ASSET_FILES:
            continue
        if path.suffix == ".json" and parts[0] not in ASSET_JSON_ROOTS:
            continue
        if path.is_symlink():
            raise RegistryError(f"symlink in asset scan space not allowed: {path}")
        found.append(safe_relpath(path, base))
    return sorted(found)


def audit_registry(registry: dict, root: Path | None = None) -> dict:
    """注册表 ↔ 磁盘 一致性审计（只读）。

    返回 {ok, errors, counts, unregistered, stale, archive_total}。
    - unregistered：扫描空间内存在但未登记的资产（默认拒绝，必须登记后才能发布）。
    - stale：已登记但磁盘不存在的资产。
    """
    base = root or ROOT
    errors: list[str] = []
    unregistered: list[str] = []
    stale: list[str] = []
    try:
        on_disk = set(scan_assets(base))
    except RegistryError as exc:
        return {"ok": False, "errors": [str(exc)], "unregistered": [], "stale": [], "counts": {}, "archive_total": 0}
    registered = set(registry["_by_path"])
    for rel in sorted(on_disk - registered):
        unregistered.append(rel)
    for rel in sorted(registered - on_disk):
        # site-data / curated-data 由 build 显式加载，不在 .md/.json 扫描空间内；
        # 只要磁盘上存在即为有效登记，否则为失效登记。
        if not (base / rel).is_file():
            stale.append(rel)
            errors.append(f"registered but missing on disk: {rel}")
    archive = [p for p, a in registry["_by_path"].items() if a["policy"] == "offline-read-only"]
    disk_archive = {p for p in on_disk if p.startswith("archive/")}
    if set(archive) != disk_archive:
        errors.append(f"archive mismatch: unregistered={[p for p in sorted(disk_archive - set(archive))]} stale={[p for p in sorted(set(archive) - disk_archive)]}")
    counts: dict[str, int] = {}
    for asset in registry["_by_path"].values():
        counts[asset["policy"]] = counts.get(asset["policy"], 0) + 1
    # 未登记资产同样使审计失败（默认拒绝 + 不得静默跳过）：调用方必须显式登记后才能构建。
    if unregistered:
        errors.insert(0, f"{len(unregistered)} asset(s) in publish scan space are not registered (default=deny)")
    return {
        "ok": not errors,
        "errors": errors,
        "unregistered": unregistered,
        "stale": stale,
        "counts": counts,
        "archive_total": len(archive),
    }
