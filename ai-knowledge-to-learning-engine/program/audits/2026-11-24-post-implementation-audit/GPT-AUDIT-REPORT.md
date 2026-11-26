## **一、整体审核结论**

**AI Knowledge Program**

有条件可用

统筹文件和 Program Manager 机制已经建立，但 NOW、ROADMAP、PROGRAM 仍有相互矛盾的信息。可以作为总入口使用，暂时不能完全信任它提供的所有项目状态。

**AI Knowledge-to-Learning Engine**

核心能力可用

HDR 批次已经真实跑通端到端生产链，能够在本地进行人工驱动的知识和教学产品生产。但仍不是全自动、多领域、可在线发布的成熟生产平台。

**Learning Experience Design**

有限可用

Skill 已有实际页面优化案例，能够指导 L13 页面设计，但目前主要验证了一个真实优化案例，尚未证明可以稳定处理各种页面类型。

**Matt Pocock Skills 中文定制发行版**

作为内容库可用

37 个 Skills 的内容和分类体系基本完整，可以作为通用技能来源。但跨 Agent 安装、发现、调用的兼容性尚未全面验证。

**Agent Workspace Governance**

MVP 可用

CLI、文档扫描、校验、ADR 和 Handoff 已有实际实现，但示例项目无法通过自身诊断，Task 和审批等关键治理能力还不完整。

**GitHub Project Radar**

暂不建议日常使用

可以一次性发现 GitHub 仓库，但持续追踪、增长趋势、人工审核和研究导出存在实质性问题。尤其是重新分析可能覆盖人工审核状态。

这里的“可用”需要区分具体用途：一个工具能够运行，不代表它已经可以安全地承担最初规划中的完整职责。

## **二、逐项目详细审核**

### **1. AI Knowledge Program**

需要先修正状态管理

项目文件：

- [PROGRAM.md](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-program/PROGRAM.md?utm_source=chatgpt.com)
- [NOW.md](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-program/NOW.md?utm_source=chatgpt.com)
- [ROADMAP.md](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-program/ROADMAP.md?utm_source=chatgpt.com)
- [PROGRAM-MANAGER.md](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-program/PROGRAM-MANAGER.md?utm_source=chatgpt.com)

**目前做得好的地方**

已经建立了 Program、Now、Roadmap、Parking Lot，以及 Program Manager 的启动和任务恢复规则。

这符合我们最初的设计目标：用轻量统筹层管理整个项目群，而不是开发新的项目管理平台。

**发现的问题**

第一，Program 状态不一致。

我发现：

- NOW 已经记录 2026-11-23 kickoff 获批，11 月 24 日推进到 EVIDENCE。
- ROADMAP 仍然写着 kickoff 待批准。
- PROGRAM 仍有旧仓库名称和“Governance/Radar 冻结”的描述。
- PROGRAM-MANAGER 仍有 `Render_Notes/.agent/README.md` 旧路径。
- 某些历史待决事项没有同步 D17–D20 的实际裁决情况。

这意味着新 Agent 即使正确读取 Program，也可能接收到过期指令。

第二，NOW 和 ROADMAP 的职责仍有部分重叠。NOW 保留了过多历史流水，Roadmap 又没有及时反映当前进度。

**建议修改**

| 优先级 | 修改内容                                                     |
| ------ | ------------------------------------------------------------ |
| P0     | 统一 NOW、ROADMAP、PROGRAM 的当前事实                        |
| P1     | 将旧路径和旧名称从活跃指引中清理掉                           |
| P1     | 关闭已完成的 PENDING_DECISIONS，历史记录保留                 |
| P2     | NOW 只保留当前任务、阻塞、最近状态，历史交给子项目和归档文件 |

我建议保留现有文件体系，不要再新增一套 Program 数据库或任务管理工具。

**最终定位：轻量项目群控制台，而不是项目管理平台。**

### **2. AI Knowledge-to-Learning Engine**

核心生产链已验证，但有限制

主要文件：

- [Engine README](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-to-learning-engine/README.md?utm_source=chatgpt.com)
- [Engine 使用指南](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-to-learning-engine/docs/USER-GUIDE.md?utm_source=chatgpt.com)
- [具身智能研究报告](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-to-learning-engine/reviews/embodied-batch1/research-report-embodied.md?utm_source=chatgpt.com)
- [发布允许清单](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-to-learning-engine/tools/publish-allowlist.json?utm_source=chatgpt.com)

**这是目前整个项目群最有价值、最接近原始目标的成果。**

HDR 批次不是简单生成了几份 Markdown，而是真正经过：

```
INTAKE
  ↓
RESEARCH
  ↓
EVIDENCE
  ↓
ARCHITECT
  ↓
WRITE
  ↓
DESIGN
  ↓
PRACTICE
  ↓
REVIEW
  ↓
PUBLISH
  ↓
FEEDBACK
```

审计材料记录了：

- P10 的真实 run 到达 FEEDBACK/done。
- 18 个 artifact。
- G3 通过。
- 84 条 claims。
- 43 条来源。
- 19 篇课时教材。
- 7 个实验。
- 5 份 quiz。
- 本地学习站构建及浏览器呈现验证。

这足以支持一个重要判断：

**Engine 的端到端生产链已经被一个真实批次验证，而不是停留在架构设计阶段。**

但仍然有四个问题。

#### **问题 A：Engine 还不是全自动知识生产系统**

目前：

- 原始资料主要通过人工 manifest 登记。
- Research 依赖 Agent 执行。
- 断言审核需要人工批准。
- 课程结构和教材仍需人工参与。
- Feedback 目前没有真实数据。
- KCR 主要提供影响分析和审核，不自动修改下游知识。

这些并不意味着架构失败。实际上，我认为保留人工审核是合理的。

真正的问题是应该准确定位：

**它现在是人机协作的可恢复知识生产工作流，而不是无人值守的全自动流水线。**

#### **问题 B：学习网站混入了内部工程文档**

这是我认为 Engine 最值得优先修复的问题之一。

目前 `publish-allowlist.json` 的 `policy` 仍是 `advisory`，不是强制门禁。

而且允许发布的根目录中存在：

- `DECISIONS.md`
- `CHANGELOG.md`
- `WORKFLOW_STATE.md`
- `README.md`
- `courses/`
- `docs/`
- `archive/`

审计还发现学习站 bundle 中出现过内部审核和治理内容，例如教材质量诊断、G2 审核材料和项目状态文档。

这会导致学习者看到不属于教学产品的工程内部信息。

**建议修改：**

将内容发布机制从“允许哪些路径”改成更明确的“哪些教学资产可以发布”。

例如：

```
允许发布：
- 课程正式知识内容
- 经过审核的教材
- 正式实验和练习
- 课程导航和术语
- 必要的学习辅助内容

默认禁止：
- DECISIONS.md
- CHANGELOG.md
- WORKFLOW_STATE.md
- reviews/
- .agent/
- .governance/
- 内部审核材料
- 任务交接与 Agent 工作文档
- 未经确认的工作草稿
```

然后让 Build 和 Validate 都能执行强制检查，并添加回归测试。

这项修改应在网站对外展示之前完成。

#### **问题 C：人工审批证据不够可靠**

审计指出：

- G3 审批记录的 approver 是写在运行状态 JSON 里的字符串。
- 18 个 artifact 中有 7 个 hash 与当前文件不一致。
- 运行记录位于 `.agent/runs/`，被 Git 忽略。

这使得以后无法仅靠仓库完整还原“某个文件在被批准时究竟是什么内容”。

**建议修改：**

建立持久化的审批记录，例如：

```
approvals/
  RUN-2026-11-20-p10-hdr/
    G1.md
    G2.md
    G3.md
```

每份记录明确：

- 审批对象。
- 审批范围。
- 审批人。
- 审批日期。
- 被批准文件的 SHA256。
- 审批结果。
- 关联的运行记录。

每次正式发布之前重新校验 artifact hash。

注意，这应当是一个小型可审计性增强，不需要重新开发整套审批系统。

#### **问题 D：具身智能课程还没有完成**

这是 11 月 24 日快照中最新的进度。

[当前 NOW](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-program/NOW.md?utm_source=chatgpt.com) 表明：

- `RUN-2026-11-23-embodied-batch1` 已经完成 RESEARCH。
- 已经进入 EVIDENCE。
- 产生了 7 份提取文档。
- 新增 V68–V84，共 17 条 open/low claims。
- 独立算例复算 70/70 通过。
- 已完成 3 项外部权威核验。

这很好，但目前还没有完成六课教材的完整生产和网站呈现。快照中能够看到研究资料和 08 目录，但尚未看到完整的 `courses/embodied-loop-journey/` 课程交付。

因此，不应该把多课程复用能力的代码扩展，直接当成多课程生产能力已经验收。

**我的建议：继续把具身智能六课作为 Engine 的下一项主任务，暂时不要再开新的领域。**

### **3. Learning Experience Design**

可以使用，但只验证了初步方法

文档：

[Learning Experience Design 使用指南](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/ai-knowledge-to-learning-engine/.agent/skills/learning-experience-design/USAGE.md?utm_source=chatgpt.com)

这项工作方向是对的，而且不应该独立成仓库。

我检查了实际内容：

- `SKILL.md` 已经 active。
- 有 Floor / Reflex / Finish 三级质量判断。
- 有页面原型分类。
- 有设计原则。
- 有页面质量检查脚本。
- 有使用模板。

L13 试点已经真正进行了六项页面增强：

- 学习目标。
- 前置知识。
- 空间链标注。
- P·V·M 推导表。
- 术语绑定。
- 自测与上下章衔接。

但是有一个重要区别：

**L13 是真正完成优化的案例，L19 只是 Floor 静态检查通过，并没有完成页面设计优化。**

目前不应宣称 LXD 已经在各种类型页面上稳定复用。

此外，13 份 references 存在重复和交叉，增加了使用时的阅读成本。

**建议修改：**

| 优先级 | 任务                                      |
| ------ | ----------------------------------------- |
| P1     | 将 13 份 references 整合为 5–6 份核心指南 |
| P1     | 让 SKILL.md 对所有保留指南有明确引用      |
| P1     | 在 AGENTS.md 中补充 LXD Skill 的显式索引  |
| P2     | 再选择一个实验页面做真实设计优化          |
| P2     | 增加一个不同类型的教材页面案例            |

特别不要为了验证 Skill，就把 19 篇课文全部改造一遍。

可以先选择实验页面和面试速查页面各一个，验证其能否处理不同类型的学习体验需求。

**最终定位：Engine 的内部页面设计与质量控制 Skill。**

### **4. Matt Pocock Skills 中文定制发行版**

内容库可用，运行时兼容性未完全验证

项目：

[Matt Pocock Skills 中文定制发行版](https://github.com/Vin535LFJ/ai-knowledge-workspace/tree/main/matt-pocock-skills-zh-cn?utm_source=chatgpt.com)

[使用指南](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/matt-pocock-skills-zh-cn/docs/USER-GUIDE.md?utm_source=chatgpt.com)

目前有 37 个 Skills：

| 分类         | 数量   |
| ------------ | ------ |
| Engineering  | 20     |
| Productivity | 7      |
| Misc         | 4      |
| In-progress  | 6      |
| **合计**     | **37** |

其中 plugin 发布 31 个，in-progress 6 个不参与正式发布。

优点是：

- Skills 来源明确。
- 中文翻译有维护规则。
- 有 4 处本地回填。
- 有上游同步体系。
- 有调用方式分类。
- 明确区分 user-invoked 和 model-invoked。
- 有 Agent 兼容性说明。

我认为这一项目已经达到了作为**通用 Skills 内容来源库**的基本目标。

但它还没有达到“安装一次，所有 Agent 都能正常使用”的程度。

目前验证程度有区别：

| 环节              | 现状               |
| ----------------- | ------------------ |
| Skills 内容存在   | 已验证             |
| 安装器识别        | 已有验证记录       |
| 文件安装投放      | 已有验证记录       |
| Agent 发现        | 没有跨宿主充分证据 |
| Agent 实际调用    | 未充分验证         |
| 跨 Agent 稳定兼容 | 未充分验证         |

另外，有一项环境限制：使用指南记录的本机 Node 版本是 v20.19.5，而它要求的安装器版本需要更高的 Node 版本。因此，安装器当前没有在本机完成验证。

**建议修改：**

1. 保留现有 37 个 Skills 和分类，不再重新设计分类体系。
2. 清理 `AGENT-COMPATIBILITY.md` 中过期的技能数量和状态描述。
3. 修复 `in-progress/README.md` 中指向旧上游的安装命令。
4. 处理没有对应 Skill 的悬空文档。
5. 将 `docs/USER-GUIDE.md` 提交到真正的 Skills 来源仓库。
6. 在你主要使用的 Agent 环境做一次实际安装、发现、调用测试，记录截图或运行日志。

我不建议现在投入大量精力验证所有 Agent 环境。

先选最主要的两种环境完成真实验证，再逐步扩展。

**最终定位：通用 Agent Skills 供应库，继续独立维护。**

### **5. Agent Workspace Governance**

基础工具可用，完整治理能力尚未闭环

项目：

[Governance README](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/agent-workspace-governance/README.md?utm_source=chatgpt.com)

[Governance 使用指南](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/agent-workspace-governance/docs/USER-GUIDE.md?utm_source=chatgpt.com)

核心实现：

[governance.py](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/agent-workspace-governance/cli/governance.py?utm_source=chatgpt.com)

这个项目已经有相当完整的基础：

- CLI。
- 5 个 JSON Schema。
- 6 个模板。
- 4 份 Constitution。
- 5 个客户端 Adapter 说明。
- 28 个测试。

目前能做的事情：

- 初始化治理配置。
- 扫描和登记文档。
- 校验文档元数据。
- 诊断孤儿、重复、引用和状态问题。
- 创建和检查 ADR。
- 生成 Handoff。
- 查看 Agent / Skill / Tool / MCP 元数据。

这些能力已经有实际价值。

但它距离最初规划的通用 Agent Workspace Governance 仍有差距。

#### **问题 A：最小示例本身不能通过诊断**

`examples/basic-project/` 的 document registry 中出现：

- `project-readme`
- `formal-tech-doc`

而当前 Schema 只接受 13 类合法文档类型。

审计记录中：

```
doctor --project examples/basic-project
exit code = 1
```

一个用来证明可移植性的示例项目，自己却无法通过治理工具的检查。

这是必须修复的基础问题。

#### **问题 B：初始化已有项目不够完善**

当目标项目已经有 `AGENTS.md` 时：

- `init` 会跳过写入治理入口。
- 不会自动追加治理说明。
- 部分模板中的治理目录路径仍然写死。

这会导致最常见的“接入一个已有项目”场景需要手工修复。

#### **问题 C：Task 和审批功能不完整**

Task Schema 已经存在，但没有完整的 Task Create / Claim CLI。

审批政策也要求记录审批人、时间、对象、结果和范围，但缺少对应的完整存储结构。

所以现在它比较接近：

**文档登记、扫描、诊断及协作辅助工具。**

而不是一个完整的治理自动化平台。

#### **建议修改**

| 优先级 | 任务                                                 |
| ------ | ---------------------------------------------------- |
| P0     | 修复 basic-project 的非法 type，确保 `doctor` exit 0 |
| P1     | 修复已有 AGENTS.md 时的治理入口处理                  |
| P1     | 改为相对路径或可配置路径，消除硬编码目录             |
| P1     | 补充审批记录 Schema，或明确删除尚未实现的审批承诺    |
| P1     | 对齐 README、CLI 与 User Guide 的命令数量            |
| P2     | 在第二个不同类型的真实项目上完整验证                 |

另外，现在 Engine 的治理注册表中已有 183 篇文档，但 task、agent、ADR 注册表为空，且 Engine 缺少 Governance 的明确入口。

不要只因为注册了文档，就宣布已经完成跨项目治理集成。

**最终定位：可移植治理工具包的早期 MVP。先修复基本接入流程，不要开发 Dashboard 或新功能。**

### **6. GitHub Project Radar**

目前不适合日常趋势追踪

项目：

[GitHub Project Radar README](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/github-project-radar/README.md?utm_source=chatgpt.com)

[Radar 使用指南](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/github-project-radar/docs/USER-GUIDE.md?utm_source=chatgpt.com)

核心代码：

- [storage.py](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/github-project-radar/radar/storage.py?utm_source=chatgpt.com)
- [export.py](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/github-project-radar/radar/export.py?utm_source=chatgpt.com)
- [radar.py](https://github.com/Vin535LFJ/ai-knowledge-workspace/blob/main/github-project-radar/cli/radar.py?utm_source=chatgpt.com)

这是我认为当前最需要谨慎使用的项目。

它有 38 个测试，真实采集也确实完成过，但实际能力与“持续 GitHub 趋势雷达”还有明显距离。

#### **问题 A：200 条快照不代表积累了长期趋势数据**

审计中的真实 SQLite 数据记录：

| 指标                 | 数值      |
| -------------------- | --------- |
| Repositories         | 121       |
| Snapshots            | 200       |
| Collection Runs      | 1         |
| 快照时间点           | 4         |
| 快照时间跨度         | 20 秒     |
| 增长指标不足历史数据 | 121 / 121 |

所以这 200 条快照并不是跨越几天的历史数据。

所有 121 个项目的 7 天、30 天增长数据都为空。

目前的“每周崛起项目”报告不能作为真正的增长排名使用。

#### **问题 B：分析会覆盖人工筛选状态**

我直接检查了 `storage.py` 和 `cmd_analyze()`。

当前逻辑：

1. `cmd_analyze()` 每次都以 `Discovered` 状态构造候选。
2. `upsert_candidate()` 的 SQL 在冲突更新时，连人工状态一起更新。
3. 原有的 `Research` 状态和 `human_selected_for_research` 可能因此被重置。

这意味着：

**人工已经筛选过的项目，可能在下一次执行 analyze 后丢失审核状态。**

在修复之前，不建议对已经人工筛选的数据库反复执行 `analyze`。

#### **问题 C：人工审批门可以被绕过**

`export.py` 的 `--approved` 目前仅修改：

```
review_status = approved_for_research
```

但没有同步写入：

```
human_selected_for_research = true
```

快照中的实际导出样本该字段仍为 `false`。

这会造成 Radar 报告看起来已批准，但 Engine 交接契约认为它没有被人工批准。

这是接口一致性问题。

#### **问题 D：缺少真正的历史跟踪入口**

`collector.refresh_tracked()` 已经有实现，但没有暴露给 CLI。

`snapshot` 子命令固定使用 fixture 客户端，不能用它为真实 GitHub 数据库持续补充快照。

所以现在还没有真正完成：

```
发现项目
  ↓
加入关注列表
  ↓
每日刷新同一批仓库
  ↓
积累时间序列
  ↓
计算 7 天 / 30 天增长
  ↓
生成可信周报
```

**建议修改顺序**

| 优先级 | 修改                                                        |
| ------ | ----------------------------------------------------------- |
| P0     | 修改 upsert：保留已有人工审核状态                           |
| P0     | 增加回归测试：重复 analyze 不能重置 Research 状态           |
| P1     | 让批准导出真正设置 human_selected，并保存审批人、时间和理由 |
| P1     | 增加真实仓库刷新/快照 CLI                                   |
| P1     | 保留 Rate Limit 剩余量，避免配额保护失效                    |
| P1     | 增长数据不足时禁止生成虚假的“崛起排名”                      |
| P2     | 补全来源和采集时间溯源                                      |
| P2     | 积累真实历史后再接 Windows 定时任务                         |

**目前可以怎么用？**

可以用它做一次性 GitHub 项目发现和初步筛选。

但是不要将它作为可信的增长趋势判断系统，也暂时不要把它导出的候选直接交给 Engine 自动处理。

## **三、跨项目整合审核：目前还没有真正闭环的地方**

虽然每个项目都产生了交付物，但项目之间的实际连接仍有缺口。

**当前真实的项目关系**

**AI Knowledge Program**

项目目标与状态管理（部分状态指针过期）

**AI Knowledge-to-Learning Engine**

领域知识、研究、课程教材、学习网站、KCR

**LXD**

已在 L13 实际应用

**Skills Repository**

提供 Skills，但 Engine 尚无充分的实际引用验证

**Governance**

Engine 已有部分注册表，但治理入口和校验尚未闭环

**Radar**

有 JSON 导出，但人工批准字段与 Engine 接口不一致

我发现的主要集成问题有：

| 集成关系            | 目前状态                 | 需要做什么                         |
| ------------------- | ------------------------ | ---------------------------------- |
| Program → Engine    | 部分成立                 | 修复旧路径和状态指针               |
| Skills → Engine     | 主要是架构上的可引用关系 | 选择实际 Skill 做调用验证          |
| LXD → Engine        | 已有真实案例             | 增加第二类页面验证                 |
| Governance → Engine | 部分成立                 | 修复入口、样例和诊断问题           |
| Radar → Engine      | 不成立                   | 修复人工审批字段和 Intake 数据契约 |

这里我不建议为了“六项目集成”而开发一个新的 Orchestrator。

目前最值得打通的是 **Radar → Engine Research Intake**，因为它是一个真正有业务价值的跨项目接口；其余关系可以通过文档链接、Skills 引用和现有工作流实现。

## **四、还有一个非常重要的问题：你的项目仓库发布状态**

这次我不仅看了快照，也核对了实际 GitHub 仓库。

[AI Knowledge Workspace](https://github.com/Vin535LFJ/ai-knowledge-workspace?utm_source=chatgpt.com) 本质上是一个 2026-11-24 的单提交快照仓库，提交为 `09ddfcc`。它把五个项目的文件集中放在一起，但明确不包含原项目的 Git 历史和被忽略的本地数据。

实际检查结果：

| 项目                            | 独立 GitHub 仓库                  | 公开可访问 |
| ------------------------------- | --------------------------------- | ---------- |
| AI Knowledge Program            | 当前未发现独立远程仓库            | 否         |
| AI Knowledge-to-Learning Engine | `ai-knowledge-to-learning-engine` | 是         |
| Matt Pocock Skills              | `matt-pocock-skills-zh-cn`        | 是         |
| Agent Workspace Governance      | 暂未发现独立仓库                  | 否         |
| GitHub Project Radar            | 暂未发现独立仓库                  | 否         |

我还发现：

- Engine 快照中有 `docs/USER-GUIDE.md`，但实际独立 Engine 仓库的这个路径目前返回 404。
- Skills 快照中有 `docs/USER-GUIDE.md`，但实际独立 Skills 仓库的这个路径目前也返回 404。
- 快照中的其他项目文档也不因此自动进入独立仓库。

换句话说，**快照仓库里的文件存在，不等于原来的项目仓库已经同步了这些文件。**

如果你要把 AI Knowledge 作为日常工作环境，我建议：

1. 将 Program、Engine、Skills、Governance、Radar 的使用文档分别同步到各自真正的项目位置。
2. Program 可以继续作为本地项目管理目录，不必急着创建独立 GitHub 仓库。
3. Governance 和 Radar 暂时先在本地使用；等基本功能修复后再决定是否创建独立仓库。
4. `ai-knowledge-workspace` 可以保留作为综合审查快照，但不要把它误当作所有独立项目的 Git 主仓库。

## **五、建议的修复计划：先解决真正影响使用的问题**

我不建议重新进行六阶段建设。现在已经有了大量可用资产，下一步应当是修缺陷、统一状态、证明稳定性。

我会按以下顺序安排：

## **第一批：必须优先处理**

P0

**1. Radar 数据安全**

修复 `analyze` 覆盖人工审核状态的问题，并增加回归测试。在修复前不要在已经人工筛选的数据库上重复运行 analyze。

P0

**2. Program 状态一致性**

修正 PROGRAM、NOW、ROADMAP、PROGRAM-MANAGER 以及历史待决状态，使新 Agent 读取到同一份事实。

P0

**3. Engine 内容发布边界**

将内部治理文档、审核材料和工程记录排除出学习者网站，增加真正强制的发布门禁。

## **第二批：让项目真正容易使用**

P1

**4. Governance 最小可用修复**

确保 basic-project 自身能通过 doctor，修复已有 AGENTS.md 的接入方式，澄清实际支持的审批和 Task 能力。

P1

**5. Radar 人工批准与快照机制**

修复 `--approved`，增加真实仓库追踪和快照入口，完善历史数据不足时的报告处理。

P1

**6. Engine 审批证据链**

让 G1/G2/G3 审批与实际被批准文件版本绑定，解决 artifact hash 过期问题。

## **第三批：成熟度提升**

**7. LXD 第二案例**：完成一个实验页优化，检查 Skill 能否从教材页迁移到交互页面。

**8. Skills 真实运行验证**：在你的主要 Agent 环境中验证安装、发现和调用。

**9. 文档和 Git 发布同步**：把快照中有价值的使用指南同步回独立仓库。

**10. 全项目最终回归**：重新核对 Program 状态、Engine 门禁、Governance 示例、Radar 数据安全和项目间接口。

## **六、每个项目以后应该保持什么状态？**

我建议不要因为修复问题，就重新开启所有项目的大规模功能开发。

| 项目       | 后续状态             | 功能扩展原则                     |
| ---------- | -------------------- | -------------------------------- |
| Program    | 持续维护             | 只维护状态和路线图               |
| Engine     | 主动开发             | 继续完成具身智能首批六课         |
| LXD        | Engine 内部工作流    | 随真实页面迭代，不单独扩张       |
| Skills     | 维护态               | 上游同步和兼容性验证             |
| Governance | 缺陷修复后冻结功能   | 等第二个真实项目验证再扩展       |
| Radar      | 修复前冻结使用级扩展 | 先证明快照和审核可靠，再谈自动化 |

尤其是 Governance 和 Radar：

**不要为了证明项目存在价值，就继续往里面加功能。**

它们应该先证明自己能解决实际问题，而不是再发展成两个需要长期投入的大工程。

## **七、我的最终判断**

现在的 AI Knowledge 已经不是一个概念项目了。你已经有了：

- 能够生产真实教学内容的 Engine。
- 能够指导页面设计的 LXD Skill。
- 可复用的 Skills 内容来源库。
- 有实际 CLI 和 Schema 的 Governance MVP。
- 有真实 GitHub 采集能力的 Radar MVP。
- 统一管理这些项目的 Program。

但目前还不能说所有模块都已经达到原始规划中所设想的完整成熟度。

**我建议把当前状态正式定义为：核心生产能力已建立，周边工具进入稳定性修复和使用验证阶段。**

当前最重要的是：

1. 继续完成 Engine 的具身智能课程，保持唯一主动开发主线。
2. 修复 Radar 和 Governance 的使用级缺陷，避免错误数据和虚假审批。
3. 修正 Program 的状态漂移及 Engine 的学习站发布边界。
4. 同步各项目的使用文档，使它们真正能被独立使用。

我这次的审核依据包含公开快照里的代码和文件，以及仓库中记录的 11 月 23–24 日实测结果；没有直接访问你本地被 Git 忽略的 Radar 数据库或 Engine 运行态，也没有在我的环境中复跑所有 Windows 测试。因此，代码缺陷可以根据已检查的实现确认，部分运行结果仍属于仓库所记录的实测证据，而非我重新执行所得。

**下一步我建议先制定一份《AI Knowledge 稳定性修复任务书》，只包含 P0/P1 的最小修改，不新增功能，并把 Engine 具身智能课程继续保留为唯一主要研发任务。**