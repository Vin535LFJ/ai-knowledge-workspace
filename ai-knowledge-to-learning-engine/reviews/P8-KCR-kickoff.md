---
doc_id: P8-KCR-KICKOFF
type: review-material
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# P8 启动检查点 · KCR 最小闭环（2026-11-20）

> **性质**：阶段转换检查点（P7.2 十篇收官 → P8 启动）。本文件只做**范围界定与续跑指引**，不含实现。
> **授权链**：PD-003（Engine 唯一活跃线）+ handoff §3 T3（P8 范围）+ 用户 2026-11-20 "继续推进下一个阶段"（接受"先 P8"建议，见 WORKFLOW_STATE 续跑点）。
> **执行纪律**：实现工作在**新窗口**进行（本窗口上下文预算已尽）；一次一个最小切片，每片过门禁留痕。

## 1. 已有资产（不重建，逐一核对过）

| 资产 | 状态 | 位置 |
|---|---|---|
| KCR 五阶段机制设计 + schema 提案 | ✅ 完整（D13） | `reviews/KNOWLEDGE_CHANGE_REVIEW.md` |
| Stage 1 影响分析只读工具 | ✅ 已起步可用：`--source-id/--claim-id/--report/--claim-draft` 四模式，双向索引构建、impact-report JSON 输出到 `reviews/kcr/` | `tools/kcr_impact.py` |
| Stage 3 人工关卡纪律 | ✅ 已有制度（G1 性质，AI 不自主；review-decision.json 人工填写） | 同上设计文档 |
| 文档注册表一致性 | 部分——validate §8 已校验 claim↔source 双向索引；**document-registry（frontmatter）一致性门禁未接入 validate** | `tools/validate_site.py` / `tools/build_document_registry.py` |
| 数据契约样例 | 十篇新教材 + V21–V38 登记过程 = KCR 流水线的真实演练样本 | `evidence/*` |

## 2. 最小闭环范围（P8-MVP，建议三片、一片一窗口）

1. **片一（Stage 1 完善）**：`kcr_impact.py` 补 `--proposal` 输入（读 change-proposal.json 草稿做影响比对）+ 单元自测（用 V21–V24 登记过程做真实回放样本）；验收：`py -3 tools/kcr_impact.py --claim-draft "..."` 输出与人工判断一致。
2. **片二（schema 固化）**：把设计文档中的 `impact-report.json` / `change-proposal.json` / `review-decision.json` 三个 schema 落为 `tools/kcr/schema/*.json`（JSON Schema，D05 stdlib 原则）+ kcr_impact 输出按 schema 校验；验收：schema 校验通过 + 现有样本可回放。
3. **片三（门禁接入）**：validate_site 增加第 12 节——document-registry 与磁盘 frontmatter 的一致性检查（只读比对，FAIL 需重建 registry）；验收：故意弄脏一处 frontmatter → validate FAIL → 重建后恢复。**改 validate 属核心门禁改动，动手前报批。**

## 3. 明确不做（P8-MVP 之外）

- 不做 Stage 4 自动 apply（增量更新仍人工驱动）；不做 Web/数据库；不做多课程泛化；不动 `.agent/**` 结构；不做 Stage 2 之外的提案生成自动化。

## 3b. 片二进度（2026-11-20 本窗口）

- **已落盘**：`tools/kcr/schema/impact-report.schema.json`、`change-proposal.schema.json`、`review-decision.schema.json`（按 D13 设计文档字段结构固化，三文件 JSON 有效）。
- **冒烟测试发现（片一的对齐目标）**：`kcr_impact.py --claim-draft` 实际输出与设计 schema 存在漂移——缺顶层 `trigger`/`new_sources`、`affected` 多 `website` 键。真实样本：`reviews/kcr/impact-l09-p07.json`（L05/验真队列 P07 的 flush 断言草稿影响分析）。**片一续跑 = 把工具输出对齐 schema**（补 trigger 段或 schema 分模式），漂移不掩盖、不伪造。

## 3c. 片一完成（2026-11-20，独立复核窗口）

- **对齐完成**：trigger 四模式映射（source_update / claim_status_request / new_research_report / 草稿=claim_status_request）+ new_sources 恒 []（来源登记属 Stage 2）；affected 元素对象化（id+relation/via_claim）；website→非契约 website_artifacts；结构完整性检查→integrity_findings（不冒充契约 conflicts）；uncovered→字符串数组。另修复 `--out` 仓库外路径崩溃 bug。
- **自测**：`tools/kcr/selftest_impact.py` 5/5 OK（真实回放 COLORMGMT→V21–V24→L03 / V14→K-STRIDE/L01/L01#L01-Q2 / V21 open 标注 / 草稿 CLI / 未知 seed）。
- **样本重生成**：impact-l09-p07.json / impact-v14-replay.json / impact-colormgmt-replay.json 均符合契约。
- **下一步**：片二收尾 = 程序化校验器（stdlib-only，对三 schema 做 required/type/enum 校验，接入 kcr_impact 输出与样本回放）；片三 registry 门禁接入 validate **动手前报批**。

## 3d. 片二完成（2026-11-20，本窗口）

- **校验器落盘**：`tools/kcr/validate_kcr.py`（stdlib-only）——实现三 schema 实际用到的全部关键字子集（type 含类型数组 / required / properties / items / enum / pattern / minItems）；未支持关键字直接抛错（防 schema 演进静默漏检）；`semantic_errors` 实现文档化硬规则（modify/deprecate/reverify 必须 target.id；--stage2 时 human_decision 必须 null）；CLI 多文件 + 文件名推断契约 + 退出码 0/1/2。
- **接入**：`kcr_impact.py` 写盘前强制契约校验，失败不写、退出码 3。`selftest_impact.py` assert_shape 升级全量校验 + ValidatorTests 11 例，**16/16 OK**；CLI 实测三份真实样本全 OK（impact-v14.json / impact-draft.json / impact-demo.json 为对齐前历史冒烟工件，保留不改写、不作契约样本）。
- **同窗口执行**：L02 遗留 major M1（用户采纳推荐）——labs.json + app.js 两处「DTS ≤ PTS 恒成立」改为 I/P 帧 PTS ≥ DTS、B 帧 PTS < DTS 口径；连带修复 tlDelta "+-1" 符号 bug；Edge headless 双路 QA（http/file）渲染 DOM 实测通过；G2-L02 材料追加执行补记。
- **门禁**：build 75 docs / 552 cards；validate 11/0/0；arc 11/11；publish 11/11；review_gate 55 claims（18v/30o/7c）误标 0。
- **下一步**：片三（document-registry ↔ frontmatter 一致性门禁接入 validate，**改核心门禁，动手前报批**）→ L10 恢复 → P9 → P10。

## 3e. 片三完成（2026-11-20，用户批准后执行）

- **门禁接入**：validate_site.py 第 12 节 [registry]——生成器 `collect_entries()`（本片从 main 抽出的纯函数，生成/校验共用单一口径）重算磁盘真值，与注册表逐条比对（缺失/残留/字段漂移/meta.total），只读；FAIL 自带重建命令。检查数 11→**12**。
- **首跑实证**：抓到 16 处真实漂移（registry 142 vs 磁盘 158：6 新教材 + 9 G2 材料 + 本 kickoff）→ 重建 → 12/0/0。
- **验收演练通过**：弄脏本文件 frontmatter `updated` → validate 精确 FAIL（exit=1，字段级定位）→ 重建恢复 12/0/0 → 还原 frontmatter 再重建 → 12/0/0；本文件 SHA256 演练前后一致（A952DC56…691F），零残留。
- **P8-MVP 三片全部完成**。按 §4 续跑：L10《显式 API 与同步》教材生产恢复 → P9 最小状态机 → P10 端到端验收；研究队列 C1–C7 按 P8 节奏执行。前置建议仍有效：先授权提交未提交文件再叠加新改动。

## 4. 续跑指引（下一窗口）

1. 读本文件 + `reviews/KNOWLEDGE_CHANGE_REVIEW.md` + `tools/kcr_impact.py`。
2. 按片一→片二→片三顺序执行，每片：实现 → 自测 → 全门禁（build/validate/arc/review_gate/publish）→ CHANGELOG/WORKFLOW_STATE 留痕 → G2/P8 材料归档。
3. **未提交的 31 文件（P7.2 十篇）应先获用户 commit 授权**——P8 改动叠加其上会混淆回滚边界，建议先提交再动工。
4. L10《显式 API 与同步》教材生产在 P8-MVP 后恢复（依赖关系：P8 的 KCR 正是 L03–L09 登记流程的工程化）。
