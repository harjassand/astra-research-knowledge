# FP integration generator handoff

`build_fp_integration.py` is a standard-library, scratch-only curation generator. It consumes finalized, root-authored data and creates public records using the existing Astra architecture. It never derives a scientific claim from filenames, topics, numerical output, or indexing. No mutation or export has been run against the real repository by this worker.

The exact input template is `CURATION_INPUT.template.json`; optional notice, paired-bridge, gate and scoped-relation shapes are in `OPTIONAL_RECORD_TEMPLATES.json`. Copy the filled input to `updates/FP/CURATION_INPUT.json` after freezing the proofs. All `REPLACE_` strings must be replaced.

## Mandatory input

- Top-level: `schema="astra.fp-curation-input.v1"`, `intake_id="FP"`, full `base_revision`, `date_version`, nonempty `evidence` object and `cards` array. `sources` identifies the selected new files to index. Optional `checkpoint_path` is propagated to every FP `CLAIMS.json` record; the generator does not create, validate or publish that checkpoint.
- Each new source: repository-relative `path` under `updates/FP/`, full original-byte `sha256`, `title`, and actual per-file `read_depth`. Bytes must already exist. Optional `source_id` must be in the `src-FP-` namespace; otherwise it is deterministically derived from the path. No files are copied and no tree-wide source inventory is inferred.
- Each named evidence object: `path`, full `sha256`, inclusive one-based `lines=[first,last]`, and `range_scope`. Optional `read_path`, `hash_kind`, `source_id`, `source_revision` and `status` preserve existing public-source conventions. Exact UTF-8 bytes must be recoverable directly or from an explicitly identified HTML `pre` block. A PDF/binary source may be indexed, but cannot substitute for an exact proof text range.
- Each card: full `id`, `title`, nonempty `topics`, `scientific_scope`, `statement`, nonempty `assumptions`, nonempty `proof_spine`, `costs`, `information_acquisition`, `obstruction`, `comparator`, `missing_lemma`, `next_decisive_step`, `read_review_depth`, and nonempty `proof_refs` (evidence keys). The allowed numeric routes are the reserved N822, N823 and N824, with one full card per route. A card proof must resolve to source metadata. Explicit `UNKNOWN` is valid; empty strings and template placeholders are not.
- Optional card fields: additional `paragraphs`, `inventory_refs`, `aliases`, `reported_failed_attempts`, `missing_artifacts`, and scoped relation arrays `depends_on`, `supersedes`, `invalidates`, `material_updates`, `contrasting_blockers`. Each supplied relation has `target`, `scope`, `relation_status`, and `ref_ids`. This intake forbids `whole_claim_invalidated=true`.

The source metadata is limited to the files explicitly listed in `sources`. A card's provenance and proof arrays are limited to its selected `proof_refs`; listing forty preserved files does not attach forty proof pointers to every card. Existing proof references can be reused when their exact path/hash resolves to an existing metadata record. Supply `source_id` explicitly if multiple historical metadata IDs match the same path/hash.

## Optional records

- A notice needs `notice_id` in the `SN-FP-` namespace, full `card_ids`, `issue`, exact `clarification`, and `ref_ids`. It appends a new semantic notice with scoped reciprocal material-update text. Existing older cards/status sidecars remain byte-identical.
- A paired bridge needs `id` in the `FP_` namespace, one of the five composition `state` values, full `cards`, `source_interface`, `destination_interface`, `alignment`, `missing_lemma`, `falsifier`, and `ref_ids`. Both interfaces require exactly the eight FO contract fields: `objects`, `regime_and_quantifiers`, `supplied_information`, `acquired_information`, `legal_access`, `guarantee`, `units_norm_and_precision`, `costs`. Optional `reciprocity` supplies explicit `forward` and `reverse` scopes. Incompatible/refuted records append to `rejected_transfers`; other states append to `bridges`. A bridge state preserves the supplied claim; it grants no external scientific validation.
- An additional gate needs `gate_id` in the `G-FP-` namespace, full `card_ids`, `title`, `question`, `pass_condition`, and `ref_ids`. Two default open gates per card retain independent review and the supplied next consequential operation. Every generated gate has `status="open"` and `completion_evidence=[]`.

## Generated files and append behavior

New immutable files are raw cards, matching review wrappers, current-status sidecars, source/card HTML pages, paired-bridge sidecars, and FP `CURATION.json`, `CLAIMS.json`, `INDEXED_SOURCES.json`, `EVIDENCE_REFS.json`, `SCOPED_NOTICES.json`, `BRIDGES.json`, `INTEGRATION_GENERATOR_RECEIPT.json`.

JSONL ledgers retain their exact existing byte prefix: claims, current statuses, source metadata, proof gates, semantic notices and web documents. Catalog/graph/web-catalog/bridge-registry arrays retain every existing record in order and append selected records only. Existing aliases are unchanged. JSON containers may be reformatted, but no historical record value is changed. Graph additions are provenance edges only; paired bridge semantics remain in the existing bridge registry.

Every new claim is `source_derived_unreviewed`; correctness, novelty, formal/empirical confirmation and physical capability remain `UNKNOWN` in generated validation metadata. The input must accurately state actual internal work in its per-file/card reading and proof fields. Historical checkpoint failures and prior receipts are neither modified nor reinterpreted.

## Root commands after freeze

First run a read-only plan, optionally saving the full plan outside the repository:

```text
python3 /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-capital-mining-v1/workers/integration_builder/build_fp_integration.py --repo /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange --input /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange/updates/FP/CURATION_INPUT.json --dry-run --report /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-capital-mining-v1/workers/integration_builder/FINAL_DRY_RUN.json
```

The plan reports the finalized input SHA256. After the root authorizes that exact input, use the same command with `--apply --expect-input-sha256 <that-full-sha256>`. Apply refuses unless current HEAD and freshly read `origin/main` both equal `base_revision`; this forces a fresh remote-collision/reconciliation check before real authority is appended. It uses a transient Git lock and preflights every read registry/source byte before any write. An identical rerun produces zero changes. A changed immutable output or conflicting existing identifier fails closed.

Then the root runs the existing public projection:

```text
python3 frontier/build_access.py build --base-revision <full-base-revision>
python3 frontier/build_access.py check --base-revision <full-base-revision>
```

The generator deliberately does not run these commands, commit, push, merge, publish a checkpoint, rebuild private SQLite views, or create technology records. It does not modify inherited legacy topic inventories; current generated concept/dossier/connection/proof/gate routes and the navigation manifest are refreshed by `build_access.py`. Legacy topic inventories already omit FO cards on this baseline; expanding that older architecture is outside this minimal tooling task.

## Verification and current limitations

`test_disposable_fixture.py` tests software safeguards entirely in a temporary directory and imports the real current `frontier/build_access.py` only for a fixture projection. `FIXTURE_TEST_RECEIPT.json` records twelve passing checks: no-write planning, apply, identical rerun, actual public projection acceptance, open gates, checkpoint-pointer propagation, immutable collision, source-hash mismatch, invalid line range, numeric-route collision, concurrent source change and conflicting ledger identifier.

No finalized root curation input has been consumed. The final real dry run and public checks remain root work after freezing the selected evidence. Remote main drift or an N822–N824 collision requires reconciliation before apply; the script intentionally does not guess replacement scientific IDs. Existing global checkpoint-schema failures remain outside this generator and must be preserved and reported separately.
