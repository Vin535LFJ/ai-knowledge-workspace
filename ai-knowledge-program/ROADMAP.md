---
doc_id: PROG-ROADMAP
type: program-roadmap
status: active
owner: human
created: 2026-11-19
updated: 2026-11-25
---

# ROADMAP · NOW / NEXT / LATER / COMPLETED

> 顺序固定，不并行开新战线。每阶段有明确进入/退出条件；门禁未过不进入下一阶段；人工关卡未回复不视为同意。
> 授权来源：PD-003（accepted）+ 用户 2026-11-19 三层重组指令 + 2026-11-21 六阶段批准计划 + 2026-11-23 下一主线裁决（"1 和 3"，新领域参考 Robot_Learn）。

## NOW · P1'：P10.3 多领域课程复用 —— embodied-loop-journey（唯一主线）

**进入条件**：P10 端到端验收 done（✅ 2026-11-21，D20）+ kickoff 方案用户批准（✅ 2026-11-23 用户批准，`plans/2026-11-23-embodied-course-kickoff.md`）。
**退出条件**：首批 6 课以 run_state 真实 run 走通 INTAKE→FEEDBACK + G1/G2/G3 人工门闭合 + 复用专项验收（共享 Evidence/Glossary/Skills 零重建、跨课程概念去重、工具链多课程支持）。

| 工作流 | 内容 | 状态 |
|---|---|---|
| 主线：新课程 | embodied-loop-journey《具身智能：一条指令如何变成物理动作》，源参考 Robot_Learn（只读）；首批 6 课（闭环判据/六环时间预算/时空对齐/运动学与雅可比/模仿学习与 Sim2Real/开源生态实践） | ✅ kickoff 已批准（2026-11-23）；run `RUN-2026-11-23-embodied-batch1`：六课写完，经独立审读 → 修复 → 复审 → 整改 → 复评（建议分全部 ≥85，AI 诊断分非裁决），**REVIEW / paused 等人工 G1 / G2 / G3**（2026-11-25）；**用户验收包已备齐**（Engine `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`，裁决栏留空） |
| 内部工作流：LXD 铺开 | 新课程页面直接按六项增强 + Floor 标准建；既有 19 课分批增强（每批 3–5 课，独立小提交，不占主线门禁） | 🔄 六课按六项增强建成（逐课实测见 Engine `reviews/embodied-batch1/design-note.md`）；实验页第二案例完成（transform-mvp，`239169a`）；推广到其余 6 个实验与既有 19 课的增强待用户确认（PD-Q9）；七实验样式回归通过（2026-11-25） |
| 稳定化验证（维护项） | Radar 真实库副本验证 / Governance Engine 副本接入 / LXD 七实验回归 / Git 同步审查 | ✅ 已执行（2026-11-25）：Radar 与 LXD 通过（仅限副本与回归）；Governance 部分通过（`validate` / `doctor` 在真实文档上不过，PD-Q14）；Skills 仍 PARTIAL。见 `plans/2026-11-25-stabilization-verification.md` |
| 积压（不阻塞） | G2 历史 17 篇评分（L19 模式）/ U1–U3 / P07 / C1–C7 研究队列 / P9.4 工具盘点 / 2026-11-24 任务书遗留的审计档案归档 | ⬜ 穿插（两处源笔误已随 D21 修正；Radar / Governance P0 与审批证据链已于 2026-11-25 完成） |

**边界**：Robot_Learn 只读参考不修改；SLAM/刚体动力学/控制理论/ROS 实操为源库自认缺口，课程定位不承诺；首批不含 VLA/世界模型前沿深潜（快照时效风险）。工具链若需多课程扩展，动手前报批。

## NEXT · Engine 质量收口与第二批

- 首批验收后：embodied 课程扩到 12–19 课（源材料够，见盘点）；或按用户裁决转其他领域（gpu/procedural/ai-engineering journey）。
- 研究队列闭合（C1–C7/U1–U3/P07）+ G2 历史评分清零 + 源笔误修正。
- LXD 成熟化持续从真实页面迭代提炼（Skill 已 active，不建独立仓库）。两个真实案例：教材页 L13、交互实验页 transform-mvp。
- 审计整改：2026-11-24 第一批中 TASK 0 推送、TASK 1 Program 一致性、TASK 2 Engine 发布边界强制化均已完成；**TASK 3 审计档案归档未执行**（会话中断，`audits/2026-11-24-post-implementation-audit/` 目录不存在，待执行）。2026-11-25 任务书六项执行结论见 `plans/2026-11-25-stage-execution-report.md`。

## LATER · Governance / Radar（已解冻验证，按需维护）

- **Governance**：2026-11-21 阶段 3 解冻执行——ENGINE 真实适配实跑（183 docs）+ IGNORE_DIRS 修复（`6aec3d3`+`1b4a880`）。**审计口径修正（2026-11-24）**：原称「9/9 验收」为文档自证，实际示例项目 doctor 不通过、真实项目 0 task/0 agent/0 ADR，独立审计判定 PARTIAL。此后**维护期**：仅修缺陷与可靠性验证（示例项目过 doctor、已有 AGENTS.md 的项目接入），不追加新功能；无第二个持续真实项目需求前不抽取。反向接入/独立抽取仍须 ADR + 用户批准。**P0 已修**（2026-11-25，`2ab2891`）：示例 doctor 退出码 0、init 接入已有 AGENTS.md 且幂等，41 tests；**2026-11-25 副本验证更正**：Engine 里已有被 git 跟踪的 `.governance/`（2026-11-21 适配写入，5 个文件）；在 Engine 副本上 `init` 安全且幂等、AGENTS.md 原文保留，但 `validate` exit 1、`doctor` exit 1（Engine 文档类型不在 13 类枚举、146 条登记为 unknown），原因是两套规范的类型口径未对齐，非 P0 回归（PD-Q14）。
- **Radar**：2026-11-21 阶段 4 解冻执行——rest.py 匿名真实采集 121 仓 + 首份周报 + Intake 导出 1 条（`b7442da`）。**审计口径修正（2026-11-24）**：原称「200 快照」实为 20 秒内 4 次搜索（增长数据全空）；`analyze` 会覆盖人工复核状态、`--approved` 不写人工批准字段、导出物 `human_selected_for_research=false`，独立审计判定 PARTIAL。此后**维护期**：仅修 P0/P1 缺陷（人工状态保留/人工门字段/增长口径），不追加功能；PAT（PD-Q4）未申请、不自动导入 Engine；持续采集成为明确负担时再评估自动化。**P0 已修**（2026-11-25，`dbff9c7`）：analyze 不再覆盖人工状态、`--approved` 写入完整人工批准字段，58 tests；已在真实库的隔离副本上验证通过（2026-11-25：人工状态不被重置、批准幂等、非法转换被拒，58 tests）；真实库仍是修复前结构，升级待批（PD-Q15）。
- **PD-Q3 远程创建**（Program/Governance/Radar）：仍待用户另批（不可逆公开动作）。

## COMPLETED · P1：Engine 主目标达成（2026-11-21 P10 done）

- ✅ P0–P9 全部：治理基座 / 19 份教材（L00 地图课无正文）/ P8 KCR 三片 / P9 状态机（25 tests）。
- ✅ **P10 端到端验收**：HDR 批次真实 run（RUN-2026-11-20-p10-hdr）INTAKE→FEEDBACK 18 artifacts 全闭环；四件人工门全过（G1 六项升级 / KCR APPROVED→VERIFIED / G2=91 用户本人 / G3 passed）；D20 裁决记录；84 claims（24v/53o/7c）误标 0。
- ✅ 六阶段总验收：`final-acceptance-2026-11-21.md`（阶段 0 Program / 1 Engine / 2 LXD 试点 A / 3 Governance / 4 Radar / 5 整合核对）。**注**：2026-11-24 独立审计对阶段 3/4 判 PARTIAL（文档口径与真实状态有差距，修正见上 LATER 节），总验收报告已加声明。
- ✅ **push 收口（2026-11-23 用户授权）**：Engine `e848d28..3115cad` 6 笔 + Skills `e1936f2..7326522` 1 笔，ls-remote 实测一致。
- ✅ **push 收口第二批（2026-11-24 审计整改 TASK 0）**：Engine `79c3fe8..46a04d3` 2 笔 + Skills `7326522..4604bd6` 1 笔，ls-remote 实测一致；此前 USER-GUIDE.md 远程 404 已消除。

## COMPLETED · P0：建立 Program 管理层（2026-11-19 验收）

- ✅ 四个管理文件 + PROGRAM-MANAGER 规则；物理集中（PD-002）；收口版本化；命名统一（T1，2026-11-20 完成）。
- 边界：不开发 Dashboard、数据库、Web 管理系统、自动任务调度平台、新多 Agent 框架。

## 不列入路线图

独立 Knowledge / Skills / MCP / Tools 中央管理平台；知识库收录 / skill 收录独立项目；超级多 Agent 平台。（PROGRAM.md §7）