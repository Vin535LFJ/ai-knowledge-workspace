---
id: L10
course: video-rendering-journey
title: 显式 API 与同步
prerequisites: [L09]
objectives:
  - 对比 OpenGL 状态机与 Vulkan 显式模型
  - 区分 CPU-GPU 同步与 GPU-GPU 同步
  - 说明 barrier 缺少时会发生什么
source_documents:
  - 04-跨平台与高性能架构/显式API与同步原语.md#1-为什么需要显式-api
  - 04-跨平台与高性能架构/显式API与同步原语.md#4-同步三件套
  - 04-跨平台与高性能架构/显式API与同步原语.md#5-三类-barrier
  - 04-跨平台与高性能架构/显式API与同步原语.md#7-pso-与描述符
  - 06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#2-同步vulkan-面试的第一道分水岭
claims: [V07, V35, V36, E02, V39, V40, V41, V42]
status: draft
---

# 显式 API 与同步

> **本章回答**：同一条后处理链，OpenGL 下"就是能跑"，换到 Vulkan 为什么画面偶尔闪烁、首帧黑屏、退出崩溃？
> **写作纪律**：正文用自己的语言展开机制，权威定义与完整细节链接主文档锚点；陌生术语首次出现给出一句话解释。
> **路线位置**：主课程 U4 第 1 课（prerequisites：L09），建议 50 分钟。本章无绑定实验（`tools/labs.json` 无 L10 实验），动手形式为验证层 + RenderDoc 走查（§7）。

## 1. 从一个问题开始

L06 里你用 FBO 串过一条多 Pass 特效链：画到离屏纹理、再采样、再上屏。在 OpenGL 下你几乎没想过"顺序"这件事——`glBindFramebuffer` 换目标、绑定纹理、画，驱动把前后依赖都替你处理了。

现在把同一条链搬到 Vulkan。代码"看起来都对了"，运行起来却是一组诡异的故障（[主文档 §5.5 故障表](../../../04-跨平台与高性能架构/显式API与同步原语.md#55-常见同步错误)）：

- 画面**偶尔**闪烁一帧旧内容——不是每帧都错，重跑一遍又好了；
- **首帧黑屏**——之后一切正常；
- 退出时**崩溃**——渲染时明明没事。

这三个故障没有一个会稳定复现，也没有一个直接指向某行代码。主文档的一句话总结点破了原因：**barrier 写错不会立刻崩，只会偶发花屏——这才是它最难的地方**。OpenGL 里驱动替你猜依赖；Vulkan 把"猜"取消了，依赖要你自己说清楚——说漏了是竞态，说多了是 GPU 空转（断言 `V39`/`V41`）。

这一章回答三个问题：**显式模型到底把什么责任交给了你？CPU 等 GPU 和 GPU 等 GPU 为什么是两套原语？barrier 缺了（或多了）究竟发生什么？**

## 2. 学习前提

- **L08**：管线七阶段与 CPU/GPU 异步——你已经知道 CPU 可以领先 GPU 1–3 帧（Frame in flight，断言 `V35`），本章给"领先但不出事"配上正式的同步工具。
- **L09**：TBDR 与 tile memory——`loadOp=LOAD` 为什么贵、`DONT_CARE` 为什么省（断言 `V36`），本章 §4.4 把这两个开关放进显式 API 的正式机制里。
- **L06**：多 Pass FBO 链的亲身体验——本章的故障场景就是它的 Vulkan 版。
- 几个首次出现的术语，先给一句话解释（权威定义在 `tools/glossary.json`，站点术语卡自动收录）：
  - **Vulkan**：现代显式 GPU API 的代表（同类还有 Metal、D3D12）——状态、内存、同步全部由应用显式声明。
  - **CommandBuffer**（命令缓冲）：把绘制/拷贝/屏障命令先**录制**下来、再一次性提交给 GPU 执行的容器。
  - **PSO**（Pipeline State Object，管线状态对象）：把一次绘制所需的**全部**管线状态冻结成一个不可变对象。
  - **Descriptor**（描述符）：告诉着色器"去哪个缓冲/纹理取数据"的绑定描述，按集合（DescriptorSet）管理。
  - **Fence / Semaphore / Barrier**：三种同步原语——分别管 CPU 等 GPU、GPU 队列之间、GPU 内部的顺序与可见性（§4.2/§4.3 展开）。

## 3. 直观认识

主文档的概括最准确：**显式 API 把"驱动猜你想干什么"变成"你告诉驱动要干什么"**（[§1](../../../04-跨平台与高性能架构/显式API与同步原语.md#1-为什么需要显式-api)）。

用开车类比：OpenGL 像**坐出租车**——你说目的地，路线、换挡、什么时候加油都由司机（驱动）决定，省心，但你无法精确控制过程，司机还可能"过度谨慎"绕路（隐式同步可能过度）。Vulkan 像**自己开车**——每个动作自己操作，路线完全可预测，还能多人分工（多线程录制命令）；代价是你得会开车，操作错了不会有人提醒你——除非你主动装上"教练"（验证层，可选，发布时关闭）。

> **类比的边界**：出租车类比覆盖"责任转移"，但不覆盖两点——第一，显式 API 的错误往往**延迟且偶发**（漏 barrier 不是立刻熄火，而是偶尔跑偏），比"开错路"更难排查；第二，自己开车**不一定更快**：路况简单（DrawCall 少、状态切换少、瓶颈在填充率）时，出租车可能更省事，Vulkan 的收益是可预测性与多线程，不是自动提速（面试库 Q2 ⚠️，§4.1）。

## 4. 一步一步理解原理

### 4.1 OpenGL 状态机 vs 显式模型（objective ①）

五个维度的责任转移（[主文档 §1 对比表](../../../04-跨平台与高性能架构/显式API与同步原语.md#1-为什么需要显式-api)，断言 `V39`）：

| 维度 | OpenGL | Vulkan / Metal / D3D12 |
|---|---|---|
| 状态管理 | 全局状态机，驱动隐式跟踪 | 显式 PSO / 编码器 |
| 多线程 | 上下文绑定线程，难并行录制 | command buffer 可多线程录制 |
| 内存 | 驱动决定布局与生命周期 | 应用决定类型、布局、别名 |
| 同步 | 驱动隐式插入，可能过度同步 | 应用显式声明依赖 |
| 错误检查 | 运行时 GL 错误 | 验证层（可选，发布时关闭） |

多线程这一行值得展开：Vulkan 里每个线程用**各自的 CommandPool** 录制命令，最后主线程统一提交（[主文档 §3.2](../../../04-跨平台与高性能架构/显式API与同步原语.md#32-多线程录制)）；CommandPool 本身是外部同步的，一个池不能同时被多线程操作（面试库 Q1 追问）。OpenGL 的全局状态机 + 单上下文模型使这条路几乎走不通。

但**不要把"显式"读成"更快"**（面试库 [Q2](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#q2vulkan-一定比-opengl-快吗) ⚠️）：如果应用 DrawCall 少、状态切换少、瓶颈在 GPU 填充率，Vulkan 不会自动变快，甚至因为同步写错而更慢。收益来自**可预测性**——这正好接上 L08 的 `V07`：DrawCall 成本与状态切换相关，显式 API 把状态切换的成本从"运行时驱动猜测"挪到"创建时 PSO 固化"（§4.5），而不是消灭它。

### 4.2 同步三件套：分别在等谁（objective ②）

先分清两个世界：**CPU 与 GPU 之间**是异步的两台机器（L08 `V35`）；**GPU 内部**还有多条队列（图形/计算/传输/呈现）与交换链。三个原语各管一段（[主文档 §4](../../../04-跨平台与高性能架构/显式API与同步原语.md#4-同步三件套)、面试库 [§2.1](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#21-三种同步原语)，断言 `V40`）：

| 原语 | 同步对象 | 典型用途 | CPU 可等待？ |
|---|---|---|---|
| **Fence** | CPU ↔ GPU | CPU 等某帧命令执行完（回收该帧的缓冲） | ✅ `vkWaitForFences`，有"已信号"状态可查询 |
| **Semaphore** | GPU ↔ GPU（队列/提交之间） | 交换链 acquire/present、图形队列→传输队列 | ❌ 只能用于队列提交 |
| **Event** | 队列内细粒度 | 同一队列内 split barrier（前半段写、后半段读） | 有限 |

**checkpoint ① 的答案**：CPU 等 GPU 用 **fence**，不是 semaphore——binary semaphore 没有 CPU 等待的语义（timeline semaphore 带计数值、可跨队列跨帧，是另一套用法，见主文档 §4.2）。反过来用 fence 做队列间同步也不行。**混用会死锁或读到未完成的数据**（面试库 §2.1"最常见错误"原文）。

Fence 的帧级用法：每帧一个 in-flight fence，`vkWaitForFences` + `vkResetFences` 控制 CPU 不超前 GPU 太多帧（主文档 §4.1）——这就是 L08"Frame in flight 必须有上限"的正式实现。注意 `vkDeviceWaitIdle` 不是替代品：它阻塞到 GPU **完全空闲**，摧毁 CPU/GPU 并行，每帧调用必掉帧（面试库 Q3）。

GPU 一侧的方向纪律（主文档 §4.2 原文）：**等待的是"生产完成"，发出的是"消费可开始"**。标准帧循环是一个 ring（面试库 [§2.3](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#23-帧循环的标准同步结构)）：

```
[CPU] wait fence[i]            // 该帧上一轮已完成，可以复用它的资源
[CPU] acquire swapchain image  // 信号 imageAvailable[i]
[CPU] reset fence[i]
[CPU] 录制命令
[CPU] submit: 等待 imageAvailable[i]，信号 renderFinished[i]
[CPU] present: 等待 renderFinished[i]
```

每帧一套 fence + imageAvailable/renderFinished 信号量；frames in flight 通常 2–3，车载上 2 帧更常见（降延迟，但要防止 CPU 追不上——面试库 §2.3 原文口径，平台取舍按源文档验证状态分类属 ⚠️ 有条件成立）。首帧黑屏的根因就在这张图里：**没等 `imageAvailable` 就写颜色**（主文档 §5.5）。

### 4.3 Barrier 缺少时会发生什么（objective ③）

Fence/Semaphore 管的是"哪一批命令等哪一批"；**同一个命令缓冲内部**，前一个 Pass 写的纹理要被后一个 Pass 读，靠 **barrier**。它一次管三件事（[主文档 §5](../../../04-跨平台与高性能架构/显式API与同步原语.md#5-三类-barrier)、面试库 [§2.2](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#22-屏障barrier三类)，断言 `V41`）：

1. **执行依赖**（stage mask）：`srcStageMask → dstStageMask`，保证源阶段的命令在目标阶段开始前完成——管**顺序**。
2. **内存依赖**（access mask）：`srcAccessMask / dstAccessMask`，保证写入对后续读取**可见**（cache flush/invalidate）——管**可见性**。
3. **布局转换**（old/new layout）：图像从 `COLOR_ATTACHMENT_OPTIMAL` 转到 `SHADER_READ_ONLY_OPTIMAL` 等——管**资源形态**。

为什么顺序对了还不够？推一遍：GPU 各阶段有自己的缓存。Pass A 写完纹理，数据可能还停在 A 阶段的缓存里；Pass B 开始读时，即使"顺序上 A 先 B 后"，B 从自己的缓存路径看到的仍是旧值。**只写 stage mask 不写 access mask，就是只保证了顺序、没保证可见性**——表现为"偶尔读到旧数据"（主文档 §5.2 原文：这是最常见的错误）。这就是 §1 那个"偶尔闪烁一帧旧内容"的完整机制，不是玄学。

故障与根因对照（主文档 §5.5，六行 ✅）：

| 现象 | 原因 |
|---|---|
| 画面偶尔闪烁/旧帧 | 缺少 access mask 或 barrier 范围不对 |
| 验证层报 layout 错误 | 图像布局与 descriptor 不符 |
| 首帧黑屏 | 未等 `imageAvailable` 就写颜色 |
| 退出时崩溃 | 未等 fence 就销毁资源 |
| 多队列竞争 | binary semaphore 方向错误或复用未重置 |
| 过度同步、GPU 空转 | barrier 粒度过大（整条管线）或每 draw 一个 barrier |

注意最后一行：**barrier 不是越多越安全**。范围过窄→数据竞争花屏；范围过宽→GPU 气泡、性能下降（面试库 Q4）。两个边界都要守住。

两条连带纪律：布局转换**不是免费的**，TBDR 上可能触发 tile 的 load/store，能合并的转换要合并（面试库 §2.2）；**tiling（LINEAR/OPTIMAL）是创建时属性，barrier 改不了**——需要转换时必须新建图像再拷贝（主文档 §8.3）。

### 4.4 RenderPass 的 load/store：接上 L09 的带宽账

先补两个本章正式登场的术语（权威定义在 `tools/glossary.json`）：**RenderPass** = 一组附件与子 pass 的显式声明（对应 GL 的 FBO + 状态，主文档 §2 对象表）；**Subpass** = RenderPass 内的子阶段。L09 说过 `loadOp=LOAD` 在 TBDR 上代价高——现在给它正式机制（[主文档 §6.1](../../../04-跨平台与高性能架构/显式API与同步原语.md#61-附件操作)，断言 `V36` 的 API 面）：

| 操作 | 含义 | 移动端影响 |
|---|---|---|
| `loadOp = CLEAR` | 开始时清空 | 不读旧内容，省带宽 |
| `loadOp = LOAD` | 保留旧内容 | 读 tile memory/系统内存 |
| `storeOp = STORE` | 结束时写回 | 写系统内存，费带宽 |
| `storeOp = DONT_CARE` | 丢弃 | 省带宽，但内容不可用 |

**TBDR 优化核心**（主文档 ✅）：中间 pass 用 `DONT_CARE`，让 tile 数据留在片上；只有最终输出才 `STORE`。再进一步：同一 RenderPass 内，前一个 subpass 的颜色附件可以作为后一个 subpass 的 **input attachment** 读取（`subpassLoad`），**无需离开 tile memory**（主文档 §6.2）——色调映射、Bloom 合成这类"读上一 pass 结果"的操作因此不付系统内存带宽。注意限制（主文档 §6.2 原文）：input attachment 的布局/格式必须匹配，且**不能同时作为 color attachment 写入**；subpass 内也不能任意采样其他附件，只能走 input attachment 这条通道（面试库 Q8）——它不是普通纹理采样，做不了任意邻域滤波。子 pass 之间的依赖用 `VkSubpassDependency` 声明，不要手动逐个插 barrier（主文档 §5.4）。移动 SoC 共享 DRAM、带宽功耗敏感（`E02`），这套机制就是 L09 带宽账在 API 层的落点。

### 4.5 PSO 为什么不是单纯的 shader 程序（checkpoint ②）

**PSO 冻结的是一次绘制所需的全部管线状态**（[主文档 §7.1](../../../04-跨平台与高性能架构/显式API与同步原语.md#71-pso-包含什么)，断言 `V42`）：顶点输入布局、图元装配（拓扑/剔除/绕序）、光栅化（视口/深度偏移/线宽）、多重采样、深度/模板测试、颜色混合、着色器阶段与 specialization constants（创建时固化的着色器常量）、RenderPass 兼容性。shader 只是其中一项。

两个关键性质，出处分开记：**不可变**——创建后混合、深度、顶点布局、着色器全部冻结，改状态 = 换管线（仅少量字段可用 dynamic state，面试库 §1.1）；**任何一项不同都是一个新 PSO**（主文档 §7.1 原文）——所以 PSO 数量容易爆炸。

创建成本（主文档 §7.2、面试库 §4.1 ⚠️ 源给区间）：首次创建包含 shader 编译与状态验证，**可能几十到几百毫秒**；缓存后可降到毫秒级。运行时现建 = 卡顿。治理手段（面试库 §4.3 表列五项，此处取与创建成本直接相关的四项，动态状态一项已在上文"不可变"处交代）：管线缓存（`VkPipelineCache` 序列化到磁盘）、状态分组（按"材质 × 顶点布局 × 渲染目标"建 key）、变体裁剪（构建期按平台/质量档裁宏组合）、预热（loading 阶段创建）。**缓存数据与驱动/GPU 型号绑定，不能跨设备复用**；跨版本/跨驱动也可能失效，需要版本号与校验（主文档 §7.2、面试库 §4.1）。

## 5. 数学原理 / 数据形态

本章没有新公式，但有两笔账要算清楚。

**PSO 组合账**（教学算例，组合维度来自面试库 §4.3 状态分组）：设材质 M 种、顶点布局 V 种、渲染目标格式 R 种，PSO 上限组合数：

$$
N_{\text{PSO}} = M \times V \times R
$$

- **符号含义**：每个维度独立变化都会产生新 PSO（§4.5"任何一项不同都是新 PSO"）。
- **数值算例**：10 材质 × 3 顶点布局 × 2 目标格式 = 60 个 PSO；若每个首建 100 ms 且都在运行时触发，累计 6 s 的卡顿分布在交互里。
- **工程后果**：必须预热 + 缓存 + 变体裁剪——把创建挪到 loading 阶段，把组合数砍到实际需要的子集。

**帧环的数据形态**（§4.2 ring 的资源视角，frames in flight = 2）：

```
帧槽 i = 0, 1 轮流使用：
  fence[i]              CPU 等待该槽上一轮完成
  imageAvailable[i]     交换链图像就绪 → 渲染可开始
  renderFinished[i]     渲染完成 → present 可开始
  该帧的 UBO（uniform buffer，存 shader 常量数据的小缓冲）/descriptor  只有 fence[i] 通过后才能改写
```

同一 semaphore 不能在未等待时跨帧复用（面试库 §2.3：否则触发 validation error）——ring 的每个槽位一套，正是 `V35`"领先必须有上限"的资源配套。

## 6. 工程应用与常见错误

**排查现场**（由主文档 §5.5 与面试库 [Q9](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#q9如何调试-vulkan-的同步问题) 重组的教学案例）：车机后处理链偶发闪烁旧帧，日志无线索。按 §4.3 机制倒推：偶发 + 旧数据 = 可见性问题而非顺序问题 → 打开 **Validation Layer（含 synchronization validation）**，报告指向某处 barrier 缺 access mask → RenderDoc 抓帧核对 barrier 与 layout 确认 → 补上 `srcAccessMask/dstAccessMask`，故障消失。同步 bug 往往"偶发"，**必须靠工具而不是日志**（Q9 原文）；定位不了时用二分法：减少 frames in flight、禁用多线程录制，缩小变量。

常见误区：

- **"Vulkan 一定比 OpenGL 快。"** 收益是可预测性与多线程，不是自动提速；瓶颈在填充率时不会变快（面试库 Q2 ⚠️，`V39` 条件）。
- **"fence 和 semaphore 差不多，可以互换。"** 一个 CPU 等 GPU、一个 GPU 队列之间，混用死锁或读未完成数据（`V40`，§4.2）。
- **"stage mask 写了，barrier 就写完了。"** 顺序 ≠ 可见性；缺 access mask 偶发读旧数据（`V41`，§4.3）。
- **"每帧 `vkDeviceWaitIdle` 最保险。"** 摧毁 CPU/GPU 并行；用帧级 fence 只等要复用的那一帧（面试库 Q3）。
- **"PSO 就是 shader 程序。"** 它是全部管线状态的不可变冻结，shader 只是其中一项（`V42`，§4.5）。
- **"LINEAR 转 OPTIMAL 插个 barrier 就行。"** tiling 是创建时属性，必须新建图像再拷贝（主文档 §8.3）。

## 7. 动手核查清单

本章无绑定实验（`tools/labs.json` 无 L10 实验）；动手形式为**验证层 + RenderDoc 走查**（工具与方法来自面试库 Q9，在任意 Vulkan demo 工程上可做）：

- [ ] **验证层全开跑一帧**（做什么：启用 `VK_LAYER_KHRONOS_validation` 含 synchronization validation → 预期：无报告或拿到精确到命令的同步错误 → 对应机制：§4.1 错误检查责任转移）。
- [ ] **故意删一个 access mask**（做什么：在 demo 里去掉某 barrier 的 access mask 再跑 → 预期：验证层报可见性风险；关闭验证层则可能偶发旧数据 → 对应机制：§4.3 顺序 ≠ 可见性）。
- [ ] **RenderDoc 抓帧看 barrier 与 layout**（做什么：截一帧逐 Pass 核对图像布局转换 → 预期：每次"写后读"都有对应 barrier 与布局匹配 → 对应机制：§4.3 三类 barrier）。
- [ ] **二分定位练习**（做什么：把 frames in flight 从 3 降到 1 观察故障频率变化 → 预期：竞态窗口随环深变化 → 对应机制：§5 帧环）。
- [ ] **数一遍 demo 的 PSO**（做什么：统计管线创建调用与触发时机 → 预期：运行时零创建（全部预热/缓存）→ 对应机制：§4.5 创建成本）。

## 8. 总结与主动回忆

合上文档，复述这条因果链（说不出来就回到对应小节）：

**OpenGL 驱动隐式猜依赖 → 显式 API 把状态/内存/同步的声明责任交给应用，换来可预测性与多线程，但不自动更快（`V39`）→ CPU 等 GPU 用 fence、GPU 队列之间用 semaphore、队列内细粒度用 event，混用会死锁或读脏（`V40`/`V35`）→ barrier 一次管顺序 + 可见性 + 布局三件事，只写 stage 不写 access 偶发读旧数据，缺了竞态花屏、多了 GPU 气泡（`V41`）→ RenderPass 的 load/store 与 subpass 把 L09 的 TBDR 带宽账落到 API 层（`V36`/`E02`）→ PSO 冻结全部管线状态、创建贵，缓存 + 预热 + 变体裁剪（`V42`/`V07`）。**

再自问三个"为什么"：为什么 barrier 错误是"偶发"而不是"必现"？为什么 CPU 等待不能用 semaphore？为什么 PSO 缓存不能跨设备复用？

## 9. 自我检测

1. CPU 等待 GPU 应该用 fence 还是 semaphore？
2. PSO 为什么不是单纯的 shader 程序？

题目来源：`tools/course.json` L10 checkpoint（参考答案要点与断言挂接：Q1 → `V40`/§4.2，Q2 → `V42`/§4.5；quiz 文件待本课纳入 pilot 课程层后按 validate §10 规则补建）。

## 10. 下一章的桥

依赖已经会"说清楚"了——但 Pass 一多，手工管理就失控：每对 Pass 之间的 barrier 要人排（漏了花屏、多了卡顿），每张中间纹理各自长期占显存。[下一章](L11-RenderGraph与资源生命周期.md)把这两件事自动化：RenderGraph 用 DAG（有向无环图）描述依赖、编译期自动插 barrier、aliasing（生命周期不重叠的资源共用同一块显存）复用显存——它的前提正是本章的同步语义。

## 11. 术语与延伸

- 本章术语：Vulkan、CommandBuffer、PSO、Descriptor、Fence、Semaphore、Barrier、RenderPass、Subpass、Swapchain（权威定义在 `tools/glossary.json`，站点术语卡自动收录）。
- 机制细节：[显式 API 与同步原语 §4 同步三件套](../../../04-跨平台与高性能架构/显式API与同步原语.md#4-同步三件套)、[§5 三类 Barrier](../../../04-跨平台与高性能架构/显式API与同步原语.md#5-三类-barrier)、[§6 RenderPass/Subpass/Load-Store](../../../04-跨平台与高性能架构/显式API与同步原语.md#6-renderpass-subpass-load-store)、[§7 PSO 与描述符](../../../04-跨平台与高性能架构/显式API与同步原语.md#7-pso-与描述符)；面试视角：[Vulkan 与显式 API 对照 §2 同步](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#2-同步vulkan-面试的第一道分水岭)、[§4 PSO](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#4-管线状态对象pso)。
- 延伸：Metal 对象对照 → [主文档 §9](../../../04-跨平台与高性能架构/显式API与同步原语.md#9-metal-对照)；GL→Vulkan 迁移顺序（先抽象资源/pass/状态三层 + RenderGraph，再换后端）→ [主文档 §10](../../../04-跨平台与高性能架构/显式API与同步原语.md#10-与-opengl-的映射与迁移陷阱)；AHardwareBuffer 零拷贝导入 Vulkan → [面试库 §5.3](../../../06-面试知识库/车载渲染引擎/02-Vulkan与显式API对照.md#53-与-android-零拷贝)（L06 的 Vulkan 路径）；NDC 差异 → [L13](L13-坐标变换与MVP.md)。
- 断言状态说明：`V07`（已验证/medium——DrawCall 成本与状态切换相关）、`E02`（已验证/medium——PC 独显 PCIe vs 移动 SoC 共享 DRAM；条件：先说平台）为已验证断言；`V35`（CPU/GPU 异步与同步三件套概览）、`V36`（TBDR 家族与 load/store 差异）为 **open/low** 断言；`V39`（显式模型责任转移与收益边界）/ `V40`（同步三件套语义与帧环）/ `V41`（三类 barrier 与缺失/过度后果）/ `V42`（PSO 构成与创建成本治理）为本轮新登记的 **open/low** 断言（升级待 G1 人工裁决；SRC-RN-EXPLICIT-API / SRC-RN-INTERVIEW-VK 反向索引已同步）。正文结论以主文档锚点为权威依据。