# Codex Instructions — R6R8 Clean-Room Closure

## Read first
1. Read this file.
2. Read `STATUS.md`.
3. Use the controlled Google Drive workspace for manuscript, source packages, data, large artifacts, and return binaries:
   https://drive.google.com/drive/folders/125rI_3FaZh3rKqsxCnIazTk9npJGETPe
4. In Drive, read everything in `00_READ_FIRST` before doing any work.
5. Work on the branch `codex/r6r8-clean-room` for GitHub changes.

## User authorization
You are authorized to do the **appropriate technical, reproducibility, packaging, and editorial work needed to close the paper**, including:
- recover or reconstruct missing source/reproducibility structure from authenticated project lineage;
- repair scripts and packaging defects;
- reorganize code and manifests;
- regenerate figures/tables only from the locked admitted data and locked equations;
- improve build scripts, README files, provenance notes, environment files, QA scripts, and submission packaging;
- apply the already-approved production corrections;
- create any additional verification report needed to demonstrate reproducibility;
- prepare the final JEST-facing source/reproducibility package.

Use technical judgment and complete the task rather than stopping for minor implementation choices.

## Scientific rule
Active baseline:
`PIAF_DI_PaperB_v29R3R6R6R8_JEST`

**Preserve the locked science unless an actual reproducible error is found.**

Do not silently:
- add a new dataset to the scientific evidence base;
- change candidate lattices;
- change k=4;
- change equations, dispatch assumptions, thresholds, or frozen portfolios;
- introduce new economics, degradation, feeder constraints, hardware-controller studies, or Simulink results into R6R8;
- change a locked result merely to make a replay pass.

If a reproducible mismatch changes a locked result, evidence object, equation, or conclusion:
1. STOP the scientific rewrite;
2. preserve the failing artifacts;
3. document the mismatch in `CODEX_RETURN_MANIFEST.md`;
4. mark the affected gate STOP, not PASS.

Minor implementation, packaging, build, formatting, and documentation repairs do **not** require a new scientific version.

## Current task
Close the R6R8 reproducibility/package gap using:

**verified R6R7 lineage + R6R8 SlimPark delta -> clean replay -> full R6R8 QA -> JEST closure**

The detailed clean-room task and locked numerical values are stored in Google Drive under:
`00_READ_FIRST/CODEX_TASK_R6R8_CLEAN_ROOM`

## Google Drive is the canonical binary workspace
Read inputs from the Drive workspace.

Write every returned binary/source package to:
`03_CODEX_RETURN_INBOX`

Do not overwrite `00_READ_FIRST`, `01_CHATGPT_CURRENT`, or `02_BASELINE_INPUTS`.

When finished, the Drive inbox should contain:
- reconstructed source ZIP;
- reproducibility archive ZIP;
- rebuilt Main PDF;
- rebuilt Supplement PDF;
- replay report;
- SlimPark verification table;
- global verification table;
- source provenance report;
- final QA report;
- SHA256SUMS;
- `CODEX_RETURN_MANIFEST.md`;
- one master return ZIP.

## GitHub use
The repository is intentionally **public**.

Commit to `codex/r6r8-clean-room`:
- code that is legally/publicly releasable;
- scripts;
- environment specifications;
- public-safe manifests;
- README/provenance/QA text;
- public-safe derived tables needed for reproducibility.

Do not commit third-party raw data when the source licence does not permit redistribution. Keep such data in the controlled Drive workspace and document how it is obtained and verified.

Do not expose passwords, tokens, private author information, or credentials.

## Final decision
Required top-level return report:
`CODEX_RETURN_MANIFEST.md`

It must state:
- RETAIN or STOP;
- PASS/HOLD/STOP for every gate;
- exact unresolved blockers;
- SHA-256 for every returned artifact;
- final master ZIP SHA-256;
- exact Git commit used for the replay.

ChatGPT independently audits the Codex return. Do not label the paper `SUBMISSION READY` until that independent review is complete.

## Zenodo
Do **not** create or publish a Zenodo release yet. First close the clean-room replay and final QA. After ChatGPT verifies the return, prepare a clean public release for Zenodo/GitHub and then obtain the permanent DOI for the manuscript Data Availability statement.
