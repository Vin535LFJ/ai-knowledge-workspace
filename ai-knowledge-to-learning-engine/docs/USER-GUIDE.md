---
doc_id: ENGINE-USER-GUIDE
type: user-guide
status: active
owner: qwenwork
created: 2026-11-23
updated: 2026-11-23
verified_at: 2026-11-23
verified_against: ai-knowledge-to-learning-engine@79c3fe8
---

# AI Knowledge-to-Learning Engine 使用指南

> 面向真正要生产一批教材的人。目标：不读源码，也能把「原始资料 → 研究 → 知识 → 教材 → 实验 → 网站 → 审核」跑一遍。
> 所有命令均在仓库根目录 `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine` 执行。

---

## 1. 项目理解

### 1.1 目标

把任意领域的原始资料，变成**可信、可学、可实践**的学习产品：

```
原始资料 → 深度研究 → 证据提取 → 结构化知识 → 知识关联
        → 课程设计 → 教材 → 实践/实验 → 交互式网站 → 反馈 → 知识更新
```

它**不是**只生成 Markdown：它有证据台账、知识模型、课程 JSON、离线学习站、交互实验、人工审核门、KCR 影响分析和可恢复的运行状态机。

它**也不是**全自动流水线：研究、写作、审核仍由人/AI 协作完成，工具负责约束、校验、留痕和呈现。

### 1.2 主要能力

| 能力 | 入口 |
|---|---|
| 断言与来源台账 | `evidence/claim-ledger.json`、`evidence/source-registry.json` |
| 概念/术语/关系 | `knowledge-model/concepts.json`、`tools/glossary.json`、`tools/graph.json` |
| 课程结构（两层） | `tools/course.json`（站点）、`courses/*/course.json`（pilot 契约） |
| 教材 | `courses/video-rendering-journey/lessons/*.md` |
| 实验/自测 | `tools/labs.json`、`courses/*/quizzes/*.json` |
| 离线学习站 | `tools/build_site.py` → `web/content.js` |
| 结构门禁 | `tools/validate_site.py`（12 项） |
| 章节弧检查 | `.workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py` |
| 断言审核门 | `tools/review_gate.py` |
| 发布边界 | `tools/publish_boundary.py` + `tools/publish-allowlist.json` + `tools/test_publish_boundary.py` |
| KCR 影响分析 | `tools/kcr_impact.py` + `tools/kcr/schema/*` + `tools/kcr/validate_kcr.py` |
| 工作流状态机 | `tools/run_state.py`（十阶段 + KCR 子状态） |
| 文档注册表 | `tools/build_document_registry.py` |
| 视觉 Floor 检查 | `.agent/skills/learning-experience-design/scripts/check_visual_floor.py` |

### 1.3 目录结构（真实）

```
ai-knowledge-to-learning-engine/
├── 00-导航与索引/ ... 07-3D渲染与算法实现/   ← 主知识文档（26 篇）
├── archive/                                  ← 旧版知识（12 篇，只读）
├── courses/video-rendering-journey/
│   ├── course.json                           ← pilot 课程契约（5 课）
│   ├── lessons/L01..L19.md                   ← 教材（19 份；L00 为地图课）
│   └── quizzes/L01,L02,L06,L11,L13.json      ← pilot 自测（5 份）
├── evidence/                                 ← claim-ledger / source-registry / README
├── knowledge-model/                          ← concepts / taxonomy / README
├── tools/
│   ├── course.json / glossary.json / graph.json / labs.json / feedback.json
│   ├── build_site.py / validate_site.py / review_gate.py
│   ├── kcr_impact.py / run_state.py / report_feedback.py
│   ├── build_document_registry.py / build_knowledge_model.py
│   ├── publish_boundary.py / publish-allowlist.json / test_publish_boundary.py
│   └── kcr/                                  ← schema / validate_kcr.py / selftests
├── web/                                      ← 离线学习站（index.html + content.js + assets）
├── site-vitepress/                           ← 第二套在线站源码（构建受 D10.6 阻塞）
├── reviews/                                  ← G1/G2 材料、KCR、审计、p10 批次
├── .agent/                                   ← 治理基座（constitution/skills/indexes/runs）
└── AGENTS.md / DECISIONS.md / WORKFLOW_STATE.md / CHANGELOG.md
```

### 1.4 重要数据类型

| 文件 | 关键字段 | 说明 |
|---|---|---|
| `evidence/claim-ledger.json` | `id`（V01…/C01…/P01…）、`claim`、`verification.status`（verified/open/conditional）、`verification.confidence`、`conditions`、`evidence`、`used_by_lessons` | 一条断言一条记录；**AI 不得自行升级状态** |
| `evidence/source-registry.json` | `id`（SRC-…）、`title`、`url`、`type`、`accessed`、`used_by_claims` | 来源与断言双向索引 |
| `knowledge-model/concepts.json` | 概念 id（K-…）、名称、关系 | 概念图，校验无环 |
| `tools/glossary.json` | `groups[].terms[]`（name/aliases/定义/为什么重要） | 站点术语层 |
| `tools/course.json` | `units[]`、`lessons[]`（id/title/objectives/reading/checkpoint/next） | **站点课程**（20 课/8 单元） |
| `courses/*/course.json` | `lessons[]`（pilot 契约，字段更严） | **pilot 课程**（5 课） |
| `tools/labs.json` | `id`、`lesson`、`terms`、任务 | 交互实验与课时绑定 |
| `.agent/runs/*.json` | `phase`、`status`、`artifacts[]`（path+sha256）、`human_gate`、`write_paths`、`transitions` | 运行态，**本地 gitignored** |

### 1.5 各生产阶段的职责

| 阶段 | 谁做 | 产物 | 检查 |
|---|---|---|---|
| INTAKE | 人 + AI | `reviews/<batch>/intake-manifest.md` | 查重、范围边界 |
| RESEARCH | AI（按 Skill） | `research-report-*.md` | 来源可访问、事实可核 |
| EVIDENCE | 人 + AI | claim-ledger / source-registry | `review_gate.py` |
| ARCHITECT | AI | concepts / glossary / graph | `validate_site.py` §9 |
| WRITE | AI | lessons/*.md | `check_chapter_arc.py` |
| DESIGN | AI（LXD Skill） | 页面增强、设计说明 | `check_visual_floor.py` |
| PRACTICE | AI | labs / quizzes | `validate_site.py` §10/§11 |
| REVIEW | **人** | G1/G2 材料 | 人工评分 |
| PUBLISH | 人批准 + AI | 本地 bundle | `build_site.py` + `validate_site.py` |
| FEEDBACK | 人 | feedback.json / 记录 | `report_feedback.py` |

---

## 2. 快速开始

### 2.1 环境要求

- Windows 10/11（当前实测环境）
- **Python 3**（命令用 `py -3`；若没有 `py` 启动器，用 `python`）
- 无第三方 Python 依赖（全部 stdlib）
- 可选：Node.js 20+（只用于 `site-vitepress/` 与 Skills 仓库的脚本，不影响主站）
- 可选：Microsoft Edge（无头渲染 QA）

### 2.2 依赖安装

**不需要 `pip install`。** 仓库工具全部只用标准库。

```powershell
py -3 --version
```

### 2.3 配置文件

无需环境变量。生产数据都在仓库内的 JSON：

- 课程：`tools/course.json`、`courses/video-rendering-journey/course.json`
- 术语：`tools/glossary.json`
- 实验：`tools/labs.json`
- 发布边界（强制，默认拒绝）：`tools/publish-allowlist.json`（v2，逐资产登记）
- 断言/来源：`evidence/*.json`（内部数据，不进学习站）

**新增任何 .md（或 evidence/、knowledge-model/ 下的 .json）后必须先登记**：在 `tools/publish-allowlist.json` 的 `assets` 里逐个加 `{"path": ..., "policy": "public"}`（或 `excluded-internal` + `reason`），否则 build 与 validate 双双 FAIL（默认拒绝，无目录通配）。archive/ 只允许 `offline-read-only`；`DECISIONS.md` / `CHANGELOG.md` / `WORKFLOW_STATE.md` / `reviews/` / `.agent/` 永不发布。

### 2.4 启动 / 构建 / 测试

```powershell
cd C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine

# 1) 构建学习站（唯一输出 web/content.js）
py -3 tools/build_site.py

# 2) 结构门禁（14 项；第 13 项 = 发布边界 v2：注册表↔磁盘、bundle==注册表、内部文件零泄露、在线树只含 public）
py -3 tools/validate_site.py

# 2b) 发布边界回归测试（29 项，夹具在临时目录，不碰真实课程）
py -3 tools/test_publish_boundary.py

# 3) 本地打开网站
py -3 -m http.server 8791 --directory web
# 浏览器访问 http://localhost:8791
```

### 2.5 测试命令

```powershell
# 发布边界（11 个测试）
py -3 tools/test_publish_boundary.py

# KCR 契约与影响链（16 个）
py -3 tools/kcr/selftest_impact.py

# 状态机（25 个）
py -3 tools/kcr/selftest_runstate.py

# 章节弧（19 篇；PowerShell 用 (Get-ChildItem ...).FullName 展开通配符）
py -3 .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py (Get-ChildItem "courses/video-rendering-journey/lessons/*.md").FullName

# 视觉 Floor（单篇）
py -3 .agent/skills/learning-experience-design/scripts/check_visual_floor.py "courses/video-rendering-journey/lessons/L13-坐标变换与MVP.md"

# 断言审核门（只打印，不改状态）
py -3 tools/review_gate.py
```

### 2.6 本地网站启动方式

- 离线双击：直接打开 `web/index.html`（零依赖，file:// 可用）。
- 本地服务：`py -3 -m http.server 8791 --directory web`（推荐，避免个别浏览器 file:// 限制）。
- 快捷键：`Ctrl/Cmd+K` 搜索、`G` 术语、`C` 教材、`L` 实验、`T` 技术索引、`M` 依赖图。

### 2.7 第二套站点（VitePress，可选）

```powershell
cd site-vitepress
npm run docs:dev
```

> **限制**：`docs:build` 在当前机器曾被 D10.6（删除权限拦截）阻塞；`site-vitepress/docs/` 是生成物且 gitignored。主用站点是 `web/`。

---

## 3. 日常工作流

### 3.1 导入原始资料

当前**没有**导入 CLI，INTAKE 是人工 + 模板：

1. 新建 `reviews/<batch>/intake-manifest.md`，记录：批次名、资料清单、来源、范围边界、查重结论。
2. 查重（示例）：

```powershell
rg -n "关键词1|关键词2" -g "*.md" .
```

3. 在 `run_state.py new` 时把本批要写的路径声明为 `--write-path`。

### 3.2 开始深度研究

1. 读 `.agent/skills/research-to-learning/SKILL.md`，按五阶段执行。
2. 产出 `reviews/<batch>/research-report-*.md`：每条事实带来源、区分「已核实/待核实/有争议」。
3. 外部来源必须真实可访问；抓取失败要如实记录，不能用不可核实内容充当证据。

### 3.3 生成结构化知识

1. 新断言写入 `evidence/claim-ledger.json`，**默认 `open/low`**；新来源写入 `source-registry.json` 并双向索引。
2. 新概念写 `knowledge-model/concepts.json`；新术语写 `tools/glossary.json`。
3. 重建派生文件：

```powershell
py -3 tools/build_knowledge_model.py
py -3 tools/validate_site.py
py -3 tools/review_gate.py
```

### 3.4 生成课程

1. 站点课程：编辑 `tools/course.json`（units/lessons/objectives/reading/checkpoint/next）。
2. pilot 契约：编辑 `courses/video-rendering-journey/course.json`（字段更严，validate §10 会逐字比对 frontmatter）。
3. 校验：`py -3 tools/validate_site.py`。

> **限制**：validate §10 要求 pilot 课 id ⊆ `tools/course.json`。**独立新课程会 FAIL**；多课程扩展是报批项（D21）。

### 3.5 生成教材

1. 新建 `courses/<course>/lessons/Lxx-标题.md`，frontmatter 至少含：`title/objectives/reading/checkpoint/claims/lab?`。
2. 按 `reviews/decision-kit/B4` 确立的 L01 Gold Standard + `.agent/skills/research-to-learning/references/lesson-quality-standard.md` 十维度写。
3. 门禁：

```powershell
py -3 .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py (Get-ChildItem "courses/video-rendering-journey/lessons/*.md").FullName
```

### 3.6 生成实践内容

- 实验：编辑 `tools/labs.json`（id/lesson/terms/任务/预期）。
- 自测：`courses/*/quizzes/Lxx.json`（pilot 5 课有；其余按规则缓建）。
- 联动：课程 `checkpoint` 与 quiz `prompt` 必须逐字一致（validate §11）。

### 3.7 生成和预览网站

```powershell
py -3 tools/build_site.py
py -3 tools/validate_site.py
py -3 -m http.server 8791 --directory web
```

构建会报告：documents / sections / glossary / course units / lessons / labs / cards / KB。

### 3.8 执行质量审核

1. `py -3 tools/review_gate.py`：看断言状态分布、conditional/contested 是否被误标 verified、未挂载课程。
2. `py -3 tools/validate_site.py`：12 项结构检查。
3. G2：按 `lesson-quality-standard` 十维度人工评分（≥85 通过），材料写在 `reviews/G2-Lxx-*.md`。
4. 独立审读：让另一个 Agent 只读审读，产出 blocker/major/minor，逐条修复。

### 3.9 处理知识变更（KCR）

```powershell
# 影响分析（只读）
py -3 tools/kcr_impact.py --claim-id V14
py -3 tools/kcr_impact.py --source-id SRC-RN-COLORMGMT --out reviews/kcr/impact-xxx.json

# 校验变更提案（Stage 2：human_decision 必须为 null）
py -3 tools/kcr/validate_kcr.py reviews/<batch>/change-proposal-*.json --stage2

# 真实 run 的 KCR 子状态
py -3 tools/run_state.py kcr --run-id <RUN-ID> --to APPROVED --approver "你的名字"
```

**规则**：AI 不预填 `human_decision`；APPROVED 必须人工。

### 3.10 恢复失败任务

```powershell
py -3 tools/run_state.py list
py -3 tools/run_state.py show --run-id <RUN-ID>
py -3 tools/run_state.py resume --run-id <RUN-ID>
py -3 tools/run_state.py retry --run-id <RUN-ID>
```

`show` 里的 `resume_point` 就是下一步；`write_paths=[]` 表示没有活动写锁，可安全接手。

---

## 4. 输出产物

| 阶段 | 目录/文件 | 类型 | 命名规则 | 依赖 |
|---|---|---|---|---|
| 研究 | `reviews/<batch>/research-report-*.md` | Markdown | `research-report-<topic>.md` | intake-manifest |
| 证据 | `evidence/claim-ledger.json` | JSON | `V##/C##/P##/E##` | 来源 |
| 来源 | `evidence/source-registry.json` | JSON | `SRC-<DOMAIN>-<NAME>` | — |
| 概念 | `knowledge-model/concepts.json` | JSON | `K-<NAME>` | glossary |
| 术语 | `tools/glossary.json` | JSON | 11 组 / 129 词 | — |
| 课程 | `tools/course.json` | JSON | L00–L19，8 单元 | 教材 |
| 教材 | `courses/*/lessons/*.md` | Markdown | `Lxx-标题.md` | course.json |
| 自测 | `courses/*/quizzes/*.json` | JSON | 与课 id 同名 | checkpoint |
| 实验 | `tools/labs.json` | JSON | 7 个 | 教材 |
| 站点 | `web/content.js`（生成物） | JS | 唯一产物 | 全部 JSON/MD |
| 审核 | `reviews/G2-Lxx-*.md`、`reviews/p10/*` | Markdown | `G2-<课>-deepening.md` | 教材 |
| 运行态 | `.agent/runs/*.json` | JSON | `RUN-YYYY-MM-DD-<slug>` | 全部阶段 |
| 注册表 | `.agent/indexes/document-registry.json`（生成物） | JSON | — | 所有 md frontmatter |

**依赖关系（简）**：
`source-registry → claim-ledger → concepts/glossary → course.json → lessons → quizzes/labs → content.js`
`run_state` 横切全部阶段；`document-registry` 由所有 md 派生。

---

## 5. 人工审批

| 门 | 谁批 | 材料 | 怎么批 |
|---|---|---|---|
| G1 证据 | 人 | `reviews/<batch>/G1-*-verification-queue.md` | 在裁决栏填写「升级/保持/补证」 |
| G2 质量 | 人 | `reviews/G2-Lxx-*.md` §5 | 五项打分 + 总分 + 裁决人/日期 |
| G3 发布 | 人 | run 的 artifact 汇总 | 两步，同一个人名：① `approval_chain.py record --run-id <ID> --gate G3 --approver "你的名字" --scope "批准了什么"`（把当前产物冻结为路径+哈希）② `run_state.py gate --run-id <ID> --pass --approver "你的名字"` |
| KCR | 人 | change-proposal JSON | `run_state.py kcr --to APPROVED --approver "你的名字"` |
| commit/push | 人 | 文件清单 | 明确授权后执行 |

**未回复不视为同意。** AI 不得代批、不得预填 G2 分数、不得自升断言。

> 审批证据链（2026-11-25 起）：登记审批之后，任何产物再被改动、或批准后新增产物，`advance` 进入 PUBLISH / FEEDBACK 都会被拦下，需要重新登记。`approval_chain.py verify --run-id <ID>` 可随时查看复核结果。说明与历史审批登记见 `reviews/approvals/README.md`。
> 审计提示：`approver` 仍是人工输入的字符串，不是独立身份证明；审批记录文件 `reviews/approvals/` 入库可追溯，运行态 `.agent/runs/` 仍只在本机。历史批准（HDR 批次）没有哈希绑定，标为 legacy / unverifiable，不补造。

---

## 6. 故障排查（真实存在）

| 现象 | 原因 | 修复 |
|---|---|---|
| `[registry]` FAIL，提示 N 份文档缺失 | 新增/改动 md 后未重建注册表 | `py -3 tools/build_document_registry.py` |
| `check_chapter_arc.py` 报「找不到文件」 | PowerShell 不展开通配符 | 用 `(Get-ChildItem "...").FullName` 内联展开（见 §2.5） |
| 文章里改了内容，网站没变 | 没重建 `content.js` | `py -3 tools/build_site.py` |
| 手改 `web/content.js` 后下次构建被覆盖 | 它是生成物 | 改源 md/JSON，重建 |
| 运行态「消失」 | `.agent/runs/` 被 gitignore | 它只在本机；需要留存就手动备份 JSON |
| PowerShell 中文乱码 | 控制台编码 | `[Console]::OutputEncoding=[Text.Encoding]::UTF8` |
| `py` 不是命令 | 未装 py launcher | 用 `python` 或 `python3` |
| `[publish] unregistered asset (default=deny)` 或 `BUILD FAILED: publish registry / disk mismatch` | 新文件没在发布清单登记 | 在 `tools/publish-allowlist.json` 逐个登记（`public` / `offline-read-only`（仅 archive/）/ `excluded-internal` + `reason`） |
| `[publish] source changed after build (sha256 mismatch)` | 登记后改了源文件未重建 | `py -3 tools/build_site.py` |
| `docs:build` VitePress 失败 | D10.6 权限拦截 | 用 `web/` 离线站；或手动放行 |
| `run_state new` 重复 run_id | 已存在 | 换 id，或 `show` 现有 run |
| `gate --pass` 报错 | 缺 `--approver` | 加 `--approver "姓名"` |
| `advance` 报「审批证据链未通过」 | 没有 `reviews/approvals/<ID>/` 记录，或批准后产物被改 / 新增了产物 | 人工重新登记：`approval_chain.py record ...`（先看 `verify --run-id <ID>` 列出的具体问题） |
| `advance` 报「…已由 … 通过，审批记录的 approver 必须一致」 | 登记审批用的人名与 `gate --pass` 用的不一致 | 用同一个人名登记 |
| KCR 卡在 REVIEWING | 未人工批准 | `--to APPROVED --approver` |
| `kcr_impact --claim-draft` 没有匹配结果 | 该参数只回显，不做匹配 | 用 `--claim-id` 或 `--source-id` |
| `report_feedback.py` 提示 empty | 还没有导出反馈 | 网站提交→localStorage→导出 JSON→粘贴到 `tools/feedback.json` |
| 新课程 validate FAIL | §10 要求 pilot ⊆ 主课程 | 先按知识文档形态产出，或申请多课程扩展 |

---

## 7. 日常提示词（可复用）

**A. 新批次开工**
```
按 Engine 的 P10 流程开一批新资料：<主题>。
先建 reviews/<batch>/intake-manifest.md，做查重与范围边界；用 run_state new 建 run 并声明 write_path。
新断言一律 open/low。每一步报告：产物路径 + 命令 + 退出码。
```

**B. 写一篇教材**
```
以 L01 Gold Standard + lesson-quality-standard 十维度写 L<xx>《<标题>》。
frontmatter 与 tools/course.json 逐字一致；新断言登记 open/low；桥接前后课；
完成后跑 build/validate/arc，并给我 G2 材料（不要自评）。
```

**C. 修一节内容**
```
只改 <文件> 的 <范围>。先给我 diff 方案与影响面（哪些断言/课程/quiz/术语会变），
我批准后再改。改完跑 review_gate 与 validate，并列出受影响的 used_by_lessons。
```

**D. 变更影响**
```
用 kcr_impact 分析 <claim-id 或 source-id> 的下游影响，列出 lesson/quiz/course/website，
生成 change-proposal JSON 并过 --stage2 校验。不要改任何状态。
```

**E. 中断恢复**
```
读 .agent/runs/<RUN-ID>.json，报告 phase/status/resume_point/write_paths/artifacts，
对照磁盘检查 artifact hash 是否仍一致，然后只做 resume_point 的下一步。
```

**F. 发布前检查**
```
跑全门禁：build_site / validate_site / arc / publish_boundary / review_gate / kcr selftest / runstate selftest。
汇总：docs/lessons/cards/KB、12 checks、claims 分布、失败项。
然后列出本次改动文件与我需要批准的事项（G3/commit/push）。
```

---

## 8. 当前已知限制（审计实测，2026-11-23）

1. **无资料导入工具**：INTAKE 靠人工清单；查重靠 `rg`。
2. **单课程工具链**：validate §10 限制独立课程；多课程扩展未批准。
3. **只有 5/19 课有 quiz**；7 个实验；无自动判分与学习分析。
4. **反馈闭环为空**：`tools/feedback.json` entries=0，尚无真实反馈。
5. **站点仅本地**：在线发布受 D02 未授权；GitHub Pages/Actions 未配置。
6. **学习站混入内部文档**：`content.js` 当前包含 `DECISIONS.md`、`CHANGELOG.md`、`WORKFLOW_STATE.md`、`G2-审核材料-P6.md`、`教材质量诊断.md` 等（审计 P1-4）。
7. **artifact hash 会过期**：run 记录的是登记时 hash；18 条中 7 条与现状不符（审读修复后未重登记）。
8. **人工门身份不可独立验证**：approver 是字符串；无签名/独立审批文件。
9. **README 数字过期**：仍写 26 篇/124 术语/19 课/31 断言/16 来源（实际 83 docs/129/20/84/43）。
10. **两套站点**：`web/` 主用；`site-vitepress/` 构建受阻。
11. **具身课程刚起步**：`RUN-2026-11-23-embodied-batch1` 在 RESEARCH，尚无教材。
12. **开发者文档会进学习者 bundle**：本文件位于 `docs/`，下一次 `build_site.py` 会把它计入（83→84 篇）。若不想让使用指南出现在学习站，需在 `tools/publish_boundary.py` 排除 `docs/`（审计 P1-4 的一部分，属代码改动，需批准）。

---

**最后验证**：2026-11-23，Engine `79c3fe8`（工作树 10 个未提交：D21 笔误修正 + embodied INTAKE）。
**最近更新**：2026-11-23。