---
doc_id: ARCH-PROCESS-HISTORY
type: knowledge
status: archived
owner: qwenwork
created: 2026-11-24
updated: 2026-11-24
---

# 过程文档归档（P6 时代）

> 2026-11-24 文档治理：以下六份立项/P6 时期的过程文档自仓库根移入本目录，**内容按原样保留（仅加归档标注），不再更新**。与当前文档冲突时，一律以当前权威文档为准。

## 清单与替代关系

| 文件 | 原职责 | 当前权威替代 |
|---|---|---|
| Master Prompt：构建 AI Knowledge-to-Learning Engine.md | 立项任务书（V2.0/V3.0） | `DECISIONS.md`（裁决萃取）+ Program `PROGRAM.md`/`NOW.md` |
| Render_Notes：从知识库到 AI 原生教学系统的工作流设计.md | 立项工作流设计建议 | `.agent/constitution/` + `DECISIONS.md` |
| PROJECT_CURRENT_STATE.md | 2026-11-18 状态审计基线 | `WORKFLOW_STATE.md` + `reviews/REVIEW_STATUS.md` + Program `NOW.md` |
| CURRENT_GAPS.md | 2026-11-18 缺口清单 | Program `NOW.md` 积压清单 + `ai-knowledge-program/AUDIT-REPORT.md` §E |
| NEXT_PHASE_PLAN.md | P6–P10 实施计划（已执行完） | Program `ROADMAP.md` |
| IMPLEMENTATION_PLAN.md | P6 执行索引 | `DECISIONS.md` + Program `ROADMAP.md` |

## 使用原则

1. 历史参考与追溯用途，不是第二事实源（D08）。
2. 文内提到的根目录相对路径（如 `CURRENT_GAPS.md`）按本目录新位置理解；历史叙述中的旧仓库名 Render_Notes = 现 ai-knowledge-to-learning-engine。
3. 依 D10.4，archive/ 在离线站只读发布；VitePress 与知识校验器排除本目录。