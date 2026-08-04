# 我的 AI 知识库

这是一个私有、可迁移的 Markdown 知识库。GitHub 负责跨设备保存，Codex、Claude、Gemini、Cursor 或其他 AI 只在获得授权后读取这些文件。

## 从这里开始

- 人工浏览：先看 [知识导航](KNOWLEDGE_INDEX.md)。
- Codex：从仓库根目录启动，它应先读取 [AGENTS.md](AGENTS.md)。
- 其他 AI：先提供 [AI_CONTEXT.md](AI_CONTEXT.md)，再提供当前任务相关文件。
- 恢复项目：先看 [TASK_STATE.md](TASK_STATE.md)，再打开对应的 `projects/` 页面。

## 主要内容

- `knowledge/`：已经提炼、可长期复用的方法和规则。
- `projects/`：项目现状、证据、阻塞项和恢复步骤。
- `sources/`：来源卡、技能清单、自动化清单和工作区目录。
- `inbox/`：新资料的暂存区，不能直接当作长期知识。
- `decisions/`：重要决定及其理由。
- `templates/`：统一的知识卡、来源卡和项目状态模板。

## 关键操作指南

- [Shopify 接入与验证指南](knowledge/sites/shopify-connection-guide.md)：主题 CLI、Admin API、Storefront API、权限、验证和发布边界。
- [v2rayN 节点配置与出口验证指南](knowledge/infrastructure/node-configuration-guide.md)：客户端、VPS、住宅出口、切换、验证和排障。
- [New API 中转站配置与恢复指南](knowledge/infrastructure/relay-configuration-guide.md)：Docker、origin、Cloudflare、模型路由和跨主机恢复。
- [外贸执行手册](knowledge/trade/foreign-trade-execution-runbook.md)：发现、发送包、邮箱风险门、预演、受控发送和监督。
- [自媒体蒸馏运行手册](knowledge/media/self-media-distillation-runbook.md)：账号准备、导入、Whisper 转写、审计、蒸馏和搜索。
- [客户优先选品执行手册](knowledge/commerce/customer-first-research-runbook.md)：客户池、访谈、付费证据、概念和逐级淘汰门。
- [技能迁移](knowledge/system/skills-portability-guide.md)、[自动化重建](knowledge/system/automation-rebuild-guide.md)、[工作区迁移](knowledge/system/workspace-portability-guide.md)和 [Git 跨设备同步](knowledge/ai-workflows/git-cross-device-guide.md)：另一台电脑恢复可执行能力。

## 审阅与打包

- [完整知识与要求审阅稿](reports/full-knowledge-requirements-review-2026-08-04.md)：打包前逐项确认长期要求、知识、项目、技能、自动化和工作区范围。
- 当前状态：`PACKAGE_BUILT_LOCAL`。用户已于 2026-08-04 确认打包；本地总包位于 `D:\codex\output\personal-ai-knowledge-package-20260804-230623.zip`，本轮改动尚未提交或推送。

Windows 解压时建议使用 `D:\AIKB` 之类的短路径。插件缓存包含较深目录，解压到长用户名/多层目录时可能触发旧版 Windows 260 字符限制。

## 重要边界

- 仓库必须保持 `Private`，不得启用 GitHub Pages。
- 不保存密码、令牌、Cookie、API Key、浏览器资料或原始客户敏感信息。
- 状态文件中的 `PASS/WATCH/FAIL/BLOCKED` 必须保留，不能把准备、草稿或本地运行写成上线、发送或成交。
- 大型 CSV、日志、视频、图片、压缩包和完整项目代码留在原工作区，本知识库保存摘要、来源路径和恢复方法。

当前远程状态：`PRIVATE_REMOTE_VERIFIED`。私有仓库为 [ljx30829/personal-ai-knowledge-base](https://github.com/ljx30829/personal-ai-knowledge-base)，`master` 已推送，GitHub Pages 未启用。
