---
doc_id: CONSOL-ACCEPTANCE
type: audit
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# FINAL-ACCEPTANCE-REPORT · D22 统一收敛端到端验收（2026-11-26）

> 口径：**已实现并验证 / 已实现部分验证 / 已设计未实现 / 有意不做 / 等待人工 / 技术债**。
> 所有命令当日实跑；退出码与产物路径如实记录。本地浏览器测试通过 ≠ 公网部署成功（在线发布 D02 未授权）。

## 1. 资产保护（Phase 2 前置）

| 项 | 命令/方式 | 结果 |
|---|---|---|
| 六仓 bundle + ignored 数据 + SHA256 清单 | `consolidation_backup.py`（git bundle --all / verify / clone 恢复比对） | **6/6 PASS**：HEAD 一致、tree 一致、归一化 blob 哈希 0 差异 |
| 恢复验证口径 | clone `-c core.autocrlf=false` + `git hash-object` 比对 | 工作树 CRLF 差异属预期（全局 autocrlf=true），tree/blob 级一致为保真判据 |
| 原目录处置 | Move-Item → `AI-Knowledge-backups/2026-11-26-consolidation/retired/` | HEAD 实测 ba35e4a / 7d9a187 / e2815d9 完好，**未删除** |
| 并入副本保真 | `verify_copies.py`（git hash-object 逐文件） | Program 31/31、Governance 40/40 一致；Radar 39 中 2 处为有意修改（research.py + tests） |

## 2. 整合与结构（Phase 2）

- 五项目 → 两仓（核心仓 + Skills 库）；program/ 31 文件、legacy/ 40+5 文件、integrations/github-radar/ 43 文件并入。
- 双轨治理清除：`.governance/` git mv → legacy/；文档注册表唯一（291 条）、运行状态唯一（run_state）。
- .gitignore 补 radar db/research 规则；`git check-ignore` 实测两个 .db 被忽略。
- **状态：已实现并验证。**

## 3. 核心产品质量（Phase 3）

| 检查 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 构建 | `py -3 tools/build_site.py` | 0 | 91 docs / 25 lessons / 7 labs / 673 term cards / 3152 KB |
| 结构门禁 | `py -3 tools/validate_site.py` | 0 | **20 checks / 0 FAIL / 0 WARN**（含 quizzes payload e1b 新检查） |
| 发布边界回归 | `py -3 tools/test_publish_boundary.py` | 0 | **Ran 33 / OK (skipped=1)**（skip=符号链接权限环境限制；junction 逃逸演练此前已单独验证） |
| 断言状态 | `py -3 tools/review_gate.py` | 0 | **105 claims（24v/74o/7c）误标 0** |
| 章节弧（主课程） | `check_chapter_arc.py`（19 份展开） | 0 | 0 FAIL |
| LXD Floor（具身 6 课） | `check_visual_floor.py` | 0 | OK |
| KCR 影响分析自测 | `py -3 tools/kcr/selftest_impact.py` | 0 | Ran 16 / OK |
| 状态机自测（含新依赖检查） | `py -3 tools/kcr/selftest_runstate.py` | 0 | **Ran 28 / OK**（25+3 新增：环检测/前沿阻塞/篡改态拒绝） |
| 审批链自测 | `py -3 tools/kcr/selftest_approval.py` | 0 | Ran 15 / OK |
| Radar 模块测试 | `py -3 -m unittest discover -s integrations/github-radar/tests` | 0 | **Ran 58 / OK** |
| Governance 归档测试（一次性留档） | `py -3 -m unittest discover -s legacy/agent-workspace-governance/tests` | 0 | Ran 41 / OK |
| Skills 校验 | `node scripts/check-translation.mjs` / `audit-english.mjs` | 0 / 0 | 通过 |
| 链接检查 | `check_links_d22.py`（45 份活跃文档） | 0 | **135 条相对链接 0 broken** |

### 浏览器实测（headless Edge，http://127.0.0.1:8796，临时副本不碰仓库）

证据：`reviews/consolidation-qa-course-switch-20261126.json`（8 个场景原始输出）。

| 场景 | 结果 |
|---|---|
| 主课程地图 `#/course` | 3 个课程切换 chip（active 正确）、20 课卡片 |
| 具身地图 `#/course?c=embodied-loop-journey` | 6 课 E01–E06，标题/进度正确 |
| pilot 地图 `#/course?c=video-rendering-journey` | 5 课 L01/L02/L06/L11/L13 |
| E02 课时页 | quiz 4 题；选择题点击→判分反馈「正确答案是 B」+正确项标记+选项禁用；简答展开 62 字参考答案；返回链→具身地图；下一课→E03 |
| L01 课时页 | quiz 3 题，交互同上；返回链→主地图 |
| E06 课时页 | quiz 3 题（简答），末课返回课程地图 |
| 移动端 360px（E02 / 具身地图） | scrollWidth 345 ≤ 360，**无横向溢出** |
| 全部场景 | console errors=[]，无原始 Markdown 泄漏 |

- **状态：已实现并验证**（课程切换 + 检查点可达，P0-6 闭合）。

## 4. 端到端工作链（Phase 5 口径）

| 环节 | 证据 | 状态 |
|---|---|---|
| 原始资料→研究→证据→知识→课程→教材→网站→审核 | HDR 批真实 run `RUN-2026-11-20-p10-hdr` INTAKE→FEEDBACK **done**（18 artifacts，四人工门全过，2026-11-21） | 已实现并验证（历史一次完整闭环） |
| 具身批 | `RUN-2026-11-23-embodied-batch1` REVIEW/paused，24 artifacts 哈希全有效 | **等待人工**（G1/G2/G3/KCR，设计行为） |
| 人工审批+Hash 证据链 | approval_chain selftest 15/15；发布前重算比对；历史批准如实标 legacy | 已实现并验证（审批人身份验证除外，见技术债） |
| KCR/Feedback | kcr selftest 16/16；feedback.json entries=0 | 已实现部分验证（反馈闭环空） |
| Radar→Engine 摄取 | 契约就绪，摄取端无代码，human_selected=0 | **有意不实现**（接通需人工批准后立项） |

## 5. 文档治理（Phase 4）

- 10 份必备文档齐备：总 README（工作区+核心仓）/ 架构（TARGET-ARCHITECTURE）/ 当前状态（program/NOW）/ 路线图（ROADMAP）/ 文档导航（PROJECT-DOCUMENTATION-INDEX，路径已按新结构更新并 0 broken）/ 决策入口（DECISIONS D22 + CONSOLIDATION-DECISIONS）/ Agent 入口（AGENTS.md 新指针）/ Skills 入口（Skills 仓 USER-GUIDE + 核心仓 .agent/skills）/ 构建测试指南（docs/USER-GUIDE §8 已更新）/ 历史归档说明（legacy/README + archive/process-history）。
- 状态职责去重：NOW=项目级七字段快照；WORKFLOW_STATE=执行续跑点；CHANGELOG=只追加历史；README=产品入口（数字当日实测）。
- 11-24 审计档案补做（program/audits/，原报告原文 + 核实 + 处置），ROADMAP 悬空指针消除。
- Skills 过时文档修复（AGENT-COMPATIBILITY 更正注记 / in-progress 安装命令改本仓 slug / USER-GUIDE 锚点注记 / 本地记忆更正注记）；两校验脚本 exit 0。
- **状态：已实现并验证。**

## 6. Git 与发布收口（Phase 6）

见 CHANGELOG 当日条目与提交记录（分组提交 + 普通推送 + ls-remote 核实）。快照仓更新为最终结构。
远端归档/删除/可见性变更：**等待人工**（无 gh/API 凭据；条件清单见 TARGET-ARCHITECTURE §8）。

## 7. 如实清单

**等待人工**：embodied G1（V68–V88）/G2/G3/KCR；PD-Q9~Q16（含公开边界 PD-Q16、Radar 真实库升级 PD-Q15）；Skills 全新会话验证；远端归档/可见性操作。
**有意不做**：摄取端自动化、中央注册平台、Orchestrator、Dashboard、调度平台、在线自动发布、自动审批、全面重写旧教材/重设计实验。
**技术债**：审批人字符串（无签名）；HDR 历史 run 6 哈希过期（如实标注）；Radar 真实库旧 schema；Skills 35 技能运行时未验证、tag 指向孤儿历史（不再重写）；`query` 子命令只读靠自律。
**未验证项**：公网部署（未授权）；全新会话 Skills 调用；其余宿主运行时。