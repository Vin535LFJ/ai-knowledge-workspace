---
doc_id: PROG-POST-AUDIT-2026-11-23
type: audit-summary
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
---

# 审计后收口摘要（POST-AUDIT-SUMMARY）

> 对应审计：`AUDIT-REPORT.md`（2026-11-23）
> 本文回答四件事：审计结论是什么、生成了哪些文档、文档验证到什么程度、还剩什么问题与下一步。

---

## 1. 六阶段审计结论

| 阶段 | 结论 | 一句话 |
|---|---|---|
| 0 Program | PASS WITH LIMITATIONS | 文件与机制可用；PROGRAM/NOW/PENDING 有状态漂移 |
| 1 Engine | PASS WITH LIMITATIONS | 端到端真实跑通；门证据与 artifact 完整性弱；站点未在线发布 |
| 2 LXD | PASS WITH LIMITATIONS | Skill active + L13 一个真实试点；仅单案例 |
| 3 Governance | PARTIAL | CLI + 28 测试可用；9/9 为文档自证；真实注册为空 |
| 4 Radar | PARTIAL | 八功能 + 38 测试 + 121 仓真实数据；趋势/人工门/日常快照未闭环 |
| 5 集成 | PARTIAL | 八项核对存在；第 4 项误判、第 1 项指针失效、第 2 项无实际链接 |

**总判断**：不建议宣布「六阶段全部闭环」。建议表述为 **「六阶段交付完成；Engine 主目标成立；Governance/Radar 为 PARTIAL；Program 需纠偏」**。

## 2. 严重偏差（详见 AUDIT-REPORT §D）

1. Governance「9/9」不成立：`1b4a880` 只改文档；示例项目 `doctor` exit 1；Engine 0 task/0 agent/0 ADR；无治理入口。
2. Radar 有人工状态覆盖（`analyze`）与人工门绕过（`--approved` 不置 `human_selected`）；当前导出物该字段为 `false`。
3. 人工门证据弱：G3 approver 是 AI 写入的字符串；18 条 artifact 中 7 条 hash 与现状不符；run 记录在 gitignored 目录。
4. Program 状态漂移：PROGRAM.md 仍指 `Render_Notes/` 与「冻结」；NOW 同时写「已批/待批」；final-acceptance 第 4 项误判。
5. 学习站混入内部治理/审核文档（`DECISIONS`、`CHANGELOG`、`G2 材料`、`教材质量诊断` 等）。
6. 两套站点生成器并存（`web/` 与 `site-vitepress/`）。
7. Skills 的宿主兼容性无仓库内证据（仅文档叙述）。

## 3. 已生成文档（本次交付）

| # | 文件 | 内容 | 验证基线 |
|---|---|---|---|
| 1 | `ai-knowledge-program/AUDIT-REPORT.md` | 六阶段审计（A–F + 测试记录 + 证据索引 + NOT VERIFIED） | 2026-11-23 实测 |
| 2 | `ai-knowledge-program/POST-AUDIT-SUMMARY.md` | 本文件 | 同上 |
| 3 | `ai-knowledge-program/PROJECT-DOCUMENTATION-INDEX.md` | 全项目文档导航 | 17 文件 / 116 链接检查 |
| 4 | `ai-knowledge-program/USER-GUIDE.md` | Program 使用指南（14 节 + 5 段提示词） | Program `cc098df` |
| 5 | `ai-knowledge-to-learning-engine/docs/USER-GUIDE.md` | Engine 使用指南（理解/快速开始/工作流/产物/审批/排障/提示词/限制） | Engine `79c3fe8` |
| 6 | `matt-pocock-skills-zh-cn/docs/USER-GUIDE.md` | Skills 使用指南（15 节 + 37 技能索引表） | Skills `7326522` |
| 7 | `ai-knowledge-to-learning-engine/.agent/skills/learning-experience-design/USAGE.md` | LXD 操作指南（15 节 + 4 段提示词） | Engine `79c3fe8` |
| 8 | `agent-workspace-governance/docs/USER-GUIDE.md` | Governance 使用指南（16 节 + 迁移/回滚/缺陷） | Governance `1b4a880` |
| 9 | `github-project-radar/docs/USER-GUIDE.md` | Radar 使用指南（20 节 + 已知缺陷） | Radar `b7442da` |

**README 更新**（按任务书 §12 收敛 / 修复过期信息）：

| 仓库 | 改动 |
|---|---|
| Engine | README 从 276 行重写为 ~100 行：准确规模、能力、Quick Start、文档入口、状态、限制；数字与 build 实测一致 |
| Skills | 顶部加文档入口 + 当前 37 技能口径 |
| Governance | 顶部加文档入口 + 真实状态（PARTIAL） |
| Radar | 顶部加文档入口/状态；修正「离线、不发起网络请求」「三个离线 stub」等与 `rest.py` 矛盾的表述 |
| Program | PROGRAM.md 顶部加 USER-GUIDE / 文档导航 / 审计入口 |

## 4. 文档验证结果

### 4.1 链接与路径

- 检查 17 份文档（9 份新文档 + 5 份 README + NOW/ROADMAP/PARKING/PROGRAM-MANAGER）。
- 本地相对链接 **116 条**，修复 1 条错误层级（`../AUDIT-REPORT.md`）后 **0 broken**。
- 所有引用的关键路径（`docs/USER-GUIDE.md`、`.agent/skills/.../USAGE.md`、`reviews/REVIEW_STATUS.md`、各项目 docs）均 `Test-Path` 存在。
- 外部链接未逐一抓取（网络不稳定），保留原 URL，不做真实性承诺。

### 4.2 命令真实性（均在 2026-11-23 实跑）

| 命令 | Exit | 结果 |
|---|---|---|
| `py -3 tools/build_site.py` | 0 | 83 docs / 17 sections / 129 terms / 20 lessons / 7 labs / 624 cards / 3149 KB |
| `py -3 tools/validate_site.py` | 0 | 12 checks, 0 warnings, 0 failures |
| `check_chapter_arc.py L01..L19` | 0 | 19/19 OK |
| `py -3 tools/test_publish_boundary.py` | 0 | 11 tests OK |
| `py -3 tools/review_gate.py` | 0 | 84 claims（24v/53o/7c），误标 0 |
| `py -3 tools/kcr/selftest_impact.py` | 0 | 16 tests OK |
| `py -3 tools/kcr/selftest_runstate.py` | 0 | 25 tests OK |
| `check_visual_floor.py L13 / L19` | 0 / 0 | OK / OK |
| `py -3 -m http.server 8791 --directory web` | — | index/content/app/css 均 200 |
| Edge headless dump-dom | 0 | 渲染出课程/术语/课时标题 |
| `py -3 tests\test_governance.py` | 0 | 28 tests OK |
| `governance.py doctor --project examples\basic-project` | **1** | 2 个 type 非法（已知缺陷，文档如实写） |
| `governance.py doctor --project <ENGINE>` | 1 | 621 项（如实写） |
| `py -3 -m unittest discover -s tests`（Radar） | 0 | 38 tests OK |
| `node scripts/check-translation.mjs`（Skills） | 0 | 通过 |
| `node scripts/audit-english.mjs`（Skills） | 0 | 通过 |

### 4.3 文档与代码一致性

- Engine README 的规模数字改为 build 实测值（83/129/20/7/84/43/3.1MB）。
- Skills 索引表 37 行由 `SKILL.md` frontmatter 脚本生成，非照抄 README。
- Radar 指南的 121/200/1 run/4 时间点/20 秒/provenance NULL 由 SQLite 只读查询复核。
- Governance 指南的 28 tests / doctor exit 1 / 183 docs / 621 项由实跑复核。
- LXD 指南的 L13/L19 Floor 由实跑复核。
- Engine 文档注册表因新增 2 份文档由 **183 → 185**，重建后 `validate` 仍 12/0/0；当前 `web/content.js` 仍是 83 篇（未重新构建，故使用指南暂未进入学习者 bundle）。

### 4.4 已知矛盾（已在文档中标注，未擅自改写历史）

| 矛盾 | 处理 |
|---|---|
| `final-acceptance` 第 4 项 ✅ vs Radar 导出 `false` | 在 final-acceptance 顶部加「历史文档声明」，指向审计更正 |
| `PROGRAM.md` 仍写 `Render_Notes/` / 冻结 | USER-GUIDE §3 明确「以真实目录为准」，并列为 P0-2；未改章程 |
| `NOW.md` 内「已批/待批」并存 | 审计报告列为 P0-2；文档未改写状态（避免审计期间篡改证据） |
| Skills `AGENT-COMPATIBILITY` 的「14 技能」 | USER-GUIDE README 入口与 §15 明确以 37 为准 |
| Radar README「离线、不联网」 | 已修正为「默认 fixture；`--source rest` 真实」 |

## 5. 尚未解决的问题

### 5.1 需要代码/数据修复（不在本次文档权限内）

1. **Radar P0**：`analyze` 覆盖人工状态；`--approved` 不置 `human_selected_for_research`；搜索丢弃 rate-limit。
2. **Governance P1**：`examples/basic-project` type 非法；`init` 不追加 AGENTS 指针；approval 无 schema；命令数口径。
3. **Engine P1**：artifact 最终 hash 校验；G3 独立审批记录；发布边界排除内部文档；README 已完成。
4. **LXD P1**：13 份 references 合并；第二案例。
5. **Skills P2**：陈旧数字、错误安装命令、悬空 docs 页。

### 5.2 需要用户裁决/授权

1. **commit/push**：本次所有文档改动**未提交**（见 §6）。按既有纪律，等用户授权。
2. **G2 历史 17 篇评分**：材料齐，AI 不自评。
3. **Program 状态纠偏**（P0-2）：是否现在改 PROGRAM.md/NOW/PENDING（涉及管理事实，需用户确认口径）。
4. **在线发布（D02）**：仍未授权；本次未做任何部署。
5. **多课程扩展**（validate §10 + build_site + allowlist）：embodied WRITE 前需批准。

### 5.3 无法验证的功能

1. Skills 在任何宿主上的安装/发现/调用（仓库内无证据）。
2. Radar 121 仓 Stars 的外部真实性（只核对内部一致）。
3. G3 审批的用户原话载体（只有 AI 写入的字符串与 G2 §5）。
4. Governance 在 Engine 内的原始执行日志。
5. 10 倍规模下的构建/门禁性能。
6. 在线发布可行性（未部署）。

## 6. 修改文件清单（未提交）

| 仓库 | HEAD | 改动 |
|---|---|---|
| ai-knowledge-program | `cc098df` | 新增 `AUDIT-REPORT.md`、`POST-AUDIT-SUMMARY.md`、`PROJECT-DOCUMENTATION-INDEX.md`、`USER-GUIDE.md`；改 `PROGRAM.md`、`final-acceptance-2026-11-21.md`；`NOW.md`（本批前已有未提交） |
| ai-knowledge-to-learning-engine | `79c3fe8` | 新增 `docs/USER-GUIDE.md`、`.agent/skills/learning-experience-design/USAGE.md`；重写 `README.md`；`web/content.js`（构建，时间戳）；`document-registry.json`（前批已有） |
| matt-pocock-skills-zh-cn | `7326522` | 新增 `docs/USER-GUIDE.md`；改 `README.md` |
| agent-workspace-governance | `1b4a880` | 新增 `docs/USER-GUIDE.md`；改 `README.md` |
| github-project-radar | `b7442da` | 新增 `docs/USER-GUIDE.md`；改 `README.md`（修正离线表述） |

**未做**：commit、push、删除、reset、任何业务代码修改、任何数据文件改写。

**建议提交分组**（等授权）：
1. Program：审计报告 + 文档导航 + 使用指南 + 验收更正声明（1 笔）
2. Engine：docs/USER-GUIDE + LXD USAGE + README（1 笔，与 D21 业务改动分开）
3. Skills：docs/USER-GUIDE + README（1 笔）
4. Governance：docs/USER-GUIDE + README（1 笔）
5. Radar：docs/USER-GUIDE + README（1 笔）

## 7. 当前最重要的下一步

1. **修 Program 状态 + final-acceptance 已加声明**（P0-2 剩余：PROGRAM.md/NOW/PENDING 的旧名与「待批」）。这一步恢复「单一事实源」。
2. **修 Radar P0 与 Governance P1**（若这两个项目还要继续用）。不修则只能按「一次性探索 / 扫描工具」使用。
3. **Engine 收口 P1**：artifact 终检 + 独立审批文件 + 发布边界排除内部文档；然后继续 embodied 首批 RESEARCH。

## 8. 一句话回答「现在拥有什么」

> 你拥有一个**已被真实跑通一次的知识生产线**（Engine）、一个**单案例可用的学习体验方法**（LXD）、一个**能扫描但尚未被真实治理使用的工具包**（Governance）、一个**能抓一次数据但还不能持续追踪的情报工具**（Radar）、一个**能承载恢复但状态需要纠偏的统筹层**（Program），以及一个**结构完整、兼容性未验证的 37 技能库**（Skills）。

---

**最后验证**：2026-11-23 20:13 (+08:00)。
**最近更新**：2026-11-23。