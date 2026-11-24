---
doc_id: G2-L12-DEEPENING
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · L12《系统合成与显示》新写

> 供 G2 人工审核。**AI 不自评、不填分数**；审读结论只作线索。

## 1. 范围与产出

- 新写 `courses/video-rendering-journey/lessons/L12-系统合成与显示.md`（0 → 约 180 行，无绑定实验，工程机制型）。
- 结构：双场景钩子（延迟慢半拍/撕裂）→ 快递分拣类比（三层边界声明）→ §4.1 合成器/HWC 职责 + 端到端 ASCII 链路 + 三阶段瓶颈表（objective ①）→ §4.2 撕裂相位推导（标注教学展开）+ 双/三缓冲交易 + Jank≠pacing（objective ②/checkpoint ②）→ §4.3 overlay 路由判据 + SurfaceView/TextureView 五行表（取舍注明）+ 数字纪律（objective ③/checkpoint ①）→ §4.4 智驾数据入画与兜底路径 → §5 BufferQueue 三态 + 延迟分段账（源不给固定数字）→ §6 排查现场 + 5 误区 → §7 四项决策/观察练习 → 桥 L13。
- 联动：publish boundary 断言 76→77。

## 2. 新断言登记（open/low）

| ID | 内容概要 | evidence | conditions |
|---|---|---|---|
| V43 | 合成器选路（overlay/GPU 回退）+ 三阶段职责瓶颈 | SRC-RN-GPU-BASE §3.1/§3.2 | 合成器实现因平台而异 |
| V44 | 双缓冲+VSync 治撕裂；三缓冲交易；pacing 定义；Jank≠pacing | SRC-RN-GPU-BASE §3.3 | 延迟代价依场景（源 ⚠️） |
| V45 | 纯显示优先 overlay；SurfaceView/TextureView 对应与选择原则 | SRC-RN-GPU-BASE §3.4 + SRC-RN-DECODE-PIPELINE §6.2/§6.3 | 延迟数值带设备/版本条件；绝对化表述错误 |

复用挂接 L12：V34（open/low）、C01（conditional，条件按台账原文转述）。review_gate 实测 **62 claims（18v/37o/7c）误标 0**。

## 3. 独立审读结论（只读换人子代理）

**首轮：acceptable = true（0 blocker / 1 major / 6 minor），小修一轮。**

- major 1 条：§1 钩子撕裂方向（上旧下新）与 §4.2 推导矛盾——**已修复**（钩子改"上半截旧、下半截新"）。
- minor 6 条：五行表取舍注明（源另有线程安全行）、撕裂推导标注教学展开、"不透明"判据超源口径改"通常无需复杂变换"、§11 C01 条件按台账原文、Swapchain 首现补释、§2 V35 挂接改纯 L08 链接——**全部修复**。
- 专项确认：ASCII 链路忠实重组源 mermaid 无新增环节；三阶段表逐字对应；11 个锚点全有效；objectives/checkpoint 逐字一致；数字纪律被审读评为"全书示范级"（经验区间/分段账/⚠️ 条件贯穿）。
- 十维度：9 ✓ + 1 部分（Swapchain 首现，修复后补齐）。

## 4. 门禁实测

见 CHANGELOG 2026-11-20 L12 条目（build/validate 12 checks/arc/publish/review_gate/registry）。

## 5. G2 人工判定（待填——AI 不自评）

| 项 | 待人工填写 |
|---|---|
| G2 判定（通过 / 有条件通过 / 退回修订） | |
| 评分 | |
| 备注 | |

## 6. 边界

未 commit/push；未改既有断言状态；stash 原样；L12 不在 pilot course.json（quiz 待纳入后补建）。