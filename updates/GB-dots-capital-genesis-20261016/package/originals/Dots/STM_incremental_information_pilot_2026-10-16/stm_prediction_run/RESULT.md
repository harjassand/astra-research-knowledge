# STM incremental-information pilot: final held-out result
Date: 2026-10-16. Frozen protocol v1.1. Single joint held-out evaluation completed; all test outcomes are now burned.

## Decision: NO-GO
On the recorded-scan proxy subset, selected A+F has macro endpoint error **0.223225 nm**, versus **0.217981 nm** for A: **0.005244 nm worse (2.406% worse)**. All six prespecified research-screening conditions fail. The command-request baseline is best at **0.149674 nm**. Physical pre-scan timing/freshness interpretation remains conditional on the documented logger semantics; this is numerical prediction of recorded image-localization labels.

## Design, sample counts and execution record
A contains matched action/history, anchor/goal and radial-d features; A+C adds compact current descriptors; A+F adds sampled current traces to C. Each arm selected candidate 2 (512-tree ExtraTrees, minimum leaf size 8) using development macro endpoint error. All nine candidates were trained on train only, with equal episode weighting; no development refit. Candidate 1 uses minimum leaf size 2; candidate 3 uses two coordinate-specific HistGradientBoosting fits. The two deterministic baselines are persistence and latest stored command-request endpoint relative to the last measured anchor, not actual executed tip/atom position.

| Split | Planned episodes | Eligible episodes | Eligible boundaries |
| --- | --- | --- | --- |
| train | 120 | 120 | 384 |
| development | 40 | 39 | 72 |
| test | 60 | 60 | 100 |

Compatibility/eligibility gate PASS; no systemic schema failure and no schema exclusions. Acquired the 220 manifest files, 210,440,337 bytes, with exact size/Git-blob SHA1 checks and recorded SHA256; no retry/replacement or adaptive expansion. Development episode 1501 was excluded because its exact-image connected component touched burned diagnostic 1500. Test episodes 2661 and 2721 each record one missing-trace event and one dependent-boundary-without-anchor exclusion; fixed rules re-established anchors, with no outcome-based exclusion. Reused images supply no new labels. Changed-byte eligibility can omit genuine identical scans.

Pre-access changes: protocol v1.1 replaced an infeasible historical physical-freshness proof with documented-logger compatibility and mandatory conditional interpretation; split, features, models and metrics were unchanged. A missing prebound test-label digest in initial held-out stage scripts was corrected and old versions preserved before any real held-out operation; no model choice changed. No post-test rerun, refit, retuning, new acquisition or marker deletion was performed for this report. Report generation reads existing results only. The label seal and separate stages are procedural safeguards, not owner-proof OS isolation.

## Prespecified overall errors
All distances are nm; macro squared error is nm². Primary = mean of within-episode mean Euclidean endpoint errors, giving each eligible episode equal weight. Root macro MSE = square root of mean within-episode mean squared Euclidean error, not a pooled-row RMSE. Pooled median/p90 give every boundary equal weight. Target-radius error is the macro mean absolute error in distance to the reset goal. Every row below covers the same 60 episodes / 100 boundaries.

| Model | Primary | Macro MSE | √macro MSE | Pooled median | Pooled p90 | Target-radius MAE |
| --- | --- | --- | --- | --- | --- | --- |
| A | 0.217981 | 0.077035 | 0.277552 | 0.177781 | 0.412064 | 0.146989 |
| A+C | 0.222734 | 0.081409 | 0.285323 | 0.168446 | 0.419101 | 0.149562 |
| A+F | 0.223225 | 0.081659 | 0.285761 | 0.172705 | 0.431848 | 0.149198 |
| Command request | 0.149674 | 0.047107 | 0.217042 | 0.148385 | 0.274881 | 0.079372 |
| Persistence | 0.862112 | 1.055715 | 1.027480 | 0.552839 | 1.587304 | 0.751681 |

## Paired episode comparisons
Improvement = comparator error minus candidate error; positive favors the model named first. Summaries use 60 paired episode means. Strict wins exclude ties. Full individual-episode values are retained in test_result_once.json, including block and same-hyperparameter pairs.

| Comparison | Mean improvement | Median | Minimum | Maximum | Strict wins |
| --- | --- | --- | --- | --- | --- |
| A+C vs A | -0.004753 | -0.001008 | -0.135269 | 0.091800 | 48.33% |
| A+C vs Command request | -0.073060 | -0.050210 | -0.652719 | 0.242788 | 33.33% |
| A+C vs Persistence | 0.639377 | 0.533743 | -0.030249 | 1.578504 | 98.33% |
| A+F vs A | -0.005244 | -0.001932 | -0.161589 | 0.125628 | 45.00% |
| A+F vs A+C | -0.000491 | 0.000119 | -0.075273 | 0.040226 | 51.67% |
| A+F vs Command request | -0.073551 | -0.054657 | -0.650299 | 0.237273 | 35.00% |
| A+F vs Persistence | 0.638887 | 0.536319 | -0.028193 | 1.561787 | 98.33% |
| A vs Command request | -0.068307 | -0.062253 | -0.646223 | 0.236727 | 35.00% |
| A vs Persistence | 0.644131 | 0.533315 | -0.005030 | 1.586438 | 98.33% |

### All three fixed same-hyperparameter comparisons
These are descriptive checks of all frozen candidates, not a new test-time selection. Only candidate 3 improves A+F over A (1 of 3); the two ExtraTrees settings worsen it. Selected F does not improve on C (mean improvement −0.000491 nm).

| Candidate | Comparison | Mean improvement | Median | Minimum | Maximum | Strict wins |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A+C vs A | -0.009527 | -0.001617 | -0.422978 | 0.183699 | 48.33% |
| 1 | A+F vs A | -0.008441 | -0.001109 | -0.447420 | 0.228346 | 50.00% |
| 1 | A+F vs A+C | 0.001087 | 0.002916 | -0.070188 | 0.095111 | 56.67% |
| 2 | A+C vs A | -0.004753 | -0.001008 | -0.135269 | 0.091800 | 48.33% |
| 2 | A+F vs A | -0.005244 | -0.001932 | -0.161589 | 0.125628 | 45.00% |
| 2 | A+F vs A+C | -0.000491 | 0.000119 | -0.075273 | 0.040226 | 51.67% |
| 3 | A+C vs A | -0.000055 | -0.005287 | -0.529628 | 0.442671 | 46.67% |
| 3 | A+F vs A | 0.029224 | 0.042704 | -0.517094 | 0.533053 | 65.00% |
| 3 | A+F vs A+C | 0.029279 | 0.034108 | -0.171323 | 0.247952 | 70.00% |

## Fixed chronology blocks
Membership was fixed before test access; each block retains 20 eligible episodes. These are chronological sensitivity checks, not established physical tip/session regimes.

| Block / planned IDs | Episodes | Rows | A | A+C | A+F | Command request | Persistence | A+F vs A improvement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1: 2201–2391 | 20 | 26 | 0.226419 | 0.233824 | 0.234767 | 0.143622 | 0.963212 | -0.008348 |
| 2: 2401–2591 | 20 | 28 | 0.196703 | 0.207309 | 0.207043 | 0.095322 | 0.875403 | -0.010340 |
| 3: 2601–2791 | 20 | 46 | 0.230821 | 0.227070 | 0.227865 | 0.210077 | 0.747719 | 0.002956 |

Other blockwise mean paired improvements (same sign convention):
| Block | Comparison | Mean improvement |
| --- | --- | --- |
| 1 | A+C vs A | -0.007405 |
| 1 | A+C vs Command request | -0.090202 |
| 1 | A+C vs Persistence | 0.729388 |
| 1 | A+F vs A+C | -0.000943 |
| 1 | A+F vs Command request | -0.091146 |
| 1 | A+F vs Persistence | 0.728445 |
| 1 | A vs Command request | -0.082798 |
| 1 | A vs Persistence | 0.736793 |
| 2 | A+C vs A | -0.010606 |
| 2 | A+C vs Command request | -0.111987 |
| 2 | A+C vs Persistence | 0.668094 |
| 2 | A+F vs A+C | 0.000267 |
| 2 | A+F vs Command request | -0.111720 |
| 2 | A+F vs Persistence | 0.668361 |
| 2 | A vs Command request | -0.101380 |
| 2 | A vs Persistence | 0.678701 |
| 3 | A+C vs A | 0.003752 |
| 3 | A+C vs Command request | -0.016992 |
| 3 | A+C vs Persistence | 0.520650 |
| 3 | A+F vs A+C | -0.000796 |
| 3 | A+F vs Command request | -0.017788 |
| 3 | A+F vs Persistence | 0.519854 |
| 3 | A vs Command request | -0.020744 |
| 3 | A vs Persistence | 0.516898 |

## Fixed empirical residual envelopes
q was the linear 90th percentile of development episode-maximum endpoint residuals and was not adjusted on test. Each prediction uses the same radius q; coverage is the fraction of test episodes with every residual ≤q. These are descriptive empirical envelopes, neither confidence guarantees nor conformal coverage.

| Arm | Development q = mean radius (nm) | Test episodes fully covered | Fraction |
| --- | --- | --- | --- |
| A | 0.617667 | 58/60 | 96.67% |
| A+C | 0.575020 | 57/60 | 95.00% |
| A+F | 0.582898 | 57/60 | 95.00% |

## Supplementary target-attainment classification
Strict attainment threshold: radius <0.16627687752661222 nm (0.288√3/3). Predictions are deterministic thresholds of regressed endpoints; no classifier, probability, calibration or class rebalancing was fitted. Support passes: train and development each require ≥20 rows and ≥10 distinct episodes per class; test requires ≥15 rows and ≥10 episodes per class. An episode can contribute to both classes, so class episode counts need not sum to the split total.

| Split | Nonattainment rows / episodes | Attainment rows / episodes |
| --- | --- | --- |
| development | 36 / 19 | 36 / 36 |
| test | 45 / 24 | 55 / 55 |
| train | 329 / 96 | 55 / 55 |

| Model | Balanced accuracy | Sensitivity | Specificity | Precision | TP / FP / TN / FN |
| --- | --- | --- | --- | --- | --- |
| A | 0.543434 | 0.509091 | 0.577778 | 0.595745 | 28 / 19 / 26 / 27 |
| A+C | 0.547475 | 0.472727 | 0.622222 | 0.604651 | 26 / 17 / 28 / 29 |
| A+F | 0.576768 | 0.509091 | 0.644444 | 0.636364 | 28 / 16 / 29 / 27 |
| Command request | 0.515152 | 0.763636 | 0.266667 | 0.560000 | 42 / 33 / 12 / 13 |
| Persistence | 0.500000 | 0.000000 | 1.000000 | undefined | 0 / 0 / 45 / 55 |

Classification metrics are pooled-row statistics. Persistence predicts no positives, so its precision is undefined. A+F improves balanced accuracy over A (0.576768 versus 0.543434), but this supplementary result cannot rescue the failed primary endpoint.

## Forward/back localization-disagreement sensitivity
The frozen disagreement threshold is 0.16627687752661222 nm. All 100 test boundaries across all 60 episodes are above it; the at-or-below stratum has 0 boundaries / 0 episodes and its errors are unavailable. Thus the above-threshold results for all five models are exactly the overall table, with no lower-disagreement contrast possible. This raises label-quality concerns but is not grounds to remove rows, trim residuals or replace the primary analysis.

## Six frozen research-screening gates
| Requirement | Observed | Result |
| --- | --- | --- |
| Relative primary reduction ≥10% | -2.406% | FAIL |
| Absolute primary reduction ≥0.02 nm | -0.005244 nm | FAIL |
| A+F beats both baselines | Beats persistence; loses to command request | FAIL |
| Positive A+F vs A in every fixed block | Negative in blocks 1 and 2; positive in block 3 | FAIL |
| Strict episode wins ≥60% | 45.00% (27/60) | FAIL |
| At least 2 of 3 same-hyperparameter improvements | 1 of 3 | FAIL |

NO-GO is for expanding this exact prediction hypothesis on these data without a new plan. This does not establish absence of all predictive current information or conditional mutual information: it is a fixed small-model/budget test. Even GO would only recommend a larger independently held-out study with better metadata; neither outcome authorizes extra downloads, deployment, scanning changes or scan skipping.

## Physical scope and limitations
- The unconditional finding is prediction of recorded labels in a selectively imaged Ag/Ag(111) subset. Interpretation immediately before already-triggered physical scans is conditional on documented logger timing/freshness. Serialized aliases and changed bytes do not prove physical scan freshness.
- Radial d is tip displacement from trace start, not cumulative travel or atom displacement. It is shared across arms; its pre-image timing has the same conditional interpretation. The archive lacks per-sample time and full XY/Z trajectories.
- Stored requests are pre-addition/pre-clipping, not certified executed coordinates. Numerical current uses source-implied A converted to nA; hardware gain, run-specific physical calibration and servo mode are unverified. Fixed-XYZ current readout and constant-current Z are not interchangeable.
- Exact image-component leakage control cannot exclude near-duplicates. Unknown tip/session boundaries, drift and chronological dependence preclude IID confidence intervals or significance claims; block checks are descriptive.
- No counterfactual controller claim, actual saved-scan claim, physical-safety guarantee, unique current-to-site inversion or generic novelty claim follows. Current-based motion/site readout predates this pilot.

## Provenance and read-only integrity verification
All five supplied SHA256 values below were recomputed from the existing files and matched. Reporting did not reopen raw test labels or perform inference/scoring. The result provenance binds the same held-out lock and prediction hashes. Original stage markers and frozen artifacts remain intact.

| Artifact | SHA256 |
| --- | --- |
| test_label_seal.json | f7040c21a1ea3fb0e67cc2ea3d7179755db4d36ce7fe87d54ad3e950a17fd8cc |
| heldout_lock.json | 3b87badab6afb6c954dd47fb239f911b68c3b64e58b1cde55333ab984ea6a936 |
| test_predictions.json | 7563650baeb98d1f38729391ff4bc1daee9eea2b513c3ba1b003036137bf5f20 |
| test_result_once.json | 9996114c744bf58c1fa68c0d3e227c4e7e943b7fa77483b82caf4de5382a16e2 |
| fits/fit_lock.json | 3e2ae20e8141e99eb9fb4486771b6d45d362d6078316aae2d81ad20c0db6d9bb |

Primary sources: test_result_once.json; fits/fit_lock.json; audit_report.json; PHASE_ONE_REPORT.md; HELDOUT_STAGE_HANDOFF.md; ../stm_prediction_protocol/PROTOCOL_v1.1.md. Pinned data source: https://github.com/SINGROUP/Atom_manipulation_with_RL/tree/ace9ca3f9be401bb9c8146d0bfc2882e87141f7e ; associated paper: https://doi.org/10.1038/s41467-022-35149-w .
