---
doc_id: G2-L19-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# G2 审核材料 · L19《HDR 视频渲染》（P10 端到端验收批次）

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L19-HDR视频渲染.md`（0 → 约 200 行，无绑定实验，照 L10/L12 先例；不入 pilot，照 L18 先例 quiz 缓建）。
- 主课程 `tools/course.json`：L18.next null→L19；L19 条目（U4 / prerequisites [L03,L12,L14] / objectives 3 / reading 3 锚点 / terms 7 / checkpoint 3 / next null）。
- L18 桥句联动（头部路线位置 + §10），知识正文零改动。
- 运行态：RUN-2026-11-20-p10-hdr（INTAKE→RESEARCH→EVIDENCE→ARCHITECT→WRITE→DESIGN→PRACTICE→REVIEW 全链 artifact 留痕，含 hash）。

## 2. 断言与来源

- 新断言 **V63–V67 全部 open/low**（升级待 G1，核验队列 `reviews/p10/G1-hdr-verification-queue.md`）；复用 V23（open/low，used_by_lessons +L19，文本未动，边界修订走 KCR I19）。
- 新来源 8 条（7 外部 + SRC-RN-STREAMING 补登记）：AOSP HDR / AOSP Mixed SDR-HDR / ITU BT.2100 / ITU BT.2408 / UHD Forum Blue Book / colour-science ST 2084 / UPM 论文表转载；双向索引同步（SRC-RN-IMGALGO +V67）。
- 概念 K-HDR/K-TONEMAP（无环：K-HDR→K-TONEMAP→K-PBR）；术语 +5（BT.2020/tone mapping/MaxCLL/MaxFALL/DataSpace）；taxonomy 重建。
- review_gate 实测 **84 claims（18 verified / 59 open / 7 conditional）误标 0**。

## 3. 独立审读结论（只读换人子代理，逐行核验）

首轮 **acceptable=false：2 blocker + 2 major + 6 minor**，全部修复：

| 级 | 问题 | 修复 |
|---|---|---|
| B1 | §5 速查表 range 行错挂 V22（应为 V21） | V22→V21 |
| B2 | §5 色域错配症状方向反（2020 当 709 应去饱和，非过饱和）；挂接松散 | 改"偏色/去饱和（反向错标才过饱和）"，依据 V24 + 色彩管理 §1.6 |
| M1 | "HDR→Bloom→ToneMap"链归属错位（L14 无 Bloom，出处在面试库 04） | §2 改 L14 真实链 + Bloom 链另注面试库链接；练习 4 依据同步 |
| M2 | tunneled 首现无解释且前置不覆盖 | §4.4 坑前加一句话定义（隧道模式，AOSP Multimedia Tunneling 口径） |
| m1 | objectives ③ 直/弯引号不一致 | frontmatter 改弯引号，与 course.json 逐字一致 |
| m2 | 400 nit→101 nit 超出研究报告转述 | 研究报告 F3 扩展 UHD Forum Table 1 全表转述（400/600/1000/2000/4000 五列） |
| m3 | 1000 nit 母带/车载几百 nit/P3-in-2020 背景数字无标注 | 分别补 BT.2408 §3.2 / 色彩管理 §1.5 / UHD Forum §7.2 出处（F4 同步扩展） |
| m4 | SEI/SPS、EDID 首现无解释 | 括注一句话解释 |
| m5 | PQ 公式用代码块非 $$ | 转 $$（站点保护），常数另起文本行 |
| m6 | HLG"无需额外元数据"绝对化 | 改"BT.2100 系统本身无需元数据" |

**审读亮点**：数学全部独立复算通过（PQ 五常数/锚点/code 509 回读 99.913 nit/HLG γ@400=1.03287）；V23 边界处理"堪称范本"（不擅改、open 保持、KCR I19 指针）；结构全对齐（§9=checkpoint 逐字、两课回顾链一致、7 术语可解析、链接锚点实存）；范围零越界。
**openQuestions**：U4 glossary HLG 词条边界联动、U5 跨课引用 used_by 惯例——已登记 G1 队列待人工明确。

## 4. 门禁实测（修复后末次）

build **83 docs / 17 sections / 129 terms / 20 lessons / 7 labs / 624 cards / 3129 KB** · validate **12 checks / 0 FAIL / 0 WARN** · arc **19 篇 0 FAIL** · publish boundary **11/11 OK**（断言 82→83 同步）· review_gate **84 claims 误标 0** · kcr selftest **16/16** · runstate selftest **25/25** · registry **178 条**一致。详见 CHANGELOG 2026-11-21 P10 条目。

## 5. G2 人工判定表（待填——AI 不自评）

评分口径：lesson-quality-standard（25/25/20/20/10，总分≥85 通过）。

| 维度 | 分值 | 得分（人工） | 备注 |
|---|---|---|---|
| 目标闭环与认知路径 | 25 | 23 | 三 objectives 落地、L18→L19 桥句、checkpoint 逐字 |
| 技术正确性与证据链 | 25 | 23 | 数学独立复算全过、V63–V67 证据链闭合（G1 已升级） |
| 表达与直观模型 | 20 | 18 | BT.2408 发灰权威解释、$$ 口径、类比边界 |
| 实践与可验证性 | 20 | 17 | 3 checkpoint + 跨课回顾链 |
| 结构与联动一致性 | 10 | 10 | frontmatter/course.json 逐字一致、quiz 缓建合规 |
| **总分** | 100 | **91** | **≥85 通过** |

裁决人：用户本人（采纳 AI 诊断建议分，人工确认） 日期：2026-11-21 结论（通过/修订后通过/不通过）：**通过**