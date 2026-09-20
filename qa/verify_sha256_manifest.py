"""Verify a two-column SHA-256 manifest rooted at a chosen directory."""

from __future__ import annotations

import argparse
from pathlib import Path

from hashlib import sha256


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    failures = []
    count = 0
    for raw in args.manifest.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        expected, relative = line.split(maxsplit=1)
        relative = relative.lstrip("* ").replace("/", "\\")
        path = args.root / relative
        actual = digest(path) if path.is_file() else "MISSING"
        count += 1
        if actual.lower() != expected.lower():
            failures.append((relative, expected, actual))
    print(f"files={count}; failures={len(failures)}")
    for failure in failures:
        print("FAIL", *failure)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
