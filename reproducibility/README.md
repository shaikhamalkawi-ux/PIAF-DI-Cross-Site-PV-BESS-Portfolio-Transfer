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
Raw workbooks are not redistributed because the source README specifies a
CC BY-NC-SA licence and asks users to consult the dataset contact before
sharing transformations.

## Locked boundary

Both raw measured-input replays pass. The older R6R7 machine-readable objects
needed to replay the manuscript's aggregate 1,317/507/342 verification claims
were not supplied. Those claims remain `HOLD`, not silently replaced by the
historical v24 tables.
