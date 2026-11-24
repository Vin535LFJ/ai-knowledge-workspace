---
doc_id: G2-L14-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L14《光照、材质与图像算法》新写

> 供 G2 人工审核。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L14-光照材质与图像算法.md`（0 → 约 200 行，工程机制型 + 对比边界型）。
- 结构：三 bug 归层钩子 → 摄影类比（边界声明）→ §4.1 演进表 + BRDF/PBR 定位（objective ①/checkpoint ①）→ §4.2 三条铁律 + 归层表（objective ②）→ §4.3 mipmap 机制与两种锯齿（checkpoint ②）→ §4.4 后处理地图（objective ③前）→ §4.5 批处理 CPU 侧定位（objective ③后）→ §5 管线位置图 + 变体账 → §6 归层排查现场 → §7 四项练习 → 桥 L15。

## 2. 断言与来源

V46（PBR 模型约束）/V47（归层与铁律）/V48（mipmap）/V49（后处理地图）/V50（批处理位置），均 open/low；复用 V07（verified/medium）/V38（open/low）；新来源 SRC-RN-LIGHTING/IMGALGO/BATCHING + COLORMGMT 扩展。全部新断言默认 open/low，升级待 G1 人工裁决；反向索引已同步。

## 3. 独立审读结论（只读换人子代理）

首轮 acceptable=false（0 blocker / 2 major / 7 minor）。major：U5 课序错（第 1→第 2 课）、管线图 dither 顺序与源 §7.2 矛盾（改 sRGB 编码后 dither）。minor：两处引文逐字还原、diffuse 原词、间接绘制补'或扩展'、V48/V50 conditions 补全、双重 gamma 练习措辞、CAS/NLM/TAA/TNR/NPU 首现释义、course.json L14.reading 补色彩管理条目。**全部修复**。

L14/L18 分工边界审读确认守住（D/G/F 公式深潜与 pbr 实验归 L18，未预占）。

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
