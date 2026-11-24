---
doc_id: PROG-REVIEW-20261120
type: review-report
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# 前一窗口进度独立复核（2026-11-20）

> 复核对象：另一 AI 窗口报告的 T1 命名迁移收尾 + P7.2 十篇 + P8 启动（其 08:37 快照）。
> 方法：只读核验（git 实测 + 门禁复跑 + 逐篇行数/断言状态/材料清点）+ content.js JSON 级对比。复核窗口随后执行了 P8 片一（见 §4）。
> 总结论：**实质工作全部属实，纪律基本合规；发现 4 处记录笔误/ hygiene 问题（已更正），1 个既有工具 bug（已修），无数据损坏、无越权升级、无未授权 push。**

## 1. 符合既有决策（核验通过项）

| 声明 | 核验结果 | 证据 |
|---|---|---|
| T1 四笔提交、未 push | ✅ Engine 本地 HEAD=`ac81548`（父 `cf91738`，祖父 `e848d28`=远端）；Skills HEAD=`7326522`（远端 `e1936f2`）；Program HEAD=`2de2fe0`；ls-remote 两仓远端 HEAD 未变 | git log/ls-remote 实测 |
| remote 已切新 URL | ✅ 两仓 origin 均为新名；Skills upstream-en/zh 未动 | git remote -v |
| P7.2 十篇行数 | ✅ 逐篇实测完全一致：L02 217 / L06 200 / L11 193 / L13 235 / L03 168 / L04 199 / L05 175 / L07 150 / L08 149 / L09 153；L01 标杆 239 未动 | Get-Content .Count |
| 新断言纪律 | ✅ 55 claims = 18 verified / 30 open / 7 conditional；V21–V38 全部 open/low；V17–V20/P02 未被擅自升级；误标 0 | review_gate 复跑 |
| 十份 G2 材料 | ✅ reviews/G2-{L02,L03,L04,L05,L06,L07,L08,L09,L11,L13}-deepening.md 齐全，评分栏留人工 | git status + 文件清点 |
| publish 断言同步 | ✅ test_publish_boundary.py 69→75，算式注释正确（77+6−8=75）；11/11 OK | git diff + 复跑 |
| stash / 保护路径 | ✅ stash@{0} 原样；archive/memory/vendor 未触碰；index.html 改动在 T1 批准的品牌文案范围内 | git stash list / status / show |
| P8 启动件 | ✅ kickoff + 三 schema 落盘；冒烟漂移**主动如实登记**（不掩盖，符合真实留痕纪律） | 文件读取 |
| 门禁 | ✅ validate 11/0/0 · arc 11/11 · publish 11/11 · review_gate 误标 0（复核复跑） | 本窗口实测 |

## 2. 必修缺口（复核窗口已处理）

| # | 问题 | 性质 | 处理 |
|---|---|---|---|
| 1 | card 数记录 **553 有误，真值 552**（工作区工件与新鲜重建均 552；JSON 级对比仅时间戳+内嵌状态文档快照差异） | 记录笔误 | CHANGELOG/WORKFLOW_STATE 已更正；Program NOW.md 同步 |
| 2 | build 体积记录 2790 KB，真值 **2800 KB** | 记录笔误 | 同上 |
| 3 | content.js 构建于 07:23，其后状态文档更新未入 bundle（内嵌 WORKFLOW_STATE/CHANGELOG 快照过期） | hygiene | 已重建同步（75 docs/552 cards/2800 KB），validate 复跑通过 |
| 4 | 来源摘要"四个新 SRC"不准确：registry 真值 **24 个**，本窗口新增 **5 个**（COLORMGMT/GPU-BASE/GRAPHICS/INTERVIEW-GL/RASDEPTH） | 记录笔误 | CHANGELOG 更正 |
| 5 | Program 办公室报告"0 未提交"，实际 NOW.md 1 个未提交 | 报告小误 | 登记，随 Program 批次提交 |
| 6 | kcr_impact.py `--out` 指向仓库外路径时 relative_to 崩溃（既有 bug，自测暴露） | 工具 bug | 已修（片一内） |

## 3. 需你拍板（不阻塞 P8 片二）

1. **L02 遗留 major（前一窗口已登记，复核确认属实）**：时间轴实验界面有一句静态文案"DTS ≤ PTS 恒成立"，但实验自己的帧模型和课文五帧表都展示了 DTS > PTS 的帧（启动缓冲场景）——学习者做实验任务 3 时必然撞见矛盾。**推荐**：把该句改为与课文一致的表述（如"解码完成时刻先于显示时刻，启动缓冲补偿序位差"）或删除，同步 labs.json 与 app.js 两处 + 浏览器 QA。属事实性错误修正，你点头即可执行。
2. **commit 授权**：Engine 现 **38 个未提交文件**（P7.2 十篇 31 + P8 启动 4 + 复核窗口片一 3：kcr_impact.py/selftest/样本，另有重建 content.js 与状态文档更新）；Program 办公室 NOW.md 等。建议分组：① P7.2 十篇+配套数据；② P8 启动+片一；③ Program 同步。**另请确认**：前一窗口四笔提交（cf91738/ac81548/7326522/2de2fe0）的授权来源——你按文件逐个提交的习惯与该窗口的批量提交不同，若当时已授权则无问题。
3. **push 授权**：Engine 领先远端 2 笔、Skills 领先 1 笔，均未 push（纪律合规），等你授权。
4. **G2 评分**：十篇材料已备齐，AI 不自评。
5. **片三报批预留**：registry 一致性门禁接入 validate 属核心门禁改动，动手前会单独报批（片二不需要）。

## 4. 复核窗口已推进的工作（P8 片一，用户"没问题就继续推进"指令）

- `tools/kcr_impact.py` 输出对齐 impact-report.schema.json：trigger 四模式映射 + new_sources + affected 对象化 + website/integrity_findings 移出契约 + uncovered 字符串数组；修复 --out 外部路径 bug。
- 新增 `tools/kcr/selftest_impact.py`（stdlib-only）：**5/5 OK**，真实回放 COLORMGMT→V21–V24→L03、V14→K-STRIDE/L01/L01#L01-Q2/两层 course、open 断言如实标注、草稿 CLI、未知 seed。
- 三份真实样本按契约重生成（impact-l09-p07 / impact-v14-replay / impact-colormgmt-replay）。
- 门禁末次实测：build 75 docs/552 cards/2800 KB · validate 11/0/0 · arc 11/11 · publish 11/11 · review_gate 55 claims（18v/30o/7c）误标 0 · selftest 5/5。
- 留痕：Engine CHANGELOG/WORKFLOW_STATE/kickoff §3c 已更新。
- **下一步 = P8 片二**：三 schema 的程序化校验器（stdlib-only），接入 kcr_impact 输出与样本回放。

## 5. 证据索引

- git：Engine ac81548/cf91738/e848d28；Skills 7326522/e1936f2；Program 2de2fe0/87f9edf；ls-remote 远端 HEAD e848d2801ec9940e154b9bf40bc26198a5d197ba / e1936f23e6e149c581124cc218e79860c07108ef。
- content.js 对比：备份-重建-恢复法 + JSON 级 diff（仅 generatedAt 与 WORKFLOW_STATE/CHANGELOG 内嵌快照差异）；card 计数脚本实测工作区工件=552。
- 前一窗口报告原文：用户 2026-11-20 会话粘贴（08:37 快照）。