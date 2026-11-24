---
doc_id: basic-project-design
type: formal-tech-doc
level: L1
status: active
owner: human
created: 2026-11-19
updated: 2026-11-19
source_of_truth: docs/design.md
---

# 设计说明：待办清单 CLI

## 目标

提供一个本地、无依赖的待办清单管理工具。

## 数据模型

- `Task`：`id`、`title`、`done`（布尔）。
- 存储：本地 JSON 文件。

## 命令

- `add <title>` —— 新增任务
- `list` —— 列出任务
- `done <id>` —— 标记完成

## 治理说明

这是一份普通的 L1 正式技术文档，单一权威来源为自身。它不产生 ADR（因为不是架构层面的不可逆决策）。
