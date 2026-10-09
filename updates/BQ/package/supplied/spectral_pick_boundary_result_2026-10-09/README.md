# Global positive spectral interpolation with unknown semicircular noise

Research deliverable, 9 October 2026. **Priority is provisional.** This package concerns an independently derived algorithm for an established inverse problem. It does not claim the first recovery of noise variance or of a sparse spectral law.

## Result in plain language

Suppose a probability distribution is an unknown finite-atomic spectral law blurred by additive semicircular noise. When its atom count k is known, k complex Stieltjes-transform values suffice for an exact constructive recovery: find the endpoint of a scalar positive-semidefinite feasibility interval, then solve one Hermitian eigenproblem. The output has real atoms and positive weights summing to one. There is no nonlinear search over atom locations or weights.

The proposed contribution is the particular **normalized Pick path and its global variance-endpoint theorem**. The exact finite-node theorem, backward Schur-series proof and constructive realization are in `CANDIDATE_THEOREM.md`. The proof credits classical Pick/Loewner tools, and the prior comparison credits classical Gaussian/Hankel boundary-variance estimation and Ying's same-model 2025 eigenmatrix method.

## Scope that matters

- The implemented estimator is **known k, m=k transform nodes**. All comparison methods receive the same known k.
- The exact variance theorem permits m>=k, so a known upper bound can suffice for variance identification in exact arithmetic. For m>k, the true Pick Gram matrix is singular; rank reduction is not implemented. No atom-count-free practical algorithm is supplied.
- The signal has k distinct atoms with positive weights. It need not have low matrix rank. Macroscopic spectral atoms and finite-rank spikes are different objects.
- Only the spectral distribution and noise variance are recovered. Eigenvectors and the underlying matrix are not recovered.
- The random-matrix interpretation assumes a deterministic signal matrix and independent additive GOE noise, in the large-N limit. Finite-N spectra are approximate model data.
- A non-atomic signal can contain its own semicircular component. Then the maximal removable variance may exceed the planted noise; that is a genuine identifiability ambiguity.
- Close atoms, tiny weights, wrong k and poor node placement can make recovery unstable. Ordinary floating-point signs near a PSD boundary are not a certified numerical bracket.
- No laboratory validation, downstream scientific discovery, external expert review, formal proof certification, or publication-priority certification is claimed.

## Evidence and strongest comparisons

`matched_comparison_results.json` and `matched_comparison_raw.npz` contain 16 fixed-seed N=1024 GOE trials: k=3 or 5, noise standard deviation .25 or .75, four realizations each. `finite_matrix_raw.npz` contains every source spectrum. The signal examples follow Ying's three- and five-atom families.

Every node design uses the **observed** spectral midpoint and halfspan, never true atom locations or a true spectral scale. The candidate takes k upper-half-plane nodes. The eigenmatrix baseline uses 32 conjugate pairs on an enclosing ellipse. Full nonlinear forward fitting uses 32 upper-half-plane nodes, analytic derivatives, four independent noise-scale starts and an additional candidate warm start. A separate four-start fit uses exactly the candidate's k nodes.

The same-k-node nonlinear fit agrees with the candidate on all 16 trials. This confirms that the deterministic construction reaches the same positive interpolant, rather than improving error by changing the target. The 32-transform full fit has lower median Wasserstein-1 error in all four scenario groups; the candidate is **not a universal accuracy improvement**. The five-atom/high-noise case remains poorly resolved by all tested methods.

Mean spectral Wasserstein-1 errors (candidate; 32-node full fit):

- k=3, noise SD .25: 0.000880; 0.000547
- k=3, noise SD .75: 0.01208; 0.01187
- k=5, noise SD .25: 0.001266; 0.001178
- k=5, noise SD .75: 0.09691; 0.09496

Candidate transform evaluation plus inversion took about 1.8–2.2 ms in these small-k prototype runs. The fastest independent single 32-node fit that matched the best multistart objective took roughly 7–21 ms, selected retrospectively. Complete multistart and eigenmatrix timings, all initialization costs, convergence diagnostics and raw results are supplied. These do **not** establish a universal matched-error speed factor. The baseline is an independently implemented version of Ying's algorithm, with disclosed numerical choices, not author-certified code or a claim to its best possible performance.

Input to each solver is the already-computed spectrum. Matrix construction and its eigendecomposition are shared upstream costs and are recorded separately; they can dominate the full pipeline. Matrix-free trace estimation is not implemented.

## Stability and failure evidence

`STABILITY_AND_FINITE_N.md` is a separate derived note: local variance stability has a positive, data/model-dependent boundary slope. An elementary fixed-node GOE transform bound scales as 1/N only in the conservative high-imaginary region eta^2>t. The adaptive-node experiments are not covered by that fixed-node confidence statement. No empirical confidence interval is marketed as theoretically certified.

`correctness_and_adverse_results.json` records:

- Exact 3- and 5-atom inversion checks, plus coincident transform values
- Analytic full-forward Jacobian versus central differences (maximum error 2.1e-11)
- Boundary derivative versus its atomic formula and finite differences
- Double-precision failure as atoms coalesce
- Strong sensitivity to an incorrect model order
- Rejection of an invalid normalized Pick covariance, with no silent PSD repair

## Reproduction

Python 3.12, NumPy 2.3.5 and SciPy 1.17.0 were used; exact platform details are in `environment.json`. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 python pick_inverse.py
OPENBLAS_NUM_THREADS=1 python finite_matrix_test.py
OPENBLAS_NUM_THREADS=1 python eigenmatrix_baseline.py
OPENBLAS_NUM_THREADS=1 python direct_fit_baseline.py
OPENBLAS_NUM_THREADS=1 python matched_comparison.py
OPENBLAS_NUM_THREADS=1 python correctness_and_adverse.py
```

The first finite-matrix exploratory scripts used fixed test geometry. The final `matched_comparison.py` replaces that geometry with the observed-scale rule described above and is the comparison to use. No random seed is tuned to select favorable runs.

## Review and preservation status

One focused AI-assisted mathematical check has completed, covering the exact theorem, positive realization, the stated conditional stability/GOE calculations, existing implementation tests, and closest primary prior art. It found no load-bearing mathematical error in those scoped claims. This is not external expert review, formal verification, or priority certification. See FOCUSED_CHECK_2026-10-09.md and CHECK_MANIFEST.json. No additional audit is implied.

`pick_candidate_snapshot_2026-10-09T1334.zip` is an immutable pre-check historical snapshot. Its `PRIOR_BASELINE.md` contained an overbroad atom-count-free phrase, corrected in the current report with a dated notice. Do not use that historical phrase as a capability claim. Earlier fragmentation archives are separate and unchanged.
