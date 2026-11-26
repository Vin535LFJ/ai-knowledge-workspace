# AI Knowledge 工作区快照（2026-11-26）

> 用途：给外部专家评审用的**当前状态快照**。五个项目的**已提交**内容原样放进来（不含 git 历史，不含各仓被忽略的本机文件）。权威事实源是各自的代码仓与状态文档；本快照只是便于一次性浏览与评论。
>
> 上一版快照（2026-11-24）用于外部 AI 复核；本版是刷新到最新已提交状态，供人工专家讨论"接下来该怎么做"。

## 一、五个目录与来源

| 目录 | 项目 | 本快照时的 commit | 正式远端 |
|---|---|---|---|
| `ai-knowledge-program/` | AI Knowledge Program（统筹层） | `ba35e4a`（18 笔） | 无（本地仓，PD-Q3 待决） |
| `ai-knowledge-to-learning-engine/` | AI Knowledge-to-Learning Engine（**唯一主动开发主线**） | `3062b4a`（43 笔） | `Vin535LFJ/ai-knowledge-to-learning-engine` |
| `matt-pocock-skills-zh-cn/` | Matt Pocock Skills 中文定制发行版 | `4e01df4`（142 笔） | `Vin535LFJ/matt-pocock-skills-zh-cn` |
| `agent-workspace-governance/` | Agent Workspace Governance（维护期） | `7d9a187`（6 笔） | 无（本地仓） |
| `github-project-radar/` | GitHub Project Radar（维护期） | `e2815d9`（5 笔） | 无（本地仓） |

文件数：Program 31 · Engine 359 · Skills 162 · Governance 40 · Radar 39（合计 631）。

## 二、只想花 30 分钟了解全貌，按这个顺序读

1. **`ai-knowledge-program/NOW.md`** — 当前唯一主项目、阶段、当前任务、阻塞、下一步（只有 7 个字段，读完就知道现在卡在哪）
2. `ai-knowledge-program/ROADMAP.md` — Now / Next / Later 阶段规划
3. **`ai-knowledge-program/decisions/PENDING_DECISIONS.md`** — **需要人拍板的事**：PD-Q3、PD-Q4（仍待决）+ PD-Q9 至 PD-Q17（本轮新登记 9 项，均未批准），每项都有背景 / 影响 / 推荐方案 / 不处理的后果 / 是否阻塞
4. `ai-knowledge-program/PARKING-LOT.md` — 明确**不做**的方向（范围控制记录）
5. `ai-knowledge-program/plans/2026-11-25-stage-execution-report.md` + `plans/2026-11-25-stabilization-verification.md` — 上一轮做了什么、验证到什么程度（PASS WITH LIMITATIONS 没有被改写成 PASS）
6. `ai-knowledge-program/AUDIT-REPORT.md` + `POST-AUDIT-SUMMARY.md` — 独立审计结论与真实状态纠偏
7. **`ai-knowledge-to-learning-engine/reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`** — **当前真正卡住的地方**：具身六课的人工验收材料（G1 21 条断言逐条依据与分类建议、G2 六课逐课依据与评分表、专项复核、审批登记顺序）。**所有裁决栏留空**
8. `ai-knowledge-to-learning-engine/reviews/embodied-batch1/independent-review.md` + `recheck-planA-fixes.md` + `targeted-recheck.md` — 独立审读链（含"首轮审读报告因断网丢失"这一如实说明）

## 三、当前状态一句话

Engine 的端到端生产链已**真实跑通一次**（P10 done，2026-11-21）。本轮主线是第二批课程 `embodied-loop-journey` 的 6 课：已写完 → 独立审读 → 修复 → 复评（建议分 88/91/91/92/90/88，均过 85 线），**停在人工验收门前**：G1（断言升级）、G2（六课评分）、G3（审批）、KCR 四道门全部由人裁决，AI 不自评自批。周边三个项目进入维护期，只修缺陷、不扩功能。

## 四、给专家的三个具体问题

1. **具身六课的验收该按什么标准收口？** 验收包里的 G1 分级建议与 G2 十维度评分是否够用，还缺哪一类证据？
2. **"单活跃线 + 三个项目维护期"的组织形态是否合理？** Governance 与 Engine 的文档类型口径不对齐（PD-Q14，真实 Engine 副本上 `validate` / `doctor` 均 exit 1），现在做映射还是等第二个真实项目？
3. **仓库公开 vs 内部材料（PD-Q16）怎么取舍？** Engine 仓库为 Public，`reviews/`、`.agent/`、`.governance/` 等过程材料对外可见。

## 五、快照边界（重要）

- 只含各仓**已跟踪**（已提交）文件：不含 git 历史，不含被 `.gitignore` 忽略的本机文件（Engine 的 `.agent/runs/` 运行态、`.workbuddy-ai/memory/`、Radar 的本地 `.db` 等）。
- 三个本地仓（Program / Governance / Radar）没有 GitHub 远程；**本快照是它们目前唯一的远端副本**。
- 2026-11-26 全部仓的提交作者已统一为 GitHub 身份 `Vin535LFJ <169535939+Vin535LFJ@users.noreply.github.com>`（公司邮箱已从公开历史移除，内容零改动），**所有旧 commit SHA 失效**；文档里出现的旧 SHA 指重写前的历史。
- 本快照是**只读浏览副本**；要改动请回到五个仓本体。
