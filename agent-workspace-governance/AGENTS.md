---
doc_id: AGENTS
type: adapter-entry
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# AGENTS.md —— 通用 Agent 入口（指针）

> 本文件是**指针式入口**，面向任意 AI Agent / AI 编码工具。它只告诉 Agent「去哪里读规则」，不重复任何规则正文。

## 你是谁

进入本项目工作的 Agent，请先确认自己的身份、能力与验证状态，并在 Agent 注册表中登记（`runtime_verification_status` 为 `verified` / `unverified`）。

## 请先阅读（按顺序）

1. [`constitution/PROJECT_PRINCIPLES.md`](constitution/PROJECT_PRINCIPLES.md) —— 12 条治理原则
2. [`constitution/AGENT_RULES.md`](constitution/AGENT_RULES.md) —— 所有 Agent 共用规则
3. [`constitution/DOCUMENTATION_POLICY.md`](constitution/DOCUMENTATION_POLICY.md) —— 文档分级与生命周期
4. [`constitution/HUMAN_APPROVAL_POLICY.md`](constitution/HUMAN_APPROVAL_POLICY.md) —— 人工审批清单
5. [`docs/specification.md`](docs/specification.md) —— 完整规范

## 你在这个项目里要遵守的核心约定

- **一个任务一个 owner + 明确读写范围**；写前先确认 `write_paths` 归属自己。
- **正式文档单一权威来源**；工作文档与正式文档分离。
- **ADR 只记架构决策**，且绝不因实现完成就自动 accepted。
- **人工决策不可被 AI 替代**；无回复 ≠ 同意。
- **能力未验证就显式标记 unverified**；配置存在 ≠ 可调用。
- 交接用 [`templates/handoff.md`](templates/handoff.md)；评审用 [`templates/review-report.md`](templates/review-report.md)。

## 工具与命令

治理 CLI：`cli/governance.py`（9 个命令，详见 [`README.md`](README.md)）。所有操作均为本地文件操作。

> 若你使用了某个具体客户端 Adapter（Claude Code / Codex / WorkBuddy / ZCode / 通用），请只按该 Adapter 的指针加载对应入口，不要复制规则正文到客户端私有目录。
