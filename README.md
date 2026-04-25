# Image to Frontend Reconstruction

`image-to-frontend-reconstruction` is a Codex/Claude skill for rebuilding frontend pages from raster UI references, AI-generated mockups, screenshots, and design comps with higher visual fidelity.

The core idea is simple: do not ask the model to redraw everything from memory. Split the reference into native UI, extracted image assets, and low-risk CSS primitives. Text, layout, buttons, and controls stay native. Detailed icons, decorative motifs, textures, and generated illustration fragments are cropped from the source image when fidelity matters.

## Why This Exists

Tools such as Stitch, Figma, and GPT Image can produce polished product mockups quickly. The hard part often starts after that: turning the image into a real frontend page.

For non-frontend builders, there may be no designer available to slice assets. For frontend agents, direct image-to-code reconstruction is still easy to get wrong: the model may "paint" a similar page, but it is not truly slicing the design. Small icon details, spacing, background motifs, and button treatment drift quickly.

This skill captures a practical reconstruction workflow inspired by UI slicing and frontend implementation:

- inspect the reference at original resolution;
- reverse-engineer typography, spacing, color, radius, and hierarchy;
- classify each visual element before coding;
- extract hard-to-recreate assets from the source image;
- render text, controls, and layout natively;
- verify the page across realistic viewport sizes.

In the author's own experiments, this approach reached roughly 90% fidelity on many consumer-facing mockups, and even higher fidelity on some backend/admin interface references where the design system is more regular.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── extract_reference_assets.py
├── docs/
│   └── wechat-article.md
├── requirements.txt
└── LICENSE
```

## Install

For Codex:

```bash
mkdir -p ~/.codex/skills/image-to-frontend-reconstruction
cp -R SKILL.md agents scripts ~/.codex/skills/image-to-frontend-reconstruction/
```

For Claude Code or Claude Desktop skill setups, copy the same files into the matching skill directory used by your environment.

## Use

Ask your coding agent to use this skill when implementing from a visual reference:

```text
Use image-to-frontend-reconstruction to rebuild this page from /path/to/reference.png.
Extract detailed icons and decorative motifs from the image, but keep text and controls native.
```

The included helper can crop explicit image boxes or create a transparent decoration overlay:

```bash
python3 scripts/extract_reference_assets.py \
  --source reference.png \
  --out-dir src/assets/home \
  --crop hero-icon=120,180,220,280 \
  --decor-output src/assets/home/background-decor.png \
  --mask 0,120,390,640
```

The script requires Pillow:

```bash
pip install -r requirements.txt
```

## What This Skill Is Not

This is not a magic "screenshot to perfect app" button. It is a workflow guardrail.

It works best when the original reference image is available, the target frontend project can serve local assets, and someone can visually inspect the result. Font rendering, platform controls, responsive behavior, and image scaling can still create differences that need human review.

## License

MIT
