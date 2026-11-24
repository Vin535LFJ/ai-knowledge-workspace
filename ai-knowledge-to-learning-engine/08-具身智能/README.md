---
doc_id: EMB-README
type: knowledge
status: draft
owner: qwenwork
created: 2026-11-24
updated: 2026-11-24
---

# 08-具身智能 · 目录说明

> embodied-loop-journey《具身智能：一条指令如何变成物理动作》首批 6 课的知识底本（RESEARCH 阶段源提取产物，run `RUN-2026-11-23-embodied-batch1`）。
> **状态：draft**——全部断言 open/low，升级待 G1 人工核验；本目录是 Engine 内提取文档，不是源库副本。

## 源与纪律

- 源库：`C:\Users\Giant\Desktop\GITCODE\Robot_Learn`（**只读，零改动**）。主源：textbook-embodied.md（10 章）/ embodied-principles.md（6 章）/ ch05 5.15、5.16 verified 块 / embodied-openlab.md。
- 提取纪律：公式 Unicode→LaTeX 显示块规范化；**全部关键算例经 Engine 独立复算（py -3，70/70 通过）**，不信任源库"node 复算通过"自称；教学假设参数一律保留"（教学假设，存疑）"标注。
- 源库问题**登记不擅改**（Robot_Learn 只读）：见 `reviews/embodied-batch1/research-report-embodied.md` §源勘误队列（含"300 毫米"单位笔误、混叠释义条件写反、qⁿ 界方向三处口径冲突等 12 项）。本目录文档按正确表述撰写并显式注记差异。
- 章节映射更正：textbook **§7 = Sim2Real、§8 = VLA 与世界模型**（模仿学习复合误差在 §8.5）——intake 清单的"§7/§8"主题映射不变，节号以源文件实际为准。

## 文档清单（课–源映射）

| 文档 | 支撑课 | 主源 |
|---|---|---|
| 01-闭环判据与错误落点.md | L1 | textbook §1 + kb:5.1 |
| 02-六环闭环与时间预算.md | L2 | textbook §3 + principles ch1 + kb:5.3/5.15.7 |
| 03-时空对齐与标定.md | L3 | textbook §5 + principles ch2 + kb:5.5/5.15.1–3/5.15.8 |
| 04-运动学与雅可比奇异.md | L4 | kb:5.16.1–3（verified） |
| 05-模仿学习复合误差与Sim2Real.md | L5 | textbook §7/§8 + principles ch3/ch4 + kb:5.8/5.15.5–6/5.16.5–6 |
| 06-开源生态与实践路径.md | L6 | textbook §10 + openlab |

## 边界（如实定位）

首批是"可手算最小核"（平面两连杆级运动学 + 闭环/对齐/复合误差/域随机化的算术直觉），**不承诺** SLAM、动力学、控制实操、ROS 实操；VLA/世界模型仅概念级 + 快照日期。外部权威核验已完成三项（Tobin 2017 域随机化 / Ross 2011 DAgger / MuJoCo MJWarp 官方 FAQ），其余关键结论的权威核验在 G1 队列。