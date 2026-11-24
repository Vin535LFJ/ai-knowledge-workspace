---
doc_id: G2-L15-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L15《性能评测与项目复盘》新写

> 供 G2 人工审核。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L15-性能评测与项目复盘.md`（0 → 约 180 行，方法论/工程机制型）。
- 结构：报告 A/B 对比钩子 → 体检类比（边界声明）→ §4.1 严谨实验三原则（objective ①）→ §4.2 P50/P99 vs 平均 + 线程活跃周期口径（objective ②）→ §4.3 画质指标体系 + 陷阱 + 成对出现（objective ③）→ §4.4 表达规范 + 趋势红线（checkpoint ②）→ §5 证据链模板 → §6 报告 A 审计现场 → §7 四项练习 → 桥 L16。

## 2. 断言与来源

V51（三原则）/V52（量化口径与表达规范）/V53（画质指标体系），均 open/low；复用 V32（open/low）；新来源 SRC-RN-PRACTICE/ADAS + GPU-BASE 扩展。全部新断言默认 open/low，升级待 G1 人工裁决；反向索引已同步。

## 3. 独立审读结论（只读换人子代理）

首轮 acceptable=false（**1 blocker** / 4 minor）。**blocker：源文档 §5.3 'PSNR 每提高 6dB，MSE 约减半' 为数学笔误**（10·log₁₀2≈3.01dB，+6dB 对应 MSE≈1/4）——教材按正确数学表述并显式登记勘误，练习改 MSE=50/25 双算例；V53 台账文本同步更正 + conditions 登记；**源文档未擅自修改，更正待 G1/源所有者裁决**。minor：checkpoint 弯引号逐字、P99 口径半句、frontmatter 补三份源、CABAC/GOP/preset/tone mapping 释义。**全部修复**。

**待人工裁决：源文档 05-项目实战/项目实战指南.md 行 372 的 dB/MSE 换算笔误更正**（教材已按正确数学表述，源与教材目前口径不一致，属已知登记项）。

## 4. 门禁实测

见 CHANGELOG 2026-11-20 批量条目（build/validate 12 checks/arc/publish/review_gate/registry，修复后复跑）。

## 5. G2 人工判定（待填——AI 不自评）

| 项 | 待人工填写 |
|---|---|
| G2 判定（通过 / 有条件通过 / 退回修订） | |
| 评分（参照 review-report.md 维度体系） | |
| 备注 | |

## 6. 边界

未 commit/push；未改既有断言状态；stash 原样（B12）；本课不在 pilot course.json（quiz 待纳入后按 validate §10 补建，与 L03–L12 先例一致）；源文档笔误仅登记未擅改。
