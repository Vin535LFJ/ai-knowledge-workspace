---
doc_id: PROG-PROGRAM
type: program-charter
status: active
owner: human
created: 2026-11-19
updated: 2026-11-25
---

# AI Knowledge Program · 目标与边界（章程）

> 本文件夹是**统筹管理层**，不是产品，也不是第五个知识库。
> 它只回答：整个 AI Knowledge 要去哪（PROGRAM）、现在唯一在做什么（NOW）、接下来按什么顺序（ROADMAP）、什么暂时不做（PARKING-LOT）。
> 本文件是入口。Agent 工作规则见 `PROGRAM-MANAGER.md`。

**文档入口**：[USER-GUIDE.md](USER-GUIDE.md)（使用指南）· [PROJECT-DOCUMENTATION-INDEX.md](PROJECT-DOCUMENTATION-INDEX.md)（全项目文档导航）· [AUDIT-REPORT.md](AUDIT-REPORT.md)（2026-11-23 六阶段独立审计）· [POST-AUDIT-SUMMARY.md](POST-AUDIT-SUMMARY.md)（审计后收口）。

## 1. 长期愿景

让 AI 把任意领域的原始资料，稳定地变成**可信、可学、可实践**的学习产品：
原始资料 → 深度研究与证据提取 → 结构化知识 → 课程与教材 → 实践与练习 → 交互式学习网站。

愿景可以很长，但**当前只允许一个项目处于主动开发状态**：AI Knowledge-to-Learning Engine（仓库旧名 Render_Notes，2026-11-19 改名）。

## 2. 三层结构（不同性质的东西不在同一层）

| 层 | 成员 | 职责 | 当前状态 |
|---|---|---|---|
| 第 1 层 · 统筹管理 | AI Knowledge Program（本文件夹） | 目标、优先级、路线图、项目状态、范围控制 |  active，保持薄 |
| 第 2 层 · 核心产品 | AI Knowledge-to-Learning Engine（`ai-knowledge-to-learning-engine/`） | 知识生产全链路：资料→研究→知识→教材→实践→网站 | **唯一主动开发线** |
| 第 3 层 · 未来可复用能力 | Agent Workspace Governance / GitHub Project Radar | 经真实需求验证后才值得抽取的独立能力 | 已解冻并真实验证（2026-11-21，D20）；**维护期**：仅允许明确范围内的缺陷修复与必要可靠性验证，不扩展功能。2026-11-24 独立审计判定两者 PARTIAL（Governance「9/9」为文档自证；Radar「200 快照」口径夸大），整改见 AUDIT-REPORT.md §C/§E；无持续真实需求不追加投入（见 PARKING-LOT） |

`matt-pocock-skills-zh-cn/`（旧名 mattpocock-skills-zh-CN-custom）是**独立的 Skills 来源仓库**，不属于以上任何一层的产品建设：不并入 Governance，不重建第二套 Skills 仓库。

## 3. 五类事物的边界（有关联 ≠ 同一个项目）

| 类别 | 定义 | 归属 |
|---|---|---|
| Knowledge | 要沉淀的领域知识 | 跟随实际领域和产品归档（Engine 内） |
| Skills | Agent 使用的专业工作方法 | 通用技能在 Skills 来源仓库；项目专属 Skill 在 Engine 内 |
| MCP / Tools | Agent 调用的能力和工具 | 由实际使用它们的项目维护 |
| Governance | 管理 Agent 协作过程、文档、任务和规范的机制 | 现阶段 = Engine 自有 `.agent/`；通用抽取暂缓 |
| Program | 管理整个项目群的目标和优先级 | 本文件夹，只管项目级状态 |

## 4. 目录结构（2026-11-26 D22 统一收敛后，位置唯一权威）

```
C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\
├── ai-knowledge-to-learning-engine\    ← 核心仓（唯一活跃线；= Vin535LFJ/ai-knowledge-to-learning-engine）
│   ├── program\                        ← 统筹层（本目录，D22 并入；原独立仓退出）
│   ├── integrations\github-radar\      ← 外部研究入口模块（D22 并入）
│   ├── legacy\                         ← Governance 整仓归档 + 旧适配产物（只读不维护）
│   └── docs\consolidation\             ← D22 决策/盘点/映射/审计/验收
├── matt-pocock-skills-zh-cn\           ← Skills 来源库（独立仓 = Vin535LFJ/matt-pocock-skills-zh-cn）
└── README.md                           ← 工作区导航（两仓）
```

- **D22（2026-11-26）**：五项目 → 两仓。Program/Governance/Radar 原目录移入 `AI-Knowledge-backups\2026-11-26-consolidation\retired\`（bundle 恢复验证 PASS，不删除）。决策与映射：`../docs/consolidation/TARGET-ARCHITECTURE.md` / `MIGRATION-MAP.md`。
- 2026-11-19：Render_Notes 自 `GITCODE\Render_Notes` 迁入（PD-002 收尾）；同日经用户批准**本地目录改名**为 `ai-knowledge-to-learning-engine` 与 `matt-pocock-skills-zh-cn`（Move-Item 成功，git 完好：Engine HEAD=`e848d28`、Skills HEAD=`e1936f2`；改名后门禁复跑 validate 11/0/0、37 claims 误标 0）。
- **过渡态已消除（2026-11-20 T1 执行完成）**：本地目录、GitHub 仓库名、git remote 均为新名（remote set-url ×2 已执行，ls-remote 复核通过）；仓库 URL 引用已按迁移方案 Phase 2/4/5 集中更新（含品牌文案 + README 正式名）。旧 URL 重定向兜底不再依赖。详见 `plans/2026-11-19-rename-audit-and-migration.md`（status 已改 completed）。
- 父文件夹本身不是 git 仓库；各子项目是独立仓库。任何再迁移必须先改本节 + 记 PD 决策。
- 旧绝对路径（`GITCODE\Render_Notes`、`AI-Knowledge\Render_Notes`、`E:\AI-Tools\mattpocock-skills-zh-CN-custom`）的引用已失效，发现时按新路径核对，不静默批量改写。

### 项目入口（真实状态以项目内文档为权威，Program 不复制）

| 项目 | 入口文档 | 权威状态源 |
|---|---|---|
| Engine | `ai-knowledge-to-learning-engine/.agent/README.md` | `WORKFLOW_STATE.md` / `DECISIONS.md` / `reviews/REVIEW_STATUS.md` / `reviews/decision-kit/` |
| Skills 库 | `matt-pocock-skills-zh-cn/README.md` | `SYNC.md` / `BACKPORTS.md` |
| Governance（冻结） | `agent-workspace-governance/README.md` | 其本地 git 与测试 |
| Radar（冻结） | `github-project-radar/README.md` | 其本地 git 与测试 |

## 5. 本文件夹文件职责（唯一职责，不重叠）

| 文件 | 唯一职责 |
|---|---|
| `PROGRAM.md` | 目标、边界、原则、非目标（本文件） |
| `NOW.md` | 当前唯一主目标、正在做的任务、验收标准、阻塞事项 |
| `ROADMAP.md` | Now / Next / Later 阶段规划 |
| `PARKING-LOT.md` | 所有暂时不做的想法、需求和未来项目 + 准入规则 |
| `PROGRAM-MANAGER.md` | Program Manager Agent 工作规则（五项职责 + 范围控制硬规则） |
| `decisions/` | 程序级决策记录（PD-001…PD-003）与 PD-Q 裁决存档 |
| `plans/` | 程序级 working plan 与执行报告（命名迁移方案已完成；进度复核 2026-11-20；embodied kickoff 2026-11-23；阶段执行报告 2026-11-25） |
| `handoffs/` | 跨项目交接指针索引（正文留在产生它的项目内） |
| `references/` | 用户提供的引导文档原件（只读） |
| `archive/` | 被取代的旧统筹文件（只移动不删，保留历史） |

## 6. 原则

1. **单活跃线**：任何时刻只有一个项目主动开发（当前 = Engine）。其他方向保留成果，不新增投入。
2. **不提前平台化**：一个能力在没有被真实需求验证之前，不因为它"未来可能成为平台"就先平台化。
3. **冻结 ≠ 删除**：裁剪只停止新增投入，不销毁任何已有工作。
4. **单一事实源**：项目内部状态以项目自己的文档 + git 实测为权威；Program 只存带日期的项目级快照与指针，冲突时以项目内为准。
5. **人工关卡不可自批**：commit/push、远程创建、部署、断言升级、课程路线、范围变更必须人工批准；**未回复不视为同意**。
6. **质量优先于数量**：完整可重复的工作流优先于批量生成；不批量生成课程制造进度。
7. **复用既有治理**：Engine 的 `.agent/`、DECISIONS、KCR、reviews 继续作为 Engine 治理权威，不重做一套。

## 7. 非目标（明确不做）

- 不把几个项目整合成一个超级项目；不建统管所有 Agent/Skills/MCP/Tools 的复杂多 Agent 平台。
- 不建"所有知识、Skill、MCP、Tools 的中央管理平台/注册表"（不列入当前路线图）。
- 不开发 Program Dashboard、数据库、自动化调度平台。
- 不新建"知识库收录 / skill 收录"独立项目（PD-003 §2.5：合理内核已被 Engine P8 输入合同与 Skills 库覆盖）。
- 不让 learning-experience-design 独立成仓；不把治理做进 Skills 库。
- 不复制 Engine 的工作流状态、技术决策和项目文档进 Program。

## 8. 正式命名体系（2026-11-19 用户任务书固定；正式名称与仓库名分离）

**原则：正式名称承担解释，仓库名只是标识。** 产品增加新功能、Skills 库增加新技能，都不需要改名。

| 类型 | 正式名称 | 仓库名 / 目录名 |
|---|---|---|
| 项目群 | AI Knowledge Program | `AI-Knowledge-Program` |
| 本地总目录 | AI Knowledge Workspace | `AI-Knowledge` |
| 核心产品 | AI Knowledge-to-Learning Engine | `ai-knowledge-to-learning-engine` |
| Skills 来源库 | Matt Pocock Skills 中文定制发行版 | `matt-pocock-skills-zh-cn` |
| 未来治理项目 | Agent Workspace Governance | `agent-workspace-governance` |
| 未来情报项目 | GitHub Project Radar | `github-project-radar` |
| Engine 内部 Skill | Learning Experience Design | `learning-experience-design` |

**README 标准描述（改名执行时采用）**：
- Engine：*An AI-powered knowledge-to-learning production engine that transforms source materials into structured knowledge, courses, learning materials, practical exercises, and interactive learning experiences.*
- Skills 库：*A Chinese-adapted and customized distribution of Matt Pocock's Agent Skills, including translation, verified backports, compatibility notes, and upstream synchronization.*（必须明确标注为中文适配定制发行版，不得造成上游官方发行版的误解）

**命名规则**：
1. 项目展示名称使用清晰的英文正式名称。
2. GitHub Repository 使用小写 kebab-case。
3. 本地项目目录与仓库名保持一致。
4. README 标题、项目描述和文档中的正式名称保持一致。
5. 不再混用 Render Notes、Render_Notes、Knowledge Engine 等旧名称。
6. 旧名称只在迁移说明、历史记录和必要的兼容说明中出现。
7. 所有文档链接、远程地址、配置引用使用新的规范名称。

**执行状态**：命名体系即日生效于 Program 文档与新产出物。**本地目录已于 2026-11-19 改为新名**（用户批准）；**GitHub 两仓已于 2026-11-19 由用户手动改名并经 ls-remote 核实**；**2026-11-20 T1 执行完成**：remote set-url ×2 切换至新 URL、仓库 URL 引用集中更新（含品牌文案 + README 正式名/标准描述）、验证通过，OmniWorld-Engine 跟进（Q4）完成（方案 `plans/2026-11-19-rename-audit-and-migration.md` 已改 status: completed；实测门禁数字由留痕补记于 NOW.md 与 Engine CHANGELOG）。含旧名的历史文件名不改，git 历史不重写。改名不改变任何项目的功能边界。

## 9. 项目状态词汇（全 Program 统一）

`Active`（主动开发，**任何时刻至多一个**，当前 = Engine）/ `Planned`（已排期未启动）/ `Maintenance`（维护期：仅允许明确范围内的缺陷修复与必要可靠性验证，不扩展功能）/ `Deferred`（冻结/暂缓，成果保留）/ `Blocked`（等待外部条件或人工裁决）/ `Completed`（完成并验收）。
当前：Engine = Active（主线 = embodied-loop-journey 首批 6 课，run 处 EVIDENCE）；Skills 库 = Completed（稳定供应，维护态）；Governance / Radar = Maintenance（2026-11-21 解冻验证后由 Deferred 转入；独立审计 PARTIAL，维护期先修缺陷）；LXD = Engine 内部工作流（Skill 已 active，不独立成仓）。

## 10. 决策依据

- `decisions/PD-003-scope-trim.md`（accepted）：单活跃线 + 冻结其余，是本章程的直接授权来源。
- `decisions/PD-002-physical-consolidation.md`（accepted）：物理集中，2026-11-19 全部完成。
- 用户 2026-11-19 三层重组指令（本文件即其落地）；引导原件见 `references/`。