---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - ../../sources/inventory/workspaces.json
  - ../../sources/inventory/skills.json
next_review: 2026-09-04
---

# 工作区地图

本页是路径索引，不是项目备份。独立 Private 仓库、Codex task pack、审阅归档以及目标电脑恢复步骤见 [项目工作区跨设备迁移指南](workspace-portability-guide.md)。

## 当前工作区

| 名称 | 原始路径 | 状态 | 首要入口 |
| --- | --- | --- | --- |
| ArmorHue、外贸与 Shopify | `D:\codex` | `ACTIVE` | `AGENTS.md`、`TASK_STATE.md`、图像与推广工作流 |
| 独立站选品研究 | `C:\Users\26014\Documents\独立站` | `ACTIVE` | `TASK_STATE.md` |
| 自媒体运营与蒸馏 | `C:\Users\26014\Documents\自媒体运营` | `ACTIVE` | `README.md`、`TASK_STATE.md` |
| 技能清单工具 | `C:\Users\26014\Documents\技能` | `ACTIVE` | `README.md`、`TASK_STATE.md` |
| 中转站 | `C:\Users\26014\Documents\中转站` | `CONFIG_ONLY` | 当前只有隐藏配置或 Git 元数据 |
| 节点 | `C:\Users\26014\Documents\节点` | `CONFIG_ONLY` | 当前只有隐藏配置或 Git 元数据 |

`CONFIG_ONLY` 只说明当前工作树没有可见业务文件，不代表历史上没有做过相关工作。中转站和节点的可复用历史应记录在专题页，并标记证据日期和待复核项。

## 使用规则

- 本知识库是索引与交接层，不代替原始工作区。
- 进入项目时先读原工作区的本地说明与状态文件，再用本知识库补充跨项目方法。
- 大型输出、日志、CSV、视频、图片、网页镜像和压缩包留在原路径。
- 路径不存在或移动后，先更新 `sources/inventory/workspaces.json`，再修改本文。
- 不从隐藏目录、环境文件或凭据配置中抽取内容。

## 技能位置

- 用户技能根目录：`C:\Users\26014\.codex\skills`。
- 本次元数据扫描找到 186 个 `SKILL.md` 文件，包括根目录和其子目录中的定义。
- 完整技能清单共 251 条，因为它还统计了插件缓存；两个数字口径不同，均不是错误。
- 技能详细路由见 [技能与路由](skills-and-routing.md)。

## 未知项

- 原始工作区之后可能被移动、重命名或删除；当前状态是 2026-08-04 快照。
- 中转站和节点的现行服务、提供商、端点与健康度不能从空工作树确认，使用前需实时检查。

## 来源与证据

- [工作区机器清单](../../sources/inventory/workspaces.json)
- [技能路径清单](../../sources/inventory/skills.json)
