#!/usr/bin/env python3
"""Generate a card thumbnail from a full-size portrait.

Usage:
    python tools/make-thumb.py characters/<slug>/<portrait>.png

Writes characters/<slug>/thumb.<ext> (480px wide, Lanczos), which is
the path the roster's `image` field should point at.
"""
import sys
from pathlib import Path

from PIL import Image

WIDTH = 480

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    im = Image.open(src)
    w, h = im.size
    if w > WIDTH:
        im = im.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
    dest = src.parent / f"thumb{src.suffix.lower()}"
    im.save(dest)
    print(f"{dest}  ({im.width}x{im.height})")

if __name__ == "__main__":
    main()
