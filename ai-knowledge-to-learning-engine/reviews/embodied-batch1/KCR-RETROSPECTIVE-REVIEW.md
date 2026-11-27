---
doc_id: EMB-B1-KCR-RETRO
type: review-material
status: active
owner: qwenwork
created: 2026-11-27
updated: 2026-11-27
related_run: RUN-2026-11-23-embodied-batch1
---

# KCR 追溯审核 · embodied-loop-journey 首批（提案 KCR-2026-11-002）

> **这是一份追溯性提案，不是先行审批。** 它列出的全部变更都已经应用并推送。整理它的目的，是让 KCR 的人工审核有逐项对象，而不是用一个状态转换代替审核。
> **本文件不包含任何裁决。** 逐项的 approve / reject / request_research 只能由你本人做出。

## 1. 为什么要做追溯审核

KCR 的正式流程是五个阶段：影响分析 → 变更提案 → 人工逐项裁决 → 只应用已批准的项目 → 验证归档。

这次具身六课的实际情况是：变更（新课程、六课教材、21 条断言、11 个来源、8 个概念）在 2026-11-24 至 11-27 之间随 5 笔提交应用；其间 G1 与 G2 已由你裁决并登记。但 `reviews/kcr/` 下没有属于这次 run 的变更提案，也没有人工裁决文件。KCR 子状态停在 REVIEWING。

所以不能把流程伪装成"先批准、后应用"。诚实的做法是：把已发生的变更逐项列出，由你追认或驳回。**驳回某一项意味着要回退或修订对应内容，那本身会产生一次新的变更。**

## 2. Stage 1 · 影响分析（工具产出，11 份）

位置：`reviews/embodied-batch1/kcr/impact-*.json`，由 `tools/kcr_impact.py --source-id <来源>` 生成，全部通过契约校验。

| 来源 | 影响断言 | 影响概念 | 影响课时 |
|---|---:|---:|---:|
| SRC-RL-TEXTBOOK | 17 | 5 | 5 |
| SRC-RL-PRINCIPLES | 4 | 2 | 3 |
| SRC-RL-KB515 | 8 | 4 | 3 |
| SRC-RL-KB516 | 4 | 3 | 2 |
| SRC-RL-OPENLAB | 3 | 0 | 1 |
| SRC-RL-KB-AUX | 3 | 3 | 3 |
| SRC-EXT-TOBIN2017 | 1 | 1 | 1 |
| SRC-EXT-DAGGER2011 | 1 | 1 | 1 |
| SRC-EXT-MUJOCO-MJWARP | 1 | 0 | 1 |
| SRC-EXT-BEVFORMER | 1 | 0 | 1 |
| SRC-EXT-MUJOCO-REPRODUCIBILITY | 1 | 0 | 1 |

工具按来源统计，同一条断言可被多个来源支撑，各行不能相加。

## 3. Stage 2 · 变更提案（机器可读，`human_decision` 为空）

位置：`reviews/embodied-batch1/kcr/change-proposal-embodied-batch1.json`，已通过 Stage 2 契约校验（`validate_kcr.py --stage2`）。逐项内容、证据、条件和"已随哪笔提交应用"都在该文件里。

| 项 | 动作 | 对象 | 摘要 | 已应用 |
|---|---|---|---|---|
| A1 | add | 课程 `embodied-loop-journey` | 独立课程，首批 6 课 | `176d973` 起 |
| A2 | add | 课时 E01–E06 + 测验 + 课源 + 术语 | 六课教材与检查点测验 | `176d973` → `67abc1d` |
| A3 | add | 断言 V68–V88（21 条） | 登记时全部 open/low | `1a70c3a` → `ecab4b9` |
| A4 | add | 来源 11 个 | 课源 6 + 外部权威来源 5 | `1a70c3a` → `ecab4b9` |
| A5 | add | 概念 K-EMB-*（8 个） | 闭环、六环、时间预算、对齐、运动学、雅可比、复合误差、Sim2Real | `176d973` |
| R1–R7 | reverify | V72、V73、V75、V76、V77、V78、V81 | open/low → verified（V73、V78、V81 为 high，其余 medium） | `67abc1d` |
| R8–R13 | reverify | V70、V71、V74、V79、V83、V85 | open/low → conditional（均 medium，附条件） | `67abc1d` |
| M1 | modify | 课时 E01–E06 的状态说明 | 与台账同步，决议内容不变 | `67abc1d` |

R1–R13 就是你 2026-11-27 的 G1 裁决（记录 G1-01）。KCR 追溯审核与 G1 的关系：G1 裁的是"这些断言现在该是什么状态"，KCR 审的是"这批知识变更作为一个整体是否成立"。两者对象重叠，但不是同一个决定。

## 4. Stage 3 · 人工逐项裁决（留空）

对每一项选择一个：**approve**（追认）/ **reject**（需回退或修订，将产生新变更）/ **request_research**（需补证据后再议）。

| 项 | 你的裁决 | 备注 |
|---|---|---|
| A1 课程 | | |
| A2 六课与测验 | | |
| A3 断言 V68–V88 | | |
| A4 来源 11 个 | | |
| A5 概念 8 个 | | |
| R1 V72 → verified | | |
| R2 V73 → verified | | |
| R3 V75 → verified | | |
| R4 V76 → verified | | |
| R5 V77 → verified | | |
| R6 V78 → verified | | |
| R7 V81 → verified | | |
| R8 V70 → conditional | | |
| R9 V71 → conditional | | |
| R10 V74 → conditional | | |
| R11 V79 → conditional | | |
| R12 V83 → conditional | | |
| R13 V85 → conditional | | |
| M1 状态说明同步 | | |
| **总体** | | |

裁决人：____________　日期：____________

可以把裁决直接写在上表，或口头告诉我、由我按原话代录（代录会如实标注）。机器契约在 `tools/kcr/schema/review-decision.schema.json`。

## 5. Stage 4 与 Stage 5（裁决之后）

- **只应用已批准的项目。** 由于变更已经应用，"应用"在这里的实际含义是：驳回的项进入回退或修订，其余保持现状。
- 全部裁决完成后，才执行 KCR 状态转换（`run_state.py kcr --to APPROVED --approver <你的署名>`），并补登变更历史与来源追溯。
- 这一步**没有代理代执行的授权**。代理只准备材料。

## 6. 本文件没有核实的内容

- 各项"已应用"的提交号取自 `git log -S <标识>` 的首见提交（实测），没有逐文件比对每笔提交的完整 diff。
- 11 份影响分析的数字是工具按当前台账计算的结果，没有人工逐条复核。
