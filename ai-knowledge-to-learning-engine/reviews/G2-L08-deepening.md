---
doc_id: G2-L08-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第九篇 L08《一帧怎么画出来》新写教材（2026-11-20，「其余篇目」第五篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写），独立子代理审读（只读换人、行号实地核对）。改动一律未 commit。

## 1. 深化摘要

- **L08 正文**：0 → 149 行（新文件，工程机制型）。SwapBuffers 提交≠显示钩子 → 装配线类比（边界：领先 1–3 帧/V-Sync 背压）→ 管线七阶段与片元淘汰赛（V33）→ FBO/多 Pass + PSO/变体纪律 → Frame in flight 上限与三同步原语（V35）→ Swap→合成→上屏链路（V34）→ 完整链图转载 + 工程红线四项 → P99 尖刺分层排查现场 + 5 误区 → 帧循环走查清单 → 桥句→L09。
- **新断言登记**：V33（管线七阶段，SRC-RN-GRAPHICS 新增）/ V34（SwapBuffers 提交≠显示——复合断言双挂 SRC-RN-GPU-BASE + **SRC-RN-INTERVIEW-GL 新增**）/ V35（Frame in flight 与三同步原语，SRC-RN-GPU-BASE），open/low；既有 V07（verified）预挂转正。
- **quiz 边界**：非 pilot 课无 quiz 文件（validate §10 规则），正文 §9 如实声明。

## 2. 独立审读原始结论（第一轮）

- **acceptable = true，修订 0 轮**；**22 处技术表述全部溯源**（行号实地核对）。
- 亮点（审读员原文）：§4.4"提交≠显示"把分散在三份文档的链路证据串成因果链且逐句挂源；§4.1 七阶段流转引文与源逐字一致；无编造数字；两层 course.json 四处联动一致。
- 十维度：9 ✓ + 2 部分（概念层 PSO/V-Sync 释义——已修；桥句 L09 主题表述——已修）。

## 3. 审读发现（1 major + 8 minor）及修复对照（全部已修，修复后门禁复跑通过）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **major** | V34 复合断言 evidence 仅挂 GPU-BASE，"vsync 背压"子断言的逐字原文在面试库文档（:288/:356）且该文档未注册 SRC；"View 树混合"原文在解码链路 :130——追溯面不完整，影响 G1 升级裁决依据 | evidence 双挂（+SRC-RN-INTERVIEW-GL）；source_documents 扩为三向（GPU 基础/解码链路/面试库）；registry 新增 SRC-RN-INTERVIEW-GL（used_by=[V34]） |
| 2 | minor | "面试题库 §6"标注错位（该句逐字位于 §3 管线表） | 改"管线表与 §6"双指向 |
| 3 | minor | 两处含小节号的链接为 doc 级无锚点 | 解码链路链接补 #32 锚点（L06 已验证的锚点）；面试库保持 doc 级并改文字指向 |
| 4 | minor | PSO/V-Sync 首现无一句话解释 | 两处各补一句话释义 |
| 5 | minor | §10 "L09 沿跨平台主题继续"与 course.json L09 主题（移动端瓶颈与 TBDR）不符 | 改"L09《移动端瓶颈与 TBDR》（教材页待建）" |
| 6 | minor | L07 桥句"L08 教材页待建"已过时（跨篇联动） | L07 §10 更新为直链 L08 |
| 7 | minor | §4.3 引用"L07 的占用率机制"概念层级偏宽 | 改指主文档 §4.2 验证表第 2 行（气泡=CPU 提交不足） |
| 8 | minor | §11 延伸/术语完整性 | 已核对（V07/V33/V34/V35 分层状态如实） |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**74 documents（69+L03/L04/L05/L07/L08）/ 17 sections / 124 terms / 19 lessons / 7 labs / 544 cards / 2752 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**10 篇 · OK**
- review_gate：**52 claims（verified 18 / open 27 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 73→74 同步）

## 5. 待人工事项

1. **G2 评分**（L02/L03/L04/L05/L06/L07/L08/L11/L13 九篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. V33–V35（open/low）升级待 G1 另裁；「其余篇目 vs 先转 P8」顺序决策留用户。
