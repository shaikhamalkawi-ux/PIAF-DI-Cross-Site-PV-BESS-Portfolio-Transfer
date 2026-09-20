"""Compare two rendered-PDF page directories pixel for pixel."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    left = sorted(args.reference.glob("page-*.png"))
    right = sorted(args.candidate.glob("page-*.png"))
    if len(left) != len(right):
        raise SystemExit(f"page-count mismatch: {len(left)} != {len(right)}")
    differing = 0
    max_channel_difference = 0
    different_pixels = 0
    for expected, actual in zip(left, right):
        a = np.asarray(Image.open(expected).convert("RGB"), dtype=np.int16)
        b = np.asarray(Image.open(actual).convert("RGB"), dtype=np.int16)
        if a.shape != b.shape:
            raise SystemExit(f"shape mismatch: {expected.name}")
        delta = np.abs(a - b)
        if np.any(delta):
            differing += 1
            max_channel_difference = max(max_channel_difference, int(delta.max()))
            different_pixels += int(np.any(delta, axis=2).sum())
    print(f"pages={len(left)}; differing_pages={differing}; differing_pixels={different_pixels}; max_channel_difference={max_channel_difference}")
    raise SystemExit(1 if differing else 0)


if __name__ == "__main__":
    main()
