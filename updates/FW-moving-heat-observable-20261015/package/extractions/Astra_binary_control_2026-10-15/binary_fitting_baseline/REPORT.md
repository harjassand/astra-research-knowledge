# Reproducible binary inverse-model fitting baseline

Synthetic numerical experiment only. No hardware, measured-data calibration, installation, downloaded code, or outreach. Date: 2026-10-15.

## Bottom line

A small multi-start nonlinear least-squares baseline can recover full binary response tables from the proposed two-anchor O(m²) acquisition on these physically admissible examples. This is useful empirical support for local identifiability, but it is not a guaranteed global learner. At the same reading budget, random acquisition was more reliable under this optimizer and appreciably more noise-tolerant in this small ensemble. This does not establish universal superiority of random sampling or a negative identifiability result for two anchors.

With 12 starts and training-loss-only selection, exact full-table recovery (maximum absolute error <1e-7) succeeded on 11/12 two-anchor instances and 12/12 random instances. The lone two-anchor failure had a nonzero training residual, hence is an optimization failure, not an indistinguishable competing exact model. Oracle-near initialization solved every case to maximum full-table error <6.1e-12; this is a diagnostic, never counted as a deployable method.

With independent raw noise SD 0.001 and four repeats at every calibration setting, median heldout RMSE was 0.00919 for two-anchor and 0.00124 for random. The maximum heldout RMSE was 0.0160 versus 0.00156; maximum absolute error anywhere on the full table was 0.0576 versus 0.00544. Only two ground-truth seeds per dimension were used; these observations do not support population-level or hardware claims.

## Model and physical admissibility

The fitted response is g(S)=a_Sᵀ(I+B_SS)^−1 1 with diagonal B fixed to zero. For bookkeeping the synthetic raw reading is f(S)=0.3+g(S); changing this plus convention to f0−g changes only the sign of measured differences. Baseline and singletons are measured separately to obtain f0 and a; their noise is propagated into the subsequent joint-response fit. a is fixed after that calibration, not jointly refitted.

For each m=5,...,10 and seed=0,1, draw independent real Gaussian matrices and form H0=I+S+K, with S symmetric, ||S||₂=0.65, K skew-symmetric, ||K||₂=0.55. Thus sym(H0)>=0.35 I. Set t=1, L_ii=1+H0_ii, B_ij=H0_ij/L_jj for i!=j, and draw a_i uniformly on [0.5,1.5]. This is the normalization I+B=(I+H0)L^−1, without an additional gauge W. H0 is realizable as PᵀA^−1P with P=I and A=H0^−1 accretive. A suitable output linear functional can realize the independently chosen positive a.

The true full-system condition numbers range 1.386–1.774. The minimum verified weighted shifted margin of I+B is 0.719 over the ensemble. These are stable forward problems, but forward stability is distinct from inverse identification conditioning. The median truth acquisition Jacobian condition number is 698 for two-anchor and 534 for random, with respective ranges 543–2332 and 322–1143. No prior knowledge of the true margin or matrix is supplied to the practical fits.

## Schedule, reading budget, and holdouts

Two-anchor settings are all S with |S\{0,1}|<=2. The random comparator includes exactly the same empty set and all singletons and samples the remaining required number uniformly without replacement from subsets of cardinality >=2. Overlapping settings share the same simulated raw readings in the paired comparison. There are 12 independently generated ground truths, not 48 independent ground truths.

| m | Calibration settings Q | Baseline + singletons | Joint settings | Exact readings | Noisy readings (4 repeats) | Heldout settings |
|---|---:|---:|---:|---:|---:|---:|
|5|28|6|22|28|112|4|
|6|44|7|37|44|176|20|
|7|64|8|56|64|256|64|
|8|88|9|79|88|352|168|
|9|116|10|106|116|464|396|
|10|148|11|137|148|592|876|

Every nontraining subset is a heldout, and full-table errors include every one of 2^m subsets. These diagnostic truth values are evaluated from the synthetic generating model; they are not free physical validation readings. If implemented as exhaustive experimental validation, they would add 2^m−Q distinct settings (and the chosen validation repeats) beyond calibration. This exponential validation is deliberately limited to m<=10 and is not an acquisition algorithm. Restarts reuse readings, adding compute but no settings. No heldout reading participates in fit selection.

## Optimizer and reproducibility

NumPy 2.3.5 and SciPy 1.17.0, Python 3.12.14. Existing packages only. SciPy least_squares, trust-region reflective method, off-diagonal box bounds [-0.6,0.6], max_nfev=1000, ftol=xtol=gtol=1e-11. Twelve starts: zero and eleven independent Gaussian N(0,0.04²) initializations. For each setting solve x=(I+B_SS)^−1 1 and y=(I+B_SS)^−T a_S; the analytic Jacobian entry is −y_i x_j. The code batches masked full-size systems to keep every setting in a common array shape. An independent central finite-difference check has maximum absolute discrepancy 1.26e-9.

The box is an optimizer guard, not a passivity constraint or a certified model enclosure. All ground truths fit inside it. Every fitted model in this run nevertheless had positive Euclidean shifted margin (minimum 0.499), as checked after fitting. Least squares is unweighted: it does not exploit the correlated errors caused by the shared estimated baseline or jointly refine the singleton estimates. Such improvements remain untested and could change the comparison.

Run:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python benchmark.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python diagnostics.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python summarize.py

Main benchmark wall time: 44.1 seconds. Total optimizer time, all starts combined: exact two-anchor 11.44 s, exact random 9.30 s, noisy two-anchor 12.22 s, noisy random 9.86 s. These are local small-m timings, not a polynomial global-recovery complexity guarantee. The diagnostic/summarization scripts are separate. A preliminary three-start run is preserved in pilot_3starts; increasing starts materially improved exact success from 8/12 and 9/12, illustrating initialization sensitivity rather than just reporting an unfavorable first run.

## Fit success and nonuniqueness

Of the individual exact-data starts, 51/144 two-anchor and 69/144 random fits met the all-table 1e-7 criterion. Selected by minimum measured training loss, this became 11/12 and 12/12. Optimizer termination flags, evaluations, all-start errors, and residuals are all recorded; a positive SciPy success flag is not treated as correct global recovery.

The single remaining two-anchor failure is m=5, seed=0: training RMSE 9.30e-5, heldout RMSE 0.0172, full-table max error 0.0200. This does not supply an exact ambiguity example. All exact successful fits in this experiment are compatible with recovery of a response-equivalent branch; no claim that all possible exact branches have been enumerated is made.

The inherent weighted-transpose ambiguity B*=diag(a)^−1 Bᵀ diag(a) is explicitly checked on every full binary table: maximum difference <=3.6e-15, despite Frobenius parameter separation 0.832–1.350. For example m=5, seed=1, the selected exact two-anchor fit has parameter error 0.832 but predicts the entire table accurately. Parameter error to the generating B is therefore not a valid sole fit-success metric. Full response agreement here does not prove an unknown fitted model's interval enclosure or give a prediction certificate under future drift.

## Files and receipts

- benchmark.py: complete locally written generating/fitting source, fixed random seeds.
- diagnostics.py: truth Jacobian conditioning, weighted-transpose invariance, explicitly oracle-near initialization test.
- summarize.py: human-readable CSV exports.
- results.json: 576 individual fit records, including runtime, errors, success, parameter error, shifted margins, Jacobian rank/conditioning indicators, and budgets.
- selected_results.csv: all 48 selected model results, with heldout/full-table RMSE and max error and summed runtime across starts.
- all_table_selected_errors.csv: every selected model's per-subset prediction and signed error, with calibration membership.
- m*_seed*_noise*_{two_anchor,random}.npz: complete raw repeated synthetic readings, truth matrices, masks, training/heldout lists, parameters and full-table predictions/errors for every restart.
- diagnostics.json, audits.json, metadata.json, run.log: additional numerical receipts.
- pilot_3starts/: preserved pilot source and outputs.

The comparison reveals useful empirical structure: O(m²) two-anchor measurements often suffice for full-table prediction in stable generic examples, yet calibration geometry and optimizer branch behavior matter. It does not fill the unresolved global scaffold-acquisition theorem or establish a finite-noise uniform recovery guarantee. The separate exact schedule derivation belongs to ../practical_binary_schedule/RESULTS.md; this baseline neither replaces nor independently proves that algebra.

## Stronger noisy comparator added

See joint_raw_fit/REPORT.md for joint raw-mean fitting of f0,a,B using exactly the same readings and starts. That comparison removes frozen calibration estimates and should be preferred for practical interpretation: random still wins all 12 paired full-table RMSE comparisons, with median 0.000759 versus two-anchor 0.00652. It adds 288 optimizations and 33.38 seconds; prior results are preserved.
