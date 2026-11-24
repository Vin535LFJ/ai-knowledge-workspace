# AI Knowledge Workspace（复核快照）

本仓库是 `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge` 工作区在 **2026-11-24** 的一次性快照，用于外部复核。它不是任何项目的开发主线：五个子目录原本是五个独立 git 仓库，各自的提交历史不包含在这里，权威来源仍是原仓库。

## 目录

| 目录 | 正式名称 | 性质 | 入口文档 |
|---|---|---|---|
| `ai-knowledge-program/` | AI Knowledge Program | 统筹层（不生产内容、不开发功能） | `PROJECT-DOCUMENTATION-INDEX.md`、`NOW.md`、`AUDIT-REPORT.md` |
| `ai-knowledge-to-learning-engine/` | AI Knowledge-to-Learning Engine | 核心产品：原始资料 → 研究 → 结构化知识 → 课程教材 → 实践 → 交互式学习网站 | `README.md`、`docs/USER-GUIDE.md`、`CHANGELOG.md`、`DECISIONS.md` |
| `matt-pocock-skills-zh-cn/` | Matt Pocock Skills 中文定制发行版 | Agent Skills 发行库（上游的中文适配，非上游官方） | `README.md`、`docs/USER-GUIDE.md` |
| `agent-workspace-governance/` | Agent Workspace Governance | 工作区文档治理 CLI（验证阶段） | `README.md`、`docs/USER-GUIDE.md` |
| `github-project-radar/` | GitHub Project Radar | GitHub 项目发现与追踪工具（验证阶段） | `README.md`、`docs/USER-GUIDE.md` |

## 建议阅读顺序

1. `ai-knowledge-program/AUDIT-REPORT.md` — 对五个项目的一次独立审计，含每个项目的结论（通过 / 有条件通过 / 部分完成）与证据索引
2. `ai-knowledge-program/POST-AUDIT-SUMMARY.md` — 审计收口摘要
3. `ai-knowledge-program/PROGRAM.md`、`NOW.md`、`ROADMAP.md`、`PARKING-LOT.md` — 目标、边界、当前状态
4. `ai-knowledge-to-learning-engine/` — 核心产品，文档量最大
5. 其余三个工具项目

## 快照说明

- 包含快照时刻工作区里的全部已版本化文件，以及当时尚未提交的工作内容。
- 已排除：各子仓库的 `.git` 目录、`node_modules`、Python 缓存、站点构建缓存，以及被各仓库 `.gitignore` 忽略的本机文件（运行态 JSON、本机 agent 记忆文件、本地 `.db` 数据库）。
- 因此本仓库里"文件存在"不等同于"已在原仓库提交"；提交状态以原仓库为准。
- 文档中出现的本机绝对路径（`C:\Users\...`）是原作者机器上的路径。
