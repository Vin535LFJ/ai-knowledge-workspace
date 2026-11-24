---
doc_id: PD-003
type: decision
status: accepted
owner: human
created: 2026-11-19
updated: 2026-11-19
---

# PD-003 · 范围裁剪：单活跃线 + 冻结其余（已批准）

> 状态：**accepted**（2026-11-19 用户批准："批准 PD-Q7 裁剪方案，PD-Q1、PD-Q2、PD-Q8 也按推荐执行，之后只推进 Engine 一条线"）。
> 执行记录：PD-Q1 四笔收口已 push（Render_Notes 远端 HEAD=`e848d28`）；PD-Q2 P03 `dec60ba`/P04 `942530b` 本地 git；PD-Q8 副本已清理。详见 STATUS_BOARD 证据日志与 Render_Notes DECISIONS D16。
> 触发：用户反馈"感觉越做越多了，需要裁剪"（2026-11-19），并给出 01 Engine → 02 体验 Skill → 03 治理抽取 → 04 Radar 的优先序。
> 依据：两份引导附件（references/gpt-architecture-guidance.txt 与 2026-11-19 生态架构建议 §10–§11）本身结论一致——**三项目 + 一个主 Skill，Engine 先行，治理从真实痛点抽取，Radar 最后**。

## 1. 问题诊断（本轮实测）

扩张不是计划造成的，是**执行先于裁决**造成的：

| 事实 | 证据 |
|---|---|
| P03/P04 MVP 已建成（25/38 tests），早于引导文档要求的"Engine 稳定后再抽取" | 迁移后 unittest 实测 |
| learning-experience-design Skill 已建成（CHG-0001），早于其四个前置条件 | .agent/skills/learning-experience-design/ |
| Render_Notes 未提交改动已累积**三批**（D15 治理 / CHG-0001 / 今日 P8-P9 预研），收口越拖越难 | git status 本轮实测 |
| 用户新增想法（知识库收录项目、skill 收录项目）若立项将开出第 5/6 条战线 | 本轮用户消息 |

## 2. 裁剪决定（批准后生效）

### 2.1 唯一活跃线：Engine（项目 01）

顺序固定，不并行开新战线：

1. **收口**：三批未提交改动审计 + commit/push（PD-Q1）；Render_Notes 迁入 AI-Knowledge（PD-002 收尾）。
2. **人工审核**：G1/G2 裁决（B4/B10/B11/V13–V20；decision-kit/ 已备好逐项材料）。
3. **P7.2**：按依赖逐篇补教材，一次一篇，不批量。
4. **P8**：KCR 最小闭环（kcr_impact.py 只读影响分析已起步，属本线，继续）。
5. **P9**：最小状态机，一门 pilot 课证明可断点续跑。
6. **P10**：**一批新资料端到端验收**——这是"Engine 完成"的定义，不是 19 课写完。

### 2.2 learning-experience-design：保留文件，冻结试点

- 已建 Skill 文件不删除（是资产不是负债），但**冻结扩展**。
- 解冻条件（引导文档 §10 四条，全部满足才启动试点）：P7 质量稳定 + P8 闭环可用 + P9 记录过一次完整 run + 发布边界明确。
- PD-Q6（试点方向 A/B）**顺延**到解冻后。不建独立仓库（附件明确反对）。

### 2.3 P03 Governance：冻结在 MVP

- 保留现有 MVP 与测试作为 sandbox，**停止新功能/新 CLI/新目录**。
- 只允许一个动作：把 Engine 协作中真实发生的痛点追加记录到其需求清单（为将来抽取备料）。
- 不做反向接入 Render_Notes、不建 GitHub 远程。
- 解冻条件：Engine P10 验收通过 **且** 痛点清单有真实案例支撑。
- PD-Q2（git init）仍建议执行——冻结的资产也需要版本保护，防丢失。

### 2.4 P04 Radar：冻结在 MVP

- 不申请 PAT、不建 Actions、不启动真实采集。
- 理由（附件 §10 原话）：Engine 消化能力未建成前，Radar 只会不断收藏却无法消化。
- 期间想查某个热点项目：直接用 web 搜索，不建系统。
- 解冻条件：Engine P8 输入合同（source inbox）就绪后。

### 2.5 不新建"知识库收录 / skill 收录"独立项目（回应用户想法 4）

- **skill 收录管理**：供应库已是项目 02（37 技能 + 安装/兼容性纪律）；跨项目 skill/mcp/tools 登记是 P03 解冻后的 Registry 职责。无需新项目。
- **知识库收录**：就是 Engine P8 的输入合同 + source inbox，属 Engine 内部能力。拆出去反而切断"收录→消化"闭环。
- 结论：该想法的合理内核已被现有边界覆盖；现在立项 = 第 5/6 条战线，违背裁剪目标。将来若出现真实痛点（如多领域知识库互相引用混乱），再按 PD 流程重议。

### 2.6 办公室保持薄

- 只维护：PROJECT_INDEX / STATUS_BOARD / PENDING_DECISIONS / 本决策目录。
- 不新增治理层、不新增文档类型；审计只在收口与里程碑节点做。

## 3. 冻结 ≠ 删除

所有已建产物（P03/P04 MVP、P2 Skill、三批未提交改动）全部保留。裁剪只停止**新增投入**，不销毁任何已有工作。

## 4. 批准后的立即动作（仍需逐项授权）

| 动作 | 授权项 |
|---|---|
| 三批改动审计 + 拆分 commit + push | PD-Q1 |
| P03/P04 git init + 首笔提交（版本保护） | PD-Q2 |
| Render_Notes 迁入 AI-Knowledge | PD-002 收尾（已授权，执行受阻待重试） |
| program-office-delivery 副本清理（防 bundle 污染） | 新授权项 PD-Q8 |

## 5. 人工裁决栏

裁决（批准 / 驳回 / 修改范围）：**批准**（PD-Q7，连同 PD-Q1/Q2/Q8 按推荐执行）

日期：2026-11-19（用户会话指令）