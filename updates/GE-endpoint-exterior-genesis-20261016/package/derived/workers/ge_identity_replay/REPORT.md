# Source identity and bounded replay report

16 October 2026. Scope: packet identity, local source inventory, static review, and only the three explicitly bounded exact-copy replays. All generated receipts and replay copies are under `research/2026-10-16-endpoint-exterior-genesis-v1/workers/ge_identity_replay/`.

## Identity and provenance

The supplied `SOURCE_MANIFEST.json` marks packet contents as `source=DATA` and pins W to `adb0a306e9bfdc33b9fbd105efb58baed0cc021e`. W is at that commit and clean. Both ZIP envelope hashes and sizes match the manifest. I streamed all 43 pair-packet members and all 32 exterior-packet members individually; each member's byte length, CRC-32, and SHA-256 matched both the ZIP metadata and source manifest. The paths contain no traversal or absolute-path entries, duplicate member names, or symlinks. All 75 materialized originals named by the manifest also match. A post-run pass reconfirmed both ZIPs, all 75 members/materialized paths, and all 147 files covered by C's manifest.

The pair packet's 41-entry delivery manifest and 14-entry pair-certificate manifest verify against their referenced members. The exterior packet's 31-entry internal manifest and its three dependency hashes also verify. The exact duplicate payloads inside the exterior packet are the two empty dense-run logs and the two byte-identical copies of `run_dense_bounded.py`. Across packets, three dependencies are exact duplicates: `rigorous_pair_certificate.py`, `fair_bit_sampler.py`, and `PAIR_CERTIFIED_AVERAGING_REPORT.md`. The duplicates establish shared inputs, not independent evidence.

For prior W, I compared each packet-member SHA-256 against every tracked W file of the same byte length: 467 candidate files, 1,032,638 bytes in total. No nonempty packet member has an exact content match in W. The two zero-byte log members match generic empty W files. The full candidate hashes and paths are in `PRIOR_W_TARGET_HASHES.json`.

## Portable and tested snapshots

`run_dense_bounded.py` is byte-identical in the portable and tested snapshots; it was not run. Five other script pairs differ. The portable `exterior_certificate.py`, `verify_exterior.py`, `dense_comparator.py`, `check_sampler.py`, and `check_incumbent_residuals.py` use the packet's local dependency path, while the tested copies hard-code `/workspace/shared/interchange_local_saturation`. The portable `exterior_certificate.py` also restores an `n >= 4` input assertion that is absent in the tested snapshot. The portable `check_incumbent_residuals.py` includes scalar transcription diagnostics that the tested snapshot omits. The complete byte hashes and unified diffs are in `PORTABLE_TESTED_DIFFS.json`.

The stored portable and tested exterior result receipts agree on their exact bound, certification flag, and other mathematical fields; their differences are runtime and resource timings. The portable replay receipt advertises `portable_replay_exact_match=true`; the current comparison supports equality of the stored result fields, with timing fields kept separate.

## C inventory and decisive files

C's `MANIFEST.json` declares 147 files and 25,218,036 bytes. All 147 paths, lengths, and SHA-256 values match. The current directory also contains the manifest itself and 13 `.pyc` files under excluded `__pycache__` directories, for 161 physical files total; those 14 excluded files are listed in `C_INVENTORY.json`.

The 147 manifested files divide into 44 source-tree files and 103 campaign-side artifacts: 81 under `workers/`, 15 under `checks/`, 2 under `root/`, and 5 top-level reports/state/ledger files. The 44 source files include two version-pinned paper trees and source audit material. The 17 binary source payloads are 15 PDFs and two `.tar.gz` source archives: two primary paper PDFs, four reference PDFs, nine embedded figure PDFs, and two primary source archives.

The decisive campaign records are `REPORT.md`, `CAMPAIGN_STATE.json`, `CLAIM_LEDGER.json`, `CONTINUATION_HANDOFF.md`, `RESOURCE_RECEIPTS.json`, and `sources/l01/SOURCE_AUDIT.md`. The main mathematical/interface records include `workers/s01_controller_repair/TRANSITION_TABLE.md` and `REPORT.md`, `workers/s06_controller_adversary/REPORT.md`, `workers/s02_alternative_architecture/CANDIDATE_SPEC.md` and `RECOMBINATION_TEST.md`, `workers/s03_history_interface/FINITE_DISCHARGE.md`, and `root/ALL_HISTORY_CHANNEL_CONTRACT.md`. The finite replay trail is indexed by `checks/FINAL_DISCHARGE_REPLAY.json`, `checks/ROOT_REPLAY_RECEIPTS.json`, and `checks/ARTIFACT_VALIDATION.json`. C's own report labels the campaign `NOT_ACHIEVED`; this identity audit does not change that status.

## Static review and bounded replays

Static review found that the three selected scripts read only constants in code and copied local Python dependencies. Their writes are limited to a receipt JSON beside each copied script, plus captured stdout/stderr and run metadata in the same output tree. No network access, installation, campaign launcher, dense run, optimization, full SSA, or 200,000-sample run was used. `PYTHONPATH` was removed and Python bytecode writes were disabled. Every invocation had a 60-second timeout.

| Exact copied script | Runtime | Result |
|---|---:|---|
| Pair `rigorous_pair_certificate.py` | Python 3.14.3, NumPy 2.5.3; 0.175 s | Exit 0, no stderr. Its supplied six-site run reports `certified: true`, total upper bound `0.0438772355502554` for epsilon `1/20`, and 23 intervals. The fresh JSON matches the supplied result except for elapsed `seconds`. |
| Exterior `verify_exterior.py` | Python 3.14.3, NumPy 2.5.3, preinstalled mpmath 1.3.0; 1.495 s | Exit 0, no stderr. Reports 5 exact generator identities, 33 exact rounding checks, 2 invalid-input rejections, and 25 mpmath diagnostics. Its output is byte-identical to the supplied verification receipt. An initial attempt with `PYTHONNOUSERSITE=1` failed at import because that setting hid the existing mpmath package; no installation was made, and the exact copied script then passed with the preinstalled package enabled. |
| Exterior `cycle_extension/check_cycle.py` | Python 3.13.2, NumPy 1.26.4, SciPy 1.17.1; 0.534 s | Exit 0. Reports integer wedge/cover identities for cycles 3–12 and star-loop sign product `-1`. All 30 floating heat rows are finite and below the script's `2e-12` assertion threshold. The largest reported cover and survival errors are `7.22e-16` and `4.22e-15`. SciPy emitted divide-by-zero, overflow, and invalid-value `RuntimeWarning`s inside its matrix-exponential squaring routine; they are preserved in the replay receipt. The saved output contains finite diagnostics, but the warnings limit what those floating checks establish. |

The fresh pair result differs from its supplied receipt only in runtime. The fresh cycle result has different floating heat-error values from its stored snapshot, while its exact identity fields and assertions pass. Strict JSON parsing rejected nonstandard `NaN`/`Infinity` constants, and every numeric float in the replay JSON receipts was finite.

These runs establish source identity and bounded reproducibility only. Exit codes, hash parity, script-level certificate flags, exact finite checks, and finite floating diagnostics do not independently establish proof correctness, asymptotic behavior, novelty, external validation, or physical capability.

## Receipts

- `SOURCE_AUDIT_RECEIPT.json` — archive, member, internal-manifest, duplicate, and materialization checks.
- `PRIOR_W_TARGET_HASHES.json` — targeted W content scan.
- `IMMUTABLE_PAYLOAD_HASHES.json` — ZIP and member hashes plus C's 147 manifested file hashes.
- `C_INVENTORY.json` — C file counts, source/binary breakdown, excluded files, and decisive file index.
- `PORTABLE_TESTED_DIFFS.json` — snapshot hashes and diffs.
- `STATIC_REPLAY_REVIEW.json` — dependency and output-side-effect review.
- `REPLAY_RECEIPTS.json` and `REPLAY_COMPARISON.json` — process outcomes, warnings, finite checks, and source receipt comparisons.
- `FINAL_SOURCE_IMMUTABILITY_CHECK.json` — post-run source recheck.
