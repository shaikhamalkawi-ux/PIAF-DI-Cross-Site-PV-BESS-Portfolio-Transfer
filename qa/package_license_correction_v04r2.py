"""Build the V04R2 licence-only correction, preserving all scientific payloads."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path, PurePosixPath
import zipfile


SOURCE_SHA256 = "b8e21ad264e27369e869c308da03ac26619bbd9243d0bf19dbbcb1fa3d2be07d"
DATE = (2026, 9, 22, 0, 0, 0)
MIXED_CSV = {
    "r6r8_current/code/reproducibility/reference/definitions/headline_reported_values.csv":
        "Rows where family=SlimPark all9 native: CC-BY-NC-SA-4.0; other author-owned contributions: CC-BY-4.0",
    "r6r8_current/control_records/R6R8_PERCENTILE_INTEGER_COMPATIBILITY.csv":
        "Rows where case starts SlimPark: CC-BY-NC-SA-4.0; other author-owned contributions: CC-BY-4.0",
}
ARITHMETIC = "r6r8_current/control_records/verify_reported_arithmetic.py"
METADATA_EDITS = {
    "README.md", "LICENSES.md", "THIRD_PARTY_DATA_BOUNDARY.md", "CITATION.cff",
    "licenses/LICENSE_DOCS_DERIVED_CC_BY_4_0.txt",
    "r6r8_current/README_REPLAY.md",
    "qa/ZENODO_PUBLIC_SAFETY_AUDIT_V04R1_20260921.md",
}
EXTRAS = {
    "licenses/SLIMPARK_ATTRIBUTION_AND_NOTICE.md",
    "licenses/LICENSE_SLIMPARK_CC_BY_NC_SA_4_0.txt",
    "qa/LICENSE_CORRECTION_V04R2_20260922.md",
    "qa/VALIDATED_ENVIRONMENT_V04R2.txt",
    "requirements-core.txt",
}
GENERATED = {
    "PUBLIC_RELEASE_MANIFEST.csv", "SHA256SUMS.txt", "COMPONENT_LICENSE_MAP.csv",
    "qa/V04R2_LICENSE_AND_CONTENT_QA.json", "qa/V04R2_SCIENTIFIC_PAYLOAD_PARITY.csv",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--output-zip", type=Path, required=True)
    args = parser.parse_args()
    root = args.package_dir.resolve()
    assert root.is_dir(), "Prepared package directory is missing"
    assert not args.output_zip.exists(), "Refusing to overwrite a release archive"
    assert sha(args.source_zip.read_bytes()) == SOURCE_SHA256, "Wrong source archive"
    with zipfile.ZipFile(args.source_zip) as source:
        assert source.testzip() is None
        original = {n: source.read(n) for n in source.namelist() if not n.endswith("/")}
    old_manifest = {
        row["path"]: row for row in csv.DictReader(io.StringIO(original["PUBLIC_RELEASE_MANIFEST.csv"].decode("utf-8-sig")))
    }
    names = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    assert not (names - set(original) - EXTRAS - GENERATED), "Unexpected added files"
    assert set(original) <= names, "Original payload was removed"
    assert EXTRAS <= names, "Required licence/environment files missing"

    parity = []
    changed_metadata = []
    for name, old in sorted(original.items()):
        new = (root / name).read_bytes()
        if name in {"PUBLIC_RELEASE_MANIFEST.csv", "SHA256SUMS.txt"}:
            continue
        if name in METADATA_EDITS:
            if new != old:
                changed_metadata.append(name)
            continue
        if name == ARITHMETIC:
            assert ast.dump(ast.parse(new.decode("utf-8"))) == ast.dump(ast.parse(old.decode("utf-8"))), "Arithmetic logic changed"
            parity.append({"path": name, "comparison": "AST identical; licence comments only", "status": "PASS", "original_sha256": sha(old), "corrected_sha256": sha(new)})
        else:
            assert new == old, f"Scientific payload changed: {name}"
            parity.append({"path": name, "comparison": "byte-identical", "status": "PASS", "original_sha256": sha(old), "corrected_sha256": sha(new)})

    direct = {n for n in old_manifest if ("/reference/derived/slimpark_" in n or "/replay_output/slimpark/" in n)}
    assert len(direct) == 12, f"Expected twelve SlimPark direct files, found {len(direct)}"
    for name in sorted(names - {"SHA256SUMS.txt", "PUBLIC_RELEASE_MANIFEST.csv"}):
        rel = PurePosixPath(name)
        assert not rel.is_absolute() and ".." not in rel.parts and ":" not in name
        assert rel.suffix.lower() not in {".zip", ".7z", ".rar", ".xlsx", ".pyc", ".aux", ".log"}, f"Disallowed payload: {name}"
        data = (root / name).read_bytes()
        assert not data.startswith((b"PK\x03\x04", b"7z\xbc\xaf\x27\x1c", b"Rar!")), f"Nested archive: {name}"
        if rel.suffix.lower() in {".md", ".txt", ".csv", ".json", ".py", ".cff"}:
            content = data.decode("utf-8-sig")
            assert not re.search(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)", content), f"Private path: {name}"
            assert not re.search(r"\b(?:sessionId|userId|driverId|reportedZip)\b", content), f"Source identifier: {name}"
            assert not re.search(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}|Bearer\s+[A-Za-z0-9._-]{24,})", content), f"Possible secret: {name}"

    scopes = []
    for name in sorted(direct):
        scopes.append({"path": name, "licence": "CC-BY-NC-SA-4.0", "scope": "SlimPark-derived output; applicable copyright/database rights", "attribution": "licenses/SLIMPARK_ATTRIBUTION_AND_NOTICE.md"})
    for name, scope in MIXED_CSV.items():
        scopes.append({"path": name, "licence": "CC-BY-4.0 AND CC-BY-NC-SA-4.0", "scope": scope, "attribution": "licenses/SLIMPARK_ATTRIBUTION_AND_NOTICE.md"})
    scopes.append({"path": ARITHMETIC, "licence": "MIT AND CC-BY-NC-SA-4.0", "scope": "Original code: MIT; checks tuples (126,120,95.238), (12650,12271,97.004), (12650,12337,97.526): CC-BY-NC-SA-4.0 where rights apply", "attribution": "licenses/SLIMPARK_ATTRIBUTION_AND_NOTICE.md"})
    write_csv(root / "COMPONENT_LICENSE_MAP.csv", ["path", "licence", "scope", "attribution"], scopes)
    write_csv(root / "qa/V04R2_SCIENTIFIC_PAYLOAD_PARITY.csv", ["path", "comparison", "status", "original_sha256", "corrected_sha256"], parity)
    report = {
        "status": "PASS", "version": "V04R2", "date": "2026-09-22",
        "source_archive_sha256": SOURCE_SHA256,
        "direct_slimpark_files_cc_by_nc_sa": len(direct),
        "mixed_csv_files_with_scoped_licenses": len(MIXED_CSV),
        "mixed_code_files_with_scoped_licenses": 1,
        "byte_identical_original_payload_files": sum(x["comparison"] == "byte-identical" for x in parity),
        "arithmetic_ast_identical": True,
        "changed_metadata_files": changed_metadata,
        "new_files": sorted(EXTRAS),
        "private_path_secret_identifier_nested_archive_scan": "PASS",
        "scientific_values_figures_and_computations_changed": False,
        "consultation_requested_by_source": True,
        "consultation_or_extra_permission_claimed": False,
        "licensing_basis": "Existing CC-BY-NC-SA-4.0 grant; retain NC, SA, attribution, modification and warranty notices; component scope only",
    }
    (root / "qa/V04R2_LICENSE_AND_CONTENT_QA.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    files = sorted(p for p in root.rglob("*") if p.is_file())
    manifest = []
    for p in files:
        name = p.relative_to(root).as_posix()
        if name in {"PUBLIC_RELEASE_MANIFEST.csv", "SHA256SUMS.txt"}:
            continue
        entry = old_manifest.get(name, {"class": "documentation/metadata", "licence": "CC-BY-4.0"})
        licence = entry["licence"]
        if name in direct:
            licence = "CC-BY-NC-SA-4.0"
        elif name in MIXED_CSV:
            licence = "CC-BY-4.0 AND CC-BY-NC-SA-4.0"
        elif name == ARITHMETIC:
            licence = "MIT AND CC-BY-NC-SA-4.0"
        scope = next((row["scope"] for row in scopes if row["path"] == name), "Author-owned contribution only; third-party rights and public-domain facts unaffected")
        manifest.append({"path": name, "bytes": p.stat().st_size, "sha256": sha(p.read_bytes()), "class": entry["class"], "licence": licence, "licence_scope": scope})
    write_csv(root / "PUBLIC_RELEASE_MANIFEST.csv", ["path", "bytes", "sha256", "class", "licence", "licence_scope"], manifest)
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
    (root / "SHA256SUMS.txt").write_text("".join(f"{sha(p.read_bytes())}  {p.relative_to(root).as_posix()}\n" for p in files), encoding="utf-8")
    args.output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output_zip, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(p.relative_to(root).as_posix(), date_time=DATE)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, p.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(args.output_zip) as archive:
        assert archive.testzip() is None
        for line in archive.read("SHA256SUMS.txt").decode().splitlines():
            expected, name = line.split("  ", 1)
            assert sha(archive.read(name)) == expected, name
        for row in csv.DictReader(io.StringIO(archive.read("PUBLIC_RELEASE_MANIFEST.csv").decode())):
            data = archive.read(row["path"])
            assert len(data) == int(row["bytes"]) and sha(data) == row["sha256"]
        print(json.dumps({"status": "PASS", "zip": args.output_zip.name, "bytes": args.output_zip.stat().st_size, "sha256": sha(args.output_zip.read_bytes()), "md5": hashlib.md5(args.output_zip.read_bytes()).hexdigest(), "zip_files": len(archive.namelist()), "payload_manifest_rows": len(manifest), "source_payload_parity_checks": len(parity)}, indent=2))


if __name__ == "__main__":
    main()
