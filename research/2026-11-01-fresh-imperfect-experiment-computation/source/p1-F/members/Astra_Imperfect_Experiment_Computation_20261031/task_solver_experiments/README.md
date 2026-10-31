# Noisy task-triggered Galerkin acquisition — executed comparisons

These are synthetic finite diagnostics of the construction in `research/PROOF.txt`. They do not establish historical novelty, universal superiority, physical experimental cost, or floating-point correctness for every input.

## Reproduce

Run, with NumPy and SciPy available:

```bash
OPENBLAS_NUM_THREADS=1 python task_solver_experiments/noisy_galerkin_benchmark.py
OPENBLAS_NUM_THREADS=1 python task_solver_experiments/check_affine_noncommuting.py
```

The first writes `benchmark_results.json` with all task-level records. The second writes `affine_noncommuting_results.json`. The recorded wall times include checker operations and are not practical performance comparisons.

## Main experiment and equal-information comparisons

The fixed source has dimension 160 and is `A=0.2 I+B`. Its four dominant eigenvalues are 4, 2, 1, 0.5. A dense, positive, generically full-rank tail on the dominant-subspace complement has norm `tau/8=0.0004901960784313725`. Thus B has full rank. The learner receives neither the dominant basis nor its dimension.

There are 80 tasks. The first 55 right-hand sides exclude the fourth dominant eigenvector. Task index 55 (the 56th task) deliberately excites it. Subsequent tasks are generic. The source reports `Bv+tol Fv` for one fixed nonsymmetric matrix F of norm one. This is correlated deterministic noise satisfying the action contract; it is not averaged away.

Target relative solution error is epsilon=0.02. All methods use the same explicit residual certificate, `tau=mu epsilon/(1+epsilon)` and `sigma=tau/16`, with mu=0.2. Every cache column and transient orthogonal right-hand-side direction is queried at `sigma/sqrt(cap)`. The power-of-two capacity is the least power at least rank+1. All capacity-triggered remeasurements count.

| Method | Full-vector source actions | Final retained rank | Precision proxy, sum tol^-2 | Maximum actual relative error |
|---|---:|---:|---:|---:|
| Adaptive action-image cache | 92 | 4 | 7.9403328e9 | 0.00168049 |
| Identical method reset for every task | 691 | 0 | 4.20155136e10 | 0.00381090 |
| Raw solution snapshots | 1192 | 80 | 1.560849696e12 | 0.00821671 |
| Affine-correction snapshots `x-b/alpha` | 103 | 4 | 8.8725312e9 | 0.00678657 |
| Gaussian range, 8 columns | 96 | 8 | 2.55688704e10 | 0.00639042 |
| Gaussian 8-probe SVD proposal, threshold tau/4 | **92** | **4** | 1.331712e10 | 0.00641899 |

**The strongest ordinary comparator ties the adaptive construction on source actions and retained dimension.** The conservative precision proxy differs because the adaptive cache remains smaller during the first part of the stream; this is not a proof that its precision allocation is optimal or that it wins physically.

The SVD threshold supplies only a candidate basis. It never certifies that a discarded component is absent: every subsequent task still has the full residual check and may enrich. The 8-probe count and threshold are fixed rules, not chosen from access to the hidden rank.

These randomized baselines retain a range and check each task. They are not a globally certified Nyström approximation capable of returning all later answers without a source call. Such a method is a stronger potential competitor, with its own noise-aware global certification bill. Ordinary Krylov recycling can also adopt the same cache construction and tie it.

### What happened at the late direction

The adaptive cache had rank 2 after task 0 and rank 3 after task 1. It remained rank 3 through task 54. Task 55 failed its check, acquired the fourth direction, refreshed all four columns at the smaller tolerance required by capacity 8, and completed. It used six actions on that task. Later ordinary tasks used one action each.

Thus the source remains live: a fresh right-hand side usually needs one directly prepared transient action. There is no zero-source-call deployment claim.

### Verification scope

For the adaptive run, the maximum actual error-matrix norm divided by sigma was 0.511973. The minimum appended image separation was 0.03833294, above the required `tau-2sigma=0.00343137255`. The maximum basis orthogonality defect was 6.81e-16. All methods' true solution errors were independently checked against direct source-matrix solves and satisfied their declared tolerance.

The learner's choices do not access the true matrix or true errors. Checker matrices are used only to verify the synthetic results. Source calls made by a checker are not confused with charged learner action calls; the checker computes directly from the constructed synthetic source.

## Accuracy tightening makes the hidden tail relevant

After the main adaptive run, the same rank-four cache is reused for 12 additional right-hand sides supported in the tail subspace. The requested epsilon is tightened from 0.02 to 0.00025. This changes tau to `4.9987503124218944e-5`, much smaller than the old source tail norm.

The cache first **remeasures all four retained columns at the new precision**. Those four calls and their precision costs are included. It then enriches once per new task, growing from rank 4 to rank 16. Including the initial precision refresh, later capacity refreshes, and every trial, the challenge costs 62 additional full-vector source actions and precision proxy `1.180237897728e14`. The maximum true relative error was `2.9600010780169236e-6`, within the newly requested tolerance.

This is an explicit failure of treating the old tail as exactly absent. The algorithm handles it by spending additional information and precision, not by claiming the old representation remains sufficient at every accuracy.

## Two noncommuting primitive operators

The separate extension uses n=128, k=2 and 40 changing affine tasks. The two PSD primitives have a common four-dimensional dominant subspace, but their dominant restrictions do not commute. Each also has an independently generated dense positive tail on the **full ambient space**, of norm tau/8; consequently the small perturbations do not preserve an exact common four-dimensional invariant subspace.

The mixture theta lies in the probability simplex and depends on the preceding computed answer. Both primitive actions are acquired and retained on every cache direction, and each current weighted action is assembled from the actual individual noisy reports. The learner receives no dominant basis.

Results:

- Commutator operator norm: 1.4953321104771744.
- Outside-dominant-subspace operator norms: 0.00048946549 and 0.00048908344, each below tau/8.
- Total source actions: 104, comprising 52 from each primitive.
- Final cache rank: 4.
- Retained basis and primitive-action entries: 1536 scalars.
- Precision proxy: 1.24182144e10.
- Maximum true relative solution error: 0.00916024, within epsilon=0.02.
- Maximum individual error-matrix norm/sigma: 0.485236.
- Maximum weighted error-matrix norm/sigma: 0.329389.
- Minimum appended image separation: 0.00788976, above 0.00343137.

This resolves the finite implementation risk of combining individually cached primitive actions under changing noncommuting mixtures. It is not an empirical assertion about arbitrary sources or arbitrary precision.

## Finite arithmetic and cost qualifications

The proof in `research/PROOF.txt` is a real-arithmetic theorem with external action noise. The code uses double precision and two-pass orthogonalization. A transient vector is omitted only below `16 * machine_epsilon * n * norm(b)`. This is a floating-point implementation decision, not mathematical evidence of exact dependence. The root proof's explicit preparation-aware cutoff is a separate analytical variant; this diagnostic implementation does not claim a complete validated-rounding theorem.

`sum tol^-2` is an explicitly declared proxy for precision-sensitive experimental work. It is not a measured time, number of repetitions, energy, or monetary cost. Fixed biased error does not automatically improve by repeated averaging. Full-vector preparation, n output coordinates per source action, retained n-by-r arrays, small dense solves and numerical arithmetic remain real costs.
