# PIAF-DI Cross-Site PV-BESS Portfolio Transfer

Working repository for the PIAF-DI Paper B research workflow.

## Paper
**Cross-Site Reuse of Compact PV-Battery Candidate Portfolios: Representation Limits and Transfer-Selection Loss**

Target journal: **Journal of Energy Storage (JEST)**

## Active scientific baseline
`PIAF_DI_PaperB_v29R3R6R6R8_JEST`

Current decision: **retain R6R8 science**. Do not open a new scientific version unless a reproducible source/model/numerical error changes a locked scientific result or conclusion.

## Working model
- Google Drive is the controlled file workspace for manuscripts, packages, large data, and Codex returns.
- GitHub is the version-controlled code, instructions, manifests, QA, and reproducibility layer.
- Codex should read `CODEX_INSTRUCTIONS.md` before making changes.
- ChatGPT reviews Codex returns before anything is labelled submission-ready.

## Google Drive workspace
Private project workspace:
`PIAF_DI_PaperB_R6R8_CODEX_WORKSPACE`

Folder:
https://drive.google.com/drive/folders/125rI_3FaZh3rKqsxCnIazTk9npJGETPe

## Important
This repository is currently **public**. Do not commit unpublished manuscript PDFs, restricted/raw datasets, author-private metadata, or controlled source archives here until the repository visibility is changed or the authors explicitly approve public release.

Public-safe reproducibility material can be added after audit and source-licence review.

## Clean-room closure status

The public-safe Dingle and SlimPark replay implementations, locked derived
tables, source manifests, figure builder, and QA utilities are now present on
`codex/r6r8-clean-room`. Both measured-input branches replay successfully and
the reconstructed manuscript source passes clean-build/render QA.

The controlled return remains **HOLD for submission** because the historical
R6R7 binaries and the machine objects behind the aggregate 1,317/507/342
verification claim were not available. See `STATUS.md` and
`data_manifest/MISSING_LINEAGE.md`. No Zenodo release has been created.
