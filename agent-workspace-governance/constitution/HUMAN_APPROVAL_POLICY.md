---
doc_id: HUMAN_APPROVAL_POLICY
type: constitution
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 人工审批策略

## 一、必须人工审批的动作

以下动作 AI 不得自行决定或执行，必须由人确认：

1. 架构决策（ADR 从 proposed 推进到 accepted / superseded / deprecated）
2. 业务目标变更
3. 文档结构重大调整
4. 权威知识升级（L1 内容升格）
5. 课程路线变更（学习路径类项目）
6. 高风险文档删除
7. 重要归档（把 active 文档移入 L3）
8. git 提交 / 推送
9. 生产环境部署

## 二、审批记录字段

每条审批记录必须包含：

- `approver` —— 批准人
- `time` —— 批准时间
- `object` —— 审批对象（文档 / 决策 / 动作）
- `decision` —— 决定（approved / rejected / deferred）
- `authorization_scope` —— 授权范围（避免过度授权）

## 三、铁律

- **无回复 ≠ 同意（no reply is not consent）。**
- 审批必须在动作**发生前**完成，事后补批无效。
- 审批范围仅限本次对象，不得自动扩展到其他对象。
- 审批记录写入 `.governance/` 的状态中，可审计、可追溯。

## 四、AI 可以做的事

在不触及上述清单的前提下，AI 可自主进行研究、起草 L2 工作文档、执行已被批准的任务、生成交接与评审报告、维护注册表索引。但任何上升为「正式事实」或「不可逆动作」的那一刻，必须回到人工审批。
