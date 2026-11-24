---
doc_id: P9-ORCHESTRATOR-DESIGN
type: agent-plan
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-20
---

# P9 轻量 Agent Orchestration 设计（已实现，见 §6）

> 2026-11-19 建立设计；2026-11-20 用户批准后实现（tools/run_state.py + run-state 第四契约）。
> 设计期边界（不创建运行态文件）已由实现轮取代：运行态落 `.agent/runs/`（D15 本地 only，gitignore）。

## 1. 角色（ ≠ 9 个独立进程）
Research Agent · Evidence Analyst · Knowledge Architect · Documentation Writer · Learning Designer · Practice Designer · Knowledge Reviewer · Knowledge Publisher · Feedback Analyst。按任务复杂度选单 Agent / 多 Agent / 并行子任务 / 顺序执行。

## 2. 状态机（每阶段明确完成条件）
```
INTAKE → RESEARCH → EVIDENCE → ARCHITECT → WRITE → DESIGN → PRACTICE → REVIEW → PUBLISH → FEEDBACK
```
每个 KCR 变更叠加子状态：
```
PROPOSED → REVIEWING → APPROVED → APPLIED → VERIFIED
```
- 支持断点恢复（run-state 落盘）、失败重试、人工暂停。
- 同一批权威数据（claim-ledger / concepts / course.json）不得多 Agent 无协调同时写——单写者约定（见 Governance Kit 的 Task Claim 协议）。

## 3. 最小 run-state JSON schema（内联，未落盘）
```json
{
  "run_id": "string",
  "phase": "INTAKE|RESEARCH|...|FEEDBACK",
  "status": "pending|running|paused|done|failed",
  "kcr_substate": "PROPOSED|REVIEWING|APPROVED|APPLIED|VERIFIED",
  "owner_agent": "string",
  "dependencies": ["run_id"],
  "artifacts": [{"phase": "string", "path": "string", "hash": "string"}],
  "human_gate": {"gate": "G1|G2|G3", "status": "open", "approver": null, "approved_at": null},
  "resume_point": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

## 4. 不变量（不可绕过）
1. **人工门不可绕过**：G1/G2/G3 状态只能由人改为通过；AI 不得写入 `approved`。
2. **AI 不预填裁决**：decision-kit 与 claim 升级的裁决栏，AI 保持空白。
3. **未批准不应用**：KCR 子状态未到 APPROVED/VERIFIED 前，不写回权威 JSON、不改正式教材、不发布。
4. **单写者**：同一 `write_path` 同时刻仅一个 owner_agent 持有。
5. **可追溯**：每阶段产物记录 path + hash；状态变更记录时间/操作者/理由。

## 5. 本轮交付边界（设计轮，2026-11-19，已被 §6 取代）
- 交付：本文（设计 + schema 内联）。
- 不交付：run-state 实例、编排执行代码、`.agent/runs/`、任何已通过的 G 门。
- 下一步（待人工裁决）：是否按此设计实现最小状态机 + 与 `tools/kcr_impact.py` 的输出对接。

## 6. 实现记录（2026-11-20，用户批准）
- **实现**：`tools/run_state.py`（CLI + API，stdlib-only）；契约 `tools/kcr/schema/run-state.schema.json`
  （§3 schema 的实现扩展：phase_records/transitions/write_paths/retry_count，字段语义见工具说明）。
- **校验**：`tools/kcr/validate_kcr.py` 扩为四契约；run-state 硬规则（人工门/未批准不发布/KCR 人工批准/done 仅在 FEEDBACK）入 semantic_errors。
- **对接**：impact-report artifact 登记前自动过契约校验（kcr_impact 输出直接入链）。
- **自测**：`tools/kcr/selftest_runstate.py` 25 tests OK（含 SRC-RN-COLORMGMT 真实回放）；selftest_impact 回归 16/16 OK。
- **说明**：`reviews/kcr/RUN-STATE-TOOL.md`（CLI 速查/不变量/边界）。
- **仍待**：P9.4 工具盘点（G-W3）；P10 端到端验收时以真实 run 使用本工具。
