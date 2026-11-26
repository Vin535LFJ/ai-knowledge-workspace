---
doc_id: README
type: root-readme
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-26
---

# Agent Workspace Governance

**一个可移植、可迁移的「Agent 项目治理工具包」。**

它让多个 AI Agent 与多个 AI 编码工具在同一个项目里协作时，有一套共同遵守的「协作规则」——文档权威、任务归属、共享上下文、文档状态、ADR、变更管理、Agent 身份与能力映射、人工审批、交接与审计。

它不是重型多 Agent 平台，也不是任务编排器（orchestrator）。

## 文档入口

- **[docs/USER-GUIDE.md](docs/USER-GUIDE.md)** — 使用指南：初始化、文档/任务/交接/ADR、迁移到已有项目、回滚、已知缺陷。
- [docs/specification.md](docs/specification.md) — 规范；[docs/architecture.md](docs/architecture.md) — 架构；[docs/migration-guide.md](docs/migration-guide.md) — 迁移。
- `examples/basic-project/` — 最小示例（`doctor` 退出码 0，可直接当模板）。
- `examples/render-notes/README.md` — Engine 适配记录与九条对照表。

## 当前状态（2026-11-23 独立审计；2026-11-25 更新）

- 可用：`init / inventory / validate / doctor / audit / adr / handoff`，41 个测试通过，Engine 183 篇文档登记可复现。
- 2026-11-25 修复两项 P0：示例 `basic-project` 的 `doctor` 退出码 0；`init` 可接入已有 `AGENTS.md`（末尾追加指针段，幂等、原内容不变）。
- 2026-11-26：5 笔提交作者统一重写为 `Vin535LFJ <169535939+Vin535LFJ@users.noreply.github.com>`，公司邮箱从提交历史移除；tree 哈希前后一致（内容零改动）；无 remote，不涉及推送。
- 未闭环：Task/审批/Agent 注册在真实项目中为空；`9/9` 是文档自证；Engine 真实目录尚未执行 `init`（仅在副本上验证）。
- 成熟度：**PARTIAL**。详见 `../ai-knowledge-program/AUDIT-REPORT.md`。

---

## 一、三个概念的边界（重要）

本工具包只解决三者中的「治理」这一层。请务必区分：

| 概念 | 含义 | 由谁负责 |
| --- | --- | --- |
| **Agent Skills（Agent 技能）** | 单个 Agent「如何工作」——研究、写作、审查等可复用能力。 | 复用外部技能库，本工具包**绝不重复造技能集**。参考：<https://github.com/Vin535LFJ/mattpocock-skills-zh-CN-custom> |
| **Agent Governance（Agent 治理）** | 多个 Agent 在**同一个项目内**如何协作——文档权威、任务归属、共享上下文、文档状态、ADR、变更管理、Agent 身份与能力映射、人工审批、交接、审计。 | **正是本工具包提供的内容。** |
| **Agent Orchestration（Agent 编排）** | 真正的任务调度与执行——把任务排程、分发、驱动完成。 | 由**各业务项目自己保留**。例如 Render_Notes 自带轻量状态机（`WORKFLOW_STATE.md`）。本工具包**不实现编排器**。 |

一句话记忆：**Skills 管「怎么干」，Governance 管「谁在何时按什么规则干」，Orchestration 管「真正把活排起来干」。**

本工具包刻意不碰 Skills，也不做 Orchestration，因此它可以被任何项目「插拔式」采用。

---

## 二、设计原则（速览）

1. 项目独立、可迁移——治理配置随项目走，不绑定某个平台。
2. 每份正式文档只有一个权威来源（single authoritative source）。
3. 工作文档与正式文档严格分离。
4. 所有 Agent 共用同一套规则。
5. 每个任务一个 owner + 明确读写范围。
6. 每次文档变更都有来源与记录。
7. ADR 只用于架构决策。
8. 普通计划不产生 ADR。
9. 重要状态机器可读。
10. 人工决策不可被 AI 替代。
9. Adapter 不复制规则正文，只做指针/索引。
12. 未经验证的 Agent 能力显式标记为 unverified。

完整 12 条见 [`constitution/PROJECT_PRINCIPLES.md`](constitution/PROJECT_PRINCIPLES.md)。

---

## 三、目录结构

```
agent-workspace-governance/
├── constitution/      # 治理章程：原则、Agent 规则、文档策略、人工审批策略
├── schemas/           # JSON Schema：project/document/agent/task/decision
├── templates/         # Markdown 模板：ADR/变更提案/研究报告/执行计划/交接/评审
├── skills/            # 说明：本工具包引用外部技能，不重建
├── adapters/          # 各客户端适配说明（generic/claude-code/codex/workbuddy/zcode）
├── cli/               # governance.py（9 个命令）
├── tests/             # unittest 测试
├── examples/          # basic-project 与 render-notes 两个示例
└── docs/              # 架构、规范、迁移指南
```

---

## 四、快速开始

### 1. 在目标项目初始化

```bash
py -3 path/to/agent-workspace-governance/cli/governance.py init --project path/to/your-project
```

`init` 会（幂等地）：
- 建立 `AGENTS.md` 治理入口指针：文件不存在时生成；**已存在时只在末尾追加带稳定标记的指针段，原有内容逐字节不变，重复执行不再追加**；
- 生成 `.governance/config.json`；
- 生成 `.governance/` 下的注册表骨架（document / task / agent / adr）。

`--project` 相对当前目录解析；指针中的工具包路径相对项目根目录计算（不写死盘符），支持含空格/中文的路径。

### 2. 登记文档 → 校验 → 查看状态

```bash
py -3 governance.py inventory --project path/to/your-project   # 扫描并登记文档
py -3 governance.py validate  --project path/to/your-project   # 校验元数据/引用
py -3 governance.py status    --project path/to/your-project   # 任务与审批状态
py -3 governance.py map       --project path/to/your-project   # Agent/Skill/Tool/MCP 映射
```

### 3. 日常治理动作

```bash
py -3 governance.py handoff      --project ... --task TASK-001
py -3 governance.py adr create   --project ... --title "采用事件溯源"
py -3 governance.py adr list     --project ...
py -3 governance.py archive-check --project ...
py -3 governance.py audit        --project ...
```

---

## 五、CLI 命令一览

| 命令 | 作用 |
| --- | --- |
| `init` | 在目标项目初始化治理配置（幂等） |
| `inventory` | 扫描项目文档并登记到文档注册表（含 frontmatter 提取） |
| `index` | `inventory` 的别名，行为完全一致（保留 `inventory` 名向后兼容） |
| `validate` | 校验 frontmatter / 元数据 / 必填字段 / 引用；失败时非零退出 |
| `status` | 从任务注册表展示任务与审批状态 |
| `map` | 从 Agent 注册表展示 Agent / Skill / Tool / MCP 映射 |
| `handoff` | 从任务生成标准交接文档 |
| `adr` | 创建 / 列出 / 检查 ADR |
| `archive-check` | 检查文档与任务的归档条件 |
| `audit` | 发现冗余 / 孤儿 / 冲突 / 过期引用 / 未登记文档 |
| `doctor` | 只读诊断：JSON 可解析 / 必填字段 / type 枚举 / 单写者冲突 / 依赖环；有问题时非零退出 |

通用参数：`--project PATH`（目标项目路径，默认当前目录）。所有命令均为纯本地文件操作，不联网、不执行 git。

---

## 六、状态与数据

所有状态以 JSON 存放于目标项目的 `.governance/` 目录：

- `config.json` —— 项目治理配置
- `document-registry.json` —— 文档注册表（索引，不是另一套知识库）
- `task-registry.json` —— 任务注册表
- `agent-registry.json` —— Agent 注册表
- `adr-index.json` —— ADR 索引

> 文件所有权（file ownership）是**约定**，不是真实的锁。可在支持的客户端上用 hooks / pre-commit / CI 做辅助检查，但本工具包本身不实现分布式锁。

---

## 七、适配客户端

每个客户端有独立 Adapter 与验证记录，Adapter 只生成索引/指针/配置/兼容条目，**从不复制完整规则正文**：

- [`adapters/generic`](adapters/generic/README.md)
- [`adapters/claude-code`](adapters/claude-code/README.md)
- [`adapters/codex`](adapters/codex/README.md)
- [`adapters/workbuddy`](adapters/workbuddy/README.md)
- [`adapters/zcode`](adapters/zcode/README.md)

> 配置文件存在 ≠ 能被发现 ≠ 能成功调用。未验证的能力必须标记为 `unverified`。

---

## 八、许可

[MIT](LICENSE)

---

## 九、名称映射（架构文档建议名 ≡ 本地目录名）

新架构文档建议使用目录名 `agent-docs-governance`；本工具包当前实际目录名为 `agent-workspace-governance`。二者指向同一套治理工具包：

> `agent-docs-governance`（新架构文档建议名）≡ `agent-workspace-governance`（本地目录名）

按用户裁决，本轮**不改名**，仅做增量补齐；所有命令、路径引用与文档继续沿用本地目录名 `agent-workspace-governance`。若未来统一改名，需同步更新 `AGENTS.md` 指针与 Adapter 中的路径引用。
