---
doc_id: PROG-HANDOFF-20261119
type: handoff
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# AI Knowledge Program · 跨项目交接文档（2026-11-19）

> **自包含交接**：接手的 AI 只读本文档 + 所列权威文件即可继续全部工作，无需原会话上下文。
> 产生者：qwenwork（绑定 `AI-Knowledge\` 的会话）。交接范围：Program 统筹层收尾、命名迁移收尾、Engine 主线 P7.2→P10、冻结项目维护边界。
> **最高原则：减少复杂度、减少重复建设、减少当前任务数量，优先完成已有产品。任何时刻只有一个主动开发项目 = AI Knowledge-to-Learning Engine。**

---

## 0. 接手后先做什么（读取顺序）

1. 本文档 → `ai-knowledge-program/PROGRAM.md`（目标/边界/命名）→ `NOW.md`（当前状态）→ `ROADMAP.md` → `PARKING-LOT.md` → `PROGRAM-MANAGER.md`（工作规则，必须遵守）。
2. Engine：`ai-knowledge-to-learning-engine/.agent/README.md` → `WORKFLOW_STATE.md` → `DECISIONS.md`（D01–D19）→ `reviews/REVIEW_STATUS.md` / `reviews/decision-kit/README.md`（7/7 已决）。
3. 两仓 `git status` 实测，核对 §8 的未提交清单；发现清单外的未知改动 = 漂移，**先登记报告，不静默修复、不覆盖、不顺手提交**。
4. 按 §3 任务顺序推进。能安全做的直接做；高影响操作（§6）集中列给用户批准，不反复追问。

## 1. 工作区布局与命名（2026-11-19 实测核实）

```
C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\          ← 伞目录（AI Knowledge Workspace，非 git）
├── ai-knowledge-program\                             ← 统筹层（本地 git，无远程）
├── ai-knowledge-to-learning-engine\                  ← Engine（原 Render_Notes，唯一活跃线）
├── matt-pocock-skills-zh-cn\                         ← Skills 来源库（原 mattpocock-skills-zh-CN-custom）
├── agent-workspace-governance\                       ← 冻结 MVP（本地 git dec60ba，25 tests）
└── github-project-radar\                             ← 冻结 MVP（本地 git 942530b，38 tests）
```

**命名体系（正式名与仓库名分离，已固定）**：
| 正式名称 | 仓库/目录名 | GitHub | 本地目录 |
|---|---|---|---|
| AI Knowledge Program | AI-Knowledge-Program | 无远程 | `ai-knowledge-program`（大小写改名为可选遗留项） |
| AI Knowledge-to-Learning Engine | ai-knowledge-to-learning-engine | ✅ 已改名 | ✅ 已改名 |
| Matt Pocock Skills 中文定制发行版 | matt-pocock-skills-zh-cn | ✅ 已改名 | ✅ 已改名 |

**GitHub 改名已核实（2026-11-19 git ls-remote 实测）**：
- `https://github.com/Vin535LFJ/ai-knowledge-to-learning-engine` HEAD = `e848d2801ec9940e154b9bf40bc26198a5d197ba`（= 本地 e848d28）
- `https://github.com/Vin535LFJ/matt-pocock-skills-zh-cn` HEAD = `e1936f23e6e149c581124cc218e79860c07108ef`（= 本地 e1936f2）

**⚠️ 当前过渡态（接手时的第一个任务就是消除它）**：本地目录已是新名、GitHub 已是新名，但**两仓 git remote 仍指旧 URL**，文档/配置中的仓库 URL 引用尚未批量更新。旧 URL 目前靠 GitHub 重定向兜底，不可长期依赖。

## 2. 各项目当前进度（实测快照）

| 项目 | 状态 | 进度 | 阻塞 |
|---|---|---|---|
| Engine | **Active** | P0–P6、B1–B5、V3-Loop1/2、P7.1 完成；**decision-kit 七项裁决全闭合（D17/D18/D19）**；P8 仅预研（kcr_impact.py 只读工具 + publish allowlist）；P9 仅设计稿；P10 未启动 | 无裁决阻塞；**17 文件未提交**（待用户授权）；G2 评分表待人工 |
| Skills 库 | Completed（维护态） | main @ e1936f2 = origin，37 技能 + 4 处上游回填，干净 | 改名引用更新（T1） |
| Program 办公室 | Active（薄管理层） | 四文件 + PM 规范 + 迁移方案已建立；本轮重组**未提交** | commit 授权 |
| Governance | **Deferred** | MVP 冻结（25 tests OK） | 解冻条件未满足 |
| Radar | **Deferred** | MVP 冻结（38 tests OK，离线 fixture） | 解冻条件未满足 |

**Engine 门禁真值（D19 后复跑）**：build **69 docs** / 17 sections / 124 terms / 19 lessons / 7 labs / 504 cards；validate **11 checks / 0 FAIL / 0 WARN**；arc **5/5**；publish boundary **11/11**；review_gate **37 claims（18 verified / 12 open / 7 conditional）误标 0**。

**裁决结果（D17–D19，权威记录在 Engine DECISIONS.md）**：
- B4=B：L01《为什么视频不是 RGB》= Gold Standard 样板；minor 修订已执行（§4.2 记号精确化 + V13 表述三处同步修正）。
- B15=A：研究任务 C1–C7 **全部立项**入队（执行按 P8 节奏；建议 C2/C3/C6 优先）。
- V13/V14=A：升级 verified/high（V14 保留两条平台差异 conditions）。
- B10=A：V17–V20 确认登记 open/low，升级另裁。B11=A：L06↔P02 保留挂载（P02 仍 open）。B12=A：**stash@{0} 原样保留，绝不 pop/drop/apply**（本轮提交稳定后由用户重议）。

## 3. 任务清单（按此顺序推进）

### T1 · 命名迁移收尾（已获用户批准，可直接执行；建议最先做，短窗口一次性完成）

完整方案与影响清单：`ai-knowledge-program/plans/2026-11-19-rename-audit-and-migration.md`（审计真值，含逐文件行号）。要点：

**T1.1 更新 remote（两条命令；Skills 的 upstream-en/zh 绝不动）**
```
git -C "C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine" remote set-url origin https://github.com/Vin535LFJ/ai-knowledge-to-learning-engine.git
git -C "C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\matt-pocock-skills-zh-cn" remote set-url origin https://github.com/Vin535LFJ/matt-pocock-skills-zh-cn.git
```
验证：`git fetch` + `git ls-remote origin HEAD` 与 §1 哈希一致。

**T1.2 Engine 引用更新（范围含品牌文案，用户 Q2 已定）**
必改（功能依赖）：
- `tools/build_site.py:63` `REPO_URL` → 新 URL（改后**必须重建 content.js**，否则前端 GitHub 按钮仍指旧名）
- `site-vitepress/.vitepress/config.mjs:17` socialLinks GitHub URL
- `web/index.html:73` repoLink fallback href
- `PROJECT_CURRENT_STATE.md:16` origin URL
应改（活跃文档/品牌）：README 标题与描述（用 PROGRAM.md §8 标准英文描述）、`.agent/README.md:14`、五个适配入口标题（CLAUDE.md/AGENTS.md/.cursor/.github/.gemini）、两个 Skill 文档中的仓库名、`tools/course.json:3` title、`evidence/source-registry.json` 5 处来源 title、`web/assets/app.js` 面包屑/标题品牌文字（约 16 处）、index.html meta/title、site-vitepress/README。
**绝不能动**：
- `window.RENDER_NOTES` 全局变量名 = 4 文件契约（app.js:4 / build_site.py:510 / validate_site.py:251-252 / test_publish_boundary.py:81），改了 validate 直接 FAIL。
- 历史层：DECISIONS.md / CHANGELOG.md 历史条目 / `.agent/decisions|changes|plans` / reviews 历史审计材料 / 两份旧方案文档（D13 保护）/ archive / `.workbuddy-ai/memory`。
- 含旧名的**文件名**（`Render_Notes_2.0_双线规划.md`、`Render_Notes：...md`、`.cursor/rules/render-notes.mdc`）不改，指向它们的链接继续有效。
- npm 包名 `render-notes-site-vitepress`（private，不改不坏，可不动）。
改后重建：`py -3 tools/build_site.py`（+ 如 frontmatter 有变则 `py -3 tools/build_document_registry.py`）。

**T1.3 Skills 库引用更新（⚠️ 最高纪律：锚定精确替换）**
- 只允许替换完整串 `Vin535LFJ/mattpocock-skills-zh-CN-custom` → `Vin535LFJ/matt-pocock-skills-zh-cn`（及本地目录名自述）。
- **禁止裸替换 `mattpocock-skills-zh-CN`**：它是上游 `vinvcn/mattpocock-skills-zh-CN`（29 处）的前缀子串；另有 `mattpocock/skills` 71 处上游链接与 4 处"本地回填"注释，全部不动。
必改/应改清单：`.claude-plugin/plugin.json:10` repository；`AGENTS.md:23`（安装命令指向规则）；`README.md` 7 处（:34/:74 npx skills add、:42/:93 plugin marketplace add、:100 claude plugin marketplace add、:108/:111 skills.sh URL）；`AGENT-COMPATIBILITY.md` 5 处（:156/:160/:161/:170/:209）；`UPSTREAM.md`（:9 目录自述、:32 origin HTTPS、:38 SSH、:68 分发合规段）；README 标题/描述用正式名（**必须标注中文适配定制发行版，不得冒充上游官方**）。
验证：`node scripts/check-translation.mjs` 通过；`grep -rl "本地回填" skills/` 恰 4 个文件；`claude plugin validate . --strict`（若本机有 claude CLI，否则如实标注待验）。SYNC.md/BACKPORTS.md/marketplace.json/脚本均无需改。

**T1.4 Program 办公室同步**：PROGRAM.md §4/§8（GitHub 待同步注记→已完成）、NOW.md、plans 方案状态、PARKING-LOT 迁移行、handoffs 索引。`references/gpt-architecture-guidance.txt` 是用户原件**只读不改**；decisions/ 历史与 archive/ 不改。冻结仓（governance/radar）正文中的 3 处旧 URL **冻结期不动**（重定向兜底，解冻时更新）。

**T1.5 外部消费者跟进（用户 Q4 已授权）**
- `C:\Users\Giant\Desktop\GITCODE\OmniWorld-Engine\AGENTS.md:74` 安装命令 → 新 slug。
- 重装技能（**必须 pin skills@1.7.1**，1.7.2 在 Node 20 崩溃）：
  `npx -y skills@1.7.1 add Vin535LFJ/matt-pocock-skills-zh-cn -s '*' -a codex --copy -y`（在 OmniWorld-Engine 目录）
- 验证 `OmniWorld-Engine\skills-lock.json` 37 条 source = 新 slug。
- 用户级 `.zcode` 活跃记忆（omniworld 项目的 `mattpocock-skills-zh-custom-repo.md`、`agent-skills-deployment.md`）**追加"已改名"更正条目**，不改写历史。
- `E:\AI-Tools\skills-zh-full`（lock 指 vinvcn 上游）**不动不重装**；`E:\AI-Tools\_mp_skills_verify`（lock 指向已不存在的 E 盘旧路径，改名前就已断）按需重建或废弃，不阻塞。

**T1.6 验证与留痕**：两仓 fetch/ls-remote 正常、历史提交可访问；Engine 全量门禁（§5 命令）；Skills check-translation；活跃层 grep 旧 slug 残留清零（历史层除外）；实测数字写入 NOW.md + Engine CHANGELOG；更新 plans 方案状态为 completed。
**回滚**：GitHub 改回旧名 / 目录 Move-Item 移回 / 引用更新单笔 git revert / content.js 重建。详见方案 §5。
**节奏纪律**：T1 一次性短窗口完成，**不与 Engine 内容开发交织**；commit 需用户授权（§6）。

### T2 · Engine 主线：P7.2 逐篇深化（当前主任务，T1 后立即开始）

- **第一篇 = L02《时间戳与同步》**（pilot 路线 L01→L02→L06→L11→L13；P7.1 blocker 已修复：V15/V16 open 登记 + 正文重写 + quiz）。
- 做法：以 **Gold Standard L01**（`courses/video-rendering-journey/lessons/L01-为什么视频不是-RGB.md`）+ **质量规范**（`.agent/skills/research-to-learning/references/lesson-quality-standard.md`，十维度）为基准，把 L02 深化到标杆质量。**一次一篇，不批量生成**；新断言默认 open/low，不自升 verified；正文结论可追溯到主文档锚点或断言。
- 每篇结束：跑门禁（§5）→ 实测数字记入 CHANGELOG/WORKFLOW_STATE → 留 G2 审核材料 → 更新 NOW.md。
- 后续篇目按先修图推进（L06→L11→L13→其余）；同一术语多章出现按"直观→原理→数学→架构→实践"递进，不因重复术语判重复。
- 参考：`NEXT_PHASE_PLAN.md` P7 节（注意其"待用户拍板"段已过时——B1/B2/B3/B5/B6 已在 D12 裁决，B4 在 D17）。

### T3 · P8：Research-to-Learning 生产化（P7.2 推进后按序）

- KCR 最小闭环：设计在 `reviews/KNOWLEDGE_CHANGE_REVIEW.md`，只读影响分析工具 `tools/kcr_impact.py` 已起步 → schema + 工具集成；文档注册表一致性门禁接入 validate。
- 输入合同（source inbox）：七类输入（MD/PDF/网页/论文/官方文档/GitHub 仓库/已有研究报告）；先查已有知识再研究。
- **研究队列 C1–C7 已全部立项（B15=A）**：C2 SurfaceTexture 官方 API / C3 stride 对齐基数平台差异 / C6 来源 locator 精度 优先（支撑 V17–V20、P02 升级与 G1 收敛）；研究只读、不自动改结论；升级逐条人工裁决。
- 增量资料处理：同源判断→变化对比→受影响断言/章节，全程变更记录，不重生成全库。

### T4 · P9：轻量编排（P8 后）

- 设计稿 `reviews/P9-orchestrator-design.md`；JSON 状态文件记录 INTAKE→…→FEEDBACK 各阶段输入/输出/完成条件；支持重试、断点恢复、防重复写入、人工暂停。**扩展现有 tools/，不上分布式框架**。验收：一门 pilot 课证明可断点续跑。

### T5 · P10：端到端验收（= Engine 主目标达成）

- **一批全新真实资料**完整走通：导入→查重→研究→证据→建模→路线→教材→实践→人工审核→网站→留痕。
- 完成标准：工作流可重复；中间产物有数据契约；各阶段有质量检查；人工审批点明确；网站正常呈现（可用/清晰/基本美观）；知识变更可影响分析（KCR）；失败可定位恢复。
- **不要求 19 课全部写完**。VitePress 本地构建已授权（D12.6），但 `docs:build` 清理自身 .temp 会触发删除权限请求——需用户放行，不绕过、不伪造成功。**GitHub Pages 在线发布未授权（D02），不做**。

### T6 · 版本化收口（需用户授权，贯穿进行）

- Engine 17 文件 + Program 办公室本轮改动均未提交（清单 §8）。**用户按文件逐个提交，从不一次性 git add**——AI 可建议分组与提交信息，执行提交必须用户明确授权；push 另行授权。
- 建议分组：① Engine 裁决执行（D17–D19 相关 17 文件，含重建的 content.js）；② T1 迁移引用更新（两仓各一笔）；③ Program 办公室重组。中文提交信息写入临时文件后 `git commit -F <file>`（PowerShell 内联中文会被转义破坏）。

### 冻结项目（不开发，只维护边界）

- **Governance**：唯一允许动作 = 把 Engine 协作中真实发生的痛点追加到其需求清单。解冻 = Engine P10 通过 **且** ≥第二个真实项目需要复用 + 痛点有真实案例；反向接入先 ADR。不建远程（PD-Q3 另行授权）。
- **Radar**：不申请 PAT、不采集、不建 Actions。解冻 = Engine P8 输入合同就绪 **且** 项目追踪成为持续明确负担。查热点直接用 web 搜索。
- **Learning Experience Design**：Skill 骨架冻结在 `.agent/skills/learning-experience-design/`；解冻四条件 = P7 质量稳定 + P8 闭环 + P9 一次完整 run + 发布边界明确。P1 期间网站只保证基本可用性，不提前建设计体系。

## 4. Skills 库维护纪律（独立来源仓库）

- 不并入 Engine、不改造成 Governance、不重建第二套发行机制。
- 上游同步走 `SYNC.md`/`BACKPORTS.md` 既有纪律；upstream-en = mattpocock/skills，upstream-zh = vinvcn/mattpocock-skills-zh-CN，**两个上游 remote 与全部上游引用绝不动**。
- Engine 引用通用 Skills，但领域专属 Skill（research-to-learning / learning-experience-design）留在 Engine `.agent/skills/`。

## 5. Engine 门禁命令（本机实测可用）

```powershell
# 工作目录 = C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine
py -3 tools/build_site.py          # 重建 web/content.js（生成物，禁手改）
py -3 tools/validate_site.py       # 目标 12 checks / 0 FAIL / 0 WARN（2026-11-20 片三起 11→12）
$files = (Get-ChildItem "courses/video-rendering-journey/lessons/*.md").FullName
py -3 .workbuddy-ai/skills/research-to-learning/scripts/check_chapter_arc.py @files   # 必须显式展开，PowerShell 不展开通配符
py -3 tools/review_gate.py         # 只读；G1/G2/G3 结论 AI 不填
py -3 tools/test_publish_boundary.py   # 11 tests
py -3 tools/kcr/selftest_impact.py     # 16 tests（P8 片一+片二）
```
- **Python 一律 `py -3`**（`python` 解析到 cygwin stub 不可用）。
- **validate 第 12 节 [registry] FAIL 时**：规定修复动作 = `py -3 tools/build_document_registry.py` 重建注册表（生成物，禁手改），再复跑 validate。
- 改前端后另做离线站浏览器 QA（file:// 与 http://localhost:8765 两路）。
- 任何改动后重跑门禁，把**实测数字/哈希**记入治理文档（真实留痕，不估算冒充）。

## 6. 纪律红线（违反 = 事故）

**必须用户明确批准才做**：git commit/push、远程仓库创建、部署、删除重要文件、大规模移动目录、改公共接口、不可逆迁移、新建独立项目、大规模重构、改变核心定位、断言升级（open→verified）、课程路线调整。未回复不视为同意。
**禁区**：`.workbuddy-ai/memory/**`、`archive/**`、`web/vendor/**`、`web/index.html` 的结构性改动（T1 的 fallback href 一行除外）、两份旧方案文档、**stash@{0}（B12 保留裁决）**、claim 状态（未经裁决）、`.agent/**` 结构（变更走 DECISIONS + KCR）、生成物手改（content.js/registry/VitePress 树只能重建）。
**协作**：单写者；接手先查 git status；外来产物不触碰；漂移先登记。Program 只存项目级状态与指针，不复制 Engine 技术文档。
**防膨胀**：新想法先过 PARKING-LOT 四问；不建 Dashboard/数据库/调度平台/中央管理平台/通用 Orchestrator；不在同一次执行里既改名又迁移又重构。
**环境怪癖**：PowerShell 内联 python/`$`/引号会被转义破坏 → 写临时 .py/.ps1 文件执行；活动会话绑定的目录被句柄占用时 Move-Item 报 busy（失败是原子的，换绑定父目录的会话做）；工作区外文件无法用 file_present_files 呈现。

## 7. 待人工事项（集中列给用户，不反复追问）

1. **commit/push 授权**：Engine 17 文件 + Program 办公室改动（§8）；建议分组见 T6。
2. **G2 评分表**：`courses/video-rendering-journey/review-report.md`（25/25/20/20/10，总分≥85 且前两项各≥80%）——AI 不填；填完 G2 才正式通过。G3 发布审核同理。
3. **B12 重议**：本轮提交稳定后，验证 stash 里 20 处链接修正是否仍需要，用户决定 pop/drop。
4. **V17–V20 / P02 升级**：待 C2/C3/C6 等研究核验后逐条裁决。
5. 可选：Program 目录大小写改名 `ai-knowledge-program → AI-Knowledge-Program`（两步 Move-Item 经临时名）；PD-Q3 冻结仓远程创建（解冻后再议）。

## 8. 证据附录（2026-11-19 实测）

**Engine 未提交（17 文件，HEAD=e848d28）**：
`01-基础理论/音视频基础理论.md`、`CHANGELOG.md`、`DECISIONS.md`、`PROJECT_CURRENT_STATE.md`、`WORKFLOW_STATE.md`、`courses/video-rendering-journey/lessons/L01-为什么视频不是-RGB.md`、`evidence/claim-ledger.json`、`reviews/REVIEW_STATUS.md`、`reviews/decision-kit/{B4,B10,B11,B12,B15,V13,V14,README}.md`（8 文件）、`web/content.js`（重建生成物）。

**Program 办公室未提交（HEAD=87f9edf）**：新增 PROGRAM/NOW/ROADMAP/PARKING-LOT/PROGRAM-MANAGER + archive/ + plans/；删除（=移入 archive/）README/PROGRAM_PLAN/PROJECT_INDEX/STATUS_BOARD/SUPERVISION_RULES；修改 decisions/{PD-002,PENDING_DECISIONS,README} + handoffs/README。

**远端哈希**：Engine `e848d2801ec9940e154b9bf40bc26198a5d197ba`；Skills `e1936f23e6e149c581124cc218e79860c07108ef`（ls-remote 新 URL 实测）。
**门禁**：见 §2 真值。**审计全文**：`plans/2026-11-19-rename-audit-and-migration.md`（两仓逐文件引用清单 + 替换雷区 + 回滚）。
**关键历史决策**：D12（B1/B2/B3/B5/B6 + G1 核验）、D13（KCR 机制）、D14/D15（.agent 治理基座）、D16（PD-003 裁剪 + 收口）、D17–D19（decision-kit 七项）。