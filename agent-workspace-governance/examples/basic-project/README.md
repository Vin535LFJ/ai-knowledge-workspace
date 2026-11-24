---
doc_id: basic-project-readme
type: project-readme
status: active
owner: human
created: 2026-11-19
updated: 2026-11-19
---

# Basic Project（最小普通软件项目示例）

这是一个**普通软件项目**，用来证明本治理工具包**不依赖任何 Render_Notes 知识结构**。

## 项目内容

一个极简的「待办清单」命令行小工具，仅用于演示。

- `README.md` —— 本文件
- `docs/design.md` —— 一份普通设计文档
- `.governance/config.json` —— 已初始化的治理配置

## 治理接入

本项目已经通过 `governance.py init` 初始化：

```bash
py -3 <kit>/cli/governance.py inventory --project .
py -3 <kit>/cli/governance.py validate --project .
py -3 <kit>/cli/governance.py status   --project .
```

注意：这里没有任何「源材料 → 主张 → 概念 → 课程」的知识结构，也没有 `WORKFLOW_STATE.md`。治理工具包把它们当作普通文档处理即可。
