---
doc_id: CONSOL-ARCH
type: architecture
status: active
owner: qwenwork
created: 2026-11-26
updated: 2026-11-26
related_adr: [ADR-0001]
---

# TARGET-ARCHITECTURE · 最终项目结构决策（Phase 1）

## 1. 三方案比较与决定

| 方案 | 优点 | 代价 | 判定 |
|---|---|---|---|
| A 单一主仓（Skills 也并入） | 入口最少 | Skills 的双上游同步、版本 tag、npx/plugin 多客户端分发会被核心仓的发布节奏绑架；上游 133 笔历史与核心仓历史混在一起 | 否 |
| **B 核心仓 + 独立 Skills 来源库** | 核心系统一个入口；Skills 保留独立发行生命周期（审计 skills §5 四要素实证）；仓库数 5→2 | Program/Governance/Radar 需要真实合并而非搬运 | **采纳** |
| C 核心 + Skills + 其他独立仓 | 形式独立 | Governance 对 Engine 零增量（审计 15 项能力 9 项已覆盖）、Radar 无独立发布需求——"独立生命周期"不成立 | 否 |

**决定：方案 B。** 核心仓沿用 `ai-knowledge-to-learning-engine`（保留 43 笔历史与现有远端，避免无必要的重建/作者重写——任务书 §7.3 明确保持已完成的 GitHub 身份处理结果）。正式产品名不变：**AI Knowledge-to-Learning Engine**；工作区品牌 AI Knowledge。

## 2. 最终目录结构（核心仓）

```
ai-knowledge-to-learning-engine/
├── README.md / AGENTS.md / CLAUDE.md      # 产品入口 + Agent 指针（统一入口）
├── DECISIONS.md / CHANGELOG.md / WORKFLOW_STATE.md   # 决策索引 / 历史日志 / 执行续跑点
├── program/                  # ← Program 并入：项目级管理层（PROGRAM/NOW/ROADMAP/PARKING-LOT/
│                             #    PROGRAM-MANAGER/PENDING_DECISIONS/decisions/plans/handoffs/audits/archive）
├── 00-导航与索引 … 08-具身智能/   # 知识资产（领域目录，权威内容源）
├── courses/                  # 课程契约 + 教材 + quiz（video-rendering-journey / embodied-loop-journey）
├── evidence/                 # Source Registry + Claim Ledger（精选发布）
├── knowledge-model/          # Concept / 关系（精选发布）
├── tools/                    # 全部生产与门禁工具（build/validate/publish_boundary/run_state/
│                             #    approval_chain/kcr_impact/kcr/…，含并入的依赖前沿/环检测）
├── web/                      # 离线学习站（零依赖，content.js 为生成物）
├── site-vitepress/           # 在线镜像源（D02 未授权发布；生成物 ignored）
├── .agent/                   # 治理正文：constitution/indexes/skills(LXD+research-to-learning)/decisions/templates
├── reviews/                  # 内部审读/验收/审批证据（不进学习站）
├── integrations/github-radar/  # ← Radar 并入：外部研究入口模块（代码+测试+文档；*.db ignored 本地数据）
├── legacy/                   # ← Governance 整仓归档 + Engine 遗留 .governance 适配产物（只读，不维护，不进学习站）
├── archive/                  # 知识历史归档（D10.4 离线站只读发布）
└── docs/                     # USER-GUIDE + consolidation/（本决策、盘点、映射、验收报告）
```

## 3. 模块边界与权威来源

| 关注点 | 唯一权威 | 生成物/副本 |
|---|---|---|
| 项目目标/优先级/待决 | `program/PROGRAM.md`、`program/decisions/PENDING_DECISIONS.md` | NOW.md 是带日期快照，不是第二事实源 |
| 当前状态 | `program/NOW.md`（项目级，七字段） | Engine `WORKFLOW_STATE.md` 只管执行续跑点；CHANGELOG 只追加历史 |
| 知识内容 | 领域目录 md + frontmatter | document-registry.json（生成物，漂移门禁） |
| 事实与证据 | evidence/claim-ledger.json + source-registry.json | 站点 curated 嵌入（哈希校验） |
| 课程结构 | tools/course.json + courses/*/course.json | content.js courses[] payload |
| 运行态 | .agent/runs/*.json（ignored 本地） | reviews/ 内的摘要与审批记录 |
| 发布边界 | tools/publish-allowlist.json（v2 资产级，默认拒绝） | build/validate 双侧强制 |
| Agent 规则 | .agent/constitution/ | AGENTS.md/CLAUDE.md/.cursor/.gemini/.github 只是指针 |

**去重决定**：Governance 的 `.governance/` 双轨注册表移入 legacy（不再维护）；文档注册表只有 `.agent/indexes/document-registry.json` 一套；运行状态只有 run_state 一套。

## 4. Skills 使用方式

- **项目内 Skill**（LXD、research-to-learning）：留在 `.agent/skills/`，由 AGENTS.md 指针按任务触发。
- **通用 Skills**：独立仓 `matt-pocock-skills-zh-cn`（37/31，双上游同步+4 回填），用户级安装；不建 Skills Registry。
- 已验证边界如实标注：QwenWork 2 技能部分验证（会话重建后），其余未验证。

## 5. Governance 保留方式

- 整仓归档于 `legacy/agent-workspace-governance/`（含 41 测试与 USER-GUIDE 已知缺陷清单，历史价值保留）。
- **Embed**：`check_frontier` / `detect_dependency_cycles` / `_dependency_ids` 并入 `tools/run_state.py`（new 拒绝成环依赖、advance 校验依赖就绪），测试移植。这是审计确认的唯一真实空白填补。
- 不再把 Engine 文档纳入 Governance 13 类枚举（type 词表零交集是设计级不兼容；Engine 14 类小写枚举 + 渐进补齐政策为准）。

## 6. Radar 去向

- `integrations/github-radar/`，定位=研究入口模块，不是独立产品。
- 必改三处（审计 §3）：research.py CWD 相对输出锚定模块根；默认 db/reports 落点 + Engine .gitignore 配套（*.db 绝不入库）；运行命令文档化（独立进程跑测试，避免顶层包名冲突）。
- 人工批准门槛保持代码强制；真实库 schema 升级仍待 PD-Q15；不建摄取端自动化（接通需人工批准候选后另行立项）。

## 7. GitHub 公开/私有边界

- 最终远端：核心仓 + Skills 仓（均沿用现有 Public 远端）+ 快照仓（更新为最终结构）。
- **现状如实声明**：核心仓 Public 且含 reviews/、.agent/、program/ 等内部过程材料（PD-Q16 待决）。本机无 gh CLI、无 API 凭据，**可见性变更只能由用户在 GitHub Settings 操作**；整合不新增密钥/凭据/运行态入库（.db、runs/、memory/ 全部 ignored）。
- 建议（待用户裁决）：将核心仓转 Private，或拆出公开知识子集；在裁决前维持既有公开状态（用户历次推送已授权），不擅自扩大公开面。

## 8. 旧项目去向

| 旧目录 | 去向 |
|---|---|
| ai-knowledge-program/ | 内容并入 program/；原目录（含 .git）移入备份区 `AI-Knowledge-backups/2026-11-26-consolidation/retired/`；bundle 已验证 |
| agent-workspace-governance/ | 源码副本入 legacy/；原目录同上移入备份区 |
| github-project-radar/ | 代码+数据移入 integrations/github-radar/；原目录同上移入备份区 |
| matt-pocock-skills-zh-cn/ | 原地保留（独立仓） |
| 远端 ai-knowledge-workspace | 更新为最终结构快照；是否归档由用户在 GitHub 操作 |
| 远端 engine/skills | 沿用为最终远端，不新建、不删除 |

## 9. 不再建设

独立 Knowledge Repository、Skills/MCP/Tools Registry、通用 Orchestrator、Control Center、调度平台、大型 Dashboard、通用文档管理平台、在线自动发布、自动审批。新增能力一律先过 program/PARKING-LOT.md 四问准入。