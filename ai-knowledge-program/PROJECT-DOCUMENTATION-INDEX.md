---
doc_id: PROG-DOC-INDEX
type: doc-index
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
---

# 全项目文档导航（PROJECT-DOCUMENTATION-INDEX）

> 从一个文件进入全部项目的使用文档。所有链接均为相对本文件（`ai-knowledge-program/`）的路径，已于 2026-11-23 逐条检查存在性。
> 想看「项目现在到底怎么样」，先读 [`AUDIT-REPORT.md`](AUDIT-REPORT.md) 与 [`POST-AUDIT-SUMMARY.md`](POST-AUDIT-SUMMARY.md)。

## 1. 总览

| 项目 | 使用指南 | 快速开始 | 技术文档 | 测试说明 | 当前状态 |
|---|---|---|---|---|---|
| AI Knowledge Program | [USER-GUIDE.md](USER-GUIDE.md) | §4 启动 PM / §6 查状态 | [PROGRAM.md](PROGRAM.md) · [PROGRAM-MANAGER.md](PROGRAM-MANAGER.md) · [ROADMAP.md](ROADMAP.md) | 无自动化（文档层） | 审计 **PASS WITH LIMITATIONS** |
| AI Knowledge-to-Learning Engine | [docs/USER-GUIDE.md](../ai-knowledge-to-learning-engine/docs/USER-GUIDE.md) | §2 Quick Start | [AGENTS.md](../ai-knowledge-to-learning-engine/AGENTS.md) · [DECISIONS.md](../ai-knowledge-to-learning-engine/DECISIONS.md) · [WORKFLOW_STATE.md](../ai-knowledge-to-learning-engine/WORKFLOW_STATE.md) | 指南 §2.5 + §6 | 审计 **PASS WITH LIMITATIONS**；P10 done |
| Matt Pocock Skills 中文发行版 | [docs/USER-GUIDE.md](../matt-pocock-skills-zh-cn/docs/USER-GUIDE.md) | §6 安装 / §7 验证发现 | [SYNC.md](../matt-pocock-skills-zh-cn/SYNC.md) · [BACKPORTS.md](../matt-pocock-skills-zh-cn/BACKPORTS.md) · [AGENT-COMPATIBILITY.md](../matt-pocock-skills-zh-cn/AGENT-COMPATIBILITY.md) | 指南 §11（check-translation / audit-english） | 审计 **PASS WITH LIMITATIONS**；37 技能维护态 |
| Learning Experience Design | [USAGE.md](../ai-knowledge-to-learning-engine/.agent/skills/learning-experience-design/USAGE.md) | §7 标准流程 | [SKILL.md](../ai-knowledge-to-learning-engine/.agent/skills/learning-experience-design/SKILL.md) · `references/` | 指南 §10/§12（Floor + build/validate） | 审计 **PASS WITH LIMITATIONS**；1 个真实试点 |
| Agent Workspace Governance | [docs/USER-GUIDE.md](../agent-workspace-governance/docs/USER-GUIDE.md) | §4 init / §15 迁移 | [README](../agent-workspace-governance/README.md) · [specification](../agent-workspace-governance/docs/specification.md) · [architecture](../agent-workspace-governance/docs/architecture.md) | 指南 §13（28 tests） | 审计 **PARTIAL** |
| GitHub Project Radar | [docs/USER-GUIDE.md](../github-project-radar/docs/USER-GUIDE.md) | §7 首次运行 | [data-model](../github-project-radar/docs/data-model.md) · [engine-interface](../github-project-radar/docs/engine-interface.md) · [operating-guide](../github-project-radar/docs/operating-guide.md) | 指南 §7 + §19 | 审计 **PARTIAL** |

## 2. 审计与验收

| 文档 | 内容 |
|---|---|
| [AUDIT-REPORT.md](AUDIT-REPORT.md) | 六阶段独立审计：结论、证据、偏差、P0–P3 建议 |
| [POST-AUDIT-SUMMARY.md](POST-AUDIT-SUMMARY.md) | 审计后收口：已生成文档、验证结果、未解决问题、下一步 |
| [final-acceptance-2026-11-21.md](final-acceptance-2026-11-21.md) | 六阶段总验收（历史记录；其中 Radar→Engine 第 4 项已被本次审计更正） |
| [NOW.md](NOW.md) | 当前主目标与最近快照 |
| [ROADMAP.md](ROADMAP.md) | NOW / NEXT / LATER / COMPLETED |

## 3. 按任务找文档

| 我想… | 去这里 |
|---|---|
| 启动一次 AI 会话并恢复上下文 | [Program USER-GUIDE §4/§5](USER-GUIDE.md) |
| 跑一遍 Engine 的构建、门禁、本地站点 | [Engine USER-GUIDE §2](../ai-knowledge-to-learning-engine/docs/USER-GUIDE.md) |
| 生产一篇新教材 | [Engine USER-GUIDE §3.5/§7-B](../ai-knowledge-to-learning-engine/docs/USER-GUIDE.md) |
| 做知识变更影响分析（KCR） | [Engine USER-GUIDE §3.9](../ai-knowledge-to-learning-engine/docs/USER-GUIDE.md) |
| 恢复中断的 Engine 任务 | [Engine USER-GUIDE §3.10/§7-E](../ai-knowledge-to-learning-engine/docs/USER-GUIDE.md) |
| 安装 / 验证 Skills | [Skills USER-GUIDE §6–§8](../matt-pocock-skills-zh-cn/docs/USER-GUIDE.md) |
| 同步上游 / 维护回填 | [Skills USER-GUIDE §11–§12](../matt-pocock-skills-zh-cn/docs/USER-GUIDE.md) |
| 改一个学习页面 | [LXD USAGE §7/§11](../ai-knowledge-to-learning-engine/.agent/skills/learning-experience-design/USAGE.md) |
| 给已有项目接治理 | [Governance USER-GUIDE §15](../agent-workspace-governance/docs/USER-GUIDE.md) |
| 跑一次 GitHub 项目发现与周报 | [Radar USER-GUIDE §7–§14](../github-project-radar/docs/USER-GUIDE.md) |
| 判断某个项目现在能不能用 | [AUDIT-REPORT §B](AUDIT-REPORT.md) + 各指南「已知限制」 |

## 4. 阅读顺序建议

**第一次接触**
1. `PROGRAM.md`（为什么有这个项目群）
2. `AUDIT-REPORT.md` §A（现在到底有什么）
3. `NOW.md`（现在在做什么）
4. 目标项目的 USER-GUIDE

**要动手**
1. 对应项目 USER-GUIDE 的 Quick Start
2. 跑一次测试命令，确认环境
3. 再读「日常工作流」
4. 最后读「已知限制」，避免踩坑

**要交接**
1. `handoffs/` 最新一份
2. `NOW.md`
3. 项目 `WORKFLOW_STATE.md` / `SYNC.md`
4. 本索引

## 5. 文档维护规则

- 每份 USER-GUIDE / USAGE 顶部有 `verified_at` 与 `verified_against`（commit）；改动后更新。
- 命令必须实测；不能实测的写「未验证」。
- 状态结论以 `AUDIT-REPORT.md` 为准；历史验收文档不追改，只在审计报告中标注更正。
- README 只保留简介 / 价值 / 能力 / Quick Start / 文档入口 / 状态 / 链接；详细流程进 USER-GUIDE。

---

**最后验证**：2026-11-23。所有相对路径已逐条 `Test-Path` 检查。
**最近更新**：2026-11-23。