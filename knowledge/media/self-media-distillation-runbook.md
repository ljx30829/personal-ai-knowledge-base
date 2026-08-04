---
updated: 2026-08-04
status: VERIFIED_LOCAL_CLI
confidence: HIGH
sources:
  - C:\Users\26014\Documents\自媒体运营\README.md
  - C:\Users\26014\Documents\自媒体运营\TASK_STATE.md
  - C:\Users\26014\Documents\自媒体运营\src\account_knowledge_distiller
next_review: 2026-08-18
---

# 自媒体账号采集、转写与知识蒸馏运行手册

目标是把公开或获授权内容转成可检索、可追溯的方法知识，不是搬运视频。账号列表、标题或页面壳不能冒充“蒸馏了整个账号”。

## 本地入口

```powershell
Set-Location 'C:\Users\26014\Documents\自媒体运营'
$env:PYTHONPATH='src'
python -m account_knowledge_distiller.cli --help
```

已有本地 Whisper：

```text
程序：D:\codex\tools\whisper.cpp\v1.9.1-blas-x64\Release\whisper-cli.exe
模型：D:\codex\.cache\whisper\ggml-small-q5_1.bin
```

不需要新 API、数据库、常驻服务或 Torch 模型。若这些路径在新电脑不存在，先估算安装体积并确认 D: 位置。

## 一、准备账号工作区

```powershell
python -m account_knowledge_distiller.cli prepare-douyin `
  --account '<ACCOUNT_ID_OR_HANDLE>' `
  --probe-status '<PUBLIC_STATUS>' `
  --probe-url '<PUBLIC_ACCOUNT_URL>' `
  --probe-note '<NON_SECRET_NOTE>'
```

只使用公开页面或用户提供的导出。遇到 JavaScript 验证壳、登录、验证码或访问限制时记录真实状态，例如 `blocked-js-shell`，不绕过。

## 二、导入证据

### 平台导出 JSON

```powershell
python -m account_knowledge_distiller.cli import-douyin-export `
  --account '<ACCOUNT>' `
  --input '<RAW_EXPORT_JSON>'
```

### 浏览器媒体捕获 JSON

```powershell
python -m account_knowledge_distiller.cli import-media-capture `
  --account '<ACCOUNT>' `
  --input '<MEDIA_CAPTURE_JSON>'
```

导入前保留来源 URL、内容 ID、作者、发布时间、采集时间和权限。原始视频/音频留在自媒体工作区，不提交到便携知识库。

## 三、本地转写

把授权音频放到账号工作区的 `audio/` 后运行：

```powershell
python -m account_knowledge_distiller.cli transcribe-whisper `
  --account '<ACCOUNT>' `
  --whisper 'D:\codex\tools\whisper.cpp\v1.9.1-blas-x64\Release\whisper-cli.exe' `
  --model 'D:\codex\.cache\whisper\ggml-small-q5_1.bin' `
  --language zh `
  --threads 4 `
  --merge
```

先用 `--limit <N>` 做小批量验证。已有转写默认不覆盖；只有确认旧转写错误并保留原证据时才用 `--force`。转写后检查时长覆盖、空文本、乱码、重复内容和专有名词。

已有人工/其他来源转写可放入 `transcripts/`，再合并：

```powershell
python -m account_knowledge_distiller.cli merge-transcripts `
  --account '<ACCOUNT>' `
  --rebuild
```

## 四、构建、审计和蒸馏

```powershell
python -m account_knowledge_distiller.cli build-account --account '<ACCOUNT>'
python -m account_knowledge_distiller.cli audit-account --account '<ACCOUNT>'
python -m account_knowledge_distiller.cli distill-account-content --account '<ACCOUNT>'
```

固定顺序是先构建、再审计覆盖、最后蒸馏。审计至少核对：

- 已知内容总数与实际导入数。
- 标题级、页面级、媒体级和完整转写级各有多少。
- 缺 URL、缺媒体、缺转写和重复内容有哪些。
- 每条结论是否能回到具体来源。

蒸馏输出应分开：内容摘要、反复主张、可复用方法、反例/冲突、作者主张、独立验证和未知项。

## 五、本地搜索问答

```powershell
python -m account_knowledge_distiller.cli ask `
  --index '<ACCOUNT_WORKSPACE>\knowledge\search_index.json' `
  --query '<KEYWORDS>' `
  --limit 10
```

搜索命中只证明本地索引含相关文本。回答仍需引用内容 ID/转写/报告，不把检索结果自动当事实。

## 六、从蒸馏到自媒体生产

1. 选择一个与用户业务一致的身份和受众，例如外贸运营、独立站执行或 AI 工作流。
2. 从蒸馏报告提取钩子、论点、证据镜头、节奏、字幕结构、场景和 CTA。
3. 换成用户自己的真实业务输入、屏幕过程、前后对比和交付证据。
4. 生成脚本、镜头清单、字幕和素材清单，保留第三方参考来源。
5. 发布前人工审核版权、事实、账号、商品卡、CTA 和平台规则。
6. 发布、评论、私信、挂卡或投放必须取得当次明确授权。
7. 发布后分开记录播放、停留、点击、询盘和成交；没有后台证据的字段保持未知。

## 质量门

```text
[ ] 内容来源公开或获授权
[ ] 每条媒体有 ID、URL、日期和证据级别
[ ] 原始媒体有哈希/基本属性记录
[ ] 转写覆盖率和缺口已审计
[ ] 作者主张与独立验证分开
[ ] 销量、利润、工具效果没有凭空确认
[ ] 方法是重新表达并用于自己的业务，不是复制作品
[ ] 发布/互动/投放仍需明确授权
```

## 故障处理

| 现象 | 处理 |
| --- | --- |
| 页面只有 JS 壳 | 标记 `blocked-js-shell`，使用用户导出或合法公开证据 |
| 账号内容数对不上 | 保留采集日期和覆盖率，不声称全账号完成 |
| Whisper 找不到程序/模型 | 核对 D: 路径；大型重装前先估算并确认 |
| 转写大量空白/乱码 | 先抽查音频格式、语言和时长，再小批重转 |
| 标题很多但无法蒸馏方法 | 证据级别不足，补媒体/字幕，不用 AI 补造正文 |
| 搜索命中但结论冲突 | 回到来源逐条对比，记录冲突和适用条件 |

## 跨设备恢复

1. 单独迁移自媒体项目代码和经审阅的账号工作区；本知识库不含原媒体。
2. 在目标电脑设置 `$env:PYTHONPATH='src'` 并运行 CLI 帮助。
3. 恢复 Whisper 程序/模型到 D: 或更新命令路径。
4. 对账号重新运行 `audit-account`，确认媒体与转写没有遗漏。
5. 运行 `build-account` 和一个 `ask` 查询作为最小验收。
6. 保持发布和账号操作未授权，直到用户指定账号、内容和动作。

## 记录模板

```text
账号：<ACCOUNT>
采集日期：YYYY-MM-DD
公开内容总数：<N|UNKNOWN>
已导入：<N>
媒体证据：<N>
完整转写：<N>
覆盖率：<VALUE|UNKNOWN>
审计报告：<PATH>
蒸馏报告：<PATH>
独立验证：<N>
阻塞：<TEXT>
发布动作：0 | <AUTHORIZED_COUNT>
结论：PASS | WATCH_PARTIAL_COVERAGE | FAIL | BLOCKED
```

## 相关文档

- [自媒体运营](self-media-operations.md)
- [内容蒸馏系统](../distillation/content-distillation-system.md)

