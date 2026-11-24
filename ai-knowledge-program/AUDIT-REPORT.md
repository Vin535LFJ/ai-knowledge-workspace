---
doc_id: PROG-AUDIT-2026-11-23
type: audit-report
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
---

# 六阶段实施后独立审计报告

> 审计基线：2026-11-23 20:13 (+08:00)
> 审计对象：AI Knowledge Program 六阶段（Program / Engine / LXD / Governance / Radar / 集成）
> 审计方式：只读实测（git、文件、测试、SQLite 只读查询、本地 HTTP + 无头浏览器渲染），不依赖此前完成报告的自述
> 审计人：QwenWork（曾参与实施，本次按独立审计纪律重新核对）

---

## 0. 审计方法与证据边界

**先声明三个边界，避免把结论读得过宽：**

1. **审计同时使用了「我本人实测」和「三个只读子审计」**。Governance、Radar、Skills 的细项由独立子代理在只读约束下核对（禁止 commit/push/reset/clean，测试只写临时目录），我复核了其中的关键数字（121/200 快照、28/38 测试、9/9 的 doctor 失败、Skills 37 技能）。凡我未亲自复跑的项目，在文中标注「子审计实测」。
2. **只读优先**。除 `build_site.py`（文档化构建命令，产出 `web/content.js`，实测仅 1 行时间戳差异）外，未修改任何源码、数据、运行态或历史交付物；未提交、未 push、未删除。
3. **测试通过 ≠ 目标达成**。本报告把「提交存在」「工作树干净」「测试绿」「Skill active」分别与「功能完成」「产品验收」「目标达成」分开判断。

**五个仓库基线**

| 仓库 | HEAD | 工作树 | 远端 |
|---|---|---|---|
| ai-knowledge-program | `cc098df` | 1 个未提交（NOW.md） | 本地 git，无 remote |
| ai-knowledge-to-learning-engine | `79c3fe8` | 10 个未提交（D21 笔误修正 + embodied INTAKE） | `Vin535LFJ/ai-knowledge-to-learning-engine` |
| matt-pocock-skills-zh-cn | `7326522` | 干净 | `Vin535LFJ/matt-pocock-skills-zh-cn` |
| agent-workspace-governance | `1b4a880` | 干净 | 无 remote |
| github-project-radar | `b7442da` | 干净 | 无 remote |

**关于「六阶段状态」的总判断先说结论：** 六阶段都有真实交付物，但 **只有 3 个阶段可以判「符合要求但有已知限制」，另外 3 个只能判「部分完成」**。不建议按「全部 PASS」宣布 Program 闭环。

---

## A. Executive Summary

### A.1 六阶段总体状态

| 阶段 | 报告自述 | 本次审计结论 | 一句话依据 |
|---|---|---|---|
| PHASE 0 · Program | 完成 | **PASS WITH LIMITATIONS** | 四文件 + PM 规则真实存在且能承载恢复；但 PROGRAM.md/NOW/PENDING 存在过期与自相矛盾 |
| PHASE 1 · Engine | 完成 | **PASS WITH LIMITATIONS** | P10 真实 run 走通 INTAKE→FEEDBACK、18 artifacts、四门记录齐；但门证据不可独立验证、7/18 artifact hash 已失效、站点未在线发布 |
| PHASE 2 · LXD | 完成 | **PASS WITH LIMITATIONS** | Skill active + 1 个真实试点（L13）+ Floor 双 PASS；仅 1 个案例、13 份参考文档重叠 |
| PHASE 3 · Governance | 9/9 完成 | **PARTIAL** | CLI 可运行、28 测试绿；但「9/9」是文档自证，独立示例项目过不了自身 doctor，真实注册 0 task/0 agent/0 ADR，Engine 无治理入口 |
| PHASE 4 · Radar | 完成 | **PARTIAL** | 八功能代码在、38 测试绿、121 仓数据真实；但「200 快照」是 20 秒 4 次搜索、增长全空、analyze 会覆盖人工状态、导出违反自身人工门 |
| PHASE 5 · 集成 | 完成 | **PARTIAL** | 八项核对表存在，但第 4 项（Radar→Engine Intake 门控）为误判，第 1 项指针已失效，第 2 项无文件级链接 |

### A.2 当前总体成熟度

- **Engine**：**单批可复现的端到端生产链已验证**（这是六阶段里最有价值、最硬的成果），但仍是「人工驱动的单批流水线」，不是「常态化生产线」。
- **LXD**：**方法已建立、单案例已跑通**，未达到「多案例稳定复用」。
- **Governance**：**可运行的文档扫描/诊断工具**，不是「可移植治理平台」；真实使用只完成「注册表落地」一层。
- **Radar**：**八功能 MVP + 一次性真实抓取**，不是「可持续情报系统」。
- **Program**：**能用的轻量统筹层**，但状态维护纪律已出现漂移。

### A.3 最重要的五项发现

1. **Engine 的端到端链路是真实的，但「done」的边界被报告扩大了。**
   证据：`RUN-2026-11-20-p10-hdr` = FEEDBACK/done、G3 passed、18 条 artifact、`write_paths=[]`；`validate 12/0/0`、`arc 19/19`、`84 claims（24 verified/53 open/7 conditional）误标 0`、`build 83 docs/20 lessons/624 cards/3149 KB`；本地站点 HTTP 200 且无头渲染出课程与术语。
   但：在线发布受 D02 未授权，站点只是本地静态站；19 份课时教材中只有 5 份有 quiz（L00 为地图课不计）；新增独立课程受 validate §10 硬约束，多课程尚未打通。

2. **人工门（G1/G2/G3）在流程上被强制，在证据上不可独立验证。**
   证据：`human_gate.approver = "user(2026-11-21 G2=91 通过)"` 是 AI 写入的字符串，无独立审批文件、无姓名/身份、无签名；schema 只要求 approver 非空。G2 §5 的「裁决人：用户本人」同样不是可核验身份。
   另外 18 条 artifact 中 **7 条 sha256 与当前文件不一致**（审读修复、G1 裁决、G2 回填后未重登记），说明 hash 是「登记时快照」，不是「最终交付校验值」。

3. **Governance 的「9/9」名不副实，属于文档自证。**
   证据：`1b4a880` 只改 1 个文档（+17 行）不含代码/测试；第 8 项「独立示例项目」实测 `doctor --project examples/basic-project` **exit 1**（2 个 type 不在 13 类枚举）；ENGINE 侧 `task=0 / agent=0 / adr=0`；Engine `AGENTS.md` 无任何治理入口指针；人工审批「要求写入 .governance」但**无对应 schema/文件**。
   它真实可用的是：`init/inventory/validate/doctor/audit/adr/handoff` 等 CLI + 28 个测试 + 183 篇文档登记，可作「扫描与诊断工具」。

4. **Radar 的「真实数据」成立，「能力语义」被高估。**
   证据（SQLite 只读）：repositories **121**、snapshots **200**、candidates 121（Discovered 120 / Research 1）、collection_runs **1**；快照时间跨度 `11:46:46–11:47:06`，**仅 4 个时间点/20 秒**；`source_url` 200/200 为 NULL。因此 24h/7d/30d 增长 **121/121 `insufficient_history`**，周报「每周崛起项目」按全 0 的增长分排序。
   另有三个必须修的行为缺陷：`analyze` 会把人工 `Research` 状态重置为 `Discovered`；`--approved` 只改状态字符串、不置 `human_selected_for_research`（导出样本该字段为 **false**）；搜索路径丢弃 rate-limit 剩余量。

5. **Program 作为「唯一入口」已出现状态漂移，并导致一处跨项目误判。**
   证据：`PROGRAM.md` 仍写 `Render_Notes/`（目录已改名）、仍称 Governance/Radar「冻结、无远程、不新增投入」（实际已解冻交付）；`NOW.md` 同一文件内既写「用户批准 kickoff」又写「kickoff 待批准」；`PENDING_DECISIONS.md` 的 PD-Q5 仍空白（实际 D17–D19 已闭合）；`final-acceptance` 第 4 项判「human_selected 门控 ✅」，而导出物该字段为 false。

### A.4 是否建议宣布 Program 阶段闭环

**不建议现在宣布「六阶段全部闭环」。** 建议的表述是：

> **「六阶段交付完成；Engine 主目标经独立复核成立；Governance/Radar 为 PARTIAL，需按 P0/P1 最小修复后才能称为可用；Program 需先修正状态漂移。」**

完成 A.3 中第 2、3、4、5 条对应的最小修复（见 §E 的 P0/P1）后，可以宣布「有条件闭环」，而不是「全部 PASS」。

---

## B. 六阶段逐项审计

### B.1 PHASE 0 · AI Knowledge Program

**原始目标**：轻量统筹层；管目标/进度/优先级/范围；不复制子项目技术文档；有 PROGRAM/NOW/ROADMAP/PARKING-LOT；PM 可恢复任务；不演化为复杂平台。

**实际交付**
- 五份文件真实存在：`PROGRAM.md`（140 行）、`NOW.md`（96 行）、`ROADMAP.md`（54 行）、`PARKING-LOT.md`（101 行）、`PROGRAM-MANAGER.md`（97 行）。
- 辅助体系：`decisions/`（PD-001~003 + PENDING）、`plans/`（3 份，含 embodied kickoff）、`handoffs/`（2 份自包含交接 + 索引）、`references/`、`archive/`、`final-acceptance-2026-11-21.md`。
- PM 规则包含：五项职责、范围控制硬规则、十二步启动流程、写入边界、AI 权限限制、防膨胀六问、交接要求、审计节奏、禁区。

**实证材料**
- `PROGRAM.md:21,28,31,50-51,65-66`：仍写 `Render_Notes`、`mattpocock-skills-zh-CN-custom`、Governance/Radar「冻结 MVP」。
- `NOW.md:12` 写「用户批准课程名+6 课范围」，`NOW.md:19,32` 写「kickoff 待批」。
- `NOW.md:69-80` 保留了一整段教材逐篇历史流水（与「NOW 只存带日期快照」的定位不符）。
- `PENDING_DECISIONS.md` PD-Q5 裁决列为空；PD-Q6 仍写「已按 PD-003 顺延」。
- `PROGRAM-MANAGER.md:37` 指向 `Render_Notes/.agent/README.md`（路径已不存在）。
- `final-acceptance-2026-11-21.md:57` 判 Radar→Engine「human_selected 门控 ✅」，与导出物 `false` 矛盾。

**测试结果**：Program 无自动化测试（合理，它是文档层）。文档链接未做全量校验；本次只针对关键指针做了存在性核对。

**偏差**
1. 目录/项目名过期（3 处以上），会让新 Agent 打开不存在的路径。
2. 冻结状态过期（Governance/Radar 已解冻并交付）。
3. NOW 内部自相矛盾（已批 vs 待批）。
4. PENDING_DECISIONS 未随 D17–D20 更新，形成第二套过期状态。
5. NOW 承载历史流水，维护成本上升。

**风险**：Program 的唯一价值是「准确的项目级事实」，一旦过期，它会把错误传给下一个 Agent（本次已发生：跨项目第 4 项误判）。

**优化建议（不新增系统）**
- 把 PROGRAM.md 的「当前状态」列改为指针式（只写「详见项目内 WORKFLOW_STATE」），避免每次交付都要改章程。
- NOW.md 只保留「最近 7 天 + 当前主目标 + 阻塞」，历史流水移入 `archive/` 或项目 CHANGELOG。
- PENDING_DECISIONS 增加「已由 Dxx 关闭」列，或直接冻结为存档。

**审计结论：PASS WITH LIMITATIONS**

---

### B.2 PHASE 1 · AI Knowledge-to-Learning Engine（重点）

#### B.2.1 真实交付链逐环节核对

| 环节 | 实现位置（真实文件） | 运行方式 | 输入 → 输出 | 测试/证据 | 已知限制 |
|---|---|---|---|---|---|
| 原始资料 | **无导入工具**；`reviews/p10/intake-manifest.md` 为人工清单模板 | 人工登记 | 外部资料 → 批次清单 | P10 清单 16 行；查重 151 处命中 | 无 schema、无自动查重工具、无资料库 |
| 深度研究 | `.agent/skills/research-to-learning/`（100 行）+ `reviews/p10/research-report-hdr.md` | Agent 按 Skill 执行 + 外部检索 | 清单 → 研究报告（F1–F8） | 8 条来源真实抓取，失败通道如实记录 | 流程可重复性依赖 Agent，非程序化 |
| 证据 | `evidence/claim-ledger.json`（84 条）、`evidence/source-registry.json`（43 条） | `validate_site.py` §8 + `review_gate.py` | 断言 ↔ 来源双向索引 | `review_gate` 84/24v/53o/7c，误标 0 | 断言升级需人工；来源 22/43 为 repo_doc |
| 结构化知识 | `knowledge-model/concepts.json`（25 概念）、`tools/glossary.json`（11 组/129 词） | `build_knowledge_model.py` | 概念/术语 → taxonomy | `validate_site.py` §9 | 概念层仅 25 条，覆盖有限 |
| 知识关联 | `tools/graph.json` + `concepts.json` 关系 | build + validate §9 | 概念 → 图 | 无环校验通过（P10 登记记录） | 关系类型少，未做语义强度 |
| 课程设计 | `tools/course.json`（8 单元/20 课）+ `courses/video-rendering-journey/course.json`（pilot 5 课） | 人工编辑 JSON | 知识 → 课程结构 | `validate_site.py` §10 | **多课程硬约束**：validate §10 要求 pilot id ⊆ 主课程；独立新课程会 FAIL（D21 已报批） |
| 教材 | `courses/video-rendering-journey/lessons/L01–L19.md`（19 份，L00 为地图课） | 人工/Agent 写作 | 课程 → 教材 | `check_chapter_arc` **19/19 OK**；G2 材料 18 份 | 只有 L19 有用户确认分（91）；其余 17 篇待评分 |
| 实践 | `tools/labs.json`（7 实验）+ `courses/.../quizzes/*.json`（5 份） | 站点内置交互 | 教材 → 实验/自测 | publish 11/11；站点渲染含 labs | **quiz 仅 5/19 课**；无自动判分/学习分析 |
| 网站 | `tools/build_site.py` → `web/content.js`；`web/index.html` + `assets/app.js` | `py -3 tools/build_site.py` | Markdown/JSON → 离线站 | build 83 docs/624 cards/3149 KB；HTTP 200；无头渲染出课程/术语 | 仅本地；无在线部署（D02 未授权）；无多课程 UI |
| 反馈 | `tools/feedback.json`（entries=0）+ `tools/report_feedback.py` + 站点 localStorage | 站点导出 → 手工粘贴 → 汇总 | 反馈 → hints | 工具实跑 exit 0（空提示） | **尚无真实反馈数据**；无自动回流 |
| 知识更新 | `tools/kcr_impact.py` + `tools/kcr/schema/*.json` + `tools/kcr/validate_kcr.py` | `kcr_impact.py --claim-id/--source-id` | 变更 → 影响链 JSON | selftest 16/16；P10 影响分析样本 3 份 | 只读分析；不自动改下游；需人工裁决 |

#### B.2.2 G3 复核

- **记录位置**：`.agent/runs/RUN-2026-11-20-p10-hdr.json`（gitignored，本地）。`human_gate = {gate: G3, status: passed, approver: "user(2026-11-21 G2=91 通过)", approved_at: 2026-11-21T22:22:05+08:00}`；`phase=FEEDBACK`、`status=done`、`write_paths=[]`。
- **18 artifacts**：INTAKE 1 / RESEARCH 2 / EVIDENCE 3 / ARCHITECT 2 / WRITE 3 / DESIGN 1 / PRACTICE 1 / REVIEW 3 / PUBLISH 1 / FEEDBACK 1。**唯一路径 16 条**（L19 教材被登记 3 次）。
- **artifact 完整性实测**：18 条中 **7 条 sha256 与当前文件不符**（research-report、G1 队列、glossary、course.json、G2 材料、L19 的 WRITE/PRACTICE 两条）。REVIEW 阶段重登记的 L19 hash 与当前一致，说明「最后一次登记」有效，但历史记录不再是最终交付校验值。
- **`write_paths=[]` 的业务含义**：run 创建时声明了 6 条可写路径（claim-ledger / source-registry / concepts / glossary / course.json / 08-具身智能）；`done` 会释放全部声明。空数组 = **当前没有活动写锁**，其他 Agent 可以安全接手；它**不代表**「这些文件没被改过」，也**不代表**「改动已提交」。
- **G3 代表什么**：代表「该批次可以进入 PUBLISH 阶段（本地 bundle 口径）」。
- **G3 不代表什么**：不代表在线发布已授权（D02 仍禁）、不代表全部课程达标、不代表断言全部核实、不代表产品长期目标完成。

#### B.2.3 D20 复核

- `DECISIONS.md` D20 完整记录了：G1 六项升级（V63–V67 + V23，含 I19=A 先补 HLG 边界）、KCR APPROVED、G2=91、G3 passed、阶段 2–4 解冻执行、收口提交与「未 push」。
- 与 D12–D14 的关系：D12 是 V13/V14 的核验与升级口径；D13 建立 KCR；D14 建立 `.agent/` 统一仓库。D20 是这三者的**执行结果**，不是对它们的改写；未发现「代码推翻决策但决策未更新」的情况。
- 唯一弱点：D20 只记录「用户批准」，未记录**批准载体**（哪条消息/哪个文件/谁），与 A.3 第 2 条同源。

#### B.2.4 G2-L19 复核

- `reviews/G2-L19-deepening.md` §5：23/23/18/17/10 = **91**，≥85 通过；裁决人「用户本人（采纳 AI 诊断建议分，人工确认）」，日期 2026-11-21。
- 评分规则来自 `lesson-quality-standard`（25/25/20/20/10）。证据与扣分点在 §5 备注列可见。
- **误判风险**：该分数是「AI 先给诊断建议分、用户确认」。这符合用户此前的授权模式，但它**不是独立评分**；且 `reviews/` 下仍有 17 篇 G2 材料未评分。把 L19=91 当作「全课程质量已达标」是扩大解释。

#### B.2.5 Engine 完整性清单

| 分类 | 内容 |
|---|---|
| 已完成的生产能力 | 断言/来源台账、概念/术语/图、课程 JSON、19 份教材、7 个实验、5 份 quiz、离线站构建、12 项结构门禁、KCR 影响分析、run_state 状态机、文档注册表、反馈汇总入口 |
| 仅有原型的能力 | 多课程（validate §10 未支持独立课程）；在线发布（无部署/CI）；学习反馈闭环（无真实数据）；三维评分/趋势（Radar） |
| 仅有设计未实现 | P8 输入合同中的「原始资料导入」程序化；研究阶段自动化；quiz 自动判分；学习者进度分析 |
| 仍需人工操作 | 资料登记与查重、研究、断言升级、G1/G2/G3、课程路线、发布授权、commit/push |
| 不能稳定重复的部分 | 深度研究质量（依赖 Agent + 外部抓取）；跨课程复用（工具链限制）；G2 评分（人工） |
| 未覆盖的知识类型 | 只覆盖音视频/图形/GPU 一个领域；具身智能仅 INTAKE；无数学/语言/管理等非工程领域样本 |
| 规模/性能限制 | 83 docs / 3.1 MB bundle 可接受；全量重建秒级；未测 10 倍规模；无增量构建 |

**Vertical Slice 是否真实证明端到端**：**是**。P10 用一批**新**资料（HDR）走完 INTAKE→FEEDBACK，产出新教材入站、断言入账、KCR 提案、发布与反馈记录，且中途被 G1/G2/G3 人工门真实阻塞过。这是六阶段里最强的证据。

#### B.2.6 Engine 优化空间

- 过度复杂的 Agent 协作：无（没有多 Agent 编排器）。
- 重复 Skills：**存在**——`research-to-learning` 同时存在于 `.agent/skills/`（正文）与 `.workbuddy-ai/skills/`（脚本）；这是 D14 的设计（脚本不迁移），但对外部读者是「两处同名」。
- 重复 MCP/Tools：无。
- 相似数据模型：`tools/course.json` 与 `courses/*/course.json` 两层结构，字段重叠但职责不同（站点课程 vs pilot 契约），维护时需双改——P10 已出现「两层 checkpoint 对齐」的额外工作。
- 过多中间产物：`reviews/` 183 篇中 78 篇 unregistered、45 篇 review-material；治理材料与学习内容混在同一仓库，靠 allowlist 排除。
- 过度复杂的人工审核：G1+G2+G3+KCR 四道门对单批教材偏重，但这是质量要求的结果，不建议削减；建议**合并材料**（一页裁决指引已做）。
- 重复文档：README 276 行且数字过期；`site-vitepress` 与 `web/` 两套站点。
- 无价值抽象层：未发现。
- 难恢复的长任务：run_state 已提供 pause/resume/retry，25 测试覆盖；这是加分项。
- 测试覆盖不到的关键路径：`build_site.py` 本身无单测（靠 validate §7 产物检查）；`publish_boundary` 为 advisory，不阻断；G2/G3 人工门无自动化校验（设计如此，但缺少独立证据）。

**审计结论：PASS WITH LIMITATIONS**

---

### B.3 PHASE 2 · Learning Experience Design

**原始目标**：Engine 内部专属 Skill，不独立成仓；改善阅读/交互/信息架构/学习路径/视觉；真实页面验证；有可执行方法与检查标准；不与 Engine 原有设计规范重复维护。

**实际交付**
- `.agent/skills/learning-experience-design/`：`SKILL.md`（131 行，`status: active`）、13 份 references、3 份 assets 模板、`preview/PILOT-L13-plan.md`、`scripts/check_visual_floor.py`。
- `SKILL.md` 定义 Floor（硬阻塞）/Reflex（可豁免）/Finish（不阻塞）三级门槛，绑定现有 `course.json/glossary.json/labs.json/graph.json`，不另建内容库。
- 试点 A：L13 页面六项增强（学习目标条、空间链 V17 标注、P·V·M 分行推导表、MVP 术语绑定、前后对照、偏差记录），提交 `4945711`（L13 +15 行）。
- L19 作为第二应用点：仅 Floor 静态检查通过，**未做页面增强**。

**测试与证据**
- `check_visual_floor.py` L13 → exit 0（我本人复跑）；L19 → exit 0。
- `validate_site` 12/0/0；`arc 19/19`；L13 增强内容在正文可定位（`L13:24` 学习目标、`L13:89` MVP 术语卡）。
- 无浏览器截图、无多宽度回归、无真实用户测试记录。

**偏差与风险**
1. **只有 1 个真实优化案例**（L13）。把「一个试点」推断为「适用于所有课程/页面/Agent」不成立。
2. **13 份 references 明显重叠**：`accessibility.md` vs `accessibility-and-responsive.md`；`design-system.md` vs `visual-system-and-layout.md`；`interaction-patterns.md` vs `learning-interaction-patterns.md`；`responsive-design.md` 与上面两组交叉；`ux-review-checklist.md` vs `visual-quality-gates.md`。SKILL.md 只显式引用 6 份，其余处于「存在但未挂接」状态。
3. **可发现性依赖 `.agent/README.md` 索引**，AGENTS.md 不直接列 Skill；对不读 `.agent/` 的 Agent，发现链是断的。
4. **Floor 脚本只做静态检查**（标题层级、outline:none、硬编码颜色、主题变量、生成物引用），明确不替代浏览器与人工；报告若把它当「视觉质量通过」会过度解释。

**成熟度定位**：**「Skill 已完成一次真实优化」**，未达到「多案例验证」，更未达到「稳定复用」。

**优化建议**
- 合并 13 份 references 为 5–6 份（原理 / 设计系统 / 页面原型 / 可视化 / 审查门槛 / 无障碍与响应式），消除重叠。
- 再做 2 个不同类型页面（实验页、面试速查页）才升级「稳定复用」表述。
- 在 AGENTS.md 增加一行 Skill 索引，保证发现链完整。

**审计结论：PASS WITH LIMITATIONS**

---

### B.4 PHASE 3 · Agent Workspace Governance

**原始目标**：可移植 Agent 项目治理工具包；管文档/任务/交接/ADR/规范生命周期；登记 Skills/MCP/Tools 元数据；区分安装/发现/调用/验证；至少两个项目验证可移植；不替代业务 Orchestration；不做复杂 Dashboard。

**实际交付**
- `cli/governance.py`（1176 行，stdlib-only，11 个子命令：init/inventory/index/validate/status/map/doctor/handoff/adr/archive-check/audit）。
- 5 个 JSON schema（document/task/agent/decision/project）、6 个模板、4 篇 constitution、3 篇 docs、5 个 adapter 说明。
- `tests/test_governance.py`：28 个测试。
- 真实适配产物：Engine 的 `.governance/` 5 个 JSON，`document-registry.json` 登记 **183** 篇文档（审计基线；本次新增 2 份使用文档后重建为 185）。

**「9/9」逐项核对**

| # | 声称项 | 真实文件/能力 | 测试 | 审计判定 |
|---|---|---|---|---|
| 1 | 治理规范 | constitution 4 篇 + specification | 无自动化 | 存在，属规范 |
| 2 | 文档生命周期 | DOCUMENTATION_POLICY + archive-check | `test_archive_check` | 部分可执行 |
| 3 | Task/Handoff 契约 | task.schema + handoff 命令 | 2 测试 | Handoff 可生成；Task 无创建/认领 CLI |
| 4 | ADR | decision.schema + adr create/list/check | `test_adr_*` | 可创建/列出；状态推进需手改 |
| 5 | 元数据结构 | 5 schema + 6 必填 frontmatter + 13 类枚举 | 2 测试 | 可校验 |
| 6 | 最小自动化 | 11 子命令 | 28 测试 | 可执行（但命令数三处口径不一：9/10/11） |
| 7 | 真实项目适配 | Engine `.governance` 183 docs | 仅关键词测试 | 注册表落地；**Engine 无治理入口指针** |
| 8 | 独立示例项目 | `examples/basic-project` | 3 测试 | **doctor exit 1**（2 个 type 非法） |
| 9 | 使用说明 | README + migration-guide | 无 | 存在，但示例类型照抄会出错 |

**测试实跑**
- `py -3 tests\test_governance.py` → **exit 0，28 tests OK**。
- `py -3 cli\governance.py doctor --project examples\basic-project` → **exit 1**（2 项错误）。
- `py -3 cli\governance.py doctor --project ..\ai-knowledge-to-learning-engine` → **exit 1，621 项**（与文档记载一致）。

**关键问题**
1. **9/9 是文档自证**：`1b4a880` 只改 `examples/render-notes/README.md`（+17 行），无代码无测试。
2. **入口指针缺失**：`init` 对已存在 AGENTS.md 静默跳过；Engine `AGENTS.md` 无 `agent-workspace-governance` 字样；生成的指针还硬编码 `agent-workspace-governance/constitution/`（在临时项目指向不存在路径）。
3. **注册表空转**：Engine `task-registry=0 / agent-registry=0 / adr-index=0`；5 个 adapter 全部 `unverified`。
4. **审批无 schema**：`HUMAN_APPROVAL_POLICY` 要求记录 approver/time/object/decision/scope 并写入 `.governance/`，但 task schema 只有 `human_approval_required` 布尔，没有存储结构。
5. **契约与实现不一致**：`AGENT_RULES.md:75` 声称 doctor 检查「进行中但缺 claimed_at」，实测 `doctor` exit 0；`DOCUMENTATION_POLICY` 列出的 expired/duplicates 等查询中部分未实现。
6. **可移植性**：只验证了 Engine 一个真实项目；`examples/basic-project` 不通过自身 doctor，不能作为第二项目证据。

**它现在真正能帮上忙的**：批量清点 Markdown、按 doc_id 去重、检出未登记/孤儿/重复/过期引用、检出单写者冲突与依赖环、生成 handoff/ADR。**不能**：自动补 frontmatter、自动迁移、强制审批、跨仓库调度。

**优化建议**
- 修 `examples/basic-project` 的 type 到 13 类枚举，让 9/9 第 8 项成立。
- `init` 在已有 AGENTS.md 时追加「治理入口」段（或明确提示），并把工具包路径写成相对路径。
- 给 approval 增加最小记录文件/schema（5 字段），否则删掉政策里的「写入 .governance」承诺。
- 修正 9/10/11 命令数口径；README 与 AGENTS.md 对齐。
- 停止新增功能，先把「一个普通项目从 init 到 doctor=0」的路径打通。

**审计结论：PARTIAL**

---

### B.5 PHASE 4 · GitHub Project Radar

**原始目标**：发现 GitHub 项目；跟踪变化；24h/7d/30d；识别趋势；可解释筛选；历史快照与来源；候选管理与报告；导出 Research Intake；不自动安装/导入。

**实际交付**
- `cli/radar.py` 9 子命令；`radar/` 模块（collector/growth/scoring/storage/reports/review/export/sources/rest）；SQLite 4 表；`config/topics.json`、`config/scoring.json`；`tests/test_radar.py` 38 测试；`reports/2026-W47/` 7 文件 + intake JSON。
- 真实抓取：`radar-real-20261121.db`（本地、gitignored）。

**数据实测（我只读 SQLite 复核）**
- repositories **121**、snapshots **200**、candidates **121**（Discovered 120 / Research 1）、collection_runs **1**。
- 快照跨度 `2026-11-21T11:46:46Z – 11:47:06Z`，**4 个不同时间点，20 秒**；每仓 1–4 条。
- `snapshots.source_url` **200/200 NULL**；`repositories` 溯源字段同样 NULL。
- 增长：**121/121 `insufficient_history`**，`star_growth_7d/30d` 全 null。
- 周报 `star-growth.json` 121 条与 DB 逐条一致；`weekly-report.md` 的「每周崛起项目」按 `growth_momentum.score` 排序，而该分 121/121 为 0.0 → 实际按插入顺序取前 15。

**八项能力**
| 能力 | 实现 | 判定 |
|---|---|---|
| 发现项目 | `collector.discover` + `rest.py` | 真实可用（匿名 60 req/h） |
| 保存快照 | `insert_snapshot`，UNIQUE(repo,captured_at) | 可用；但真实库无法通过 CLI 追加（`snapshot` 固定 fixture） |
| 24h/7d/30d | `growth.compute_growth` | 算法正确；数据不足时如实返回 insufficient_history |
| 过滤排序 | `list_candidates` + `compare_group` | 可用；跨组拒绝排名 |
| 候选状态 | `ReviewStateMachine` + review_log | 可用；但 `analyze` 会覆盖人工状态（D1） |
| 报告生成 | `reports.py` 7 文件/摘要/JSON | 可用；「崛起」板块语义失真 |
| Intake 导出 | `export.py` 15 字段 | 可用；但人工门可绕过（D3） |
| 失败恢复 | 重试/退避/事务/幂等 | 有；无 HTTP 缓存/断点续采 |

**关键问题**
1. **D1 数据丢失**：`cli/radar.py:140,143` + `storage.py:340-346` 在 `analyze` 时 upsert 覆盖 `review_status` 与 `human_selected_for_research`；当前库中的 1 条 `Research` 重跑即丢。
2. **D2 配额感知失效**：`rest.py:140-141` 的 `search_repositories` 丢弃 `_rate_limit_remaining`，`collector.py:53-54` 的保护拿不到值。
3. **D3 人工门可绕过**：`export.py:101-102` 的 `--approved` 只改 `review_status` 字符串，不置 `human_selected_for_research`；产物该字段 **false**，按自家 `docs/engine-interface.md` 不可导入。
4. **D4 审计不全**：`collection_runs.query_params` 只记 `query_count`，不记查询语句与错误清单；「0 错误」只能由 `status=success` 间接推定。
5. **D5 溯源全空**：无法区分 live/demo、无法做数据质量分级。
6. **无调度**：仓库内 0 个 scheduler 配置；`collection_runs=1` 印证只跑过一次。
7. **文档漂移**：README/AGENTS 仍写「离线、不发起网络请求」；`operating-guide.md` 描述 `research` 子命令但 CLI 不存在；三维评分实现未接入 `analyze`。

**它现在真正能帮上忙的**：一次性发现 + 打分 + 周报 + 候选导出（人工可控）。**不能**：持续追踪趋势、可靠维护人工筛选状态、自动接入 Engine。

**优化建议**
- **P0**：修 D1（保留人工字段），加「analyze 两次不改变 Research 状态」回归测试。
- **P1**：修 D3（`--approved` 必须写 `human_selected_for_research=true` 并记录 reviewer/time）；修 D2；给 `snapshot` 增加真实库入口（或把 `refresh_tracked` 暴露为 CLI）。
- **P1**：周报 A 板块在增长不可得时改为「数据不足，暂不排名」。
- **P2**：README/AGENTS 与 rest.py 对齐；补 `research` 子命令或删文档；三维评分接入或删除。
- **P2**：加最小调度（Windows 任务计划 XML 或文档化命令），否则「持续追踪」不成立。

**审计结论：PARTIAL**

---

### B.6 PHASE 5 · 跨项目整合

**八项核对复核**

| # | 报告判定 | 审计复核 | 证据 |
|---|---|---|---|
| 1 Program↔Engine 指针 | ✅ | **部分失效** | `PROGRAM.md:21,28` 与 `PROGRAM-MANAGER.md:37` 仍指 `Render_Notes/`（已改名）；`NOW.md` 指针有效 |
| 2 Engine↔Skills 引用 | ✅（架构约定） | **成立但无文件级链接** | Engine 使用自有 `.agent/skills/research-to-learning`；未引用 `matt-pocock-skills-zh-cn`。这是设计选择，但「能使用通用 Skills」未被实际验证 |
| 3 Governance→Engine 适配 | ✅ | **部分成立** | `.governance/` 5 JSON + 183 docs 真实；但 `AGENTS.md` 无治理入口，doctor 621 项未清零 |
| 4 Radar→Engine Intake | ✅ 门控 | **不成立（误判）** | 导出物 `human_selected_for_research=false`；Engine 无 intake JSON 契约，`reviews/p10/intake-manifest.md` 是人工清单 |
| 5 LXD↔门禁链 | ✅ | 成立 | Floor 脚本 + validate/arc 可并存；L13 已落地 |
| 6 Radar/Governance 提交 | ✅ | 成立 | `b7442da` / `1b4a880`+`6aec3d3` |
| 7 Skills 库定位 | ✅ | 成立（供应库维护态） | README/安装命令指向正确；37 技能 |
| 8 Program 未提交 | ✅ | 当时成立；现在 NOW.md 又脏 | `git status` 1 个文件 |

**依赖关系图（实测）**

```
                    ┌──────────────────────────────┐
                    │ AI Knowledge Program (meta)  │
                    │ PROGRAM/NOW/ROADMAP/PARKING  │
                    └───────┬──────────────┬───────┘
            指针(部分失效)  │              │ 状态引用(过期)
                            ▼              ▼
        ┌───────────────────────────┐   ┌──────────────────────────┐
        │ Engine (唯一产品)          │   │ Governance (本地工具包)   │
        │ 知识/课程/教材/站点/KCR     │◄──┤ .governance/ 183 docs     │
        │ .agent/skills/*            │   │ 无入口指针 / doctor 621   │
        └───┬───────────┬───────────┘   └──────────────────────────┘
            │           │
   LXD Skill│           │ 输出 JSON（未导入）
   (内部)   ▼           ▼
     ┌────────────┐  ┌──────────────────────────┐
     │ 页面增强    │  │ Radar (本地情报)          │
     │ L13 试点    │  │ 121 repo / 200 snapshots │
     └────────────┘  │ export: human_selected=  │
                     │ false → Engine 不消费     │
                     └──────────────────────────┘

Skills 库（GitHub, 37 skills）── 独立供应库，未被 Engine 文件级引用
```

**整合层面的真实缺口**
- Program 的指针过期（第 1 项）。
- Radar→Engine 没有可执行契约（第 4 项误判）。
- Governance 对 Engine 只有注册表，没有入口（第 3 项）。
- Engine 与通用 Skills 库无实际调用关系（第 2 项仅架构声明）。
- 两套站点生成器（`web/` 与 `site-vitepress/`）并存，VitePress 构建被 D10.6 阻塞。
- 同一语义多处命名：`review-report` / `G2 材料` / `质量诊断` 并存；`task` / `review` / `approval` 在不同项目含义不同。

**审计结论：PARTIAL**

---

## C. 原规划符合性矩阵

| 原始要求 | 实际实现 | 证据 | 符合程度 | 问题 |
|---|---|---|---|---|
| Program 是轻量统筹层 | 5 文件 + decisions/plans/handoffs | `PROGRAM.md` 140 行 | 高 | 状态过期 |
| Program 不复制子项目文档 | 原则明确，仅指针 | `PROGRAM.md` §5 | 高 | NOW 仍抄了历史流水 |
| Program Manager 可恢复任务 | 12 步流程 + 2 份 handoff | `PROGRAM-MANAGER.md:32` | 高 | 依赖文档准确；当前 NOW 矛盾 |
| 范围控制/准入规则 | 四问 + 硬规则 + 防膨胀六问 | `PARKING-LOT.md:16` | 高 | — |
| 不建管理平台 | 无 Dashboard/DB | 目录结构 | 高 | — |
| Engine 不是只产 Markdown | 站点 + 实验 + 状态机 | `web/`、`labs.json`、`run_state.py` | 高 | 站点仅本地 |
| 真实端到端 Vertical Slice | HDR 批次真实 run | run JSON 18 artifacts | 高 | 单批、单领域 |
| 阶段输入输出契约 | KCR 四 schema；研究/INTAKE 无 schema | `tools/kcr/schema/*` | 中 | 前段靠 Markdown |
| 质量检查 | 12 结构检查 + arc + review_gate + G2 | `validate_site.py` | 高 | G2 17 篇未评 |
| 证据可追踪 | 84 claims / 43 sources / 双向索引 | `evidence/*.json` | 高 | artifact hash 7/18 失效 |
| 失败定位与恢复 | pause/resume/retry/fail/skip | `run_state.py` | 高 | 仅 1 个真实 run |
| 人工审批节点 | G1/G2/G3 + approver 非空 | run JSON | 中 | 无独立审批证据 |
| KCR 下游影响 | Source→Claim→Concept→Lesson→Quiz→Course→Site | `kcr_impact.py` | 高 | 只读、不自动应用 |
| 网站可访问/呈现 | 本地 HTTP 200 + 无头渲染 | 实测 | 中 | 未在线发布；内部文档混入 |
| 覆盖边界明确 | 19 课/1 领域/具身仅 INTAKE | course.json | 中 | 边界未写进 README |
| LXD 属 Engine 内部 | `.agent/skills/learning-experience-design` | SKILL.md | 高 | — |
| LXD 改善真实页面 | L13 六项增强 | `4945711` | 中 | 1 案例 |
| LXD 有可执行检查 | Floor 脚本 | `check_visual_floor.py` | 中 | 仅静态 |
| LXD 不与原规范重复 | 13 份 references 重叠 | references/ | 中 | 需合并 |
| Governance 可移植工具包 | CLI + 5 schema + 28 测试 | `cli/governance.py` | 中 | 仅 1 真实项目 |
| Governance 管文档/任务/交接/ADR | 文档/ADR/handoff 可执行；任务仅 schema | CLI | 中 | 任务无入口 |
| Governance 元数据四态 | config/discovery/invocation + 总 status | `agent.schema.json` | 低 | 无 install；verify 粒度粗 |
| 两项目验证 | Engine + basic-project | 实测 | 低 | basic-project doctor 失败 |
| 不替代 Orchestration | 无 run_state/KCR 复制 | rg 证据 | 高 | 有轻度 task claim 重叠 |
| Radar 发现/快照/增长/筛选/报告/导出 | 八项代码均在 | `radar/*` | 高 | — |
| Radar 真实 API 与限流 | rest.py + 退避 | 121 仓实跑 | 中 | 配额丢弃、无缓存 |
| Radar 增量正确 | 累计 vs 窗口区分 | `growth.py` | 中 | 无数据；不校正采样间隔 |
| Radar 可解释评分 | 5 维 + reason/basis | `scoring.py` | 高 | 三维评分未接入 |
| Radar 人工门槛 | review 状态机 | `review.py` | 中 | 导出可绕过 |
| Radar 不自动导入 | 无导入代码 | — | 高 | — |
| 集成：Program 知状态 | 指针 | PROGRAM.md | 中 | 过期 |
| 集成：Engine 用通用 Skills | 无文件级引用 | — | 低 | 仅架构声明 |
| 集成：Governance 可被使用 | 注册表落地 | `.governance` | 中 | 无入口/621 诊断 |
| 集成：Radar 供候选 | JSON 导出 | `research-intake-hdr-demo.json` | 低 | 门控 false |
| 无重复建设 | 两套站点 + 两处 research skill + 13 参考 | — | 中 | 需收敛 |

---

## D. 严重偏差

> 只列「可能影响整体项目价值」的问题；轻微文案问题进 §E 的 P2/P3。

1. **Governance「9/9 完成」不成立，且是文档自证。**
   影响：如果按 9/9 宣布阶段完成，后续不会再投入，实际它只完成「扫描/诊断工具 + 注册表」；Task/审批/Agent 注册在真实项目中为空。新项目照 README 接入会得到 600+ 诊断错误且没有入口指针。

2. **Radar 存在数据丢失与人工门绕过。**
   影响：`analyze` 覆盖人工复核状态；`--approved` 不置 `human_selected`。一旦开始日常使用，人工筛选成果会被一次重跑清空，且「人工批准」在数据上不可证明。这是**使用级阻断**，不是 cosmetic。

3. **人工门与 artifact 的可追溯性弱于报告表述。**
   影响：G3 approver 是 AI 写入的字符串；18 条 artifact 中 7 条 hash 与现状不符；run JSON 在 `.agent/runs/`（gitignored），不随仓库版本化。外部审计者无法仅凭仓库证明「谁在何时批准了哪一版」。

4. **Program 状态漂移导致跨项目误判。**
   影响：`final-acceptance` 第 4 项把 Radar→Engine 判为通过，而导出物 `human_selected_for_research=false`；PROGRAM.md 仍指 `Render_Notes/`。Program 的「唯一入口」作用因此不可靠。

5. **学习站发布边界把内部治理/审核材料带进学习者视图。**
   证据：`web/content.js` 的 83 docs 含 `DECISIONS.md`、`CHANGELOG.md`、`WORKFLOW_STATE.md`、`NEXT_PHASE_PLAN.md`、`courses/.../G2-审核材料-P6.md`、`教材质量诊断.md`、`review-report.md`。`publish-allowlist.json` 只排除 `reviews/`，未排除 `courses/` 内的审核材料；且 allowlist 仍含已删除的 `program-office-delivery`。
   影响：网站「可用、清晰」打折扣；学习者会看到项目治理内容。

6. **两套站点生成器并存。**
   `web/`（离线站，主用）与 `site-vitepress/`（在线站源码，D10.6 build 被拦）。两套共用 publish_boundary，但只有一套被验证；长期是维护负担。

7. **Skills 库的 Agent 兼容性全部无仓库内证据。**
   文档分层诚实（官方支持/安装器声称/未验证），但 `.claude/`、`.agents/`、`skills-lock.json` 均不存在；「已验证安装」只是叙述。这不影响它作为技能内容库，但影响「可安装性」承诺。

---

## E. 优化建议（按优先级）

### P0（立即处理：影响正确性/数据安全/核心入口）

**P0-1 Radar `analyze` 覆盖人工状态**
- 问题：upsert 把 `review_status` / `human_selected_for_research` 重置。
- 原因：`storage.py:340-346` 的 ON CONFLICT 更新了人工字段。
- 影响：人工复核成果丢失；候选池不可持续。
- 最小修复：ON CONFLICT 只更新机器字段（stars/score/growth），人工字段仅在新插入时初始化；`review` 是唯一写入口。
- 验收：连续两次 `analyze`，`Research` 状态与 `human_selected` 保持不变（新增 1 个测试）。
- 新复杂度：低。

**P0-2 Program 状态纠偏（单一事实源）**
- 问题：PROGRAM.md 的 `Render_Notes`/`冻结`、NOW 的「待批」、PM 的旧路径、PENDING 的空裁决。
- 原因：六阶段交付后只更新了 NOW/ROADMAP 的局部。
- 影响：新 Agent 会沿错误路径工作；跨项目判断出错（已发生）。
- 最小修复：改 6 处（PROGRAM §2/§4/§5、PM §2/§5、NOW 主目标、PENDING PD-Q5/Q6、final-acceptance #4）。
- 验收：全仓 grep `Render_Notes|mattpocock-skills-zh-CN-custom|冻结` 只剩历史记录段；NOW 内无「待批/已批」矛盾。
- 新复杂度：无。

### P1（尽快处理：影响可用性/可信度）

**P1-1 人工门证据独立化**
- 问题：approver 字符串无身份；artifact hash 失效。
- 最小修复：新增 `approvals/<run>-<gate>.md`（approver 姓名、时间、范围、被批文件 hash 列表），`gate --pass` 时重算并写入；`done` 前校验全部 artifact hash，过期则要求重登记。
- 验收：改动任一被批文件后 `gate`/`done` 失败并指出文件。
- 新复杂度：中（1 个新目录 + 2 个校验函数）。

**P1-2 Governance 让「9/9」成立或改口径**
- 修 `examples/basic-project` 的 2 个 type；`init` 在已有 AGENTS.md 追加治理入口（相对路径）；给 approval 增加 5 字段记录；统一 9/10/11 命令数。
- 验收：`doctor --project examples/basic-project` exit 0；Engine AGENTS.md 出现治理指针；新增 1 个 approval 测试。
- 新复杂度：低。

**P1-3 Radar 人工门与配额**
- `--approved` 写 `human_selected_for_research=true` + reviewer/time；`search_repositories` 保留 `_rate_limit_remaining`；周报 A 板块在增长不可得时标注「数据不足」。
- 验收：导出物 `human_selected=true`；rate-limit 字段可读；周报不含伪「崛起」排名。

**P1-4 发布边界**
- 把 `DECISIONS/CHANGELOG/WORKFLOW_STATE/NEXT_PHASE_PLAN/PROJECT_CURRENT_STATE`、`courses/**/G2-*`、`教材质量诊断`、`review-report`、`课程覆盖矩阵` 移出学习者 bundle（或改为「项目文档」独立入口）；删除 allowlist 中已不存在的 `program-office-delivery`。
- 验收：`content.js` 文档清单不含治理/审核材料；validate 仍 12/0/0。

**P1-5 Engine README 与实际对齐并瘦身**
- 数字：26 篇主文档 / 57 非归档 / 124 术语 / 19 课 / 31 断言 / 16 来源 → 实际 83 docs / 129 术语 / 20 课 / 84 断言 / 43 来源。
- 按任务书 §12，README 只留简介/价值/能力/Quick Start/文档入口/状态/链接，操作流程移入 `docs/USER-GUIDE.md`。
- 验收：README ≤120 行；所有数字与 `build_site` 输出一致。

**P1-6 LXD references 去重 + 第二案例**
- 13 → 5–6 份；SKILL.md 显式挂接每一份；再做 1 个实验页案例。
- 验收：无两份文档讲同一主题；SKILL.md 引用覆盖率 100%。

**P1-7 D20 决策载体补记**
- 在 D20 增加「批准载体」：用户消息日期/渠道、G2 §5 链接、G3 记录路径。
- 验收：外部审计者可沿一条链走到用户原话。

### P2（重要改进，可后续）

- **P2-1** Radar README/AGENTS 与 REST 实现对齐；`research` 子命令补实现或删文档；三维评分接入或删除。
- **P2-2** Skills `AGENT-COMPATIBILITY.md` 的「14 技能」陈旧断言（37 技能/31 公开）；`in-progress/README.md` 安装命令仍指向上游 `vinvcn`；`docs/engineering/resolving-merge-conflicts.md` 悬空页。
- **P2-3** Engine 双站点收敛：VitePress 若保留，纳入门禁；否则标记 archived。
- **P2-4** 19 课 quiz 覆盖：至少给每个单元 1 课配 quiz，或明确「quiz 仅 pilot 5 课」写进 README。
- **P2-5** `research-to-learning` 两处同名（`.agent/skills` 正文 + `.workbuddy-ai/skills` 脚本）加一份「为什么两处」的说明链接。
- **P2-6** Program NOW 历史流水移出，改为「最近 7 天」。

### P3（可选）

- Skills 109 处 `—` 违反自定规则；2 个英文标题、2 个占位标题。
- Governance `ResourceWarning: unclosed file`（测试）。
- `publish-allowlist` policy 从 advisory 升强制（需人工裁决）。
- `web/content.js` 时间戳导致每次 build 都有 1 行 diff（可接受，但提交时需说明）。

---

## F. 最终结论

**1. 六阶段是否真的完成？**
交付物层面：**是**（都有代码/文档/产物/提交）。
目标层面：**不是全部**。Engine 主目标成立；LXD 是「单案例成立」；Governance/Radar 是「MVP 成立、承诺未闭环」；集成是「表格成立、两处判断失真」。

**2. 是否符合最初总体规划？**
大方向符合：单活跃线、不建平台、Engine 端到端、LXD 内部化、Governance 可移植、Radar 不自动导入。
偏差集中在「把 MVP 说成完成」：Governance 9/9、Radar 八功能+真实数据、集成第 4 项。

**3. 有哪些明显偏差？**
见 §D 七条；最严重的是 Governance 9/9 自证、Radar 人工门/状态覆盖、人工门证据弱、Program 状态漂移、发布边界混入治理材料。

**4. 哪些地方已经过度建设？**
- Governance 的 13 类文档 × 5 注册表 × 5 adapter，相对「0 task/0 agent/0 ADR」的真实使用明显偏大。
- LXD 13 份 references（6 份即够）。
- Engine 两套站点。
- Program NOW 承载历史流水。
这些都不是代码膨胀，而是「文档/协议表面 > 已验证使用」。

**5. 是否可以开始常态化使用？**
- **Engine 本地生产**：可以，按批次 + 人工门；不要承诺在线发布与多课程。
- **Skills 库**：可以当内容库用；「已安装/已发现/已调用」需自行验证。
- **LXD**：可以在新页面上用，但要接受「单案例方法」。
- **Governance**：可以当扫描/诊断工具；不要当「治理平台」接入。
- **Radar**：**修完 P0-1 + P1-3 再用**；现在只适合一次性探索。

**6. 当前最应该做的三件事**
1. **修 Program 状态 + 跨项目第 4 项**（P0-2，半天内可完成）——恢复「单一事实源」。
2. **修 Radar P0-1/P1-3 与 Governance P1-2**——把两个 PARTIAL 拉到可用。
3. **Engine 收口 P1-1/P1-4/P1-5**——让「人工门可审计、站点干净、README 不误导」。

**7. 哪些项目应冻结，不再增加功能？**
- **Radar**：修完 3 个缺陷前冻结新功能；修完后保持「按需跑周报」，不做自动调度平台。
- **Governance**：冻结新功能，只修缺陷与文档一致性；等第二个真实项目再谈扩展。
- **LXD**：冻结新增 references，先做 2 个案例。
- **Skills**：维护态（上游同步 + 回填），不加新分类体系。
- **Engine**：继续，但**不同时开新领域**；embodied 首批按批推进，P10.3 其他领域另批。

---

## 附录 A · 测试记录（2026-11-23）

| 项目 | 测试对象 | 命令 | Exit | 结果 | 证据/输出 | 验证范围 | 未验证 |
|---|---|---|---|---|---|---|---|
| Engine | 站点构建 | `py -3 tools/build_site.py` | 0 | PASS | 83 docs/17 sections/129 terms/20 lessons/7 labs/624 cards/3149 KB | 构建链路 | 视觉细节 |
| Engine | 结构门禁 | `py -3 tools/validate_site.py` | 0 | PASS | 12 checks, 0 warnings, 0 failures | 链接/锚点/JSON/LaTeX/bundle/evidence/model/course/coverage/registry | 语义正确性 |
| Engine | 章节弧 | `check_chapter_arc.py L01..L19` | 0 | PASS | 19/19 OK | 教学目标闭环结构 | 内容深度 |
| Engine | 发布边界 | `py -3 tools/test_publish_boundary.py` | 0 | PASS | Ran 11 tests, OK | allowlist/排除口径 | 在线部署 |
| Engine | 断言门 | `py -3 tools/review_gate.py` | 0 | PASS | 84 claims, 24v/53o/7c, 误标 0 | 状态一致性 | 断言真值 |
| Engine | KCR 自测 | `py -3 tools/kcr/selftest_impact.py` | 0 | PASS | 16 tests OK | 四契约 + 影响链 | 真实变更应用 |
| Engine | 状态机自测 | `py -3 tools/kcr/selftest_runstate.py` | 0 | PASS | 25 tests OK | 五不变量/恢复/重试 | 多 run 并发 |
| Engine | 视觉 Floor | `check_visual_floor.py L13 / L19` | 0/0 | PASS | OK / OK | 静态可读性前置 | 浏览器视觉 |
| Engine | 站点访问 | `http.server 8791` + GET | 200 | PASS | index/content/app/css 均 200 | 本地可访问 | 公网 |
| Engine | 渲染 | Edge headless dump-dom | 0 | PASS | 出现「为什么视频不是 RGB」「学习路径」「术语」 | 首屏渲染 | 交互操作 |
| Governance | 单测 | `py -3 tests\test_governance.py` | 0 | PASS | Ran 28 tests OK | CLI/文档/ADR/handoff | 真实项目端到端 |
| Governance | 示例项目 | `doctor --project examples/basic-project` | **1** | **FAIL** | 2 个 type 不在枚举 | 9/9 第 8 项 | — |
| Governance | Engine 适配 | `doctor --project <ENGINE>` | 1 | 诊断发现 621 项 | 与文档一致 | 真实适配规模 | 清零可行性 |
| Radar | 单测 | `py -3 -m unittest discover -s tests` | 0 | PASS | Ran 38 tests OK | 八功能单元 | 真实 REST 分支 |
| Radar | 真实库 | SQLite `mode=ro` 查询 | 0 | PASS（数据一致） | 121 repo/200 snap/1 run/4 时间点/20 秒/provenance 全 NULL | 数据真实性 | 星数外部核验 |
| Skills | 翻译校验 | `node scripts/check-translation.mjs` | 0 | PASS | 无输出 | 结构/名称/许可证 | 语义翻译 |
| Skills | 英文残留 | `node scripts/audit-english.mjs` | 0 | PASS | 无输出 | 启发式 | 术语一致性 |
| Skills | 技能计数 | `Get-ChildItem skills -Recurse -Filter SKILL.md` | — | 37 | 37 | 清单 | 兼容性 |

> 说明：本机未安装 pytest，项目也均未使用 pytest；Governance 用直接脚本、Radar 用 unittest，均为项目自带方式。

## 附录 B · 证据索引

- Engine run：`.agent/runs/RUN-2026-11-20-p10-hdr.json`（本地，gitignored）
- Engine 发布/反馈：`reviews/p10/publish-record-hdr.md`、`reviews/p10/feedback-record-hdr.md`
- Engine G1/G2：`reviews/p10/G1-hdr-verification-queue.md`、`reviews/G2-L19-deepening.md`
- Engine 决策：`DECISIONS.md` D12–D14、D20、D21
- Engine 状态：`WORKFLOW_STATE.md`、`reviews/P8-KCR-kickoff.md`、`reviews/P9-orchestrator-design.md`
- Engine 工具：`tools/*.py`、`tools/kcr/schema/*.json`
- Program：`PROGRAM.md`、`NOW.md`、`ROADMAP.md`、`PARKING-LOT.md`、`PROGRAM-MANAGER.md`、`final-acceptance-2026-11-21.md`
- Governance：`cli/governance.py`、`tests/test_governance.py`、`examples/basic-project/`、`examples/render-notes/README.md:74-88`
- Radar：`cli/radar.py`、`radar/*.py`、`radar-real-20261121.db`、`reports/2026-W47/`
- Skills：`skills/**/SKILL.md`、`scripts/check-translation.mjs`、`BACKPORTS.md`、`AGENT-COMPATIBILITY.md`

## 附录 C · 未能验证的事项（NOT VERIFIED）

1. Governance 在 Engine 内的原始执行日志（只有产物与文档陈述，无命令日志）。
2. Governance 是否有第三个不同领域项目验证（工作区内不存在）。
3. Skills 的「已验证安装/发现/调用」在任何宿主上的真实证据（仓库内无安装产物/日志）。
4. Radar 121 仓 Stars 绝对值的外部真实性（只核对了内部一致性，未逐仓对比 GitHub）。
5. G3 审批的用户原话载体（只有 AI 写入的 approver 字符串与 G2 §5 的「用户本人」）。
6. 在线发布可行性（D02 未授权，未做任何部署尝试）。
7. 10 倍规模下的构建/门禁性能（未压测）。