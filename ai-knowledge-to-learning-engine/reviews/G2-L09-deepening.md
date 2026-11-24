---
doc_id: G2-L09-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第十篇 L09《移动端瓶颈与 TBDR》新写教材（2026-11-20，「其余篇目」第六篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写，对比边界型），独立子代理审读（只读换人、四项数值独立重算）。改动一律未 commit。

## 1. 深化摘要

- **L09 正文**：0 → 153 行（新文件）。桌面经验三连变形钩子 + 720p 带宽账 → 瓷砖类比（边界声明）→ IMR vs TBDR 流程与七行差异表（V36）→ Overdraw/RMW 与 Early-Z 三失效条件（V37）→ MSAA 原理/成本/非 SSAA（V38）→ API 层差异（C05/V09）→ 带宽账三件套 + 优化顺序六条 + 判断表五行 + 红线五条 → 排查现场 + 5 误区 → Overdraw 视图走查清单 → 桥句→L10。
- **新断言登记**：V36/V37/V38（open/low，SRC-RN-RASDEPTH 新增，双向索引一致）；既有 E02/C05/V09 挂载，条件如实转述。
- **quiz 边界**：非 pilot 课无 quiz 文件（validate §10 规则），正文 §9 如实声明。

## 2. 独立审读原始结论（第一轮）

- **acceptable = false（1 blocker）+ 7 minor**；37 处技术表述 36 处逐行溯源（四项带宽重算全部闭合：3.69/7.37/442/4.4GB/s）。
- 亮点：七行差异表、六条优化顺序、五行判断表、五条红线与主文档逐行一致；Q1/Q5/Q6/Q8/Q9 转述忠实；V36–V38 两层台账同步、锚点 slugify 复算精确匹配。

## 3. 审读发现（1 blocker + 7 minor）及修复对照（全部已修）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **blocker** | §4.2"每次半透明混合……三倍带宽"挂源无据且算术不成立（RMW=读+写两次传输对一次；源只给机制不给倍数；标准 §2.7 说比例必带基准） | 改为"以单次写为基准 RMW 是读+写两次传输；源文档只给机制不给倍数，×N 按 §3.2 账实测" |
| 2 | minor | 面试提醒引文截断（漏"与优化建议"） | 补齐 |
| 3 | minor | 类比边界"分派本身有成本"无出处推断 | 改为源文档事实（binning 在几何阶段先做） |
| 4 | minor | loadOp/storeOp/alphaToCoverage 首现无解释 | 表后补一句 + alphaToCoverage 释义 |
| 5 | minor | "Overdown"错字 | 改 Overdraw |
| 6 | minor | L10 课时名误写为专题文档名《显式 API 与同步原语》 | 改 course.json 课时名《显式 API 与同步》 |
| 7 | minor | L08 桥句"L09 教材页待建"过时（跨篇联动） | L08 §10 更新为直链 L09 |
| 8 | minor | 720p 带宽账未声明十进制口径 | §1 补"十进制"（沿用 L01/L07 纪律） |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**75 documents（69+六篇新教材）/ 17 sections / 124 terms / 19 lessons / 7 labs / 553 cards / 2790 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**11 篇 · OK**
- review_gate：**55 claims（verified 18 / open 30 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 74→75 同步）

## 5. 待人工事项

1. **G2 评分**（L02–L09/L11/L13 十篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. V36–V38（open/low）升级待 G1 另裁；「其余篇目 vs 先转 P8」顺序决策留用户。
