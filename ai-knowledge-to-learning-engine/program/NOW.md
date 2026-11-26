---
doc_id: PROG-NOW
type: program-state
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-26
---

# NOW · 当前唯一主目标

> 本文件是带日期的项目级快照，**不是第二事实源**。只保留七项：主项目 / 阶段 / 任务 / 阻塞 / 下一步 / 更新时间 / 关键文件链接。历史明细以 Engine CHANGELOG / DECISIONS / reviews 与 `handoffs/` 为准。
> D22（2026-11-26）后本目录位于核心仓内 `ai-knowledge-to-learning-engine/program/`；Engine 文件链接以 `../` 为根。

## 1. 当前唯一主项目

**AI Knowledge-to-Learning Engine**（核心仓 `ai-knowledge-to-learning-engine/`，GitHub `Vin535LFJ/ai-knowledge-to-learning-engine`）。**D22 统一收敛已执行**：五项目 → 两仓（核心仓 + 独立 Skills 来源库 `matt-pocock-skills-zh-cn`）。Program 并入 `program/`、Radar 并入 `integrations/github-radar/`、Governance 归档 `legacy/`；原三个本地仓移入备份区 retired/（bundle 恢复验证 PASS）。LXD 保持 Engine 内部 Skill。

## 2. 当前阶段

**人工验收与稳定化阶段。** 主线仍是 embodied-loop-journey 首批 6 课，run `RUN-2026-11-23-embodied-batch1` 停在 **REVIEW / paused，等待用户裁决**。上一主目标 P1 已于 2026-11-21 达成；D22 整合与 P0 质量收口（多课程切换 + 检查点练习）已于 2026-11-26 完成并浏览器实测。

## 3. 当前任务

1. **用户完成六课裁决**。材料：`../reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`（G1 V68–V88 共 21 条、G2 六课评分表、专项复核、审批登记顺序）。裁决栏全部留空；AI 没有升级断言、没有填分。
2. **PD-Q 待决清单逐项裁决**（`decisions/PENDING_DECISIONS.md`）：活跃项 PD-Q3/Q4/Q9/Q11/Q15/Q16；PD-Q12/Q14 因 Governance 已归档转为非活跃（如重新启用再议）。

> 已收口（不再是当前任务）：D22 整合产物已分组提交并推送（核心仓 HEAD `67ac3ec`、Skills `d6fa00f`，ls-remote 核实一致）；Skills 过时文档修复已随 `d6fa00f` 完成；**视频 pilot 课程上下文缺陷已修复**（路由/下一课/返回链贯穿 `?c=`，3 个浏览器回归场景通过，证据 `../reviews/consolidation-qa-pilot-context-20261126.json`）。

## 4. 阻塞问题（需人工，AI 不自批）

- **embodied 四件人工门**：G1（V68–V88 是否升级）→ G2（六课评分，基于修复后版本）→ 登记审批 + G3 → KCR。run 无法被 AI 推进。
- **待裁决清单**：PD-Q9 至 PD-Q16（`decisions/PENDING_DECISIONS.md`）；其中 **PD-Q16 公开仓内部材料可见性**只能由用户在 GitHub Settings 操作（本机无 gh/API 凭据）。
- **Skills 全新会话验证未做**（会话重建后发现/加载/执行均成功，全新会话未测）。

## 5. 下一步

1. 用户读验收包，填 G1 裁决栏与 G2 评分。
2. AI 按裁决更新台账与课文状态说明，重建并跑门禁，报结果。
3. 用户确认文件不再改动后：登记审批 → G3 → KCR → resume → PUBLISH（本地口径，D02 约束在线发布）→ FEEDBACK → done。
4. 穿插：Skills 全新会话确认；PD-Q 活跃项逐项裁决（Q3/Q4/Q9/Q11/Q15/Q16）。

## 6. 最近状态更新时间

**2026-11-26 19:30**（外部审核定点修复批次：视频 pilot 课程上下文缺陷修复 + 3 浏览器回归通过；文档治理收口——NOW/PENDING 关闭 Q10/Q13/Q17、Q12/Q14 转非活跃，REQUIREMENT-COVERAGE/FINAL-ACCEPTANCE/README 数字与课时口径更正，Radar README/AGENTS 改为内部模块口径，验收包版本说明更正为 ecab4b9）。D22 统一收敛已于本日 earlier 完成（备份 6/6 PASS、三仓并入、多课程切换 + quiz 上线）。逐日明细以 Engine `../CHANGELOG.md` / `../WORKFLOW_STATE.md` 为准。

## 7. 关键状态文件链接

- 整合决策与证据：[../docs/consolidation/TARGET-ARCHITECTURE.md](../docs/consolidation/TARGET-ARCHITECTURE.md) · [../docs/consolidation/ASSET-INVENTORY.md](../docs/consolidation/ASSET-INVENTORY.md) · [../docs/consolidation/MIGRATION-MAP.md](../docs/consolidation/MIGRATION-MAP.md)
- 稳定化验证报告：[plans/2026-11-25-stabilization-verification.md](plans/2026-11-25-stabilization-verification.md)
- 章程与边界：[PROGRAM.md](PROGRAM.md) · 阶段规划：[ROADMAP.md](ROADMAP.md) · 暂缓登记：[PARKING-LOT.md](PARKING-LOT.md) · PM 规则：[PROGRAM-MANAGER.md](PROGRAM-MANAGER.md)
- 待决：[decisions/PENDING_DECISIONS.md](decisions/PENDING_DECISIONS.md) · 文档导航：[PROJECT-DOCUMENTATION-INDEX.md](PROJECT-DOCUMENTATION-INDEX.md)
- 审计：[AUDIT-REPORT.md](AUDIT-REPORT.md) · [final-acceptance-2026-11-21.md](final-acceptance-2026-11-21.md) · [audits/](audits/)
- Engine 权威状态：`../WORKFLOW_STATE.md` / `../DECISIONS.md`（D22）/ `../reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md` / `../reviews/approvals/README.md`
- 交接索引：[handoffs/README.md](handoffs/README.md)