# Historical lineage recovery status — RESOLVED

The earlier clean-room pass correctly marked historical lineage as HOLD because the required binaries were not then available in the controlled workspace.

That condition has now been resolved from the retained project Library.

## R6R7 named binaries — PASS

Recovered exact locked objects:

- manuscript + supplement ZIP  
  `833e449738b6cc328241de6d08fa3dd9ce5d2581b7e084b100ed6e56b0bcc63f`
- submission package  
  `eded7546842df939d61217b0bb036bccbe0c0840c0e41d01e8adbc5e4a4bce77`
- complete delivery  
  `cdb169eddd49cfa2c8b2ad9eece111dc94e224dc59e381044fd66df6fb667608`

All recovered ZIPs pass CRC.

## Global 1,317 / 507 / 342 machine evidence — PASS

Recovered exact historical controlled archive:

`PIAF_DI_PaperB_v28_Controlled_Reproducibility_Archive.zip`

SHA-256:
`7c618af56e8978fadaa4c41ae680881d4544cef49b797c9481836ec55258953d`

Verification:
- archive CRC PASS;
- internal V28 SHA-256 manifest 104/104 PASS before execution;
- frozen development-portfolio hash matches the current Supplement:
  `d1a500baa468b0659c4fefaf027029691204f011efbdd1a015f9be0a666e1495`;
- frozen Norway protocol hash matches the current Supplement:
  `58a2526fdfd059d187aaff1062a71fc221115b588ae068acd4f9ef0bed624c79`;
- fresh candidate-budget replay reproduced 1,317 rows;
- independent dense-grid binary-MILP verification passed 507 checks;
- independent coarse-grid exact enumeration passed 342 checks;
- maximum discrepancy:
  `4.440892098500626e-16`, reported in the manuscript as `4.44e-16`;
- a second clean replay produced byte-identical key CSV/JSON outputs.

No historical substitute was used: these are the retained machine objects that generated the locked candidate-budget/cross-resolution verification layer.

## Dingle outer ZIP — PASS

The exact locked Figshare ZIP was also recovered:
`5ec52a61851936b5b9a537c3565863d7c1cbaa5271e0fce3a02e61703bf76beb`

It passes full ZIP CRC and its admitted source members match the locked hashes.

## Current boundary

There is no remaining scientific/reproducibility HOLD from the previously missing lineage. Remaining closure is archival/author-controlled: permanent repository/Zenodo DOI and final submission metadata/declarations.
