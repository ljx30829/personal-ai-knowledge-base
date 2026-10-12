---
updated: 2026-10-12
status: PASS_OFFLINE_ATLAS_READY
confidence: HIGH
sources:
  - docs/workflows/coverage-report.json
  - docs/workflows/diagrams/archify-overview.finalize.json
  - docs/workflows/diagrams/email-outreach.finalize.json
next_review: 2026-11-12
---

# 知识库离线工作流地图

## 目标

把知识库从文档目录提升为可离线浏览的工作系统：先选工作目的，再查看完整流程、底层判断逻辑、人工授权门、对应技能和仓库内完整原文。

## 当前结果

- `PASS_OFFLINE_ATLAS_READY`：入口为 `docs/workflows/index.html`。
- 13 类工作目的、每类 10 个阶段、1 张总览和 13 张独立 Archify 流程图。
- `docs/workflows/index.html` 默认直接内嵌 Archify 总览；进入任一工作目的会把主画布切换到对应交互流程图，文字字段和技能卡作为图下方的证据说明。
- 219 个技能来源实例、161 个不同名称；同名来源没有合并丢失。
- 搜索、来源筛选、重复来源筛选、技能详情、哈希链接、主题切换和本地原文链接可用。
- 真实浏览器已验证 390×844 和 1280×720 下图表非空、流程切换正确、无外层水平溢出且控制台零错误；全量测试与验证结果记录在 `TASK_STATE.md`。

## 真实性边界

- 所有技能卡目前为 `WATCH`，因为很多原文没有显式说明全部结构化字段。
- 分类用于导航。名称不能可靠判断的技能保留“分类待复核”，不能据此声称已经运行。
- 图是指导流程，不代表已经发送、发布、部署或执行外部动作。
- Git 仓库提供文档、源码、配置和离线页面；目标电脑仍需按技能原文验证依赖和环境。

## 恢复与重建

1. 从私有 Git 仓库克隆到短路径。
2. 直接打开 `docs/workflows/index.html`。
3. 需要重建目录时运行 `python scripts/build_workflow_atlas.py . --archify-candidates`。
4. 运行 `python scripts/validate_workflow_atlas.py .` 和 `python scripts/validate_vault.py .`。
5. Archify HTML 已生成，无需在目标电脑重新安装 Archify才能浏览。

## 证据入口

- 使用和限制：`docs/workflows/README.md`
- 覆盖报告：`docs/workflows/coverage-report.json`
- 图表浏览器凭证：`docs/workflows/diagrams/*.browser-check.json`
- 图表最终交付凭证：`docs/workflows/diagrams/*.finalize.json`
- 设计：`docs/superpowers/specs/2026-10-11-knowledge-vault-workflow-atlas-design.md`
- 实施计划：`docs/superpowers/plans/2026-10-12-knowledge-vault-workflow-atlas.md`

