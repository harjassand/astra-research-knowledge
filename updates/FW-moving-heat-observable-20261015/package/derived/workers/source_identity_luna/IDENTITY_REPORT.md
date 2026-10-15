# Source identity and exact-hash dedup audit

This audit verifies the intake manifest against original and preserved bytes, checks ZIP extractions and declarative SHA manifests, and compares exact SHA-256 values with the selected Astra Capital update/intake paths. It makes no scientific claim.

Audit window: 2026-10-15T08:35:00+00:00 to 2026-10-15T08:35:01+00:00 UTC.
Research intake pin: `33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`. Capital worktree HEAD at audit: `33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`.
Source manifest: `research/2026-10-15-moving-heat-observable-power-v1/SOURCE_MANIFEST.json`; SHA-256 `60ad681e5f370b03caf9c2934af754eb4d31602eeb3d4c2a5fc68d846728ffe5`.

## Manifest and original-byte checks

The manifest declares 13 groups and 58 files (11,379,563 bytes). Computed from entries: 13 groups, 58 files (11,379,563 declared bytes).
Original paths matching declared bytes and SHA-256: 58/58. Preserved copies matching: 58/58. Original and preserved bytes equal: 58/58.

| Source group | Listed files | Extracted ZIP members | Distinct observed hashes | Capital matches | New hashes in selected scope |
|---|---:|---:|---:|---:|---:|
| `archive:Astra_PR94_acquisition_2026-10-15.zip` | 1 | 20 | 21 | 0 | 21 |
| `archive:Astra_avalanche_capability_2026-10-15.zip` | 1 | 71 | 71 | 0 | 71 |
| `archive:Astra_binary_control_2026-10-15.zip` | 1 | 165 | 166 | 0 | 166 |
| `archive:Astra_complete_failure_2026-10-15.zip` | 1 | 15 | 16 | 0 | 16 |
| `archive:Astra_critical_storage_2026-10-15.zip` | 1 | 11 | 12 | 0 | 12 |
| `archive:Astra_interacting_failure_2026-10-15.zip` | 1 | 12 | 13 | 0 | 13 |
| `archive:Astra_positive_clock_2026-10-15.zip` | 1 | 25 | 26 | 0 | 26 |
| `directory:ASTRA_dislocation_transport_checkpoint` | 4 | 0 | 4 | 0 | 4 |
| `directory:astra_compatible_heat_result` | 19 | 0 | 19 | 0 | 19 |
| `directory:astra_pulse_observable` | 25 | 0 | 25 | 0 | 25 |
| `pasted:computation_pasted.txt` | 1 | 0 | 1 | 0 | 1 |
| `pasted:mathematics_pasted.txt` | 1 | 0 | 1 | 0 | 1 |
| `pasted:physical_pasted.txt` | 1 | 0 | 1 | 0 | 1 |

Missing original paths: 0; original byte/hash mismatches: 0; missing preserved copies: 0; preserved byte/hash mismatches: 0.
The artifact inventory has 377 observed file rows and 376 distinct hashes; repeated source hashes: 1.
- Repeated exact bytes `9b3fa720d035e62f27ab9613a193fc789dcca149023e7586c742084931931cf4` in `sources/Astra_avalanche_capability_2026-10-15.zip!/Astra_avalanche_capability/avalanche_independent_audit/portable_replay.txt` (archive:Astra_avalanche_capability_2026-10-15.zip); `sources/Astra_avalanche_capability_2026-10-15.zip!/Astra_avalanche_capability/avalanche_independent_audit/rare_integer_1024_results.json` (archive:Astra_avalanche_capability_2026-10-15.zip).

## ZIP and embedded hash-manifest checks

ZIPs checked: 7. Members compared with preserved extraction: 319 total; 7/7 archives have every member extracted byte-for-byte.
- `sources/Astra_interacting_failure_2026-10-15.zip`: 12 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_complete_failure_2026-10-15.zip`: 15 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_avalanche_capability_2026-10-15.zip`: 71 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_critical_storage_2026-10-15.zip`: 11 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_positive_clock_2026-10-15.zip`: 25 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_PR94_acquisition_2026-10-15.zip`: 20 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
- `sources/Astra_binary_control_2026-10-15.zip`: 165 members; exact extraction=True; missing=0; extra=0; unsafe paths=0; ZIP symlinks=0.
Embedded source SHA manifests discovered with hash records: 7; listed records: 159; verified: 158; parse, resolution, or hash issues: 1.
- Internal digest discrepancy: `large_result_400_author.json` in `Astra_avalanche_capability/avalanche_boundary_dp/LARGE_SHA256.txt` lists `66052387c62c88aef91b082e82461d0047d24251c17b6bd35580646469dd9b23`, while the archived member hashes to `80b30cf0ab73bb81c31c3af2bcf1f08dd6c08083711013b2b5ac54d4d3064b39`. The ZIP member and its preserved extraction agree byte-for-byte; the source manifest discrepancy is retained as observed.
- `SHA256.json`: 11/11 listed hashes verified; issues=0.
- `SHA256.json`: 14/14 listed hashes verified; issues=0.
- `Astra_avalanche_capability/avalanche_boundary_dp/LARGE_SHA256.txt`: 12/13 listed hashes verified; issues=1.
  - Mismatched: [{"expected": "66052387c62c88aef91b082e82461d0047d24251c17b6bd35580646469dd9b23", "listed_path": "large_result_400_author.json", "member": "Astra_avalanche_capability/avalanche_boundary_dp/large_result_400_author.json", "observed": "80b30cf0ab73bb81c31c3af2bcf1f08dd6c08083711013b2b5ac54d4d3064b39"}]
- `Astra_avalanche_capability/SHA256SUMS.json`: 70/70 listed hashes verified; issues=0.
- `Astra_positive_clock/SHA256SUMS.json`: 24/24 listed hashes verified; issues=0.
- `research/2026-10-15-moving-heat-observable-power-v1/sources/ASTRA_dislocation_transport_checkpoint/manifest_sha256.json`: 3/3 listed hashes verified; issues=0.
- `research/2026-10-15-moving-heat-observable-power-v1/sources/astra_pulse_observable/MANIFEST.json`: 24/24 listed hashes verified; issues=0.

## Capital comparison scope and results

Hashed 1495 regular files across the five FT/FU/FV update trees, 3 FV-declared candidate intake directories, and explicit existing file references from selected metadata manifests. Metadata contained 2456 file-reference records; 145 unique explicit file targets fell outside the selected update and candidate-intake directories. The source artifact inventory contains 377 observed files, representing 376 distinct SHA-256 values. Exact matches: 0 distinct hashes (0 source artifact rows). New to this selected comparison scope: 376 distinct hashes.

| Capital update | Recorded manifest/checkpoint dates | Recorded manifest/checkpoint pins | Listed file records | Source-manifest SHA-256 |
|---|---|---|---:|---|
| `FT-direction-transport-20261015` | manifest 2026-10-15T02:15:21.124733+00:00 | `manifest b7cada92d2eb304578be5ed974f1e44b10a89928` | 23 | `1f39706a97f980a43ad1304e0de74cbd9ff20d115998b3f845240dca316fe918` |
| `FT-foundational-capability-20261015` | checkpoint 2026-10-15T02:57:41Z | `checkpoint base b7cada92d2eb304578be5ed974f1e44b10a89928` | 79 | `b8cc3da373d58de0f8eeccd620bae9ac97a29a0d84158ad2a74290c6520f4baa` |
| `FT-foundational-capability-v2-20261015` | manifest 2026-10-15 03:42:25 UTC; checkpoint 2026-10-15T03:59:24.279096Z | `checkpoint base 0c789ca775808e23e57138b56a393ad1e58cb15c` | 57 | `067ba8702b4853dcb40bc2270246507962fa90d48879421b3eb5291c746fce25` |
| `FU-regularization-clock-pressure-20261015` | checkpoint 2026-10-15T06:10:40.346331+00:00 | `manifest 0c789ca775808e23e57138b56a393ad1e58cb15c; checkpoint base 6fde70a4668f877bc9988bc8f20c570ef4513d08` | 3 | `44eb7ffb04f099407e9f7c7d90b1bf0eaf9025a92a67d953d08d7bbef3077f05` |
| `FV-positive-consequences-20261015` | checkpoint 2026-10-15T07:53:26.317335+00:00 | `manifest a6190a1083f688a7e4bf64adbc5244ef150ff2c4; checkpoint base a6190a1083f688a7e4bf64adbc5244ef150ff2c4` | 3 | `4ef169ca0c424b4c73bfbb55700169be32ea8150a9ecaa5ea90baaebcdb5d474` |

FV-declared candidate intake directories included:

- `work/astra-capital-positive-consequences-20261015/updates/FT-direction-transport-20261015/package` — 23 regular files.
- `work/astra-capital-positive-consequences-20261015/updates/FT-foundational-capability-v2-20261015/package/inputs` — 3 regular files.
- `work/astra-capital-positive-consequences-20261015/updates/FU-regularization-clock-pressure-20261015/package/sources` — 3 regular files.

## Reference-containment limits

Exact SHA-256 matches are allowed across source-group, filename, and capital-directory boundaries. A match establishes identical bytes only; it does not transfer a source label or provenance claim. Direct file references outside selected update trees are listed as explicit references. ZIP member paths were checked for absolute/parent traversal; symlinks were recorded and not followed.
The three additional intake folders are taken only from FV's `supplied3_duplicate_check.candidate_source_folders` field. Broad search roots such as Downloads and the attachment archive were not recursively scanned. The report preserves the path that produced each match so a same-byte result across folders or labels is visible. There are 145 explicit metadata file targets outside the selected directories; their exact paths and referring metadata are recorded in the JSON ledger.
