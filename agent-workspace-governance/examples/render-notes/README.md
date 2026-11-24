---
doc_id: example-render-notes-mapping
type: migration-adapter-note
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Render_Notes 迁移适配说明（Adapter Note）

> **重要：这是一份「适配说明」，不是对 Render_Notes 的重写。**
> Render_Notes 继续保留自己的目录、状态机与知识结构；本工具包只提供「如何把它的现有资产映射到治理概念」的指针。

## 一、概念分层（不要三套全栈）

- **Change Governance** 借鉴 OpenSpec：`proposal.md`、`specs/`、`design.md`、`tasks.md`。
- **Architecture Decision** 使用 MADR。
- **Knowledge Change Governance（KCR）** 是「通用变更接口 + 项目 Adapter」。
  Render_Notes 的 `Source → Claim → Concept → Lesson → Quiz → Course` 只是**其中一个 Adapter**，绝不强迫其他项目采用。

> 禁止把 OpenSpec、MADR、KCR 三套完整流程同时压到一个项目上；按需取用。

## 二、目录映射表

| Render_Notes 现有资产 | 治理工具包中的对应概念 | 处理方式 |
| --- | --- | --- |
| `.agent/constitution/` | `constitution/`（治理章程正文） | **权威规则来源**。工具包的 `constitution/` 与之一一对应；Adapter 只做指针，不复制正文。 |
| `.agent/decisions/0001-*.md` | ADR（MADR 决策记录） | 每个编号决策文件登记为一个 ADR，状态按 MADR 生命周期推进，不因实现完成自动 accepted。 |
| `DECISIONS.md` | 历史索引（不是权威决策本身） | 作为 ADR 的历史目录索引；权威正文仍在各 `0001-*.md`。 |
| `reviews/` | 评审报告（review report, L2） | 每次评审登记为一份 review-report 文档。 |
| `reviews/KNOWLEDGE_CHANGE_REVIEW.md` | KCR Adapter | 这是知识变更治理在项目内的**具体适配器**，不是通用规则；映射到通用变更接口即可。 |
| `WORKFLOW_STATE.md` | 当前项目状态（L1 项目状态） | 登记为「current project state」文档；其状态机由 Render_Notes 自己保留，工具包不接管编排。 |
| `.agent/skills/research-to-learning/` | 外部技能引用 | 只引用、不重建；登记到 Agent 注册表的 `supported_skills`，能力需实跑验证后标记 verified/unverified。 |

## 三、编排边界

Render_Notes 自带轻量状态机（`WORKFLOW_STATE.md`）负责真正的任务排程与执行——这属于 **Agent Orchestration**，由业务项目自己保留。

治理工具包**不实现编排器**，只做：
- 文档权威与状态登记；
- 任务 owner 与读写范围约定；
- ADR 与变更管理；
- Agent 身份与能力映射；
- 人工审批、交接与审计。

## 四、迁移步骤（建议）

1. 在 Render_Notes 项目根放置指向本工具包的 `AGENTS.md` 指针（可用 `governance.py init`）。
2. 用 `governance.py inventory` 扫描现有 Markdown 并登记。
3. 将 `.agent/decisions/0001-*.md` 逐个登记为 ADR，保留原文件不动。
4. 把 `reviews/KNOWLEDGE_CHANGE_REVIEW.md` 标注为 KCR Adapter，而非通用规则。
5. 把 `WORKFLOW_STATE.md` 登记为 L1 项目状态，状态机仍由项目自身维护。
6. 用 `governance.py validate` / `audit` 检查缺 owner、孤儿与过期引用。

## 五、铁律复述

- 本工具包**不**重写 Render_Notes 的知识结构（`Source → Claim → Concept → Lesson → Quiz → Course`）。
- 本工具包**不**复制 `.agent/constitution/` 的正文到客户端私有目录。
- 未验证的 Agent 能力显式标记 `unverified`。

## 六、真实项目适配实跑记录（2026-11-21，验收标准第 7 条闭环）

> 本节把上方"建议迁移步骤"替换为**实际执行记录**（对真实 Render_Notes 仓库=AI Knowledge-to-Learning Engine 执行，2026-11-21）。

- **实跑命令**：`governance.py init / inventory / validate / map / doctor / audit --project <ENGINE>`（全部 `--project` 定位，未在 ENGINE 内执行任何 git 操作）。
- **产出**：ENGINE 根新增 `.governance/` 五 JSON（config/document-registry/task-registry/agent-registry/adr-index）；document-registry 登记 **183 份 Markdown**。
- **type 分布**：adapter 2 / review-material 31 / agent-plan 1 / kcr 2 / research-report 1 / **unknown 146**——Engine 文档用的是项目自有 frontmatter 约定（type/level/status/owner），与治理工具包的 owner/created_at/updated_at 必填字段约定不同，146 份 unknown 是**真实迁移成本的量化**（对应 docs/migration-guide.md 的迁移路径）。
- **真实适配发现的工具缺口与修复**：首跑 `inventory` 把 `site-vitepress/node_modules/` 全量吞入（1233 项问题）——已修：`scan_markdown_docs` 增加 `IGNORE_DIRS`（node_modules/vendor/dist/build 等），修复后 25 测试全过 + 新增 3 个示例/忽略回归测试。
- **诊断结论（doctor 621 项，非零退出）**：属"真实项目未完全采纳治理 frontmatter"的预期诊断，不阻塞使用——映射关系（§二）依然成立；正式采纳需按 migration-guide 补 frontmatter（由目标项目自行决定）。
- **编排边界实跑确认**：治理工具包未触碰 ENGINE 的 `.agent/`、状态机与知识结构（红线复述的实跑验证）。


## 七、阶段 3 验收九条对照（2026-11-21）

| # | 验收标准 | 状态 | 证据 |
|---|---|---|---|
| 1 | 治理规范 | 已有 | constitution 4 篇 + docs/specification.md（12 原则/13 类文档/三级分层） |
| 2 | 文档生命周期 | 已有 | specification §3/§4 + archive-check 命令 |
| 3 | Task/Handoff 契约 | 已有 | task.schema.json（read/write/protected、acceptance_criteria、human_approval_required）+ handoff 命令 |
| 4 | ADR | 已有 | MADR 模板 + adr create/list/check + adr-index.json |
| 5 | 元数据结构 | 已有 | 5 schemas + 6 必填 frontmatter + 13 类 type 枚举 |
| 6 | 最小自动化 | 已有 | cli/governance.py 1169 行 stdlib-only 11 命令 + doctor 非零退出诊断 |
| 7 | 真实项目适配案例 | **本次闭环** | §六实跑记录（183 docs/621 诊断/IGNORE_DIRS 修复） |
| 8 | 独立示例项目验证 | **本次闭环** | examples/basic-project 纳入 ExampleProjectTests（状态完整性/可扫描性） |
| 9 | 使用说明 | 已有 | README 快速开始+命令表、docs/migration-guide、docs/architecture |

结论：9/9 全部闭环；25→28 tests OK；提交 6aec3d3（未 push）。
