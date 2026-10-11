---
updated: 2026-08-24
status: VERIFIED_ARCHITECTURE_WITH_PLATFORM_PERMISSION_WATCH
confidence: MEDIUM_HIGH
sources:
  - ../../sources/research/jd-product-selection-pricing-listing-automation-github-research-2026-08-24.md
next_review: 2026-09-07
---

# 京东选品、核价、优化与上架自动化

## 可行性

可以做成一键启动的自动化，但生产首版应在正式上架前保留人工批准门。推荐流程是：

`一键启动 -> 授权数据采集 -> 证据化选品 -> 确定性核价 -> AI Listing 优化 -> 合规/字段校验 -> 人工批准 -> 京东官方 API 写入 -> 回读验证`

选品、利润计算、Listing 生成和任务编排已有可参考的开源组件；没有发现一个可直接投入生产、完整覆盖全链路的京东开源成品。京东商品写入需要为目标店铺单独核实开放平台应用、授权包、经营模式、类目和接口权限。

## 固定原则

- AI 负责研究、归纳、文案和解释；最低售价、毛利、库存和字段完整性由规则引擎硬控制。
- 竞品挂牌、热度、评价和销量估算是代理信号，不是需求、销量或利润证明。
- 不编造成本、规格、认证、功效、销量、评价、供应能力或店铺权限。
- 图片必须是自有、供应商授权、许可清楚或新制作素材。
- 上架请求必须幂等，写入后回读 SKU、价格、库存、状态和图片；“接口返回成功”本身不算完成。
- 浏览器 RPA 只作人工监督下的临时兜底，官方 API 是生产主路径。
- 密钥和 Token 只放安全的环境变量或凭证库，不写入知识库、日志或商品草稿。

## 推荐开源组合

- 编排与审批：Activepieces；已有 n8n 环境时也可用 n8n，但要复核其分发许可证。
- 京东只读连接器参考：`TonyWang-hub/mcp-cn-commerce`，仅作代码骨架，真实 API 必须逐项复核。
- 选品/利润/Listing 方法参考：`bin1732/global-ecommerce-intelligence`，只复用确定性方法，不采信无来源市场数字。
- JOS SDK 协议参考：`pifeifei/jingdong-jos-api-sdk`、`wappyer/jos-golang-sdk`；许可证和接口覆盖分别审查。
- 不采用：无数据连接却输出精确销量利润的“选品技能”、扫码账号池 EXE、以网页 Playwright 抓取充当稳定商家 API 的方案。

## 阶段门

1. `DRY_RUN`：只生成选品、核价和 Listing 待审核包。
2. `DRAFT_WRITE`：用户批准后，只创建草稿/待售商品并回读验证。
3. `CONTROLLED_PUBLISH`：仅对白名单类目、供应商和价格规则开放自动上架。
4. `AUTONOMOUS_PUBLISH`：只有持续验证、告警、熔断和回滚成熟后才考虑；不是默认状态。

## 恢复入口

详细仓库证据、快照数据、风险和下一步见 [2026-08-24 GitHub 调研](../../sources/research/jd-product-selection-pricing-listing-automation-github-research-2026-08-24.md)。继续前先确认用户属于京东 POP 商家、自营供应商、联盟推广还是纯研究场景。
