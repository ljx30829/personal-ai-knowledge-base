---
updated: 2026-08-04
status: VERIFIED_CURRENT_SCRIPTS_RUNTIME_GATED
confidence: HIGH
sources:
  - D:\codex\AGENTS.md
  - D:\codex\TASK_STATE.md
  - D:\codex\PROMOTION_WORKFLOW.md
  - D:\codex\output\armorhue-b2b-leadgen-run-20260605
next_review: 2026-08-05
---

# ArmorHue 外贸线索、邮件与监督执行手册

本手册把线索发现、发送包、SMTP 身份探测、真实发送、社交准备和监督分成独立步骤。所有命令都必须从当前项目状态恢复；脚本存在不代表当天具备发送资格。

## 固定入口

```text
工作区：D:\codex
输出根：D:\codex\output\armorhue-b2b-leadgen-run-20260605
发现脚本：build_20260804_leads.py
发送包脚本：build_20260804_domain_send_pack.py
SMTP 认证探测：test_zoho_smtp_auth_probe.ps1
发送器：zoho-smtp-send-day21-domain.ps1
```

文件名带日期或 `day21` 是历史命名，不表示可跳过当天状态检查。新批次优先生成日期化新文件，避免覆盖历史日志。

## 一、每次开始前

从 `D:\codex` 依次读取：

1. `AGENTS.md`。
2. `TASK_STATE.md` 最顶部的最新批次。
3. `PROMOTION_WORKFLOW.md`。
4. 对应自动化的 `memory.md`，只用于恢复，不复制进知识库。
5. 最新 discovery、sender、supervisor 和 social 健康报告。
6. 全部历史发送日志与抑制证据。

若最新 supervisor 是 `BLOCKED_NO_SEND`，发现流程仍可做只读研究，但发送流程必须停止，直到指定复核完成。

## 二、线索发现（永不发送）

当前脚本是固定批次脚本，无命令行参数：

```powershell
Set-Location D:\codex\output\armorhue-b2b-leadgen-run-20260605
python .\build_20260804_leads.py
```

输出至少应包含新的日期化候选 CSV 和 discovery 健康报告。候选表关键字段分为：

- 身份：`Lead ID`、`Company Name`、国家/地区/城市、官网。
- 联系入口：公开业务邮箱、联系表、公开社交入口。
- 适配证据：业务类型、主要服务、产品兴趣、实体经营、近期活动、来源 URL 和验证来源。
- 决策：Lead/Intent Score、Priority、推荐渠道、适配理由、风险说明、语言语气、首个报价路径。
- 草稿：主题和邮件正文，仅为准备，不是发送证明。

发现门：

```text
[ ] 来源是公开的官方业务页面
[ ] 官网和业务适配有日期化证据
[ ] 联系入口是公开商业入口，不是推断的私人信息
[ ] 已对历史邮件、网站域名和抑制记录去重
[ ] A 级同时满足适配、入口、证据和无碰撞
[ ] CAPTCHA / 429 / 登录墙 / 异常空结果已停止并记录
[ ] 本步骤发送数为 0
```

## 三、构建发送包

当前构建器会扫描历史候选、历史发送和风险文本，并给安全上限内的行写入 `Ready`：

```powershell
Set-Location D:\codex\output\armorhue-b2b-leadgen-run-20260605
python .\build_20260804_domain_send_pack.py
```

发送包除候选字段外，还必须有：

```text
Cleaned Email / Subject Used / Send Status / Reply Status
Bounce Status / Unsubscribe Status / Actual Send Time / Actual Channel
Next Action / Notes / Source Candidate File
```

`Ready` 只表示构建器筛到候选，不表示邮箱复核已完成，更不算真实发送。人工抽查每条的官网、收件身份、文案、STOP/opt-out 说明和来源文件。

## 四、SMTP 身份与认证探测

凭据只放在本机受控环境文件或临时环境变量中，不读出、不显示、不提交。探测脚本只做 AUTH，不发送消息：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\test_zoho_smtp_auth_probe.ps1
```

通过条件：

- `ZOHO_SMTP_USER`、`ZOHO_SMTP_FROM`、`ZOHO_SMTP_REPLY_TO` 都以 `@armorhue.com` 结尾。
- 当前允许的发件身份是 `samples@armorhue.com`；不得临时换 QQ、Gmail 或其他免费邮箱面向客户发送。
- AUTH 探测为 PASS 且明确 `message_sent=NO`。

SMTP AUTH 通过不等于邮件风险复核通过。Zoho IMAP/POP 不可用时，必须在 Zoho Webmail 人工检查退信、回复、STOP/退订、投诉、负面回复和审核时间。

## 五、发送预演

不带 `-Send` 时，发送器只预演：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\zoho-smtp-send-day21-domain.ps1 `
  -SendPackCsv '<SEND_PACK_CSV>' `
  -DelaySeconds 45 `
  -MaxSends 12
```

预演必须确认：只处理 `Ready`、跳过 `Sent` 和非 Ready 行、上限不超过 12、间隔不少于 45 秒、没有历史域名/邮箱碰撞和抑制命中。预演输出不计发送。

## 六、真实发送的硬门

只有当前任务明确授权，并且下列全部 PASS 才可执行：

```text
[ ] 最新 supervisor 没有 NEXT_EMAIL_SEND_BLOCKED_NO_SEND
[ ] Zoho/人工邮箱风险复核发生在上一批发送之后
[ ] 域名发件身份、From、Reply-To 和 SMTP AUTH 均通过
[ ] 历史 Sent、退信、退订、投诉、负面回复、域名/邮箱去重均通过
[ ] 发送包已人工抽查且仍是 Ready
[ ] MaxSends <= 12，DelaySeconds >= 45
[ ] 用户明确授权本批目标和真实发送
```

获授权后的显式命令格式：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\zoho-smtp-send-day21-domain.ps1 `
  -SendPackCsv '<SEND_PACK_CSV>' `
  -Send `
  -Confirm SEND_DAY21_DOMAIN `
  -DelaySeconds 45 `
  -MaxSends 12
```

确认口令只是最后一道机械门，不能替代前述业务授权和邮箱风险复核。

## 七、发后核对与监督

1. 直接回读本批 CSV，不依赖终端退出码。
2. 精确统计 `Sent`、`Failed`、`Ready`、`BLOCKED_NO_SEND`；只将 `Sent` 计为发送。
3. 核对 `Actual Send Time`、`Actual Channel` 和剩余 Ready 行。
4. 立即做 Zoho Webmail 人工风险复核；IMAP 不可用不能由 QQ 审计替代。
5. 生成日期化 sender 健康报告。
6. supervisor 重新汇总 discovery、sender、social 和历史日志，写回 `D:\codex\TASK_STATE.md` 并回读。
7. 社交 CSV 只有 action log 中的真实动作才能计触达；准备队列仍为 0 动作。

## 2026-08-04 最新证据快照

- discovery：10 个接受机会，A=7、B=3；本步骤无发送。
- sender：day44 日志有 12 个精确 `Sent`，0 Failed，发送后历史主日志合计 311 个 `Sent`、308 个唯一邮箱。
- supervisor：Zoho IMAP 仍不可用，下一批邮件为 `BLOCKED_NO_SEND`，直到完成发送后的 Zoho Webmail 人工风险复核或恢复 IMAP/POP。
- social：100 行均需人工复核，动作日志 0。

这是日期化历史事实，不是下一次发送授权。

## 故障矩阵

| 现象 | 处理 |
| --- | --- |
| SMTP AUTH 失败 | 停止发送，检查本机秘密配置和 Zoho 状态，不输出密码 |
| IMAP 提示未启用 | 记录 `BLOCKED_NO_SEND`，转人工 Zoho Webmail 复核或由管理员启用 |
| 发现历史碰撞/退订/投诉 | 抑制该邮箱与必要的域名范围，不靠改写地址绕过 |
| 出现 429/异常活动/安全警报 | 立即停止剩余发送并保留日志 |
| CSV 仍有 Ready 但脚本退出 0 | 只说明上限或跳过逻辑完成，不能把 Ready 算 Sent |
| 社交平台需要登录/验证码 | 停止自动化，等明确账号、目标、动作和时间授权 |

## 跨设备恢复

1. 先按 [工作区迁移指南](../system/workspace-portability-guide.md) 恢复 `D:\codex` 项目代码和历史日志。
2. 在新设备重新配置邮箱秘密；知识库不迁移凭据。
3. 重新做全历史去重与抑制，不只复制最新候选 CSV。
4. 先跑发现、发送包、AUTH 探测和发送预演。
5. 新设备第一批真实发送默认阻塞，直到人工确认邮件风险和当次授权。
6. 新建自动化时按 [自动化重建指南](../system/automation-rebuild-guide.md) 先保持暂停。

## 记录模板

```text
日期：YYYY-MM-DD HH:mm +08:00
批次：<BATCH_ID>
发现：A=<N> B=<N> C=<N> / SEND=0
发送包：Ready=<N> / 审核=<PASS|FAIL>
身份：PASS | FAIL
SMTP AUTH：PASS_NO_MESSAGE | FAIL | NOT_RUN
邮箱风险复核：PASS | BLOCKED | UNKNOWN
真实发送授权：YES | NO
发送：Sent=<N> Failed=<N> Ready=<N> Blocked=<N>
社交动作：<N>
最终报告：<PATH>
结论：PASS | WATCH | FAIL | BLOCKED_NO_SEND
```

## 相关文档

- [外贸运营原则](foreign-trade-operations.md)
- [自动化重建指南](../system/automation-rebuild-guide.md)

