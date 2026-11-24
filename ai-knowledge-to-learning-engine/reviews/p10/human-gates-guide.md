---
doc_id: P10-HUMAN-GATES-GUIDE
type: review-material
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# P10 人工门裁决指引（RUN-2026-11-20-p10-hdr，REVIEW 暂停中）

> 生产链已走通 INTAKE→REVIEW（13+ artifact 全程 hash 留痕）。**PUBLISH/FEEDBACK 被 G3 人工门硬阻塞**——这是设计行为（不变量 1/3），不是故障。以下裁决全部由你执行，AI 不代批。

## 1. 你要裁决的四件事（按依赖顺序）

| # | 事项 | 材料 | 动作 |
|---|---|---|---|
| ① | **G1 证据核验**：V63–V67 升级与否 + V23 边界修订（KCR I19：A 先补条件再升 / B 附条件升 / C 维持 open） | `reviews/p10/G1-hdr-verification-queue.md`（逐条证据定位 + 裁决栏空白） | 填裁决栏；告诉 AI 结果，AI 执行台账更新 |
| ② | **KCR 提案批准**：KCR-2026-11-001（19 项：5 断言 + 8 来源 + L19 + 2 概念 + 课程/桥句联动 + V23 reverify） | `reviews/p10/change-proposal-hdr.json`（human_decision=null） | 批准后执行：`py -3 tools/run_state.py kcr --run-id RUN-2026-11-20-p10-hdr --to APPROVED --approver <你的名字>` |
| ③ | **G2 质量评分**：L19 十维度评分（≥85 通过） | `reviews/G2-L19-deepening.md` §5 判定表 | 填表；AI 不自评 |
| ④ | **G3 发布门**：本地 bundle 已构建验证（83 docs 全绿）；是否认可"发布就绪" | 本指引 §2 验收对照 | 通过后执行：`py -3 tools/run_state.py gate --run-id RUN-2026-11-20-p10-hdr --pass --approver <你的名字>` |

④ 之后 AI 才能 advance 进入 PUBLISH（登记发布记录）→ FEEDBACK（反馈收集）→ done（释放 write_paths）。**在线发布（GitHub Pages 等）仍受 D02 约束，G3 通过 ≠ 授权在线发布**——本批"发布"指本地学习站 bundle 就绪。

## 2. P10 验收标准对照（NOW.md 主目标判据）

| 判据 | 本批实证 | 状态 |
|---|---|---|
| 一批全新真实资料完整走通 | 7 份外部权威源（AOSP×2/ITU×2/UHD Forum/colour-science/UPM）+ 3 份库内 → L19 教材 | ✅ INTAKE→REVIEW 全链 |
| 工作流可重复执行 | run_state 状态机 + 每阶段完成条件硬检查；selftest 25/25 | ✅ |
| 中间产物有明确数据契约 | impact-report / change-proposal / run-state 三契约程序化校验（validate_kcr 四契约） | ✅ |
| 各阶段有质量检查 | 每阶段门禁 + 独立审读（2 blocker+2 major+6 minor 全修复） | ✅ |
| 关键人工审批点明确 | G1/G2/G3 + KCR APPROVED 全部程序强制留给人工 | ✅（本指引） |
| 生成结果在网站正常呈现 | build 83 docs / 624 cards，validate 12/0/0，L19 入 bundle | ✅ 本地（在线待 D02） |
| 知识变更可做影响分析 | impact-v23-baseline（既有链）+ impact-bt2100-new（新链）两份真实报告 | ✅ |
| 失败可定位与恢复 | run_state fail/retry/pause/resume 自测覆盖；本批零失败 | ✅ |

## 3. 恢复命令（裁决后）

```
py -3 tools/run_state.py resume --run-id RUN-2026-11-20-p10-hdr
py -3 tools/run_state.py advance --run-id RUN-2026-11-20-p10-hdr --reason "G3 已通过"   # → PUBLISH
py -3 tools/run_state.py artifact --run-id RUN-2026-11-20-p10-hdr --path <发布记录>
py -3 tools/run_state.py advance ...   # → FEEDBACK → artifact → advance → done
py -3 tools/run_state.py show --run-id RUN-2026-11-20-p10-hdr
```

## 4. 遗留登记（不阻塞裁决）

- U1–U5 见 G1 队列 §4（TextureView 官方出处 / BT.2100 英文原版 / HLG 主观测试 / glossary HLG 边界联动 / 跨课 used_by 惯例）。
- 两处源文档笔误（PSNR dB / 花冠→花瓶）仍待裁（2026-11-20 登记）。
- commit/push 授权积压（Engine 未提交文件持续累积，建议本批裁决后一次性分组提交）。