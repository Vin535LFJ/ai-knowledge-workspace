---
doc_id: CONSOL-COVERAGE
type: audit
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
---

# REQUIREMENT-COVERAGE · 原始需求 × 现有功能对照

> 状态口径：**已实现并验证** / **已实现部分验证** / **已设计未实现** / **有意不做** / **等待人工**。
> 证据以当日实测为准（门禁输出、审计报告、浏览器 QA），历史报告不作为当前事实。

## 1. 需求演进对照（任务书 §1）

| 阶段需求 | 现状 | 证据 |
|---|---|---|
| 1.1 知识集中管理 + 关联/来源/可信度 | **已实现并验证**：01–08 领域目录、Source Registry 52 条、Claim Ledger 105 条（验证状态/置信度/条件）、Concept 33、Glossary 129 术语、知识图谱页 | validate 20/0/0；review_gate 误标 0 |
| 1.2 AI 辅助检索/分析/提取/查重/更新 | **已实现部分验证**：research-to-learning Skill + INTAKE 查重 + KCR 影响分析（kcr_impact 真实回放）+ 断言登记流程；两个真实批次（HDR、具身）走通 | reviews/p10、reviews/embodied-batch1；selftest 16/16 |
| 1.3 呈现与学习体验（LXD） | **已实现部分验证**：LXD Skill active，L13 教材页 + transform-mvp 实验页两案例，七实验对比度 3.04→6.39 回归；其余 6 实验增强待决（PD-Q9） | PILOT-L13-plan / PILOT-LAB-mvp / labqa 回归记录 |
| 1.4 工作流与 Skills | **已实现并验证**（Engine 内部）：run_state 十阶段 + 审批哈希链 + KCR 五契约 + AGENT_RULES 五规则；通用 Skills 库独立维护（37/31） | selftest_runstate 28、selftest_approval 15；Skills 两脚本 exit 0 |
| 1.5 GitHub 项目发现 | **已实现部分验证**：Radar 发现/评分/人工审核/导出全链路代码+58 测试；真实采集 121 仓一次；**Engine 摄取端未实现**，human_selected=0 | audit-radar.md §2/§4 |
| 1.6 完整工作链 | **已实现并验证一次**（HDR 批 INTAKE→FEEDBACK done，18 artifacts）；具身批停在人工门（设计行为） | RUN-2026-11-20-p10-hdr.json |

## 2. 功能目标对照（任务书 §5）

| 目标 | 状态 | 说明 |
|---|---|---|
| 5.1 知识资料管理 | 已实现并验证 | 目录+元数据+权威位置（DOCUMENTATION_POLICY）；归档 archive/ 只读；无重复维护（注册表漂移门禁） |
| 5.2 AI 辅助研究与整理 | 已实现部分验证 | 9 步流程中 1–8 有工具/先例；第 9 步人工确认由 G1/G3 强制（AI 不自批）。自动化边界在 USER-GUIDE 如实写明 |
| 5.3 知识组织模型 | 已实现并验证 | 全部模型有真实消费方（build/validate/review_gate/站点）；无空壳 Schema（KCR 五契约均有 selftest） |
| 5.4 教程生产 | 已实现并验证 | 3 条课程路径 / 26 份唯一课时（主课程 20 + 具身 6）+ pilot 精选 5 入口（复用主课程内容）+ 38 quiz 题 + 7 实验；课程契约/前置/目标/自检齐全 |
| 5.5 学习网站 | **本轮 P0 修复**：多课程切换 + quiz 呈现此前缺失（bundle 无 quiz payload、教材模式仅主课程）；其余（搜索/术语/响应式/明暗/键盘/Floor）已验证 | 修复后浏览器 QA 见 FINAL-ACCEPTANCE-REPORT |
| 5.6 LXD 内部规范 | 已实现部分验证 | 两案例提炼 + Floor/Reflex/Finish 签发单；新教材/实验页条件已写入 SKILL |
| 5.7 工作流与 Agent 协作 | 已实现并验证（本轮去重） | 硬门禁（validate/publish/review_gate/selftests）与文档约定（AGENT_RULES）区分明确；双轨注册表（.governance）本轮清除 |
| 5.8 GitHub 发现 | 已实现部分验证 | 保持小型研究入口；人工批准门槛代码强制；不建调度平台（有意不做） |

## 3. 有意不做（本轮与既有裁决一致）

独立 Knowledge Repository / 完整 Skills Registry / MCP-Tools Registry / 通用 Orchestrator / Agent Control Center / 多项目调度平台 / 大型 Dashboard / 通用文档管理平台 / 在线自动发布（D02 未授权）/ 自动审批。

## 4. 等待人工（不阻塞整合）

- embodied 六课 G1（21 条）/ G2 评分 / G3 / KCR —— 核心阻塞，材料已备齐。
- PD-Q9~Q16（LXD 推广、课程切换入口已按任务书 P0 执行、源勘误反馈、Governance level 可空、审计档案补档、Radar 真实库升级、公开边界等）。
- Skills 全新会话验证。

## 5. 已知技术债（如实保留）

- Radar 真实库旧 schema（升级待 PD-Q15）；`query` 子命令只读靠自律（审计 §1.2）。
- Skills：tag 指向孤儿历史（不再重写，README 注记）；AGENT-COMPATIBILITY 旧数字（本轮修复）；35 技能运行时未验证。
- Engine：历史 run（HDR）6 个产物哈希与现状不符（后续编辑所致，审批链如实标 legacy/unverifiable）；审批人仍为字符串（无数字签名，如实声明）。
- 公开仓含内部过程材料（PD-Q16，需用户在 GitHub 侧决定可见性）。