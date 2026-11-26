---
doc_id: PROG-PENDING
type: decision-request
status: under_review
owner: qwenwork
created: 2026-11-19
updated: 2026-11-26
---

# 统一待裁决清单（程序级）

> **本文件为 PD-Q 系列裁决存档**：当前活阻塞以 `../NOW.md` 为准（embodied 首批 G1 / G2 人工裁决，材料在 Engine `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`）。**活跃待决项：PD-Q3 / Q4 / Q9 / Q11 / Q15 / Q16**；PD-Q10 / Q13 / Q17 已关闭（见各行裁决栏）；PD-Q12 / Q14 因 Governance 已归档（`legacy/`，只读不维护）转为非活跃，如重新启用再议。
> 未回复不视为同意。Engine 内部审核票据以 `ai-knowledge-to-learning-engine/reviews/` 为权威，此处只列程序级收口项与指针。

| 编号 | 事项 | 推荐 | 影响 | 裁决（人工填写） |
|---|---|---|---|---|
| PD-Q1 | Render_Notes 未提交批次收口：**三批**——D15 治理基座 + CHG-0001（P7 修复 + P2 Skill）+ 今日 P8/P9 预研（kcr_impact.py / publish_boundary+allowlist / P9 设计 / reviews/kcr+decision-kit）commit + push | 授权；按来源拆 3 笔，content.js 随最后一笔重建提交 | 解除 M4 阻塞；三批交织需先审计 | ✅ 已执行（2026-11-19）：`5a4de84`/`a45ffa9`/`7c05bc7`/`9bfa732`+留痕 `e848d28` 已 push；test_publish_boundary 断言笔误修正 77→69 后 11/11 OK |
| PD-Q2 | P03/P04 本地 git init + 首笔提交 | 授权（本地，无远程） | 两项目获得版本保护，MVP 成果可回滚 | ✅ 已执行：P03 `dec60ba`（39 文件）/ P04 `942530b`（30 文件），测试 25/38 OK，无远程 |
| PD-Q3 | 三个新仓库（Program/P03/P04）GitHub 远程创建 + push | 本地验证后另行授权；届时定公开/私有 | 不可逆公开动作，需明确授权 | |
| PD-Q4 | Radar GitHub PAT（环境变量注入，5000 req/h） | 提供只读 public_repo 权限 PAT；无 token 则 60 req/h 仅够手动小规模 | 阶段 E 前置 | |
| PD-Q5 | Engine decision-kit 七项裁决指针：B4 / B10 / B11 / B12 / B15 / V13 / V14 | 逐项见 Engine `reviews/decision-kit/`；V13 先修正杆/锥表述再升级 | Engine 审核收口 | ✅ **已执行（2026-11-19，用户逐项裁决；对应 Engine DECISIONS D17/D18/D19，票据 Resolution 与总表 7/7 闭合）**：**D17** = B4=B（L01 为 Gold Standard + §4.2 记号与 V13 表述两处小修订，断言状态未升）+ B15=A（C1–C7 全部入研究队列）；**D18** = V13=A（表述三处修正后升级 verified/high，依据 D12.7 权威核验）+ V14=A（升级 verified/high，保留两条平台差异 conditions）；**D19** = B10=A（V17–V20 确认登记 open/low，升级待逐条核验另裁）+ B11=A（L06↔P02 挂接确认）+ B12=A（stash@{0} 原样保留）。对应关系核实：PD-Q5 原文「V13–V20 升级」实为 V13/V14 两张升级票（D18）+ V17–V20 登记确认（D19/B10），不存在 V15/V16 裁决票。 |
| PD-Q6 | P2 试点方向：A 增量增强 vs B 重设计（PILOT-L13-plan.md） | **若 PD-Q7 批准则顺延**至解冻条件满足（P7 稳定+P8 闭环+P9 一次 run+发布边界明确） | 阶段 C 前置 | ⏸ 已按 PD-003 顺延（冻结至解冻条件满足）；**2026-11-21 六阶段计划批准后顺延状态被覆盖**：试点 A 已执行（Engine `4945711`：L13 六项增强 + SKILL draft→active + Floor L13/L19 双 PASS），LXD 全面铺开转为 Engine 内部工作流（见 ROADMAP P1'），不独立成仓 |
| PD-Q7 | **范围裁剪提案 PD-003**：单活跃线 Engine；P2 Skill/P03/P04 冻结在现有成果；不新建知识库/skill 收录项目 | 批准（与两份引导附件 §10–§11 结论及用户 01–04 优先序一致） | 停止战线扩张；冻结≠删除 | ✅ 批准（2026-11-19 用户指令），PD-003 accepted |
| PD-Q8 | Render_Notes 内 program-office-delivery/ 交付副本清理（未跟踪 .md，会污染知识 bundle） | 安全删除（回收站可恢复）；权威原件在办公室 | 防重演 .zcode 污染 | ✅ 已执行：10 份副本→回收站（可恢复）；.qoder-input-images/ 加入 gitignore |
| PD-Q9 | 是否把 LXD 实验页试点推广到其余 6 个实验（补实验目标 / 观察记录 / 键盘提示；对比度与复选框关联已对所有实验生效） | 首批验收后做，每批 2–3 个实验，独立小提交 | 不做：6 个实验仍缺实验目标与观察记录 | |
| PD-Q10 | 是否给学习站补一个最小的课程切换入口（当前教材模式只展示主课程，具身课程只能从首页目录或搜索进入，课后测验走不到） | 补，属发布体验缺陷修复而非新功能；范围限定为切换入口 + 测验可达 | 不做：具身课程的两条学习路径残缺，六课"实践与可验证性"各被扣 2 分 | ✅ 已关闭（2026-11-26，D22 P0 实现）：多课程切换条（主课程/具身/pilot）+ 检查点练习嵌入站点（11 份/38 题），浏览器 QA 通过；pilot 课程上下文缺陷另于本日修复（`reviews/consolidation-qa-pilot-context-20261126.json`） |
| PD-Q11 | 是否把 15 项源勘误反馈给 Robot_Learn 所有者（源库只读，Engine 已按正确表述撰写并注记） | 反馈；先由用户过目勘误表（Engine G1 队列 §3） | 不反馈：源头错误保留，下一个读者仍会被误导 | |
| PD-Q12 | 是否接受 Governance 的 `level` 字段可空（P0 修复中采纳的一处 schema 调整） | 接受（`level` 本就不是必填，原 schema 与 CLI 不一致） | 不接受：可单独回退这一行，示例项目 doctor 会重新失败 | ⏸ 转非活跃（2026-11-26）：Governance 已随 D22 归档至 `legacy/`（只读不维护），不再作为当前活跃人工决策；schema 调整保留在归档代码中，如重新启用 Governance 再议 |
| PD-Q13 | 是否补做 2026-11-24 任务书的审计档案归档（`audits/2026-11-24-post-implementation-audit/`，会话中断未执行；ROADMAP 有指针指向不存在的目录） | 补做，纯文档归档 | 不补：原始 GPT 审计与本机核实结果只留在会话记录里 | ✅ 已关闭（2026-11-26，D22 补档）：`program/audits/2026-11-24-post-implementation-audit/` 已建（README/GPT-AUDIT-REPORT/LOCAL-VERIFICATION/AUDIT-DISPOSITION 四件齐全），ROADMAP 指针不再悬空 |
| PD-Q14 | Governance 与 Engine 的文档类型映射（Engine 的 `review-material` / `agent-plan` / `kcr` / `knowledge` 等不在 Governance 13 类枚举；真实 Engine 副本上 `validate` exit 1、`doctor` exit 1） | 暂不处理；在 Governance 文档里写明"不适用于 Engine 知识文档"，等第二个真实项目出现再决定是否做映射 | 不处理：Governance 对 Engine 只能做安全 init 与索引，校验不可用 | ⏸ 转非活跃（2026-11-26）：Governance 已归档至 `legacy/`，Engine 文档治理由自身 registry/validate 门禁负责（不再依赖 Governance 校验）；类型映射不再是当前活跃决策，如重新启用再议 |
| PD-Q15 | 对 Radar 真实库 `radar-real-20261121.db` 执行 `init-db`（补 approver 等三列；副本验证通过，真实库仍为旧结构） | 批准后执行；执行前后记录 SHA256 与行数 | 不做：真实库继续停留在修复前结构，`--approved` 在真实库上无法写入 | |
| PD-Q16 | Engine 的 GitHub 仓库为 Public，`reviews/`、`.agent/`、`.governance/` 等内部材料已公开可见（站点发布边界 v2 不管 git 仓库） | 维持现状并在 README 注明"仓库含内部过程材料"；或改私有 | 不处理：内部审读与裁决材料持续公开 | ◑ 部分执行（2026-11-26）：提交作者的公司邮箱已通过全历史重写从公开历史移除（作者统一为 GitHub 身份 `Vin535LFJ` + noreply）；「内部材料公开可见」主体问题维持现状待裁决 |
| PD-Q17 | 本轮产物提交与 10 笔推送（Engine 9 笔 + Skills 1 笔，另加本轮未提交项） | 先提交本轮产物，再普通 push（单次代理参数，不 force） | 不推：全部成果只在本机 | ✅ 已执行（2026-11-26）：分批提交 + 普通 push 完成（Engine 10 笔 / Skills 2 笔）；随后按用户指令全部重写提交作者（公司邮箱 → GitHub noreply），公开仓 `--force-with-lease` 强推，ls-remote 核实一致 |

### PD-Q9 至 PD-Q17 详述（2026-11-25 登记；2026-11-26 状态更新：Q10/Q13/Q17 已关闭，Q12/Q14 转非活跃，其余仍待决）

| 编号 | 背景 | 影响 | 推荐方案 | 不处理的后果 | 是否阻塞六课发布 |
|---|---|---|---|---|---|
| PD-Q9 | LXD 第二案例只在 transform-mvp 一个实验页做了"实验目标 / 观察记录 / 键盘提示"；公共样式修复已覆盖全部 7 个 | 其余 6 个实验结构上仍缺目标与观察记录 | 首批验收后分批补，每批独立提交并复测 | 6 个实验保持现状，可读性硬伤已修、结构缺口仍在 | 否 |
| PD-Q10 | 学习站教材模式只读主课程 | 具身课程无教材模式、课后检查点测验不可达 | 补最小切换入口（范围见 Engine `independent-review.md` U1） | 两条学习路径残缺 | ✅ 已关闭（D22 P0 实现 + pilot 上下文修复） |
| PD-Q11 | Robot_Learn 源文有 15 处错误或歧义 | 源库只读，Engine 已按正确表述写 | 用户过目勘误表后决定是否反馈 | 源头错误保留 | 否 |
| PD-Q12 | Governance P0 修复中把 schema 的 `level` 放宽为可空 | 与 CLI 实际写入一致 | 接受 | 回退后示例项目 doctor 失败 | ⏸ 非活跃（Governance 已归档） |
| PD-Q13 | 2026-11-24 任务书 TASK 3 未执行 | 审计原始材料未归档，ROADMAP 指针悬空 | 补做归档（只读材料整理） | 审计链不完整 | ✅ 已关闭（D22 补档，四件齐全） |
| PD-Q14 | 本轮副本验证发现（见 `plans/2026-11-25-stabilization-verification.md` §3） | Governance 的校验对 Engine 不可用 | 暂不处理，文档写明适用范围 | 误以为已校验通过 | ⏸ 非活跃（Governance 已归档） |
| PD-Q15 | 真实库仍是修复前结构 | 真实库上无法使用人工批准写入 | 批准后执行并留痕 | 真实数据与已验证代码不同步 | 否 |
| PD-Q16 | 仓库公开且含内部材料（既有状态） | 审读、裁决、运行态材料对外可见 | 维持并注明，或改私有 | 持续公开 | 否 |
| PD-Q17 | 10 笔已提交未推送 + 本轮未提交项 | 成果只在本机 | 先提交本轮产物，再普通 push | 本机丢失风险 | ✅ 已关闭（提交+push+作者重写完成） |

## 已按默认执行并记录（低风险，可推翻）

- Program 位置与名称：办公室 `ai-knowledge-program`（PD-001，用户指令授权）。
- ~~索引而非迁移（PD-001）~~ → **已被 PD-002 取代：四项目物理集中到 `GITCODE\AI-Knowledge\`**（用户本轮指令）。
- 本轮复跑 P03/P04 测试与 Render_Notes 只读门禁取证（只读动作）。
- PD-Q1 收口路径已随 PD-002 变为 `AI-Knowledge\Render_Notes`（现 `ai-knowledge-to-learning-engine`）；该三批已于 2026-11-19/20 收口提交并 push（见 Engine CHANGELOG 与 D17），此行仅历史记录。