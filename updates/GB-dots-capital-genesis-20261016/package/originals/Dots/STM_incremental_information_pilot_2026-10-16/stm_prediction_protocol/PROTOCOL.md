# Frozen STM incremental-information pilot, v1.0

## Status and estimand

Prepared 2026-10-16 using the existing inventory, published source text, and three already-burned diagnostic summaries only. No additional episode was acquired, decoded, or scored; no model was trained. This is a locally frozen preregistration, not a time-stamped external registry. Changes after freeze require a dated amendment that preserves these files and states whether any new outcomes were accessed. A future run needs authorization and the compatibility gate below. This document does not authorize execution.

Primary question: at an already-triggered STM scan boundary, after the executed manipulation and its recorded current have been acquired but before imaging, does current add predictive information about the next image-localized two-dimensional displacement, beyond the last genuinely measured position/goal and matched action/history information? Secondary question: does it improve image-coordinate target-error prediction? Target attainment is supplementary and conditional on adequate class representation.

This is an observed, selectively imaged-subset prediction experiment on Ag/Ag(111), not a counterfactual controller evaluation, physical safety guarantee, proof of saved scans, unique current-to-site inversion, or novelty claim for current-based site inference. Published motion detection and current-to-site readout precede this work. In particular, the Stroscio/Celotta Science 2004 fixed-XYZ current readout and Hla et al. PRB 2003 Ag manipulation/Z-trace work prevent a generic novelty claim. Constant-current Z and fixed-XYZ current signals are not interchangeable. Instrument servo mode is not documented here. The archive discards per-sample time and full XY/Z trajectories; radial d does not restore them.

## Pinned inputs and strict execution gates

Repository: https://github.com/SINGROUP/Atom_manipulation_with_RL at ace9ca3f9be401bb9c8146d0bfc2882e87141f7e. Paper: https://doi.org/10.1038/s41467-022-35149-w . Inventory and source provenance are in the sibling stm_control_logs directory. Hardened reader is in stm_reader_audit/safe_reader.py. Do not execute author code, import serialized globals, use pickle.load/loads, or enable NumPy pickle. Use installed NumPy 2.3.5, SciPy 1.17.0 and scikit-learn 1.8.0 only; no new installation.

Before acquisition/training, a separate auditor must document why the archived logs are compatible with the inspected measurement/logging implementation: meanings and timing of start state/goal, current/d, image creation/reuse, coordinate frame, and averaging of forward/back localizations. A commit containing files and matching schema is evidence of consistency, not proof that every historical run used that implementation. The current reader audit explicitly leaves physical freshness unknown. If historical compatibility cannot be established from documentation/provenance, stop: no qualified pre-scan inference test. A future exploratory serialized-image endpoint study would require its own amended claim and authorization; do not silently substitute it.

Conditional on that gate, require forward AND backward image objects to be new relative to the preceding image pair, with at least one pair member's bytes changed. Reject mixed identity changes, copied/ambiguous arrays, nonfinite/missing coordinates, incompatible frame/shape, malformed episodes and missing traces. Reused image pairs supply no new labels; retain their intervening actions and traces. Exclusion because of changed bytes is conservative and may omit genuinely identical new scans; state this selection explicitly. Neither identity nor byte changes alone certifies physical freshness. Do not infer no motion from reused coordinates.

At reset, use the documented measured start position even if its scan was inherited from the preceding episode, only if no unlogged manipulation occurred after that measurement. Reset pullbacks can occur outside the logged transitions; reject starts whose provenance cannot establish a measured post-reset state. No position history is stitched across episodes.

Static source establishes d timing conditionally: Env_new.step obtains current_series,d from step_latman before check_similarity/scan; step_latman constructs d=sqrt((x-x[0])²+(y-y[0])²) from acquired tip channels. Thus d is radial tip displacement from its trace start, not cumulative travel or atom displacement. Require compatible lineage, finite nonnegative aligned current/d lengths; do not assume d is monotonic. d is shared by every fitted arm, including action-only. Failure to verify pre-image d timing stops this frozen design rather than introducing asymmetric inputs.

## Frozen acquisition and episode split

The accompanying split_manifest.json is authoritative. Whole episodes only, never randomly split transitions:

- Train: 1,11,...,1191 (120 episodes; 135,509,332 bytes)
- Development: 1401,1411,...,1791 (40 episodes; 30,906,682 bytes)
- Test: 2201,2211,...,2791 (60 episodes; 44,024,323 bytes)
- Burned diagnostics: 0,1500,2920; never train/development/test
- Unused boundary guard intervals: 1192–1400 and 1792–2200, inclusive

New payload total: 210,440,337 bytes. Existing diagnostic payload: 2,449,226 bytes. Combined: 212,889,563 bytes. Use decimal MB. Hard acquisition ceiling is 350,000,000 bytes, counting all future received episode payload bytes including retries; no archive-wide download, extra neighbors, replacements, or adaptive expansion. Verify each planned file's exact size and Git blob SHA-1 (SHA1 of `blob <size>\0` + bytes); also compute SHA-256 on receipt. A mismatch aborts that file, with no automatic substitute. Download budgets are payload budgets; HTTP headers are not included. No new episode payloads have been fetched for this protocol.

Auditor alone computes SHA-256 over image dtype, shape and canonical numerical bytes for every start, transition and end image, separately for forward/back, in selected and burned episodes. Images, fingerprints, image provenance IDs, episode IDs and absolute chronological indices never enter predictor arrays. Connect episodes if ANY forward or backward image fingerprint is shared (not only entire matching pairs); take transitive components. Exclude every selected episode in a component touching burned diagnostics or more than one split. Also exclude later duplicates within each split, retaining the smallest episode ID per connected component. Never reassign or replace. This conservative rule may drop train episode 1 if it shares diagnostic 0's image. Guard gaps reduce inheritance risks but do not replace the hash audit. Record audit counts without exposing outcomes to the modeling process. Hash equality is a leakage control, not freshness evidence; near-duplicates cannot be ruled out by exact hashes.

Retain the original manifest unchanged; create separate derived eligibility/audit files. If fewer than 80 train, 25 development or 35 test eligible episodes remain, or fewer than 100/30/40 eligible scan boundaries respectively, declare this pilot infeasible without inspecting model scores. No outcome-based episode exclusion, residual trimming, terminal-only selection, or enlargement.

## Sample clock, label and feature firewall

For every eligible already-triggered scan, create one row. Let p be the latest measured two-dimensional atom position before that scan, g its reset-defined goal, and H the complete executed action/trace prefix since that measurement through the current manipulation. Initial p comes from episode_start_info.info.start_absolute_nm. Following an eligible fresh scan, advance p to that scan's atom_absolute_nm. If a later boundary has an ambiguous intervening scan, reject dependent rows until a genuinely measured anchor is re-established. No current-row state/info object is passed wholesale to feature code.

Primary label is Δ=p_next−p in nm from the post-scan averaged forward/back absolute localizations. Continuous secondary label r=||p_next−g||; attainment y=1[r<0.288√3/3 nm], strictly. Record forward/back disagreement ||p_next_f−p_next_b|| as audit/label-quality output only. Do not exclude high disagreement post hoc. Report errors separately for disagreement ≤threshold and >threshold, clearly as label-quality sensitivity, not adjusted primary results. Absolute-coordinate drift/frame compatibility is a gate, not silently corrected with future image information.

Allowed predictive inputs only: p; g−p; previously measured forward/back disagreement; executed normalized six-component action vectors; stored pre-addition/pre-clipping start_nm/end_nm requests; finite pre-image radial d traces; current samples in the current arms; and summaries of this prefix. No nominal voltage/current conversion without run-specific support. Do not use an image or its extent as a feature. The action-only model may use sample counts derived from d (shared current/d acquisition length) to prevent current length alone masquerading as current-value information. Historical positions/rewards outside this measurement interval are not inputs.

Explicitly prohibited: reward, done, current/post-scan states or coordinates, current/post-scan distance, images, terminal fields, scan trigger reason, freshness/hash/object IDs, episode identifier, time/regime index, future actions, future episode length and any audit or eligibility flags. No label may be used to tune features. Unit tests must mutate all prohibited fields while keeping authorized inputs fixed and verify identical feature values; labels are separately write-protected to the evaluator for test. Audit routing keys are allowed for joins and per-episode aggregation but are stripped before fit/predict.

## Fixed feature maps

All calculations use finite float64. No clipping/winsorization learned from test, interpolation over missing values, or zero-fill for unknown measurements. Every eligible action in H contributes; history is never truncated. Sample position means normalized array index, never elapsed time. Define S(v) as [first,last,mean,population-standard-deviation,min,max,q10,median,q90,mean(abs(diff(v))),max(abs(diff(v)))]; use linear quantiles, and zero for difference summaries of a length-one array. Require all traces length≥2. Define B32(v) as 32 equally spaced linear-interpolation samples from normalized indices [0,1]. Signed current is retained, expressed as numerical nA by multiplying source-implied A values by 1e9; report that hardware gain calibration is unverified.

Shared action/d vector A:
1. p_x,p_y,(g−p)_x,(g−p)_y,||g−p||, prior measured forward/back disagreement, and number of actions in H.
2. For each action, construct 10-vector [normalized six action components, requested start x/y, requested end x/y]. Include first and latest vectors, componentwise sum/mean/population-std/min/max across H, and each component linearly interpolated to 16 evenly spaced action-index locations (repeat if H has one action). Include current-request end−start x/y and its norm.
3. For each d trace compute S(d), length, and sum(abs(diff(d))). Include the latest vector and componentwise sum/mean/std/min/max over all H; include B32 of latest d and B32 of all d arrays concatenated chronologically. This concatenation is an index summary, not a physical continuous trajectory.

Simple-current increment C: for each trace compute S(I), length-normalized counts of abs(diff(I)) greater than 3 and 6 times max(MAD(diff(I)),1e−6 nA), signed median(second half)−median(first half), and max absolute deviation from its median divided by max(MAD(I),1e−6 nA). Include latest summaries and componentwise mean/std/min/max across H. Split halves at floor(n/2). MAD is median absolute deviation, unscaled. Spike/change summaries are descriptors, not hop counts.

Full-current increment F: C plus B32(latest I), B32(concatenated chronological currents), and B32 of each respective trace after subtracting its median and dividing by max(MAD,1e−6 nA). For the concatenated normalized trace, normalize each constituent trace before concatenation. This is a small fixed sampled-trace model, not a trained neural sequence encoder. Freeze these features before any new outcome access; richer models require another study.

No learned feature selection. All fit-time transforms, if required for numerical implementation, are fitted on train only. Both coordinate targets use the same features; no rotation inferred from post-scan images or lattice registration is allowed.

## Eleven predeclared model choices and selection

Two deterministic physical baselines:
- Persistence: Δ_hat=(0,0).
- Command-request endpoint: Δ_hat=latest stored end_nm, added to p. This uses the last observed anchor, not a sum of requested endpoints. Requests are pre-addition/pre-clipping, so label it requested endpoint, not actual executed tip or atom endpoint. Do not invent unknown clipping limits.

Nine fitted candidates: three identical estimators applied separately to A, A+C, A+F:
1. ExtraTreesRegressor(n_estimators=512,min_samples_leaf=2,max_features=1.0,bootstrap=False,random_state=20261016,n_jobs=1).
2. Same with min_samples_leaf=8.
3. Two independently fitted HistGradientBoostingRegressor models (one per coordinate), max_iter=300,learning_rate=.05,max_leaf_nodes=15,min_samples_leaf=10,l2_regularization=1,early_stopping=False,random_state=20261016; all other parameters pinned sklearn defaults.

Eleven model choices total including deterministic baselines. No classifier fitting, extra seeds, model stacking, tuning sweeps or test-time ensembling. Each training row has weight 1/(number of eligible rows in its episode), normalized to mean 1. Pass identical weights to all fitted estimators. Train candidates on train only. Select one model per arm by lowest development macro-episode Euclidean endpoint error; ties within 1e−9 nm choose order 1,2,3. Do not refit on development. Report fixed baselines and all three selected arms in the single held-out evaluation. Primary comparison is A+F versus A; A+C is a prespecified secondary ablation. Report all three same-hyperparameter paired comparisons descriptively to reveal capacity/tuning artifacts, without choosing the best test pair.

Training and development budgets are exactly equal across arms. Feature dimensionality differs by design, not estimator hyperparameters. These comparisons support incremental predictive value at this model/budget, not proof of conditional mutual information or absence of all action confounding. An installed library failure stops that model with a documented error; do not substitute an unregistered estimator.

## Metrics, uncertainty and one test use

For each row compute e=||Δ_hat−Δ|| in nm; average e within each episode and average those episode means (primary). Also report macro-episode mean squared Euclidean error and its square root, pooled median/90th-percentile endpoint error with clear pooled weighting, and macro-episode absolute target-radius error | ||p+Δ_hat−g||−r |. Report paired per-episode improvements and their median/range, episode-level win fraction, and sample counts. No IID standard errors, confidence intervals, random-transition bootstraps, or conformal-coverage claims across drifting tip regimes.

Before opening test, partition its fixed ID list into three predetermined blocks of 20 planned episodes each (2201–2391,2401–2591,2601–2791). Keep original block membership after exclusions. Report blockwise macro errors and mean paired improvement. These are chronology sensitivity checks, not known physical tip regimes. Unknown tip/session boundaries remain a limitation. No block-dependent tuning.

For each selected arm, report a descriptive development-residual radius: take each development episode's maximum endpoint residual and its linear 90th percentile q. On test report the fraction of episodes with every residual≤q and mean radius q. Call this an empirical residual envelope; it is neither a guaranteed confidence set nor conformal coverage. Do not adjust q after test.

Supplementary classification uses only y_hat=1[||p+Δ_hat−g||<threshold], no probability/calibration claim. Report balanced accuracy, sensitivity, specificity and precision only if train and development EACH contain ≥20 rows of each label across ≥10 distinct episodes per label, and test contains ≥15 rows of each label across ≥10 distinct episodes per label. Test support is checked by evaluator before displaying classification metrics. If the requirement fails, report support counts and classification unavailable; do not resample, rebalance or change threshold. Do not convert the residual envelope into success probabilities.

Lock candidate parameters, selected arms, train-only fits, development q values, code hash and feature schema hash before one joint test evaluation. Auditor may inspect test schema/hashes and label support only for predetermined gates; modeling agent receives no test outcomes, distributions, plots or examples beforehand. A result file is created once. Numerical/implementation bugs require an explicit invalidation/amendment; never quietly rerun and select favorable results. All test outcomes are burned after first score.

## Go/no-go for further research

Gate failure, insufficient eligibility, incompatible source timing/freshness, ambiguous frame, leakage-audit failure, unbounded parser behavior, unexpected content mismatch, or unregistered feature dependence means NO-GO for this protocol. Stop before model scoring when possible.

Conditional on gates passing, GO means all of: primary A+F reduces test macro endpoint error versus selected A by ≥10% relative AND ≥0.02 nm absolute; A+F beats both persistence and command-request endpoint on that metric; improvement is positive in each of the three chronological test blocks; and at least 60% of eligible test episodes have strictly lower mean error than A. Also require at least two of the three same-hyperparameter A+F vs A comparisons to improve overall, to guard against one selected fit. No significance claim is attached to these screening thresholds. Classification is not a gate and cannot rescue a failed primary endpoint result. Simple-current results distinguish compact descriptor value from additional sampled-trace value; no claim of benefit from F beyond C unless its paired macro error is lower.

Otherwise NO-GO for expanding this exact prediction hypothesis on these data without a new plan. A GO authorizes only recommending a larger independently held-out study with better source/tip/measurement metadata. It does not authorize more downloads, hardware deployment, scanning changes or prospectively skipping scans. Publish negative and inconclusive findings and the selected-subset limitation equally.
