---
doc_id: REV-README
type: review-material
status: active
owner: qwenwork
created: 2026-11-24
updated: 2026-11-24
---

# reviews/ 导航与历史标注

> 治理与审核材料目录：**不进学习站 bundle**（publish_boundary 排除），但被 document-registry 索引。
> 2026-11-24 文档治理：本 README 为目录导航；历史材料只标注、不改写、不移动（大量交叉引用保持原路径）。

## 目录结构

| 位置 | 性质 | 状态 |
|---|---|---|
| `decision-kit/` | 七项人工裁决材料（B4/B10/B11/B12/B15/V13/V14） | ✅ 全闭合（D17–D19，2026-11-19）；B12 stash 处置待重议 |
| `p10/` | P10 HDR 批次端到端验收全套（intake/研究/G1 队列/KCR 提案/人工门指引/发布与反馈记录） | ✅ run done（D20，2026-11-21） |
| `embodied-batch1/` | embodied-loop-journey 首批（当前主线） | 🔄 RESEARCH 进行中 |
| `kcr/` | KCR 工具说明与影响分析样本（含对齐前历史冒烟工件，保留不改写） | 活跃工具文档 |
| `G2-L02…L19-deepening.md` | 逐篇教材人工评分材料（18 份） | L19 已评 91 分；L02–L18 共 17 篇待用户评分 |
| `P8-KCR-kickoff.md` / `P9-orchestrator-design.md` | P8/P9 启动检查点与设计稿 | ✅ 已执行完，转历史参考 |

## Loop 1 历史材料（2026-11-18/19，使命已完成）

以下文件为 V3-Loop1 审核准备产物，**历史参考，不再是当前事实源**；当前审核状态以 `REVIEW_STATUS.md` 与 Program `NOW.md` 为准：

- `CURRENT_AUDIT.md` — P6 后真实状态审计（V3.0 基线）
- `DECISION_REQUIRED.md` — 当时待裁决清单（后续裁决见 decision-kit/ 与 DECISIONS.md D17–D21）
- `EXECUTION_PLAN_V3.md` — V3 执行计划（P7–P10 已完成）
- `G1-evidence-review.md` / `G2-curriculum-review.md` / `G3-release-readiness.md` — Loop 1 三门材料（后续批次各有专属材料）
- `KNOWLEDGE_CHANGE_REVIEW.md` — KCR 流程设计（已由 tools/kcr/ 实现落地）

## 使用原则

1. 历史材料中的数字/状态为当时快照，与现状冲突时以实测与当前权威文档为准（D08）。
2. 人工关卡材料（G1/G2/G3、decision-kit）的裁决栏只能由用户填写，AI 不自批。
3. 新增批次材料按 `reviews/<批次名>/` 组织（先例：p10/、embodied-batch1/）。