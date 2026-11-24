---
doc_id: PROG-NOW
type: program-state
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-24
---

# NOW · 当前唯一主目标

> **最近状态更新：2026-11-24 18:30（embodied 首批 RESEARCH 完成 + 工具链扩展落地）**：① **工具链多课程最小扩展已批准并落地**（validate §10 independent 命名空间 / build_site courses[] / allowlist 08-具身智能；夹具演练通过/FAIL 对照/现场恢复）。② **RESEARCH 完成→EVIDENCE**：08-具身智能/ 七份提取文档、V68–V84 全 open/low（**101 claims=24v/70o/7c**）、来源 52、独立复算 70/70、外部核验 3 项（Tobin/DAgger/MJWarp FAQ）、源勘误队列 12 项登记不擅改；Robot_Learn 只读零改动。③ 门禁全绿：build 92 docs/641 cards · validate 12/0/0 · publish 12/12 · arc 19/19 · kcr 16/16 · runstate 25/25 · registry 195。④ 前批文档治理+公式修复已提交（Engine `46a04d3` / Program `8c718ac`，未 push；Engine ahead 2 / Skills ahead 1）。**本批改动未提交待授权**。积压：G2 历史 17 篇 / U1–U3 / P07 / C1–C7 / 审计 §E 整改 / 源勘误反馈裁决。
> 本文件是带日期的项目级快照，**不是第二事实源**。
> **接管交接入口：`handoffs/2026-11-21-p10-handoff.md`**（GLM 5.3 Flash 接管，自包含 + 启动提示词；2026-11-21 16:16 实测快照）。
> Engine 内部权威状态：`ai-knowledge-to-learning-engine/WORKFLOW_STATE.md` / `DECISIONS.md` / `reviews/REVIEW_STATUS.md`。冲突时以项目内文档 + git 实测为准。

## 唯一主目标

**P10.3 多领域课程复用：embodied-loop-journey《具身智能：一条指令如何变成物理动作》**——复用已验证的生产链（run_state 全链 + 共享 Evidence/Glossary/Skills），源参考 `C:\Users\Giant\Desktop\GITCODE\Robot_Learn`（**只读**，具身智能知识库）；**LXD 全面铺开为内部质量工作流**（新页面直接按六项增强+Floor 标准建；既有 19 课分批增强，不另开战线）。kickoff **已批准**（2026-11-23，课程名+首批 6 课）：`plans/2026-11-23-embodied-course-kickoff.md`；run `RUN-2026-11-23-embodied-batch1` 已开工（INTAKE→RESEARCH 完成→**EVIDENCE**，2026-11-24）。

> 上一主目标（Engine 生产链端到端）**已于 2026-11-21 达成**（P10 done，D20）；六阶段总验收见 `final-acceptance-2026-11-21.md`。Governance/Radar 已解冻并真实验证，此后按需维护、无持续真实需求不追加投入（PARKING-LOT）。

## 当前进度（2026-11-24 更新）

| 项 | 状态 | 证据 |
|---|---|---|
| Engine 主目标 P10 | ✅ **done（2026-11-21）** | run FEEDBACK/done、G3 passed、18 artifacts、D20、G2=91 用户本人 |
| push 收口 | ✅ 2026-11-23 用户授权 | Engine `79c3fe8`（含回执笔）/ Skills `7326522` = 远端（ls-remote 实测）；审计文档笔未 push |
| LXD | ✅ 试点 A + SKILL active | Engine `4945711`；Floor L13/L19 双 PASS；全面铺开转入新主线工作流 |
| Governance / Radar | ✅ 解冻验证完成（审计 PARTIAL） | `1b4a880` / `b7442da`（121 仓周报）；独立审计发现见 `AUDIT-REPORT.md` §C/§D；按需维护 |
| 门禁终态 | ✅ 全绿 | validate 12/0/0 · publish 12/12（新增公式保护回归门禁）· 84 claims（24v）误标 0 · kcr 16/16 · runstate 25/25 · arc 19/19 |
| 下一主线 | 🔄 EVIDENCE（RESEARCH 完成，工具链扩展已落地） | run `RUN-2026-11-23-embodied-batch1`；下一步 G1 队列→ARCHITECT→WRITE 6 课 |
| 人工积压 | ⬜ | G2 历史 17 篇 / U1–U3 / P07 / C1–C7 / 审计 §E 整改（源笔误×2 已随 D21 修正） |

## 程序级并行任务：仓库命名统一（✅ 已完成，2026-11-20 T1 执行完毕）

- **已完成**：本地目录改名（2026-11-19）；**GitHub 两仓改名（用户手动，2026-11-19 核实）**——ls-remote 新 URL 实测：Engine 远端 HEAD=`e848d2801ec9940e154b9bf40bc26198a5d197ba`、Skills 远端 HEAD=`e1936f23e6e149c581124cc218e79860c07108ef`（2026-11-20 复核远端可达）。
- **T1 收尾已完成（2026-11-20，实测已留痕）**：remote set-url ×2 切换至新 URL（Skills upstream-en/zh 未动）→ 锚定引用更新完成（含品牌文案 + README 正式名/标准描述；Engine 24 文件、Skills 5、Program 5、OmniWorld 5）→ 全量验证通过，六道门禁全绿（build **69 documents/17 sections/124 terms/19 lessons/7 labs/504 cards/2426 KB** · validate **11 checks passed, 0 warnings, 0 failures** · arc **5 篇 · OK** · review_gate **37 claims**（verified 18 / open 12 / conditional 7，conditional/contested 误标 verified 无）· publish boundary exit 0 · check-translation exit 0）；残留清点：本地回填注释 **4 个文件（预期 4）**、活跃层残留 26 条、`claude plugin validate . --strict` 本机无 claude CLI **待验（不算失败）**→ OmniWorld-Engine 跟进（Q4）完成（`skills-lock.json` **37 条全部指向 `Vin535LFJ/matt-pocock-skills-zh-cn`**，旧 slug 0 条；AGENTS.md:74 安装命令已指新 URL，pin `skills@1.7.1` 保留）。笔① `cf917386e22af0cf0a4a9b665fc48d41c1ca9130`（Engine 本地提交，未 push）。步骤依据：`handoffs/2026-11-19-program-handoff.md` §3 T1；实测详情：Engine `CHANGELOG.md` 2026-11-20 T1 条目 + `plans/2026-11-19-rename-audit-and-migration.md` 执行实测段。
- 过渡态已消除：旧 URL 重定向兜底不再依赖；引用更新改动已随 T1 提交并于 2026-11-23 经用户授权 push 收口。

## Engine 真实状态审计（2026-11-19，按任务书 §08 分类；依据 WORKFLOW_STATE / NEXT_PHASE_PLAN / 本会话实测）

| 分类 | 内容 |
|---|---|
| ✅ 已完成（有实测证据） | P0–P6、B1–B5、V3-Loop1；P7.1 四篇 blocker（L02/L06/L11/L13）；D14/D15 治理基座；发布边界 allowlist；三批收口 push；物理迁移 |
| 🔄 部分完成 | P4 VitePress（源码树完成，docs:build 被权限拦截，D10.6）；V3-Loop2（Category A 已执行，P7.2 未启动）；P8 仅预研（kcr_impact.py 只读工具 + allowlist）；P9 仅设计稿 |
| 🗑 过时 | NEXT_PHASE_PLAN"待用户拍板"第 1 条（L02 目标取舍 B1 已决）；WORKFLOW_STATE 迁移待办（本会话已修正）；旧 build 数字 48/77（现 69 docs） |
| 🔁 被替代 | "19 课写完才算完成"的旧口径 → 被 PD-003/P10"一批新资料端到端验收"取代；重型 Orchestrator 设想 → 被 P9 轻量 JSON 状态机取代 |
| ⛔ 实际阻塞 | **decision-kit 裁决阻塞已解除（7/7，D17–D19）**；剩余人工事项：G2 评分表填写（关卡正式通过）、GitHub 仓库改名同步、commit 授权；在线发布 D02 未授权 |
| ⬜ 未启动 | P7.2 逐篇深化、P8 生产化（输入合同/Evidence 扩展/KCR 闭环）、P9 状态机、P10 端到端验收 |

**当前真正最重要的一项工作**：**embodied-loop-journey 首批 EVIDENCE→ARCHITECT→WRITE**（RESEARCH 已完成：08-具身智能/ 七份提取文档 + V68–V84 open/low + 独立复算 70/70 + 外部核验 3 项；工具链多课程扩展已批准落地）。下一步：G1 核验队列（白皮书名称/BEVFormer NDS/前沿模型数字）→ 概念/术语注册 + course.json（independent）→ 6 课教材（LXD 六项增强+Floor 直接建）。积压（不阻塞）：G2 历史 17 篇评分（L19 模式可分批）；U1–U3/P07/C1–C7 研究队列；源勘误队列 12 项是否向 Robot_Learn 所有者反馈待裁决。另批事项：P10.3 其他领域、PD-Q3 远程、在线发布 D02。前批治理+公式修复已提交（Engine 46a04d3 / Program 8c718ac，未 push）；本批 RESEARCH 改动待授权提交。

## 裁决状态：decision-kit 七项全闭合（2026-11-19，D17/D18/D19）

| 项 | 裁决 | 执行 |
|---|---|---|
| B4 | B 认可 L01 为 Gold Standard + minor 修订 | ✅ §4.2 记号精确化 + V13 表述三处同步修正 |
| B15 | A C1–C7 全部立项 | ✅ 入研究队列，执行按 P8 节奏 |
| V13 | A 修正后升级 verified/high | ✅ 台账升级（依据 D12.7 权威核验） |
| V14 | A 升级 verified/high + 保留平台条件 | ✅ 台账升级，两条 conditions 保留 |
| B10 | A 确认 V17–V20 登记 open，升级另裁 | ✅ 确认现状，状态不变 |
| B11 | A 确认 L06↔P02 保留挂载 | ✅ 确认现状 |
| B12 | A stash 继续保留 | ✅ 未触碰；本轮提交稳定后重议 |

门禁（D19 后复跑）：validate **11/0/0**；review_gate **37 claims（18v/12o/7c）误标 0**；build 69 docs / arc 5/5 / publish 11/11（D18 后实测）。
**注意**：G1/G2 的裁决项已闭合，但关卡本身仍待人工宣布通过（G2 评分表 review-report.md 待填，AI 不自评）；G3 未通过、在线发布 D02 未授权。

## 当前主任务（教材生产 ✅ 18/18 完成；P8-MVP ✅ 三片；P9 ✅ 状态机；下一步 P10 端到端验收）

**P7.2 逐篇深化教材**：以 Gold Standard L01 + lesson-quality-standard 为基准，按认知依赖一次一篇，每篇跑门禁 + 留痕。
- **第一篇 L02《时间戳与同步》✅ 完成（2026-11-20，审读 acceptable=true、修订 0 轮）**：正文 125 → 217 行（frontmatter 一字未动）+ quiz 更新（Q1/Q2/Q4 prompt 与 checkpoint 逐字一致保持，新增 Q5 挂 V03 / Q6 挂 V10）；**未新增断言**（newClaims=[]，正文重要结论均由既有 V03/V10/V15/V16 或主文档 ✅/⚠️ 锚点覆盖；claim-ledger.json 未改动）。**门禁实测（全 exit 0）**：build **69 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2459 KB** · validate **11 checks passed, 0 warnings, 0 failures** · arc **5 篇 OK** · review_gate **conditional/contested 误标 verified 无**（未挂载课程 claim 仅 ['P03']，open/conditional 可预期）· publish boundary exit 0。审读遗留 7 条（1 major：labs.json/app.js「DTS ≤ PTS 恒成立」静态句与 lab 模型 B0 及 L02 五帧表冲突，涉 `web/assets/app.js:2350`；6 minor）与 openQuestions 5 条（含 objectives 三层措辞漂移、glossary AV Sync「recover」词条口径）待人工/后续处理，详见 Engine `reviews/G2-L02-deepening.md` 与 Engine `CHANGELOG.md` 2026-11-20 P7.2 条目。未 commit。
- **第二篇 L06《纹理桥与零拷贝》✅ 完成（2026-11-20，审读 acceptable=true、修订 0 轮）**：正文 85 → 200 行（frontmatter 仅 claims 追加 E01，属三处齐挂扩展；其余字段一字未动）；**未新增断言**（newClaims=[]，P02 如实保持 open/low contested、C02 conditional 如实）；两层 course.json checkpoint 补第 3 题与 quiz Q3 四处联动；审读 40 处技术表述 39 处逐条溯源、11 条 minor 全部修复（含锚点升级与实验显示名对齐 labs.json）。**门禁实测（全 exit 0）**：build **69 docs / 504 cards / 2497 KB** · validate **11 checks passed, 0 warnings, 0 failures** · arc **5 篇 OK** · review_gate **37 claims 误标 0** · publish boundary **11 tests OK**。详见 Engine `reviews/G2-L06-deepening.md` 与 Engine `CHANGELOG.md` 2026-11-20 P7.2 第二篇条目。未 commit。
- **第五篇 L03《色彩与显示范围》✅ 新写完成（2026-11-20，「其余篇目」首篇，审读 1 blocker + 8 minor 修复后通过）**：0 → 168 行（非 pilot 课，无 quiz——validate §10 规则实测并如实留痕）；**新登记断言 V21–V24**（open/low，SRC-RN-COLORMGMT 双向索引）；审读 blocker = 有效灰阶三处口径互斥，已统一（黑 6%/白 92%/可用 86%）。**门禁实测（全 exit 0）**：build **70 docs / 512 cards / 2599 KB** · validate **11/0/0** · arc **6 篇 OK** · review_gate **41 claims 误标 0** · publish **11 tests OK**（数量断言 69→70 同步）。详见 Engine `reviews/G2-L03-deepening.md`。未 commit。
- **第六篇 L04《从文件到码流》✅ 新写完成（2026-11-20，「其余篇目」第二篇，审读 acceptable=true / 0 修订轮 / 40 处全溯源）**：0 → 199 行；**新登记断言 V25–V26**（open/low，SRC-RN-AV-BASE）；既有 V01/V11（verified）预挂转正；审读 9 条 minor 全部修复（含 L03 桥句联动更新）。**门禁实测（全 exit 0）**：build **71 docs / 520 cards / 2642 KB** · validate **11/0/0** · arc **7 篇 OK** · review_gate **43 claims 误标 0** · publish **11 tests OK**（断言 70→71）。详见 Engine `reviews/G2-L04-deepening.md`。未 commit。
- **第七篇 L05《硬解与 ownership》✅ 新写完成（2026-11-20，审读 1 blocker + 1 major + 8 minor 修复后通过）**：0 → 175 行；**新登记断言 V27–V28**（open/low，SRC-RN-VERIFICATION）；C03（conditional）预挂转正；审读 blocker = "openQuestions 已登记"查无实据——已做实（flush 候选登记验真队列 **P07**）；major = 搬运账口径与源失实已修正；台账反向索引双向修正（C01 移除 L05/V01 增补 L05）。**门禁实测（全 exit 0）**：build **72 docs / 528 cards / 2681 KB** · validate **11/0/0** · arc **8 篇 OK** · review_gate **45 claims 误标 0** · publish **11 tests OK**（断言 71→72）。详见 Engine `reviews/G2-L05-deepening.md`。未 commit。
- **第八篇 L07《GPU 为什么快》✅ 新写完成（2026-11-20，审读 1 blocker + 2 major + 6 minor 修复后通过）**：0 → 150 行；**新登记断言 V29–V32**（open/low，新增 SRC-RN-GPU-BASE）；审读 blocker = 7.9 MB 二进制口径与 8.29 MB 十进制冲突（MB/MiB 纪律），已双口径统一；2 major = L06/L11 机制归属错位与小节号错位 3 处，已修复。**门禁实测（全 exit 0）**：build **73 docs / 536 cards / 2717 KB** · validate **11/0/0** · arc **9 篇 OK** · review_gate **49 claims 误标 0** · publish **11 tests OK**（断言 72→73）。详见 Engine `reviews/G2-L07-deepening.md`。未 commit。
- **第六篇 L09《移动端瓶颈与 TBDR》✅ 新写完成（2026-11-20，审读 1 blocker + 7 minor 修复后通过）**：0 → 153 行；**新登记断言 V36–V38**（open/low，SRC-RN-RASDEPTH）；审读 blocker = "三倍带宽"修辞无据（RMW 实为两次传输对一次、源只给机制不给倍数），已改为按账实测表述。**门禁实测（全 exit 0）**：build **75 docs / 553 cards / 2790 KB** · validate **11/0/0** · arc **11 篇 OK** · review_gate **55 claims 误标 0** · publish **11 tests OK**（断言 74→75）。详见 Engine `reviews/G2-L09-deepening.md`。未 commit。
- **教材线已清空（2026-11-20 批量收官）**：L10/L12/L14/L15/L16/L17/L18 七篇本日新写并独立审读修复，18 份课时教材齐备（L00 地图课无独立教材）。以下逐篇记录为历史留痕。
其后顺序固定：**P10 一批新资料端到端验收**（= 主目标达成；用 run_state 真实 run 走全链，G1/G2/G3 人工门实测）；P9.4 工具盘点（G-W3）与研究队列 C1–C7 穿插，不阻塞主线。

## 验收标准（主目标 = P10 端到端）

一批全新真实资料完整走通：导入 → 查重 → 研究 → 证据提取 → 知识建模 → 学习路线 → 教材 → 实践练习 → 人工审核 → 交互式网站 → 状态留痕。完成标准关注：
- 工作流可重复执行；中间产物有明确数据契约；各阶段有质量检查；关键人工审批点明确；
- 生成结果在网站正常呈现（可用、清晰、基本美观，不要求完整设计方法论）；
- 知识变更可做影响分析（KCR）；失败可定位与恢复（断点续跑）。

不要求第一轮完成所有历史课程与全部教材——先证明生产链能工作，再扩大规模。

## 遗留事项（不阻塞主线，登记待处理）

1. Render_Notes 旧名/旧路径引用已于 2026-11-24 文档治理分类处理：活跃文档口径已修正（Program PROGRAM/NOW、Engine README/allowlist）；历史叙述（CHANGELOG/DECISIONS/reviews/P6 快照）按原样保留；六份 P6 过程文档已移入 Engine `archive/process-history/`。
2. VitePress 本地构建被删除权限拦截（D10.6）；如需验证由用户手动放行其自身临时目录清理。
3. G3 发布审核未通过；在线发布（D02）未授权——本阶段不发布。
4. 程序级 PD-Q3（远程创建）/ PD-Q4（Radar PAT）随冻结顺延，见 PARKING-LOT。