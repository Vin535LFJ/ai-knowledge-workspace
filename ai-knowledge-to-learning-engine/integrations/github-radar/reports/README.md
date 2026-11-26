---
doc_id: "reports-readme"
type: "readme"
status: "active"
owner: "github-project-radar"
created: "2026-11-19"
updated: "2026-11-19"
---

# reports/ 周报目录

> 名称映射：新架构文档建议名 `github-radar` ≡ 本地目录 `github-project-radar`，按用户裁决不改名。

本目录存放系统生成的周报。周编号用 ISO year-week（`datetime.isocalendar()`），格式 `YYYY-Www` 零填充（如 2026-W47）。

## 目录格式（原样保留）

每个周目录包含 7 个文件：

- `weekly-report.md` —— 主报告，含 A–G 七个板块（A 崛起、B 遗珠、C AI Agent、D Skills、E MCP、F 工程、G 图形与渲染）。
- `star-growth.json` —— 星标与增长数据。
- `rising-projects.md` —— A 板块明细。
- `new-skills.md` —— D 板块明细。
- `mcp-and-tools.md` —— E 板块明细。
- `engineering-practices.md` —— F 板块明细。
- `research-candidates.json` —— 进入研究/观察/采纳状态的候选清单。

生成命令（默认目录格式，行为不变）：

```bash
py -3 cli/radar.py report [--week YYYY-Www] [--reports-root DIR]
```

## 单文件 / JSON 格式（新增）

```bash
py -3 cli/radar.py report --format summary   # reports/YYYY-Www.md，含 A–G 七个板块精简摘要
py -3 cli/radar.py report --format json      # reports/YYYY-Www.json，机器可读
```

内容基于库内快照与评分自动生成；数据不足处明确标注，不编造事实。
