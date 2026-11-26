---
doc_id: GOV-USER-GUIDE
type: user-guide
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-25
verified_at: 2026-11-25
verified_against: agent-workspace-governance@73b22c8+P0修复
---

# Agent Workspace Governance 使用指南

> 一句话：这是一个**纯本地、仅标准库、不联网**的 Agent 项目治理工具包，帮你清点文档、校验 frontmatter、发现孤儿/重复/冲突、生成 handoff 与 ADR。
> 它**不是**自动化治理平台，也**不替代**业务项目自己的状态机与编排。

---

## 1. 项目定位

- 目标：让一个「普通 GitHub 项目」也有一套可执行的文档/任务/交接/ADR 治理。
- 形态：`cli/governance.py`（单文件，11 个子命令）+ 5 个 JSON schema + 6 个模板 + 4 篇 constitution。
- 边界：不调用 git、不联网、不改源文件内容；只读写目标项目的 `.governance/` 与生成的交接/ADR 文件。

## 2. 适用场景

- 项目文档变多，想知道「哪些没登记、哪些孤儿、哪些重复、哪些引用过期」。
- 多个 Agent 协作，需要单写者约定、依赖前沿、交接文档。
- 想把 ADR、任务契约、Skills/MCP/Tools 清单落到文件，而不是散在聊天里。
- 想给项目加一层「可审计的文档元数据」。

**不适合**：需要真实锁、实时调度、跨仓库编排、Web Dashboard、自动 CI 的场景。

## 3. 目录结构

```
agent-workspace-governance/
├── cli/governance.py          ← 唯一可执行入口（stdlib-only）
├── schemas/                   ← document / task / agent / decision / project
├── constitution/              ← 原则 / Agent 规则 / 文档政策 / 人工审批政策
├── templates/                 ← ADR / change-proposal / execution-plan / handoff / research-report / review-report
├── adapters/                  ← generic / claude-code / codex / workbuddy / zcode（均为说明，未验证）
├── examples/
│   ├── basic-project/         ← 最小示例（`doctor` 退出码 0，可直接当模板）
│   └── render-notes/          ← Engine 适配记录
├── docs/                      ← architecture / specification / migration-guide
├── tests/test_governance.py   ← 41 个测试
└── README.md
```

治理产物写在**目标项目**的 `.governance/`：

```
你的项目/
└── .governance/
    ├── config.json
    ├── document-registry.json
    ├── task-registry.json
    ├── agent-registry.json
    └── adr-index.json
```

## 4. 如何初始化一个新项目

下文 `<KIT>` 指治理工具包根目录（即本仓库 `agent-workspace-governance/`）。请用**相对路径**或你自己环境里的路径替换，不要照抄别人的绝对路径。

```powershell
cd path\to\your-project
py -3 <KIT>\cli\governance.py init --project .
```

`init` 会（幂等）：

1. 创建 `.governance/` 与 5 个 JSON（已存在则不覆盖）。
2. 建立项目根 `AGENTS.md` 治理入口指针：
   - 文件**不存在或为空** → 生成完整指针入口（含 frontmatter）；
   - 文件**已存在** → 只在**末尾追加**一段带稳定标记的指针段（`<!-- governance-pointer:start -->` … `<!-- governance-pointer:end -->`），**原有内容逐字节不变**，不覆盖、不重复追加；
   - 文件**已含标记** → 不做任何修改。
3. 指针里的工具包路径在运行时按「相对项目根目录」解析（Windows 跨盘符时退回绝对路径），不再写死目录名或盘符。

> `--project` 一律相对当前目录解析；文件路径含空格/中文均可。若已有 `AGENTS.md` 不是 UTF-8 文本，`init` 不会改动它，并会打印明确的「警告」行，此时按 §6 手工补指针。

## 5. 如何配置治理规则

编辑 `.governance/config.json`：

| 字段 | 作用 | 默认 |
|---|---|---|
| `project_id` / `name` / `description` | 项目标识 | 目录名 |
| `doc_root` | 扫描根目录 | `.` |
| `state_dir` | 治理产物目录 | `.governance` |
| `doc_levels` | 文档层级 | `L1/L2/L3` |
| `lifecycles` | 三类生命周期（general / change_proposal / adr） | 见示例 |
| `registries` | 四个注册表文件名 | 固定 |
| `adapters` | 使用的宿主适配器 | `generic` |

**13 类合法文档类型**（type 必须在此枚举内，否则 doctor 报错）：
`ADR / Spec / Plan / Task / Runbook / Glossary / Architecture / Skill / Workflow / Script / Handoff / Audit / Session Note`

**6 个必填 frontmatter**：`doc_id / type / status / owner / created / updated`。

## 6. 如何建立项目上下文

`init` 会自动在已有 `AGENTS.md` 末尾追加治理入口指针段（见 §4）。只有在该文件不是 UTF-8 文本、`init` 打印警告并跳过时，才需要手工加一段：

```markdown
<!-- governance-pointer:start -->

## Agent 治理入口

- 工具包：`<相对项目根的路径>/agent-workspace-governance/`
- 先读：`<KIT>/constitution/AGENT_RULES.md`
- 文档政策：`<KIT>/constitution/DOCUMENTATION_POLICY.md`
- 文档有效性：查 `.governance/document-registry.json`，不要遍历猜测
- 人工审批：`<KIT>/constitution/HUMAN_APPROVAL_POLICY.md`

<!-- governance-pointer:end -->
```

**验收**：`rg "governance-pointer:start" AGENTS.md` 恰好 1 处命中；指针里的 `constitution/`、`AGENTS.md`、`cli/governance.py` 路径相对项目根真实存在。

## 7. 如何管理文档

```powershell
$G = "<KIT>\cli\governance.py"

py -3 $G inventory --project .      # 扫描并登记（不改源文件）
py -3 $G validate  --project .      # 校验 frontmatter/必填/引用
py -3 $G audit     --project .      # 冗余/孤儿/冲突/过期引用/未登记
py -3 $G archive-check --project .  # 归档条件
py -3 $G status    --project .      # 任务与审批状态
py -3 $G map       --project .      # Agent/Skill/Tool/MCP 映射
```

典型输出：`inventory` 会告诉你「登记 N 篇、跳过 M 篇」；`validate` 会逐条列出缺字段；`audit` 会列出孤儿/重复/过期引用。

> `inventory` 只登记，**不改源文件**；补 frontmatter 需要你手工或另写脚本。

## 8. 如何管理任务

任务契约是 `schemas/task.schema.json`，必填 11 项：

`task_id / title / owner_agent / status / read_paths / write_paths / protected_paths / dependencies / outputs / acceptance_criteria / human_approval_required`

**当前现实**：没有 `task create/claim` CLI；需要手工编辑 `.governance/task-registry.json`。
`doctor` 会检查单写者冲突与依赖环，但**不会**检查「in_progress 是否缺 claimed_at」（文档声称会，实测不会）。

最小任务示例：

```json
{
  "task_id": "TASK-001",
  "title": "补充 L20 教材",
  "owner_agent": "qwenwork",
  "status": "in_progress",
  "read_paths": ["courses/"],
  "write_paths": ["courses/video-rendering-journey/lessons/L20-*.md"],
  "protected_paths": ["web/content.js"],
  "dependencies": [],
  "outputs": ["L20 正文", "门禁日志"],
  "acceptance_criteria": ["validate 12/0/0", "arc OK"],
  "human_approval_required": true
}
```

## 9. 如何进行 Agent Handoff

```powershell
py -3 $G handoff --project . --task TASK-001 --to "下一个 Agent"
```

它会用 `templates/handoff.md` 生成一份包含任务、写入范围、验收标准的交接文档。

**限制**：只替换模板占位符，不校验交接对象是否真实存在，也不检查审批。

## 10. 如何管理 ADR

```powershell
py -3 $G adr create --project . --title "采用事件溯源"
py -3 $G adr list   --project .
py -3 $G adr check  --project .
```

- 模板是 MADR；索引写 `.governance/adr-index.json`。
- 合法状态：`proposed / accepted / deprecated / superseded`。
- **限制**：`accepted/deprecated/superseded` 的推进需要手改 JSON 或文件；`check` 只校验状态枚举与 `human_approved`。

## 11. 如何管理 Skills / MCP / Tools

用 `agent-registry.json` 的 agent 条目承载：

| 字段组 | 字段 |
|---|---|
| 身份 | `agent_id` / `agent_name` / `provider` / `model` / `harness` |
| 能力 | `capabilities` / `supported_skills` / `supported_mcp` / `supported_tools` |
| 运行 | `context_limit` / `invocation_mode` / `parallel_capability` / `background_task_capability` / `file_access_scope` |
| 验证 | `config_present` / `discovery_success` / `invocation_success` / `runtime_verification_status` / `verification_record` |

**诚实的边界**：
- 没有独立的 skills/MCP registry，只有 agent 条目里的列表。
- 没有 `install` 状态；`config_present` 只是「配置在」。
- `verified` 是单 Agent 级总状态，不是逐能力验证。

## 12. 如何配置兼容性

`adapters/` 下有 5 份说明（generic / claude-code / codex / workbuddy / zcode）。它们是**说明与检查表**，不是自动安装器。

当前 5 个 adapter 的 `discovery_success` / `invocation_success` 全部为**未验证**。不要把它们当「已支持」。

## 13. 如何运行检查脚本

```powershell
# 工具包自身测试（41 个，纯临时目录，不联网）
py -3 <KIT>\tests\test_governance.py

# 目标项目诊断（只读）
py -3 $G doctor --project .

# 目标项目校验
py -3 $G validate --project .
```

退出码：`doctor` 发现问题 → **非零**；`validate` 有错误 → 非零。

## 14. 如何使用模板

| 模板 | 用途 |
|---|---|
| `adr-template.md` | 架构决策 |
| `change-proposal.md` | 变更提案（before/after/风险/回滚） |
| `execution-plan.md` | 执行计划（阶段/产物/验收） |
| `handoff.md` | 交接 |
| `research-report.md` | 研究报告 |
| `review-report.md` | 审核报告 |

复制到目标项目对应目录后填写；不要改模板本身（模板是工具包资产）。

## 15. 如何迁移到已有项目

### 15.1 从空白仓库开始的完整示例

```powershell
mkdir demo-gov; cd demo-gov
git init
"# Demo" | Out-File README.md -Encoding utf8

py -3 <KIT>\cli\governance.py init --project .
py -3 <KIT>\cli\governance.py inventory --project .
py -3 <KIT>\cli\governance.py validate --project .
py -3 <KIT>\cli\governance.py doctor --project .
```

预期：`init` 生成 5 JSON + `AGENTS.md`；`inventory` 登记 1 篇；`validate`/`doctor` 对无 frontmatter 的 README 报缺字段。

### 15.2 接入现有项目（推荐路径）

1. **备份/分支**：`git status` 必须干净；新建分支 `chore/governance`。
2. `init --project .`（创建 `.governance/`；已有 `AGENTS.md` 则只在末尾追加指针段，原内容不变）。
3. `inventory --project .`：先看规模（Engine 183 篇）。
4. 检查 `AGENTS.md` 末尾的治理入口指针段（`init` 已自动追加，见 §6）。
5. **分批**补 frontmatter：先 L1 核心文档（10–20 篇），再逐步。
6. `validate` / `doctor` 从「几百项」降到可接受，再考虑纳入 CI。
7. 提交 `.governance/` 与 `AGENTS.md`（一次独立 commit，便于回滚）。

### 15.3 实际示例：Engine 适配结果

```powershell
py -3 <KIT>\cli\governance.py doctor --project path\to\ai-knowledge-to-learning-engine
```

实测（审计基线）：`183 docs`、`621 项诊断问题`、`exit 1`。这不是失败，是「存量文档元数据未补齐」的真实规模。**不要**因此认为工具坏了；也不要指望一次补齐。本次新增 2 份使用文档后，重建注册表为 **185 docs**（百分比口径相应变化）。

### 15.4 迁移限制

- 不改源文件：不会自动补 frontmatter。
- 13 类 type 与很多项目现有 type 不兼容（Engine 146/183 为 unknown）。
- 已有 `AGENTS.md` 只在末尾追加指针段，原有内容逐字节不变（重复 `init` 不再追加）。
- 不生成 CI 配置。

### 15.5 回滚

1. `git status` 确认新增的只有 `.governance/` 与 `AGENTS.md` 改动。
2. 用 `git checkout -- AGENTS.md` 撤销 `init` 追加的指针段（若你另外改过内容，请先手工删掉 `governance-pointer` 标记段）。
3. `.governance/` 用**回收站**移除（不要 `rm -rf`）；或 `git clean` 前先确认未被跟踪。
4. 若已提交：`git revert <commit>`（不要 rewrite 历史）。

## 16. 常见问题

**Q1：为什么 `doctor` 对 Engine 报 621 项？**
A：183 篇里大量文档没有 frontmatter 或 type 是 `unknown`；每篇 3–4 项，累计 621。属于存量债务。

**Q2：`9/9` 是什么意思？**
A：`examples/render-notes/README.md:74-88` 的九条对照表。**审计结论：这是文档自证，不是九项自动化验收**；其中第 8 项「独立示例项目」已由 `ExampleProjectTests` 覆盖（`doctor` 退出码 0）。

**Q3：能直接用 `examples/basic-project` 当模板吗？**
A：可以。其 2 篇文档的 type 已改为 13 类枚举内的 `Architecture` / `Spec`，注册表与 `inventory` 重跑结果一致，`doctor` 退出码 0。

**Q4：能替代 Engine 的 run_state 吗？**
A：不能。它没有 run_state、KCR、审核门。它是文档/任务元数据层，不是编排器。

**Q5：能在 CI 里跑吗？**
A：可以，但先让 `validate`/`doctor` 达到可接受噪声；当前无 CI 配置与依赖声明。

**Q6：为什么测试用 `py -3 tests\test_governance.py` 而不是 pytest？**
A：项目未依赖 pytest；本机也没有安装。直接运行脚本即可（41 tests OK）。

## 17. 已知缺陷（2026-11-23 审计；2026-11-25 更新 P0 修复状态）

1. ~~`examples/basic-project` 的 2 个 type 非法 → `doctor` exit 1~~ **已修复（2026-11-25）**：示例 type 改为 `Architecture` / `Spec`，`doctor` exit 0。
2. ~~`init` 对已存在 `AGENTS.md` 静默跳过；指针路径硬编码工具包目录名~~ **已修复（2026-11-25）**：改为末尾追加带稳定标记的指针段（幂等、原内容不变），路径相对项目根解析。
3. Engine `AGENTS.md` 尚未接入治理入口 → **能力已具备但未对真实目录执行**（已在副本上验证：原 953 字节逐字节不变 + 指针段追加 + 重复 init 幂等）。在真实 Engine 上执行 `init` 需人工授权。
4. `task=0 / agent=0 / adr=0`（真实项目里三个注册表为空）。
5. 人工审批要求「写入 `.governance/`」但没有 schema/存储字段。
6. `AGENT_RULES.md:75` 声称 doctor 检查 task claim，实测不检查。
7. 命令数三处口径不一致（README 9 / AGENTS 9 / 文档 11）。
8. 无 CI、无 `pyproject.toml`、无依赖声明；只能绝对路径调用。
9. **新增记录**：13 类枚举里没有「入口指针 / README / 指南」这类文档的类型。`init` 生成的指针 frontmatter 为 `type: adapter-entry`（本工具包自己的 AGENTS.md 同样如此），`inventory` 登记后 `doctor` 会对该条目报 1 项 type 枚举错误。是否新增类型（如 `Entry`）涉及规范 §十三的「13 类」口径，需人工裁决，本次未改。

---

**最后验证**：2026-11-25，Governance `73b22c8` + P0 修复（未提交）；`41 tests OK`；`doctor examples/basic-project` exit 0；Engine 副本 `init` 后 `doctor` 仍为 `183 docs / 621 项 / exit 1`（与 init 前完全一致，属存量债务）。
**最近更新**：2026-11-25。