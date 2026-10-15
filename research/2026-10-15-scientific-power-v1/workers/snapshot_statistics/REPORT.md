# Snapshot-score statistical acquisition plan

15 October 2026. Bounded statistical side analysis of the three-snapshot operation in `research/2026-10-15-operational-closure-v1`. Status: **SCOPED_STATISTICAL_PLANNING_ONLY**. This is a fixture-specific calculation, not a new physical lead, an experiment, or evidence of a physical reversal.

## Result

For the exact three-state ring fixture, a predeclared fixed-score e-process gives a materially tighter finite-sample sufficient plan than the earlier Hoeffding-radius calculation. At the selected fixed lag `t=1/4`, score center `r=9/10`, and half-deficit threshold `u=-20503/10000000`, the plan is **27,000 iid stationary triplets** for a 5% test size and at least 95% power under the exact iid fixture law. Its unrounded Bernstein sufficient count is 26,594; the reported count is rounded upward to 27,000 after a 1% numerical pad and a generous 1,000-triplet increment. The exact interval-moment calculation leaves 0.09006 slack in the Bernstein inequality after its explicit numerical guard.

This is a threshold-specific test, not a confidence sequence over every possible score mean. If a study might choose between the separate zero-mean and half-deficit tests after seeing the data, it must allocate a joint error budget (for example, by Bonferroni); otherwise one test must be named as primary in advance.

## Fixture and test

The checked generator is

```text
Q = [[-21/20, 1,    1/20],
     [ 1/20, -21/20, 1   ],
     [ 1,     1/20, -21/20]]
pi = (1/3, 1/3, 1/3), labels = (0,1,1), t = 1/4, r = 9/10.
```

For ordered binary triplets `000,...,111`, the fixed score is

```text
W = Y0 (Y_- - r)(Y_+ - r)
W = (0, 0, 81/100, -9/100, 0, 0, -9/100, 1/100).
```

The exact fixture checker encloses the score mean at `-0.00410059931486791588734...`, so `D=-E[W]=0.00410059931486791588734...`. Its ideal-model all-even floor at this lag is `0.18653127301836...` nats per model-time unit. That is a result about the supplied mathematical law; it is not measured dissipation.

For a fixed null-mean threshold `u` and stake `lambda`, define

```text
E_n(u) = product_{i=1}^n [1 - lambda (W_i-u)].
```

For fixed `lambda >= 0`, when every factor is nonnegative and the null satisfies `E[W_i | past] >= u`, each factor has conditional expectation at most one. Thus `E_n` is a nonnegative supermartingale under the null, and Ville's inequality gives `Pr(sup_n E_n >= 1/alpha) <= alpha`. This is the standard nonnegative-supermartingale route to time-uniform tests; the specific factor here follows directly from the bounded score and the fixed null threshold. See [Howard et al., *Time-uniform, nonparametric, nonasymptotic confidence sequences*](https://doi.org/10.1214/20-AOS1991).

Power is planned under the **exact iid target fixture**, not an arbitrary alternative. Let `Z_i=log(1-lambda(W_i-u))`, with fixture mean `g`, variance `v`, and range width `R`. A one-sided Bernstein bound makes the test reach `E_n >= 1/alpha` with probability at least `1-beta` whenever

```text
n g - log(1/alpha) >= sqrt(2 n v log(1/beta)) + R log(1/beta)/3.
```

The selected threshold is a fixed rational slightly more negative than `-D/2`; the script verifies that relation against the exact deficit interval. Rejection of `H0: E[W] >= u` therefore tests for a deficit strictly larger than half the fixture's `D`. If the test rejects, the existing all-even theorem would imply a floor above `0.0921784407260...` nats per model-time unit, conditional on its assumptions. This is still a mathematical-model conclusion, not a physical measurement.

The cell probabilities come from the rational interval checker. Score values, stakes, and thresholds are exact rationals. Logarithms used in the power moments are enclosed by the atanh series, with its analytic remainder bound. Conversion to binary floating point is outward-rounded and guarded by relative/absolute pads; the final reported count also includes the explicit upward rounding described above.

## Acquisition counts and like-for-like correction

The previous `241,709` figure was for the same `t=3/10`, `r=9/10` fixture but only set a one-sided Hoeffding radius to `D/2`. It was not a power guarantee for a test or a confidence endpoint. At that legacy lag, a fixed rational threshold `u=-2241/1000000` is slightly more negative than `-D/2`. An e-process with `lambda=33/200` needs 30,085 triplets by the interval Bernstein calculation, reported as **31,000** after upward padding. A formally matched Hoeffding test at the same threshold, with 5% size and at least 95% fixture-specific power, needs **967,320** triplets.

| Plan or comparator | Gap and threshold | Triplets | What the number means |
|---|---:|---:|---|
| Earlier Hoeffding radius plan | `t=3/10`, radius `D/2` | 241,709 | A confidence-radius sizing calculation only; not a power guarantee. |
| Fixed-score e-process at the same legacy lag | `t=3/10`, `u=-2241/1000000`, `lambda=33/200` | 31,000 | 5% test size and at least 95% power under the exact iid fixture law. |
| Hoeffding test at that same legacy threshold | `t=3/10`, same `u` | 967,320 | 5% test size and at least 95% fixture-specific power. |
| Coarse lag/stake scan minimum | grid candidate `t=.247`, `lambda=.205` | 26,584 | Design-only floating-point scan; not the selected rational setting and not a global-optimum claim. |
| Selected rational lag and half-deficit test | `t=1/4`, `u=-20503/10000000`, `lambda=1/5` | **27,000** | Exact interval-moment Bernstein sufficient plan, padded upward; 5% size and at least 95% iid fixture power. |
| Separate zero-mean e-process test | `t=1/4`, `u=0`, `lambda=1/3` | **8,000** | 5% test size and at least 95% iid fixture power for rejecting nonnegative mean; not a half-deficit count. |
| Empirical-Bernstein plug-in geometry | `t=1/4`, fixed score | 13,577 | Uses the fixture population variance in the bound's sizing equation; the actual theorem uses observed sample variance, so this is not a power guarantee. |
| Full eight-cell LR projection geometry | `t=1/4`, all triplet cells | 35,944 | Finite-sample-valid projected confidence region, but with the expected cell table substituted for random counts; not a power guarantee. |

For context, the `t=1/4` Hoeffding half-radius plan is 288,618, while a Hoeffding test with the same fixed half-deficit threshold and separate 5% size/95% fixture-power guarantees needs 1,154,473. Comparing the 27,000 e-process plan to either radius-only count would mix promises; compare tests to tests.

The empirical-Bernstein comparator uses the fixed-score bound of [Maurer and Pontil, Theorem 4](https://arxiv.org/abs/0907.3740). The full-cell comparator uses the finite-sample multinomial relative-entropy tail bound of [Guo and Richardson](https://arxiv.org/abs/2003.08614), not a Wilks approximation. Their validity does not convert the plug-in counts above into power claims.

## Lag selection and strongest same-snapshot comparator

A design-only uniformization scan over gaps `0.010,...,0.900` in steps of `0.001` and stakes `0.005,...,1.230` in steps of `0.005` found its lowest fixture-specific half-deficit sufficient count at `(t,lambda)=(0.247,0.205)`. The nearby rational design `(1/4,1/5)` was fixed for the exact calculation and rerun through the interval checker. This is a finite coarse-grid search, not proof of a continuous global optimum. Choosing a lag or stake after observing study data would require a selection correction or independent design data.

The full eight-cell likelihood route is a valid same-record statistical comparator: retain all cell counts, form the finite-sample confidence set `C={q: n KL(p_hat||q) <= t_alpha}`, and maximize `q dot W` over `C`. Its reported 35,944 count is only expected-table geometry. The strongest equally informed comparator remains unresolved: profile the complete eight-cell likelihood over all compatible all-even hidden-CTMC/readout laws, and compare it with optimized reflected moments and other methods using the same raw snapshots, timing, preparation, calibration, and analysis budget. The hidden-model class has not been characterized computationally here, so no statistical superiority claim is made.

## Separate information lower bound

The sufficient count above is not a lower bound. A distinct information-theoretic bound is available for one specified pair only. Let `p` be the target ring's exact eight-cell law at `t=1/4`; let `q` be the exact law from the three-state equilibrium complete-graph CTMC with each off-diagonal rate `14/25`, the same stationary distribution and labels, and the same lag. For any test with size at most `0.05` at `q` and power at least `0.8` at `p`, data processing for KL divergence gives

```text
n KL(p || q) >= kl(0.8 || 0.05),
KL(p || q) ~= 0.0015666702388470377 nats/triplet,
kl(0.8 || 0.05) ~= 1.906442054182515 nats,
n >= 1216.875... , hence at least 1,217 iid triplets.
```

The cell law is enclosed by the exact rational checker; the displayed KL values use double-precision logarithms of those interval midpoints. This is a necessary lower bound against this one equilibrium null, not against every compatible hidden model, not a minimum for the score test, and not a lower bound on end-to-end physical acquisition cost.

## Gates and uncharged acquisition

These counts assume independent, identically distributed stationary triplets from the ideal mathematical law. They correspond to at least 81,000 binary snapshot readouts at 27,000 triplets, before charging stationary preparation, matched-clock calibration, detector setup, discarded or failed trials, and analysis. No readout bandwidth, real noise spectrum, missed-state response, detector memory, or back-action was measured. The checker supplies an idealized warning: 5% independent symmetric readout flips at each snapshot make the selected score mean positive (`+0.00542049...`), so more ideal iid samples cannot recover the negative-mean certificate in that noise case. At 2% independent flips the exact mean remains negative but shrinks to about `-0.0003438294`; this does not establish a practical noise tolerance.

No independent-preparation or dependence-control interface was acquired. Overlapping windows cannot be counted as iid triplets without a justified dependence model; the conditional-mean premise of the e-process would also need to be established. The all-even CTMC and physical-reversal premises remain unvalidated, and no physical reversal observable or independent energy/entropy ledger was obtained. The operational report's parity-lift countermodel shows why the binary record alone cannot validate that physical premise.

Thus 27,000 is a fixture-specific statistical sufficiency plan after the gates are met. It is not a run count already acquired, a device requirement verified against detector bandwidth, a complete experiment budget, a proof of physical reversal, or evidence of physical dissipation.

## Reproducibility

Run from the workspace root:

```sh
python3 -B research/2026-10-15-scientific-power-v1/workers/snapshot_statistics/stats_plan.py
python3 -B research/2026-10-15-scientific-power-v1/workers/snapshot_statistics/source/verify_snapshot_operation.py
```

The analysis imports only its bundled [`source/verify_snapshot_operation.py`](source/verify_snapshot_operation.py), a byte-identical copy of the operational-closure checker. `cmp` passed, and both source files have SHA-256 `02c76587799b84c5c3c8573e797fdf0a8f2b5aaaebad8e8d6f56488b80eacee1`. Outputs are in [`RESULTS.json`](RESULTS.json) and [`source/SNAPSHOT_EXACT_RESULTS.json`](source/SNAPSHOT_EXACT_RESULTS.json). The statistical script ran successfully after bundling; the exact checker ran successfully from the bundle and returned `PASS`.
