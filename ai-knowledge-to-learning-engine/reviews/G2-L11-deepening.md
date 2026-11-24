---
doc_id: G2-L11-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第三篇 L11《RenderGraph 与资源生命周期》深化（2026-11-20）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评、不宣布通过。
> **深化方式**：主会话执笔，独立子代理审读（只读换人、逐条对源）。改动一律未 commit。

## 1. 深化摘要

- **L11 正文**：85 → 193 行（工程机制型：问题→失控场景→机制→边界→案例→实验）。frontmatter **objectives 对齐两层 course.json**（消除三层措辞漂移），source_documents 补显式API §6 与概念引入说明。
- **配套数据（四处联动）**：两层 `course.json` L11 checkpoint 各补第 3 题「RenderGraph 主要解决什么问题？」（quiz Q3 原已存在，claim_ids=[E04]）；正文 §9 同步三题。
- **断言纪律**：未新增断言；**P06 三处齐挂补全**（ledger used_by 原已含 L11 → frontmatter claims +P06 + §11 状态说明；正文引用 40% 数字一律带 [测试数据-仅供参考]）；C06 conditional、E04 附条件如实；quiz claim_ids {C06,E04} ⊆ claims。
- **未新增断言**（newClaims=[]）；无任何 claim 状态变化。

## 2. 独立审读原始结论

- **acceptable = true，修订 0 轮**；**52 处技术表述全部可溯源**。
- 十维度全 ✓；亮点：40%+（主文档实测参考，带标签）与 33%（教学算例）的「来源与口径分离、不互相冒充」被点名为引用纪律示范；「Pass≈RenderPass 阶段 / RenderPass≠RenderGraph」三层辨析补上主文档未明说的一句；五个锚点全部通过 slugify 复算。

## 3. 审读发现的 8 条 minor 及修复对照（全部已修，修复后门禁复跑通过）

| # | 审读发现 | 修复 |
|---|---|---|
| ① | §1「都只在特定机型上复现」无直接出处 | 改引显式API §5.5 典型表现（画面偶尔闪烁/旧帧），删除无据断言 |
| ② | L08 链接文本承诺 §2.3 但 href 无锚点；L06 行无链接 | L08 链接补 #23-管线与状态；L06 行补课内链接 |
| ③ | 工具名截断「Nsight Timeline」 | 改全名「Nsight Graphics Timeline」（主文档 §2.3 原文） |
| ④ | 层次表 RenderPass 行较源漏「与同步」二字 | 对齐源文档「声明与同步」 |
| ⑤ | 写→读/写→写细分置于 §2.1 引用后，细分实际出自 labs.json | 标注「细分口径见 rendergraph-dag 实验的依赖边定义」 |
| ⑥ | 主文档 aliasing 示例 Frame 1-3/4-6 被静默改写为 Pass 1–3/4–6 | 加注「主文档用 Frame 口径；transient 按 Pass 区间表述是同一结构，沿用 lab 口径并如实注明」 |
| ⑦ | 公式以行内代码呈现未用 $$…$$；lab formula 未入正文 | §5 升级 $$…$$ 展示（lab formula 字段原文）+ 峰值公式三件套保留 |
| ⑧ | 跨层差异：ledger P06.used_by 含 L11 但 frontmatter 未挂、§11 未提 P06 | frontmatter claims +P06；§11 补状态说明（open，contested，40% 待逐案核验） |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**69 documents / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards / 2530 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**5 篇 · OK**
- review_gate：**37 claims 误标 0**
- test_publish_boundary：**11 tests OK**

## 5. 待人工事项

1. **G2 评分**（L02/L06/L11 三篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. P06（open，contested）与 C06（conditional）的升级均待逐案实证；P02 同。
