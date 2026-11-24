---
id: L19
course: video-rendering-journey
title: HDR 视频渲染
prerequisites: [L03, L12, L14]
objectives:
  - 区分 PQ 与 HLG 的编码逻辑与适用场景，读懂 PQ EOTF 的关键锚点
  - 解释 HDR10 静态元数据（MaxCLL/MaxFALL/母带显示）如何参与 tone mapping 决策
  - 沿 Android HDR 播放链定位“画面发灰”的丢失环节
source_documents:
  - 02-解码与播放链路/流媒体与实时采集.md#5-10bithdr-与-av1
  - 02-解码与播放链路/流媒体与实时采集.md#53-android-上的-hdr-链路
  - 03-图形与GPU工程/色彩管理与采样滤波.md#15-hdr
claims: [V23, V63, V64, V65, V66, V67]
status: draft
---

# HDR 视频渲染

> **本章回答**：为什么同一部 HDR 电影，有的屏幕鲜艳通透，有的屏幕"灰蒙蒙一片"？
> **写作纪律**：正文用自己的语言展开推导，权威定义与完整细节链接主文档锚点与外部标准；陌生术语首次出现给出一句话解释；新断言默认 open/low，升级待 G1。
> **路线位置**：主课程 U4 扩展课（prerequisites：L03、L12、L14），建议 45 分钟。本课无绑定实验（`tools/labs.json` 无 L19 实验），动手形式为 §7 的四项核查与算例练习。本课是主课程 next 链的终点（L18 延伸而来）。

## 1. 从一个问题开始

同一部 HDR 电影：旗舰手机上阳光刺眼、暗部有细节；接到车载屏上却像蒙了一层灰——亮部不亮、颜色发淡。屏幕没坏，片源也没坏。数字摆出来就明白张力在哪：HDR 内容的亮度容器上限是 **10000 nit**（cd/m²，亮度单位），母带常在 **1000 nit** 监视器上制作（BT.2408 §3.2：1000 cd/m² nominal peak 适合典型制作环境），而 SDR 时代的参考亮度只有 **100 nit** 量级，车载屏峰值往往也只有几百 nit（车载屏约束，[色彩管理 §1.5](../../../03-图形与GPU工程/色彩管理与采样滤波.md#15-hdr)）（`V63`/`V64`，AOSP HDR 官方页口径）。

内容说的"亮度语言"和屏幕能发的"亮度能力"不匹配时，谁负责翻译？翻译错了会怎样？L03 给过概览（PQ 绝对、HLG 相对），本章把这条链拆到能定位故障的精度：**编码曲线怎么算 → 元数据怎么帮屏幕决策 → Android 链路哪一环会丢信息 → tone mapping 为什么必须那样做**。

## 2. 学习前提

- **L03《色彩与显示范围》**：三字段（standard 色域 / transfer 传递函数 / range 数值范围）与线性工作流；"发灰"的两种 SDR 病因（range 错、双重 gamma）。本章的"发灰"是第三种病因——HDR 信息在链路中丢失。
- **L12《系统合成与显示》**：SurfaceFlinger/HWC 合成链与 overlay 路由。HDR 帧最终也要走这条合成链，只是多了亮度适配一步。
- **L14《光照、材质与图像算法》**：后处理顺序与 tone mapping 的位置（后处理 Pass → tone mapping → sRGB 编码 → dither → 写 8bit）。含 Bloom 的完整顺序（HDR→Bloom→ToneMap→LUT→AA→UI）见[面试库 04-3D图形学与几何原理](../../../06-面试知识库/车载渲染引擎/04-3D图形学与几何原理.md)。本章解释 tone mapping 这一步"为什么必须在线性光做"。

## 3. 直观模型：亮度货币与兑换窗口

把亮度想成货币（`V63`/`V65`/`V67` 的教学类比）：

- **PQ 是绝对金本位**：每个码值直接标价"多少 nit"，0.508 就是 100 nit，不随屏幕变——像印着面额的钞票。
- **HLG 是相对购买力**：码值只说"比参考白亮多少倍"，到了哪块屏就按那块屏的峰值"汇率"折算——像只标相对价值的凭证。
- **元数据是报关单**：MaxCLL/MaxFALL/母带显示信息告诉屏幕"这批货整体有多亮、在哪做的"，屏幕据此决定怎么兑换。
- **tone mapping 是兑换窗口**：内容亮度超出屏幕能力时，把超出部分非线性压缩进来，而不是等比缩水。

**类比边界**：只覆盖亮度一维。色域转换（gamut mapping，BT.2020→屏幕原生色域）是独立的另一步，两者常一起发生但机制不同；PQ 的"绝对"是对参考显示而言，真实屏幕峰值各异，仍需要适配（这正是元数据与 tone mapping 存在的原因）。

## 4. 核心概念与原理

### 4.1 PQ 与 HLG：两套不能混用的系统

ITU-R BT.2100 定义了两套参考传递系统，**制作与显示必须全程用同一套，不得混用**（`V63`，BT.2100 Table 4/5；[流媒体 §5.2](../../../02-解码与播放链路/流媒体与实时采集.md#52-hdr-格式)）：

| 维度 | PQ | HLG |
|---|---|---|
| 标准编号 | SMPTE ST 2084（EOTF） | ARIB STD-B67（OETF，与 BT.2100 逐字一致） |
| 定义侧 | EOTF（显示端解码曲线） | OETF（拍摄端编码曲线） |
| 亮度参照 | display-referred，**绝对** 0–10000 nit | scene-referred，**相对**（随屏幕峰值折算） |
| 提出者 | Dolby | BBC + NHK |
| 元数据 | 需要（HDR10 静态 / HDR10+、DV 动态） | BT.2100 系统本身无需元数据 |
| 典型场景 | 流媒体、电影母带 | 广播、直播 |

系统色度都是 **BT.2020**（宽色域标准，L03 三字段中 standard 维的 HDR 取值），位深 **10/12 bit**（10 bit narrow range 码值 64–940，共 876 级；full range 0–1023）。

**HLG 的兼容边界要说精确**：L03 概览说"HLG 相对亮度、兼容 SDR"（`V23`，open）。精确口径是——兼容**仅针对 SDR/BT.2020 宽色域显示**；只支持 BT.709 的 SDR 屏会看到去饱和 + 色相偏移的画面（UHD Forum Blue Book §7.1.3、ITU BT.2408 §3.2.1）。`V23` 的边界修订与升级已列入 G1 裁决（KCR-2026-11-001 I19），本章按精确口径表述。

HLG 的"相对"有直接证据：75% HLG 信号（HDR 参考白）在 1000 nit 屏上显示 **203 nit**，在 400 nit 屏上只有 101 nit——同一码值，绝对亮度随屏而变（UHD Forum Table 1）。显示端系统 gamma 也随峰值调整：1000 nit 时 γ=1.2，`γ = 1.2 + 0.42·log10(Lw/1000)`（BT.2100 Note 5e）。

**checkpoint ①**：PQ 与 HLG 为什么不能混用？各自的亮度参照是什么？

### 4.2 PQ EOTF：把 10000 nit 装进 10 bit

PQ 的核心是一条把归一化信号 V 映射到绝对亮度 L 的曲线（`V64`，ST 2084:2014；colour-science 官方文档可复算）：

$$L = 10000 \times \left[ \frac{\max\left(V^{1/m_2} - c_1,\ 0\right)}{c_2 - c_3 \cdot V^{1/m_2}} \right]^{1/m_1}$$

常数（标准定死）：m1 = 2610/16384 ≈ 0.1593017578125，m2 = 78.84375，c1 = 0.8359375，c2 = 18.8515625，c3 = 18.6875。

- **符号含义**：V 是 [0,1] 归一化编码值（中性灰时三通道同值）；L 是参考显示上的绝对亮度（nit）；五个常数是标准定死的曲线形状参数。
- **数值算例**（锚点，精确值→舍入值）：V=0.508078 → **100 nit**；V=0.751827 → **1000 nit**；V=1.0 → **10000 nit**。10 bit narrow range 下 100 nit 的码值：64 + 876×0.508078 ≈ **509**；回读 (509−64)/876 ≈ 0.507991 → ≈99.9 nit——舍入误差可见，这是有限精度的正常代价（算例口径：Emby 技术页交叉核对，常数以 ST 2084 为准）。
- **工程后果**：100 nit（SDR 参考白量级）只占码值范围的一半，1000 nit 占到 3/4——**大部分码值分给了中低亮度**。为什么？PQ 基于 Barten (1999) 对比敏感度模型设计，每个量化步长≈人眼刚好能分辨的亮度差（JND）：暗部人眼敏感，给细刻度；亮部人眼迟钝，给粗刻度。于是 **10 bit PQ 就能在全亮度范围抑制 banding**——呼应 L03"10-bit 要全链路才有意义"：曲线再精，中间环节截成 8 bit 照样出色带。

### 4.3 HDR10 元数据三件套：屏幕的决策依据

PQ 是绝对的，但屏幕峰值各异：1000 nit 母带内容放到 400 nit 屏上，哪些高光该压、压多少？光看像素值不够——屏幕需要知道"内容整体有多亮"。这就是静态元数据（`V65`，UHD Forum §7.2；HDR10 = PQ10 + 以下三件套）：

| 元数据 | 定义 | 告诉显示端什么 |
|---|---|---|
| **ST 2086 MDCV**（母带显示色彩体积） | 制作监视器的 primaries/白点 x,y 坐标 + min/max 亮度 | 创作意图是在什么能力的屏上定的（UHD Forum §7.2 示例：P3 色域、1000 nit 母带屏装在 BT.2020 容器里） |
| **MaxCLL** | 全片最亮**单像素**亮度 | 高光极值在哪，超出屏幕能力的部分有多少 |
| **MaxFALL** | 全片最大**帧平均**亮度 | 整体亮度分布——避免把"一帧闪电"误判为"全片很亮" |

三个如实的边界（都来自权威原文）：**部分显示会忽略部分或全部静态元数据**；**直播节目 MaxCLL/MaxFALL 允许填 0**（节目没结束，统计不出来）；母带实践可能产生 outlier 使 MaxCLL 虚高（有内容方改用统计法）。动态元数据（HDR10+ / Dolby Vision）逐场景/逐帧给亮度信息，Android 解码输出以 `KEY_HDR_STATIC_INFO`（静态）/ `KEY_HDR10_PLUS_INFO`（动态，逐帧可变）携带（AOSP HDR 页）。

### 4.4 Android HDR 播放链：信息逐环传递

官方口径的完整链路（`V66`，AOSP HDR 页 + [流媒体 §5.3](../../../02-解码与播放链路/流媒体与实时采集.md#53-android-上的-hdr-链路)）：

```
能力发现   Display.getHdrCapabilities() → HDR_TYPE_HDR10/HLG/HDR10_PLUS/DOLBY_VISION
           + desired max/min luminance；CodecCapabilities.profileLevels
           → HEVCProfileMain10HDR10 / VP9Profile2HDR …
    ↓
解封装     MP4 Extractor（HDR10）/ WebM Extractor（VP9）
    ↓
硬解码     HEVC 解码器解析 SEI/SPS（补充增强信息/序列参数集）里的母带元数据
    ↓
输出格式   output format 携带 KEY_HDR_STATIC_INFO（Android 9+ 非 tunneled 也报告）
    ↓
Surface    buffer 带色彩描述（DataSpace：standard × transfer × range 三维标记）
    ↓
合成       SurfaceFlinger / HWC2（传播 HDR 静态数据；Android 13 libtonemap 统一
           HWC/SF/app 的 tone mapping 曲线）
    ↓
显示       面板按自身峰值适配（EDID——显示器能力自描述块，CTA-861.3 声明，ST 2084 → HDR10）
```

两个官方明示的坑（先弄清 **tunneled**：隧道模式——解码器输出绕过应用渲染循环、经专用通道直达显示硬件的播放模式，见 AOSP Multimedia Tunneling 文档；非 tunneled 则是应用拿解码帧再提交 Surface 的常规路径。两者决定 HDR 信息由谁持有）：

1. **tunneled 与非 tunneled 的差异**：Android 7.0 只定义了 tunneled 模式的 HDR 播放；**非 tunneled 解码可能丢失 HDR 信息，内容被压平进 SDR color volume**（AOSP 原话口径）——这是"发灰"的官方病因之一。Android 9+ 非 tunneled 也报告元数据，但播放保证仍依设备实现。
2. **混合 SDR/HDR 合成**（Android 13，AOSP Mixed SDR/HDR 页）：HDR 内容在屏时屏幕亮度提升，同屏的 SDR 图层按 `sdrHdrRatioMap`（LUT）**调暗**以保持感知亮度不变；`minimumHdrPercentOfScreen` 控制高亮模式触发（13 之前固定 50%）。代价：dimming 可能把暗部码值坍缩出 **black crush**，不可接受时必须 **dither**；硬件不足时回退 GPU 合成（耗电）。

**checkpoint ②**：HDR10 的 MaxCLL/MaxFALL/母带显示元数据各告诉显示端什么？

### 4.5 tone mapping：为什么必须在线性光、为什么非线性

**"发灰"的权威解释**（`V67`，ITU BT.2408 §3.1 原话口径）：PQ 信号送入期望 BT.709 输入的显示，画面会 **dim and washed out**（暗且发白）、颜色去饱和、还有色相偏移。原因用 §4.2 的锚点一眼看穿：PQ 的 0.5 是 ~100 nit 的"绝对标价"，被当成 SDR gamma 解读后，亮度语义整个错位——不是屏幕不够亮，是**翻译错了曲线**。

tone mapping（色调映射）= 图像动态范围压缩（down-map，HDR→SDR；BT.2408 §5 定义）。两条硬道理：

- **必须非线性**：教学算例（显式标注为推导）——4000 nit 内容 → 1000 nit 屏，等比 ÷4 会把 100 nit 的人脸压到 25 nit（太暗看不清）；正确做法是暗部基本不动、高光大幅压缩。算子族：Reinhard / ACES / Filmic / AgX（[色彩管理 §1.5](../../../03-图形与GPU工程/色彩管理与采样滤波.md#15-hdr)），广播侧参考 ITU-R BT.2390；选择依平台与内容，无统一"正确观感"。
- **必须在线性光做**：亮度压缩是对物理光强的操作，gamma 空间的数值不是光强（L03 线性工作流、L14 后处理顺序的同一原理；[GPU图像处理算法](../../../07-3D渲染与算法实现/GPU图像处理算法.md) 明确色调映射须线性 RGB）。推论：**8 bit FBO 先截断了高光，再 tone mapping 已经晚了**——信息在截断那一刻就没了（流媒体 §5.3 原话口径）。所以 HDR 渲染目标用 RGBA16F 这类浮点格式（L03 §4.4），tone mapping 之后才量化到输出位深，必要时 dither。

顺带分清 **hard clip**（超过阈值直接截断，制作监看常用以暴露超范围像素）与 tone mapping（soft clip，平滑压缩）——语义不同，用途不同（BT.2408 §3.1/§5）。

## 5. 全链路与数据形态

从制作到眼睛的完整链（本章知识汇总图）：

```
制作端                    分发            播放端（Android）                 显示端
场景光 → PQ/HLG 编码   →  码流+元数据  →  解封装→硬解→format→Surface   →  合成适配 → 面板
（BT.2100 双系统选一）    （SEI/SPS/      （DataSpace 三维标记逐环传递）    （tone mapping
 + BT.2020 + 10/12bit     容器元数据）                                       + gamut mapping）
```

**参数丢失后果速查表**（每行可定位到断言/前课）：

| 丢失/错配 | 后果 | 依据 |
|---|---|---|
| transfer 丢失（PQ 被当 SDR gamma） | 发灰、去饱和、色相偏移 | `V67`（BT.2408 §3.1） |
| 非 tunneled 链路丢 HDR 信息 | 内容被压平进 SDR color volume | `V66`（AOSP HDR 页） |
| 色域未转换（BT.2020 当 BT.709） | 偏色/去饱和（反向错标——709 内容标成 2020/P3——才过饱和） | `V24` + [色彩管理](../../../03-图形与GPU工程/色彩管理与采样滤波.md) §1.6 |
| range 错配 | 对比度异常（黑不够黑/白不够白） | L03 §4.2（`V21`） |
| 8 bit 中间截断 | 高光丢失 + 暗部色带，后续 TM 无法挽回 | `V67`（流媒体 §5.3） |
| 元数据缺失/被忽略 | tone mapping 失去决策依据，只能默认曲线 | `V65`（UHD Forum §7.2） |

## 6. 工程现场与常见误区

**排查现场**（由 AOSP 官方链路与流媒体 §5.3 重组的教学案例）：车载播放器接 HDR10 片源，画面发灰。四步定位，每步有明确观测点：

1. **屏幕能力**：`Display.getHdrCapabilities()` 返回的 `getSupportedHdrTypes()` 是否含 `HDR_TYPE_HDR10`？desired luminance 是多少？——空数组 = 屏幕根本不支持，系统必然走 SDR 适配。
2. **解码输出**：output format 里有没有 `KEY_HDR_STATIC_INFO`？profile 是不是 `HEVCProfileMain10HDR10`？——没有 = 元数据在解码环节就没出来。
3. **色彩标记传递**：Surface buffer 的色彩描述（DataSpace/color aspects）是否逐环传到合成？——断在哪环，哪环就把 HDR 当 SDR。
4. **合成路径**：tunneled 还是非 tunneled？GPU 合成时 tone mapping 曲线是否生效（Android 13 libtonemap）？——非 tunneled 在老平台上可能直接压平 SDR。

常见误区：

- **"HDR 就是把亮度拉高。"** 错。是换了一套亮度编码语言（PQ 绝对/HLG 相对）+ 宽色域 + 高位深，选择由分发场景定（`V63`，L03 误区第五条的深化）。
- **"HLG 兼容任何 SDR 屏。"** 不精确。兼容仅限 SDR/BT.2020 宽色域屏；BT.709 屏去饱和 + 色相偏移（`V63` 条件，UHD Forum §7.1.3）。
- **"元数据缺失就播不了。"** 错。缺失/被忽略时仍可播放，只是 tone mapping 失去决策依据、效果打折（`V65` 条件）。
- **"tone mapping 在 gamma 空间做也行。"** 错。压缩的是物理光强，必须线性光；8 bit 先截断更是不可逆（`V67`）。
- **"换个 10 bit 屏就消色带。"** 不完整。要全链路 10 bit（L03 §Q8 同一结论）；PQ 曲线的 JND 设计只是让 10 bit 够用，不是让 8 bit 够用（`V64`）。

## 7. 动手练习

本课无绑定实验（`tools/labs.json` 无 L19 实验）；四项练习，每项"做什么→预期看到什么→对应哪个机制"：

1. **复算 PQ 锚点**：用 colour-science 库（`colour.models.eotf_ST2084(0.508078421517399)`）或按 §4.2 公式手算。预期：≈100.0 nit；再算 0.751827 → ≈1000 nit。对应：PQ 绝对亮度语义（`V64`）。
2. **读真实 HDR10 元数据**：用 ffprobe/mediainfo 打开任一 HDR10 文件，找 MaxCLL/MaxFALL/mastering display 三项。预期：三件套齐（或直播源为 0）；对照 §4.3 表说出每项含义。对应：`V65`。
3. **发灰定位走查**：给定"车载屏播 HDR10 发灰"场景，按 §6 四步写出每步的观测点与"若此处异常说明什么"。预期：能区分屏幕不支持/元数据未出/标记断链/合成压平四种病因。对应：`V66`/`V67`。
4. **tone mapping 位置决策**：画一条含 Bloom 的后处理链，标出 tone mapping 应在哪一步、用什么位深的缓冲。预期：TM 在 Bloom 之后、量化到 8 bit 之前，中间缓冲浮点/高位深，线性光域。对应：`V67` + L14 后处理顺序（含 Bloom 的完整链见 §2 面试库链接）。

## 8. 主动回忆

**BT.2100 双系统不得混用：PQ 绝对（0–10000 nit，EOTF 定义）/ HLG 相对（OETF 定义，兼容仅限 BT.2020 WCG SDR）（`V63`）→ PQ 锚点 100 nit≈0.508、1000 nit≈0.752，JND 步长让 10 bit 够用（`V64`）→ HDR10 三件套（MDCV/MaxCLL/MaxFALL）给显示端决策依据，可缺失可被忽略（`V65`）→ Android 链逐环传 DataSpace，非 tunneled 可能压平 SDR，13 起 libtonemap 统一 + SDR dimming（`V66`）→ PQ 被当 SDR 解读 = 发灰权威解释；TM 必须线性光 + 非线性压缩，8 bit 先截断已晚（`V67`）。**

再自问三个"为什么"：为什么 PQ 把一半码值给了 100 nit 以下？为什么 HLG 不需要元数据而 PQ 需要？为什么 black crush 要靠 dither 而不是提高亮度解决？

## 9. 自我检测

1. PQ 与 HLG 为什么不能混用？各自的亮度参照是什么？
2. HDR10 的 MaxCLL/MaxFALL/母带显示元数据各告诉显示端什么？
3. Android HDR 播放链上哪些环节可能丢失 HDR 信息导致发灰？

题目来源：`tools/course.json` L19 checkpoint（参考答案要点与断言挂接：Q1 → `V63`/§4.1，Q2 → `V65`/§4.3，Q3 → `V66`/`V67`/§4.4–4.5；quiz 文件待本课纳入 pilot 课程层后按 validate §10 规则补建，照 L18 先例）。

## 10. 下一章的桥

主课程 next 链到此收官。按叙事顺序回顾：**像素的形状（L01）→ 时刻（L02）→ 进 GPU 的路（L06）→ 多遍的组织（L11）→ 落屏的数学（L13）→ 显式合同（L10）→ 系统合成（L12）→ 光照与算法地图（L14）→ 证据链（L15）→ 表达（L16）→ 几何生产（L17）→ 质感公式（L18）→ HDR 显示（L19）**。一帧画面从文件到屏幕、从数学到质感、再到真实亮度世界的完整旅程闭环。继续深挖的方向在[知识缺口登记表](../../../00-导航与索引/知识缺口登记表.md)与本章研究队列（U1 TextureView/SurfaceView 位深官方出处、U2 BT.2100 英文原版核对、U3 HLG 兼容主观测试原文，见 `reviews/p10/G1-hdr-verification-queue.md`）；也可以回到[一帧画面的探索之旅](../../../00-导航与索引/一帧画面的探索之旅.md)，用四段式把整条链讲成一个 3 分钟项目故事（L16 的练习）。

## 11. 术语与延伸

- 本章术语：HDR、PQ、HLG、BT.2020、tone mapping、MaxCLL、DataSpace（权威定义在 `tools/glossary.json`，站点术语卡自动收录；MaxFALL 词条同组）。
- 机制细节：[流媒体 §5 10bit/HDR/AV1](../../../02-解码与播放链路/流媒体与实时采集.md#5-10bithdr-与-av1)（§5.2 格式对比 / §5.3 Android 链路）；[色彩管理 §1.5 HDR](../../../03-图形与GPU工程/色彩管理与采样滤波.md#15-hdr)（浮点 RT 与算子族）；tone mapping 的图像处理位置 → [GPU图像处理算法](../../../07-3D渲染与算法实现/GPU图像处理算法.md)。
- 外部权威源（本批新登记，accessed 2026-11-21）：ITU-R BT.2100（SRC-ITU-BT2100）/ BT.2408（SRC-ITU-BT2408）、AOSP HDR 与 Mixed SDR/HDR（SRC-ANDROID-HDR / SRC-ANDROID-MIXED-SDR-HDR）、UHD Forum Blue Book（SRC-UHDF-BLUEBOOK）、colour-science ST 2084 文档（SRC-COLOUR-ST2084）、UPM 论文 BT.2100 表转载（SRC-UPM-BT2100-TABLES）。
- 断言状态说明：`V63`–`V67` 为本轮新登记的 **open/low** 断言（升级待 G1 人工裁决，核验队列见 `reviews/p10/G1-hdr-verification-queue.md`；来源双向索引已同步）；`V23`（L03 登记的 PQ/HLG 概览）仍 **open/low**，其边界修订与升级申请见 KCR-2026-11-001 I19。正文结论以标准原文与主文档锚点为权威依据。