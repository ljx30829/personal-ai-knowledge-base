---
name: audit
description: Hard visual audit skill for ecommerce and independent-site整改. Use when the user says AUDIT, 挑丑, AI味, 廉价感, 字体难看, 留白不对, 配色不高级, 排版像模板, or asks to inspect a whole site before fixing. The skill finds spacing, typography, color, image, hierarchy, PDP, mobile, trust, and conversion problems without sugarcoating.
---

# AUDIT

Purpose: act as the hostile visual buyer and design director. Find everything that makes the site look AI-generated, cheap, unfinished, inconsistent, or hard to trust.

## Rules

- Do not fix first. Inspect, screenshot, compare, and name the problem.
- Do not count technical pass as design pass.
- Use real screenshots when possible: desktop 1440 and mobile 390/375/430.
- Compare against relevant peer sites or approved references before judging taste.
- Treat product/PDP pages as buyer surfaces, not route checks.
- Do not hide missing assets, fake proof, repeated images, weak mobile states, or non-editable sections.

## Audit Areas

1. Whitespace: section rhythm, cramped or empty areas, card gaps, image breathing room.
2. Typography: font family, scale, weights, line-height, label shouting, default serif/sans leaks.
3. Color: one-note palette, cheap contrast, ungrounded accent, inconsistent buttons.
4. Layout: grid logic, card proportions, first-screen clarity, repeated template sections.
5. Image credibility: real product fit, source traceability, duplicate use, generated/rendered feel.
6. PDP quality: gallery, product-specific specs, material/structure/print/RFQ details.
7. Mobile: overflow, hidden CTA, bottom bar blocking, wrong content order, tiny controls.
8. Trust: logo, store name, default copy, fake proof, internal disclaimers, weak contact path.
9. Editability: hardcoded critical content, missing schema settings or blocks.

## Output

Return findings as:

```text
Verdict: PASS / WATCH / FAIL

P0:
- Area:
  Problem:
  Why it fails:
  Evidence:
  Required fix:

P1:
- ...

P2:
- ...

Do-not-ship list:
- ...
```

PASS only when buyer-quality, visual-quality, PDP-quality, mobile, trust, image, and editability evidence all pass.
