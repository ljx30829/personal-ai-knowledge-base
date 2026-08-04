---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - ../../sources/inventory/automations.json
next_review: 2026-09-04
---

# 自动化目录

## 当前配置快照

| 自动化 | 状态 | 配置周期 | 工作区 |
| --- | --- | --- | --- |
| ArmorHue B2B daily lead discovery | `ACTIVE` | 每天 19:30 | `D:\codex` |
| ArmorHue B2B daily email sender | `ACTIVE` | 每天 21:30 | `D:\codex` |
| ArmorHue B2B daily supervisor | `ACTIVE` | 每天 22:20 | `D:\codex` |
| ArmorHue TikTok/IG/FB/WhatsApp execution queue | `ACTIVE` | 周一至周六 18:40 | `D:\codex` |
| ArmorHue Daily SEO Traffic Monitor | `ACTIVE` | 每天 09:30 | `D:\codex` |
| 监督 Yufeng P18 线程 | `PAUSED` | 每 30 分钟 | `D:\codex` |
| UUMit 统一巡航 | `PAUSED` | 每 5 分钟 | 未配置工作区 |
| memory-writing-agent-phase-2 | `METADATA_MISSING` | 未知 | 未知 |
| memory-writing-agent-phase2 | `METADATA_MISSING` | 未知 | 未知 |
| phase2-memory-writing-agent | `METADATA_MISSING` | 未知 | 未知 |

时间按当前 Codex 本地配置理解。精确 RRULE 和路径见 [自动化机器清单](../../sources/inventory/automations.json)。

## 状态解释

- `ACTIVE` 只表示自动化配置启用，不证明最近一次业务执行成功。
- `PAUSED` 表示配置存在但当前暂停。
- `METADATA_MISSING` 表示目录存在但没有可解析的 `automation.toml`；不能据此判断任务正在运行。
- 业务真相必须以最新日期日志、健康报告、发送记录、证据矩阵和项目 `TASK_STATE.md` 为准。

## 安全与执行边界

- 清单只读取 `name`、`status`、`rrule` 和 `cwds`，不导入自动化提示词或 `memory.md` 正文。
- 自动化启用不等于授权扩大。发送邮件、社交互动、WhatsApp、发布、部署和线上修改仍需满足对应授权规则。
- 邮件发送必须区分 `Sent`、`Failed`、`BLOCKED_NO_SEND`、演练和待审核记录。
- 社交自动化是人工审核的执行队列，不是无人监管的批量发送器。
- `$env:CODEX_HOME` 可能为空；需要更新自动化记忆时使用已确认的绝对路径，并在写后回读。

## 复核方法

1. 重新运行 `python scripts/build_workspace_inventory.py --output sources/inventory`。
2. 查看自动化配置状态与时间是否变化。
3. 到对应工作区核对最新 `TASK_STATE.md` 和日期证据。
4. 更新本页快照日期、业务状态和未知项。

## 未知项

- 三个缺少元数据的记忆写入目录可能是历史残留、迁移中目录或仅保存记忆；未经用户确认不删除。
- 配置状态可能在本次快照后改变，执行前重新读取。

## 来源与证据

- [自动化机器清单](../../sources/inventory/automations.json)
- `C:\Users\26014\.codex\automations`
