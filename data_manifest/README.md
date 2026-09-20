# Data manifest

`SOURCE_LOCKS.csv` records source identity, checksum, and redistribution status.
Raw third-party data are intentionally excluded from this public repository.
Users obtain the files from the cited repositories and verify the recorded
hashes before replay.

`MISSING_LINEAGE.md` records the specific historical artifacts that were not
available to the clean-room run. Missing objects are reported as `HOLD`; no
nearby archive is substituted as if it were the same lineage.
