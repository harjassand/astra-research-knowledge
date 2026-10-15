# FT additive tooling handoff

This derivative is prepared from the published FS exporter at `b7cada92d2eb304578be5ed974f1e44b10a89928`. Only files in the new research scratch tooling directory were written. No repository authority export, checkpoint publication, scientific execution or old-source change was performed.

The operational namespace is `updates/FT-direction-transport-20261015/`, input schema `astra.ft-curation-input.v1`, intake `FT`, source IDs `src-FT-`, semantic notices `SN-FT-`, gates `G-FT-`, bridges `FT_`, and checkpoint template `worker-ft-direction-transport`. Tentative routes are N850, N851 and N852. The exporter enforces these values, including error messages and lock/temp paths.

`RESERVATION_CHECK.json` records the live point-in-time audit: local HEAD and remote main matched the pinned base; N850–N852 were absent from the base; complete paginated changed-file inventories for all four open PRs had no matching FT namespace/routes. Root must repeat this check before actual export/publication. Main absence alone does not reserve a namespace against open or future work.

Use `CURATION_INPUT.ft.template.json` and `OPTIONAL_FT_RECORD_TEMPLATES.json`. Card titles, statements, scopes and proof routes remain placeholders for root adjudication; none are inferred or auto-filled.

Required top-level fields are `schema`, `intake_id`, full `base_revision`, `date_version`, selected `sources`, nonempty named `evidence`, and `cards`. Optional `checkpoint_path` is copied into the claim map without publishing or validating a checkpoint. Each new source needs an already preserved path under the FT intake, full original-byte `sha256`, `title` and actual `read_depth`. Existing capital can be cited through exact existing metadata/source versions instead of being relabelled as newly supplied.

Each evidence object needs `path`, full `sha256`, one-based inclusive `lines` and exact `range_scope`; optional `read_path`, `source_id`, `hash_kind`, `source_revision` and `status` follow the prior schema. Each card needs full `id`, `title`, nonempty `topics`, `scientific_scope`, `statement`, `assumptions`, `proof_spine`, `costs`, `information_acquisition`, `obstruction`, `comparator`, `missing_lemma`, `next_decisive_step`, `read_review_depth`, and selected `proof_refs`. Explicit `UNKNOWN` is valid. Unfilled placeholders are rejected.

Optional scoped relations, semantic notices, paired bridges and extra gates retain the existing public architecture. Paired interfaces require `objects`, `regime_and_quantifiers`, `supplied_information`, `acquired_information`, `legal_access`, `guarantee`, `units_norm_and_precision` and `costs`. Claims remain `source_derived_unreviewed`; review and capability gates remain open. The exporter adds two default open gates per card. It infers no theorem dependency from topic overlap and leaves old cards/status sidecars unchanged.

The pinned metadata registry has 31,381 rows, including 9,500 without `source_id`/`path` and 25,742 without `sha256`. Optional-field `.get` guards and unidentified-candidate filtering are retained. Every tested JSON registry round-trips byte-exactly using insertion order and differs under sorted serialization. The exporter preserves existing object key order and JSONL byte prefixes; it uses deterministic sorted keys only for new owned sidecars.

`SOURCE_BYTE_AUDIT.json` records all 23 supplied files/417,216 bytes and all 23 available original-path checks. Nine direction-manifest entries and six closure SHA256 entries match. Three direction audit files/10,274 bytes exactly match existing FS verification evidence; preserve their supplied provenance and mark aliases without claiming new science. These are integrity observations, not correctness or novelty clearance.

`INHERITED_PUBLICATION_AUDIT.json` records a fresh read-only global validation failure with `ERROR: unsupported checkpoint schema`. The same three known historical records remain byte-identical to Git. Standard publish was not attempted; root must retain the actual future publisher receipt and validate a new handoff separately.

After proofs/reviews are adjudicated and inputs frozen, root fills `updates/FT-direction-transport-20261015/CURATION_INPUT.json` and runs:

```text
python3 -B /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-direction-transport-v1/workers/integration_tooling/build_integration.py --repo /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015 --input /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015/updates/FT-direction-transport-20261015/CURATION_INPUT.json --dry-run --report /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-direction-transport-v1/workers/integration_tooling/FINAL_DRY_RUN.json
```

After reviewing that exact plan/input hash, replace `--dry-run` with `--apply --expect-input-sha256 <full-reported-input-hash>`. Apply requires current HEAD and freshly read remote main to equal `base_revision`, rejects numeric-route/immutable-output collisions, and preflights every read source/registry byte before writing. An identical rerun changes zero files. A changed immutable output requires an explicit new version instead of replacement.

Root then uses the existing public projection from the repository:

```text
python3 -B frontier/build_access.py build --base-revision b7cada92d2eb304578be5ed974f1e44b10a89928
python3 -B frontier/build_access.py check --base-revision b7cada92d2eb304578be5ed974f1e44b10a89928
```

If main moves, reconcile source pins/reservations and the input base before applying; do not disguise the change by rewriting old records. The public projection does not rebuild private SQLite data or certify science.

`FT_FIXTURE_TEST_RECEIPT.json` records fifteen disposable integration checks, including actual current access-builder acceptance, metadata heterogeneity, historical key order, immutable collisions, source/range/hash drift, namespace consistency and zero-change rerun. These are software fixtures only.

Later replay and scoped validation must use root's actual final verifier selection and manifests. No earlier wave's 16-step replay, 67-source or 118-derived-file count is carried into this exporter/template. Selected checks may use the permitted isolated previous-wave runtime at `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-phase-closure-v1/.venv/bin/python`, with actual package versions recorded at execution. No raw source download, exploratory search or Torch rerun is needed for this preparation.
