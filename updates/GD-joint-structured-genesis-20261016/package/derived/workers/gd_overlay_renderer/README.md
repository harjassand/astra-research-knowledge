# GD overlay renderer

These three scripts stage root-authored GD records against a pinned Astra checkout. They copy exact configured bytes and render metadata; they do not write scientific claims, interpret source content, or infer model or inference usage.

## Config contract

claim_config.json must be outside the Astra checkout and use:

- schema: astra.gd-claim-config.v1
- intake_id: GD-joint-structured-genesis-20261016
- pins: full base_revision, expected_branch_head, and expected_remote_main Git SHAs
- cards: one to five root-authored card objects, each with a distinct ID on N898–N902, plus title, topics, exact card_text, and status_record
- sources: records with exact source_id (src-GD-*), destination path under updates/GD-joint-structured-genesis-20261016/, title, sha256, bytes, date_version, read_depth, reported_verification, extraction, provenance_role, and source_handling; each item also has a source_file path relative to the config or an absolute path inside --research-root
- optional gates, notices, and bridges arrays authored by the root and scoped to the configured cards
- worker_deployment_source_id, naming one configured UTF-8 JSON source, and optional worker_receipt_source_ids

Each card status keeps the configured producer status and UNKNOWN validation fields. Its proof_availability.located_proof_sources entries need exact repository-relative path, sha256, inclusive UTF-8 lines, and the matching source_id. The renderer checks these against configured source bytes or the pinned checkout.

Do not index or cite files under acquired_excluded_from_publication, and do not include full-text PDF or EPUB files. The source loader also rejects acquired-full-text provenance roles and requires supplied files to remain inside the research root. Source records retain exact hashes and byte counts.

The sidecar renderer reads total_spawn_and_followup_dispatches from the configured worker-deployment JSON only when it is a nonnegative integer. Model identity, inference duration, token usage, and missing values remain unknown.

## Commands

Set the three roots and file paths for the current run. The stage directory must be new and outside the Astra checkout.

~~~sh
python3 workers/gd_overlay_renderer/build_overlay.py \
  --repo "$ASTRA_REPO" \
  --config "$GD_CONFIG" \
  --research-root "$GD_RESEARCH_ROOT" \
  --output "$GD_STAGE"

python3 workers/gd_overlay_renderer/metadata_sidecars.py \
  --repo "$ASTRA_REPO" \
  --config "$GD_CONFIG" \
  --research-root "$GD_RESEARCH_ROOT" \
  --stage "$GD_STAGE"
~~~

The second command adds a checkpoint draft, a workflow metadata record, and a schema/reference validation receipt to the existing stage and refreshes PLAN.json. It reads the worker deployment file supplied by the config. It does not add technology opportunity records or scientific summaries.

After the complete stage has been reviewed, the apply command can create the staged files and append registry deltas. The checkout must still match the pinned HEAD, have a clean working tree, and retain all recorded registry hashes. The receipt path must be new and outside the checkout.

~~~sh
python3 workers/gd_overlay_renderer/apply_overlay.py \
  --repo "$ASTRA_REPO" \
  --stage "$GD_STAGE" \
  --receipt "$GD_RECEIPT"
~~~

Application creates only new overlay paths and appends configured registry deltas. Existing JSONL bytes remain an exact prefix; old JSON registry keys and array values retain their order. The apply command does not stage or commit Git changes.
