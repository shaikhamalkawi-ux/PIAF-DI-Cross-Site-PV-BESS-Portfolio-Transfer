# Missing historical lineage objects

The clean-room workspace did not contain the named R6R7 binaries whose locked
hashes were supplied in the project instructions:

- manuscript + supplement ZIP:
  `833e449738b6cc328241de6d08fa3dd9ce5d2581b7e084b100ed6e56b0bcc63f`
- submission package:
  `eded7546842df939d61217b0bb036bccbe0c0840c0e41d01e8adbc5e4a4bce77`
- complete package:
  `cdb169eddd49cfa2c8b2ad9eece111dc94e224dc59e381044fd66df6fb667608`

The source machine files behind the later 1,317 reference target-budget rows,
507 dense-grid MILP checks, and 342 coarse-grid enumeration checks were also
absent. The run therefore records these gates as `HOLD`. The authenticated v24
archive is retained and independently verifies its own Norway branch, but it is
not represented as a byte-identical substitute for missing R6R7/R6R8 objects.
