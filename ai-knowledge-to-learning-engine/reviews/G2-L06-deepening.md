---
doc_id: G2-L06-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第二篇 L06《纹理桥与零拷贝》深化（2026-11-20）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分（25/25/20/20/10，总分 ≥85 且事实/连贯各 ≥80%）由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评、不宣布通过。
> **深化方式**：主会话执笔（接续任务书 P7.2 推进指令），独立子代理审读（只读换人、逐条对源）。改动一律未 commit。

## 1. 深化摘要

- **L06 正文**：85 → 200 行（frontmatter 一字未动——claims 字段追加 E01 属三处齐挂扩展，见 §3-⑤）。结构对照 Gold Standard L01：开篇数字张力 → 前置唤起（L01/L02/L05 + 三术语一句话解释）→ 仓库+钥匙类比（附边界声明）→ §4 三步机制（updateTexImage/变换矩阵 → OES 三限制与第一道转换 Shader → PC/移动通路）→ §5 搬运账公式三件套 → §6 排查现场 + 5 误区 → §7 实验（frame-pipeline 四任务）→ §8 因果链 → §9 自我检测 → §10 桥（→L11）→ §11 术语与断言状态说明。
- **配套数据（四处联动）**：两层 `course.json`（tools/ 与 courses/video-rendering-journey/）L06 checkpoint 各补第 3 题「手机 SoC 的 CPU→GPU 数据通路走 PCIe 吗？」（quiz Q3 原已存在，claim_ids=[E02] ⊆ claims）；`evidence/claim-ledger.json` E01.used_by_lessons 增补 "L06"（正文 4 处引用 E01，按 L01 三处齐挂先例补 frontmatter claims + ledger 反向索引）；`web/content.js`、`.agent/indexes/document-registry.json` 由生成器重建（禁手改纪律未破）。
- **未新增断言**：newClaims=[]。正文重要结论全部由既有断言（V04/V05/C02/E02/P02）或主文档 ✅/⚠️ 锚点覆盖；P02 保持 **open/low（contested）**（B11 确认保留挂载），C02 保持 conditional，未发生任何状态升级。

## 2. 独立审读原始结论（审读员，非 G2 人工评分）

- **acceptable = true，修订 0 轮**。
- **逐条对源**：40 处技术表述，39 处溯源成功。亮点：五断言（V04/V05/C02/E02/P02）的状态、confidence、conditions、used_by 与 claim-ledger 逐字对上（含 P02=open/low contested + B11=D19 属实、C02 条件「需绑定 Surface」、E02 条件「先说平台」且正文表格确实先说平台）；三个锚点经仓库 validate_site.py 的 slugify 算法全部解析命中；labs.json 六阶段/四任务/selfTest/note 数字（8.3 MB、16.6 MB、「在移动端足以吃掉一帧预算」原话）逐字吻合，无编造数字；算术（8.29×30=249 已删、8.29×2=16.6、16.6×30=498、3.11 MB）全部正确。
- **十维度**：1 开篇 ✓ / 2 动机 ✓ / 3 前置 ✓ / 4 概念 部分（已修） / 5 因果 ✓ / 6 类比 ✓（边界声明覆盖两处失效点）/ 7 图解公式 ✓ / 8 案例 ✓ / 9 实践 ✓ / 10 桥 ✓（与 pilot course.json L06.next=L11 一致，且与 L02 §10 交棒语句闭环）。

## 3. 审读发现的 11 条 minor 及修复对照（全部已修，修复后门禁复跑通过）

| # | 审读发现（位置） | 修复 |
|---|---|---|
| ① | §7.2 标「✅已验证」无据（主文档 §7.2 标题无验证标记，§7.1/§7.4 才标 ✅） | 移除徽标，改为「内容由 V04（verified，Khronos 规范依据）背书」 |
| ② | 「实验代码 note 原文」张冠李戴（该句出自 frame-pipeline selfTest[1] 答案，note 是拷回带宽说明；2 处） | 两处改标「frame-pipeline 实验 selfTest」 |
| ③ | getTransformMatrix「旋转/裁剪」中「裁剪」超源（主文档 §3.2/§7.4 只写旋转；2 处） | 删「裁剪」，仅保留「旋转角度」（主文档口径） |
| ④ | §1 把解码输出按 RGBA 8.29 MB 计账、§6 沿用，与解码输出 YUV420 3.11 MB 口径松动 | §1 改两段账（YUV 3.11 读回 → RGBA 8.29 上传）；§6 改 CPU 经手账（3.11 + 8.29 ≈ 340 MB/s @30fps，含一次格式转换） |
| ⑤ | E01 簿记不同步：正文 4 处挂 E01，frontmatter claims 未含、ledger used_by 未收录 | frontmatter claims +E01；ledger E01.used_by_lessons +L06；registry 重建（L01 三处齐挂先例） |
| ⑥ | 实验任务 2 映射错位（标 §4.2，实为 §3/§5 内容） | 改「对应 §3 的两条路线对比与 §5 的搬运账」 |
| ⑦ | 实验显示名「一帧端到端链路实验」与 labs.json 标题《解码帧到纹理的所有权迁移实验》不一致 | 改用 labs.json 原标题（#/lab/frame-pipeline 链接本身有效） |
| ⑧ | BufferQueue/FBO/Effect Pass 首现无一句话解释 | 三处各补一句话（BufferQueue 所有权队列机制 / FBO 帧缓冲对象-离屏纹理 / Effect Pass 一轮特效着色器处理） |
| ⑨ | quiz 3 题与 checkpoint 2 题不齐、§9 来源行悬空 | 两层 course.json checkpoint 补第 3 题 + 正文 §9 补题 + 来源行改双层声明（四处联动补齐，validate §11 通过） |
| ⑩ | 小节引用全部为文档根链接、不带锚点（跳转精度弱于 L01/L02） | §2.2/§3/§3.2/§7.3/§8.3 升级为锚点链接（#22-…/#3-…/#32-…/#73-…/#83-…，validate 锚点解析全部通过） |
| ⑪ | Premultiplied Alpha 列入本章术语但正文未使用（收录而未用） | 移出「本章术语」，降为「延伸」条目并链术语表 |

## 4. 门禁实测（执行会话，修复后复跑，全 exit 0）

- build_site：**69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards / 2497 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**（含新增锚点解析与 quiz/checkpoint/claim 覆盖）
- check_chapter_arc：**5 篇 · OK**
- review_gate：**37 claims（verified 18 / open 12 / conditional 7；contested 4）conditional/contested 被标为 verified：无**
- test_publish_boundary：**Ran 11 tests — OK**

## 5. 待人工事项（不阻塞，登记）

1. **G2 评分**：本篇 + L02 一并由人工按 review-report.md 评分表填写；AI 不自评。
2. **L02 遗留 major（跨篇）**：labs.json pts-dts-timeline「同步约束」desc 与 `web/assets/app.js:2350`「DTS ≤ PTS 恒成立」静态句、与 L02 五帧表（B 帧 PTS 2/DTS 3）三处冲突——涉及实验前端文件，超出单篇正文授权范围，修法方向见 `reviews/G2-L02-deepening.md`，建议随 L11 一并裁决。
3. **P02 升级**：open/low → 更高状态需逐平台 buffer ownership + copy trace（对应研究队列 C 类证据），G1 人工裁决。
4. **objectives 三层措辞漂移**（L02 审读 minor 之一）属既有数据层事实，本轮未动 frontmatter，待人工统一。
