# Bounded identity and replay support

This report covers archive provenance, manifest bindings, selected historical byte comparisons, and the three permitted bounded checker reruns for `2026-10-16-joint-structured-genesis-v1`. It does not certify the mathematics, physical relevance, novelty, or completeness of any scientific claim.

## Archive and manifest identity

The requested worktree is at pin `2688d7a383502df4fc1e64001d04bb76e6ec05e5`; it was clean before and after the audit. The root `SOURCE_MANIFEST.json` agrees with the four archive byte lengths and SHA-256 values below. All 43 manifest members passed ZIP CRC checks, member path checks, declared byte/hash checks, and exact comparison to their extracted paths. The four ZIP member sets matched their rows exactly, with no unsafe paths or duplicate member names.

| Archive | Bytes | Members | SHA-256 |
| --- | ---: | ---: | --- |
| `Astra_joint_finite_action_bound_2026-10-16.zip` | 13,649 | 5 | `3a59e98a9fd48ea4568927e39051126dee6a8f5eed2eed27bcfc009d1998598a` |
| `Astra_PR105_receiving_audits_2026-10-16.zip` | 101,264 | 21 | `4a483f753b283353045202f6c65d0bc7d00891f2a47c40a941bc30191dfa8f37` |
| `Astra_structured_noise_compiler_2026-10-16.zip` | 16,532 | 5 | `9bb54774ddf6184e816c3e8c5671207b5d4d09361857b6b8422bf0e0e5ff56b5` |
| `Astra_pair_clock_and_regularization_audit_2026-10-16.zip` | 40,861 | 12 | `3da2cc5f32edc05f708eae3e340fc721a8376164ac0fb5f37f71c659a598cc7c` |

The nested compiler, joint, and pair-clock hash manifests bind all payload siblings they enumerate. The receiving hash manifest binds 19 entries and omits `READ_ME.txt`; the parent root manifest binds both that file and the receiving manifest itself. The nested minimax source manifest has eight rows, each pointing to the pinned W checkout; all eight Git blob IDs, byte counts, SHA-256 values, and received source copies match. There are no duplicate payload hashes within the 43-member intake.

## Historical comparisons

I compared the received material with manifest files and small text/data files in the selected GC, GB, GA, and FZ update packages. The eight files under `originals/receiving/pr105_minimax_audit/source/` are exact byte copies of their GC-pinned files. The received homogeneous certificate is an exact duplicate of the GC certificate. Two pair-clock documents are exact duplicates of FZ artifacts. These are provenance relationships, not independent evidence.

The received `originals/receiving/pr105_homogeneous_audit/received_proof.md` is exactly the GC `gc_nonsep_genesis/PROOF.md` bytes followed by one additional LF: 13,607 versus 13,606 bytes. Removing that final LF yields the earlier SHA-256 `c564e52914d70ba14000e1abadb17ac7432b04d19fd62cb0bfb159b6c8713b36`; the received file’s SHA-256 is `c45c95d4f1ecd8f3957aacdcb65ae06d96c7aec1d662eb7b935983dd879d505f`. Across 71 selected-family manifest files, matching intake hashes appeared in GC and FZ records; none appeared in the scanned GA or GB manifest JSON. The same-basename content comparison found no GA or GB exact or one-final-LF match within its recorded suffix and size limits.

## Checker inspection and execution

Static inspection covered all six supplied Python programs, including imports, paths, writes, subprocess use, and bounded loops. The two acquired receiving checkers and the old public replay wrapper were not run. The wrapper has a hard-coded W path, unpacks/copies files, launches checker subprocesses, and can write or replace receipt files. The available Python 3.13.2 runtime had NumPy 1.26.4, SciPy 1.17.1, and SymPy 1.14.0; no dependency blocked a permitted run.

| Program | Disposition | Result |
| --- | --- | --- |
| `originals/joint/independent_checks.py` | Executed as an exact temporary copy | Exit 0; 16 finite cases. Emitted 12 NumPy runtime-warning lines (divide by zero, overflow, invalid value in matrix multiplication). |
| `originals/compiler/check_compiler.py` | Executed as an exact temporary copy | Exit 0. Emitted 30 NumPy runtime-warning lines in the same three categories. |
| `originals/pair_clock/pair_clock_adversary/check_ticket.py` | Executed as an exact temporary copy | Exit 0; 32,556 comparable state/label checks and 319 reachable local states; no warnings. |
| `originals/receiving/pr105_minimax_audit/independent_checks.py` | Not run | Acquired legacy checker. |
| `originals/receiving/pr105_homogeneous_audit/independent_checks.py` | Not run | Acquired legacy checker; reads sibling proof/certificate and writes `CHECKS.json`. |
| `originals/receiving/pr105_minimax_audit/source/replay_public_evidence.py` | Not run | Old replay wrapper; explicitly excluded. |

None of the checks was dependency-blocked. The old wrapper’s source-level aggregate rule accepts `ENVIRONMENT_BLOCKED`, `INPUT_EXCLUDED`, and `INSPECTED_NOT_RUN` rows while reporting overall `PASS`. Therefore an old `PASS` value cannot establish that every mandatory check ran; mandatory completeness remains `UNKNOWN`. This policy was inspected only; the wrapper was not executed.

The rerun JSON outputs differ bytewise from the supplied joint/compiler result JSON. Their structures are unchanged; observed differences are floating-point values, plus the joint result’s recorded runtime versions. The joint source result recorded Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0, while this rerun used Python 3.13.2, NumPy 1.26.4, and SciPy 1.17.1. Maximum absolute numeric deltas were about `5.6e-16` for the joint output and `1.2e-14` for the compiler output. The temporary reruns did not replace any original result files. Runtime warnings and full outputs are retained in the execution receipt.

## Boundary and frozen artifacts

The archive and source-file snapshots are unchanged, and the pinned W checkout remains clean. Finite checker exits and content hashes establish only the recorded identity and execution scope. Universal mathematical correctness, physical validation, priority, novelty, and practical capability remain `UNKNOWN`.

Machine receipts: `IDENTITY_RECEIPTS.json`, `HISTORICAL_COMPARISONS.json`, `CHECKER_STATIC_AUDIT.json`, `EXECUTION_RECEIPTS.json`, `SOURCE_RESULT_COMPARISONS.json`, and `SOURCE_UNCHANGED.json`. Their SHA-256 values are listed in `FROZEN_HASHES.sha256`; that list does not self-hash.
