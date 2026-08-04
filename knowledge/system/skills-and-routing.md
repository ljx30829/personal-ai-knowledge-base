---
updated: 2026-08-04
status: VERIFIED
confidence: HIGH
sources:
  - ../../sources/codex-inventory/codex-inventory.md
  - ../../sources/codex-inventory/codex-skill-organization.md
next_review: 2026-09-04
---

# 技能与路由

## 可复用结论

- 先读取仓库内的 `AGENTS.md`、状态文件和相关工作流，再选择技能。
- 同名技能同时出现在根目录与 `gstack/` 时，默认优先根目录版本；不要自动删除重复项。
- 强制流程技能是质量关卡，不是领域专家。规划、测试、调试和交付验证应与领域技能组合使用。
- 只加载完成当前任务所需的最小技能集合。多个技能规则冲突时，用户的当前明确要求和仓库 `AGENTS.md` 优先。
- 技能清单是某一时点的快照。安装、删除或升级技能后重新生成清单，不靠旧计数推断当前状态。

## 当前清单

- 生成时间：2026-08-04。
- 技能条目：251。
- 唯一技能名：193。
- 重复技能名：58，共 116 个重复条目。
- 潜在规则冲突技能：33。
- 要求条目：1569。

完整数据见 [Codex 技能清单](../../sources/codex-inventory/codex-inventory.md) 和 [重复与路由报告](../../sources/codex-inventory/codex-skill-organization.md)。

## 任务路由

| 任务 | 首选技能 | 完成前检查 |
| --- | --- | --- |
| 一般仓库工作 | `using-superpowers` 或当前仓库指定流程 | `verification-before-completion` |
| 新功能或行为变化 | `brainstorming`、`test-driven-development` | 聚焦测试与完整测试 |
| 故障、失败测试、异常行为 | `systematic-debugging` | 回归测试与根因证据 |
| 长计划执行 | `executing-plans` | 每项状态、测试、最终验收 |
| 完整独立站或 Shopify 页面 | `independent-site-build-orchestrator` | `end-to-end-quality-auditor` |
| ArmorHue 视觉与店铺质量 | `armorhue-luxury-ecommerce-art-director` | `armorhue-no-slop-delivery-gate` |
| 产品图、主图、横幅 | `exact-visual-asset-director` | 来源、颜色、车型、授权与移动端截图 |
| 汽车膜 PDP、TDS、参数、质保 | `automotive-film-pdp-tds-builder` | 不虚构参数；做图文与变体一致性审计 |
| B2B 批发、经销商、样品漏斗 | `armorhue-b2b-wholesale-funnel-architect` | 价格隔离、资格收集、真实商务依据 |
| 竞品参考和重建 | `competitor-site-reference-rebuilder` | 不复制代码、图片、商标、文案或评论 |
| 自媒体或外贸执行 | 对应项目运行手册和专用技能 | 发送、发布和互动的当次明确授权 |
| 浏览器或视觉验收 | `playwright`、`qa` | 桌面和移动端证据、控制台与关键流程 |
| 只读审计 | `audit`、`qa-only` | 不修改目标系统 |

## 安装与升级规则

- 安装工具、包、模型、浏览器或 Docker 镜像前，先说明下载量、安装后体积、默认位置和能否放到 D:。
- 大型安装必须先征得确认。优先使用 `D:\codex\.cache`、`D:\codex\tools` 或项目本地环境，避免占用 C:。
- 不为这套知识库安装数据库、向量库、本地模型或常驻服务。Markdown 与 Git 是基础能力。

## 未知项

- 清单生成后新安装或更新的技能尚未包含，使用前可按任务重新生成。
- 潜在冲突表示规则可能重叠，不代表技能损坏；未经验证不得批量删除。

## 来源与证据

- `sources/codex-inventory/codex-inventory.json`
- `sources/codex-inventory/codex-skill-organization.json`
- `C:\Users\26014\Documents\技能\codex_inventory.py`

