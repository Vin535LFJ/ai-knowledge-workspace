---
doc_id: PROJECT_PRINCIPLES
type: constitution
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 项目治理原则（12 条）

本项目遵循以下 12 条不可妥协的治理原则。所有 Agent、所有客户端 Adapter、所有项目配置都不得与之冲突。

---

## 1. 项目独立、可迁移

治理配置随项目走，不绑定某个平台、某个 IDE 或某个云端服务。把项目目录整体搬走，治理能力应当完整保留。禁止把权威状态藏在工具私有目录或云端。

## 2. 每份正式文档只有一个权威来源

L1 正式文档在同一时间只有一个权威版本（single authoritative source）。其他位置只能是指针、副本或历史版本，并显式标注 `source_of_truth`。

## 3. 工作文档与正式文档严格分离

草稿、计划、研究草稿、执行日志等工作产物（L2/L3）不得被当作正式事实（L1）引用。分级规则见 [`DOCUMENTATION_POLICY.md`](DOCUMENTATION_POLICY.md)。

## 4. 所有 Agent 共用同一套规则

无论 Agent 来自哪个厂商、哪个客户端，进入同一项目都遵守同一套章程。禁止为某个 Agent 单独维护一份「规则正文副本」。

## 5. 每个任务一个 owner + 明确读写范围

每个任务只有一个主 writer（`owner_agent`），并声明 `read_paths` / `write_paths` / `protected_paths`。并行研究允许，并行写同一文件禁止。

## 6. 每次文档变更都有来源与记录

任何正式文档变更必须记录来源（`source`）与变更记录（`record`）。无来源的变更视为非法，审计会标记。

## 7. ADR 只用于架构决策

ADR 仅记录架构层面的、难以逆转的决策。普通技术选择、任务完成、实现细节不写 ADR。

## 8. 普通计划不产生 ADR

执行计划、变更计划、任务清单都是 L2 工作文档，不因完成而升格为 ADR。

## 9. 重要状态机器可读

重要的项目状态、任务状态、审批状态以机器可读的 JSON 存放（`.governance/`），便于查询与自动检查，但不取代人类可读的文档。

## 10. 人工决策不可被 AI 替代

架构决策、业务目标变更、权威知识升级、课程路线变更、高风险删除、重要归档、git 提交/推送、生产部署——必须由人确认。无回复 ≠ 同意。详见 [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)。

## 11. Adapter 不复制规则正文

各客户端 Adapter 只生成索引 / 指针 / 配置 / 兼容条目，指向本工具包的权威规则。禁止把章程正文复制进客户端私有目录。

## 12. 未验证的 Agent 能力显式标记为 unverified

配置文件存在 ≠ 能被发现 ≠ 能成功调用。每个客户端有独立验证记录；未实际验证的能力必须标记为 `unverified`，不得假定可用。

---

## 13. 三条协作协议为铁律

原则 5（一任务一 owner + 明确读写范围）进一步落实为三条可执行协议，任何 Agent 与 Adapter 都不得绕过。CLI `doctor` 命令提供只读诊断。

### 13.1 Task Claim（开工前认领）

先认领、后开工。认领记录必须包含 Agent、分支/worktree、时间与任务范围四要素，并生成唯一 `claim_token`，将任务置为 `in_progress`。已被他人认领的任务不得重复认领——这是 Single Writer 在「任务层」的体现。未认领就写视为违规。

### 13.2 Single Writer per Path（同一路径唯一写入者）

同一文件同一时刻只有一个写入者。当两个 `in_progress` 任务的 `write_paths` 重叠且 owner 不同，即构成冲突，必须停止写入并等待人工裁决。其他人只能提交建议或独立补丁。文件所有权是约定而非真实锁，靠分支/worktree 隔离与 hooks / CI 辅助校验。

### 13.3 Dependency Frontier（依赖前沿）

依赖全部完成或批准后才可开工，不越 `write_paths`、不碰 `protected_paths`。未满足的依赖列表必须显式记录，任务保持 `blocked`。依赖环视为死锁，必须人工拆解。依赖就绪不等于跳过人工审批，需审批者仍须人工确认。

> 三条协议互为补充：Task Claim 确定「谁在主写」，Single Writer 保证「同一路径不并发写」，Dependency Frontier 保证「依赖就绪才开工」。三者均由 `doctor` 进行只读检查，发现冲突或环时以非零退出码告警。
