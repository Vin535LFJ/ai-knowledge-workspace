---
doc_id: PROG-SUPERVISION
type: supervision
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# 监督规则（跨项目协作纪律）

针对已发生的真实事故制定：`.zcode` 计划污染 bundle、另一 Agent 重建 content.js 致 drift、过期计划引用残留、**两个 Agent 会话先后写入 Render_Notes 同一工作区（D15 + CHG-0001）**。

## 规则一 · 单一事实源

- 各项目内部状态以该项目自己的状态文档为权威（见 PROJECT_INDEX.md 入口）。
- 本 Program 看板是**带日期的快照索引**，不是第二事实源；冲突时以项目内文档 + git 实测为准，并更新看板。
- 生成物不是源文件：`web/content.js`、`site-vitepress/docs/`、注册表 JSON 等只能由对应生成器重建，禁止手改。
- 适配入口（CLAUDE.md/AGENTS.md/.cursor 等）只跳转不复制正文。

## 规则二 · 一个任务一个主要写入者

- 可以并行研究，但同一组文件只能由一个 Agent 整合写入。
- 每个任务开始前声明任务合同：Owner Agent / 允许读 / 允许写 / 禁止改 / 预期输出 / 验收条件（模板见 Render_Notes `.agent/templates/agent-handoff.md` 与项目03 `schemas/task.schema.json`）。
- **接手前先查工作区**：`git status` 有非本任务来源的未提交改动时，先登记到看板"未提交批次"，不得覆盖、不得顺手提交他人改动。
- 重要任务用独立分支/worktree；禁止多 Agent 同时改 course.json / claim-ledger.json / README。

## 规则三 · 人工关卡不可自批

必须人工批准：架构决策（ADR accepted）、业务目标改变、目录结构重大改变、权威断言升级（open→verified）、课程路线调整、高风险删除、历史归档、**git commit/push、远程仓库创建、部署**。
审批记录含：审批人、时间、对象、决策、授权范围。**未回复不视为同意。**
AI 自动检查通过 ≠ 人工审核通过（G1/G2/G3 评分表 AI 不得填写）。

## 规则四 · 阶段门禁

按 PROGRAM_PLAN.md：阶段 A 收口前不开深度建设；Engine P10 验收是最高优先级里程碑；P3 反向接入必须先 ADR；Radar 候选必须先人工批准再导出。

## 规则五 · 完成必须交接

任务结束时输出：实际修改文件清单、运行过的测试与真实结果、遗留问题、下一步建议；更新 STATUS_BOARD.md 对应行 + handoffs/ 登记指针。没有交接的任务视为未完成。

## 审计节奏（监督动作）

1. **每次会话开始**：读 README → STATUS_BOARD → 目标项目 git status；发现漂移（未知改动/未知文件/状态不符）先登记报告，不静默修复。
2. **每次收口提交前**：按来源拆分批次审计（当前 Render_Notes 有 D15 与 CHG-0001 两批交织），逐批列文件清单给用户确认。
3. **每周或每个里程碑**：复跑四项目门禁/测试，把新鲜证据写入看板证据日志；旧证据标注日期，不冒充当前状态。
4. **跨项目变更**：涉及两个以上项目的变更走程序级决策（decisions/PD-xxx）；单项目内部变更走该项目自己的 Change Proposal / DECISIONS。

## 禁区（继承各项目既有保护）

Render_Notes：`.workbuddy-ai/memory/**`、`archive/**`、`web/vendor/**`、`web/index.html`、两份旧方案文档、stash（B12 前）。
Skills 仓：不承载治理代码，上游同步纪律不变。
本 Program：不复制知识内容/Skill 正文；references/ 只读。