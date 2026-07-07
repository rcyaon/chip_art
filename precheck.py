#!/usr/bin/env python3
"""
Usage:
    python3 precheck_chip_art.py input.png
    python3 precheck_chip_art.py input.png --max-metal 4 --out annotated.png

Exit code: 0 = no diagonal-touch issues found, 1 = issues found, 2 = bad input.
"""

import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw

BACKGROUND = 0
MIN_METAL = 0
MAX_METAL_DEFAULT = 4


def quantize(image_in, max_metal):
    image = Image.open(image_in).convert("L").transpose(Image.FLIP_TOP_BOTTOM)
    pixels = np.asarray(image, dtype=np.uint64)
    pmin, pmax = pixels.min(), pixels.max()
    if pmax == pmin:
        print("Warning: image is a single flat color; chip_art.py would crash "
              "on this input (division by zero). Add some contrast.")
        layer = np.full(pixels.shape, MIN_METAL, dtype=np.uint8)
        return layer, image.size
    scaled = (pixels - pmin) * (max_metal - MIN_METAL + 0.49) / (pmax - pmin) + MIN_METAL
    return np.uint8(scaled), image.size


def find_diagonal_touches(layer):
    h, w = layer.shape
    issues = []
    for y in range(h - 1):
        for x in range(w - 1):
            a = layer[y, x]        # top-left
            b = layer[y, x + 1]    # top-right
            c = layer[y + 1, x]    # bottom-left
            d = layer[y + 1, x + 1]  # bottom-right

            if a != BACKGROUND and a == d and b != a and c != a:
                issues.append((x, y, x + 1, y + 1, int(a)))
            if b != BACKGROUND and b == c and a != b and d != b:
                issues.append((x + 1, y, x, y + 1, int(b)))
    return issues


def annotate(image_in, issues, out_path):
    image = Image.open(image_in).convert("RGB")
    draw = ImageDraw.Draw(image)
    h = image.size[1]
    for (x1, y1, x2, y2, _metal) in issues:
        fy1 = h - 1 - y1
        fy2 = h - 1 - y2
        draw.line([(x1, fy1), (x2, fy2)], fill=(255, 0, 0), width=1)
        draw.ellipse([x1 - 1, fy1 - 1, x1 + 1, fy1 + 1], outline=(255, 0, 0))
        draw.ellipse([x2 - 1, fy2 - 1, x2 + 1, fy2 + 1], outline=(255, 0, 0))
    image.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image_in", help="Input PNG/bitmap, same file you'd pass to chip_art.py")
    ap.add_argument("--max-metal", type=int, default=MAX_METAL_DEFAULT,
                     help="Must match MAX_METAL in chip_art.py (default 4)")
    ap.add_argument("--out", default=None,
                     help="Save an annotated copy of the image marking corner-touch pixels in red")
    args = ap.parse_args()

    try:
        layer, size = quantize(args.image_in, args.max_metal)
    except FileNotFoundError:
        print(f"Could not open {args.image_in}")
        sys.exit(2)

    issues = find_diagonal_touches(layer)

    print(f"Image size: {size[0]}x{size[1]} px, metal layers 1..{args.max_metal}")
    if not issues:
        print("PASS: no diagonal corner-touch pixels found for any metal layer.")
        print("(This only rules out the specific failure mode chip_art's README "
              "warns about — still run full DRC before tapeout.)")
        sys.exit(0)

    print(f"FOUND {len(issues)} diagonal corner-touch pixel pair(s):")
    by_metal = {}
    for (x1, y1, x2, y2, metal) in issues:
        by_metal.setdefault(metal, []).append((x1, y1, x2, y2))
    for metal, pts in sorted(by_metal.items()):
        preview = ", ".join(f"({x1},{y1})-({x2},{y2})" for x1, y1, x2, y2 in pts[:5])
        more = "" if len(pts) <= 5 else f" ... +{len(pts) - 5} more"
        print(f"  metal{metal}: {len(pts)} location(s): {preview}{more}")

    print("\nFix: change one of the two 'bridge' pixels adjacent to each flagged "
          "corner pair to match the diagonal metal (connects them into one solid "
          "shape) or to background (removes the touch entirely).")

    if args.out:
        annotate(args.image_in, issues, args.out)
        print(f"\nAnnotated image saved to: {args.out} (red = corner-touch pixels)")

    sys.exit(1)


if __name__ == "__main__":
    main()
