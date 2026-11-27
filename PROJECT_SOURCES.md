# 项目重整来源与迁移说明

2026-11-06：本页把11月1—5日已审查公开来源按项目归档。详细会话/文件定位仍只留本地。旧日期来源卡及Git历史保留，操作入口以PROJECTS_RECENT.md为准。

## 归档来源 LEARNING_SOURCES_20261101.md

---
updated: 2026-11-01
status: WATCH_RESEARCH_ONLY
confidence: MEDIUM
next_review: 2026-12-01
---

# 来源、观察面与验证边界

本方法来自一轮公开仓库研究：比较了答案/来源采集、GEO 内容与网站诊断、人工测试包、Android 商品卡采集和电商排名实验项目；检查仓库说明、实现路径、目录或样例。未安装运行这些项目，未连接店铺账号，也未做真实商品卡排名实验。

可复查的公开入口：

- [Doubao shopping and service terms](https://www.doubao.com/legal/terms)：公开条款只能说明面向用户的服务边界，不提供可复现的排序公式。
- [geo-data-engine](https://github.com/jerry3747/geo-data-engine)：答案与来源采集类项目。
- [OmniRank-GEO](https://github.com/OmniRankGEO/OmniRank-GEO)：内容、发布与监测工作流；不同模块的覆盖面须按实现分别判断。
- [doubao-android-collector](https://github.com/MYX0915/doubao-android-collector)：Android 客户端商品卡观测方向，需核对设备、版本与字段提取限制。
- [cn-geo-check](https://github.com/woodrelfay/cn-geo-check)：标准化人工测试材料方向。
- [geo-doctor](https://github.com/Fangx-AI/geo-doctor)：网站与事实一致性诊断方向。
- [E-GEO](https://github.com/psbagga17/E-GEO)：电商排名实验研究方向，不等于豆包线上工具。

上述项目链接只用于复核分类，不构成部署推荐或性能保证。若 README、样例与实现不一致，以当前代码与实际可重复运行结果为准；本轮没有取得线上实测证据。后续复查前需重新核对仓库默认分支、活跃状态、代码和平台行为。


## 归档来源 LEARNING_SOURCES_20261102.md

---
updated: 2026-11-02
status: WATCH_EVIDENCE_BOUNDARIES
confidence: MEDIUM
next_review: 2026-12-02
---

# AI 商品推荐诊断的来源与边界

本方法来自一轮私有项目操作复盘：区分面向工作的助手与普通问答入口；以固定问题记录回答、来源和商品卡差异；核对商品详情、店铺属性与后台运营统计范围；追踪资料稿、平台提交、审核与公开发布状态。具体账号、SKU、后台数字、问答原文和操作凭据保留在受控项目工作区，不复制到公开知识库。

复核入口：

- [豆包官方产品说明](https://www.doubao.com/work/docs/zh-cn/articles/562542181047-which-product)：用于理解普通豆包与豆包工作定位差异；不提供商品卡排序机制。
- [抖店官方学习中心](https://school.jinritemai.com/)：后台渠道指标与商品信息应以当前账号中显示的统计口径和时间范围为准；全店数据不可当作单品表现。
- [Google 搜索中心：创建有帮助、可靠、以用户为先的内容](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)：说明公开网页内容需要服务真实用户；不证明其会被特定 AI 引用或带来推荐。

以上来源不揭示豆包或其他平台的内部商品排序规则。单一设备或账号下的样本只代表该条件下的观察；要评价变化需保留相同测试集并重复采样。公开内容是否被抓取、引用或转成订单，应分别使用对应平台可核验证据。


## 归档来源 LEARNING_SOURCES_20261103.md

---
updated: 2026-11-03
status: WATCH_SINGLE_ACCOUNT_FLOW_VERIFIED
confidence: MEDIUM
next_review: 2026-12-03
---

# 比特浏览器多账号发布方法的来源与边界

本方法来自一次经授权的短视频发布链路测试及多个隔离浏览器环境的启动观察。记录了应用/API/环境/页面/登录/上传/草稿保存/提交/审核可见状态之间的层级差异，并在恢复草稿和作品管理页复核话题及文案。单次短片提交处于审核中且仅自己可见；不代表公开发布或导流结果。

复核入口：

- [BitBrowser Local API 文档](https://doc2.bitbrowser.cn/jiekou.html)：环境管理接口参考，不证明本地具体版本或账号状态。
- [TikTok 视频可见性帮助](https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/video-visibility)：可见范围说明，不证明内容审核通过或外部访问成功。

测试时间、账号、原始视频、可回访作品 URL、代理信息、浏览器/CDP 端点及详细窗口记录保留在受控本地工作区，不放入公开知识库。多账号并发、长期稳定、日处理上限和业务归因仍需在合法授权条件下用小批次另行验证。


## 归档来源 LEARNING_SOURCES_20261104.md

---
updated: 2026-11-04
status: WATCH_DOCUMENTED_METHODS
confidence: MEDIUM
next_review: 2026-12-04
---

# 来源、去重与验证边界

本次复盘核对可访问的本机普通/压缩历史、用户最终修正、工具结果和已有产物；其他设备、删除和未同步历史不可读。原始来源定位、本人素材、客户、账号、后台经营资料、路径和凭据均只保留在受控本地台账。

已与默认分支及开放学习 PR 的手册/来源去重：基础 SEO、缓存分层、完整包交付、发送状态、浏览器启动和发布核验已覆盖。本轮补模型身份/回退日志与整条计费、公开销量原始口径/国家覆盖、现网后补变更保留和性能回归。低价文档、available 或免费代码不证明服务效果、实际账单或硬件速度，未执行样片生成。

## 复查入口

- [InfiniteTalk 官方仓库](https://github.com/MeiGen-AI/InfiniteTalk)：模型实现与许可的核查起点，不证明第三方托管实例正在运行相同模型。
- [MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano)：语音实现和硬件说明应以当前版本为准；CPU 支持不等于无资源需求。
- [Cloudflare Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)：核当前网页和 CLI 的部署能力/限额，不把历史限额当永久规则。
- [web.dev CLS](https://web.dev/articles/cls)：布局位移诊断；单次合成结果不等于真实用户分布。
- [Google 官方更新：移除 FAQ 富结果文档](https://developers.google.com/search/updates#removing-faq-rich-result)：本轮实时复查原 FAQ 文档跳转后读取到 2026-06-15 条目，说明 FAQ 富结果已不再展示；修正旧稿仅限制商业站的过时表述。
- [Amazon 巴西雨伞类目榜](https://www.amazon.com.br/gp/bestsellers/fashion/17682045011)：仅作公开口径案例入口；榜单/价格随时间变动，不能作为常量或后台净成交证据。

公开稿不刊客户清单、业务发送数量、私人路径、测试码、内部入口、资产标识、原始会话或受限素材。本轮只整理仓库；没有安装、充值、生成、客户/社交发送、网站广告修改或事件发送。

[方法增补](PROJECTS_RECENT.md)。既有开放 PR 的导航和状态增补在合并时须保留；默认分支仍未合并，不能写默认内容已更新。


## 2026-11-06：数字人口播实测与 Amazon 榜单采样

本日复盘只把工具调用、真实任务输出和用户确认作为执行证据。数字人存在一次短音频生成和一次失败视频样片；失败分析指向遮罩合成输入，后续另存人物直连配置但未再运行。不要公开账号扣点明细、人物素材或云端工作流标识。

- [RunningHub](https://www.runninghub.cn/)：平台入口，本文提到的节点编辑/配音与视频运行以平台当时界面和账单记录为准；不是某个模型或 Skill 的来源证明。
- [LTX Director 项目](https://github.com/WhatDreamsCost/WhatDreamsCost-ComfyUI)：节点/时间线参考实现，不证明托管服务运行状态、版本或成片质量。
- [Easy IndexTTS2](https://github.com/yolain/ComfyUI-Easy-IndexTTS2)：声音生成节点项目来源；单次成功配音不代表本人相似度、授权或长文本质量验收。
- [Amazon Rain Umbrellas Best Sellers](https://www.amazon.com/Best-Sellers-Rain-Umbrellas/zgbs/fashion/15744111)：美国站当日类目榜单来源。排名、页面价格及购买区间是时间快照，未显示不是零销量，也不是后台净成交。
- [Bright Data Web Scraper API](https://brightdata.com/products/web-scraper)：本日实际调用的网页抓取服务公开入口。具体 MCP 帐户套餐、计费和其他站点覆盖要另查，单次抓取不证明普遍可用或免费。

Skill/工具边界：`qinghu-amazon-product-research` 的本地 Skill 文件实际读取用于筛选研究路线，但本次执行使用的是 `brightdata_amazon` MCP，而不是 Qinghu 选品 API；专用 Skill 是否有可公开源码链接待核。RunningHub 浏览器编辑器和国内版工作流助手用于改图及读回；IndexTTS-2 与 LTX-2.3 是模型/节点层，不把它们写成 Codex Skill。Seedance 分支未运行，最终删除保存状态待复核。

详细页面快照、商品明细、扣点与会话定位留在受控本地记录。公开知识只保留可重复的榜单口径、工作流诊断顺序和公开来源，不转存受限素材或个人样片。


## 2026-11-07 增补来源与状态

证据来自本机可访问普通/压缩历史、工具返回、用户否定与实际本地报告；不以会话标题、助手总结或计划单独证明执行。数字人补录来自前日晚后续工具记录；浏览器后台只读、飞书界面写入、Semrush查询/草稿/跟踪分别有页面快照。历史工具声称但当前镜像缺失的1688接口模块标为可复现性待核。

公开核查入口：[Ego Lite](https://lite.ego.app/)、[Semrush](https://www.semrush.com/)、[Search Console](https://search.google.com/search-console/)、[飞书开放平台](https://open.feishu.cn/)、[飞书官方CLI](https://github.com/larksuite/cli)、[考古加](https://ad.kaogujia.com/)、[1688](https://www.1688.com/)、[青虎](https://www.iqinghu.com/)。入口可读只证明网站存在，不证明已授权、效果或计费。

技能实读与底层执行详见各原项目主文档；未找到已确认的公开 Skill 源码不猜链接。飞书排版、OpenCLI等仅调研候选不算安装/运行。账户、经营数据、商品/素材标识、私人地址、私有代理入口及原始会话定位只留本地。知识合并回复用原主入口，未另建日期版教程。


## 2026-11-10 来源与覆盖状态

本次依据可读本地会话、压缩历史及实际产物，覆盖上次检查点后至本轮扫描时；精确来源定位、会话标识、账号/作品链接、平台对象和经营数据仅留本地。其他设备、删除或未同步内容不可读。原始操作来自各授权工作会话，本次仅整理。

SEO依据部署包/版本、HTTP/结构化检查、GSC与Semrush页面、目录匿名复核和部分Google搜索截图；视频依据源片探测、解码、清单、BitBrowser返回连接的后台记录和版权/私密状态；外贸依据研究审核文件、SMTP结果、五文件夹与聊天状态；Windows依据迁移工具返回、联接核查、空间快照和Release/服务检查；数字人替代方案只有公开文档读取。

公开学习入口：[Ego Lite](https://lite.ego.app/)、[BitBrowser API](https://doc2.bitbrowser.cn/jiekou.html)、[Playwright](https://playwright.dev/)、[FFmpeg](https://ffmpeg.org/)、[Search Console](https://search.google.com/search-console/)、[Cloudflare重定向](https://developers.cloudflare.com/rules/url-forwarding/)、[YouTube版权声明说明](https://support.google.com/youtube/answer/6013276)、[Comfy价格](https://comfy.org/pricing)、[RunComfy价格](https://www.runcomfy.com/pricing)。公开链接说明能力/计费，不证明本账号权限或效果；Skill独立源码待核时照实标记。

实际读取与底层执行已分别写入各主文档；技能名不能证明模型运行。AI搜索与市场项目本窗口没有独立的新方法证据，保留原文，不制造新日期教程。公开库当前仍Public；开放PR1—10存在且默认分支未吸收稳定主文档，最新本地准备与PR9/10的项目文件有重叠，后续审阅须保留全部历史导航与修正。


## 2026-11-11 来源与验证边界

可读本机普通/压缩历史与现存执行产物对照：SEO的分版本部署/生产回读/布局差异/审计报告；视频的缺失盘点、原片清单、重建报告、平台定时和合集回读；发布器源码与连接失败测试；WhatsApp逐条结果与页面快照；邮件零发送检查点；官方Release安装及Docker版本工具输出。详细会话定位、私有入口、账号作品、客户信息和原始素材只留本地。

发现聊天成功总数与批次JSON冲突，保留冲突而不把自述当完成证据。未使用其他设备、已删除或未同步历史推断动作。模型配置、工具声明和README仅按对应验证层记录。

公开学习：[OpenMausBot](https://github.com/milind-soni/OpenMausBot)、[Docker](https://docs.docker.com/engine/)、[Sitemaps](https://www.sitemaps.org/protocol.html)、[Schema.org](https://schema.org/Organization)、[TikTok合集](https://www.tiktok.com/creator-academy/article/tool-playlists-intro?lang=en)、[YouTube播放列表](https://support.google.com/youtube/answer/57792)。技能编排/执行器/模型分列；缺专用Skill新读取证据不推测。

公开默认分支与10个开放PR已检查，既有项目增补仍有重叠待合并。本轮本地浏览器在Work设置禁用，私有日报远端不可读；本地整理不称远端同步，本轮无业务操作。


## 2026-11-12 来源与状态

来源包括原工具输出、运行/验证JSON、代码差异、文件哈希、官方README与API文档。详细来源定位、账号/资产ID、私有链接、截图和原业务数据只留本地。新增StaffDeck、Agent Desktop与项目中枢稳定指南；既有SEO、视频、外贸、数字人回写原入口。Hunter/Apollo及研究索引设计为候选，HubSpot只读接入有执行证据；源码研究不等于安装。历史索引与业务看板数量只代表其核对时点。

本轮没有新的远端PR或同步；旧PR与本地积压需要合并审查。公开内容只保留通用步骤，不包含客户、邮件、业务排期明细或受限媒体。


## 2026-11-13 来源与公开边界

依据本机普通/压缩历史、用户逐次修正、原工具返回及实际部署/采集/聊天/邮件/游戏产物；逐条来源与详细定位仅留本地。可访问Codex近期和归档清单及新增线程已读，ChatGPT会话接口对当前登录账户不可用；其他设备、删除、未同步及压缩前已丢失的内容仍有缺口。不能把标题、助手总结或浏览器标签当执行证据。

稳定入口已增补SEO、外贸、视觉、口播、Windows及视频，唯一新项目是[电商模拟器](PROJECT_ECOMMERCE_SIMULATOR.md)。游戏原始资源/源码、同行全文/图片、客户名单/聊天正文、后台经营数据、私人入口与凭据不上传。技能编排和工具/模型分别记，独立源码来源未核就不猜。

公开学习：[Wrangler完整上传](https://developers.cloudflare.com/pages/get-started/direct-upload/)、[URL检查](https://support.google.com/webmasters/answer/9012289)、[Ego Lite](https://lite.ego.app/)、[Node原生测试](https://nodejs.org/api/test.html)、[Playwright](https://playwright.dev/)。这些链接证明文档来源，不证明当前账户权限或业务结果。

公开默认分支与10个开放PR变更已刷新并比较；当前草稿包含前期未同步项目指南，恢复提交前须重核重叠。私有日报远端404、Git无可用认证、Codex内置浏览器不可用，未创建新PR，不称同步。


本轮新学习链接抽样6项HTTP200，原游戏站直连503保留为故障状态；不将其写可用或丢弃历史资源证据。正式站两商业页只读HTTP200并核title/H1/description/canonical，与本轮整理状态一致，未重新提交索引。


## 2026-11-16 来源和覆盖缺口

本机普通/压缩历史与Codex会话回读交叉核对；会话接口包含尚未落入本机文件的命令，因此优先记录实际返回并保存本地来源账。中断研究有官网快照，未有完整批次；当前邮箱、官网研究和视频任务仍在运行，仅纳入已完成的读取/业务复核及网络故障阶段，未来发送/发布待核。其他设备、已删除/未同步记录与当前账户不可用的ChatGPT历史明确列缺口。

只把通用恢复步骤回写原外贸/视频指南；没有公开客户清单、邮箱正文、账号/素材ID、私有路径或原始会话。公开默认分支与10个开放PR差异已读取；私有日报API404，Git无可用非交互认证；Codex浏览器初始化明确返回Work设置禁用本地浏览器，不等同GitHub会话过期。没有新PR/远端同步；已有本地积压保留。


## 2026-11-16 用户开启权限后的恢复

用户开启权限后，已通过新的统一Computer Use浏览器通道成功打开既有已登录GitHub的内置浏览器，私有日报和公开知识库均可读取。此前Work禁用是已恢复的历史阻塞；API无认证404不能替代已登录浏览器的真实访问状态。已核日报11个开放PR、知识库10个开放PR，默认分支未合并积压；本次准备在新日期分支提交，PR最终状态以对应回读为准。未导出凭据、未改默认分支或自动合并。


## 2026-11-16 下午：来源和覆盖

核本机普通/压缩历史、Codex可读会话原工具/命令返回、原部署/发送/媒体检查JSON与用户最后修正；详细定位只留本地。脚本研究的ASR未全部校订，3/10深拆不能写全账号已看；知识手册不是原视频效果验证。原受限视频、图片、剧本全文、私人路径、客户/经营数据、资产ID与后台入口不入公开仓库。

短剧Skill公开来源与准确名称见[制作主文档](PROJECT_SHORT_DRAMA.md)，四仓库安装固定版本留本地manifest；15离线测试不是生成端到端。第三方视频API只研究说明与报价，没有实测调用；原业务浏览器生成与此次文档维护分别记录。官网竞争研究见[市场项目](PROJECT_MARKET_RESEARCH.md)，只读不联系。

本轮公开默认分支已fetch、11个开放PR文件差异已读，基于既有PR11保留项目主文档积累。内置浏览器实际返回不可用，私有日报API404、Git读写缺可用认证；私有远端README/当前日报/开放PR不能重新读取，不称完整远端去重或同步。旧PR链接为上次成功记录，当前私有状态未验证。其他设备、删除/未同步、当前账户不可用ChatGPT历史仍是缺口。


本轮新增学习链接只读抽测未全部成功：https://api.seedance.nz/en/models/seedance-2.0 — <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1010)>；https://www.rodongroup.com/ — HTTP Error 403: Forbidden。这些是当前可访问性限制，不据此否认历史读取；能力与费用仍需原平台核对。


## 2026-11-17 来源、工具与覆盖

核本机192份普通/压缩历史（122份压缩，0解析错误）、当前可访问Codex活动及归档清单、相关原会话命令结果和实际关键词/媒体/邮件文件。原始材料、详细会话定位、客户/账号、受限正文、二维码/凭据与私人路径仅留本地。ChatGPT历史对当前账号不可用，其他设备/删除/未同步记录及未校订OCR仍是缺口。新项目来源是公开Muse Link和MuseCanvas仓库，前者源码审查未部署，后者README研究未运行；不是独立安全认证或生成实测。

公开知识默认分支和11个开放PR文件差异已刷新；新日期分支保留PR11及上轮本地积压，内容仍需合并时保全旧导航。内置浏览器本轮返回不可用，私有日报API404，非交互Git读/写预检无可用认证；未完成私有远端最新去重，不称新PR或同步。最后成功远端覆盖不推进，恢复授权通道后重新核两库默认分支与开放PR再提交。


## 2026-11-18 来源、覆盖与验证边界

本机普通/压缩历史、可访问Codex活动/归档清单及原会话工具结果，结合原发布回读、复制哈希、导演manifest/测试/Preflight、白模实际渲染、3D工程和GLB检查。只公开通用方法；原视频/剧本全文、素材、私有路径、详细会话定位、后台账号/资产ID/推广链接、客户/邮件/经营数据及凭据只留本地。当前运行中的3D工作只记录已观察阶段，不接管或启动其工具。

公开来源与准确Skill名称见[短剧入口](PROJECT_SHORT_DRAMA.md)，原生资产与导出方法见[商品3D指南](PROJECT_PRODUCT_3D.md)。候选古装带货技能不是已确认的热门作者原版；上游安装、说明与真实后端分别验收。原参考片全解码不证明语义全看、许可或商品效果，白模剖视不证明真实材质。

公开默认分支与11个开放PR文件差异重新读取，保留原PR11和前轮全部未同步文件。内置浏览器实际返回不可用，私有日报API404、Git读写预检无可用认证；无法完整重读私有最新README/日报/开放PR，本地README与既有日报只是历史基线。没有新PR、推送或合并，远端覆盖不推进；其他设备、删除/未同步及当前不可访问ChatGPT历史仍为缺口。

新增学习来源9项只读检查：8项HTTP200，Blender首页HTTP403；官方glTF文档可读，首页限制不否认历史访问或软件可用。3D后续快照只读GLB结构，单动画59通道不是最终目标软件播放验收。


## 2026-11-19 来源与缺口

本轮从上次本地成功覆盖时间重叠读取本机208份普通/压缩历史（146份压缩、0解析错误）、Codex活动/归档清单及8个相关会话原工具返回；旧自动化仅作定位和去重，子任务不重复计独立成果。结合3D现场报告/GLB/场景往返、角色PNG、文本包、研究validation、发送hash与平台快照核状态。详细行号/会话ID、完整剧本/提示词、客户邮件与经营统计、账号/素材/后台ID、私人路径和凭据只保留本地。

最新公开默认与11个开放PR文件差异已读取；日期分支保留PR11及前轮全部本地积压。内置浏览器明确返回不可用；私有日报API404、非交互Git私有读/公开写预检128无凭据，私有最新README/日报/PR仍不可读。旧README/日报仅作历史基线，未完成完整私有远端去重，未推送或创建新PR，不称同步。其他设备、删除/未同步和不可访问ChatGPT记录、参考片声音审查及实际API账单仍是缺口。外部来源状态在本地验证表，不能由可访问链接推论生成效果或商用许可。

本轮新增及复用学习链接15项检查14项HTTP200、Blender首页403；失败如实保留，不代表软件不可用。项目主文档仍是本地待提交稿，默认分支尚无文件时不提供假有效链接。


## 2026-11-20 来源与公开边界

依据本机普通/压缩历史、可访问Codex活动及归档清单、七个相关原会话工具输出与本地文件只读复核。新增[拍前测稿台](PROJECT_SCRIPT_REVIEW_STUDIO.md)源码职责、SQLite表分层、原表导入及页面读取有证据；逐句模型审稿、服务加载及预测误差未确认。后台数据、原表、用户素材、详细会话定位、私人地址与客户邮件仅留本地。

学习链接使用 Python HTTP/SQLite、openpyxl、Ollama、Windows事件查询和Chromium原始代码；准确 Skill/工具/模型状态见各项目“使用的技能与工具”，没有调用证据不从安装推定。Grokbot只是协作建议，没有已集成证据。原片示例值不是用户稿预测。

公开默认分支和11个开放PR差异本轮重读，保留原PR11及前轮积压。内置浏览器不可用、私有API404、Git非交互读写无认证，私有最新README/日报/开放PR仍不可读；不创建假PR、不推进远端水位。其他设备/删除/未同步记录仍是缺口。


## 2026-11-21 来源与验证范围

本轮从上次本地覆盖重叠扫描普通/压缩历史，并读取Codex活动/归档清单和相关原会话工具。项目证据包括正式无参数页面回读、部署版本文件、GSC筛选、剪辑容器/解码、统计源码/页面测试、原表/只读数据库、分页生效CIM和CLI真实错误；详细会话行号和原输出仅存本地。公开知识不含客户名单、正文、账号及后台经营统计、密钥、私有路径、素材ID或受限素材。

公开默认分支与全部开放PR文件差异已重读，保留此前积压。内置浏览器本轮明确返回Work设置禁用本地浏览器，私有日报API404、Git非交互认证失败；私有最新README、日报和开放PR未能重读，不能宣称远端完整去重/已同步。其他设备、删除和未同步历史继续为缺口。稳定入口见[近期项目](PROJECTS_RECENT.md)，后续修改直接回写，旧日期学习稿保留历史地位。


## 2026-11-23 来源与覆盖

从最近成功本地检查点重叠读取普通/压缩历史、Codex全部可读活动/归档清单及十三个原会话近期工具。原工具和独立产物用于核状态；标题、自动触发、计划和助手结语只作线索。公开默认和十一个开放PR逐文件变更已读，保留PR11及前轮本地积压。私有日报API404、非交互Git私有读/公开推送预检缺凭据；本轮内置浏览器明确返回Work设置禁用本地浏览器，未能检查GitHub登录态，不能说已退出登录。私有最新README/日报/PR和其他设备、删除/未同步、不可访问ChatGPT记录仍为缺口。

SEO证据为原部署完成输出、正式域版本/路由回读、多宽度JSON、Bing/GSC逐URL回执、目录状态CSV及同行导出；发布与索引/流量效果分开。视频证据为原FFmpeg执行/解码、版本文件、原片帧与用户否定；未通过审美确认。下载证据为源码目录/版本；商城只有公开阅读和规划，测稿打包只有文件盘点。本地台账保存详细会话行号、数据和路径，公开库不含原会话、素材、后台经营数据、客户名单、邮件正文、账号/资产标识和凭据。

新入口的公开项目与官方学习链接见[音乐工具](PROJECT_MUSIC_CLIENT_RESEARCH.md)和[数字商城](PROJECT_DIGITAL_GOODS_STORE.md)；其余学习与技能/执行工具分工合并回原项目指南。实际生成模型不明则待核，不由技能安装推定已调用。公开链接可访问不证明真实设备兼容、授权、付费或业务效果。本轮无平台经营动作、安装、邮件/社交发送、网站/广告修改或Meta事件。


## 2026-11-24 项目维护

原入口累积更新，新增Pachat和侧睡用品两个稳定指南；来源为本机可读原工具输出及产物独立校验，详细定位仅留本地。新增页面为研究/本地原型，未上线或支付。

- [PROJECT_SITE_SEO.md](PROJECT_SITE_SEO.md)
- [knowledge/trade/foreign-trade-execution-runbook.md](knowledge/trade/foreign-trade-execution-runbook.md)
- [PROJECT_ECOMMERCE_VISUAL.md](PROJECT_ECOMMERCE_VISUAL.md)
- [DIGITAL_HUMAN_QUICKSTART.md](DIGITAL_HUMAN_QUICKSTART.md)
- [PROJECT_SCRIPT_REVIEW_STUDIO.md](PROJECT_SCRIPT_REVIEW_STUDIO.md)
- [PROJECT_MULTI_ACCOUNT_VIDEO.md](PROJECT_MULTI_ACCOUNT_VIDEO.md)
- [PROJECT_WINDOWS_STORAGE_DOWNLOAD.md](PROJECT_WINDOWS_STORAGE_DOWNLOAD.md)
- [PROJECT_MARKET_RESEARCH.md](PROJECT_MARKET_RESEARCH.md)
- [PROJECT_PACHAT.md](PROJECT_PACHAT.md)
- [PROJECT_SLEEP_COMMERCE.md](PROJECT_SLEEP_COMMERCE.md)
- [PROJECT_AI_SEARCH.md](PROJECT_AI_SEARCH.md)


## 2026-11-25 项目维护

新增唯一主入口[岛仔模型用量](PROJECT_DAOZAI.md)、[OpenMontage视频框架](PROJECT_OPENMONTAGE.md)；继续回写[SEO](PROJECT_SITE_SEO.md)、[外贸手册](knowledge/trade/foreign-trade-execution-runbook.md)、[AI搜索](PROJECT_AI_SEARCH.md)、[侧睡用品](PROJECT_SLEEP_COMMERCE.md)、[市场](PROJECT_MARKET_RESEARCH.md)、[视觉](PROJECT_ECOMMERCE_VISUAL.md)、[多账号发布](PROJECT_MULTI_ACCOUNT_VIDEO.md)、[Pachat](PROJECT_PACHAT.md)和[Windows](PROJECT_WINDOWS_STORAGE_DOWNLOAD.md)。详细来源只留本地。

SEO有请求接收而非新增收录；邮件仍未发送。侧睡项目已核本地测试订单，未收款/上线；CartSignal仍有实时扫描与监控缺口。岛仔编译部署不代替界面验收，OpenMontage环境通过不代替成片渲染。每项Skill编排、执行工具与模型调用分别记录；没有新证据的项目保留历史状态。当前本地准备，未新增PR或同步；恢复GitHub后先核私有积压与开放PR。


2026-11-25 最终回读修正：OpenMontage原部署通过与当前在线分开；当前健康/首页连接被拒绝，未由日报任务重启，详见[原指南](PROJECT_OPENMONTAGE.md)。


## 2026-11-26 项目维护

新增稳定完整入口[Claude Shorts程序动画](PROJECT_CLAUDE_SHORTS_SKILLS.md)、[MuseLink Windows连接器研究](PROJECT_MUSELINK_WINDOWS.md)。后者与原微信桥不同项目，只有研究/转贴草稿，没有部署。旧日期学习稿继续作为历史，主入口不每日重建。

直接回写[岛仔](PROJECT_DAOZAI.md)、[多账号发布](PROJECT_MULTI_ACCOUNT_VIDEO.md)、[Windows存储](PROJECT_WINDOWS_STORAGE_DOWNLOAD.md)、[侧睡商城](PROJECT_SLEEP_COMMERCE.md)、[SEO](PROJECT_SITE_SEO.md)、[市场](PROJECT_MARKET_RESEARCH.md)、[外贸手册](knowledge/trade/foreign-trade-execution-runbook.md)、[Pachat](PROJECT_PACHAT.md)、[视觉](PROJECT_ECOMMERCE_VISUAL.md)和[短剧](PROJECT_SHORT_DRAMA.md)。按原工具和产物区分排期/公开、迁移/删除、静态预览/支付、相对热度/成交、技能安装/模型调用；来源细定位仅保留本地。

30秒程序样片已导出，45秒新集仍在渲染；最终美术和像素门禁待核。GitHub内置浏览器不可用、Git缺可用认证，私有日报远端不可读，不能声称远端去重或同步完成。三平台店铺和广告、数字人口播、AI搜索及其余项目未见本窗独立新完成证据，保留原状态；OpenMontage未做新的重启或完整渲染验证。


## 2026-11-27：恢复GitHub提交访问

用户本人重新登录后，Codex内置浏览器已实读私有日报仓库和公开知识库，确认日报默认main/12个旧开放PR、知识库默认master/11个旧开放PR。此前访问阻塞是历史状态，不能继续称当前浏览器不可用。本次仅恢复截至11月26日已审阅积压；没有据今天登录时间推进业务覆盖、推定新发布/收录/发送或业务效果。

从最新默认分支建立新的日期分支，保留旧PR导航/来源/状态及所有原项目指南，交由新PR审核。旧PR全部保持未合并，默认分支不直推。项目历史段落中的当日失败保留；当前远端提交状态以本地检查点与新PR实际回读为准。浏览器登录不会自动赋予Git命令行凭据，不导出浏览器认证。
