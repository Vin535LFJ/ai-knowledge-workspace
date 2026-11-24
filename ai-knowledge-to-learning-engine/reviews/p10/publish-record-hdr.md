---
doc_id: P10-PUBLISH-RECORD-HDR
type: review-material
status: active
owner: qwenwork
created: 2026-11-21
updated: 2026-11-21
---

# P10 发布记录 · HDR 批次（RUN-2026-11-20-p10-hdr · PUBLISH artifact）

> **发布口径**：本地学习站 bundle 就绪（web/ 离线站 + content.js 重建）。
> **在线发布（GitHub Pages 等）仍受 D02 约束未授权**——本记录不构成在线发布。

## 发布内容

- 学习站 bundle：**83 docs / 17 sections / 129 terms / 20 lessons / 7 labs / 624 cards / 3129 KB**（build_site 重建实测）
- 本批新增：L19《HDR 视频渲染》入 bundle；L18.next→L19 桥句；K-HDR/K-TONEMAP 概念图；术语 5 条
- 断言台账：**84 claims**（G1 裁决后 **verified 24 / open 53 / conditional 7**，误标 0）；来源 43 条

## 发布前门禁真值（G3 通过后复跑口径）

- validate_site：**12 checks / 0 FAIL / 0 WARN**
- check_chapter_arc：**19 篇 OK**
- review_gate：**84 claims 误标 0**
- test_publish_boundary：**11/11 OK**
- kcr selftest **16/16** · runstate selftest **25/25** · registry **180 条**

## 人工门完成记录

| 门 | 结果 | 依据 |
|---|---|---|
| G1 证据核验 | ✅ 六项升级 verified/high（采纳 AI 推荐授权） | G1-hdr-verification-queue.md 裁决栏已回填 |
| KCR-2026-11-001 | ✅ APPROVED（19 项） | run_state kcr --to APPROVED（22:22 留痕） |
| G2 质量评分 | ✅ **91/100 通过**（23/23/18/17/10，用户本人确认） | G2-L19-deepening.md §5 已回填 |
| G3 发布门 | ✅ passed（approver: user，2026-11-21T22:22:05+08:00） | run_state gate --pass |

## 已知边界（如实）

- 8bit FBO/面板下的 banding 与 black crush 风险已在 L19 正文标注（dither/10-bit 缓解）
- HLG 兼容边界仅 BT.2020 WCG（I19=A 修订后口径，glossary HLG 词条已联动）
- 遗留：验真队列 P07、U1–U5、两处源笔误——均不阻塞本批发布
