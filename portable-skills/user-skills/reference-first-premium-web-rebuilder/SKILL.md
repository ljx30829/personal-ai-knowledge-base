---
name: reference-first-premium-web-rebuilder
description: Use when designing, rebuilding, auditing, or improving a website by first replicating premium reference websites screen by screen, then adapting the replicated structure, visual hierarchy, motion rhythm, and responsive behavior to the target brand. Use for brand sites, product sites, ecommerce pages, B2B independent sites, factory websites, landing pages, and service websites that must avoid AI-template visuals and need concrete reference fidelity before original adaptation.
---

# Reference-First Premium Web Rebuilder

## Purpose

Use this skill to make Codex rebuild premium websites through concrete reference-first screen replication. The method is not "inspired by". The method is not abstract style analysis. The method is reference-first screen replication: open real reference sites, capture screenshots, replicate the rendered screens, compare side by side, fix differences, then adapt the proven system to the target brand.

The final public site must be original and legally usable. Reference screenshots may be used for private learning and comparison only.

## When To Use

Use this skill for brand sites, product sites, ecommerce pages, B2B independent sites, factory websites, packaging sites, landing pages, service websites, and any page that must stop looking like an AI template.

Use it when the task involves:

- Premium visual hierarchy, layout, motion, responsive behavior, image art direction, or anti-template redesign.
- References such as Viktor Oddy, Cuberto, Locomotive, Lusion, Dogstudio, Active Theory, Unseen Studio, Resn, Ovra Studio, HC Design, Rootree, CarePac, PackMint, Accredo, Flexiarte, or ePac Connected Packaging.
- Rebuilding a target page against a real reference with screenshot proof.

## Required Inputs

Collect or infer:

- Target URL or local page path.
- Reference URL for every page type being rebuilt. If missing, choose from `references/reference-sites.md` and state why.
- Page type: Home, Products, Product detail, Category/collection, Service page, Bag style/product taxonomy, Capabilities/factory/operations, Case study/project page, QR/connected packaging/data service, Contact/quote/lead form, About, Quality/trust, FAQ, Landing page, or Long-scroll brand page.
- Target brand content, real assets, constraints, and unconfirmed claims.
- Verification viewport sizes. Default to desktop 1440 x 900 and mobile 390 x 844.

## Core Principle: Replicate First, Adapt Second

Do not start by designing.
Do not start by writing code.
Do not start by choosing colors or typography.
Do not start from memory or impressions.

Start by opening the reference site and capturing desktop and mobile screenshots. A page is not complete if it only loosely resembles the reference. A build is not complete without side-by-side screenshots. A page is not complete if it still looks like an AI template, if mobile was not checked, if images were not checked, if horizontal overflow exists, or if major images are broken or low quality.

## Workflow

1. Read project instructions and state files first when working in a repository.
2. Select a reference for the page using `references/reference-sites.md` and `references/page-application.md`.
3. Open the reference website in a real browser.
4. Capture reference desktop screenshots.
5. Capture reference mobile screenshots.
6. Capture current target desktop screenshots.
7. Capture current target mobile screenshots.
8. Stop if any required reference or target-before screenshot is missing. Do not write implementation code from memory.
9. Decompose each screen into layout, spacing, typography, image, motion, mobile, content, navigation, forms, and footer behavior.
10. Build one private representative-page replica first. Do not batch-generate the whole site before one page passes the visual gate.
11. Create side-by-side screenshots: reference vs replica/target, desktop and mobile.
12. Produce a difference table with status for every major screen/section.
13. Fix differences by priority: structure, proportions, typography, image crop/quality, spacing, motion, mobile, forms, footer.
14. Re-capture screenshots after each correction pass.
15. Repeat until the representative page passes the side-by-side visual gate.
16. Adapt the passed page to the target brand using original or authorized assets/content.
17. Apply the proven visual system to the rest of the site. If all pages share the same template and only swap headings, fail the task.
18. Run the hard acceptance gate before handoff.

Read `references/reference-replication-workflow.md` for the detailed procedure.

## Reference Capture Requirements

Capture:

- Reference desktop full-page and first-viewport screenshots.
- Reference mobile full-page and first-viewport screenshots.
- Target before desktop full-page and first-viewport screenshots.
- Target before mobile full-page and first-viewport screenshots.
- Hover, menu, form, sticky, scroll, and motion states when relevant.
- Final desktop and mobile screenshots after correction.
- A capture manifest that lists each screenshot path, viewport, URL, timestamp, and whether it is reference, target-before, target-after, or side-by-side evidence.

Each page type needs a reference source. Do not rebuild a page type from generic taste alone.

## Side-By-Side Comparison Requirements

Mandatory evidence:

- Reference desktop vs target/replica desktop.
- Reference mobile vs target/replica mobile.
- Before vs after when redesigning an existing target.
- Per-page side-by-side evidence for every page type being claimed as complete. A page cannot inherit approval from another page unless the difference table explicitly says why that inheritance is valid.
- A difference table using this schema:
  - Screen / section
  - Reference screenshot path
  - Target screenshot path
  - Difference type: layout / spacing / typography / image / motion / mobile / content
  - Exact issue
  - Required correction
  - Status: fixed / pending / intentionally different

Do not deliver if side-by-side evidence is missing.

## Reference Learning Stage Vs Final Public Stage

Reference learning stage allows:

- Use reference screenshots for internal comparison.
- Temporarily replicate layout, proportions, visual rhythm, and motion rhythm.
- Analyze image composition, position, crop, lighting, and section cadence.

Final public deliverable stage requires:

- Remove reference logos, trademarks, client cases, reviews, original copy, and unauthorized competitor images.
- Do not copy reference source code.
- Replace with target brand content, images, products, copy, forms, and proof.
- Use user-provided authorized materials only within the authorized scope.
- If no authorization exists, create or source target-brand assets with similar composition, quality, and placement without copying protected materials.

## Visual Replication Rules

Follow `references/visual-replication-rules.md`. The replica must cover first screen structure, navigation, title proportions, font hierarchy, image position, image crop, module order, card ratio, button placement, whitespace rhythm, scroll rhythm, hover effects, transition behavior, mobile stacking, form structure, and footer structure.

## Motion Replication Rules

Follow `references/motion-replication-rules.md`. Capture trigger, duration, easing, stagger, transform, opacity, clip/mask, scroll behavior, hover states, mobile reduction, and reduced-motion fallback.

Only reproduce useful commercial motion. Motion must not hide content, block forms, create horizontal overflow, or become random fade-in decoration.

## Page-Specific Adaptation Guidance

Use `references/page-application.md`. Each page type must state its primary reference type, what to replicate, what to adapt, common AI failure, and required verification.

For B2B and factory sites, premium must remain credible: show real capabilities, production context, quality control, product detail, forms, and confirmed proof. Never invent certifications, capacity, clients, reviews, warehouse claims, specs, warranties, prices, or metrics.

## Anti-AI Template Rules

Use `references/anti-ai-template-checklist.md`. Block handoff for generic card grids, fake metrics, low-quality SVG hero/product placeholders, huge AI-template headlines, repeated page templates, broken images, mobile overflow, loose "inspired by" output, or cloned reference assets in final public output.

## Hard Acceptance Gate

PASS only when:

- Reference screenshots exist.
- Target before screenshots exist.
- Side-by-side screenshots exist.
- Difference table exists.
- Every completed page type has its own reference source and evidence, or a documented reason it inherits a passed system from a closely equivalent page.
- One representative page passes visual comparison before full-site expansion.
- Desktop was checked.
- Mobile was checked.
- No horizontal overflow.
- All key images have `naturalWidth > 0`.
- No broken images.
- No low-quality SVG hero/product placeholders.
- No fake metrics, fake ratings, fake reviews, or fake proof.
- No repeated generic card grids.
- No huge AI-template hero headline unless directly supported by the reference and target content.
- No template-style dark/green/black background used without direct reference evidence.
- No cloned reference brand assets remain in final public output.

FAIL when:

- No reference screenshots.
- No side-by-side evidence.
- "Inspired by" without visible screen replication.
- Batch-generated pages with the same layout.
- Mobile overflow.
- Broken or low-quality major images.
- Unusable forms.
- The result still looks like an AI landing page.

## Verification Checklist

Before handoff, verify:

- YAML/frontmatter and skill references are intact when editing the skill itself.
- Every page has an identified reference source.
- Reference, target-before, side-by-side, and final screenshots are saved with paths.
- Difference table records fixed, pending, and intentionally different items.
- Desktop and mobile screenshots were inspected.
- Horizontal overflow was checked.
- Key images load and are high enough quality for their role.
- Hover, transition, scroll, menu, sticky, and form states were checked where relevant.
- Final public output uses original or authorized target content/assets.
- No reference-owned public content remains.
- No fake business proof was invented.

## Output Format

For build/redesign work, report:

- Target URL/path and reference URL(s).
- Representative page selected and why.
- Screenshot evidence paths for reference, target before, side-by-side, and final target.
- Difference table path or inline table.
- Fixed, pending, and intentionally different items.
- Desktop, mobile, overflow, image-loading, motion, and form verification results.
- Files changed and preview URL.
- Any unconfirmed facts or assets requiring user/supplier confirmation.

Example prompt:

```text
Use reference-first-premium-web-rebuilder to rebuild http://127.0.0.1:8129/bag-styles.html against Rootree. Capture desktop/mobile reference screenshots, build side-by-side comparisons, fix differences, and do not hand off until the visual gate passes.
```
