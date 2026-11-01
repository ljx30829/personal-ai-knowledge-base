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
