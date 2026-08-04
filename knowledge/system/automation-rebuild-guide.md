---
updated: 2026-08-04
status: VERIFIED_SPEC_ONLY
confidence: HIGH
sources:
  - ../../sources/inventory/automations.json
  - automation-catalog.md
next_review: 2026-08-11
---

# Codex 自动化跨设备重建指南

自动化目录不能像普通知识一样直接复制后就假设可运行。另一台电脑需要重新确认工作区、时区、调度能力、提示词、安全门和输出路径。本页只保存可复建规格，不复制原始提示词和 `memory.md` 正文。

## 先区分三种状态

- `ACTIVE`：配置处于启用状态，不证明最近一次业务成功。
- `PAUSED`：配置存在但暂停；迁移后也应先保持暂停。
- `METADATA_MISSING`：只有历史目录，当前用途、周期和工作区均未知，不能补造或删除。

知识库在电脑关机后仍可从 GitHub 查看；本地自动化不会凭空继续运行。若目标 Codex/AI 没有免费的云端调度能力，就只能在设备开机时运行，或另行使用持续在线主机。当前知识库不承诺任何免费平台可长期代跑。

## 当前 10 个重建规格

| 名称 | 计划（本地时区） | 工作区 | 重建目的 | 默认权限 |
| --- | --- | --- | --- | --- |
| ArmorHue B2B daily lead discovery | 每天 19:30 | `D:\codex` | 公开来源发现、去重、分级、生成候选与健康报告 | 只读/不发送 |
| ArmorHue B2B daily email sender | 每天 21:30 | `D:\codex` | 对已审核队列执行发送门和受控发送 | 高风险，默认暂停 |
| ArmorHue B2B daily supervisor | 每天 22:20 | `D:\codex` | 汇总 discovery/sender/social 的最终证据并写状态 | 只读监督 |
| ArmorHue TikTok/IG/FB/WhatsApp 100 touchpoint execution queue | 周一至周六 18:40 | `D:\codex` | 生成/审核社交触点队列 | 准备阶段不发送 |
| ArmorHue Daily SEO Traffic Monitor | 每天 09:30 | `D:\codex` | 只读检查网站、SEO、分析证明与阻塞 | 不修改线上系统 |
| 监督 Yufeng P18 线程 | 每 30 分钟 | `D:\codex` | 历史线程监督 | 保持暂停，先确认任务仍存在 |
| UUMit 统一巡航 | 每 5 分钟 | `UNKNOWN` | 历史巡航任务 | 保持暂停，工作区未知 |
| memory-writing-agent-phase-2 | `UNKNOWN` | `UNKNOWN` | 历史记忆写入目录 | 不重建、不删除，待确认 |
| memory-writing-agent-phase2 | `UNKNOWN` | `UNKNOWN` | 历史记忆写入目录 | 不重建、不删除，待确认 |
| phase2-memory-writing-agent | `UNKNOWN` | `UNKNOWN` | 历史记忆写入目录 | 不重建、不删除，待确认 |

## 通用重建顺序

1. 在目标电脑先恢复对应项目工作区；只克隆本知识库不够。
2. 在项目根目录读 `AGENTS.md`、`TASK_STATE.md`、相关运行手册和最新日期证据。
3. 确认目标平台支持调度、时区为 `Asia/Shanghai` 或按用户决定转换。
4. 新建自动化时先设为暂停，工作目录使用目标电脑的真实绝对路径。
5. 用下面的安全契约重新撰写最小提示词；不要从旧 `memory.md` 复制可能过期的业务状态。
6. 手工运行一次只读或 dry-run 任务，检查输出路径、状态写回和重复执行安全性。
7. 只读任务通过后才能启用；发送、发布、部署类任务仍需单独确认授权与风险门。
8. 运行后以最终文件和精确状态计数验收，不以任务显示 `ACTIVE` 或进程退出 0 验收。

## 每个提示词必须包含的安全契约

```text
先读 AGENTS.md、TASK_STATE.md、相关 runbook、自动化记忆和最新日期证据。
不读取或显示密码、Cookie、token、API Key、SMTP 密码、邮箱正文或浏览器资料。
没有明确目标与当次授权时，不发送、不发布、不提交表单、不改 Shopify/Admin、不部署。
发现、发送、社交准备和监督分开计数；只统计最终日志中的精确结果。
结束后写回日期化报告、TASK_STATE.md 和必要的自动化记忆，并直接回读验证。
```

## 分任务恢复门

### 发现与社交准备

- 输入：公开业务来源、历史去重/抑制记录、目标画像。
- 输出：日期化候选 CSV、来源证据、质量等级、健康报告。
- 必须为 `NO_SEND`；登录墙、验证码、429 或平台风险时停止。
- 社交队列必须保留平台、账号、目标、动作和人工审核状态；队列行数不算触达数。

### 邮件发送

- 新设备上默认 `PAUSED/BLOCKED_NO_SEND`。
- 必须现场确认发件、From 和 Reply-To 都是获准的 ArmorHue 域名身份。
- 必须复核历史已发送、硬退信、退订、投诉、负面回复、邮箱可用性和人工 Zoho Webmail 状态。
- 实际发送上限、节奏和确认口令以最新项目运行手册为准；不得直接照搬旧状态。
- 只把发送日志中的精确 `Sent` 计入结果。

### 监督与 SEO

- 监督只汇总已有证据，不提升状态、不补写发送数。
- SEO 默认只读；`daily_gate PASS` 不等于店铺、GA4/GTM、Shopify Admin 或转化已健康。
- HTTP 429 时页面级字段保持 `WATCH`，不能将不完整 HTML 当成修复依据。

## 验证清单

```text
[ ] 目标工作区存在且不是空壳
[ ] AGENTS.md / TASK_STATE.md / runbook 已读取
[ ] 时区和 RRULE 已确认
[ ] 第一次运行保持暂停或 dry-run
[ ] 没有秘密进入提示词、日志或 Git
[ ] 输出使用日期化文件且不会覆盖历史证据
[ ] TASK_STATE.md 写入后已回读
[ ] 发送/发布/部署任务有独立授权门
[ ] 业务结果由最终日志证明，不由 ACTIVE/退出码推断
```

## 故障处理

| 现象 | 判断与处理 |
| --- | --- |
| 自动化显示启用但无输出 | 检查调度平台是否真正运行、工作目录和状态文件，不先声称成功 |
| 新电脑路径不存在 | 先恢复工作区或修改绝对路径；知识库不会恢复项目代码 |
| 时区错位 | 暂停任务，核对平台时区与本表计划后再启用 |
| 重复发送或重复写入风险 | 停止任务，检查幂等、去重、抑制和历史日志 |
| 三个记忆目录没有配置 | 保持 `UNKNOWN`，不重建、不删除、不合并 |
| 平台不能关机后运行 | 接受仅开机执行，或另选持续在线主机；不假定存在免费替代 |

## 记录模板

```text
自动化名称：<NAME>
重建日期：YYYY-MM-DD HH:mm +08:00
目标平台：<CODEX / OTHER>
工作区：<ABSOLUTE_PATH | UNKNOWN>
时区与计划：<TZ / RRULE>
初始状态：PAUSED | ACTIVE | UNKNOWN
首次验证：DRY_RUN_PASS | WATCH | FAIL | NOT_RUN
最终证据：<DATED_ARTIFACT_PATH>
外部动作：NONE | AUTHORIZED_SCOPE
结论：PASS | WATCH | FAIL | BLOCKED
```

## 相关文档

- [自动化目录](automation-catalog.md)
- [外贸执行运行手册](../trade/foreign-trade-execution-runbook.md)
- [工作区迁移指南](workspace-portability-guide.md)

