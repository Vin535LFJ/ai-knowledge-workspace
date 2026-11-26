---
doc_id: ADAPTER_WORKBUDDY
type: adapter
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Adapter：WorkBuddy

## 说明

面向 WorkBuddy 客户端。只提供指针与兼容配置，**不复制治理规则正文**。

## 挂载方式

1. 项目根 `AGENTS.md` 指向本工具包的 `AGENTS.md` 与 `constitution/`。
2. 权威规则以 `constitution/` 为准。
3. Agent 注册表登记：`provider: workbuddy`、`harness: workbuddy`、可用技能/连接器/工具。

## 映射要点

- WorkBuddy 的 Skill 来自其技能目录，本工具包只引用、不重造。
- 连接器 / 插件能力写入 `supported_mcp` / `supported_tools`，配置文件存在 ≠ 已授权 ≠ 已发现 ≠ 可调用，分别记录。
- 未验证能力标记 `unverified`。

## 本 Adapter 不做什么

- 不把中文规则正文复制到 `~/.workbuddy-ai/skills/` 作为第二来源。
- 不实现任务编排（各业务项目保留自己的状态机，例如 Render_Notes 的 `WORKFLOW_STATE.md`）。

## 验证记录（独立）

| 项 | 值 |
| --- | --- |
| config_present | 待填写 |
| discovery_success | 待实跑 |
| invocation_success | 待实跑 |
| runtime_verification_status | `unverified`（默认） |
