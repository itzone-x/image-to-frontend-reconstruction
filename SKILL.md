---
name: image-to-frontend-reconstruction
description: Use when converting a visual reference image, AI-generated UI mockup, screenshot, or design comp into a high-fidelity frontend page, especially when matching icons, background motifs, spacing, cards, buttons, or mobile mini-program UI from raster images.
---

# Image To Frontend Reconstruction

## Overview

Turn a raster reference image into a faithful frontend implementation by combining native UI code with extracted image assets. Prefer deterministic asset extraction from the reference over hand-drawn approximations when exact icon, texture, or motif fidelity matters.

Use alongside framework-specific skills such as `frontend-design`, `frontend-patterns`, or platform skills when available.

## Core Rule

Separate the reference into three layers before coding:

1. **Native UI layer**: text, buttons, layout, input controls, navigation, and dynamic content.
2. **Extracted asset layer**: icons, decorative background motifs, textures, illustrations, logos, and shapes that are hard to recreate exactly.
3. **Code-drawn fallback layer**: simple lines, borders, shadows, dots, and shapes where fidelity risk is low.

Never hand-draw a high-detail reference icon or decorative motif if the source image file is available and the user wants high fidelity.

## Workflow

1. **Locate the source image**
   - Use the exact local file when provided.
   - Inspect dimensions with `file` and platform tools such as `sips`, `identify`, or PIL.
   - View the source at original resolution before estimating crop boxes.

2. **Reverse-engineer the UI spec**
   - Record palette, typography scale, spacing, radius, shadow, card hierarchy, CTA treatment, background motifs, and responsive assumptions.
   - Record which elements must stay single-line across devices: primary CTAs, secondary CTAs, short tags, eyebrow labels, chips, tab labels, compact card titles, counters, and icon+text controls.
   - Save a concise spec in the project when future pages will reuse the direction.

3. **Classify every visual element**
   - Keep all readable text as native frontend text.
   - Use source-derived image assets for icons, background motifs, product visuals, illustration fragments, generated textures, and marks.
   - Use CSS/WXSS/SVG only for low-detail primitives.

4. **Extract assets deterministically**
   - Create a project-local asset directory such as `miniprogram/assets/<page>/`, `src/assets/<page>/`, or the repo's existing equivalent.
   - Crop icons from the original image with stable pixel boxes or color-threshold detection.
   - For background motifs, prefer transparent PNG/WebP overlays that keep only decoration and remove text/card/button pixels.
   - Keep asset sizes small. Delete intermediate extraction files that are not referenced by the app.

5. **Implement the page**
   - Preserve existing behavior, routes, state, analytics, and copy unless the user requested changes.
   - Use extracted assets via native image tags/components.
   - Keep content and controls native for accessibility, localization, tap targets, and responsiveness.
   - Scope page-specific styling to the page. Avoid changing global tokens unless the new visual system applies broadly.
   - Treat the screenshot width as one breakpoint, not the whole design. Add responsive constraints for smaller and larger device presets before finishing.

6. **Lock the contract**
   - Add or update tests that verify critical copy, asset references, layout hooks, and the absence of old approximations.
   - Run targeted behavior tests, type checks, and formatting/diff checks.

7. **Report fidelity limits**
   - State whether assets were extracted from the reference or regenerated.
   - Call out any remaining approximation, such as font rendering differences, device chrome, or platform image scaling.

## Asset Extraction Guidance

Use `scripts/extract_reference_assets.py` when the task resembles a mobile page reference with repeated icon cards and background decoration. Read the script help first:

```bash
python3 <skill-dir>/scripts/extract_reference_assets.py --help
```

The script requires Pillow. If Pillow is unavailable, install it in the project environment or use platform image tools for simple crop-only extraction.

If crop boxes are obvious, pass them explicitly. If not, inspect the image and use color-threshold detection to identify icon bounds. Validate every output with an image viewer before wiring it into the page.

Prefer these outputs:

- `path-current.png`, `path-risk.png`, `path-free.png` style icon crops for repeated cards.
- `*-decor.png` transparent overlays for low-opacity background lines/stars/motifs.

Avoid these outputs:

- Full-page screenshot backgrounds with text removed by block fills.
- Assets containing source text, buttons, card borders, or shadows that should be native UI.
- AI-regenerated replacement icons when the original source image is available.

## Mini Program Notes

For WeChat mini-programs:

- Use `<image mode="aspectFill">` for circular icon crops.
- Use `<image mode="widthFix">` for transparent decorative overlays.
- Put assets under `miniprogram/assets/<page>/` and reference them as `/assets/<page>/file.png`.
- Keep WXML text native; do not bake Chinese copy into a background image.
- Replace WXSS-drawn high-detail illustrations with extracted assets when the reference is from GPT Image2 or another image model.
- Prevent native `<button>` text wrapping explicitly. Set `line-height`, `white-space: nowrap`, `box-sizing: border-box`, and `overflow: hidden` on single-line buttons.
- Do not place decorative icons inside CTA button flex flow with large fixed `gap` values. Center the label and absolutely position stars/arrows/badges so decoration cannot reduce text width.
- Add `white-space: nowrap` to single-line chips, eyebrow labels, compact card titles, segmented controls, and short CTA labels. Reduce letter spacing or font size at narrow breakpoints before allowing wrap.
- Use width budgets for dense rows: available row width minus padding, icon width, gaps, and trailing arrow must exceed the longest title's approximate rendered width. If not, reduce gaps/padding or add a breakpoint.
- Check at least a narrow iPhone preset, the reference preset, and a larger modern iPhone preset. In WeChat Developer Tools, include iPhone 12/13 and iPhone 15 Pro when the page targets iOS mini-program users.

## Common Mistakes

- **Mistake: hand-drawing detailed icons from a generated mock.** Fix by cropping from the source image and deleting the CSS illustration.
- **Mistake: using the entire mockup as a page background.** Fix by extracting only decoration into transparent overlays and rendering UI natively.
- **Mistake: leaving content residue in background assets.** Fix by masking all text/card/button areas and checking the transparent overlay at original size.
- **Mistake: changing product copy while matching visuals.** Fix by preserving existing copy and behavior unless explicitly requested.
- **Mistake: matching only the reference screenshot size.** Fix by checking larger and smaller phone presets and locking single-line UI elements with explicit nowrap, line-height, and width budgets.
- **Mistake: using fixed flex gaps inside buttons.** Fix by absolutely positioning decorative stars/arrows and centering the text label independently.
- **Mistake: validating only by code tests.** Fix by inspecting generated assets and, when possible, running a visual preview or screenshot pass.
