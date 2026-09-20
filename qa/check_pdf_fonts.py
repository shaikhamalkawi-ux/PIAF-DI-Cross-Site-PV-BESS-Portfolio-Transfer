"""Fail when a PDF contains Type 3 or unembedded fonts."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def check(path: Path) -> None:
    result = subprocess.run(
        ["pdffonts", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = result.stdout.splitlines()[2:]
    failures: list[str] = []
    for row in rows:
        if not row.strip():
            continue
        lower = row.lower()
        if "type 3" in lower:
            failures.append(f"Type 3: {row}")
        fields = row.split()
        if len(fields) >= 5 and fields[-5].lower() != "yes":
            failures.append(f"not embedded: {row}")
    if failures:
        raise SystemExit(f"{path}: FAIL\n" + "\n".join(failures))
    print(f"{path}: PASS ({len(rows)} font records; embedded; zero Type 3)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.pdf:
        check(path)


if __name__ == "__main__":
    main()
