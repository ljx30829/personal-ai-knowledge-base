# OpenMausBot 桌面部署与模型接入指南

更新：2026-11-11。首次建立稳定入口；已有通用节点/中转/迁移文档不覆盖该桌面应用的安装与 Docker 分层，本页不替代那些文档。

## 目标、网站与组件分工

目标是在本地桌面管理多个 AI 助手、连接模型与工具，验证能执行指定小任务。公开入口：[项目仓库](https://github.com/milind-soni/OpenMausBot)、[版本发布](https://github.com/milind-soni/OpenMausBot/releases)、[自定义引擎](https://github.com/milind-soni/OpenMausBot/blob/main/docs/custom-engines.md)、[MCP 工具](https://github.com/milind-soni/OpenMausBot/blob/main/docs/custom-mcp-servers.md)。README 能力属于项目说明，未全部在本机验证。

桌面程序负责界面与助手管理；CLI/API 引擎负责实际模型请求；MCP 负责外部工具；Docker CLI 只是客户端，Docker Engine 才运行容器。云电脑和第三方连接服务是可选依赖，不因安装应用就已开通。

## 准备条件与权限

核 Windows 架构、可用空间、官方发布版本与安装权限。模型需已有 CLI 正常登录或服务商 API 权限，兼容接口须核请求格式、模型名、计费及工具调用；不把“支持自定义 API”解读成任何地址都可用。Docker 仅在选定能力确需容器时准备 Engine。凭据在受控配置中保存，不进入教程、日志、截图或公开库。安装、登录和真实工具写入授权分别核对。

## 按顺序操作

1. 从官方 Releases 选操作系统和架构，记录版本、大小及官方校验值（若提供）；下载完整性、签名与哈希各自记录，没核签名不称已核。保留安装包与旧配置恢复点。
2. 执行用户授权的安装，检查程序文件和实际进程，再确认欢迎界面。欢迎界面仅证明启动，不证明模型、MCP或任务链可用。
3. 在应用设置中选择 CLI 登录或兼容 API；以当前官方引擎文档为准设置端点、模型及权限。保存后重新读取配置界面，给目标助手选中该引擎，不能只配置总协调入口。
4. 用不含敏感数据的小任务发送一次真实请求，记录服务商、实际模型、返回与消耗。若没有请求证据，维持“模型未验证”；不能凭助手对默认模型的判断确认当前服务。
5. 若应用提示找不到 docker，先检查 PATH 与 `docker --version`。只有 CLI 的机器仍需 `docker version` 的 Server 或 `docker info` 核 Engine；不要为消除命令提示把 CLI 当成 Docker Desktop。
6. 用户 PATH 更新后正常重启应用，使其读取新环境，再验工具入口。模型小任务通过后，才以最小权限配置 MCP 并验证一次读操作；写操作另验具体授权和写后读取。

## 输入、产出与使用的技能和工具

输入为官方安装包、系统架构、用户授权、模型服务配置与测试任务。输出为安装版本、程序启动证据、CLI路径与版本、模型请求和工具读写验收。实际历史工具为 PowerShell/HTTP 官方 Release 读取与下载、Windows UI安装启动、Docker CLI 版本命令和 PATH 回读。独立安装 Skill 的确切读取/公开源码未确认，标待核；不能从已安装技能列表推断使用。没有本次成功模型请求证据，模型服务名与质量尚待验证。

## 费用与当前验证状态

软件仓库公开开源不等于服务免费。模型订阅/API、云电脑、第三方连接、磁盘与运行资源分别计费，具体套餐和当期费用到服务商核实。已确认一次 Windows x64 v0.1.152 安装与欢迎界面，以及 Docker CLI 29.9.3 版本输出、PATH 和应用重启。Docker Engine、容器执行、模型接入、MCP和完整任务未验收。不引用未验证的默认模型名称，也不把与其他产品的助手比较当事实。

## 故障恢复与边界

软件源 TLS失败保留错误，优先查正常网络/官方源，不关闭证书验证或强装不明包。安装回退用正常卸载与受控配置备份。CLI可见而容器失败时检查 Engine、权限和上下文；模型失败分别查登录、模型名、格式和额度，不泄露凭据。应用能启动、命令能输出、模型能响应和工具能执行是四层证据。来源见[项目来源档案](PROJECT_SOURCES.md)。

学习：[Docker CLI](https://docs.docker.com/reference/cli/docker/)、[Docker Engine](https://docs.docker.com/engine/)。
