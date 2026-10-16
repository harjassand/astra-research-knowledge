# GE overlay renderer

These scripts render metadata for the GE endpoint-exterior intake. The builder reads a pinned Astra checkout and explicit root-supplied files, then writes a new review stage outside that checkout. The sidecar step adds neutral checkpoint and workflow records to the same stage. Neither step authors scientific claims or changes the canonical store.

## Config contract

The root-authored `claim_config.json` must remain outside the Astra checkout and use:

- `schema`: `astra.ge-claim-config.v1`
- `intake_id`: `GE-endpoint-exterior-genesis-20261016`
- `pins`: full `base_revision`, `expected_branch_head`, and `expected_remote_main` Git SHAs
- `cards`: one to five root-authored cards with distinct IDs on N903–N907, plus `title`, `topics`, exact `card_text`, and `status_record`
- `sources`: records containing `source_id`, `path`, `title`, `sha256`, `bytes`, `date_version`, `read_depth`, `reported_verification`, `extraction`, `provenance_role`, and `source_handling`; each also needs its explicit `source_file` binding. IDs use `src-GE-*`, and destination paths stay under `updates/GE-endpoint-exterior-genesis-20261016/`
- optional `gates`, `notices`, and `bridges` arrays, scoped to configured cards and using `G-GE-*`, `SN-GE-*`, and `GE_*` identifiers
- `worker_deployment_source_id`, naming a configured UTF-8 JSON source, and optional `worker_receipt_source_ids`

Every source item must bind an explicit `source_file`. A relative value is resolved from the config; an absolute value is also accepted. The resolved file must be inside the supplied `--research-root` (the GE research package) and outside the Astra checkout. The renderer reads its exact bytes, checks the configured SHA-256 and byte count, and stages those bytes without normalizing them. It does not unpack or preload archives.

The accepted `provenance_role` values are `supplied_original_file`, `root_synthesis`, `worker_derivation`, `same_team_review`, `same_team_research_or_review`, `root_or_worker_executable_check`, and `capital_comparison`. An authored literature report is recorded as `worker_derivation` or `capital_comparison`; acquired full text is not an accepted provenance role and must not be indexed. Paths marked `acquired_excluded_from_publication`, `acquired_full_texts`, or `third_party_full_texts`, and PDF or EPUB files, are rejected.

Each card status keeps `claim_status` at `source_derived_unreviewed` and the configured validation fields at `UNKNOWN`. Its `proof_availability.located_proof_sources` entries need an exact repository-relative path, SHA-256, inclusive UTF-8 line range, and matching source ID. The renderer checks references against the configured source bytes or the pinned checkout.

The workflow copies `total_spawn_and_followup_dispatches` from the configured root-supplied deployment JSON only when it is a nonnegative integer. It does not hardcode or infer a model identity, inference duration, token use, or worker count. Those fields remain unknown. The checkpoint `created_at_utc` records when the metadata record was rendered; it is not a model runtime measurement.

## Draft and application boundary

The build output directory must be new and outside the Astra checkout. The stage records exact source hashes, pins, registry hashes, and planned additions. JSONL additions retain the original byte prefix when later applied. JSON registries retain their old key order and array prefixes.

This intake remains a draft outside the canonical store. Three inherited old-schema failures are known and remain outside this renderer's scope. The apply command is included for a separately reviewed overlay, but it has not been run for this intake. If used later, it rechecks the pinned base, branch head, remote main, working tree, and registry hashes, writes only create-only files and append-only deltas, and never stages or commits Git changes.

## Commands

Set paths for the pinned checkout, root-authored config, research root, stage, and receipt. The config and source files must be in the GE research package; the stage must not exist yet.

```sh
python3 workers/ge_overlay_renderer/build_overlay.py \
  --repo "$ASTRA_REPO" \
  --config "$GE_CONFIG" \
  --research-root "$GE_RESEARCH_ROOT" \
  --output "$GE_STAGE"

python3 workers/ge_overlay_renderer/metadata_sidecars.py \
  --repo "$ASTRA_REPO" \
  --config "$GE_CONFIG" \
  --research-root "$GE_RESEARCH_ROOT" \
  --stage "$GE_STAGE"
```

The sidecar step adds a checkpoint draft, workflow metadata, and a schema/reference validation receipt to the external stage. It validates record shape, hashes, UTF-8 lines, and links only; it does not certify scientific truth.

After separate review and authorization, an overlay can be applied with:

```sh
python3 workers/ge_overlay_renderer/apply_overlay.py \
  --repo "$ASTRA_REPO" \
  --stage "$GE_STAGE" \
  --receipt "$GE_RECEIPT"
```
