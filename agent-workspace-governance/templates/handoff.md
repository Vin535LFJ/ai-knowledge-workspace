---
doc_id: handoff-{{TASK_ID}}
type: handoff
status: active
owner: {{OWNER_AGENT}}
created: {{DATE}}
updated: {{DATE}}
---

# 交接文档：{{TASK_ID}} — {{TITLE}}

> 标准交接文档。由 `governance.py handoff` 从任务注册表生成。

## 任务信息

- 任务 ID（task_id）：{{TASK_ID}}
- 标题（title）：{{TITLE}}
- 当前状态（status）：{{STATUS}}
- 原 owner（owner_agent）：{{OWNER_AGENT}}
- 接手方（to_agent）：{{TO_AGENT}}
- 交接时间（date）：{{DATE}}

## 读写范围

- 读（read_paths）：{{READ_PATHS}}
- 写（write_paths）：{{WRITE_PATHS}}
- 保护（protected_paths）：{{PROTECTED_PATHS}}

## 依赖（dependencies）

{{DEPENDENCIES}}

## 已产出（outputs）

{{OUTPUTS}}

## 验收标准（acceptance_criteria）

{{ACCEPTANCE_CRITERIA}}

## 人工审批

- 是否需要人工审批：{{HUMAN_APPROVAL_REQUIRED}}
- 无回复 ≠ 同意。

## 未决事项与交接备注

{{HANDOFF_NOTES}}
