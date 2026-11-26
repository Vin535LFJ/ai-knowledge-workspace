# github-project-radar 只读审计报告

- 审计时间：2026-11-26（本地时间）
- 审计对象：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\github-project-radar`（本地 git 仓，5 笔提交）
- 审计方式：只读。代码/文档用 Read/grep；数据库用 `py -3` + `sqlite3.connect("file:...?mode=ro", uri=True)`；测试运行仅写 tempfile 临时库（tests 全部使用 `tempfile.TemporaryDirectory`，见 tests/test_radar.py:68 等），未触碰两个真实 .db。
- 对照仓：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine`（下称 Engine，git 仓，`git rev-parse` 确认 true）。

## 0. 提交历史（git log --oneline）

```
e2815d9 docs: 提交作者重写注记（4 笔，公司邮箱移除，tree 哈希不变）
0842515 fix: P0-A analyze 不再覆盖人工审核状态；P0-B --approved 写入完整人工批准状态
d09fad6 docs: 新增 USER-GUIDE（20 节 + 12 条已知限制）+ README 纠偏
375f51b feat: 真实 GitHub REST 客户端落地 + 匿名最小发现实跑 + 首份周报产物
45ee5ec init: GitHub Project Radar MVP 首笔提交
```

`git status --short` 干净；`git ls-files` 共 38 个文件，两个真实 .db 均未被跟踪（.gitignore 含 `radar*.db`、`*.db-journal`）。

## 1. 代码结构盘点

### 1.1 radar/ 各模块实际实现（均为纯 Python 标准库）

| 模块 | 行数 | 实际实现 | 证据 |
|---|---|---|---|
| `radar/storage.py` | 590 | SQLite 封装：4 表（repositories/snapshots/collection_runs/candidates）；快照按 (repository_id, captured_at) 唯一、INSERT OR IGNORE 只增不改；`init_db` 幂等建表 + `_ensure_columns` ALTER 补齐旧库增量列（storage.py:135-166）；**机器/人工字段分离**：`CANDIDATE_MACHINE_COLUMNS` / `CANDIDATE_HUMAN_COLUMNS`（storage.py:96-111），`upsert_candidate` 冲突时只更新机器列并保留 evaluation 内人工审计键（storage.py:381-444）；`approve_candidate` 写完整批准状态（review_status=approved_for_research、human_selected_for_research=1、approver/approved_at/approval_reason + review_log），重复批准幂等 no-op（storage.py:446-508） | 已全文读 |
| `radar/collector.py` | 236 | 注入式 ApiClient Protocol（search_repositories/get_repository）；重试退避 `_call_with_retry`；`build_search_queries` 按 topics 配置生成查询；`discover` / `refresh_tracked`；`collection_runs` 记录运行审计；`_persist` 单事务落库 | collector.py:23-207 |
| `radar/scoring.py` | 510 | 双评分体系：旧综合分 5 维（innovation/relevance/engineering_maturity/reusability/growth_momentum，各含 score/reason/basis）+ `evaluate_three_scores` 三维独立分（发现信号/工程质量/相关性），信号缺失标 unknown；配置从 config/scoring.json 读 three_scores，失败回退内置默认（scoring.py:248-269） | 函数清单 + 抽读 |
| `radar/growth.py` | 109 | `compute_growth`：基于自有快照算 7d/30d 星标/Fork 增量；快照 <2 或时间跨度不足时 `insufficient_history=true`、增长字段置 null，不编造数字（growth.py:44-127） | grep 证实 3 处 insufficient_history 分支 |
| `radar/review.py` | 155 | 旧状态机 STATES=[Discovered,Triaged,Watch,Research,Adopt,Ignore] + 受限转换表；canonical 生命周期（含 approved_for_research）与旧别名双向映射 `normalize_status`/`to_legacy_status`；`record_transition` 审计 | review.py:16-149 |
| `radar/research.py` | 106 | 深度研究 Markdown 模板渲染（13 节），不可验证内容一律 `[未验证]`；默认输出 `research/owner__repo.md`（**CWD 相对路径**，research.py:34,77-80） | 已全文读 |
| `radar/export.py` | 191 | 研究任务 JSON 纯输出：15 字段契约 `EXPORT_FIELDS`；`validate_task`+`validate_intake_task` 强校验类型与人工门槛（approved_for_research 必须 human_selected_for_research=true，export.py:116-117）；`--approved` 先经 storage.approve_candidate 落库再**回读数据库真实状态**导出（export.py:147-170）；无任何写外部项目代码 | 已全文读 |
| `radar/reports.py` | 294 | 周报三格式：dir（reports/YYYY-Www/ 下 7 文件 A–G 板块）、summary（单文件 .md）、json；输出根目录由参数 `reports_root` 传入，模块内无硬编码绝对路径（reports.py:137-288） | grep + 抽读 |
| `radar/sources/` | base 26 / rest 151 / trending 17 / ossinsight 17 | `base.SourceClient` ABC；`rest.GitHubRestClient` 为**真实实现**（stdlib urllib，GITHUB_TOKEN 仅环境变量，匿名 7s/认证 1s 限速，403/429 抛 RateLimitError，rest.py:55-124）；trending/ossinsight 为离线 stub（NotImplemented 类占位，仅授权联网后注入） | 已抽读 rest.py |
| `radar/models.py` | 125 | Repository/Snapshot/Candidate/Evaluation dataclass + utc_now_iso | 函数清单 |
| `radar/__init__.py` | 19 | `PACKAGE_ROOT` 由 `__file__` 推导，`load_config` 从包根 config/ 读 JSON | 已全文读 |
| `fixtures/client.py` | 38 | 离线 FixtureApiClient，读同目录 sample_data.json（106 行样例），子串匹配模拟搜索，零网络 | 已全文读 |

### 1.2 cli/radar.py 子命令（共 10 个）

`init-db`、`collect`（--source fixture/rest，--max-queries）、`snapshot`（--full-name/--captured-at）、`analyze`、`candidates`（--status）、`report`（--reports-root/--week/--format dir|summary|json）、`export`（--output/--status/--approved/--approver/--reason）、`query`（SQL）、`review`（candidate_id/--current/--target/--reviewer/--decision/--objective）。全局 `--db`（默认 PROJECT_ROOT/radar.db）。证据：cli/radar.py:238-297。

注：`query` 帮助文案称"只读 SQL"，但实现是普通 `sqlite3.connect(args.db)`（cli/radar.py:210），可执行写 SQL——只读靠使用者自律，非强制（小瑕疵，非本次审计引入）。

### 1.3 测试

- 测试文件：仅 `tests/test_radar.py`（854 行）。
- 实测：`py -3 -m unittest discover -s tests` → **`Ran 58 tests in 2.880s` / `OK`**（stderr 中的 "[export] 错误: --approved 必须…" 为负路径测试的预期输出）。
- 测试全部用 tempfile 临时库/临时输出（tests/test_radar.py:68,202,254,272 等），不触碰仓内真实 .db。

## 2. 真实数据盘点（只读 sqlite，mode=ro）

### 2.1 radar-real-20261121.db（389,120 字节）

| 表 | 行数 |
|---|---|
| repositories | 121 |
| snapshots | 200 |
| candidates | 121 |
| collection_runs | 1 |
| sqlite_sequence | 3 |

- **review_status 分布**：Discovered=120，Research=1（id=100，ruvnet/ruflo，总分 63.0，为全库最高分）。
- **human_selected_for_research=1 计数：0**。即按契约**没有任何一条可导入 Engine 的任务**。
- **approver / approved_at 列：不存在**（PRAGMA table_info 实测列表止于 data_quality）。该库建于 P0-B 修复（0842515）之前，schema 未升级；代码 `init_db` 的 `_ensure_columns` 会在下次运行时幂等 ALTER 补齐（storage.py:149-155），本次审计未执行。
- **快照采集时间范围**：2026-11-21T11:46:46Z → 11:47:06Z，4 个批次 × 50 条（每仓库仅 1 个快照 → 全部 insufficient_history=true，与导出物一致）。collection_runs 仅 1 次：started_at=2026-11-21T11:46:44Z，source=collector.discover，status=success。
- Top5 候选：ruvnet/ruflo 63.0、bytedance/deer-flow 61.0、Graphify-Labs/graphify 59.33、langchain-ai/langchain 59.0、paperclipai/paperclip 58.0。

### 2.2 radar-real-hdr.db（36,864 字节）

- 4 张业务表全部 **0 行**（repositories/snapshots/candidates/collection_runs），sqlite_sequence 0 行。
- candidates 列同样**无 approver/approved_at**（旧 schema）。
- 无快照，无时间范围。结论：这是一个只跑过 `init-db` 的空壳库（推测为 HDR 主题采集预留，从未采集）。

### 2.3 仓内导出物

`reports/research-intake-hdr-demo.json`（已提交入 git）：schema_version=1，task_count=1，任务即真实库候选 id=100 ruvnet/ruflo，exported_at=2026-11-21T11:47:48Z（紧接快照采集之后，review_log 记"P10 验收：…Research Intake 导出演示"）。关键字段：`review_status="Research"`、**`human_selected_for_research=false`**、四个溯源字段全 null。按 engine-interface.md 的人工门槛，该文件是**演示导出，不构成可导入任务**。文件名含 "hdr" 但内容是 ai-agent 主题仓库，与空的 radar-real-hdr.db 无数据关联。

## 3. 嵌入 Engine（integrations/github-radar/）的路径可行性

总体结论：**几乎所有路径都由 `__file__` 推导，整仓平移本身不会坏**；真正的风险是①默认输出落点进入 Engine 仓、②CWD 相对路径、③顶层包名占用。逐点清单：

| 位置 | 现状 | 平移后的影响 |
|---|---|---|
| cli/radar.py:15-17 | `PROJECT_ROOT = dirname(dirname(__file__))`，插入 sys.path[0] | 随目录移动自动正确；但把 `radar`/`cli`/`fixtures` 三个**通用顶层包名**注入 sys.path，若 Engine 将来出现同名模块会被遮蔽（当前 Engine 顶层无 cli/radar/fixtures，tools/ 为平铺脚本，暂无冲突——实测目录清单） |
| cli/radar.py:29 | `DEFAULT_DB = PROJECT_ROOT/radar.db` | 默认库将落在 `Engine/integrations/github-radar/radar.db`。**Engine 的 .gitignore 没有任何 *.db 规则**（实测其 .gitignore 全文），真实数据有误提交风险。需改默认路径指向数据目录，或在 Engine .gitignore 增加 `integrations/github-radar/*.db` |
| cli/radar.py:30, 267 | `DEFAULT_REPORTS = PROJECT_ROOT/reports`；--reports-root 默认同上 | 周报默认写进 Engine 仓内 integrations/github-radar/reports/；需裁决提交产物还是 ignore，或改默认到 Engine 的 evidence/ 类目录 |
| cli/radar.py:179 | `os.path.relpath(path, PROJECT_ROOT)` | 仅打印相对路径，随移正确，无碍 |
| radar/__init__.py:11-12 | PACKAGE_ROOT/CONFIG_DIR 由 `__file__` 推导 | 随移正确，config/ 一起搬即可 |
| fixtures/client.py:10 | FIXTURE_PATH = 同目录 sample_data.json | 随移正确 |
| radar/research.py:34, 77-80, 88 | `output_dir="research"` 为 **CWD 相对路径** | 从 Engine 根运行会在 **Engine 根**创建 research/ 目录——这是唯一真正"会坏"的路径假设。需锚定到模块根或改为必填参数 |
| radar/collector.py:207 | `sqlite3.connect(self.storage.db_path)` | 使用传入 db 路径，无独立假设 |
| radar/scoring.py:248-256 | three_scores 配置经 `load_config`（包根 config/） | 随移正确 |
| tests/test_radar.py:16-18 | PROJECT_ROOT 由 `__file__` 推导并插 sys.path | 用 `py -3 -m unittest discover -s integrations/github-radar/tests` 可跑；但从 Engine 根做全仓 discover 时，`radar`/`cli`/`fixtures` 顶层导入依赖该 sys.path 注入，与 Engine 其他测试同进程跑存在包名冲突隐患 |
| tests/test_radar.py:592, 628 | `from fixtures.client import ...`、`from cli.radar import main` | 同上：顶层包名占用问题；建议长期改为 `integrations.github_radar.*` 命名空间或独立进程运行 |
| docs/operating-guide.md:50-56、README.md:60-90 | 示例命令均为 `py -3 cli/radar.py ...`、`--db radar-real.db`、`--reports-root reports` | 隐含 CWD=仓根；平移后文档命令需加目录前缀或说明 cd |

另外：仓内 `__pycache__`/`.pyc` 已被 .gitignore 覆盖，平移时应剔除物理缓存目录（cli、radar、fixtures、tests 下均有）。

## 4. 与 Engine 的接口

### 4.1 导出契约（docs/engine-interface.md，已全文读）

- 单向纯输出：Radar 只产研究任务 JSON，**没有任何写入 Engine（Render_Notes）的代码**；是否导入由 Engine 决定（engine-interface.md:14-18）。
- 人工门槛：仅 `human_selected_for_research=true` 的任务可导入 Engine source inbox；Engine 必须按该字段过滤，不得仅凭 review_status（:20-23, :34）。
- 结构：顶层 schema_version=1 / exported_at / task_count / tasks；每任务 15 字段（candidate_id、repository、url、topic、discovery_reason、star_metrics、evaluation、review_status、research_objective、created_at、human_selected_for_research、source_url、observed_at、retrieved_at、data_quality），导出前 validate 自检（:36-69；代码 export.py:21-38,77-119 与文档一致）。
- 真实性：insufficient_history=true 时增长为 null；**所有 Radar 初筛分数不得当作知识证据**，导入后须 Research Agent 重新核验（:71-77）。
- 名称映射：架构建议名 `github-radar` ≡ 本地目录 `github-project-radar`，用户裁决不改名（:12）。

### 4.2 Engine 侧实际使用证据：**未找到**

- `rg -i "research-intake|research_intake"` 在 Engine 全仓：**0 命中**。
- `rg -i "radar"` 在 Engine 全仓仅命中 3 个状态文档：WORKFLOW_STATE.md:77、CHANGELOG.md:693/712、DECISIONS.md:141——都是把 radar 作为**兄弟项目**的建设记录（P4/P6/PD-Q2），不是导入消费记录。
- `reviews/p10`（10 文件）与 `reviews/embodied-batch1`（11 文件）逐一 grep `radar|ruvnet|ruflo|intake`：intake-manifest 均为 Engine 自己的外部权威源清单（p10 为 AOSP/ITU/UHD Forum 等 HDR 资料；embodied 为具身智能资料），**无任何 Radar 导出物被引用**。
- Engine 仓不存在 `integrations/` 目录（Test-Path False）。
- 结论：接口契约已定义且导出侧已实现并有演示产物，但 **Engine 侧的摄取端从未落地，闭环未走通**。这与数据侧一致：真实库 human_selected_for_research=1 计数为 0，本来也没有可导入任务。

## 5. 结论与建议

1. **作为 Engine 内部模块保留：合理，但当前是"契约就绪、未接通"状态。** 理由：纯标准库零依赖、58 测试全绿、机器/人工字段分离与人工批准门槛设计严谨（P0-A/P0-B 已修复）、导出契约文档与代码一致；平移成本低（路径基本 `__file__` 相对）。保留为独立仓或平移为 `integrations/github-radar/` 均可行；若平移，必改项只有三处：research.py 的 CWD 相对输出（research.py:34,77）、默认 DB/reports 落点与 Engine .gitignore 配套（cli/radar.py:29-30）、顶层包名冲突防护（cli/radar.py:15-17 + tests 导入方式）。
2. **数据文件处置：保持 ignored 本地数据，不入任何 git。** 本仓 .gitignore 已覆盖（`radar*.db`、`*.db-journal`），两个 .db 实测未被跟踪，现状正确。若平移，Engine .gitignore 必须补 db 规则（现无）。radar-real-20261121.db 是有价值的真实采集样本（121 仓库、200 快照、单次 20 秒窗口），建议原地保留作本地数据；radar-real-hdr.db 为 0 行空壳，可保留亦可清理（清理属写操作，须用户另行授权，本次未动）。
3. **schema 滞后提示**：两个真实库都缺 approver/approved_at/approval_reason 列（建库早于 0842515）。下次对真实库跑任何含 `init_db` 的命令会幂等补齐，无需迁移脚本；在此之前不应对旧库使用 `--approved`（cmd_export 已先调 init_db 补列，cli/radar.py:186，路径是安全的）。
4. **接通 Engine 前的门槛**：目前 0 条 human_selected_for_research=true；demo 导出（research-intake-hdr-demo.json）该字段为 false，只能当格式样例。真正接通需要：人工批准若干候选 → `export --approved --approver` → Engine 侧新建摄取端（现无 integrations/、无 research-intake 消费代码）。

## 附：审计操作留痕

- 只读 DB 脚本：`C:\Users\Giant\AppData\Local\Temp\qwenwork\audit_radar_db.py`、`audit_radar_q2.py`（均 `file:...?mode=ro` URI 连接）。
- 测试运行：`py -3 -m unittest discover -s tests`（cwd=radar 仓根）→ Ran 58 tests, OK；测试自身仅写系统 tempfile。
- 未修改仓内任何文件，未对真实数据库执行任何写入。