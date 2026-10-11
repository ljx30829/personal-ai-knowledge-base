---
updated: 2026-08-24
status: WATCH_RESEARCH_COMPLETE_IDENTITY_AND_API_SCOPE_UNVERIFIED
confidence: MEDIUM_HIGH
sources:
  - ../sources/research/jd-product-selection-pricing-listing-automation-github-research-2026-08-24.md
  - ../knowledge/commerce/jd-product-automation.md
next_review: 2026-09-07
---

# 京东电商自动化

## 目标

评估并设计“一键启动选品、核价、商品内容优化和京东上架”的自动化流程。

## 当前结论

- `PASS_RESEARCH_COMPLETE`：已检查京东开放平台公开入口并审查 11 个 GitHub 候选/编排项目。
- `WATCH_PLATFORM_PERMISSION`：没有目标店铺登录态，未确认商品新增、编辑、价格、库存和上下架接口权限。
- `WATCH_NO_COMPLETE_OSS_PRODUCT`：没有找到许可证、维护、真实验证和全链路覆盖都满足生产要求的开源成品。
- 推荐组合：Activepieces/n8n 编排 + 自建京东官方 API 适配器 + 证据化选品/核价规则 + AI Listing 优化 + 人工批准门 + 写后回读。
- 未登录、未读取店铺数据、未安装重型依赖、未创建应用、未修改价格、未上架商品。

## 下一决策

先确认业务身份：京东 POP 商家、京东自营供应商、京东联盟推广或纯市场研究。随后确认目标类目和“核价”的准确含义，再只读核对开放平台控制台的可申请权限。

## 实施前置条件

- 用户明确目标店铺和当次授权范围。
- 供应商报价、库存、运费、税费、平台费、促销、广告、退款损耗和目标毛利有真实输入。
- 类目属性、资质、商品素材版权和禁限售规则通过。
- 先完成 dry-run 和单个测试 SKU 草稿写入/回读，不直接批量上架。

## 证据

- [GitHub 与京东平台调研](../sources/research/jd-product-selection-pricing-listing-automation-github-research-2026-08-24.md)
- [可复用自动化方法](../knowledge/commerce/jd-product-automation.md)
