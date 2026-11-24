---
doc_id: "data-model"
type: "design"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# 数据模型

> 名称映射：新架构文档建议名 `github-radar` ≡ 本地目录 `github-project-radar`，按用户裁决不改名。

## repositories（仓库身份元数据）

| 字段 | 类型 | 说明 |
|---|---|---|
| repository_id (PK) | INTEGER | GitHub 仓库 ID |
| full_name | TEXT | `owner/name` |
| description | TEXT | 描述 |
| language | TEXT | 主语言 |
| topics | TEXT | JSON 数组 |
| license | TEXT | SPDX 标识 |
| created_at | TEXT | 仓库创建时间 |
| homepage | TEXT | 主页 |
| default_branch | TEXT | 默认分支 |
| archived | INTEGER | 是否归档 |
| first_seen_at | TEXT | 系统首次发现时间（确定后不变） |
| source_url | TEXT | 溯源：记录来源 URL（可选） |
| observed_at | TEXT | 溯源：观测时间（可选） |
| retrieved_at | TEXT | 溯源：数据取得时间（可选） |
| data_quality | TEXT | 溯源：数据质量标记（可选） |

去重口径：按 `repository_id` 去重；仓库 rename/transfer 时保留 `repository_id` 与历史名称映射，不另起新记录。

## snapshots（每日指标快照，只增不改）

| 字段 | 类型 | 说明 |
|---|---|---|
| id (PK) | INTEGER | 自增 |
| repository_id | INTEGER | 关联仓库 |
| captured_at | TEXT | 采集时间 |
| stargazers_count | INTEGER | 星标数 |
| forks_count | INTEGER | Fork 数 |
| watchers_count | INTEGER | 关注数 |
| open_issues_count | INTEGER | 未关闭 Issue 数 |
| pushed_at | TEXT | 最近推送时间 |
| updated_at | TEXT | 仓库更新时间 |
| release_info | TEXT | JSON（release 信息） |
| source_url | TEXT | 溯源：记录来源 URL（可选） |
| observed_at | TEXT | 溯源：观测时间（可选） |
| retrieved_at | TEXT | 溯源：数据取得时间（可选） |
| data_quality | TEXT | 溯源：数据质量标记（可选） |

**唯一约束**：`(repository_id, captured_at)`。重复写入被幂等忽略，历史永不覆盖。

## collection_runs（采集审计）

记录 `started_at`、`query_params`（JSON）、`source`、`status`（running/success/failed/partial），满足可审计性。

## candidates（候选与复核）

| 字段 | 类型 | 说明 |
|---|---|---|
| id (PK) | INTEGER | 自增 |
| repository_id | INTEGER | 关联仓库 |
| topic | TEXT | 主题组（与 topics.json 的 id 对应） |
| discovery_reason | TEXT | JSON，发现依据 |
| evaluation | TEXT | JSON，评分与复核日志 |
| review_status | TEXT | canonical: discovered/triaged/watchlist/deep_dive/adopted/rejected/archived；旧别名 Watch/Research/Adopt/Ignore 仍可读 |
| research_objective | TEXT | 研究目标 |
| created_at | TEXT | 创建时间 |
| human_selected_for_research | INTEGER | 人工选择标志（默认 0/False）；仅 true 才允许导入 Engine source inbox |
| source_url | TEXT | 溯源：记录来源 URL（可选） |
| observed_at | TEXT | 溯源：观测时间（可选） |
| retrieved_at | TEXT | 溯源：数据取得时间（可选） |
| data_quality | TEXT | 溯源：数据质量标记（可选） |

**唯一约束**：`(repository_id, topic)`。
**生命周期**：canonical 状态为 `discovered → triaged → watchlist → deep_dive → adopted / rejected / archived`；旧状态 `Watch≡watchlist`、`Research≡deep_dive`、`Adopt≡adopted`、`Ignore≡rejected`。`radar.review.normalize_status()` 双向兼容；`record_transition()` 生成含时间/操作人/理由的变更记录，追加到 `evaluation.review_log`。状态变更只记录审计，不触发任何自动副作用。

## 增长与评分口径

- 增长：`growth.compute_growth` 基于快照时间窗口计算 24h/7d/30d 星标增长、Fork 增长、活跃度（pushed_at 距今）、加速度（近 7d vs 前 7d）。
- **快照不足（<2 或缺少窗口历史）时返回 `insufficient_history=true`，窗口指标为 `None`，绝不编造。**
- 评分：`scoring.evaluate` 按可配置权重对五个维度打分；增长势能直接消费增长输出，历史不足时为 0（中性）并给出原因；每个维度含 `score`/`reason`/`basis`。
- 分组比较：`scoring.compare_group` 拒绝跨主题组直接排名。
- **三维独立评分**：`scoring.evaluate_three_scores` 输出 `discovery_signal` / `engineering_quality` / `relevance` 三个独立分数，每个含 `score`（数字或 `unknown`）、`explanation`、`basis`。字段缺失的子信号标 `unknown`，不默认满分/零分；规则与阈值见 `config/scoring.json` 的 `three_scores`。旧的 `evaluate()` 综合分与 total 权重完全不变。

## 报告格式

- 目录格式（原样保留）：`reports/YYYY-Www/` 下 7 个文件（weekly-report.md 等）。
- 单文件摘要：`reports/YYYY-Www.md`，含 A–G 七个板块精简摘要（YAML frontmatter）。
- 机器可读：`reports/YYYY-Www.json`，含 A–G 七个板块载荷。
- 周编号用 `datetime.isocalendar()`，格式 `YYYY-Www` 零填充（如 2026-W47）。
