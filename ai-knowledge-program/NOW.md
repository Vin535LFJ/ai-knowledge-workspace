---
doc_id: PROG-NOW
type: program-state
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-26
---

# NOW · 当前唯一主目标

> 本文件是带日期的项目级快照，**不是第二事实源**。只保留七项：主项目 / 阶段 / 任务 / 阻塞 / 下一步 / 更新时间 / 关键文件链接。历史明细以各项目 CHANGELOG / DECISIONS / reviews 与 `handoffs/` 为准。

## 1. 当前唯一主项目

**AI Knowledge-to-Learning Engine**（`ai-knowledge-to-learning-engine/`，GitHub `Vin535LFJ/ai-knowledge-to-learning-engine`）。任何时刻至多一个主动开发项目；其余项目状态见 PROGRAM.md §2/§9（Skills 库 = 维护与兼容性验证，**实机验证仍为 PARTIAL**；Governance / Radar = 维护期；LXD = Engine 内部工作流，不独立成仓）。

## 2. 当前阶段

**人工验收与稳定化阶段（2026-11-25 进入）。** 主线仍是 P1'：embodied-loop-journey 首批 6 课，run 停在 **REVIEW / paused，等待用户裁决**。上一主目标 P1 已于 2026-11-21 达成。

## 3. 当前任务

1. **用户完成六课裁决**。材料已备齐并反映修复后的版本：Engine `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`（G1 21 条断言逐条依据与分类建议、G2 六课逐课依据与评分表、专项复核、审批登记顺序）。裁决栏全部留空；AI 没有升级断言、没有填分。
2. **方案甲修复已执行（2026-11-25 22:35，用户批准）**：验收包 §6 的 11 项最小修复全部落地，独立审读员复核 9 项改动全部修对、无新的事实错误（Engine `reviews/embodied-batch1/recheck-planA-fixes.md`）。新增断言 V88（open / low）；V83 的 CPU 行出处同步为 MuJoCo 官方文档。run 仍 REVIEW / paused，产物哈希已重新登记。
3. 维护项的副本验证已做完（Radar 真实库副本、Governance Engine 副本、LXD 七实验回归、Git 审查），结论见 §7 的稳定化验证报告。PASS WITH LIMITATIONS 没有被改成 PASS。

## 4. 阻塞问题（需人工，AI 不自批）

- **embodied 四件人工门**：G1（V68–V88 是否升级）→ G2（六课评分，请基于修复后的版本）→ 登记审批 + G3 → KCR。run 无法被 AI 推进。
- **提交与推送（2026-11-26 已收口）**：方案甲修复批次已分组提交并普通推送（Engine 10 笔 / Skills 2 笔，ls-remote 核实一致）。**同日按用户指令全部重写提交作者**：公司邮箱作者统一改为 `Vin535LFJ <169535939+Vin535LFJ@users.noreply.github.com>`，内容零改动（tree 哈希前后一致），公开仓已 `--force-with-lease` 强推。全部旧 SHA 失效，历史材料保留原 SHA 并加整段注记；本地仓（Program / Governance / Radar）重写不涉及远程。
- **Skills 全新会话验证未做**（本会话会话重建后发现、加载、执行均成功，但全新会话未测）。
- **待裁决九项**：PD-Q9 至 PD-Q17（`decisions/PENDING_DECISIONS.md`），本轮未批准任何一项。

## 5. 下一步

1. 用户读完验收包，填 G1 裁决栏与 G2 评分。
2. AI 按裁决更新台账、同步课文状态说明，重建并跑门禁，报结果。
3. 用户确认文件不再改动后，按顺序登记审批 → G3 → KCR；AI 复核通过后 resume → PUBLISH（本地口径，在线发布仍受 D02 约束）→ FEEDBACK → done。
4. 其间可穿插：提交本轮产物并推送（PD-Q17）；Skills 全新会话确认。

## 6. 最近状态更新时间

**2026-11-26**（提交作者统一重写完成、五仓注记落盘时）。同日另：全历史作者重写为公司邮箱 → GitHub 身份（用户批准，公开仓 `--force-with-lease` 强推），全部旧 SHA 失效。逐日明细以 Engine `CHANGELOG.md` / `WORKFLOW_STATE.md` 为准。

## 7. 关键状态文件链接

- 稳定化验证报告：[plans/2026-11-25-stabilization-verification.md](plans/2026-11-25-stabilization-verification.md) · 上一轮执行报告：[plans/2026-11-25-stage-execution-report.md](plans/2026-11-25-stage-execution-report.md)
- 章程与边界：[PROGRAM.md](PROGRAM.md) · 阶段规划：[ROADMAP.md](ROADMAP.md) · 暂缓登记：[PARKING-LOT.md](PARKING-LOT.md) · PM 规则：[PROGRAM-MANAGER.md](PROGRAM-MANAGER.md)
- 程序级决策：[decisions/](decisions/)（PD-001…003 + PD-Q 裁决存档；**待决见 [PENDING_DECISIONS.md](decisions/PENDING_DECISIONS.md)**）· 使用指南：[USER-GUIDE.md](USER-GUIDE.md) · 文档导航：[PROJECT-DOCUMENTATION-INDEX.md](PROJECT-DOCUMENTATION-INDEX.md)
- 审计：[AUDIT-REPORT.md](AUDIT-REPORT.md) · [POST-AUDIT-SUMMARY.md](POST-AUDIT-SUMMARY.md) · [final-acceptance-2026-11-21.md](final-acceptance-2026-11-21.md)
- Engine 权威状态（冲突时以项目内 + git 实测为准）：`ai-knowledge-to-learning-engine/WORKFLOW_STATE.md` / `DECISIONS.md` / `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md` / `reviews/embodied-batch1/targeted-recheck.md` / `reviews/approvals/README.md`
- 交接索引：[handoffs/README.md](handoffs/README.md)
