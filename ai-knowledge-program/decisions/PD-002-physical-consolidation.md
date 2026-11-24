---
doc_id: PD-002
type: decision
status: accepted
owner: qwenwork
created: 2026-11-19
updated: 2026-11-19
---

# PD-002 · 四项目物理集中到 AI-Knowledge 父文件夹

- 日期：2026-11-19
- 状态：accepted（用户本轮指令："把几个项目都放在一个新的文件夹下面吧，方便我阅读，统筹管理"；结构化裁决：新建独立父文件夹 + 全部项目物理移入）
- 决策人：用户；执行：qwenwork
- 取代：PD-001 决策 #2/#5 的"保持原位置、索引而非迁移"。PD-001 建立统筹办公室本身仍有效。

## 背景

PD-001 采用索引而非迁移以规避移动活跃仓库的风险。用户复核后明确希望物理集中以便阅读与统筹管理。
实测确认风险可控：git 仓库整目录移动保留历史/远程/未提交改动；P03/P04 尚未 git init（移动零 git 顾虑）；技能库已推送 origin（中断可恢复）。

## 决策

1. 新建父文件夹 `C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\`（独立于办公室，平级容纳各项目）。
2. 物理移入五者：`ai-knowledge-program`（办公室）、`Render_Notes`（01）、`mattpocock-skills-zh-CN-custom`（02，自 E:\AI-Tools 跨盘）、`agent-workspace-governance`（03）、`github-project-radar`（04）。
3. 父文件夹本身不做 git 仓库；各项目保持独立仓库与各自远程。
4. `PROJECT_INDEX.md` 同步更新为新路径，仍是唯一位置权威。
5. 迁移顺序：先移非工作区项目 + 技能库 → 更新办公室文档并验证 → **最后移 Render_Notes**（当前会话工作区，避免沙箱失去锚点）。

## 执行结果（2026-11-19 实测）

- ✅ 办公室 + 项目02（E:→C: 跨盘）/03/04 已移入 `AI-Knowledge\`，旧路径清空，git 完整（技能库 e1936f2 远程保留；办公室提交 a8956c7）。
- ✅ 迁移后验证：P03 **25 tests OK** / P04 **38 tests OK** / Render_Notes validate **11/0/0**、review_gate 正常。
- ⏳ **项目01 Render_Notes 迁移待完成**：`mv` 报 `Device or resource busy`——该目录是当前 QwenWork 会话的沙箱工作区根，被进程持有句柄，活跃会话内无法安全移动（强移/复制后删原均有损工作风险，未做）。仓库完好仍在 `GITCODE\Render_Notes`，HEAD=474c667，D15+CHG-0001 未提交改动保留。
- **收尾路径**：在 workspace 非 Render_Notes 的新会话（如打开 `AI-Knowledge\`）中执行移动，或关闭本会话后移动；移入后更新本索引项目01 路径为最终址。
- ✅ **2026-11-19 收尾完成**：在绑定 `AI-Knowledge\` 的会话中 Move-Item 成功，Render_Notes 现址 `AI-Knowledge\Render_Notes`；旧路径已不存在；git 完好（HEAD=`e848d28`，工作树干净，收口五笔已随 PD-Q1 push）；迁移后只读门禁复跑 validate 11/0/0、review_gate 37 claims 误标 0。PD-002 全部执行完毕。位置权威改由 `PROGRAM.md §4` 承载（PROJECT_INDEX.md 已归档）。

## 后果与注意事项

- **Render_Notes 会话重绑定**：旧工作区 `GITCODE\Render_Notes` 绑定失效，需在新路径 `AI-Knowledge\Render_Notes` 重开会话继续 Engine 主线；其 D15+CHG-0001 未提交改动随目录保留，PD-Q1 收口仍待授权。
- **技能库安装路径**：原按 `E:\AI-Tools\mattpocock-skills-zh-CN-custom` 的 npx skills/插件安装引用需按新路径重核；E:\AI-Tools 的安装投放产物（skills-zh-full 等）未动。
- 沙箱 bash 在迁移中曾触发 ACL 恢复锁，改用宿主执行完成；后续命令以新路径为准。
- 任何再迁移必须先改 PROJECT_INDEX + 记 PD（沿用 PD-001 规则）。