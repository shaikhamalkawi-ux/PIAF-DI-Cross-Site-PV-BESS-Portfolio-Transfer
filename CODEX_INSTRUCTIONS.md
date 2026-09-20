# Codex Instructions — R6R8 Clean-Room Closure

## Read first
1. Read this file.
2. Read `STATUS.md`.
3. Use the controlled Google Drive workspace for manuscript, source-package, dataset, and return binaries:
   https://drive.google.com/drive/folders/125rI_3FaZh3rKqsxCnIazTk9npJGETPe
4. In Drive, read `00_READ_FIRST` before doing any work.

## Scientific rule
Active baseline:
`PIAF_DI_PaperB_v29R3R6R6R8_JEST`

**Do not change the science.**

Do not:
- add a new dataset;
- change candidate lattices;
- change k=4;
- change equations, dispatch assumptions, thresholds, or frozen portfolios;
- add economics, degradation, feeder constraints, hardware-controller studies, or Simulink results;
- silently repair a scientific mismatch.

If a reproducible mismatch changes a locked scientific result, STOP and report it.

## Current task
Close the R6R8 reproducibility/package gap using:

**verified R6R7 lineage + R6R8 SlimPark delta -> clean replay -> full R6R8 QA -> JEST closure**

The detailed clean-room task and locked numerical values are stored in the private Drive workspace under:
`00_READ_FIRST/CODEX_TASK_R6R8_CLEAN_ROOM.md`

## Return protocol
Do not overwrite controlled inputs.

Put all binary/source return artifacts in:
`03_CODEX_RETURN_INBOX` in Google Drive.

For GitHub, commit only public-safe text/code/manifests unless the authors explicitly approve public release.

Required top-level return report:
`CODEX_RETURN_MANIFEST.md`

It must state:
- RETAIN or STOP;
- PASS/HOLD for every gate;
- exact unresolved blockers;
- SHA-256 for every returned artifact;
- final master ZIP SHA-256.

ChatGPT independently audits the return before submission readiness is declared.
