---
updated: 2026-08-04
status: WATCH
confidence: HIGH
sources:
  - D:\codex\TASK_STATE.md
  - ../knowledge/trade/foreign-trade-operations.md
  - ../knowledge/sites/independent-sites-and-shopify.md
next_review: 2026-08-11
---

# ArmorHue

## 范围

汽车膜 Shopify 独立站、SEO、图片与内容、B2B 线索发现、域名邮件、社交/WhatsApp 准备、批发与经销商漏斗。主工作区是 `D:\codex`。

## 已完成

- 已形成 Shopify 主题、商品目录、图像、推广工作流和大量日期化 QA/监控证据。
- B2B 已形成发现、发送、监督和社交准备四套独立自动化。
- 截至 2026-08-01 监督快照，主发送日志记录 299 条精确真实 `Sent`、296 个唯一已发送邮箱。
- 2026-08-02 新发现 8 个去重 A 级机会，仅准备未发送。

## 当前状态

- 邮件：`BLOCKED_NO_SEND`。2026-08-02 当日 `Sent=0`，需要 Zoho IMAP/POP 或 day42 之后的人工 Zoho Webmail 风险复核。
- 社交：`WATCH_NO_SEND_PREP_ONLY`。2026-08-01 的 100 条队列全部需人工复核，实际动作 0。
- SEO：`WATCH`。2026-08-02 完整监控因 7 个 HTTP 429 页面信号为 `FAIL`，Lighthouse 仍有部分可用证据。
- 转化：GA4/GTM 必要事件证明 0/8，当前 `BLOCKED_MISSING_REQUIRED_PROOF`。
- Shopify：本地可准备项不能在 P1 和当次授权前同步到线上。

## 阻塞项

- 邮箱退信、回复、退订、投诉和负面回复复核未闭环。
- Shopify Admin 的 `shop.name` 非秘密证据仍未完全闭环。
- GA4/GTM 的 `page_view`、`view_item`、`add_to_cart`、`begin_checkout`、`purchase` 与 lead/contact 事件缺证。
- HTTP 429、Color TPU PPF 自定义域缓存一致性和部分内部链接需要复查。

## 授权边界

- 发现、只读监控和本地准备不授权发送或线上修改。
- 真实邮件必须重新通过身份、抑制、去重和邮箱复核门；社交/WhatsApp 需要操作时的具体平台、账号、目标和动作授权。
- Shopify Admin、线上主题、Search Console、广告、分析配置、发布和删除均需明确授权。

## 恢复步骤

1. 读取 `D:\codex\AGENTS.md` 和 `D:\codex\TASK_STATE.md` 的最新顶部段落。
2. 根据任务读取 `PROMOTION_WORKFLOW.md`、`IMAGE_WORKFLOW.md` 和对应自动化记忆。
3. 邮件任务先读 2026-08-02 sender blocker 与 2026-08-01 supervisor 报告；不得跳过邮箱风险复核。
4. SEO 任务运行前查看 `reports\site-audit\armorhue-daily-monitor\README.md` 和最新摘要。
5. 有意义的变更后同时更新原项目状态与本知识库项目页。

## 证据路径

- `D:\codex\TASK_STATE.md`
- `D:\codex\output\armorhue-b2b-leadgen-run-20260605`
- `D:\codex\reports\site-audit\armorhue-daily-monitor\latest-daily-pipeline-summary.md`
- [外贸运营方法](../knowledge/trade/foreign-trade-operations.md)
- [独立站与 Shopify 方法](../knowledge/sites/independent-sites-and-shopify.md)

