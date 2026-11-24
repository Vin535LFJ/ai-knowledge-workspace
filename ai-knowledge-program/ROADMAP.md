---
doc_id: PROG-ROADMAP
type: program-roadmap
status: active
owner: human
created: 2026-11-19
updated: 2026-11-23
---

# ROADMAP · NOW / NEXT / LATER / COMPLETED

> 顺序固定，不并行开新战线。每阶段有明确进入/退出条件；门禁未过不进入下一阶段；人工关卡未回复不视为同意。
> 授权来源：PD-003（accepted）+ 用户 2026-11-19 三层重组指令 + 2026-11-21 六阶段批准计划 + 2026-11-23 下一主线裁决（"1 和 3"，新领域参考 Robot_Learn）。

## NOW · P1'：P10.3 多领域课程复用 —— embodied-loop-journey（唯一主线）

**进入条件**：P10 端到端验收 done（✅ 2026-11-21，D20）+ kickoff 方案用户批准（⬜ `plans/2026-11-23-embodied-course-kickoff.md`）。
**退出条件**：首批 6 课以 run_state 真实 run 走通 INTAKE→FEEDBACK + G1/G2/G3 人工门闭合 + 复用专项验收（共享 Evidence/Glossary/Skills 零重建、跨课程概念去重、工具链多课程支持）。

| 工作流 | 内容 | 状态 |
|---|---|---|
| 主线：新课程 | embodied-loop-journey《具身智能：一条指令如何变成物理动作》，源参考 Robot_Learn（只读）；首批 6 课（闭环判据/六环时间预算/时空对齐/运动学与雅可比/模仿学习与 Sim2Real/开源生态实践） | ⬜ kickoff 待批 |
| 内部工作流：LXD 铺开 | 新课程页面直接按六项增强 + Floor 标准建；既有 19 课分批增强（每批 3–5 课，独立小提交，不占主线门禁） | ⬜ 随主线 |
| 积压（不阻塞） | G2 历史 17 篇评分（L19 模式）/ 两处源笔误 / U1–U3 / P07 / C1–C7 研究队列 / P9.4 工具盘点 | ⬜ 穿插 |

**边界**：Robot_Learn 只读参考不修改；SLAM/刚体动力学/控制理论/ROS 实操为源库自认缺口，课程定位不承诺；首批不含 VLA/世界模型前沿深潜（快照时效风险）。工具链若需多课程扩展，动手前报批。

## NEXT · Engine 质量收口与第二批

- 首批验收后：embodied 课程扩到 12–19 课（源材料够，见盘点）；或按用户裁决转其他领域（gpu/procedural/ai-engineering journey）。
- 研究队列闭合（C1–C7/U1–U3/P07）+ G2 历史评分清零 + 源笔误修正。
- LXD 成熟化持续从真实页面迭代提炼（Skill 已 active，不建独立仓库）。

## LATER · Governance / Radar（已解冻验证，按需维护）

- **Governance**：2026-11-21 阶段 3 解冻执行——ENGINE 真实适配实跑（183 docs）+ IGNORE_DIRS 修复 + 9/9 验收（`6aec3d3`+`1b4a880`）。此后**按需维护**：Engine 协作真实痛点继续记录；无第二个持续真实项目需求前不追加新功能。反向接入/独立抽取仍须 ADR + 用户批准。
- **Radar**：2026-11-21 阶段 4 解冻执行——rest.py 匿名真实采集 121 仓/200 快照/0 错误 + 首份周报 + Intake 导出 1 条（`b7442da`）。此后**按需跑周报**；PAT（PD-Q4）未申请、不自动导入 Engine；持续采集成为明确负担时再评估自动化。
- **PD-Q3 远程创建**（Program/Governance/Radar）：仍待用户另批（不可逆公开动作）。

## COMPLETED · P1：Engine 主目标达成（2026-11-21 P10 done）

- ✅ P0–P9 全部：治理基座 / 19 份教材（L00 地图课无正文）/ P8 KCR 三片 / P9 状态机（25 tests）。
- ✅ **P10 端到端验收**：HDR 批次真实 run（RUN-2026-11-20-p10-hdr）INTAKE→FEEDBACK 18 artifacts 全闭环；四件人工门全过（G1 六项升级 / KCR APPROVED→VERIFIED / G2=91 用户本人 / G3 passed）；D20 裁决记录；84 claims（24v/53o/7c）误标 0。
- ✅ 六阶段总验收：`final-acceptance-2026-11-21.md`（阶段 0 Program / 1 Engine / 2 LXD 试点 A / 3 Governance 9/9 / 4 Radar 真实数据 / 5 整合核对）。
- ✅ **push 收口（2026-11-23 用户授权）**：Engine `e848d28..3115cad` 6 笔 + Skills `e1936f2..7326522` 1 笔，ls-remote 实测一致。

## COMPLETED · P0：建立 Program 管理层（2026-11-19 验收）

- ✅ 四个管理文件 + PROGRAM-MANAGER 规则；物理集中（PD-002）；收口版本化；命名统一（T1，2026-11-20 完成）。
- 边界：不开发 Dashboard、数据库、Web 管理系统、自动任务调度平台、新多 Agent 框架。

## 不列入路线图

独立 Knowledge / Skills / MCP / Tools 中央管理平台；知识库收录 / skill 收录独立项目；超级多 Agent 平台。（PROGRAM.md §7）