---
updated: 2026-08-04
status: VERIFIED_LOCAL_TOOLS_ONLY
confidence: HIGH
sources:
  - https://shopify.dev/docs/storefronts/themes/tools/cli
  - https://shopify.dev/docs/api/admin-graphql/2026-04
  - https://shopify.dev/docs/api/storefront/2026-04
  - D:\codex\AGENTS.md
next_review: 2026-09-04
---

# Shopify 接入与验证指南

这份指南把 Shopify 接入分成三条独立通道：主题 CLI、Admin API 和 Storefront API。先按任务选择通道，不要把“已经登录”“已经连接”“已经上传未发布主题”和“已经发布到线上”混为一谈。

## 先选择正确的接入通道

| 要做的事 | 接入通道 | 典型权限 | 是否会改线上数据 |
| --- | --- | --- | --- |
| 本地检查 Liquid、JSON、CSS、JS | Shopify CLI `theme check` | 不需要店铺权限 | 否 |
| 读取主题列表、拉取远程主题 | Shopify CLI 主题命令 | Themes/Manage themes 或 Theme Access | 读取远程；拉取可能覆盖本地文件 |
| 预览本地主题 | `theme dev` 或未发布主题 | 主题写权限 | 会创建或更新开发主题，但不等于发布 |
| 上传候选主题 | `theme push --unpublished` | 主题写权限 | 会写入主题库，但不等于发布 |
| 发布正式主题 | `theme publish` | 主题写权限及单独授权 | 是，改变访客看到的线上主题 |
| 读取或修改商品、订单、客户、元字段 | Admin GraphQL API | 对应 `read_*` / `write_*` scopes | 取决于调用的查询或 mutation |
| 自建前端读取商品、创建购物车 | Storefront GraphQL API | Storefront token/权限 | 商品查询只读；购物车操作会创建购物车状态 |

默认原则：能用主题 CLI 完成的主题工作，不申请 Admin API；只读任务不申请写权限；任何真实写入、上传或发布都需要当次明确授权。

## 当前机器上的已知工具

- Shopify CLI：`3.94.3`，PowerShell 中使用 `shopify.cmd`。
- 官方开发文档入口已配置为 `shopify-dev` MCP；通用框架文档可使用 `context7` MCP。
- ArmorHue 历史店铺目标：`e1rkqv-mg.myshopify.com`。
- Yufeng 历史店铺目标：`wa5nu1-eb.myshopify.com`。

上面两个域名只是历史目标，不代表当前登录、权限或店铺状态。每次执行前都要让用户确认品牌、店铺域名、主题 ID/角色和本次允许的动作。

## 一、接入主题开发

### 前置条件

1. 本地目录必须是标准 Shopify 主题结构，至少包含 `layout/`、`templates/`、`sections/`、`snippets/`、`assets/` 和 `config/` 中的适用目录。
2. 确认 Git 工作树状态或先复制到候选目录，避免 `theme pull` 覆盖未保存修改。
3. 准备以下四项，但不要写入知识库：
   - `<STORE>.myshopify.com`
   - 本地 `<THEME_DIR>`
   - 目标 `<THEME_ID>` 或主题名
   - Shopify 账户登录，或 Theme Access 密码/自定义应用令牌

### 1. 先做完全本地的检查

```powershell
shopify.cmd version
shopify.cmd theme check --path "<THEME_DIR>" --no-color
```

`theme check` 只证明本地主题语法和部分最佳实践通过，不证明已经连接店铺，也不证明线上页面、图片、路由、分析或转化流程正常。

### 2. 选择认证方式

推荐优先级：

1. 店主、Staff 或 Collaborator 账户交互登录。运行需要店铺访问的命令时，CLI 会提示登录。
2. Theme Access 应用生成的密码。适合把主题权限交给开发者或自动化。
3. 具备 `read_themes` / `write_themes` scopes 的自定义应用令牌。只在已有应用治理流程时使用。

交互登录示例：

```powershell
shopify.cmd auth login
shopify.cmd theme info --store "<STORE>.myshopify.com" --path "<THEME_DIR>"
```

Theme Access 示例使用当前 PowerShell 会话的环境变量，关闭窗口后失效：

```powershell
$env:SHOPIFY_CLI_THEME_TOKEN = '<THEME_ACCESS_PASSWORD>'
$env:SHOPIFY_FLAG_STORE = '<STORE>.myshopify.com'
shopify.cmd theme info --path "<THEME_DIR>"
```

不要把真实密码直接写进命令历史、`.env`、Markdown、任务包或 Git。跨电脑时重新登录或在目标机器的秘密管理工具中设置。

### 3. 确认连接的是正确店铺

```powershell
shopify.cmd theme info --store "<STORE>.myshopify.com" --path "<THEME_DIR>"
shopify.cmd theme list --store "<STORE>.myshopify.com" --path "<THEME_DIR>"
shopify.cmd theme list --store "<STORE>.myshopify.com" --role live --path "<THEME_DIR>"
shopify.cmd theme list --store "<STORE>.myshopify.com" --role unpublished --path "<THEME_DIR>"
```

验收时记录非秘密信息：店铺域名、主题 ID、主题名称、角色 `live` / `unpublished` / `development`、检查日期。登录成功只证明身份可用，不代表用户授权修改该店铺。

### 4. 安全拉取远程主题

优先拉到新目录，或确认本地修改已经受 Git 保护：

```powershell
shopify.cmd theme pull --store "<STORE>.myshopify.com" --theme "<THEME_ID>" --path "<EMPTY_OR_SAFE_DIR>" --nodelete
```

省略 `--theme` 会进入交互选择。`--live` 会明确选择线上主题；除非任务就是取得线上基线，否则不要默认使用。拉取前后检查 `git status` 和文件差异。

### 5. 使用开发主题预览

只有用户明确允许连接并创建/更新开发主题后才运行：

```powershell
shopify.cmd theme dev --store "<STORE>.myshopify.com" --path "<THEME_DIR>" --open
```

它会创建或更新 development theme，并给出本地预览、主题编辑器和分享预览地址。命令运行期间，本地改动可能实时同步到开发主题。不要加 `--allow-live`，除非用户明确要求在 live theme 上开发并确认风险。

### 6. 上传未发布候选主题

先检查，再只上传为未发布主题：

```powershell
shopify.cmd theme check --path "<THEME_DIR>" --no-color
shopify.cmd theme push --store "<STORE>.myshopify.com" --path "<THEME_DIR>" --unpublished --strict --json
```

保存返回的非秘密 `theme.id`、`role`、`preview_url` 和 `editor_url` 作为验收证据。不要使用 `--publish`、`--live` 或 `--allow-live`。上传到主题库仍然不是发布。

### 7. 发布必须单独授权

只有用户明确给出店铺、主题 ID 和“现在发布”授权后，才可执行：

```powershell
shopify.cmd theme publish --store "<STORE>.myshopify.com" --theme "<THEME_ID>"
```

发布前至少确认：目标主题角色为 `unpublished`、预览通过桌面和移动验收、关键商品/集合/购物车路由可用、控制台无关键错误、主题 ID 与品牌匹配。不要用 `--force` 跳过确认。

## 二、接入 Admin GraphQL API

Admin API 用于后台资源，例如商品、订单、客户、库存和元字段。它不是主题 CLI 的替代品。

### 1. 创建并授权应用

1. 在 Shopify 的应用开发入口创建 custom app，或在 Dev Dashboard 创建并安装应用。
2. 只申请本任务需要的 scopes。例如只读商品用 `read_products`；只有确实要改商品时才增加 `write_products`。
3. 让店主检查 scopes 并安装应用。
4. 获取 Admin API access token。令牌通常只显示一次，立即放入目标机器的秘密管理位置，不写入仓库。
5. 记录非秘密信息：应用名、店铺域名、API 版本、granted scopes、安装日期和负责人。

### 2. 在当前 PowerShell 会话设置凭据

```powershell
$env:SHOPIFY_STORE_DOMAIN = '<STORE>.myshopify.com'
$env:SHOPIFY_ADMIN_TOKEN = '<ADMIN_ACCESS_TOKEN>'
```

另一台电脑或另一个 AI 不会因为克隆了知识库就自动得到 Shopify 权限。必须在那台机器重新登录或由用户单独配置令牌。

### 3. 用只读查询验证连接

下面的查询已按 Admin GraphQL `2026-04` Schema 校验：

```graphql
query ConnectionCheck {
  shop {
    name
    myshopifyDomain
  }
}
```

PowerShell 调用：

```powershell
$adminHeaders = @{
  'Content-Type' = 'application/json'
  'X-Shopify-Access-Token' = $env:SHOPIFY_ADMIN_TOKEN
}
$adminBody = @{
  query = 'query ConnectionCheck { shop { name myshopifyDomain } }'
} | ConvertTo-Json
Invoke-RestMethod -Method Post `
  -Uri "https://$env:SHOPIFY_STORE_DOMAIN/admin/api/2026-04/graphql.json" `
  -Headers $adminHeaders `
  -Body $adminBody
```

成功标准：HTTP 成功、响应中无 `errors`、`shop.myshopifyDomain` 与目标店铺一致。只读查询成功不授权后续 mutation。

### 4. Admin API 写操作关卡

每次写操作前必须明确：店铺、资源、对象 ID、字段、旧值、新值、回滚方式和当次授权。先读当前值，再做最小 mutation，再回读验证。批量商品、订单、客户或库存修改还要先生成 dry-run 清单。

## 三、接入 Storefront GraphQL API

Storefront API 面向自建前端、移动端或 Headless 商店，用于读取公开商品数据和创建购物车。它不能执行 Admin 后台管理。

### 1. 选择 token 类型

- Public access token：用于浏览器或移动应用。它仍应只授予最小 Storefront 权限，不能当作 Admin token。
- Private access token：用于服务器、Hydrogen 后端或其他私有上下文，绝不能放进浏览器包或公开仓库。
- Tokenless：只支持一部分无需 token 的公开查询；要使用完整功能仍需 token。

### 2. 设置会话变量

```powershell
$env:SHOPIFY_STORE_DOMAIN = '<STORE>.myshopify.com'
$env:SHOPIFY_STOREFRONT_TOKEN = '<STOREFRONT_ACCESS_TOKEN>'
```

### 3. 验证商品读取

下面的查询已按 Storefront GraphQL `2026-04` Schema 校验：

```graphql
query StorefrontConnectionCheck {
  products(first: 3) {
    nodes {
      id
      handle
      title
      availableForSale
    }
  }
}
```

下面的 PowerShell 示例使用 Public access token。Private access token 只应在服务器端通过 Shopify 官方客户端或对应的服务器认证方式使用，不能照搬到浏览器代码中。

```powershell
$storefrontHeaders = @{
  'Content-Type' = 'application/json'
  'X-Shopify-Storefront-Access-Token' = $env:SHOPIFY_STOREFRONT_TOKEN
}
$storefrontBody = @{
  query = 'query StorefrontConnectionCheck { products(first: 3) { nodes { id handle title availableForSale } } }'
} | ConvertTo-Json
Invoke-RestMethod -Method Post `
  -Uri "https://$env:SHOPIFY_STORE_DOMAIN/api/2026-04/graphql.json" `
  -Headers $storefrontHeaders `
  -Body $storefrontBody
```

成功标准：响应无 `errors`，商品来自正确店铺；返回空数组时还要区分“连接成功但没有已发布到该销售渠道的商品”和“权限/查询失败”。

### 4. 购物车能力

创建购物车使用 `cartCreate`，不是 Admin API 的订单写入。下面的 mutation 已按 `2026-04` Schema 校验：

```graphql
mutation CreateCart($lines: [CartLineInput!]) {
  cartCreate(input: { lines: $lines }) {
    cart {
      id
      checkoutUrl
      totalQuantity
    }
    userErrors {
      field
      message
    }
  }
}
```

测试时使用测试商品变体 ID，并检查 `userErrors`。得到 checkout URL 不等于已下单、已付款或已成交。

## 四、跨设备和其他 AI 的接入方式

1. 在新电脑登录 GitHub，克隆这个 Private 仓库。
2. 让 AI 先读 `AI_CONTEXT.md`、本指南和对应项目页。
3. 单独安装/验证 Shopify CLI；大安装前仍按磁盘规则确认。
4. 在新电脑通过浏览器登录或设置环境变量，不把凭据同步进 Git。
5. 先运行 `theme check` 或只读 API 查询。
6. 让 AI 报告目标店铺、权限、主题角色和计划动作，得到明确授权后才进行远程写入。

## 五、常见故障

| 现象 | 优先检查 | 不要误判为 |
| --- | --- | --- |
| CLI 一直要求登录 | 当前账户、店铺权限、浏览器验证码、是否切错账户 | CLI 未安装 |
| `theme info` 指向错误店铺 | 显式传 `--store`，再看输出域名 | 主题代码错误 |
| Theme Access 认证失败 | 密码是否撤销、店铺是否匹配、Themes 权限 | 必须重装 CLI |
| `theme pull` 后本地文件变化很大 | 是否拉错主题、是否省略 `--nodelete`、本地是否有未提交修改 | Shopify 自动损坏主题 |
| `theme check` 通过但线上仍错 | live theme ID、发布状态、路由、资源、Admin 设置、缓存 | 已经上线成功 |
| Admin API `401/403` | token、安装状态、API 版本、granted scopes | GraphQL 语法必然错误 |
| GraphQL 返回 `errors` | 错误正文、字段是否属于当前 API、权限是否足够 | HTTP 成功就等于业务成功 |
| Storefront 商品为空 | 商品是否发布到对应销售渠道、Markets/可售状态 | token 一定失效 |
| 上传候选后访客没变化 | 候选仍是 `unpublished` | 上传失败 |

## 六、每次操作的记录模板

```text
日期：YYYY-MM-DD HH:mm +08:00
品牌：<BRAND>
店铺：<STORE>.myshopify.com
通道：Theme CLI | Admin API | Storefront API
权限：只读 | 写入候选 | 发布
目标对象：<THEME_ID / RESOURCE_ID>
执行动作：<COMMAND_OR_OPERATION>
结果：PASS | WATCH | FAIL | BLOCKED
非秘密证据：<REPORT_PATH / THEME_ROLE / PREVIEW_URL>
未执行：<LIVE_PUBLISH / DATA_MUTATION / OTHER>
```

## 相关文档

- [独立站与 Shopify](independent-sites-and-shopify.md)
- [用户长期要求](../system/user-requirements.md)
- [完整知识与要求审阅稿](../../reports/full-knowledge-requirements-review-2026-08-04.md)
