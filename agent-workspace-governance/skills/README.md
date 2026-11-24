---
doc_id: SKILLS_README
type: skills-index
status: active
owner: governance-kit
created: 2026-11-19
updated: 2026-11-19
---

# 关于 Agent Skills（本工具包不重建技能）

## 定位

本目录**不包含也不实现任何 Agent Skill**。

- **Agent Skills 解决「Agent 如何工作」**——研究、写作、审查等可复用能力。
- 这类能力应当**复用外部技能库**，而不是在本治理工具包里另造一套。

参考技能库：<https://github.com/Vin535LFJ/mattpocock-skills-zh-CN-custom>

## 为什么不放技能进来

1. 治理工具包只负责「协作规则」，Skills 属于「工作能力」，两者关注点不同。
2. 重复造技能集会造成多权威来源，违反治理原则 #2。
3. 技能随外部库演进而更新，本工具包只需要引用指针，不固化副本。

## 本项目如何接入技能

- Agent 注册表（`agent.schema.json`）通过 `supported_skills` 字段声明某 Agent 可用的技能。
- 各 Adapter 可声明「可从外部技能库加载哪些技能」，但只写指针，不复制技能正文。
- 技能的实际能力必须实跑验证，未验证则在 `runtime_verification_status` 标记为 `unverified`。

> 记住：Skills 管「怎么干」，Governance 管「按什么规则协作」。本目录只做后者，前者交给外部库。
