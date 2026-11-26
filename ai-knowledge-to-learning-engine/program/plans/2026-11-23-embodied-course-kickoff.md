---
doc_id: PROG-PLAN-EMBODIED-KICKOFF
type: agent-plan
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
---

# Kickoff 方案 · embodied-loop-journey（P10.3 多领域复用首批）

> **已批准（2026-11-23 用户："批准 embodied-loop-journey 课程名和首批 6 课范围，继续"）**。run `RUN-2026-11-23-embodied-batch1` 已建立，INTAKE 完成→RESEARCH（实测见 Engine reviews/embodied-batch1/intake-manifest.md；源清单修订：facts.md 实为法规卷底本、textbook-embodied 实测 10 章）。工具链多课程最小扩展仍为报批项（WRITE 前需批准）。

## 1. 课程定位与名称

- **推荐**：`embodied-loop-journey`《具身智能：一条指令如何变成物理动作》——闭环叙事贯穿，与 video-rendering-journey（"一帧视频如何从文件抵达屏幕"）对仗；源材料匹配度最高。
- 备选：`robot-learning-journey`（机器人学习之旅）。**不做**传统机器人学课（SLAM/动力学/控制/ROS 实操为源库自认缺口，不承诺）。
- 受众画像沿用 Engine 模板：工程面试/转岗学习者，重判据+可手算算例+误区+自测。

## 2. 源批（首批 8 份，全部 Robot_Learn 高置信层）

| # | 路径（Robot_Learn 内） | 用途 |
|---|---|---|
| 1 | knowledge/manual/textbook-embodied.md（12 章教材卷） | 主源：课程骨架 |
| 2 | knowledge/manual/embodied-principles.md（6 章原理） | 时空对齐算例/七组件数据表 |
| 3 | knowledge/content/embodied/ch05/5.16-*原理深挖*.md（verified） | 运动学→策略学习，手算例全复算 |
| 4 | knowledge/content/embodied/ch05/5.15-*原理深入*.md（verified） | 时间戳/外参/混叠/域随机化 |
| 5 | knowledge/manual/embodied-openlab.md | 生态选型 + 16 周路线（实践课） |
| 6 | knowledge/manual/learning-paths.md | 路径 B 8 周（课程路线参考） |
| 7 | rerun/facts.md（80 行 A 级结论） | 证据层映射底本 |
| 8 | knowledge/interview/quiz-bank.md + 教材章末自测 | 习题映射（273+48 题） |

**不纳入首批**：reference/research（自标未独立核实）、av-playback/mobile-gpu（与现有课程同源，去重红线）、VLA/世界模型前沿深潜（快照时效）、AI/ 培训 PDF。
**外部核验**：关键结论按 P8 合同补外部权威源（论文/官方文档），Robot_Learn 的 verified 分级只作线索不作终证；新断言默认 open/low。

## 3. 首批范围（6 课，端到端验收批）

L1 闭环判据与错误落点 → L2 六环闭环与时间预算 → L3 时空对齐（27mm 算例）→ L4 正逆运动学与雅可比奇异 → L5 模仿学习复合误差与 Sim2Real → L6 开源生态三件套与小闭环实践。
覆盖"定义→机制→数学→学习→工程"全链；每课照 L01 标杆 + 十维度规范 + **LXD 六项增强直接内建**（学习目标条/概念标注/分行推导/术语绑定/Floor 检查）。

## 4. 落地机制（INTAKE 检查单）

1. **run**：`RUN-2026-11-23-embodied-batch1`（gate G3，--kcr，write_paths 声明新课程目录与共享 JSON）。
2. **知识目录**：新建 `08-具身智能/`（Engine 内新顶层）——需同步 build/validate/build_vitepress 收集机制与 publish-allowlist（**工具链改动清单先列明，核心门禁改动报批**）。
3. **课程结构**：`courses/embodied-loop-journey/`（course.json + lessons/ + quizzes/）。**多课程支持评估**：现 tools/course.json 为单主课程；validate §3/§10 与 build_site 的课程读取是否支持第二课程——INTAKE 阶段只读评估，需扩展则列方案报批，不擅自改核心。
4. **来源登记**：Robot_Learn 文件登记为 repo_doc 来源（url 用可核实路径引用 + accessed 日期）；**claim.source_documents 必须指向 Engine 内新文档**（validate §8 文件存在性硬约束）——先研究产出 Engine 知识文档，再挂断言。
5. **概念去重**：坐标变换/外参 ↔ K-MVP 挂接复用；渲染/延迟预算 ↔ 现有概念链接；纯新增（闭环判据/雅可比奇异/Sim2Real/复合误差）建新概念，无环。
6. **公式规范化**：源库 Unicode 行内数学 → $$ LaTeX（站点保护），算例保留"复算通过"纪律（独立复算，不照抄源库结论）。
7. **习题**：quiz 按 pilot 规则（若纳入 pilot 层则 checkpoint 覆盖 + claim_ids ⊆ frontmatter claims）。

## 5. LXD 内部工作流（与主线同批，不另开战线）

- 新课程 6 页：直接按六项增强 + Floor 标准建，每页 Floor PASS 留痕。
- 既有 19 课：分批增强（每批 3–5 课，独立小提交 + Floor + 门禁），排在主线批次间隙；**不阻塞主线门禁**。
- 真实浏览器验证（Edge headless 双路）按 LXD 规范执行；设计体系继续从迭代提炼进 Skill refs。

## 6. 验收标准（复用 P10 八项 + 复用专项）

P10 八项（全链走通/可重复/契约/质量检查/人工门/网站呈现/KCR/失败恢复）+ **复用专项**：共享 Evidence/Glossary/Skills 零重建验证、跨课程概念去重报告、工具链多课程支持结论、源库只读零改动核实（Robot_Learn git status 前后一致）。

## 7. 风险与边界

- 源库数学为平面两连杆级——课程如实定位"可手算最小核"，不假装覆盖 6-DoF。
- 前沿内容（VLA/世界模型）首批只做概览提及 + 快照日期标注，深潜留后续批。
- 工具链多课程扩展是本批最大工程风险——INTAKE 只读评估先行，改动报批。
- commit/push 逐次授权；在线发布 D02 不变。

## 8. 批准栏（用户填写）

- 课程名：□ embodied-loop-journey（推荐） □ robot-learning-journey □ 其他：____
- 首批 6 课范围：□ 同意 □ 调整：____
- 开工：□ 继续（AI 建 run 从 INTAKE 开始） □ 暂缓