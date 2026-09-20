"""Write a stable SHA-256 manifest for selected files below a root."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    rows = []
    output = args.output.resolve()
    for pattern in args.paths:
        for path in args.root.glob(pattern):
            if path.is_file() and path.resolve() != output:
                relative = path.relative_to(args.root).as_posix()
                rows.append((relative, digest(path)))
    unique = sorted(dict(rows).items())
    args.output.write_text("".join(f"{value}  {relative}\n" for relative, value in unique), encoding="utf-8", newline="\n")
    print(f"wrote {len(unique)} entries to {args.output}")


if __name__ == "__main__":
    main()
