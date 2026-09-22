# Reproducibility

This directory contains the public-safe R6R8 clean-room replay code and locked
derived reference tables. It does not contain raw Norway, Boulder, Dingle, or
SlimPark data.

## Environment

- Python 3.11 or newer
- `numpy`, `pandas`, `openpyxl`, `matplotlib`, and `Pillow`
- A LaTeX distribution for manuscript builds
- Poppler for PDF rendering/preflight

Install the Python dependencies with:

```text
python -m pip install -r reproducibility/requirements.txt
```

## Dingle replay

Obtain the public Dingle archive from DOI
`10.6084/m9.figshare.30294478`, verify the source ZIP SHA-256 recorded under
`data_manifest/`, and point the replay at the extracted `Dataset` directory:

```text
python reproducibility/dingle_replay.py \
  --source-dir /path/to/Dataset \
  --output-dir replay_output/dingle
```

The script verifies all twelve admitted file hashes, reconstructs the four
household interval loads, runs the primary and three sensitivity branches,
enumerates all 126/12,650 exact four-label alternatives, and compares its output
with the admitted tables.

## SlimPark replay

Obtain Version 1 from DOI
`10.4121/0fb5054c-0cc0-4c58-833e-fe89c8d13183.v1` and run:

```text
python reproducibility/slimpark_replay.py \
  --source-zip /path/to/slimpark_v1.zip \
  --output-dir replay_output/slimpark
```

The ZIP hash must be
`84bc48f1fe7631e52c431b6da117b2f55bf2fbbfa5f9c150757c2818f53f9a78`.
Raw workbooks are excluded by this project's public-release boundary.
SlimPark-derived components retain the source CC BY-NC-SA 4.0 licence,
attribution, modification notices, and consultation request; see the root
`LICENSES.md`. The request to consult is retained without claiming that
consultation occurred or imposing a separate permission condition on the
standard CC licence.

## Locked boundary

Both raw measured-input replays pass. The original historical machine evidence
was subsequently recovered and independently replayed: 1,317 target-budget
rows, 507 dense-grid MILP checks, and 342 coarse-grid enumeration checks pass,
with maximum discrepancy `4.440892098500626e-16`. The V04R2 sanitized archive
also passes a fresh clean core replay. See `STATUS.md` for archive integrity
and draft-deposit status. No historical v24 substitute was used to manufacture
these counts, and no locked scientific result was changed.
