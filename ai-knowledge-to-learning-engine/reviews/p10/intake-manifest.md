---
doc_id: P10-INTAKE-MANIFEST
type: review-material
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# P10 端到端验收 · INTAKE 资料清单（RUN-2026-11-20-p10-hdr）

> 批次主题：**HDR 视频渲染**（PQ/HLG 传递函数、HDR10 元数据、Android HDR 播放链、tone mapping）。
> 目标产物：L19《HDR 视频渲染》教材 + 配套断言/来源/概念/术语。run 状态见 `.agent/runs/RUN-2026-11-20-p10-hdr.json`。

## 1. 查重结论（先查已有知识，再研究）

全库 grep `HDR|PQ|HLG|BT.2020|tone mapping|色调映射|高动态`：**151 处命中**，现有覆盖为**概览层、分散**：

| 位置 | 覆盖程度 |
|---|---|
| L03《色彩与显示范围》§4.4 | PQ/HLG 一句话对比表 + 渲染四要点转述（objective ③"说出 PQ 与 HLG 的适用场景"） |
| 02-解码与播放链路/流媒体与实时采集.md §5 | HDR 格式对比表、Android 链路要点、KEY_HDR_STATIC_INFO、8bit FBO 陷阱（参考文档层，无教学展开） |
| 03-图形与GPU工程/色彩管理与采样滤波.md §1.5 | PQ 0–10000 nit / HLG / RGBA16F / tone mapping 算子名（Reinhard/ACES/Filmic/AgX） |
| V23（open/low） | "PQ 绝对亮度映射（0–10000 nit）…HLG 相对、兼容 SDR"——**无外部权威来源支撑**（evidence 仅 repo_doc） |
| source-registry | **0 条 HDR 专属外部来源**（无 BT.2100/ST 2084 条目） |

**差异化定位（L19 不重复 L03）**：L03 回答"HDR 是什么、三字段怎么读"；L19 回答"**PQ 曲线怎么算、元数据怎么帮显示端决策、Android 链路哪一环丢了信息会发灰、tone mapping 为什么必须在线性光做**"——渲染侧管线深潜 + 可复算的数学 + 可定位的故障链。

## 2. 输入资料清单（一批 7 份外部 + 3 份库内）

外部（全部真实抓取/检索核实，accessed 2026-11-21）：
1. AOSP《HDR video》官方页（source.android.com/docs/core/display/hdr，经 google.cn 镜像全文抓取）
2. AOSP《Mixed SDR and HDR composition》官方页（source.android.com/docs/core/display/mixed-sdr-hdr，检索全文提取）
3. ITU-R BT.2100-3 (2025/02)（itu.int 官方 docx 提取；rec 页直接抓取被拒，内容经官方文档镜像核实）
4. ITU-R BT.2408-3 (2019) 报告（itu.int 官方 docx 提取，§3.1 PQ→BT.709 发灰权威描述）
5. Ultra HD Forum Blue Book v3.2.0（ultrahdforum.org 官方 PDF 提取，§7.1/7.2 PQ10/HLG10/HDR10 定义与元数据）
6. colour-science 官方文档 eotf_ST2084（colour.readthedocs.io，常数 + Barten 模型 + doctest 100nit 锚点）
7. UPM 硕士论文（oa.upm.es/48645，逐字转载 BT.2100 Table 4/5：PQ 常数 + HLG a/b/c + 系统 gamma 公式）

库内（repo_doc）：
8. 02-解码与播放链路/流媒体与实时采集.md §5（**需新登记 SRC-RN-STREAMING**，现无来源条目）
9. 03-图形与GPU工程/色彩管理与采样滤波.md §1.5（SRC-RN-COLORMGMT 已有）
10. 07-3D渲染与算法实现/GPU图像处理算法.md（SRC-RN-IMGALGO 已有，线性光/tone mapping 位置）

## 3. 范围边界

- **做**：PQ/HLG 编码逻辑与关键数学、HDR10 静态元数据、Android 播放链（发现→解码→合成→显示）、tone mapping 原理与故障定位、L19 教材 + 练习。
- **不做**：杜比视界/HDR10+ 动态元数据深潜（仅对比表提及）、HDR 拍摄/制作侧、AV1（流媒体 §5 已有）、新交互实验（无绑定 lab，照 L10/L12 先例）、pilot 层纳入（照 L18 先例，quiz 待纳入后补建）。
- **断言纪律**：新断言 V63 起默认 open/low；不升级任何既有断言（V23 的升级属 G1 人工裁决，本批只补外部证据链）。