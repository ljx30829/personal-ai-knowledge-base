---
name: end-to-end-quality-auditor
description: Final quality-audit workflow for completed site, Shopify theme, content, image, automation, and setup tasks. Use when Codex needs to avoid assumptions, inspect finished work from multiple angles, find remaining problems, fix them, re-check, and provide evidence before handing off as done.
---

# End-to-End Quality Auditor

## Purpose

Make Codex stop at verified completion instead of "it should be fine." After implementation, inspect the result from the buyer, operator, technical, visual, and business angles. Fix issues found when feasible, then verify again.

## Operating Rule

Do not mark work complete based on belief. Use evidence:

- screenshots
- command output
- validation reports
- route checks
- image inventories
- source traces
- preview URLs
- before/after files

## Audit Loop

1. Restate what done means
   - What user asked for.
   - What artifact/page/system must work.
   - What evidence proves it.

2. Inspect from multiple angles
   - User/buyer: can the buyer understand and act?
   - Visual: does it look premium and match the product?
   - Mobile: no overlap, overflow, broken crop, or unusable tap targets.
   - Technical: validations pass, routes work, images load, links are not dead.
   - Shopify/business: no unauthorized publish/delete/payment/domain/checkout changes.
   - Compliance: no copied competitor assets, fake reviews, old brand residue, or leaked secrets.

3. Find issues
   - Treat issues as expected, not exceptional.
   - Prioritize by severity and conversion risk.
   - Do not hide unresolved problems.

4. Fix feasible issues
   - Fix within the task scope.
   - Re-run the relevant check after fixing.
   - If blocked, capture blocker, evidence, and exact next action.

5. Handoff
   - Summarize changes.
   - Provide evidence paths.
   - State tests/checks run.
   - State residual risk or blocked items.

## Minimum Checks For Shopify Site Work

- Desktop screenshot.
- Mobile screenshot.
- No horizontal overflow.
- Important routes return 200.
- No broken important images.
- No old/competitor brand text.
- Product visuals match the title/spec.
- Product cards and PDP galleries do not reuse wrong-color or unrelated images.
- PDP content is not generic copied text when product color/type/finish differs.
- Evidence screenshots are not blocked by cookie/chat/admin overlays and do not show placeholder-looking or cartoon visuals as final assets.
- Theme check or equivalent validation after Liquid/theme edits.
- Links/CTAs lead somewhere useful.

Read `references/quality-pass-checklist.md` for full-site or launch-critical tasks.
