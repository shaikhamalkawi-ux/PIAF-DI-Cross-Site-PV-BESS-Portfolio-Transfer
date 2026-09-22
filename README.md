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

The historical R6R7/R6R8 lineage and the machine objects behind the aggregate
1,317/507/342 verification claim have been recovered and independently
replayed. See `STATUS.md` for the current closure evidence; older missing-lineage
reports are historical. The exact locked Dingle outer ZIP also passes its
source-integrity gate. The rebuilt manuscript has no Type 3 fonts.

The V04R2 public archive corrects component licensing without changing locked
scientific values or executable calculations. MIT applies to original software,
CC BY 4.0 to applicable author-owned documentation and contributions, and
CC BY-NC-SA 4.0 to the scoped SlimPark-derived material. These are component
licences, not alternatives for the entire package. See `LICENSES.md`.

The approved archive was **published on 22 September 2026** on
[Zenodo](https://zenodo.org/records/22894501). Its version DOI
[10.5281/zenodo.22894501](https://doi.org/10.5281/zenodo.22894501) resolves to
the public record. See `CITATION.cff` for the archive citation. The deposited
V04R2 reproducibility archive supports the current JEST V05 manuscript;
these version labels describe different artifacts, not different science.

The DOI-only V05 manuscript rebuild passes technical QA (32-page Main,
12-page Supplement, 44-page combined PDF), including clean-extracted source
compilation, numerical/source parity and all-page visual review. Controlled
submission and new-page-transfer packages are returned through Drive.
Final independent review and author-controlled journal-submission items remain
separate from Zenodo publication; publication is not a submission-ready claim.
