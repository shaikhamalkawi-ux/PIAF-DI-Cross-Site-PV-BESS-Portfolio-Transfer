# Zenodo Release Plan

Zenodo is recommended for the **final reproducibility release**, but it is not the next task.

## Order of operations

1. Codex completes the R6R8 clean-room replay and package reconstruction.
2. Codex writes all binary/source outputs to the Google Drive `03_CODEX_RETURN_INBOX`.
3. Codex commits public-safe code/manifests/reports to `codex/r6r8-clean-room`.
4. ChatGPT independently audits the replay, hashes, source provenance, build, and package QA.
5. Resolve any HOLD/STOP item.
6. Merge the reviewed public-safe branch to `main`.
7. Prepare a clean archival release containing only redistributable material.
8. Tag the reviewed release, e.g. `v1.0.0-reproducibility`.
9. Deposit that exact release to Zenodo and obtain a permanent DOI.
10. Insert the DOI into:
   - manuscript Data Availability statement;
   - repository README;
   - final reproducibility manifest;
   - citation metadata.
11. Re-run final manuscript/package QA after DOI insertion.

## What should go to Zenodo

Preferred:
- public-safe source code;
- environment/requirements;
- exact verification scripts;
- public-safe derived candidate/verification tables;
- manifests and SHA-256 checksums;
- source-provenance/acquisition instructions;
- final QA report;
- citation metadata;
- optionally the accepted/final manuscript version if journal policy permits.

Do not redistribute third-party raw datasets unless their licence explicitly permits it. For non-redistributable public data, archive the DOI/source identity, acquisition procedure, hashes, and validation checks instead.

## Current status

**ZENODO: WAIT**

Do not mint the final DOI until the R6R8 replay and independent ChatGPT audit are closed. This avoids assigning the permanent DOI to an unverified or superseded package.
