# QA

Public QA utilities:

- `verify_sha256_manifest.py` checks a two-column SHA-256 manifest.
- `verify_zip_integrity.py` performs a complete CRC read of ZIP archives.
- `build_sha256_manifest.py` creates stable manifests for release staging.
- `compare_rendered_pages.py` checks clean-build PDF render parity pixel by
  pixel after Poppler rendering.

The controlled return package contains the run-specific QA report, replay
report, verification CSVs, page-render inspection record, and package hashes.
No submission-ready claim is made while the R6R7 global verification objects
remain absent.
