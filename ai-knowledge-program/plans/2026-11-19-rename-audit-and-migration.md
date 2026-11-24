---
doc_id: PROG-RENAME-PLAN
type: migration-plan
status: completed
owner: qwenwork
created: 2026-11-19
updated: 2026-11-20
---

# 仓库命名统一 · 现状审计与迁移方案（已裁决：暂不执行，存档待重启）

> **2026-11-20 T1 已执行完成：Phase 2/4/5 + OmniWorld 跟进完成，实测见 NOW.md 与 Engine CHANGELOG**（详细实测数字由留痕补进本文件）。
> 任务书：用户 2026-11-19《项目统筹、架构收敛与仓库命名统一执行任务》Step 1 / Step 4。
> **2026-11-19 用户裁决（Q1–Q4）**：Q1 = 暂不执行（方案存档）；Q2 = 执行时引用更新范围**含品牌文案**（仍不动 window.RENDER_NOTES 内部契约与历史文档）；Q3 = **已执行**（残留旧副本 10 份→系统回收站，可恢复）；Q4 = **授权跟进**（OmniWorld-Engine 重指重装，待改名实际执行时生效）。
> **2026-11-19 后续指令（覆盖 Q1 的本地部分）**：用户批准**先改本地目录名**，GitHub 仓库名由用户稍后手动同步。已执行：`Render_Notes → ai-knowledge-to-learning-engine`、`mattpocock-skills-zh-CN-custom → matt-pocock-skills-zh-cn`（Move-Item 成功；git 完好 Engine `e848d28` / Skills `e1936f2`；改名后 validate 11/0/0、review_gate 37 claims 误标 0）。
> **2026-11-19 Phase 1 完成（用户手动 GitHub 改名，AI 核实）**：ls-remote 新 URL 实测 Engine HEAD=`e848d2801ec9940e154b9bf40bc26198a5d197ba`、Skills HEAD=`e1936f23e6e149c581124cc218e79860c07108ef`。**剩余 Phase 2（remote）/4（引用，含品牌文案+README 正式名）/5（验证）+ OmniWorld 跟进已移交下一个 AI，执行步骤见 `../handoffs/2026-11-19-program-handoff.md` §3 T1**。过渡态：remote 仍指旧 URL（重定向兜底）。
> 执行纪律：GitHub 重命名、本地目录移动、引用批量更新均属高影响操作，逐项经用户批准；commit/push 另行授权。

## 执行实测（T1 收尾 · 2026-11-20 留痕补记）

> 数据口径：六道门禁数字 / 引用更新统计 / 残留清点 = T1 执行会话实测（按实转记）；remote URL、GitHub 改名 ls-remote、笔①哈希、OmniWorld lock 37 条指向 = 留痕会话本机复核实测。

- **六道门禁（全部 exit 0）**：
  - build_site：Wrote `web\content.js`——69 documents / 17 sections / 11 glossary groups / 124 terms / 8 course units / 19 lessons / 7 interactive labs / 504 chapter term cards generated / 2426 KB（content.js 重建）；
  - validate_site：**11 checks passed, 0 warnings, 0 failures**；
  - check_chapter_arc：**5 篇 · OK**；
  - review_gate：**37 claims**（verification.status：verified 18 / open 12 / conditional 7；claim_type：verified_fact 13 / engineering_fact 13 / conditional 7 / contested 4；conditional/contested 被标为 verified：无）；
  - test_publish_boundary：exit 0；
  - check-translation：exit 0（翻译审计通过）。
- **引用更新统计**：Engine 24 文件、Skills 库 5 文件、Program 5 文件、OmniWorld-Engine 5 文件（Q2 含品牌文案；`window.RENDER_NOTES` 契约 / 上游引用 / 历史层未动）。
- **残留清点（Phase 5 验证项）**：本地回填注释 **4 个文件（预期 4，符合）**；活跃层残留 **26 条**（T1 实测）；`claude plugin validate . --strict` **not-installed（待验）**——`command -v claude` 与 `where.exe claude` 均无结果（T1 实测，留痕会话复核同为 exit 1），本机无 claude CLI，无法执行，按要求不算失败。
- **OmniWorld lock 验证（Q4，留痕会话复核实测）**：`OmniWorld-Engine/skills-lock.json` **37 条 `"source"` 全部 = `Vin535LFJ/matt-pocock-skills-zh-cn`，旧 slug 0 条**（`grep -c` 实测 37 / 0）；`AGENTS.md:74` 安装命令已指新 URL，pin `skills@1.7.1` 保留。
- **GitHub 改名核实（留痕会话复核实测）**：两仓新 URL `git ls-remote origin HEAD` 均 exit 0，远端 HEAD = Engine `e848d2801ec9940e154b9bf40bc26198a5d197ba` / Skills `e1936f23e6e149c581124cc218e79860c07108ef`；两仓 origin 已为新 URL（`git remote -v` 实测），upstream-en/zh 未动。
- **笔①**：`cf917386e22af0cf0a4a9b665fc48d41c1ca9130`（2026-11-20 02:30 +08:00，Engine 本地提交 "docs: decision-kit 七项裁决执行（D17–D19）+ 门禁复跑留痕（含重建 content.js）"；ahead origin/master 1，未 push，push 另行授权）。
- **遗留阻塞**：无（阻塞列表为空）。待授权/待验项：引用更新改动 commit/push（交接文档 §6 范围）；`claude plugin validate . --strict`（需本机有 claude CLI）。

## 1. 现状审计（2026-11-19 实测）

### 1.1 架构与状态

```
AI-Knowledge\（伞目录，非 git）
├── ai-knowledge-program\        统筹层（本地 git @ 87f9edf+本轮未提交重组）
├── Render_Notes\                Engine【唯一活跃线】master @ e848d28 = origin，工作树干净
├── mattpocock-skills-zh-CN-custom\  Skills 库 main @ e1936f2 = origin，干净；upstream-en/zh 双远程
├── agent-workspace-governance\  冻结 MVP（本地 git dec60ba，25 tests）
└── github-project-radar\        冻结 MVP（本地 git 942530b，38 tests）
```

- **Engine 真实进度**：P0–P6 完成；P7.1 四篇 blocker 修复完成；P8 仅预研（kcr_impact.py 只读影响分析 + 发布边界 allowlist）；P9 仅设计稿；P10 未启动。门禁（迁移后本会话复跑）：validate **11/0/0**、review_gate **37 claims**（16v/14o/7c）误标 0；build 69 docs（收口会话实测）。**G1/G2/G3 全部未通过**，decision-kit 七项全 OPEN。在线发布（D02）未授权。
- **Skills 库**：37 技能中文全量发行 + 4 处上游回填；SYNC/BACKPORTS/翻译审计脚本齐全；`check-translation.mjs` 断言上游引用存在。
- **已有能力（不重建）**：Engine `.agent/` 治理基座、research-to-learning Skill、KCR 设计、reviews 审核机制、四道 QA 门禁；Skills 库发行/同步/兼容性机制。
- **重复能力（均已冻结，无新增）**：Governance MVP ↔ Engine `.agent/`（sandbox 关系）；LXD Skill ↔ 未来设计体系；Radar ↔ 人工收藏。
- **CI/Pages/badge 实测**：两仓均**无 GitHub Actions、无 gh-pages 分支、无 CNAME、无 shields badge**。Render_Notes `.github/` 仅 copilot-instructions.md。改名不存在 CI/ Pages 断链面。
- **gh CLI 未安装**：AI 无法直接改 GitHub 仓库设置 → **GitHub 重命名需用户手动**（§4 Phase 1）。

### 1.2 过时文档与既有问题（审计发现）

| # | 问题 | 证据 | 处置 |
|---|---|---|---|
| 1 | ~~Engine 内残留统筹办公室旧副本~~ **已清理（2026-11-19 Q3 批准执行）**：`site-vitepress/docs/program-office-delivery/` 10 份→系统回收站（可恢复）；Test-Path 复核 False | 本会话 host_safe_delete 回执 + Test-Path 实测 | 已关闭 |
| 2 | WORKFLOW_STATE.md:99 "迁移待办"已过期（迁移已完成） | 上轮迁移实测 | 下次 Engine 收口更新 |
| 3 | VitePress config.mjs **无 base 字段**（默认 '/'）；若未来发 GitHub Pages 项目页必须补 base，否则资源 404 | config.mjs 全文 24 行实测 | 与本次改名无关；发布（D02）未授权，登记不处理 |
| 4 | `_mp_skills_verify\skills-lock.json`（E:\AI-Tools）14 条指向 `../mattpocock-skills-zh-CN-custom`，该 E 盘路径 PD-002 迁移后已不存在——**改名前就已断** | lock 原文实测 | 一次性验证产物，按需重建或废弃，不阻塞 |
| 5 | 外部活跃消费者：`OmniWorld-Engine\skills-lock.json` 37 条 GitHub 源 = custom 仓旧 slug；`OmniWorld-Engine\AGENTS.md:74` 安装命令逐字引用旧 slug | 本会话读 lock 原文核实 | 改名后需重指 + 重装（**需拍板 Q4**，范围外项目） |

## 2. 命名方案（正式名称与仓库名分离，2026-11-19 任务书固定）

**原则：正式名称承担解释，仓库名只是标识**——Engine 增加新功能、Skills 库增加新技能都不必改名。正式命名体系全表见 `../PROGRAM.md §8`（含 README 标准描述与 7 条命名规则）。

| 当前 | 目标仓库名/目录名 | 正式名称 | 动作 |
|---|---|---|---|
| GitHub `Vin535LFJ/Render_Notes` + 本地目录 | `ai-knowledge-to-learning-engine` | AI Knowledge-to-Learning Engine | GitHub 重命名（用户手动）+ remote set-url + Move-Item |
| GitHub `Vin535LFJ/mattpocock-skills-zh-CN-custom` + 本地目录 | `matt-pocock-skills-zh-cn` | Matt Pocock Skills 中文定制发行版 | 同上 |
| 本地 `ai-knowledge-program` | `AI-Knowledge-Program`（仅大小写） | AI Knowledge Program | 两步 Move-Item（经临时名），可选 |
| `AI-Knowledge` / `agent-workspace-governance` / `github-project-radar` | 不变 | AI Knowledge Workspace / Agent Workspace Governance / GitHub Project Radar | 已符合规范 |

**README 更新（随 Phase 4 引用批次执行）**：两仓 README 标题改为正式名称，描述采用 PROGRAM.md §8 标准英文描述；Skills 库必须明确标注"中文适配定制发行版"，不得造成上游官方发行版误解。旧名称此后只出现在迁移说明、历史记录与必要兼容说明中。

**命名规范**：产品/能力仓库与本地目录一律小写 kebab-case 且目录与仓库名一致；**含旧名的历史文件名不改**（`Render_Notes_2.0_双线规划.md`、旧方案文档、`.cursor/rules/render-notes.mdc`），指向它们的相对链接继续有效；git 历史不重写。

## 3. 影响清单（全量扫描结论）

### 3.1 Engine（Render_Notes → ai-knowledge-to-learning-engine）

**必须改（功能依赖，3 处 URL + 1 处状态文档）**
| 位置 | 内容 |
|---|---|
| `tools/build_site.py:63` | `REPO_URL`（注入 content.js 的 repo 字段 → 前端 GitHub 按钮） |
| `site-vitepress/.vitepress/config.mjs:17` | socialLinks GitHub URL |
| `web/index.html:73` | repoLink fallback href（运行时被 content.js 覆盖，仍需同步） |
| `PROJECT_CURRENT_STATE.md:16` | 写死的 origin URL |

**应改（活跃文档名称/路径，约 40 处）**：README 标题、`.agent/README.md:14`、两个 Skill 文档（research-to-learning 6 处 / learning-experience-design 8 处）、`tools/course.json:3` title、source-registry.json 5 处来源 title、site-vitepress/README、五个适配入口标题品牌。**其中约 1/3 是指向含旧名文件名的链接——文件不改名则不会坏，可不改。**

**生成物（重建，不手改）**：`web/content.js`（约 95 处旧名，含 repo URL）、`.agent/indexes/document-registry.json`（5 处）、site-vitepress docs/sidebar/dist（gitignored）。改 build_site.py 后必须重建 content.js，否则前端 GitHub 按钮仍指旧名。

**绝不能动**：
- `window.RENDER_NOTES` 全局变量名 = **4 文件契约**（app.js:4 / build_site.py:510 / validate_site.py:251-252 / test_publish_boundary.py:81），改名必须四处联动否则 validate FAIL——**本次不改**（纯内部标识，无外部影响）。
- 历史层：DECISIONS.md / CHANGELOG.md / `.agent/decisions|changes|plans` / reviews 历史材料 / 两份旧方案文档（D13 保护"不改不删不覆盖"）/ archive / `.workbuddy-ai/memory`。
- 前端品牌文案（app.js 面包屑/标题 16 处、index.html meta）——纯文案，是否随改由 Q2 决定。
- npm 包名 `render-notes-site-vitepress`（private 不发布，不改不坏）。

**本地目录改名风险 ≈ 0**：五个核心 Python 工具全部 `Path(__file__).resolve().parent.parent` 相对解析，无硬编码绝对路径（逐一抽查实测）。唯一注意：移动前确认无其他会话/IDE 占用该目录。

### 3.2 Skills 库（mattpocock-skills-zh-CN-custom → matt-pocock-skills-zh-cn）

**必须改（活跃配置/规则，3 处）**：`.claude-plugin/plugin.json:10` repository URL（改后按 AGENTS.md 跑 `claude plugin validate . --strict`，本机若无 claude CLI 则标注待验）；`AGENTS.md:23` "安装命令保持指向旧 slug"的活跃规则；`.git/config` origin（set-url，**upstream-en/zh 不动**）。

**应改（活跃文档 16 处）**：README.md 7 处（npx skills add / plugin marketplace add / skills.sh URL）、AGENT-COMPATIBILITY.md 5 处验收命令、UPSTREAM.md 4 处 origin URL/SSH + 自述目录名。

**替换雷区（最高优先纪律）**：`vinvcn/mattpocock-skills-zh-CN`（29 处上游引用）是旧 slug 的**前缀子串**；`mattpocock/skills`（71 处）遍布 docs issue 链接与 4 处回填注释；`check-translation.mjs:54-60` 断言上游引用必须存在。**只允许锚定 `Vin535LFJ/mattpocock-skills-zh-CN-custom` 全串精确替换，禁止裸替换 `mattpocock-skills-zh-CN`**。替换后跑 `node scripts/check-translation.mjs` + 核对"本地回填"注释恰 4 处。

**不动**：SYNC.md / BACKPORTS.md（0 处 custom 引用，全上游/历史）、marketplace.json（source:"./" 无 slug）、check-translation.mjs、全部脚本（无 slug 无绝对路径）、历史记忆。

**外部消费者**：
| 位置 | 指向 | 处置 |
|---|---|---|
| `OmniWorld-Engine\skills-lock.json`（37 条）+ AGENTS.md:74 | custom 仓 GitHub 源 | 改名后新 slug 重装（**pin skills@1.7.1**，1.7.2 在 Node 20 崩溃）+ 更新命令；需 Q4 批准 |
| `E:\AI-Tools\skills-zh-full\skills-lock.json`（37 条） | **vinvcn 上游** | **不动、不重装** |
| `E:\AI-Tools\_mp_skills_verify\skills-lock.json`（14 条） | 已断的 E 盘旧路径 | 改名前已断；按需重建或废弃 |
| `E:\AI-Tools\doc-governance` | 0 引用 | 无关 |
| 用户级 `.zcode` 活跃记忆（omniworld 项目 2 文件） | 旧 slug/旧路径 | 追加"已改名"更正条目，不改写历史 |
| agent-workspace-governance 3 处 URL | custom 仓 | 冻结期不动正文，GitHub 重定向兜底；解冻时更新 |

### 3.3 Program 办公室与跨项目

- PROGRAM.md / NOW.md / ROADMAP.md / PARKING-LOT.md / handoffs 中的目录名与路径：随本地改名同步更新（本办公室活跃文档）。
- `references/gpt-architecture-guidance.txt`：用户引导原件，**只读不改**。
- decisions/ 历史 PD 记录、archive/：**不改**。
- 其他 AI 会话的工作区绑定：旧路径会话需在新路径重开（迁移后已知事项）。

## 4. 迁移顺序（批准后执行）

| Phase | 动作 | 执行者 | 验证 |
|---|---|---|---|
| 0 前置 | 记录两仓 HEAD 基线；清理 Engine 内残留旧副本（Q3）；确认无会话占用 | AI | git status 干净；副本入回收站可恢复 |
| 1 GitHub 重命名 | 两仓 Settings → General → Repository name 改为目标名 | **用户手动**（环境无 gh CLI） | 新 URL 可访问；旧 URL 301 重定向（git/web 均兜底，但不可长期依赖） |
| 2 remote 更新 | 两仓 `git remote set-url origin <新URL>`（Skills 库 upstream 不动） | AI | `git fetch` + `git ls-remote` 成功 |
| 3 本地目录改名 | Move-Item ×2（+ 可选办公室大小写两步改名） | AI | git log/status 完好；Engine 只读门禁复跑 |
| 4 引用更新 | 按 §3 锚定精确替换，**两仓各一笔独立 commit**（授权后）；Engine 重建 content.js + document-registry | AI | 见 Phase 5 |
| 5 验证留痕 | Engine：build/validate/arc/review_gate/publish-boundary 全量复跑；Skills：check-translation.mjs + 回填计数 + plugin validate（若可用）；grep 活跃层旧 slug 残留清零；更新 NOW.md 与本文件状态 | AI | 实测数字写入 NOW.md；commit/push 另行授权 |
| 6 外部跟进 | OmniWorld-Engine 重指重装（Q4）；.zcode 记忆更正条目 | AI（另行批准） | 新 lock source = 新 slug |

**不做**：字符串全局裸替换；改历史文档/文件名/内部契约变量；动上游 remote 与上游引用；动冻结仓正文；顺手发布 Pages。

**执行节奏（用户 2026-11-19 明确要求）**：不在同一次执行里既改名、又大规模迁移、又重构 Engine。先 Program + 审计 + 方案（已完成）→ 用户确认 GitHub 改名 → 集中一次性迁移全部引用并验证 → Engine 开发持续推进，不被改名工作打断。未批准前不提前修改远程 URL 和本地路径，避免新旧地址混用。

**逐仓验证清单（Phase 5 必验）**：
- 两仓：`git fetch` / `git push`（授权后）正常；历史提交仍可访问（`git log` 全量在）；remote 指向新 URL。
- Engine：build/validate/arc/review_gate/publish-boundary 全绿；前端 GitHub 按钮指向新 URL（content.js 重建后）；文档内链可达；Agent 适配入口能找到 `.agent/` 与 Skills。
- Skills：`node scripts/check-translation.mjs` 通过；"本地回填"注释恰 4 处；上游引用 29+71 处未误伤；`claude plugin validate . --strict`（若 CLI 可用）；安装命令按新 slug 可解析。
- 外部：OmniWorld-Engine 新 lock source = 新 slug（Q4 已授权）；活跃层 grep 旧 slug 残留清零（历史层除外）。

## 5. 回滚方案

| 层 | 回滚 |
|---|---|
| GitHub | Settings 改回旧名（重定向随之恢复）；旧名未被他人注册前完全可逆 |
| 本地目录 | Move-Item 移回原名（git 整目录移动无损） |
| remote | `git remote set-url` 改回旧 URL（重定向期内旧 URL 仍可用） |
| 引用更新 | 两仓各一笔独立 commit → `git revert` 单笔即可；content.js/registry 用生成器重建 |
| Skills 重装 | lock 恢复旧 slug（重定向期内可解析） |
| 副本清理 | 回收站恢复 |

风险窗口：GitHub 改名后旧 slug 若被他人抢注则重定向失效——Phase 2–4 应在同一工作时段连续完成，缩短窗口。

## 6. 裁决记录（2026-11-19 用户会话）

- Q1 迁移方案：**暂不执行**——方案存档（deferred），先回 Engine 主线；重启需用户重新批准。
- Q2 引用更新范围：**含品牌文案**（执行时生效；window.RENDER_NOTES 契约、历史文档、上游引用仍不动）。
- Q3 残留副本清理：**批准，已执行**——10 份→系统回收站（recoverable=true），Test-Path 复核 False，Engine 工作树保持干净。
- Q4 OmniWorld-Engine 跟进：**授权**（待改名实际执行时生效：新 slug 重装 pin skills@1.7.1 + AGENTS.md:74 更新 + .zcode 活跃记忆更正条目）。

## 7. 审计证据索引

- 两仓 git remote/branch/status/log：本会话宿主实测（2026-11-19）。
- Engine 全量扫描：子代理只读报告（A≈43 处/14 文件、B≈41 处/16 文件、C 生成物 content.js≈95、D 历史≈39、E 外部≈20；全仓活跃层约 270 处匹配）。
- Skills 全量扫描：子代理只读报告（主仓 custom slug 22 处/7 文件；上游 vinvcn 29 + mattpocock 71 不动；外部 lock 三处原文核实）。
- 关键异常复核：program-office-delivery 存在性 + git check-ignore（本会话实测）；OmniWorld-Engine lock source（本会话读原文）。