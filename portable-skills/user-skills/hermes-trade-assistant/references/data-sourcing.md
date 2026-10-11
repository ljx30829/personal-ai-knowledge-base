# 客户数据获取方案 — 实测完整指南

> 来源: 2026-06-06 ~ 06-07 Hermes Foreign Trade V0.1.2 开发过程中实测验证

---

## 已验证可行方案（按推荐度排序）

### ⭐ 方案 1: Google Maps 搜索（主力）

**验证状态**: ✅ 德/英/美三国实测通过 | ✅ 8次连续搜索压力测试通过
**费用**: 免费 | **限制**: 20次/小时（产品限制），需浏览器工具

**URL 模板**: `https://www.google.com/maps/search/{产品关键词}+{国家}`

**压力测试数据** (2026-06-07):

| # | 搜索词 | 间隔 | 结果 |
|---|--------|------|------|
| 1 | LED Leuchte Großhandel Deutschland | — | ✅ 5家 |
| 2 | Lichttechnik Import Deutschland | ~5秒 | ✅ 6家+网站直链 |
| 3 | Elektrogroßhandel Beleuchtung Deutschland | ~5秒 | ⚠️ ß字符导致空 |
| 4 | LED Beleuchtung Importeur Deutschland | ~5秒 | ✅ 5家 |
| 5 | Leuchten Grosshandel Import Deutschland | ~5秒 | ✅ 5家 |
| 6 | Licht Import Export Deutschland | ~5秒 | ✅ 5家 |
| 7 | LED Handler Import Deutschland | ~5秒 | ✅ 5家 |
| 8 | Licht Grosshandel Vertrieb Deutschland | ~5秒 | ✅ 6家+网站直链 |

**关键发现**:
- 7/8 搜索成功，0 次 CAPTCHA，0 次 IP 封禁
- 3 次失败全部是 ß 特殊字符问题 → 替换 **ß→ss, ä→ae, ö→oe, ü→ue**
- 关键词用纯目标国家语言，避免中英德混搭
- 搜索间隔 ≥ 5秒，单会话 ≤ 20次/小时
- ⚠️ 自动化搜索违反 Google Maps TOS；手动辅助模式作为合规替代方案

---

### ⭐ 方案 2: 各国官方企业注册库验证（配合方案1使用）

| 国家 | 验证渠道 | 状态 | 网址 |
|------|----------|:--:|------|
| 🇩🇪 德国 | Handelsregister / Impressum | ✅ 已实测 | 法律强制，每个商业网站必含 |
| 🇬🇧 英国 | Companies House | ✅ 已实测 | find-and-update.company-information.service.gov.uk |
| 🇺🇸 美国 | 州 Secretary of State | ✅ 已实测(MI) | 各州不同 |
| 🇫🇷 法国 | SIRENE / Infogreffe | 📋 待开发 | sirene.fr |
| 🇮🇹 意大利 | Registro Imprese | 📋 待开发 | registroimprese.it |
| 🇨🇦 加拿大 | 各省企业注册局 | 📋 待开发 | 各省不同 |
| 🇦🇺 澳大利亚 | ASIC | 📋 待开发 | asic.gov.au |
| 🇳🇱 荷兰 | KVK | 📋 待开发 | kvk.nl |
| 🇯🇵 日本 | 法人番号検索 | 📋 待开发 | houjin-bangou.nta.go.jp |

⚠️ "待开发" = 需要单独适配其查询系统，不是改 URL 即可。V0.2 前确定优先开发 2-3 个市场。

**实测案例**:

| 国家 | 公司 | 得分 | 董事信息 |
|------|------|:--:|------|
| 🇩🇪 | LEDclusive.de | 93 | Rüdiger Rohn, Jörg Prowald |
| 🇬🇧 | Wholesale LED Lights | 99 | Amit Soni, Prashant Soni |
| 🇺🇸 | LED Lighting Wholesale Inc. | 80 | — |

---

## 已验证不可行的方案

| 方案 | 尝试 | 失败原因 |
|------|------|----------|
| ImportYeti API | curl 403, 浏览器列表页可通 | 默认显示 Supplier（出口商），非 Buyer（进口商）；详情页 Cloudflare 拦截 |
| UN COMTRADE API | 404 API 改版 | 新 API 需要注册 + API Key；旧版端点失效 |
| OEC.world | Cloudflare 拦截 | 不允程序化访问 |
| Revor.ai | 付费，成本高 | 增加用户使用成本，不适合内测 |
| Europages/WLW/黄页 | Cloudflare 全部拦截 | 商业网站通用防护 |
| Google 文本搜索 | 触发 CAPTCHA | 搜索引擎反爬比 Maps 严格 |
| Playwright headless | 超时/连接失败 | 终端环境 Google 被屏蔽；Hermes 浏览器工具可通 |

---

## 为什么 Google Maps 可行但 Google 搜索不行为什么 Google Maps 可行但 Google 文本搜索不可行

2026-06-07 实测: 同样的网络环境，Google Maps 连续搜索 8 次 0 封禁，但 Google 文本搜索首次即触发 CAPTCHA。原因:
- Google Maps 对低频率的搜索容忍度高于文本搜索
- Maps 被视为"正常使用"行为（找商家），文本搜索的自动化痕迹更明显
- Hermes 浏览器工具（Browserbase）使用真实浏览器环境，对 Maps 支持良好

---

## 完整搜索验证 SOP

```
Step 1: Google Maps 搜索
  输入: "{产品关键词} {角色词} {国家}"
  角色词根据语言选择: wholesaler/importer/distributor (英) | Großhandel/Importeur/Händler (德)
  特殊字符替换: ß→ss, ä→ae, ö→oe, ü→ue

Step 2: 提取字段
  公司名 / 地址 / 电话 / 网站 / 评分 / 商家类型 / 营业时间

Step 3: 官网验证
  访问网站 → 确认业务描述 + 产品线匹配 + 获取邮箱
  (德国站: 直接访问 /impressum 获取法律注册信息)

Step 4: 官方注册库验证
  英国: Companies House 搜索公司名 → 查注册号+董事
  美国: 州 Secretary of State 企业查询
  德国: Impressum 已包含所有法律信息

Step 5: 数据质量评分
  按 5维度100分制打分 → 80+优先开发
```
