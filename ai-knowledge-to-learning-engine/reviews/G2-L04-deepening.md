---
doc_id: G2-L04-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第六篇 L04《从文件到码流》新写教材（2026-11-20，「其余篇目」第二篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写），独立子代理审读（只读换人、逐条对源）。改动一律未 commit。

## 1. 深化摘要

- **L04 正文**：0 → 199 行（新文件）。直灌崩溃钩子 → 拆包流水线类比（附边界）→ 三段管线职责表 → 容器/码流两表与正交关系 → MediaExtractor/MediaCodec/FFmpeg 分工 → NALU/SPS/PPS/SEI 与缺 SPS 后果 → Annex B vs AVCC 双表 + CSD ⚠️ → MP4 Box 树与帧寻址 → 排查现场 + 5 误区 → §7 容器字段走读核查（五项含预期）→ 桥句→L05。
- **新断言登记**：V25（Annex B vs AVCC，附条件 ⚠️）/ V26（容器/码流职责分离与直灌异常），open/low，SRC-RN-AV-BASE（used_by_claims 同步 +V25/+V26，原 V13/V14/V16 保留）。既有 V01/V11（verified/high）此前已预挂 L04。
- **quiz 边界**：非 pilot 课无 quiz 文件（validate §10 规则），正文 §9 如实声明。

## 2. 独立审读原始结论（第一轮）

- **acceptable = true，修订 0 轮**；**40 处技术表述全部可溯源**。
- 十维度：9 ✓ + 1 部分（§7 清单缺"预期"——已修）；亮点：两张表/采样表五行/帧寻址流程逐字忠实于源，⚠️有条件成立（CSD 直喂 AVCC）连同边界原样保留，V01/V11=verified 与 V25/V26=open/low 的分层在 §11 如实说明，台账与 source-registry 反向索引完全同步。

## 3. 审读发现的 9 条 minor 及修复对照（全部已修，修复后门禁复跑通过）

| # | 发现 | 修复 |
|---|---|---|
| ① | 繁体"偏愛"两处 | 改"偏爱" |
| ② | §8"两者正交"挂 V26 超出 claim 原文范围 | 改标"教材推导"，V26 只挂职责分离 |
| ③ | MediaExtractor"能力以平台容器为限"无直接出处 | 收窄为 §1.2 表的组件事实 |
| ④ | "解封装链路 ✅"标签与所引三模块表不符 | 改"三段管线的职责表" |
| ⑤ | "§1.3 原话"标签过强（仅「全格式拆包工」为原话） | 收窄标注 |
| ⑥ | "avcC box"术语源文档未出现且未解释 | 改 CSD 口径（源文档有据） |
| ⑦ | §7 清单缺"预期看到什么"（标准 §2.9 三段式） | 五项各补预期 |
| ⑧ | MediaCodec/熵解码首现无释义 | §1 各补一句话 |
| ⑨ | L03 桥句"L04 教材页待建"已过时（跨篇联动） | L03 §10 更新为直链 L04 |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**71 documents（69+L03+L04）/ 17 sections / 124 terms / 19 lessons / 7 labs / 520 cards / 2642 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**7 篇 · OK**
- review_gate：**43 claims（verified 18 / open 18 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 70→71 同步）

## 5. 待人工事项

1. **G2 评分**（L02/L03/L04/L06/L11/L13 六篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. V25/V26（open/low）升级待逐条权威核验后 G1 另裁。
4. 「其余篇目 vs 先转 P8」顺序决策（Engine WORKFLOW_STATE 已登记建议）。
