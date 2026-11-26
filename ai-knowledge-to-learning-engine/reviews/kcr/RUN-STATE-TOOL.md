---
doc_id: RUN-STATE-TOOL
type: kcr
status: active
owner: qwenwork
created: 2026-11-20
updated: 2026-11-20
---

# P9 轻量工作流状态机工具说明（tools/run_state.py）

> 2026-11-20 实现（用户批准"开工 P9 轻量状态机，按设计稿扩展现有 tools 实现"）。
> 设计依据：`reviews/P9-orchestrator-design.md`（十阶段 + KCR 子状态 + 五条不变量）、
> `NEXT_PHASE_PLAN.md` P9.2、`reviews/EXECUTION_PLAN_V3.md` P9。stdlib-only（D05），不引 DB/队列/分布式组件。

## 作用

把 WORKFLOW_STATE.md 的人工叙述补上一层**机器可读的运行态**：每个生产任务一个 run，
记录阶段、输入/输出 artifact（path+sha256）、执行记录、失败原因、重试次数、人工关卡与续跑点。
支持断点恢复、防重复写入、失败重试、人工暂停/跳过、单写者冲突检查（G-W1 闭合）。

## 状态机

```
INTAKE → RESEARCH → EVIDENCE → ARCHITECT → WRITE → DESIGN → PRACTICE → REVIEW → PUBLISH → FEEDBACK
```

- 每阶段完成条件（硬）：本阶段至少登记 1 个 artifact；进入 PUBLISH/FEEDBACK 另需 human_gate passed **且通过审批证据链复核**（见 `tools/approval_chain.py`）。
- 每阶段角色/完成条件/下一步动作内置于 `PHASE_INFO`，`show` 的 resume_point 直接给出下一步。
- KCR 变更叠加子状态：`PROPOSED → REVIEWING → APPROVED → APPLIED → VERIFIED`（严格顺序，APPROVED 必须人工）。
- run 状态：`pending | running | paused | done | failed`；done 只能出现在 FEEDBACK。

## 六条不变量（程序强制）

1. **人工门不可绕过**：`gate --pass` 必须 `--approver <人名>` 且非空；无任何自动批准路径；已 passed 不重复批准、不可重置。
2. **AI 不预填裁决**：工具只记录关卡状态与材料 artifact，不写评分/裁决内容（G2 评分仍走人工材料）。
3. **未批准不应用**：进入 PUBLISH/FEEDBACK 必须 gate passed；KCR APPROVED 必须人工 approver，APPLIED 只能在 APPROVED 之后。工具本身不写权威 JSON——写回仍走 KCR 流程与任务授权。
4. **单写者**：同一 write_path 声明即持有（pending/running/paused/failed 均算），第二个 run 声明/新建即拒绝；done 自动释放，或 `release-path` 显式释放。
5. **可追溯**：artifact 记 path+sha256（同 phase+path+hash 幂等不重复；内容演进记新 hash）；每次变更追加 transitions（时间/操作者/动作/理由）。
6. **批准对应到文件版本**（TASK 4，2026-11-25）：进入 PUBLISH/FEEDBACK（含人工 `skip`）前，`approval_chain.verify` 重算人工批准时冻结的产物哈希——任何产物在批准后变化、被移走，或批准后新增了已批准阶段的产物，都拒绝推进并要求重新审核。没有审批记录的已过关卡报 legacy/unverifiable，不补造。

## 运行态落盘

- `.agent/runs/<run_id>.json`，契约 `tools/kcr/schema/run-state.schema.json`（第四契约，已接入 validate_kcr）。
- D15：运行态本地 only（.gitignore 已含 `.agent/runs/`）；摘要留痕走 CHANGELOG，不提交运行态。
- 每次保存前全量契约校验（schema + semantic），失败不写盘；固定名 tmp + os.replace 原子替换，全程无删除操作。

## 与 kcr_impact 对接

`artifact --path reviews/kcr/impact-*.json` 自动识别为 impact-report，登记前过 impact-report 契约校验，
失败不登记。RESEARCH/EVIDENCE 阶段的影响分析产物由此进入可追溯链。

## CLI 速查（本机用 py -3）

```
py -3 tools/run_state.py new --run-id RUN-2026-11-20-x --owner qwenwork --gate G3 [--kcr] [--write-path tools/course.json]
py -3 tools/run_state.py start|pause|resume|fail --reason ...|retry --run-id ...
py -3 tools/run_state.py artifact --run-id ... --path <文件> [--phase P] [--note ...]
py -3 tools/run_state.py advance --run-id ... --reason ...
py -3 tools/run_state.py gate --run-id ... --pass --approver <人名>    # 仅人工执行
# 发布前还需人工登记审批（TASK 4），approve 人名须与上一行一致：
py -3 tools/approval_chain.py record --run-id ... --gate G3 --approver <人名> --scope "<批准覆盖什么>"   # 仅人工执行
py -3 tools/approval_chain.py verify --run-id ...                                                    # 任何人都可查看复核结果
py -3 tools/run_state.py skip --run-id ... --to WRITE --approver <人名> --reason ...
py -3 tools/run_state.py kcr --run-id ... --to APPROVED --approver <人名>
py -3 tools/run_state.py claim-path|release-path --run-id ... --path ...
py -3 tools/run_state.py show --run-id ... / list
```

退出码：0 成功；1 规则拒绝；2 用法/文件错误。`--runs-dir` 可指向临时目录（测试用）。

## 自测

`py -3 tools/kcr/selftest_runstate.py` — 25 tests：schema 正反用例 / 六条不变量 /
断点恢复 / 失败重试 / 防重复写入 / 人工跳过暂停 / KCR 顺序 / kcr_impact 真实回放
（SRC-RN-COLORMGMT）/ CLI 退出码。全部写入临时目录，不触碰真实 `.agent/runs/`。

`py -3 tools/kcr/selftest_approval.py` — 15 tests（TASK 4）：approval-record 契约正反用例 / 登记守卫 /
只增不改 / 批准后文件变化拦截与还原恢复 / 越权新增产物拦截 / 后续阶段产物不误伤 /
历史批准 legacy-unverifiable 不补造 / 记录被改坏拦截 / 与状态机联动（含人工 skip）/ 临时 git 仓库提交号采集 / CLI 退出码。

## 边界（不做的事）

- 不自动执行阶段任务（编排执行仍由 Agent 按任务授权进行；本工具只管状态与不变量）。
- 不写权威 JSON（claim-ledger/concepts/course.json）、不升级 claim、不发布。
- 不做多进程并发锁（单用户单写者场景；跨进程竞争由"声明即持有 + 保存前校验"兜底，真并发需求出现再评估）。
- 工具盘点（P9.4 / G-W3）不在本工具范围，仍待做。