---
updated: 2026-08-04
status: VERIFIED_METHOD_CURRENT_PATHS_REQUIRE_RECHECK
confidence: HIGH
sources:
  - ../../sources/inventory/workspaces.json
  - workspace-map.md
next_review: 2026-09-04
---

# 项目工作区跨设备迁移指南

私有知识库保存“要求、方法、状态和恢复路线”，不包含 `D:\codex` 等原项目的完整代码、图片、CSV、视频、数据库和运行环境。另一台电脑克隆知识库后能理解工作，但不能因此直接运行原项目。

## 三种可迁移状态

| 方式 | 包含内容 | 适用情况 | 限制 |
| --- | --- | --- | --- |
| 独立 Private Git 仓库 | 代码、小型配置模板、文档和测试 | 持续开发的项目 | 秘密和大文件必须排除；需确认远程已设置 |
| Codex task pack | `CODEX_TASK.md`、必要上下文、目标与证据路径 | 把单个任务交给另一个 Codex | 只恢复该任务，不等于完整项目 |
| 审阅后的项目归档 | Git 未跟踪但确需保留的素材/输出/工具 | 一次性迁移或灾备 | 体积大；需清除秘密、缓存和重复文件 |

不要把六个工作区全部塞进知识库仓库。每个项目独立迁移，知识库继续充当导航层。

## 前置盘点

在每个源工作区运行只读检查：

```powershell
git status --short
git remote -v
git branch --show-current
git ls-files
```

然后记录：

- 本地路径、项目用途和首要入口文件。
- 是否是有效 Git 工作树、当前分支和远程是否存在。
- 未跟踪文件数量以及其中哪些是源文件、业务证据、大型输出或秘密。
- 外部依赖的位置，例如 D: 工具、E: Docker 数据、浏览器或本地模型。
- 最新 `TASK_STATE.md`/`PROJECT_STATE.md` 和可复现的验证命令。

当前盘点显示多个主工作区有大量未跟踪文件，且没有在本次审阅中确认所有远程。因此不能写成“已经备份到 GitHub”。

## 方案 A：独立 Private Git 仓库

适合代码型工作区，例如 ArmorHue/Yufeng、自媒体蒸馏器和研究工具。

1. 先补 `.gitignore`，排除 `.env*`、凭据、浏览器资料、数据库、缓存、日志、视频、图片大包和生成输出。
2. 用 `git status --short` 逐项审阅待提交文件。
3. 运行项目自身测试和秘密扫描。
4. 在 GitHub 创建单独的 `Private` 仓库，确认可见性后再设置远程。
5. 提交并推送；登录另一个设备做只读克隆回读。
6. 记录仓库 URL、默认分支和最后验证提交到对应 `projects/` 页面，不记录 token。

不要从“GitHub 当前已登录”推断任何新仓库自动是私有，也不要把不同品牌或商店的凭据放进同一项目。

## 方案 B：Codex task pack

ArmorHue Site Builder 已能把任务包输出到：

```text
D:\codex\output\armorhue-site-builder\codex-task-packs
```

任务包至少包含：

```text
目标与完成定义
禁止动作与授权边界
源工作区路径和目标文件
已完成内容与当前阻塞
最新证据路径
精确验证命令
需要用户确认的事实
```

另一个 Codex 先读 `CODEX_TASK.md`，再按其中路径读取项目状态。任务包不能携带秘密，也不能把本机绝对路径误当成目标电脑已存在的路径。

## 方案 C：审阅后的归档

适合未跟踪的媒体、交付文件或尚未整理成 Git 的历史工作区。

1. 先生成文件清单和总大小，不马上压缩。
2. 按 `source`、`required-output`、`rebuildable-cache`、`secret` 分类。
3. 排除所有秘密、缓存、浏览器资料、邮箱内容和可重新生成的依赖。
4. 对保留文件生成 SHA-256 清单。
5. 用户确认大小和范围后再压缩到 D: 或 E:。
6. 在目标电脑解压后核对哈希和入口文件，再运行项目验证。

## 目标电脑恢复顺序

1. 克隆本知识库并读 `AGENTS.md`、`TASK_STATE.md`、`KNOWLEDGE_INDEX.md`。
2. 按对应项目选择独立仓库、任务包或归档并恢复到合适路径。
3. 修改知识页中的旧绝对路径只作为本机映射，不改变历史证据原路径。
4. 检查项目自己的 `AGENTS.md` 和状态文件。
5. 估算依赖体积和安装位置；大型安装先确认，优先 D:/E:。
6. 重新配置秘密和账号登录，不从 Git/知识库恢复凭据。
7. 运行只读检查、测试和本地预览；线上连接与修改仍需当次授权。
8. 把新的路径、验证日期和阻塞写回知识库。

## 验证标准

只有以下均满足，才可标记项目迁移 `PASS`：

- 目标电脑能读取项目入口与状态文件。
- Git/归档完整性通过，关键未跟踪源文件未遗漏。
- 依赖和外部工具要么已恢复，要么明确列为阻塞。
- 项目测试或最小运行命令通过。
- 没有秘密进入仓库、归档清单或可见日志。
- Shopify、邮件、社交、部署等外部动作仍保持未授权状态。

## 故障处理

| 现象 | 处理 |
| --- | --- |
| 克隆知识库后找不到项目代码 | 正常；按对应项目页恢复独立仓库、任务包或归档 |
| `git remote -v` 为空 | 说明没有已确认远程，先审计再创建 Private 仓库 |
| 大量 `??` 未跟踪文件 | 分类后再决定 Git、归档或排除，不用清理命令直接删除 |
| 旧绝对路径失效 | 建立目标路径映射并更新当前状态，保留历史证据路径 |
| 测试通过但线上不可用 | 本地迁移与线上状态分开验收，线上必须实时检查和授权 |

## 记录模板

```text
项目：<NAME>
源路径：<SOURCE_PATH>
迁移方式：PRIVATE_REPO | TASK_PACK | REVIEWED_ARCHIVE
远程/归档：<NON_SECRET_LOCATION>
分支或清单哈希：<VALUE>
未跟踪文件审阅：PASS | WATCH | FAIL
秘密扫描：PASS | FAIL
目标路径：<TARGET_PATH>
目标端验证：PASS | WATCH | FAIL
外部系统：NOT_CONNECTED | READ_ONLY | AUTHORIZED
阻塞与下一步：<TEXT>
```

## 相关文档

- [工作区地图](workspace-map.md)
- [技能跨设备迁移](skills-portability-guide.md)
- [Git 跨设备同步](../ai-workflows/git-cross-device-guide.md)

