---
doc_id: AUDIT-20261124-LOCAL
type: audit
status: archived
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# 本机逐项核实结果（2026-11-24 会话实测）

> 对 GPT 审计报告关键论断的只读核实。口径：**属实 / 过时 / 不精确 / 未验证**。
> 本文件是历史核实记录；后续变化见 AUDIT-DISPOSITION.md 与 Engine CHANGELOG。

| GPT 论断 | 核实结果 | 性质 |
|---|---|---|
| ROADMAP 仍写"kickoff 待批" | ROADMAP.md L17/L22 确为 ⬜ 待批 | 属实（当时统筹层遗漏，后已修） |
| PROGRAM 仍写 Governance/Radar"冻结" | L52/53/67/68 仍是"冻结 MVP" | 属实（后已改为维护期口径） |
| PROGRAM-MANAGER 有旧路径 | L37 `Render_Notes/.agent/README.md`；L96"冻结项目" | 属实（后已修） |
| 历史待决事项没同步裁决 | PD-Q5 裁决栏空白（D17–D19 实际已决）；PD-Q3/Q4 挂"待批" | 属实（PD-Q5 后按 D17–D19 精确回填；Q3/Q4 保持待决） |
| PROGRAM"仍有旧仓库名称" | 剩余 Render_Notes 仅在改名说明与历史记录 | 不精确：真正过期的是"冻结"标注 |
| Engine 发布清单 advisory-only，含 DECISIONS/CHANGELOG/WORKFLOW_STATE | 属实；站点包 92 篇含 6 篇内部文档 | 属实（2026-11-24 TASK 2 发布边界 v2 强制化已修） |
| 站点包混入 G2 审核材料 | reviews/ 已排除；但 courses/video-rendering-journey/G2-审核材料-P6.md 在课程目录内进站 | 部分属实（后 git mv 至 reviews/） |
| Radar analyze 覆盖人工状态 | storage.py L340–345 冲突更新连人工字段一起覆盖 | 属实（P0-A 已修，58 测试覆盖） |
| Radar --approved 不写人工批准字段 | export.py L101–102 只改 review_status | 属实（P0-B 已修） |
| 独立仓库 docs/USER-GUIDE.md 404 | 属实：当时 Engine 领先 2 笔、Skills 领先 1 笔未 push | 属实（后推送解决，raw 实测 200） |
| 84 断言 / 43 来源 / 183 文档 | 核实当时已为 101/52/195 | 过时（引用审计时点数字） |
| Governance 示例 doctor 失败 / 审批人字符串 / 7/18 哈希失效 | 与本机此前审计一致 | 属实（未重复验证，沿用当时实测） |
| Skills 三条新发现（in-progress 安装命令指旧上游、悬空文档、Node 版本） | 当时未核实 | 未验证（2026-11-26 audit-skills.md 已证实前两条） |

## 当时结论

报告整体可信，主要问题属实；4 处过时或不精确不影响其判断。Program 状态漂移是当时统筹层遗漏，已在后续批次修正。