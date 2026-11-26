---
doc_id: CONSOL-DECISIONS
type: adr
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# CONSOLIDATION-DECISIONS · 合并/保留/归档/删除决定及原因（D22）

> 决策记录入口在 Engine `DECISIONS.md` D22；本文件是逐项明细。依据：三份只读审计（本目录）+ 当日实测。

| # | 对象 | 决定 | 原因（证据） |
|---|---|---|---|
| 1 | 五仓结构 | **方案 B：核心仓 + 独立 Skills 库** | Governance 对 Engine 零增量（15 项能力 9 项已覆盖且更强）；Radar 无独立发布需求；Skills 有独立上游同步/版本/多客户端分发实证（audit-skills §5）。A 方案绑架 Skills 发布节奏，C 方案维持无独立生命周期的仓。 |
| 2 | 核心仓身份 | **沿用现仓现远端，不重建、不再重写作者** | 任务书 §7.3 明确保持已完成的 GitHub 身份处理；43 笔历史与远端同步状态有价值；重建无收益。 |
| 3 | Program | **Merge → program/** | 纯文档管理层，无独立代码；为 4-5 个管理文件维护独立仓不合理（任务书 §3.1）。18 笔历史 bundle 保存。 |
| 4 | Governance | **Archive → legacy/ + Embed 两个纯函数** | type 枚举与 Engine 零交集（设计级不兼容）；唯一真实空白=依赖前沿/环检测 → check_frontier/detect_dependency_cycles 并入 run_state（28 测试）。整仓归档保留 41 测试与诚实缺陷清单的教学价值。 |
| 5 | Engine .governance/ 残留 | **git mv → legacy/** | 双轨注册表违反"一个门禁一处维护"（D04/D07）；183 条过时条目 + 三空注册表无消费方。 |
| 6 | Radar | **Embed → integrations/github-radar/** | 纯 stdlib、58 测试、人工批准门槛代码强制；平移成本低（3 处路径修正）。保持小型研究入口，不建调度/自动采集。 |
| 7 | Radar 真实 .db | **保持 ignored 本地数据，不升级 schema** | 升级需用户批准（PD-Q15）；副本验证已通过；数据随模块平移并备份。 |
| 8 | Radar 摄取端 | **有意不实现** | human_selected=0，无真实可导入任务；接通需人工批准候选后另行立项（任务书：不建没有真实使用需求的功能）。 |
| 9 | Skills 库 | **Keep 独立** | 双上游同步机制 + 4 处回填 + 37/31 发行 + 多客户端打包；与 Engine 内部技能零重复。 |
| 10 | Skills 过时文档 | **本轮修复** | audit-skills §6 c/d/f/g：旧数字 14/7、上游安装命令、失效 SHA 锚点、悬空文档。tag 孤儿问题**不再重写**（任务书禁止），README 注记保持。 |
| 11 | LXD | **Keep 内部** | 两真实案例 + Floor 门禁有效；不独立成仓（任务书 §3.3）。 |
| 12 | 多课程切换 + quiz | **本轮实现（P0）** | bundle 无 quiz payload、教材模式仅主课程 = 真实学习缺陷（任务书 §5.5/Phase 3 P0-6）。最小实现：courses[] 已有 payload 复用 + quizzes site-data 嵌入 + 课程切换条 + 练习交互；浏览器实测通过。 |
| 13 | 旧目录删除 | **不删除，移入备份区 retired/** | 任务书 §7.1：备份可恢复验证通过前不得删除；移入备份区后工作区只留两仓，无重复副本。 |
| 14 | 远端删除/归档 | **本轮不执行** | 无 gh/API 凭据；快照仓更新为最终结构；归档/删除由用户在 GitHub 操作（条件清单见 TARGET-ARCHITECTURE §8）。 |
| 15 | 公开边界 | **维持既有公开状态 + 显式待决** | PD-Q16 未裁决；不擅自扩大公开面（新增内部目录全部排除出学习站；.db/runs/memory 不入库）；转 Private 需用户操作。 |
| 16 | 11-24 审计档案 | **补做** | ROADMAP 悬空指针；原报告原文保存 + 本机核实 + 处置表（program/audits/）。 |

## 明确不做（本轮与既有裁决一致）

独立 Knowledge Repository / Skills Registry / MCP-Tools Registry / 通用 Orchestrator / Control Center / 调度平台 / 大型 Dashboard / 通用文档管理平台 / 在线自动发布 / 自动审批 / 全面重写 19 篇旧教材 / 全面重设计 7 个实验。