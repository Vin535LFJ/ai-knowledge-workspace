---
doc_id: PROG-USER-GUIDE
type: user-guide
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
verified_at: 2026-11-23
verified_against: ai-knowledge-program@cc098df / ai-knowledge-to-learning-engine@79c3fe8
---

# AI Knowledge Program 使用指南

> 这份文档写给**使用这个项目群的人**，不是架构说明，也不是开发计划。
> 目标：不读源码、不问 AI，也能知道现在有什么、怎么推进、怎么恢复。

## 1. Program 是什么

AI Knowledge Program 是整个项目群的**轻量统筹层**。它只做五件事：

1. 记住整个 AI Knowledge 要去哪（`PROGRAM.md`）。
2. 记住现在唯一在做什么、卡在哪（`NOW.md`）。
3. 记住阶段顺序与准入/退出条件（`ROADMAP.md`）。
4. 记住什么暂时不做、为什么（`PARKING-LOT.md`）。
5. 给接手 Agent 一套工作规则（`PROGRAM-MANAGER.md`）。

它**不生产知识**、**不开发功能**、**不复制子项目文档**。

## 2. Program 与各子项目的关系

| 项目 | 性质 | 当前状态 | 权威状态源 |
|---|---|---|---|
| AI Knowledge-to-Learning Engine | 第 2 层核心产品，唯一主动开发线 | P10 端到端验收已 done；当前 P10.3 embodied 首批在 RESEARCH | `ai-knowledge-to-learning-engine/WORKFLOW_STATE.md` |
| Matt Pocock Skills 中文定制发行版 | 独立 Skills 供应库 | 37 技能，维护态 | `matt-pocock-skills-zh-cn/SYNC.md` / `BACKPORTS.md` |
| Agent Workspace Governance | 第 3 层可复用能力 | 已交付，审计为 PARTIAL（工具可用、9/9 表述不成立） | 其 README + 本地 git |
| GitHub Project Radar | 第 3 层可复用能力 | 已交付，审计为 PARTIAL（八功能在、可持续性不足） | 其 README + 本地 git |
| Learning Experience Design | Engine 内部 Skill | active，1 个真实试点（L13） | `.agent/skills/learning-experience-design/` |

**关键边界**：Knowledge / Skills / MCP·Tools / Governance / Program 是五类不同事物，有关联但不是一个项目。不要因为有关联就合并。

## 3. 目录结构（真实）

```
C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\
├── ai-knowledge-program\                 ← 本统筹层（本地 git，无 remote）
│   ├── PROGRAM.md                        ← 目标/边界/原则/非目标
│   ├── NOW.md                            ← 当前唯一主目标 + 快照
│   ├── ROADMAP.md                        ← NOW / NEXT / LATER / COMPLETED
│   ├── PARKING-LOT.md                    ← 不做的事 + 准入规则
│   ├── PROGRAM-MANAGER.md                ← PM Agent 工作规则
│   ├── AUDIT-REPORT.md                   ← 2026-11-23 六阶段独立审计
│   ├── POST-AUDIT-SUMMARY.md             ← 审计后收口摘要
│   ├── PROJECT-DOCUMENTATION-INDEX.md    ← 全项目文档导航
│   ├── USER-GUIDE.md                     ← 本文件
│   ├── decisions\                        ← PD-001~003 + PENDING_DECISIONS
│   ├── plans\                            ← 命名迁移 / 进度复核 / embodied kickoff
│   ├── handoffs\                         ← 跨会话交接（自包含）
│   ├── references\                       ← 用户提供的原件（只读）
│   └── archive\                          ← 被取代的旧统筹文件
├── ai-knowledge-to-learning-engine\      ← 核心产品（GitHub: Vin535LFJ/ai-knowledge-to-learning-engine）
├── matt-pocock-skills-zh-cn\             ← Skills 库（GitHub: Vin535LFJ/matt-pocock-skills-zh-cn）
├── agent-workspace-governance\           ← 本地 git，无 remote
└── github-project-radar\                 ← 本地 git，无 remote
```

> **历史偏差（已于 2026-11-24 一致性修正中修复，审计 P0-2）**：`PROGRAM.md` §2/§9 与 `PROGRAM-MANAGER.md` §2/§8 曾残留旧目录名 `Render_Notes/` 与「Governance/Radar 冻结」表述，现已全部改为现名与「维护期」口径；历史记录段落中的旧名按命名规则保留。活跃指引以本指南 §3 和实际目录为准。

## 4. 如何启动 Program Manager

Program Manager 不是常驻程序，也没有独立可执行文件。它是**一个规则文件 + 一段启动提示词**。

在新 AI 会话里粘贴：

```
你是 AI Knowledge Program 的 Program Manager。
先读 C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-program\PROGRAM-MANAGER.md，
再按它的十二步启动流程执行。
第一步只做只读状态核实，不要改任何文件；核实后向我报告：
1) 当前唯一主目标与阶段；2) 最近一次交付；3) 当前阻塞；4) 你建议的唯一下一步。
```

PM 的五项职责：目标管理、进度管理、任务管理、范围控制、架构管理。
硬规则：**新增项目/子系统/工具/架构默认不进入当前计划**，除非是完成当前阶段不可缺少且用户明确批准。

## 5. 新会话如何恢复上下文

按顺序读，不要凭记忆：

1. `ai-knowledge-program/NOW.md`（最近快照 + 主目标 + 阻塞）
2. `ai-knowledge-program/ROADMAP.md`（阶段与准入/退出）
3. `ai-knowledge-program/handoffs/` 最新一份（自包含交接）
4. 目标项目内的权威状态：
   - Engine：`WORKFLOW_STATE.md` → `DECISIONS.md` → `reviews/REVIEW_STATUS.md`
   - Skills：`SYNC.md` / `BACKPORTS.md`
5. 用 git 实测核对（见 §6）。

**冲突处理**：项目内文档 + git 实测 > Program 快照。Program 过期时以项目内为准，并回头修 Program。

## 6. 如何查看当前状态

```powershell
cd C:\Users\Giant\Desktop\GITCODE\AI-Knowledge

# 五个仓库的 HEAD / 未提交 / 领先远端
foreach ($r in @("ai-knowledge-program","ai-knowledge-to-learning-engine","matt-pocock-skills-zh-cn","agent-workspace-governance","github-project-radar")) {
  "===== $r ====="
  git -C $r log --oneline -1
  (git -C $r status --short | Measure-Object -Line).Lines
  git -C $r status -sb | Select-Object -First 1
}

# Engine 当前 run（真实工作流状态）
py -3 ai-knowledge-to-learning-engine\tools\run_state.py list
py -3 ai-knowledge-to-learning-engine\tools\run_state.py show --run-id RUN-2026-11-23-embodied-batch1
```

## 7. 如何推进任务

PM 的节奏是「一次只给一个明确的下一步主任务」：

1. 读 NOW + 项目权威状态。
2. 确认当前阶段与退出条件（ROADMAP）。
3. 找**唯一**阻塞（人工门 / 技术缺口 / 范围决策）。
4. 给出「下一步主任务 + 验收标准 + 预计产物」。
5. 执行后更新项目内文档，再回写 NOW 的带日期快照。
6. 如果任务跨会话，写 `handoffs/`。

## 8. 如何添加新项目想法

不要直接开工。先过 `PARKING-LOT.md` §准入规则四问：

1. 它是否阻碍当前主目标？→ 是：可进当前任务计划。
2. 它是否是当前交付必须具备的能力？→ 是：作为项目内部能力实现，不急着独立。
3. 它是否只是未来可能复用？→ 是：进 PARKING-LOT，不启动。
4. 它是否已在多个项目反复验证？→ 是：才评估抽取为独立项目。

登记到 PARKING-LOT 时至少写：**价值 / 提出原因 / 暂缓原因 / 重新评估条件**。

## 9. 如何处理 Parking Lot

- **登记 ≠ 立项**。登记只表示「想到了，但现在不做」。
- 解冻需要：真实需求验证 + 用户明确批准。
- 冻结 ≠ 删除。已有成果保留，只停止新增投入。
- 每次阶段评审时检查一遍：有没有条目的「重新评估条件」已经满足。

## 10. 如何调整阶段计划

1. 先确认当前阶段是否满足退出条件（ROADMAP 每条都有）。
2. 新阶段必须写清：进入条件、退出条件、边界（不做什么）。
3. 任何「并行开第二条主线」的提议默认拒绝；单活跃线是硬规则。
4. 调整后同步 `ROADMAP.md` + `NOW.md`，并记一条 `decisions/PD-xxx`（若涉及范围变更）。

## 11. 如何记录完成状态

顺序固定：**项目内先留痕，Program 后回写**。

1. 项目内：`CHANGELOG.md` + 状态文档（如 `WORKFLOW_STATE.md`）+ 产物/测试证据。
2. Program：`NOW.md` 更新「最近状态」与进度表；必要时更新 `ROADMAP.md` 的 COMPLETED。
3. 涉及范围/架构：补 `decisions/`。
4. 跨会话：补 `handoffs/`。

不要只写「完成了」，要写：**证据路径 + 命令 + 结果 + 已知限制**。

## 12. 如何在任务中断后恢复

- 如果任务在 Engine 的 run_state 里：`run_state.py show` 看 `resume_point`；`resume` 继续；`retry` 重试。
- 如果任务在会话里：读最新 handoff → 读项目状态 → 用 git 核实 → 从「下一步主任务」继续。
- 如果状态文档冲突：先诊断（git diff / 文件时间），不要盲目修复或回滚。

## 13. 常用提示词（可直接复制）

**A. 每日启动**
```
读 ai-knowledge-program\NOW.md 与 PROGRAM-MANAGER.md，按十二步启动。
只做只读核实，报告：主目标 / 最近交付 / 阻塞 / 唯一下一步。
```

**B. 状态体检**
```
只读核实五个仓库的 HEAD、未提交、领先远端，以及 Engine 的 run_state。
对照 NOW.md 找出过期项，列成「文档说 vs 实测」两列表，不要修改。
```

**C. 新想法准入**
```
我有一个新想法：<描述>。
按 PARKING-LOT 四问分类，给出：进当前计划 / 项目内实现 / 进 Parking Lot / 评估独立。
如果你认为「有价值但当前不该做」，直接说，并给重新评估条件。
```

**D. 收口**
```
这一批做完了。按「项目内先留痕、Program 后回写」收口：
更新项目 CHANGELOG/状态文档，回写 NOW.md，列出未提交文件与建议提交分组。
不要 commit/push，等我授权。
```

**E. 交接**
```
写一份自包含 handoff 到 ai-knowledge-program\handoffs\：
当前状态、已完成、未完成、下一步、纪律红线、环境坑、验证命令。
要求下一个 AI 只读这份文档就能接手。
```

## 14. 常见问题

**Q1：为什么不做一个 Dashboard？**
A：Program 的价值是「准确 + 轻」，不是「可视化」。Dashboard 会变成第二个需要维护的产品。当前用 Markdown + git 足够。

**Q2：为什么 Program 没有 GitHub 远程？**
A：它是本地统筹层，只服务本机工作区。PD-Q3 未批准远程创建（不可逆公开动作）。

**Q3：NOW.md 和项目 WORKFLOW_STATE 有什么区别？**
A：NOW 是**项目级**快照（跨项目视角）；WORKFLOW_STATE 是 Engine **内部**的详细状态。冲突以 Engine 为准。

**Q4：Program 说完成了，但项目里还有 TODO，算完成吗？**
A：看 ROADMAP 的退出条件。完成指「该阶段退出条件满足」，不是「所有 TODO 清零」。遗留项应登记，不应藏起来。

**Q5：可以直接改 PROGRAM.md 吗？**
A：可以，但它是章程。改目标/边界/非目标要记 PD 决策；改状态应改 NOW。

**Q6：为什么文档里还有 `Render_Notes`？**
A：仅存于历史记录段落（决策/迁移说明，按命名规则保留）。活跃指引中的旧名已于 2026-11-24 一致性修正中清理完毕。真实目录是 `ai-knowledge-to-learning-engine`。以本指南 §3 为准。

**Q7：审计说 Governance/Radar 是 PARTIAL，还能用吗？**
A：能用，但要按边界用：Governance 当「扫描/诊断工具」，Radar 当「一次性探索 + 周报」，不要当平台。详见各自 USER-GUIDE 的「已知限制」。

---

**最后验证**：2026-11-23，Program `cc098df`、Engine `79c3fe8`、Skills `7326522`、Governance `1b4a880`、Radar `b7442da`。
**最近更新**：2026-11-24（审计整改 TASK 1：Program 状态一致性修正——PROGRAM/PROGRAM-MANAGER/ROADMAP/NOW/PENDING_DECISIONS/decisions-README/本指南；Engine `46a04d3` 与 Skills `4604bd6` 已 push，远端 USER-GUIDE 404 消除）。