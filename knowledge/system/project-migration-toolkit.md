---
updated: 2026-10-11
status: PASS_TOOLKIT_ADDED_WATCH_PROJECTS_NOT_PACKAGED
confidence: HIGH
sources:
  - ../../scripts/build_project_inventory.py
  - ../../scripts/check_project_dependencies.py
  - ../../scripts/build_project_manifest.py
  - ../../scripts/doctor_project.ps1
  - ../../scripts/smoke-test.ps1
---

# 项目迁移工具包

这组工具把“另一台电脑能恢复项目”拆成可核对的步骤，但不会把本机所有工作区直接塞进知识库，也不会把外部服务、账号或依赖安装结果伪装成已恢复。

## 当前范围

工具会为每个候选工作区记录：Git 是否存在、入口文件、状态文件、依赖文件、疑似秘密文件名和大文件摘要。它只读取文件名、大小和少量版本提示，不复制源代码、`.env`、Cookie、Token、浏览器资料、数据库、缓存、日志或大媒体。

用户明确排除的品牌、产品领域和内容类别会自动标记为 `EXCLUDED`，不得生成项目清单或文件哈希清单。历史知识页不代表这些资料会进入新的项目迁移包。

## 推荐流程

1. 盘点：`python scripts/build_project_inventory.py --output sources/inventory/project-migration.json`。
2. 人工审阅每个项目的 `status`、`entrypoints`、`state_files`、`dependency_files` 和 `secret_candidates`。
3. 对需要保留的项目建立独立 Private Git 仓库或审阅后的归档；知识库只保存入口、证据路径和恢复方法。
4. 对目标电脑准备安装依赖前，先记录运行时、锁文件、预计下载量、安装位置和 D:/E: 替代位置；大型安装必须先确认。
5. 生成安全清单：`python scripts/build_project_manifest.py --project-path <项目路径> --output <项目路径外>/manifest.json`。
6. 源码型项目可用 `python scripts/export_project_source.py --project-path <项目路径> --output <D:/E:目标目录> --execute` 生成只含源码、测试、示例和安全入口文档的迁移包；默认先不加 `--execute` 做估算。
7. 目标端运行 `scripts/doctor_project.ps1 -ProjectPath <项目路径>`，或在 POSIX 系统运行 `scripts/doctor_project.sh --project-path <项目路径>`。
8. 只有项目明确提供并经用户授权的本地命令才能运行 smoke test：`scripts/smoke-test.ps1 -ProjectPath <项目路径> -Command '<命令>'`。没有命令时只返回 `WATCH_NO_SMOKE_COMMAND`。
9. 将目标端验证结果、路径映射和未恢复的外部服务写回对应 `projects/` 页面和 `TASK_STATE.md`。

## 状态解释

- `PASS`：工具发现项目路径和依赖描述完整，且没有文件名级秘密候选；不等于依赖已安装或服务可用。
- `WATCH_NO_SMOKE_COMMAND`：项目路径可读，但没有安全的项目自带最小命令。
- `EXCLUDED`：命中明确排除领域，不生成迁移清单。
- `FAIL`：缺少项目、检测到秘密候选或明确的 smoke 命令失败。
- `BLOCKED`/`UNVERIFIED`：由项目状态文件保留，不能被盘点工具擅自升级。

## 不会自动恢复的部分

Python/Node/Docker/浏览器/模型等外部依赖、API Key、Cookie、账号登录、Shopify/VPS/数据库/Redis、域名和线上部署仍需目标电脑重新配置和授权。工具包不安装任何包，也不连接线上系统。

## 当前源码包示例

自媒体蒸馏器已生成一个源码-only 包用于跨设备验证：

- Private 仓库：`https://github.com/ljx30829/account-knowledge-distiller`
- 远端提交：`41a53041d32b063b5d97744ca33af3cdbc92b354`
- 本地 ZIP：`D:\codex\output\self-media-source-export-20261011-complete2.zip`
- ZIP SHA-256：`6B1DC3D4269E59FF79661737B74ADF4E343F0524B0BD7E0DF5949E40A2122CD7`
- 内容：53 个源码/测试/示例/README 文件，约 0.59 MiB；解压后 118 个测试通过。
- 准备入口：`scripts/setup.ps1`、`scripts/setup.sh` 和 `DEPENDENCY_REPORT.json`；核心 Python 依赖为空。
- 未包含：账号资料、原始媒体、生成输出、浏览器/缓存、机器本地工具和秘密。

独立站研究文档也已单独迁移：

- Private 仓库：`https://github.com/ljx30829/independent-site-research-vault`
- 远端提交：`74f6cbc80cd2c10a3c6cdcab6a20a908973f8da1`
- 本地 ZIP：`D:\codex\output\independent-site-research-export-20261011-clean.zip`
- ZIP SHA-256：`78152A3F794A4EF6F20981060AE20EA490351D6DDF6C0883C0B6259E42F428A8`
