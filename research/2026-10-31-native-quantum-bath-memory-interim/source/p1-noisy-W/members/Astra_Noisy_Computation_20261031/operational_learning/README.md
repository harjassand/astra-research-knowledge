# Operational spectral learning: independent construction

The main proof is in `theorem.md`. It defines a reusable spectral decision envelope, an adaptive cell-vertex certificate, an explicit bounded-noise spectral implementation, exact original-action accounting, a full-column baseline, and a hidden-rank-one impossibility argument.

The principal practical caveat is that a small learned envelope does not make an unseen global spectral mode experimentally distinguishable. The general action-noise theorem needs an approximately inverse-square-root-dimension noise floor; the numerical prototype uses the stronger fixed-operator calibration-error model.

## Reproducible commands

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python operational_learning/spectral_envelope_demo.py --n 32768
OPENBLAS_NUM_THREADS=1 python operational_learning/useful_failures.py
```

## Numerical record

The implicit physical model has 32,768 states and two controls. Its unperturbed margin is the minimum of seven affine functions. Small generic perturbations destroy the commuting algebra: H0 is diagonal with distinct entries, and H1 has every off-diagonal entry nonzero, so spectral projectors of H0 and H1 generate all matrix units. The learner sees only coefficient matvec functions and declared norm/noise bounds, not this decomposition.

- Learned 7 affine witness planes, storing 21 coefficient scalars, plus certificate metadata.
- Checked 16 final cell vertices; 23 spectral calls occurred overall.
- Those calls used 5,914 Lanczos steps and **17,612 original coefficient-vector actions**. Counts include expectation and residual actions and skip zero control coefficients.
- Full-column reconstruction would use 98,304 original coefficient-vector actions and store 3,221,225,472 dense coefficient entries. This baseline wins in query count in the smaller n=1024 record, so the method is not universally cheaper.
- Requested uniform margin error: 0.06. Final maximum cell-vertex certificate gap: 0.00676613.
- An independent 151 by 151 control grid, audited against the hidden generator plus an operator-norm perturbation bound, gives an envelope-error upper bound of 0.00829037. This grid is an audit, not the basis of the uniform theorem.
- After acquisition, 60 new linear-price/resource-polytope design tasks needed **zero additional physical actions**. The total LP time was 0.144 seconds in this environment; acquisition took 68.0 seconds. These timings are illustrative, not cross-method benchmarks.
- An independent generator-based regret upper bound over those 60 tasks was 0.02354545, below the requested 0.06 certificate.

The practical implementation is fully reorthogonalized randomized Lanczos with a published exact-arithmetic gap-free step count. It is **not** interval arithmetic; floating-point roundoff is audited empirically. The general bounded-query-noise construction in `theorem.md` is separate and deliberately more conservative. The coherent simulation must not be used as evidence of robustness to arbitrary per-query noise at the same amplitude.

`useful_failures.json` records three concrete failures: a zero-residual wrong eigenpair; endpoint samples that miss a new spectral mode at an envelope cell vertex; and a fixed rank-one mode completely hidden by allowed vector errors.

## Literature positioning

The closest geometric mechanisms are Rote's Sandwich approximation and Sandwich/Benson-type multiobjective approximation. The closest spectral solver comparators are Kelley cuts, Helmberg–Rendl spectral bundles, and stable randomized Lanczos. Historical novelty is **not** asserted. The useful result is an explicit construction linking experimental resolution, a certifiable learned representation, and a class of genuinely tractable later decisions.
