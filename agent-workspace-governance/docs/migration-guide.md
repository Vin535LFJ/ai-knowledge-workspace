---
doc_id: MIGRATION_GUIDE
type: migration-guide
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-25
---

# 迁移指南：把治理工具包接入任意项目

## 一、适用场景

- 你的项目有多个 AI Agent / 多个 AI 编码工具协作。
- 你想要可移植、可迁移的规则——不绑平台、不绑云端。
- 你不想要重型多 Agent 平台，也不想引入编排器。

## 二、三步接入

### 第 1 步：初始化

```bash
py -3 <kit>/cli/governance.py init --project <your-project>
```

产出（幂等，不覆盖已有文件）：
- 项目根 `AGENTS.md` 指针（已存在时只在末尾追加带标记的指针段，原内容不变）
- `.governance/config.json`
- 四个注册表骨架

### 第 2 步：登记与校验

```bash
py -3 <kit>/cli/governance.py inventory --project <your-project>
py -3 <kit>/cli/governance.py validate  --project <your-project>
```

`inventory` 扫描所有 Markdown，提取 frontmatter，按 `doc_id` upsert 到文档注册表。
`validate` 检查 `doc_id/type/status/owner/created/updated` 必填字段与引用完整性；失败返回非零退出码。

> 若现有文档缺 frontmatter，请先补上这 6 个字段。`owner` 不能为空——无 owner 是典型问题。`type` 请取 13 类标准类型（见 [`specification.md`](specification.md) §十三），否则 `doctor` 会报错。

### 第 3 步：日常使用

```bash
py -3 <kit>/cli/governance.py status       --project <your-project>
py -3 <kit>/cli/governance.py map          --project <your-project>
py -3 <kit>/cli/governance.py handoff      --project <your-project> --task TASK-001
py -3 <kit>/cli/governance.py adr create   --project <your-project> --title "采用事件溯源"
py -3 <kit>/cli/governance.py adr list     --project <your-project>
py -3 <kit>/cli/governance.py archive-check --project <your-project>
py -3 <kit>/cli/governance.py audit        --project <your-project>
```

## 三、frontmatter 最小示例

```markdown
---
doc_id: design-doc
type: Spec
level: L1
status: active
owner: alice
created: 2026-11-19
updated: 2026-11-19
---

# 设计文档正文
```

## 四、从 Render_Notes 迁移

见 [`examples/render-notes/README.md`](../examples/render-notes/README.md) 的具体映射表。要点：

- `.agent/constitution/` → `constitution/`（权威正文，只做指针）
- `.agent/decisions/0001-*.md` → ADR
- `DECISIONS.md` → 历史索引
- `reviews/` → 评审报告
- `reviews/KNOWLEDGE_CHANGE_REVIEW.md` → KCR Adapter（项目适配器，不是通用规则）
- `WORKFLOW_STATE.md` → L1 项目状态（状态机由项目自己保留）
- `.agent/skills/research-to-learning/` → 外部技能引用（不重建）

**不重写 Render_Notes 的知识结构，不叠加三套完整工作流。**

## 五、普通项目示例

见 [`examples/basic-project/`](../examples/basic-project/README.md)：一个不含任何知识结构的普通软件项目，证明本工具包无 Render_Notes 依赖。

## 六、接入后的纪律

1. 每个任务写清 owner 与读写范围；并行写冲突要警告。
2. ADR 只记架构决策，人工推进状态。
3. 正式文档单一权威来源，工作文档分离。
4. 人工审批清单必须遵守；无回复 ≠ 同意。
5. Agent 能力未验证标记 `unverified`。
6. Adapter 只做指针，不复制规则正文。
