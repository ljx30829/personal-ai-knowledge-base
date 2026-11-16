---
updated: 2026-08-04
status: VERIFIED_CURRENT_SCRIPTS_RUNTIME_GATED
confidence: HIGH
sources:
  - D:\codex\AGENTS.md
  - D:\codex\TASK_STATE.md
  - D:\codex\PROMOTION_WORKFLOW.md
  - D:\codex\output\ExcludedBrand-b2b-leadgen-run-20260605
next_review: 2026-08-05
---

# ExcludedBrand 外贸线索、邮件与监督执行手册

本手册把线索发现、发送包、SMTP 身份探测、真实发送、社交准备和监督分成独立步骤。所有命令都必须从当前项目状态恢复；脚本存在不代表当天具备发送资格。

## 固定入口

```text
工作区：D:\codex
输出根：D:\codex\output\ExcludedBrand-b2b-leadgen-run-20260605
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
Set-Location D:\codex\output\ExcludedBrand-b2b-leadgen-run-20260605
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
Set-Location D:\codex\output\ExcludedBrand-b2b-leadgen-run-20260605
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

- `ZOHO_SMTP_USER`、`ZOHO_SMTP_FROM`、`ZOHO_SMTP_REPLY_TO` 都以 `@ExcludedBrand.com` 结尾。
- 当前允许的发件身份是 `samples@ExcludedBrand.com`；不得临时换 QQ、Gmail 或其他免费邮箱面向客户发送。
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



## 2026-11-10：跨渠道历史、未知状态与配额

近期增补以本节覆盖旧稿中的历史状态；跨设备首轮权限需核实，既有有效授权不因日期变化重复索要。研究任务仍只研究，不因找到公开号码自动发消息。

1. 历史草稿的“未发送”可被后续其他授权会话发送覆盖；先核真实聊天、发送日志、集团关系、邮箱/号码和抑制，再决定是否是新联系人。官网当前岗位、采购职责、个人审批权限三列；公司候选配额达标不等于联系人与独立主体交叉核验完成。
2. 每日额度统计本地 SMTP 接受、状态未知及其他渠道已发送邮件；跨会话材料邮件按真实发送计入全日统计，即使业务用途与冷开发队列不同，也不能从额度中漏掉或重复加算。
3. SMTP连接在提交附近中断时记 UNKNOWN 并占用保守名额，不自动重发；只继续从未尝试且审核通过的记录。服务商重试队列写入本地抑制，交由服务商处理，不另发一份。
4. WhatsApp 首次联系、历史聊天跳过、自动回复、人工转介、资料发送分开记；页面显示发送/送达/已读各自留证。对方索要邮件资料后，先核具体邮箱和用户授权，附件分封也保留各自哈希与 SMTP 结果；通知已送达不能证明附件邮件已收取。
5. 发送前、批间、发送后五文件夹审查与不可变文案/哈希核对继续执行。联系人研究只保存草稿，不修改发送清单；旧受限来源按来源级阻塞处理，不冒充全局不可研究。

使用的技能与工具：`guarded-zoho-outreach` 用于守门编排，`ego-browser` 用于登录网页复核/WhatsApp页面操作；研究任务实际读取 `cold-draft`、`cold-email`、`hermes-trade-assistant`、`end-to-end-quality-auditor`、`verification-before-completion`，读取不等于其全部流程已执行。底层是 Ego Lite CLI、Python SMTP、SQLite及本地审计文件，非生成模型自动证明采购权限。Skill 独立公开源码未确认，标待核；[Zoho Mail SMTP](https://www.zoho.com/mail/help/zoho-smtp.html)仅说明传输设置。

输入为经核公司证据、历史与授权；产出为未发送审核稿或独立发送结果，依赖邮箱/页面登录与发送权限。费用按邮箱套餐、模型/浏览器执行和人工核查分别核。恢复时保持 UNKNOWN/抑制不可重放；用户回复“收到”前仍无实际邮件收取证明。客户清单、聊天原文、业务附件、精确后台数据只留受控本地。


## 2026-11-11：批次汇总与逐条证据冲突

适用：浏览器发送批次的总结数字与结果文件不一致，或邮箱读回通道故障。先按对象、渠道、日期和实际动作对账，不沿用助手声称的整批成功数。

1. 分开原请求、脚本候选、执行结果与独立页面回读；结果文件中的 SENT_UI、NO_RESULT、ERROR 不能都累计为已发送。按钮点击/回车成功不一定有发送状态，单条 SENT_UI 也不证明送达、阅读或采购意向。
2. 有独立人工回复的聊天与批次结果分账，先去重再统计。名单截图、草稿总量和以前已发记录不是当日新增；身份/资格待核项保留不发送。原始联系人、号码和正文只留本地。
3. 遇结果文件与总结冲突，保留两者和原时间，不编一个统一数；逐条核对记录完整性后才改总数。因页面“新聊天”按钮禁用而错误的项目，不能写成账号不存在，也不能自动重发状态不明项。
4. 邮箱支持的控制通道多次不可用时，不复用旧五文件夹快照，不启动发送器；保留已审核草稿、UNKNOWN和抑制表。恢复读取后重新查五文件夹、全日外部发送与服务商事件，再跑 preflight。无须重复索要已存在的授权，但授权不能替代新鲜状态证据。

本轮复核确认一批结果文件与历史整批成功自述冲突，已在本地日报降级；没有发送新消息。邮件原工作会话因真实邮箱复核失败本轮零发送，剩余额度未知。实际执行层为已登录浏览器、Ego Lite 页面快照/CLI、桌面控制故障输出和 JSON 台账；技能编排沿用原受控外贸规则，独立 Skill 新读取证据待核，无新生成模型或额外付费验证。


## 2026-11-12：只读邮箱API、频控恢复与研究工具

旧“邮箱读取始终阻塞”已过期：官方Zoho只读OAuth真实账户/文件夹/正文/续期验证成功；IMAP套餐限制仍在，不能由此推断REST API不可用。先本人完成敏感验证，再确认accounts.READ、folders.READ、messages.READ最小权限；长期凭据只放系统凭据库。列表成功不等于业务复核：按最后成功业务水位保留重叠，messageId去重，读正文分类退信/自动回执/人工回复，对账Sent/Outbox和发送库，才生成合法新快照。空结果先核过滤参数，错误归档标失效，不能当无邮件。

真实发送工作随后通过API及原浏览器扩展逐封复核；SMTP接受、服务商Delivered、Queued、收件/阅读分层。API频繁续期触发限流时不连续探测，使用已授权扩展完成当前复核；缓存有效access token及到期时间，剩余大于120秒才复用，否则单次续期并保存。有效缓存零网络与过期单次续期模拟通过，修复后真实API仍待下一正常运行。未知发送不重试、自动回执不作人工兴趣、永久失败抑制、活动不可变清单及额度门禁不变。Gmail附件0%时未点发送，不能计成功或保证服务端草稿持久化。

使用的工具：`mcp__cua_repl`浏览器扩展、Python只读IMAP探测/Zoho REST API、Windows凭据库、既有SMTP发送器和哈希审查；`cold-email`等独立Skill本轮读取证据未全部归一，不推定。输入为原授权、台账与合法复核水位；产出为API证据、分类、清单及回读。无新增付费升级，套餐资格按账号实测，技术投递不证明采购权限或业务效果。恢复需先对账再续跑，不修原生管道也可用已验证替代通道，但不能说底层已修。

### 获客研究与CRM分工

官网先证明公司资格并去重，再按公司域名查相关岗位，最后补公开业务邮箱与技术验证。公司配额、岗位职责、采购审批权分列。Hunter/Apollo官方远程MCP是候选，未安装/授权/试跑；旧Hunter仓库已弃用。公开定价快照：Hunter Free50 credits/月，查找1、验证0.5；Apollo人员搜索0 credits不返邮箱/电话且有账户资格限制。结算与当前计划需重核，不能保证找到指定人数。

源码审查得到可复用结构：独立研究索引、证据与主张账本、firstSeen/lastSeen、缺口调度、审核桥接；保持原发送SQLite与门禁，不将多来源研究库替换发送库。镜像仓库不算独立数据源；许可证按实际文件，摘要提邮箱、猜contact路径、默认排除distributor、硬编码行业邮件或吞异常不能照搬。RapidFuzz仅提示疑似重复，不能证明集团；Trafilatura清正文时保留原HTML和页脚证据。设计仍未实施，无安装或名单迁移。

HubSpot官方MCP经最小CRM只读授权，通过本地工具限制桥接、OAuth PKCE、真实读取/续期/stdio验证。公司、联系人、交易只读；未导入本地客户、未写CRM、未发信。试用不是购买，新聊天自动工具加载尚需独立核实。HubSpot是管理/查询层，不自动提供全球采购人数据，也不是新增外发授权。

学习：[Zoho OAuth](https://www.zoho.com/mail/help/api/using-oauth-2.html)、[Hunter MCP](https://hunter.io/mcp)、[Apollo MCP](https://www.apollo.io/product/mcp)、[HubSpot MCP](https://developers.hubspot.com/mcp)、[研究技能合集](https://github.com/FloydTang/trade-skills-collection)、[Trafilatura](https://github.com/adbar/trafilatura)、[RapidFuzz](https://github.com/rapidfuzz/RapidFuzz)。


## 2026-11-13：有效token实测、渠道授权及聊天发送验收

状态修正：前日“缓存修复后真实API待核”已由正常发送任务实测覆盖；官方只读API复用系统凭据库有效access token，逐封后的Sent/Outbox与正文复核完成，不依赖网页在线。API `status=1`未被证明是Delivered，只记可见，不把它翻译成服务商送达。SMTP接受与后续永久退信可同时存在，不能把接受总量当净送达。

实际使用`cold-draft` Skill辅助逐公司草稿审核，执行层为既有Python/SQLite不可变清单、SMTP发送器、Zoho只读API与哈希核验；Skill公开独立来源待核。单独回复草稿读取`hermes-trade-assistant`，没有越过日额和停止触达门禁发送。输入为合法清单、当前官网事实、全历史抑制和真实邮箱复核，输出为审核、SMTP与逐封回读。采购权限仍需原证据，不从邮箱存在或接待回执推导。邮件额度、WhatsApp号码数、消息数、公司数不可混加。

### 用户单独授权的WhatsApp执行流程

适用已明确授权的回复/开发，不从邮件授权扩张到社交渠道。实际读取`ego-browser` Skill，使用Ego Lite CLI与页面快照；公开产品来源[Ego Lite](https://lite.ego.app/)，独立Skill源码待核。没有新增生成模型或客户数据服务费用。

1. 核正确账号与指定空间；“未读0”不等于没有已读待回。先加载完整聊天再写，历史迟到时暂停并重读，不机械重复首条介绍或采购问题。
2. 号码格式与公司/集团关系分别去重，既有抑制、官网证据缺口、搜索不到与身份待核分列。只作身份核实的消息不能把对象提前计为合格买家。
3. 按实际问题回复；询价先补款式、数量、到货地/日期，不编MOQ、价格和交期。已有目录需求就接续该需求，不重新问同一采购入口。
4. 逐条保存attempt和发送后页面回读，分已发送、已送达、已读；按号码汇总与同号码多轮消息分开，名单外回复另列分母。对方自述转售/提供采购邮箱只是新证据，不自动证明采购审批权或邮件已发送。
5. 文件选择后等待附件预览，延迟出现重复项时先移除重复，再核收件对象和仅一份附件；点击发送后必须看到文件气泡、文件名和状态。两次选择不等于两次发送，前文“附件失败”也可能被后续送达证据覆盖，保留修正事件。
6. 对方提供供应商表单时检查真实目的与收件对象，仅填已有业务资料；页面“资料收到”记已提交，不能写审核通过、供应商获批或订单。
7. 邮件转介回到原邮件门禁，不能因为WhatsApp给了邮箱就超日额、绕抑制或自动改投。新指令与既有明确限制冲突、覆盖范围不清时保留草稿交用户决定；不把未发送草稿计结果。

验证/恢复：保留原始快照和分母清单；UNKNOWN不重试，延迟加载先查聊天是否已发；文件/表单失败先查现态，不重复提交。浏览器回读证明当时状态，不能代替之后业务效果。客户号码、正文、邮箱、表单私链及详细证据仅留本地。


## 2026-11-16：中断研究接续与运行中邮箱证据

变更：历史工具可用不能代替本次可用性；本轮研究遇到既有Ego命令及历史可执行路径失效，普通公开网页读取仍有成功响应。此前中断任务已有部分官网快照，但没有完整批次验收，不增加公司或负责人完成数量。邮箱在另一授权会话完成只读采集、业务分类与延迟事件保存，是阶段性完成，不代表当日发送任务完成。

1. 先读原周期与最新批次，再按公司、页面、用途对照原始快照。没有新批次、哈希审核及角色证据的研究，不从已读页面数推算合格数量；同一公司补联系人不计新公司。
2. 命令失效先确认本机已登记路径和依赖，记录实际错误；本次允许的普通公开HTTP读取只适用于无认证公开页，不复用浏览器私密状态。返回200而正文仅有标题时记不完整；403、429、验证码或登录墙即停该来源，不换抓取后端绕过，不把单工具故障说成网站全面不可访问。
3. 中断前已保存HTML/正文是部分证据；任务没有最终批次就保存缺口，不编INCOMPLETE的完成日期。下次核最新官网、全历史去重和抑制后再续接，不能整批继承草稿审核。
4. 邮箱采集完成后，核覆盖时间、文件夹完整性、正文分类与外部发送对账。延迟回执只记服务商重试，不触发本地重发；拒绝/永久失败按原门禁抑制。生成合法新业务快照后，后续发送仍需独立清单、额度和逐封后复核。
5. 回顾仍运行的任务时固定读取时点，只陈述已返回的命令和文件；尚未发生的发送及后续回执保留待核，下轮重叠读取，不能用运行状态或最后更新时间当完成水位。

使用的技能与工具：研究原会话实际读取`ego-browser`和`cold-email`；本轮Ego执行受路径缺失阻塞，已实际使用PowerShell `Invoke-WebRequest`、本地HTML与既有周期JSON。`cold-email`不等于发送器。邮箱原会话为既有Python只读Zoho API、SQLite事件与抑制、正文哈希及业务快照；专用Skill本轮完整调用证据待核。公开产品来源：[Ego Lite](https://lite.ego.app/)、[Zoho Mail API](https://www.zoho.com/mail/help/api/using-oauth-2.html)、[PowerShell网页读取](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/invoke-webrequest)。Skill独立公开源码待核；没有新生成模型、付费采购、CRM写入或本轮日报外发授权。

输入为原周期、合法邮箱权限与公开页面；产出为部分来源快照、业务复核和缺口。验证以保存文件和实际返回为准；未形成全轮研究验收或当日发送最终结果。成本沿用原服务/网络/维护，未独立测算新增成本。详细联系人、客户站点清单、邮箱正文和私有运行证据仅留本地。
