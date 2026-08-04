---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - D:\codex\TASK_STATE.md
  - D:\codex\PROMOTION_WORKFLOW.md
next_review: 2026-08-11
---

# 外贸运营

真实脚本入口、CSV 字段、SMTP 探测、预演/实发命令、发后复核和跨设备恢复见 [ArmorHue 外贸线索、邮件与监督执行手册](foreign-trade-execution-runbook.md)。

## 可复用流程

1. 从公开官方业务来源发现潜在企业，记录公司、官网、业务适配、公开联系入口和证据日期。
2. 先做历史去重与抑制，再按证据强度分级；弱适配、来源不明或无法验证的线索不进入 A 级。
3. 发现、发送、社交准备和监督是四条独立流水线，不能互相替代证明。
4. 发送前复核发件身份、邮箱可用性、历史已发送、硬退信、退订、投诉、负面回复和人工复核状态。
5. 最终只按发送日志中精确的 `Sent` 状态计数；`Ready`、草稿、演练、阻塞和准备记录均不计入。
6. 每批结束后写回项目状态、证据路径、真实数量、阻塞项和下一步。

## 线索质量门

- A 级需要公开可核验的业务适配、有效业务联系入口、无历史碰撞且通过当次风险检查。
- B/C 级可保留用于研究或人工补证，但不能冒充可发送队列。
- CAPTCHA、HTTP 429、登录墙、异常空结果或官方页面不可用时停止扩展，不绕过平台限制。
- 不推断私人联系方式、地点、身份、客户意向或购买力。

## 发送与社交边界

- 当前 ArmorHue 邮件只允许使用经验证的 ArmorHue 域名身份；任何替代免费邮箱都不能面向客户发送。
- 发件邮箱身份正确不等于可发送。退信、回复、退订、投诉和负面回复的复核门必须同时通过。
- 社交队列必须包含明确平台、账号、目标和动作类型，并在操作时取得授权；准备 100 条不等于执行 100 次。
- 登录墙、验证码、429、异常安全提示、设备或账号风险信号出现时立即停止。

## 2026-08-04 ArmorHue 快照

- 发现：`WATCH_NO_SEND_DISCOVERY_ONLY`，接受 10 个机会，A=7、B=3；发现流程发送 0。
- 当日 sender：day44 日志记录 12 个精确 `Sent`、0 Failed、0 Ready。
- 历史计数：44 个主发送日志中有 311 条精确 `Sent`、308 个唯一已发送邮箱；这是带日期快照，不代表下一批可继续发送。
- supervisor：Zoho IMAP 仍不可用，下一批为 `BLOCKED_NO_SEND`，直到完成 day44 之后的人工 Zoho Webmail 风险复核或恢复 IMAP/POP。
- 社交：100 行全部需要人工复核，动作日志 0。

## 未知项

- 当前邮箱复核、回复、退信、退订和投诉状态未在本知识库中保存，发送前必须到原工作区复查。
- 当前客户回复、订单、收入和转化并无本页可验证结论。

## 来源与证据

- `D:\codex\TASK_STATE.md`
- `D:\codex\output\armorhue-b2b-leadgen-run-20260605\automation-health-20260804.md`
- `D:\codex\output\armorhue-b2b-leadgen-run-20260605\automation-health-20260804-b2b-send.md`
- `D:\codex\output\armorhue-b2b-leadgen-run-20260605\automation-health-20260804-discovery.md`
