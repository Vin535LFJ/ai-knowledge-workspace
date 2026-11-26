---
doc_id: PROG-STABILIZATION-VERIFY-20261125
type: review-report
status: active
owner: qwenwork
created: 2026-11-25
updated: 2026-11-25
---

# 稳定化验证报告 · 人工验收准备与维护项副本验证（2026-11-25）

> 执行依据：用户 2026-11-25 任务书《六课人工验收准备与稳定化阶段》。
> 性质：本报告只记录**实际执行并有证据的结果**。没有执行的写"未做"，推断的写"未核实"。PASS WITH LIMITATIONS 没有被改写成 PASS；Skills 仍是 PARTIAL。
> 起点：各仓 HEAD = Engine `9923708`（领先远端 9 笔）、Skills `9ac74ea`（领先 1 笔）、Program `175a957`、Governance `2ab2891`、Radar `dbff9c7`；五仓工作树在本轮开始时干净（Engine 无未提交项），`stash@{0}` 原样。

## 0. 结论速览

| 交付项 | 结论 | 关键证据 |
|---|---|---|
| 1. G1 / G2 用户验收包 | **已产出**（Engine `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`） | 20 条断言逐条 12 个字段；六课逐课 11 个字段 + 评分表；裁决栏全部留空 |
| 2. E03 / E06 及两处小修专项复核 | **完成，无 blocker、无 major；8 条 minor + 1 处证据链缺口** | 独立审读代理只读复核 + 我方重算；全文 `targeted-recheck.md` |
| 3. Radar 真实数据库副本验证 | **通过（仅限副本）** | 人工状态不被重置、批准幂等、非法转换被拒；58 项测试 exit 0；真实库 SHA256 前后一致 |
| 4. Governance 真实项目副本接入 | **部分通过** | init 安全且幂等、AGENTS.md 原文保留；`validate` 与 `doctor` 在真实文档上 exit 1（类型口径不对齐，非回归） |
| 5. LXD 七个实验样式回归 | **通过** | 小字对比度 3.04 → 6.39；画布输出与基线逐字节相同；零报错 |
| 6. Skills 新会话验证步骤 | **步骤已给；另有新证据** | 本会话（会话重建后）发现、加载、执行均成功；全新会话仍待用户确认，状态保持 PARTIAL |
| 7. Git 10 笔提交同步审查 | **完成** | 无密钥模式、无大文件、可快进；推送建议见 §6 |
| 8. Program NOW 与待决清单 | **已更新** | NOW.md 重写；PD-Q9 至 PD-Q16 |

**最需要用户知道的三件事**

- 两处"修复后未复审"的小修**各只修对一半**，其中 E06 L113 的"θ2 是不是 0"漏了 180°（§1）。
- V83 的 CPU 行今天拿到了官方原文，教材与台账里"未直核"的说法已经落后于事实（§1）。
- Governance 的 `validate` / `doctor` 在真实 Engine 的文档上本来就过不了；上一轮"ENGINE 183 docs 适配实跑"留下的注册表，正是 doctor 报错的对象（§3）。

## 1. 用户验收包与专项复核（Engine）

**run 状态（实测）**：`RUN-2026-11-23-embodied-batch1` = REVIEW / paused，KCR REVIEWING，G3 open，无审批记录；23 条产物记录对应 21 个文件，哈希失效 0 个。本轮**没有推进 run、没有改动六课课文与测验、没有升级任何断言、没有填写任何分数**。

**验收包内容**（`reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`）：

- G1：V68–V87 每条给出断言内容、状态、来源、原始位置、直接证据、核验过程、来源矛盾、AI 推荐、理由、下游影响、保持 open 的后果。分类：A 类建议升级 verified 7 条（V72、V73、V75、V76、V77、V78、V81）；B 类建议 conditional 6 条（V70、V71、V74、V79、V83、V85）；C 类建议保持 open/low 7 条（V68、V69、V80、V82、V84、V86、V87）；无建议 contested；更正类 6 条需用户确认口径。
- G2：六课逐课依据 + 评分表（AI 建议分 88 / 91 / 91 / 92 / 90 / 88，均注明"不是正式评分"）。我通读了六课并重算全部算例，与课文一致。
- 专项复核、两处小修说明、11 项最小修复方案（未执行）、审批登记顺序、未解决问题。

**专项复核结论**（独立审读代理，只读）：

| 项 | 判定 |
|---|---|
| E03 三维框算例 | 成立。0.003 → 0.004488 m³、+49.60%、背景点 33.2%，设定、过程、数字一致 |
| E06 GPU 非确定性 | 基本成立。没有一句把 GPU 非确定当普适结论；小节标题按设备二分，比正文口径宽 |
| E06 L160 参考答案（小修一） | 修对一半。第 1 题指向正确；第 2 题的理由在 §1 而非指引写的 §4.2；末句"练习 1 覆盖生态四组"不属实 |
| E06 L113 忽略动作空间（小修二） | 修对一半。删掉的半句确实错了；新写的"θ2 是不是 0"漏 180°，与 E04 L127 不一致 |

**本轮新证据与新发现**：

1. **MuJoCo 官方文档 Reproducibility 节原文**（`doc/computation/index.rst`，main 分支，2026-11-25 直取）："MuJoCo's simulation pipeline is entirely deterministic and reproducible"，后接三条注意事项，与 E06 L99 逐条对应。V83 的 CPU 行由此有了官方原文。**未写入台账与教材**（它们是已登记哈希的产物），列为验收包 §6 第 4 项待批。
2. **E03 §4.5 容差算例没有任何断言覆盖**（正文 L133–141 无断言引用；V88 编号空闲）。列为 §6 第 9 项。
3. G1 队列 V83 一行把当时未直核的 CPU 行也写成"官方文档逐字"，需更正（§6 第 10 项）。

**方案选择（待用户）**：方案甲 = 先修 11 处 → 独立复核改动行 → 再评分裁决；方案乙 = 按现状裁决，登记为已知缺陷。AI 推荐甲，**未执行任何修复**。

## 2. Radar 真实数据库副本验证

**真实库现状（只读）**：`github-project-radar/radar-real-20261121.db`（389,120 字节）121 个仓库 / 200 条快照 / 1 条采集记录 / 121 条候选（120 Discovered、1 Research，`human_selected_for_research` 全为 0）；候选表**没有** approver / approved_at / approval_reason 三列，即停留在修复前的结构。`radar-real-hdr.db` 为空库。

**隔离方式**：原件备份与副本均在系统临时目录（`radar-verify/backup-20261125-195030/`、`copy-20261125-195030/`），副本初始 SHA256 与原件一致。所有写操作只对副本执行。

| 步骤 | 命令（对副本） | 退出码 | 结果 |
|---|---|---|---|
| 升级 | `init-db` | 0 | 补上三列；原有 13 列逐值不变 |
| 评分 | `analyze` | 0 | 评估 121 个仓库；非候选三张表不变；机器评分哈希与升级后相同；人工状态全部不变 |
| 复核 | `review` ×2（候选 1：Discovered → Triaged → Research） | 0 / 0 | 状态生效，研究目标写入 |
| 普通导出 | `export` | 0 | 2 条任务，`human_selected_for_research` 均为 false（既有设计：未经批准不可导入） |
| 批准导出 | `export --approved --approver TEST-ONLY-NOT-A-USER` | 0 | 2 条任务（候选 100、1）；库内两条均为 `approved_for_research`、人工选择 = 1、带批准人与时间 |
| 再评分 | `analyze` | 0 | 批准状态与其余 119 条均未变 |
| 重复批准 | `export --approved --approver TEST-ONLY-SECOND` | 0 | no-op；保留首次批准人与时间；两次导出任务集合相同 |
| 非法转换 | `review` 候选 2：Discovered → Research | 1 | `ValueError: 非法状态转换`；库无变化 |
| 空批准人 | `export --approved --approver "  "` | 2 | 拒绝 |
| 回归测试 | `py -3 -m unittest discover -s tests` | 0 | **Ran 58 tests，OK** |

**特别验证项**：Research 状态不被重置 ✓；Approved 状态不被重置 ✓；人工选择标记保留 ✓；导出审批状态一致 ✓（导出物带 `review_status` 与 `human_selected_for_research`）；重复执行幂等 ✓。数据对比：未触碰的 119 条候选在原有 13 列上 119/119 逐值相同；repositories 121 行、snapshots 200 行、collection_runs 1 行全部相同；新增三列在未触碰候选上全为空。

**限制与观察**：

- 只在副本上验证。**真实库仍是修复前的结构**，对它执行 `init-db` 是一次真实写入，需用户批准（PD-Q15）。
- 导出契约（`docs/engine-interface.md` 字段表）本来就没有 approver / approved_at，下游看不到是谁批准的。属设计观察，不是这次修复的缺陷。
- 真实库里候选 100 的历史复核人写的是"user(采纳AI推荐授权 2026-11-21)"，是 AI 写入的字符串，不是身份验证。
- 没有覆盖：`--source rest` 真实采集、`report` / `candidates` 命令、并发写入。

## 3. Governance 真实项目副本接入

**方式**：把 Engine 复制两份到系统临时目录（排除 `.git`、`node_modules`、`__pycache__`）：场景 A 不带 `.governance`（模拟首次接入），场景 B 带（模拟已有治理目录）。所有命令只对副本执行。

| 验证项 | 场景 A（首次） | 场景 B（已有） |
|---|---|---|
| `init` | exit 0；新增 `.governance/` 下 5 个文件 | exit 0；无新增文件 |
| 已有 AGENTS.md 保护 | 原文 1222 字节是改后文件的前缀 ✓；仅在末尾追加 868 字节指针块 | 同左 |
| 治理入口生成 | 三个指针路径逐一解析存在 ✓ | ✓ |
| `.governance` 内绝对路径 | 无 | 无 |
| `doctor`（inventory 之前） | exit 0（0 条目） | **exit 1** |
| `inventory` | exit 0，登记 231 个文档 | exit 0，231 个文档 |
| `doctor`（inventory 之后） | **exit 1，717 条** | **exit 1，793 条** |
| `validate` | **exit 1，860 条** | **exit 1，917 条** |
| `status` / `audit` | exit 0 / exit 0（孤儿文档一批） | 同左 |
| 重复 `init` | exit 0，"无需变更（幂等）"，变化文件 0 | 同左 |
| 原有文件被改动 / 被删除 | 仅 AGENTS.md（追加）/ 无 | AGENTS.md 与 `.governance/document-registry.json`（重新扫描）/ 无 |
| 真实 Engine 的 AGENTS.md | 哈希未变 ✓ | ✓ |

**`validate` / `doctor` 为什么不过**（要点）：

- 114 篇文档没有 frontmatter（知识文档 00–07、archive 等按 Engine 自身规范本就不带）。
- Engine 自己的文档类型不在 Governance 的 13 类枚举里：`review-material`、`agent-plan`、`kcr`、`research-report`、`knowledge`、`adapter`、`user-guide`。
- 一批注册表条目缺 owner / created_at / updated_at，146 条被登记为 `unknown`。

**需要更正的旧说法**：Engine 里**已经有** `.governance/`（5 个文件，被 git 跟踪），是 2026-11-21 那轮"真实适配实跑"写入的；其注册表 183 条里 146 条 `type=unknown` 且没有 owner。此前"真实 Engine 只做过副本验证"只对 `init` 与指针成立。

**结论**：接入动作本身安全（不破坏、幂等、指针可用），这部分通过；`validate` / `doctor` 在真实 Engine 文档上不可用，原因是两套文档规范的类型与必填字段没有映射。这不是 P0 修复的回归，也不在本轮"不新增功能"的范围内，列为待裁决（PD-Q14）。Governance 自身 41 项测试 exit 0。

**没有验证**：`handoff`、`adr`、`archive-check`、`map` 在真实副本上的表现；任务与 Agent 登记流程（两场景均为 0 task / 0 agent）。

## 4. LXD 七个实验样式回归

对当前构建重新测量七个实验（Edge 无头浏览器，三档宽度），与优化前基线、上一轮复测三方对照：

| 实验 | 小字对比度 浅色 基线/上轮/今天 | 深色 基线/上轮/今天 | 画布输出字节 基线/上轮/今天 | 阶段数值 今天=上轮 | 报错 | 横向滚动 360/768/1280 |
|---|---|---|---|---|---|---|
| transform-mvp | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 21802 / 21802 / 21802 | 是 | 0 | 无 / 无 / 无 |
| procedural-lathe | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 66366 / 66366 / 66366 | 是 | 0 | 无 / 无 / 无 |
| pbr-lighting | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 59310 / 59310 / 59310 | 是 | 0 | 无 / 无 / 无 |
| yuv-to-rgb | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 36914 / 36914 / 36914 | 是 | 0 | 无 / 无 / 无 |
| pts-dts-timeline | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 37982 / 37982 / 37982 | 是 | 0 | 无 / 无 / 无 |
| frame-pipeline | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 34210 / 34210 / 34210 | 是 | 0 | 无 / 无 / 无 |
| rendergraph-dag | 3.04 / 6.39 / 6.39 | 4.63 / 7.76 / 7.76 | 33846 / 33846 / 33846 | 是 | 0 | 无 / 无 / 无 |

公共样式修复（对比度、动手任务复选框关联文字）对七个实验全部生效；"实验目标 / 观察记录 / 键盘提示"只在 MVP 试点页，与其余六个无关，符合设计。全部对比度键在上一轮与今天之间无差异。证据存入 Engine `.agent/skills/learning-experience-design/preview/lab-mvp/regress-20261125.json` 与 `regress-compare-20261125.txt`。

没有做的：没有重新截图做视觉审查；360 宽度下代码块与公式元素的溢出元素列表与基线在个别实验上不同，但均未造成整页横向滚动。

## 5. Skills

**安装**：`handoff`、`writing-for-agents` 仍在用户级技能目录，已安装的 `SKILL.md` 与仓库源文件（`skills/productivity/<技能名>/SKILL.md`）SHA256 一致。本轮未重新安装。

**新证据（本会话，会话重建后）**：

| 技能 | 发现（技能检索） | 调用（宿主技能加载） | 执行 |
|---|---|---|---|
| `handoff` | 成功，第一个候选 | 成功 | 成功：交接文档写到系统临时目录，含 "Suggested skills"，不含敏感信息 |
| `writing-for-agents` | 成功，第一个候选 | 成功 | 成功（夹具）：在工作区外的临时 `AGENTS.md` 上按规则改写并通过确定性检查 |

本会话开头这两个技能检索与加载都失败；中间经历了一次会话重建。上一轮"新会话才能用"的结论修正为"会话重建或新会话后可用"。记录已补入 Skills 仓 `docs/HOST-VERIFICATION-2026-11-25.md` §8 与 `docs/USER-GUIDE.md` 的宿主证据表。

**状态仍是 PARTIAL**：全新会话没有测；`handoff` 是使用者点名要求验证后才加载的，没有测试模型是否会自行调用它。确认步骤见 Engine 验收包同级的说明与 Skills 仓该文件 §6：新开一个会话，说"用 handoff 技能给当前对话写一份交接文档"，观察检索、加载与产出位置。

## 6. Git 同步审查

| 仓 | 待推送 | 规模 | 敏感扫描 | 可快进 | 未提交 |
|---|---|---|---|---|---|
| Engine | 9 笔（`65dca1d..9923708`） | 61 个文件，+9010 / −502 | 无密钥模式；11 处新增行为本机路径（文档内，含用户名） | 落后 0（按上次 fetch） | 5 项（见下） |
| Skills | 1 笔（`9ac74ea`） | 2 个文件，+84 / −5 | 同上 | 落后 0 | 2 项（本轮的验证记录更新） |
| Program / Governance / Radar | 无远程 | — | — | — | Program 本轮改动若干；另两仓干净 |

- Engine 未提交 5 项：`.agent/indexes/document-registry.json`（新增两份审读文档后重建）、`USER-ACCEPTANCE-PACKAGE.md`、`targeted-recheck.md`、两份实验回归证据。全部是本轮产物。
- `stash@{0}` 原样。
- 最大文件 `web/content.js` 3.2 MB，是已跟踪的生成物，不是新的大文件。
- **内容边界**：Engine 的 GitHub 仓库是 **Public**（未登录可见），`reviews/`、`.agent/`、`.governance/`、`.workbuddy-ai/`、DECISIONS / CHANGELOG / WORKFLOW_STATE 都已公开。学习站的发布边界（v2）管的是站点包，不管 git 仓库。这是既有状态，不是本轮引入；是否调整列为待裁决（PD-Q16）。

**推送建议（未执行，等授权）**：

1. 先提交本轮产物（Engine 一笔"验收准备材料 + 实验回归证据"；Skills 一笔"宿主验证补充记录"；Program 一笔"稳定化验证报告与统筹层同步"），避免推上去的版本与本地不一致。
2. 推送前 `git fetch` 复核远端未动，再做普通 push。Engine 与 Skills 都需要单次代理参数：`git -c http.proxy=http://127.0.0.1:10808 push origin <分支>`。
3. 不 force、不改写历史。也可以等六课裁决完成后再推，代价是这些成果只在本机。

## 7. 待裁决事项

已列入 `decisions/PENDING_DECISIONS.md` 的 PD-Q9 至 PD-Q16，每项含背景、影响、推荐方案、不处理的后果、是否阻塞当前课程发布。本轮没有批准其中任何一项。

## 8. 本报告没有核实的

- Robot_Learn 源文的行号定位（除上一轮已打开的几处）。
- Tobin 2017 与 DAgger 2011 的论文全文；依据的是上一窗口对官方摘要的核对。
- 学习站六课页面在浏览器里的实际显示（本轮只跑了静态门禁，validate 20 / 0 / 0）。
- 全新会话里的技能表现。
- Radar 与 Governance 在真实对象上的任何写入。

## 9. 证据位置

- Engine：`reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`、`targeted-recheck.md`、`.agent/skills/learning-experience-design/preview/lab-mvp/regress-*`
- Skills：`docs/HOST-VERIFICATION-2026-11-25.md` §8
- 临时目录中的原始日志（系统可能清理）：Radar `radar-verify/copy-20261125-195030/verify-log.txt`、`verify-log-2.txt`；Governance `gov-verify-20261125-195318/log.txt`、`log-counts.txt`；Git `git-review.txt`

## 10. 追加：方案甲修复执行记录（2026-11-25 22:35，用户批准）

本节晚于 §0–§9。用户选定方案甲后，验收包 §6 的 11 项最小修复已执行：

- **课文与测验**：E06 L113（"θ2 是不是 0" → "0° 或 180°"；"所以" → "换句话说"）、L160（答案指向与覆盖范围说明）、L90（小节标题）、L22 / L92 / L96 / L164（CPU 行出处）；E06 测验第 3 题答案。
- **证据层**：V83 的 claim、evidence、conditions 更新（**状态仍为 open / low**）；新登记 **V88**（E03 §4.5 容差三笔账，open / low）；来源注册表新增 1 条；术语表与课程契约同步。
- **审读材料**：G1 队列更正 V83 行并扩为 V68–V88；独立审读记录更新复审状态。
- **独立复核**（Engine `reviews/embodied-batch1/recheck-planA-fixes.md`）：9 项改动全部修对，无新的事实错误；6 处收尾问题 5 处已处理、1 处判定无需改。
- **run**：仍 REVIEW / paused，G3 open，无审批记录；10 个产物重新登记哈希，24 个文件哈希全部有效。
- **门禁**：validate 20 / 0 / 0；发布回归 32 项；105 条断言（24 / 74 / 7）误标 0；两门课程衔接 0 FAIL；三套自测 25 / 16 / 15；六课 Floor 全过。

§1 中"方案选择（待用户）"一项至此关闭；§0 结论表第 1、2 行的描述是修复前的状态，以本节为准。全部改动**未提交、未推送**。
