# 当前维护状态（2026-11-24）

日报和九个既有项目入口更新，新增Pachat与侧睡用品指南。当前仅本地准备，GitHub写入认证及内置浏览器不可用阻塞新PR；未同步，不推进远端水位。旧日期为历史，当前入口见[近期项目](PROJECTS_RECENT.md)。

# 当前维护状态（2026-11-23）

日报23、21日晚补录及22日覆盖说明已本地准备；更新七份原指南，新增[音乐工具研究](PROJECT_MUSIC_CLIENT_RESEARCH.md)与[数字商城规划](PROJECT_DIGITAL_GOODS_STORE.md)。158文档与43项既有测试通过；本轮尚未推送/新PR/同步，浏览器设置与Git认证阻塞仍在。当前入口见[近期项目](PROJECTS_RECENT.md)。以下旧日期为历史。

# 当前维护状态（2026-11-21）

日报21与20日晚补录、七既有项目主文档已增补，新增[自有测试面板指南](PROJECT_CLOUDFLARE_TEST_PANEL.md)。当前只在本地日期分支；Work设置禁用本地浏览器且Git无可用认证，尚未新PR/推送/同步。远端水位不推进，以下历史状态不代表本轮已同步。

# 我的 AI 知识库

这是一个公开、可迁移的 Markdown 知识库，只保存脱敏通用方法。GitHub 负责跨设备保存，Codex、Claude、Gemini、Cursor 或其他 AI 只在获得授权后读取这些文件。

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
- 历史打包已完成；原离线包及详细定位保留受控本地，不提交公开库。最新同步以 TASK_STATE 和当前PR回读为准。

Windows解压建议使用短路径；长目录可能触发旧版路径长度限制。

## 重要边界

- 仓库保持 Public，仅提交脱敏通用方法；私人材料不进入公开库。
- 不保存密码、令牌、Cookie、API Key、浏览器资料或原始客户敏感信息。
- 状态文件中的 `PASS/WATCH/FAIL/BLOCKED` 必须保留，不能把准备、草稿或本地运行写成上线、发送或成交。
- 大型 CSV、日志、视频、图片、压缩包和完整项目代码留在原工作区，本知识库保存摘要、来源路径和恢复方法。

当前远程可见性已核为 Public，默认分支 master；本轮本地增量尚未同步，详见 TASK_STATE。


稳定项目入口新增 [OpenMausBot](PROJECT_OPENMAUSBOT.md)；其余项目继续从[近期项目](PROJECTS_RECENT.md)进入。


2026-11-16下午：新增[AI短剧与漫剧制作完整指南](PROJECT_SHORT_DRAMA.md)，继续回写各稳定项目入口。此次本地更新尚未推送/创建PR；历史PR成功不代表本轮同步，状态以[TASK_STATE](TASK_STATE.md)为准。


2026-11-25：新增[岛仔](PROJECT_DAOZAI.md)及[OpenMontage](PROJECT_OPENMONTAGE.md)完整稳定指南，原项目继续跨日回写。当前仅本地，实际同步状态见[TASK_STATE](TASK_STATE.md)。
