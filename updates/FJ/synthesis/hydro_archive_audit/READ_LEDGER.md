# Read ledger: physical archive delta

Workspace: `/Users/harjas/Documents/Codex/2026-10-14/astra-research-capital-integration-synthesis-breakthrough`

## Frozen source and provenance read

- `work/FJ_WORKER_CONTRACT.txt`: read worker ownership, copy-before-execution, source-preservation, and evidence requirements. This delta writes only under `work/FJ-hydro-archive-audit/`.
- `work/FJ-sources/SUPPLEMENTAL_INTAKE_MANIFEST.json` (SHA-256 `969ca83d86c0384b6a30f461a3e2d21ef9ed19894bd68291451972fd1126b17a`): read archive acquisition path and exact archive/member sizes and hashes. Its `initial_manifest_sha256` matches the preserved initial intake manifest.
- `work/FJ-sources/INTAKE_MANIFEST.json` (SHA-256 `2a8f77ee0e5ebfd2105a6d51270c0e44cc4029275a223c519d685cea94795043`): read to confirm the initial intake was preserved.
- `work/FJ-sources/physical/MANIFEST.json` (SHA-256 `fac8dc9ebc888bb7ba28422a5c5728497496744115b4615081308e0f7a3fbf62`): read full internal file-hash map.
- `work/FJ-sources/physical.zip` (11,200 bytes; SHA-256 `b473e6eb11d0dc531a72f3b6b9d7e4c2f0d5a7afb263197fa3ac7a5288575f2f`): listed archive members; four members total, 24,824 uncompressed bytes.
- Full `work/FJ-sources/physical/RESEARCH_NOTE.md` (15,226 bytes; SHA-256 `0cd43feb3528a6f59ad29df404a476251dbf3be89ad78395f9faabcf3d18c458`): read complete note, including assumptions, network derivation, contact-explicit Hall model, load bound, scope, experimental gate, and provenance.
- Full `work/FJ-sources/physical/check_model.py` (6,753 bytes; SHA-256 `968b6a2e3207dd6d22be5e0a21caaf7c656a5ca01547af94906421eb8dd20e3b`): read complete source before execution and again from the copied replay file.
- Full `work/FJ-sources/physical/model_checks.json` (2,573 bytes; SHA-256 `ec5c8172fec862acde5883903bb54a2c121d3c6ba6a6b3630b8fde3ab3fbd4cf`): read complete producer result.
- `work/FJ-sources/physical_PASTED_SOURCE.txt` (26,371 bytes; SHA-256 `040c3c95168c6c088e07e50943e934276bca88ff1ba4bd5d00d31bacd1d9a845`): verified the copy hash. Earlier owned audit ledger records its relevant claim ranges (53–89, 90–105, 106–130, and 154–188); the earlier frozen report is preserved and not edited by this delta.

An independent `zipfile` read verified the exact four archive members, including `MANIFEST.json`, byte-for-byte and hash-for-hash against the supplemental intake manifest; the initial intake hash also matches the supplement reference. All copied archive/member hashes in `input_snapshot/` match. The full replay command and output hashes are in `REPLAY_RECEIPT.json`.

## Literature scope

No new external literature claim was added in this delta. The earlier frozen `work/FJ-hydro-audit/READ_LEDGER.md` records primary-source reading for Onsager reciprocity, Büttiker multi-terminal quantum Hall transport, Hall terminal/contact loss, microwave circulator scope, and hydroelectronic measurements/theory. This delta relies on the archive's stated literature anchors only to identify that no physical wet transducer is supplied.
