# AI短剧与漫剧：从剧本到媒体验收

更新：2026-11-16。新稳定入口。已检索既有导航与数字人/多账号指南：前者是真人口播，后者是已有素材剪辑发布，均不替代新短剧制作流程；因此在本页独立维护。目标是按可核原著或原创需求，交付可继续生产的剧本、资产、分镜、提示词和验收记录。

## 能做什么与组件分工

文字Agent与Skill管理剧本及中间文件；生图/视频/配音由实际后端执行；FFmpeg负责媒体检查或剪辑；浏览器/CLI负责提交和取回。Skill不是模型，不自带账户、积分或已验证质量。

| 公开来源 | 准确Skill名称 | 当前证据 |
| --- | --- | --- |
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | `short-drama-assets`, `short-drama-breakdown`, `short-drama-develop`, `short-drama-edit`, `short-drama-image-prompts`, `short-drama-novel-analyze`, `short-drama-produce`, `short-drama-review`, `short-drama-storyboard`, `short-drama-video-prompts`, `short-drama-write`, `short-drama` | 已安装；各阶段运行按证据另列 |
| [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) | `character-refs`, `novel-art`, `novel-characters`, `novel-outline`, `novel-script`, `novel-staging`, `novel-storyboard` | 已安装；各阶段运行按证据另列 |
| [zhanghao123vip/ai-manju-skills](https://github.com/zhanghao123vip/ai-manju-skills) | `chongsheng-manju`, `chuanyue-manju`, `dushi-manju`, `gongdou-manju`, `jiating-manju`, `minsu-manju`, `moshi-manju`, `niandai-manju`, `quanmou-manju`, `shangzhan-manju`, `tianchong-manju`, `wuxia-manju`, `xiaoyuan-manju`, `xihuan-manju`, `xingji-manju`, `xitong-manju`, `xuanhuan-manju`, `xuanyi-manju`, `yule-manju`, `zhaidou-manju`, `zhongtian-manju` | 已安装；各阶段运行按证据另列 |
| [djyy1031/ai-comic-drama-director-skills](https://github.com/djyy1031/ai-comic-drama-director-skills) | `ai-character-performance-assets`, `ai-cinematic-directing-assets`, `ai-comic-scene-assets`, `ai-shot-execution-continuity`, `ai-storyboard-asset-grounding`, `ai-storyboard-blocking-assets`, `make-ai-comic-drama` | 已安装；各阶段运行按证据另列 |

原安装共47项、47/47文件存在，15项仓库离线检查通过；21题材模板仅文件核验。已读主路由、生产、大纲与导演说明，不能推定47项全部实际参与创作。`skill-installer`实际用于原会话安装；本轮维护没有安装。平台工具另有`xyq-short-drama-skill`、`xyq-marketing-skill`、`xyq-skill`和pippit-tool-cli，三个Skill已装，尚无本次CLI生成和授权闭环。公开产品入口：[小云雀CLI](https://www.xiaoyunque.com/cli)。

## 准备条件、输入与权限

准备可用小说/原创故事、制作目标、画幅、画风、角色与商品参考和目标时长；已有信息不重复索要。媒体须有相应使用权限，公开片段不自动允许重发或复制演员形象。只有文字策划时不申请后端。实际生成前核当前登录、模型版本、参考支持、余额、报价与输出权限；收费和发布分开授权，不自动充值。

## 按顺序操作

1. 锁定故事任务和范围。先出改编/原创方案与可审核首集，不能把选题库100条默认当整批投产。
2. 选择一个主流程。drama-skills以剧本、视觉设定、分镜、图片/视频提示词和剪辑单推进；shuohao小说路线以outline.json、cast.json等结构化文件推进。两者需映射才互通，不让两套同时重写一集。
3. 建角色/服装/场景/商品资产表，区分原作依据、待核引文与二创新增；名句出处须核版本，不能因熟悉就误记剧名。
4. 逐场形成事件因果、人物动机、空间站位、说话人、动作与收尾。需要时用导演/连续性技能精修；不是所有技能机械跑一遍。
5. 先做少量代表镜头。提示词明确人物、画幅、时长、台词归属、画外声、无字幕等保留项。用户修正的服装/人物/特效必须同步至资产表，旧错图作废，不能只在新提示词末尾加否定句。
6. 在指定模型渠道核价后提交一次，保存任务状态；提交失败与生成受理分列。先查询已有任务再决定重提，避免重复扣费。
7. 下载实际输出，核容器/时长/音轨、抽帧与完整播放；检查角色一致、嘴型串话、字幕、手部/商品、动作与剧情。生成成功不等于可用。保留旧版和否定理由，再局部返修。
8. 完成分镜组装和用户验收后才考虑发布。制作不授权社交发布；多账号项目继续遵循其专用API规则。

## 实际产出与最新修正

原会话已交付100张创作选题卡及串烧方案，字段检查通过，但没有逐条看100个原片场景，不是全部核实可拍。一个20秒H3-RH Enhanced概念首版已取回并抽帧/取音轨，出现字幕与台词角色问题，被用户否定；不能当合格成片。用户要求以后本制作无字幕，并用Seedance重制。

原作风格只保留可识别人物和剧情逻辑，不要求逐帧复刻；不得擅加无依据的兜帽蛛腿怪、游戏法阵。修订为30秒Seedance 2.5/720p/16:9，实际提交因积分不足失败、未受理，故没有新版成片。纠正参考图只提交，随后用户接管，未验收；禁止自行夺回控制。旧视频与错图不替代新版。

## 使用的技能与工具

| 层级 | 实际用途及产出 | 验证/依赖 |
| --- | --- | --- |
| Skill编排 | 47项制作/小说/题材/导演技能安装及离线自检；具体媒体阶段按需读取 | 安装通过不代表已执行47项或打通后端 |
| 提交工具 | 统一Computer Use内置/扩展浏览器操作RunningHub Runow与画布；ego-browser操作指定生图空间 | 登录依赖平台；用户控制时停止；无CLI生成成功证据 |
| 模型服务 | 原首版网页标H3-RH Enhanced；修订尝试Seedance 2.5；参考图网页标image2.0 | 服务商页面模型标识不证明底层权重身份；首版被拒，修订未受理，图片未验收 |
| 检查工具 | Python/Node离线自检、FFmpeg抽帧/音轨、浏览器结果回读 | 离线15项通过不代表艺术质量或商用资格 |

## 网站、费用口径与选型

[RunningHub](https://www.runninghub.ai/)、[LibTV](https://www.liblib.tv/)、[小云雀](https://www.xiaoyunque.com/)分别核当前套餐与权限。[Seedance 2.0官方说明](https://www.volcengine.com/docs/ark/seedance-2-0?lang=zh)及[2.5说明](https://www.volcengine.com/docs/ark/seedance-2-5?lang=zh)用于能力对照，不能凭版本号断言效果更好。

本轮曾研究[APIMart](https://apimart.ai/)、[KIE](https://kie.ai/seedance-2-0)、[METASO H3](https://metaso.cn/minimax-h3/)、[ZZAI](https://api.seedance.nz/en/models/seedance-2.0)等视频渠道；仅页面报价/能力候选，未充值或API实测。图片已解决时聚焦视频；先核满足角色/画风/动作/参考输入需求，再比同模型、版本、时长、分辨率、音频、并发和实际可用率。低价可能只适用于高额充值档；按次价不等于任意时长同价。人民币折算写日期与汇率，不能把一次换算当长期价格。

实际成本按成功且可用的输出计算，失败退款不能推定包含“画面不好看”；页面免费、账户余额、实际扣款三者分开验。平台修订任务余额不足，不自动充值或换回被否定模型。尚无全片成本、稳定产出或模型对照结论。

## 故障恢复与完成门禁

安装器拒绝管理员环境：保留已校验包与日志，不擅改系统安全设置。CLI与桌面插件分开核：CLI版本可读不代表插件安装/登录。网页超时先看现有任务，不重复提交。余额不足保存提示词/报价和失败状态，等待用户决定。原参考缺失先核原片关键关系，不凭印象补怪物或特效。用户接管立即停止，待明确继续。

已完成：技能安装/离线检查、文字初稿库、首版媒体取回及问题识别。待核：所有模板实际适配、参考图验收、修订任务受理/成片、完整媒体生产链、插件授权、可用成本和平台发布。后续直接更新本页，日报只记当天动作；相关入口：[数字人口播](DIGITAL_HUMAN_QUICKSTART.md)、[已有素材跨平台发布](PROJECT_MULTI_ACCOUNT_VIDEO.md)、[Windows安装恢复](PROJECT_WINDOWS_STORAGE_DOWNLOAD.md)。


## 2026-11-17：画布候选与消息桥分离

[MuseCanvas指南](PROJECT_MUSE_CANVAS.md)为画布研究候选，只有公开README阅读，未安装/生成；[Muse Link指南](PROJECT_MUSE_LINK.md)负责微信消息桥，已读候选源码但缺合格Linux运行环境，未登录或值守。两者不是同一产品，也不因名字或账号相近就已互通。短剧原生产入口保持本页；47技能与原模型失败状态没有新增验收，原用户接管边界保持。


## 2026-11-18：导演部署、白模与模型正文

本次实质推进为导演工具本地部署、参考片技术检查、白模和分镜文本；没有新付费媒体生成。原47项技能保持原状态，新装4项不能概括成51项全部实际运行。

| 准确Skill/工作流与公开来源 | 分工与实际调用 | 依赖、输入、产出及边界 |
| --- | --- | --- |
| `seedance-storyboard-generator`：[来源](https://github.com/liangdabiao/Seedance2-Storyboard-Generator) | 安装并读取资产/分镜方法 | 输入故事；文字规划，不自带模型；许可未核明，不再分发源码 |
| `seedance-storyboard-generator-realman`：[来源](https://github.com/liangdabiao/seedance-storyboard-generator-realman) | 安装、读取真人摄影及剧情指南并用于修稿 | 输入已确认稿/参考；输出真人风格文字，不是渲染器 |
| `seedance-director`：[来源](https://github.com/gifted-professor/seedance-director) | 安装并运行Python CLI、Lint、Preflight、媒体技术扫描 | MIT；Python虚拟环境、FFmpeg/ffprobe，输入计划和本地视频，输出检查JSON；自带适配器为2.5，不能直接说已验证2.0平台 |
| `seedance-2-5-fight-director`：[来源](https://github.com/liyue-aigc/seedance-2-5-fight-director) | 安装并读取动作因果/空间规则用于审查 | 文字技能，不执行碰撞或真实生成；许可待核 |
| Seedance-Director-4.0：[来源](https://github.com/aaronbedolla560-cell/Seedance-Director-4.0) | 部署完整16阶段工作流；SCAI预演3.1示例及本地场景运行 | 不是16项独立Skill；自定义共享许可限制转售，不能当标准MIT；本地Python/浏览器预演 |
| `wangyibianju`：[来源](https://github.com/ares99668/wangyibianju) | 深入读取固定源码，候选未安装 | MIT；故事事件/商品因果/逐字稿；默认8分钟必须按本片60秒覆盖 |
| `cinematic-video-prompt-engineer`：[来源](https://github.com/CyberJ0605/cinematic-video-prompt-engineer-skill) | 深入读取固定源码，候选未安装 | MIT；可见声画正文；Python辅助脚本仅AST和人工阅读，未运行；示例视频未看 |

操作顺序补充：先恢复用户最后确认的事件和保留项，再画世界坐标、场景几何、人物/道具/门窗/光区；列接近→接触→受力→转移/松开→终态以及左右手状态；按串行/并行、对白、反应和观看时间估预算；用机位图或白模看遮挡与轴线；再写给人的导演合同和给模型的纯净TXT；随后绑定实际平台、参考图、硬意图trace和审核哈希，运行Preflight；实际生成仍需登录、额度和受理回读。

实测上游61项测试46通过、15跳过、0失败，部分跳过因公开包缺案例。一次60秒项目的4个15秒计划Lint均通过，Preflight均REVISE，含动作时间紧、缺最终正文/意图追踪/哈希审核及案例索引等问题。不能把Lint通过、三遍文字审查或精确时间标签写成可拍摄保证。对白估时未试读；复杂动作必须预演或承认预算冲突。图片提示词不是已选成品图；8K/RAW/14bit为外观目标，不是实测输出规格。

白模使用独立复制的预演引擎本地扩展曲面伞、骨架和静态双手接触，保留原引擎。三机位实际浏览器渲染与轴线检查有证据，并修正头顶裁切和标签显示；半透明剖视只用于位置检查，未验证绿色透视特效、弹道碰撞、布料或手指。白模是空间工具，不能带入真人成片画风。

用户修正：剧情“收紧”指补全因果、连续动作和具体场面，不自动缩短；商品须中途介入且持续参与交易，危机/客户着急与卖家介绍可并行推进，不写成普通救援或最后揭职业。已交文字版本保留，不把反复否定的S02或高空救援稿称批准；普通伞的承重/飞行不符合现实，提示词细化不能修复物理前提。奇幻防弹/避光属于剧情设定，不能移植成实物功效。

当前确认片的真人低饱和、高反差与真实皮肤要求优先；无字幕、无音乐和环境氛围床，仅对白与必要动作声。导演解释、策略、验收提醒与模型正文分开，后者只写可见动作、摄影、光线和声音。参考示例的角色/画风不继承。已交24镜/71节拍文本与图片提示词版本，后续纯正文另有修订；未生成新视频、未实测配音、未验收成片。平台、SKU图、材质和涂层缺证据时标待核，不编UPF或黑胶。

恢复：保留固定提交、依赖锁定、原稿/否定理由和上次输出；缺案例夹具标缺口，不伪造案例；Preflight REVISE先修具体缺口，不以重装或重复提交替代。古装带货公开视频演示不证明作者Skill源码已公开，候选与原版分开。费用仍分安装/本地计算、账号额度、生成扣费和失败退款；此次新流程无模型调用费用证据。相关[商品3D指南](PROJECT_PRODUCT_3D.md)与本页互链，商品资产验收独立于剧情审查。


## 2026-11-19：案例技能与真人资产分层

当前新增成果为技能文件/案例检索、参考片抽帧审查、单节点文字和部分角色生图；没有新完整视频生成验收。之前“本链未生图”仅属旧阶段，不能覆盖本次图像API成功。已保留原吸血鬼项目，审稿先核用户当前指定稿及实际首帧，避免误审另一个故事。

### 使用的技能与工具

| 准确名称与公开来源 | 负责步骤和实际状态 | 后端、输入、产出与验证 |
| --- | --- | --- |
| `microdrama-ad-prompts`：[saibodafu/advertisement-skills](https://github.com/saibodafu/advertisement-skills)，固定07ecd297 | 官方安装器部署、入口回读 | 短剧商业策划编排；截图SkillHub版本是否相同待核，不是视频模型 |
| `seedance-20`：[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)，固定4668457e/6.7.0 | 安装主入口与28个子技能文件 | 提示词/镜头/声音/连续性编排；不等于28项均执行，也不等于已验证各路由API |
| [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)，固定043a0a4 | 部署15个Codex技能及案例库；Node实际检索关键词 | 1059条本地案例可检索；27模板和上游494次复测覆盖481案例是固定快照，不是本机生成复测 |
| [LearnPrompt/goodcase](https://github.com/LearnPrompt/goodcase)，固定aff3330 | 补70项视频技能/创作者方法及`goodcase`通用入口；140文件对源哈希核验 | 目录并集86项有入口，不将安装数写成执行数；第三方案例许可和新场景效果另核 |
| `short-drama-review`、`short-drama-breakdown`、资产/分镜/视频提示词技能 | 原会话实读用于文本与参考片审查，具体名称见下方实际调用清单 | 同作者自检如实标注；文字审查不是独立评审或动态/听审 |
| FFmpeg/ffprobe、Python/Pillow | 原视频取帧、规格检查、裁片和逐图对比 | 一条参考片1280×720/24fps/约30秒；逐秒/重点帧观看不等于全声画验收 |
| `xyq-skill` / pippit-tool-cli | 查询本机状态：未登录，未提交生成 | 此备用链阻塞不能推出其他生图后端也不可用；官方[CLI入口](https://www.xiaoyunque.com/cli) |
| Codex CLI模型选项 / 图像API | 前者返回403未启用；后者原授权会话实际调用generations和edits | 请求模型`gpt-image-2.5-sunburst`，仅是服务返回模型标识，不独立认证供应商底层模型；3840×2160文件已核，私人端点与密钥不公开 |

### 可照做的更新流程

1. 固定原稿、首帧和实物用途。第一人称只写该视点能见的画面；转头与身体位移分别描述，画外方位若是导演设定明确标明。原始参考编号会变，提交前绑定实际文件。
2. 每段先确定人物的起因、空间、接触和终态，再给反应与台词留时间。旁白解释不能替代可见动作；互相矛盾的火花/禁特效先删冲突来源，不能只堆负向词。
3. 固定角色身份图，近脸、手部交接、商品按钮和关键遮挡另出用途图；全身图尺寸大不表示脸部能撑近景。先让静帧表达尺度/阴影关系，再测试动态。
4. 黑伞按实拍保留微收腰握柄、扁按钮、布卷、短尖；全黑是当片配色要求，不能把所有实物概括成等粗圆柱。电影人物取真人演员/试装摄影观感，禁止未经确认退回动漫立绘。
5. 分别保存纯白资产、实景首帧、视频正文。母图负责身份/结构，首帧负责机位/光影/动作接点；后镜编辑前镜并明确保留脸、手位、光向、道具和场景地标。
6. 先试一张并下载原图核像素、裁切、白底和100%细节，再做参考编辑。保持整脸可读，近白不能冒称严格#FFFFFF。场景化试装仍有窗影时，不当均匀白底合格。
7. 4K目标3840×2160与8K目标7680×4320分别核文件；相机型号、RAW、8K等提示词不证明实际规格。已交30项8K正负词和原稿备份，尚未生成30张8K，也未验收30秒新视频。

费用口径：本地阅读/安装与模型调用分开，API成功不证明免费或单张实际结算；本次实际账单待核，不写单价。准备权限包括合法参考、账号对应模型与参考编辑权限及额度。恢复时保留被否定版、请求错误与已成功原图；CLI403只阻塞该路由，不盲目重复扣费。密钥仅本地受控读取，不放仓库、示例命令或来源档案。原始角色素材、完整剧本/提示词和受限参考不随知识发布。


固定快照86项的准确安装名（全部仅按文件核验，不自动视为实际调用）：

`3d-cartoon-character-short`, `3d-cartoon-character-short-by-18gc2qf`, `action-continuity-choreography`, `action-continuity-choreography-by-15zo1bq`, `action-continuity-choreography-by-18paelt`, `action-continuity-choreography-by-1ktgmlf`, `action-continuity-choreography-by-1lcb8j2`, `action-continuity-choreography-by-1picsey`, `action-continuity-choreography-by-1wr1qau`, `action-continuity-choreography-by-cle9yv`, `action-continuity-choreography-by-d5g808`, `animation-style-consistency`, `animation-style-consistency-by-1diwzmp`, `animation-style-consistency-by-1lqimyw`, `cinematic-drama-scene`, `code-rendered-explainer-video`, `epic-fantasy-scifi-spectacle`, `epic-fantasy-scifi-spectacle-by-18paelt`, `epic-fantasy-scifi-spectacle-by-1g5goov`, `epic-fantasy-scifi-spectacle-by-1napzjr`, `epic-fantasy-scifi-spectacle-by-1picsey`, `epic-fantasy-scifi-spectacle-by-1r2e570`, `epic-fantasy-scifi-spectacle-by-1sduwzc`, `epic-fantasy-scifi-spectacle-by-6moylp`, `epic-fantasy-scifi-spectacle-by-ha1tt9`, `epic-fantasy-scifi-spectacle-by-uaxh44`, `fashion-lookbook-portrait`, `food-asmr`, `game-ui-livestream`, `goodcase`, `horror-suspense-short`, `horror-suspense-short-by-1jqwyww`, `horror-suspense-short-by-1ktgmlf`, `horror-suspense-short-by-43hd7f`, `pets-and-animals-lead`, `pets-and-animals-lead-by-18gc2qf`, `pets-and-animals-lead-by-1tmw5t`, `pov-vlog-presence`, `pov-vlog-presence-by-1d090cw`, `pov-vlog-presence-by-1en62on`, `pov-vlog-presence-by-1jqwyww`, `pov-vlog-presence-by-1sduwzc`, `pov-vlog-presence-by-1wr1qau`, `pov-vlog-presence-by-1yyrk1e`, `pov-vlog-presence-by-2zdsi5`, `pov-vlog-presence-by-e2fac1`, `pov-vlog-presence-by-ewg9kn`, `pov-vlog-presence-by-ha1tt9`, `pov-vlog-presence-by-v2wqfs`, `pov-vlog-presence-by-wat8s8`, `pov-vlog-presence-by-yai6a9`, `process-transformation-story`, `product-ad-shot-design`, `product-ad-shot-design-by-1napzjr`, `product-ad-shot-design-by-1oyim0r`, `retro-dv-home-video`, `retro-dv-home-video-by-2zdsi5`, `retro-dv-home-video-by-6moylp`, `retro-dv-home-video-by-wat8s8`, `seedance-3d-cartoon`, `seedance-car-vehicle`, `seedance-epic-fantasy-scifi`, `seedance-fashion-lookbook`, `seedance-food-asmr`, `seedance-game-ui-livestream`, `seedance-horror-suspense`, `seedance-meme-comedy`, `seedance-pet-animal`, `seedance-production-workflow`, `seedance-prompt-library`, `seedance-retro-dv-home-video`, `seedance-sports-extreme`, `seedance-storyboard-grid-to-video`, `seedance-travel-city-walk`, `sports-extreme-stunts`, `stage-dance-music-video`, `storyboard-grid-to-video`, `travel-city-walk`, `travel-city-walk-by-1oyim0r`, `travel-city-walk-by-1r2e570`, `travel-city-walk-by-1tmw5t`, `travel-city-walk-by-1uczxsi`, `travel-city-walk-by-ewg9kn`, `twist-comedy-skit`, `twist-comedy-skit-by-1en62on`, `vehicles-at-speed`.


原会话工具调用中可定位的SKILL.md读取/检查名称（包含安装核验，逐项用途以前文状态为准）：`short-drama-breakdown`, `short-drama-image-prompts`, `short-drama-review`, `short-drama-storyboard`, `xyq-skill`. 本机自定义技能的公开上游无法从此路径确定时，来源待核，不编仓库。


## 2026-11-20：局部秒点回写总时间线

适用于多轮返修的单节点视频稿：先保留用户锁定的全片区间，再逐段核对起止、转场和对白；独立片段的零秒制换成全片绝对秒点时，所有子镜、分句、脚步与遮幅同步平移。不要只改标题。以现存文件和最后一次用户修正为准，历史草稿保留。

本轮实际产出是详细分镜文本和统一时码文件，未观察新的成片生成/发布；细化提示词不计新模型调用。前段仓库/草船与“直接从挡箭开场”曾有切换，最终使用版回到仓库接草船，不能让旧描述与新稿同时当有效版本。对白压缩到短区间必须试读，时码排满不证明口型、动作和语速可实现。文本编辑使用原会话 PowerShell 文件写入/回读；具体新 Skill 调用待核实，生成模型与新费用待核实。


## 2026-11-23：对标先核原片，再按段落功能改编

原会话最初只凭分享标题推断销售喜剧和真人试用，被用户指出未实看；随后实际取得三条原片，按时间抽帧，再对两条字幕区逐秒放大。修正金银二选一为规格识别的第三个答案，补齐买贵踩坑、含量/克重/打理验证及价格揭晓。画面、烧录字幕、音轨逐句校订分别记覆盖；不得把抽帧理解成完整听看。

操作：取得授权参考→测时长和字幕覆盖→建立原片时间/画面/对白/段落作用表→新稿用自身商品动作兑现同一作用→核真实规格、价格与可拍性→用户审稿。不能只复制古装或外星人外壳；商品必须影响剧情，比较必须同人、同包、同机位、同测量口径。原稿中模糊或互相不一致的含量表述分别记录，不替作者编补。

用户再次否定两稿，最后重写仍未确认；本窗没有生成或发布雨伞改编成片。保留拒稿和最新方向，不把聊天稿当已验收拍摄方案。第三方原片只用于本地对标，许可未核不打包公开。

使用的技能与工具：实际读取 `short-drama-breakdown`、`douyin`、`qinghu-douyin-video-basic`；具体Skill可公开上游来源待核实，不编造作者归属。短链解析、下载、FFmpeg抽帧及字幕区域放大有证据；技能具备转录不代表本轮完成音轨ASR。工具/模型服务分层，未确认新的生成模型调用或API费用。输入为用户分享链接与本地媒体，产出是时间线对照和未确认新稿，验证范围限已读画面/字幕。失败恢复先补缺失段落和对白，不继续用错误推断扩稿。


## 2026-11-26：程序动画项目分流

新增[Claude Shorts技能与程序默片](PROJECT_CLAUDE_SHORTS_SKILLS.md)稳定入口，记录4技能安装、离线测试、两轮退稿后的30秒纸偶样片，以及45秒3D新集的关键帧/FX门禁与在途渲染。与本页AI生成短剧分开验收：代码渲染不等于Seedance等生成模型调用，上游案例不等于本机已做完整3D工程。
