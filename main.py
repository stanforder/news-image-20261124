#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261124.

Writes the pre-rendered 1024x1024 PNG of Tuesday 24 November 2026's
world news to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
The image bytes are stored in this repository as entry.png.b64 (a
single line of base64) and are decoded verbatim: the program is
deterministic by construction (no network, no randomness, no time),
so two runs write identical bytes.

The image itself is drawn by draw_entry.py (PIL) from the verified
29 stories in the research notes; this file only reproduces it.
"""
import base64
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png.b64"), "rb") as f:
        data = base64.b64decode(f.read().strip())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"Wrote {out_path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
