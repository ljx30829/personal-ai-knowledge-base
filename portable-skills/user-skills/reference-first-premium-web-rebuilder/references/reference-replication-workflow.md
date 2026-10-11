# Reference Replication Workflow

## Goal

Force learning through rendered evidence. The agent must inspect, capture, replicate, compare, correct, and only then adapt. A loose "inspired by" page fails.

## Stage 1: Select A Reference Per Page Type

Every page type needs a reference source. Do not use one generic reference for the whole site unless that reference genuinely covers every needed page type.

Select by purpose:

- Premium visual/motion: Viktor Oddy, Cuberto, Locomotive, Lusion.
- Experimental motion: Dogstudio, Active Theory, Resn, Unseen Studio.
- Commercial adaptation: PackMint, Rootree, CarePac, Accredo, Flexiarte, ePac Connected Packaging.

State:

- Target page.
- Primary reference URL.
- Secondary reference URL if motion or commercial content logic comes from a different source.
- What the reference is allowed to teach: layout, hierarchy, motion, mobile, taxonomy, form logic, proof structure, or product presentation.

## Stage 2: Capture Before Any Design Or Code

Before writing code or choosing style tokens, capture:

- Reference desktop first viewport.
- Reference desktop full page.
- Reference mobile first viewport.
- Reference mobile full page.
- Target current desktop first viewport.
- Target current desktop full page.
- Target current mobile first viewport.
- Target current mobile full page.

Write a capture manifest with URL, viewport, screenshot path, timestamp, and purpose for each image. If a screenshot fails, stop and fix capture rather than continuing from memory.

Also capture states when relevant:

- Navigation open/closed.
- Sticky header on scroll.
- Card/button/image hover.
- Product gallery states.
- Form focus/error/submit states.
- Scroll-triggered motion states.

Default viewports:

- Desktop: 1440 x 900.
- Mobile: 390 x 844.

## Stage 3: Decompose Screen By Screen

Create notes for each screen/section:

- Section height and viewport position.
- Navigation height, logo scale, link alignment, CTA position.
- Hero title max width, line breaks, line-height, and relation to media.
- Image crop, aspect ratio, focal point, quality, and loading.
- Grid columns, margins, gutters, and max-width.
- Card ratio, radius, media/text split, and hover state.
- CTA size, position, spacing, and visual priority.
- Whitespace rhythm between sections.
- Scroll rhythm and section transition.
- Motion trigger, duration, easing, stagger, transform, opacity, clip/mask.
- Mobile stacking order and removed/condensed content.
- Form field grouping and usability.
- Footer structure and density.

## Stage 4: Build One Representative Page First

For a full-site build, first make one representative page pass the reference side-by-side gate.

Do not batch-generate the whole site before one page visually passes. The representative page should be the page with the hardest combination of layout, media, motion, commercial logic, and mobile behavior.

Once it passes:

- Extract the visual system.
- Apply it to the rest of the site.
- Vary page structure by page type.
- Fail the task if all pages share the same template and only swap headings.

## Stage 5: Build The Private Replica

Build from observation, not copied source code:

- Match layout structure before colors.
- Match proportions before decorative details.
- Match typography hierarchy before final font selection.
- Match image placement and crop before replacing assets.
- Match motion rhythm before adding extra effects.
- Match mobile behavior before expanding desktop features.

The private replica may use placeholders while learning, but the final public target must not retain unauthorized reference assets.

## Stage 6: Make Side-By-Side Evidence

Create side-by-side comparisons for:

- Reference desktop vs replica/target desktop.
- Reference mobile vs replica/target mobile.
- Target before vs target after.

If the comparison is not visually legible, remake it. Evidence must show enough of the page to judge structure, proportions, image treatment, mobile stacking, and motion states.

For multi-page work, create side-by-side evidence for every page type being claimed complete. Do not let a product detail page, service page, case study, FAQ, or contact page pass only because the home page passed. Closely equivalent pages may inherit a visual system only when the difference table documents the shared template, the page-specific content risks, and the screenshot check for that page.

## Stage 7: Produce The Difference Table

Required columns:

| Screen / section | Reference screenshot path | Target screenshot path | Difference type | Exact issue | Required correction | Status |
|---|---|---|---|---|---|---|
| Hero | path | path | typography | Heading wraps one line earlier than reference | Reduce max-width or font size | pending |

Allowed statuses:

- fixed
- pending
- intentionally different

Use "intentionally different" only when the target brand, content, legal limits, or commercial needs justify the difference.

## Stage 8: Correct Until The Gate Passes

Correction priority:

1. Page structure and module order.
2. First viewport composition.
3. Section height and spacing rhythm.
4. Typography scale and wrap points.
5. Image crop, quality, style consistency, and loading.
6. Navigation alignment and density.
7. Cards, buttons, forms, and repeated modules.
8. Motion rhythm and hover behavior.
9. Mobile stacking and horizontal overflow.
10. Footer completeness.

After each correction pass:

- Rebuild.
- Re-capture desktop/mobile.
- Regenerate side-by-side evidence.
- Update the difference table.

Continue while screenshots still do not match closely enough.

## Stage 9: Adapt To Target Brand

Only after the representative replica passes:

- Replace reference brand marks with target brand marks.
- Replace copy with target-owned copy.
- Replace projects, customers, reviews, awards, and metrics with confirmed target proof or remove them.
- Replace reference images with owned, licensed, supplier-authorized, clearly reusable, generated, or newly produced target assets.
- Retain the learned layout, hierarchy, media placement, motion discipline, and mobile behavior.

## Stage 10: Final Public Gate

Before handoff:

- Confirm every claimed page type has a reference URL, reference screenshots, target-before screenshots, final screenshots, side-by-side evidence, and a difference table.
- Confirm no reference-owned public assets remain.
- Confirm all key images load and have `naturalWidth > 0`.
- Confirm no horizontal overflow on mobile.
- Confirm forms are usable.
- Confirm motion does not hide content.
- Confirm no fake claims were invented.
- Confirm final screenshots and side-by-side evidence paths are reported.
