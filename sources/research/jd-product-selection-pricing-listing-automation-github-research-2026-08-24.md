---
date: 2026-08-24
updated: 2026-08-24
status: PASS_RESEARCH_COMPLETE_WITH_API_PERMISSION_WATCH
scope: 京东选品、核价、Listing 优化和商家上架自动化的 GitHub 项目与架构调研
confidence: MEDIUM_HIGH
sources:
  - https://open.jd.com/
  - https://jos.jd.com/
  - GitHub REST API repository metadata and public repository contents
next_review: 2026-09-07
---

# 京东选品、核价、优化、上架自动化 GitHub 调研

## 结论

这个流程可以做成“一点击开始运行”，但第一版推荐采用：

`点击启动 -> 自动选品/核价/生成商品资料 -> 规则校验 -> 人工批准 -> 官方 API 上架 -> 回读验证`

技术上能把后半段也设成无人值守，但前提是商家账号、类目资质、开放平台应用和商品写入接口权限已经通过，并且已经定义最低毛利、最高/最低售价、库存、图片版权、禁限售和失败回滚规则。没有这些输入，AI 只能生成看似完整的结果，不能可靠地完成核价和上架。

本次没有登录京东、没有读取店铺数据、没有申请接口权限、没有执行商品发布或价格修改。

## 2026-08-24 官方入口现场核验

- `https://open.jd.com/` 返回 HTTP 200，页面标题为“京东零售开放平台”。
- `https://jos.jd.com/` 返回 HTTP 200，页面标题为“宙斯开发者中心 | 京东开放平台”。
- 开放平台前端包含 API 文档、授权包、OAuth/控制台和 `https://api.jd.com/routerjson` 网关入口。
- 未使用商家登录态，因此没有确认某个具体店铺当前可申请的商品新增、编辑、价格、库存和上下架接口权限。接口是否可用必须以目标店铺、经营模式、类目和应用授权包的控制台结果为准。

## GitHub 候选审查

仓库数据为 2026-08-24 读取到的公开快照。Stars 只作维护热度参考，不代表代码正确或已通过京东真实店铺验证。

| 项目 | 快照 | 实际覆盖 | 结论 |
| --- | --- | --- | --- |
| [TonyWang-hub/mcp-cn-commerce](https://github.com/TonyWang-hub/mcp-cn-commerce) | MIT，36 stars，2026-08-24 有提交 | 京东 MCP 只读工具，订单、商品、评价、价格、库存等 | `WATCH / 可作只读连接器骨架`。明确不做写入；测试把 `_call` mock 掉，不能证明所有 API 名称和参数已在真实京东授权环境通过。不能直接用于上架。 |
| [LuFering/ShoppingClaw](https://github.com/LuFering/ShoppingClaw) | 2 stars，2026-05-25 最后提交，README 称 MIT 但 GitHub API 未识别许可证 | LangGraph 多 Agent、JD SDK、商品搜索和消费推荐 | `WATCH / 架构参考`。面向消费者选购，不是商家刊登；依赖 PostgreSQL、Redis、Docker、Ollama 等，明显偏重。SDK 中虽然存在价格、库存、商品状态类请求，但不等于目标店铺拥有权限。 |
| [Frank-789/VERTEX-pro](https://github.com/Frank-789/VERTEX-pro) | 20 stars，2026-07-13 最后提交，无许可证 | 选品界面、利润分析、Listing 文案、Playwright 京东搜索 | `FAIL_REUSE / 仅看交互思路`。京东采集是网页选择器，商品详情函数仍为 placeholder；没有上架连接器。无许可证，不应直接复用；网页采集也有稳定性和平台规则风险。 |
| [pifeifei/jingdong-jos-api-sdk](https://github.com/pifeifei/jingdong-jos-api-sdk) | PHP，3 stars，2026-03-12 有提交，无许可证 | JOS 请求签名、Access Token 和大量请求类 | `WATCH / 协议参考`。不是完整业务系统；缺少清晰许可证，并且仓库树中没有确认到完整的商家商品创建流程。 |
| [wappyer/jos-golang-sdk](https://github.com/wappyer/jos-golang-sdk) | Apache-2.0，0 stars，2025-06-18 最后提交 | Go 版 JOS 客户端，地址、ECLP、订单、库存、联盟类目等有限请求 | `WATCH / 小型 SDK 参考`。许可证清楚，但接口面不足以承担选品到上架全链路。 |
| [bin1732/global-ecommerce-intelligence](https://github.com/bin1732/global-ecommerce-intelligence) | MIT，0 stars，2026-08-23 有提交 | 选品评分、利润计算、Listing/合规方法和脚本 | `PASS_METHOD_ONLY`。可参考利润和反幻觉规则，但没有经核实的京东商家数据连接与商品发布能力。 |
| [ggq-eng/ecommerce-product-selector](https://github.com/ggq-eng/ecommerce-product-selector) | 0 stars，约 9 KB，只有 6 个技能文件 | 声称支持京东选品 | `FAIL_EVIDENCE`。没有平台采集或分析实现；示例直接给出热度、月销和利润数字，不能作为真实选品引擎。 |
| [ljltom-gb/personal-price-bot](https://github.com/ljltom-gb/personal-price-bot) | 4 stars，约 7 KB，无许可证 | 京东联盟等官方商品搜索与个人比价 | `WATCH / 查询模式参考`。这是消费者/联盟比价，不是商家成本核价、改价或上架。 |
| [min-ory/YRelaxedSku](https://github.com/min-ory/YRelaxedSku) | Apache-2.0，3 stars，2025-06-03 最后提交 | 批量查询京东 SKU 好评率 | `FAIL_OPERATIONAL_RISK`。README 要求运行 EXE、激活密钥和扫码登录账号池，只适合学习观察，不应接入商家生产账号。 |
| [activepieces/activepieces](https://github.com/activepieces/activepieces) | 社区版 MIT，24k+ stars，2026-08-24 活跃 | 可视化工作流、人机审批、自定义 TypeScript Piece | `PASS_ORCHESTRATOR`。适合承载“一键运行”和审批节点，但需要自己开发京东连接器。 |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 202k+ stars，2026-08-24 活跃，Sustainable Use License | 成熟工作流、HTTP/代码/AI/人工审批 | `PASS_ORCHESTRATOR_WITH_LICENSE_WATCH`。也可承载流程，但不是京东连接器；商业分发前要审许可证。 |

## 可复用组合

没有发现一个许可证清楚、持续维护、真实验证并且完整覆盖“京东选品 -> 商家核价 -> AI 优化 -> 正式上架”的开源成品。最现实的方案是组合，而不是 fork 一个仓库后直接上线：

1. 工作流：Activepieces 或已有的 n8n；若只做本机单店，也可先用项目内队列和一个按钮，减少部署负担。
2. 京东只读：审计后参考 `mcp-cn-commerce` 的连接器结构，但 API 名称、签名和权限必须逐项对照目标应用的官方文档并做沙箱/小流量验证。
3. 选品与核价：吸收 `global-ecommerce-intelligence` 的利润计算和证据标记思路，使用自己的供应成本、平台费、运费、税费、退款损耗、促销、广告和目标毛利数据。
4. AI 优化：生成标题、卖点、属性映射、详情结构和图片任务，但不能编造材质、认证、功效、销量、评价或售后承诺。
5. 上架：单独实现京东官方写入适配器；不要用 Playwright 模拟京麦后台作为主方案。

## 推荐的自动化边界

### 阶段 1：一键生成待审核包

- 输入：目标类目、预算、供应商报价/库存、允许的数据源、目标毛利和风险阈值。
- 自动：授权数据采集、去重、证据分级、选品评分、成本核算、售价区间、标题/属性/详情优化、图片与合规检查。
- 输出：每个 SKU 的证据卡、成本表、建议价、最低可售价、Listing 草稿、缺失字段和 `PASS/WATCH/BLOCKED`。
- 停止点：人工审核，不触发京东写入。

### 阶段 2：批准后创建草稿或测试商品

- 为每次运行生成唯一 Run ID 和商品幂等键，避免重试时重复创建。
- 只对 `PASS` 且字段齐全的 SKU 调用已授权 API。
- 默认创建草稿/待售状态；价格和库存有硬阈值，AI 无权突破。
- 写入后立刻回读 SKU、价格、库存、状态和图片，逐项比对。

### 阶段 3：受控自动上架

- 在连续多次草稿验证通过后，只对白名单类目和供应商开放。
- 设置每日 SKU 数、单次价格偏差、最低毛利、库存上限和熔断阈值。
- 任一接口权限、属性映射、图片、价格或库存校验失败，整项进入 `BLOCKED`，不得猜值补齐。
- 保存请求摘要、平台响应、回读结果和人工批准人，不保存明文密钥。

## 核价必须使用的真实输入

```text
到岸/采购成本
+ 国内运费和包装
+ 仓储/履约
+ 京东扣点及技术服务费
+ 支付/发票/税费
+ 退款退货损耗准备
+ 促销补贴与优惠券承担
+ 广告获客成本
+ 售后和质保准备
+ 目标净利润
= 可接受售价区间
```

平台挂牌、竞品价格和模型估算只能辅助定价，不能替代上述成本。最低价应该由确定性公式和规则引擎计算，AI 只解释与提出方案。

## 三种实现路线

1. `推荐：API + 审批门`。稳定、可审计，适合长期生产；前期需要申请开放平台应用和写入权限。
2. `API 全自动`。用户一次点击后直接上架；只有在权限、类目、字段、价格和回读验证成熟后才开启，仍需白名单和熔断。
3. `浏览器 RPA`。开发演示快，但容易受登录验证、验证码、页面改版和平台规则影响；仅作为人工监督下的临时兜底，不作为主架构。

## 当前阻塞项

- 用户尚未说明是京东 POP 商家店铺、京东自营供应商、京东联盟选品，还是仅做价格/市场研究。
- 未确认目标类目、SKU 数量、供应商数据格式和“核价”是采购核价、竞品比价还是销售定价。
- 未确认目标店铺在开放平台控制台可申请哪些商品写入、价格、库存和上下架权限。
- 未授权登录、创建应用、读取店铺数据或执行上架。

## 下一步验证

先确认经营身份和目标店铺类型，再在用户登录的官方控制台中只读查看应用资质及可申请接口清单。随后做 1 个虚拟/测试 SKU 的字段映射和 dry-run；在权限与回读证据通过前，不安装重型项目、不接生产账号、不执行上架。
