---
doc_id: ARCHITECTURE
type: architecture-doc
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 架构说明

## 一、总体定位

Agent Workspace Governance 是一个**可移植的治理工具包**：一组章程、Schema、模板、Adapter 指针与一个本地 CLI。它不提供运行时、不提供云端、不提供编排。

```
        ┌───────────────────────────────────────────┐
        │            目标业务项目（本地目录）        │
        │  AGENTS.md(指针) + .governance/*.json 状态 │
        └───────────────────┬───────────────────────┘
                            │ 治理 CLI（纯文件读写）
        ┌───────────────────▼───────────────────────┐
        │          治理工具包（本仓库）              │
        │  constitution/ schemas/ templates/         │
        │  adapters/ skills/(仅引用) cli/            │
        └───────────────────────────────────────────┘
```

## 二、组件职责

| 组件 | 职责 | 不是 |
| --- | --- | --- |
| `constitution/` | 治理规则的唯一权威正文 | 不是某客户端的私有配置 |
| `schemas/` | 数据结构的 JSON Schema（数据契约） | 不是数据库 DDL |
| `templates/` | 标准文档骨架（含占位符） | 不是填写好的正式文档 |
| `adapters/` | 各客户端的索引/指针/兼容配置 | 不复制规则正文 |
| `skills/` | 说明「引用外部技能，不重建」 | 不实现任何 Skill |
| `cli/governance.py` | 9 个治理命令，本地文件操作 | 不是编排器、不联网、不调用 git |

## 三、状态模型

所有状态位于目标项目的 `.governance/`，均为 UTF-8 JSON：

- `config.json` —— 项目身份、生命周期定义、注册表文件名
- `document-registry.json` —— 文档索引
- `task-registry.json` —— 任务契约
- `agent-registry.json` —— Agent 身份与能力
- `adr-index.json` —— ADR 索引

> 注册表是**索引**，不是第二套知识库；正文仍在各自的 Markdown 文件里。

## 四、CLI 数据流

```
init ──> 创建 AGENTS.md 指针 + .governance 骨架（幂等）
inventory ──> 扫描 *.md ──> 提取 frontmatter ──> upsert 文档注册表
validate ──> 检查 frontmatter/必填字段/引用 ──> 错误列表（失败非零退出）
status ──> 读 task-registry ──> 任务与审批状态
map ──> 读 agent-registry ──> Agent/Skill/Tool/MCP 映射
handoff ──> 读任务 + templates/handoff.md ──> 生成交接文档
adr ──> create/list/check ──> adr-index.json + docs/adr/*.md
archive-check ──> 旧 superseded 文档 + 已完成任务 ──> 归档候选
audit ──> 冗余/孤儿/冲突/过期引用/未登记
```

## 五、关键设计决策

1. **纯标准库**：不引入 PyYAML/jsonschema 等依赖，frontmatter 解析器只覆盖治理所需子集。
2. **幂等 init**：重复执行不覆盖用户已有配置，只补缺失文件。
3. **文件所有权是约定**：不实现真实锁；并行冲突靠约定 + 可选 hooks/CI 辅助。
4. **能力显式标注**：`runtime_verification_status` 默认 `unverified`，避免「配置存在即假设可用」。
5. **状态与正文分离**：JSON 只做索引与查询，Markdown 承载人类可读正文。

## 六、可扩展性边界

- 新增客户端：加一个 `adapters/<name>/README.md`，不碰规则正文。
- 新增文档类型：在 `document.schema.json` 与模板中扩展，不引入新状态机。
- 新增 CLI 命令：在 `cli/governance.py` 增加纯函数 + argparse 子命令 + 测试。

任何扩展都不得把本工具包变成编排器或重型平台。
