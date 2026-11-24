---
doc_id: EMBODIED-B1-INTAKE
type: review-material
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
---

# INTAKE 清单 · embodied-loop-journey 首批（RUN-2026-11-23-embodied-batch1）

> 用户 2026-11-23 批准：课程名 embodied-loop-journey《具身智能：一条指令如何变成物理动作》+ 首批 6 课范围（kickoff §8）。
> 源库：`C:\Users\Giant\Desktop\GITCODE\Robot_Learn`（**只读参考，零改动**——run 前后 git status 核实）。

## 1. 查重结论

Engine 全库（01–07 知识目录/courses/knowledge-model/glossary/evidence）grep `具身|embodied|雅可比|Sim2Real|模仿学习|世界模型|VLA`：**0 命中**——完全新增领域，无重复风险。概念级共享面：坐标变换/外参 ↔ K-MVP（挂接复用）；延迟/帧预算账 ↔ L07/L08 方法论（链接不复制）。

## 2. 源批清单（实测修订版）

**主源（首批 6 课直接依据）**：
| 源 | 实测结构 | 支撑课 |
|---|---|---|
| knowledge/manual/textbook-embodied.md | **10 章**（盘点报告"12 章"口径更正）+术语表+参考文献；章章有结论框/算例/自测 | L1–L6 骨架 |
| knowledge/manual/embodied-principles.md | 6 章原理手册 + 来源与核验节 | L2/L3/L5 |
| knowledge/content/embodied/ch05/5.15-*原理深入*.md（verified） | 时间戳/外参/混叠/域随机化/链式成功率 | L3/L5 |
| knowledge/content/embodied/ch05/5.16-*原理深挖*.md（verified） | 正逆运动学/雅可比奇异/τ=JᵀF/复合误差，手算例 node 复算 | L4/L5 |
| knowledge/manual/embodied-openlab.md | 生态选型 + 16 周路线 + 每周验收 | L6 |

**辅助源**：learning-paths.md（路径 B）、quiz-bank.md + 章末自测（习题映射）、ch05 其余 verified 块（5.1/5.3/5.5/5.8）。

**⚠️ 源清单诚实修订**：kickoff 把 rerun/facts.md 列为"证据层映射底本"——**实测其内容为《人工智能训练师国家职业技能标准》/法规卷的事实底本**（职业编码/法条/数据质量国标/Kappa），非具身核心。首批仅按需引用其中具身相关条目（#20 具身智能白皮书官方名称、#21 高质量数据集建设指引、#22–23 GB/T 36344 数据质量六项、#24–25 Kappa 适用人数），**不作 6 课主证据**。

**不纳入**：reference/research（自标未独立核实）、av-playback/mobile-gpu（与现有课程同源，去重红线）、VLA/世界模型深潜卷（首批仅概念级提及 + 快照日期）、AI/ 培训 PDF。

## 3. 课–源映射（首批 6 课）

L1 闭环判据与错误落点（textbook §1/§3 + kb:5.1/5.3）→ L2 六环闭环与时间预算（textbook §3 + principles ch1 + kb:5.15）→ L3 时空对齐：时间戳/外参顺序/27mm 算例（textbook §5 + principles ch2 + kb:5.5/5.15）→ L4 正逆运动学与雅可比奇异（kb:5.16.1–3）→ L5 模仿学习复合误差与 Sim2Real（textbook §7/§8 + kb:5.8/5.16.5）→ L6 开源生态三件套与小闭环实践（textbook §10 + openlab）。

## 4. 工具链多课程支持评估（只读实测，核心改动报批）

- **build_site.py**：COURSE_PATH 硬编码 tools/course.json（单主课程 payload）；md 收集为 ROOT.rglob 排除列表制——**新课程 lessons 会自动进 bundle 文档层**，无需改收集。
- **validate_site.py §10（L392–422）**：遍历 courses/*/course.json，但 **L411 硬约束 pilot lesson id ⊆ tools/course.json ids**——独立新课程（自有 id 命名空间）会 FAIL。
- **最小扩展方案（报批，WRITE 前需批准）**：① validate §10 对声明 `"independent": true` 的课程跳过"派生自主课程"检查，id 唯一性/前置/unit 在本课程内校验；② build_site 增量输出 `courses[]` payload（additive，app.js 旧 UI 读 .course 不受影响；新课程站点导航属后续 LXD/app.js 工作，另批）；③ publish-allowlist allowed_top_levels += `08-具身智能`。三项均为核心门禁/构建改动，**未经批准不动手**。
- **过渡路径（若扩展未批）**：首批教材先以 `08-具身智能/` 知识文档形态产出（rglob 自动进 bundle），courses/embodied-loop-journey/course.json 待扩展批准后建立——RESEARCH/EVIDENCE 不受阻。

## 5. 范围边界与纪律

- Robot_Learn 只读；新断言默认 open/low；源库 verified 分级只作线索，关键结论按 P8 合同补外部权威核验；公式 Unicode→$$ 规范化 + 独立复算（不照抄源库"复算通过"结论）。
- 课程如实定位"可手算最小核"（平面两连杆级），不承诺 SLAM/动力学/控制/ROS 实操；前沿内容首批仅概念级 + 快照日期。
- LXD 工作流：6 页直接按六项增强 + Floor 标准建；既有 19 课分批增强穿插。
- 知识目录 `08-具身智能/` 新建（allowlist 同步见 §4）；claim.source_documents 必须指向 Engine 内新文档（validate §8 硬约束）。

## 6. 穿插任务记录（本 run INTAKE 期间执行，用户已批准）

两处源笔误修正完成：项目实战指南 §5.3 PSNR "+6dB 减半"→"+3dB 减半（+6dB≈1/4）"；程序化几何 §2 "花冠"→"花瓶"；L15 勘误注记闭合；V53 台账同步（D21）。