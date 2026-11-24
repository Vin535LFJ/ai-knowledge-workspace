---
doc_id: G2-L13-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第四篇 L13《坐标变换与 MVP》深化（2026-11-20，pilot 路线收官）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（数学推导型），独立子代理审读（只读换人、逐条对源 + 独立重算）。改动一律未 commit。

## 1. 深化摘要

- **L13 正文**：89 → 235 行。数学推导型结构：开篇双钩子（GL→Vulkan 深度事故 / T·R·S 顺序症状）→ 六空间表（新增「缺了它会怎样」列）→ MVP 组合顺序推导（列向量右侧作用、主序陷阱表、T·R·S）→ 投影矩阵推导重组（矩阵、端点验证表、w_clip=-z_eye、数值算例、透视除法不能手动做的插值面原因）→ 五 API NDC 表 + 负视口高度边界 + 视口公式 + UV 原点表 + FBO Y-flip 事故（回收 L06 getTransformMatrix 伏笔）→ 视锥剔除一瞥 → 正交投影 → 排查现场 + 五行参数错误表 + 5 误区 → 桥句宣告 pilot 五课收官（course.json pilot L13.next=null 一致）。
- **断言纪律**：V17–V20 **如实保持 open/low（engineering_fact，B10=D19 确认登记）**，V18/V20 附条件如实；§11 登记原 V06 移除；**ledger V06.used_by_lessons 同步移除 "L13"**（反向索引一致）。
- **四处联动**：两层 course.json L13 checkpoint 补第 3 题「MVP 对列向量的正确相乘顺序是？」（quiz Q3，挂 V18）；正文 §9 三题（Q1 加"投影空间=裁剪空间"括注）。

## 2. 独立审读原始结论（第一轮）

- **acceptable = true（修 1 major 后）**；46 处技术表述，推导主链零错误。
- 审读员独立完成：5 处数值全部重算（1.73205 / 0.97428 / 0.487 / 0.0974 / 0.83910）无误；端点代数验证成立（GL 版 -N→-1、-F→+1；Vulkan 版 -N→0、-F→1）；两张投影矩阵、六空间表、主序表、五行参数错误表、五 API NDC 表与源逐字对齐；三个锚点 slugify 逐字符验证并实际运行 validate_site.py（11 项全过）。

## 3. 审读发现（1 major + 7 minor）及修复对照（全部已修）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **major** | §1 把 T·R·S 顺序错误的症状（绕世界原点旋转）错挂到 M·V·P 上，且「M·V·P 画面看似能跑」不成立——与 §4.2 正确叙述自相矛盾（源 §2.2 的症状专属模型矩阵内部顺序） | 症状各归其位：T·R·S 写反→绕世界原点旋转；M·V·P 写反→投影套在原始局部坐标、w 全错、整体畸变不存在"看似能跑" |
| 2 | minor | §6「查上表第 3 行」方向词错误（五行表在下方向） | 改「查下表第 3 行」 |
| 3 | minor | ledger V06.used_by_lessons 仍含 L13，与 V17 note「替代原误挂 V06」及正文 §11 矛盾 | ledger V06.used_by_lessons 移除 "L13"（保留 L08） |
| 4 | minor | 「盲目 transpose…换台设备又坏」修辞冒充跨设备随机性（确定性数学错误） | 改「掩盖症状，错误根源还在」 |
| 5 | minor | 「与近平面求交（§4.4）」内部引用失准（细节在源 §6.2） | 改引源 §6.2，补「或交给 GPU 裁剪」 |
| 6 | minor | 「贴脸消失」把两个不同归因并列（未归一化 vs 跨近平面丢弃，源 §6.2 分列） | 分开表述：未归一化→剔除尺度误判；跨近平面丢弃→贴脸消失 |
| 7 | minor | 两处「光栅化深度与移动GPU架构.md」链接缺 #2-深度缓冲 锚点 | 两处补锚点 |
| 8 | minor | 检测题用「投影空间」，正文通篇「裁剪空间（Clip）」 | §9 Q1 加括注「投影空间即正文 §4.1 的裁剪空间 Clip」 |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**69 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2561 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**5 篇 · OK**
- review_gate：**37 claims 误标 0**
- test_publish_boundary：**11 tests OK**

## 5. 待人工事项

1. **G2 评分**（L02/L06/L11/L13 四篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. V17–V20 升级：open → verified 需逐条权威核验后 G1 另裁（B10 口径）。
4. **pilot 收官后的路线选择**（集中决策点）：其余篇目（L03 起新生产）vs 转入 P8 KCR 闭环——见 Engine WORKFLOW_STATE 续跑点与 Program NOW.md。
