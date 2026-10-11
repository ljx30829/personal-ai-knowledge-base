# 外贸助手 V0.1.3 — 代码库指南

> 完整的 Python Flask Web 应用，实现了客户搜索→提取→评分→邮件发送全流程。

## 项目位置

`D:\Hermes Foreign Trade\`

## 目录结构

```
D:\Hermes Foreign Trade\
├── SKILL.md                          ← Hermes 技能入口
├── requirements.txt                  ← flask, requests
│
├── client/                           ← Flask Web 应用
│   ├── main.py                       ← 🔑 入口: python client/main.py
│   │   └── 路由: /api/chat, /api/conversations, /api/leads,
│   │             /api/products, /api/templates, /api/followup-rules,
│   │             /api/settings, /api/health, /api/stats
│   │
│   ├── core/
│   │   ├── database.py               ← SQLite + 全部 CRUD
│   │   │   └── 表: conversations, chat_history, leads,
│   │   │           products, email_templates, followup_rules,
│   │   │           email_logs, settings
│   │   ├── hermes_client.py          ← LLM 通信（支持 DeepSeek/Qwen/OpenAI）
│   │   │   └── 注入外贸主管 SYSTEM_PROMPT
│   │   │   └── 从 DB settings 读取 llm_provider/llm_model/llm_api_key
│   │   ├── email_extractor.py        ← 邮箱提取 + 10国法律页路径
│   │   ├── searcher.py               ← Tavily + Serper API 封装
│   │   └── scorer.py                 ← 1-5 评分 + 网站特征检测
│   │
│   ├── web/
│   │   ├── templates/index.html      ← 单页面应用
│   │   └── static/
│   │       ├── css/style.css         ← 亮色主题（#f0f2f5 背景）
│   │       └── js/app.js             ← 前端逻辑（SSE 聊天 + CRUD）
│   │
│   └── data/
│       ├── schema.sql
│       └── hermes.db
│
├── scripts/
│   └── send_emails.py                ← 邮件批量发送（--db/--json/--csv）
│
├── skills/
│   └── hermes-trade-assistant/       ← 完整技能包（可分享）
│
└── docs/                             ← 设计文档
    ├── 外贸助手V0.1.3_设计文档.md
    ├── 数据质量评估框架.md
    ├── 英美客户评估报告.md
    └── 获客数据方案_免费付费组合.md
```

## 启动

```bash
cd D:\Hermes Foreign Trade
pip install flask requests
python client/main.py
# → http://127.0.0.1:5821
```

## 核心工作流（代码层面）

```
用户发消息 → POST /api/chat → save_message(conv_id, 'user', msg)
    ↓
hermes_client.chat_stream(msg, conv_id)
    ↓ 注入系统提示词 "你是一个外贸主管..."
    ↓ 根据 settings 表选择 LLM Provider
    ↓ SSE 流式返回 → 前端 EventSource 接收
    ↓
返回 [DONE] → save_message(conv_id, 'assistant', full_response)
```

## 关键技术决策

1. **不经过 Hermes Gateway 中转** — hermes_client.py 直接调用 LLM API
   - 原因：用户自配 API Key，避免 401 问题
   - 支持: DeepSeek (chat/reasoner), 通义千问, OpenAI, 自定义
   
2. **亮色主题** — 用户明确要求，拒绝深色 AI 风格
   - 背景: #f0f2f5, 卡片: #fff, 强调色: #10a37f
   
3. **卡片式布局** — 客户和产品用卡片网格，不用表格
   - 每卡显示: 名称/评分/网站/邮箱/国家/类型/操作按钮
   
4. **对话历史** — 侧边栏会话列表，点击加载历史消息
   - conversations + chat_history 双表存储
   - 自动用首条用户消息作标题（前30字）
   
5. **独立保存按钮** — 设置页每个模块单独保存
   - AI/搜索/公司/SMTP 四个 section 各一个保存按钮
   
6. **DeepSeek 双版本** — V4-flash(chat) + V4-plus(reasoner)
   - 模型选择下拉框清晰标注
   
7. **Google Maps 方案已弃用** — 12次跨国搜索后反爬封禁
   - 替代方案: Tavily + Serper 免费 API 池 (6,500次/月)
