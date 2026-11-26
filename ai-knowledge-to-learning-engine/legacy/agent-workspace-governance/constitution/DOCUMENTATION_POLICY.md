---
doc_id: DOCUMENTATION_POLICY
type: constitution
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 文档策略：分级与生命周期

## 一、三级文档

### L1 — Canonical（正式权威）

同一时间只有一个权威版本。包括：

- 章程（constitution）
- 规范（specification）
- ADR（架构决策记录）
- 当前架构文档
- 正式技术文档
- 正式研究报告
- 当前项目状态

> L1 文档可被引用为「当前事实」。变更必须带来源与记录。

### L2 — Active Work（在制工作）

- 变更提案（change proposal）
- 研究草稿
- Agent 计划
- 执行计划（execution plan）
- 评审报告（review report）
- 交接文档（handoff）
- 当前任务

> L2 是进行中的工作产物，不得当作正式事实引用。

### L3 — Archive（归档）

- 已完成的计划
- 旧报告
- 被取代的 ADR
- 执行日志
- 旧评审

> L3 可追溯，但**永远不被当作当前事实**。引用归档内容必须注明其历史性。

---

## 二、三条独立生命周期（禁止强行合并为一条状态机）

不同文档类型遵循各自的生命周期，互不混用。

### 通用文档生命周期

```
draft → proposed → under_review → approved → active → superseded → archived
```

### 变更提案生命周期

```
draft → proposed → approved → implementing → verifying → completed → archived
```

### ADR 生命周期

```
proposed → accepted → deprecated | superseded
```

> **铁律**：ADR 绝不因实现完成就自动 accepted。状态推进由人决定。

### 执行日志

执行日志可以有自己的生命周期，不套用上面任何一条。

---

## 三、文档注册表

所有文档在 `.governance/document-registry.json` 登记。字段见 `schemas/document.schema.json`：

`document_id` / `path` / `type` / `status` / `owner` / `created_at` / `updated_at` / `source_of_truth` / `generated` / `related_task` / `related_adr` / `related_documents` / `replaces` / `superseded_by` / `retention_policy`。

注册表是**索引，不是另一套知识库**。它只回答「有哪些文档、什么状态、谁负责、引用关系如何」，不承载正文。

### 支持的查询

- active（当前有效）
- pending approval（待审批）
- expired（过期）
- duplicates（重复）
- orphans（孤儿，无人引用）
- unregistered（未登记）
- missing owner（缺 owner）
- old versions missing supersession（旧版本缺取代记录）
- docs referenced by current task（被当前任务引用的文档）
