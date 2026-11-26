---
doc_id: ADP-AGENTS
type: adapter
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-26
related_adr: [ADR-0001]
generated: false
---

# AI Knowledge-to-Learning Engine — 通用 Agent 适配入口（Codex 等）

> 指针文件（D15 / ADR-0001）：只负责发现与跳转，**不复制智能体文档正文**。正文统一在 `.agent/`。

- **先读**：`.agent/README.md`（统一索引与读取规则）
- **技能**（按任务触发）：把资料做成课程、写教材、登记断言与证据 → `.agent/skills/research-to-learning/SKILL.md`；设计或优化学习页、实验页，做视觉与可读性审查 → `.agent/skills/learning-experience-design/SKILL.md`
- **协作规则**：`.agent/constitution/AGENT_RULES.md`（写所有权五规则：单写者 / 默认只读 / worktree / 生成物非源 / 交接）
- **文档政策**：`.agent/constitution/DOCUMENTATION_POLICY.md`（类型 × 生命周期 / L1-L3 / 状态机）
- **文档有效性**：先查 `.agent/indexes/document-registry.json`，不遍历仓库猜测
- **人工关卡**：`reviews/DECISION_REQUIRED.md`（未答复不视为同意）
- **决策**：`DECISIONS.md`（历史索引）+ `.agent/decisions/`（MADR）
- **项目管理**（目标 / 优先级 / 待决 / 交接）：`program/NOW.md` → `program/ROADMAP.md` → `program/decisions/PENDING_DECISIONS.md`（D22 并入，原独立 Program 仓已退出）
- **外部项目发现**（GitHub 候选 / 人工批准 / 导出）：`integrations/github-radar/INTEGRATION.md`（只读研究入口，不自动导入知识）
- **归档区**（Governance 工具包 / 旧适配产物，只读不维护）：`legacy/README.md`
- **整合决策与验收**（D22 结构 / 映射 / 证据）：`docs/consolidation/TARGET-ARCHITECTURE.md`
