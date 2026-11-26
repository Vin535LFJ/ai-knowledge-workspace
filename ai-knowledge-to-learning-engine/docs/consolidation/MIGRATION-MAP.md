---
doc_id: CONSOL-MIGMAP
type: plan
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# MIGRATION-MAP · 旧目录/旧仓库 → 最终结构映射（D22）

## 1. 目录映射

| 旧位置 | 新位置 | 方式 | 验证 |
|---|---|---|---|
| `AI-Knowledge/ai-knowledge-program/*`（31 个跟踪文件） | 核心仓 `program/*` | 逐文件复制（排除 .git/.zcode） | git hash-object 逐文件 0 差异 |
| `AI-Knowledge/agent-workspace-governance/*`（40 个跟踪文件） | 核心仓 `legacy/agent-workspace-governance/*` | 逐文件复制（排除 .git/__pycache__） | 逐文件 0 差异 |
| `AI-Knowledge/github-project-radar/*`（39 个跟踪文件 + 2 个 ignored .db） | 核心仓 `integrations/github-radar/*` | 复制 + 2 处有意修改（research.py 默认输出锚定模块根；tests 对应断言更新） | 除 2 处有意修改外 0 差异；58 测试 OK |
| 核心仓 `.governance/`（5 文件，双轨注册表残留） | 核心仓 `legacy/governance-engine-adaptation-20261121/` | git mv（保留历史） | validate 20/0/0 |
| 三个原目录（含 .git 与 ignored 数据） | `AI-Knowledge-backups/2026-11-26-consolidation/retired/` | Move-Item（**不删除**） | HEAD 实测 ba35e4a / 7d9a187 / e2815d9 完好 |
| 工作区根 `README.md`（快照导航） | 原地更新为最终两仓导航 | 编辑 | — |

## 2. 仓库映射

| 旧仓 | 最终去向 | 远端 |
|---|---|---|
| ai-knowledge-to-learning-engine（43 笔） | **核心仓本体**（保留历史，不重建、不再重写作者） | Vin535LFJ/ai-knowledge-to-learning-engine（沿用） |
| matt-pocock-skills-zh-cn（142 笔） | **独立 Skills 来源库**（保留） | Vin535LFJ/matt-pocock-skills-zh-cn（沿用） |
| ai-knowledge-program（18 笔，本地） | 退出使用；历史在 bundle + retired/ | 无远端（从未建） |
| agent-workspace-governance（6 笔，本地） | 退出使用；源码归档 legacy/ | 无远端 |
| github-project-radar（5 笔，本地） | 退出使用；模块在 integrations/ | 无远端 |
| ai-knowledge-workspace（快照，2 笔） | 更新为最终结构快照 | Vin535LFJ/ai-knowledge-workspace（沿用；归档由用户操作） |

## 3. 备份清单（恢复验证 6/6 PASS）

位置：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge-backups\2026-11-26-consolidation\`

每仓：`history.bundle`（--all，bundle verify 通过）+ `manifest-sha256.json` + `repo-state.json`（HEAD/分支/stash/remotes/tags）+ `ignored-data/`（runs JSON ×2、memory ×5、.db ×2、.zcode 草稿 ×2）。
恢复验证：从 bundle 克隆（core.autocrlf=false）→ HEAD 一致 + tree 一致 + git 归一化 blob 哈希逐文件 0 差异。
注意：全局 core.autocrlf=true 导致工作树 CRLF 差异属预期，**tree/blob 级一致才是内容保真判据**。

## 4. 引用更新

- 核心仓 AGENTS.md：新增 program/ / integrations/ / legacy/ / docs/consolidation 指针。
- program/NOW.md：Engine 链接改 `../` 相对根。
- integrations/github-radar/INTEGRATION.md：新运行命令（从 Engine 根）。
- legacy/README.md：归档说明 + 恢复方法。
- 历史文档中的旧路径/旧 SHA **不改写**（保留来源与时间点），现行指针已更新。

## 5. 提交分组建议（Phase 6 执行）

1. `chore: D22 备份与资产并入`（program/ legacy/ integrations/ 复制 + .governance git mv + .gitignore）
2. `feat: 多课程切换与检查点练习`（build_site quizzes payload + app.js + styles.css + 注册表 site-data ×11 + validate e1b + 回归测试）
3. `feat: run_state 依赖前沿与环检查`（run_state.py + selftest 28）
4. `docs: D22 文档治理`（README/AGENTS/NOW/ROADMAP/PROGRAM/索引/审计档案/consolidation 文档/USER-GUIDE）
5. Skills 仓单独一笔：过时文档修复。