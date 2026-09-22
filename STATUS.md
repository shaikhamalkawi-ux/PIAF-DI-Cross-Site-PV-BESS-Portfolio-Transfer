# Project Status

## Active baseline
`PIAF_DI_PaperB_v29R3R6R6R8_JEST`

## Target
Journal of Energy Storage (JEST)

## Scientific status
**RETAIN R6R8 SCIENCE**

No new scientific version is justified unless a reproducible source/model/numerical error changes a locked result, evidence object, equation, or conclusion.

## Current closure stage
- Scientific/adversarial audit: PASS
- Reported-value arithmetic cross-check: PASS
- Norway/Boulder inherited branch: retained
- Dingle inherited branch: retained
- SlimPark manuscript/supplement integration: retained
- Historical v24 Norway independent verifier: PASS
- Dingle raw-source replay, all primary/sensitivity tables: PASS
- Dingle locked outer ZIP recovery and CRC: PASS
- SlimPark official raw-source replay, all primary/sensitivity tables: PASS
- Exact R6R7 named binaries: **RECOVERED / PASS**
- Exact original R6R8 complete delivery, source, and replication packages: **RECOVERED / PASS**
- Global candidate-budget machine replay: **PASS**
  - 1,317 target-budget rows reproduced
  - 507 dense-grid binary-MILP oracle checks PASS
  - 342 coarse-grid exact-enumeration checks PASS
  - maximum discrepancy = `4.440892098500626e-16` (reported as `4.44e-16`)
  - second clean replay produced byte-identical key CSV/JSON outputs
- Reconstructed/production-patched R6R8 clean build and render parity: PASS
- PDF references/fonts/all-page visual QA: PASS (zero Type 3 fonts)
- Final clean-room package integrity: PASS
- Scientific/reproducibility blockers: **NONE**
- Remaining closure items: return upload verification and independent/author-controlled submission review
- Public archive V04R2 component-licence correction: PASS
- V04R2 science parity, ZIP CRC, and complete SHA manifests: PASS
- V04R2 clean global replay: PASS (1,317 rows / 507 MILP / 342 enumeration)
- Zenodo record: **PUBLISHED**, record `22894501`, 22 September 2026
- Version DOI: [10.5281/zenodo.22894501](https://doi.org/10.5281/zenodo.22894501), public resolution PASS
- Zenodo uploaded ZIP MD5 matches local: PASS
- Zenodo publication: completed after the user's explicit confirmation for the approved draft
- V05 published-DOI-only rebuild: PASS, 32/12/44 pages, no Type 3 fonts, no overfull or undefined references/citations
- V05 source/numeric parity and all-page visual review: PASS
- Exact returned V05 source ZIP clean-extracted compile: PASS, pagewise text parity on all 44 pages
- JEST submission-ready label: pending independent review and author-controlled closure

## Recovered authoritative machine evidence
The aggregate 1,317 / 507 / 342 verification claim is backed by the exact retained historical archive:
`PIAF_DI_PaperB_v28_Controlled_Reproducibility_Archive.zip`

SHA-256:
`7c618af56e8978fadaa4c41ae680881d4544cef49b797c9481836ec55258953d`

Its internal SHA manifest passed 104/104 before execution. Its frozen development-portfolio and Norway-protocol hashes match the hashes printed in the current R6R8 Supplement.

## Canonical controlled workspace
Google Drive:
https://drive.google.com/drive/folders/125rI_3FaZh3rKqsxCnIazTk9npJGETPe

## V04R2 licence correction and publication

Published record: https://zenodo.org/records/22894501

Uploaded file: `R6R8_PUBLIC_REPRODUCIBILITY_LICENSE_CORRECTED_V04R2_20260922.zip`

- Size: 783,168 bytes
- SHA-256: `4017d7a3107832ef20deb54041dbc9663e73f3c774818e9c8978ff9264799e18`
- Local and Zenodo MD5: `bc875f22ebebe6aab7f7ae0d7a725958`
- ZIP CRC: PASS, 96 entries
- SHA manifest: PASS, 95/95 entries
- Public release manifest: PASS, 94/94 payload entries
- All 56 shared scientific CSV/JSON/PNG files are byte-identical to V04R1.
- All 16 shared Python files have identical abstract syntax trees.

The earlier separate-permission HOLD was overstated. CC BY-NC-SA 4.0 permits
compliant noncommercial sharing/adaptation; its attribution, NonCommercial and
ShareAlike conditions are preserved for the SlimPark-derived components.
The source's consultation request remains documented, but no consultation or
endorsement is claimed. Commercial downstream reuse is not pre-cleared.

The published record verifies the approved creator order: Ghassan Malkawi,
Ahmed Elsayed, Mohammed Alhagyan, Bakeel Hussein. The three licence labels
are accompanied by explicit component scopes. The authoritative V05 Main
and Supplement now include the published DOI; only their two archival
availability paragraphs changed. The other seven source files and all
scientific numerical tokens remain unchanged. R6R8 remains the baseline.

The Supplement's non-fatal line-193 glue-shrinkage diagnostic is reproduced
by the unchanged V05 baseline and documented in controlled QA. All affected
pages are visually clean; this is not a zero-warning claim. The original
funding/APC statement is preserved, not newly approved by Codex.
