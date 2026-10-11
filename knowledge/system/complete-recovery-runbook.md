---
updated: 2026-10-11
status: PASS_RECOVERY_ENTRYPOINT_READY
confidence: HIGH
sources:
  - ../../scripts/bootstrap_portable_workspace.ps1
  - ../../scripts/install_portable_skills.py
  - project-migration-toolkit.md
---

# 完整跨设备恢复入口

另一台电脑需要三个 Private GitHub 仓库：

- `personal-ai-knowledge-base`：长期知识、恢复脚本和筛选后的技能文件。
- `account-knowledge-distiller`：可运行的自媒体蒸馏源码、测试和恢复入口。
- `independent-site-research-vault`：经过审阅的独立站研究文档，不是应用源码。

## Windows 恢复

```powershell
git clone https://github.com/ljx30829/personal-ai-knowledge-base.git D:\AIWorkspace\knowledge-vault
cd D:\AIWorkspace\knowledge-vault
.\scripts\bootstrap_portable_workspace.ps1 -Root D:\AIWorkspace
.\scripts\bootstrap_portable_workspace.ps1 -Root D:\AIWorkspace -Execute
```

第一条脚本命令只输出计划，不写入；带 `-Execute` 才克隆两个项目仓库、审计并安装已审阅的用户技能与插件技能，再运行源码测试。已有同名文件不会被覆盖。

## macOS / Linux 恢复

```sh
git clone https://github.com/ljx30829/personal-ai-knowledge-base.git "$HOME/AIWorkspace/knowledge-vault"
cd "$HOME/AIWorkspace/knowledge-vault"
sh scripts/bootstrap_portable_workspace.sh "$HOME/AIWorkspace"
EXECUTE=1 sh scripts/bootstrap_portable_workspace.sh "$HOME/AIWorkspace"
```

## 外部依赖

核心源码使用 Python 标准库，不要求联网安装 Python 包。FFmpeg 和 Whisper 属于可选本地工具；浏览器、模型、Docker 镜像和其他大型依赖必须先估算下载量、安装量和目标磁盘，再单独确认。

## 不能由 Git 恢复的状态

API 密钥、Cookie、账号登录、浏览器资料、邮件、私有客户数据、平台额度、远程服务器、数据库、域名和线上部署状态不会进入仓库。目标电脑需要重新授权，doctor 或测试通过也不等于线上系统已连接。
