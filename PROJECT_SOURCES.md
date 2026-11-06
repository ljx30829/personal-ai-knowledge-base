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
