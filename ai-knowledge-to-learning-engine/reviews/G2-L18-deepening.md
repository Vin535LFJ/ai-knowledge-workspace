---
doc_id: G2-L18-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L18《PBR 光照与材质参数》新写

> 供 G2 人工审核。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L18-PBR光照与材质参数.md`（0 → 约 190 行，数学推导型（含实验，next 链收官））。
- 结构：三滑杆质感变化钩子 → 镜子海类比（边界声明：不覆盖 G/漫反射）→ §4.1 Cook-Torrance 分解与 D/G/F 职责（objective ①）→ §4.2 metalness 能量分配 + F0 表 + 工作流代码（objective ②/checkpoint ①）→ §4.3 GGX 四步推导 + Smith/Schlick（objective ③/checkpoint ②③）→ §4.4 多次散射补偿 → §5 参数对照表 + D 峰值 625 倍算例 → §6 粗糙金属发黑现场 → §7 pbr 实验四任务 + selfTest → §10 收官桥（叙事顺序回顾 + 缺口表延伸）。

## 2. 断言与来源

V60（CT 分解）/V61（GGX/Smith/Schlick 公式族与工作流）/V62（多次散射与实验边界），均 open/low；复用 V46（open/low）；SRC-RN-LIGHTING 扩展；lab=pbr-lighting 双向绑定。全部新断言默认 open/low，升级待 G1 人工裁决；反向索引已同步。

## 3. 独立审读结论（只读换人子代理）

首轮 acceptable=true（0 blocker / 0 major / 5 minor）。minor：'总能量守恒'措辞改'大致守恒+高粗糙度损失'、F_ss/E_ms/F_avg 符号含义补全、tasks/note 改标转述/摘要、收官链标'叙事顺序'、§4.2 补 §10 自测问答第二锚点。**全部修复**。

selfTest 宏观 N·V 与公式 V·H 形式差异已在正文与 V61 conditions 双层披露；D 峰值算例 3183/5.09/625 审读复算无误。

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
