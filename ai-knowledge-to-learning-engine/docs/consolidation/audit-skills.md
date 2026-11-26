# 审计报告：matt-pocock-skills-zh-cn

- 审计日期：2026-11-26（只读审计，未修改任何仓库文件）
- 仓库路径：`C:\Users\Giant\Desktop\GITCODE\AI-Knowledge\matt-pocock-skills-zh-cn`
- HEAD：`4e01df4`（142 笔提交，工作树干净）；origin = `https://github.com/Vin535LFJ/matt-pocock-skills-zh-cn.git`
- 环境：Windows，Node v20.19.5；审计期间 github.com:443 连接失败，远端状态无法直接核验（见 §6-m）

---

## 1. 技能数量核对

**磁盘实测（Get-ChildItem 递归统计 SKILL.md）：共 37 个**

| bucket | 数量 |
|---|---|
| engineering | 20 |
| productivity | 7 |
| misc | 4 |
| in-progress | 6 |
| deprecated | 0 |
| **合计** | **37** |

另有 `.skills/translate-skill/SKILL.md` 1 个维护者自用翻译技能，不计入对外 37 个（USER-GUIDE §1 同口径）。

**发布清单实测**：`.claude-plugin/plugin.json` 的 `skills` 数组共 **31 条**（`node -e "...p.skills.length"` 输出 `plugin skills: 31`），version 字段 `1.3.1`。构成为 engineering 20 + productivity 7 + misc 4。

**一致性判定：一致（符合仓库规则）**。AGENTS.md 明确规定 in-progress/deprecated 不得进入 README 主清单与 plugin.json；31 = 37 − 6（in-progress）。README.md:11 与 USER-GUIDE §6B 均写明「plugin 发布 31 个」，与实测相符。
注意：plugin.json 与 marketplace.json 的 description 写「37 个技能」，指全仓技能集而非发布数，口径易误读但不构成错误（USER-GUIDE 已澄清）。

**调用方式分类实测**：`rg -l "disable-model-invocation: true" skills -g SKILL.md` 命中 22 个文件 → user-invoked 22 / model-invoked 15，与 USER-GUIDE §2、AGENT-COMPATIBILITY §1 的 22/15 一致。

**回填实测**：`rg -l "本地回填" skills` 恰好命中 4 个 SKILL.md（implement、code-review、diagnosing-bugs、grilling），与 BACKPORTS.md 承诺一致。

## 2. 校验脚本运行结果

| 脚本 | 退出码 | 输出 |
|---|---|---|
| `node scripts/check-translation.mjs` | **0** | 无输出（脚本设计为通过时静默，失败才打印 `✗ 文件: 原因`） |
| `node scripts/audit-english.mjs` | **0** | 无输出（无「单行 ≥8 个 4+ 字母英文单词」的报警行） |

脚本检查内容（读源码确认）：
- check-translation：全部已跟踪 md 的代码围栏配对；SKILL.md frontmatter 的 name/description 存在、name 为 ASCII slug、description ≤1024 字符；README 安装命令不得指向 `mattpocock/skills`、不得指向 `vinvcn/skills-zh-CN`、**必须引用 `vinvcn/mattpocock-skills-zh-CN`**；LICENSE 未被修改且 LICENSE.zh-CN.md 存在。
- audit-english：启发式英文残留扫描（排除代码块、URL、白名单术语），非硬校验。

**弱点**：check-translation 对 README 的断言锚定的是**上游** slug（由 README:27 的上游致谢满足），并不校验本仓库自己的安装命令 slug（`Vin535LFJ/matt-pocock-skills-zh-cn`）；安装命令若被改错但上游致谢仍在，脚本不会拦截。

## 3. 宿主兼容性验证状态（如实区分）

依据 `docs/HOST-VERIFICATION-2026-11-25.md`（含 §8 晚间补充）与 `docs/USER-GUIDE.md` §7/§9/§15。

### 3.1 QwenWork（千问办公桌面版 2.1.0，Windows）——唯一有实机记录的宿主，状态「部分验证」

仅测了 2 个技能：`handoff`（user-invoked）、`writing-for-agents`（model-invoked），手动投放到 `C:\Users\Giant\.qwenworkcn\skills\`。

| 层次 | 结果 | 证据 |
|---|---|---|
| 安装 | ✅ 成功 | 逐文件 SHA256 与仓库源一致（记录 §3-A） |
| 发现（宿主设置清单） | ✅ 成功 | 安装后即时可见，用户技能数 18→20，无需重启（§3-B） |
| 发现/加载（安装所在会话） | ❌ 起初失败 | 检索翻 3 页不含目标；加载返回 `Skill not found...`；子代理复核同样失败（§3） |
| 发现/加载（会话重建后） | ✅ 成功 | 两技能检索均第一候选命中，宿主技能加载工具真实载入（§8） |
| 执行 handoff | ✅ 成功 | 交接文档写入系统临时目录、含 Suggested skills 节（§8-D） |
| 执行 writing-for-agents | ✅ 成功（夹具） | 临时 AGENTS.md 夹具上按技能改写并量化前后差异（§8-D）；另有真实修改旁证：Engine 仓库提交 `4951d99`（本审计已在 Engine 仓库核实该提交存在，按 context pointer 写法给根 AGENTS.md 补技能指针） |

**仍未验证（记录自认）**：全新会话（关闭重开应用）的表现；`disable-model-invocation` 是否被宿主尊重；`agents/openai.yaml` 是否被读取；其余 35 个技能。因此整体保持「部分验证」，不得升级为「已验证」。
旁证：本审计会话的可用技能目录中确实包含 handoff 与 writing-for-agents（用户级安装持续存在）。

### 3.2 其他宿主——运行时层面全部未验证

- **Claude Code / Codex / OpenCode / Cursor / VS Code Copilot / ZCode**：AGENT-COMPATIBILITY.md §4/§11 声称在 `skills@1.7.1`（Node v22.22.2 环境）完成「安装器识别 + 文件投放 + 逐字节一致」（仅③层），**运行时发现与实际调用一律未验证**。且该文档数字陈旧（写 14 技能，见 §6-c），仓库内无 `.claude/`、`.agents/`、`.zcode/`、`skills-lock.json` 等安装产物（均被 .gitignore 排除且不存在）。USER-GUIDE §9 据此判「未验证」。
- **WorkBuddy**：全流程未验证，不在 installer agent 列表，历史曾注册失败（AGENT-COMPATIBILITY §4.2、USER-GUIDE §9）。
- **npx 安装器路径在本机未实测**：本机 Node v20.19.5 < skills CLI `engines.node >=22.20.0`（USER-GUIDE §6A/§15.2；本审计实测 node --version = v20.19.5）。
- 未tracked 的 `.workbuddy-ai/memory/2026-10-09.md` 第九轮记录声称曾推送全量版并用旧 slug 实测 `Found 37 / Installed 37`（迁移场景），属历史消费侧记录，非仓库内可复核证据。

**结论**：已验证「安装→发现→加载→执行」全链路的只有 QwenWork 上的 2 个技能，且限「会话重建后」条件；其余宿主最多到「安装器写文件」层，其余 35 个技能在一切宿主上均未验证。

## 4. 上游同步机制

**双上游结构**（UPSTREAM.md、`git remote -v` 实测）：

| remote | 仓库 | 角色 |
|---|---|---|
| upstream-en | `mattpocock/skills` | 英文内容来源 |
| upstream-zh | `vinvcn/mattpocock-skills-zh-CN` | 中文翻译来源、**直接基线**（沿用其 Git 历史） |
| origin | `Vin535LFJ/matt-pocock-skills-zh-cn` | 本仓库公开发布远程 |

**基线**（UPSTREAM.md/BACKPORTS.md）：中文上游 HEAD `bf98e53`（2026-10-08）= 英文上游 v1.3.1 tag `24fe0ef`；建库时英文 HEAD 已前进到 `b0618bc`，**本仓库未整体同步到该 HEAD**，仅按需回填 4 处（依据区间 `24fe0ef..b0618bc`，每处附上游完整 SHA 与 diff）。

**同步方式**：skill-guided content localization，**不做 Git fork-sync**。流程（SYNC.md §0–5）：fetch 两上游（不合并）→ 按基线 SHA 比较差异 → 先读 `.skills/translate-skill/SKILL.md` 再刷新（只译自然语言，保留 identifiers/命令/路径/代码块；术语以 TRANSLATION-GLOSSARY.md 为准）→ 保持全量 37 → **重新应用 4 处回填**（grep "本地回填" 须恰 4）→ 验证（37/4/31、两脚本、可选 `npx skills add . --list` 与 `claude plugin validate . --strict`）→ 提交推送 origin。

**最近一次同步记录**（SYNC.md「同步记录」）：2026-10-08 中文上游同步 `mattpocock/skills@24fe0ef`（v1.3.1），维护 commit `f659bb3`；本仓库自身记录止于 2026-10-09「收口为全量发行副本 37 + 4 回填」。`git log --grep=sync` 证实此后无新的上游同步提交（后续均为 docs/custom/作者重写）。上游新增 `in-progress/chief-of-staff` 未收录；tdd/to-tickets/handoff 等 5 组上游改动明确「未回填」（BACKPORTS.md 末节）。

**CONTRIBUTING.md**：只覆盖术语翻译流程（issue 请求 → 维护者决定入术语表 → 认领 PR 落地 → 状态 applied）；内容刷新仍由维护者按 translate-skill 执行。PR 检查清单要求先 `git add` 再跑两脚本（脚本只扫已跟踪文件）。

## 5. 独立存在理由评估

**支持独立存在的要素（均有实证）**：
1. **独立发布身份**：公开 origin（Vin535LFJ），README/安装命令/marketplace 均指向本仓库；改名提交 `4b1861e`（custom → zh-cn）已落地。
2. **独立内容差异**：4 处经英文上游验证的最小回填（跨工具「Skill 工具」调用措辞、code-review 前台并行、diagnosing-bugs 造红自证、grilling 措辞约束），中文上游没有；BACKPORTS.md 提供逐条上游 SHA 与重新应用方法。
3. **独立同步/维护机制**：SYNC.md + UPSTREAM.md + BACKPORTS.md + translate-skill + 两个校验脚本，形成可重复的刷新流程。
4. **多客户端分发需求**：npx skills 安装器（多 agent）+ Claude Code 单 plugin marketplace（`.claude-plugin/marketplace.json` 实测存在，唯一 plugin `mattpocock-skills`）。但分发仅「文件层」被历史验证，运行时层只有 QwenWork 部分验证（§3）。

**版本 tag 指向（实测）**：

| tag | peeled 提交 | 日期 | 内容 |
|---|---|---|---|
| v1.1.0 | `f2b2464` | 2026-07-23 | Merge PR #17（vinvcn/codex/sync-upstream-ed37663） |
| v1.2.3 | `47500f8` | 2026-09-14 | docs: drop the obsolete tarball fallback（annotated，tagger vinvcn） |
| v1.3.1 | `5be0dc1` | 2026-10-08 | 全仓翻译 Markdown 标题（Option B）PR #41；tag 消息「v1.3.1：同步上游 mattpocock/skills@24fe0ef」 |

三个 tag 均**继承自中文上游历史**。2026-11-26 作者重写（8 笔定制提交改作者为 Vin535LFJ）后，`git merge-base --is-ancestor <tag> HEAD` 对三者均返回 1：**tag 全部指向重写前的孤儿历史，未随重写移动**（README:13 自认）。plugin.json version=1.3.1 与 tag 名对应，但当前内容基线是 bf98e53+4 回填。
重写保真核验：HEAD 142 = 上游 133 + 定制 9（8 笔重写 + 1 笔重写注记 `4e01df4`）；`HEAD~1` 与 `refs/original/refs/heads/main`（141 笔）的**去重 tree 集合相等**（实测 True），支持 README「内容逐一保留」 claims；旧 SHA（`7326522`、`4604bd6`、`186e725`）仅经 refs/original 可达。

**与 Engine 内部技能是否重复：不重复**。`ai-knowledge-to-learning-engine/.agent/skills/` 实测仅 2 个技能：`learning-experience-design`、`research-to-learning`（另 `.workbuddy-ai/skills/research-to-learning` 为镜像），frontmatter 自述为 Engine 内部专属；与本仓 37 个技能名零重叠。Engine 根 AGENTS.md:17 的技能指针只指向其自有 2 技能（提交 4951d99）。本仓 handoff/writing-for-agents 装在**用户级**目录，与 Engine 项目级技能互补而非重复。

**综合判定**：独立存在理由**成立但属「发行与维护层」**——技能内容 100% 派生自上游，独立价值在于中文全量发行身份、4 处回填、同步流程与多客户端打包。短板：tag 与新历史脱节；「独立分发」的运行时证据薄弱（仅 1 宿主 2 技能部分验证）；相对中文上游的增量很小（4 处最小回填），若中文上游吸收这些修复，独立理由将进一步减弱。

## 6. 过时/问题清单（按严重度）

a. **旧 slug 与 Render_Notes 扫描结果**：对全仓（含隐藏与忽略文件，`rg -uu -g "!.git"`）扫描，`Render_Notes` **0 命中**；`mattpocock-skills-zh-CN-custom` 在**已跟踪文件中 0 命中**（改名提交 4b1861e 有效），仅命中未跟踪的 `.workbuddy-ai/memory/`（4 处，见 b）。

b. **未跟踪记忆文件与现身份冲突**（`.gitignore:4` 排除 `.workbuddy-ai/`，`git ls-files` 确认未跟踪）：`.workbuddy-ai/memory/MEMORY.md:1` 标题仍为「mattpocock-skills-zh-CN-custom · 项目长期约定」，硬约束写「**只发布 14 个技能**，不得重新引入其余技能」，与当前「全量 37」身份直接矛盾；`2026-10-09.md:4,12` 仍用旧目录名/旧远程 slug。虽不进发布包，但作为本地 agent 记忆可能误导后续会话。

c. **AGENT-COMPATIBILITY.md（已跟踪）严重陈旧**：§0/§2-L4/§5 写「7 个 user-invoked」（实测 22）；§6 写 `Found 14 skills`、plugin.json「14 条」（实测 31）；§9 A1/A2 期望 14、A5 期望 7；§6.2/A11 声称远程 main=`186e725`、「全量 37 版本尚未推送」——本地 origin/main=HEAD=`4e01df4`，README:13 称已 force-with-lease 推送，该文档明显停留在建库初期。README:8 已提示「部分 14 技能数字过时」，但文档本体未修。

d. **错误安装命令**：`skills/in-progress/README.md:8` 仍写 `npx skills@latest add vinvcn/mattpocock-skills-zh-CN --skill=<name>`（指向上游而非本仓库）。USER-GUIDE §15.4 记录了此问题但引用行号 12，实测在第 8 行。

e. **em-dash 数字过时且恶化**：USER-GUIDE §15.7 写「17 个 md、109 处」；本审计实测已跟踪 md 中 **19 个文件、113 处** `—`。AGENTS.md 明令禁用破折号，而 SYNC.md/UPSTREAM.md/BACKPORTS.md 的标题自身即含「—」。

f. **验证锚点 SHA 失效**：USER-GUIDE frontmatter `verified_against: 7326522`、HOST-VERIFICATION §1 引用 `4604bd6`，两者在作者重写后均**不再是 HEAD 祖先**（实测 is-ancestor 返回 1，仅 refs/original 可达）；USER-GUIDE 页脚「最后验证/最近更新 2026-11-23」与 frontmatter `updated: 2026-11-25` 自相矛盾。

g. **悬空文档**：`docs/engineering/resolving-merge-conflicts.md` 存在（实测 True），对应技能已随上游 v1.3.1 删除（SYNC.md 同步记录）。

h. **翻译残留（与 USER-GUIDE §13.5 自认一致）**：`triage/SKILL.md:7` `# Triage`、`wizard/SKILL.md:6` `# Wizard` 为英文 H1；`to-questionnaire/SKILL.md:23` `# <Questionnaire title>`、`writing-fragments/SKILL.md:45` `# Working title` 实为**模板占位示例**而非「未翻译标题」，USER-GUIDE 称「占位标题」措辞欠准。

i. **Node 版本口径冲突**：AGENT-COMPATIBILITY §6.1 称「本机实测 v22.22.2」，USER-GUIDE 称「本机 v20.19.5 未实测」——系不同机器/时期记录未标注；本审计实测当前机器 v20.19.5，安装器路径在本机确实不可测。

j. **tag 未随历史重写移动**（README:13 自认）：v1.1.0/v1.2.3/v1.3.1 全部指向孤儿历史；若按 tag 发布或 `git describe` 将失效，需重新打 tag 或移动。

k. **description 口径**：plugin.json/marketplace.json description「37 个技能」vs 实际发布 31（指全仓，README/USER-GUIDE 已澄清，易误读非错误）。

l. **校验脚本弱点**：check-translation 的 README 断言只锚定上游 slug，不校验本仓库安装命令 slug（§2）。

m. **远端核验受阻**：`git ls-remote origin main` 失败（github.com:443 连不上）。「已推送」仅有本地 origin/main 引用（=HEAD）、README:13 与未跟踪记忆记录佐证，本审计无法独立确认 GitHub 侧状态。

## 7. 总体结论

- 数量口径健康：磁盘 37、发布 31、回填 4、user-invoked 22，全部实测吻合，两校验脚本 exit 0。
- 兼容性主张总体诚实：文档明确区分「安装器识别 / 文件投放 / 宿主发现 / 真实调用」，唯一全链路证据是 QwenWork 上 2 个技能的部分验证（会话重建后），其余一律未验证。
- 独立存在理由成立（独立发行身份 + 4 处回填 + 同步机制 + 多客户端打包），与 Engine 内部技能无重复；但增量小、tag 脱节、运行时证据薄。
- 主要债务集中在**文档陈旧**：AGENT-COMPATIBILITY.md 的 14/7 旧数字与旧远程 SHA、in-progress README 的上游安装命令、未跟踪记忆中的旧 slug 与「只发布 14」硬约束、失效的验证锚点 SHA、悬空文档与 em-dash 违规。建议按 §6 清单逐项修复（本次审计未做任何修改）。