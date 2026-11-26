#!/usr/bin/env python3
"""Entry program for news-image-20261125.

Copies the committed front-page image (entry.png, the world news of
Wednesday 25 November 2026) to the output directory, byte for byte.
Standard library only; no network, nothing generated at run time.

Usage:
    python3 main.py
Writes entry.png to $MAKEFUN_OUTPUT_DIR when set, else /output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    print(dest)
    print(size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
