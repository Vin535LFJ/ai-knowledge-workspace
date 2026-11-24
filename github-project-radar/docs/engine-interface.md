---
doc_id: "engine-interface"
type: "interface"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# 与知识到学习引擎（Render_Notes）的交接接口

> 名称映射：新架构文档建议名 `github-radar` ≡ 本地目录 `github-project-radar`，按用户裁决不改名。

## 原则

本系统只**输出**研究任务 JSON，供 Render_Notes 的「AI 知识到学习引擎」按需摄取。
导出模块（`radar/export.py`）**只有导出能力，没有任何写入 Render_Notes 或 Render_Notes 项目目录的代码**。
是否导入、如何导入完全由外部引擎决定。

**人工门槛（强约束）**：只有候选记录 `human_selected_for_research=true`（人工明确选择深入调研）时，
该任务才属于「可导入 Engine source inbox 的研究任务」。导入后由 **Research Agent 重新核验**事实，
**Radar 的初筛分数（包括旧综合分与三个独立分数）一律不得当作知识证据**——它们只是启发式信号，
不是已证实结论。

## 导出命令

```bash
py -3 cli/radar.py export --output research-tasks.json --status Research --approved
```

`--approved` 会把每条任务的 `review_status` 设为 `approved_for_research`，表示已经人工批准进入研究。
是否「可导入 Engine」以导出 JSON 中的 `human_selected_for_research` 为准：**只有该字段为 true 的任务才是可导入的研究任务**；引擎必须据此过滤，不得仅凭 `review_status` 导入。

## 研究任务 JSON 结构

顶层：

```json
{
  "schema_version": 1,
  "exported_at": "ISO-8601",
  "task_count": 2,
  "tasks": [ /* 下列字段 */ ]
}
```

每条 `task` **严格包含**以下字段：

| 字段 | 说明 |
|---|---|
| candidate_id | 候选记录 id |
| repository | 仓库全名 `owner/name` |
| url | `https://github.com/{repository}` |
| topic | 主题组 id |
| discovery_reason | 发现依据（JSON 对象） |
| star_metrics | 星标/ Fork / 增长指标（含 `insufficient_history`） |
| evaluation | 完整评分（各维度 score/reason/basis + total） |
| review_status | 复核状态，如 `approved_for_research` |
| research_objective | 研究目标（人工填写） |
| created_at | 候选创建时间 |
| human_selected_for_research | 人工选择标志（bool）。仅 true 才允许导入 Engine source inbox |
| source_url | 溯源：记录来源 URL（缺失为 null） |
| observed_at | 溯源：观测时间（缺失为 null） |
| retrieved_at | 溯源：数据取得时间（缺失为 null） |
| data_quality | 溯源：数据质量标记（缺失为 null） |

导出前由 `validate_task` 自检字段完整性，缺失即报错。

## 数据真实性约定

- `star_metrics` 中的增长数字来自系统自有快照；历史不足时 `insufficient_history=true` 且增长字段为 `null`，引擎应据此避免做增长论断。
- `evaluation` 中的旧综合分各维度理由为启发式判断（非事实陈述）；新增的 `three_scores`（如同时写入）为发现信号 / 工程质量 / 相关性的独立初筛分数，字段缺失标 `unknown`。**所有 Radar 初筛分数都不得当作知识证据**，导入后必须由 Research Agent 重新核验。
- 深度研究模板中的 `[未验证]` 标记表示待查证内容，引擎/研究者须查证后再使用。
- 溯源字段 `source_url` / `observed_at` / `retrieved_at` / `data_quality` 缺失时为 `null`，引擎不得据此推断数据可信度。
- 本模块只有导出能力，**没有任何写入 Render_Notes 的代码**；导入完全由外部引擎负责。
