# 已验证与已放弃的方案

> 更新: 2026-06-07 | 外贸助手 V0.1 设计过程中反复实测

---

## ✅ 已验证可行

| 方案 | 验证方式 | 适用场景 | 限制 |
|------|----------|----------|------|
| Google Maps 单市场搜索 | 德/英/美三国实测 | 手动搜索单个国家 | 12次跨国搜索后封禁 |
| 德国 Impressum 验证 | LEDclusive.de, HRB-Nr. 30006 | 德国市场 | — |
| 英国 Companies House | Mirrorstone Lighting Ltd, #07504296 | 英国市场 | — |
| 美国州注册查询 | LED Lighting Wholesale Inc., MI | 美国市场 | 各州系统不同 |
| docx XML 直接解析 | 14 个 "NULL 错误" 文件全部提取 | 处理 .docx 文件 | — |
| frankfurter.app 汇率 | EUR/CNY 实时返回 | 实时汇率 | — |
| 四合一搜索 API 组合 | Tavily+Serper+Brave+Bing=6500次/月 | 全球客户搜索 | 需各平台注册 |

---

## ❌ 已放弃

| 方案 | 原因 | 教训 |
|------|------|------|
| ImportYeti 浏览器抓取 | 只显示中国供应商（出口商），不显示进口商 | 海关数据"默认视角"是供应商端 |
| Google Maps 全球规模化 | 12次跨国多语搜索后全部返回空页 | 单市场可行 ≠ 全球可行 |
| UN COMTRADE API | API 改版 404 | 免费 API 不稳定是常态 |
| OEC.world | Cloudflare 拦截 | 数据网站都加了反爬 |
| Revor.ai | 成本转嫁用户，API 文档不透明 | 第三方依赖要评估稳定性 |
| v0.9 自建 Agent 流水线 | 脱离硬编码流程就失效 | 伪智能体不如真 Agent |

---

## 🔑 关键教训

1. **单次验证 ≠ 规模化可行**。Google Maps 德国 8 次成功，扩展到 5 国 12 次崩了。
2. **免费网站都有反爬**。ImportYeti 在浏览器能看，curl 403；OEC 被 Cloudflare 全拦。
3. **海关数据默认显示 Supplier**。搜 "LED lighting Germany" 返回深圳工厂，不是德国进口商。
4. **搜索引擎组合优于单一引擎**。Tavily(语义) + Serper(精确) + Brave(独立) + Bing(欧洲) 四路并发最稳。
