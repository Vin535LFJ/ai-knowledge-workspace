---
doc_id: P10-G1-HDR-QUEUE
type: review-material
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# G1 核验队列 · HDR 批次（V63–V67 + V23 升级申请）

> **AI 只准备证据与选项，裁决栏由人填写。** 新断言已全部登记 open/low（review_gate 84 claims 误标 0）；本材料供 G1 人工核验后裁决升级。
> 关联：KCR-2026-11-001（I19 = V23 reverify）· RUN-2026-11-20-p10-hdr · 研究报告 reviews/p10/research-report-hdr.md

## 1. 新断言核验清单（逐条：断言 → 证据定位 → 核验动作）

| ID | 断言要点 | 权威证据定位（可点开核对） | 建议核验动作 |
|---|---|---|---|
| V63 | BT.2100 PQ/HLG 双系统、BT.2020 色度、10/12bit、不得混用；HLG 兼容仅限 BT.2020 WCG | ITU BT.2100-3 Table 4/5/9（UPM 论文逐字转载可对照）；UHD Forum §7.1.2–7.1.4 | 对照 Table 4/5 定义与 §7.1.3 兼容边界原文 |
| V64 | PQ EOTF 公式 + 5 常数 + 锚点 100nit≈0.508078 / 1000nit≈0.751827；Barten 模型；code 509 算例 | colour-science eotf_ST2084 文档（doctest 可复算）；UPM Table 4；BT.2100 Table 4 | 用 colour-science 或手算复核 doctest：eotf_ST2084(0.508078421517399)=100.0 |
| V65 | HDR10 = PQ10 + ST 2086 MDCV + MaxCLL + MaxFALL；KEY_HDR_STATIC_INFO/KEY_HDR10_PLUS_INFO；部分显示忽略元数据；直播可为 0 | UHD Forum §7.2/7.2.1/7.2.2；AOSP HDR 页元数据段 | 核对三件套定义与"忽略/0 值"原文 |
| V66 | Android 发现→解码→合成链；7.0 仅 tunneled 保证、非 tunneled 可丢 HDR 压平 SDR；13 libtonemap + sdrHdrRatioMap SDR dimming | AOSP HDR 页 Discovery/Playback/HDR10 pipeline；AOSP Mixed SDR/HDR 页 | 核对 tunneled caveat 原句与 libtonemap/dimming 配置段 |
| V67 | PQ→BT.709 显示 = dim/washed out/去饱和/色相偏移；TM 须线性光；8bit FBO 先截断已晚；dimming black crush 须 dither | ITU BT.2408 §3.1 + §5；AOSP Mixed 页 Issues；repo 流媒体 §5.3 / GPU图像处理算法 | 核对 BT.2408 §3.1 原句（发灰权威描述） |

## 2. V23 升级申请（KCR I19，reverify open→verified）

- **现状**：V23（PQ 绝对/HLG 相对概览，L03 挂载）open/low，原证据仅 repo_doc。
- **本批变化**：外部权威证据链闭合（BT.2100/UHDF/UPM）。
- **遗留问题**：V23 文本"HLG 兼容 SDR"缺边界——UHD Forum §7.1.3 明确兼容**仅 SDR/BT.2020 WCG**，BT.709 屏去饱和+色相偏移（BT.2408 §3.2.1 同口径）。
- **选项**：A 先 modify 补边界条件再升级 verified；B 直接升级并附条件；C 维持 open。
- **AI 推荐（仅供参考）**：A——边界是这条断言准确性的一部分（先例：V14 保留平台条件升级，D18）。

## 3. 裁决栏（人工填写）

| 项 | 裁决（升级/维持/附条件） | 裁决人 | 日期 |
|---|---|---|---|
| V63 | 升级 verified/high（采纳 AI 推荐授权） | user（授权 AI 推荐执行） | 2026-11-21 |
| V64 | 升级 verified/high（采纳 AI 推荐授权） | user（授权 AI 推荐执行） | 2026-11-21 |
| V65 | 升级 verified/high（采纳 AI 推荐授权） | user（授权 AI 推荐执行） | 2026-11-21 |
| V66 | 升级 verified/high（采纳 AI 推荐授权） | user（授权 AI 推荐执行） | 2026-11-21 |
| V67 | 升级 verified/high（采纳 AI 推荐授权） | user（授权 AI 推荐执行） | 2026-11-21 |
| V23（I19） | A——先补 HLG 兼容边界（BT.2020 WCG）再升级 verified/high（采纳 AI 推荐授权；glossary HLG 词条已联动更新） | user（授权 AI 推荐执行） | 2026-11-21 |

## 4. 未解决问题（不阻塞本批，登记入研究队列）

- U1：TextureView 8bit / SurfaceView 10bit 差异的官方出处（现仅二手转述，未入断言）。
- U2：BT.2100 英文原版 PDF 直接抓取（现经官方阿文 docx + UPM 逐字转载 + UHD Forum 三重交叉）。
- U3：HLG 在 BT.709 屏兼容度的主观测试原文（EBU/RAI/IRT，UHD Forum 引用）。
- U4（审读登记）：`tools/glossary.json` HLG 词条"向下兼容 SDR 显示"无 BT.2020 WCG 边界，与 L19 精确口径存在张力——建议随 V23 的 G1 裁决（I19）联动更新术语卡；本批不动共享术语资产的既有文本。
- U5（审读登记；G1 惯例裁决：跨课引用按**前课指针**口径可接受——实质性依赖（正文以其结论为依据）才同步 used_by；L19 引 V21/V24 属前课指针，不同步）：L19 §5 速查表跨课引用 V21/V24（L03 登记，used_by_lessons 未含 L19）——按"前课指针"口径可接受；若按实质性依赖口径需同步 used_by，请 G1 时明确惯例。