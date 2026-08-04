---
updated: 2026-08-04
status: VERIFIED_LOCAL_TOOLS_ONLY
confidence: HIGH
sources:
  - ../../sources/inventory/skills.json
  - ../../sources/codex-inventory/codex-inventory.md
  - ../../scripts/export_portable_skills.py
  - ../../scripts/install_portable_skills.py
next_review: 2026-09-04
---

# Codex 技能跨设备迁移指南

这份指南解决“另一台电脑或另一个 Codex 不只看见技能名称，还能实际加载技能文件”的问题。知识库中的技能清单只是索引；真正可执行的技能正文和配套脚本仍位于 Codex 用户目录，必须另行导出和安装。

## 当前已核对范围

| 来源 | 路径 | `SKILL.md` 数量 | 2026-08-04 体积快照 |
| --- | --- | ---: | ---: |
| 用户技能 | `C:\Users\26014\.codex\skills` | 186 | 约 91.60 MB |
| 插件缓存 | `C:\Users\26014\.codex\plugins\cache` | 65 | 约 31.72 MB |
| 合计 | 两个来源 | 251 | 约 123.32 MB |

插件缓存是某一时点的下载结果，不等于长期稳定的用户技能。默认只恢复用户技能；插件缓存只有在目标环境无法重新安装同一插件、且用户确认需要固定快照时才恢复。

2026-08-04 的过滤后 dry-run 为 2,468 个文件、251 个 `SKILL.md`、108,369,128 bytes（约 103.35 MiB）。它还排除了 1 个指向版本目录的插件 `latest` junction，避免同一技能被重复打包。文件和体积会随技能更新而变化，实际导出前必须重新 dry-run。

## 前置条件

1. 源电脑能读取上述两个目录。
2. 目标电脑已安装 Codex，或至少已确定目标 `CODEX_HOME`。
3. 导出目录不能放在源技能目录里面，且必须是尚不存在的新目录。
4. 先运行估算，不执行复制；约 123 MB 的实际导出和后续压缩仍需用户确认。
5. 不把技能包提交到当前知识库，除非用户审阅后明确决定存放方式。

## 一、只读估算

在知识库根目录运行：

```powershell
python scripts\export_portable_skills.py `
  --output D:\codex\output\portable-skills-review
```

没有 `--execute` 时状态必须是 `DRY_RUN`，目标目录也不应创建。重点核对：

- `file_count`：拟导出的全部文件数。
- `skill_file_count`：拟导出的 `SKILL.md` 数量。
- `total_bytes`：实际复制前的体积估算。
- `excluded`：因秘密风险、缓存、日志、数据库或链接而排除的文件数。

## 二、经确认后导出

使用一个全新的日期化目录：

```powershell
python scripts\export_portable_skills.py `
  --output D:\codex\output\portable-skills-YYYYMMDD `
  --execute
```

导出器会保留两棵独立目录：

```text
portable-skills-YYYYMMDD/
  user-skills/
  plugin-cache/
  portable-skills-manifest.json
```

它默认排除 `.env*`、名称含 token/secret/session/cookie/credential 的文件、私钥/证书、数据库、日志、缓存、虚拟环境、`node_modules`、符号链接和 Windows junction。名称过滤不能证明内容绝对无秘密，导出后仍需运行知识库校验器和人工抽查。

## 三、完整性验证

清单给每个导出文件保存 SHA-256。抽查单个文件：

```powershell
$manifest = Get-Content -Raw -Encoding UTF8 `
  D:\codex\output\portable-skills-YYYYMMDD\portable-skills-manifest.json |
  ConvertFrom-Json
$item = $manifest.files | Select-Object -First 1
$actual = (Get-FileHash -Algorithm SHA256 `
  (Join-Path 'D:\codex\output\portable-skills-YYYYMMDD' `
    (Join-Path $item.source $item.path))).Hash.ToLower()
$actual -eq $item.sha256
```

结果应为 `True`。安装器还会在 dry-run 和实际安装前核对全部选中源文件：缺失、额外文件或任一 SHA-256 不一致都会停止。转移介质或私有远程存储损坏时，停止安装并重新导出。

## 四、在另一台电脑预演安装

先把导出目录安全传到目标电脑，再运行：

Windows 上先把总包解压到 `D:\AIKB`、`D:\transfer` 等短路径。插件缓存目录层级较深，解压到长用户名下的多层目录可能触发旧版 Windows 260 字符限制。

```powershell
python scripts\install_portable_skills.py `
  --bundle D:\transfer\portable-skills-YYYYMMDD `
  --target-codex-home C:\Users\<USER>\.codex
```

没有 `--execute` 时会先完整验证 manifest，再返回源文件数、可安装数、冲突跳过数和安装体积。`manifest_verified` 必须是 `true`。确认目标路径后再安装用户技能：

```powershell
python scripts\install_portable_skills.py `
  --bundle D:\transfer\portable-skills-YYYYMMDD `
  --target-codex-home C:\Users\<USER>\.codex `
  --execute
```

安装器绝不覆盖同名现有文件；冲突会计入 `conflicts_skipped`。需要插件缓存时必须额外明确加入：

```powershell
python scripts\install_portable_skills.py `
  --bundle D:\transfer\portable-skills-YYYYMMDD `
  --target-codex-home C:\Users\<USER>\.codex `
  --include-plugin-cache `
  --execute
```

## 五、验证技能真的可用

1. 目标目录存在相应 `skills\<skill-name>\SKILL.md`。
2. 重启 Codex，让它重新扫描技能目录。
3. 查看目标 Codex 的技能列表，确认名称出现。
4. 用一个只读小任务显式指定技能，确认 Codex 能完整读取 `SKILL.md`。
5. 如果技能引用 `scripts/`、`templates/` 或 `assets/`，逐项确认相对路径仍存在。
6. 如果技能依赖未安装的 CLI、Python 包、浏览器、模型或 MCP，按该技能说明单独安装；迁移技能文件不等于迁移运行环境。

## 六、零付费存放选择

| 方式 | 适用情况 | 注意事项 |
| --- | --- | --- |
| 单独 Private GitHub 仓库 | 希望多设备 Git 同步、文件均低于 GitHub 单文件限制 | 必须先审计许可证和秘密；不要与知识索引混在一起 |
| 审阅后的 ZIP | 偶尔迁移、用 U 盘或自己的云盘 | GitHub 不适合频繁提交二进制 ZIP；传输后核对哈希 |
| 目标电脑重新安装插件 + 只迁用户技能 | 最稳妥的常规方案 | 插件版本可能变化，但减少缓存快照与许可证风险 |

仓库私有不等于可以忽略第三方许可证。插件缓存内的内容应先确认是否允许再分发，即使只在自己的私有仓库中使用。

## 故障处理

| 现象 | 处理 |
| --- | --- |
| 导出目录已存在 | 换新的日期化目录，不删除或覆盖旧结果 |
| 技能数量少于清单 | 先确认根路径，再重新生成 `sources/inventory/skills.json` |
| 安装显示大量冲突 | 保留目标现有文件，逐项比较版本，不批量覆盖 |
| 技能出现但执行失败 | 检查其依赖、MCP、环境变量和外部工具，不先重装所有技能 |
| 插件技能未出现 | 优先在目标 Codex 正常安装插件；确认后才使用缓存恢复开关 |
| 校验发现疑似秘密 | 停止传输和 Git 操作，删除该导出目录，检查源文件并轮换已暴露凭据 |

## 记录模板

```text
日期：YYYY-MM-DD HH:mm +08:00
源 Codex 版本：<VERSION>
用户技能：<COUNT / BYTES>
插件缓存：<COUNT / BYTES>
导出状态：DRY_RUN | EXPORTED | BLOCKED
清单路径：<MANIFEST_PATH>
完整性抽查：PASS | FAIL
安装状态：DRY_RUN | INSTALLED | NOT_RUN
冲突跳过：<COUNT>
目标端验证：PASS | WATCH | FAIL
未导出：凭据 / 缓存 / 日志 / 数据库 / 链接
```

## 相关文档

- [技能与路由](skills-and-routing.md)
- [工作区迁移指南](workspace-portability-guide.md)
- [Git 跨设备同步指南](../ai-workflows/git-cross-device-guide.md)
