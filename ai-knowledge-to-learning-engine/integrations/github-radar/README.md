---
doc_id: "readme"
type: "readme"
status: "active"
owner: "qwenwork"
created: "2026-11-19"
updated: "2026-11-26"
---

# github-radar · Engine 内部 Research Discovery 模块

**外部项目发现与人工筛选的研究入口**，是 AI Knowledge-to-Learning Engine 的内部模块（D22 并入 `integrations/github-radar/`），**不是独立产品，不是长期运行的情报系统**。它只负责发现候选、记录快照、计算增长、人工筛选与导出；**绝不自动向知识库写入任何内容**，不开发调度平台或自动采集平台。

> **唯一权威口径见 [INTEGRATION.md](INTEGRATION.md)**（并入说明、运行方式、本地数据、与 Engine 的边界）。本 README 是技术参考；两者冲突时以 INTEGRATION.md 为准。

## 文档入口

- **[INTEGRATION.md](INTEGRATION.md)** — 模块定位、从 Engine 根的运行命令、真实数据限制、人工批准边界（权威）。
- [docs/USER-GUIDE.md](docs/USER-GUIDE.md) — 使用指南：发现/快照/增长/评分/报告/导出、Rate Limit、备份恢复、已知缺陷。
- [docs/data-model.md](docs/data-model.md) · [docs/engine-interface.md](docs/engine-interface.md) · [docs/operating-guide.md](docs/operating-guide.md)
- 审计与成熟度：[../../program/AUDIT-REPORT.md](../../program/AUDIT-REPORT.md)（结论 **PARTIAL**）。

## 当前状态（2026-11-26）

- 可用：八项能力代码齐备，**58 个离线测试通过**；已完成一次真实匿名采集（121 仓 / 200 快照 / 1 次运行）。
- **真实数据限制**：快照时间跨度仅约 20 秒 → 增长 121/121 全部 `insufficient_history=true`，**当前历史不足以计算有效增长**；无日常快照 CLI、无调度、无 HTTP 缓存。
- **两个真实库均为旧 schema**（无 approver/approved_at 列）；升级需用户批准（PD-Q15），副本验证已通过。
- 数据正确性修复（2026-11-25）：`analyze` 只更新机器字段，不覆盖人工审核状态；`export --approved` 必须带 `--approver`，批准状态写入数据库后再导出。
- **Engine 摄取端未实现**（有意：接通需人工批准候选后另行立项）；现有 demo 导出物 `human_selected_for_research=false`，只是格式样例。
- 成熟度：**PARTIAL**。使用前先读 USER-GUIDE §20 与 INTEGRATION.md。

## 名称与位置（D22 后）

- 现位置：核心仓内 `integrations/github-radar/`。原独立仓 `github-project-radar` 已退出使用，git 历史备份在 `AI-Knowledge-backups/2026-11-26-consolidation/github-project-radar/history.bundle`（恢复验证 PASS）。
- 文档与代码中出现的 `github-radar` / `github-project-radar` 均指本模块。

## 能力与边界

模块提供以下**手动 CLI 能力**（无调度、无实时监控、无 Dashboard、无前端）：

1. **发现候选**：按外部化主题分类法（`config/topics.json`）从搜索结果发现仓库。
2. **记录快照 / 计算增长**：依靠自己的快照数据库，只用真实快照计算 24h/7d/30d 增长；历史不足时明确标记 `insufficient_history`，绝不编造。
3. **三维独立评分**：发现信号 / 工程质量 / 学习生态相关性（见下）。
4. **人工筛选与导出**：只有 `human_selected_for_research=true` 的候选才允许导出为研究任务；导出是纯输出，**导入由 Engine 人工决定**，Radar 初筛分数不得当作知识证据。

默认约定：

- 存储 **SQLite**（单文件，零依赖）；仅采集**公开仓库**。
- 数据源默认 `fixtures/`（离线、无网络）；`collect --source rest` 走真实 GitHub REST（匿名或 `GITHUB_TOKEN`）。`trending.py`/`ossinsight.py` 仍是离线 stub。
- 令牌等敏感信息**仅通过环境变量提供**；源码、配置、日志中不含任何令牌。
- 真实数据库与 research 输出已被 Engine `.gitignore` 覆盖，**绝不入库**。

## 快速开始（从 Engine 根目录运行）

```powershell
# 测试（58 项，独立进程，避免顶层包名与 Engine 工具冲突）
py -3 -m unittest discover -s integrations/github-radar/tests

# CLI（--db 建议显式指定；真实库为旧 schema，升级前需 PD-Q15 批准）
py -3 integrations/github-radar/cli/radar.py init-db --db integrations/github-radar/radar-real-20261121.db
py -3 integrations/github-radar/cli/radar.py collect --source rest --max-queries 4 --db <db>
py -3 integrations/github-radar/cli/radar.py snapshot --db <db>
py -3 integrations/github-radar/cli/radar.py analyze --db <db>
py -3 integrations/github-radar/cli/radar.py candidates --db <db>
py -3 integrations/github-radar/cli/radar.py report --db <db>
py -3 integrations/github-radar/cli/radar.py review <候选id> --current Discovered --target Triaged --reviewer <姓名> --decision "说明" --db <db>
py -3 integrations/github-radar/cli/radar.py export --db <db> --approved --approver "<姓名>" --output <path>
py -3 integrations/github-radar/cli/radar.py query "SELECT COUNT(*) AS n FROM snapshots" --db <db>
```

`--db` 指定数据库路径；`report` 用 `--reports-root` 指定周报根目录。运行 `py -3 integrations/github-radar/cli/radar.py --help` 查看中文帮助。

## 命令一览

| 命令 | 作用 |
|---|---|
| `init-db` | 建表（幂等；含 approver 等列的 ALTER 升级） |
| `collect` | 发现采集：默认 fixtures（无网络）；`--source rest` 走真实 GitHub REST |
| `snapshot` | 记录仓库指标快照（历史只增不改） |
| `analyze` | 增长 + 加权评分，写入候选池（不覆盖人工字段） |
| `candidates` | 列出候选记录（可按状态过滤） |
| `report` | 生成周报：`--format dir`（默认 7 文件）/ `summary`（单文件）/ `json` |
| `review` | 人工复核状态转换（无自动副作用） |
| `export` | 导出研究任务 JSON（纯输出；`--approved` 须带 `--approver`） |
| `query` | 执行只读 SQL |

## 三维独立评分

`radar.scoring.evaluate_three_scores(repo, topic_config, growth=None, group=None)` 输出三个**彼此独立**的分数：

| 分数 | 含义 | 主要子信号 |
|---|---|---|
| `discovery_signal` | 发现信号 | 24h/7d/30d 星标增长、Fork 增长、提交活跃度、相对新颖性 |
| `engineering_quality` | 工程质量 | README 清晰度、文档可运行、许可证、版本发布、Issue/PR 维护、社区活跃 |
| `relevance` | 对我学习生态的相关性 | Engine / Agent Docs Governance / Radar 本身 / 网站体验与教学交互 / 音视频-GPU 五维 |

每个分数含 `score`（数字或 `"unknown"`）、`explanation`、`basis`。字段缺失标 `unknown`，**不默认满分或零分**。规则与权重在 `config/scoring.json` 的 `three_scores` 块。**注意**：三维分已在库函数实现并测试，但尚未接入 `analyze`/报告（当前报告仍用旧综合分）。

## 生命周期与状态别名

canonical：`discovered → triaged → watchlist → deep_dive → adopted / rejected / archived`。旧状态作 1:1 别名：`Watch≡watchlist`、`Research≡deep_dive`、`Adopt≡adopted`、`Ignore≡rejected`。`radar.review.normalize_status()` 双向兼容；`record_transition()` 生成含时间/操作人/理由的变更记录。去重按 `repository_id`，rename/transfer 保留历史映射。

## 溯源字段与数据源

`Repository`/`Snapshot`/`Candidate` 带可选溯源字段 `source_url`/`observed_at`/`retrieved_at`/`data_quality`，经 `to_dict()`/`from_dict()` 往返透传。`radar/sources/` 提供 `SourceClient` 抽象；`rest.py` 已实现真实 GitHub REST（含 7s 匿名节流与退避），`trending.py`/`ossinsight.py` 为离线 stub。默认注入 `fixtures/client.py`，只有显式 `--source rest` 才联网。

## 配置与目录

- `config/topics.json`：主题分类法（追加条目即生效）。
- `config/scoring.json`：`version=2`；`weights` 旧综合分权重，`three_scores` 三维独立评分。

```
config/    主题与评分配置
radar/     核心模块（models/storage/collector/growth/scoring/reports/research/review/export）
radar/sources/  数据源适配器（base + rest/trending/ossinsight）
fixtures/  离线样例响应（默认注入客户端）
cli/       命令行入口
tests/     unittest 测试（58 项）
reports/   周报输出（ignored）
research/  深度研究模板输出（模块根，ignored）
docs/      数据模型、操作指南、引擎接口
```

## 许可证

MIT，见 `LICENSE`。