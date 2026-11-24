#!/usr/bin/env python3
"""KCR schema 程序化校验器（P8 片二，stdlib-only，D05 原则）。

覆盖 tools/kcr/schema/ 四个契约：impact-report / change-proposal / review-decision / run-state（P9）。
实现的 JSON Schema 关键字子集 = 各 schema 实际用到的全部关键字：
    type（含类型数组）/ required / properties / items / enum / pattern / minItems
元信息关键字（$schema/title/description）忽略；**遇到未支持关键字直接抛错**——
schema 未来演进时强制校验器同步升级，不静默漏检。

另实现 schema description 中文档化的硬规则（semantic_errors）：
- change-proposal：action ∈ {modify, deprecate, reverify} 时 target.id 必填；
  --stage2 时 human_decision 必须为 null（AI 不预填，G1 性质）。
- run-state（P9 设计稿 §4 不变量）：human_gate passed 必须有人工 approver+approved_at；
  进入 PUBLISH/FEEDBACK 必须 gate passed；kcr_substate APPROVED 及以后必须有
  kcr_approved 人工过渡记录；status=done 只能出现在 FEEDBACK。

用法（本机用 py -3）：
    py -3 tools/kcr/validate_kcr.py reviews/kcr/impact-v14-replay.json
    py -3 tools/kcr/validate_kcr.py proposal.json --schema change-proposal --stage2
    py -3 tools/kcr/validate_kcr.py .agent/runs/RUN-x.json --schema run-state
不指定 --schema 时按文件名推断（run-state* / impact* / *proposal* / *decision*）。
退出码：0 全部通过；1 存在校验错误；2 用法/文件错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent / "schema"
SCHEMA_NAMES = ("impact-report", "change-proposal", "review-decision", "run-state")

_META_KEYWORDS = {"$schema", "title", "description"}
_SUPPORTED_KEYWORDS = _META_KEYWORDS | {"type", "required", "properties", "items", "enum", "pattern", "minItems"}

_TYPE_MAP = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
}


def load_schema(name: str) -> dict:
    if name not in SCHEMA_NAMES:
        raise ValueError(f"未知 schema: {name}（可选 {SCHEMA_NAMES}）")
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


def _check_type(value, type_spec) -> bool:
    types = type_spec if isinstance(type_spec, list) else [type_spec]
    for t in types:
        if t not in _TYPE_MAP:
            raise ValueError(f"未支持的 type: {t}")
        if _TYPE_MAP[t](value):
            return True
    return False


def validate(instance, schema: dict, path: str = "$") -> list[str]:
    """返回错误列表（空 = 通过）。路径用 JSONPath 风格定位。"""
    unknown = set(schema) - _SUPPORTED_KEYWORDS
    if unknown:
        raise ValueError(f"{path}: schema 含未支持关键字 {sorted(unknown)}——校验器需同步升级，不静默漏检")

    errors: list[str] = []
    if "type" in schema and not _check_type(instance, schema["type"]):
        errors.append(f"{path}: 类型应为 {schema['type']}，实际 {type(instance).__name__}")
        return errors  # 类型不对时后续关键字无意义
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: 值 {instance!r} 不在枚举 {schema['enum']}")
    if "pattern" in schema and isinstance(instance, str) and not re.search(schema["pattern"], instance):
        errors.append(f"{path}: 值 {instance!r} 不匹配 pattern {schema['pattern']!r}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: 缺必填字段 {key!r}")
        for key, sub in schema.get("properties", {}).items():
            if key in instance:
                errors.extend(validate(instance[key], sub, f"{path}.{key}"))
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: 数组长度 {len(instance)} < minItems {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors.extend(validate(item, schema["items"], f"{path}[{i}]"))
    return errors


def semantic_errors(doc: dict, name: str, *, stage2: bool = False) -> list[str]:
    """schema description 中文档化、但 JSON Schema 子集表达不了的硬规则。"""
    errors: list[str] = []
    if name == "change-proposal":
        for i, item in enumerate(doc.get("items", []) or []):
            action = item.get("action")
            target = item.get("target", {}) or {}
            if action in ("modify", "deprecate", "reverify") and not target.get("id"):
                errors.append(f"$.items[{i}]: action={action} 必须提供 target.id（既有项 id）")
        if stage2 and doc.get("human_decision") is not None:
            errors.append("$.human_decision: Stage 2 提交时必须为 null（人工裁决属 Stage 3，AI 不预填）")
    if name == "run-state":
        gate = doc.get("human_gate")
        late_phase = doc.get("phase") in ("PUBLISH", "FEEDBACK")
        if isinstance(gate, dict):
            if gate.get("status") == "passed" and (not gate.get("approver") or not gate.get("approved_at")):
                errors.append("$.human_gate: passed 必须记录人工 approver 与 approved_at（人工门不可绕过，AI 不得批准）")
            if late_phase and gate.get("status") != "passed":
                errors.append(f"$.human_gate: phase={doc.get('phase')} 要求 gate 已 passed（未批准不发布）")
        elif late_phase:
            errors.append(f"$.human_gate: phase={doc.get('phase')} 必须携带已 passed 的人工关卡记录")
        if doc.get("kcr_substate") in ("APPROVED", "APPLIED", "VERIFIED"):
            if not any(t.get("action") == "kcr_approved" and t.get("operator")
                       for t in doc.get("transitions", []) or []):
                errors.append("$.kcr_substate: APPROVED 及以后必须有 kcr_approved 过渡记录（含人工操作者）")
        if doc.get("status") == "done" and doc.get("phase") != "FEEDBACK":
            errors.append("$.status: done 只能出现在 FEEDBACK 阶段（阶段跳转检查）")
    return errors


def infer_schema(filename: str) -> str | None:
    low = filename.lower()
    if "run-state" in low or "runstate" in low:
        return "run-state"
    if "impact" in low:
        return "impact-report"
    if "proposal" in low:
        return "change-proposal"
    if "decision" in low:
        return "review-decision"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="KCR 三契约程序化校验（stdlib-only）")
    parser.add_argument("files", nargs="+", help="待校验 JSON 文件")
    parser.add_argument("--schema", choices=SCHEMA_NAMES, help="契约名（缺省按文件名推断）")
    parser.add_argument("--stage2", action="store_true", help="change-proposal 按 Stage 2 提交口径校验（human_decision 必须 null）")
    args = parser.parse_args()

    failed = False
    for f in args.files:
        path = Path(f)
        name = args.schema or infer_schema(path.name)
        if name is None:
            print(f"{f}: 无法从文件名推断契约，请用 --schema 指定", file=sys.stderr)
            return 2
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{f}: 读取/解析失败：{exc}", file=sys.stderr)
            return 2
        errors = validate(doc, load_schema(name)) + semantic_errors(doc, name, stage2=args.stage2)
        if errors:
            failed = True
            print(f"{f} [{name}]: FAIL（{len(errors)} 处）")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"{f} [{name}]: OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())