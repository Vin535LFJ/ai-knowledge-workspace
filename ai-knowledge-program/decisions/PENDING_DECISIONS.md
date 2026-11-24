---
doc_id: PROG-PENDING
type: decision-request
status: under_review
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# 统一待裁决清单（程序级）

> **2026-11-19 重组后本文件为 PD-Q 系列裁决存档**：活阻塞以 `../NOW.md` 为准（Engine G1/G2 七项，对应 PD-Q5），冻结顺延项（PD-Q3/Q4）见 `../PARKING-LOT.md`。
> 未回复不视为同意。Render_Notes 内部 B 项裁决仍以 `reviews/DECISION_REQUIRED.md` 为权威，此处只列程序级收口项与指针。

| 编号 | 事项 | 推荐 | 影响 | 裁决（人工填写） |
|---|---|---|---|---|
| PD-Q1 | Render_Notes 未提交批次收口：**三批**——D15 治理基座 + CHG-0001（P7 修复 + P2 Skill）+ 今日 P8/P9 预研（kcr_impact.py / publish_boundary+allowlist / P9 设计 / reviews/kcr+decision-kit）commit + push | 授权；按来源拆 3 笔，content.js 随最后一笔重建提交 | 解除 M4 阻塞；三批交织需先审计 | ✅ 已执行（2026-11-19）：`5a4de84`/`a45ffa9`/`7c05bc7`/`9bfa732`+留痕 `e848d28` 已 push；test_publish_boundary 断言笔误修正 77→69 后 11/11 OK |
| PD-Q2 | P03/P04 本地 git init + 首笔提交 | 授权（本地，无远程） | 两项目获得版本保护，MVP 成果可回滚 | ✅ 已执行：P03 `dec60ba`（39 文件）/ P04 `942530b`（30 文件），测试 25/38 OK，无远程 |
| PD-Q3 | 三个新仓库（Program/P03/P04）GitHub 远程创建 + push | 本地验证后另行授权；届时定公开/私有 | 不可逆公开动作，需明确授权 | |
| PD-Q4 | Radar GitHub PAT（环境变量注入，5000 req/h） | 提供只读 public_repo 权限 PAT；无 token 则 60 req/h 仅够手动小规模 | 阶段 E 前置 | |
| PD-Q5 | Render_Notes G1/G2 裁决指针：B4 / B10 / V13–V20 升级 / B11 / B12 / B15 | 逐项见 reviews/DECISION_REQUIRED.md 与 G1 §7；V13 先修正杆/锥表述再升级 | Engine 审核收口 | |
| PD-Q6 | P2 试点方向：A 增量增强 vs B 重设计（PILOT-L13-plan.md） | **若 PD-Q7 批准则顺延**至解冻条件满足（P7 稳定+P8 闭环+P9 一次 run+发布边界明确） | 阶段 C 前置 | ⏸ 已按 PD-003 顺延（冻结至解冻条件满足） |
| PD-Q7 | **范围裁剪提案 PD-003**：单活跃线 Engine；P2 Skill/P03/P04 冻结在现有成果；不新建知识库/skill 收录项目 | 批准（与两份引导附件 §10–§11 结论及用户 01–04 优先序一致） | 停止战线扩张；冻结≠删除 | ✅ 批准（2026-11-19 用户指令），PD-003 accepted |
| PD-Q8 | Render_Notes 内 program-office-delivery/ 交付副本清理（未跟踪 .md，会污染知识 bundle） | 安全删除（回收站可恢复）；权威原件在办公室 | 防重演 .zcode 污染 | ✅ 已执行：10 份副本→回收站（可恢复）；.qoder-input-images/ 加入 gitignore |

## 已按默认执行并记录（低风险，可推翻）

- Program 位置与名称：办公室 `ai-knowledge-program`（PD-001，用户指令授权）。
- ~~索引而非迁移（PD-001）~~ → **已被 PD-002 取代：四项目物理集中到 `GITCODE\AI-Knowledge\`**（用户本轮指令）。
- 本轮复跑 P03/P04 测试与 Render_Notes 只读门禁取证（只读动作）。
- PD-Q1 收口路径已随 PD-002 变为 `AI-Knowledge\Render_Notes`；未提交批次内容不变，仍待授权。