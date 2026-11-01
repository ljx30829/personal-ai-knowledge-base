# 我的 AI 知识库

这是一个公开、可迁移的 Markdown 知识库。GitHub 负责跨设备保存；仅保留脱敏后的通用方法，不放入原始会话、客户/邮件资料、凭据、私人路径或受限素材。

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
- `portable-skills/`：经过凭据过滤、内容筛选和哈希记录的可迁移技能包；原始加载路径保持不变，分类清单只用于检索。
- `docs/workflows/index.html`：离线交互工作流地图，从 13 类工作目的进入完整流程、技能卡和仓库内原文。

## 关键操作指南

- [Shopify 接入与验证指南](knowledge/sites/shopify-connection-guide.md)：主题 CLI、Admin API、Storefront API、权限、验证和发布边界。
- [v2rayN 节点配置与出口验证指南](knowledge/infrastructure/node-configuration-guide.md)：客户端、VPS、住宅出口、切换、验证和排障。
- [New API 中转站配置与恢复指南](knowledge/infrastructure/relay-configuration-guide.md)：Docker、origin、Cloudflare、模型路由和跨主机恢复。
- [外贸执行手册](knowledge/trade/foreign-trade-execution-runbook.md)：发现、发送包、邮箱风险门、预演、受控发送和监督。
- [自媒体蒸馏运行手册](knowledge/media/self-media-distillation-runbook.md)：账号准备、导入、Whisper 转写、审计、蒸馏和搜索。
- [客户优先选品执行手册](knowledge/commerce/customer-first-research-runbook.md)：客户池、访谈、付费证据、概念和逐级淘汰门。
- [技能迁移](knowledge/system/skills-portability-guide.md)、[自动化重建](knowledge/system/automation-rebuild-guide.md)、[工作区迁移](knowledge/system/workspace-portability-guide.md)和 [Git 跨设备同步](knowledge/ai-workflows/git-cross-device-guide.md)：另一台电脑恢复可执行能力。
- [项目迁移工具包](knowledge/system/project-migration-toolkit.md)：盘点项目入口和依赖、生成安全哈希清单，并在目标电脑做 doctor/smoke 检查。
- [完整跨设备恢复入口](knowledge/system/complete-recovery-runbook.md)：在另一台电脑恢复知识库、两个独立项目仓库和筛选后的技能文件。
- [可迁移技能包](portable-skills/README.md)：恢复当前筛选后的用户技能和插件技能，并按 `portable-skills-manifest.json` 做完整性校验。
- [离线工作流地图](docs/workflows/README.md)：查看工作目的、底层逻辑、授权门、失败恢复、对应技能和验证边界。

## 审阅与打包

- [完整知识与要求审阅稿](reports/full-knowledge-requirements-review-2026-08-04.md)：打包前逐项确认长期要求、知识、项目、技能、自动化和工作区范围。
- 历史记录：知识库曾于 2026-08-04 完成打包；相关历史验证结果见对应审阅报告。旧的本地归档位置不在公开文档中列出。

跨设备恢复时按当前迁移指南选择合适的短路径；依赖、远端访问和平台状态须在目标设备重新验证。

## 重要边界

- 当前 GitHub 仓库保持 `Public`；仅允许发布脱敏后的通用知识。可见性变更需另行按用户授权执行。
- 不保存密码、令牌、Cookie、API Key、浏览器资料或原始客户敏感信息。
- 状态文件中的 `PASS/WATCH/FAIL/BLOCKED` 必须保留，不能把准备、草稿或本地运行写成上线、发送或成交。
- 大型 CSV、日志、视频、图片、压缩包和完整项目代码留在原工作区；公开知识库只保留脱敏摘要、公开来源和通用恢复方法，不记录私人路径。

当前远端页面于 2026-11-01 检查为 `Public`，默认分支为 `master`。GitHub Pages 状态本轮未检查。
