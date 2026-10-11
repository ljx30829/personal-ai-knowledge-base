---
name: hermes-trade-assistant
description: >-
  外贸 B2B 客户开发全流程技能。核心工作流：多API并发搜索(Tavily/Serper)→提取邮箱(10国法律页面路径)→1-5评分→网站特征分析→个性化邮件生成。
  包含500+工具合集、20+国家市场分析、开发信模板库、跟进策略。
  当用户询问外贸客户开发、找客户、写开发信、外贸邮件、市场分析时加载。
---

# 外贸助手 — 核心知识体系

## 使用方式

当用户提出外贸相关问题，按以下流程：
1. **判断问题类别**（客户搜索 / 市场分析 / 邮件撰写 / 跟进谈判 / 工具推荐 / 数据评估）
2. **查阅下方快速索引**，定位具体策略
3. **如需详细内容**，读取 `references/` 下的对应文件

---

## 工作流速查

当用户提出找客户需求时，自动执行四步，无需中间确认：

```
搜索 → 提取邮箱 + 评分 → 分析网站内容 → 生成个性化邮件
```

每次用户说"找 N 个客户"时，按这个顺序走。3 分以下自动丢弃，不干扰用户。

详细说明见: `references/scoring-and-angles.md` 和 `references/country-legal-pages.md`

---

## 一、客户搜索 — 快速索引

### ⭐ 四合一搜索 API 组合（推荐 — 免费 6,500 次/月）

**并发调用 Tavily + Serper.dev + Brave Search + Bing Search**

| API | 免费/月 | 擅长 |
|------|:--:|------|
| Tavily | 1,000 | AI 语义搜索，结构化 JSON |
| Serper.dev | 2,500 | Google 搜索，速度快 |
| Brave Search | 2,000 | 独立索引，隐私 |
| Bing Search | 1,000 | 欧洲数据优势 |

**策略**: 四路并发 → 合并去重 → 按需分流（不同任务用不同 API）
详见: `references/search-api-strategy.md`

**备用**: Apollo.io (付费, 邮箱+职位+电话) | Google Maps 浏览器（单市场少量搜索可用，不适合规模化）

### ⚠️ Google Maps 免费搜索 — 适用范围与限制

**适用于**: 单市场、少量搜索（德/英/美已验证可行）
**不适用于**: 全球多国规模化搜索

**2026-06-07 压力测试发现**:
- 单一国家 8 次搜索全部成功（0 封禁 0 验证码）
- 跨国多语搜索（中/英/法/德/意混合）→ 第 12 次后触发反爬，后续全部返回空页
- 结论: Google Maps 浏览器抓取做不了全球规模化的商用产品

**仍可用的场景**: 用户主动发起单次搜索、德国/英国/美国市场、手动辅助模式兜底

### Google 文本搜索（辅助方法）
- Importers/Distributor/Buyer 关键词组合
- 详见: `references/customer-search.md`

### ⚠️ 海关数据陷阱

ImportYeti 等免费海关数据网站默认显示 **Supplier（出口商）**，不是 Buyer（进口商）。搜 "LED lighting Germany" 返回的可能是中国工厂。

### LinkedIn / Facebook / WhatsApp 开发
- 详见: `references/customer-search.md`

---

## 二、客户数据质量评估 ⭐

搜到客户后 **必须打分**。

### 快速评分: 1-5 制（日常使用，推荐）
详见: `references/scoring-and-angles.md`

| 分 | 标准 | 操作 |
|:--:|------|:--:|
| 5 | 独立站 + 专业邮箱 + 匹配产品 + B2B | ✅ 优先开发 |
| 4 | 有邮箱 + 匹配产品 | ✅ 写入 |
| 3 | 有邮箱，待确认 | ⚠️ 保留 |
| ≤2 | 大平台/不相关/死站 | ❌ 丢弃 |

### 详细评估: 5 维度 100 分制（需要深度评估时）
框架: `references/customer-evaluation-framework.md`
80+ 优先 | 60-79 可联系 | <40 放弃

**实测分数参考**: LEDclusive.de 93分 | Wholesale LED Lights 99分 | LED Lighting Wholesale Inc. 80分

---

## 三、市场分析

全球五大洲 + 20+ 国家采购商特点。详见: `references/market-analysis.md`

---

## 四、邮件与跟进

开发信模板、跟进策略、询盘回复、英文例句。详见: `references/email-templates.md` + `references/negotiation-followup.md`

---

## 扩展参考

| 文件 | 内容 | 何时加载 |
|------|------|----------|
| `references/search-api-strategy.md` | 四合一搜索 API 组合 + 分流策略 | 需要搜客户时（优先参考） |
| `references/data-sourcing.md` | 免费客户数据方案 + 各国验证渠道 | 需要搜客户时 |
| `references/country-legal-pages.md` | 10 国法律/联系页面路径表 | 提取邮箱时 |
| `references/scoring-and-angles.md` | 1-5 评分 + 网站特征→邮件角度映射 | 评分和写邮件时 |
| `references/commercial-data-api-comparison.md` | 8家商业 B2B API 对比 | 讨论付费方案时 |
| `references/v013-codebase-guide.md` | V0.1.3 Flask 应用完整代码库指南 | 修改/部署项目时 |
| `references/customer-search.md` | Google 43招 + LinkedIn/Facebook/WhatsApp | 需要详细搜索方法时 |
| `references/market-analysis.md` | 20+ 国家采购商特点 | 需要市场分析时 |
| `references/email-templates.md` | 开发信 + 跟进模板 + 英文例句 | 需要写邮件时 |
| `references/negotiation-followup.md` | 8种跟进错误 + 34招谈判 | 需要跟进策略时 |
| `references/tools-resources.md` | 500+ 外贸工具合集 | 需要工具推荐时 |

---

## UI 设计偏好（开发 Web 界面时遵循）

- **亮色主题** — 背景 #f0f2f5，卡片 #ffffff，强调色 #10a37f。不使用深色/AI 风格。
- **卡片式布局** — 客户和产品用卡片网格展示，不用传统表格。
- **对话历史侧边栏** — 左侧会话列表，点击加载历史消息。
- **独立保存按钮** — 设置页每个配置模块一个保存按钮，不用全局保存。
- **打开即对话页** — 不需要工作台首页，直接进入对话界面。
- **DeepSeek 双版本** — V4-flash(chat) + V4-plus(reasoner) 都显示在模型下拉框中。

---

## 注意事项

1. **真实第一**: 绝不编造客户数据。搜不到就诚实告知，不要凑数。
2. **搜到客户必须评分**: 按 5 维度框架打分，标注数据来源 `[Google Maps]` `[官网]` `[官方注册库]`。
3. **Google Maps 不适合规模化**: 全球多国搜索会触发反爬（12次+跨国多语后封禁）。商用产品优先考虑 Apollo.io API；单市场少量搜索仍可用。
4. **海关数据默认显示出口商（Supplier）**: 进口商（Buyer）需在详情页查找。ImportYeti 搜索结果列表全是供应商，对外贸找客户无用。
5. **知识库为中文资料，邮件模板用英文**。
6. **信息不足时主动追问**（一次最多 2 个问题）。
7. **数据验证三源确认**: Google Maps + 官网 + 官方注册库 三源一致方可信任。
