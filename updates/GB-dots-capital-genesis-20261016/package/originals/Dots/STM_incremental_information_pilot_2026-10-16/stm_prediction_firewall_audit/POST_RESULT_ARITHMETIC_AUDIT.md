# Independent reconstruction of released held-out arithmetic

2026-10-16 UTC. **PASS: 3,910 checks; no discrepancy found.**

This is independent arithmetic reconstruction on the **same** released and already-burned held-out records, not a new experimental validation, new test use for model choice, replication on new data, or significance analysis. Root explicitly authorized reading the now-released labels/predictions for this check. All prior no-access reviews remain preserved and accurate for their timestamps.

## Method and integrity

Original standalone script: `reconstruct_released_arithmetic.py`. Machine-readable findings: `released_arithmetic_check.json`. Execution log: `released_arithmetic_check_log.txt`.

The script uses JSON, hashlib, math and NumPy. It does not import train, prediction_stage or evaluate_once; it never invokes the evaluator, any predictor, fitting function or model. It reads existing frozen files and writes only new audit artifacts in this audit directory. No marker, locked artifact, model or input was modified. No acquisition, tuning or extra model was performed.

Verified the root-supplied hashes:

- Held-out lock: 3b87badab6afb6c954dd47fb239f911b68c3b64e58b1cde55333ab984ea6a936
- Predictions: 7563650baeb98d1f38729391ff4bc1daee9eea2b513c3ba1b003036137bf5f20
- Result: 9996114c744bf58c1fa68c0d3e227c4e7e943b7fa77483b82caf4de5382a16e2

Also verified every held-out lock dependency hash, all nine model-file hashes, fit-lock self-binding and train/development input hashes, seal artifact hash, exact sealed-label bytes against both pre-prediction expected digest and result provenance, prediction-to-fit and prediction-to-lock bindings, and both canonical started markers' output/hash targets. Routing equality is exact. Predictions contain the two correct deterministic baseline arrays. Label radius and strict attainment labels agree with displacement and goal geometry.

All numeric comparisons use absolute/relative tolerance1e-12, except the protocol's radius-geometry consistency gate1e-9. Integer counts, IDs, hashes and booleans compare exactly.

## Reconstructed endpoint result

100 recorded-scan proxy rows across60 eligible test episodes. All three selected arms are candidate2 (ExtraTrees min_samples_leaf8), fixed from development.

Macro-episode endpoint errors, nm:

- A:0.217981137819830
- A+C:0.222734324944990
- A+F:0.223225105085671
- Persistence:0.862111655603673
- Command-request endpoint:0.149673829995918

A+F minus A is +0.005243967265841nm worse. Expressed as the predeclared improvement A minus A+F:−0.005243967265841nm, or−2.4056977% relative reduction. A+F strictly wins27/60 episodes (45%).

Fixed-block mean A-minus-A+F improvements, nm:

1. 2201–2391:−0.008348031151367
2. 2401–2591:−0.010339849875565
3. 2601–2791:+0.002955979229410

Same-hyperparameter A-minus-A+F mean improvements:

- Candidate1:−0.008440510768978nm
- Candidate2:−0.005243967265841nm
- Candidate3:+0.029224011400669nm

All six predeclared GO conditions are false: insufficient relative and absolute improvement; does not beat both baselines; improvement not positive in every block; fewer than60% strict episode wins; fewer than two favorable same-hyperparameter comparisons. **NO-GO is arithmetically correct.** A+F also does not improve on A+C.

Independently reconstructed all reported main metrics (macro Euclidean, macro squared/root, pooled median/p90, macro radius absolute error), per-episode results, label-quality strata, selected-arm/baseline paired summaries, same-hyperparameter pairs and their fixed-block counterparts. All match.

## Supplementary classification

The support gate passes. Negative/positive rows and distinct-episode support are:

- Train:329 negative rows/96 episodes;55 positive rows/55 episodes.
- Development:36 negative rows/19 episodes;36 positive rows/36 episodes.
- Test:45 negative rows/24 episodes;55 positive rows/55 episodes.

Counts reconstructed directly from labels and routing in each split, not just accepted from the fit summary. Episode counts can overlap between classes because an episode can contain both labels.

Test confusion counts (TP,TN,FP,FN):

- A:(28,26,19,27), balanced accuracy0.5434343434
- A+C:(26,28,17,29), balanced accuracy0.5474747475
- A+F:(28,29,16,27), balanced accuracy0.5767676768
- Persistence:(0,45,0,55), balanced accuracy0.5; precision undefined because no predicted positives
- Requested endpoint:(42,12,33,13), balanced accuracy0.5151515152

All sensitivity, specificity, precision and balanced-accuracy values match. These supplementary classification results cannot rescue the failed endpoint screen.

## Empirical residual envelopes

Reconstructed against the already-locked development q values; no radius was changed or refitted:

- A:q0.617666876754637nm;58/60 test episodes have every residual within q (96.6667%).
- A+C:q0.575019994511643nm;57/60 (95%).
- A+F:q0.582897539415188nm;57/60 (95%).

These are empirical residual envelopes, not confidence sets or guaranteed/conformal coverage. This post-result audit verifies use of the locked q and test fractions; it does not independently regenerate development predictions or refit/reselect any model.

## Interpretation boundary

The numerical outcome concerns prediction of recorded image-localization labels on the compatible serialized-new-image proxy subset. Physical pre-scan timing/freshness interpretation remains conditional on documented logger semantics. Arithmetic agreement does not certify physical freshness, current hardware calibration, causal current information, scan savings or safety. The negative screen supports no expansion of this exact prediction hypothesis on these data without a new plan.
