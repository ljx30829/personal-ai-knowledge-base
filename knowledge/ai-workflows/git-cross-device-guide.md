---
updated: 2026-08-04
status: VERIFIED_CURRENT_PRIVATE_REMOTE
confidence: HIGH
sources:
  - ../../README.md
  - portable-ai-brain.md
next_review: 2026-09-04
---

# Private GitHub 跨设备同步与 AI 使用指南

当前知识库远程是 Private 仓库 `ljx30829/personal-ai-knowledge-base`。它让另一台电脑在本机关闭时仍可读取已推送的知识，但不会自动同步尚未提交/推送的本地改动，也不会恢复原项目工作区或秘密。

## 一、在当前电脑查看状态

```powershell
Set-Location 'C:\Users\26014\Documents\知识库'
git status --short
git branch --show-current
git remote -v
git log -1 --oneline
```

推送前必须运行：

```powershell
python -m unittest discover -s tests -v
python scripts\validate_vault.py .
git diff --check
```

然后人工审阅 `git diff`。只有用户确认审阅稿和打包范围后，才提交本轮新增内容。

## 二、确认远程仍是私有

在浏览器登录授权的 GitHub 账号，打开：

```text
https://github.com/ljx30829/personal-ai-knowledge-base
```

确认页面显示 `Private`，Settings -> Pages 未启用，协作者/应用只有必要对象。登录 GitHub 不等于所有仓库或应用自动获得访问权。

## 三、另一台电脑首次克隆

1. 在另一台电脑登录同一 GitHub 账号，或给该账号单独授予私有仓库权限。
2. 安装轻量 Git；安装前仍确认下载量和目标盘。
3. 选择非系统盘或合适工作目录：

```powershell
New-Item -ItemType Directory -Force D:\codex\knowledge | Out-Null
Set-Location D:\codex\knowledge
git clone https://github.com/ljx30829/personal-ai-knowledge-base.git
Set-Location .\personal-ai-knowledge-base
```

4. 验证：

```powershell
git remote -v
git status --short
python scripts\validate_vault.py .
```

5. 从仓库根目录打开 Codex，让它先读 `AGENTS.md`、`TASK_STATE.md` 和 `KNOWLEDGE_INDEX.md`。

GitHub 登录凭据由 Git Credential Manager/浏览器流程保存，不粘贴进 Markdown、环境示例、脚本或聊天。

## 四、日常同步

开始工作前：

```powershell
git status --short
git pull --ff-only
```

结束工作前：

```powershell
git status --short
git diff
python -m unittest discover -s tests -v
python scripts\validate_vault.py .
git diff --check
```

确认后再 `git add`、`git commit` 和 `git push`。不使用会覆盖本地工作的 `git reset --hard` 或 `git checkout --`。如果两台设备都有改动，先提交各自工作，再通过正常 merge/rebase 解决冲突；不删除一边来“同步”。

## 五、给其他 AI 使用

### AI 支持 GitHub 私库连接

只授权这一个仓库和只需权限。让 AI 按顺序读：

1. `AI_CONTEXT.md`
2. `PROFILE.md`
3. `KNOWLEDGE_INDEX.md`
4. 当前任务相关的 `knowledge/` 页面
5. 对应 `projects/` 页面和日期化来源卡

默认读权限优先。需要 AI 修改仓库时，再单独授权写权限并审阅 diff。

### AI 不支持 GitHub 私库

上传 `AI_CONTEXT.md` 加当前任务相关的少量 Markdown。不要一次上传 `.git`、整个原项目、技能缓存、凭据或客户敏感数据。

### 另一个 Codex

最稳妥方式是在私库克隆目录根部启动。知识库告诉它如何工作；若任务需要真实项目代码，再按工作区迁移指南恢复对应项目。

## 六、冲突处理

```powershell
git status
git diff --name-only --diff-filter=U
```

逐个打开冲突文件，合并事实与日期，不机械选择“ours/theirs”。尤其保护：

- `TASK_STATE.md` 顶部最新状态。
- `PASS/WATCH/FAIL/BLOCKED/UNKNOWN` 区分。
- 用户新要求和安全边界。
- 两台设备各自新增的证据路径。

解决后重新运行完整测试和校验器，再提交。

## 七、秘密泄露响应

如果 `git diff`、校验器或 GitHub 历史中发现凭据：

1. 立即停止提交和推送。
2. 如果已推送，先按泄露处理轮换/撤销凭据；只删当前文件不够。
3. 确认影响的提交和远程副本后，制定受控历史清理方案。
4. 通知所有克隆端重新同步清理后的历史。
5. 更新 `.gitignore` 和校验规则，避免再次发生。

不要在聊天中粘贴发现的秘密来求助，只报告文件路径和已脱敏的错误类型。

## 八、离线、关机和免费边界

- GitHub 免费私有仓库可保存已推送的文本知识；电脑关机后仍能从其他设备登录查看。
- 未推送的本地修改只在当前硬盘上，关机不丢但其他设备看不到。
- GitHub 不会替你运行本地 Docker、中转站、Whisper、浏览器或自动化。
- 仓库是否继续免费、AI 连接器是否收费、私库配额和权限模型可能变化，使用前以平台当前页面为准。

## 记录模板

```text
设备：<DEVICE_LABEL>
日期：YYYY-MM-DD HH:mm +08:00
仓库：ljx30829/personal-ai-knowledge-base
可见性：PRIVATE_VERIFIED | UNKNOWN | FAIL
分支：<BRANCH>
同步前提交：<SHA>
同步结果：PASS | CONFLICT | FAIL
校验器：PASS | FAIL
秘密检查：PASS | BLOCKED
AI 授权：NONE | READ_ONLY | WRITE
下一步：<TEXT>
```

## 相关文档

- [跨设备 AI 大脑](portable-ai-brain.md)
- [工作区迁移指南](../system/workspace-portability-guide.md)
- [技能跨设备迁移指南](../system/skills-portability-guide.md)
