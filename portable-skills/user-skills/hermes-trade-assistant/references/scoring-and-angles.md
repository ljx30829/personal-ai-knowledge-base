# 客户评分系统 + 个性化邮件角度映射

> 简化为 1-5 分制。3 分以下直接丢弃，不写入数据库。

## 评分标准

| 分 | 标准 | 操作 |
|:--:|------|:--:|
| 5 | 独立站 + 专业邮箱(@域名) + 匹配产品 + 实体店/B2B标识 | ✅ 写入，优先开发 |
| 4 | 有邮箱 + 匹配产品，免费邮箱(Gmail等) | ✅ 写入 |
| 3 | 有邮箱，产品可能相关，无明确证据 | ⚠️ 写入待确认 |
| 2 | 不相关产品 / 邮箱不匹配 | ❌ 丢弃 |
| 1 | 大平台(alibaba/amazon等) / 死站 / 无网站 | ❌ 丢弃 |

## 网站特征检测 → 邮件角度映射

发邮件前，先爬对方网站首页检测特征，然后根据特征选角度。**每封邮件必须包含对方网站上的唯一特征。**

### 检测关键词表

| 特征 | 关键词 | 语言 |
|------|--------|------|
| 成立年份 | `since`, `seit`, `desde`, `est.`, `建立于`, `成立于` | 多语 |
| B2B 分销商 | `distributor`, `wholesale`, `partner`, `großhandel`, `grossiste` | 多语 |
| 高端定位 | `premium`, `natural`, `organic`, `bio`, `luxury`, `高端` | 多语 |
| 实体店 | `store`, `laden`, `tienda`, `visit us`, `filiale`, `门店` | 多语 |
| 科技/智能 | `smart`, `tech`, `digital`, `app`, `智能` | 多语 |
| 线上为主 | `online shop`, `e-commerce`, `webshop`, `网购` | 多语 |

### 特征 → 邮件角度映射

| 检测到特征 | 邮件切入点 | 开场思路 |
|-----------|-----------|---------|
| 成立年份 | 传统+创新 | "看到你们自 1985 年起就在XX经营..." |
| B2B 分销商 | 品类补充 | "你们代理的品牌集中在XX，我们有互补产品线" |
| 高端定位 | 匹配品质 | "你们客户追求品质，我们的产品符合这种标准" |
| 实体店 | 规模化供应 | "有多家门店，适合规模化合作" |
| 科技/智能 | 技术互补 | "你们在智能XX方面的布局，我们的产品是自然延伸" |
| 线上为主 | 跨境直发 | "了解线上运营的痛点，我们可以一件代发" |
| 无特征 | 城市切入 | "在XX市，越来越多消费者在寻找XX产品" |

## 禁止模式（写邮件时绝对避免）

```
❌ 开头就介绍自己公司（"We are a leading manufacturer..."）
❌ Subject 只换公司名（"LED products for {Company}"）
❌ 每封邮件列同样的产品清单（群发感）
❌ "As {Company}, which offers..." 句式
❌ 第一句不是对方网站上的具体发现（造假）
❌ 感叹号/问号过多（触发垃圾过滤器）
❌ 全部大写（FREE SAMPLE / BEST PRICE）
```

## 邮件结构模板

```
Subject: {基于特征的独特钩子，不是模板}

{称呼}

第一句：我在你网站上看到的具体东西
  "I noticed you carry [specific product line]..."
  "看到你们自 [年份] 起就在 [城市] 经营..."

第二段：为什么我们的产品适合你们
  "Our [product] would complement your existing [category]..."
  "Having supplied [similar companies], we understand..."

第三段：低压力邀约
  "Would you be open to a quick look at our catalogue?"
  "No pressure — just thought it might be a fit."

{签名}
```

## 验证效果

实测 LEDclusive.de：检测到 B2B 标识 + 实体店 + 15年运营 + 专业邮箱 → 5分 → 个性化角度可选"传统+创新"或"品类补充"
