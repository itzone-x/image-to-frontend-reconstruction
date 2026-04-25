#!/usr/bin/env python3
"""Extract UI assets from a raster reference image.

This utility intentionally stays small and explicit. Use crop boxes for exact
assets, and use the transparent-decor mode for faint background motifs after
masking native UI regions.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image


Box = tuple[int, int, int, int]


def parse_box(value: str) -> tuple[str, Box]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("box must use name=x1,y1,x2,y2")
    name, raw_box = value.split("=", 1)
    parts = raw_box.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box must have four coordinates")
    try:
        box = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("coordinates must be integers") from exc
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError("box must have positive width and height")
    return name, box  # type: ignore[return-value]


def parse_mask(value: str) -> Box:
    parts = value.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("mask must use x1,y1,x2,y2")
    try:
        box = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("mask coordinates must be integers") from exc
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError("mask must have positive width and height")
    return box  # type: ignore[return-value]


def base_color(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
    tx = x / max(1, width - 1)
    ty = y / max(1, height - 1)
    return (
        round(250 - 5 * tx - 1 * ty),
        round(250 - 1 * tx - 1 * ty),
        round(248 - 2 * tx - 1 * ty),
    )


def is_masked(x: int, y: int, masks: Iterable[Box]) -> bool:
    return any(left <= x < right and top <= y < bottom for left, top, right, bottom in masks)


def crop_assets(image: Image.Image, output_dir: Path, boxes: list[tuple[str, Box]]) -> None:
    for name, box in boxes:
        filename = name if Path(name).suffix else f"{name}.png"
        image.crop(box).save(output_dir / filename, optimize=True)


def extract_decor(image: Image.Image, output: Path, masks: list[Box]) -> None:
    rgb = image.convert("RGB")
    width, height = rgb.size
    source = rgb.load()
    result = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    target = result.load()

    for y in range(height):
        for x in range(width):
            if is_masked(x, y, masks):
                continue
            r, g, b = source[x, y]
            br, bg, bb = base_color(x, y, width, height)
            dist = (abs(r - br) + abs(g - bg) + abs(b - bb)) / 3
            saturated_green = g > r + 16 and g > b + 6 and r < 190 and b < 180
            pale_green_line = (
                r > 205 and g > 212 and b > 205 and g >= r + 1 and g >= b + 3 and dist > 2.6
            )
            if saturated_green:
                alpha = min(230, 100 + int(dist * 8))
            elif pale_green_line:
                alpha = min(68, 16 + int(dist * 9))
            else:
                continue
            target[x, y] = (r, g, b, alpha)

    result.save(output, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Reference image path")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for extracted assets")
    parser.add_argument(
        "--crop",
        action="append",
        default=[],
        type=parse_box,
        help="Crop asset as name=x1,y1,x2,y2. Repeat for multiple assets.",
    )
    parser.add_argument("--decor-output", type=Path, help="Optional transparent decoration output path")
    parser.add_argument(
        "--mask",
        action="append",
        default=[],
        type=parse_mask,
        help="Mask native UI region for decor extraction as x1,y1,x2,y2. Repeat as needed.",
    )
    args = parser.parse_args()

    image = Image.open(args.source)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.crop:
        crop_assets(image, args.out_dir, args.crop)
    if args.decor_output:
        extract_decor(image, args.decor_output, args.mask)


if __name__ == "__main__":
    main()
