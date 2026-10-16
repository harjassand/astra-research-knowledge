# Independent aggregate-fit sensitivity audit

## Bottom line

The source data support selected directly measured QEC advantages, but the numerical Gaussian lifetime enhancement is materially dependent on the offset domain. The strongest concrete model obstruction is the combination of an unreproduced ambient QEC optimum without an additional offset restriction, and large standardized residuals for the injected physical comparator. Neither requires rejecting the measured finite-time differences.

This is an independent **sensitivity study**, not replacement experimental analysis, raw-count reconstruction, or calibrated uncertainty estimation. No author code was executed or imported. Input files are preserved in the source evaluator directory. Run `OPENBLAS_NUM_THREADS=1 python audit.py`; dependencies are NumPy and SciPy. `results.json` contains fitted values and directly paired differences; `profiles.csv` contains nuisance-profile objectives; `summary.txt` is the compact numerical listing.

## Objective and domains

For the displayed fidelity y_i and marginal error s_i, minimize Q=Σ[(a+c exp(−(t_i/τ)^2)−y_i)/s_i]^2. At each τ, solve the convex two-variable nuisance problem exactly by checking the unconstrained weighted-linear solution and all feasible edges. Search log τ from log(.001 ms) to log(100000 ms) on a grid and refine the best basin with bounded scalar minimization. The minima reported are interior in τ. Profile endpoints for Q_min+1 are root-refined. They describe objective curvature only: **they are not confidence intervals**, and Q is not established as a true likelihood.

Domains:
- Simplex: a≥0, c≥0, a+c≤1. This guarantees a monotone bounded fidelity curve; it does not certify a physical CPTP time-evolution family.
- Fixed a=.5: phase-randomized qubit identity-process-fidelity floor, conditional on an appropriate normalized pure-dephasing model with no extra leakage/other errors. It is only a conditional stress test for corrected or unnormalized data.
- Fixed a=.25: fully depolarized normalized qubit floor, conditional on that different channel model. It is a stress test, not a justified mechanism for this dephasing experiment. In particular the physical injected data strongly disfavor it under the displayed marginal-error objective.
- Diagnostic a≥.4: simplex with this additional offset restriction, included solely to check numerical consistency with the deposited ambient QEC coefficients. No source found here documents that bound. This is **not** a claim about the authors' actual fitting procedure.

For unnormalized data neither .5 nor .25 is a universal physical floor. Leakage and reconstruction conventions can change their meaning. Do not pool these models as equally credible choices or interpret their extrema as a statistical error bar.

## Reconstructing the deposited fits

Ten of twelve deposited (file,series) fits reproduce the independent simplex WLS optimum to numerical precision, including every physical and no-QEC fit and both injected QEC fits. Maximum lifetime differences are about 0.0002 ms, compatible with numerical optimizer tolerance. Thus there is no broad failure to reconstruct the stated WLS.

The two exceptions are ambient QEC:

| Representation | Deposited τ,a,Q | Simplex τ,a,Q | Diagnostic a≥.4 τ,a,Q |
|---|---|---|---|
| Normalized |42.66163,.4,23.66985|62.32911,0,16.02762|42.66166,.4,23.66985|
| Unnormalized |40.01463,.4,23.35659|59.16446,0,15.45433|40.01469,.4,23.35659|

The restricted problem reproduces the deposited result, while the larger domain does not. This is evidence of sensitivity to admissible nuisance offsets and is numerically consistent with an undocumented restriction; it cannot establish the authors' actual constraint, initialization, or revised methods. These substantive differences should not be attributed to a general WLS implementation mismatch. Rounded data, errors and unknown procedures still limit full reconstruction.

The simplex ambient QEC optima themselves reach our explicitly imposed a=0 edge: these longer fitted lifetimes should not be promoted as better-established measured lifetimes. The optimum moving from one offset edge to another exposes extrapolation sensitivity.

## Lifetime ratio and chosen .75 threshold

Each row uses the same stated offset domain for QEC and physical curves. Threshold time is τ sqrt[−ln((.75−a)/c)] where applicable, measured from the provided storage-time axis. All entries are sensitivity-model quantities; .75 is an evaluator choice.

| Noise, representation | Model | τ_QEC/τ_phy | .75 crossing QEC/physical (ms) |
|---|---|---:|---|
|Ambient normalized|deposited|1.4520|27.389 / 22.875|
||simplex|2.1214|28.568 / 22.875|
||fixed .5|1.2404|26.941 / 22.904|
||fixed .25|1.1288|27.973 / 25.626|
|Ambient unnormalized|deposited|1.4616|25.236 / 21.368|
||simplex|2.1610|26.508 / 21.368|
||fixed .5|1.2406|24.804 / 21.420|
||fixed .25|1.1156|25.855 / 24.235|
|Injected normalized|deposited/simplex|11.8686|7.619 / .823|
||fixed .5|11.1123|7.521 / .828|
||fixed .25|9.3669|8.586 / 1.058|
|Injected unnormalized|deposited/simplex|11.3615|6.516 / .833|
||fixed .5|9.6815|6.236 / .840|
||fixed .25|9.8793|7.356 / 1.134|

The .75 crossing comparison stays favorable across these particular alternatives, with ambient positive gaps 1.620–5.693 ms. This is useful but does not demonstrate robustness over all possible decay families, thresholds, noise processes, fit weights or reconstructions. Lifetime ratios vary much more than this finite-threshold comparison.

## Residual and precision obstruction

Deposited normalized/unnormalized physical objective values are ambient 33.998/37.312 for 8 observations, injected 543.243/488.984 for 18 observations. Normalized/unnormalized QEC values are ambient 23.670/23.357 for 8, injected 48.657/35.732 for 11. There are nominally three fitted parameters before constraints, but these should not be converted to calibrated chi-square tests: covariance, count-level distributions, repeated-batch structure and model adequacy are missing.

Fixing the injected physical floor to .25 worsens Q to 6694.443/5609.949. The .25 alternatives therefore should not be used to claim equally well-supported enhancement estimates. The large residual issue already exists with the best-fit free offsets, however; it is not caused solely by the floor stress test.

EDFig4b lists the initial physical fidelity as .993 with s=.00001, much finer than the three-decimal fidelity display. That point almost pins the amplitude+offset, and the aggregate precision is insufficient to reconstruct any unrounded high-precision datum. Its near-zero residual is not evidence that the printed value is an exact physical probability. No rounding-error Monte Carlo or fabricated shots were introduced.

## Fit-independent paired observations

Ambient at t=29.0445 ms: QEC−physical = +.078 normalized, +.065 unnormalized. Across all eight matched ambient times, each representation has four positive and four negative differences; there is no uniform measured ambient advantage.

Injected exact same-time pairs:

|t (ms)|normalized QEC−physical|unnormalized QEC−physical|
|---:|---:|---:|
|.7555|.209|.188|
|2.2365|.349|.322|
|4.458|.225|.215|
|11.1225|.162|.144|
|15.5655|.118|.095|

These five positive observed differences survive every fitting assumption above because no fit or interpolation enters them. They are not five independent certified successes, confidence statements, an across-noise threshold theorem, or evidence against an optimized dynamical-decoupling comparator absent from the experiment.

## Next evidence needed

Obtain the revised fitting specification, especially admissible offsets and error treatment; unrounded aggregates and joint bootstrap samples/covariance; and the underlying repeated experimental/count records. A matched controlled-memory comparator and independently varied noise/correction rates are separate experimental requirements. Replacing one Gaussian fit with more flexible functions cannot repair those missing identifiability and comparison conditions.
