#!/usr/bin/env python3
"""KCR 影响分析（只读）：计算 Source → Claim → Concept → Lesson → Quiz → Course → Website 影响链。

用法（本机用 py -3）：
    py -3 tools/kcr_impact.py --source-id SRC-RN-AV-BASE
    py -3 tools/kcr_impact.py --claim-id V14
    py -3 tools/kcr_impact.py --report reviews/CURRENT_AUDIT.md
    py -3 tools/kcr_impact.py --claim-draft "Stride 是物理行宽" --out reviews/kcr/impact-demo.json

硬边界（2026-11-19）：
- **只读**：不写任何源 JSON / 正文 / 断言状态，不升级 claim，不过门禁。
- 输出仅为审阅工件（默认 reviews/kcr/impact-report-<date>.json），供人工裁决使用。
- 历史不足或字段缺失时如实标注 unknown / 空，不伪造影响关系。

契约（2026-11-20，P8 片一对齐）：
- 输出符合 tools/kcr/schema/impact-report.schema.json（trigger/new_sources/affected/conflicts/uncovered）。
- affected 各数组元素为对象（id + relation/via_claim）；website 影响与结构完整性检查为非契约附加字段
  （website_artifacts / integrity_findings），不混入契约 conflicts（语义冲突属 Stage 2）。
- 自测：py -3 tools/kcr/selftest_impact.py（真实回放 V21–V24 / V14）。

契约校验（2026-11-20，P8 片二接入）：
- 写盘前经 tools/kcr/validate_kcr.py 程序化校验（stdlib-only）；校验失败不写文件，退出码 3。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from kcr import validate_kcr

ROOT = Path(__file__).resolve().parent.parent
CLAIM_LEDGER = ROOT / "evidence" / "claim-ledger.json"
SOURCE_REGISTRY = ROOT / "evidence" / "source-registry.json"
CONCEPTS = ROOT / "knowledge-model" / "concepts.json"
QUIZ_DIR = ROOT / "courses" / "video-rendering-journey" / "quizzes"
COURSE_PATHS = [ROOT / "tools" / "course.json", ROOT / "courses" / "video-rendering-journey" / "course.json"]
LESSON_DIR = ROOT / "courses" / "video-rendering-journey" / "lessons"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_graph() -> dict:
    """读取现有 JSON，构建双向索引。只读。"""
    ledger = _load(CLAIM_LEDGER)
    registry = _load(SOURCE_REGISTRY)
    concepts = _load(CONCEPTS)

    claims = {c["id"]: c for c in ledger.get("claims", [])}
    sources = {s["id"]: s for s in registry.get("sources", [])}

    # source -> claims
    source_to_claims: dict[str, list[str]] = {sid: [] for sid in sources}
    for cid, claim in claims.items():
        for ev in claim.get("evidence", []):
            sid = ev.get("source_id")
            if sid in source_to_claims and cid not in source_to_claims[sid]:
                source_to_claims[sid].append(cid)
        # 兼容 used_by_sources 字段（若存在）
        for sid in claim.get("used_by_sources", []) or []:
            if sid in source_to_claims and cid not in source_to_claims[sid]:
                source_to_claims[sid].append(cid)

    # claim -> concepts
    claim_to_concepts: dict[str, list[str]] = {cid: [] for cid in claims}
    for concept in concepts.get("concepts", []):
        for rel in concept.get("relations", []) or []:
            sc = rel.get("source_claim")
            if sc in claim_to_concepts:
                claim_to_concepts[sc].append(concept["id"])

    # claim -> lessons
    claim_to_lessons: dict[str, list[str]] = {cid: [] for cid in claims}
    for cid, claim in claims.items():
        for lid in claim.get("used_by_lessons", []) or []:
            if lid not in claim_to_lessons[cid]:
                claim_to_lessons[cid].append(lid)

    # lesson frontmatter claims（从正文 frontmatter 读取，覆盖/补充 ledger 声明）
    if LESSON_DIR.exists():
        for path in LESSON_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^claims:\s*\[([^\]]*)\]", text, re.M)
            lesson_id = path.name.split("-")[0]
            if m:
                for cid in re.findall(r"[A-Z]\d+", m.group(1)):
                    if cid in claim_to_lessons and lesson_id not in claim_to_lessons[cid]:
                        claim_to_lessons[cid].append(lesson_id)

    # claim -> quizzes / quiz -> lessons
    claim_to_quizzes: dict[str, list[str]] = {cid: [] for cid in claims}
    quiz_to_lesson: dict[str, str] = {}
    if QUIZ_DIR.exists():
        for path in QUIZ_DIR.glob("*.json"):
            quiz = _load(path)
            lesson = quiz.get("lesson", path.stem)
            quiz_to_lesson[path.stem] = lesson
            for q in quiz.get("questions", []):
                for cid in q.get("claim_ids", []) or []:
                    if cid in claim_to_quizzes:
                        key = f"{path.stem}#{q.get('id', '?')}"
                        claim_to_quizzes[cid].append(key)

    # lessons -> courses（两层 course.json 的 lesson id 集合）
    course_of_lesson: dict[str, list[str]] = {}
    for cp in COURSE_PATHS:
        if not cp.exists():
            continue
        data = _load(cp)
        for lesson in data.get("lessons", []) or []:
            lid = lesson.get("id")
            if lid:
                course_of_lesson.setdefault(lid, []).append(cp.relative_to(ROOT).as_posix())

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "counts": {
            "sources": len(sources), "claims": len(claims),
            "concepts": len(concepts.get("concepts", [])),
            "quizzes": len(quiz_to_lesson), "courses": len(COURSE_PATHS),
        },
        "sources": sources, "claims": claims,
        "source_to_claims": source_to_claims,
        "claim_to_concepts": claim_to_concepts,
        "claim_to_lessons": claim_to_lessons,
        "claim_to_quizzes": claim_to_quizzes,
        "quiz_to_lesson": quiz_to_lesson,
        "course_of_lesson": course_of_lesson,
    }


def analyze(g: dict, *, source_id: str | None = None, claim_id: str | None = None,
            trigger_type: str | None = None, trigger_ref: str | None = None) -> dict:
    """从 seed（source 或 claim）展开影响链。输出含契约 trigger/new_sources 段。"""
    seeds: list[str] = []
    if source_id:
        if source_id not in g["sources"]:
            return {"error": f"未知 source_id: {source_id}", "available": sorted(g["sources"])[:20]}
        seeds = g["source_to_claims"].get(source_id, [])
    elif claim_id:
        if claim_id not in g["claims"]:
            return {"error": f"未知 claim_id: {claim_id}", "available": sorted(g["claims"])}
        seeds = [claim_id]

    if trigger_type is None:
        trigger_type = "source_update" if source_id else "claim_status_request"
    if trigger_ref is None:
        trigger_ref = source_id or claim_id or "(no seed)"
    trigger = {"type": trigger_type, "ref": trigger_ref,
               "date": datetime.now().strftime("%Y-%m-%d")}

    claims = sorted(set(seeds))
    concept_via: dict[str, str] = {}
    lesson_via: dict[str, str] = {}
    quiz_via: dict[str, str] = {}
    courses: set[str] = set()
    integrity: list[dict] = []

    for cid in claims:
        for kid in g["claim_to_concepts"].get(cid, []):
            concept_via.setdefault(kid, cid)
        for lid in g["claim_to_lessons"].get(cid, []):
            lesson_via.setdefault(lid, cid)
        for qkey in g["claim_to_quizzes"].get(cid, []):
            quiz_via.setdefault(qkey, cid)
        claim = g["claims"][cid]
        status = (claim.get("verification") or {}).get("status", "unknown")
        if status != "verified":
            integrity.append({
                "type": "unverified_claim_in_chain", "claim": cid,
                "status": status, "note": "链中断言未 verified，升级/应用需人工裁决",
            })

    for lid in lesson_via:
        courses.update(g["course_of_lesson"].get(lid, []))

    # 缺口检测：quiz 挂接了链中 claim，但对应 lesson 未被 claim 的 used_by_lessons 声明
    for qkey in quiz_via:
        lesson = g["quiz_to_lesson"].get(qkey.split("#")[0])
        if lesson and lesson not in lesson_via:
            integrity.append({
                "type": "quiz_lesson_not_linked", "quiz": qkey,
                "lesson": lesson, "note": "quiz 引用链中断言，但该课未声明此断言",
            })

    relation_note = (
        "source→claim 支持链（seed=source）" if source_id else
        "claim 状态请求的主体断言（seed=claim）" if claim_id else
        "无 seed（草稿模式仅回显）"
    )
    uncovered = [
        f"{cid}: 无来源登记（evidence 缺 source_id）"
        for cid in claims
        if not any(ev.get("source_id") for ev in g["claims"][cid].get("evidence", []))
    ]
    return {
        "trigger": trigger,
        "new_sources": [],
        "seed": {"source_id": source_id, "claim_id": claim_id},
        "affected": {
            "claims": [{"id": cid, "relation": "supports", "note": relation_note} for cid in claims],
            "concepts": [{"id": kid, "via_claim": concept_via[kid]} for kid in sorted(concept_via)],
            "lessons": [{"id": lid, "via_claim": lesson_via[lid]} for lid in sorted(lesson_via)],
            "quizzes": [{"id": qkey, "via_claim": quiz_via[qkey]} for qkey in sorted(quiz_via)],
            "courses": [{"id": cpath, "objectives_maybe": False} for cpath in sorted(courses)],
        },
        # 契约 conflicts 专指"新草稿 vs 既有断言"的语义冲突（Stage 2 提案流程产出）；
        # 本工具只做结构完整性检查，结果放非契约字段 integrity_findings，不冒充语义冲突。
        "conflicts": [],
        "uncovered": uncovered,
        "integrity_findings": integrity,
        "website_artifacts": ["web/content.js (build 生成物)", "site-vitepress/docs/ (build 生成物)"]
        if claims else [],
        "counts": g["counts"],
        "generated_at": g["generated_at"],
        "read_only": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="KCR 影响分析（只读）：Source→Claim→Concept→Lesson→Quiz→Course→Website")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-id", help="来源 ID，如 SRC-RN-AV-BASE")
    group.add_argument("--claim-id", help="断言 ID，如 V14")
    group.add_argument("--report", help="报告 md 路径（从中抽取 source/claim ID）")
    group.add_argument("--claim-draft", help="断言草稿文本（仅回显，无实际匹配）")
    parser.add_argument("--out", help="输出 JSON 路径（默认 reviews/kcr/impact-report-<date>.json）")
    args = parser.parse_args()

    g = load_graph()

    source_id = args.source_id
    claim_id = args.claim_id
    if args.report:
        text = Path(args.report).read_text(encoding="utf-8", errors="replace") if Path(args.report).exists() else ""
        found_sources = sorted(set(re.findall(r"SRC-[A-Z0-9-]+", text)))
        found_claims = sorted(set(re.findall(r"\b[VCE]\d{2}\b", text)))
        source_id = found_sources[0] if found_sources else None
        claim_id = found_claims[0] if not source_id and found_claims else None
        if not source_id and not claim_id:
            print("报告中未找到 source/claim ID", file=sys.stderr)
            return 2

    if args.report:
        result = analyze(g, source_id=source_id, claim_id=claim_id,
                         trigger_type="new_research_report", trigger_ref=Path(args.report).as_posix())
    elif args.claim_draft:
        result = analyze(g, trigger_type="claim_status_request", trigger_ref="(inline claim draft)")
    else:
        result = analyze(g, source_id=source_id, claim_id=claim_id)
    if args.claim_draft:
        result["claim_draft_echo"] = args.claim_draft
        result["note"] = "草稿模式仅回显文本，未匹配到现有断言；正式分析请用 --claim-id/--source-id。new_sources 由 Stage 2 提案登记，本工具只读不登记来源。"

    if "error" not in result:
        contract_errors = validate_kcr.validate(result, validate_kcr.load_schema("impact-report"))
        if contract_errors:
            print("契约校验失败（impact-report.schema.json），未写文件：", file=sys.stderr)
            for e in contract_errors:
                print(f"  - {e}", file=sys.stderr)
            return 3

    out = Path(args.out) if args.out else ROOT / "reviews" / "kcr" / f"impact-report-{datetime.now().strftime('%Y%m%d')}.json"
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if "error" in result:
        print(f"错误：{result['error']}")
        return 2
    aff = result["affected"]
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"KCR 影响报告已写入 {shown}")
    print(f"  claims={len(aff['claims'])} concepts={len(aff['concepts'])} lessons={len(aff['lessons'])} "
          f"quizzes={len(aff['quizzes'])} courses={len(aff['courses'])}")
    print(f"  conflicts={len(result['conflicts'])} uncovered={len(result['uncovered'])} integrity_findings={len(result.get('integrity_findings', []))}")
    print("  只读：未修改任何源 JSON / 正文 / 断言状态。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
