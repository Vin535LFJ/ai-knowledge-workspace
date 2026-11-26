---
doc_id: CONSOL-INVENTORY
type: audit
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# ASSET-INVENTORY · 五项目资产盘点（2026-11-26 实测）

> Phase 0 交付。所有数字来自当日本机实测（git / 门禁 / 只读审计），不沿用历史报告。
> 三份只读审计全文：`audit-governance.md` / `audit-radar.md` / `audit-skills.md`（本目录）。
> 备份与恢复验证：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge-backups\2026-11-26-consolidation\backup-report.json`（6/6 PASS）。

## 1. Git 与远端状态（盘点时点）

| 仓 | HEAD | 提交数 | 分支 | 工作树 | stash | tags | remote |
|---|---|---|---|---|---|---|---|
| ai-knowledge-program | ba35e4a | 18 | master | 干净 | 0 | 无 | **无（本地仓）** |
| ai-knowledge-to-learning-engine | 3062b4a | 43 | master | 干净 | **1（B12 用户手改，原样保护）** | 无 | Vin535LFJ/ai-knowledge-to-learning-engine（Public，已同步） |
| matt-pocock-skills-zh-cn | 4e01df4 | 142 | main | 干净 | 0 | v1.1.0/v1.2.3/v1.3.1（指向作者重写前孤儿历史，README 已注记） | Vin535LFJ/matt-pocock-skills-zh-cn（Public，已同步） |
| agent-workspace-governance | 7d9a187 | 6 | master | 干净 | 0 | 无 | 无 |
| github-project-radar | e2815d9 | 5 | master | 干净 | 0 | 无 | 无 |
| （快照）ai-knowledge-workspace | 632fd5b | 2 | main | 干净 | 0 | 无 | Vin535LFJ/ai-knowledge-workspace（Public，扁平快照，无子仓历史） |

## 2. 不可再生 ignored 资产（已全部备份）

| 仓 | 文件 | 性质 |
|---|---|---|
| Engine | `.agent/runs/RUN-2026-11-20-p10-hdr.json`、`RUN-2026-11-23-embodied-batch1.json` | 运行态证据（18/24 artifacts 哈希链），D15 本地 only |
| Engine | `.workbuddy-ai/memory/2026-11-17/18/19.md` | Agent 工作日志 |
| Skills | `.workbuddy-ai/memory/MEMORY.md`、`2026-10-09.md` | 本地记忆（含旧 slug 与"只发布 14"过时硬约束，见审计 §6-b） |
| Radar | `radar-real-20261121.db`（121 仓/200 快照/121 候选）、`radar-real-hdr.db`（空壳） | 真实采集数据，旧 schema（无 approver 列） |
| Program | `.zcode/workflow-drafts/`（2 文件） | 宿主工作流草稿 |

可再生（不备份）：node_modules、site-vitepress/docs 与 dist/.temp/cache、__pycache__、sidebar.generated.*。

## 3. 整合表（Keep / Merge / Embed / Archive / Remove / Not implemented）

| 原项目 | 实际价值 | 已实现能力（证据） | 尚未实现 | 重复能力 | 最终去向 | 处理动作 |
|---|---|---|---|---|---|---|
| **Engine** | 核心产品，唯一真实跑通端到端生产链 | 知识目录 01–08、Source Registry 52、Claim Ledger 105（24v/74o/7c）、Concept/Glossary、2 课程 25 课、7 实验、离线站（91 docs）、run_state 十阶段+审批哈希链、KCR 五契约、发布边界 v2 强制（32 测试）、validate 20 检查、LXD 内部 Skill（2 真实案例） | 在线发布（D02 未授权）；Radar 摄取端；多课程 UI 切换与 quiz 呈现（本轮 P0 修复） | — | **核心仓本体**（保留现有 git 历史与远端） | Keep |
| **Program** | 项目级管理层，18 笔决策/审计/交接记录 | PROGRAM/NOW/ROADMAP/PARKING-LOT/PENDING_DECISIONS、PD-001~003、D17–D21 指针、审计报告×2、稳定化验证报告、handoffs | 无独立代码；其"管理"全部是文档 | 与 Engine WORKFLOW_STATE/CHANGELOG 的状态描述部分重叠（Phase 4 去重） | 核心仓 `program/` 目录 | **Merge**（内容并入，原仓 bundle 归档后退出） |
| **Governance** | 通用治理教学/模板仓；对 Engine 无增量 | CLI 1289 行 10 命令、41 测试 OK；ensure_agents_pointer 字节级保护（9 测试）；check_frontier/detect_dependency_cycles 纯函数（6 测试） | schemas 无运行时消费方；audit/archive-check/status/map 无真实数据验证；对 Engine doctor 621/validate 804 项失败（type 枚举零交集+口径冲突，审计 §3） | 15 项能力 9 项 Engine 已覆盖且更强（注册表/单写者/审批/写盘纪律） | 两个纯函数 **Embed** 进 run_state；整仓 **Archive** 至核心仓 `legacy/agent-workspace-governance/`；Engine 内遗留 `.governance/` 双轨注册表移入 legacy | Embed + Archive |
| **Radar** | 外部项目发现模块，契约就绪未接通 | 纯 stdlib 10 子命令、58 测试 OK、rest.py 真实采集、机器/人工字段分离+批准幂等（P0 已修）、导出契约 15 字段 | Engine 摄取端（grep research-intake 0 命中）；真实库 human_selected=0；趋势跟踪（快照仅 20 秒窗口，insufficient_history 如实标记） | 无（Engine 无同类能力） | 核心仓 `integrations/github-radar/`（修 3 处路径假设；.db 保持 ignored 本地数据，schema 升级仍待 PD-Q15） | **Embed** |
| **Skills 库** | 独立发行与维护层 | 37 技能（发布 31）、4 处上游回填、双上游同步流程、2 校验脚本 exit 0、QwenWork 2 技能部分验证（会话重建后全链路） | 其余 35 技能/其他宿主运行时验证；npx 安装器本机 Node 20 不可测 | 与 Engine 内部 2 技能零重复 | **保留独立仓**（独立上游同步+版本+多客户端分发理由成立） | Keep（修过时文档，见审计 §6） |
| LXD | Engine 内部质量规范 | SKILL active、L13+transform-mvp 两案例、Floor 脚本、七实验对比度修复回归 | 其余 6 实验的目标/观察记录块（PD-Q9 待决） | — | 已在 Engine `.agent/skills/` | Keep |
| 快照仓 | GPT/专家复核入口 | 632fd5b 扁平快照 | 无子仓历史 | 与五仓内容重复（有意） | 整合后更新为最终结构快照；远端归档由用户在 GitHub 操作 | Merge（内容更新） |

**Not implemented（仅设计，不进最终产品）**：统一 Skills Registry、MCP/Tools Registry、通用 Orchestrator、Agent Control Center、多项目调度平台、大型 Dashboard、通用文档管理平台（PARKING-LOT 已登记，维持不做）。

## 4. 项目间引用与依赖

- Engine → Skills：无代码依赖；用户级安装 handoff/writing-for-agents 互补（审计 skills §5）。
- Engine → Radar：仅导出契约文档；无消费代码（本轮不新建摄取端，保持"契约就绪、人工接通"现状）。
- Engine → Governance：遗留 `.governance/`（183 条过时注册表、三空注册表）= 双轨治理残留，本轮清除。
- Program → 各项目：纯文档指针；合并后指针改相对路径。
- OmniWorld-Engine（工作区外）：skills-lock 已指新 slug，只读不动。

## 5. 当前阻塞与未完成（如实）

1. **embodied 六课人工验收**：run REVIEW/paused；G1（V68–V88 共 21 条）/G2/G3/KCR 全部等用户。材料齐备（USER-ACCEPTANCE-PACKAGE.md，方案甲修复后版本）。
2. PD-Q9~Q16 待决清单（Program decisions/PENDING_DECISIONS.md）。
3. 真实 Radar 库 schema 升级（PD-Q15）；公开仓内部材料边界（PD-Q16）。
4. Skills 全新会话验证、其余宿主验证。