---
doc_id: ADAPTER_CLAUDE_CODE
type: adapter
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Adapter：Claude Code

## 说明

面向 Claude Code 客户端。本 Adapter 只提供指针与兼容配置，**不复制治理规则正文**。

## 挂载方式

1. 项目根 `AGENTS.md`（或 Claude Code 识别的项目指令入口）指向本工具包的 `AGENTS.md`。
2. 权威规则始终以 `constitution/` 为准。
3. 在 Agent 注册表登记：`provider: anthropic`、`harness: claude-code`、可用 `supported_skills` / `supported_mcp` / `supported_tools`。

## 映射要点

- 能力声明写入 Agent 注册表的 `capabilities` / `supported_mcp` / `supported_tools`。
- 并行与后台任务能力分别由 `parallel_capability` / `background_task_capability` 记录，未验证则 `unverified`。
- 技能从外部技能库引用，不在此重造。

## 本 Adapter 不做什么

- 不把规则正文写入 `.claude/` 之类私有目录作为副本。
- 不实现任务编排。

## 验证记录（每个客户端独立）

| 项 | 值 |
| --- | --- |
| config_present | 待填写 |
| discovery_success | 待实跑 |
| invocation_success | 待实跑 |
| runtime_verification_status | `unverified`（默认，直到实跑验证） |
