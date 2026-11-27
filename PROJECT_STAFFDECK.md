# StaffDeck 工作台部署指南

## 目标、能力与组件
用于数字员工工作台：Python后端负责任务和模型接入，Node前端提供操作界面；与跨对话知识中枢是两套组件。[官方项目](https://github.com/OpenBMB/StaffDeck)、[中文README](https://github.com/OpenBMB/StaffDeck/blob/main/README.zh.md)。源码服务、桌面安装包和模型任务分别验收。

## 准备、权限与顺序
1. 阅读当前README并记录版本；准备受支持Python/Node、git与真正可用的npm。Node存在不等于npm可用，Windows没有py启动器时使用已知Python可执行文件。
2. 克隆至独立目录，创建backend/.venv，按README装backend开发依赖；用npm --prefix frontend-enterprise ci遵循锁文件，勿擅换安装器。
3. 从示例创建backend/.env；由用户填写真实OpenAI兼容接口与Key，示例地址不是已接通模型，不公开配置或秘密。
4. 用官方PowerShell dev_up.ps1 --detach启动，检查日志、health与gallery；中文Windows读取清单报gbk时核编码并用PYTHONUTF8=1恢复。
5. 模型接入后再发最小任务，分别检查请求、响应、工具执行及产物；桌面版若另装需再核版本，不能从网页服务推定已装桌面包。

## 使用的技能与工具
本次已用git、Python3.12.14、Node24.22.1、npm、PowerShell官方启动脚本和HTTP路由检查；无专用Skill已读证据，不编造Skill来源。模型由用户配置，未调用生成模型。输入为仓库和依赖锁文件，输出为依赖环境、日志及可响应页面。

## 费用、验收和恢复
源码服务启动不证明模型免费；模型API、托管与工具服务分别按实际计划核价，本次未购买。历史health返回status ok、gallery HTTP200；模型对话与完整数字员工任务未验。重用前核服务进程与日志，保留原配置安全备份；失败先核编码、运行时、端口和依赖，不接管其他聊天服务。2026-11-12建立稳定入口，后续回写本页。
