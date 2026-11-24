---
doc_id: G2-L07-DEEPENING
type: review-material
status: draft
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# G2 审核材料 · P7.2 第八篇 L07《GPU 为什么快》新写教材（2026-11-20，「其余篇目」第四篇）

> **性质**：AI 执行留痕与审核材料，**不是评分**。G2 正式评分由人工填写于 `courses/video-rendering-journey/review-report.md`；AI 不自评。
> **深化方式**：主会话执笔（新写），独立子代理审读（只读换人、逐行验证 + 独立重算）。改动一律未 commit。

## 1. 深化摘要

- **L07 正文**：0 → 150 行（新文件，概念直觉型+工程机制型）。TOPS vs 帧率钩子 → 车道类比（边界豁免访存/调度）→ 并行模型表与分支发散代价（V29）→ 存储层次 + 带宽账模板与算术强度（V30）→ 占用率是手段非目标（V31）→ 别只看 TOPS、车机看 P99（V32）→ §5 带宽账算例 + 验证实验表转载 → 降分辨率排查现场 + 5 误区 → 带宽账手算清单 → 桥句→L08。
- **新断言登记**：V29（warp 分支发散串行化，附条件 32/64 lane 常见值 ⚠️）/ V30（带宽账口径与模板，附条件算术强度）/ V31（占用率是手段非目标）/ V32（TOPS 峰值≠帧率），open/low；source-registry 新增 **SRC-RN-GPU-BASE**（repo:03-图形与GPU工程/GPU与渲染引擎基础与链路.md，双向索引 [V29–V32]）。
- **quiz 边界**：非 pilot 课无 quiz 文件（validate §10 规则），正文 §9 如实声明。

## 2. 独立审读原始结论（第一轮）

- **acceptable = false（1 blocker + 2 major）+ 6 minor**；21 处技术表述全部在主文档找到行级出处、无编造数字；V29–V32 三处登记一致、均 open/low、used_by 双向同步；两层 course.json 对齐；锚点匹配。
- **亮点**：7.9MB/475MB/s/GB/s 量级、并行模型表（含 32/64 lane ⚠️ 条件）、验证表四行、降档顺序、§4.4 引语逐字全部有行级出处。

## 3. 审读发现（1 blocker + 2 major + 6 minor）及修复对照（全部已修）

| # | 级别 | 发现 | 修复 |
|---|---|---|---|
| 1 | **blocker** | "1920×1080×4B ≈ 7.9 MB" 口径错误（该式=8.29 MB 十进制；7.9 是 MiB 值），与 L01/L06 的 8.29 MB 冲突、checkpoint 答案两口径打架 | §1/§4.2/§5/§9 四处统一双口径（8.29 MB 十进制 / 7.91 MiB；498 MB/s 十进制 / 475 MB/s 源二进制口径），沿用 L01 MB/MiB 纪律；ledger V30 同步 |
| 2 | **major** | "L06 的 aliasing/RenderGraph 在带宽账上直接兑现"双重错位（aliasing/RenderGraph 属 L11；aliasing 省 VRAM 峰值非带宽） | 改分科目归属：L06 零拷贝省 CPU 搬移；L11 loadOp/storeOp 优化带宽、aliasing 省 VRAM 峰值 |
| 3 | **major** | 小节号错位 3 处（验证表/模板/少不确定性 引用互串） | 全部改为"主文档 §x.x"无歧义标注，本章转载处标"本章转载" |
| 4 | minor | "按 Pass 累加"归因 L06 超前（L06 账按拷贝次数） | 改"该口径由本章 §4.2 登记为 V30" |
| 5 | minor | P99 帧时间首现无一句话解释 | 补"99% 的帧耗时低于该值——尾部延迟指标" |
| 6 | minor | §10 "[下一章]"链接落点无法承载承诺（L08 无文件） | 改"L08 教材页待建"+总览链接 |
| 7 | minor | L06↔L07 双路线断层（L06 桥句指 L11，主课程 L06.next=L07） | 属 pilot/主课程双路线既有设计——记录为跨路线观察（见 §5.4），未改动 L06 桥句 |
| 8 | minor | "可合并的uniform"缺空格；延伸链接缺 #3-overdraw-与带宽 锚点 | 均已修 |
| 9 | minor | §11 延伸"RenderGraph 的带宽收益→L11"口径不符（L11 量化口径是 VRAM Peak 等） | 改"显存峰值收益（aliasing）与 loadOp/storeOp 带宽优化" |

## 4. 门禁实测（修复后复跑，全 exit 0）

- build_site：**73 documents（69+L03/L04/L05/L07）/ 17 sections / 124 terms / 19 lessons / 7 labs / 536 cards / 2717 KB**
- validate_site：**11 checks passed, 0 warnings, 0 failures**
- check_chapter_arc：**9 篇 · OK**
- review_gate：**49 claims（verified 18 / open 24 / conditional 7）误标 0**
- test_publish_boundary：**11 tests OK**（数量断言 72→73 同步）

## 5. 待人工事项

1. **G2 评分**（L02/L03/L04/L05/L06/L07/L11/L13 八篇材料齐备）。
2. L02 遗留 major（labs.json/app.js「DTS ≤ PTS 恒成立」）仍开放。
3. **跨路线观察（5.4）**：L06 桥句按 pilot 路线指向 L11，而主课程 L06.next=L07——主课程读者从 L06 会跳过 L07；属双路线设计（pilot 层 course.json L06.next=L11），是否需要"L07 直达链接"留人工裁决。
4. V29–V32（open/low）升级待 G1 另裁；「其余篇目 vs 先转 P8」顺序决策留用户。
