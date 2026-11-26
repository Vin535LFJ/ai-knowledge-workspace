---
doc_id: CONSOL-LEGACY
type: archive
status: archived
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# legacy/ · 归档区（只读，不维护，不进学习站）

D22（2026-11-26）统一收敛的归档产物。本目录内容**保留历史价值但退出日常维护**；
发布边界 v2 默认拒绝未登记资产，本目录不进入学习站 bundle。

| 子目录 | 来源 | 说明 |
|---|---|---|
| `agent-workspace-governance/` | 原独立仓 agent-workspace-governance（HEAD 7d9a187，6 笔提交） | 通用治理工具包整仓归档。41 测试与 USER-GUIDE 已知缺陷清单原样保留。其中 `check_frontier` / `detect_dependency_cycles` / `_dependency_ids` 三个纯函数已改编并入 `tools/run_state.py`（D22，出处注明）。归档理由与逐项能力对照见 `docs/consolidation/audit-governance.md`。原仓 git 历史备份：`AI-Knowledge-backups/2026-11-26-consolidation/agent-workspace-governance/history.bundle`（恢复验证 PASS）。 |
| `governance-engine-adaptation-20261121/` | 原 Engine 根 `.governance/`（git mv） | 2026-11-21 治理适配实跑产物：183 条过时文档注册表 + 三个空注册表（task/agent/adr）。双轨治理残留，D22 清除出活跃区。Engine 唯一文档注册表是 `.agent/indexes/document-registry.json`。 |

## 使用约束

- 不得把本目录内容当作现行规范引用；现行治理正文在 `.agent/constitution/`。
- 归档测试可运行（`py -3 -m unittest discover -s legacy/agent-workspace-governance/tests`，需在该目录下执行），但不属于核心门禁套件。
- 如需恢复原独立仓：从备份区 bundle 克隆（`git clone history.bundle`），已验证 HEAD/tree/逐文件一致。