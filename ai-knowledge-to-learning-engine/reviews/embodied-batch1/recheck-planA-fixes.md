---
doc_id: EMB-B1-PLANA-RECHECK
type: review-material
status: active
owner: independent-readonly-reviewer
created: 2026-11-25
updated: 2026-11-25
---

> 归档说明（执行方添加；正文自下一行起为独立审读代理原样输出，未改写）。审读员指出的 6 处收尾问题，处置如下：
> 1. V88 的 locator 章节号写错 → **已改**为"§6.3 L526–529（三笔账）/§6 L487（小结）"。
> 2. 5 个已登记哈希的产物被改动、run 记录与 CHANGELOG 未更新 → **已处理**：用 `run_state.py artifact` 重新登记，CHANGELOG 追加本轮条目（见该文件 2026-11-25"方案甲"条目）。
> 3. V83 条件第一条仍写"以官方 FAQ 直核为准" → **已改**为 CPU 行以官方文档、GPU 行以 FAQ 为准。
> 4. "逐位可复现"措辞 → 审读员判定不构成错误，**保留未改**。
> 5. 课源 `06` 的 frontmatter `updated` → **已改**为 2026-11-25。
> 6. E06 L164 对 GPU 行取文日期的表述 → **已统一**为"2026-11-24 取文、2026-11-25 复核"。
> 范围外告知的两项：课程 README L33 的断言范围 → **已改**为 V68–V88；来源注册表两处既有双向不一致（`SRC-BASIS-UNIVERSAL` / `SRC-RN-CONCEPT-INTRO`）与 Embodied 批次无关，**未处理**，待排期。审读员对第 2 项定级为 major（流程留痕），不是教材内容问题。

# 独立教材复核报告（方案甲修复 · 针对性复核 · 只读）

复核日期：2026-11-25 22:30（+08:00）
范围：只核对任务书列出的 9 项改动点及其波及一致性，不做全面审读。
手段：`git diff` / `git show HEAD:`（只读）、逐行阅读、`py -3` 脚本（`planA_recheck.py`、`planA_hashes.py`，位于 `C:\Users\Giant\AppData\Local\Temp\qwenwork\`）、直取 MuJoCo 官方文档 `doc/computation/index.rst`（main 分支，2026-11-25 取文）与 Robot_Learn `textbook-embodied.md` L482–533。
纪律：未修改仓库任何文件；未运行 `build_document_registry.py` / `build_site.py`；未执行改变 git 状态的命令；没有任何文件写入 `C:\Users\Giant\Desktop\`。

## 一、逐项判定表

| 项 | 判定 | 行号 | 依据 |
|---|---|---|---|
| 1. E06 §4.4 括注含 0° 与 180°，与 E04 一致，"所以"不再是因果推断 | **修对了** | E06 L113；E04 L127、L79 | E06 L113 现为"是否奇异只看关节角（θ2 是不是 0° 或 180°），换句话说，'用哪种量当动作'不是记法问题"。E04 L127 为"θ2 = 0° 或 180° → detJ = 0"，两处一致。独立重算：detJ = L1·L2·sinθ2（L1 = 0.4，L2 = 0.3）；θ2 = 180°、θ1 = 0 时 J = [[0, 0], [0.1, −0.3]]，det = 1.5e−17 ≈ 0，秩为 1，确实奇异；θ1 = 30°/37°、θ2 = 180° 时 det 同样为 0（|det| < 3e−17）；在 θ1 ∈ [0°, 360°)、θ2 ∈ [−180°, 180°) 网格上，数值 det 与闭式 L1·L2·sinθ2 的最大偏差 1.6e−16，即与 θ1 无关。顺带复算 E04 L142–144 表中 detJ：5° → 0.0105、45° → 0.0849、90° → 0.12，吻合。"所以"已改为"换句话说"，不再是从单射/奇异推出"动作表示不兼容"的因果链。 |
| 2. E06 §7 参考答案章节指向 | **修对了** | E06 L160；L30–32、L79–80、L109、L113、L132–135 | 第 1 题："§4.4 第一组"对应 L109"只看演示视频"、L113 的逐条对应；"代替演示视频的是可重复的成功率（§4.2 第 4 周验收标准）"对应 L80。第 2 题："见 §1 与 §4.2 第 0 周验收标准"——理由"不能复现的成功无法证明是能力而不是运气"在 L32（L30 给出路线），第 0 周验收在 L79。第 3 题："§4.3 与其后'证据的边界'"对应 L90–99 与 L101。末句"起步三件由练习 1 覆盖；生态四组没有练习或自测题覆盖"属实：练习 1（L132–135）问的是第一周装哪三件及何时加 GPU 仿真器，预期"ROS 2 + MuJoCo + LeRobot"；练习 2–4（L137–150）与自测三题（L156–158）均不涉及 A–D 四组。 |
| 3. E06 §4.3 小节标题 | **修对了** | E06 L90；L92 | 标题改为"可复现性分层：先问设备，再问物理后端"，与 L92"在哪种设备上、用哪个物理后端？"口径一致，不再按设备二分。 |
| 4. V83 CPU 行出处全部改为官方文档且相互一致 | **修对了**（有 1 处措辞残留，见问题 3） | E06 L22、L92、L96、L164；E06.json L28；课源 `06` L12、L44、L65；台账 L2713、L2732–2734、L2743；术语表 L1675；来源注册表 L638–646 | 逐处核对：① E06 L22"CPU 一行经 MuJoCo 官方文档 Reproducibility 节逐字核验（2026-11-25）"；② L92 同；③ L96 表格 CPU 行"（MuJoCo 官方文档 Reproducibility 节，2026-11-25 核对原文）"；④ L164"CPU 一行有 MuJoCo 官方文档 Reproducibility 节支持"；⑤ E06.json L28"据官方文档 Reproducibility 节为逐位可复现"；⑥ 课源 L12、L44（逐字引文）、L65（外部核验行）；⑦ 台账 V83 claim、新增 evidence 条目、conditions 第二条；⑧ 术语表 L1675"MuJoCo 可以逐位重跑（MuJoCo 官方文档 Reproducibility 节）"。以上均不再写"依据课源转述 / 未直核官方文档"。全文检索"课源转述 / 未直核"：教学材料、台账、术语表、课源、G1 队列中 **0 处**残留；剩余命中只在 CHANGELOG L12、L53 与 `reviews/embodied-batch1/` 的历史记录（g2-diagnostic、recheck-after-fix、USER-ACCEPTANCE-PACKAGE、independent-review、targeted-recheck）。直取官方原文核对：课源 L44 与 G1 L22 的引文"MuJoCo's simulation pipeline is entirely deterministic and reproducible -- if a state in a trajectory is saved and reloaded and mj_step called again, the resulting next state will be identical."与 main 分支原文逐字一致（去掉 rst 的 `:ref:` 标记后）；原文三条注意事项与课源 L44、E06 L99 逐条对应；锚点 `piReproducibility` 存在。来源注册表新增 `SRC-EXT-MUJOCO-REPRODUCIBILITY`（L638–646，type official_doc，accessed 2026-11-25，used_by_claims [V83]），台账 V83 evidence 引用了它（L2732）；注册表与台账双向一致。 |
| 5. 课源 `06` "关联断言"列全 | **修对了** | 课源 `06` L66 | 现为 V82、V83、V86、V87 四条，与 E06 frontmatter（L15）逐项相同。 |
| 6. V88 数字与挂接 | **数字全部修对；挂接齐全；locator 章节号有 1 处错（见问题 1）** | 台账 L2870–2895（locator 在 L2876）；E03 L15、L135、L139–141、L192；course.json L171；来源注册表 L527；Robot_Learn L487、L526–529 | 独立重算：0.22×0.17×0.12 = **0.004488 m³**；原体积 0.003；增幅 0.004488/0.003 − 1 = **49.60%**；背景占比 1 − 0.003/0.004488 = 33.155% → **33.2%**；0.20×sin10° = 34.730 mm → **34.7 mm**；2.5/10 = **25%**；要压到 5% 粒度 = 10×0.05×2 = **1 N**（粒度 1 N 时 0.5/10 = 5%）。全部与 V88 claim、E03 L139–141、源文一致。V88 是台账最后一条（台账共 105 条，无重复 id），status open / confidence low。挂接核对：E03 frontmatter claims（L15）✓；course.json E03 claims（L171）✓；台账 used_by_lessons = [E03] ✓；E03 §4.5 正文（L135"断言 `V88`"）✓；E03 §8 边界说明（L192）✓；来源注册表 `SRC-RL-TEXTBOOK`.used_by_claims 含 V88（L527）✓。打开 Robot_Learn 原文：L487 是第 6 章"三条关键结论"第 1 条（容差写成数字，含 49.6%、33.2%、34.7 毫米）；L526 框体积账、L527 朝向账、L528 力值粒度账、L529 共同读法。**但这两处都在第 6 章（L484 起），三笔账在 §6.3（L520）；台账 locator 写的是"§5 L526–529（三笔账）/L487（小结）"，行号对，章节号错**——台账其余 locator（§5 L421–445、§7 L647、§8 L683、§10 L876）都与原文章节号吻合，可见是这一条写错。另：V88 条件里"每边放宽 10 毫米"的歧义登记（勘误队列 #14，G1 L65）与源文 L526 一致。 |
| 7. G1 队列 | **修对了**（"105 claims 误标 0"未复跑，见未核实） | G1 L10、L12、L22、L47、L52、L72–73 | 标题 L10"G1 核验队列 · embodied-loop-journey 首批（V68–V88）"；说明 L12"全部 21 条已登记 open/low…review_gate 105 claims 误标 0"；§2 表格实数 21 行（V68–V88，脚本逐行计数）；V83 行（L47）依据栏现为"GPU 行 MJWarp 官方 FAQ 逐字（2026-11-24）；CPU 行 MuJoCo 官方文档 Reproducibility 节逐字（2026-11-25）"，两行各有出处与日期；新增 V88 行（L52）；§4 裁决栏 L72"V68–V88 \| \| \| \|"、L73 仅有原有的"（反馈 / 不反馈）"提示，裁决人、日期两列全空，**没有被代填**。台账 V68–V88 共 21 条全部 open/low，与说明一致。 |
| 8. 一致性总检 | **通过** | E03 L15；E06 L15；course.json L171 及 E06 段；E06 L156–158；E06.json L8/L18/L27 | E03 frontmatter [V71, V72, V73, V74, V88] 与 course.json 逐项、逐序相同；E06 frontmatter [V82, V83, V86, V87] 与 course.json 相同。正文 V 编号：E03 正文出现 V71–V74、V88，⊆ frontmatter；E06 正文出现 V82、V83、V86、V87，⊆ frontmatter。E06.json 三题 claim_ids ⊆ E06 claims。台账中 used_by_lessons 含 E03 / E06 的断言集合与两课 frontmatter 完全相等。E06 自测三题（L156–158）与 course.json checkpoint（L318–320）、E06.json 前三题题干（L8、L18、L27）逐字相同；与 HEAD 版本比对，三处题干本轮均未改动（E06.json 只改了 L28 答案）。 |
| 9. 是否引入新的事实错误或内部矛盾 | **未发现新的事实错误；"逐位"一词有官方原文支撑，属可接受的加粗表述**（另有 1 处留痕问题，见问题 2） | E06 L96、L99；课源 `06` L44；官方原文 Reproducibility 节 | 官方原文："MuJoCo's simulation pipeline is entirely deterministic and reproducible -- if a state in a trajectory is saved and reloaded and mj_step called again, the resulting next state will be identical." 并在第一条注意事项里写 warmstart accelerations "should be saved if **bit-wise equality** is required"。因此"逐位可复现，附三个警告"且第一条警告就是"保存全部积分状态（否则 warmstart 不同）"，与原文的条件结构一致，不是无依据的加码。"Exact reproducibility is only guaranteed within a single version, on the same architecture"对应 E06 的"同版本、同架构"。更贴原文的写法是"可精确重放（identical / bit-wise equality）"，但现表述不构成错误，见问题 4。其余新改文字（L90、L113、L160、L164、课源 L12/L44/L65/L66、E06.json L28、术语表 L1675、台账两条、G1 三处）逐句与来源或正文其他位置对照，未发现互相矛盾。 |

## 二、发现的问题清单

教学正文、测验、术语表层面：**无 blocker，无 major**。

| 级别 | 位置 | 问题 | 最小修复建议 |
|---|---|---|---|
| minor | `evidence/claim-ledger.json` L2876（V88 locator） | "§5 L526–529（三笔账）/L487（小结）"——行号正确，但 L484–579 是 textbook **第 6 章**（具身标注与质检），三笔账在 **§6.3**（L520）；第 5 章是"时空对齐与标定"（L387–483）。同库其余 locator 的章节号都与原文吻合，仅此条写错。 | 改为"§6.3 L526–529（三笔账）/§6 L487（小结）" |
| major（流程留痕，非教材内容） | `.agent/runs/RUN-2026-11-23-embodied-batch1.json`；`CHANGELOG.md` L9、L12、L13、L17 | 本轮改动了 5 个已登记哈希的产物，run 记录未更新（updated_at 仍为 2026-11-25 18:41）：按登记的 sha256 逐个重算，23 条登记中 7 条失效（G1 队列、course.json 各登记两次，E03、E06、E06.json 各一次；其余 16 条吻合）。同时 CHANGELOG 没有本轮修复的记录：L12 仍写"尚未同步"，L13 仍写"建议登记 V88，待批"，L17 仍写"没有执行 11 项修复"，L9 仍写"哈希失效 0 个"——这四句现在都不成立。 | 由人决定：在 CHANGELOG 追加一条本轮修复记录（改了哪些文件、V88 已登记、V83 CPU 行出处已同步、裁决栏仍空），并用现有 runstate / 审批链工具重新登记这 5 个产物的哈希。 |
| minor | `evidence/claim-ledger.json` L2742（V83 conditions 第一条） | "CPU 确定性限同版本同架构；…Engine 以官方 FAQ 直核为准"——CPU 行现在依据的是官方文档 Reproducibility 节，不是 FAQ（FAQ 是 GPU 行）。第二条已写对，第一条没同步。 | 改为"CPU 一行以官方文档 Reproducibility 节直核为准，GPU 一行以官方 FAQ 直核为准" |
| minor（措辞，可不改） | E06 L96、L99；E06.json L28；术语表 L1675 | "逐位可复现"比原文的"next state will be identical"略强：原文只在"保存 warmstart 加速度"的条件下才用"bit-wise equality"一词。E06 L96/L99 把该条件放在同一句的警告里，读者不会误解，但"逐位"单独看像无条件承诺。 | 可选：L96 改为"可精确重放（保存全部积分状态时逐位相同）"；不改也不构成错误。 |
| minor | `08-具身智能/06-开源生态与实践路径.md` L7 | frontmatter `updated: 2026-11-24`，但 L12、L44、L65、L66 在 2026-11-25 有实质修改（新增官方引文与取文日期）。 | `updated` 改为 2026-11-25 |
| minor | E06 L164 对比台账 L2743、课源 `06` L12 | E06 L164 写"两处原文均于 2026-11-25 核对"；台账与课源写 GPU 行取文日期 2026-11-24。不矛盾（GPU 行在 11-24 首次取文，11-25 由独立审读再次直取核对，见 targeted-recheck.md L35），但三处对 GPU 行的日期表述不统一。 | 可选：E06 L164 改为"GPU 一行 2026-11-24 取文、2026-11-25 复核，CPU 一行 2026-11-25 取文" |

范围外、本轮之前已存在、未因本轮改动而变化的（仅告知，不计入本轮修复评价）：

- `courses/embodied-loop-journey/README.md` L33 写"V68–V85 在写作时全部为 open/low"，现在应为 V68–V88；同文件 L34"可复现性分层（MuJoCo 官方文档）另有外部来源核验"在本轮之后变为属实（上一轮建议收窄，本轮走的是另一条路：把出处补齐）。
- 来源注册表与台账的双向对照有两处既有不一致：`SRC-BASIS-UNIVERSAL` 的 used_by_claims 含 V08，但 V08 的 evidence 未指向它；`SRC-RN-CONCEPT-INTRO` 的 used_by_claims 写的是"E04"（课时，不是断言）。与 Embodied 批次无关。
- E03 L139 的"33.2% 是背景点"隐含"点在框内均匀分布"，课文未写；该假设只登记在台账 V88 conditions（L2886）。上一轮已指出，本轮不在修复清单内，未改。
- `reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md` L440、L470、L472 仍描述"课源转述、未直核"的旧状态；它是给用户的验收快照，若仍作为裁决材料使用，需要加一句"§6 第 4–10 项已于 2026-11-25 修复"。

## 三、没有核实的内容

- **未运行** `build_document_registry.py` / `build_site.py` / review_gate / validate / runstate 任何工具，所以 G1 L12 的"review_gate 105 claims 误标 0"没有复跑；我只确认了台账实际为 105 条、V68–V88 共 21 条全部 open/low。
- 生成物与源是否同步只做了间接检查：`web/content.js`（22:24:46）与 `.agent/indexes/document-registry.json`（22:24:44）的修改时间晚于最后一次源文件修改（22:24:18），且 content.js 中能检出本轮新句子（"先问设备，再问物理后端""θ2 是不是 0° 或 180°""起步三件由练习 1 覆盖"各 2 处），检不出"课源转述"（0 处）。没有在浏览器里打开任何页面。
- MuJoCo 官方文档取自 **main 分支的活文档**，没有对应的版本号或提交哈希；课文、课源、台账里"2026-11-25 取文"的日期属实，但"哪个发布版本包含这段话"未核。
- MJWarp 官方 FAQ（GPU 行）、PR #1422 原文本轮未重新取文核对（GPU 行的措辞本轮未改）。
- Robot_Learn 只打开了 `textbook-embodied.md` L482–533 并检索了全文章节标题；`kb:5.7.2`、`kb:5.15.8` 等被转引的底层块未打开。V82、V86、V87 的源文一致性本轮未核（不在清单内）。
- 哈希核对用的是文件原始字节的 SHA-256，与 run 记录登记值直接比对；未核对登记时是否对换行做过规范化（未改动的 16 条全部吻合，说明比对方法与登记方法一致）。
- 是否已获用户批准执行这批修复（"方案甲"）、是否应重新登记哈希，属人工裁决事项，我没有查 DECISIONS.md 与审批记录，不作判断。
- 课文内 Markdown 锚点链接是否有效未验证。
