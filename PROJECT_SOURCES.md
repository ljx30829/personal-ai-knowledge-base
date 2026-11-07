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
