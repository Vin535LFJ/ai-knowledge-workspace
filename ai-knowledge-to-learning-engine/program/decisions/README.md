---
doc_id: PROG-DECISIONS-README
type: decision-index
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# 程序级决策（PD）

只记录**跨项目/程序级**的长期决策（MADR 风格，精简版）。单项目内部决策留在该项目：
Engine（`ai-knowledge-to-learning-engine`，旧名 Render_Notes）→ `DECISIONS.md`（D01–D21+）+ `.agent/decisions/`（ADR-0001…）；其余项目 → 各自 decisions。

| 编号 | 标题 | 状态 |
|---|---|---|
| PD-001 | 建立统筹 Program：索引而非迁移 | accepted（2026-11-19）；位置策略被 PD-002 取代 |
| PD-002 | 四项目物理集中到 AI-Knowledge 父文件夹 | accepted（2026-11-19 用户指令）；**全部迁移完成**（含 01 Render_Notes，2026-11-19 收尾） |
| PD-003 | 范围裁剪：单活跃线 Engine + 冻结其余 | **accepted**（2026-11-19 用户批准 PD-Q7；Q1/Q2/Q8 已执行） |

待裁决清单：`PENDING_DECISIONS.md` 为 PD-Q 系列裁决存档（Q1/Q2/Q5/Q7/Q8 已执行；Q6 顺延后被 2026-11-21 六阶段计划覆盖，试点 A 已执行）。**当前活阻塞见 `../NOW.md`（embodied 首批 G1 核验队列 + 人工积压）；活跃待决项 PD-Q4/Q9/Q11/Q15 见 `../PARKING-LOT.md` 与 `PENDING_DECISIONS.md`（PD-Q3 已被 D22 取代，Q10/Q13/Q17 已关闭，Q12/Q14 非活跃；Q16 已于 2026-11-27 裁决——两仓先设 Private 再整理公开边界，待用户执行）。** 未回复不视为同意。
普通实现任务不建 PD，走变更提案/任务清单。