# OpenMontage：视频生产框架本机部署与验收

更新：2026-11-25。目标是让编码助手按受控流程完成拆片、脚本、分镜、素材和后期。公开项目[OpenMontage](https://github.com/OpenMontageInc/OpenMontage)、[官网](https://openmontage.video)、[Agent Guide](https://github.com/OpenMontageInc/OpenMontage/blob/main/AGENT_GUIDE.md)、[服务商说明](https://github.com/OpenMontageInc/OpenMontage/blob/main/docs/PROVIDERS.md)。本机已部署源码2e003e6，Backlot健康和首页200、Python依赖检查、Remotion版本一致及FFmpeg编码冒烟通过；完整成片渲染、云端生成和用户审片尚未验证。

补充实时状态：本轮最后只读请求Backlot健康与首页均连接被拒绝。原部署会话成功仍保留为历史，但当前看板不在线，启动原因待核；本次未重启服务。下一次使用时按原启动脚本恢复并重新检查，不能把历史200当持续在线。

## 分工、准备和权限

编码助手执行项目规范，Backlot为本地分镜看板，Python承接流程与工具，Remotion/FFmpeg负责合成，云端服务单独生成图像/视频/语音。仓库支持列表不是账号权限或实测清单；Codex入口导向AGENT_GUIDE及项目上下文。具体服务/model/host须按官方契约选择，不静默换模型。

准备可信源码版本、Python虚拟环境、符合项目引擎要求的Node/npm、FFmpeg/ffprobe、磁盘空间和本机服务权限。云端API凭据尚未配置，不公开或从别的项目擅自复用；付费生成、素材版权和发布权限分别核。源码采用AGPL-3.0，分发和商业使用边界以原LICENSE为准，不等于所有依赖/素材均无限制。

## 顺序、输入和产出

1. 核公开仓库与锁定提交，阅读CODEX/AGENT_GUIDE及依赖要求，先保留恢复点。
2. 依说明建隔离Python环境并安装项目依赖，运行`python -m pip check`；Node与npm要分别可调用，避免只查node版本。
3. 安装渲染子项目锁定依赖，在该子项目目录核Remotion包版本一致。根目录报找不到Remotion不能直接判安装失败，先核工作目录。
4. 确认FFmpeg与ffprobe可用，用短H.264样片及回读验证编码，不把这个当完整Remotion工程渲染通过。
5. 使用本机启动脚本设置环境后运行`python -m backlot open`，读健康和首页。原会话一次端口解析命令错误后已修正并确认服务，旧失败保留为过程证据。
6. 输入用户已确认素材、比例、声音、时长和预算；固定时间线/分镜后先小样，再完整渲染与全片解码、抽帧和音频核验。无字幕/无装饰字要求须写入输入并逐镜检查生成片段自带文字。
7. 准备调用云端时核精确模型、hosting provider、权限与报价；异步任务留job恢复信息，超时先查同一任务，不盲目重提付费POST。

输入可以是参考视频、实拍或已确认生成片段；本次实际产出只有安装环境、启动入口、本地看板与编码冒烟文件，没有新业务成片。

## 使用的技能与工具

原执行用Git、PowerShell、Python/pip、Node/npm、Remotion CLI、FFmpeg/ffprobe和本地HTTP；已读项目CODEX和依赖文档。项目内部技能存在不等于逐项调用，专用外部Skill实际调用待核。没有云端生成模型实调证据。公开学习入口[Remotion](https://www.remotion.dev/docs/)、[FFmpeg](https://ffmpeg.org/documentation.html)及项目服务商说明；原部署路径与看板端口只留本地。

## 费用、验证与故障恢复

原环境Remotion为4.0.484一致，Python依赖无冲突，FFmpeg输出可回读；npm审计记录2项中危和9项高危，未擅自升级/修复。不能从这些检查推定完整渲染、模型生成或生产安全已通过。云端按模型、时长、分辨率、语音及重试核实际报价，未知成本记未知，不写0或全程免费。

启动失败先核工作目录、虚拟环境、Node与FFmpeg PATH，再读服务日志和健康；包版本问题在渲染子目录核锁定版本，保留审计记录而非盲目大版本升级。生成超时用同一任务继续，未拿job时先查服务商后台。恢复保留源码版本、环境说明、分镜/任务检查点与原素材；发布和商业效果仍单独验收。本轮日报维护只整理，没有再次安装、生成或部署。


2026-11-26只读复核：当前Backlot健康请求仍连接被拒绝，与上次末次状态一致；未启动服务。保留历史部署检查通过，完整渲染和云端调用仍未验证，本日无新方法增量。
