---
doc_id: ADAPTER_ZCODE
type: adapter
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Adapter：ZCode

## 说明

面向 ZCode 客户端。只提供指针与兼容配置，**不复制治理规则正文**。

## 挂载方式

1. 项目指令入口指向本工具包的 `AGENTS.md` 与 `constitution/`。
2. 权威规则以 `constitution/` 为准。
3. Agent 注册表登记：`provider: zcode`、`harness: zcode`、可用技能/MCP/工具。

## 映射要点

- 能力声明写入注册表对应字段。
- 并行 / 后台任务能力未验证则 `unverified`。
- 技能从外部技能库引用，不在本工具包重造。

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
