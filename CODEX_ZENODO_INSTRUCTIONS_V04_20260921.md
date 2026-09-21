# CODEX — ZENODO DEPOSIT AND JEST DOI CLOSURE
## PIAF-DI Paper B — V04 instructions
Date: 2026-09-21

### Mission
Create and verify the Zenodo reproducibility deposit for the locked PIAF-DI Paper B R6R8 study, then return all machine-readable evidence through the existing Google Drive Codex inbox. Do **not** change the locked scientific results.

### Authoritative scientific baseline
`PIAF_DI_PaperB_v29R3R6R6R8_JEST`

Current journal-facing delivery baseline:
`V03_20260921`

Target journal:
**Journal of Energy Storage (JEST)**

Current manuscript title:
**Cross-Site Reuse of Compact PV-Battery Candidate Portfolios: Representation Limits and Transfer-Selection Loss**

### Google Drive workspace
Root:
https://drive.google.com/drive/folders/125rI_3FaZh3rKqsxCnIazTk9npJGETPe

Use these folders:
- `00_READ_FIRST` — instructions
- `01_CHATGPT_CURRENT` — current V03 manuscript/source/QA
- `03_CODEX_RETURN_INBOX` — return ALL V04 outputs here
- `05_ZENODO_READY` — Zenodo deposit inputs

### Required input files in `05_ZENODO_READY`
The folder currently contains:
1. `R6R8_REPRODUCIBILITY_ARCHIVE.zip`
2. `PIAF_DI_PaperB_v28_Controlled_Reproducibility_Archive.zip`
3. `R6R8_GLOBAL_MACHINE_EVIDENCE_CLOSURE_REPORT.md`
4. `R6R8_GLOBAL_MACHINE_REPLAY_GATES.csv`
5. `RECOVERED_LINEAGE_SHA256.txt`
6. `CITATION.cff`
7. `ZENODO_METADATA_DRAFT.md`
8. `LICENSE_DECISION_REQUIRED.txt`

### CRITICAL metadata correction
The current Zenodo metadata draft and historical CITATION file may still contain:
`Ahmed Abdelaziz Elsayed`

For this V04 deposit, the approved author display name is:
**Ahmed Elsayed**

Creator order must be exactly:
1. Ghassan Malkawi
2. Ahmed Elsayed
3. Mohammed Alhagyan
4. Bakeel Hussein

Do not silently restore the older longer Ahmed name.

### Zenodo record metadata
Use:
**Title**
Reproducibility materials for Cross-Site Reuse of Compact PV-Battery Candidate Portfolios: Representation Limits and Transfer-Selection Loss

**Resource type**
Software / reproducibility materials. If the Zenodo UI forces one best-fit type, use `Software` because the deposit is code/verification-centered and the existing CITATION.cff identifies it as software.

**Description**
Machine-readable reproducibility materials supporting a cross-site PV-battery candidate-portfolio transfer study for electric-vehicle charging. The deposit contains public-safe code, derived candidate-response/Pareto and verification tables, exact finite-subset and candidate-budget checks, Dingle and SlimPark replay materials without redistribution of third-party raw source workbooks, the historical controlled lineage, and the recovered V28 machine archive that independently reproduces 1,317 target-budget rows, 507 dense-grid MILP checks, and 342 coarse-grid exact-enumeration checks.

**Keywords**
PV-battery; BESS; electric vehicle charging; cross-site transfer; candidate portfolios; reproducibility; Pareto; energy storage

**Related identifier**
GitHub:
https://github.com/shaikhamalkawi-ux/PIAF-DI-Cross-Site-PV-BESS-Portfolio-Transfer

Do not invent a journal article DOI because the manuscript is not yet published.

### Public-safety / redistribution gate
Before uploading/publishing:
1. Inspect all intended Zenodo files.
2. Confirm that raw third-party Norway, Boulder, Dingle, and SlimPark source datasets/workbooks are NOT redistributed.
3. Confirm no credentials, access tokens, passwords, private filesystem paths, personal data, or unrelated files are present.
4. Confirm all public deposit artifacts are original code, derived results, provenance, or author-controlled/recovered machine evidence that is safe to redistribute.
5. Record this audit in `ZENODO_PUBLIC_SAFETY_AUDIT_V04_20260921.md`.

If a file fails the public-safety gate, STOP before publication and return a HOLD report.

### Zenodo authentication / secrets
- Never place a Zenodo access token in GitHub, Google Drive, source files, logs, or the returned ZIP.
- If the environment already provides a `ZENODO_ACCESS_TOKEN`, use it only through HTTPS and redact it from all logs.
- Required API scopes for full API publication are normally `deposit:write` and `deposit:actions`.
- If an authenticated Zenodo browser session is available, the web UI is acceptable.
- If no authenticated Zenodo access is available, do NOT fabricate success. Prepare the exact deposit package and return `ZENODO_AUTH_BLOCKER_V04_20260921.md`.

### File-size warning
`R6R8_REPRODUCIBILITY_ARCHIVE.zip` is about 136 MB.
The current Zenodo web upload supports large files, but the legacy deposition file API documented by Zenodo has a 100 MB per-file limitation.
Therefore:
- Prefer the current Zenodo web upload workflow or a current large-file API supported by the account.
- Do NOT silently split or recompress the archive.
- If the only available API path rejects the file because of size, return a blocker instead of altering the locked archive without approval.

### DOI workflow
1. Create a new Zenodo draft upload.
2. Upload the exact public-safe files.
3. Fill metadata.
4. Request/reserve a Zenodo DOI in the draft.
5. Save the draft.
6. Verify preview, creator order, title, description, keywords, file list, sizes and checksums.
7. Record:
   - deposition/record ID;
   - reserved DOI;
   - draft URL;
   - uploaded filenames;
   - Zenodo-returned checksums;
   - local SHA-256 values.

### LICENSE GATE — DO NOT GUESS
`LICENSE_DECISION_REQUIRED.txt` is still an explicit author/legal gate.

Do **not** choose a license on behalf of the authors and do not publish a permanent record unless:
- an author-approved license is already available in the workspace/account, or
- the author has explicitly approved the license in the active workflow.

If no explicit license approval exists:
- create/save the Zenodo draft and reserve the DOI if possible;
- do NOT press Publish;
- return `ZENODO_LICENSE_BLOCKER_V04_20260921.md`;
- preserve the draft and reserved DOI.

If an explicit author-approved license is available, apply it exactly and continue to publish.

### Publish gate
Only after all of the following pass:
- public-safety audit PASS;
- exact creator order/name PASS;
- metadata PASS;
- file/hash verification PASS;
- license explicitly approved;
- authenticated Zenodo session/token available.

Then publish the record and verify that the DOI resolves.

### After successful publication only
If and only if the Zenodo record is actually published and the DOI resolves:
1. Update the current V03 manuscript/source into **V04**.
2. Insert the Zenodo DOI in Main Data Availability.
3. Update the corresponding Supplement repository statement if applicable.
4. Update `CITATION.cff` to use **Ahmed Elsayed** and the published Zenodo DOI.
5. Update repository README/metadata as needed.
6. Do not change any locked scientific value or claim.
7. Rebuild Main and Supplement.
8. QA:
   - Main pages;
   - Supplement pages;
   - 0 Type 3 fonts;
   - 0 undefined refs/cites;
   - 0 overfull boxes;
   - search for TODO/TBD/FIXME/internal notes;
   - confirm all figures/tables;
   - compare locked numeric results with V03.
9. Produce JEST V04 package and new-page transfer package.

If only a draft DOI was reserved but the record was not published because of the license/auth gate, do NOT patch the manuscript as if the repository were permanently public. Return the reserved DOI and blocker status for author action.

### Required Codex return — Google Drive
Put every return artifact in:
`03_CODEX_RETURN_INBOX`

Use V04 filenames. At minimum return:
- `CODEX_ZENODO_STATUS_V04_20260921.md`
- `ZENODO_METADATA_FINAL_V04_20260921.md`
- `ZENODO_PUBLIC_SAFETY_AUDIT_V04_20260921.md`
- `ZENODO_FILE_HASHES_V04_20260921.txt`
- `ZENODO_API_OR_UI_LOG_REDACTED_V04_20260921.txt`
- `ZENODO_DRAFT_RECORD_V04_20260921.md` OR `ZENODO_PUBLISHED_RECORD_V04_20260921.md`
- `ZENODO_LICENSE_BLOCKER_V04_20260921.md` only if required
- `ZENODO_AUTH_BLOCKER_V04_20260921.md` only if required
- updated `CITATION_V04.cff`
- exact deposit ZIP/package if one is assembled
- if published: V04 Main PDF, Supplement PDF, source ZIP, JEST submission package, SHA256 manifest, and NEW_PAGE_TRANSFER V04.

### Status vocabulary
Return one and only one top-level status:
- `PASS — ZENODO PUBLISHED AND DOI VERIFIED`
- `HOLD — ZENODO DRAFT + RESERVED DOI; LICENSE APPROVAL REQUIRED`
- `HOLD — ZENODO AUTHENTICATION REQUIRED`
- `HOLD — PUBLIC-SAFETY/REDISTRIBUTION ISSUE`
- `STOP — REPRODUCIBLE SCIENTIFIC ERROR FOUND`

### Scientific lock
Do not:
- open R6R9;
- add datasets;
- add Simulink;
- add degradation/economics/feeder claims;
- change equations/results/candidate grids/dispatch rules;
- reinterpret 5% or 10% as engineering standards.

R6R8 science stays locked unless a reproducible result-changing error is found.

### Final instruction
Do as much as can be completed safely and verifiably. Never claim publication, DOI registration, file upload, or PASS unless the corresponding Zenodo record/state can be independently verified.
