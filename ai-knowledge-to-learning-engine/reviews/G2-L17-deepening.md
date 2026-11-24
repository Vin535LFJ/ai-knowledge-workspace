---
doc_id: G2-L17-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L17《程序化几何 · 从轮廓到网格》新写

> 供 G2 人工审核。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L17-程序化几何从轮廓到网格.md`（0 → 约 180 行，数学推导型（含实验））。
- 结构：改参数回 Blender 之痛钩子 → 拉坯类比（双重边界声明）→ §4.1 参数方程三件套（objective ①/checkpoint ②）→ §4.2 M×N 顶点 + 索引四角公式推导（objective ②）→ §4.3 成本四公式 + 6 倍账（objective ③/checkpoint ①）→ §4.4 GPU 执行 + 三误区 + 适用边界（checkpoint ③）→ §5 生成代码骨架 + 索引/顶点量级 → §6 数据驱动花瓶现场 → §7 lathe 实验四任务 + selfTest → 桥 L18。

## 2. 断言与来源

V57（参数方程与适用边界）/V58（顶点索引推导与成本）/V59（细分取舍与工程定位），均 open/low；复用 V17（open/low）；新来源 SRC-RN-PROCEDURAL；lab=procedural-lathe 双向绑定。全部新断言默认 open/low，升级待 G1 人工裁决；反向索引已同步。

## 3. 独立审读结论（只读换人子代理）

首轮 acceptable=true（0 blocker / 0 major / 4 minor）。minor：'第一次生产级应用'与 L14 冲突改'第一次亲手生产顶点数据'、误区三补源限定词'通常'（两处）、tasks/note 改标转述/摘要、源 §5 '花冠'疑似笔误登记（教材用'花瓶'与 labs/V57 一致，源未改）。**全部修复**。

**源笔误登记：程序化几何与旋转曲面.md 行 68 '花冠'应为'花瓶'**（教材/实验/台账均用花瓶；源更正待 G1/源所有者裁决）。

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
