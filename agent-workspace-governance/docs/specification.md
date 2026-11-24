---
doc_id: SPECIFICATION
type: specification
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 治理规范（Specification）

## 一、三个概念的边界（核心）

| 概念 | 定义 | 归属 |
| --- | --- | --- |
| **Agent Skills** | Agent「如何工作」的可复用能力（研究、写作、审查等）。 | **复用外部技能库**：<https://github.com/Vin535LFJ/mattpocock-skills-zh-CN-custom>。本工具包**绝不重建技能集**。 |
| **Agent Governance** | 多 Agent 在**同一项目内**如何协作：文档权威、任务归属、共享上下文、文档状态、ADR、变更管理、Agent 身份与能力映射、人工审批、交接、审计。 | **本工具包提供的正是这一层。** |
| **Agent Orchestration** | 真正的任务调度与执行。 | 由**各业务项目自己保留**（如 Render_Notes 的 `WORKFLOW_STATE.md` 轻量状态机）。本工具包**不实现编排器**。 |

> Skills 管「怎么干」，Governance 管「按什么规则协作」，Orchestration 管「真正把活排起来干」。

## 二、12 条原则

见 [`constitution/PROJECT_PRINCIPLES.md`](../constitution/PROJECT_PRINCIPLES.md)。要点：项目独立可迁移；单一权威来源；工作/正式文档分离；一套规则；一任务一 owner；变更有来源与记录；ADR 只记架构；普通计划无 ADR；重要状态机器可读；人工决策不可替代；Adapter 不复制正文；未验证能力标记 unverified。

## 三、文档三级

- **L1 Canonical**：章程、规范、ADR、当前架构、正式技术文档、正式研究报告、当前项目状态。**单一权威版本**。
- **L2 Active Work**：变更提案、研究草稿、Agent 计划、执行计划、评审报告、交接、当前任务。
- **L3 Archive**：已完成计划、旧报告、被取代 ADR、执行日志、旧评审。**可追溯但永不作为当前事实**。

## 四、三条独立生命周期（不得合并）

```
通用：draft → proposed → under_review → approved → active → superseded → archived
变更提案：draft → proposed → approved → implementing → verifying → completed → archived
ADR：proposed → accepted → deprecated | superseded
```

- ADR **绝不因实现完成自动 accepted**。
- 执行日志可有自己的生命周期。

## 五、MADR ADR 字段

`id` / `title` / `date` / `status` / `context` / `problem` / `goals` / `constraints` / `options` / `comparison/tradeoffs` / `decision` / `rationale` / `consequences` / `supersession` / `related docs` / `owner`。

类型区分：**ADR / RFC-Proposal / Change Plan / Task / Execution Log**。只有架构决策写 ADR；没有「每完成一个任务就产生一个 ADR」。

## 六、Agent Registry

字段：`agent_id`、`agent_name`、`provider`、`model`、`harness`、`capabilities`、`supported_skills`、`supported_mcp`、`supported_tools`、`context_limit`、`invocation_mode`、`parallel_capability`、`background_task_capability`、`file_access_scope`、`runtime_verification_status`。

支持 Claude Code、Codex、Cursor、OpenCode、WorkBuddy、ZCode 与 generic。

> **配置文件存在 ≠ 能被发现 ≠ 能成功调用。** 每个客户端有独立 Adapter 与验证记录。Adapter 只生成索引/指针/配置/兼容条目，从不复制完整规则正文。

## 七、Task Contract（JSON）

`task_id` / `title` / `owner_agent` / `status` / `read_paths` / `write_paths` / `protected_paths` / `dependencies` / `outputs` / `acceptance_criteria` / `human_approval_required`。

- 一个任务一个主 writer；并行研究允许；冲突要警告。
- 依赖检查、交接、完成前后审计。
- 建议分支/worktree 隔离。
- 文件所有权是**约定，不是真实锁**；可选 hooks/pre-commit/CI 仅在支持的客户端启用。

## 八、Document Registry

字段：`document_id` / `path` / `type` / `status` / `owner` / `created_at` / `updated_at` / `source_of_truth` / `generated` / `related_task` / `related_adr` / `related_documents` / `replaces` / `superseded_by` / `retention_policy`。

查询能力：active、pending approval、expired、duplicates、orphans、unregistered、missing owner、old versions missing supersession、docs referenced by current task。

> 注册表是索引，不是另一套知识库。

## 九、OpenSpec / MADR / KCR 分层

- Change Governance 借鉴 OpenSpec（`proposal.md`、`specs/`、`design.md`、`tasks.md`）。
- Architecture Decision 用 MADR。
- KCR 是「通用变更接口 + 项目 Adapter」；Render_Notes 的 `Source → Claim → Concept → Lesson → Quiz → Course` 只是**一个 Adapter**，不强迫所有项目采用。

**禁止把三套完整工作流叠加。**

## 十、Human-in-the-loop

必须人工审批：架构决策、业务目标变更、重大文档结构调整、权威知识升级、课程路线变更、高风险文档删除、重要归档、git 提交/推送、生产部署。

审批记录含 approver / time / object / decision / authorization scope。**无回复 ≠ 同意。**

## 十一、CLI 命令

`init` / `inventory`（别名 `index`）/ `validate` / `status` / `map` / `handoff` / `adr` / `archive-check` / `audit` / `doctor`。`doctor` 为只读诊断，发现错误时退出码 1。详见 [`README.md`](../README.md)。

## 十二、约束

Python 标准库 only；JSON Schema + Markdown；无云端 DB、无前端、无分布式锁、无 SaaS；不执行 git 操作；纯本地文件。

## 十三、13 类文档类型

本节定义标准的 13 类文档类型，对应 `schemas/document.schema.json` 中 `type` 字段的枚举。旧值（如 `change-proposal`、`research-report`、`formal-tech-doc`）作为历史数据继续兼容、可正常读取，但新建文档应优先使用下表标准类型；`doctor` 命令会提示非标准类型。

> 名称说明：`Session Note` 含空格，是其 type 字面值；文件名/路径建议用 `session-note` slug。

| 类型（type 值） | 用途 | 必填 frontmatter | 权威源 / 保留策略 |
| --- | --- | --- | --- |
| `ADR` | 架构决策记录（MADR 字段），仅记录难以逆转的架构决策 | `doc_id` `type` `status` `owner` `created` `updated` | 自身为 L1 权威源；`keep-forever`，被取代标 `superseded` 并指向新 ADR |
| `Spec` | 规格说明：系统/接口/行为的精确约定 | 同上 | L1 自身为权威源；实现变更后更新或标 `superseded` |
| `Plan` | 计划：阶段目标、步骤、里程碑（L2 工作文档） | 同上 | 引用对应 `Spec`/`Task`，不单独作为 L1 事实；完成后归档 |
| `Task` | 任务契约：读写范围、依赖、验收标准 | 同上（另建议 `task_id`） | 以 `.governance/task-registry.json` 为机器可读权威源；完成后归档 |
| `Runbook` | 运维手册：可执行的操作步骤与应急流程 | 同上 | 自身为权威源；每次演练后复核更新 |
| `Glossary` | 术语表：项目统一术语与定义 | 同上 | L1 自身为权威源；`keep-forever` 或随版本更新 |
| `Architecture` | 架构说明：当前系统结构、组件与关系 | 同上 | L1 自身为权威源；架构变更时更新并留痕 |
| `Skill` | 技能说明：Agent 可复用能力的描述与边界 | 同上（建议 `source_of_truth` 指向外部技能库） | 指针型文档，权威源指向技能实现；本工具包不重建技能集 |
| `Workflow` | 工作流：跨步骤的协作流程与状态流转 | 同上 | 自身为权威源；状态机以机器可读文件为准 |
| `Script` | 脚本说明：脚本用途、入参、副作用与调用方式 | 同上 | 权威源指向脚本实现；脚本变更时同步更新 |
| `Handoff` | 交接文档：任务移交时的产出、验收、未决事项 | 同上（建议 `related_task`） | 引用对应 `Task`；交接完成后归档 |
| `Audit` | 审计报告：冗余/孤儿/冲突/过期引用等检查结果 | 同上（建议 `related_documents`） | 快照型文档，`archive-after-180d` |
| `Session Note` | 会话记录：一次协作会话的过程与结论摘要 | 同上（建议 `date`） | 工作记录，不作为 L1 事实；`archive-after-180d` |

> 所有类型均需 `doc_id` / `type` / `status` / `owner` / `created` / `updated` 六个必填 frontmatter 字段（与 `REQUIRED_FM` 一致）；「权威源 / 保留策略」列给出该类型的建议取向，而非额外必填字段。
