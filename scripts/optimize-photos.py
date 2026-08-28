#!/usr/bin/env python3
"""Turn camera/scanner originals into web-deliverable photographs.

Reads from _masters/photos/ (git-ignored, never published) and writes to
assets/photos/. Originals stay untouched on disk, so this is always re-runnable
and the repository only ever carries the web copies.

Three things matter here beyond resizing:

  progressive=True  A baseline JPEG paints top-down as it downloads, so a large
                    photograph on a slow connection looks like it is not filling
                    its frame. Progressive paints the whole image immediately and
                    then sharpens, which reads as "loading" rather than "broken".

  LANCZOS           Downscaling a film scan is where most of the visible quality
                    is won or lost; the default filter softens grain into mush.

  quality 84 / 4:2:0
                    Measured against a lossless downscale of the masters, this
                    holds SSIM ~0.93 on grain-heavy film at roughly 700KB-1MB per
                    photograph, which matches the density of the existing set.
                    Grain punishes SSIM harder than it punishes the eye.

Usage:  python3 scripts/optimize-photos.py [--force]
"""

import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_masters", "photos")
OUT = os.path.join(ROOT, "assets", "photos")

MAX_EDGE = 2200
QUALITY = 84
SUBSAMPLING = 2  # 4:2:0

def web_name(stem: str) -> str:
    """Cinestill400D030 -> cinestill400d-030, GC003 -> gc-003.

    Keeps the film-stock convention the photographs already use; just makes it
    URL-safe and consistent. Anything that does not end in digits is simply
    lowercased and hyphenated.
    """
    m = re.match(r"^(.*?)[\s_-]*(\d{2,4})$", stem)
    if m and m.group(1):
        stem = f"{m.group(1)}-{m.group(2)}"
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("-")
    return stem.lower()

def main() -> int:
    force = "--force" in sys.argv
    if not os.path.isdir(SRC):
        sys.exit(f"missing {os.path.relpath(SRC, ROOT)} — put the originals there first")
    os.makedirs(OUT, exist_ok=True)

    names = sorted(f for f in os.listdir(SRC)
                   if f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")))
    if not names:
        print("nothing to do")
        return 0

    total_in = total_out = 0
    for name in names:
        src = os.path.join(SRC, name)
        dest_name = web_name(os.path.splitext(name)[0]) + ".jpg"
        dest = os.path.join(OUT, dest_name)
        if os.path.exists(dest) and not force:
            print(f"  skip   {dest_name}  (exists; --force to redo)")
            continue

        with Image.open(src) as im:
            im = im.convert("RGB")
            before = im.size
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            im.save(dest, "JPEG", quality=QUALITY, progressive=True,
                    optimize=True, subsampling=SUBSAMPLING)

        a, b = os.path.getsize(src), os.path.getsize(dest)
        total_in += a
        total_out += b
        print(f"  ok     {dest_name:26s} {before[0]}x{before[1]} -> "
              f"{im.size[0]}x{im.size[1]}   {a/1048576:6.1f} MB -> {b/1024:6.0f} KB")

    if total_in:
        print(f"\n  {total_in/1048576:.0f} MB of originals -> "
              f"{total_out/1048576:.1f} MB published "
              f"({100 - total_out/total_in*100:.0f}% smaller)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
