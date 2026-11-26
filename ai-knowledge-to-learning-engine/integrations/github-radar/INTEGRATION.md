---
doc_id: RADAR-INTEGRATION
type: runbook
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# github-radar · Engine 内部研究入口模块（D22 并入说明）

原独立仓 github-project-radar（HEAD e2815d9，5 笔提交）于 2026-11-26 并入本目录。
定位：**外部项目发现与人工筛选的研究入口**，不是独立产品；不自动向知识库写入任何内容。
原仓 git 历史备份：`AI-Knowledge-backups/2026-11-26-consolidation/github-project-radar/history.bundle`（恢复验证 PASS）。

## 运行方式（从 Engine 根）

```powershell
# 测试（58 项，独立进程，避免顶层包名与 Engine 工具冲突）
py -3 -m unittest discover -s integrations/github-radar/tests

# CLI（--db 建议显式指定；默认落点为本目录 radar.db，已被 .gitignore 覆盖）
py -3 integrations/github-radar/cli/radar.py init-db --db integrations/github-radar/radar-real-20261121.db
py -3 integrations/github-radar/cli/radar.py candidates --db integrations/github-radar/radar-real-20261121.db
py -3 integrations/github-radar/cli/radar.py export --db <db> --approved --approver <人名> --output <path>
```

## 并入时的三处路径修正（审计 audit-radar.md §3）

1. `radar/research.py`：默认输出从 CWD 相对 `research/` 改为**模块根** `integrations/github-radar/research/`（已 gitignore）。
2. 默认 db/reports 落点随目录平移（`__file__` 推导）；Engine .gitignore 增加 `integrations/github-radar/*.db`、`*.db-journal`、`research/`，真实数据绝不入库。
3. 测试与 CLI 以独立进程运行（`radar`/`cli`/`fixtures` 顶层包名不与 Engine 工具同进程混用）。

## 本地数据（ignored，不入库）

- `radar-real-20261121.db`：121 仓 / 200 快照（2026-11-21 约 20 秒窗口，全部 insufficient_history=true）/ 121 候选（120 Discovered + 1 Research），human_selected_for_research=0。
- `radar-real-hdr.db`：空壳（仅 init-db）。
- **两库均为旧 schema（无 approver/approved_at 列）**。升级=下次含 init_db 的命令幂等 ALTER；对真实库执行前需用户批准（PD-Q15）。副本验证已通过（2026-11-25 稳定化报告）。

## 与 Engine 的边界（保持现状，不新建自动化）

- 导出契约：`docs/engine-interface.md`（15 字段，仅 human_selected_for_research=true 可导入）。
- Engine 摄取端**未实现**（有意：接通需人工批准候选后另行立项）；现有 demo 导出物该字段为 false，只是格式样例。
- 人工审核/批准门槛由代码强制（storage.approve_candidate 幂等、analyze 不覆盖人工字段，P0 已修，58 测试覆盖）。
- 不开发调度平台/自动采集平台（任务书与 PARKING-LOT 明确不做）。