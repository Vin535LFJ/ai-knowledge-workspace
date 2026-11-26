#!/usr/bin/env python3
"""Validate AI Knowledge-to-Learning Engine source data, links, anchors, terms and generated site bundle.

Run after every `python tools/build_site.py`. Stdlib only.

Checks (FAIL blocks the build, WARN is informational):
  1. relative .md links in every doc resolve to an existing file
  2. #anchors resolve to a real heading in the target doc (app.js slugify port)
  3. course integrity: reading docs, prerequisites, terms, next pointers
  4. lab integrity: docs, lesson binding, terms, known renderer type
  5. glossary integrity: unique names / aliases, all terms parseable
  6. LaTeX balance: $$...$$ and $...$ delimiters are even / not nested
  7. generated web/content.js exists and starts with the expected assignment
  8. evidence layer: unique claim ids, resolvable sources, valid enums, lesson refs
  9. knowledge model: unique concept ids, resolvable glossary terms/anchors/relations
  10. pilot courses: lesson frontmatter, source anchors, quizzes, claim back-refs
  11. coverage: orphan assertions, quiz/checkpoint/claim alignment, feedback refs
  12. document-registry: .agent/indexes/document-registry.json matches disk frontmatter
       (read-only; FAIL means rebuild via `py -3 tools/build_document_registry.py`)
  13. publish boundary v2: tools/publish-allowlist.json (enforce, default=deny) is the single
       source of truth — registry/disk audit, bundle docs == registry-allowed set, internal
       files never in the bundle, online (VitePress) tree only contains online-allowed docs

Exit code is non-zero when any FAIL is present.
"""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
import sys
import unicodedata
from pathlib import Path

import build_document_registry as doc_registry
import publish_boundary as publish_boundary

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = ROOT / "tools" / "glossary.json"
COURSE_PATH = ROOT / "tools" / "course.json"
LABS_PATH = ROOT / "tools" / "labs.json"
GRAPH_PATH = ROOT / "tools" / "graph.json"
CONTENT_PATH = ROOT / "web" / "content.js"
VITEPRESS_DOCS = ROOT / "site-vitepress" / "docs"

# Lab types that web/assets/app.js knows how to render.
KNOWN_LAB_TYPES = {"mvp", "lathe", "pbr", "yuv", "timeline", "pipeline", "dag"}

fails: list[str] = []
warns: list[str] = []
passes = 0


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def ok() -> None:
    global passes
    passes += 1


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# 0. publish registry (single source of truth; shared with build_site.py)
# ---------------------------------------------------------------------------
def load_publish_registry() -> dict | None:
    """fail closed：注册表缺失/损坏/不合规 → FAIL，后续依赖它的检查全部跳过（不回退旧口径）。"""
    try:
        return publish_boundary.load_registry()
    except publish_boundary.RegistryError as exc:
        fail(f"[publish] registry fail-closed: {exc}")
        return None


def scan_publish_assets() -> list[str]:
    try:
        return publish_boundary.scan_assets(ROOT)
    except publish_boundary.RegistryError as exc:
        fail(f"[publish] asset scan aborted: {exc}")
        return []


PUBLISH_REGISTRY = load_publish_registry()
PUBLISH_ASSETS = scan_publish_assets() if PUBLISH_REGISTRY is not None else []


def markdown_files() -> list[Path]:
    """链接/锚点校验用的源文档集。

    2026-11-24：不再独立维护排除表——候选集来自 publish_boundary.scan_assets()（与
    build_site 同一口径）。archive（offline-read-only）是只读历史材料，不参与现行链接
    校验（保持既有行为）；excluded-internal 的内部文档仍做链接完整性检查（那是源质量
    检查，与是否发布无关）。注册表不可用时返回空集，由第 13 节 FAIL。
    """
    if PUBLISH_REGISTRY is None:
        return []
    return sorted(
        ROOT / rel
        for rel in PUBLISH_ASSETS
        if rel.endswith(".md")
        and publish_boundary.policy_for(rel, PUBLISH_REGISTRY) != "offline-read-only"
    )


def slugify(text: str) -> str:
    """Port of app.js slugify() so anchor checks match the browser exactly."""
    text = re.sub(r"<[^>]*>", "", text)
    text = text.strip().lower()
    # JS \p{L}\p{N} == unicode letters/numbers; keep letters, digits, spaces, hyphen.
    text = "".join(
        ch if (ch.isalnum() or ch.isspace() or ch == "-") else "" for ch in text
    )
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def headings(markdown: str) -> set[str]:
    out: set[str] = set()
    for line in markdown.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            out.add(slugify(m.group(2)))
    return out


# ---------------------------------------------------------------------------
# 1 & 2. doc links and anchors
# ---------------------------------------------------------------------------
doc_text: dict[str, str] = {}
doc_headings: dict[str, set[str]] = {}
for path in markdown_files():
    doc_id = relpath(path)
    text = path.read_text(encoding="utf-8")
    doc_text[doc_id] = text
    doc_headings[doc_id] = headings(text)

LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

for doc_id, text in doc_text.items():
    for m in LINK_RE.finditer(text):
        href = m.group(1).strip()
        # Skip app routes, external URLs, mailto, anchors-only.
        if href.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        if href.startswith("#/"):
            continue
        # Strip the anchor part for file resolution.
        target, sep, anchor = href.partition("#")
        if not target:
            continue
        decoded = target.replace("%20", " ")
        # Only validate relative markdown / file links, not tool asset links.
        if decoded.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico")):
            continue
        base_dir = posixpath.dirname(doc_id)
        resolved = posixpath.normpath(posixpath.join(base_dir, decoded))
        target_path = ROOT / resolved
        if not target_path.exists():
            # Some links intentionally point at GitHub blob URLs via rewrite; those are http(s) above.
            fail(f"[link] {doc_id}: missing target -> {href}")
            continue
        # Anchor check only for markdown targets we have parsed.
        if sep and anchor and resolved in doc_headings:
            if anchor not in doc_headings[resolved]:
                fail(f"[anchor] {doc_id}: #{anchor} not found in {resolved}")

if doc_text:
    ok()

# ---------------------------------------------------------------------------
# 3, 4, 5. JSON data integrity
# ---------------------------------------------------------------------------
def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"[json] {relpath(path)}: cannot parse: {exc}")
        return None


glossary = load_json(GLOSSARY_PATH)
course = load_json(COURSE_PATH)
labs = load_json(LABS_PATH)
graph = load_json(GRAPH_PATH) if GRAPH_PATH.exists() else None

term_names: set[str] = set()
term_aliases: set[str] = set()
if glossary is not None:
    for g in glossary.get("groups", []):
        for t in g.get("terms", []):
            name = t.get("name", "")
            if not name:
                fail("[glossary] term without name")
                continue
            if name in term_names:
                fail(f"[glossary] duplicate term name: {name}")
            term_names.add(name)
            for a in t.get("aliases", []) or []:
                term_aliases.add(a)


def term_resolves(name: str) -> bool:
    return name in term_names or name in term_aliases


if course is not None:
    lesson_ids = {l.get("id") for l in course.get("lessons", [])}
    unit_ids = {u.get("id") for u in course.get("units", [])}
    for l in course.get("lessons", []):
        lid = l.get("id", "<unknown>")
        if l.get("unit") not in unit_ids:
            fail(f"[course] {lid}: unknown unit {l.get('unit')!r}")
        for pre in l.get("prerequisites", []) or []:
            if pre not in lesson_ids:
                fail(f"[course] {lid}: unknown prerequisite {pre}")
        nxt = l.get("next")
        if nxt is not None and nxt not in lesson_ids:
            fail(f"[course] {lid}: unknown next {nxt}")
        for r in l.get("reading", []) or []:
            d = r.get("doc", "")
            if d and d not in doc_text:
                fail(f"[course] {lid}: reading doc missing -> {d}")
            elif d and r.get("anchor") and r["anchor"] not in doc_headings.get(d, set()):
                fail(f"[course] {lid}: reading anchor #{r['anchor']} missing in {d}")
        for t in l.get("terms", []) or []:
            if not term_resolves(t):
                fail(f"[course] {lid}: unresolved term {t!r}")

if labs is not None:
    lesson_ids = {l.get("id") for l in (course or {}).get("lessons", [])}
    for lab in labs.get("labs", []):
        lid = lab.get("id", "<unknown>")
        for d in lab.get("docs", []) or []:
            if d not in doc_text:
                fail(f"[lab] {lid}: doc missing -> {d}")
        lesson = lab.get("lesson")
        if not lesson:
            warn(f"[lab] {lid}: no lesson binding (orphan lab)")
        elif lesson not in lesson_ids:
            fail(f"[lab] {lid}: unknown lesson {lesson}")
        for t in lab.get("terms", []) or []:
            if not term_resolves(t):
                fail(f"[lab] {lid}: unresolved term {t!r}")
        if lab.get("type") not in KNOWN_LAB_TYPES:
            fail(f"[lab] {lid}: no renderer for type {lab.get('type')!r}")
        if "selfTest" not in lab:
            warn(f"[lab] {lid}: no selfTest field")

if graph is not None:
    node_ids = {n.get("id") for n in graph.get("nodes", [])}
    for n in graph.get("nodes", []):
        route = n.get("route", "")
        if not route.startswith("#/"):
            fail(f"[graph] node {n.get('id')}: bad route {route!r}")
    for e in graph.get("edges", []):
        if e.get("from") not in node_ids or e.get("to") not in node_ids:
            fail(f"[graph] edge references unknown node: {e}")

# ---------------------------------------------------------------------------
# 6. LaTeX delimiter balance
# ---------------------------------------------------------------------------
for doc_id, text in doc_text.items():
    if text.count("$$") % 2 != 0:
        fail(f"[latex] {doc_id}: odd number of $$ delimiters")
    # Strip $$ blocks before counting single $ to avoid double-count.
    without_display = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    if without_display.count("$") % 2 != 0:
        fail(f"[latex] {doc_id}: odd number of $ delimiters outside $$ blocks")

# ---------------------------------------------------------------------------
# 7. generated bundle
# ---------------------------------------------------------------------------
if CONTENT_PATH.exists():
    head = CONTENT_PATH.read_text(encoding="utf-8")[:200]
    if not head.startswith("window.RENDER_NOTES = "):
        fail("[bundle] web/content.js does not start with window.RENDER_NOTES")
    else:
        ok()
else:
    fail("[bundle] web/content.js missing — run python tools/build_site.py")

# ---------------------------------------------------------------------------
# 8. evidence layer (claim ledger + source registry)
# ---------------------------------------------------------------------------
EVIDENCE_DIR = ROOT / "evidence"
LEDGER_PATH = EVIDENCE_DIR / "claim-ledger.json"
SOURCE_PATH = EVIDENCE_DIR / "source-registry.json"


def all_lesson_ids() -> set:
    """主课程 + courses/*/course.json 的全部课时 id。

    2026-11-25：independent 课程（多课程扩展）拥有自有 id 命名空间，断言的 used_by_lessons
    可以指向它们；只认主课程会让独立课程无法挂接任何断言。
    """
    ids = {l.get("id") for l in (course or {}).get("lessons", [])}
    for cj in sorted((ROOT / "courses").glob("*/course.json")):
        pc = load_json(cj)
        if pc:
            ids |= {l.get("id") for l in pc.get("lessons", [])}
    return ids


lesson_ids = all_lesson_ids()
claim_ids: set[str] = set()

if LEDGER_PATH.exists() and SOURCE_PATH.exists():
    ledger = load_json(LEDGER_PATH) or {}
    registry = load_json(SOURCE_PATH) or {}
    claims = ledger.get("claims", [])
    sources = registry.get("sources", [])
    source_ids = {s.get("id") for s in sources}
    claim_ids = {c.get("id") for c in claims}
    if len(claim_ids) != len(claims):
        fail("[evidence] duplicate claim id in claim-ledger.json")
    for c in claims:
        cid = c.get("id", "<unknown>")
        v = c.get("verification", {}) or {}
        if c.get("claim_type") not in {"verified_fact", "engineering_fact", "conditional", "contested"}:
            fail(f"[evidence] {cid}: bad claim_type {c.get('claim_type')!r}")
        if v.get("status") not in {"verified", "conditional", "open"}:
            fail(f"[evidence] {cid}: bad verification.status {v.get('status')!r}")
        if v.get("confidence") not in {"high", "medium", "low"}:
            fail(f"[evidence] {cid}: bad verification.confidence {v.get('confidence')!r}")
        for e in c.get("evidence", []) or []:
            sid = e.get("source_id")
            if sid not in source_ids:
                fail(f"[evidence] {cid}: unknown source_id {sid!r}")
            elif cid not in next(s for s in sources if s.get("id") == sid).get("used_by_claims", []):
                fail(f"[evidence] {cid}: source {sid} reverse index missing")
        for d in c.get("source_documents", []) or []:
            if not (ROOT / d).exists():
                fail(f"[evidence] {cid}: source_document missing -> {d}")
        for lid in c.get("used_by_lessons", []) or []:
            if lid not in lesson_ids:
                fail(f"[evidence] {cid}: unknown lesson {lid}")
    for s in sources:
        sid = s.get("id", "<unknown>")
        if s.get("type") not in {"official_doc", "spec", "paper", "book", "repo_doc", "derivation"}:
            fail(f"[evidence] source {sid}: bad type {s.get('type')!r}")
        for cid in s.get("used_by_claims", []) or []:
            if cid not in claim_ids:
                fail(f"[evidence] source {sid}: unknown claim {cid}")
    if claims and sources:
        ok()
elif LEDGER_PATH.exists() != SOURCE_PATH.exists():
    fail("[evidence] claim-ledger.json and source-registry.json must exist together")

# ---------------------------------------------------------------------------
# 9. knowledge model (concepts + taxonomy)
# ---------------------------------------------------------------------------
MODEL_DIR = ROOT / "knowledge-model"
CONCEPTS_PATH = MODEL_DIR / "concepts.json"
if CONCEPTS_PATH.exists():
    model = load_json(CONCEPTS_PATH) or {}
    concepts = model.get("concepts", [])
    concept_ids = {c.get("id") for c in concepts}
    if len(concept_ids) != len(concepts):
        fail("[knowledge-model] duplicate concept id")
    for c in concepts:
        cid = c.get("id", "<unknown>")
        if c.get("layer") not in {f"L{i}" for i in range(8)}:
            fail(f"[knowledge-model] {cid}: bad layer {c.get('layer')!r}")
        term = c.get("glossary_term", "")
        if not term_resolves(term):
            fail(f"[knowledge-model] {cid}: unresolved glossary_term {term!r}")
        ref = c.get("definition_ref", "")
        if ref:
            ref_file, sep, ref_anchor = ref.partition("#")
            if not (ROOT / ref_file).exists():
                fail(f"[knowledge-model] {cid}: definition_ref missing -> {ref_file}")
            elif sep and ref_anchor and ref_anchor not in doc_headings.get(ref_file, set()):
                fail(f"[knowledge-model] {cid}: definition anchor #{ref_anchor} missing in {ref_file}")
        rels = c.get("relations", []) or []
        if not rels:
            fail(f"[knowledge-model] {cid}: isolated concept (no relations)")
        for r in rels:
            if r.get("type") not in {"prerequisite_of", "contrast_with", "used_by", "part_of"}:
                fail(f"[knowledge-model] {cid}: bad relation type {r.get('type')!r}")
            if r.get("target") not in concept_ids:
                fail(f"[knowledge-model] {cid}: unknown relation target {r.get('target')!r}")
            sc = r.get("source_claim")
            if sc and claim_ids and sc not in claim_ids:
                fail(f"[knowledge-model] {cid}: unknown source_claim {sc!r}")
    if concepts:
        ok()

# ---------------------------------------------------------------------------
# 10. pilot courses (courses/*/course.json + lesson frontmatter + quizzes)
# ---------------------------------------------------------------------------
COURSES_DIR = ROOT / "courses"


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser for the lesson schema (stdlib only)."""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm: dict = {}
    current_key: str | None = None
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            existing = fm.get(current_key)
            if isinstance(existing, list):
                existing.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        current_key = key
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fm[key] = [v.strip().strip('"').strip("'") for v in inner.split(",")] if inner else []
        elif value == "":
            fm[key] = []
        else:
            fm[key] = value.strip('"').strip("'")
    return fm


REQUIRED_FRONTMATTER = ["id", "course", "title", "prerequisites", "objectives", "source_documents", "claims", "status"]

if COURSES_DIR.exists():
    main_lesson_ids = {l.get("id") for l in (course or {}).get("lessons", [])}
    for course_dir in sorted(p for p in COURSES_DIR.iterdir() if p.is_dir()):
        pc_path = course_dir / "course.json"
        if not pc_path.exists():
            continue
        pc = load_json(pc_path)
        if pc is None:
            continue
        cname = pc.get("id", course_dir.name)
        # 2026-11-24 多课程最小扩展（用户批准）：声明 independent: true 的课程
        # 拥有自有 id 命名空间，跳过"派生自主课程"检查；id 唯一性/前置/unit/
        # frontmatter/quiz 仍在本课程内全量校验。
        independent = bool(pc.get("independent"))
        unit_ids = {u.get("id") for u in pc.get("units", [])}
        seen_lessons: set[str] = set()
        pilot_lesson_ids: set[str] = set()
        for l in pc.get("lessons", []):
            lid = l.get("id", "<unknown>")
            if lid in seen_lessons:
                fail(f"[pilot] {cname}/{lid}: duplicate lesson id in course.json")
            seen_lessons.add(lid)
            pilot_lesson_ids.add(lid)
            if not independent and lid not in main_lesson_ids:
                fail(f"[pilot] {cname}/{lid}: lesson id not derived from tools/course.json")
            if l.get("unit") not in unit_ids:
                fail(f"[pilot] {cname}/{lid}: unknown unit {l.get('unit')!r}")
            for pre in l.get("prerequisites", []) or []:
                if pre not in pilot_lesson_ids and pre not in main_lesson_ids:
                    fail(f"[pilot] {cname}/{lid}: unknown prerequisite {pre}")
            lesson_file = course_dir / "lessons" / str(l.get("lessonFile", ""))
            if not l.get("lessonFile"):
                fail(f"[pilot] {cname}/{lid}: no lessonFile")
            elif not lesson_file.exists():
                fail(f"[pilot] {cname}/{lid}: lesson file missing -> lessons/{l['lessonFile']}")
            else:
                fm = parse_frontmatter(lesson_file.read_text(encoding="utf-8"))
                for field in REQUIRED_FRONTMATTER:
                    if field == "prerequisites":
                        # 2026-11-25：独立课程的开篇课合法地没有前置课。prerequisites 以
                        # course.json 的声明为准，要求 frontmatter 与之逐项一致
                        #（比"一律非空"更严：其余各课两边必须对得上，声明为空才允许为空）。
                        declared = sorted(str(p) for p in (l.get("prerequisites") or []))
                        got = sorted(str(p) for p in (fm.get("prerequisites") or []))
                        if got != declared:
                            fail(f"[pilot] {cname}/{lid}: frontmatter prerequisites {got} != course.json {declared}")
                        continue
                    if field not in fm or fm[field] in ("", [], None):
                        fail(f"[pilot] {cname}/{lid}: frontmatter missing {field}")
                if fm.get("id") != lid:
                    fail(f"[pilot] {cname}/{lid}: frontmatter id {fm.get('id')!r} != course id {lid!r}")
                if fm.get("course") != cname:
                    fail(f"[pilot] {cname}/{lid}: frontmatter course {fm.get('course')!r} != {cname!r}")
                if fm.get("status") not in {"draft", "reviewed", "final"}:
                    fail(f"[pilot] {cname}/{lid}: bad status {fm.get('status')!r}")
                for sd in fm.get("source_documents", []) or []:
                    sfile, ssep, sanchor = str(sd).partition("#")
                    if not (ROOT / sfile).exists():
                        fail(f"[pilot] {cname}/{lid}: source_document missing -> {sfile}")
                    elif ssep and sanchor and sfile in doc_headings and sanchor not in doc_headings[sfile]:
                        fail(f"[pilot] {cname}/{lid}: source anchor #{sanchor} missing in {sfile}")
                for cl in fm.get("claims", []) or []:
                    if cl not in claim_ids:
                        fail(f"[pilot] {cname}/{lid}: unknown claim {cl!r}")
                lab_id = fm.get("lab", "")
                known_lab_ids = {lb.get("id") for lb in (labs or {}).get("labs", [])}
                if lab_id and lab_id not in known_lab_ids:
                    warn(f"[pilot] {cname}/{lid}: lab {lab_id!r} not yet in tools/labs.json (P3 pending)")
        # quizzes
        quiz_ids: set[str] = set()
        for qpath in sorted((course_dir / "quizzes").glob("*.json")):
            quiz = load_json(qpath)
            if quiz is None:
                continue
            qlid = quiz.get("lesson", "<unknown>")
            if qlid not in pilot_lesson_ids:
                fail(f"[pilot] quiz {qpath.name}: unknown lesson {qlid!r}")
            if qpath.stem != qlid:
                fail(f"[pilot] quiz {qpath.name}: filename {qpath.stem} != lesson {qlid}")
            quiz_ids.add(qlid)
            for q in quiz.get("questions", []):
                qid = q.get("id", "<unknown>")
                if qid in quiz_ids:
                    fail(f"[pilot] quiz {qpath.name}: duplicate question id {qid}")
                quiz_ids.add(qid)
                if q.get("type") == "choice":
                    opts = q.get("options", []) or []
                    ans = q.get("answer")
                    if not isinstance(ans, int) or not (0 <= ans < len(opts)):
                        fail(f"[pilot] quiz {qpath.name}/{qid}: answer index out of range")
                elif not q.get("answer"):
                    fail(f"[pilot] quiz {qpath.name}/{qid}: empty answer")
                for cl in q.get("claim_ids", []) or []:
                    if cl not in claim_ids:
                        fail(f"[pilot] quiz {qpath.name}/{qid}: unknown claim {cl!r}")
        for lid in pilot_lesson_ids:
            if lid not in quiz_ids:
                fail(f"[pilot] {cname}/{lid}: no quiz file quizzes/{lid}.json")
    if pilot_lesson_ids:
        ok()


# ---------------------------------------------------------------------------
# 11. coverage + feedback (citation coverage, quiz/checkpoint/claim, feedback refs)
# ---------------------------------------------------------------------------
# Additive section: sections 1-10 above are untouched. Uses data already loaded
# (claim_ids, course, labs, doc_headings) plus read-only feedback.json.

# 11a. every claim has at least one evidence item (no orphan assertions).
#      source_documents existence is already checked in section 8; do not repeat.
for c in (ledger.get("claims", []) if LEDGER_PATH.exists() else []):
    cid = c.get("id", "<unknown>")
    if not (c.get("evidence") or []):
        fail(f"[coverage] {cid}: no evidence item (orphan assertion)")
    # An unattached open/conditional claim is expected (e.g. P03 "暂未纳入主线");
    # only a *verified* claim that no lesson uses is a real coverage gap worth warning.
    vstatus = (c.get("verification") or {}).get("status")
    if not (c.get("used_by_lessons") or []) and vstatus == "verified":
        warn(f"[coverage] {cid}: verified claim not attached to any lesson (used_by_lessons empty)")

# 11b. quiz <-> checkpoint <-> claim coverage for each pilot lesson.
def _norm_text(s) -> str:
    return re.sub(r"[\s\W_]+", "", str(s)).lower()

if COURSES_DIR.exists():
    for course_dir in sorted(p for p in COURSES_DIR.iterdir() if p.is_dir()):
        pc_path = course_dir / "course.json"
        if not pc_path.exists():
            continue
        pc_data = load_json(pc_path)
        if pc_data is None:
            continue
        cname = pc_data.get("id", course_dir.name)
        for l in pc_data.get("lessons", []):
            lid = l.get("id", "<unknown>")
            checkpoints = [_norm_text(cp) for cp in (l.get("checkpoint") or []) if _norm_text(cp)]
            qpath = course_dir / "quizzes" / f"{lid}.json"
            if not qpath.exists():
                continue  # already FAILed in section 10
            quiz = load_json(qpath)
            if quiz is None:
                continue
            questions = quiz.get("questions", []) or []
            prompts = [_norm_text(q.get("prompt", "")) for q in questions]
            # every checkpoint question should be backed by a quiz prompt
            for cp in checkpoints:
                if not any(cp in p or p in cp for p in prompts if p):
                    fail(f"[coverage] {cname}/{lid}: checkpoint not covered by any quiz prompt -> {cp[:40]}")
            # quiz claim_ids must be a subset of the lesson's declared claims
            lesson_file = course_dir / "lessons" / str(l.get("lessonFile", ""))
            lesson_claims: set[str] = set()
            if lesson_file.exists():
                lesson_claims = set(parse_frontmatter(lesson_file.read_text(encoding="utf-8")).get("claims", []) or [])
            for q in questions:
                qid = q.get("id", "<unknown>")
                for cl in q.get("claim_ids", []) or []:
                    if lesson_claims and cl not in lesson_claims:
                        fail(f"[coverage] {cname}/{lid}/{qid}: quiz claim {cl!r} not in lesson claims")
            if checkpoints and questions:
                ok()

# 11c. feedback.json (optional): schema + resolvable refs, never auto-mutate state.
FEEDBACK_PATH = ROOT / "tools" / "feedback.json"
if FEEDBACK_PATH.exists():
    fb = load_json(FEEDBACK_PATH)
    if fb is not None:
        # Collect all pilot quiz lesson ids read-only for ref resolution.
        pilot_quiz_ids: set[str] = set()
        if COURSES_DIR.exists():
            for cdir in COURSES_DIR.iterdir():
                if cdir.is_dir():
                    for qp in (cdir / "quizzes").glob("*.json"):
                        qd = load_json(qp)
                        if qd and qd.get("lesson"):
                            pilot_quiz_ids.add(qd["lesson"])
        entries = fb.get("entries", []) or []
        if "version" not in fb:
            warn("[feedback] feedback.json missing 'version'")
        valid_types = {"confusion", "gap", "rating"}
        for i, e in enumerate(entries):
            etype = e.get("type")
            if etype not in valid_types:
                fail(f"[feedback] entry {i}: bad type {etype!r}")
            fl = e.get("lesson")
            if fl and fl not in lesson_ids:
                fail(f"[feedback] entry {i}: unknown lesson {fl!r}")
            fq = e.get("quiz")
            if fq and fq not in pilot_quiz_ids:
                warn(f"[feedback] entry {i}: quiz {fq!r} not found in any pilot course")
            for cl in e.get("claim_ids", []) or []:
                if cl not in claim_ids:
                    fail(f"[feedback] entry {i}: unknown claim {cl!r}")
        ok()

# ---------------------------------------------------------------------------
# 12. document-registry <-> disk frontmatter consistency (P8 片三，2026-11-20)
# ---------------------------------------------------------------------------
# 只读比对：用生成器同一套 collect_entries() 重算磁盘真值，与注册表 documents 逐条
# 对比（meta.generated_at 是构建时间戳，不参与比对）。FAIL 的修复动作 = 重建注册表，
# 本节不写任何文件。注册表扫描范围（含 .agent/reviews/archive）与知识 bundle 不同，
# 属预期差异，由生成器 EXCLUDED_PARTS 单一口径决定。
DOC_REGISTRY_PATH = ROOT / ".agent" / "indexes" / "document-registry.json"
if DOC_REGISTRY_PATH.exists():
    reg = load_json(DOC_REGISTRY_PATH)
    if reg is not None:
        reg_fail_baseline = len(fails)
        expected = {e["path"]: e for e in doc_registry.collect_entries()}
        actual = {e.get("path"): e for e in reg.get("documents", [])}
        for path in sorted(set(expected) - set(actual)):
            fail(f"[registry] {path}: 磁盘存在但注册表缺失 — run py -3 tools/build_document_registry.py")
        for path in sorted(set(actual) - set(expected)):
            fail(f"[registry] {path}: 注册表残留但磁盘已不存在 — run py -3 tools/build_document_registry.py")
        for path in sorted(set(expected) & set(actual)):
            exp, act = expected[path], actual[path]
            for key in sorted(set(exp) | set(act)):
                if exp.get(key) != act.get(key):
                    fail(f"[registry] {path}: 字段 {key} 漂移 registry={act.get(key)!r} disk={exp.get(key)!r} — run py -3 tools/build_document_registry.py")
        total = (reg.get("meta") or {}).get("total")
        if total != len(expected):
            fail(f"[registry] meta.total={total} != 磁盘文档数 {len(expected)} — run py -3 tools/build_document_registry.py")
        if len(fails) == reg_fail_baseline:
            ok()
else:
    fail("[registry] .agent/indexes/document-registry.json missing — run py -3 tools/build_document_registry.py")

# ---------------------------------------------------------------------------
# 13. publish boundary v2 (2026-11-24, 用户批准)：注册表 = 唯一判定来源
# ---------------------------------------------------------------------------
# 与 build_site.py 共用 publish_boundary（同一注册表、同一 API），不再有第二套排除逻辑。
#   a. 注册表 ↔ 磁盘：未登记资产（默认拒绝）/ 失效登记 / archive 不一一对应 → FAIL
#   b. bundle docs == 注册表允许进入 offline 的文档集（多一篇 = 泄露，少一篇 = bundle 过期）
#   c. 内部文件永不进 bundle；每篇 publishPolicy 与注册表一致
#   d. publishManifest 可追溯：路径集、target、registryVersion、每篇源文件 SHA256
#   e. 嵌入的站点数据（glossary/course/labs/graph）必须是已登记 site-data
#   f. 在线镜像（site-vitepress/docs，若已生成）只含 online 允许的文档，且无 archive/
if PUBLISH_REGISTRY is not None:
    publish_base = len(fails)
    R = PUBLISH_REGISTRY

    # a. registry <-> disk
    audit = publish_boundary.audit_registry(R, ROOT)
    for msg in audit["errors"]:
        fail(f"[publish] {msg}")
    for rel in audit["unregistered"]:
        fail(f"[publish] unregistered asset (default=deny): {rel} — 在 tools/publish-allowlist.json 逐个登记，或移出资产空间")

    expected_docs = {
        rel: publish_boundary.policy_for(rel, R)
        for rel in PUBLISH_ASSETS
        if rel.endswith(".md") and publish_boundary.is_publishable(rel, target="offline", registry=R)
    }

    # b/c/d. bundle vs registry
    bundle: dict | None = None
    if CONTENT_PATH.exists():
        text = CONTENT_PATH.read_text(encoding="utf-8", errors="replace")
        head = "window.RENDER_NOTES = "
        if text.startswith(head):
            try:
                bundle = json.loads(text[len(head):].rstrip().rstrip(";"))
            except ValueError as exc:
                fail(f"[publish] web/content.js payload unparsable: {exc}")
    if bundle is None:
        fail("[publish] bundle unavailable — run py -3 tools/build_site.py")
    else:
        bundle_docs = {str(d.get("id")): d.get("publishPolicy") for d in bundle.get("docs", [])}
        for rel in sorted(set(bundle_docs) - set(expected_docs)):
            fail(f"[publish] bundle contains asset not allowed offline: {rel}")
        for rel in sorted(set(expected_docs) - set(bundle_docs)):
            fail(f"[publish] allowed doc missing from bundle (stale bundle): {rel} — run py -3 tools/build_site.py")
        for rel in sorted(set(bundle_docs) & set(expected_docs)):
            if bundle_docs[rel] != expected_docs[rel]:
                fail(f"[publish] {rel}: bundle policy {bundle_docs[rel]!r} != registry {expected_docs[rel]!r}")
        for rel, policy in R["_by_path"].items():
            if policy == "excluded-internal" and rel in bundle_docs:
                fail(f"[publish] excluded-internal asset leaked into bundle: {rel}")
        manifest = bundle.get("publishManifest")
        if not isinstance(manifest, dict):
            fail("[publish] bundle missing publishManifest (not traceable) — run py -3 tools/build_site.py")
        else:
            if manifest.get("target") != "offline":
                fail(f"[publish] manifest target {manifest.get('target')!r} != 'offline'")
            if manifest.get("registryVersion") != R.get("version"):
                fail(f"[publish] manifest registryVersion {manifest.get('registryVersion')!r} != registry {R.get('version')!r}")
            mf_docs = {str(m.get("path")): m.get("sha256") for m in manifest.get("docs", []) if isinstance(m, dict)}
            if set(mf_docs) != set(bundle_docs):
                fail(f"[publish] manifest paths != bundle docs (manifest-only={sorted(set(mf_docs) - set(bundle_docs))[:3]}, bundle-only={sorted(set(bundle_docs) - set(mf_docs))[:3]})")
            for rel in sorted(set(mf_docs) & set(bundle_docs)):
                src = ROOT / rel
                if not src.is_file():
                    fail(f"[publish] manifest source missing on disk: {rel}")
                elif hashlib.sha256(src.read_bytes()).hexdigest() != mf_docs[rel]:
                    fail(f"[publish] {rel}: source changed after build (sha256 mismatch) — run py -3 tools/build_site.py")

        # e. embedded site data must be registered site-data
        for key, rel in (("glossary", "tools/glossary.json"), ("course", "tools/course.json"), ("labs", "tools/labs.json"), ("graph", "tools/graph.json")):
            if key in bundle and publish_boundary.policy_for(rel, R) != "site-data":
                fail(f"[publish] embedded payload '{key}' comes from unregistered site-data: {rel}")
        courses_list = bundle.get("courses", [])
        if not courses_list or courses_list[0] != bundle.get("course"):
            fail("[publish] payload.courses[0] must be the main course (payload.course)")
        for c in courses_list[1:]:  # 其余为 courses/<id>/course.json（pilot / independent）
            cid = str(c.get("id", ""))
            rel = f"courses/{cid}/course.json"
            if not cid or publish_boundary.policy_for(rel, R) != "site-data":
                fail(f"[publish] embedded courses[] entry not registered site-data: {rel}")
        if "course" in bundle and publish_boundary.policy_for("tools/course.json", R) != "site-data":
            fail("[publish] embedded payload 'course' comes from unregistered site-data: tools/course.json")

        # e2. 精选数据（curated-data，2026-11-25）：嵌入集合必须恰等于注册表登记、哈希可追溯；
        #     文档级证据引用只能指向精选来源注册表（claim-ledger 等内部数据永远不在其中）。
        curated_registered = {rel for rel, asset in R["_by_path"].items() if asset["policy"] == "curated-data"}
        embedded = bundle.get("curated")
        if not isinstance(embedded, dict):
            fail("[publish] bundle missing payload.curated (精选证据/知识模型未呈现) — run py -3 tools/build_site.py")
        else:
            for rel in sorted(set(embedded) - curated_registered):
                fail(f"[publish] payload.curated contains asset not registered as curated-data: {rel}")
            for rel in sorted(curated_registered - set(embedded)):
                fail(f"[publish] curated-data asset missing from payload.curated: {rel}")
            mf_curated = (
                {str(m.get("path")): m.get("sha256") for m in (manifest.get("curated") or []) if isinstance(m, dict)}
                if isinstance(manifest, dict) else {}
            )
            for rel in sorted(curated_registered & set(embedded)):
                src = ROOT / rel
                if not src.is_file():
                    fail(f"[publish] curated-data source missing on disk: {rel}")
                elif hashlib.sha256(src.read_bytes()).hexdigest() != mf_curated.get(rel):
                    fail(f"[publish] curated-data {rel}: sha256 mismatch (stale bundle) — run py -3 tools/build_site.py")
            source_ids = {
                str(s.get("id"))
                for s in (embedded.get("evidence/source-registry.json") or {}).get("sources", []) if isinstance(s, dict)
            }
            for d in bundle.get("docs", []):
                for item in d.get("evidence") or []:
                    if not isinstance(item, dict) or str(item.get("id")) not in source_ids:
                        fail(f"[publish] {d.get('id')}: evidence cites a source outside the curated registry: {item}")

    # f. online mirror (VitePress) — archive forbidden online, only public docs
    if VITEPRESS_DOCS.exists():
        vp_files = sorted(p for p in VITEPRESS_DOCS.rglob("*.md") if p.name != "index.md")
        if (VITEPRESS_DOCS / "archive").exists():
            fail("[publish] online tree contains archive/ (D10.4: archive online=forbidden)")
        vp_bad = []
        for p in vp_files:
            rel = p.relative_to(VITEPRESS_DOCS).as_posix()
            if not publish_boundary.is_publishable(rel, target="online", registry=R):
                vp_bad.append(rel)
        for rel in vp_bad[:10]:
            fail(f"[publish] online tree contains non-online asset: {rel}")
        if len(vp_bad) > 10:
            fail(f"[publish] online tree: {len(vp_bad) - 10} more non-online assets")
        if vp_files and not vp_bad:
            ok()
    if len(fails) == publish_base:
        ok()

# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------
print(f"validate_site: {passes} checks passed, {len(warns)} warnings, {len(fails)} failures")
for w in warns:
    print(f"  WARN  {w}")
for f in fails:
    print(f"  FAIL  {f}")
if fails:
    sys.exit(1)
print("OK")
