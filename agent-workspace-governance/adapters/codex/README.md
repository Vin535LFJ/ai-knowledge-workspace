---
doc_id: ADAPTER_CODEX
type: adapter
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Adapter：Codex

## 说明

面向 Codex 客户端。只提供指针与兼容配置，**不复制治理规则正文**。

## 挂载方式

1. 项目指令入口指向本工具包的 `AGENTS.md` 与 `constitution/`。
2. 权威规则以 `constitution/` 为准。
3. Agent 注册表登记：`provider: openai`、`harness: codex`、可用技能/MCP/工具。

## 映射要点

- `invocation_mode` 记为 `cli` / `api`（视实际）。
- 未实跑验证的能力一律 `runtime_verification_status: unverified`。
- 文件访问范围写入 `file_access_scope`。

## 本 Adapter 不做什么

- 不复制规则正文到客户端私有目录。
- 不实现编排器。

## 验证记录（独立）

| 项 | 值 |
| --- | --- |
| config_present | 待填写 |
| discovery_success | 待实跑 |
| invocation_success | 待实跑 |
| runtime_verification_status | `unverified`（默认） |
