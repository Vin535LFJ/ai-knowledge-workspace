---
doc_id: G2-L02-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第一篇 L02《时间戳与同步》深化

> **AI 不自评、G2 人工评分待填**：本材料由留痕 Agent 依据执行会话实测数据整理，仅供 G2 人工审核使用。第 5 节人工判定栏全部留空，生成 Agent 不得在此填写「通过」或任何分数。
> 对应续跑点：pilot 路线 L01→**L02**→L06→L11→L13；深化基准 = Gold Standard L01（B4 裁决认可）+ `.agent/skills/research-to-learning/references/lesson-quality-standard.md`。
> 权威口径：`WORKFLOW_STATE.md`（续跑点）/ `CHANGELOG.md` 2026-11-20 P7.2 条目 / `DECISIONS.md`。

## 1. 深化说明（执行摘要）

改动文件 ×2，**frontmatter 一字未动**（任务禁令「不碰任何 frontmatter 字段值」）：

| 文件 | 变化 |
|---|---|
| `courses/video-rendering-journey/lessons/L02-时间戳与同步.md` | 125 → **217 行**（本留痕会话 `wc -l` 复核实测 217）；正文按「直观→原理→数学→架构→实践」递进重构 |
| `courses/video-rendering-journey/quizzes/L02.json` | Q1/Q2/Q4 prompt 与两层 course.json checkpoint **逐字一致**保持；四题参考答案补依据与锚点；新增 Q5（-bf 0 边界，挂 V03）与 Q6（外部主时钟场景，挂 V10）；claim_ids 全部 ⊆ frontmatter claims |

正文深化十一点：

1. **开篇钩子**：补数字张力（PTS=2 的帧排在解码第 3 位、30fps 帧位 33.3ms、2 小时视频 216,000 帧）与三问题预告。
2. **前置节**：补 I/P/B 帧与 GOP 一句话解释（针对诊断「新概念不突现」）；DTS/PTS 定义改用主文档 §4.1 ✅段原文口径。
3. **直观认识**：保留流水线/队列类比并新增电影院类比，均附边界声明。
4. **§4.1**：依赖链推导 + 双时间线 ASCII 图 + 五帧表逐行注解（每帧为什么这样排）+ 重排序缓冲机制（lab selfTest 口径）+ -bf 0 边界。
5. **§4.2**：新增三种主时钟对照表（修复诊断 D-L02-5：视频/外部时钟策略缺漏）；V10 论证「人耳对音频中断最敏感」并如实注明市场占比无公开统计。
6. **§4.3**：Δt 公式三件套（符号含义→数值算例 +10ms/-50ms→工程后果）；丢帧阈值为工程参数不代拟数字；多路晶振漂移数字保留[测试数据-仅供参考]标记；PLL ±0.1% 保留⚠️有条件成立。
7. **§4.4**：精准 seek 三步 + seek 区间示意图 + 关键辨析（追赶期在丢陈旧帧 vs 目标首帧不被误丢、recover 非官方状态名）+ 代价边界（V15 conditions），全部挂 V15。
8. **§5**：新增「解码名次−显示名次」启动缓冲下界推导及 30fps≈33ms 算例（纯由 ✅五帧表算术推出，标注保守下界与硬解边界）。
9. **§6**：两个可复述排查现场（多路越播越歪→晶振漂移/PLL；seek 差半口→默认 seek 止步定位）+ 两处机制复用案例（倒放 Jitter Buffer/全 I 帧预转码=解码与播放链路 §8.2 挑战 2、硬解回退复用静默追赶=§8.4）+ 6 条误区（新增「B 帧画质救星/杀手」不下超源结论）。
10. **§7**：实验按 labs.json 四个 tasks 给「做什么→预期看到→对应机制」并声明实验边界。
11. **桥句**：保留 L06（与 pilot course.json next 一致）。

## 2. 断言与台账（newClaims = []）

- **未新增台账断言**；`evidence/claim-ledger.json` 与 `evidence/source-registry.json` 均未改动。
- **原因（机制性）**：`tools/validate_site.py` §8 要求每条断言的每个 evidence source_id 同步登记进 source-registry.json 的 used_by_claims 反向索引，而本轮任务仅允许追加 claim-ledger.json、禁止改 source-registry.json——新增任何断言（如重排序缓冲深度、倒放方案、回退状态机复用，可按 **V21** 起顺延登记）都会导致门禁 FAIL。
- 本次正文所有重要结论均由既有断言 **V03 / V10 / V15 / V16** 或主文档 ✅/⚠️ 锚点覆盖，无需新断言。
- 若后续要登记：需按 `evidence-and-claims.md` 程序同时编辑两个 evidence 文件（G1 关口）。

## 3. 审读员结论与遗留问题

**审读结论：acceptable = true；修订 0 轮。** 遗留问题 7 条（major 1 + minor 6），全部保留原文口径如下。

### 3.1 major（1 条）

| # | 位置 | 问题 | 修法方向 |
|---|---|---|---|
| M1 | `tools/labs.json` pts-dts-timeline stages「同步约束」desc + `web/assets/app.js:2350`（L02 frontmatter lab 绑定实验，L02:184 引用） | 实验界面同屏渲染静态句「DTS ≤ PTS 恒成立」（app.js:2350）与逐帧计数「PTS−DTS = −1」（lab 模型 B0 dts=2>pts=1，app.js:2146 frames），并与 L02:72-78 五帧表（B: PTS 2/DTS 3）冲突——L02 §7 任务 3 让学习者查看 PTS−DTS 时必然撞见矛盾 | 改 stage 文案为「解码完成时刻先于显示时刻（启动缓冲补偿序位差）」或删句，并同步 labs.json 与 app.js 两处文案 |

> **M1 执行补记（2026-11-20，用户采纳推荐后执行；审读原文不改写）**：两处文案已改为与课文任务 3 口径一致——labs.json「同步约束」desc =「I/P 帧 PTS ≥ DTS（提前解出等显示），B 帧 PTS < DTS（等参考帧）；音频通常是主时钟」；app.js stage 值 =「I/P 帧 PTS ≥ DTS · B 帧 PTS < DTS」。连带修复符号 bug：tlDelta 原硬编码 "+" 前缀使 B 帧显示 "+-1"，改为按正负号格式化。重建 content.js 后 Edge headless 双路 QA（http://localhost:8765 与 file://）实测：stage5/stage6 新文案渲染正确、tlDelta=-1（默认指针 B1）、旧句清零。其余 6 条 minor 与 openQuestions 仍待 G2 人工处置，未动。

### 3.2 minor（6 条）

| # | 位置 | 问题 | 修法方向 |
|---|---|---|---|
| m1 | L02-时间戳与同步.md:130 | 「MediaCodec 亦可用 BUFFER_FLAG_DECODE_ONLY 标记」无版本限定：平台 MediaCodec 该公开标记自 API 35（Android 15）才有，Media3 早期为内部常量 C.BUFFER_FLAG_DECODE_ONLY 经 MediaCodecAdapter 传递（已在线核验），且该细节不在 V15 已列 evidence（SRC-MEDIA3-SEEK 页与 repo §8.2 均无此词），仅见于台账 note | 括注「平台 API 35+；Media3 内部常量」或删去只保留 releaseOutputBuffer(index,false) |
| m2 | L02-时间戳与同步.md:215（§11） | 声称 8 个本章术语「权威定义在 tools/glossary.json」，但 drift/重排序缓冲/GOP/精准 Seek 四词不在 glossary.json（124 词逐一名单核对，仅 PTS/DTS/主时钟/AV Sync 在） | 改写为仅列 glossary 实有的四词、其余注明见正文 §4.1/§5，或补录术语卡 |
| m3 | L02 frontmatter:6-9 vs tools/course.json 与 courses/video-rendering-journey/course.json 的 L02.objectives | objectives 第 1/2 条与两层 course.json 措辞漂移（frontmatter「画出 B 帧场景中 DTS 与 PTS 的顺序差异/解释为什么音视频同步常以音频时钟为主」vs course.json「区分 DTS 的解码顺序与 PTS 的显示顺序/说明为什么音频常被选为主时钟」，第 3 条逐字一致；Gold L01 frontmatter 与两层 objectives 逐字一致）；语义等价不误导 | 三层统一措辞（本轮任务禁令「不碰任何 frontmatter 字段值」未对齐，需人工一行改写；G-D3 遗留） |
| m4 | L02-时间戳与同步.md:117,129（另 92 单调时钟） | V-Sync、ppm、解封装器（demuxer）首次出现无一句话解释或术语链接（V-Sync 在 glossary 有 VSync 卡可链），D4 边缘缺口 | 各补一句白话或链 glossary |
| m5 | L02-时间戳与同步.md:96 | 主文档标注 [AI-生成] 的「ExoPlayer、IjkPlayer、VLC 默认采用音频主时钟」以陈述句呈现，仅靠句尾括注「主文档 [AI-生成] 段口径」披露来源（虽拒给百分比），标准 §5 要求该类内容不得写成确定事实 | 改为「主文档（[AI-生成] 标注）指出……」句式使标注前置 |
| m6 | evidence/claim-ledger.json V15.evidence[0].locator | locator 写「Why is seeking slow」，Media3 troubleshooting 实际标题为「Why is seeking in my video slow?」（内容已在线核验存在：「decoded and immediately discarded (without being shown on the screen)」） | 对齐标题，避免后续 G1 人工核验时错位 |

### 3.3 开放问题（openQuestions，5 条）

1. **未新增台账断言的机制原因**：见 §2；validate_site.py §8 的 source-registry 反向索引要求与本轮「禁止改 source-registry.json」禁令互斥。
2. **frontmatter objectives 三层措辞漂移**（= m3，诊断 G-D3 遗留）：语义兼容、正文已同时覆盖两者，按任务禁令未对齐 frontmatter。
3. **Media3/ExoPlayer 细节口径**：BUFFER_FLAG_DECODE_ONLY、renderedFirstFrameAfterReset、官方状态仅 IDLE/BUFFERING/READY/ENDED 沿用 V15（open/low）登记时核验的口径，正文 §4.4 与 §11 已如实标注其状态，待 G1 升级 V15/V16。
4. **glossary.json AV Sync 词条**：仍写「seek 后还要进入 recover 状态」，与 V15 conditions「recover 非 ExoPlayer 官方状态名」口径不一致；glossary.json 不在本次允许改动范围内，建议人工软化该词条措辞。
5. **quiz 新增 Q5/Q6 题量**：若 G2 认为题量超纲可删，删除后三个 checkpoint 的覆盖检查仍由 Q1/Q2/Q4 满足（validate 已验证）。

## 4. 门禁实测（执行会话，全 exit 0）

| 门禁 | 实测输出 |
|---|---|
| build_site（`py -3 tools/build_site.py`） | Wrote web\content.js——**69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards generated / 2459 KB** |
| validate_site（`py -3 tools/validate_site.py`） | **validate_site: 11 checks passed, 0 warnings, 0 failures**（含全部链接/锚点解析与 quiz/checkpoint/claim 覆盖检查） |
| check_chapter_arc（`py -3 .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py`） | **5 篇 · 全 OK** |
| review_gate（`py -3 tools/review_gate.py`，只读） | conditional/contested 被标为 verified 的 claim：**无**；未挂载任何课程的 claim（open/conditional 可预期）：**['P03']** |
| test_publish_boundary（`py -3 tools/test_publish_boundary.py`） | exit 0 |

> 注：以上为执行会话实测数据（由执行方提供、留痕会话如实回填，未复跑）；本留痕会话另做的只读复核 = `wc -l` L02 教材 217 行、grep 抽核 m1/m5/m2 锚点行号（130/96/215 行内容与审读描述一致）。本机 `python` 解析到 cygwin stub，门禁一律 `py -3`（D11.10）。

## 5. G2 人工判定（待填——AI 不自评）

| 项 | 待人工填写 |
|---|---|
| G2 对本篇深化的判定（通过 / 有条件通过 / 退回修订） | |
| 评分（如需，参照 review-report.md 维度体系） | |
| 对遗留 7 条的处置（逐条指派：改 labs.json+app.js / 改 frontmatter / 改 glossary / 删 Q5Q6 / 其他） | |
| 对 openQuestions 5 条的意见 | |
| 备注 | |

## 6. 边界与材料来源

- 本材料由 P7.2-L02 留痕 Agent 新建（追加式治理留痕）；一律**未 commit/push**；未改写任何历史条目。
- 依据的实测输入：执行会话深化摘要（含 newClaims/openQuestions）、审读员结论（acceptable=true、0 修订轮、遗留 7 条）、五道门禁实测输出。
- 未复跑门禁（见 §4 注）；未改 claim-ledger.json / source-registry.json / glossary.json / L02 任何文件。
- 关联材料：`reviews/G2-curriculum-review.md`（课程大纲审核）、`courses/video-rendering-journey/review-report.md`（整站人工评分表，仍待人工）、`courses/video-rendering-journey/教材质量诊断.md`（L02 深化前的诊断基线）。
