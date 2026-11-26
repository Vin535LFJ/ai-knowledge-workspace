---
doc_id: "agents-md"
type: "adapter"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# AGENTS.md（适配器入口）

本文件是给 AI 编码助手 / 智能体的指针式入口。请按需查阅以下文档，**不要**在本仓库之外做任何写操作。

## 必读

- `README.md`：定位、默认约定、命令、快速开始。
- `docs/data-model.md`：表结构与字段含义。
- `docs/operating-guide.md`：日常运行流程。
- `docs/engine-interface.md`：与 Render_Notes 知识到学习引擎的交接契约。

## 关键约束

- 仅使用 Python 标准库；无第三方依赖。
- 不发起网络请求（`fixtures/` 为离线数据；采集通过注入客户端）。
- 不执行任何 git 操作。
- 令牌仅通过环境变量提供；源码/配置/日志中不得出现令牌。
- 增长数据不足时必须标记 `insufficient_history`，不得编造 7d/30d 数字。
- 导出模块为纯输出，**禁止**写入 Render_Notes 或任何外部项目。
- 复核状态转换只记录状态与审计信息，**禁止**自动安装/导入/修改任何项目。
- 所有文档使用简体中文，Markdown 文档带 YAML frontmatter。
