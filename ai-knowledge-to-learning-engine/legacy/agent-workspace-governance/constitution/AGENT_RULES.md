---
doc_id: AGENT_RULES
type: constitution
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# Agent 共用规则

无论 Agent 来自何种客户端，进入本项目都必须遵守以下规则。本文件是规则的**唯一权威正文**；Adapter 只能指向它。

---

## 1. 身份与能力

- 开始前在 Agent 注册表登记 `agent_id`、provider、model、harness、capabilities、supported_skills / mcp / tools、invocation_mode、并行与后台任务能力、file_access_scope。
- 所有未经实跑验证的能力，`runtime_verification_status` 必须为 `unverified`。
- 配置存在 ≠ 被发现 ≠ 可调用；三者分别记录，不得混为一谈。

## 2. 任务归属

- 一个任务只有一个 `owner_agent`（主 writer）。其他 Agent 可以并行**研究**，但不得并行**写**同一文件。
- 写文件前先对照 `write_paths` 与 `protected_paths`；不在范围内的文件不写。
- 遇到归属冲突，发出冲突警告并等待人工裁决，不擅自覆盖。

## 3. 依赖与交接

- 任务开始前检查 `dependencies` 是否完成。
- 交接使用标准交接文档（`templates/handoff.md`），写清产出、验收标准、未决事项。
- 完成时必须做前后审计（before/after audit）对照 `acceptance_criteria`。

## 4. 文档纪律

- 遵守 [`DOCUMENTATION_POLICY.md`](DOCUMENTATION_POLICY.md) 的分级与生命周期。
- 正式文档变更必须带 `source` 与 `record`。
- 工作文档不越级当作正式事实。

## 5. ADR 纪律

- 只有架构决策才创建 ADR，使用 MADR 字段。
- ADR 状态由人推进，**绝不因实现完成自动 accepted**。
- 被取代的 ADR 标记 `superseded` 并指向新 ADR；废弃的标记 `deprecated`。

## 6. 人工审批

- 涉及 [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md) 中清单的动作，必须暂停等待人工确认。
- 审批记录包含 approver / time / object / decision / 授权范围。
- 无回复不等于同意。

## 7. 分支与工作树

- 多 Agent 并行时建议使用独立分支或 worktree 隔离写入。
- 本工具包不提供真实分布式锁；文件所有权是约定，需靠 hooks / CI 辅助。

## 8. 客户端适配

- 通用入口是 `AGENTS.md`。
- 具体客户端只加载对应 Adapter 的指针，不复制规则正文。
- 每个客户端维护独立验证记录。

---

## 9. 三条协作协议（可执行规则）

以下三条协议对所有 Agent 强制生效，是对第 2、3、7 节的具体化。CLI 的 `doctor` 命令会据此做只读诊断。

### 9.1 Task Claim（开工前认领）

- 任何 Agent 在开始写一个任务之前，必须先认领该任务，调用 `governance.claim_task` 或在任务注册表中写入认领信息。
- 认领必须记录四要素：`agent`（认领者标识）、`branch`（分支或 worktree 标识）、`now`（认领时间，写入 `claimed_at`）、任务范围（`write_paths` / `protected_paths`）。
- 认领成功时生成唯一 `claim_token`，并将任务 `status` 设为 `in_progress`、`owner_agent` 设为认领者。
- 若任务已被其他 Agent 认领（其 `owner_agent` 不同且 `status=in_progress`），认领必须被**拒绝**，返回冲突错误；认领者只能提交建议或独立补丁，不得改写该文件。
- 未认领即写属于违规；`doctor` 会报告进行中但缺少 `claimed_at`/`claim_token` 的任务。

### 9.2 Single Writer per Path（同一路径唯一写入者）

- 同一文件在同一时刻只能有一个写入者。判断依据：`write_paths` 发生重叠、两个任务均为 `status=in_progress`、且 `owner_agent` 不同。
- 命中上述条件即为单写者冲突，`doctor` / `detect_single_writer_conflicts` 会报告冲突任务对；冲突期间双方均不得写入重叠路径。
- 非主 writer 只能通过「提交建议」或「独立补丁（不落盘到受保护路径）」参与，由主 writer 或人工合并。
- 写文件前必须核对 `write_paths` 与 `protected_paths`：越出 `write_paths` 不写，触碰 `protected_paths` 不写。
- 文件所有权是约定而非真实锁；多 Agent 并行时用独立分支/worktree 隔离，并靠 hooks / CI 辅助校验。

### 9.3 Dependency Frontier（依赖前沿）

- 任务开始前必须检查 `dependencies`（或 `dependency_frontier`）中每个依赖任务的状态；只有全部为 `completed` 或 `approved` 才算依赖就绪。
- `check_frontier` 返回就绪布尔值与未满足依赖列表；存在未满足依赖时，任务必须保持 `blocked`，不得开工。
- 不得越过 `write_paths` 写不属于本任务的路径，不得触碰 `protected_paths`；依赖未完成时不得「先干再说」。
- `detect_dependency_cycles` 检测依赖环；存在环时，环上所有任务均视为不可开工，必须人工拆解依赖后再认领。
- 依赖状态不因实现完成而自动跳过人工审批；需审批的依赖仍需人工确认后才视为就绪。
