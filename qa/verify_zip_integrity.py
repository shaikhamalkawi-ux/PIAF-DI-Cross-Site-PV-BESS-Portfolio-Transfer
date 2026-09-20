"""Run a complete CRC read over one or more ZIP archives."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archives", nargs="+", type=Path)
    args = parser.parse_args()
    failures = 0
    for archive_path in args.archives:
        try:
            with zipfile.ZipFile(archive_path) as archive:
                bad = archive.testzip()
                status = "PASS" if bad is None else f"FAIL:{bad}"
                failures += int(bad is not None)
                print(f"{status}\t{len(archive.infolist())} entries\t{archive_path}")
        except Exception as error:
            failures += 1
            print(f"FAIL\t{archive_path}\t{error}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
