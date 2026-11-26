# Governance × Engine 治理机制重叠度审计报告

- 审计日期：2026-11-26
- 审计对象：
  - `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\agent-workspace-governance`（下称 Kit，6 笔提交本地 git 仓）
  - `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\ai-knowledge-to-learning-engine`（下称 Engine）
- 审计方式：**只读**。未修改两仓任何文件。测试在 tempfile 中运行（tests/test_governance.py:2 声明"全部使用 tempfile"）；对 Engine 直接执行的 `doctor`/`validate` 均为只读代码路径（doctor 用 `_safe_read_json`，cli/governance.py:119-130、1005-1065；validate 只读扫描+读注册表，cli/governance.py:484-526），不写任何文件。

---

## 1. Governance（Kit）实际实现的功能盘点

以 `cli/governance.py`（1289 行，纯标准库，不联网、不执行 git，见文件头 L2-6）为准。
`git log --oneline` 实测 6 笔提交：`7d9a187 / d425f19 / effc774 / 925014d / 99e0d83 / ac62da6`。

### 1.1 各命令实际行为（代码证据）

| 命令 | 实现函数（行号） | 实际做什么 |
|---|---|---|
| `init` | `init_project` L359-420 | 幂等创建 `.governance/` 下 5 个 JSON（config + document/task/agent/adr 四个注册表骨架，L402-412）；调 `ensure_agents_pointer`（L414）建/追加 AGENTS.md 指针。已存在的文件一律不动（L372、L410 的 `if not os.path.exists`）。 |
| `inventory` / `index`（别名，L1121-1122、L1172-1177） | `inventory_docs` L450-477 | `scan_markdown_docs`（L252-273）扫描 md（跳过点目录、`.governance`、IGNORE_DIRS：node_modules/vendor/dist/build/out/target/__pycache__/.temp/.venv/venv，L246-249），手写 YAML 子集解析 frontmatter（`parse_frontmatter` L180-231），按 `document_id` upsert 进注册表。**登记时不校验 type**：缺 type 记 `"unknown"`（L432）。 |
| `validate` | `validate` L484-526 | 对每篇扫描到的 md 检查 frontmatter 存在 + 6 个必填字段（REQUIRED_FM：doc_id/type/status/owner/created/updated，L35）；对注册表条目查 7 个必填字段 + `replaces/superseded_by/related_adr` 引用完整性（L517-520）。**不查 type 枚举**。 |
| `doctor` | `doctor` L1005-1065 | 只读诊断：5 个 JSON 可解析性（L1018-1026）、注册表必填字段（L1035-1039）、type ∈ 13 类枚举 DOCUMENT_TYPES（L42-45、L1040-1043）、单写者冲突（`detect_single_writer_conflicts` L937-960）、依赖环（`detect_dependency_cycles` L963-998，三色 DFS）。有错 exit 1（L1199）。 |
| `status` | `task_status` L533-560 | 读 task-registry，列任务 + 待人工审批清单（`human_approval_required` 且未完成，L537-540）。纯展示。 |
| `map` | `agent_map` L567-597 | 读 agent-registry，聚合 Agent/Skill/MCP/Tool 映射，含 `runtime_verification_status`（默认 unverified，L587）。纯展示。 |
| `handoff` | `generate_handoff` L604-634 | 按 task_id 查任务，用 `templates/handoff.md` 填 `{{占位符}}`（`_fill_template` L234-243），写 `.governance/handoffs/handoff-<task>.md`。任务不存在返回 None（L608-609）。 |
| `adr create/list/check` | `adr_create` L641-692 / `adr_list` L695-698 / `adr_check` L701-714 | create：自动编号 ADR-0001（L649-655），初始 `proposed`、`human_approved: false`（L661、L675），写索引 + `docs/adr/ADR-XXXX.md`。check：状态合法性、已决定状态（accepted/deprecated/superseded）必须 `human_approved`（L712-713，"ADR 不得自动 accepted"）。 |
| `archive-check` | `archive_check` L728-753 | superseded 且超 180 天未更新的文档 + completed 任务 → 归档候选清单。只报告不动文件。 |
| `audit` | `audit` L760-848 | 五类检查：重复 document_id / 重复 source_of_truth（L795-808）、孤儿（无出边无入边，L789-792）、冲突（L3 却 active，L811-816；不同 owner 写同一 write_path，L818-825）、过期引用（L828-840）、未登记文档（L768-771）。 |

**库级纯函数（未暴露为 CLI 命令）**：`claim_task`（L879-918，单写者认领 + sha1 claim_token，纯函数不改入参）、`check_frontier`（L921-934，依赖是否全部 completed/approved）、`_dependency_ids`（L855-876）。`main()`（L1105-1285）中没有 claim/frontier 子命令——它们只能被 import 调用。

**未实现（文档设计 ≠ 实现）**：
- CLI **从不加载 `schemas/*.json` 做运行时校验**——governance.py 全文无 schema 读取；schema 仅被测试对照（test_governance.py:299-322、573-582）。
- 无编排器、无 KCR、无审核门、无审批证据链（USER-GUIDE.md:298-299 自认："不能替代 Engine 的 run_state……它是文档/任务元数据层，不是编排器"）。
- `docs/specification.md` 等描述的其余能力以 USER-GUIDE §17 已知缺陷为准（如 L314："AGENT_RULES.md:75 声称 doctor 检查 task claim，实测不检查"）。

### 1.2 测试覆盖（实测）

命令：`py -3 -m unittest discover -s tests -v`（workdir=Kit）
输出末尾：**`Ran 41 tests in 0.297s` / `OK`**（有若干 ResourceWarning，不影响结果）。

4 个测试类（tests/test_governance.py）：
- `GovernaceTests`（L34-259，11 个）：init 幂等、frontmatter 解析、登记、validate 缺字段、status、map、handoff、adr create/list、archive-check、audit 孤儿、render-notes 迁移映射。
- `GovernanceIncrementTests`（L262-497，14 个）：13 类枚举与 schema 一致、task schema claim 字段可选、doctor 6 种场景（干净/缺 owner/非法 type/单写者/依赖环/坏 JSON）、index 别名、claim_task 成功+冲突+不存在、check_frontier、单写者纯函数、依赖环纯函数。
- `ExampleProjectTests`（L500-588，7 个）：basic-project 示例自洽（doctor exit 0、type 与 frontmatter 一致、inventory 重跑可复现注册表、schema 接受 null、IGNORE_DIRS 生效）。
- `InitExistingAgentsTests`（L591-772，9 个）：见 §4。

**覆盖缺口**（如实记录）：
- `adr_check`（人工批准强制，L701-714）**无任何测试**——测试只测 create/list（L200-209）。
- `audit` 五类检查只测了孤儿一类（L234-239）；冗余/冲突/过期引用/未登记无测试。
- `validate` 的注册表引用完整性分支（L517-520）无测试。
- `claim_task`/`check_frontier` 有测试但无 CLI 集成（本身就不是命令）。

---

## 2. 对照 Engine 已有治理：逐项三分类

Engine 治理基线（代码证据）：
- `.agent/constitution/AGENT_RULES.md`（type: standard, status: approved, owner: human，L1-10）：五条写所有权规则——单写者（L17-18）、默认只读+任务授权（L20-21）、worktree（L23-24）、生成物非源（L26-37）、交接模板 `.agent/templates/agent-handoff.md`（L39-40）。
- `.agent/constitution/DOCUMENTATION_POLICY.md`：14 类小写 type 枚举（L50）、L1-L3 分级（L32-36）、状态机（L40）、**缺 frontmatter 存量文档记 unregistered、"渐进补齐，不批量回填"**（L43）、frontmatter 为事实源/注册表为生成物（L62-67）、归档保留策略（L69-74）。
- `tools/build_document_registry.py`：VALID_TYPES 14 类（L24-26）、无 frontmatter 时启发式 `derive_type`（L53-84）+ `type_source: heuristic` 标记（L125）、`derive_level`（L87-97）、`collect_entries` 纯函数与校验器共用口径（L105-138）。实测注册表 212 条：knowledge 90 / review-material 56 / skill 28 / …；status：unregistered 79 / draft 72 / active 53 / …；type_source：heuristic 107 / frontmatter 105。
- `tools/validate_site.py` 第 12 节（L634-662）：只读比对注册表 ↔ 磁盘 frontmatter，逐字段漂移即 FAIL，修复动作=重建注册表；另有第 13 节发布边界等（全文 807 行、13+ 节门禁）。
- `DECISIONS.md`：D01-D14 历史裁决索引（无 frontmatter，属存量）；权威 ADR 在 `.agent/decisions/0001-adopt-documentation-governance.md`（doc_id: ADR-0001, type: adr, status: active）。
- `tools/run_state.py`（628 行）：10 阶段状态机 + 6 条程序强制不变量（L11-23）：人工门不可绕过（gate --pass 必须 approver）、AI 不预填裁决、未批准不发布、**单写者 `_check_write_conflict`（L142-152，new/start/resume 均强制，L213/235/260）**、artifact sha256 留痕、批准绑定文件版本；每次写盘前过 `kcr/validate_kcr.py` schema+semantic 校验（L98-102），临时文件+os.replace 原子写（L105-113）。
- `tools/approval_chain.py`（264 行）：批准时冻结产物 SHA256 → `reviews/approvals/<run_id>/<gate>-NN.json` 只增不改（L6-9）；发布前 verify 重算哈希比对（L10-12）；历史批准如实报 legacy/unverifiable（L14-15）。
- `tools/kcr/`：`validate_kcr.py`（schema+semantic 双层校验，L68/L99）+ 5 个 schema（run-state / approval-record / change-proposal / impact-report / review-decision）+ 3 个 selftest（断言数实测：selftest_runstate 104、selftest_approval 72、selftest_impact 71）；另 `tools/test_publish_boundary.py` 139 处断言。
- `reviews/` 约定：`DECISION_REQUIRED.md` 统一人工裁决表，明文"**未回复的项保持待审核，不视为默认同意**……AI 不替用户选择、不预填裁决"（文件头 L3-4）；G1/G2 评审材料、approvals/、decision-kit/。

### 逐项判定

| # | Kit 能力 | 判定 | 证据与理由 |
|---|---|---|---|
| 1 | init：`.governance/` 状态目录 + 注册表骨架 | **Engine 已覆盖** | Engine 用 `.agent/indexes/document-registry.json` + schema（build_document_registry.py:16）；运行态在 `.agent/runs/`（run_state.py:51）。Kit 的 config.json 生命周期枚举（governance.py:382-388）与 DOCUMENTATION_POLICY L40 状态机同源但无消费方。 |
| 2 | init：AGENTS.md 指针（ensure_agents_pointer） | **Engine 已覆盖**（自动化本身独有但无现实需求） | Engine 根 AGENTS.md 已是指针（doc_id: ADP-AGENTS，"只负责发现与跳转，不复制正文"），且 `.cursor/.github/.gemini` 适配入口齐备（AGENT_RULES L50-52）。指针已存在、人工维护，无需自动追加。函数本身质量高（见 §4）。 |
| 3 | inventory/index：扫描登记 | **Engine 已覆盖，且 Engine 更强** | build_document_registry.py 有启发式 type（L53-84）、type_source 溯源（L125）、level 推导（L87-97）、unregistered 如实标记（L126）；Kit 缺 frontmatter 一律 `unknown`（governance.py:432-434），信息量更低。 |
| 4 | validate：frontmatter 必填 + 引用完整性 | **Engine 已覆盖（策略不同）** | validate_site.py §12 用生成器同一口径查漂移（L645-658）；Engine 对存量缺 frontmatter 是**有意的渐进策略**（DOCUMENTATION_POLICY L43），Kit 把同一现象当 804 个硬错误（§3 实测），属口径冲突而非能力增量。 |
| 5 | doctor：JSON 可解析 + 必填字段 | **Engine 已覆盖** | run_state 每次写盘前 schema+semantic 校验、失败不落盘（run_state.py:98-113）——事前强制优于 Kit 的事后诊断。 |
| 6 | doctor：13 类 type 枚举 | **仅设计未证明（对 Engine 为负价值）** | 13 类 TitleCase 枚举（governance.py:42-45）与 Engine 14 类小写枚举**交集为空**（§3 实测）。对 Engine 逐条报错 183 项，全部是误报或口径冲突。 |
| 7 | 单写者冲突检测（detect_single_writer_conflicts / audit 写路径冲突） | **Engine 已覆盖，且 Engine 更强** | run_state._check_write_conflict（L142-152）在 new/start/resume 时**拒绝写入**（声明即持有，pending/running/paused/failed 均算，L17-18）；Kit 只对已写好的注册表做事后两两比对（governance.py:937-960）。 |
| 8 | claim_task（认领 + token） | **Engine 已覆盖** | run_state new 强制 owner_agent（L164）+ 写冲突检查；Kit 的 claim_token 无 CLI 入口、无持久化流程，仅库函数。 |
| 9 | check_frontier + detect_dependency_cycles | **Governance 独有且有真实价值** | run_state 只**记录** dependencies（L167、L182；run-state.schema.json:15），全文无依赖就绪检查、无环检测（rg "dependencies|frontier|cycle" 实测仅记录/传参行）。Kit 两个纯函数（L921-934、L963-998）有完整测试（test_governance.py:441-497，含自环、对象形式 frontier）。这是唯一填补 Engine 真实空白的能力。 |
| 10 | handoff 自动生成 | **Engine 已覆盖（模板层）；自动化仅设计未证明** | Engine 有 `.agent/templates/agent-handoff.md`（type: template, active）+ 规则五强制交接（AGENT_RULES L39-40）。Kit 的"从注册表生成"依赖 task-registry 有数据——Engine 副本实测 tasks=0（§3），自动化从未在真实项目产生过一份交接。 |
| 11 | adr create/list/check | **Engine 已覆盖，且 Engine 更强** | Engine：MADR 正文（.agent/decisions/0001-*.md）+ DECISIONS.md 索引 + ADR 纪律（DOCUMENTATION_POLICY L30）+ approval_chain 哈希绑定批准。Kit 的 `human_approved` 只是一个无测试的布尔字段（governance.py:712-714；tests 无 adr_check 用例），USER-GUIDE L313 自认"人工审批……没有 schema/存储字段"。 |
| 12 | audit：孤儿/冗余/冲突/过期引用/未登记 | **仅设计未证明**（部分与 Engine 重叠） | 未登记/过期引用 ≈ validate_site §12 漂移门禁；写冲突 ≈ run_state。孤儿/重复 source_of_truth 分析已实现（L789-808）但只有 1 个合成数据测试（test_governance.py:234-239）；Engine 注册表根本没有 related_documents/source_of_truth 字段，接上即"全部孤儿"，无真实价值证明。 |
| 13 | archive-check | **仅设计未证明** | Engine 有归档政策（DOCUMENTATION_POLICY §6、archive/ 只读禁区 AGENT_RULES L48）但无自动年龄检查；Kit 的 superseded+180 天启发式（L728-753）只有合成测试（test_governance.py:212-231），真实项目未跑过、无归档动作闭环。 |
| 14 | status / map（任务与 Agent 能力视图） | **仅设计未证明** | Engine 副本三个注册表实测全空：tasks=0 / agents=0 / adrs=0（§3；USER-GUIDE L312 自认）。Engine 的任务状态由 run_state show/list + WORKFLOW_STATE.md 承担。Agent 能力注册（unverified 标记）理念好但无任何真实登记数据。 |
| 15 | constitution/ 四文件 + templates/ + adapters/ | **Engine 已覆盖（同源泛化）** | 四文件与 Engine `.agent/constitution/` 同名同创建日期（2026-11-19）；git diff --no-index 显示是改写泛化版（AGENT_RULES：75 insertions/35 deletions，owner 从 human 改 governance-kit）。examples/render-notes/README.md 映射表自认"工具包的 constitution/ 与之一一对应"、"不实现编排器"。 |

小结：15 项能力中 **9 项 Engine 已覆盖（其中 5 项 Engine 实现更强）**、**1 项独有且有真实价值（#9 依赖前沿/环检测）**、**5 项仅设计未证明**。

---

## 3. 实测：Kit 对 Engine 的 validate/doctor 为什么失败

### 3.1 实测输出（只读执行，未写 Engine）

```
py -3 agent-workspace-governance\cli\governance.py doctor   --project ai-knowledge-to-learning-engine
→ doctor 只读诊断：检查 5 个 JSON 文件、183 个注册表文档条目。
→ 诊断发现问题：共 621 项，doctor 返回非零退出码。  exit=1

py -3 ...\governance.py validate --project ai-knowledge-to-learning-engine
→ 已校验 232 个文档，183 个注册表条目。
→ 校验失败：共 804 个问题。  exit=1
```

错误分解（对输出文件逐行统计）：
- doctor 621 = **438 条缺必填字段**（owner/created_at/updated_at）+ **183 条 type 枚举错误**；单写者冲突 0、依赖环 0（任务注册表为空）。
- 183 条 type 错误按值分布：`unknown` 146、`review-material` 31、`kcr` 2、`adapter` 2、`research-report` 1、`agent-plan` 1。
- validate 804 = **114 篇缺 frontmatter** + **690 条缺必填字段**；引用错误 0。

### 3.2 根因一：type 词表零交集（枚举不兼容）

Kit DOCUMENT_TYPES（governance.py:42-45，与 schemas/document.schema.json oneOf 一致，test_governance.py:299-313 验证）：
`ADR, Architecture, Audit, Glossary, Handoff, Plan, Runbook, Script, Session Note, Skill, Spec, Task, Workflow`（13 类，TitleCase）。

Engine frontmatter type 抽查（实测读取）：
- `.agent/constitution/AGENT_RULES.md` → `type: standard`
- `.agent/constitution/DOCUMENTATION_POLICY.md` → `type: standard`
- `.agent/decisions/0001-adopt-documentation-governance.md` → `type: adr`
- `.agent/decisions/adr-template.md` → `type: template`
- `.agent/skills/research-to-learning/SKILL.md` → `type: skill`
- `DECISIONS.md`、`WORKFLOW_STATE.md`、`01-基础理论/音视频基础理论.md`、`reviews/CURRENT_AUDIT.md`、`reviews/DECISION_REQUIRED.md` → **无 frontmatter**（Engine 政策允许的存量状态）。

Engine 注册表 212 条的 type 全集（实测 Counter）：`adapter, adr, agent-plan, change-proposal, data-config, kcr, knowledge, project-state, research-report, review-material, run-log, skill, standard, template`（14 类，小写 kebab-case，DOCUMENTATION_POLICY L50 定义）。

**程序化比对：两枚举交集 = 空集**（`types & et == set()` 实测）。连 `adr`≠`ADR`、`skill`≠`Skill` 都因大小写不匹配。即 Engine 一篇元数据完全合规的文档（如 ADR-0001），进 Kit 注册表后 doctor 也必报 type 错误。这不是"存量债务" alone，而是**词表设计不兼容**。

### 3.3 根因二：存量无 frontmatter 文档的口径冲突

Engine 侧 146/183（79%）登记为 `unknown` 的文档，在 Engine 自己的注册表里是 `status: unregistered` + 启发式 type（build_document_registry.py:124-126），这是 DOCUMENTATION_POLICY L43 明文批准的渐进策略（"渐进补齐，不批量回填"）。Kit 把同一事实当硬错误（validate L494-500；doctor L1035-1043），每篇报 3-4 项，累计 621/804。USER-GUIDE L289-290 也承认此为"存量债务"而非工具故障。

### 3.4 根因三：扫描边界不一致（Kit 扫进生成物、漏掉权威区）

- Kit `scan_markdown_docs` 跳过**所有点目录**（governance.py:261-263）→ Engine 元数据最规范的 `.agent/`（51 篇 md，实测）**全部不被扫描**；
- Kit IGNORE_DIRS（L246-249）不含 `site-vitepress`/`web` → 实测 232 篇扫描结果中 **site-vitepress 占 74 篇（32%）**，全是 VitePress 生成物，直接违反 Engine AGENT_RULES 规则四"生成物不是源文件"（L26-37）；
- Engine 生成器口径相反：EXCLUDED_PARTS 排除 `web/site-vitepress/node_modules/.workbuddy-ai/.zcode`、**包含** `.agent/reviews/archive`（build_document_registry.py:20-21）。
- 数字对照：Kit 扫 232 篇 vs Engine 注册表 212 条 vs Kit 在 Engine 遗留注册表 183 条——三套口径互不一致。

### 3.5 Engine 内的遗留物（审计发现，未处置）

- Engine 根下存在 `.governance/`（config.json `created_at: 2026-11-21`，描述"由 governance.py init 初始化"），对应 Kit 提交 99e0d83"真实项目适配实跑（ENGINE 183 docs）"。
- 其中 document-registry.json 183 条（146 unknown），**task/agent/adr 三个注册表全空**（实测 tasks=0/agents=0/adrs=0）。
- Engine 根 AGENTS.md **无** `governance-pointer` 标记（rg 实测 exit 1），与 USER-GUIDE L311"Engine AGENTS.md 尚未接入治理入口……在真实 Engine 上执行 init 需人工授权"的说法存在出入：`.governance/` 已在真实 Engine 落盘，指针却不在。该目录属双轨治理遗留物，**建议交人工裁决清理或保留**（本审计只读，未动）。

### 3.6 合理纳管边界建议（若将来仍要接入）

1. **只管治理元数据区**：`.agent/` + 根治理文档（DECISIONS/WORKFLOW_STATE 等），且只校验**已有 frontmatter** 的文档；知识正文（01-08/courses/archive）沿用 Engine 注册表的启发式+unregistered 口径，不纳入硬校验。
2. **排除生成物与宿主目录**：site-vitepress/web/node_modules/.workbuddy-ai（对齐 EXCLUDED_PARTS），并取消"跳过一切点目录"改为白名单包含 `.agent`。
3. **type 词表以 Engine 14 类为准**（或做显式映射表），否则 doctor 的枚举检查对 Engine 永远是噪声源。
4. 缺 frontmatter 降级为 warning（对齐"渐进补齐"政策），而不是 error。
——但做完这四条后，Kit 剩余能力与 Engine 现有工具几乎完全重合（见 §2），接入收益趋近于零。

---

## 4. ensure_agents_pointer：幂等/保护行为与测试

实现：cli/governance.py:304-352。四态返回：
- `created`：不存在或空文件 → 写完整入口（含 frontmatter，L320-323、L332-336）；
- `appended`：已有内容 → **二进制追加模式**（`open(..., "ab")`，L350），原字节不动；沿用原文件 CRLF/LF 风格（L344）；末尾无换行先补换行（L347-349）；追加段不写第二个 frontmatter（L57-58 注释、标题降 H2 L90）；
- `present`：按字节级 `POINTER_BEGIN` 标记判定已存在（L329-330），幂等不重复追加；
- `skipped`：非 UTF-8 文件解码失败 → 原样保留（L338-341），CLI 明确警告不静默（L1167-1170）。

**测试：有，且相当充分**——`InitExistingAgentsTests` 9 个用例（tests/test_governance.py:591-772）：
- 原内容**逐字节不变** + CRLF + 无结尾换行 + 中文内容（L667-686，断言 `after.startswith(original)`、标记只出现 1 次、追加段无 frontmatter）；
- 重复 init 幂等：AGENTS.md 与 `.governance/` 全目录字节快照对比（L689-703、L706-712）；
- 空文件只写一次（L731-739）；
- GBK 非 UTF-8 文件不被破坏 + CLI 出警告（L742-751）；
- 空格/中文路径（L715-728）、kit 内相对路径（L754-760）、Windows 跨盘符回退绝对路径（L763-772）。

已知缺陷（USER-GUIDE L317，自认未修）：指针自身 frontmatter `type: adapter-entry` 不在 13 类枚举内，inventory 登记后 doctor 会对自己生成的入口报 1 项 type 错误——枚举设计与自身产物不自洽。

结论：这是 Kit 中**工程质量最高**的函数（字节级保护 + 9 测试），但 Engine 指针已存在且人工维护，对 Engine 无现实需求。

---

## 5. 结论建议：**Archive（整体归档），可选 Embed 两个纯函数**

### 5.1 为什么 Archive 而不是整体 Embed

1. **重叠度高且 Engine 更强**：15 项能力 9 项已覆盖，其中单写者（事前拒绝 vs 事后检测）、审批（SHA256 证据链 vs 无测试布尔字段）、注册表（启发式+溯源+漂移门禁 vs unknown 兜底）、写盘纪律（schema 校验+原子写 vs 直接 json.dump）Engine 均更强（§2 表 #3/5/7/11）。
2. **唯一"实跑证明"是负面的**：对 Engine 的真实适配产出 621/804 项噪声、三个空注册表、一个遗留 `.governance/` 目录（§3.5），没有产生任何被消费的任务/交接/ADR 数据。
3. **type 枚举零交集**是设计级不兼容，修复它等于放弃 Kit 的核心规范（13 类），修完后与 Engine 工具完全重合。
4. Kit 自己的文档已给出诚实定位："不能替代 run_state……不是编排器"（USER-GUIDE L298-299）、render-notes README"不实现编排器、Render_Notes 保留自己的状态机"。它作为**通用治理教学/模板仓**有保留价值，作为 Engine 的并行治理轨则违反 Engine D04/D07"一个门禁一处维护、不建第二套"的既有裁决（DECISIONS.md L26-30、L42-45）。

### 5.2 若 Embed，只值得搬这些（按价值排序）

| 优先级 | 搬什么 | 从哪到哪 | 为什么 |
|---|---|---|---|
| ★★★ | `check_frontier`（governance.py:921-934）+ `detect_dependency_cycles`（L963-998）+ `_dependency_ids`（L855-876） | 并入 `tools/run_state.py`（如 new/advance 时校验 dependencies 就绪、new 时拒绝成环依赖），测试移植 test_governance.py:441-497 到 kcr selftest 风格 | **唯一填补真实空白**：run_state 记录 dependencies（L167/182）但从不检查就绪/环；三函数纯 stdlib、纯函数、已有 6 个测试用例，改造成本低 |
| ★（仅当需要时） | `ensure_agents_pointer`（L304-352）及其 9 个测试（test_governance.py:591-772） | 独立小工具入 `tools/`，用于多适配入口的指针维护 | 字节级保护+CRLF/编码处理+幂等标记的实现质量高；但 Engine 指针已存在，**当前无需求，不建议现在搬** |
| 不搬 | 其余全部（init/inventory/validate/doctor 枚举/handoff/adr/audit/archive-check/status/map、constitution、schemas、adapters） | — | 与 Engine 重合或更弱；audit/archive-check 无真实数据验证；schemas 无运行时消费方 |

### 5.3 附带处置建议（需人工裁决，本审计未执行）

- Engine 根 `.governance/` 遗留目录（2026-11-21 适配产物，三注册表全空）：建议裁决后移除或移入 archive，避免双轨注册表误导后续 Agent（Engine AGENTS.md 明文"先查 `.agent/indexes/document-registry.json`"）。
- Kit 仓归档时保留 git 历史与 USER-GUIDE §17 已知缺陷清单（其自我审计诚实、有复用参考价值）；若采纳 ★★★ Embed，在 Kit README 标注"已并入 Engine run_state，本仓归档"。

---

## 附：证据索引

| 论断 | 证据 |
|---|---|
| 41 测试全过 | `py -3 -m unittest discover -s tests -v` → `Ran 41 tests in 0.297s / OK` |
| 6 笔提交 | `git log --oneline`（7d9a187…ac62da6） |
| doctor 621 / validate 804 / exit 1 | 实测输出（§3.1），分解统计 §3.1 |
| type 枚举零交集 | 程序化比对 `types & et == set()`（§3.2） |
| Engine 注册表 212 条 / 14 类 type / unregistered 79 | json Counter 实测（§2 基线） |
| Kit 扫 232 篇含 site-vitepress 74 篇、漏 .agent 51 篇 | scan_markdown_docs 实测 Counter（§3.4） |
| Engine .governance 遗留、三注册表空、AGENTS.md 无指针 | json 实测 + rg exit 1（§3.5） |
| run_state 无依赖就绪/环检查 | rg "dependencies\|frontier\|cycle" 全量行号（§2 #9） |
| ensure_agents_pointer 9 测试 | test_governance.py:591-772 |
| Kit 自认缺陷 | docs/USER-GUIDE.md:307-321 |