---
doc_id: PROG-INDEX
type: project-index
status: active
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# 项目索引（唯一位置权威）

> **PD-002（2026-11-19）：物理集中到父文件夹 `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\`**，取代 PD-001 的"索引而非迁移"。
> 已移入：办公室 `ai-knowledge-program\` + 项目02/03/04。**项目01 Render_Notes 迁移待完成**——被当前会话沙箱工作区占用（EBUSY），需在非其工作区的会话或关闭本会话后移入（现址仍 `GITCODE\Render_Notes`）。
> 本办公室与各项目平级同在该父文件夹下。路径为 2026-11-19 迁移后实测；任何再迁移必须先改本索引 + 记 PD 决策。
> 父文件夹本身不是 git 仓库；各项目仍是独立仓库，git 历史/远程/未提交改动随目录整体保留。

## 项目 01 · AI Knowledge-to-Learning Engine（核心产品，最高优先级）

| 项 | 值 |
|---|---|
| 本地路径 | **现址** `C:\Users\Giant\Desktop\GITCODE\Render_Notes`（迁移待完成）→ **目标** `...\AI-Knowledge\Render_Notes`。PD-002 迁移时该目录被当前 QwenWork 会话沙箱工作区挂载占用（EBUSY），无法在活跃会话内安全移动；需在非 Render_Notes 工作区的会话或关闭本会话后移入。git 历史/远程/D15+CHG-0001 未提交改动均完好。 |
| 远程 | `github.com/Vin535LFJ/Render_Notes`（master） |
| 角色 | 知识研究 → 证据 → 建模 → 教材 → 实践 → 网站的生产系统 |
| 入口文档 | `.agent/README.md` → `WORKFLOW_STATE.md` / `DECISIONS.md`（D01–D15）/ `reviews/REVIEW_STATUS.md` |
| 治理 | 自有 `.agent/`（constitution/decisions/standards/changes/indexes）+ G1/G2/G3 人工关卡 + KCR 设计 |
| 专属 Skill | research-to-learning（成熟）；learning-experience-design（CHG-0001 新建，试点待确认） |
| 当前续跑点 | **G1/G2 人工裁决（reviews/decision-kit/ 七项）→ P7.2 逐篇**；收口五笔已 push（远端 HEAD=`e848d28`）；G3 未通过；P2 试点按 PD-003 冻结 |

## 项目 02 · Matt Pocock Skills 中文定制版（技能供应库）

| 项 | 值 |
|---|---|
| 本地路径 | `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\mattpocock-skills-zh-CN-custom`（原 `E:\AI-Tools\`，PD-002 跨盘迁入） |
| 远程 | origin（main）+ upstream-en/zh 双远程，SYNC/BACKPORTS 纪律 |
| 角色 | 可复用 Agent 工作方法（37 技能：wayfinder/handoff/implement-spec/writing-for-agents 等） |
| 入口文档 | `README.md` / `AGENTS.md` / `AGENT-COMPATIBILITY.md` / `SYNC.md` |
| 边界 | **不改造成治理平台**（引导文档 §1）；治理代码不得写入本仓库 |
| 当前状态 | main @ `e1936f2`，干净、与 origin 同步（2026-11-19 实测） |

## 项目 03 · Agent Workspace Governance（通用治理基础设施）

| 项 | 值 |
|---|---|
| 本地路径 | `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\agent-workspace-governance` |
| 远程 | 无（本地 git @ `dec60ba`，PD-Q2 已执行；远程待 PD-Q3） |
| 角色 | Portable Governance Kit：宪法/schema/模板/适配器/CLI，可安装到任意项目 |
| 入口文档 | `README.md` / `AGENTS.md` / `constitution/` / `docs/` |
| 种子来源 | Render_Notes D15 基座泛化抽取（CHG-0001 已建 MVP） |
| 当前状态 | **冻结在 MVP**（PD-003）：宪法4/schemas5/templates6/adapters5/cli/tests/examples2/docs3；**25 tests OK（收口复跑）** |
| 下一步 | 冻结期仅记录 Engine 真实协作痛点；解冻=Engine P10 验收通过后做双案例验证 → 经 ADR 裁决反向接入 |

## 项目 04 · GitHub Project Radar（独立情报系统）

| 项 | 值 |
|---|---|
| 本地路径 | `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\github-project-radar` |
| 远程 | 无（本地 git @ `942530b`，PD-Q2 已执行；远程待 PD-Q3） |
| 角色 | 项目发现 + SQLite 每日快照 + 增长计算 + 评分 + 周报 + 人工审批候选导出 |
| 入口文档 | `README.md` / `AGENTS.md` / `config/` / `docs/` |
| 边界 | 不自动导入任何知识库；Token 走环境变量；历史不足不得伪造增长数据 |
| 当前状态 | **冻结在 MVP**（PD-003，离线 fixture，无网络/git 调用）；**38 tests OK（收口复跑）** |
| 下一步 | 冻结期不申请 PAT、不采集；解冻=Engine P8 输入合同就绪后 → 真实采集 → 快照积累 → 首份周报 |

## 辅助资产（非四项目成员，只读参考）

> PD-002 仅迁移项目02 的 custom 源仓库；`E:\AI-Tools\` 下的安装投放产物与其余技能**留在原处**。
> **迁移注意**：凡按旧绝对路径（`E:\AI-Tools\mattpocock-skills-zh-CN-custom` 或 `GITCODE\Render_Notes` 等）引用这些项目的安装脚本、skills-lock、插件配置、Agent 会话工作区绑定，都需按新路径重新核对；Render_Notes 旧会话工作区绑定失效，需在新路径重开会话。

| 位置 | 性质 |
|---|---|
| `E:\AI-Tools\doc-governance` | 独立文档治理技能（H1–H7 + check_links.py）；项目03 吸收规则时注明出处，原件不动 |
| `E:\AI-Tools\skills-zh-full` / `_mp_skills_verify` | 技能安装投放产物；lock 指向 vinvcn 上游而非 custom 仓，映射时如实记录 |
| `E:\AI-Tools\pet-sdk-governance` | 另一项目的治理快照，项目03 第二验证案例候选 |
| `C:\Users\Giant\Desktop\GITCODE\OmniWorld-Engine` / `Mgtv-PetCatMVP-Demo` 等 | 未来治理 Kit 接入候选（引导文档 P3 §1 点名），当前不触碰 |