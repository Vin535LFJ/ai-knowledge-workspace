# AI Knowledge-to-Learning Engine

> An AI-powered knowledge-to-learning production engine that transforms source materials into structured knowledge, courses, learning materials, practical exercises, and interactive learning experiences.
>
> 一个可重复的知识生产链：原始资料 → 研究 → 证据 → 结构化知识 → 课程 → 教材 → 实验 → 交互式学习站 → 反馈 → KCR 知识更新。

**AI Knowledge 项目群的唯一核心仓库**（D22，2026-11-26 统一收敛）：原 Program 统筹层并入 `program/`，GitHub Radar 并入 `integrations/github-radar/`，Governance 工具包归档于 `legacy/`。通用 Skills 来源库保持独立仓 `matt-pocock-skills-zh-cn`。整合决策与证据见 [docs/consolidation/TARGET-ARCHITECTURE.md](docs/consolidation/TARGET-ARCHITECTURE.md)。

## 当前规模（2026-11-26 实测）

- **91 篇**进入学习站的文档（知识目录 01–08、archive 19 篇只读、精选证据/知识模型说明）
- 术语 **129 条 / 11 组**；概念 **33 个**；来源 **52 个**
- **2 门课程 / 25 份课时教材**：主课程 20 课（L00–L19）+ 具身智能 6 课（E01–E06）；另有 5 课 pilot 精选路径
- 交互实验 **7 个**；检查点练习 **11 份 / 38 题**（全部嵌入站点，教材页内可作答）
- 证据断言 **105 条**（24 verified / 74 open / 7 conditional）
- 离线站 bundle **3.1 MB**（`web/content.js`，生成物）

## 项目定位

**适合**：系统补齐音视频播放、OpenGL/Vulkan、3D 渲染、GPU 性能、具身智能闭环；准备图形/渲染/车载座舱面试；把项目经验整理成可解释、可量化的知识结构。

**不是**：API 手册；跑得起来的工程模板；绝对权威结论（所有数字与平台行为都带验证状态）；通用 Agent 平台或文档管理平台（明确不做，见 `program/PARKING-LOT.md`）。

## 核心能力

- **离线学习站**：零外部依赖、双击即开；搜索、章节 TOC、阅读进度、代码复制、KaTeX、Mermaid、明暗主题、上下篇。
- **教材模式**（`C`）：**多课程切换**（主课程 / 具身智能 / pilot 路径），前置课时、学习目标、**检查点练习（选择判分 + 简答参考答案）**、课程地图、进度本地保存。
- **图形实验室**（`L`）：7 个交互实验（MVP / 旋转曲面 / PBR 等），与课时双向关联。
- **术语理解层**（`G`）：129 词，是什么 / 展开 / 为什么重要 / 容易混淆。
- **证据与审核**：claim ledger + source registry + **20 项结构门禁** + G1/G2/G3 人工门 + 审批哈希证据链（`tools/approval_chain.py`）。
- **KCR 影响分析**：Source → Claim → Concept → Lesson → Quiz → Course → Website。
- **可恢复运行**：`tools/run_state.py` 十阶段状态机（pause/resume/retry/skip/gate/依赖前沿与环检查）。
- **外部研究入口**：`integrations/github-radar/`（人工筛选 + 批准门槛，不自动导入知识）。

## 快速开始

```powershell
cd C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine

py -3 tools/build_site.py          # 构建学习站（唯一输出 web/content.js）
py -3 tools/validate_site.py       # 20 项结构门禁
py -3 -m http.server 8791 --directory web
# 浏览器打开 http://localhost:8791（也可直接双击 web/index.html）
```

环境：Python 3（`py -3`），**无第三方依赖**。完整工作流、命令、故障排查、审批方式见 **[docs/USER-GUIDE.md](docs/USER-GUIDE.md)**。

## 目录与文档入口

| 位置 | 内容 |
|---|---|
| [docs/USER-GUIDE.md](docs/USER-GUIDE.md) | 使用指南：理解 / 快速开始 / 工作流 / 产物 / 审批 / 排障 |
| [AGENTS.md](AGENTS.md) | 任何 Agent 的入口（指向 `.agent/` 与项目规则） |
| [program/NOW.md](program/NOW.md) | 项目级当前状态（七字段快照） |
| [program/ROADMAP.md](program/ROADMAP.md) | 路线图与阶段进出条件 |
| [program/decisions/PENDING_DECISIONS.md](program/decisions/PENDING_DECISIONS.md) | 待人工裁决清单 |
| [WORKFLOW_STATE.md](WORKFLOW_STATE.md) | Engine 执行续跑点 |
| [DECISIONS.md](DECISIONS.md) | 决策索引（D01–D22） |
| [CHANGELOG.md](CHANGELOG.md) | 逐批执行记录 |
| [docs/consolidation/](docs/consolidation/) | D22 整合：盘点 / 需求对照 / 架构 / 审计 / 映射 / 验收 |
| [reviews/REVIEW_STATUS.md](reviews/REVIEW_STATUS.md) | 审核状态 |
| [00-导航与索引/知识架构总览.md](00-导航与索引/知识架构总览.md) | L0–L7 知识地图与阅读路线 |

## 当前状态（如实）

- **P10 端到端验收 done（2026-11-21）**：HDR 批次真实 run 走通 INTAKE→FEEDBACK，四件人工门全过。
- **具身智能首批 6 课**：教材/测验/审读/修复/复核完成，run `RUN-2026-11-23-embodied-batch1` 停在 **REVIEW / paused**，等用户 G1（V68–V88）/ G2 / G3 / KCR 裁决。材料：`reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`。
- **质量门禁（2026-11-26 实测）**：validate 20/0/0 · publish 33 项 · arc 两课程 0 FAIL · 105 claims 误标 0 · selftest 16/28/15 · radar 58。
- **已知限制**：站点仅本地（在线发布 D02 未授权）；Radar 摄取端未接通（人工批准后另行立项）；审批人为字符串（无数字签名）；公开仓含内部过程材料（PD-Q16 待用户裁决可见性）。

## 相关仓库

- 通用 Skills 来源库：`../matt-pocock-skills-zh-cn/`（独立仓，37 技能 / 发布 31，双上游同步）
- 本仓库内部 Skill：`.agent/skills/`（research-to-learning、learning-experience-design）
- 原 Program / Governance / Radar 独立仓已退出使用；git 历史备份在 `AI-Knowledge-backups/2026-11-26-consolidation/`（恢复验证 PASS）。

---

历史细节在 [CHANGELOG.md](CHANGELOG.md)；早期规划与立项文档已归档至 `archive/process-history/`，仅供历史参考，不作为当前事实源。