# 工作流状态（WORKFLOW_STATE）

> 用于断点续跑：记录当前阶段、完成度、待办、审核关卡与续跑点。每阶段结束更新一次。
>
> 计划：会话级批准产物，原件位于用户目录 `~/.workbuddy-ai/plans/quantum-nebula-newton-ffFN4E3P.md`（不入仓库） · 裁决：`DECISIONS.md`（D01–D14）

**最后更新**：2026-11-26 18:25（**D22 统一收敛完成**：五项目→两仓；备份 6/6 PASS；program/legacy/integrations 并入；run_state 依赖检查 28/28；多课程切换+quiz 检查点上线并浏览器实测；门禁全绿 validate 20/0/0 · publish 33 · 105 claims 误标 0。**续跑点**：embodied run REVIEW/paused 等用户 G1/G2/G3/KCR；D22 产物分组提交+推送待执行；详见 docs/consolidation/FINAL-ACCEPTANCE-REPORT.md）

**前次记录**：**最后更新**：2026-11-26（**提交作者统一重写（用户批准）**：42 笔提交的作者/committer 由 `fangjun <lifangjun@mgtv.com>`（含 2 笔个人邮箱）统一为 `Vin535LFJ <169535939+Vin535LFJ@users.noreply.github.com>`；tree 哈希前后一致（`173c3793…`）、`git diff refs/original..HEAD` 为空，内容零改动；重写前 HEAD=`6af1871`，重写后（注记提交前）HEAD=`ecab4b9`；全部旧 SHA 失效，`refs/original` 保留本地回滚备份；已 `--force-with-lease` 推送并 ls-remote 核实。历史材料中的旧 SHA 均指重写前历史）。前次记录：2026-11-25 22:35（**方案甲修复执行完毕（用户批准）**：验收包 §6 的 11 项最小修复全部落地：E06 L113（θ2 是不是 0° 或 180°）、L160 答案指向与覆盖范围说明、L90 小节标题；V83 的 CPU 行出处（MuJoCo 官方文档 Reproducibility 节）在课文、测验、课源、台账、术语表同步；课源 `06` 关联断言补 V86 / V87；E03 §4.5 补登记 **V88**（open / low）并挂接；G1 队列口径更正并扩为 V68–V88。独立审读员复核：9 项改动全部修对，无新的事实错误（`reviews/embodied-batch1/recheck-planA-fixes.md`）；其指出的 6 处收尾问题 5 处已处理、1 处（"逐位"措辞）判定无需改。用户验收包 `USER-ACCEPTANCE-PACKAGE.md` 与修复前专项复核 `targeted-recheck.md` 已备齐，**裁决栏留空**。run 仍 **REVIEW / paused**（G3 open，KCR REVIEWING），10 个本轮改动或新增的产物已重新登记哈希（33 条记录，24 个文件哈希全部有效）。断言状态未变：105 claims（24 verified / 74 open / 7 conditional），V68–V88 仍全部 open/low。门禁：validate 20/0/0 · publish 32 · arc 两门课程 0 FAIL · 三套自测 25/16/15 · Floor 6/6。本轮全部改动**未提交、未推送**。等用户：G1 裁决 → G2 评分 → 登记审批 + G3 → KCR；PD-Q9 至 Q17；提交与推送授权。续跑点 = 按用户 G1 裁决更新台账与课文状态说明 → 重建门禁 → 用户确认文件不再改动后登记审批。前次记录：2026-11-25 19:40（**2026-11-25 任务书 TASK 0–6 全部执行完毕**：发布边界 v2 PASS / 具身六课 PASS WITH LIMITATIONS / Radar 与 Governance P0 已修 / 审批证据链 PASS WITH LIMITATIONS / LXD 第二案例 PASS WITH LIMITATIONS / **Skills 实机验证 PARTIAL**（QwenWork：安装成功、设置清单可见，本会话内发现与加载失败，技能目录在会话开始时固定，新会话未验证）。根 `AGENTS.md` 补技能指针（`4951d99`）。逐项结论见 Program `plans/2026-11-25-stage-execution-report.md`。**等用户**：embodied G1 / G2 / 审批登记 + G3 / KCR；push（Engine 领先 9 笔、Skills 1 笔）；Skills 新会话验证；LXD 试点是否推广；课程切换入口；源勘误反馈。续跑点 = 用户裁决后 resume → PUBLISH → FEEDBACK → done。前次记录：2026-11-25 19:03（**LXD 第二案例完成（TASK 5）**：transform-mvp 交互实验页——真实浏览器基线（7 实验 × 3 档宽度 × 明暗主题）发现浅色主题内容小字对比度 3.04:1、7 个实验均缺实验目标/观察记录/键盘提示；最小增强后对比度 6.39:1、复选框关联文字、试点页补目标 3 条 + 观察记录 + 键盘提示；7 个实验冒烟零报错，画布输出与分阶段数值与基线逐项相同。Skill 发现：宿主技能目录未收录，仓库内入口指针三步链路可用。未推广到其余 6 个实验（待用户确认）。记录 `preview/PILOT-LAB-mvp.md`。门禁：validate 20/0/0 · publish 32 · 三套自测 16/25/15 · 104 claims 误标 0 · registry 209。续跑点 = TASK 6 Skills 实机验证 → 阶段执行报告。前次记录：2026-11-25 18:48（**审批证据链持久化（TASK 4）完成**：新增 `tools/approval_chain.py`——人工 `record` 把 run 全部产物冻结为路径+SHA256+阶段并写入 `reviews/approvals/<run>/<gate>-NN.json`（只增不改，记提交号与未提交数）；`verify` 重算比对；`run_state.advance` / 人工 `skip` 进入 PUBLISH / FEEDBACK 必须通过复核（文件变化 / 产物被移走 / 越权新增 / 记录改坏 / 无记录均拦截）。第五契约 approval-record；历史 HDR 批次 G1/G2/KCR/G3 如实标 legacy/unverifiable，不补造。自测 approval 15/15 + runstate 25/25 + impact 16/16；真实数据演练：具身 run 21 个产物哈希失效 0，HDR run 16 个里 6 个失效（历史，无快照）。门禁：validate 20/0/0 · publish 32 · 104 claims 误标 0 · registry 208。续跑点 = TASK 5 LXD 第二案例 → TASK 6 Skills 实机验证 → 阶段执行报告。前次记录：2026-11-25 18:41（**具身六课独立审读闭环（TASK 1）；Radar / Governance P0 已提交**：首轮三位独立审读（1 blocker / 18 major，完整报告断网丢失）→ 修复 → 独立复审（抓出修复新引入 1 major）→ G2 诊断（E06 整改前 82）→ 整改（补登记 V86、V87；台账三处与课文同步；源勘误 12 → 15 项）→ 复评，**六课建议分 88 / 91 / 91 / 92 / 90 / 88，全部 ≥85**（AI 诊断建议分，非裁决）。run `RUN-2026-11-23-embodied-batch1` = **REVIEW / paused**（23 artifacts，KCR REVIEWING，G3 open）。门禁：build 91 docs / 3130 KB · validate 20/0/0 · publish 32 · arc 两门课程 0 FAIL · 104 claims（24v/73o/7c）误标 0 · Floor 6/6 · registry 207。Radar `dbff9c7`（两项 P0，38 → 58 tests）、Governance `2ab2891`（示例 doctor exit 0 + AGENTS.md 幂等接入，28 → 41 tests）已复核提交。续跑点 = TASK 4 审批证据链 → TASK 5 LXD 第二案例 → TASK 6 Skills 实机验证 → 阶段执行报告。前次记录：2026-11-25 11:55（**发布边界 v2 审计收口，TASK 0 = PASS**：全链复核 `ae60f34`——注册表 108 资产零漂移、三消费者统一、旧 API 无残留；发现并修复唯一缺口「curated-data 已登记未呈现」：build 显式嵌入 `payload.curated`（强制校验）+ 每篇文档 `evidence`/`concepts` + validate e2（集合相等/哈希/引用只指向精选注册表）+ app.js「证据与概念」面板；不输出断言验证状态。回归测试 29→32。实测：泄露演练 build exit 2 / validate 4 FAIL；过期检测 exit 1；目录联接逃逸演练两种调用均拒绝（符号链接用例仍因无特权 skipped）；Edge headless 确认 E05 面板渲染。门禁：build 91 docs（72 public + 19 archive）/3106 KB · validate 20/0/0 · publish 32 · 在线镜像 72 docs 无 archive · 102 claims 误标 0 · registry 203。**embodied run 实况 = WRITE/running**（六课初稿 E01–E06 + quiz 已提交 `7a601ba`，未经独立审读）。续跑点 = TASK 1：六课独立审读 → 修复 → Floor → G2 材料；随后 Radar/Governance P0（子代理已完成改动，待复核提交）、审批证据链、LXD 第二案例、Skills 实机验证。前次记录：2026-11-25 10:19（**发布边界 v2 强制收口完成（TASK 0）**：实施前实测确认强制化代码此前未落地（仅注册表存在）；publish_boundary.py 重写为 v2 强制 API（默认拒绝/fail closed/excluded-internal 优先/路径安全）；build/validate/vitepress 三消费者统一走注册表；validate 新增第 13 节；app.js 归档不进搜索 + 只读标记；回归测试 12→29（28 ok/1 skipped：本机无符号链接特权）；真实仓库负向演练成立（未登记文件 → build exit 2 / validate 4 FAIL / vitepress 失败）；Edge headless QA 通过。门禁：build 84 docs/2865 KB · vitepress 65 · validate 14/0/0 · publish 29 · arc 19/19 · 101 claims 误标 0 · registry 195。TASK 0 = PASS WITH LIMITATIONS（符号链接实链接用例未能在本机执行；curated-data 呈现 UI 未实现，已登记 PARKING-LOT）。续跑点 = embodied EVIDENCE（主线不变）。前次记录：2026-11-24 19:17（**审计整改 TASK 2a：遗留内部审核材料移出课程目录**：G2-审核材料-P6.md git mv courses/video-rendering-journey/ → reviews/（内部审核材料不进学习站；审计 P1-4 遗漏点）；bundle 92→91 docs，注册表重建 195；门禁全绿 validate 12/0/0 · publish 12/12 · arc 19/19 · 101 claims（24v/70o/7c）误标 0。续跑点不变 = EVIDENCE：G1 核验队列 → ARCHITECT → WRITE 6 课；发布边界强制化（TASK 2b）随后执行。前次记录：2026-11-24 18:30（**工具链多课程最小扩展落地（用户批准+夹具演练）+ embodied 首批 RESEARCH 完成**：validate §10 independent 命名空间 / build_site courses[] additive / allowlist 08-具身智能；08-具身智能/ 七份提取文档落盘；V68–V84 全 open/low（101 claims=24v/70o/7c）+9 来源（52）；独立复算 70/70 + 外部核验 3 项（Tobin/DAgger/MJWarp FAQ）；源勘误队列 12 项登记不擅改；run RUN-2026-11-23-embodied-batch1 推进 **EVIDENCE/running**（2 artifacts）；Robot_Learn 只读零改动核实。门禁末次 build **92 docs/641 cards/3267 KB** · validate 12/0/0 · publish 12/12 · arc 19/19 · 101 claims 误标 0 · kcr 16/16 · runstate 25/25 · registry 195。续跑点 = EVIDENCE：G1 核验队列 → ARCHITECT（概念/术语+course.json independent）→ WRITE 6 课。前次记录：同日**公式乱码修复**：用户报告 3D变换与坐标空间 §4.3 公式乱码；根因 = build_site 术语注入不保护多行 $$ 块，NDC 被注入 Markdown 链接；修复 = PROTECT_PATTERNS 加 $$ 同行保护 + in_math 跨行状态；源 md 零改动；全 bundle 83 公式块 0 污染 + Edge headless 渲染 QA 7 KaTeX 块全过；回归门禁 test_no_term_links_inside_display_math，publish **11→12 tests**；validate 12/0/0 · 84 claims 误标 0。前次记录：同日**文档治理完成（用户授权移动/归档/删除）**：P6 过程文档六份移入 `archive/process-history/`（各加归档标注+索引 README，根目录只剩 7 份活跃文档）；allowlist 纠偏（移除 program-office-delivery/已移根条目，新增 docs/）；reviews/README.md 导航+Loop 1 历史标注；`.qoder-input-images/` 临时缓存走回收站（可恢复）；docs/USER-GUIDE 纳入 bundle，publish 断言 83→85；Program NOW/PROGRAM 口径同步。门禁末次 build **85 docs/628 cards/3168 KB** · validate 12/0/0 · publish 11/11 · arc 19/19 · 84 claims（24v）误标 0 · kcr 16/16 · runstate 25/25 · registry 187。未 commit/push；embodied run 不变（RESEARCH/running），续跑点 = RESEARCH 源提取 + 外部核验，工具链扩展报批并行等待。前次记录：2026-11-23 20:05（**两处源笔误修正完成（D21）+ embodied-loop-journey 首批 INTAKE 完成**：run RUN-2026-11-23-embodied-batch1 推进至 RESEARCH；查重 0 命中；源清单修订（facts.md 实为法规卷底本；textbook-embodied 实测 10 章）；**工具链多课程最小扩展报批中**（validate §10 independent 命名空间 + build_site courses[] + allowlist，WRITE 前需批准）；续跑点 = RESEARCH 源提取 + 外部核验。前次记录：**push 收口 + 下一主线登记**：用户授权 7 笔已推——Engine `e848d28..3115cad` 6 笔 / Skills `e1936f2..7326522` 1 笔，ls-remote 实测一致；六阶段全部闭环、**P10 主目标达成**（run done/G3 passed/D20/G2=91 用户确认/84 claims 24v 误标 0）；**下一主线 = P10.3 embodied-loop-journey 新课程（Robot_Learn 源，只读参考）+ LXD 全面铺开内部工作流**，kickoff 方案 Program `plans/2026-11-23-embodied-course-kickoff.md` 待批准开工；积压：G2 历史 17 篇 / 两处源笔误 / U1–U3 / P07 / C1–C7；门禁末次 build 83 docs/624 cards/3141 KB · validate 12/0/0 · publish 11/11 · arc 19/19 · kcr 16/16 · runstate 25/25。前次记录：**P10 done——Engine 主目标达成**：RUN-2026-11-20-p10-hdr 八阶段 18 artifact 全闭环；四件人工门全过——G1 六项升级 verified 24v/KCR APPROVED/G2 91 分用户本人确认/G3 gate --pass；阶段 2 LXD 解冻待试点、阶段 3 Governance 9/9 提交 6aec3d3+1b4a880、阶段 4 Radar 真实数据落地 b7442da、阶段 5 总验收见 Program 仓 final-acceptance-2026-11-21.md；DECISIONS D20 + CHANGELOG 2026-11-21 P10 done 条目） · **当前阶段**：P0–P6 + B1–B5 + V3-Loop1/Loop2 完成；P7.1 四篇 blocker 全部修复；**decision-kit 7/7 已决（D17–D19）**；T1 命名迁移收尾完成（2026-11-20，remote 已切新 URL）；**P7.2 进度：L02（125→217）/ L06（85→200）/ L11（85→193）/ L13（89→235）四篇深化（pilot 收官）+ L03（0→168）/ L04（0→199）/ L05（0→175）/ L07（0→150）/ L08（0→149）/ L09（0→153）六篇新写，独立审读均通过（L13 1 major、L03 1 blocker、L05 1 blocker+1 major、L07 1 blocker+2 major、L09 1 blocker，全部修复；L04/L08 首轮即通过）；新登记断言 V21–V24（COLORMGMT）/ V25–V26（AV-BASE）/ V27–V28（VERIFICATION）/ V29–V32+V34–V35（GPU-BASE）/ V33（GRAPHICS）/ V36–V38（新增 SRC-RN-RASDEPTH），均 open/low；验真队列新增 P07；review_gate **55 claims** 误标 0；bundle 69→**75 docs**（publish 断言 69→70→…→75 六次同步）；门禁实测 build 75 docs · 552 cards · 2800 KB（复核复跑更正，原记录 553/2790 为笔误）/ validate 11 checks 0 FAIL 0 WARN / arc 19/19 OK（全量更正 2026-11-21） / publish 11 tests OK，详见 CHANGELOG 2026-11-20 P7.2 十个条目与 reviews/G2-L02/L03/L04/L05/L06/L07/L08/L09/L11/L13-deepening.md 十份材料** · **续跑点**：**阶段已切换（2026-11-20 用户确认"继续推进下一个阶段"）→ P8 KCR 最小闭环**，启动检查点与三片切片范围见 `reviews/P8-KCR-kickoff.md`（**P8-MVP 三片完成 + 教材全部完成**：P8 片一/二/三见 kickoff §3c/§3d/§3e；L10/L12/L14/L15/L16/L17/L18 七篇本日新写并审读修复，18 份课时教材齐备；**P9 已完成 → P10 进行中（HDR 批次 run 暂停于 REVIEW 等人工门，2026-11-21）**；研究队列 C1–C7 按 P8 节奏执行；前置建议：先授权提交未提交文件（Engine 55 个））；L10《显式 API 与同步》及剩余篇目在 P8-MVP 后恢复 → P9 最小状态机 → P10 一批新资料端到端验收**；G1/G2 裁决项已闭合但**关卡本身仍待人工宣布通过**（G2 评分表待填）；G3 仍未通过 · **程序级裁剪生效（D16/PD-003）**：Engine 为唯一活跃线，P2 Skill/P03/P04 冻结在现有成果，不新建收录类项目 · **T1 命名迁移收尾完成（2026-11-20）：本地目录与 GitHub 两仓均已改名，remote 已切新 URL（旧名重定向不再依赖）**。

---

## 阶段进度

| 阶段 | 内容 | 状态 | 验收 |
|---|---|---|---|
| P0 | 护栏文档 + 基线门禁 | ✅ 完成 | 基线 build/validate 0 FAIL |
| P1 | 证据层 + 知识模型 + QA 扩展 | ✅ 完成 | claim/source 双向索引；concept 术语可解析；0 FAIL |
| P2 | 正式课程闭环（优先） | ✅ 完成 | 5 样章 arc 全 OK；quiz/frontmatter/链接全过 validate；浏览器验证干净 |
| P3 | 五个交互 demo | ✅ 完成 | 4 个新 lab（yuv/timeline/pipeline/dag）+ 既有 mvp/lathe/pbr；浏览器逐个验证交互 |
| P4 | VitePress 并存 | 🔄 源码树完成 | 生成器/配置/package 完成；npm install 成功；**docs:build 被权限阻止**（见下，D10.6 已知限制，未重试） |
| P5 | 收尾验收 | ✅ 完成 | 三重门禁 exit 0（validate 5 checks / 0 FAIL / 0 WARN；arc 5/5 OK）；浏览器 QA 两路全绿；review-report 只填自动检查、AI 不自评；未 commit/push（详见 CHANGELOG.md） |
| B1+B2 | validate 第 11 节 coverage | ✅ 完成 | 11 checks / 0 FAIL / 0 WARN；负向自检确认 FAIL 触发；checkpoint/quiz 覆盖 5/5 |
| B3 | Skill 角色契约 | ✅ 完成 | 补 4b/5b 角色 + practice-and-review.md；未建顶层 skills/ |
| B4 | review_gate.py | ✅ 完成 | 只读前置清单，G1/G2/G3 待人工；不写分数 |
| B5 | 学习反馈闭环 | ✅ 完成 | feedback.json + report_feedback.py + 离线前端 UI（localStorage 队列 + JSON 导出）；端到端验证通过；D04 偏离已授权 |
| P6 | 教材质量升级（Master Prompt V2.0） | ✅ 完成，待 G2 | 审计三件套 + 教材质量诊断（2+1 处 blocker）+ 课程覆盖矩阵 + Gold Standard L01 重写 + V13/V14 登记（open）+ 质量规范提案 + G2 材料；门禁 11 checks 0 FAIL / arc 5/5；D11 登记 |
| V3-Loop1 | 审核准备（Master Prompt V3.0） | ✅ 完成，待裁决 | reviews/ 7 文件（CURRENT_AUDIT/G1/G2/G3/REVIEW_STATUS/DECISION_REQUIRED/EXECUTION_PLAN_V3）；门禁复跑 11/0/0·arc 5/5；偏差登记（L01 239 行/31 claims·16 sources/build 69 基线/.zcode 污染）；A/B/C 分类；未改既有内容文件、未升级 claim、未填人工结论 |
| V3-Loop2 | 裁决后执行（部分） | 🔄 进行中 | D12 裁决记录 + D13 KCR 机制设计（reviews/KNOWLEDGE_CHANGE_REVIEW.md）；已执行 B2 路线（脚本验证 ALL CONSISTENT）/B5 README/B3 规范采纳/A1 数字/A3 build 排除.zcode/A4 导航补 U7/A5 K-STRIDE 改挂/C2 API 勘误/B9 Pass 统一；权威核验完成（G1 §7）；P7.1 L02 修复（V15/V16 open + 正文重写 + quiz）；门禁 11/0/0·arc 5/5·33 claims 误标 0；L06/L13/L11 待续 |

图例：⬜ 待办 · 🔄 进行中 · ✅ 完成 · ⛔ 阻塞

## P4 当前状态（如实记录，D10.6）

- `tools/build_vitepress_content.py`（stdlib-only）已产出 46 篇策展文档 + index.md + sidebar.generated.mjs。
- `site-vitepress/{package.json, README.md, .vitepress/config.mjs}` 源码三件套完成；`.gitignore` 已含全部生成物。
- `npm install` 成功（vitepress 1.6.4，126 packages）。
- **`npm run docs:build` 未完成**：vitepress 需清理自身 `.vitepress/.temp/` 构建中间产物，触发删除权限请求被用户拒绝。用户已选择"跳过构建，如实记录"。修复过的脚本：`vitepress build`（不带 `docs` 参数，根目录含 config）。
- 不伪造构建成功；后续如需验证：用户手动执行 `cd site-vitepress && npm run docs:build`（放行其自身临时目录清理）。

## 基线快照（P0 时实测）

- `python tools/build_site.py`：48 documents / 11 sections / 11 glossary groups / 124 terms / 8 units / 19 lessons / 3 labs / 376 term cards / 1983 KB。
- `python tools/validate_site.py`：`2 checks passed, 0 warnings, 0 failures`。
- Git：`master` @ `2dd62d2` 已推送；`README.md` 有用户未提交改动（chat 链接）；两份方案文档未跟踪。

## 人工审核关卡（方案要求，不可由 AI 自批）

| 关卡 | 位置 | 状态 | V3.0 审核材料 |
|---|---|---|---|
| G1 研究范围审核 | P1 证据层种子确定后 | ⬜ 待人工 | reviews/G1-evidence-review.md（31 claims，V13/V14 升级评估） |
| G2 课程大纲审核（最重要） | P2 `curriculum.md` 完成后 | ⬜ 待人工 | reviews/G2-curriculum-review.md（G2-01…06 重核） |
| G3 最终发布审核 | P5；本计划不发布，仅记录 | ⬜ 待人工（**仍未通过**） | reviews/G3-release-readiness.md |

统一裁决表：`reviews/DECISION_REQUIRED.md`（B1–B15，未回复不视为同意）。

## 审核评分（P5 人工填写）

见 `courses/video-rendering-journey/review-report.md`：事实准确性 25 / 知识连贯性 25 / 教学体验 20 / 实践能力 20 / 阅读体验 10，门槛总分 ≥85 且前两项各 ≥80%。**生成 Agent 不得自评通过。**

## 续跑指引

1. 读 `DECISIONS.md`（D01–D11）与 `reviews/REVIEW_STATUS.md` 确认审核分类。
2. **decision-kit 七项已全部裁决闭合（D17/D18/D19）**：B4=B（Gold Standard 认可+minor 修订已执行）、B15=A（C1–C7 全立项）、V13/V14=A（升级 verified/high）、B10/B11/B12=A（确认现状）。权威逐项状态以 `reviews/decision-kit/README.md` 总表为准。**续跑点 = P7.2 逐篇深化**；G1/G2 关卡本身仍待人工宣布通过（G2 评分表待填），G3 未通过。
3. 收到裁决后按 `reviews/EXECUTION_PLAN_V3.md` Loop 2：记录裁决入 DECISIONS.md → 执行 Category A（A1 数字更正/A3 build 排除 .zcode/A4 学习路径指南补 U7/A5 K-STRIDE 改挂/A6 Pass 勘误）→ P7.1 blocker（L02→L06→L13→L11）→ P7.2 逐篇深化（一次一篇）。
4. 每阶段/每篇跑门禁（本机 `py -3`，`python` 解析到 cygwin stub 不可用）：`py -3 tools/build_site.py` → `py -3 tools/validate_site.py`（0 FAIL/0 WARN）→ `py -3 .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py courses/video-rendering-journey/lessons/*.md` → `py -3 tools/review_gate.py`（只读）。
5. 改前端后额外做离线站浏览器 QA（file:// 与 http://localhost:8765 两路）；VitePress 构建需 B6 授权。
6. P6 产物 commit `3ce7b2f`+`0b2c0a1`+`650bb14` 已 push；**Loop 2 产物 commit `d4a9620`（27 文件，含 reviews/ 8 份）已 push**（2026-11-19 用户授权"同步最新更改到github"，`ls-remote` 实测远端 HEAD=`d4a9620`，本地同步）；**D14 结构治理 commit `f5d4ecf`（26 文件，.agent/ 统一仓库）已 push**（2026-11-19 用户授权"授权 commit + push"，远端 HEAD=`f5d4ecf`，本地同步）。B14：`.zcode` 计划已归档入 `.agent/plans/` 并随 `f5d4ecf` 提交；临时备份 `old_content.js.tmp` 已删除（用户授权，回收站可恢复）。后续默认不 commit/push，除非明确授权（D09/D11.9）；在线发布（D02）未授权。
7. 绝对不动：`.workbuddy-ai/memory/**`、`archive/**`、`web/vendor/**`、`web/index.html`、README（B5 前）、两份方案文档、已确认路线（B2 前）、claim 状态（G1 前）、stash（B12 前）、`.agent/**`（统一智能体文档仓库，结构变更走 DECISIONS 记录 + KCR）。外来产物：`.zcode/` 已按 B14 归档入 `.agent/plans/` 并提交、空目录已移除（D14）；临时备份 `old_content.js.tmp` 已删除（用户授权，回收站可恢复）。执行结果写入 `CHANGELOG.md` 与本文件。
8. 环境事实：2026-11-19 网络已恢复（github.com:443 可达），`ls-remote` 实测远端 HEAD=`d4a9620` 与本地一致；早期 DNS 中断已解除。
9. 结构变更（D14，2026-11-19）：智能体文档统一迁入 `.agent/`（技能文档 + zcode 计划）；`.workbuddy-ai/` 只留索引 stub + scripts + memory；三个构建工具排除 `.agent`；门禁命令路径不变（scripts 未迁移）。统一规则与索引：`.agent/README.md`。
10. 文档治理基座（D15/ADR-0001，2026-11-19）：`.agent/` 新增 constitution/decisions/standards/templates/changes/indexes 分区 + 全客户端适配入口（CLAUDE.md/AGENTS.md/.cursor/.github/.gemini，只跳转不复制）+ `tools/build_document_registry.py`（frontmatter 事实源生成注册表，实测 104 篇）；三个构建工具排除适配入口；`.gitignore` 追加 `.agent/runs/`。**已提交**：D15 基座随收口第一笔 `5a4de84` 入库（D16/PD-Q1）。
11. T1 命名迁移收尾完成（2026-11-20 实测）：两仓 origin 已 set-url 至新 URL——Engine `https://github.com/Vin535LFJ/ai-knowledge-to-learning-engine.git`、Skills `https://github.com/Vin535LFJ/matt-pocock-skills-zh-cn.git`（upstream-en/zh 未动）；GitHub 改名核实 = 两仓新 URL `git ls-remote origin HEAD` exit 0（远端 HEAD `e848d2801ec9940e154b9bf40bc26198a5d197ba` / `e1936f23e6e149c581124cc218e79860c07108ef`，留痕会话复核实测）；引用收尾完成（Engine 24 文件、Skills 5、Program 5、OmniWorld 5；OmniWorld lock 37 条全部指向新 slug，旧 slug 0 条）。详见 `CHANGELOG.md` 2026-11-20 T1 条目与 `AI-Knowledge\ai-knowledge-program\plans\2026-11-19-rename-audit-and-migration.md` 执行实测段。

## CHG-0001 执行记录（2026-11-19，四项目并进）

- **P7 剩余 gap 已修复**：L13（V17–V20 open 断言 + quiz 重挂）、L06（两层 objectives/正文/source anchor/P02）、L11（RenderPass 勘误 + 乱码四处）。L02 已闭合。门禁 build/validate(0 FAIL/0 WARN)/arc(5/5)/review_gate 全绿。
- **P2 Skill**：`learning-experience-design` 建成（`.agent/skills/`），试点规格待用户确认；三个 build 脚本已排除 `.agent`。
- **P3/P4**：两个新本地项目 `agent-workspace-governance`（11 tests OK）、`github-project-radar`（17 tests OK）已初始化，未碰 git/GitHub/网络。
- **续跑点更新**：P7 内容与数据修复完成 → 下一步为 **G1/G2 人工审核**（B4/B10/V13/V14 升级等裁决）+ 试点设计方向确认；G3 仍未通过，本轮不发布。
- **边界**：未 commit/push、未建远程仓库；25 项既有未提交变更保持原样、本轮为增量追加。详见 `CHANGELOG.md` 与 `.agent/changes/CHG-0001-four-project-expansion/`。

## 融合基线增量执行记录（2026-11-19，新架构文档作为缺陷清单+规格增量）

- **发布边界修复（第一优先）**：reviews/ 8 篇审核材料不再进入 `web/content.js`（知识文档 85→77）与 VitePress 树；新增集中边界模块 + 咨询性 allowlist + 11 测试；archive 行为不变。
- **状态漂移**：早期表过期状态改指针行（B13/B14 已裁决）；PROJECT_CURRENT_STATE 加增量校正块。
- **裁决材料包**：`reviews/decision-kit/` 七项（B4/V13/V14/B10/B11/B12/B15）+ G1/G2/G3 全 OPEN，裁决栏空白，未代批。
- **Skill 增量**：learning-experience-design 参考文档 8→13 篇（旧 8 保留 + 新 5），SKILL.md 双索引，draft。
- **两新项目增量**：governance 25 tests（+doctor/index/13 类型/单写者协议）、radar 38 tests（+三维评分/生命周期别名/human_selected flag/零网络 source 接口）；目录名不变。
- **P8/P9 只读基础**：`tools/kcr_impact.py` 只读影响链工具 + P9 设计文档（draft），未写源 JSON/未升级 claim/未建运行态文件。
- **续跑点**：仍为 **G1/G2 人工审核 + 7 项裁决（decision-kit）+ P2 试点方向确认（PILOT-L13-plan.md）**；G3 未通过、本轮不发布。
- **边界**：零 git 写操作；HEAD `474c667`、stash@{0} 原样；未联网、未建远程仓库。详见 CHANGELOG.md 与 `.agent/changes/CHG-0001-four-project-expansion/handoff.md`。

## 程序级收口记录（2026-11-19，D16 / PD-Q1/Q2/Q7/Q8）

- **裁剪生效（PD-Q7/PD-003）**：Engine 唯一活跃线；learning-experience-design/P03/P04 冻结在现有成果（冻结≠删除）；不新建知识库/skill 收录类项目。程序级权威：`AI-Knowledge\ai-knowledge-program\decisions\PD-003-scope-trim.md`（accepted）。
- **三批收口（PD-Q1）**：`5a4de84`（D15 治理基座 31 文件）/ `a45ffa9`（CHG-0001 P7+P2 33 文件）/ `7c05bc7`（P8/P9 预研 20 文件）+ 留痕笔；`test_publish_boundary.py` 断言笔误修正（77→69）后 11/11 OK；发布 allowlist 生效，bundle **69 docs**（reviews 不再进学习站）。
- **P03/P04 版本保护（PD-Q2）**：本地 git `dec60ba`（39 文件）/ `942530b`（30 文件），无远程；测试 25/38 OK 实测。
- **副本清理（PD-Q8）**：`program-office-delivery/` 10 份→回收站（可恢复）；`.qoder-input-images/` gitignore。
- **门禁实测**：build 69 docs/17 sections/124 terms/19 lessons/7 labs/504 cards · validate 11/0/0 · arc 5/5 · review_gate 37 claims（16v/14o/7c）误标 0。
- **续跑点**：G1/G2 人工裁决（decision-kit 七项）→ P7.2 逐篇（一次一篇）→ P8 KCR 闭环 → P9 最小状态机 → P10 一批新资料端到端验收。
- **收尾更新（2026-11-19，Program 会话实测）**：Render_Notes 已迁入 `AI-Knowledge\Render_Notes`（PD-002 收尾完成；Move-Item 成功，git 完好 HEAD=`e848d28` 工作树干净；迁移后只读门禁复跑 validate 11/0/0、review_gate 37 claims 误标 0）。`site-vitepress/docs/program-office-delivery/` 残留旧副本 10 份已按用户批准清理至回收站（可恢复）。stash@{0} 原样（B12）；G3 未通过、在线发布（D02）未授权。
