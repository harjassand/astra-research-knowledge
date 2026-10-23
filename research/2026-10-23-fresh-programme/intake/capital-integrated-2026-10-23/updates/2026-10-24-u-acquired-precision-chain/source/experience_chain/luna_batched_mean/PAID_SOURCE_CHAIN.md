# Paid source to new-operator precision chain

**Status:** one reproducible synthetic chain executed; theorem is conditional on the stated linear-Gaussian interface. This is not a physical experiment, a new PCA method, or evidence of broad scientific-learning superiority.

## What is learned and reused

The fixture has `n=64`, `d=63`, `r=3`, known `b=e1`, `delta=1`, and `sigma=0.15`. A hidden, fixed, exactly rank-3 subspace `T` lies in `b-perp`. Each source or target task draws a fresh unit vector `v` isotropically within `T` and defines a **new** operator

```text
u = (b+v)/sqrt(2),   A_v = I + delta*u*u^T,
x_v = A_v^-1 b = (1-beta/2)b - (beta/2)v,   beta=delta/(1+delta)=1/2.
```

The learned object is the orientation of `T`, which is shared across tasks. The learner receives no `T` or `v`. It pays for a noisy output at `b`; from the returned full vector `y`, it forms `z=(2/delta)P_(b-perp)(y-b)=v+eta`. All source exposures are `m_source=128`, so `eta` has covariance `tau_source^2 I`, `tau_source^2=4 sigma^2/(delta^2 m_source)`. Each query returns all 64 coordinates and costs 128 unit-probe exposures.

Source directions are independently drawn when the next paid call is requested. Their direction RNG and the Gaussian noise RNG use separate independent streams, so the full source direction sequence is independent of the full source-noise matrix. Future directions and target noise use separate streams. The RNG seed values are evaluator-private and are not learner/control inputs. All future tasks use new `v` and new `A_v`; the shared subspace persists and there is no reset operation. The hidden-space promise and task distribution are supplied. Only its orientation and whether observed source calls cover it are acquired.

## Certificate and audit trail

At each `K_j=32*2^j`, the procedure forms

```text
C_hat = Z Z^T/K - tau_source^2 I,     S_K = V V^T/K,
Delta = a_G + b_W,
a_G = 2*tau_source*(sqrt(r)+sqrt(d)+t)/sqrt(K),
a_W = (sqrt(d)+t)/sqrt(K),
b_W = tau_source^2*(2*a_W+a_W^2),
t = sqrt(2*ln(3/alpha_source,j)),
alpha_source,j = 0.02*6/(pi^2*(j+1)^2).
```

The selected procedure uses the same-event observed-radius sharpening confirmed by the independent formula audit:

```text
h = max(0, lambda_max(C_hat)),
e_obs = min(Delta, b_W + a_G^2/2 + a_G*sqrt(h+b_W+a_G^2/4)).
```

It opens the rank-3 coverage gate when `lambda_hat_3 > e_obs`, then certifies `s <= e_obs/lambda_hat_3`. The original fixed `Delta` and `Delta/lambda_hat_3` are retained at every identical checkpoint as a conservative reference. The sharpening is a data-dependent radius derived on the same Gaussian event; it spends no additional confidence allocation. The independent audit is preserved in [POSITIVE_PROCEDURE_AUDIT.md](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_hidden_state/POSITIVE_PROCEDURE_AUDIT.md).

I initially raised a possible missing source-design term, reading the source target as the population covariance `P_T/r`. That objection was resolved before the run: the certificate targets the *empirical* `S_K=VV^T/K`. Since all unit `v_i` lie in `T`, `S_K` is supported in `T` and has rank at most `r` deterministically; no population-covariance approximation is used. Weyl's inequality and the noise-only radius then certify `rank(S_K)=r` when the gate opens, which implies the observed source vectors span all of `T`. The projector residual gives `||P_hat-P_T||_op <= e_obs/lambda_hat_3`. The gate remains closed/inconclusive for a rank-below-3 instance. This executed fixture has exact rank 3.

The audit requires: a shared stable `T`; unit source/future directions; source directions independent of the complete source-noise matrix; common known source exposure and calibrated `delta,sigma`; and fresh target noise independent of source data. The target identity is exact, and its squared error is bounded by

```text
beta^2*s^2/4 + sigma^2*Q_r(alpha_t)/((1+delta)^2*m),
Q_r(alpha)=r+2*sqrt(r*ln(1/alpha))+2*ln(1/alpha),
alpha_t=0.02*6/(pi^2*t_index^2).
```

For each target tolerance `epsilon`, the algorithm first upgrades source data until `s<=epsilon/beta`, then selects the smallest integer exposure `m` for which the displayed bound is at most `epsilon`. A failed gate or a gate with insufficient precision requires another paid source checkpoint; every acquired observation remains charged. There is no drift or off-class guarantee.

## One growing chain

The run has 1,536 held-out target operators in three consecutive blocks of 512, with requested solution tolerances `0.15`, `0.10`, and `0.06`. For each block, it first acquires enough source data, runs that block of targets, then upgrades source data before the next block. It uses cumulative source checkpoints rather than restarting or reacquiring old observations.

| Source K | `lambda_hat_3` | Fixed `Delta` | Observed `e_obs` | Fixed `s` | Observed `s` | Evaluator projector error | Decision |
|---:|---:|---:|---:|---:|---:|---:|---|
| 32 | 0.26830 | 0.12735 | 0.08986 | 0.47466 | 0.33492 | 0.07907 | Coverage gate opens; insufficient for 0.15 |
| 64 | 0.27581 | 0.09225 | 0.06262 | 0.33448 | 0.22703 | 0.04969 | Use for 0.15; insufficient for 0.10 |
| 128 | 0.29152 | 0.06597 | 0.04317 | 0.22631 | 0.14810 | 0.03622 | Use for 0.10; insufficient for 0.06 |
| 256 | 0.29715 | 0.04699 | 0.03013 | 0.15814 | 0.10139 | 0.02740 | Use for 0.06 |

The evaluator-only projector error is computed with the hidden `T`; it is not learner input. It was below both reported bounds at all four checkpoints. The independently computed SVD projector differed from the symmetric-eigendecomposition projector by at most `1.1e-15` in max absolute matrix entry. Coverage gates were open at every checkpoint; the `K=32` checkpoint and the two later cross-block reuse decisions were insufficient for their requested source precision. The selected blocks use `K=64`, `128`, and `256` respectively, with the old data retained at every upgrade.

The probability statements above are theorem-level under the stated Gaussian model and the scheduled alpha allocation. The implemented covariance, eigenvalue, and gate calculations use ordinary float64 arithmetic without outward rounding or a formal numerical enclosure, so the code does not supply a machine-verified roundoff certificate.

On these same observations, the original fixed `Delta` precision radius would miss the first block's source threshold at `K=64` (`s=0.33448>0.30`) and the second block's at `K=128` (`s=0.22631>0.20`), while the observed radius passes at those respective checkpoints. At `K=256`, fixed `Delta` also misses the final threshold (`s=0.15814>0.12`) while `e_obs` passes (`s=0.10139`). No `K=512` source data were acquired, so the subsequent fixed-radius checkpoint is unmeasured; the comparison is limited to the identical acquired checkpoints.

| Requested `epsilon` | Target count | Source K | Target exposure range | Mean target exposure | Sum of target exposures | Policy mean error | Policy p95 / max | Policy outputs within epsilon |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.15 | 512 | 64 | 6–15 | 13.9375 | 7,136 | 0.03497 | 0.05626 / 0.07519 | 512/512 |
| 0.10 | 512 | 128 | 34–36 | 34.9902 | 17,915 | 0.02189 | 0.03519 / 0.05208 | 512/512 |
| 0.06 | 512 | 256 | 104–108 | 105.8340 | 54,187 | 0.01297 | 0.02109 / 0.02921 | 512/512 |

The largest policy error was `0.07519`; the calculated theorem-derived bound was below its requested tolerance at every target. These are one deterministic synthetic realization, not a repeated-trial estimate. The realized source-checkpoint allocation sum is `0.0173090`; it is a diagnostic only and is not a stopping-valid failure bound. The policy could inspect any of 12 scheduled checkpoints, whose alpha allocations sum to `0.0190278342`; the target allocations over all 1,536 target indices sum to `0.0199920869`. Thus the conservative scheduled union-bound budget is `0.0390199211` (and is at most `0.04`).

## Same-history controls

All controls receive the same source observations, target observations, target exposures, `T`-rank promise, and model constants. The exact match between eigen-PCA and independent SVD PCA is the important comparison: these are the same standard rank-3 PCA estimator, and their per-target estimates agree up to floating-point roundoff. It is an established method independently matching the proposed estimator cheaply, not a rejection of the valid paid-source procedure.

| Method | Mean error | p95 | Maximum | Within tolerance by stage (`0.15 / 0.10 / 0.06`) |
|---|---:|---:|---:|---:|
| Policy eigendecomposition PCA | 0.0232745 | 0.0490603 | 0.0751851 | 512 / 512 / 512 |
| Independent SVD PCA | 0.0232745 | 0.0490603 | 0.0751851 | 512 / 512 / 512 |
| Empirical-Bayes/Wiener positive-part covariance shrinkage | 0.0259896 | 0.0499269 | 0.0761570 | 512 / 512 / 512 |
| Unpooled full-space target estimate (ablation only) | 0.1062318 | 0.1778353 | 0.2547803 | 142 / 255 / 360 |

The Wiener control uses the positive eigenvalues of the same noise-corrected source covariance and the target's known measurement variance. It is a useful equal-data estimator control; no finite-sample success theorem is claimed for that shrinker. The full-space row is an ablation at the selected low-dimensional method's target exposures, not a competent retaining incumbent and not a separately optimized cost baseline.

## Full acquisition and computation accounting

| Resource | Count |
|---|---:|
| Paid source queries / distinct source operators | 256 |
| Paid source exposure | 32,768 |
| Paid target queries / distinct new target operators | 1,536 |
| Paid target exposure | 79,238 |
| Total paid queries / total exposure | 1,792 / 112,006 |
| Returned scalar coordinates (`64` per query) | 114,688 |
| Raw float64 source / target observation arrays | 131,072 B / 786,432 B |
| Compressed public source / target NPZ archives | 126,668 B / 757,147 B |
| Retained source covariance / rank-3 basis | 31,752 B / 1,512 B |
| Raw source + covariance + basis, if retained | 164,336 B |
| Full eigensystem transient storage (eigenvectors and values) | 32,256 B |
| Source `Z` working array at final checkpoint | 129,024 B |
| Source covariance recomputation proxy across `K=32,64,128,256` | 1,905,120 multiply-adds |
| Covariance/eigendecomposition checkpoints and independent SVD checkpoints | 4 / 4 |
| Target PCA projection proxy (`2*d*r` per task) | 378 / task; 580,608 total |
| Target Wiener projection proxy (`2*d^2+d` per task) | 8,001 / task; 12,289,536 total |

Wall-clock timings are retained in the JSON only as local diagnostics, not as performance claims. The evaluator scored 6,144 estimate vectors (393,216 coordinates); this hidden-truth scoring is not a learner observation. The learner-facing interface is [public_manifest.json](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_batched_mean/public_manifest.json) plus the source and target observation archives. The private seeds and hidden evaluator truth are held in [the evaluator-only seed manifest](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_batched_mean/private_evaluator_seed_manifest_DO_NOT_PASS_TO_LEARNER.json) and [the evaluator-only truth file](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_batched_mean/private_evaluator_truth_DO_NOT_PASS_TO_LEARNER.npz). A previous version wrote the seed manifest under the public-looking filename `seed_manifest.json` and repeated seeds in the result JSON; those names were superseded and the bytes were retained under private filenames. Details and hashes are in [INTERFACE_REPAIR_PROVENANCE.md](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_batched_mean/INTERFACE_REPAIR_PROVENANCE.md). The learner interface receives only public constants, paid `y` arrays, exposures, and order.

## Interpretation

This is a constructive paid chain in which a statistically certified source subspace lets one estimate new operators with target-noise dimension `r=3`, rather than repeatedly treating each target as a `d=63` direction. The acquired shared subspace is useful for future tasks under this exact stable-subspace promise. The same evidence and basis are available to a conventional retaining controller; in this run, standard SVD-PCA reproduces the point estimates exactly. The result therefore supports the conditional operation and its explicit precision/exposure frontier, not superiority over competent PCA, novelty, or external scientific usefulness.

## Reproduction and data

Run `python3 paid_source_chain.py` from this directory to regenerate the synthetic fixture and evaluator report. The public learner inputs are `public_manifest.json`, `public_source_observations.npz`, and `public_target_observations.npz`; the evaluator writes its seeds and latent truth under `private_evaluator_*_DO_NOT_PASS_TO_LEARNER` names. The result JSON is an evaluation report, not a learner input. The original exact finite-field frontier remains in [RESULT.md](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/next_unit/experience_chain/luna_batched_mean/RESULT.md) and is unchanged.
