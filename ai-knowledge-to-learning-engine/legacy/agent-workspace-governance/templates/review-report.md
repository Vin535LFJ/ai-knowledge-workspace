---
doc_id: review-{{REVIEW_ID}}
type: review-report
status: draft
owner: {{OWNER}}
created: {{DATE}}
updated: {{DATE}}
---

# 评审报告：{{TITLE}}

> 评审报告属于 L2 工作文档。

## 评审对象

{{OBJECT}}

## 评审人 / 时间

{{REVIEWER}} / {{DATE}}

## 检查项

| 项 | 结果 | 备注 |
| --- | --- | --- |
| 是否有单一权威来源 | {{CHECK_SOT}} |  |
| 工作文档与正式文档是否分离 | {{CHECK_SEPARATION}} |  |
| 变更是否有来源与记录 | {{CHECK_SOURCE_RECORD}} |  |
| 是否误用 ADR | {{CHECK_ADR}} |  |
| 任务是否有唯一 owner 与读写范围 | {{CHECK_OWNER}} |  |
| 人工审批是否到位 | {{CHECK_APPROVAL}} |  |

## 发现的问题

{{FINDINGS}}

## 结论与建议

{{CONCLUSION}}
