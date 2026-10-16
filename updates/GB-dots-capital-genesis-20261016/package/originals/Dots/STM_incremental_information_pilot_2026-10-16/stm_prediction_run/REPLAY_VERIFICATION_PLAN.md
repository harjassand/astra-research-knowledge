# Portable verification and replay plan

## Status and scope

The single prespecified held-out evaluation is complete and the test set is burned. Any later recomputation is a verification/replay of that same disclosed result, not a fresh held-out experiment, replication dataset, new statistical test, or opportunity to select another model. Preserve the original prediction and evaluation markers. Do not rerun prediction_stage.py or evaluate_once.py against the original study directories. Do not refit, retune, change features/targets, fetch more episodes, or overwrite any frozen artifact.

No portable bundle or raw-data archive has been created by this plan. The 210,440,337-byte raw episode acquisition should not be packaged automatically.

## Recommended minimal metric-replay bundle

Copy these files unchanged into an explicitly named verification directory when packaging is authorized. Preserve their relative paths, bytes and SHA256 values; provide a separate relative-path manifest so original absolute paths in the frozen lock remain intact.

- test_predictions.json: all nine frozen learned-model predictions, both baselines, and row-routing keys (47,682 bytes)
- sealed/test_labels.jsonl: the now-released labels in fixed row order (11,636 bytes). Keep the study original read-only; a copy is released for arithmetic replay, not retuning.
- sanitized/test_routing.jsonl: explicit original row/episode keys (4,100 bytes)
- sanitized/test_inputs.jsonl: authorized prior-anchor/goal differences and action/current/d histories; needed to verify goal-radius and classification calculations without images (3,522,216 bytes)
- fits/fit_lock.json and fits/fit_lock.sha256.json: original arm choices, development q, support counts, candidate parameters, hashes and development results
- test_result_once.json: original complete result to compare against (118,261 bytes)
- heldout_lock.json, test_label_seal.json, and the canonical prediction/evaluation started markers: frozen provenance and proof that this is replay
- PROTOCOL_v1.1.md, split_manifest.json, audit_report.json, RESULT.md, PHASE_ONE_REPORT.md and this plan
- Frozen features.py, train.py, prediction_stage.py, evaluate_once.py, seal_labels.py and synthetic tests for inspection, not execution of their production stage entry points
- Independent review reports and arithmetic-check report when available

Use the actual seal-artifact path recorded in heldout_lock.json rather than guessing a filename. For metric-only replay no raw images, pickled episode archives, fitted-tree snapshots, author code, or hardware interfaces are required. The input table contains more history than metric arithmetic strictly requires, but retaining its original bytes avoids a new unverifiable transformation. Optional model-inference replay may include the nine numeric JSON snapshots (without training data or author code); it remains a deterministic replay of disclosed predictions.

## Verification sequence

1. Verify the original root-reviewed hashes below and every dependency listed by the held-out lock. Verify the released label bytes against the separately bound expected label digest, not merely a newly computed digest. Never change a locked file to fix a path. Instead resolve its recorded absolute path through an explicit read-only mapping to the corresponding relative-path file in the verification directory.
2. Confirm prediction row keys equal the separate routing file, are unique and ordered, and lie in the authoritative planned split. Confirm 60 eligible test episodes and 100 rows, with the three original planned blocks unchanged. Confirm every model has one finite 2-vector per row and labels have the required schema.
3. Use an independent arithmetic implementation, preferably standard-library Python or pinned NumPy, to compare the frozen prediction arrays with the released delta labels. Do not call the production stage CLI. Compute row Euclidean endpoint errors, within-episode means, then equal-weight means over episodes; compute macro squared Euclidean error and its square root. Compute pooled row median/p90 using linear quantiles. Recompute target-radius error using stored g-minus-p and labels; validate r and strict attainment threshold 0.288*sqrt(3)/3.
4. Recompute paired episode improvements (reference minus candidate), median/range and strict win fractions for the selected arms, baselines, and all three same-hyperparameter comparisons. Use selected candidate numbers from the immutable fit lock; do not select on test.
5. Retain fixed planned membership 2201–2391, 2401–2591 and 2601–2791 (step 10). Recompute each block's macro errors and paired improvements without changing eligibility or fitting by block.
6. Use unchanged development q values. Recompute the fraction of test episodes whose every residual is at most q. Report these as empirical development-residual envelopes, never guaranteed/confidence/conformal coverage.
7. Check train/development support from the fit lock and test support from released labels, then reproduce pooled deterministic-threshold balanced accuracy, sensitivity, specificity and precision. Undefined precision must remain undefined. Classification is supplementary and cannot rescue a failed primary endpoint gate.
8. Reproduce the fixed low/high forward/back-disagreement sensitivity analysis without dropping any row from the primary results. Recompute all six GO/NO-GO conditions exactly, including strict versus non-strict comparisons. Verify the scientific conclusion remains NO-GO.
9. Write a new verification report, with input hashes, implementation/library versions, maximum absolute numeric discrepancies, and an explicit statement that no model was fit or selected and no new held-out data were used. A small floating-point discrepancy is documented rather than used to replace the canonical result. A substantive inconsistency requires an explicit correction/invalidation record; preserve all originals.

## Root-reviewed artifact hashes

- Label-seal artifact: f7040c21a1ea3fb0e67cc2ea3d7179755db4d36ce7fe87d54ad3e950a17fd8cc
- Held-out lock: 3b87badab6afb6c954dd47fb239f911b68c3b64e58b1cde55333ab984ea6a936
- Frozen predictions: 7563650baeb98d1f38729391ff4bc1daee9eea2b513c3ba1b003036137bf5f20
- Canonical result: 9996114c744bf58c1fa68c0d3e227c4e7e943b7fa77483b82caf4de5382a16e2
- Train/development fit lock: 3e2ae20e8141e99eb9fb4486771b6d45d362d6078316aae2d81ad20c0db6d9bb

## Environment and interpretation

The original numerical environment was NumPy 2.3.5, SciPy 1.17.0 and scikit-learn 1.8.0. No installation has been performed for this plan. An independent arithmetic replay need not train or load sklearn models. Numeric JSON snapshots require no pickle/reducer execution. Never load raw NPY objects through pickle or NumPy allow_pickle.

All verified numbers describe recorded image-localization labels on the compatible serialized-new-image subset. Physical pre-scan interpretation remains conditional on documented logger timing/freshness. Reproducible arithmetic cannot establish historical physical freshness, hardware calibration, causal control value, saved scans or safety. New scientific work requires a new plan and genuinely independent data; replay cannot restore the held-out status of this set.
