---
doc_id: "operating-guide"
type: "guide"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# 操作指南

> 名称映射：新架构文档建议名 `github-radar` ≡ 本地目录 `github-project-radar`，按用户裁决不改名。

## 日常节奏（建议）

- **每天**：运行一次 `snapshot` 记录当日快照；必要时 `collect` 发现新仓库。
- **每周**：运行 `analyze` 更新评分，`report` 生成周报，人工复核候选并导出研究任务。

> 第一版无实时、无 Dashboard：所有节奏由命令行 / 定时任务外部驱动，系统本身不驻留后台。

## 完整流程

1. `init-db`：首次建库。
2. `collect`：通过注入的客户端（当前为 `fixtures/` 离线客户端）发现仓库并写入首条快照；采集运行参数入库以便审计。失败整体回滚，不破坏既有历史。
3. `snapshot`：为已跟踪仓库追加快照。即使某仓库掉出搜索结果，也会通过 `get_repository` 继续跟踪。
4. `analyze`：对每个仓库计算增长与评分，写入候选池。增长历史不足时增长势能记为中性。
5. `candidates` / `report`：查看候选与周报。周报默认在 `reports/YYYY-Www/` 下生成 7 个文件（A–G 板块）；`--format summary` 生成单文件 `reports/YYYY-Www.md`，`--format json` 生成机器可读 `reports/YYYY-Www.json`。
6. `review`：人工做状态转换。canonical 生命周期 `discovered → triaged → watchlist → deep_dive → adopted / rejected / archived`；旧状态 `Watch/Research/Adopt/Ignore` 为别名。状态变更记录时间/操作人/理由，不触发任何自动副作用。
7. `export`：导出研究任务 JSON（纯输出）。只有 `human_selected_for_research=true` 的任务才可导入 Engine source inbox，导入后由 Research Agent 重新核验，Radar 初筛分数不得当知识证据。
8. `research`：对高价值项目渲染深度研究模板，默认输出 `research/owner__repo.md`（可用 `--output` 覆盖）；所有未验证事实保留 `[未验证]` 标记，查证后移除。

## 数据与配置约定

- 主题扩展：编辑 `config/topics.json` 追加条目即可；发现、相关性评分、分组比较自动生效。
- 权重调整：编辑 `config/scoring.json`。
- 令牌：真实采集器的令牌只能通过环境变量提供；本仓库不含任何令牌。
- 测试使用 `tempfile.TemporaryDirectory` 隔离数据库，不污染生产数据。

## 安全边界

- 不执行 git 操作；不发起网络请求（本轮）。
- 复核状态机**不触发**任何安装、导入或修改其他项目的动作；`Adopt` 仅表示人工采纳决定。
- 导出模块只写指定输出文件，绝不写入 Render_Notes。


## 真实采集入口（2026-11-21 阶段 4 解冻后新增）

```bash
# 匿名发现（GITHUB_TOKEN 可选，未设则走 60 req/h 匿名限额；内部节流 7 秒/请求）
py -3 cli/radar.py --db radar-real.db collect --source rest --max-queries 4
py -3 cli/radar.py --db radar-real.db analyze
py -3 cli/radar.py --db radar-real.db candidates
py -3 cli/radar.py --db radar-real.db review <id> --current Discovered --target Triaged --reviewer <人工> --decision <说明>
py -3 cli/radar.py --db radar-real.db review <id> --current Triaged --target Research --reviewer <人工> --decision <说明>
py -3 cli/radar.py --db radar-real.db report --reports-root reports
py -3 cli/radar.py --db radar-real.db export --output reports/research-intake.json --status Research
```

- 数据源实现：`radar/sources/rest.py`（GitHubRestClient，stdlib urllib；GITHUB_TOKEN 环境变量可选）。
- 限额口径：匿名核心 60 req/h、搜索 ~10 req/min——一轮最小发现（4 查询 + ~121 仓库快照）已在匿名额度内实测通过（2026-11-21，121 仓库/200 快照/0 错误）。
- 定时执行（Windows）：任务计划程序 → 基本任务 → 每日 09:00 → 操作：`py -3 <repo>\cliadar.py --db <repo>adar-real.db collect --source rest --max-queries 8`（"起始于"填仓库根）。
- 安全边界不变：导出纯输出、复核状态机无自动副作用、令牌只走环境变量。
