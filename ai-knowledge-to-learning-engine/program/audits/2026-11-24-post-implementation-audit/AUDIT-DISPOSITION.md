---
doc_id: AUDIT-20261124-DISP
type: audit
status: archived
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# 审计发现处置状态（截至 2026-11-26 D22 整合）

| 发现 | 处置 | 证据 |
|---|---|---|
| Program 状态漂移（ROADMAP/PROGRAM/PM/PENDING） | **已修**（2026-11-24 TASK 1，Program 91cf844；D22 后随并入核心仓 program/） | Engine DECISIONS 与 program/ 现文 |
| 发布边界 advisory-only | **已修**（2026-11-24 TASK 2 发布边界 v2：默认拒绝 + build/validate 双侧强制 + 32→33 回归测试） | tools/publish_boundary.py、test_publish_boundary.py |
| G2-审核材料-P6.md 混入课程目录 | **已修**（git mv 至 reviews/，保留历史） | Engine git 历史 |
| Radar analyze 覆盖人工状态 / --approved 不写批准字段 | **已修**（P0-A/P0-B，58 测试；真实库副本验证通过） | integrations/github-radar/（D22 并入）、2026-11-25 稳定化报告 |
| Governance 示例 doctor 失败 | **已修**（示例类型错误修正，41 测试，doctor exit 0）；真实 Engine 纳管边界问题经 D22 审计确认为设计级不兼容 → **Governance 整仓归档**，不再接入 | legacy/README.md、docs/consolidation/audit-governance.md |
| 审批人字符串 / 历史哈希失效 | **部分缓解**：审批哈希证据链（approval_chain）已上线，历史批准如实标 legacy/unverifiable；审批人身份验证仍无（如实声明，非数字签名） | tools/approval_chain.py、reviews/approvals/README.md |
| USER-GUIDE 远程 404 | **已修**（推送后 raw 实测 200） | 2026-11-24 TASK 0 回执 |
| Skills 过时文档（14/7 旧数字、上游安装命令、悬空文档、失效 SHA 锚点） | **待修**（D22 本轮列入 Skills 维护批次） | docs/consolidation/audit-skills.md §6 |
| 公开仓内部材料可见性 | **待用户裁决**（PD-Q16；本机无 gh/API 凭据，只能用户在 GitHub Settings 操作） | program/decisions/PENDING_DECISIONS.md |

> 原审计结论不改写；本表只记录后续处置。未列项以原报告与 LOCAL-VERIFICATION 为准。