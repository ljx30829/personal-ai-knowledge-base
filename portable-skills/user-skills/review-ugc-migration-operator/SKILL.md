---
name: review-ugc-migration-operator
description: Organize real customer reviews, UGC, star ratings, review CSVs, and Shopify review sections for independent sites. Use when Codex needs to migrate reviews from owned sources, prepare Judge.me, Loox, Yotpo, or Shopify review imports, build review/UGC sections, normalize review data, or design trust blocks without copying competitor testimonials or fabricating customer proof.
---

# Review UGC Migration Operator

## Purpose

Turn real, owned, or authorized customer proof into usable Shopify review sections, import files, and conversion blocks.

## Hard Rules

- Do not copy competitor reviews or present scraped reviews as the user's own customers.
- Do not fabricate names, ratings, dates, verified badges, photos, or claims.
- Only use reviews from owned stores, authorized sources, customer submissions, or explicit user-provided content.
- If review provenance is unclear, label it as research/inspiration only and do not import or publish it.
- For sensitive customer data, avoid exposing emails, phone numbers, addresses, order IDs, or private notes in visible files.

## Workflow

1. Identify source and permission
   - Source examples: old Shopify store, Judge.me export, Yotpo export, Loox export, Amazon/Etsy owned shop export, CSV from user, email screenshots with permission.
   - Confirm whether content is publishable or only for internal research.

2. Normalize review data
   - Required: product handle/title, rating, review body, reviewer display name, date if available.
   - Optional: review title, photo/video path, country, variant, verified marker if supported by source.
   - Strip private identifiers unless the target import format requires them and the user approves.

3. Choose output
   - Import CSV mapping for a review app.
   - Shopify theme review block using existing data.
   - UGC gallery plan.
   - Trust section using aggregate stats only when stats are true.

4. Build the storefront presentation
   - Place reviews near product objections, not only at the bottom.
   - Use product-specific reviews on product pages.
   - Use dealer/installer proof for B2B wholesale pages.
   - Use visual UGC only if images are owned or authorized.

5. Verify
   - Check import columns and encoding.
   - Check no copied competitor text.
   - Check no private customer data leaks.
   - Check mobile layout and star display.

## Output Format

```text
Source status:
- publishable / needs approval / research only

Review mapping:
- ...

Storefront placement:
- ...

Safety checks:
- private data removed, no competitor reviews, no fabricated proof
```

## Extra Reference

Read `references/review-import-fields.md` when preparing a review CSV or theme review schema.
