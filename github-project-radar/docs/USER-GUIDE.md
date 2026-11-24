---
doc_id: RADAR-USER-GUIDE
type: user-guide
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
verified_at: 2026-11-23
verified_against: github-project-radar@b7442da
---

# GitHub Project Radar 使用指南

> 一句话：本地 SQLite + 标准库的 GitHub 开源情报工具，能发现仓库、存快照、算增长、打分、生成周报、导出研究候选。
> **当前成熟度：八功能 MVP + 一次性真实抓取**。它还不是「可持续趋势系统」；用前先读 §20 的已知缺陷。

---

## 1. 项目定位

- 目的：把「发现值得研究/借鉴的 GitHub 项目」变成有记录、可解释、可复核的流程。
- 形态：`cli/radar.py`（9 子命令）+ `radar/` 模块 + SQLite 单文件 + Markdown/JSON 报告。
- 边界：不自动安装、不自动导入知识库、不改 Engine；导出只是候选，需人工审核。

## 2. 工作原理

```
topics.json ──► collector.discover ──► repositories + snapshots
                     │（GitHub REST / fixtures）
                     ▼
              growth.compute_growth（24h/7d/30d）
                     ▼
              scoring.evaluate（5 维）
                     ▼
              candidates（review_status）
                     ▼
        reports（7 文件） + export（Research Intake JSON）
```

## 3. 目录结构

```
github-project-radar/
├── cli/radar.py               ← CLI 入口
├── radar/
│   ├── collector.py           ← 发现/采集/重试/事务
│   ├── growth.py              ← 增长计算
│   ├── scoring.py             ← 5 维评分 + 理由
│   ├── storage.py             ← SQLite schema/读写
│   ├── reports.py             ← 周报 7 文件
│   ├── review.py              ← 候选状态机
│   ├── export.py              ← Research Intake
│   └── sources/rest.py        ← 真实 GitHub REST 客户端
├── config/topics.json         ← 搜索主题
├── config/scoring.json        ← 权重与理由模板
├── tests/test_radar.py        ← 38 个测试
├── reports/                   ← 周报产物（入库）
├── docs/                      ← data-model / engine-interface / operating-guide
└── radar*.db                  ← 本地数据库（gitignored）
```

## 4. 环境依赖

- Windows 10/11
- Python 3（`py -3`）
- 标准库 only（`urllib`、`sqlite3`、`json`）
- 可选：`GITHUB_TOKEN` 环境变量（提高配额）

## 5. GitHub API 配置

- 认证：环境变量 `GITHUB_TOKEN`；缺失则匿名。
- 请求头：`Authorization: Bearer <token>`。
- 匿名节流：`min_interval_seconds = 7.0`。

```powershell
# 当前会话临时设置（不要写进仓库）
$env:GITHUB_TOKEN = "<your-token>"
```

## 6. Token 设置与安全

- 只需要 **public_repo 只读**（或 fine-grained 的 public read）。
- 不要提交 token；不要写进 `config/*.json`。
- 匿名配额：**60 请求/小时**；带 token：**5000 请求/小时**。
- 代码对 403/429 一律抛 `RateLimitError`，然后 `sleep(60)` + 指数退避；**不读 `Retry-After`**。
- **已知缺陷**：搜索路径会丢弃 `X-RateLimit-Remaining`（见 §20），匿名时配额感知不可靠。

## 7. 如何首次运行

```powershell
cd C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\github-project-radar

py -3 cli/radar.py init-db
py -3 cli/radar.py collect --source rest --max-queries 4
py -3 cli/radar.py analyze
py -3 cli/radar.py report --format dir
```

默认数据库：仓库根 `radar.db`。建议显式指定，避免覆盖历史：

```powershell
py -3 cli/radar.py --db radar-2026-11-23.db init-db
py -3 cli/radar.py --db radar-2026-11-23.db collect --source rest --max-queries 4
```

## 8. 如何发现项目

```powershell
py -3 cli/radar.py collect --source rest --max-queries 4
```

- `--source fixture`（默认）：离线样例，5 个仓库，不发网络请求。
- `--source rest`：真实 GitHub 搜索。
- 搜索词来自 `config/topics.json`（多关键词 `in:name,description,readme` + Skills/MCP 定向）。
- `--max-queries` 控制搜索次数；4 次 × 50 条 ≈ 200 行快照。

## 9. 如何追踪仓库

当前**没有**「加入追踪列表」的 CLI。真实库的日常快照能力未闭环：

- `snapshot` 子命令固定用 fixture 客户端，不能给真实库追加快照。
- `collector.refresh_tracked` 有实现，但**未暴露 CLI**。

**当前可行做法**：每次用新的 `--db` 跑一次 `collect --source rest`，把多次运行的结果当历史；或直接调用库函数（需改代码，不推荐）。

## 10. 如何保存快照

```powershell
py -3 cli/radar.py snapshot
```

- 只对 fixtures 有效。
- 表：`snapshots(repository_id, captured_at, stars, forks, ...)`，`UNIQUE(repository_id, captured_at)` + `INSERT OR IGNORE`。
- 同一仓库在不同搜索批次、不同秒各存一行。

## 11. 如何分析趋势

```powershell
py -3 cli/radar.py analyze
```

- 增长：`latest - nearest_before(anchor - N days)`，窗口 1/7/30 天。
- 历史不足 → `insufficient_history=true`，不外推。
- `anchor` 默认取最后一个快照时间（不是当前时间）。
- **不会校正采样间隔**：若最近快照是 25 天前，7d 增量实际是 25 天差值。
- **警告**：`analyze` 会重写候选的 `review_status` 与 `human_selected_for_research`（见 §20 D1）。

## 12. 如何筛选候选项目

```powershell
py -3 cli/radar.py candidates
py -3 cli/radar.py candidates --status Research
```

- 评分 5 维：创新 25 / 相关性 25 / 工程成熟度 15 / 可复用性 15 / 增长势能 20（`config/scoring.json`）。
- 每维输出 `score / reason / basis`；总分按权重归一化。
- 跨 topic 组不做排名（`compare_group` 拒绝跨组比较）。
- 增长缺失时记 0 分并写明原因，不编造。

## 13. 如何管理候选状态

```powershell
py -3 cli/radar.py review <candidate_id> `
  --current Discovered --target Research `
  --reviewer "你的名字" --decision "值得研究" `
  --objective "看它的 agent 编排"
```

状态：`Discovered → Triaged → Watch → Research → Adopt / Ignore`（转换表在 `radar/review.py:18-25`）。
每次转换写 `review_log`（reviewer/at/from/to/decision）。

## 14. 如何生成日报和周报

```powershell
py -3 cli/radar.py report --format dir            # 7 文件（默认）
py -3 cli/radar.py report --format summary        # 单文件 Markdown
py -3 cli/radar.py report --format json           # 机器可读
py -3 cli/radar.py report --week 2026-W47 --format dir
```

7 文件：`weekly-report.md`、`rising-projects.md`、`new-skills.md`、`mcp-and-tools.md`、`engineering-practices.md`、`star-growth.json`、`research-candidates.json`。

**注意**：`rising-projects` 按 `growth_momentum.score` 排序；当增长全为 0 时，它等于按插入顺序取前 15，**不代表真的在崛起**（§20 D6）。

## 15. 如何导出 Research Intake

```powershell
py -3 cli/radar.py export --output reports/research-intake.json --status Research
```

导出字段（15 项）：
`candidate_id, repository, url, topic, discovery_reason, star_metrics, evaluation, review_status, research_objective, created_at, human_selected_for_research, source_url, observed_at, retrieved_at, data_quality`

**重要**：`--approved` 只把 `review_status` 改成 `approved_for_research`，**不会**把 `human_selected_for_research` 置 true。按仓库自己的 `docs/engine-interface.md`，只有该字段为 true 才能导入。当前样本该字段为 `false`（§20 D3）。

## 16. 如何定时运行

**仓库内没有 scheduler**（无 `.github/workflows`、无 `.ps1/.xml`）。

手工方案（Windows 任务计划）：

1. 任务计划程序 → 创建基本任务
2. 触发器：每天 09:00
3. 操作：启动程序 `py`
4. 参数：`-3 cli/radar.py --db radar-daily.db collect --source rest --max-queries 4`
5. 起始于：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\github-project-radar`

> 由于「真实快照」未闭环，定时任务目前只能做「发现」，不能做「跟踪同一批仓库的变化」。

## 17. Rate Limit 处理

- 匿名 60/h；token 5000/h。
- 403/429 → `RateLimitError` → `sleep(60)` → 指数退避（`max_retries=2, base=2.0`）。
- 不读 `Retry-After`；不读搜索响应的剩余量。
- 建议：真实采集时设 `GITHUB_TOKEN`，并把 `--max-queries` 控制在 10 以内。

## 18. 数据备份和恢复

数据库是单文件（`radar*.db`），**被 gitignore**：

```powershell
Copy-Item radar-2026-11-23.db "D:\backup\radar-2026-11-23.db"
```

恢复：把备份复制回仓库根，用 `--db` 指向它。

**没有**断点续采/HTTP 缓存；失败后重跑会重新请求。

## 19. 常见错误

| 现象 | 原因 | 处理 |
|---|---|---|
| `403 rate limit` | 匿名配额耗尽 | 设 `GITHUB_TOKEN`，等一小时，或减少查询 |
| `no such table` | 没跑 `init-db` | 先 `init-db` |
| 增长全是 `insufficient_history` | 快照时间跨度太短 | 需要多天快照；当前没有日常快照 CLI |
| `research` 命令不存在 | 文档写了但 CLI 未实现 | 用 `review` + `export` |
| 导出 `human_selected_for_research=false` | `--approved` 不置该字段 | 见 §20 D3；修代码前只能人工改 JSON |
| 周报「崛起」不像崛起 | 增长全 0，按插入顺序 | 忽略该板块，或先积累历史 |
| 重跑 `analyze` 后人工状态没了 | D1 覆盖 | 先备份 DB；修代码前不要重跑 |
| `candidates` 为空 | 没 `analyze` 或库不对 | 检查 `--db` 路径 |

## 20. 当前功能限制（审计实测）

1. **D1 人工状态被覆盖**：`analyze` 的 upsert 会重置 `review_status` / `human_selected_for_research`。
2. **D2 配额感知失效**：`search_repositories` 丢弃 `_rate_limit_remaining`。
3. **D3 人工门可绕过**：`--approved` 不置 `human_selected_for_research`；导出样本为 false。
4. **D4 审计不全**：`collection_runs.query_params` 只记 `query_count`，不记查询语句与错误清单。
5. **D5 溯源全空**：`source_url/observed_at/retrieved_at/data_quality` 200/200 NULL，无法区分 live/demo。
6. **D6 周报语义失真**：增长全 0 时「崛起项目」仍排名。
7. **无真实日常快照**：`snapshot` 仅 fixture；`refresh_tracked` 无 CLI。
8. **无 HTTP 缓存/断点续采**；无多 token 轮换。
9. **无调度**：`collection_runs=1`，只跑过一次。
10. **文档漂移**：README/AGENTS 仍写「离线、不发起网络请求」；`operating-guide.md` 的 `research` 子命令不存在；三维评分未接入 `analyze`。
11. **数据现实**：121 仓 / 200 快照，但时间跨度只有 20 秒（4 个时间点），增长 121/121 为空。
12. **误报**：关键词主题归并会把 `bootstrap`、`tensorflow`、`react-native`、`tauri` 归到 `ai-agent` 类。

**可用性结论**：适合「一次性发现 + 打分 + 人工挑候选」；**不适合**「持续趋势追踪」或「自动供 Engine」。修完 D1/D2/D3 后再评估日常化。

---

**最后验证**：2026-11-23，Radar `b7442da`；`38 tests OK`；真实库 121 仓/200 快照/1 次采集。
**最近更新**：2026-11-23。