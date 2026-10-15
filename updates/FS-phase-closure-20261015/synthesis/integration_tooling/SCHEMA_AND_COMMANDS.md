# FS scratch tooling handoff

This is additive tooling prepared from the published FR exporter at base `846f185763ed3a27310fad4ce9471ba324d1e5f4`. It has not exported authority, changed source bytes, committed, or written to the repository. Root must adjudicate proofs and freeze the actual curation before apply.

Use `build_integration.py`, `CURATION_INPUT.fs.template.json`, and `OPTIONAL_FS_RECORD_TEMPLATES.json` in this directory. The operational mapping is:

| Field | FS value |
|---|---|
| Intake path | `updates/FS-phase-closure-20261015/` |
| Intake/schema | `FS` / `astra.fs-curation-input.v1` |
| Source/notice/gate IDs | `src-FS-`, `SN-FS-`, `G-FS-` |
| Paired bridge IDs | `FS_` |
| Tentative numeric routes | N840, N841, N842 |
| Independent checkpoint template | `state/checkpoints/worker-fs-phase-closure/2026-10-15-fs-phase-closure.json` |

The numeric routes were absent from the pinned base. This is not a reservation against newer main or open PRs; root must repeat its concurrent namespace/ID check before applying. Apply itself requires matching HEAD and freshly read remote main, the exact finalized input hash, and no conflicting numeric route or immutable artifact.

Top-level required fields are `schema`, `intake_id`, full `base_revision`, `date_version`, nonempty named `evidence`, and `cards`. `sources` lists explicitly selected, already preserved new files under the FS intake path. Optional `checkpoint_path` is propagated to the claim map without publishing or validating a checkpoint.

Each source requires `path`, full original-byte `sha256`, `title`, and actual `read_depth`. Each evidence pointer requires `path`, full `sha256`, one-based inclusive `lines`, and exact `range_scope`; optional `read_path`, `source_id`, `hash_kind`, `source_revision` and `status` preserve the prior schema. New proof text must be recoverable byte-exactly. Existing capital proof references can be reused by their precise version/hash and metadata identity; no old source is silently copied or relabelled as newly supplied.

Each card requires `id`, `title`, `topics`, `scientific_scope`, `statement`, `assumptions`, `proof_spine`, `costs`, `information_acquisition`, `obstruction`, `comparator`, `missing_lemma`, `next_decisive_step`, `read_review_depth`, and selected `proof_refs`. Template fields are placeholders, not scientific assertions. Explicit `UNKNOWN` is valid. Root can supply scoped relations, inventory pointers, failed attempts and exact additional paragraphs; the exporter infers no mathematics from them.

Notice, paired-bridge and extra-gate schemas remain the earlier public architecture. Both bridge interfaces require `objects`, `regime_and_quantifiers`, `supplied_information`, `acquired_information`, `legal_access`, `guarantee`, `units_norm_and_precision`, and `costs`. Bridge states are the five composition states. The generator gives every card open review/capability gates and preserves `source_derived_unreviewed`; no bridge or metadata check promotes scientific validity.

The actual base has 31,293 heterogeneous metadata rows: 9,500 omit `source_id` and `path`, and 25,742 omit `sha256`. All optional lookups use `.get`; unidentified legacy rows remain untouched. Appending JSON containers preserves insertion order because all five tested base registries round-trip exactly in that mode and differ under `sort_keys=True`. JSONL retains its exact old byte prefix. Owned new JSON sidecars can use deterministic sorted keys without rewriting historical registry objects.

After proof adjudication, root fills `updates/FS-phase-closure-20261015/CURATION_INPUT.json` and runs:

```text
python3 -B /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-phase-closure-v1/workers/integration_tooling/build_integration.py --repo /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015 --input /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015/updates/FS-phase-closure-20261015/CURATION_INPUT.json --dry-run --report /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-phase-closure-v1/workers/integration_tooling/FINAL_DRY_RUN.json
```

For the reviewed, unchanged input, replace `--dry-run` with `--apply --expect-input-sha256 <reported-full-input-hash>`. Then root uses the existing access projection from the repository:

```text
python3 -B frontier/build_access.py build --base-revision 846f185763ed3a27310fad4ce9471ba324d1e5f4
python3 -B frontier/build_access.py check --base-revision 846f185763ed3a27310fad4ce9471ba324d1e5f4
```

The exporter does not run those commands, change historical cards, execute scientific scripts, publish checkpoints, create technology claims, or rebuild private SQLite data. It creates the established card/status/catalog/graph/provenance/web/notice/bridge records and a hash-pinned generator receipt. Identical reruns change zero files; changed immutable outputs fail closed.

`FS_FIXTURE_TEST_RECEIPT.json` records fifteen disposable software checks, including actual public-access builder acceptance, heterogeneous metadata, historical key ordering, namespace/ID consistency, open gates, source/range/conflict checks, pre-write source drift detection, and zero-change rerun. These checks establish integration-software scope only. `SOURCE_BYTE_AUDIT.json` and `BASE_SCHEMA_AUDIT.json` contain exact inventory/hash details; `VALIDATION_AND_REPLAY_PLAN.md` describes the remaining root checks without inventing replay results.
