---
doc_id: "readme"
type: "readme"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# GitHub Project Radar

**开源情报与技术发现系统** —— 不是 GitHub Trending 查看器，而是一个长期运行的智能发现体系。

## 文档入口

- **[docs/USER-GUIDE.md](docs/USER-GUIDE.md)** — 使用指南：首次运行、发现/快照/增长/评分/报告/导出、Rate Limit、备份恢复、已知缺陷。
- [docs/data-model.md](docs/data-model.md) · [docs/engine-interface.md](docs/engine-interface.md) · [docs/operating-guide.md](docs/operating-guide.md)

## 当前状态（2026-11-23 独立审计）

- 可用：八项能力代码齐备，38 个离线测试通过；已完成一次真实匿名采集（121 仓 / 200 快照 / 1 次运行）。
- 关键限制：快照时间跨度仅 20 秒 → 增长 121/121 为空；`analyze` 会覆盖人工复核状态；`--approved` 不置 `human_selected_for_research`；无日常快照 CLI、无调度、无 HTTP 缓存。
- 成熟度：**PARTIAL**。详见 `../ai-knowledge-program/AUDIT-REPORT.md`。使用前先读 USER-GUIDE §20。

## 名称映射（重要）

新架构文档中建议的项目名为 `github-radar`，本地实际目录为 `github-project-radar`。
按用户裁决：**保留现有目录名 `github-project-radar`，不改名**。两者指同一项目，
文档与代码中出现的 `github-radar` 均等同于本地目录 `github-project-radar`。

## 定位与目标

GitHub Project Radar 持续地：

1. **发现新项目**：按外部化主题分类法（AI Agent、Agent Skills、MCP & Tools 等）从搜索结果中发现仓库。
2. **追踪真实星标增长**：依靠自己的**每日快照数据库**，只用真实快照计算 24h/7d/30d 增长、活跃度与加速度；历史不足时明确标记，绝不编造数据。
3. **识别高价值信号**：发现 Agent Skills、MCP 服务、优秀工程实践。
4. **深度研究**：每周对少数高价值项目生成结构化研究框架（事实需查证，未验证内容标 `[未验证]`）。
5. **交接给知识引擎**：通过标准化 JSON 导出把获批研究候选交给 Render_Notes 的「知识到学习引擎」——**绝不自动修改知识库**。

## 默认约定（重要）

- 第一版存储：**SQLite**（单文件，零依赖）。
- 采集节奏：**每日快照** + **每周报告**。
- **无实时监控**、**无 Dashboard**、**无前端**。
- **不会自动导入 Render_Notes**；导出是纯输出，导入由外部引擎决定。
- 仅采集**公开仓库**。
- 令牌等敏感信息**仅通过环境变量 / 密钥提供**；源码、配置、日志中不含任何令牌。
- 数据源：默认 `fixtures/`（离线、无网络）；`collect --source rest` 走真实 GitHub REST（匿名或 `GITHUB_TOKEN`）。
- **三个独立分数**（发现信号 / 工程质量 / 学习生态相关性）已在库函数中实现并测试；**尚未接入 `analyze`/报告**（当前报告仍用旧综合分）。
- **生命周期**：canonical 状态为 `discovered → triaged → watchlist → deep_dive → adopted / rejected / archived`；旧状态 `Watch/Research/Adopt/Ignore` 作为别名保留。
- **人工门槛**：只有 `human_selected_for_research=true` 的候选才允许导出为可导入 Engine 的研究任务，导入后由 Research Agent 重新核验；Radar 初筛分数不得当作知识证据。

## 快速开始

```bash
# 1) 初始化数据库
py -3 cli/radar.py init-db

# 2) 发现采集：默认 fixtures（无网络）；真实 GitHub 用 --source rest
py -3 cli/radar.py collect --max-queries 5
py -3 cli/radar.py collect --source rest --max-queries 4

# 3) 记录一次快照（可重复执行；--captured-at 用于可复现测试）
py -3 cli/radar.py snapshot

# 4) 计算增长与评分，写入候选池
py -3 cli/radar.py analyze

# 5) 查看候选
py -3 cli/radar.py candidates

# 6) 生成周报：默认目录 7 文件；也可 --format summary（单文件 YYYY-Www.md）或 --format json
py -3 cli/radar.py report
py -3 cli/radar.py report --format summary
py -3 cli/radar.py report --format json

# 7) 人工复核状态转换
py -3 cli/radar.py review <候选id> --current Discovered --target Triaged --reviewer <姓名> --decision "说明"

# 8) 导出研究任务 JSON（纯输出）
py -3 cli/radar.py export --output research-tasks.json --status Research --approved

# 9) 只读 SQL 查询
py -3 cli/radar.py query "SELECT COUNT(*) AS n FROM snapshots"
```

`--db` 可指定数据库路径；`report` 用 `--reports-root` 指定周报根目录。运行 `py -3 cli/radar.py --help` 查看中文帮助。

## 命令一览

| 命令 | 作用 |
|---|---|
| `init-db` | 建表（幂等） |
| `collect` | 发现采集：默认 fixtures（无网络）；`--source rest` 走真实 GitHub REST |
| `snapshot` | 记录仓库指标快照（历史只增不改） |
| `analyze` | 增长 + 加权评分，写入候选池 |
| `candidates` | 列出候选记录（可按状态过滤） |
| `report` | 生成周报：`--format dir`（默认，7 文件目录）/ `summary`（单文件）/ `json`（机器可读） |
| `review` | 人工复核状态转换（无自动副作用） |
| `export` | 导出研究任务 JSON（纯输出） |
| `query` | 执行只读 SQL |

## 三维独立评分

`radar.scoring.evaluate_three_scores(repo, topic_config, growth=None, group=None)` 输出三个**彼此独立**的分数：

| 分数 | 含义 | 主要子信号 |
|---|---|---|
| `discovery_signal` | 发现信号 | 24h/7d/30d 星标增长、Fork 增长、提交活跃度、相对新颖性（领域关注度/贡献者变化当前无字段） |
| `engineering_quality` | 工程质量 | README 清晰度、文档可运行、许可证及类型、版本发布、Issue/PR 维护、社区活跃（测试/CI、安全策略、依赖健康等当前无字段） |
| `relevance` | 对我学习生态的相关性 | Engine / Agent Docs Governance / Radar 本身 / 网站体验与教学交互 / 音视频-GPU 五个维度 |

每个分数包含 `score`（数字或 `"unknown"`）、`explanation`（中文说明）与 `basis`（子信号列表）。
字段缺失的子信号标 `unknown`，**不默认满分或零分**；某维度全部子信号不可观测时整体分数为 `unknown`。
量化规则与权重/阈值定义在 `config/scoring.json` 的 `three_scores` 块，确定性、可单测。

## 生命周期与状态别名

canonical 状态：`discovered → triaged → watchlist → deep_dive → adopted / rejected / archived`。
`deep_dive` 表示人工选择深入调研；`adopted` 记录吸收位置与理由；`rejected` 记录原因避免反复出现；`archived` 表示不再跟踪或失活。
旧状态作为 1:1 别名保留：`Watch≡watchlist`、`Research≡deep_dive`、`Adopt≡adopted`、`Ignore≡rejected`；`Discovered/Triaged` 仅大小写差异。
`radar.review.normalize_status()` 双向兼容 canonical 与旧别名，fixtures 中的旧值仍可读；
`radar.review.record_transition()` 生成含时间/操作人/理由的变更记录。去重按 `repository_id`，rename/transfer 保留历史映射。

## 溯源字段

`Repository` / `Snapshot` / `Candidate` 均带可选溯源字段：`source_url`、`observed_at`、`retrieved_at`、`data_quality`。
这些字段可经 `to_dict()` / `from_dict()` 往返透传，并写入 SQLite 与导出 JSON。

## 数据源适配器

`radar/sources/` 提供 `SourceClient` 抽象接口（`fetch_repositories` / `fetch_trending` / `fetch_insights`）。
`rest.py` 已实现**真实 GitHub REST**（匿名或 `GITHUB_TOKEN`，含 7s 匿名节流与退避）；`trending.py`、`ossinsight.py` 仍是离线 stub（返回 fixture 形状的空数据，不发起网络请求）。
默认注入客户端仍是 `fixtures/client.py`；只有显式 `--source rest` 才会联网。令牌只能通过环境变量提供，不得硬编码。

## 配置（改配置即可扩展，无需改代码）

- `config/topics.json`：主题分类法。新增主题只需追加一个条目，发现、相关性评分、分组比较都会自动生效。
- `config/scoring.json`：`version=2`。`weights` 为旧综合分权重（创新 25 / 相关性 25 / 工程成熟度 15 / 可复用性 15 / 增长势能 20，保持不变）；`three_scores` 为三维独立评分的权重、阈值与维度列表。

## 目录结构

```
config/    主题与评分配置
radar/     核心模块（models/storage/collector/growth/scoring/reports/research/review/export）
radar/sources/  数据源适配器（base 接口 + rest/trending/ossinsight 离线 stub）
fixtures/  离线样例响应（默认注入客户端）
cli/       命令行入口
tests/     unittest 测试
reports/   周报输出：reports/YYYY-Www/（目录 7 文件）与 reports/YYYY-Www.md/.json（单文件）
research/  深度研究模板默认输出 research/owner__repo.md
docs/      数据模型、操作指南、引擎接口
```

## 测试

```bash
py -3 -m unittest discover -s "C:/Users/Giant/Desktop/GITCODE/github-project-radar/tests" -v
```

## 许可证

MIT，见 `LICENSE`。
