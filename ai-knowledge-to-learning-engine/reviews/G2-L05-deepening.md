---
doc_id: G2-L05-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第七篇 L05《硬解与 ownership》新写教材（2026-11-20，「其余篇目」第三篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写），独立子代理审读（只读换人、逐条对源 + 独立重算）。改动一律未 commit。

## 1. 深化摘要

- **L05 正文**：0 → 175 行（新文件，工程机制型）。双俗语钩子 → 周转箱类比（三条例边界）→ buffer 流转循环（V27）→ 省电物理基础与四条件限定（C03 conditional）→ 八步回退状态机（V28）→ **flush 推导节（诚实标注推导 + 候选登记验真队列 P07）** → 软硬解搬运账（口径修正后）→ 排查现场 + 5 误区 → 状态机走查清单 → 桥句→L06（带 C02 条件）。
- **新断言登记**：V27（buffer 有限池与借还/移交，附条件）/ V28（八步状态机与触发条件，附条件：顺序不可换），open/low，SRC-RN-VERIFICATION（used_by_claims 同步 +V27/+V28，原 C01–C07/P01–P06 保留）。既有 C03（conditional）预挂转正。
- **quiz 边界**：非 pilot 课无 quiz 文件（validate §10 规则），正文 §9 如实声明。

## 2. 独立审读原始结论（第一轮）

- **acceptable = false（1 blocker + 1 major）+ 8 minor**；20 处技术表述，溯源纪律"接近 Gold Standard 水准"。
- 亮点（审读员原文）：八步状态机与源 §8.4 逐条逐序逐字吻合；功耗"不能泛化固定 10%"的反数字纪律；C03 条件化引用；⚠️ 条件三条全部如实带条件转述；flush 推导的正文诚实标注方向正确。

## 3. 审读发现（1 blocker + 1 major + 8 minor）及修复对照（全部已修）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **blocker** | §4.4/§11 声称"openQuestions 已登记"而全库查无实据（追溯断言落空） | **做实登记**：flush 候选正式登记于验真队列 ❗ 表 **P07**；正文/§11 改为指向 P07 |
| 2 | **major** | §5"软解每帧多两次主存↔显存总线搬移"与源失实（"两次"是 ByteBuffer 弯路的账） | 改"每帧多一次总线拷贝；ByteBuffer 弯路才是往返两次"，口径分离标注 |
| 3 | minor | V28/正文触发条件漏"分辨率突变"与"驱动崩溃"（源 §8.4 开头原文） | 两处补齐（ledger claim 文本同步） |
| 4 | minor | §6"§2.4 设备差异"引用错位（实为"码率与分辨率"因素） | 改正 |
| 5 | minor | L06 实验 task 4 引文不逐字 | 改逐字引用 |
| 6 | minor | §4.1 ASCII render=false 分支行残缺 | 补全为对称两行 |
| 7 | minor | DPB 列入本章术语但正文未出现 | 移出并指向 L04 §4.4 |
| 8 | minor | C01/V01 的 used_by 反向索引双向漂移（C01 挂 L05 但正文未引用；正文引用 V01 但未登记） | C01.used_by 移除 L05；V01.used_by 增补 L05 |
| 9 | minor | §10 桥句"零拷贝开始生效"丢 C02 条件；两处引文不逐字 | 补 C02 条件；引文改逐字 |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**72 documents（69+L03/L04/L05）/ 17 sections / 124 terms / 19 lessons / 7 labs / 528 cards / 2681 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**8 篇 · OK**
- review_gate：**45 claims（verified 18 / open 20 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 71→72 同步）

## 5. 待人工事项

1. **G2 评分**（L02/L03/L04/L05/L06/L11/L13 七篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. **验真队列 P07**（flush 推导）：待官方文档核验与实测复现后走断言登记程序。
4. V27/V28（open/low）升级待 G1 另裁；「其余篇目 vs 先转 P8」顺序决策留用户。
