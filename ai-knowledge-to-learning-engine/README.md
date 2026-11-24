# AI Knowledge-to-Learning Engine — 音视频处理 · 图形渲染 · GPU 工程知识库

> An AI-powered knowledge-to-learning production engine that transforms source materials into structured knowledge, courses, learning materials, practical exercises, and interactive learning experiences.
>
> 一个可重复的知识生产链：原始资料 → 研究 → 证据 → 结构化知识 → 课程 → 教材 → 实验 → 交互式学习站 → 反馈 → KCR 知识更新。

## 当前规模（2026-11-23 实测）

- **83 篇**进入学习站的文档（其中 01–07 主知识文档 **26 篇**，archive **12 篇**只读）
- 术语 **129 条 / 11 组**；概念 **25 个**
- 教材 **20 课 / 8 单元**（19 份课时教材 + L00 地图课）
- 交互实验 **7 个**；pilot 自测 **5 份**
- 证据断言 **84 条 / 来源 43 个**
- 离线站 bundle **3.1 MB**（`web/content.js`）

## 项目定位

**适合**：系统补齐音视频播放、OpenGL/Vulkan、3D 渲染、GPU 性能优化；准备图形/渲染/车载座舱面试；把项目经验整理成可解释、可量化的知识结构。

**不是**：API 手册；跑得起来的工程模板；绝对权威结论（所有数字与平台行为都带验证状态）。

## 核心能力

- **离线学习站**：零外部依赖、双击即开；搜索、章节 TOC、阅读进度、代码复制、KaTeX、Mermaid、明暗主题、上下篇。
- **教材模式**（`C`）：20 课 / 8 单元，前置课时、学习目标、自检、课程地图、进度本地保存。
- **图形实验室**（`L`）：7 个交互实验（MVP / 旋转曲面 / PBR 等），与课时双向关联。
- **术语理解层**（`G`）：129 词，是什么 / 展开 / 为什么重要 / 容易混淆。
- **证据与审核**：claim ledger + source registry + 12 项结构门禁 + G1/G2/G3 人工门。
- **KCR 影响分析**：Source → Claim → Concept → Lesson → Quiz → Course → Website。
- **可恢复运行**：`tools/run_state.py` 十阶段状态机（pause/resume/retry/skip/gate）。

## 快速开始

```powershell
cd C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine

py -3 tools/build_site.py          # 构建学习站（唯一输出 web/content.js）
py -3 tools/validate_site.py       # 12 项结构门禁
py -3 -m http.server 8791 --directory web
# 浏览器打开 http://localhost:8791
```

环境：Python 3（`py -3`），**无第三方依赖**。完整工作流、命令、故障排查、审批方式见 **[docs/USER-GUIDE.md](docs/USER-GUIDE.md)**。

## 文档入口

| 文档 | 内容 |
|---|---|
| [docs/USER-GUIDE.md](docs/USER-GUIDE.md) | 使用指南：项目理解 / 快速开始 / 日常工作流 / 产物 / 审批 / 故障排查 / 提示词 |
| [AGENTS.md](AGENTS.md) | 任何 Agent 的入口（指向 `.agent/`） |
| [WORKFLOW_STATE.md](WORKFLOW_STATE.md) | 当前阶段与续跑点 |
| [DECISIONS.md](DECISIONS.md) | 决策索引（D01–D21） |
| [CHANGELOG.md](CHANGELOG.md) | 逐批执行记录 |
| [reviews/REVIEW_STATUS.md](reviews/REVIEW_STATUS.md) | 审核状态 |
| [00-导航与索引/知识架构总览.md](00-导航与索引/知识架构总览.md) | L0–L7 知识地图与阅读路线 |

## 当前状态

- **P10 端到端验收 done（2026-11-21）**：HDR 批次真实 run 走通 INTAKE→FEEDBACK，四件人工门全过。
- **P10.3 embodied-loop-journey**：首批 6 课已获批准，run 在 RESEARCH（尚未产出教材）。
- **质量门禁**：validate 12/0/0、arc 19/19、publish 11/11、84 claims 误标 0。
- **已知限制**：站点仅本地（在线发布未授权）；单课程工具链；5/19 课有 quiz；反馈为空；学习站混入部分内部文档；artifact hash 会过期。详见 `ai-knowledge-program/AUDIT-REPORT.md`。

## 相关项目

- 统筹层：`../ai-knowledge-program/`（目标、路线图、审计）
- Skills 库：`../matt-pocock-skills-zh-cn/`（通用 Agent 技能）
- 本仓库内部 Skill：`.agent/skills/learning-experience-design/`（学习体验设计）

---

历史细节在 [CHANGELOG.md](CHANGELOG.md)；早期规划与立项文档（Master Prompt / NEXT_PHASE_PLAN / IMPLEMENTATION_PLAN / CURRENT_GAPS / PROJECT_CURRENT_STATE / 工作流设计）已归档至 `archive/process-history/`（2026-11-24 文档治理），仅供历史参考，不作为当前事实源。