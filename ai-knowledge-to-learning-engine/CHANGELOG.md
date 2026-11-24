# 变更记录（CHANGELOG）

> 本文件记录「AI Knowledge-to-Learning Engine 增量补齐」的执行结果。
> 权威口径见 `DECISIONS.md`；当前阶段见 `WORKFLOW_STATE.md`。
> P5 + Part B 执行期间遵循 D09（不 commit/push）；2026-11-18 用户新授权 commit + push 到 origin/master，见文末"git 提交"段与 DECISIONS.md D09 更新。

## 2026-11-24 · 工具链多课程最小扩展（用户批准）+ embodied 首批 RESEARCH 完成（run 推进 EVIDENCE）

- **工具链三项扩展（用户批准，夹具演练验收）**：① validate §10 声明 `independent: true` 的课程跳过"派生自主课程"检查（id 唯一性/前置/unit/frontmatter/quiz 仍全量校验）；② build_site additive `courses[]` payload（主课程首位 + courses/*/course.json，旧 UI 读 .course 不受影响）；③ allowlist += 08-具身智能。**演练**：临时 independent 夹具课程 T01 → 12/0/0 通过；independent=false → "not derived" 精确 FAIL；夹具走回收站、registry 重建恢复 187/12-0-0（演练中另发现并规避 PowerShell Set-Content BOM 破坏 frontmatter 的环境坑）。
- **RESEARCH 源提取（Robot_Learn 只读零改动）**：两个只读代理并行通读主源（textbook 1185 行/principles 512 行/openlab 639 行/5.15、5.16 verified 块）；产出 `08-具身智能/` 七份提取文档（README + L1–L6 课源，公式 LaTeX 规范化、教学假设保留存疑标注、源差异显式注记）。**章节映射更正**：textbook §7=Sim2Real、§8=VLA/世界模型（复合误差在 §8.5）。
- **独立复算 70/70 通过**（py -3，含 JᵀF 力矩/Cramer 奇异速度/qⁿ 全表/外参全向量/统计区间；不信任源"node 复算"自称）。**外部权威核验 3 项**：Tobin 2017 域随机化（arXiv 1703.06907 摘要）/ Ross 2011 DAgger（PMLR v15，O(εH²)→O(εH)）/ MuJoCo MJWarp 官方 FAQ（GPU 非确定逐字）。
- **断言与来源登记**：V68–V84 共 17 条全 **open/low**（升级待 G1）；来源 +9（SRC-RL-* ×6 / SRC-EXT-* ×3）→ **101 claims（24v/70o/7c）/ 52 sources**。源勘误队列 **12 项**登记不擅改（"300 毫米"单位笔误/混叠释义条件写反/qⁿ 界方向三处冲突/fact:72/73 登记缺口等），详见研究报告 §6。
- **run 推进**：RUN-2026-11-23-embodied-batch1 artifact +1（research-report-embodied.md，共 2）→ **RESEARCH→EVIDENCE**（running，G3 open，kcr PROPOSED）。
- **门禁实测（末次）**：build **92 docs / 641 cards / 3267 KB**；validate **12/0/0**（latex 门禁首跑抓 README 散文单个双美元字样，已改写）；publish **12/12**（计数断言 85→92）；arc **19/19**；review_gate **101 claims 误标 0**（V68–V84 未挂载可预期，WRITE 前）；kcr **16/16**；runstate **25/25**；registry **195**。
- **边界**：未 commit/push；V1–V67 状态零改动；stash 原样；Robot_Learn 只读；在线发布 D02 不变。
- **续跑点**：EVIDENCE——G1 核验队列备齐（白皮书名称/BEVFormer NDS/前沿模型数字/源勘误反馈裁决）→ ARCHITECT（概念/术语 + courses/embodied-loop-journey/course.json independent）→ WRITE 6 课（LXD 六项增强+Floor 直接建）。

## 2026-11-24 · 公式乱码修复：构建期术语注入保护 $$ 公式块（用户报告）

- **现象**：3D变换与坐标空间 §4.3 的 Vulkan/D3D 深度公式在站点显示为原始 LaTeX + Markdown 链接混合乱码（`z_{[NDC](#/glossary?term=NDC)} = \frac{...}`）。
- **根因（实测定位）**：`build_site.inject_inline_term_links` 的 PROTECT_PATTERNS 只保护单行 `$...$`，**不保护多行 `$$` display 公式块**——术语链接器把公式内的 ndc 注入为 `[NDC](#/glossary?term=NDC)`，前端 protectMath 原样保护后 KaTeX 收到链接语法。前端无责（renderMath 先于 annotateTerms，且跳过 .katex）。
- **修复**：① PROTECT_PATTERNS 增加同行 `$$...$$` 保护；② 注入循环增加 `in_math` 跨行状态（`$$` 开块至闭块整段跳过），与既有 in_fence 同构。源 md 零改动（污染只发生在构建期）。
- **验证**：重建后全 bundle **83 个公式块 0 污染**（CHANGELOG 散文 $$ 字样跨段配对为检查误报，非公式）；Edge headless 真实渲染 QA：该页 **7 个 KaTeX 块全部渲染、0 链接污染、无 parse error**，公式源码仅存于 KaTeX annotation（预期）；临时服务器已停。
- **回归门禁**：test_publish_boundary 新增 `test_no_term_links_inside_display_math`（11→**12 tests**），防止复发。
- **门禁实测**：validate **12/0/0** · publish **12/12** · review_gate **84 claims（24v）误标 0**；build 85 docs / 628 cards 不变。
- **边界**：未 commit/push；断言/教材正文/stash 零触碰。

## 2026-11-24 · 文档治理：P6 过程文档归档 + 发布口径纠偏 + reviews/ 导航（用户授权移动/归档/删除）

- **归档移动（6 份，只移不删）**：`NEXT_PHASE_PLAN.md` / `CURRENT_GAPS.md` / `IMPLEMENTATION_PLAN.md` / `PROJECT_CURRENT_STATE.md` / `Master Prompt：构建 AI Knowledge-to-Learning Engine.md` / `Render_Notes：从知识库到 AI 原生教学系统的工作流设计.md` 自仓库根移入 `archive/process-history/`，各加归档标注（内容原样保留），新增 `archive/process-history/README.md`（清单与替代关系）；`archive/README.md` 挂子目录指针。根目录只剩 7 份活跃文档（README/AGENTS/CLAUDE/CHANGELOG/DECISIONS/WORKFLOW_STATE/.gitignore）。依 D10.4 归档仍在离线站只读发布；零 Markdown 入链（实测），历史叙述中的旧路径提及不改写。
- **发布口径纠偏**：allowlist 移除已清理的 `program-office-delivery` 与六份已移根条目、新增 `docs/`；`build_vitepress_content.py` EXCLUDED_FILES 移除两份已移文档（archive 排除已覆盖）；`run_state.py` 设计依据路径更新；README 历史文档指针更新。
- **reviews/ 导航**：新增 `reviews/README.md`（目录结构 + Loop 1 历史材料标注 + 使用原则）；历史材料只标注、不移动、不改写。
- **删除（回收站，可恢复）**：`.qoder-input-images/`（gitignore 内临时输入缓存，1 png）经 host_safe_delete 移入系统回收站（status=deleted/recoverable=true）。其余文件无安全删除候选，一律保留。
- **bundle 口径修正**：docs/USER-GUIDE.md 审计期创建但此前漏在 bundle 外，本次纳入；publish 计数断言 83→85（+归档索引 README +USER-GUIDE）。
- **Program 同步**：NOW.md 过期口径修正（kickoff 已批准/提交与 push 状态/源笔误已闭合/遗留清单更新）；PROGRAM.md 旧名 Render_Notes 活跃标注改为现名（历史叙述保留）、Governance/Radar 状态更新为已解冻验证。
- **门禁实测（留痕后末次）**：build **85 docs / 628 cards / 3168 KB**；validate **12/0/0**；arc **19 篇 0 FAIL**；publish **11/11**；review_gate **84 claims（24v/53o/7c）误标 0**；kcr **16/16**；runstate **25/25**；registry **187 条**一致。
- **边界**：未 commit/push（待授权）；断言/教材正文/stash 零触碰；embodied run 状态不变（RESEARCH/running）；在线发布 D02 不变。

## 2026-11-23 · 两处源笔误修正（D21 用户批准）+ embodied-loop-journey 首批 INTAKE 完成（run 推进至 RESEARCH）

- **源笔误修正（用户批准，D21）**：① 项目实战指南 §5.3 "PSNR 每提高 6 dB，MSE 约减半"→"每提高约 3 dB 减半（10·log₁₀2≈3.01；+6 dB≈降至 1/4）"；② 程序化几何与旋转曲面 §2 "花冠"→"花瓶"（全库唯一命中）；③ L15 勘误注记更新为"已闭合（源已更正）"；④ V53 台账 claim/conditions 同步（去除"待 G1 更正"表述）。历史审读材料（G2-L15/G2-L17）不改写。
- **embodied kickoff 批准与 INTAKE**：用户批准课程名 `embodied-loop-journey`《具身智能：一条指令如何变成物理动作》+ 首批 6 课。真实 run `RUN-2026-11-23-embodied-batch1`（gate G3/--kcr/6 write_paths）建立并启动；**INTAKE 完成→RESEARCH**（artifact：reviews/embodied-batch1/intake-manifest.md）。查重：具身相关词全库 **0 命中**（完全新增领域）。
- **源清单诚实修订**：rerun/facts.md 实测为"AI 训练师职业标准/法规卷"事实底本（非具身核心），首批仅按需引用具身相关条目（白皮书名称/数据质量国标/Kappa）；主源 = textbook-embodied（**实测 10 章**，盘点"12 章"口径更正）+ embodied-principles（6 章）+ ch05 5.15/5.16 verified 块 + openlab。Robot_Learn 只读零改动。
- **工具链多课程评估（报批项）**：validate §10 L411 硬约束 pilot id ⊆ tools/course.json——独立新课程需最小扩展（§10 independent 命名空间 + build_site additive courses[] payload + allowlist 08-具身智能），**WRITE 前需用户批准**；未批则首批先以 08-具身智能/ 知识文档形态产出（RESEARCH/EVIDENCE 不受阻）。
- **门禁实测（笔误修正+INTAKE 留痕后末次）**：build **83 docs / 624 cards / 3149 KB**；validate **12/0/0**；arc **19 篇 0 FAIL**；publish **11/11**；review_gate **84 claims（24v/53o/7c）误标 0**；kcr **16/16**；runstate **25/25**；registry **183 条**一致。
- **边界**：未 commit/push（本批改动累积待授权）；断言状态除 V53 文本同步外零改动；stash 原样；在线发布 D02 不变。
- **续跑点**：RESEARCH——源提取（textbook/principles/5.15/5.16 → 断言草稿 + 外部核验）；工具链扩展报批并行等待。

## 2026-11-23 · push 收口（用户授权 7 笔）+ 下一主线登记（P10.3 具身智能课程）

- **push 回执（用户 2026-11-23 授权，ls-remote 实测）**：Engine `e848d28..3115cad` **6 笔**（cf91738 D17–D19 裁决 / ac81548 T1 命名 / 9f8ef4b 六阶段收口 / a76405b P10 done+D20 / 4945711 LXD 试点 A / 3115cad 记录更正）→ origin/master=`3115cad`；Skills `e1936f2..7326522` **1 笔**（改名引用更新）→ origin/main=`7326522`（首推 connection reset，重试成功，先例 D16 网络抖动）。Program/Governance/Radar 无 remote（PD-Q3 另批），本地提交保护。
- **六阶段收口确认（本会话独立实测，非照单全收）**：run=FEEDBACK/done、G3 passed（approver 记录）、18 artifacts、write_paths 释放；D20 完整；G2-L19=91 用户本人填分；LXD SKILL active + Floor L13/L19 双 PASS 复跑；五仓工作树清零；门禁复跑 validate **12/0/0** · publish **11/11** · review_gate **84 claims（24v/53o/7c）误标 0** · kcr **16/16** · runstate **25/25** · arc **19 篇 0 FAIL**。
- **下一主线（用户 2026-11-23 裁决"1 和 3"）**：**P10.3 多领域课程复用 = embodied-loop-journey 新课程**（源参考 `C:\Users\Giant\Desktop\GITCODE\Robot_Learn`，**只读**，具身智能知识库 625 md/十一轮复核/verified 分级）；**LXD 全面铺开为 Engine 内部工作流**（新页面直接按六项增强+Floor 标准建；既有 19 课分批增强，不另开战线）。kickoff 方案：Program `plans/2026-11-23-embodied-course-kickoff.md`（首批 6 课 + 8 源批 + run 计划，**待用户批准开工**）。
- **积压登记（不阻塞主线）**：G2 历史 17 篇评分（可复用 L19 模式：AI 诊断建议分+用户确认）；两处源笔误（PSNR dB/花瓶）；U1–U3/P07/C1–C7 研究队列；P10.3 其他领域与 PD-Q3 远程另批。
- **门禁实测（留痕重建收敛后）**：build **83 docs / 624 cards / 3141 KB**；validate **12/0/0**；publish **11/11**；review_gate **84 claims 误标 0**。
- **边界**：本条目为 push 回执+主线登记，知识内容/断言/教材零改动；stash 原样；在线发布 D02 仍未授权。

## 2026-11-21 · P10 端到端验收：HDR 批次真实 run 走通 INTAKE→REVIEW（L19 新教材，人工门暂停待裁）

- **范围**：用户批准"开工 P10 端到端验收：用 run_state 建真实 run，选一批新资料走 INTAKE→FEEDBACK 全链，人工门留给我裁决"。批次主题 **HDR 视频渲染**（查重 151 处命中确认概览层覆盖、无专课深潜、无外部 HDR 来源 → 差异化定位渲染侧管线）。真实 run `RUN-2026-11-20-p10-hdr`（.agent/runs/，本地 only）：**INTAKE→RESEARCH→EVIDENCE→ARCHITECT→WRITE→DESIGN→PRACTICE→REVIEW 八阶段全走通，16 个 artifact 全程 path+sha256 留痕**；REVIEW 暂停（pause --operator user），**PUBLISH/FEEDBACK 被 G3 人工门硬阻塞——设计行为，等用户裁决**。
- **新资料（7 外部权威源，全部真实抓取/检索核实）**：AOSP HDR video（google.cn 镜像全文）/ AOSP Mixed SDR-HDR / ITU BT.2100-3（官方 docx 提取）/ ITU BT.2408-3（§3.1 发灰权威描述）/ UHD Forum Blue Book 3.2.0 / colour-science eotf_ST2084 文档 / UPM 论文（BT.2100 Table 4/5 逐字转载）。直接抓取失败通道（itu.int rec 页/en.wikipedia）如实记录于研究报告 §3。
- **新教材 L19《HDR 视频渲染》**（0 → 约 200 行，U4，prerequisites [L03,L12,L14]，无绑定 lab 照 L10/L12 先例，不入 pilot 照 L18 先例）：发灰钩子（10000/1000/100 nit 张力）→ 亮度货币类比（边界声明）→ §4.1 PQ/HLG 双系统（HLG 兼容仅限 BT.2020 WCG 精确口径）→ §4.2 PQ EOTF $$ 公式三件套（五常数 + 锚点双精度 + code 509 算例 + Barten JND）→ §4.3 HDR10 元数据三件套（三条权威边界）→ §4.4 Android 链 ASCII 图（tunneled 定义 + 两个官方坑 + libtonemap/SDR dimming）→ §4.5 tone mapping（BT.2408 发灰原话口径 + 等比÷4 反例 + 线性光 + 8bit 截断已晚）→ §5 丢失后果速查表 → §6 四步排查现场 + 5 误区 → §7 四项练习 → §8–11 回忆/自检/桥/术语。
- **新断言 V63–V67（open/low）+ 来源 8 条**（7 外部 + SRC-RN-STREAMING 补登记；SRC-RN-IMGALGO 反向索引 +V67）；V23 复用挂接 +L19（文本未动，边界修订走 KCR I19）。review_gate **84 claims（18v/59o/7c）误标 0**。概念 K-HDR/K-TONEMAP（无环）+ 术语 5 条（BT.2020/tone mapping/MaxCLL/MaxFALL/DataSpace）+ taxonomy 重建。
- **KCR 全链实证**：Stage 1 两份真实影响报告（impact-v23-baseline 既有链 / impact-bt2100-new 新链）；Stage 2 **KCR-2026-11-001**（19 项，validate_kcr --stage2 OK，human_decision=null）；run kcr_substate PROPOSED→REVIEWING，**APPROVED 留人工**。
- **联动**：course.json L18.next null→L19 + L19 条目（20 lessons）；L18 头部路线位置 + §10 桥句改写（知识正文零改动）；publish 断言 82→**83**；研究报告 F3/F4 转述扩展（审读 m2/m3 修复，UHD Forum Table 1 全表 + P3-in-2020 示例）。
- **独立审读（只读换人）**：首轮 **2 blocker + 2 major + 6 minor**——B1 range 行错挂 V22→V21；B2 色域错配症状方向反（2020 当 709 应去饱和）→修正 + 挂 V24；M1 Bloom 链归属错位（L14 无 Bloom，出处面试库 04）→改 L14 真实链 + 另注出处；M2 tunneled 首现无解释→加一句话定义；6 minor（引号字形/101nit 转述/背景数字出处/SEI-SPS-EDID 括注/$$ 公式/HLG 元数据措辞）**全部修复**。审读亮点：数学全部独立复算通过、V23 边界处理"堪称范本"、结构全对齐、范围零越界。openQuestions U4/U5 登记 G1 队列。
- **门禁实测（修复后末次）**：build **83 docs / 17 sections / 129 terms / 20 lessons / 7 labs / 624 cards / 3129 KB**；validate **12/0/0**；arc **19 篇 0 FAIL**；publish **11/11**；review_gate **84 claims 误标 0**；kcr selftest **16/16**；runstate selftest **25/25**；registry **180 条**一致。
- **人工门材料（AI 不自评/不代批）**：`reviews/p10/G1-hdr-verification-queue.md`（V63–V67 逐条证据定位 + V23 I19 选项 + 裁决栏空白 + U1–U5）；`reviews/G2-L19-deepening.md`（十维度判定表待填）；`reviews/p10/human-gates-guide.md`（四件裁决按依赖顺序 + P10 验收标准八项对照全 ✅ + 恢复命令）。
- **边界**：未 commit/push；未升级任何断言；未擅改 V23/L03/glossary HLG 既有文本（U4 登记联动待办）；stash 原样；在线发布仍受 D02 约束（G3 通过 ≠ 在线发布授权）；run 暂停中，write_paths 持有至 done。
- **续跑点**：**等用户四件裁决（G1 核验 → KCR APPROVED → G2 评分 → G3 gate --pass）→ resume → PUBLISH（发布记录）→ FEEDBACK → done = P10 主目标达成**。遗留：commit/push 授权、两处源笔误、U1–U5。

## 2026-11-20 · P9 轻量工作流状态机实现（run_state.py + run-state 第四契约，25 tests，G-W1 闭合）

- **范围**：用户批准"开工 P9 轻量状态机，按设计稿扩展现有 tools 实现"。按 `reviews/P9-orchestrator-design.md`（十阶段 INTAKE→…→FEEDBACK + KCR 子状态 PROPOSED→…→VERIFIED + 五条不变量）与 NEXT_PHASE_PLAN P9.2 实现，stdlib-only（D05），不引 DB/队列/分布式组件。
- **新增**：① `tools/run_state.py`（CLI + API：new/start/pause/resume/fail/retry/artifact/advance/skip/gate/kcr/claim-path/release-path/show/list）；② `tools/kcr/schema/run-state.schema.json`（第四契约，设计 §3 schema 扩展 phase_records/transitions/write_paths/retry_count）；③ `tools/kcr/selftest_runstate.py`（**25 tests OK**：schema 正反用例/五条不变量/断点恢复/失败重试/防重复写入/人工跳过暂停/KCR 顺序/kcr_impact 真实回放 SRC-RN-COLORMGMT/CLI 退出码，全部写临时目录）；④ `reviews/kcr/RUN-STATE-TOOL.md`（工具说明，type: kcr / active）。
- **扩展**：`tools/kcr/validate_kcr.py` 三契约→**四契约**；run-state 硬规则入 semantic_errors（gate passed 必须人工 approver+approved_at；进入 PUBLISH/FEEDBACK 必须 gate passed；KCR APPROVED 及以后必须有 kcr_approved 人工过渡记录；done 仅在 FEEDBACK）。selftest_impact 回归 **16/16 OK**。
- **不变量（程序强制）**：人工门不可绕过（gate --pass 必须 --approver 非空，无自动批准路径）/ AI 不预填裁决 / 未批准不应用（PUBLISH 前置 gate + KCR APPROVED 人工）/ 单写者（write_path 声明即持有，done 自动释放）/ 可追溯（artifact path+sha256 幂等登记，transitions 追加时间/操作者/理由）。
- **对接**：impact-report 类 artifact 登记前自动过 impact-report 契约校验，失败不登记（kcr_impact 输出直接入追溯链）。运行态落 `.agent/runs/`（D15 本地 only，gitignore 既有）；保存前全量校验失败不写盘，固定名 tmp + os.replace 原子替换，全程无删除操作。
- **联动**：设计稿 status draft→**active** + §6 实现记录；CURRENT_GAPS **G-W1 闭合**（G-W3 工具盘点仍待）；IMPLEMENTATION_PLAN P9 行标注状态机已交付。
- **门禁实测（末次）**：build **82 docs / 608 cards / 3072 KB**；validate **12 checks / 0 FAIL / 0 WARN**；arc **18 篇 OK**；publish **11/11**；review_gate **79 claims（18v/54o/7c）误标 0**；kcr selftest **16/16**；runstate selftest **25/25**；registry 重建 **173 条**一致（+RUN-STATE-TOOL）。
- **边界**：未 commit/push（Engine 累计 60 文件未提交）；未改任何断言状态/教材正文；stash 原样（B12）；未创建真实 run 实例（P10 端到端验收时启用）；工具不写权威 JSON、不自动执行阶段任务、不做多进程并发锁（边界见工具说明）。
- **续跑点**：**P10 一批新资料端到端验收（= Engine 主目标达成）**——用 run_state 建真实 run 走 INTAKE→FEEDBACK，G1/G2/G3 人工门实测；P9.4 工具盘点（G-W3）可穿插。待用户：commit/push 授权、G2 评分（17 篇材料）、两处源笔误裁决。

## 2026-11-20 · 教材批量收官：L14/L15/L16/L17/L18 五篇新写（独立审读全修复，全部课时教材完成）

- **范围**：用户批准"继续所有教程进度完成"。新写五篇（各约 170–200 行）：**L14《光照、材质与图像算法》**（归层地图：PBR 约束/三种锯齿辨析/后处理与批处理管线位置）、**L15《性能评测与项目复盘》**（三原则/P99 vs 平均/画质指标/证据链表达规范）、**L16《面试表达与查漏补缺》**（四段式/七步项目故事/车载差异化/缺口表）、**L17《程序化几何 · 从轮廓到网格》**（参数方程→M×N 顶点→索引推导→成本账，绑定 procedural-lathe 实验）、**L18《PBR 光照与材质参数》**（Cook-Torrance D/G/F 深潜 + GGX 推导 + 多次散射，绑定 pbr-lighting 实验，next 链收官）。至此 **18 份课时教材全部完成**（L00 为地图课无独立教材；19 课元数据齐全）。
- **新断言登记（默认 open/low，共 17 条）**：V46–V50（L14）/V51–V53（L15）/V54–V56（L16）/V57–V59（L17）/V60–V62（L18）；复用挂接 V07/V38/V32/V17/V46。新来源 9 条：SRC-RN-LIGHTING/IMGALGO/BATCHING/PRACTICE/ADAS/INTERVIEW-LIST/JOURNEY/GAPS/PROCEDURAL；COLORMGMT/GPU-BASE/LIGHTING/PRACTICE 反向索引扩展。review_gate 实测 **79 claims（18 verified / 54 open / 7 conditional）误标 0**。
- **独立审读（每篇只读换人子代理）**：L14 首轮 2 major+7 minor、L15 首轮 **1 blocker**+4 minor、L16/L17/L18 首轮 acceptable=true（各 4/4/5 minor）——**全部修复**。L14/L18 分工边界（定位 vs 公式深潜）审读确认守住；L17/L18 实验双向绑定核实。
- **⚠️ 源文档笔误两处（仅登记，未擅改源，待 G1/源所有者裁决）**：① 项目实战指南.md 行 372 "PSNR 每提高 6dB，MSE 约减半"——数学上 +3dB≈减半、+6dB≈1/4（L15 教材与 V53 台账已按正确数学表述并显式登记勘误）；② 程序化几何与旋转曲面.md 行 68 "花冠"应为"花瓶"（教材/实验/台账均用花瓶）。详见 G2-L15/G2-L17 材料。
- **联动**：publish boundary 断言 77→**82**；tools/course.json L14.reading 补色彩管理条目（审读建议）；kcr selftest COLORMGMT 回放断言改子集校验（来源合法扩展支撑 V47/V48，非放宽门禁）。
- **门禁实测（修复后末次）**：build **82 docs / 17 sections / 124 terms / 19 lessons / 7 labs / 608 cards / 3064 KB**；validate **12 checks / 0 FAIL / 0 WARN**；arc **18 篇 0 FAIL**；publish boundary **11/11 OK**；review_gate **79 claims 误标 0**；kcr selftest **16/16 OK**；registry 重建 **172 条**一致。
- **G2 材料**：reviews/G2-L14/L15/L16/L17/L18-deepening.md 五份（评分待人工，AI 不自评）。
- **边界**：未 commit/push（Engine 累计 55 文件未提交）；未改任何既有断言状态；stash 原样（B12）；五篇均不在 pilot course.json（quiz 待纳入后补建，先例一致）；bundle 内嵌快照本条目留痕后重建同步。
- **续跑点**：教材生产全部完成 → **P9 轻量状态机**（设计稿 reviews/P9-orchestrator-design.md）→ **P10 一批新资料端到端验收（= Engine 主目标达成）**；研究队列 C1–C7 按 P8 节奏执行；待用户：commit/push 授权、G2 评分（17 篇材料）、两处源笔误裁决。

## 2026-11-20 · 教材第二篇：L12《系统合成与显示》新写（独立审读 1 major+6 minor 全修复）

- **范围**：新写 `courses/video-rendering-journey/lessons/L12-系统合成与显示.md`（0 → 约 180 行，无绑定实验，工程机制型）。双场景钩子 → 快递分拣类比（三层边界）→ §4.1 合成器/HWC 职责 + ASCII 端到端链路 + 三阶段瓶颈表（objective ①）→ §4.2 撕裂相位推导（标注教学展开）+ 双/三缓冲交易 + Jank≠pacing（objective ②）→ §4.3 overlay 路由判据 + SurfaceView/TextureView 表（取舍注明）+ 数字纪律（objective ③）→ §4.4 智驾入画与兜底 → §5 BufferQueue 三态 + 延迟分段账 → §6 排查现场 + 5 误区 → §7 四项练习 → 桥 L13。
- **新断言（open/low）**：**V43**（合成器选路与平面回退）/ **V44**（缓冲取舍与 pacing）/ **V45**（图层路由与组件对应）——SRC-RN-GPU-BASE（§3.1–3.4）+ SRC-RN-DECODE-PIPELINE（§6.2/§6.3）反向索引同步；复用 V34（open）/C01（conditional）挂接 L12。review_gate **62 claims（18v/37o/7c）误标 0**。
- **联动**：publish boundary 断言 76→**77**。
- **独立审读**：首轮 acceptable=true（**0 blocker / 1 major / 6 minor**）——major：钩子撕裂方向与推导矛盾；minor：表取舍注明/推导标注/判据口径/C01 条件转述/Swapchain 释义/V35 挂接精度。**全部修复**。审读亮点：数字纪律"全书示范级"、类比边界三层声明。材料 `reviews/G2-L12-deepening.md`。
- **门禁实测（修复后）**：build **77 docs / 568 cards / 2901 KB**；validate **12/0/0**；arc **13 篇 0 FAIL**；publish **11/11**；review_gate **62 claims 误标 0**；registry 162 条一致。
- **边界**：未 commit/push；未改既有断言状态；stash 原样；bundle 内嵌快照批量收官时统一重建。

## 2026-11-20 · 教材生产恢复第一篇：L10《显式 API 与同步》新写（独立审读 2 major+9 minor 全修复）

- **范围**：新写 `courses/video-rendering-journey/lessons/L10-显式API与同步.md`（0 → 约 210 行，无绑定实验，工程机制型+对比边界型）。三故障钩子（源 §5.5）→ 出租车/自驾类比（边界声明）→ §4.1 五维责任转移表（objective ①）→ §4.2 同步三件套+帧环（objective ②/checkpoint ①）→ §4.3 三类 barrier+可见性推导+六行故障表（objective ③）→ §4.4 RenderPass load/store+subpass 限制（接 L09 带宽账）→ §4.5 PSO 构成与治理（checkpoint ②）→ §5 PSO 组合账（教学算例显式标注）+帧环资源形态 → §6 排查现场+6 误区 → §7 验证层+RenderDoc 五项走查 → 桥 L11。
- **新断言登记（默认 open/low）**：**V39**（显式模型责任转移与收益边界）/ **V40**（三件套语义与帧环）/ **V41**（三类 barrier 与缺失/过度后果）/ **V42**（PSO 构成与创建成本治理）——evidence 双挂 **SRC-RN-EXPLICIT-API + SRC-RN-INTERVIEW-VK**（source-registry 新增两条 repo_doc，反向索引同步）；复用 V07/E02（verified/medium）、V35/V36（open/low）挂接 L10。review_gate 实测 **59 claims（18v/34o/7c）误标 0**。
- **联动**：L09 §10 桥句"教材页待建"→ 直链 L10；publish boundary 断言 75→**76**。
- **独立审读（只读换人子代理）**：首轮 acceptable=false（**0 blocker / 2 major / 9 minor**）——major：input attachment 限制缺失、RenderPass/Subpass 首现无解释；minor：术语计数/车载 2 帧 caveat/PSO 归因分开/治理五项取舍+缓存失效条件/UBO 与 specialization constants 释义/V39-V41 挂接精度/binary semaphore 限定/桥句 DAG-aliasing 短释。**全部修复**。专项确认：四表与源逐字一致、锚点全有效、objectives/checkpoint 逐字一致、L11 前置假设覆盖、无借挂。材料 `reviews/G2-L10-deepening.md`（G2 评分待人工）。
- **门禁实测（修复后）**：build **76 docs / 17 sections / 124 terms / 19 lessons / 7 labs / 560 cards / 2863 KB**；validate **12 checks / 0 FAIL / 0 WARN**；arc **12 篇 0 FAIL**；publish boundary **11/11 OK**；review_gate **59 claims 误标 0**；registry 重建 160 条一致。
- **边界**：未 commit/push；未改既有断言状态；stash 原样；L10 不在 pilot course.json（quiz 待纳入后补建，与 L03–L09 先例一致）。bundle 内嵌状态快照在批量收官时统一重建同步。

## 2026-11-20 · P8 片三完成：document-registry 一致性门禁接入 validate（用户批准）

- **validate_site.py 新增第 12 节 [registry]**：用生成器同一套 `collect_entries()` 重算磁盘 frontmatter 真值，与 `.agent/indexes/document-registry.json` 逐条比对（磁盘缺失/注册表残留/逐字段漂移/meta.total），**只读不写文件**；FAIL 消息自带修复命令（`py -3 tools/build_document_registry.py`）；meta.generated_at 为构建时间戳不参与比对。检查数 **11→12**。
- **build_document_registry.py 最小重构**：条目收集抽为纯函数 `collect_entries()`，main() 与 validate 第 12 节共用——生成与校验单一口径，不复制第二套解析逻辑。
- **首跑即抓到 16 处真实漂移**（门禁价值实证）：registry 停在 142 条（2026-11-19T21:21Z 构建），磁盘已有 158 份文档——6 篇新教材（L03/L04/L05/L07/L08/L09）+ 9 份 G2 材料 + P8-KCR-kickoff 未入册。按规定动作重建 registry → **12 checks / 0 FAIL / 0 WARN**。
- **验收演练（弄脏→FAIL→重建恢复，kickoff §2 片三验收标准）**：临时改 `reviews/P8-KCR-kickoff.md` frontmatter `updated: 2026-11-20→2026-11-21` → validate 精确 FAIL（exit=1，字段级定位 registry/disk 双值）→ 重建 registry 后 12/0/0 → 还原 frontmatter 再重建 → 12/0/0。**kickoff SHA256 与演练前完全一致**（A952DC56655A5F14905226D672C0899608F4A45061971B0C6A8F21941AFF691F），现场零残留；registry 对 HEAD 的差异仅为合法同步（+16 条目 + meta）。
- **门禁实测（本窗口末次，留痕后重建同步内嵌快照）**：build **75 docs / 552 cards / 2818 KB**；validate **12 checks / 0 FAIL / 0 WARN**；arc **11/11 OK**；publish boundary **11/11 OK**；review_gate **55 claims（18v/30o/7c）误标 0**；kcr selftest **16/16 OK**。
- **边界**：未 commit/push；未改任何断言状态/教材正文/课程数据；stash@{0} 原样（B12）；registry 属生成物，重建是规定修复动作非手改。
- **续跑点**：**P8-MVP 三片全部完成**（kickoff §3c/§3d/§3e）→ 按 kickoff §4 恢复 **L10《显式 API 与同步》**教材生产 → P9 最小状态机 → P10 端到端验收；研究队列 C1–C7（B15=A 全立项）按 P8 节奏执行，不阻塞教材主线。待用户：commit/push 授权、G2 十篇评分。

## 2026-11-20 · P8 片二完成：KCR 程序化校验器 + L02 实验文案修复（M1，用户采纳推荐）

- **片二核心——`tools/kcr/validate_kcr.py`（stdlib-only，D05）**：覆盖三契约（impact-report / change-proposal / review-decision）实际用到的全部 JSON Schema 关键字子集（type 含类型数组 / required / properties / items / enum / pattern / minItems）；**遇未支持关键字直接抛错**（schema 演进强制校验器同步升级，不静默漏检）。另实现 schema description 文档化硬规则 `semantic_errors`：action ∈ {modify, deprecate, reverify} 必须 target.id；`--stage2` 时 human_decision 必须 null（AI 不预填）。CLI 支持多文件、按文件名推断契约、退出码 0/1/2。
- **接入 kcr_impact 输出**：`tools/kcr_impact.py` 写盘前强制过 impact-report 契约校验，失败不写文件、退出码 3（错误 seed 路径不受影响）。
- **自测扩展**：`tools/kcr/selftest_impact.py` 5→**16 tests**——assert_shape 升级为全量 schema 校验；新增 ValidatorTests 11 例（三契约最小合法文档 / 缺必填 / 错枚举 / 错 pattern×2 / minItems×2 / human_decision 类型联合 null / modify 缺 id / stage2 预填拦截 / 未支持关键字守卫 / 三真实样本回放 / CLI 正反退出码）。**16/16 OK**；CLI 实测三份真实样本（impact-l09-p07 / impact-v14-replay / impact-colormgmt-replay）全 OK。注：reviews/kcr/ 下 impact-v14.json / impact-draft.json / impact-demo.json 为片一对齐前的历史冒烟工件，保留不改写，不作契约样本。
- **L02 遗留 major M1 修复（用户 2026-11-20 采纳推荐）**：`tools/labs.json` pts-dts-timeline「同步约束」desc 与 `web/assets/app.js` stage 值两处「DTS ≤ PTS 恒成立」改为与课文任务 3 口径一致（I/P 帧 PTS ≥ DTS 提前解出等显示，B 帧 PTS < DTS 等参考帧）；连带修复 tlDelta 硬编码 "+" 前缀致 B 帧显示 "+-1" 的符号 bug。**Edge headless 双路浏览器 QA**（http://localhost:8765 与 file://，--dump-dom 实测渲染 DOM）：stage5/stage6 新文案正确、tlDelta=-1（默认指针 B1）、旧句清零。G2-L02 材料追加 M1 执行补记（审读原文不改写；其余 6 minor + openQuestions 仍待人工）。
- **门禁实测（本窗口末次，留痕后重建同步内嵌快照）**：build **75 docs / 17 sections / 124 terms / 19 lessons / 7 labs / 552 cards / 2812 KB**；validate **11 checks / 0 FAIL / 0 WARN**；arc **11/11 OK**；publish boundary **11/11 OK**；review_gate **55 claims（18v/30o/7c）误标 0**；kcr selftest **16/16 OK**。
- **边界**：未 commit/push；未改任何断言状态/教材正文/课程数据（labs.json 与 app.js 属实验文案层）；stash@{0} 原样（B12）；保护路径未触碰；片三（registry 门禁接入 validate）**仍未动手，需报批**。
- **续跑点**：P8 片三（报批后执行）→ L10《显式 API 与同步》恢复 → P9 最小状态机 → P10 端到端验收。

## 2026-11-20 · 独立复核（另一会话）+ P8 片一完成：kcr_impact 输出↔schema 对齐

- **复核范围**：前一窗口 T1 + P7.2 十篇 + P8 启动的全部声明，只读核验 + 门禁复跑。结论：**实质工作全部属实**——三仓 git 状态/四笔提交/行数（L02 217/L06 200/L11 193/L13 235/L03 168/L04 199/L05 175/L07 150/L08 149/L09 153，逐篇实测一致）/55 claims（18v/30o/7c，V21–V38 均 open/low，无误升）/stash 原样/保护路径未触碰/未 push（远端 HEAD 仍 e848d28、e1936f2）。
- **复核更正（记录笔误，非数据问题）**：① card 数真值 **552**（原记录 553；工作区 content.js 与新鲜重建均为 552，JSON 级对比仅时间戳与内嵌状态文档快照差异）；② build 体积真值 **2800 KB**（原记录 2790）；③ source-registry 真值 **24 个来源**（本窗口新增 5 个：COLORMGMT/GPU-BASE/GRAPHICS/INTERVIEW-GL/RASDEPTH；原摘要"四个新 SRC"不准确）；④ Program 办公室有 1 个未提交文件（NOW.md，原报告称 0）。
- **content.js 重建**：原工件构建于 07:23，其后状态文档更新未同步入 bundle——本窗口重建同步（75 docs / 552 cards / 2800 KB），validate 复跑 11/0/0。
- **P8 片一完成（对齐 + 自测）**：`tools/kcr_impact.py` 输出对齐 `tools/kcr/schema/impact-report.schema.json`——补契约 trigger（四模式映射：source_update/claim_status_request/new_research_report）+ new_sources（恒 []，来源登记属 Stage 2）；affected 各数组改为对象（id+relation/via_claim）；website 移出 affected 改非契约字段 website_artifacts；结构完整性检查移入 integrity_findings（不冒充契约 conflicts，语义冲突属 Stage 2）；uncovered 改为字符串数组。修复既有 bug：`--out` 指向仓库外路径时 relative_to 崩溃。
- **自测**：新增 `tools/kcr/selftest_impact.py`（stdlib-only，5 tests）——真实回放 SRC-RN-COLORMGMT→V21–V24→L03、V14→K-STRIDE/L01/L01#L01-Q2/两层 course、V21 open→integrity_findings、草稿 CLI 契约形状、未知 seed 报错。**5/5 OK**。三份真实样本按新契约重生成：reviews/kcr/impact-l09-p07.json / impact-v14-replay.json / impact-colormgmt-replay.json。
- **门禁实测（本窗口末次）**：build **75 docs / 17 sections / 124 terms / 19 lessons / 7 labs / 552 cards / 2800 KB**；validate **11 checks / 0 FAIL / 0 WARN**；arc **11/11 OK**；publish boundary **11/11 OK**；review_gate **55 claims（18v/30o/7c）误标 0**；kcr selftest **5/5 OK**。
- **边界**：只读复核 + 工具层改动，未改任何教材正文/断言状态/课程数据；未 commit/push；L02 遗留 major（app.js:2350「DTS≤PTS 恒成立」静态句与 lab 模型及 L02 五帧表矛盾）仍待用户裁决，未擅自改。
- **续跑点**：P8 片二（程序化校验器 stdlib-only）→ 片三（registry 门禁接入 validate，**动手前报批**）→ L10 恢复 → P9 → P10。复核全文：`AI-Knowledge\ai-knowledge-program\plans\2026-11-20-progress-review.md`。

## 2026-11-20 · P8 启动：阶段切换 + 三 schema 固化 + 冒烟测试（片二部分完成）

- **阶段切换**：P7.2 十篇收官（见下方十个条目）→ **P8 KCR 最小闭环启动**（用户 2026-11-20 "继续推进下一个阶段"，接受"先 P8"建议）。启动检查点 `reviews/P8-KCR-kickoff.md`：已有资产清单（KCR 设计/kcr_impact.py 四模式/validate §8）、P8-MVP 三片切片范围与验收、明确不做清单、续跑指引。
- **片二部分完成——三 schema 落盘**：`tools/kcr/schema/impact-report.schema.json` / `change-proposal.schema.json` / `review-decision.schema.json`（按 D13 设计文档 §Stage1/2/3 字段结构固化；D05 原则下为静态契约文件，程序化校验器待下窗口）。三文件 JSON 有效性实测通过。
- **冒烟测试（Stage 1 实跑）**：`kcr_impact.py --claim-draft`（flush 断言草稿，对应验真队列 P07）产出 `reviews/kcr/impact-l09-p07.json`——claims/concepts/courses 等结构与设计一致，**但发现工具输出与设计 schema 漂移**：缺顶层 trigger/new_sources、affected 多 website 键。已如实登记于 kickoff §3b 作为片一对齐目标，不掩盖不伪造。
- **边界**：未 commit（累计未提交 32→33 文件：+3 schema+1 impact 样本+1 kickoff+本条目）；validate/publish 复跑 11/0/0 与 11 tests OK（schema 与 kickoff 在 reviews/tools 下，bundle 无变化——reviews 不进学习站、tools/kcr 为纯 JSON 非 .md）。
- **续跑点**：片一对齐（工具输出↔schema）→ 片二收尾（程序化校验器）→ 片三 registry 门禁接入 validate（动手前报批）。

## 2026-11-20 · P7.2 第十篇：L09《移动端瓶颈与 TBDR》新写教材（审读 blocker 修复后通过——「其余篇目」第六篇）

- **范围**：新写 `courses/video-rendering-journey/lessons/L09-移动端瓶颈与TBDR.md`（**0 → 153 行**，无绑定实验，对比边界型）。结构：桌面经验三连变形钩子（MSAA/discard/依赖上一帧，方向反了）+ 720p 带宽账（3.69/7.37 MB、442 MB/s、10 Pass 4.4 GB/s）→ 瓷砖类比（边界：binning 在几何阶段/厂商差异）→ §4.1 IMR vs TBDR 流程与七行关键差异表（`V36`，厂商 ⚠️+"不要断言所有移动 GPU 都是 TBDR"原文）→ §4.2 Overdraw 本质（RMW）与 Early-Z 三失效条件 + Hi-Z/深度预 Pass/半透明纪律（`V37`）→ §4.3 MSAA 原理/成本归属/"不是 SSAA"（`V38`，checkpoint ②）→ §4.4 API 层也不能照搬（`C05` conditional/`V09`）→ §5 带宽账三件套 + 优化顺序六条 + 判断瓶颈表五行 + 移动端红线五条 → §6 排查现场（Overdraw 视图+A/B）+ 5 误区 → §7 Overdraw 视图走查清单（五项含预期）→ 桥句→L10。
- **新断言登记（默认 open/low）**：**V36**（TBDR 家族 binning/tile memory/一次性写回，附条件：不断言所有移动 GPU 都是 TBDR ⚠️）/ **V37**（Early-Z 三失效条件与补救）/ **V38**（MSAA 原理/成本归属/非 SSAA）——evidence=**SRC-RN-RASDEPTH**（source-registry 新增 repo_doc 条目 repo:03-图形与GPU工程/光栅化深度与移动GPU架构.md，used_by_claims=[V36,V37,V38]）；used_by_lessons=[L09]。既有 E02/C05/V09 挂载（条件如实转述）。review_gate 实测 **55 claims**（verified 18 / open 30 / conditional 7）误标 0。
- **审读（独立子代理，只读换人 + 四项数值独立重算）**：首轮 **1 blocker + 7 minor**——**blocker** = §4.2"每次半透明混合……三倍带宽"挂源无据且算术不成立（RMW 是两次传输对一次；源文档只给机制不给倍数）——**已修复**（改为"以单次写为基准 RMW 是读+写两次传输；源文档只给机制不给倍数，×N 按 §3.2 实测"）；minor 7 条（面试引文截断补"与优化建议"、类比边界无出处推断删除、loadOp/storeOp/alphaToCoverage 首现补释义、"Overdown"错字、L10 课时名对齐 course.json《显式 API 与同步》、L08 桥句"待建"联动更新为直链、720p 口径补十进制声明）——**全部修复**。修复后全门禁复跑通过。
- **publish boundary 断言同步（先例 D16/L03/L04/L05/L07/L08）**：bundle 74→**75 docs**，数量断言 74→75。
- **门禁（执行会话实测，全 exit 0）**：build_site **75 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 553 cards / 2790 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **11 篇 · OK**（L09 加入检查集）；review_gate **55 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L09-deepening.md`。

## 2026-11-20 · P7.2 第九篇：L08《一帧怎么画出来》新写教材（审读通过——「其余篇目」第五篇）

- **范围**：新写 `courses/video-rendering-journey/lessons/L08-一帧怎么画出来.md`（**0 → 149 行**，无绑定实验）。结构：SwapBuffers 提交≠显示的反直觉钩子 → 装配线+仓库+物流类比（边界：领先 1–3 帧/V-Sync 背压）→ §4.1 管线七阶段流转与"片元→淘汰赛→像素"推导（`V33`，checkpoint ①）→ §4.2 RenderTarget/FBO 与多 Pass 衔接 + PSO/Shader 变体纪律 → §4.3 CPU/GPU 异步与 Frame in flight 上限（`V35`）→ §4.4 Swap→View 树混合→SurfaceFlinger 链路 + vsync 背压口径（`V34`）→ §5 从应用到屏幕完整链图（源 §2.1 ✅ 转载）+ 工程红线四项 → §6 P99 尖刺分层排查现场 + 5 误区 → §7 帧循环对照走查 → 桥句→L09。
- **新断言登记（默认 open/low）**：**V33**（管线七阶段流转与片元淘汰赛）/ **V34**（SwapBuffers 提交≠显示 + vsync 背压口径）/ **V35**（Frame in flight 1–3 帧上限与三同步原语）——V34 为复合断言，evidence 双挂 **SRC-RN-GPU-BASE + 新增 SRC-RN-INTERVIEW-GL**（repo:06-面试知识库/车载渲染引擎/01-OpenGL管线-FBO与离屏渲染.md，审读 major"追溯面偏窄"的修复；used_by_claims=[V34]），source_documents 三向（GPU 基础/解码链路/面试库）；used_by_lessons=[L08]。既有 `V07`（verified）预挂转正。review_gate 实测 **52 claims**（verified 18 / open 27 / conditional 7）误标 0。
- **审读（独立子代理，只读换人，行号实地核对）**：**acceptable=true，修订 0 轮**；**22 处技术表述全部溯源**（§4.4"提交≠显示"把三份文档的链路证据串成因果链且逐句挂源被点名；两层 course.json 四处联动一致；无编造数字）；**1 major + 8 minor 全部修复**（major：V34 evidence 面偏窄→补 SRC-RN-INTERVIEW-GL 与三向 source_documents；minor：面试库小节号错标、两处 doc 级链接补锚点/改口径、PSO/V-Sync 首现无释义、§10 L09 主题表述与 course.json 对齐、L07 桥句"待建"过时联动更新、§4.3 占用率引用收窄为主文档 §4.2 验证表）。修复后全门禁复跑通过。
- **publish boundary 断言同步（先例 D16/L03/L04/L05/L07）**：bundle 73→**74 docs**，数量断言 73→74。
- **门禁（执行会话实测，全 exit 0）**：build_site **74 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 544 cards / 2752 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **10 篇 · OK**（L08 加入检查集）；review_gate **52 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L08-deepening.md`。

## 2026-11-20 · P7.2 第八篇：L07《GPU 为什么快》新写教材（审读 1 blocker + 2 major 修复后通过——「其余篇目」第四篇）

- **范围**：新写 `courses/video-rendering-journey/lessons/L07-GPU为什么快.md`（**0 → 150 行**，无绑定实验）。结构：TOPS 宣传页 vs 帧率张力钩子 + 带宽账数字 → 车道类比（SIMT 同步执行，边界声明豁免访存与调度）→ §4.1 并行模型表与"分支发散整组串行化"（`V29`，32/64 lane 常见值 ⚠️ 条件）→ §4.2 存储层次 + 带宽估算模板 + 算术强度判瓶颈侧（`V30`）→ §4.3 延迟隐藏与占用率"是手段不是目标"（`V31`）→ §4.4 别只看 TOPS、车机看 P99/热稳定（`V32`）→ §5 带宽账算例 + 主文档 §4.2 验证实验表转载 → §6 降分辨率排查现场 + 5 误区 → §7 带宽账手算清单（四项含预期）→ 桥句→L08。
- **新断言登记（默认 open/low）**：**V29**（warp 分支发散串行化，附条件：32/64 lane 常见值 ⚠️）/ **V30**（带宽账口径与估算模板，附条件：算术强度定瓶颈侧）/ **V31**（occupancy 是手段非目标）/ **V32**（TOPS 峰值≠帧率，车机看 P99/热稳定）——evidence=**SRC-RN-GPU-BASE**（source-registry 新增 repo_doc 条目 repo:03-图形与GPU工程/GPU与渲染引擎基础与链路.md，used_by_claims=[V29,V30,V31,V32]）；used_by_lessons=[L07]。review_gate 实测 **49 claims**（verified 18 / open 24 / conditional 7）误标 0。
- **审读（独立子代理，只读换人 + 逐行验证）**：首轮 **1 blocker + 2 major + 6 minor**——**blocker** = §5/§1 把源文档"≈7.9 MB"的**二进制口径**展开为十进制乘法（1920×1080×4B 实为 8.29 MB），与 L01/L06 的 8.29 MB 口径直接冲突、checkpoint 答案两口径打架——**已修复**（§1/§4.2/§5/§9 四处统一双口径标注：8.29 MB 十进制 / 7.91 MiB，498 MB/s 十进制 / 475 MB/s 源口径，沿用 L01 MB/MiB 纪律；ledger V30 claim 文本同步）；**major ×2** = ①"L06 的 aliasing/RenderGraph 在带宽账上直接兑现"双重错位（aliasing/RenderGraph 属 L11 且 aliasing 省 VRAM 峰值非带宽）→ 已改为分科目归属（L06 零拷贝省 CPU 搬移、L11 loadOp/storeOp 优化带宽 + aliasing 省 VRAM 峰值）；②小节号错位 3 处（§4.4 验证表/§4.2 模板/§4.4 少不确定性）→ 已改为"主文档 §x.x"无歧义标注；minor 6 条（"按 Pass 累加"归因 L06 超前改本章 V30 引入、P99 首现无解释、§10 链接落点改"待建"模式、L06↔L07 双路线断层记录为跨路线观察、uniform 空格、延伸缺 #3-overdraw-与带宽 锚点）——**全部修复**。修复后全门禁复跑通过。
- **publish boundary 断言同步（先例 D16/L03/L04/L05）**：bundle 72→**73 docs**，数量断言 72→73。
- **门禁（执行会话实测，全 exit 0）**：build_site **73 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 536 cards / 2717 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **9 篇 · OK**（L07 加入检查集）；review_gate **49 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L07-deepening.md`。

## 2026-11-20 · P7.2 第七篇：L05《硬解与 ownership》新写教材（审读 blocker 修复后通过——「其余篇目」第三篇）

- **范围**：新写 `courses/video-rendering-journey/lessons/L05-硬解与ownership.md`（**0 → 175 行**，无绑定实验）。结构：双俗语挖坑钩子（"硬解一定更快更省电"/"不要就 flush"）→ 周转箱类比（L06 仓库+钥匙扩展，三条例边界）→ §4.1 buffer 流转循环（dequeue/queue 成对、release(true) 移交/release(false) 丢帧归还，`V27`）→ §4.2 省电的物理基础与四条件限定（`C03` conditional + §2.3 功耗行"不能泛化为固定 10%"⚠️ 原文）→ §4.3 回退触发条件与八步状态机（`V28`，§8.4 ✅）→ §4.4 RenderThread 不直接 flush codec 的推导（**明确标注推导 + 候选登记验真队列 P07**）→ §5 buffer 生命周期 ASCII + 软硬解搬运账（口径修正）→ §6 多路播放器排查现场 + 5 误区 → §7 回退状态机走查清单 → 桥句→L06（带 C02 条件）。
- **新断言登记（默认 open/low）**：**V27**（buffer 有限池与借还/移交语义，附条件：render=true 移交以绑 Surface 为前提）/ **V28**（八步回退状态机与触发条件，附条件：顺序不可换）——evidence=**SRC-RN-VERIFICATION**（used_by_claims 同步 +V27/+V28，原 C01–C07/P01–P06 保留）；used_by_lessons=[L05]。既有 `C03`（conditional）预挂转正。review_gate 实测 **45 claims**（verified 18 / open 20 / conditional 7）误标 0。
- **审读（独立子代理，只读换人 + 独立重算）**：首轮 **1 blocker + 1 major + 8 minor**——**blocker** = §4.4 声称"openQuestions 已登记"而全库查无实据（诚实标注方向正确但"登记"未落实）——**已做实**：flush 候选正式登记于[验真队列 ❗ 表 P07](00-导航与索引/验真队列与术语表.md)（缺官方文档核验与实测复现，未登记断言），正文/§11 改为指向 P07；**major** = §5 搬运账"每帧多两次主存↔显存总线搬移"与源失实（"两次"属 ByteBuffer 弯路口径）——**已修正**（普通软解每帧一次总线拷贝；弯路两次口径分离标注）；minor 8 条（V28/正文漏"分辨率突变/驱动崩溃"、「§2.4 设备差异」引用错位、L06 task 4 引文不逐字、ASCII render=false 行残缺、DPB 术语错挂、C01/V01 used_by 反向索引漂移双向修正、桥句丢 C02 条件、两处引文不逐字）——**全部修复**。修复后全门禁复跑通过。
- **台账反向索引双向修正（先例 V06/E01）**：C01.used_by_lessons 移除 "L05"（正文未引用 C01）；V01.used_by_lessons 增补 "L05"（正文 §2 引用 V01）。
- **publish boundary 断言同步（先例 D16/L03/L04）**：bundle 71→**72 docs**，数量断言 71→72。
- **门禁（执行会话实测，全 exit 0）**：build_site **72 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 528 cards / 2681 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **8 篇 · OK**（L05 加入检查集）；review_gate **45 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L05-deepening.md`。

## 2026-11-20 · P7.2 第六篇：L04《从文件到码流》新写教材（审读通过——「其余篇目」第二篇）

- **范围**：新写 `courses/video-rendering-journey/lessons/L04-从文件到码流.md`（**0 → 199 行**，无绑定实验）。结构：开篇直灌崩溃钩子（封装流→熵解码第一步非法指令异常，`V26`）→ 拆包流水线类比（附边界：不覆盖时间索引与容错重同步）→ §4.1 三段管线职责表（物理职责/技术边界/工业组件，Demux/Decode/Render，`V26`）→ §4.2 容器表五格式 + 码流表四编码、组合正交（objective ①）→ §4.3 MediaExtractor vs MediaCodec（`V01` ✅、FFmpeg 四子库表、工业组合三步）→ §4.4 NALU/SPS/PPS/SEI + 缺 SPS 的 DPB/黑屏后果（`V11` ✅）→ §4.5 Annex B vs AVCC 双表（起始码 vs 长度前缀、容错/随机访问相反、不可混用）+ MediaCodec CSD-0/CSD-1 直喂 AVCC ⚠️有条件成立（`V25`）→ §5 MP4 Box 树 ASCII 图 + 采样表五行 + 帧寻址流程（L02 精准 seek 的文件侧落点）→ §6 排查现场（黑屏三步倒推）+ 5 误区 → §7 容器字段走读核查（五项含预期）→ 桥句→L05。
- **新断言登记（默认 open/low）**：**V25**（Annex B vs AVCC 分界机制，附条件：CSD 配置后可直喂 AVCC ⚠️）/ **V26**（容器/码流职责分离与直灌异常）——evidence=**SRC-RN-AV-BASE**（used_by_claims 同步 +V25/+V26，原 V13/V14/V16 保留）；used_by_lessons=[L04]。review_gate 实测 **43 claims**（verified 18 / open 18 / conditional 7）误标 0。
- **审读（独立子代理，只读换人，逐条对源）**：**acceptable=true，修订 0 轮**；**40 处技术表述全部可溯源**（两张表/采样表/帧寻址逐字忠实、⚠️条件边界原样保留、V01/V11=verified 与 V25/V26=open/low 分层如实、锚点 slugify 核实）；**9 条 minor 全部修复**（繁体"偏愛"、"正交"挂接超范围改标教材推导、MediaExtractor 能力边界无出处表述删除、"解封装链路 ✅"标签与三模块表不符改"三段管线职责表"、"§1.3 原话"标签过强收窄、avcC 未释义改 CSD 口径、核查清单补"预期看到什么"三段式、MediaCodec/熵解码首现补释义、L03 桥句"L04 待建"已过时联动更新）。修复后全门禁复跑通过。
- **publish boundary 断言同步（先例 D16/L03）**：bundle 70→**71 docs**，数量断言 70→71。
- **门禁（执行会话实测，全 exit 0）**：build_site **71 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 520 cards / 2642 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **7 篇 · OK**；review_gate **43 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L04-deepening.md`。

## 2026-11-20 · P7.2 第五篇：L03《色彩与显示范围》新写教材（审读 blocker 修复后通过——「其余篇目」首篇）

- **范围**：按 handoff T2「其余篇目」顺序新写主课程教材 `courses/video-rendering-journey/lessons/L03-色彩与显示范围.md`（**0 → 168 行**，无绑定实验——labs.json 无 L03；frontmatter 无 lab 字段，validate REQUIRED_FRONTMATTER 不含 lab）。结构对照 Gold Standard：开篇发灰算术（Y16 显示成约 6% 灰阶电平、白 92%、可用级数 ≈220/256≈86%）→ 三件套类比（色板/调色曲线/翻译字典，附边界：range 是第四件事）→ §4.1 primaries/transfer/matrix 三字段独立（`V24`）→ §4.2 range 机制与错用后果（`V21`）→ §4.3 sRGB 分段函数（0.5 编码→0.214 线性算例）+ 线性工作流五条工程做法 + 双重 gamma 病因分叉（`V22`）→ §4.4 PQ/HLG 适用场景 + banding/抖动/全链路 10-bit（`V23`）→ §6 车载播放器发灰两步排查现场 + 5 误区 → §7 八项色彩管理检查清单（源 §3.3 全文）+ 零成本观察实验 → 桥句→L04《从文件到码流》。
- **新断言登记（evidence-and-claims 程序，默认 open/low）**：**V21**（limited/full 约定与错用后果）/ **V22**（sRGB 分段函数与 Alpha 例外）/ **V23**（PQ 与 HLG 适用场景）/ **V24**（primaries/transfer/matrix 三字段独立）——均为 engineering_fact，evidence=**SRC-RN-COLORMGMT**（source-registry 新增 repo_doc 条目，used_by_claims=[V21,V22,V23,V24] 双向索引一致）；used_by_lessons=[L03]。review_gate 实测 **41 claims**（verified 18 / open 16 / conditional 7）误标 0。
- **审读（独立子代理，只读换人 + 独立重算）**：首轮 **1 blocker + 8 minor**——**blocker** = "有效灰阶账"三处口径互斥（§5 的 219/239≈91.6% 分母无物理意义、§1 的 256→219≈86%、§8 的"压掉一成"）——**已统一修复**（黑 6%、白 92%、可用 220/256≈86%、损失约 14%，§1/§5/§8 同一口径）；minor 8 条（"亮度"措辞应为灰阶电平、工程做法漏帧缓冲一条、ST2084 未释义、"上表"方向词、§10 链接落点、两条延伸缺锚点、源 ✅ 与断言 open 的双层标注、banding 解法漏"加噪声"）——**全部修复**。修复后全门禁复跑通过。
- **quiz 边界（validate §10 规则实测）**：非 pilot 课不得有 quiz 文件（validate 把 quizzes/ 下每个 quiz 绑定到 pilot course.json）——为 L03 新建的 quizzes/L03.json 已按规则移除，正文 §9 来源行改述该规则；pilot 化后按规则补建。
- **publish boundary 断言同步（先例 D16）**：新增 1 篇知识文档使 bundle 69→**70**，`tools/test_publish_boundary.py` 数量断言 69→70（注释注明 78 总数−8 reviews 来源；reviews 零泄露的核心断言不变且通过）。
- **门禁（执行会话实测，全 exit 0）**：build_site **69→70 documents**（69+L03）/ 17 sections / 124 terms / 19 lessons / 7 labs / **512 chapter term cards** / **2599 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**（新增锚点 #14/#12/#15/#3/#22-yuvrgb-gpu转换/#5-10bithdr-与-av1 全部解析通过）；check_chapter_arc **6 篇 · OK**（L03 加入 arc 检查集）；review_gate **41 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L03-deepening.md`。

## 2026-11-20 · P7.2 第四篇：L13《坐标变换与 MVP》深化（审读通过，pilot 路线收官）

- **深化范围**：`courses/video-rendering-journey/lessons/L13-坐标变换与MVP.md` **89 → 235 行**（留痕会话 wc -l 实测），按 Gold Standard L01 + 十维度规范以**数学推导型**结构重写（问题→空间链→推导→数值验证→跨 API 差异→实验）：开篇双钩子（GL→Vulkan 深度全错事故 + T·R·S 顺序症状）→ 六空间表新增「缺了它会怎样」列（`V17`）→ MVP 组合顺序推导（列向量右侧作用/主序陷阱表/`M=T·R·S`，`V18`）→ 投影矩阵关键推导步骤重组（f=1/tan(fovY/2)、w_clip=-z_eye、端点验证表 -N→-1/-F→+1、数值算例 fovY=60° aspect16:9 同顶点 z=-2/-10 的 x_ndc≈0.49/0.10 近大远小、FOV 100° 对比；透视除法不能手动做的插值面原因，`V19`）→ 五 API NDC 表 + 「负视口高度只翻 Y 不改 z 范围」+ 视口公式 + UV 原点表 + FBO Y-flip 四事故（回收 L06 getTransformMatrix 伏笔）→ 视锥剔除一瞥（`r3±r0` 六平面/保守剔除/贴脸消失）→ 正交投影 w=1 → §6 排查现场（GL→Vulkan 移植，由 §4.2/§4.4 重组）+ 五行参数错误表 + 5 误区 → 桥句宣告 pilot 五课收官。
- **断言纪律**：未新增断言；**V17–V20 如实保持 open/low（engineering_fact，B10=D19 确认登记，升级待 G1）**；`V18` 附条件（GLSL/GLM 列主序；HLSL `mul(v,M)`）与 `V20` 附条件（默认约定可配置）在正文如实呈现；§11 登记原 V06 已移除。**ledger 反向索引同步**：V06.used_by_lessons 移除 "L13"（L13 已改挂 V17–V20，V06 仅留 L08）。
- **审读（独立子代理，只读换人，逐条对源 + 独立重算）**：首轮 **1 major + 7 minor**；重算全部 5 处数值（1.73205/0.97428/0.487/0.0974/0.83910）无误、两端点代数验证成立（含 Vulkan 版 -N→0/-F→1）、两张矩阵与四张表逐字对齐；**major** = 开篇把 T·R·S 顺序错误症状（绕世界原点旋转）错挂到 M·V·P 上且"看似能跑"不成立（与 §4.2 正确叙述自相矛盾）——**已修复**（症状各归其位：T·R·S→绕世界原点；M·V·P→投影套在局部坐标上整体畸变）；minor 7 条（"上表"方向词、ledger V06 used_by 未同步、transpose 修辞冒充跨设备随机性、"与近平面求交"内部引用失准、贴脸消失归因并列失准、#2-深度缓冲锚点缺失×2、"投影空间"与正文"裁剪空间"命名映射）——**全部修复**。修复后全门禁复跑通过。
- **四处联动（checkpoint）**：两层 course.json L13 checkpoint 均补第 3 题「MVP 对列向量的正确相乘顺序是？」（quiz Q3，挂 V18）；正文 §9 同步三题（Q1 加"投影空间=裁剪空间"括注）。
- **门禁（执行会话实测，全 exit 0）**：build_site **69 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2561 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **5 篇 · OK**；review_gate **37 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **里程碑**：**pilot 路线（L01→L02→L06→L11→L13）五篇全部达到深化质量——L01 为 P6 Gold Standard，L02/L06/L11/L13 本窗口四篇深化并全部审读通过。** P7.2 下一阶段 = handoff T2「其余篇目」（主课程 L03 起的新篇目生产）或按序转 P8，见 NOW.md 决策点。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L13-deepening.md`。

## 2026-11-20 · P7.2 第三篇：L11《RenderGraph 与资源生命周期》深化（审读通过）

- **深化范围**：`courses/video-rendering-journey/lessons/L11-RenderGraph与资源生命周期.md` **85 → 193 行**（留痕会话 wc -l 实测），按 Gold Standard L01 + 十维度规范以**工程机制型**结构重写：开篇失控账（5 Pass 最坏 10 条顺序依赖、8 Pass 28 条；4 Pass×8MB=32MB 显存失控）→ 仓库排班表类比（附边界：不管画质、一次编译多帧复用）→ 概念层次表（L3 FBO/特效链 → Pass → RenderPass/Subpass → RenderGraph，`E03` 出处）→ §4.1 Pass 正式名与「Pass≈RenderPass 阶段 / RenderPass≠RenderGraph」三层辨析 + loadOp/storeOp TBDR tile 优化（显式API §6 ✅）→ §4.2 两大机制（aliasing：首写/末读定生命周期、峰值=max 而非 sum、主文档 40%+ **[测试数据-仅供参考]**；自动 barrier：Write-Before-Read/避免过度同步/insertDebugMarker 非同步原语警示）→ §4.3 边界（不宜/必须场景 + 四维量化表 + 评测三原则，`C06` conditional）→ §5 DAG 形式化 + aliasing 峰值公式三件套（24→16 MB 教学算例与主文档实测口径分离标注）→ §6 排查现场（RenderDoc 快照对比，由 §2.2/§2.3 重组）+ 5 误区 → §7 实验（rendergraph-dag 四任务）→ 桥句→L13。
- **数据层一致性**：frontmatter **objectives 对齐两层 course.json**（消除三层措辞漂移）并补齐 source_documents（显式API §6 / 概念引入说明）；两层 course.json L11 checkpoint 均补第 3 题「RenderGraph 主要解决什么问题？」（quiz Q3，挂 E04），正文 §9 同步三题——四处联动补齐。
- **断言纪律**：未新增断言；**P06 三处齐挂补全**（claim-ledger P06.used_by_lessons 原已含 L11 → frontmatter claims +P06、§11 断言状态说明补条「open，contested——40% 待逐案核验」；正文引用该数字一律带 [测试数据-仅供参考]）；`C06` **conditional**（条件：深度≥3 且有分支；单 Pass 不宜）与 `E04` 附条件在正文三处复现且口径一致；quiz claim_ids {C06,E04} ⊆ claims。
- **审读（独立子代理，只读换人，逐条对源）**：**acceptable=true，修订 0 轮**；**52 处技术表述全部可溯源**（含五锚点 slugify 复算命中、labs.json 数字逐字吻合、"40%+ 实测参考 vs 33% 教学算例"来源与口径分离被点名为引用纪律示范）；**8 条 minor 全部修复**：①"特定机型复现"无出处改引显式API §5.5 典型表现；②L08 链接补 #23-管线与状态 锚点、L06 行补课内链接；③工具全名 Nsight Graphics Timeline；④层次表 RenderPass 行补"与同步"对齐源文档；⑤写→读/写→写细分标注 lab 出处；⑥主文档 Frame 口径→lab Pass 区间的适配如实注明；⑦公式升级 $$…$$（lab formula 原文入正文）；⑧P06 跨层挂载补齐 + §11 状态说明。修复后全门禁复跑通过。
- **门禁（执行会话实测，全 exit 0）**：build_site **69 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2530 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **5 篇 · OK**；review_gate **37 claims 误标 0**；test_publish_boundary **11 tests OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L11-deepening.md`。

## 2026-11-20 · P7.2 第二篇：L06《纹理桥与零拷贝》深化（审读通过）

- **深化范围**：`courses/video-rendering-journey/lessons/L06-纹理桥与零拷贝.md` **85 → 200 行**（留痕会话 wc -l 实测），按 Gold Standard L01 + 十维度规范重写：开篇数字张力（解码 YUV420 3.11 MB → 特效链消费 RGBA 8.29 MB 两段账 + 实验 note 弯路账 16.6 MB/帧 ≈ 498 MB/s @30fps）、仓库+钥匙类比附边界声明（钥匙交接有排队成本、显存内格式转换躲不掉）、§4.1 updateTexImage/getTransformMatrix 逐段对应主文档 §3.2（含六阶段所有权视角）、§4.2 OES 三条限制 + 第一道转换 Shader（含 GLSL 教学骨架，标注示意）+ FBO 管线图对应主文档 §7.4、§4.3 PC 独显 vs 移动 SoC 通路对照表（E01/E02）、§5 软硬解两条搬运账 + 公式三件套（符号/算例/后果）、§6 排查现场（ByteBuffer 回读 vs 绑定 Surface，由主文档 §2.2/§2.3 重组）+ 5 条误区、§7 实验四任务逐条对应机制、§8 因果链复述、桥句指向 L11（与 pilot 层 course.json next=L11 一致）。
- **断言纪律**：未新增断言（newClaims=[]，重要结论由既有 V04/V05/C02/E02/P02 或主文档 ✅/⚠️ 锚点覆盖）；**E01 三处齐挂扩展**（正文 4 处引用 → frontmatter claims +E01、claim-ledger E01.used_by_lessons +L06、document-registry 重建；先例 = L01 frontmatter+正文+ledger 三处齐挂）；**P02 如实保持 open/low（contested）**（B11 确认保留挂载）、C02 conditional 如实、E02 附"先说平台"条件且正文表格先说平台。
- **审读（独立子代理，只读换人，逐条对源）**：**acceptable=true，修订 0 轮**；40 处技术表述 39 处逐条溯源（五断言状态/条件/used_by 与 claim-ledger 逐字核对、三个锚点经 slugify 解析命中、labs.json 六阶段/四任务/selfTest/note 数字逐字吻合、算术 8.29/3.11/16.6/498 全对）；**11 条 minor 全部修复**：①§7.2 ✅ 徽标错标（主文档 §7.2 无验证标记，改由 V04 背书表述）；②"实验代码 note 原文"实为 selfTest（2 处改标）；③"裁剪"超源删除（主文档只写旋转）；④§1/§6 RGBA-YUV 口径借用改为两段账（YUV 3.11 读回 + RGBA 8.29 上传 ≈ 340 MB/s @30fps）；⑤E01 簿记三处齐挂；⑥实验任务 2 机制映射改指 §3/§5；⑦实验显示名改用 labs.json 标题《解码帧到纹理的所有权迁移实验》；⑧BufferQueue/FBO/Effect Pass 首现补一句话解释；⑨quiz Q3 四处联动补齐（两层 course.json checkpoint + 正文 §9 + 来源行声明）；⑩§2.2/§3/§3.2/§7.3/§8.3 小节引用升级为锚点链接（validate 锚点解析全通过）；⑪Premultiplied Alpha 移出本章术语降为延伸。修复后全门禁复跑通过。
- **四处联动（checkpoint）**：`tools/course.json` 与 `courses/video-rendering-journey/course.json` 的 L06 checkpoint 均补第 3 题「手机 SoC 的 CPU→GPU 数据通路走 PCIe 吗？」（对应 quiz Q3，挂 E02）；正文 §9 同步三题；validate §11 覆盖检查通过。
- **门禁（执行会话实测，全 exit 0）**：build_site **Wrote web\content.js——69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards generated / 2497 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **5 篇 · OK**；review_gate **37 claims（18 verified / 12 open / 7 conditional）conditional/contested 被标为 verified：无**；test_publish_boundary **Ran 11 tests — OK**。
- **边界**：一律未 commit/push（本条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L06-deepening.md`；L02 审读遗留的 1 条 major（labs.json/app.js「DTS ≤ PTS 恒成立」静态句与五帧表冲突，涉 `web/assets/app.js:2350`）不在本篇范围，仍待人工裁决（见 `reviews/G2-L02-deepening.md`）。

## 2026-11-20 · P7.2 第一篇：L02《时间戳与同步》深化（审读通过）

- **深化范围（改动文件 ×2，frontmatter 一字未动）**：`courses/video-rendering-journey/lessons/L02-时间戳与同步.md` **125 → 217 行**（本留痕会话 `wc -l` 复核实测 217），正文按 Gold Standard L01 样板「直观→原理→数学→架构→实践」递进；`courses/video-rendering-journey/quizzes/L02.json` 保持 Q1/Q2/Q4 prompt 与两层 course.json checkpoint 逐字一致、四题参考答案补依据与锚点，新增 Q5（-bf 0 边界，挂 V03）与 Q6（外部主时钟场景，挂 V10），claim_ids 全部 ⊆ frontmatter claims。
- **正文要点（11 项）**：①开篇钩子补数字张力（PTS=2 的帧排在解码第 3 位、30fps 帧位 33.3ms、2 小时视频 216,000 帧）与三问题预告；②前置节补 I/P/B 帧与 GOP 一句话解释（诊断「新概念不突现」），DTS/PTS 定义改用主文档 §4.1 ✅段原文口径；③直观认识保留流水线/队列类比并新增电影院类比，均附边界声明；④§4.1 依赖链推导+双时间线 ASCII 图+五帧表逐行注解（每帧为什么这样排）+重排序缓冲机制（lab selfTest 口径）+-bf 0 边界；⑤§4.2 新增三种主时钟对照表（修复诊断 D-L02-5：视频/外部时钟策略缺漏），V10 论证「人耳对音频中断最敏感」并如实注明市场占比无公开统计；⑥§4.3 Δt 公式三件套（符号含义→数值算例 +10ms/-50ms→工程后果），丢帧阈值为工程参数不代拟数字，多路晶振漂移数字保留[测试数据-仅供参考]标记、PLL ±0.1% 保留⚠️有条件成立；⑦§4.4 精准 seek 三步+seek 区间示意图+关键辨析（追赶期在丢陈旧帧 vs 目标首帧不被误丢、recover 非官方状态名）+代价边界（V15 conditions），全部挂 V15；⑧§5 新增「解码名次−显示名次」启动缓冲下界推导及 30fps≈33ms 算例（纯由 ✅五帧表算术推出，标注保守下界与硬解边界）；⑨§6 两个可复述排查现场（多路越播越歪→晶振漂移/PLL；seek 差半口→默认 seek 止步定位）+两处机制复用案例（倒放 Jitter Buffer/全 I 帧预转码=解码与播放链路 §8.2 挑战 2、硬解回退复用静默追赶=§8.4）+6 条误区（新增「B 帧画质救星/杀手」不下超源结论）；⑩§7 实验按 labs.json 四个 tasks 给「做什么→预期看到→对应机制」并声明实验边界；⑪桥句保留 L06（与 pilot course.json next 一致）。
- **新增断言：无（newClaims=[]）**：claim-ledger.json 与 source-registry.json 均未改动。原因——validate_site.py §8 要求每条断言的每个 evidence source_id 同步登记 source-registry.json 的 used_by_claims 反向索引，而本轮任务仅允许追加 claim-ledger.json、禁止改 source-registry.json，新增任何断言（如重排序缓冲深度、倒放方案、回退状态机复用，可按 V21 起顺延登记）都会导致门禁 FAIL；本次正文所有重要结论均由既有断言 V03/V10/V15/V16 或主文档 ✅/⚠️ 锚点覆盖。若后续要登记需按 evidence-and-claims.md 程序同时编辑两个 evidence 文件。
- **审读结论（审读员，非 G2 人工评分）**：**acceptable=true，修订 0 轮**；遗留问题 7 条（major 1 + minor 6）：**major** = tools/labs.json pts-dts-timeline stages「同步约束」desc + `web/assets/app.js:2350` 静态句「DTS ≤ PTS 恒成立」与逐帧计数「PTS−DTS = −1」（lab 模型 B0 dts=2>pts=1，app.js:2146 frames）及 L02:72-78 五帧表（B: PTS 2/DTS 3）三处冲突——L02 §7 任务 3 让学习者查看 PTS−DTS 时必然撞见矛盾，修法方向为改 stage 文案为「解码完成时刻先于显示时刻（启动缓冲补偿序位差）」或删句并同步 labs.json 与 app.js 两处；**minor ×6** = L02:130「MediaCodec BUFFER_FLAG_DECODE_ONLY」无版本限定（平台公开标记自 API 35（Android 15）才有，Media3 早期为内部常量 C.BUFFER_FLAG_DECODE_ONLY，已在线核验）、L02:215 称 8 个本章术语「权威定义在 tools/glossary.json」实仅 PTS/DTS/主时钟/AV Sync 4 词在内（124 词逐一名单核对，drift/重排序缓冲/GOP/精准 Seek 不在）、L02 frontmatter:6-9 objectives 与两层 course.json 措辞漂移（语义兼容不误导，Gold L01 三层逐字一致对照；本轮任务禁令「不碰任何 frontmatter 字段值」未对齐，需人工一行改写）、L02:117/129（另 92 单调时钟）V-Sync/ppm/解封装器首次出现无一句话解释或术语链接（V-Sync 有 VSync 术语卡可链，D4 边缘缺口）、L02:96 主文档标注 [AI-生成] 的「ExoPlayer、IjkPlayer、VLC 默认采用音频主时钟」以陈述句呈现仅靠句尾括注披露（标准 §5 要求该类内容不得写成确定事实，修法为「主文档（[AI-生成] 标注）指出……」句式前置）、evidence/claim-ledger.json V15.evidence[0].locator 写「Why is seeking slow」而 Media3 troubleshooting 实际标题为「Why is seeking in my video slow?」（内容已在线核验存在）。逐条修法方向见 `reviews/G2-L02-deepening.md`。
- **门禁（执行会话实测，全 exit 0）**：build_site **Wrote web\content.js——69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards generated / 2459 KB**；validate_site **11 checks passed, 0 warnings, 0 failures**（含全部链接/锚点解析与 quiz/checkpoint/claim 覆盖检查）；check_chapter_arc **5 篇 · OK**；review_gate **conditional/contested 被标为 verified 的 claim：无；未挂载任何课程的 claim（open/conditional 可预期）：['P03']**；test_publish_boundary exit 0。
- **边界**：一律未 commit/push（本留痕条目在内）；G2 评分表留空待人工（AI 不自评），材料新建于 `reviews/G2-L02-deepening.md`。另登记两处待人工状态漂移：glossary.json AV Sync 词条仍写「seek 后还要进入 recover 状态」与 V15 conditions「recover 非 ExoPlayer 官方状态名」口径不一致（glossary.json 不在允许改动范围，建议人工软化措辞）；quiz 新增 Q5/Q6 若 G2 认为题量超纲可删（删除后三个 checkpoint 覆盖仍由 Q1/Q2/Q4 满足，validate 已验证）。openQuestions 5 条全量见 G2 材料。

## 2026-11-20 · T1 命名迁移收尾：remote 切换 + 引用更新 + 全量验证（六道门禁全绿）

- **remote set-url ×2**：Engine origin → `https://github.com/Vin535LFJ/ai-knowledge-to-learning-engine.git`；Skills 库 origin → `https://github.com/Vin535LFJ/matt-pocock-skills-zh-cn.git`（upstream-en/zh 未动）。GitHub 改名核实（留痕会话 `git ls-remote origin HEAD` 复核实测，两仓均 exit 0）：远端 HEAD 分别为 `e848d2801ec9940e154b9bf40bc26198a5d197ba` / `e1936f23e6e149c581124cc218e79860c07108ef`，旧 URL 重定向兜底不再依赖。
- **引用更新统计（锚定精确替换，Q2 含品牌文案）**：Engine 24 文件、Skills 库 5 文件、Program 5 文件、OmniWorld-Engine 5 文件。`window.RENDER_NOTES` 四文件契约、上游引用（vinvcn/mattpocock）、历史层文档均未动；引用更新改动 commit/push 待授权（交接文档 §6 范围）。
- **content.js 重建（build_site 实测）**：Wrote `web\content.js`——69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards generated / 2426 KB。
- **六道门禁（T1 实测，全部 exit 0）**：build_site（数字见上条）；validate_site **11 checks passed, 0 warnings, 0 failures**；check_chapter_arc **5 篇 · OK**；review_gate **37 claims**（verification.status：verified 18 / open 12 / conditional 7；claim_type：verified_fact 13 / engineering_fact 13 / conditional 7 / contested 4）conditional/contested 被标为 verified：无；test_publish_boundary exit 0；check-translation exit 0（翻译审计通过）。
- **残留清点（Phase 5 验证项，T1 实测）**：本地回填注释 **4 个文件（预期 4，符合）**；活跃层残留 **26 条**；`claude plugin validate . --strict` **not-installed（待验）**——`command -v claude` 与 `where.exe claude` 均无结果（留痕会话复核同为 exit 1），本机无 claude CLI，无法执行，按要求不算失败。
- **OmniWorld 跟进（Q4）验证（留痕会话复核实测）**：`OmniWorld-Engine/skills-lock.json` **37 条 `"source"` 全部 = `Vin535LFJ/matt-pocock-skills-zh-cn`，旧 slug 0 条**（grep -c 实测 37/0）；`AGENTS.md:74` 安装命令已指新 URL，pin `skills@1.7.1` 保留。
- **笔①（Engine 本地提交，未 push）**：`cf917386e22af0cf0a4a9b665fc48d41c1ca9130`（2026-11-20 02:30 +08:00，"docs: decision-kit 七项裁决执行（D17–D19）+ 门禁复跑留痕（含重建 content.js）"；master ahead origin/master 1，push 另行授权）。
- **遗留阻塞**：无（阻塞列表为空）；G1/G2 关卡待人工宣布通过（G2 评分表）、G3 未通过、在线发布（D02）未授权——均为主线既有状态，非 T1 新增阻塞。

## 2026-11-19 · D19：decision-kit 收尾（B10/B11/B12 全 A，七项全闭合）

- **裁决**：B10=A（确认 V17–V20 登记 open，升级另裁）、B11=A（确认 L06↔P02 保留挂载）、B12=A（stash 继续保留，提交稳定后重议）。Resolution 回填三票；decision-kit 总表 **7/7 已决**；REVIEW_STATUS B10/B11/B12 标注。
- **执行边界**：三项均确认现状，零内容/数据改动；stash 未触碰；V17–V20/P02 状态不变。
- **续跑点推进**：P7.2 逐篇深化（一次一篇，Gold Standard L01 基准；pilot 下一篇 L02）→ P8 → P9 → P10。G1/G2 裁决项闭合 ≠ 关卡通过（G2 评分表仍待人工）。
- **门禁（记录性改动后复跑）**：validate 11 checks / 0 FAIL / 0 WARN；review_gate 37 claims（18v/12o/7c）误标 0——与 D18 后一致，无漂移。bundle 无变化（reviews/状态文档不进学习站），未重建。
- **边界**：未 commit/push（D09）；G3 未通过、D02 未授权。

## 2026-11-19 · D18：V13/V14 升级 verified（decision-kit 第二轮）

- **裁决**：V13=A（修正后升级 verified/high）、V14=A（升级 verified/high + 保留两条平台差异 conditions）。用户会话结构化裁决；Resolution 回填 V13.md/V14.md，decision-kit 总表与 REVIEW_STATUS B7/B8 同步。
- **执行**：`evidence/claim-ledger.json` V13/V14 状态升级（conditions 保留，note 记录依据）；L01 §11 断言状态说明更新；PROJECT_CURRENT_STATE 断言数更正 31→**37**（P6 基线遗留口径，含 V15–V20）。历史审计快照不改写。
- **门禁（升级后复跑，实测）**：build **69 docs** / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2421 KB；validate **11 checks / 0 FAIL / 0 WARN**；arc **5/5 OK**；publish boundary **11/11 OK**；review_gate **37 claims（18 verified / 12 open / 7 conditional）误标 0**（升级前 16v/14o/7c，恰好 +2 verified / −2 open）。content.js 已重建。
- **边界**：未 commit/push；G1/G2/G3 仍未通过；剩余裁决 B10/B11/B12。

## 2026-11-19 · D17：B4=B / B15=A 裁决执行（decision-kit 首轮）

- **裁决记录**：B4=B（L01 认可为 Gold Standard + minor 修订）、B15=A（C1–C7 全部立项入队，执行按 P8 节奏）。用户会话结构化裁决，Resolution 已回填 B4.md / B15.md，总表 README 同步；DECISIONS D17 记录。
- **B4 minor 修订（已执行）**：
  - L01 §4.2：补 4:2:0 记号精确口径（J:a:b 采样比例记号；水平垂直均 1/2 降采样；"0"=垂直共享同一组色度采样），与主文档"水平和垂直方向均 1/2 降采样"口径对齐（G2-curriculum-review §minor 建议）。
  - V13 误导性因果并列修正（三处同步）：主文档 `01-基础理论/音视频基础理论.md` §2.1（删除"因此"因果链，改为两种感光细胞分工 + 色度通路特性 + 显式非因果注记）；L01 §3（同口径重写）；`evidence/claim-ledger.json` V13 claim 文本 + note。**V13/V14 状态保持 open/low，未升级（升级待 V13/V14 票人工裁决）。**
- **B15 执行边界**：仅登记立项（队列范围 C1–C7），本轮不启动研究、不改断言；P8 启动时排期。
- **本地目录改名（程序级，用户批准）**：仓库目录现名 `ai-knowledge-to-learning-engine`（原 Render_Notes）；git 完好 HEAD=`e848d28` 起步；GitHub 仓库名/remote 仍旧名待用户同步，过渡态不改 remote。
- **门禁（修订后复跑，实测）**：build **69 docs** / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2416 KB；validate **11 checks / 0 FAIL / 0 WARN**；arc **5/5 OK**（L01/L02/L06/L11/L13）；publish boundary **11/11 OK**；review_gate **37 claims（16 verified / 14 open / 7 conditional）误标 0**（V13 仍 open，未升级）。content.js 已随修订重建。
- **边界**：未 commit/push（D09）；G1/G2/G3 仍未通过；剩余裁决 V13/V14/B10/B11/B12。

## 2026-11-19 · 迁移收尾 + 残留副本清理 + 状态修正（Program 会话，低风险状态更新）

- **PD-002 收尾完成**：Render_Notes 自 `GITCODE\Render_Notes` 整体迁入 `GITCODE\AI-Knowledge\Render_Notes`（绑定 AI-Knowledge 的会话执行 Move-Item，一次成功）；git 完好 HEAD=`e848d28`，工作树干净，远程不变。
- **迁移后门禁复跑（只读）**：validate **11 checks / 0 FAIL / 0 WARN**；review_gate **37 claims（16 verified / 14 open / 7 conditional）误标 0**。工具链全相对路径解析，迁移零破坏。
- **残留副本清理（用户批准，Q3）**：`site-vitepress/docs/program-office-delivery/` 10 份统筹办公室旧副本（gitignored、内容过时、处于 build_vitepress_content.py rmtree 范围）→ 系统回收站（recoverable=true）；Test-Path 复核 False。PD-Q8 同类清理的漏网位置，权威原件在办公室。
- **状态修正**：WORKFLOW_STATE 程序级收口段"迁移待办"过期行更新为完成事实。
- **边界**：未改任何知识内容/claim 状态/课程数据；未 commit/push（D09）；G1/G2/G3 仍待人工裁决（decision-kit 七项），续跑点不变。
- **程序级记录**：`AI-Knowledge\ai-knowledge-program\`（NOW.md / plans/2026-11-19-rename-audit-and-migration.md §6 裁决记录：改名暂不执行、范围含品牌文案、OmniWorld-Engine 跟进已授权待执行）。

## 2026-11-19 · 程序级收口：裁剪生效 + 三批提交（D16 / PD-Q1/Q2/Q7/Q8）

- **裁决**：用户批准 PD-Q7（PD-003 裁剪：Engine 单活跃线；P2 Skill/P03/P04 冻结在现有成果，冻结≠删除；不新建收录类项目）+ PD-Q1/Q2/Q8 按推荐执行。程序级权威记录在 `AI-Knowledge\ai-knowledge-program\decisions\`。
- **三批拆分提交**：`5a4de84`（D15 治理基座，31 文件）/ `a45ffa9`（CHG-0001 P7 教材修复+P2 Skill，33 文件）/ `7c05bc7`（P8/P9 预研：kcr_impact 只读影响分析+publish allowlist+decision-kit，20 文件）+ 本留痕笔。
- **测试修正**：`test_publish_boundary.py` 断言笔误 77→69（注释"移除 8 篇 reviews 后"与断言值矛盾），修正后 **11/11 OK**。
- **发布边界生效**：allowlist 使 reviews/ 不再进入学习站 bundle，build 实测 **69 docs**；archive 行为不变（D10.4）。口径更正：融合基线记录中"知识文档 85→77"为另一会话口径，当前 allowlist 实测知识文档 69（77 为含 8 篇 reviews 的旧总数）。
- **PD-Q2**：P03 本地 git `dec60ba`（39 文件）/ P04 本地 git `942530b`（30 文件），均无远程；测试 **25/38 OK** 本轮实测。
- **PD-Q8**：`program-office-delivery/` 10 份交付副本→回收站（可恢复，原件在办公室）；`.qoder-input-images/` 加入 .gitignore。
- **门禁实测（收口复跑）**：build 69 docs / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards · validate **11 checks 0 FAIL 0 WARN** · arc **5/5** · review_gate **37 claims（16 verified / 14 open / 7 conditional）误标 0** · publish boundary 11/11。
- **待办**：Render_Notes 迁入 AI-Knowledge（会话占用，需绑定其他目录的会话）；G1/G2/G3 人工裁决（decision-kit）；stash（B12）。
- **git 同步**：四笔已 push（`474c667..9bfa732`，首次遇网络 RPC/SSL 抖动重试成功，ls-remote 实测远端 HEAD=`9bfa732`）。仅 push 源码，未在线发布（D02）。

## 2026-11-19 · 多智能体文档治理基座（D15 / ADR-0001）

### 采纳的架构（用户提案 + 四项裁决）
在 D14 统一仓库之上增量落地治理能力，不改变目录归属：宪法四件套 / MADR（`decisions/` + ADR-0001；`DECISIONS.md` 保留为历史索引，不机械拆分）/ 文档类型×状态机 + frontmatter schema（`standards/`）/ 模板（change-proposal、agent-handoff）/ 轻量变更流程（`changes/`，借鉴 OpenSpec 自研）/ 文档注册表（frontmatter 事实源 + 脚本生成）/ 全客户端适配入口（只跳转不复制）。

### 新增文件
- `.agent/constitution/`：PROJECT_PRINCIPLES / AGENT_RULES（写所有权五规则）/ DOCUMENTATION_POLICY / HUMAN_APPROVAL_POLICY
- `.agent/decisions/`：README（MADR 索引）+ adr-template + 0001-adopt-documentation-governance.md
- `.agent/standards/documentation-types.md`（type/status 枚举 + frontmatter schema + level 派生）
- `.agent/templates/`：change-proposal.md + agent-handoff.md
- `.agent/changes/README.md`（轻量变更流程）
- `.agent/indexes/`：README + document-registry.schema.json + document-registry.json（生成物）
- 适配入口：CLAUDE.md、AGENTS.md、.cursor/rules/render-notes.mdc、.github/copilot-instructions.md、.gemini/GEMINI.md
- `tools/build_document_registry.py`

### 改动
- `.agent/README.md` 升级（分区索引 + constitution 指引 + frontmatter 写入规则）
- 治理文档自身补 YAML frontmatter（dogfooding 修正：初版 blockquote 元数据无法被注册表识别）
- 三个构建工具排除列表新增 `.gemini`/`.cursor`/`.github` + 根 `CLAUDE.md`/`AGENTS.md`
- `.gitignore` 追加 `.agent/runs/`

### 实测
- 注册表初版：**104 篇文档**（frontmatter 26 / unregistered 78 存量渐进补齐；L1 19 / L2 14 / L3 13 / unclassified 58；status：active 14 / approved 5 / draft 6 / archived 1 / unregistered 78）
- build **77 docs 不变**（适配入口与 `.agent` 均排除，零污染）/ validate **11 checks 0 FAIL 0 WARN**

### 边界
- 不预建 6 个空技能目录；不批量给存量文档打状态；DECISIONS 历史不拆分；Run logs 本地化；注册表一致性门禁接入 validate 留 P8
- 待 commit+push（用户授权后执行；与上轮清理分两笔提交）

## 2026-11-19 · 智能体文档统一仓库 .agent/（D14）

### 结构变更（用户裁决四项：文档迁移+脚本留原 / reviews/ 不动 / zcode 归档并提交 / README 合一）
- 建立 `.agent/` 公共智能体文档仓库（入 git）：`skills/research-to-learning/`（SKILL.md + references 5 篇 + assets 2 篇，自 `.workbuddy-ai/skills/` 迁入）、`plans/plan-sess_a45a3e3b-….md`（自 `.zcode/plans/` 归档，B14 裁决：归档并提交）。
- `.workbuddy-ai/` 只做索引：新增 `README.md` 索引；技能 `SKILL.md` 改为发现 stub（frontmatter 保留）；`scripts/check_chapter_arc.py` **不迁移**（门禁命令路径不变，迁移后实测可运行）；`memory/` 受保护不动。
- `.zcode/` 清空后移除（回收站可恢复）；`old_content.js.tmp` 仍待 B14 清理裁决。
- 规则与总索引：`.agent/README.md`（读取规则 / 索引 stub 规则 / 写入规则 / 禁区 / bundle 隔离 / 统一索引）。

### 引用同步
- 路径引用更新：`README.md`、`00-导航与索引/一帧画面的探索之旅.md`（2 处）、`NEXT_PHASE_PLAN.md`、`courses/video-rendering-journey/G2-审核材料-P6.md`、`reviews/G2-curriculum-review.md`、`PROJECT_CURRENT_STATE.md`（结构树 + §4.4）、`IMPLEMENTATION_PLAN.md`。
- 三个构建工具排除列表新增 `.agent`（`tools/build_site.py` / `tools/validate_site.py` / `tools/build_vitepress_content.py`），防知识 bundle 污染。
- 门禁命令（`check_chapter_arc.py` 路径）不变，WORKFLOW_STATE / README / courses README / review_gate.py 无需改动。

### 实测（迁移后重建）
- build：**77 documents / 18 sections / 124 terms / 8 units / 19 lessons / 7 labs / 559 term cards / 2510 KB**（= 69 知识 + 8 reviews；`.agent` 与 `.workbuddy-ai` 均排除，篇数与迁移前一致，无污染）。
- validate：**11 checks / 0 FAIL / 0 WARN**；arc：**5/5 OK**；review_gate：**33 claims 误标 0**。
- 边界：未升级任何 claim；未填人工结论；stash 未动（B12）；`old_content.js.tmp` 未动（B14 部分）。

### git 同步（2026-11-19 用户授权"授权 commit + push"）
- 结构治理 commit **`f5d4ecf`**（26 文件，+258/−91；git 识别 7 处 100% rename）已 push 到 origin/master（`656d107..f5d4ecf`）；`ls-remote` 实测远端 HEAD=`f5d4ecfa65480abcb5c276617c227c5da9d89cfb`，本地与远端同步。**仅 push 源码，未做在线发布**（D02 未授权）。

### 清理（2026-11-19，用户授权）
- 删除临时备份 `old_content.js.tmp`（2.35MB，Loop 1 的 content.js 安全备份，使命已完成；走回收站可恢复）。
- 清理 3 处过期计划引用（`DECISIONS.md:5` / `IMPLEMENTATION_PLAN.md:3` / `WORKFLOW_STATE.md:5`）：原指向仓库内不存在的 `.workbuddy-ai/plans/quantum-nebula-newton-ffFN4E3P.md`，改为如实说明——计划原件位于用户目录 `~/.workbuddy-ai/plans/`（会话级产物，不入仓库），关键裁决已萃取至 `DECISIONS.md` D01–D14。D14 已知问题就此关闭。
- 门禁复跑：build 77 docs / validate 11 checks 0 FAIL 0 WARN（content.js 同步重建）。

## 2026-11-19 · Master Prompt V3.0 · Loop 2 裁决后执行（部分）

> 收到用户裁决（D12）+ 新增 Knowledge Change Review 机制需求（D13）。网络恢复，权威来源核验完成。

### 裁决记录与机制设计
- DECISIONS.md 新增 **D12**（B1–B6/G1-01/G1-02 逐项裁决，含待定项 B4/B10–B15 不视为同意）+ **D13**（引入 KCR 机制）。
- 新增 `reviews/KNOWLEDGE_CHANGE_REVIEW.md`：KCR 五阶段（影响分析→变更提案→人工审核→增量更新→验证归档）+ impact/proposal/decision JSON schema + 与现有 tools/evidence 集成方案 + "新 GPU 同步机制" worked example。实现归 P8（D3/D4）。

### 权威来源核验（G1 §7 增补）
- SurfaceTexture：正确 `SurfaceTexture.getTransformMatrix()`（AOSP/NDK 官方），`glGetTransformMatrix()` 不存在 → 勘误解码链路:124。
- Pass 阈值：Frostbite GDC 2017/Vulkan 无硬阈值，属启发式 → 统一 ≥3 并软化，勘误跨平台:205。
- V13 生理：核心高置信支持（Wikipedia 引 Winkler 2001/Livingstone 2002/ACM），但杆/锥因果属简化 → 建议修正表述后升级（待人工，本轮未改 V13/L01）。
- seek：Media3/FFmpeg/MediaCodec/ExoPlayer 证实静默解码追赶+首帧强制渲染；原"禁止立刻丢帧"表述不准确。

### 已执行（已裁决安全项 + Category A）
- **B2**：tools/course.json L12.next L15→L13；一致性脚本复跑主线 L00→…→L18 先修全满足（branch=[]，ALL CONSISTENT）。
- **B5**：README 三处数字按实测更新（26 主文档/57 非归档 md/7 实验/124 术语；保留 chat 链接）。
- **B3**：lesson-quality-standard.md 采纳为可迭代基准。
- **A1**：L01 行数约300→239（CHANGELOG/G2材料）；PROJECT_CURRENT_STATE claim/source 29/15→31/16 + V3.0 真值指引。
- **A3**：build_site.py 排除 .zcode/（消除 bundle 污染）。
- **A4**：学习路径指南.md 补 U7/程序化几何 L17/L18（W10+ 行）。
- **A5**：concepts.json K-STRIDE source_claim V02→V14。
- **C2/B9 勘误**：解码链路:124 API 名；跨平台:205 Pass 口径。

### P7.1 第一项 L02 修复（blocker G-T1/G-T2）
- 新断言 **V15**（精准 seek 静默解码追赶+首帧强制渲染）/**V16**（Δt 分级同步+多路 PLL），默认 open；新来源 SRC-MEDIA3-SEEK（official_doc）/SRC-RN-DECODE-PIPELINE（repo_doc）；V16 复用 SRC-FFMPEG-DOC/SRC-RN-AV-BASE 反向索引。
- 两层 course.json L02：目标[2] 改写为准确 seek 表述；checkpoint[1] 失实"强纠偏区"→"Δt 正/负处理"；新增 checkpoint[2] seek。
- L02 正文重写：§4.3 夸大引用改为真实 Δt 两分支+PLL⚠️条件；新增 §4.4 精准 seek；§4.1 补 I-B-P-B-P 五帧表；§5 Δt 公式；§6 误区修正；§9 三题对应三 checkpoint；§11 断言状态说明。
- quizzes/L02.json 重写为 4 题（Q1 B帧 V03 / Q2 Δt V16 / Q3 主时钟 V10 / Q4 seek V15），覆盖 3 checkpoint。

### 门禁（本轮实测）
- build **77 documents**（69 知识 + 8 reviews；.zcode 已排除）/ 18 sections / 124 terms / 19 lessons / 7 labs / 559 term cards。
- validate **11 checks / 0 FAIL / 0 WARN**；arc **5/5 OK**（含重写 L02）；review_gate **33 claims（16 verified/7 conditional/10 open）误标 0**；一致性脚本 ALL CONSISTENT。

### 边界与待续
- 未 commit/push（D12.11）；未升级任何 claim（V13/V14/V15/V16 均 open 待 G1）；未填人工结论。
- **git 同步（2026-11-19 用户授权"同步最新更改到github"）**：commit **`d4a9620`**（27 文件，+1289/−53：Loop 2 裁决执行产物 + reviews/ 8 份审核材料 + KCR 机制文档），已 push 到 origin/master（`650bb14..d4a9620`，`ls-remote` 实测远端 HEAD=`d4a962089254e6ad419ce1e010a1a969c381f7f2`，本地与远端同步）。`.zcode/`（外来 agent 产物）与 `old_content.js.tmp`（临时备份）按 B14 未纳入；**B13 由本次同步授权解答：reviews/ 已纳入 git**。
- **未改 L01**（B4 待用户阅读；V13 表述修正建议待裁决）；未动 archive/memory/vendor/index.html/两份方案；外来产物 .zcode/old_content.js.tmp/stash 未触碰（B12/B14 待裁决）。
- 待续：P7.1 L06（第三项）/L13（第二项，待 B10 断言登记裁决）/L11（第四项）；B6 VitePress 本地构建排 P10。
- 仍待人工：B4（L01 认可）、B7/B8（V13/V14 升级）、B10–B15。

## 2026-11-19 · Master Prompt V3.0 · Loop 1 审核准备

> 审核驱动开发：本轮只做审核材料与分类，**不执行依赖人工裁决的修改**。产物在 `reviews/`（7 文件）。

### 仓库复核与基线（实测）
- 本地 HEAD=`650bb14`，origin/master 引用同值；**本 turn `git ls-remote` 因网络/DNS 中断受阻**（Could not resolve host），远端新鲜同步待网络恢复复核，不声称已验证。
- 工作区审计前非干净：`M web/content.js`（另一 agent 今早 08:59 重建，比 HEAD 多约 8.8KB）+ 未跟踪 `.zcode/plans/plan-sess_*.md`（6034B）+ `old_content.js.tmp`（2.35MB）。外来产物**未触碰**；content.js 备份至临时目录后按 V3.0 计划恢复 HEAD。
- stash@{0}：README/archive/README/学习路径指南 3 处用户改动，**未 pop/drop**（B12 待裁决）。
- 四道门禁：build **70 docs/18 sections**（含 .zcode 污染）/ validate **11 checks 0 FAIL 0 WARN** / arc **5/5 OK** / review_gate **31 claims（16 verified/7 conditional/8 open）误标 0**。
- **content.js drift 根因**：build_site.py:440-445 未排除 `.zcode/`，未跟踪工具计划文件被当第 70 篇文档；干净基线 **69 docs/17 sections/497 cards/2291 KB**（HEAD bundle）。validate §7 仅查前缀不比对篇数，恢复 HEAD 仍 0 FAIL。登记 Category A（A3）。

### 偏差登记（声称 vs 实测）
- ① L01 行数：CHANGELOG/G2材料"约300行" → 实测 **239 行**。
- ② claim/source：PROJECT_CURRENT_STATE "29/15" → 实测 **31/16**（P6 新增 V13/V14+SRC-RN-AV-BASE）。
- ③ build 篇数演进 48→62→63→69；当前干净基线 69（PROJECT_CURRENT_STATE §3 仍停 63 基线快照）。
- ④ V3.0 根目录 quizzes/ 实际在 courses/video-rendering-journey/quizzes/。
- ⑤ stash 未决（B12）。⑥ 程序化模块以 07 文档落地（非"08 章节"），course.json L00–L18/8 单元；无 08-* 目录。

### 程序化模块闭环核查
- 文档（07/程序化几何与旋转曲面.md 170行 ✅/⚠️）+ L17/L18 元数据 + procedural-lathe/pbr-lighting 实验 + glossary procedural-graphics 组 + graph.json 节点 + 双线规划§7"任务二阶段1成课"——**闭环成立**。
- 唯一导航缺口：学习路径指南.md 未收录 U7/L17/L18（F-2，Category A4）；UV 无独立术语条目（F-3，C7）。

### 审核材料（reviews/ 新增 7 文件）
- CURRENT_AUDIT.md：git/门禁/偏差/程序化闭环/真值快照。
- G1-evidence-review.md：31 claim 全量（双向索引完整、23 概念 source_claim 全解析）；V13/V14 升级评估（引源文档✅段，不自动升级）；Pass 口径冲突（跨平台:205 ">3" vs 验真队列:47/概念引入:145 "≥3"）；SurfaceTexture API（解码链路:124 glGetTransformMatrix 不准确，3D变换:225 正确）；L13 断言缺口（4 候选）；K-STRIDE 弱挂 V02。
- G2-curriculum-review.md：G2-01…06 重核（修正旧结论：seek 目标有 glossary:641 种子但与§8.2 机制语境矛盾）；G2-02 确定性复跑确认主线矛盾，**单指针修复方案 L12.next→L13**；G2-04 重读 L01 239 行十维度达标。
- G3-release-readiness.md：**G3 仍未通过**；结构层就绪/语义层未就绪；人工评分表留空。
- REVIEW_STATUS.md：A/B/C 分类（A1–A6 / B1–B14 / C1–C7）。
- DECISION_REQUIRED.md：统一裁决表 B1–B15，空白裁决栏，未回复不视为同意。
- EXECUTION_PLAN_V3.md：Loop 2（裁决→Category A→P7 blocker L02→L06→L13→L11→P7.2）/ Loop 3（P8→P9→P10 独立验收）。

### 边界确认
- 仅新建 reviews/ 7 文件 + 更新 WORKFLOW_STATE.md/CHANGELOG.md（本文件）；**未改任何既有内容文件**（含 build_site.py/concepts.json/主文档/README）。
- 未升级任何 claim；未填任何人工结论/评分；未 pop/drop stash；未触碰外来产物；未 commit/push。
- content.js 恢复 HEAD（生成物可再生，计划授权）；未动 archive/memory/vendor/index.html/两份方案。
- 记忆修正：程序化模块已并入 07（非 08）；当前续跑点=等待 DECISION_REQUIRED 裁决。

## 2026-11-18 · P6 教材质量升级（Master Prompt V2.0）

### 第一步审计（实测）
- 远程 master HEAD = 本地 HEAD = `5359259`（ls-remote 实测），工作区审计开始时干净。
- 门禁基线：build 63 docs / validate 11 checks 0 FAIL / arc 5/5 OK / review_gate 29 claims（16 verified / 7 conditional / 6 open）。
- 产出：`PROJECT_CURRENT_STATE.md`、`CURRENT_GAPS.md`、`NEXT_PHASE_PLAN.md`（根目录）。
- 记录性偏差：CHANGELOG P5 数字（62/452/2107KB）与最终源树（63/461/2136KB）漂移，已提交 content.js 与重建产物文档集合一致（仅时间戳类差异）；README 数字过时但按 D10.5 不动，列决策提案。本机 `python` 解析到 cygwin stub，门禁改用 `py -3`（D11.10）。

### P6.1 深度诊断
- 新增 `courses/video-rendering-journey/教材质量诊断.md`：十维度逐章判定 + 源文档行号核对 + 跨层数据交叉核对。
- 关键发现：L02"drift 强纠偏区/分级处置"源文档不存在（blocker，夸大引用）；L02 目标"seek 后禁止立刻丢帧"无出处（blocker）；L13 核心知识无断言支撑、quiz 弱挂/空挂（blocker）；L06 目标漂移+§7.3 错位；L11 乱码四处+RenderPass 过度简化；L01 数字口径/推导缺失。
- 诊断明确为 AI 线索，非人工评分；G1/G2/G3 状态未变。

### P6.2 覆盖矩阵
- 新增 `courses/video-rendering-journey/课程覆盖矩阵.md`：19 课 × 元数据/正文/Quiz/Claim/Lab；元数据 19/19、正文 5/19、Quiz 5/19、Lab 7/19、断言挂载 13/19。
- 核对结论：pilot 5 课为有意分阶段（非遗漏）；pilot next 指针与路线矛盾（已修）；主课程 L12.next=L15 与 L15 先修矛盾（留 G2 拍板）；L02/L06/L11 两层目标漂移（留 P7）。
- **第 3 项确定性验证**（一次性审计脚本，不入仓库）：先修存在性 19/19 + DFS 无循环；主课程 next 链行走实测 L15/L17/L18 先修未满足（G-D2 精确量化到 L17/L18）；pilot 路线 next 指针 + §10 正文桥 + lessonFile + quiz + lab 双向**全部一致 0 问题**；labs.json 7 实验 lesson 反向均有效。桥接检测限定 §10 段落，排除 §11 延伸链接误报。结论已写入覆盖矩阵 §2.1，G-D2 范围同步扩展至 L17/L18。

### P6.3 Gold Standard L01 + 数据修复
- 重写 `lessons/L01-为什么视频不是-RGB.md`（88→239 行，实测）：精确数字开篇（22.4GB vs 112.5MB 两刀分解）、生理依据（V13）、4:2:0 记号与采样对照表、NV12 布局图、stride 公式+1080@128 算例+逐行错位推导+绿屏成因计算（V14）、glPixelStorei 代码、排查案例、实验四任务+full-range 边界、因果链回忆。checkpoint 两题原文保留。
- `evidence/claim-ledger.json`：新增 V13/V14（open/low，待 G1 升级，note 说明提取来源）；V06 used_by 补 L13、E03 补 L11。
- `evidence/source-registry.json`：新增 SRC-RN-AV-BASE（repo_doc），双向索引完整。
- `quizzes/L01.json`：Q2 改挂 V14，答案补绿线/累积偏差依据。
- 两层 course.json：L01 乱码目标修复；pilot next 对齐 L01→L02→L06→L11→L13→null（D11.2）。
- 未动其余四篇样章内容（修复留 P7，D11.7）。

### P6.4 质量规范提案 + G2 材料
- 新增 `.workbuddy-ai/skills/research-to-learning/references/lesson-quality-standard.md`（十维度/六问/类比边界/数学三件套/引用与断言纪律/知识类型结构/诊断程序）；SKILL.md 登记阅读指引、Phase 5 审核动作、Helpers。**提案状态，待 G2 人工确认，AI 未宣布通过。**
- 新增 `courses/video-rendering-journey/G2-审核材料-P6.md`：变更清单 + 6 个待拍板问题（行为语言）+ 语义审核 8 项清单 + 空白评分表。

### 门禁（P6 结束实测）
- `py -3 tools/build_site.py`：69 documents / 17 sections / 124 terms / 8 units / 19 lessons / 7 labs / 497 term cards / 2291 KB（新增 6 篇审计/诊断/矩阵/G2 文档计入）。
- `py -3 tools/validate_site.py`：**11 checks passed, 0 warnings, 0 failures**，exit 0。
- arc：5/5 OK（含重写后的 L01）。
- review_gate：只读复跑正常，G1/G2/G3 仍待人工，未写任何分数。

### 边界确认
- 未 push / 远程发布（D09 远程需另行授权）；未动 archive / memory / vendor / index.html / 两份旧方案 / README。
- 治理文档同步：DECISIONS.md 新增 D11；WORKFLOW_STATE.md 更新续跑点为 G2；IMPLEMENTATION_PLAN.md 新增 P6 勾选与 P7–P10 待办。
- 已知风险：V13/V14 为 open 断言，G1 升级前教材以主文档锚点为权威；L02 blocker 内容在 P7 修复前仍在线（诊断与 G2 材料已显著标记）。

### git 提交（2026-11-18 用户授权"先提交代码，保存修改"）
- P6 全部产物本地 commit **`3ce7b2f`**（19 文件，+978 / −44）：审计三件套 + 诊断 + 覆盖矩阵 + Gold Standard L01 + V13/V14/SRC-RN-AV-BASE + quiz/next/乱码/used_by 修复 + 质量规范提案 + G2 材料 + 治理文档 + content.js。
- **仅本地 commit，未 push**（D09/D11.9：远程需另行授权）。提交后工作区干净；本笔记录哈希的文档更新随后单独提交。
- **push（2026-11-18 用户授权"push吧"）**：`git push origin master` 成功，`5359259..0b2c0a1`；`ls-remote` 实测远端 HEAD=`0b2c0a16f9de2735a722abdc8d57bc0d94620953`，本地与 origin/master 同步。**仅 push 源码，未做在线发布**（GitHub Pages 等 D02 仍未授权）。

## 2026-11-18 · P5 收尾验收

### 三重确定性门禁（实测）
- `python tools/build_site.py`：写出 `web/content.js`；`62 documents / 17 sections / 11 glossary groups / 124 terms / 8 units / 19 lessons / 7 interactive labs / 452 term cards / 2107 KB`。
  - 说明：文档数/节数高于 P0 基线（48/11），因 P1–P4 新增 `courses/`、`evidence/`、`knowledge-model/` 三个顶层树；`site-vitepress/` 生成树已被正确排除（`build_site.py` 过滤 `site-vitepress`）。
- `python tools/validate_site.py`：`validate_site: 5 checks passed, 0 warnings, 0 failures`，末行 `OK`，exit 0。
- `python .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py courses/video-rendering-journey/lessons/*.md`：5 篇样章（L01 / L02 / L06 / L11 / L13）全 `OK`，exit 0。
- JSON 结构兜底：`tools/*.json` + `evidence/*.json` + `knowledge-model/*.json` + `courses/.../*.json` 共 14 个文件全部可解析。

### 浏览器 QA（离线主站，零构建）
- 两路验证：`file://` 双击 `web/index.html`、`http://localhost:8765`（`python -m http.server 8765`）。
- 五视图（`#/`、`#/course`、`#/lab`、`#/graph`、`#/tech`、`#/glossary`）均渲染出内容；侧栏 62 链接。
- 7 个实验逐个打开均有 canvas + 3 项自检：`transform-mvp`、`procedural-lathe`、`pbr-lighting`、`yuv-to-rgb`、`pts-dts-timeline`、`frame-pipeline`、`rendergraph-dag`。
- 教材路由 `#/doc/courses/video-rendering-journey/lessons/L01-...md`：frontmatter 已剥离；教材模式 `#/course/L01` 可达。
- `Ctrl+K` 搜索框、明暗主题、390×844 移动视口、hash 刷新保持均正常；控制台/页面错误 0。
- 已知良性提示：agent-browser 报告 Chrome 版本落后（与本仓库无关）。

### review-report.md 收口
- 仅把"自动检查（已执行）"三行结果改为实测值，并新增一段"执行记录（自动检查结果，非评分）"。
- **未填任何分数**：评分表"自评"仍为 `待人工`、"人工评分"仍为 `—`；G1/G2/G3 仍为未勾选；结论仍为 `待人工评分后填写。生成 Agent 不在此处填写"通过"。`

### 已知限制（D10.6，如实记录）
- P4 VitePress `npm run docs:build` 未完成：vitepress 需清理自身 `.vitepress/.temp/` 构建中间产物，触发删除权限请求被用户拒绝；用户已选"跳过构建，如实记录"。
- 本计划**未重试**该命令；源码树（`package.json` / `README.md` / `.vitepress/config.mjs`）与生成的 46 篇策展文档保留，`npm install` 成功（vitepress 1.6.4）。不伪造构建成功。

### 边界确认
- 未 commit / 未 push / 未远程发布（D09）。
- 未改动：`README.md`、两份 GPT 方案文档、`archive/**`、`web/index.html`、`web/vendor/**`、`.workbuddy-ai/memory/**`。
- 人工审核关卡 G1/G2/G3 仍待人工，AI 未自评通过。

## 2026-11-18 · Part B 文档缺口增量补齐

批准计划：`C:\Users\Giant\.workbuddy-ai\plans\radiant-cascade-newton-e440_pIP.md`。用户确认"两者都要" + B5 连前端 UI 一起做（对 D04 的明确授权偏离，仅限 `web/assets/app.js`、`styles.css`，无远程）。

### B1+B2 · validate_site.py 第 11 节（coverage）
- 仅**新增**第 11 节，前 10 节零改动（符合 D07）：
  - 11a 每条 claim 必须有 evidence（孤立断言 FAIL）；`verified` 但未挂任何课时 WARN；`open/conditional` 未挂载属预期（P03），不误报。
  - 11b 每个 checkpoint 必须被 quiz prompt 覆盖；quiz `claim_ids[]` 必须 ⊆ 课时声明的 `claims[]`；覆盖以归一化文本双向包含判定（实测 5/5 课全覆盖）。
  - 11c `tools/feedback.json` 可选校验：`type` 枚举、lesson/quiz/claim ID 可解析（quiz 未找到记 WARN）。
- 负向自检：临时清空 V01 的 evidence → `[coverage] V01: no evidence item` FAIL、exit 1；恢复后 0 FAIL。
- 门禁：validate 由 5 checks → **11 checks passed, 0 warnings, 0 failures**。

### B3 · Skill 角色契约补齐（不建顶层 skills/）
- `SKILL.md`：frontmatter description 补两角色；角色表新增 4b Practice Designer、5b Knowledge Publisher / Feedback Analyst 两行（含 gate）；阅读指引与 Helpers 登记 `practice-and-review.md`。
- `references/workflow-details.md`：在 mapped roles 段后补两角色完整契约（input/actions/output/gate/boundary/reference）。
- 新建 `references/practice-and-review.md`：两角色契约 + G1/G2/G3 人工关卡清单 + 本地反馈循环说明。
- 验证：validate 0 FAIL；`skills/`、`scripts/` 顶层目录未创建。

### B4 · tools/review_gate.py（只读前置清单）
- 新建 stdlib 工具：打印 G1（claim 状态分布、conditional/contested 误标 verified 检查）、G2（curriculum 七段存在性 + 每课时前置/目标/checkpoint 概况）、G3（确定性门禁命令 + review-report 仍待人工状态）的自动前置条件。
- 实测：29 claims（verified 16 / conditional 7 / open 6），误标 0；curriculum 7/7 段齐全；G1/G2/G3 未勾选 3 个。
- **不写分数、不勾关卡、不运行门禁**；review-report.md 字节未因本工具改变。

### B5 · 学习反馈闭环（数据 + 只读聚合 + 离线前端 UI）
- 数据层：新建 `tools/feedback.json`（version + entries[]，空；字段 lesson/quiz/claim_ids/type/note/ts，无个人信息、无远程）。
- 聚合层：新建 `tools/report_feedback.py`（只读，按 type/lesson/claim 汇总 + 从 claim-ledger 取回断言文本输出 needs-review 线索；不改任何状态）。
- 前端 UI（`web/assets/app.js`、`styles.css`，用户授权偏离 D04）：
  - 复用既有 `rn-course-progress` 阅读进度机制，未重复造轮子；
  - 新增 `rn-feedback-queue` localStorage 队列；教材页 L## 与配套文档自动预填课时/quiz；反馈表单（type/lesson/quiz/claim_ids/note）；"加入队列 / 导出 JSON / 清空"三按钮；`Blob` + `URL.createObjectURL` 纯浏览器导出（无第三方库、无网络请求）。
  - `styles.css` 追加反馈面板样式（明暗主题 + ≤640px 移动端 + print 隐藏）。
  - **未改** `web/index.html`（UI 动态注入到 `#content`）。
- 端到端验证（浏览器实测）：填写→提交→localStorage 落库（含 lesson=L01、quiz=L01、claim_ids=[V02,V12]、ts）→刷新后保留、徽标计数同步；导出 payload 结构 = `{version:1, entries:[...]}`；将同结构样本放入 `tools/feedback.json` 后 `report_feedback.py` 正确输出 V02/V12 的复核线索；样本已移除、`feedback.json` 恢复空、门禁绿。
- 回归：五视图 + 7 实验 + 教材路由 + 搜索/主题/移动端全部正常，反馈面板仅出现在课时页，控制台 0 error。

### Part B 边界与收口
- DEFER（逐项理由）：10-Skill 树 / 多 Agent runtime / MCP / 向量 DB / 远程发布 / 修 docs:build / Shader Playground（违反 D04/D09/D10.3/D10.6 或体量过大）；机器可读知识缺口检测（与 `知识缺口登记表.md` 单一来源冲突，待定权威）。
- D04 偏离仅此一处（B5 前端），已按用户授权执行；未新建顶层 skills/ 或 scripts/。
- Part B 执行期间未 commit / push / 发布；未碰两份方案文档、archive、web/index.html、web/vendor、.workbuddy-ai/memory。（git 提交见文末，README.md 的纳入为用户新授权。）

## 2026-11-18 · git 提交（用户新授权）

- 用户在 P5 + Part B 完成后明确要求"提交 git 更新"，并确认 **commit + push 到 origin/master**、**README.md 的 3 行 chat 链接改动一并纳入**（见 `DECISIONS.md` D09 更新）。此为一次性授权，不改变其余"绝对不动"项。
- 提交内容：
  - 引擎层：`tools/validate_site.py`（第 11 节 coverage）、`tools/review_gate.py`、`tools/report_feedback.py`、`tools/feedback.json`、`tools/build_site.py`、`tools/labs.json`、`tools/graph.json`、`tools/course.json` 等既有改动。
  - 前端：`web/assets/app.js`（反馈 UI + 既有实验渲染）、`web/assets/styles.css`、`web/content.js`（生成物）。
  - 课程/证据/知识模型：`courses/`、`evidence/`、`knowledge-model/` 全部产物。
  - Skill：`.workbuddy-ai/skills/research-to-learning/`（角色契约 + practice-and-review.md + 既有脚本改动）。
  - 在线站源码：`site-vitepress/`（源码三件套；生成物由 .gitignore 排除）与 `.gitignore`。
  - 文档/状态：`DECISIONS.md`、`IMPLEMENTATION_PLAN.md`、`WORKFLOW_STATE.md`、`CHANGELOG.md`（本文件）、两份 GPT 方案文档（新增跟踪）。
  - README.md：用户此前的 3 行 chat 链接改动（按本次授权纳入）。
- 未纳入/未执行：在线发布（GitHub Pages 等，D02 未授权）；VitePress `docs:build`（D10.6 已知限制，未重试、未伪造）；`.workbuddy-ai/memory/**`（绝对不动）。
- 提交哈希与远端同步状态：见 `git log -1` 与 `git status`（push 后本地与 origin/master HEAD 一致）。

## 2026-11-19 · CHG-0001 四项目并进拓展（用户授权，本地执行）

用户裁决：四项目同时启动；只建本地、不碰 GitHub（不建仓/不 push/不部署）；P1 做完全部剩余 P7；Render_Notes 现有 25 项未提交变更保持原样、增量修改。变更包 `.agent/changes/CHG-0001-four-project-expansion/`（proposal + tasks）。

**P1 · Render_Notes P7 未闭合 gap 修复**（基线门禁 11 checks 0 FAIL/0 WARN、arc 5/5）：
- L13（G-T3/T9/B10）：新登记 4 条 open 断言 V17（坐标空间链）/V18（MVP 列序）/V19（透视除法与插值）/V20（NDC 跨 API 差异），配套 `SRC-RN-3D-TRANSFORM` 来源；frontmatter claims 从误挂 V06 改为 V17–V20；正文 §4.2/§4.3/§5/§6 修正 Y-flip 含糊表述与透视插值推导；quiz Q1/Q2/Q3 重新挂接（消除空 claim_ids）。断言默认 open，不升级 verified。
- L06（G-T5/T6/D5）：两层 course.json objectives 对齐源文档真实内容（updateTexImage/变换矩阵、第一道转换 Shader、PC vs 移动通路）；正文 §4.1/4.2 补 updateTexImage 与 FBO→2D 转换机制，纠正 §7.3 错位引用，色彩出处改 `03-图形与GPU工程/色彩管理与采样滤波.md`，补 P02 声明；source anchor slug 修正（validator 实测通过）。
- L11（G-T7/D4）：§4.1 修正"FBO=VkRenderPass 换名字"过度简化（区分 RenderPass API 声明 vs RenderGraph 工程抽象、Vulkan 附件预声明）；乱码"barrier 是由谁 inserted？"四处同步改为"barrier 由谁插入？"（两层 course.json checkpoint + 正文 §9 + quiz Q2）。
- L02：核对已闭合（V15/V16 + 正文改写已在 Loop 2 落地），本轮不改。

**P2 · learning-experience-design Skill**（Engine 内部，不独立仓库）：
- 新建 `.agent/skills/learning-experience-design/`：SKILL.md + 8 references（design-system/editorial-layout/learning-page-archetypes/educational-visualization/interaction-patterns/accessibility/responsive-design/visual-quality-gates）+ 3 assets + `scripts/check_visual_floor.py` + 试点规格 `preview/PILOT-L13-plan.md`。
- 上游核对：Impeccable（Apache-2.0）、Hallmark（MIT）——只吸收方法，不复制代码/素材。试点选 L13 教材页 + transform-mvp 实验页，**待用户确认设计方向**，不改线上站点。
- 三个 build 脚本已整体排除 `.agent`（D14），新 Skill 自动不进知识 bundle；registry 重生成（119 docs）。

**P3 · agent-workspace-governance（新本地目录 `C:/Users/Giant/Desktop/GITCODE/agent-workspace-governance`）**：
- Portable Agent Project Governance Kit：README/AGENTS/宪法四件套 + 5 JSON Schema + 6 模板 + 5 端 adapters + CLI 9 命令（init/inventory/validate/status/map/handoff/adr/archive-check/audit）+ tests（11 passing）+ 两个迁移样例（Render_Notes / 普通项目）+ docs 三篇。明确三概念边界、不重造 Skills、不做 Orchestrator。

**P4 · github-project-radar（新本地目录 `C:/Users/Giant/Desktop/GITCODE/github-project-radar`）**：
- 开源情报系统本地实现：SQLite 快照模型 + 注入式离线采集（fixtures，**不调用 GitHub API**）+ 24h/7d/30d 增长（历史不足标注、不伪造）+ 可配置评分 + 周报七板块 + 深度研究模板 + 人工审核状态机 + Engine 研究任务导出接口 + CLI + tests（17 passing）+ docs 三篇。

**门禁与边界**：build/validate(0/0)/arc(5/5)/review_gate 全绿；两新项目 unittest 11+17 全绿；未 commit/push、未建远程仓库、未联网采集、未碰受保护目录与用户未提交变更。G1/G2/G3 仍待人工，未自批。

## 2026-11-19 · 融合基线增量补齐（新架构文档 = 缺陷清单 + 规格增量）

用户裁决：保留上一会话全部已建成果（融合基准，不重做）；reviews/ 泄露为第一优先、archive 不动；只备人工裁决材料不代批；两新项目保留目录名；Skill 补 5 篇保留旧 8 篇；仅本地零 git 操作。计划见 `~/.workbuddy-ai/plans/stellar-thunder-lovelace-4LLY_xlW.md`。

**P1 · 发布边界泄露修复（第一优先）**：新增 `tools/publish_boundary.py`（集中式排除 + 咨询性 allowlist）+ `tools/publish-allowlist.json` + `tools/test_publish_boundary.py`（11 测试）；`build_site.py` / `build_vitepress_content.py` / `validate_site.py` 三处增加 `reviews/` 排除；重生成 `web/content.js`（知识文档 85→77，恰好移除 8 篇审核材料）与 VitePress 树。`archive/` 发布行为不变（D10.4）；注册表仍故意索引 reviews。strict allowlist 强制切换列为人工裁决。

**P2 · 状态文档漂移**：`WORKFLOW_STATE.md` / `reviews/DECISION_REQUIRED.md` / `reviews/REVIEW_STATUS.md` 早期表的过期"B10–B15 未答复"改为指针行（B13/B14 已裁决归档见 D11/D12）；`PROJECT_CURRENT_STATE.md` 头部加"增量校正（2026-11-19）"块（HEAD `474c667`、5/19 正文仍成立），保留原快照。

**P3 · 人工裁决材料包**：新增 `reviews/decision-kit/`（README + B4/V13/V14/B10/B11/B12/B15 七份），9 段模板 + 空白裁决栏；B12 仅 `git stash show -p stash@{0}` 只读摘录（链接路径修正），未 pop/drop/apply。7 项 + G1/G2/G3 全部 OPEN，无一项代批。

**P4 · Skill 规范增量**：`.agent/skills/learning-experience-design/references/` 新增 5 篇（learning-ux-principles / learning-interaction-patterns / visual-system-and-layout / accessibility-and-responsive / ux-review-checklist），旧 8 篇全保留，SKILL.md 改双索引表；`status: draft` 不动。参考文档 8→13 篇。

**P5 · Governance 增量**（`agent-workspace-governance`）：13 类文档类型枚举（ADR/Spec/Plan/Task/Runbook/Glossary/Architecture/Skill/Workflow/Script/Handoff/Audit/Session Note）、Task Claim / Single Writer per Path / dependency frontier 协议与纯函数、CLI 新增 `doctor` + `index`（`inventory` 保留），tests 11→25 全绿。目录名不变、名称映射写入 README。

**P6 · Radar 增量**（`github-project-radar`）：三维独立评分（Discovery Signal / Engineering Quality / Relevance to My Learning Ecosystem，缺失标 unknown）、canonical 生命周期 + 旧状态别名、`human_selected_for_research` flag、溯源字段、`YYYY-WW.md`+JSON 报告、`radar/sources/` 接口 stub（零网络）、research 默认 `research/owner__repo.md`，tests 17→38 全绿。目录名不变。

**P7 · P8/P9 只读基础**：新增只读 `tools/kcr_impact.py`（Source→Claim→Concept→Lesson→Quiz→Course→Website 影响链，实测 SRC-RN-AV-BASE 得 3 claims/2 lessons/2 quizzes）+ `reviews/kcr/KCR-IMPACT-TOOL.md` + `reviews/P9-orchestrator-design.md`（状态机 + run-state schema 内联，均 draft）。不写源 JSON、不升级 claim、不建运行态文件、不批量生成课文。

**门禁/边界**：validate 11/0/0、arc 5/5、boundary 11 tests、review_gate 只读（G1/G2/G3 未通过）、governance 25 + radar 38 tests 全绿；registry 重生成 143 docs；HEAD 仍 `474c667`、stash@{0} 仍在、零 commit/push/建仓/联网。
## 2026-11-21 · 记录更正（用户核实三处）
① arc 真值=19 篇 0 FAIL（全量更正，此前 11 篇为传入子集口径）；② L02 遗留 major「DTS ≤ PTS 恒成立」确认 2026-11-20 已修复、app.js/labs.json 0 残留，遗留清单划除；③ U4/U5 已随 D20 闭合，遗留改 U1–U3。KCR substate 补 APPLIED→VERIFIED（19 项已应用并核验）。push 授权 6 笔（Engine 5+Skills 1）。

## 2026-11-21 · P10 done——Engine 主目标达成（RUN-2026-11-20-p10-hdr 全闭环）

- **四件人工门全过**：G1 六项升级 verified（采纳 AI 推荐授权）+ V23 I19=A 先补边界再升；KCR-2026-11-001 APPROVED；G2 L19=91/100 通过（用户本人填分确认）；G3 gate --pass（approver: user，22:22:05）。
- **收尾序列**：resume → PUBLISH（发布记录 reviews/p10/publish-record-hdr.md：本地 bundle 口径，在线发布 D02 未授权）→ FEEDBACK（reviews/p10/feedback-record-hdr.md）→ **done**（write_paths 释放，artifacts 18）。
- **留痕**：DECISIONS D20；G1 裁决栏回填；glossary HLG 边界联动（U4）；U5 惯例裁决（前课指针口径）；WORKFLOW_STATE/NOW/Program final-acceptance-2026-11-21.md 同步。
- **门禁终态**：build 75 docs/553 cards · validate 12/0/0 · arc 11 篇 · publish 11/11 · review_gate 84→84（24v）误标 0 · kcr 16/16 · runstate 25/25。
- **push 暂缓**（用户：等我通知）；阶段 2 LXD 试点 A 待执行（下一窗口）。

## 2026-11-21 · P7.2 第十篇：L09《移动端瓶颈与 TBDR》新写教材（审读 blocker 修复后通过——「其余篇目」第六篇）

