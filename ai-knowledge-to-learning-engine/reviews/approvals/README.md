---
doc_id: ENG-APPROVALS-README
type: review-material
status: active
owner: qwenwork
created: 2026-11-25
updated: 2026-11-27
---

# 审批证据链 · 目录说明与历史审批登记

> 工具：`tools/approval_chain.py`（登记与复核）· 契约：`tools/kcr/schema/approval-record.schema.json` · 联动：`tools/run_state.py`（进入 PUBLISH / FEEDBACK 前自动复核）
> **`record` 只能由人工执行。AI 不得运行 record，也不得代填 `--approver`。**

## 1. 这个目录解决什么问题

此前的人工关卡只有一个状态开关：`run_state.py gate --pass --approver <名字>` 把关卡标成 passed，但不记录"批准的是哪一版文件"。文件之后被改，发布门也不知道。上一轮审计因此指出：审批人只是一个字符串，且历史 run 的 18 条产物记录里有 7 条哈希与现状不符。

现在一次批准要留下三样东西，缺一不可：

| 步骤 | 命令（人工执行） | 留下什么 |
|---|---|---|
| ① 登记审批 | `py -3 tools/approval_chain.py record --run-id <RUN> --gate G3 --approver <人名> --scope "<批准覆盖什么>"` | `reviews/approvals/<RUN>/G3-01.json`：每个产物的相对路径 + SHA256 + 所处阶段，审批人、时间、决定、范围、当时的提交号与未提交文件数 |
| ② 通过关卡 | `py -3 tools/run_state.py gate --run-id <RUN> --pass --approver <同一个人名>` | 运行态里关卡变 passed（审批人必须与 ① 一致） |
| ③ 发布前复核 | `py -3 tools/approval_chain.py verify --run-id <RUN>`；`advance` 进入 PUBLISH / FEEDBACK 时也会自动执行 | 重算每个产物的哈希，与批准时比对；检查范围、审批人、时间、决定 |

**会被拦下的情形**（都已用自测与真实仓库演练验证）：批准后任一产物内容变化；批准时的产物被移走；批准后在已批准阶段新增产物；记录被改坏；`decision` 不是 approved；关卡已过但没有审批记录。

**规则**：记录只增不改——重新批准生成 `G3-02.json`，旧记录原样保留；复核以最新一份为准。批准之后才可能产生的后续阶段产物（如 PUBLISH 阶段的发布记录）不计入越权。

## 2. 目录结构

```
reviews/approvals/
├── README.md                      ← 本文件
└── <run_id>/
    ├── G3-01.json                 ← 第一次批准
    └── G3-02.json                 ← 文件变化后重新批准
```

记录文件入库（可跨机器追溯），且在学习站发布边界之外（`reviews/` 为 excluded-internal，默认拒绝，不进站点）。运行态 `.agent/runs/` 仍是本机文件，不入库。

### 2.1 已登记的审批记录

| run | 关卡 | 记录 | 绑定提交 | 产物数 | 登记方式 |
|---|---|---|---|---|---|
| RUN-2026-11-23-embodied-batch1 | G1 | `RUN-2026-11-23-embodied-batch1/G1-01.json` | `67abc1d` | 24 | **代理代录**（见下） |
| 同上 | G2 | `RUN-2026-11-23-embodied-batch1/G2-01.json` | `67abc1d` | 24 | **代理代录**（见下） |

**这两条是一次经明确授权的例外，不改变上面的规则。** 2026-11-27 用户明确授权代理"登记已经明确作出的 G1/G2 决定"，并要求如实标注：决策人 = 用户本人；决策日期 = 2026-11-27；决策依据 = 用户在对话中明确给出的裁决；记录执行 = 代理代录；**身份认证 = 未进行**。`--approver` 字段里写明了"代理代录，未经身份认证"。**G3 与 KCR 未获代录授权**，仍须用户本人执行；截至本记录，G3 为 open、KCR 为 REVIEWING。

## 3. 历史审批登记（不补造）

以下批准发生在审批证据链建立之前。它们**有书面证据表明当时确实做过裁决**，但都没有绑定文件版本，因此一律标为 **legacy / unverifiable（无法验证对应的文件版本）**。本目录不为它们补造审批人、时间或哈希。

| run | 关卡 | 留存的证据 | 状态 |
|---|---|---|---|
| RUN-2026-11-20-p10-hdr | G1 | `reviews/p10/G1-hdr-verification-queue.md` 裁决栏：V63–V67、V23 共 6 项升级，裁决人记为"user（授权 AI 推荐执行）"，日期 2026-11-21 | legacy / unverifiable |
| 同上 | G2 | `reviews/G2-L19-deepening.md` §5：91 分，通过；裁决人"用户本人（采纳 AI 诊断建议分，人工确认）"，2026-11-21 | legacy / unverifiable |
| 同上 | KCR | 运行态（本机）REVIEWING→APPROVED，操作者记为"user（采纳 AI 推荐授权 2026-11-21）" | legacy / unverifiable |
| 同上 | G3 | 运行态（本机）：2026-11-21T22:22:05+08:00 置为 passed，审批人字段为字符串"user(2026-11-21 G2=91 通过)" | legacy / unverifiable |

需要如实说明的两点：

1. 上表中的"审批人"字符串是当时的 AI 按用户授权写入的，不是用户亲手输入。书面裁决栏与评分表是用户决定的证据；运行态里的字段不是。
2. 该 run 登记的产物去重后 16 个，按当前文件重算，**6 个哈希与登记值不符**——这些文件在登记之后被编辑过（例如评审后补写、文档治理时移动）。因为当时没有批准时的哈希快照，无法判断变化发生在批准之前还是之后，这正是本工具要消除的不确定性。

`verify` 对该 run 返回 `legacy-unverifiable`。它已经 done，不受新规则影响；新规则只约束此后进入 PUBLISH / FEEDBACK 的推进。

未做过的人工裁决（不是历史批准，不在此表）：L02–L18 共 17 篇教材的 G2 评分至今未做；具身六课的 G3 与 KCR 待用户本人批准（G1 / G2 已于 2026-11-27 登记，见 §2.1）。

## 4. 已知限制

- **审批人仍是一个字符串**。本工具无法从技术上证明 `--approver` 由人输入，这一点与 `gate --pass` 相同。它增加的是"批准对应到具体文件版本"的可追溯性与"变化即拦截"，不是身份认证。
- **范围以产物为准**。未登记为 run 产物的文件不在批准范围内（例如 `CHANGELOG.md`）；需要纳入时用 `--path` 显式追加。
- **哈希是整文件级的**。一处标点改动也会触发拦截，需要重新登记——这是有意的保守选择。
- **自测里的符号链接之外的环境限制**：无。本工具不涉及文件系统特权。
