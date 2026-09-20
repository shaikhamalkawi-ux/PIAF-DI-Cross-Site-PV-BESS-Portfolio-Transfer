# Global Machine-Evidence Replay Closure

Date: 2026-09-20

## Decision

**PASS — the previous 1,317 / 507 / 342 HOLD is closed.**

The exact retained V28 controlled reproducibility archive was recovered and executed twice from clean extractions. This is historical recovery/replay of the existing locked analysis, not a new experiment or a new scientific version.

## Archive identity

`PIAF_DI_PaperB_v28_Controlled_Reproducibility_Archive.zip`

SHA-256:
`7c618af56e8978fadaa4c41ae680881d4544cef49b797c9481836ec55258953d`

- ZIP CRC: PASS
- internal SHA-256 manifest: 104/104 PASS before execution

## Frozen-object identity

Recovered inside the archive:

- development portfolio-by-budget asset  
  `d1a500baa468b0659c4fefaf027029691204f011efbdd1a015f9be0a666e1495`
- Norway pre-outcome external protocol  
  `58a2526fdfd059d187aaff1062a71fc221115b588ae068acd4f9ef0bed624c79`

Both hashes match the current R6R8 Supplement.

## Clean replay

The archive-prescribed command `python run_all.py` returned:

- candidate-budget reproduction: **1,317 rows PASS**, max absolute difference `4.441e-16`;
- independent dense-grid binary-MILP oracle verification: **507 checks PASS**;
- V28 resolution robustness: **PASS**;
- independent 3x3 exact-enumeration verification: **342 checks PASS**;
- exact maximum 3x3 discrepancy: `4.440892098500626e-16`;
- terminal status: `V28_CLEAN_REPRODUCTION: PASS`.

The 342 checks comprise 108 Norway + 234 Boulder cases.

## Determinism

A second clean extraction and complete replay was run. Nine key regenerated CSV/JSON outputs were byte-identical across both runs.

## R6R7 lineage

The three previously named missing R6R7 packages were recovered with the exact locked hashes. Their CRC checks pass.

## Scientific effect

None. R6R8 remains the active scientific baseline. The recovery closes a reproducibility lineage gate; it does not change any result, equation, admitted source, candidate lattice, frozen portfolio, or conclusion.

## Remaining closure

Only archival/author-controlled work remains:
- permanent public repository / Zenodo DOI;
- final Data Availability identifier insertion;
- author approval, CRediT/ORCID/funding/declaration/portal metadata.
