# Held-out-stage independent review, initial submission

2026-10-16 UTC. Phase-one REPORT.md remains unchanged.

## Decision: BLOCKED pending label-integrity binding

The submitted prediction_stage.freeze hashes test inputs/routing but does not bind the sealed test-label file to a pre-prediction expected hash. The evaluator computes and reports a hash only after reading labels. A syntactically valid accidental label-file change would therefore not be detected by existing provenance checks. Root raised this specific gap during independent review; source review confirms it.

Required correction, reported to root and implementation worker before changes: use separately authorized hash-only processing to establish the exact sealed-label SHA-256 before predictions; bind that digest into the held-out lock outside its generic dependency hashes. The generic verify_lock function runs before evaluation's marker and must not read test labels. After the evaluator exclusively creates TEST_EVALUATION_STARTED.json, read label bytes once and compare their SHA-256 against the frozen expected value before decoding or scoring. A mismatch must burn the attempt, produce no result, and never permit an unamended retry. Add a synthetic valid-but-modified-label test. The existing malformed-JSON failure test is insufficient to detect this integrity gap.

No actual test labels, features, episodes, predictions or outcomes were opened during this review. No real freeze/predict/evaluate command was executed. Submitted scripts preserved in heldout_submitted/:

- prediction_stage.py SHA256 979dbb1f121f2beca664d75d6aa915feeeab6a95154169fd6f081bb7babf4767
- evaluate_once.py SHA256 8418bff40c0df70463875e002acfb6032c5b7b7770388355d2ab226b558b7857
- test_heldout_stages.py SHA256 3245475db7cbcf8630c26fc51ec23e06007db6fdcce5ffd3fbc300be80078404

## Otherwise passing review

The label-blind predictor reads frozen numeric snapshots, sanitized whitelist inputs and separate routing. It generates all nine registered model predictions plus two fixed baselines and does not select using test data. Its exclusive marker prevents alternate-output retries. Frozen dependency checks include code, protocol, authoritative test membership, train/development inputs and labels, audit status/hash, reader, schema, library versions, candidate parameters, selected development minima and all model files. Dependencies are checked again before committing predictions. Root must retain and supply the accepted lock/prediction hashes.

Evaluator requires a distinct root approval string before any label access. It validates lock/prediction hashes, selected-fit provenance and routing alignment before atomic marker creation. Result output is exclusive; marker is canonical beside labels and no exception removes it. A failure after first read is burned. Mode0400 is procedural/write protection, not isolation from the same OS owner.

Metrics match v1.1: episode-macro Euclidean and squared Euclidean error and root thereof; explicitly pooled median/p90 errors; episode-macro radius absolute error; all prespecified selected-arm and baseline paired episode improvements with median/range/wins; all three same-hyperparameter comparisons; fixed blocks retaining original membership after exclusions; prior-locked development residual envelopes; label-quality sensitivity without exclusion; exact strict attainment threshold and train/dev/test class support gates. No classifier, IID standard error, CI, bootstrap, tuning, reselection or additional fit occurs.

All six GO conditions are implemented: >=10% relative and >=.02 nm absolute primary reduction, strict improvement over both baselines, positive mean improvement in each of the three fixed blocks, >=60% strict eligible-episode wins and at least two positive same-hyperparameter comparisons. F-vs-C is separately descriptive. Empty blocks fail the block gate. Physical scan timing/freshness remains conditional; numeric recorded-scan proxy results cannot independently establish physical inference or saved scans.

## Synthetic evidence

Eight supplied tests pass independently (heldout_submitted_results.txt). Eight original tests pass (test_heldout_independent.py; heldout_independent_results.txt), covering all six GO gates individually, no test-based reselection, and marker existence before the first label read plus failure-burn/no-retry behavior. The latter run also discovers and reruns the eight imported supplied tests, for16 total tests; it is eight new tests, not16 new ones. All fixtures are temporary synthetic files; no real test file is used.
