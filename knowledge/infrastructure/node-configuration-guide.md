---
updated: 2026-08-04
status: STALE_REQUIRES_RECHECK
confidence: MEDIUM
sources:
  - C:\Users\26014\.codex\memories\MEMORY.md
  - D:\v2rayN-windows-64\v2rayN.exe
next_review: 2026-08-11
---

# v2rayN 节点配置与出口验证指南

这份指南说明客户端节点、VPS 传输入口和上游住宅出口分别在哪里配置，以及如何证明实际出口。它不保存 UUID、公钥、shortId、VLESS 完整链接、订阅 URL、代理用户名或密码。

## 当前机器的已知状态

- v2rayN 安装目录：`D:\v2rayN-windows-64`
- 已检测文件版本：`7.22.7`
- 主配置：`D:\v2rayN-windows-64\guiConfigs\guiNConfig.json`
- 节点数据库：`D:\v2rayN-windows-64\guiConfigs\guiNDB.db`
- 历史本地代理地址：`127.0.0.1:10808`
- 2026-08-04 检查时没有发现 `127.0.0.1:10808` 正在监听，因此不能声称当前节点已启动或可用。

配置文件位置可以记录，里面的凭据值不能进入知识库。优先在 v2rayN 界面中操作，不直接编辑 SQLite 数据库。

## 一、先理解三层架构

```text
Windows 应用 / 浏览器 / Codex
  -> v2rayN 本地 HTTP 或 SOCKS 监听
  -> VPS 上的 VLESS + REALITY 入口
  -> 可选：VPS 上游住宅 SOCKS5 出口
  -> 目标网站
```

| 层 | 配置位置 | 决定什么 |
| --- | --- | --- |
| Windows 客户端 | v2rayN 节点记录、本地端口、路由模式 | 连接哪个 VPS 地址和端口，哪些应用走代理 |
| VPS 传输入口 | Xray/VLESS/REALITY 服务 | 认证客户端、加密/伪装传输、接收哪个端口 |
| VPS 上游出口 | Xray outbound/路由或其他转发服务 | 目标网站最终看到哪个国家、运营商和 IP 类型 |

VPS 地址是客户端入口，不一定是最终出口 IP。若多个“美国/日本节点”都连接同一个 VPS 地址但端口不同，国家切换通常由 VPS 上每个入口端口映射到不同上游出口实现。

## 二、配置 v2rayN 客户端

### 方法 A：导入现成节点或订阅

1. 从服务提供方取得 VLESS 分享链接、二维码或订阅 URL。
2. 在 v2rayN 中使用“从剪贴板导入”“扫描二维码”或“订阅分组”对应功能。
3. 导入后立即清空剪贴板，不把原始链接保存到 Markdown、截图、聊天或 Git。
4. 检查节点别名、服务器地址、端口和协议类型是否与交付说明一致。
5. 选中节点并设为活动服务器，再按后面的五层验证顺序测试。

订阅 URL 本身通常带认证信息，按密码处理。另一台电脑需要用户重新提供或从服务商账户重新取得，知识库不会自动同步它。

### 方法 B：手工新增 VLESS + REALITY 节点

v2rayN 7.x 的界面名称可能略有差异，但字段含义如下。所有值必须与 VPS 端完全一致，不能凭经验补造。

| 客户端字段 | 应填写什么 | 来源 |
| --- | --- | --- |
| 备注/别名 | 可识别的国家、线路和序号，如 `<COUNTRY>-<LINE>-01` | 自定义，不含凭据 |
| 地址 | VPS 域名或入口 IP | VPS 配置/服务商 |
| 端口 | VPS 对外监听端口 | VPS inbound |
| 用户 ID | VLESS UUID | VPS inbound，按秘密处理 |
| 加密 | VLESS 通常为 `none` | 必须与服务端一致 |
| Flow | 常见为 `xtls-rprx-vision`，也可能留空 | 必须与服务端一致 |
| 传输 | 常见为 `tcp` | 必须与服务端一致 |
| 安全 | `reality` | VPS inbound |
| SNI/Server Name | REALITY 服务端指定的域名 | VPS inbound |
| Fingerprint | 例如服务端要求的浏览器指纹 | VPS inbound |
| Public Key | REALITY 公钥 | VPS 生成，知识库不记录实际值 |
| Short ID | REALITY shortId | VPS inbound，知识库不记录实际值 |
| SpiderX | 服务端指定路径，未指定时不要擅自改变 | VPS inbound |
| Allow insecure | 通常关闭 | 只有服务端文档明确要求才改变 |

保存后不要只看节点名称或延迟数字。字段能保存不代表握手成功，握手成功也不代表走了预期住宅出口。

### 本地监听与系统代理

1. 在 v2rayN 的本地监听设置中确认 HTTP/SOCKS/Mixed 端口。历史值是 `10808`，但应以当前界面为准。
2. 需要普通 Windows 应用走代理时，选择“设置系统代理”；选择“清除系统代理”会让依赖系统代理的应用直连。
3. 只想让特定命令走代理时，不必改全局系统代理，可在该命令显式指定 `--proxy`。
4. 路由模式决定哪些域名直连、代理或阻断。先用全局代理证明链路，再切换到规则模式；否则规则错误和节点错误会混在一起。
5. 改完后确认系统托盘中的活动节点和代理模式，不要只看主窗口选中行。

## 三、配置 VPS 与住宅出口

### VPS 入口必须与客户端一一对应

每个 VLESS + REALITY inbound 至少要明确：监听地址、外部端口、UUID、Flow、REALITY serverName、public/private key 对、shortId 和路由标签。防火墙/安全组还必须开放对应 TCP/UDP 端口。

客户端字段与 VPS inbound 有一个字符不一致，都可能导致握手失败。知识库只记录“字段从哪里取得”，实际值保留在服务器秘密配置或服务商控制台。

### 住宅 SOCKS5 是 VPS 的上游出口

若目标是住宅样式出口，VPS 端通常还需要：

1. 配置一个 SOCKS outbound，填上游住宅代理的主机、端口、用户名和密码。
2. 给 VLESS inbound 设置稳定的 tag。
3. 配置路由规则，把该 inbound tag 的流量送到对应 SOCKS outbound tag。
4. 为美国、日本等不同出口使用不同 inbound 端口或明确的路由规则。
5. 重启/重载 Xray 后，从客户端做出口 IP 验证。

更换住宅国家或供应商时，通常改的是 VPS 的 outbound 或端口到 outbound 的映射，不是把 v2rayN 的“地址”字段直接换成住宅 IP。若不确定“换节点”指客户端入口还是上游出口，必须先画出当前映射再修改。

### VPS 侧只读检查

在已获授权的服务器终端中，可按实际服务名执行：

```bash
systemctl status xray --no-pager
ss -lntp
journalctl -u xray --since "30 minutes ago" --no-pager
```

这些命令只检查服务、监听和日志。不要把包含 UUID、代理账号、完整配置或客户端 IP 的输出提交到知识库。

## 四、切换节点的正确步骤

1. 记录当前非秘密基线：活动节点别名、预期国家、当前时间。
2. 在 v2rayN 中选择目标节点并设为活动服务器。
3. 确认系统代理/路由模式与测试目的匹配。
4. 如果改了 `guiNConfig.json`，先完全退出 v2rayN，再备份、修改、启动；v2rayN 退出时可能回写配置。
5. 启动后重新检查活动节点。`IndexId` 是选中记录的内部标识，但它变化只证明“选中了另一条记录”。
6. 依次完成本地监听、VPS 端口、代理请求、出口 IP 和目标网站验证。
7. 只有实际出口国家/IP 类型符合预期，才记录切换为 `PASS`。

不要直接修改 `guiNDB.db` 来切换节点。数据库含节点记录和状态，误操作会损坏配置，也容易泄露秘密。

## 五、五层验证顺序

以下命令中的主机、端口和结果不要原样写回知识库。

### 1. 本地监听

```powershell
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
  Where-Object LocalPort -eq <LOCAL_PROXY_PORT> |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

没有输出：v2rayN 未启动、核心未启动、端口不同或端口被占用。

### 2. VPS 入口端口

```powershell
Test-NetConnection <VPS_HOST> -Port <VPS_PORT>
```

`TcpTestSucceeded : True` 只证明能到入口端口，不证明 VLESS/REALITY 认证成功，也不证明出口正确。

### 3. 代理请求

先测试历史上常用的 HTTP/Mixed 入口：

```powershell
curl.exe --proxy http://127.0.0.1:<LOCAL_PROXY_PORT> https://api.ipify.org
```

若当前端口是纯 SOCKS，再测试远程 DNS 解析：

```powershell
curl.exe --proxy socks5h://127.0.0.1:<LOCAL_PROXY_PORT> https://api.ipify.org
```

HTTP 和 SOCKS 模式不要混用。`socks5h` 的 `h` 表示域名在代理侧解析，可减少本地 DNS 污染干扰。

### 4. 实际出口

将代理结果与直连结果对比：

```powershell
curl.exe https://api.ipify.org
curl.exe --proxy http://127.0.0.1:<LOCAL_PROXY_PORT> https://ipinfo.io/json
```

只在本地看结果，记录“国家/线路是否匹配”和时间即可。VPS 入口可达但仍显示旧国家，说明选中记录、VPS 路由或上游出口映射仍未切换。

### 5. 目标网站

```powershell
curl.exe -I --proxy http://127.0.0.1:<LOCAL_PROXY_PORT> https://<TARGET_HOST>/
```

出口 IP 正确但目标网站失败时，检查目标站限制、DNS、TLS、区域限制、住宅账号状态或网站风控，不要立即重装 v2rayN。

## 六、延迟与测速

- `-1` 延迟不等于节点必然死亡。历史上 `SpeedPingTestUrl` 指向的测速目标出现 TLS/超时，而真实代理请求仍可能成功。
- 先检查 `SpeedPingTestUrl`，再用 `https://api.ipify.org` 等独立目标验证出口。
- 延迟、下载速度、出口国家和目标站可用性是四个不同指标。
- 跨国链路可能形成“本地 -> 美国 VPS -> 日本住宅出口”的绕路，IP 外观正确但速度很慢。

## 七、常见故障矩阵

| 现象 | 最可能的层 | 先做什么 |
| --- | --- | --- |
| 本地端口不监听 | v2rayN/核心/端口冲突 | 看核心日志、当前监听设置和占用进程 |
| VPS 端口不通 | VPS 服务、防火墙、安全组、地址/端口 | 检查 Xray 状态和监听，再检查安全组 |
| 端口通但代理请求失败 | VLESS/REALITY 字段不匹配 | 对照 UUID、Flow、SNI、key、shortId、传输 |
| `User was rejected by the SOCKS5 server` | VPS 上游住宅代理认证/账号状态 | 检查上游用户名、密码、白名单、套餐和账号状态 |
| v2rayN 显示 `-1` | 测速 URL 或 TLS/超时 | 换独立出口检查，不先判节点死亡 |
| 切到日本节点仍显示美国出口 | `IndexId` 回写、选错记录、VPS 映射仍指旧出口 | 重启后复查活动节点和 VPS outbound 映射 |
| 浏览器可用但 Codex 不可用 | 系统代理、应用代理、DNS 或长连接 | 检查系统代理、HTTP/SOCKS 路径和代理侧 DNS |
| 出口正确但很慢 | 跨国绕路或住宅上游性能 | 分别测直连、VPS 传输和住宅出口，避免混为一层 |

## 八、跨设备恢复

知识库只让另一台电脑知道“怎么配”，不会携带节点凭据。恢复步骤：

1. 安装同系列 v2rayN 到 D: 或其他非系统盘；大型下载前按安装规则确认。
2. 用户从服务商或服务器秘密存储重新取得订阅/节点参数。
3. 导入后确认本地监听端口和系统代理模式。
4. 按五层顺序验证，不复制旧电脑的 `guiNDB.db` 到公开位置。
5. 只把节点别名、架构、结果状态、检查日期和非秘密错误签名写回知识库。

## 九、记录模板

```text
日期：YYYY-MM-DD HH:mm +08:00
客户端版本：<V2RAYN_VERSION>
活动节点别名：<ALIAS>
预期出口：<COUNTRY / TYPE>
本地监听：PASS | FAIL
VPS 端口：PASS | FAIL
代理请求：PASS | FAIL
实际出口：MATCH | MISMATCH | UNKNOWN
目标网站：PASS | FAIL | BLOCKED
错误签名：<REDACTED_ERROR>
结论：PASS | WATCH | FAIL | BLOCKED
未记录：UUID / KEY / SHORT_ID / SUBSCRIPTION / USERNAME / PASSWORD / FULL_LINK
```

## 相关文档

- [中转站与节点运维](relay-and-node-operations.md)
- [用户长期要求](../system/user-requirements.md)
- [完整知识与要求审阅稿](../../reports/full-knowledge-requirements-review-2026-08-04.md)
