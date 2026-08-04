---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - ../../sources/videos/douyin-7655909545654950769.md
  - ../../docs/superpowers/specs/2026-08-04-portable-ai-knowledge-base-design.md
next_review: 2026-09-04
---

# 跨设备 AI 大脑

## 实际方案

知识的唯一标准格式是普通 Markdown，私有 GitHub 仓库负责保存和跨设备同步：

```text
本机文件 -> Git 提交 -> 私有 GitHub -> 另一台电脑或获授权的 AI
```

不需要付费知识库、常驻电脑、数据库、向量库、本地模型或公开网页。Obsidian 可以作为阅读和编辑界面，但不是同步和 AI 授权层。

## 三类入口

- 人工查看：打开 [知识导航](../../KNOWLEDGE_INDEX.md)。
- Codex：从仓库根目录启动，先读 [AGENTS.md](../../AGENTS.md)。
- 其他 AI：先提供 [AI_CONTEXT.md](../../AI_CONTEXT.md)，再提供相关 `knowledge/` 和 `projects/` 文件。

## 文件职责

- `PROFILE.md`：稳定偏好、目标与禁区。
- `IDENTITY.md`：AI 的角色、表达和决策原则。
- `AGENTS.md`：Codex 的强制读取顺序与安全规则。
- `AI_CONTEXT.md`：不依赖某一 AI 产品的通用入口。
- `KNOWLEDGE_INDEX.md`：主题导航。
- `TASK_STATE.md`：知识库自身的最新状态。
- `knowledge/`：已提炼、可长期复用的方法。
- `projects/`：带日期的项目状态、阻塞、证据和恢复步骤。
- `sources/`：来源卡和机器清单。
- `inbox/`：未经审核的新材料。

## 知识摄入流程

1. 新网页、视频、文档或对话先形成来源卡，记录来源、日期、可信度和缺口。
2. 音视频需要时在原工作区转写；知识库只保存摘要、证据路径和必要的小型文本。
3. 把可重复使用的方法写入 `knowledge/`，把会变化的当前状态写入 `projects/`。
4. 更新导航和 `TASK_STATE.md`，运行校验器检查结构、断链和疑似秘密。
5. 提交 Git；确认无敏感内容后推送到私有 GitHub。

## 在别的地方怎么用

### 另一台电脑上的 Codex

1. 登录自己的 GitHub。
2. 克隆同一个私有仓库。
3. 在仓库根目录打开 Codex。
4. 让 Codex按 `AGENTS.md` 恢复上下文。

### 支持私有 GitHub 的其他 AI

只授权这个仓库，先让它读 `AI_CONTEXT.md`、`PROFILE.md`、`KNOWLEDGE_INDEX.md` 和当前项目页。授权范围应限制到单一私有仓库。

### 不支持 GitHub 的其他 AI

上传 `AI_CONTEXT.md` 和当前任务相关的少量 Markdown 文件。不要一次上传整个大型原始工作区，也不要上传凭据或客户敏感数据。

## 更新和演进

- 第一阶段按实际工作手动更新，不要求本机持续开机。
- 当前自动化目录只是知识来源，不自动把所有运行日志复制进仓库。
- 未来可在确认隐私与 GitHub 权限后增加云端定时索引或 GitHub Actions，但不是当前依赖。
- 每次新增耐久知识时同步更新来源、主题页、项目页、导航和知识库状态。

## 安全边界

- 远程仓库必须是 `Private`，GitHub Pages 必须关闭。
- 密码、令牌、Cookie、密钥、浏览器资料、邮箱正文和原始客户敏感记录永不提交。
- Git 历史会保留删除前的内容，所以秘密从第一次提交起就不能出现。
- 其他 AI 只有在用户明确授权仓库或上传文件后才能读取，不假设“所有 AI 自动共享记忆”。

## 效果衡量

视频的“每天省一半时间”不是已验证结果。可用下列真实指标评估：

- 新会话恢复到可执行状态所需时间。
- 重复解释用户要求和项目背景的次数。
- 因使用过期状态造成的返工次数。
- 新知识从来源卡进入可复用主题页的时间。
- 跨电脑或跨 AI 交接能否在不暴露秘密的情况下完成。

## 未知项

- 远程 GitHub 仓库尚未创建，因此跨设备访问尚未完成。
- 不同 AI 对私有 GitHub 的连接能力和权限模型不同，需要逐个平台确认。

## 来源与证据

- [视频来源卡](../../sources/videos/douyin-7655909545654950769.md)
- [知识库设计](../../docs/superpowers/specs/2026-08-04-portable-ai-knowledge-base-design.md)
