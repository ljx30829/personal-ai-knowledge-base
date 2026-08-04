# 跨设备 AI 知识库设计

日期：2026-08-04

## 一句话说明

把知识保存成一组普通 Markdown 文件，免费存放在私有 GitHub 仓库中。Codex 和其他 AI 只是获得授权后读取这些文件的工具，不拥有这些知识。

可以把它理解成一个只有你有钥匙的在线文件柜：

- GitHub 负责在电脑关机时继续保存文件。
- Markdown 保证文件不依赖某个软件。
- Obsidian 可以作为人工阅读和编辑界面，但不是必需品。
- Codex 通过 `AGENTS.md` 知道每次开始工作前应该读什么。
- 其他 AI 通过 `AI_CONTEXT.md` 获得相同的入口说明。

## 目标

1. 不购买服务器或知识库订阅。
2. 不要求任何一台个人电脑长期运行。
3. 在其他电脑上登录后可以继续使用同一份知识。
4. 不把知识锁定在 Codex、Obsidian 或某一家 AI 平台中。
5. 保留来源、更新时间和历史修改记录。
6. 默认私有，不创建公开网页或公开仓库。

## 不做的事情

- 第一阶段不部署 MCP 服务、向量数据库或大语言模型。
- 不开启 GitHub Pages。
- 不自动授权任何第三方 AI 读取仓库。
- 不在仓库中保存密码、Cookie、API Key、身份证件、银行卡信息或未经处理的客户敏感数据。
- 不声称所有 AI 都能自动连接私有 GitHub；没有 GitHub 连接能力的 AI 需要手动导入 Markdown 文件。

## 系统结构

```text
本地电脑 A ─┐
本地电脑 B ─┼─> 私有 GitHub 仓库 <─> 获得授权的 Codex / AI
手机编辑器 ─┘
```

GitHub 仓库是跨设备副本，Markdown 文件是唯一知识来源。任何索引、摘要或 AI 回答都可以重新生成，不能取代原始文件。

## 文件结构

```text
AGENTS.md
AI_CONTEXT.md
README.md
PROFILE.md
IDENTITY.md
KNOWLEDGE_INDEX.md
TASK_STATE.md
inbox/
knowledge/
projects/
sources/
decisions/
templates/
archive/
```

- `AGENTS.md`：Codex 的启动规则、读取顺序和安全边界。
- `AI_CONTEXT.md`：其他 AI 可以理解的通用使用说明。
- `PROFILE.md`：你的稳定背景、偏好、目标和禁区。
- `IDENTITY.md`：AI 应采用的角色、表达方式和决策原则。
- `KNOWLEDGE_INDEX.md`：知识主题及其文件位置。
- `TASK_STATE.md`：当前工作、已完成内容、阻塞项和下一步。
- `inbox/`：尚未整理的新材料。
- `knowledge/`：已经验证、可以长期复用的知识。
- `projects/`：按项目保存目标、状态和产出。
- `sources/`：视频、网页、会议和文档的来源记录。
- `decisions/`：重要决定、理由和日期。
- `templates/`：知识卡、来源卡、项目卡和交接模板。
- `archive/`：不再活跃但仍需保留的内容。

## 使用流程

### 当前电脑

1. 把新资料放入 `inbox/` 或 `sources/`。
2. Codex 读取 `AGENTS.md`、`PROFILE.md`、`KNOWLEDGE_INDEX.md` 和相关项目文件。
3. Codex 提炼内容，保留原始来源和可信度说明。
4. 确认后提交到私有 GitHub。

### 另一台电脑上的 Codex

1. 登录你的 GitHub 账号。
2. 克隆或打开同一个私有仓库。
3. 从仓库根目录启动 Codex。
4. Codex 根据 `AGENTS.md` 恢复上下文。

### 其他 AI

1. 如果该 AI 支持 GitHub 连接器，只授权这个私有仓库。
2. 如果不支持连接器，导入 `AI_CONTEXT.md` 和当前任务相关的 Markdown 文件。
3. AI 输出先进入 `inbox/`，经过检查后再进入长期知识区。

## 隐私和权限

- 远程仓库必须设置为 `Private`。
- 只给需要使用的账号或 AI 应用授权，并尽可能限定到单一仓库。
- 每次连接第三方 AI 前，先确认它会读取哪些文件。
- Git 会保留历史记录，因此秘密信息从一开始就不能提交。
- 对客户资料采用摘要、编号或脱敏版本；原始敏感文件保存在独立受控位置。

## 失败处理

- GitHub 暂时不可用：本地副本仍可读取，恢复后再同步。
- 某个 AI 不支持 GitHub：手动提供相关 Markdown 文件，不更换知识格式。
- 两台电脑同时修改冲突：保留双方内容，人工确认后合并。
- AI 写入错误：通过 Git 历史恢复到正确版本。
- 文件越来越多：先维护 `KNOWLEDGE_INDEX.md`，需要时再增加搜索服务。

## 验收标准

第一阶段完成时必须证明：

1. 本地目录结构和核心文档齐全。
2. `AGENTS.md` 能指导新的 Codex 会话找到必要上下文。
3. `AI_CONTEXT.md` 不依赖 Codex 专有术语。
4. 示例知识卡包含来源、日期、可信度和可复用结论。
5. 仓库内没有明显密钥、令牌或隐私数据。
6. Git 历史可以显示和恢复一次知识修改。
7. 远程仓库创建后经读取确认仍为 `Private`。

## 实施顺序

1. 创建本地目录、核心说明和模板。
2. 将用户提供的“自动化 AI 大脑”抖音视频整理为第一条来源卡和知识卡。
3. 在本地验证 Codex 启动读取流程。
4. 检查敏感内容和仓库状态。
5. 在用户确认仓库名称后，通过已登录的 GitHub 创建私有仓库。
6. 推送并读取确认远程仓库的可见性为 `Private`。

推荐远程仓库名称：`personal-ai-knowledge-base`。
