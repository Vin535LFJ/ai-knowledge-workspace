---
doc_id: "agents-md"
type: "adapter"
status: "active"
owner: "qwenwork"
created: "2026-11-19"
updated: "2026-11-26"
---

# AGENTS.md（适配器入口）

本模块是 AI Knowledge-to-Learning Engine 的**内部 Research Discovery 模块**（D22 并入 `integrations/github-radar/`），不是独立产品。本文件是给 AI 编码助手 / 智能体的指针式入口；权威口径见 `INTEGRATION.md`。

## 必读

- `INTEGRATION.md`：模块定位、从 Engine 根的运行命令、真实数据限制、人工批准边界（权威）。
- `README.md`：技术参考（命令、评分、生命周期、数据源）。
- `docs/data-model.md`：表结构与字段含义。
- `docs/operating-guide.md`：运行流程。
- `docs/engine-interface.md`：与 Engine 的导出交接契约（15 字段，仅 human_selected_for_research=true 可导入）。

## 关键约束

- 仅使用 Python 标准库；无第三方依赖。
- 默认离线（`fixtures/` 注入客户端）；**只有显式 `collect --source rest` 才发起真实 GitHub REST 请求**（匿名或 `GITHUB_TOKEN`）。`trending`/`ossinsight` 仍为离线 stub。
- 不执行任何 git 操作。
- 令牌仅通过环境变量提供；源码/配置/日志中不得出现令牌。
- 增长数据不足时必须标记 `insufficient_history`，不得编造 7d/30d 数字。
- 导出模块为纯输出，**禁止**自动写入 Engine 知识库或任何外部项目；导入由 Engine 人工决定。
- 复核状态转换只记录状态与审计信息，**禁止**自动安装/导入/修改任何项目。
- 不开发调度平台/自动采集平台。
- 所有文档使用简体中文，Markdown 文档带 YAML frontmatter。
