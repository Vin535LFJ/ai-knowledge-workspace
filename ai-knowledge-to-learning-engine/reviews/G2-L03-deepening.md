---
doc_id: G2-L03-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第五篇 L03《色彩与显示范围》新写教材（2026-11-20，「其余篇目」首篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写，非 pilot 课），独立子代理审读（只读换人、逐条对源 + 独立重算）。改动一律未 commit。

## 1. 深化摘要

- **L03 正文**：0 → 168 行（新文件）。发灰算术开篇 → 三件套类比（附边界：range 是第四件事）→ 三字段独立（V24）→ range 机制与错用后果（V21）→ sRGB 分段函数与线性工作流（V22，0.5→0.214 算例）→ PQ/HLG 与 banding（V23）→ 排查现场（发灰双病因）+ 5 误区 → §7 八项色彩管理检查清单（源 §3.3 全文）+ 零成本观察实验 → 桥句→L04。
- **新断言登记（evidence-and-claims 程序，默认 open/low）**：V21/V22/V23/V24（engineering_fact）+ source-registry 新增 SRC-RN-COLORMGMT（repo:03-图形与GPU工程/色彩管理与采样滤波.md，used_by_claims=[V21,V22,V23,V24]，双向索引一致）。review_gate 实测 41 claims 误标 0。
- **quiz 边界**：validate §10 要求 quizzes/ 下每个 quiz 的 lesson ∈ pilot course.json——非 pilot 课不得有 quiz 文件。为 L03 新建的 quiz 已按规则移除；正文 §9 来源行如实改述该规则，pilot 化后补建。

## 2. 独立审读原始结论（第一轮）

- **acceptable = false（1 blocker）+ 8 minor**；26 处技术表述全部溯源、三处引号原文逐字准确、validate/arc 门禁全过、V21–V24/SRC-RN-COLORMGMT 登记如实、pilot 层确无 L03 属实。
- 审读员独立重算全部数值：16/255≈6.27%、(16/255)^2.2≈0.23%（光度口径）、sRGB 0.5→0.526^2.4≈0.214、0.03→0.0023、反向 0.214→0.49996 闭合、219/239=0.9163、219/255=0.8588。

## 3. 审读发现（1 blocker + 8 minor）及修复对照（全部已修）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **blocker** | "有效灰阶账"三处口径互斥：§5 的 219/239≈91.6%（239 分母无物理意义）、§1 的 256→约219（≈86%）、§8 的"压掉一成"——同一量化对象三个互斥数量 | 统一口径（0–255 满量程）：黑位 6%、白位 92%、可用级数 220/256≈86%（损失约 14%），§1/§5/§8 三处同一表述 |
| 2 | minor | "6% 亮度"措辞会被读成光度意义（光度口径实为 0.2–0.5%） | 全文改"6% 灰阶电平" |
| 3 | minor | "工程做法五条"实列四条，漏源 §1.3 表第 3 行"帧缓冲 sRGB 编码/手动 pow" | 补第五条帧缓冲（恰是排查②与清单第 5 项的机制来源） |
| 4 | minor | "ST2084"两次出现未释义 | 表内补"SMPTE 对 PQ 传输函数的标准编号"，术语表收录 |
| 5 | minor | §6"查上表第 3 行"方向词错误 | ——（L03 排查现场无此表述；该条属 L13，本篇无此问题。审读员跨篇提示，已确认） |
| 6 | minor | §10 "[下一章]"链接落在知识架构总览而非下一课（L04 无 lesson 文件属客观限制） | 改纯文字"L04《从文件到码流》（教材页待建）"+总览链接并注明 |
| 7 | minor | 两条延伸链接含节号但无锚点（#22-yuvrgb-gpu转换 / #5-10bithdr-与-av1） | 两条补锚点（validate 解析通过） |
| 8 | minor | "三概念表（✅，断言 V24）"✅ 易误读为断言已验证（V24 为 open/low） | 改双层标注"源文档 ✅；断言 V24 open/low，见 §11" |
| 9 | minor | banding 解法漏源文档第三项"加噪声" | 补齐三项 |

注：⑤号在首轮审读 JSON 中指向 L13 的"上表"问题（跨篇提示），L13 已在自身修复轮处理；L03 全文核对无此表述。

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**70 documents（69+L03）/ 17 sections / 124 terms / 19 lessons / 7 labs / 512 cards / 2599 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**（含 6 个锚点解析、V21–V24 双向索引）
- check_chapter_arc：**6 篇 · OK**（L03 加入检查集）
- review_gate：**41 claims（verified 18 / open 16 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 69→70 同步，reviews 零泄露核心断言不变）

## 5. 待人工事项

1. **G2 评分**（L02/L03/L06/L11/L13 五篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. V21–V24（open/low）与 V17–V20 的升级均待逐条权威核验后 G1 另裁。
4. L03 是否纳入 pilot 层（纳入后需按 validate §10 补 quiz）属课程路线决策，留人工。
