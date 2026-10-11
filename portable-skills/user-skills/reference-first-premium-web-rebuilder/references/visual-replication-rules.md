# Visual Replication Rules

## Non-Negotiable Rule

Do not make a page that is merely "inspired by" the reference. Rebuild the visible screen system: structure, proportion, hierarchy, image behavior, spacing, motion states, and mobile stacking.

## Measurement Checklist

For each major screen, compare:

- Screenshot path and viewport for both reference and target. If either side is missing, the comparison is invalid.
- Hero title max width, line count, line-height, and position.
- Section height relative to viewport.
- Navigation height, logo alignment, link spacing, and CTA position.
- Main media size, aspect ratio, crop, focal point, and distance from text.
- Card ratio, media/text split, radius, border/shadow, and hover state.
- CTA size, text density, icon use, color/contrast, and position.
- Whitespace above/below headings, images, cards, and section boundaries.
- Grid columns, gutters, margins, and max-width.
- Footer density, columns, legal links, and contact hierarchy.
- Mobile stacking order, spacing, tap target size, and overflow.

## First Screen

Replicate:

- What is visible before scrolling.
- Whether the next section peeks into view.
- Whether the brand/product/object is visible immediately.
- Ratio between navigation, headline, support copy, media, CTA, and empty space.
- The confidence level of the first screen: sparse editorial, dense commercial, image-led, type-led, or motion-led.

Fail when:

- The hero is a generic oversized headline with a paragraph and two buttons.
- The first screen uses a stock-looking background or low-quality SVG in place of real reference structure.

## Navigation

Compare:

- Header height in pixels.
- Logo size and optical alignment.
- Link count, spacing, and weight.
- CTA position and size.
- Sticky/fixed/transparent behavior.
- Mobile menu trigger, menu panel, item spacing, and close behavior.

Fail when:

- Mobile menu is clipped, inaccessible, or misaligned.
- Header takes excessive space compared with the reference.

## Typography

Compare:

- H1/H2/body/caption size relationships.
- Heading max width and wrap points.
- Line-height and paragraph measure.
- Weight contrast between labels, headings, body, and metadata.
- Whether type is editorial, product-dense, technical, or service-oriented.

Fail when:

- Headline is huge only because "premium" was assumed.
- Every section uses the same heading scale.
- Text overflows, overlaps, or wraps awkwardly on mobile.

## Images And Media

Compare:

- Crop and focal point.
- Aspect ratio.
- Position relative to text.
- Visual style consistency across the page.
- Resolution and sharpness.
- Lighting, color temperature, material feel, and product relevance.
- Loading behavior above and below the fold.
- Whether each repeated product/category image is unique enough for its role.

Image quality rules:

- Key images must load and have `naturalWidth > 0`.
- Key images should also have nonzero rendered dimensions and must not be hidden behind empty wrappers, lazy-load failures, cookie overlays, or failed background-image URLs.
- Hero and product images must not be blurry, stretched, watermarked, tiny, or unrelated.
- Product image sets must be complete enough for the page role.
- Do not use fake 3D renders or low-quality SVG placeholders for hero/product proof.
- Do not mix mismatched image styles unless the reference intentionally does so.

## Cards And Product Modules

Compare:

- Card width/height ratio.
- Media area ratio.
- Text hierarchy.
- Hover behavior.
- Border/radius/shadow/background.
- Density and spacing between cards.

Fail when:

- The page becomes a generic grid of rounded cards.
- Cards repeat identical imagery or only swap headings.
- Card layout is used where the reference uses editorial bands, large media, or asymmetric composition.

## Buttons And CTAs

Compare:

- CTA location relative to headline/media.
- Primary vs secondary hierarchy.
- Size, padding, and label length.
- Icon use.
- Hover/focus behavior.
- CTA cadence across the page.

Fail when:

- CTA is visually detached from the decision point.
- Every section repeats identical button placement without reference evidence.

## Forms

Compare:

- Field order.
- Label style.
- Field width and grouping.
- Required-field indication.
- Button placement.
- Support copy and privacy/trust notes.
- Mobile field size.

Fail when:

- Form is decorative but unusable.
- Fields are too small or clipped on mobile.
- Submit CTA is hidden below excessive decoration.

## Difference Table Template

Use this table for every replication pass:

| Screen / section | Reference screenshot path | Target screenshot path | Difference type | Exact issue | Required correction | Status |
|---|---|---|---|---|---|---|
| Hero | ref.png | target.png | spacing | Reference has tighter media-to-title gap | Reduce gap from 72px to about 40px | pending |

Difference types:

- layout
- spacing
- typography
- image
- motion
- mobile
- content

## Forbidden Shortcuts

- No design from memory.
- No coding before reference and target-before screenshots exist.
- No generic template.
- No low-quality SVG hero/product placeholder.
- No fake metrics, ratings, badges, client logos, or testimonials.
- No repeated generic card grids.
- No template-style dark/green/black background unless directly supported by the reference.
- No "make it premium" claim without screenshot proof.
