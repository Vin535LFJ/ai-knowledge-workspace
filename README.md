# AI Knowledge 工作区（D22 统一收敛后，2026-11-26）

> **一个以知识为核心、由 AI 辅助生产和维护、以课程和学习网站为主要消费方式的知识管理与学习系统。**
> 原五个项目已收敛为**两个仓库**（D22 决策）：核心系统 + 通用 Skills 来源库。整合证据与映射见核心仓 `docs/consolidation/`。

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
5. **`reviews/embodied-batch1/USER-ACCEPTANCE-PACKAGE.md`** — 当前真正卡住的地方：具身六课人工验收（G1 21 条断言 / G2 评分 / 审批顺序），裁决栏全部留空
6. `program/AUDIT-REPORT.md` + `program/audits/` — 独立审计与处置

## 当前状态一句话

核心生产链已真实跑通一次（HDR 批 INTAKE→FEEDBACK done）；具身智能 6 课教材完成、停在人工验收门；D22 整合与多课程切换/检查点练习已上线并浏览器实测，视频 Pilot 精选路径的课程上下文缺陷已修复（下一课/前置/返回链均带课程上下文，三个浏览器场景回归通过）；门禁全绿（validate 20/0/0 · publish 34 · 105 claims 误标 0）。

## 快速开始

```powershell
cd ai-knowledge-to-learning-engine
py -3 tools/build_site.py
py -3 -m http.server 8791 --directory web
# 打开 http://localhost:8791（或双击 web/index.html）
```

## 边界

- 学习站 bundle 只含登记资产（发布边界 v2 默认拒绝）；内部审读/审批/运行态不进站点。
- 在线发布未授权（D02）；公开仓可见性待用户裁决（PD-Q16）。
- 快照仓 `Vin535LFJ/ai-knowledge-workspace` 是扁平快照（无子仓历史），仅供一次性浏览；权威事实源是上面两个仓。