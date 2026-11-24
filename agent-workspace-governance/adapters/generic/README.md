---
doc_id: ADAPTER_GENERIC
type: adapter
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 通用 Adapter（generic）

## 用途

面向任意尚未提供专用 Adapter 的 AI Agent / AI 编码工具。这是所有 Adapter 的基准参考。

## 入口约定

- 通用入口文件：项目根的 `AGENTS.md`（指针式入口）。
- 权威规则正文位于本工具包的 `constitution/`，Adapter 只指向，不复制。

## 挂载方式

1. 在目标项目根放置/更新 `AGENTS.md`，指向本工具包的 `AGENTS.md` 与 `constitution/`。
2. 在 Agent 注册表登记该 Agent 的身份与能力。
3. 未验证能力标记 `unverified`。

## Adapter 只做什么

- 生成索引 / 指针 / 配置 / 兼容条目。
- 声明如何发现并加载权威规则。

## Adapter 不做什么

- 不复制章程正文到客户端私有目录。
- 不引入第二套规则来源。
- 不实现编排器。

## 验证记录

| 项 | 值 |
| --- | --- |
| config_present | 视具体客户端填写 |
| discovery_success | 未验证 |
| invocation_success | 未验证 |
| runtime_verification_status | `unverified`（默认） |
