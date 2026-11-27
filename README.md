# AI Knowledge 工作区（D22 统一收敛后，快照更新于 2026-11-27）

> **一个以知识为核心、由 AI 辅助生产和维护、以课程和学习网站为主要消费方式的知识管理与学习系统。**
> 原五个项目已收敛为**两个仓库**（D22 决策）：核心系统 + 通用 Skills 来源库。整合证据与映射见核心仓 `docs/consolidation/`。

## 本快照对应的源版本

| 源仓 | 提交 | 已推送核实 |
|---|---|---|
| `ai-knowledge-to-learning-engine` | `c36c906`（2026-11-27） | 是 |
| `matt-pocock-skills-zh-cn` | `d6fa00f`（2026-11-26） | 是 |

逐路径 blob SHA 与两个源仓一致（校验结果见快照提交说明）。

## 两个仓库

| 目录 | 职责 | 远端 |
|---|---|---|
| `ai-knowledge-to-learning-engine/` | **核心系统**：知识管理 + AI 辅助研究 + 证据核验 + 课程教材生产 + 离线学习站 + 内部治理（`.agent/`）+ 项目管理（`program/`）+ 外部研究入口（`integrations/github-radar/`）+ 归档（`legacy/`） | `Vin535LFJ/ai-knowledge-to-learning-engine` |
| `matt-pocock-skills-zh-cn/` | **通用 Skills 来源库**：37 技能（发布 31）、双上游同步、4 处回填、多客户端分发 | `Vin535LFJ/matt-pocock-skills-zh-cn` |

原 Program / Governance / Radar 独立仓已退出使用：内容分别并入 `program/`、归档 `legacy/`、并入 `integrations/github-radar/`；原目录（含 git 历史）在 `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge-backups\2026-11-26-consolidation\retired\`，bundle 恢复验证 PASS。

## 30 分钟了解全貌

1. **`ai-knowledge-to-learning-engine/README.md`** — 产品定位、能力、快速开始
2. **`ai-knowledge-to-learning-engine/program/NOW.md`** — 当前主项目 / 阶段 / 任务 / 阻塞 / 下一步（七字段）
3. `program/ROADMAP.md` + `program/decisions/PENDING_DECISIONS.md` — 规划与**需要人拍板的事**
4. `docs/consolidation/TARGET-ARCHITECTURE.md` + `CONSOLIDATION-DECISIONS.md` — 为什么是这个结构
5. **`ai-knowledge-to-learning-engine/reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`** — 具身六课人工验收：**G1（21 条断言）与 G2（六课评分）已于 2026-11-27 由用户裁决并登记**（§2.8、§3.2 已回填；审批记录见 `reviews/approvals/RUN-2026-11-23-embodied-batch1/`）；**G3 与 KCR 仍待用户本人批准**，run 继续 REVIEW / paused。G3 与 KCR 的裁决材料：同目录 `G3-readiness-addendum.md`（含当前版本浏览器验收证据与统一后的执行口径）与 `KCR-RETROSPECTIVE-REVIEW.md`（追溯性提案 KCR-2026-11-002，19 项待逐项裁决）
6. `program/AUDIT-REPORT.md` + `program/audits/` — 独立审计与处置

## 当前状态一句话

核心生产链已真实跑通一次（HDR 批 INTAKE→FEEDBACK done）；具身智能 6 课教材完成，G1 / G2 已裁决并登记，停在 G3 与 KCR 人工门（run 仍 REVIEW / paused，等用户本人批准）；D22 整合与多课程切换/检查点练习已上线并浏览器实测，视频 Pilot 精选路径的课程上下文缺陷已修复（下一课/前置/返回链均带课程上下文，四个浏览器场景回归通过，含末课 L13 的真实点击链路）；门禁全绿（validate 20/0/0 · publish 34 · 105 claims 误标 0）。具身六课：G1 / G2 已裁决并登记（代理代录，身份认证未进行）；G3 与 KCR 待用户本人批准，run 继续 REVIEW / paused。

## 快速开始

```powershell
cd ai-knowledge-to-learning-engine
py -3 tools/build_site.py
py -3 -m http.server 8791 --directory web
# 打开 http://localhost:8791（或双击 web/index.html）
```

## 边界

- 学习站 bundle 只含登记资产（发布边界 v2 默认拒绝）；内部审读/审批/运行态不进站点。
- 在线发布未授权（D02）。
- **仓库可见性（PD-Q16，2026-11-27 已关闭）**：本快照仓与核心仓均为 **Public**，含内部审读 / 运行态 / 裁决材料，对外可见。用户最终决定**暂不调整**（此前"两仓先设 Private"的方案未执行、搁置）。学习站的 publish-allowlist 只管站点内容，**不约束 GitHub 仓库文件可见性**。
- 快照仓 `Vin535LFJ/ai-knowledge-workspace` 是扁平快照（无子仓历史），仅供一次性浏览；权威事实源是上面两个仓。