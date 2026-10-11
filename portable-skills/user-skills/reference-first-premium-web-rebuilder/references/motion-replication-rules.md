# Motion Replication Rules

## Goal

Replicate useful motion rhythm from the reference, then adapt it for commercial clarity. Do not add random fade-ins to every section.

## Capture Reference Motion

Capture motion by scrolling and interacting with the reference page. Record:

- Trigger: load, scroll, hover, drag, click, menu open, sticky transition, viewport entry.
- Duration.
- Easing.
- Stagger.
- Transform: translate, scale, rotate, skew.
- Opacity.
- Clip/mask.
- Blur or filter.
- Scroll distance before activation.
- Whether the animation is one-time or repeated.
- Desktop vs mobile differences.

Use screen recordings when screenshots cannot show the behavior.

Record at least one before/after still for important motion states: menu open, sticky header after scroll, hover card state, gallery transition, pinned section, masked reveal, or form interaction. If motion cannot be reproduced exactly, document the simplified commercial version in the difference table.

## What To Reproduce

Reproduce only motion that helps:

- Reveal hierarchy.
- Guide attention.
- Show product or process detail.
- Improve navigation confidence.
- Add premium rhythm without blocking comprehension.

Translate portfolio motion into commercial motion:

- Keep rhythm and polish.
- Reduce friction.
- Keep CTAs and forms visible.
- Avoid hiding key product/capability information behind gestures.
- Replace abstract effects with product/process/proof staging.

## Timing Rules

Compare:

- First reveal delay.
- Transition duration.
- Easing curve feel.
- Stagger interval.
- Scroll trigger position.
- Enter/exit direction.
- Mask/clip shape and speed.
- Hover transition duration.

Fail when:

- Motion hides content.
- Motion creates layout shift.
- Motion blocks forms or CTAs.
- Motion causes horizontal overflow.
- Motion is slow enough to frustrate commercial users.
- Every section uses the same fade-in without reference evidence.

## Mobile And Reduced Motion

Mobile:

- Reduce heavy transforms.
- Avoid hover-only interactions.
- Keep sticky elements from covering content.
- Prefer simple opacity/transform reveals if the reference motion is too heavy for mobile.

Reduced motion:

- Use `prefers-reduced-motion` for substantial animation.
- Provide non-motion access to all content.
- Avoid flashing or rapid repeated motion.

## Verification

Before handoff:

- Scroll the page on desktop and mobile.
- Test hover/focus states.
- Test menus, sticky headers, galleries, and forms.
- Test with reduced motion enabled or inspect the `prefers-reduced-motion` fallback when substantial animation exists.
- Confirm no animation overlaps or clips text.
- Confirm no motion causes horizontal overflow.
- Confirm image/video/motion panels are not blank.
- Record any intentionally simplified motion in the difference table.
