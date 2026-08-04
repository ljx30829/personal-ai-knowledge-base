---
updated: 2026-08-04
status: STALE_REQUIRES_RECHECK
confidence: MEDIUM
sources:
  - C:\Users\26014\.codex\memories\MEMORY.md
  - ../../sources/inventory/workspaces.json
next_review: 2026-08-11
---

# 中转站与节点运维

具体的 v2rayN 导入/手工字段、VPS 与住宅出口分层、切换步骤、验证命令和故障矩阵见 [v2rayN 节点配置与出口验证指南](node-configuration-guide.md)。New API 的启动器、Docker/origin/Cloudflare/模型路由分层和跨主机恢复见 [New API 中转站配置与恢复指南](relay-configuration-guide.md)。

## 当前证据状态

- `C:\Users\26014\Documents\中转站` 和 `C:\Users\26014\Documents\节点` 当前只有隐藏配置或 Git 元数据，没有可见状态文件。
- 下述内容来自历史记录，只可作为排障路线，不能证明任何服务、节点、出口或账号当前可用。
- 公开中转域名历史上是 `https://api.gptai.asia/`；当前在线状态必须重新检查。

## 中转站分层排障

1. 检查公网域名和 Cloudflare 返回，不把 502 直接归因于模型提供商。
2. 检查隧道进程是否在运行，以及它连接的本地 origin 地址。
3. 检查 Docker Desktop/WSL2 和 New API 容器是否运行。
4. 分别检查本机端口、容器健康、隧道到 origin、域名到 Cloudflare。
5. 只有四层都通过，才能说中转站恢复；域名可打开不等于模型渠道、额度和鉴权都正常。

历史 502 的已知模式是：Cloudflare 隧道仍运行，但 Docker 和端口 3000 的 origin 已停止。相关程序位于 `D:\codex\tools\new-api`、`D:\codex\tools\new-api-deploy` 及其相邻目录。任何凭据文件只做存在性检查，禁止读取或复制值。

## v2rayN 与出口验证

- 界面选中节点或配置里的 `IndexId` 改变，不等于实际出口已经改变。
- 验证链路应分为：本地监听端口、目标服务器端口、代理请求、外网出口 IP、目标站可访问性。
- `-1` 延迟可能来自测速 URL 失败，不能单独证明节点死亡；应换独立出口检查交叉验证。
- SOCKS5 返回 `User was rejected` 更偏向上游认证或账号状态，不应先重装 v2rayN 或改本地工具。
- 住宅出口链路要区分客户端入口、VPS 传输层和上游住宅代理。更换“出口 IP”通常发生在 VPS 上游，不是改客户端连接地址。
- v2rayN 可能在退出时回写配置；修改前先关闭，修改后重启并再次验证实际出口。

## 安全规则

- 不把节点订阅、用户名、密码、私钥、Cookie、令牌或完整客户端数据库写入知识库。
- 不在命令输出中打印代理 URL 内的认证部分。
- 记录非秘密架构、文件位置、错误签名、验证命令类型和最后验证日期。
- 若需要电脑关机后仍提供服务，必须迁移到持续在线的远程主机；本机方案无法满足这一点。

## 未知项

- 当前 New API、Cloudflare、Docker、v2rayN、VPS 和上游住宅代理均未在 2026-08-04 实时验证。
- 当前选中节点、实际出口 IP、端口、订阅和账户有效性未知。

## 来源与证据

- `C:\Users\26014\.codex\memories\MEMORY.md` 中的 New API 恢复与 v2rayN 历史条目。
- [工作区机器清单](../../sources/inventory/workspaces.json)
- [v2rayN 节点配置与出口验证指南](node-configuration-guide.md)
