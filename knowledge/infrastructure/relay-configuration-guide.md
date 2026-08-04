---
updated: 2026-08-04
status: VERIFIED_CONFIGURATION_STALE_RUNTIME
confidence: HIGH
sources:
  - D:\codex\tools\new-api-deploy\start-new-api-stack.ps1
  - relay-and-node-operations.md
next_review: 2026-08-11
---

# New API 中转站配置与恢复指南

本页记录当前 New API 中转栈的非秘密架构、启动入口、验证顺序和跨设备恢复方式。2026-08-04 只确认了文件路径，不代表容器、渠道、额度、鉴权或公网接口当前健康。

## 当前架构

```text
客户端
  -> https://api.gptai.asia/v1
  -> Cloudflare Tunnel
  -> http://127.0.0.1:3000
  -> New API 容器
  -> 已配置的上游模型渠道
```

| 组件 | 当前已知位置/地址 |
| --- | --- |
| 一键启动器 | `D:\codex\tools\new-api-deploy\start-new-api-stack.ps1` |
| 部署文件 | `D:\codex\tools\new-api-deploy` |
| New API 源码/工具 | `D:\codex\tools\new-api` |
| 手工充值工具 | `D:\codex\tools\new-api-manual-topup`，历史端口 `3010` |
| 持久数据 | `E:\DockerData\new-api` |
| 本地 origin | `http://127.0.0.1:3000` |
| 公网根地址 | `https://api.gptai.asia` |
| 客户端 API Base | `https://api.gptai.asia/v1` |

敏感文件包括 `.env`、渠道密钥、数据库、隧道 token/JSON、证书和支付配置实际值。本指南不读取、不复制、不提交这些内容。

## 前置条件

1. Docker Desktop 位于 `E:\Programs\Docker\Docker\Docker Desktop.exe`，Docker 数据优先保留在 E:。
2. `cloudflared` 位于 `E:\Programs\cloudflared\cloudflared.exe`。
3. 隧道配置由本机秘密存储提供；知识库只记录其存在性，不迁移内容。
4. Docker 镜像、数据库和隧道服务属于较重/持续运行组件；重新安装或拉取镜像前先估算体积并经用户确认。
5. 启动会改变本机服务状态和公网可达性，必须在用户授权的目标机器上执行。

## 一、启动当前栈

在已授权的本机 PowerShell 中：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File D:\codex\tools\new-api-deploy\start-new-api-stack.ps1
```

启动器会依次：

1. 检查 Docker daemon；必要时从 E: 启动 Docker Desktop。
2. 调用 `start-new-api.ps1` 启动 New API。
3. 等待本地 `/api/status` 返回 2xx。
4. 检查并启动 Cloudflare Tunnel。
5. 等待公网 `/api/status` 返回 2xx。

启动器显示成功只证明健康端点当时通过，不证明某个具体模型渠道、余额或用户 token 可用。

## 二、分层只读验证

### 1. Docker 与容器

```powershell
docker version --format "{{.Server.Version}}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

只记录容器名、状态和非秘密端口。不要把环境变量或容器 inspect 全量输出写入知识库。

### 2. 本地 origin

```powershell
Invoke-WebRequest http://127.0.0.1:3000/api/status `
  -UseBasicParsing -TimeoutSec 15 |
  Select-Object StatusCode
```

应返回 2xx。本地失败时先修容器/数据库，不先修 Cloudflare。

### 3. Cloudflare 隧道与公网

```powershell
Get-Process cloudflared -ErrorAction SilentlyContinue |
  Select-Object ProcessName, Id, Path
Invoke-WebRequest https://api.gptai.asia/api/status `
  -UseBasicParsing -TimeoutSec 20 |
  Select-Object StatusCode
```

本地正常而公网 502，重点检查隧道进程、ingress 到 `127.0.0.1:3000` 的映射和 Cloudflare 日志错误签名。

### 4. OpenAI 兼容路由

```powershell
Invoke-WebRequest https://api.gptai.asia/v1/models `
  -UseBasicParsing -TimeoutSec 20 |
  Select-Object StatusCode
```

若接口要求鉴权，401/403 只能证明路由到达鉴权层。不要把 Authorization Header 或 token 打印到终端、日志或知识库。

### 5. 真实渠道测试

使用用户现场提供的临时环境变量和最小请求测试一个获准模型。只记录状态码、模型名、时间、延迟、非敏感错误签名和是否计费；不记录 token 或上游密钥。

## 三、客户端接入

OpenAI 兼容客户端通常只需：

```text
Base URL: https://api.gptai.asia/v1
API Key: 由用户在目标设备现场配置，不进知识库
Model: 先从 /v1/models 或 New API 管理界面确认
```

客户端返回 401 时查下游用户 token；返回“模型不存在/无渠道”时查模型映射和渠道；返回 429 时查额度、速率限制和上游响应；公网 502 时回到隧道/origin 分层。

## 四、常见故障矩阵

| 现象 | 先查层 | 处理方向 |
| --- | --- | --- |
| Docker daemon 不可用 | Docker Desktop/WSL2 | 检查安装路径、daemon 和 E: 数据盘 |
| `127.0.0.1:3000` 拒绝连接 | 容器/origin | 检查容器、端口映射、数据库和启动日志 |
| 本地 200、公网 502 | Cloudflare Tunnel | 检查进程、ingress 和隧道日志，不改模型渠道 |
| `/api/status` 200、`/v1/models` 401 | 客户端鉴权 | 现场核对用户 token，不暴露值 |
| 模型列表正常、调用失败 | New API 渠道 | 查模型映射、渠道状态、上游额度与非秘密错误码 |
| 手工充值页不可用 | 3010 工具 | 单独检查 `new-api-manual-topup`，不要把它与 3000 混为一层 |
| 重启后数据丢失 | 持久卷 | 核对 E: 数据目录和 compose 挂载，停止反复重建容器 |

## 五、跨设备/服务器恢复

知识库不会携带数据库、用户 token、渠道密钥、支付配置或 Cloudflare 隧道凭据。恢复必须分为：

1. 迁移经审阅的部署代码和 compose 文件。
2. 备份并恢复 `E:\DockerData\new-api` 的持久数据，备份前停止写入并生成哈希。
3. 在目标主机重新配置 `.env` 和渠道/隧道秘密，不通过 Git 传输。
4. 核对域名 ingress 指向新的 origin。
5. 先验证本地 `/api/status`，再验证公网 `/api/status`，最后验证 `/v1/models` 和最小模型请求。
6. 旧主机在新主机验收前不删除数据或撤销可恢复配置。

若要求本机关机后中转站仍可用，必须把 Docker、New API 和隧道部署到持续在线的远程主机。GitHub 只能保存代码和说明，不能替代运行服务器；当前没有已验证的零费用永久在线方案。

## 安全与变更边界

- 不读取或提交 `.env`、数据库、隧道 token/JSON、`cert.pem`、支付密钥或 Authorization Header。
- 不因健康检查通过就自动启用新渠道、改额度、改价格、开支付或创建用户。
- 数据备份、容器重建、DNS/隧道切换和公网发布是有外部影响的动作，需要明确授权。
- 状态必须带日期；本页架构可复用，但当前运行状态每次都要现场复查。

## 记录模板

```text
日期：YYYY-MM-DD HH:mm +08:00
主机：<NON_SECRET_HOST_LABEL>
Docker：PASS | FAIL
New API 容器：PASS | FAIL
本地 /api/status：<STATUS>
隧道：PASS | FAIL | UNKNOWN
公网 /api/status：<STATUS>
/v1/models：PASS | AUTH_REQUIRED | FAIL
最小模型调用：PASS | WATCH | FAIL | NOT_RUN
持久数据：PRESENT | MISSING | NOT_CHECKED
结论：PASS | WATCH | FAIL | BLOCKED
未记录：ENV / TOKEN / CHANNEL_KEY / DB / TUNNEL_SECRET / CERT
```

## 相关文档

- [中转站与节点运维](relay-and-node-operations.md)
- [v2rayN 节点配置](node-configuration-guide.md)
- [工作区迁移](../system/workspace-portability-guide.md)
