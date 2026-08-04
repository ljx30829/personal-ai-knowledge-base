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

## 重要边界

- 仓库必须保持 `Private`，不得启用 GitHub Pages。
- 不保存密码、令牌、Cookie、API Key、浏览器资料或原始客户敏感信息。
- 状态文件中的 `PASS/WATCH/FAIL/BLOCKED` 必须保留，不能把准备、草稿或本地运行写成上线、发送或成交。
- 大型 CSV、日志、视频、图片、压缩包和完整项目代码留在原工作区，本知识库保存摘要、来源路径和恢复方法。

当前远程状态：`PRIVATE_REMOTE_VERIFIED`。私有仓库为 [ljx30829/personal-ai-knowledge-base](https://github.com/ljx30829/personal-ai-knowledge-base)，`master` 已推送，GitHub Pages 未启用。
