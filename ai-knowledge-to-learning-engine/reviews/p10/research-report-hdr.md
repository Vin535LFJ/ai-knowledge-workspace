---
doc_id: P10-RESEARCH-REPORT-HDR
type: research-report
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# 研究报告 · HDR 视频渲染（P10 批次，D2 合同）

> 放置说明：documentation-types 建议 research-report 放 `.agent/plans/` 或课程研究目录；本批作为 run 审核材料统一放 `reviews/p10/`（不进学习站 bundle，registry 正常索引）。
> 运行态：RUN-2026-11-20-p10-hdr · RESEARCH 阶段产物。所有外部来源 accessed 2026-11-21。

## 1. 目标与范围

为 L19《HDR 视频渲染》提供可核验的外部证据链：PQ/HLG 传递函数定义与关键数学、HDR10 静态元数据语义、Android HDR 播放链与 tone mapping 机制、"发灰"故障的权威解释。范围边界见 intake-manifest §3。

## 2. 已有知识与缺口

已有：L03 §4.4 概览（V23 open/low，仅 repo 证据）、流媒体 §5 / 色彩管理 §1.5 参考层。
缺口：① V23 无外部权威来源；② PQ/HLG 数学无教学展开；③ 元数据三件套语义无系统表述；④ Android 链路的官方口径（tunneled/非 tunneled 差异、libtonemap、SDR dimming）未入库；⑤ "发灰"现象只有二手转述，无权威描述。

## 3. 搜索策略

官方优先：AOSP 显示文档（镜像抓取）→ ITU 官方文档（docx 提取）→ 行业权威（UHD Forum Blue Book）→ 公式常数三重交叉（ITU 表转载论文 + colour-science 官方库文档 + 厂商技术页）。直接抓取失败的通道（itu.int rec 页 / en.wikipedia）如实记录，改用官方文档镜像与检索提取，未使用不可核实的二手内容作断言证据。

## 4. 发现（F1–F8，每条带来源定位）

**F1 · BT.2100 双系统**：BT.2100 定义 PQ 与 HLG 两套参考非线性传递函数，系统色度 BT.2020，10/12bit（narrow 64–940 / full 0–1023），两套系统不得混用。PQ 由 EOTF 定义（display-referred，绝对亮度 0–10000 cd/m²，Dolby 提出，SMPTE ST 2084 标准化）；HLG 由 OETF 定义（scene-referred，相对亮度，BBC/NHK 提出，ARIB STD-B67 与 BT.2100 OETF 逐字一致）。
来源：ITU BT.2100-3 Table 4/5/9 + recommends 段；UHD Forum §7.1.2–7.1.4；UPM 论文 Table 4/5 转载。

**F2 · PQ EOTF 数学**：`L = 10000 × [max(V^(1/m2) − c1, 0) / (c2 − c3·V^(1/m2))]^(1/m1)`，常数 m1=2610/16384=0.1593017578125、m2=2523/4096×128=78.84375、c1=3424/4096=0.8359375、c2=2413/4096×32=18.8515625、c3=2392/4096×32=18.6875。锚点（中性灰）：100 nit≈0.508078、1000 nit≈0.751827、10000 nit=1.0。设计基于 Barten (1999) 对比敏感度模型，步长≈JND，10bit PQ 抑制全亮度范围 banding。10bit narrow range 算例：64 + 876×0.508078 ≈ code 509（回读 (509−64)/876≈0.507991 → ≈99.9 nit，舍入误差可见）。
来源：UPM Table 4（逐字）；colour-science eotf_ST2084 文档（常数 + Barten + doctest `eotf_ST2084(0.508078421517399)=100.0`）；Emby 技术页（code 509 算例，交叉核对用，不入断言证据）。

**F3 · HLG OETF 数学**：分段 `E' = √(3E)`（0≤E≤1/2）；`E' = a·ln(12E−b)+c`（1/2<E≤1），a=0.17883277、b=0.28466892、c=0.55991073。显示端系统 gamma： nominal peak 1000 cd/m² 时 γ=1.2；`γ = 1.2 + 0.42·log10(Lw/1000)`（Note 5e）。HLG 参考白 = 75% HLG 信号，1000 nit 屏上显示 203 nit、400 nit 屏上 101 nit（UHD Forum Table 1 原表含 400/600/1000/2000/4000 五列）——相对系统的直接证据：同一信号在不同峰值屏上绝对亮度不同。
来源：UPM Table 5（逐字）；UHD Forum §7.1.3 Table 1；ITU BT.2408 §3.2。

**F4 · HDR10 静态元数据**：HDR10 = PQ10 + ST 2086 MDCV（母带显示 primaries/白点 x,y + min/max 亮度）+ MaxCLL（全片最亮单像素）+ MaxFALL（最大帧平均亮度）。元数据供显示端做 color volume transform / tone mapping 决策；UHD Forum §7.2 原文示例：母带显示可用 DCI-P3 色域装在 BT.2020 容器里、亮度范围是 PQ 0–10000 的子集。**部分显示忽略部分或全部静态元数据**；直播节目 MaxCLL/MaxFALL 允许 0（未知，节目未结束无法统计）；母带实践可能产生 outlier 使 MaxCLL 虚高（有内容方用统计法修正）。动态元数据（HDR10+ ST 2094-40 / DV ST 2094-10）逐场景/逐帧。
来源：UHD Forum §7.2/7.2.1/7.2.2；AOSP HDR 页（KEY_HDR_STATIC_INFO / KEY_HDR10_PLUS_INFO 输出格式键）。

**F5 · Android HDR 播放链（官方口径）**：发现 = `Display.getHdrCapabilities`（HDR_TYPE_DOLBY_VISION/HDR10/HDR10_PLUS/HLG + desired max/min luminance）+ `CodecCapabilities.profileLevels`（HEVCProfileMain10HDR10、VP9Profile2HDR 等）；HDR10 管线 = MP4Extractor → HEVC 解码器（解析 SEI/SPS 母带元数据）→ 输出 format 携带 HDR 信息 → surface；Android 9+ 非 tunneled 模式也报告元数据；**Android 7.0 只定义 tunneled HDR 播放，非 tunneled 可能丢 HDR 信息被压平为 SDR color volume**；HWC2 传播 HDR 静态数据；HDMI EDID（CTA-861.3）EOTF 映射 ET_2 ST 2084→HDR10；合成 = 找包含所有图层的线性色彩空间 → 统一转换 → 混合 → 转显示信号。
来源：AOSP HDR 页全文（Discovery/Playback/HDR10 decoder pipeline/Hardware composition 各节）。

**F6 · Android 13 混合 SDR/HDR 合成**：libtonemap 使 HWC/SurfaceFlinger/app 的 tone mapping 一致（OEM 可共享自定义曲线）；HDR 在屏时屏幕亮度提升，SDR 图层按 sdrHdrRatioMap（LUT）调暗保持感知亮度不变；minimumHdrPercentOfScreen 控制高亮模式触发（Android 13 前固定 50%）；**dimming 可致 black crush（暗部码值坍缩），不可接受时必须 dither**；硬件不足时回退 GPU 合成（耗电）。
来源：AOSP Mixed SDR and HDR composition 页（OEM requirements/Configuration/Caveats/Issues 各节）。

**F7 · "发灰"权威解释**：PQ 信号送入期望 BT.709 输入的显示器 → "image will appear dim and washed out; colours will be desaturated and there will be some hue shifts"；需 3D LUT 下变换才能满意显示。tone mapping 定义 = 图像动态范围压缩（down-map HDR→SDR）；inverse tone mapping = 扩展（up-map）；hard clip vs soft clip 语义区分。
来源：ITU BT.2408 §3.1 + §5 Definitions。

**F8 · 库内既有覆盖（repo 证据）**：流媒体 §5.2 HDR 格式对比表（HDR10/HLG/HDR10+/DV）、§5.3 Android 链路（KEY_HDR_STATIC_INFO、getHdrCapabilities、HWC/GPU tone mapping、"8bit FBO 后丢失高光，再 tone mapping 已经晚了"）；色彩管理 §1.5（PQ 0–10000 nit、RGBA16F、算子名）；GPU图像处理算法（tone mapping 须线性 RGB、10bit→8bit 后 dither）。
来源：repo:02-解码与播放链路/流媒体与实时采集.md §5；repo:03-图形与GPU工程/色彩管理与采样滤波.md §1.5；repo:07-3D渲染与算法实现/GPU图像处理算法.md。

## 5. 争议与边界（如实登记）

- **HLG 兼容性边界**：UHD Forum 明确 HLG 向后兼容**仅针对 SDR/BT.2020 WCG 显示，不针对仅 BT.709 的显示**（BT.709 屏会去饱和+色相偏移，BT.2408 §3.2.1 同口径）。L03/V23 的"兼容 SDR"表述需加此边界——**本批不改 V23 文本**（属既有断言修订，走 KCR 人工裁决），L19 正文按精确口径写并显式注明与 L03 概览的关系。
- **TextureView 8bit / SurfaceView 10bit**：仅二手来源（知乎转述 AOSP），官方抓取文本未含此句 → **不入断言**，登记为未解决问题 U1。
- **MaxCLL 虚高**：UHD Forum 指出 outlier 问题 → V65 附条件。
- **PQ 锚点舍入**：0.508/0.752 为 rounded 值，精确值 0.508078/0.751827 → 教材双精度标注。

## 6. 结论与未解决问题

结论：F1–F8 足以支撑 5 条新断言（V63–V67，open/low）与 L19 全部正文；外部证据链闭合 V23 的升级前置（升级本身留 G1）。
未解决：U1 TextureView/SurfaceView 位深差异的官方出处（候选研究，并入研究队列）；U2 BT.2100 英文原版 PDF 未直接抓取（现经官方阿文 docx + UPM 逐字转载 + UHD Forum 三重交叉，G1 核验时可选补英文原版）；U3 HLG 在 BT.709 屏的兼容度主观测试细节（EBU/RAI/IRT 测试，UHD Forum 引用，未读原文）。

## 7. 参考（登记映射）

| 来源 | 拟登记 id | type |
|---|---|---|
| AOSP HDR video | SRC-ANDROID-HDR | official_doc |
| AOSP Mixed SDR/HDR | SRC-ANDROID-MIXED-SDR-HDR | official_doc |
| ITU-R BT.2100-3 | SRC-ITU-BT2100 | spec |
| ITU-R BT.2408-3 | SRC-ITU-BT2408 | official_doc |
| UHD Forum Blue Book 3.2.0 | SRC-UHDF-BLUEBOOK | official_doc |
| colour-science eotf_ST2084 | SRC-COLOUR-ST2084 | official_doc |
| UPM 论文（BT.2100 表转载） | SRC-UPM-BT2100-TABLES | paper |
| 流媒体与实时采集 §5 | SRC-RN-STREAMING | repo_doc（新登记） |