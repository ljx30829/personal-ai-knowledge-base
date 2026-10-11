# 10 国法律页面与联系方式路径表

> 外贸客户开发中，不同国家有不同法律要求的公开页面。访问这些页面可以获取公司注册信息、邮箱、电话。

## 各国路径

| 国家 | 代码 | 法律/注册页面 | 联系方式页 | 备注 |
|------|:--:|------|------|------|
| 🇩🇪 德国 | DE | `/impressum` | `/kontakt` | 法律强制公开，含HRB注册号+CEO姓名 |
| 🇪🇸 西班牙 | ES | `/aviso-legal` | `/contacto` | |
| 🇫🇷 法国 | FR | `/mentions-legales` | `/contact` | 含SIREN/SIRET企业号 |
| 🇮🇹 意大利 | IT | `/privacy` | `/contatti` | 或 `/informativa-legale` |
| 🇺🇸 美国 | US | `/privacy-policy` | `/contact` | 各州不同，通用路径 |
| 🇬🇧 英国 | UK | `/terms-conditions` | `/contact` | Companies House 号通常在footer |
| 🇳🇱 荷兰 | NL | `/privacy` | `/contact` | KVK号通常在footer |
| 🇧🇷 巴西 | BR | `/politica-de-privacidade` | `/contato` | CNPJ税号通常在footer |
| 🇯🇵 日本 | JP | `/privacy` | `/contact` | 法人番号通常在footer |

## 通用兜底路径

当国家不在上表中时，依次尝试：
```
/contact, /contact-us, /contactus
/about, /about-us, /aboutus
/kontakt, /contacto, /contatti
/impressum, /imprint
```

## 邮箱提取优先级

1. 首页 → 最快
2. 法律页面 → 邮箱通常在底部（Impressum等）
3. 联系方式页 → 专门的邮箱入口
4. 通用路径兜底

## 已验证案例

| 公司 | 国家 | 页面 | 提取结果 |
|------|:--:|------|------|
| LEDclusive.de | 🇩🇪 | `/impressum` | ✅ info@ledclusive.de + HRB-Nr. + CEO |
| Wholesale LED Lights | 🇬🇧 | `/` (footer) | ✅ cs@wled.co.uk + Company No. |
| LED Lighting Wholesale Inc. | 🇺🇸 | `/` (header) | ✅ 电话，邮箱需进一步获取 |
