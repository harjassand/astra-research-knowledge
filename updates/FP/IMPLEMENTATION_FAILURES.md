# FP integration failure ledger

This records implementation attempts, not scientific counterexamples. The final check results and exact logs are in `VALIDATION.json` and `validation/`.

- The first local authority-generation script stopped before any authority write because it looked for `path` rather than `copy` in the source manifest. The script was corrected and run once against the untouched authority files.
- The first public-view build rejected the new status records because `proof_availability.available_evidence_sources` was an integer rather than an iterable of source references. Only the two new uncommitted status records were corrected. The historical prefix of `frontier/CURRENT_CLAIM_STATUS.jsonl` was restored byte-for-byte before rebuilding.
- The first FP validator assumed every historical source-metadata row had `source_id`; a legacy row does not. The new validator now filters with `get`, without altering that row.
- The first new-only checkpoint fallback tried to render its branch view before the new checkpoint file existed; `views()` needs the record hash from disk. That attempt stopped before writing a checkpoint or registry row. The corrected locked fallback exclusively created the new checkpoint, then its view, then appended one registry row.
- The standard checkpoint publisher and global checkpoint validation both fail with `ERROR: unsupported checkpoint schema` on inherited records. Their bytes were preserved. The new FP record passed individual `validate_record`; `PUBLICATION_STATUS.json` states the narrower fallback result. The publisher's software fixtures pass.
- After the frozen authored campaign packet arrived, the standard publisher failed again on the same inherited schema. A second individually valid FP checkpoint was exclusively appended with the first FP checkpoint as its sole parent. Only that branch's generated view and registry head were refreshed; the first record stayed byte-identical.

No commit, push or pull request was made by this worker.
