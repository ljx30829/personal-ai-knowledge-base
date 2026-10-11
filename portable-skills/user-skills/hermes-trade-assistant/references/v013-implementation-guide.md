# V0.1.3 实现指南

> 本次会话（2026-06-07）从设计到代码的全流程实战总结

## 项目概述

V0.1.3 是一个 Hermes 技能驱动的外贸 B2B 客户开发工具，通过 Flask Web UI 提供浏览器操作界面。

## 核心架构

```
浏览器 (http://127.0.0.1:5821)
    ↓
Flask Web UI (client/main.py — ~190行)
    ├─ /api/chat → hermes_client.py → LLM API (DeepSeek/Qwen/OpenAI)
    ├─ /api/leads → database.py → SQLite CRUD
    ├─ /api/search → searcher.py → Tavily + Serper
    ├─ /api/settings → 数据库 settings 表
    └─ /api/health → Hermes + DB 状态检查
```

## 关键模块

| 文件 | 功能 | 要点 |
|------|------|------|
| `client/core/hermes_client.py` | LLM 通信 | 支持 DeepSeek/Qwen/OpenAI/custom；注入"外贸主管"系统提示词；SSE 流式 |
| `client/core/searcher.py` | 搜索 | Tavily + Serper 四路并发；关键词构建模板；去重 |
| `client/core/email_extractor.py` | 邮箱提取 | urllib 抓 HTML + 正则；10 国法律页面路径表；存活检测 |
| `client/core/scorer.py` | 评分 | 1-5 分制；网站特征检测；平台排除 |
| `client/core/database.py` | 数据库 | SQLite WAL；Leads/EmailLogs/Settings 三表；带默认值的 CRUD |
| `scripts/send_emails.py` | 发送 | SMTP 批量；支持 JSON/CSV/DB 输入；预览模式 |

## 前端要点

- **风格**: Codex 暗色主题（#1e1e2e 背景, #10a37f 强调色）
- **工作台按钮**: 差异化行为——找客户/写开发信/市场分析各自预填对话内容
- **客户管理**: 9 列表格 + 右侧详情面板 + CSV 导出
- **设置**: LLM 提供商选择 + API Key + 搜索 Key + SMTP
- **对话**: 显示"外贸主管·Trade Director"角色头衔

## LLM 配置

用户通过设置页面自配 API Key。`hermes_client.py` 从数据库读取配置：

```
llm_provider: deepseek | qwen | openai | custom
llm_model: deepseek-chat | qwen-plus | gpt-4o
llm_api_key: sk-...
llm_api_base: https://api.deepseek.com/v1
```

默认 Provider 是 DeepSeek，API Base 自动填充。

## 数据库

3 张核心表：
- `leads` — 客户线索（含 fit_score 1-5、status、source_keyword）
- `email_logs` — 邮件日志
- `settings` — 键值对配置（含 LLM/搜索/SMTP）

## 已验证的技术点

- ✅ Tavily API 实测可用（Key: tvly-dev-...，返回 10 条结构化结果）
- ✅ urllib + 正则提取邮箱（ledclusive.de → info@ledclusive.de）
- ✅ 德国 /impressum 路径直接命中邮箱
- ✅ Flask SSE 流式聊天正常工作
- ✅ Hermes 健康检查 `/api/health` 返回 hermes + db 状态

## 已知限制

- Google Maps 浏览器抓取 12 次跨国搜索后封禁（仅适合单市场少量使用）
- Tavily 返回结果偏供应商而非进口商（需要配合关键词优化）
- 邮件发送需用户自行配置 SMTP
- 暂无用户认证系统

## 会话关键决策记录

### 获客数据方案演变

1. **ImportYeti** — 放弃。只显示供应商(Supplier)，非进口商(Buyer)
2. **Google Maps 浏览器抓取** — 放弃规模化。12次跨国搜索后封禁。单市场少量可用
3. **Revor.ai** — 放弃。成本转嫁用户，API 文档不透明
4. **Apollo.io** — 备选付费方案，$49/月起，75次免费/月
5. **Tavily + Serper + Brave + Bing 四合一** — **当前方案**。6,500次/月免费

### 邮箱提取策略

- urllib.request（非浏览器）获取原始 HTML，快且不被反爬拦截
- 10 国法律页面路径表：DE→/impressum, UK→/terms, FR→/mentions-legales...
- 正则 `[\w.+-]+@[\w-]+(?:\.[\w-]+)+` 提取
- CloudFlare data-cfemail → 跳过，无法提取

### 抖音博主方案吸收

从 `generic-b2b-lead-generation` 技能包吸收了：
- 网站特征检测 → 邮件角度映射表
- 禁止模式清单（❌ 开头介绍自己公司等）
- 10 国法律页面路径（原来我们只有 3 国）
- 飞书表格作为备选数据库
