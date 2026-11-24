---
doc_id: G2-L10-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L10《显式 API 与同步》新写（P8-MVP 后教材生产恢复第一篇）

> 本材料供 G2 人工审核使用。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L10-显式API与同步.md`（0 → 约 210 行，无绑定实验，工程机制型 + 对比边界型混合结构）。
- 结构：三故障钩子（偶发闪烁/首帧黑屏/退出崩溃，源 §5.5）→ 出租车/自驾类比（边界：错误延迟偶发、不自动更快）→ §4.1 五维责任转移表（objective ①）→ §4.2 同步三件套 + 帧环（objective ②，checkpoint ①）→ §4.3 三类 barrier + 可见性推导 + 六行故障表（objective ③）→ §4.4 RenderPass load/store + subpass（接 L09 带宽账，兑现 L09"L10 展开"承诺）→ §4.5 PSO 构成与治理（checkpoint ②）→ §5 PSO 组合账（教学算例标注）+ 帧环资源形态 → §6 排查现场（验证层 + RenderDoc）+ 6 误区 → §7 五项走查清单 → §8 因果链回忆 → §9 checkpoint 两题 → §10 桥 L11 → §11 术语与断言状态。
- 联动：L09 §10 桥句由"教材页待建"改直链 L10；publish boundary 断言 75→76。

## 2. 新断言登记（默认 open/low，升级待 G1 人工裁决）

| ID | 内容概要 | evidence | conditions |
|---|---|---|---|
| V39 | 显式模型五维责任转移；收益=可预测性+多线程 | SRC-RN-EXPLICIT-API §1/§3.2 + SRC-RN-INTERVIEW-VK §0/Q1/Q2 | Vulkan 不自动更快（Q2 ⚠️） |
| V40 | 三件套语义 + 帧环结构 + frames in flight 2–3 | 同上 §4 + §2.1/§2.3/Q3 | 车载 2 帧属平台取舍；vkDeviceWaitIdle 非替代品 |
| V41 | 三类 barrier（顺序/可见性/布局）+ 缺失/过度后果 + tiling 创建时属性 | 同上 §5/§8.3 + §2.2/Q4 | TBDR 布局转换代价因实现而异 |
| V42 | PSO 八项构成/不可变/创建成本区间/治理/缓存绑定 | 同上 §7 + §1.1/§4 | 耗时为源给区间；缓存跨版本可能失效 |

复用断言挂接 L10：V07（verified/medium）、E02（verified/medium）、V35（open/low）、V36（open/low）。来源新增：SRC-RN-EXPLICIT-API、SRC-RN-INTERVIEW-VK（反向索引已同步）。review_gate 实测 **59 claims（18 verified / 34 open / 7 conditional）误标 0**。

## 3. 独立审读结论（只读换人子代理）

**首轮：acceptable = false（0 blocker / 2 major / 9 minor），一轮修订。**

- major 2 条：① input attachment 只写收益未写限制（布局/格式匹配、不能同时作颜色附件、不能任意采样）；② RenderPass/Subpass 首现无一句话解释。**均已修复**。
- minor 9 条（术语计数、车载 2 帧 caveat 与 ⚠️ 标注口径、PSO 两性质归因分开、治理五项取舍注明 + 缓存失效条件转述、UBO/specialization constants 首现解释、V39/V41 挂接精度、binary semaphore 限定、桥句 DAG/aliasing 短释）——**全部修复**。
- 审读专项确认：四张表与源逐字一致；帧环与面试库 §2.3 一致；全部锚点有效；教学算例标注与算术正确；objectives/checkpoint 与 course.json 逐字一致；L11 前置假设实质覆盖；无借挂；V07/E02 medium 置信度如实标注。
- 十维度：9 ✓ + 1 部分（新概念不突现，修复后补齐）。亮点：§4.3 可见性推导为"不复制但展开"范本；数字纪律执行到位；追溯链完整。

## 4. 门禁实测（修复后复跑，见 CHANGELOG 2026-11-20 L10 条目）

build / validate（12 checks）/ arc / publish boundary / review_gate / registry 一致性——实测数字以 CHANGELOG 留痕为准。

## 5. G2 人工判定（待填——AI 不自评）

| 项 | 待人工填写 |
|---|---|
| G2 对本篇的判定（通过 / 有条件通过 / 退回修订） | |
| 评分（参照 review-report.md 维度体系） | |
| 对审读修复的意见 | |
| 备注 | |

## 6. 边界

- 未 commit/push；未改任何既有断言状态；stash 原样（B12）；L10 不在 pilot course.json，quiz 待纳入 pilot 后按 validate §10 补建（与 L03–L09 先例一致）。
- 依据：两份源文档逐条对源 + 质量规范十维度 + L01 标杆 + 独立审读报告（本文件 §3 摘要）。