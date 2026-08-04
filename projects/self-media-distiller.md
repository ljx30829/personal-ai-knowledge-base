---
updated: 2026-08-04
status: WATCH_PARTIAL_COVERAGE
confidence: HIGH
sources:
  - C:\Users\26014\Documents\自媒体运营\README.md
  - C:\Users\26014\Documents\自媒体运营\TASK_STATE.md
  - ../knowledge/distillation/content-distillation-system.md
next_review: 2026-08-18
---

# 自媒体内容蒸馏器

## 范围

本地优先的 `account_knowledge_distiller`，把公开或用户授权的创作者内容转为逐视频卡、账号报告、方法蒸馏、质量审计和本地关键词索引。工作区是 `C:\Users\26014\Documents\自媒体运营`。

## 已完成

- 支持 JSON/CSV、抖音导出、逐视频页面/媒体捕获导入、转写合并、账号构建和本地搜索。
- 支持抖音账号探测；遇到 JavaScript 验证壳会诚实记录阻塞。
- 支持 D: 上现有 `whisper.cpp` 的批量转写，不依赖付费 API 或重型 Torch 环境。
- 支持质量审计、账号内容蒸馏、基准账号发现和 P0 基准的第一轮公开证据蒸馏。
- 一个现有账号快照为 20/22 转写覆盖，两条因没有可用媒体 URL 保持缺口。

## 当前状态

- `WATCH_PARTIAL_COVERAGE`：工具可用，但账号级结论仍受来源和转写覆盖限制。
- 2026-07-20 的四条用户参考视频已完成本地转写和方法蒸馏。
- 部分抖音账号探测仍为 `blocked-js-shell`；没有授权导出或逐条页面证据时不能称为完整账号蒸馏。

## 阻塞项

- 缺媒体 URL 的内容无法生成真实转写。
- 平台登录/验证壳、缺作者主页和缺后台数据限制归属与商业结果验证。
- OCR、多模态丰富和 UI 尚是可选未来项，不影响当前本地规则型流程。

## 授权边界

- 只处理公开或用户授权数据，不绕过平台权限，不保存或重发第三方视频资产。
- 发布、挂卡、私信、评论、投放和账号连接不属于蒸馏工具的默认授权。
- 创作者的销量、利润、曝光和转化主张需独立证据。

## 恢复步骤

1. 读取工作区 `README.md` 和 `TASK_STATE.md`。
2. 对目标账号先运行准备/导入，再执行质量审计，确认页面、OCR、转写覆盖。
3. 只对证据足够的条目生成精确知识卡，其余标记缺口。
4. 运行测试并检查输出来源引用，再把耐久结论写入本知识库。

## 证据路径

- `C:\Users\26014\Documents\自媒体运营\src\account_knowledge_distiller`
- `C:\Users\26014\Documents\自媒体运营\tests`
- `C:\Users\26014\Documents\自媒体运营\accounts`
- [内容蒸馏方法](../knowledge/distillation/content-distillation-system.md)

