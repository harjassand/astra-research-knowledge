# Independent substantive review: general extremal recovery-face acquisition

2026-10-28, reviewer `producer-workspace/review_general_face`.

**Disposition: cleared at the explicitly conditional finite-dimensional mathematical and acquisition-interface scope below.** This is independent internal scientific review, not formal proof verification, historical-novelty clearance, end-to-end solver benchmarking or an efficient architecture claim. The governing manuscript deliberately retains its original author-unreviewed label; this receipt is the separate scoped review record.

## Claims checked

1. The leakage block argument is valid: PSD factorization bounds cross-block Frobenius mass by `(d-t)t`; the orthogonal remainder has squared norm at most `2dt-t²`; support TP injectivity and partial-trace norm `sqrt(k)` yield `G=2d(1+k/sigma²)`. Complementarity plus the strict off-support dual gap proves full-CPTP uniqueness and global quadratic growth, not merely optimality within the exposed support.
2. The fitted-objective perturbation proof gives distance to **every** actual optimizer at most `G_c e/mu_c`, and actual calibration objective regret at most `G_c e²/(4mu_c)`. The different constants are correct. Future objectives do not inherit the latter quadratic regret merely by sharing an optimizer.
3. The ordinary IC input/output dual-frame estimator in section 3a is unbiased for each conditional native objective. Its coordinate martingale radius is conservative and valid. The target is the predictable bank average, which inherits a single common conditional optimizer. Private fresh choices and an initially independent probe are load-bearing; no environment preparation or full environment reconstruction is assumed. Bias is separately paid. Summable bank failure budgets close the repeated-acceptance issue.
4. Rank enumeration includes the true extreme rank because TP support injectivity implies rank at most d. Guarded PSD truncation and input-side partial-trace normalization are physically CPTP. At the true rank, a nonzero spectral floor yields convergent support. The fixed-support exact-kernel dual parameterization is valid, even though its fitted objective need not be a physical native objective.
5. Conditional completion is justified: an empirical primal-dual certified gap bounds proposal distance; support convergence preserves injectivity; near-identity ambient unitary transport of the true slack gives a nearby feasible fitted objective with a positive gap. This transport is an existence witness for fitting, not an assumed physical operation. The manuscript explicitly requires a fixed limiting objective, or suitable uniform replacements; arbitrary drift alone does not imply acceptance.
6. The rational strict primal/dual enumeration fallback is a valid computability mechanism under algebraic inputs and vanishing tolerances. It does not claim polynomial complexity. For the dual fit, bounded caps or feasible-point enumeration suffice; no attainment of a potentially nonclosed-image least-squares infimum is required. Strict margins permit certified finite checks. Hardware synthesis and control errors remain additional obligations.
7. The half-diamond channel substitution bound follows from the unnormalized Choi trace-norm bound and `||J||_1 <= sqrt(dk)||J||_F`. It is operation-only and composes by a hybrid argument. It does not establish future high fidelity, capacity, or source-membership promises.
8. The flagged-loss qubit-to-qutrit fixture is a physical strict rank-two full-CPTP oracle. Its TP support Gram has eigenvalues `{1/2,1,1/2,1/2}`, hence G=30. The dual positive spectrum `{2s,s(1+s),1+s,p}` is strictly positive for `0<p<1`, and the unique optimal fidelity is `(1+s)/2`. It is not perfect error correction. Unknown fixed receiver orientation and varying flagged-loss probabilities preserve the promised common recovery in the stated family.

## Challenges raised and resolved during review

- Initial acquisition wording supplied only a concentration interface. Requested an actual IC dual-frame estimator, correct filtration and fresh-input assumptions; section 3a now supplies them.
- Requested confidence valid across repeated bank acceptance, rather than pointwise confidence after adaptive selection; summable failure budgets are now explicit.
- Requested removal of implicit global optimizer attainment for dual fitting; feasible residual acceptance and expanding bounded caps/enumeration are now explicit.
- Challenged empirical SDP oracle treatment; the author added dense rational strict primal/dual witnesses and certified finite objective-gap search, while keeping the efficiency disclaimer.

## Reproducible checks

- Independently reran the author's exact SymPy fixture after its complex-convention extension. All four rational flagged-loss settings, 36 feasible competitor mixtures, TP-normalization fixture, real unknown orientation, complex Choi identity and exact IC input reconstruction passed.
- Wrote and ran the separately bound independent NumPy convention test: 60 complex random native/recovery pairs over `(d,k)=(3,2),(2,3),(4,2)`. Kraus and Choi entanglement-fidelity objectives agree to worst absolute error `1.1105279146216472e-16`; native swapped-transposed Choi identities pass. These floating tests guard conventions, not the universal theorem.
- No cvxpy installation is present in this environment. No empirical-SDP runtime, numerical rank-selection reliability or complete laboratory execution benchmark is represented by this receipt.

## Scope not cleared

No favorable high-dimensional sample or computation scaling; no separation from equally informed conventional process acquisition plus recovery SDP; no proof of a common future optimizer from finite past data; no generic unknown-noise preservation; no memory threshold; no historical priority claim. Generic native process statistics are still acquired, though the complete environment is not reconstructed. The useful new cleared interface is general nonunitary extreme-recovery robustness and conditional finite acquisition, beyond the earlier restricted extractor family.

## SHA-256 bindings

- `general_extremal_recovery_face_acquisition_20261028.md`: `c0c9d2af5c7b51e913657f342b6f0771ef82f136be65a2e26183ef55ec04312c`
- `general_extremal_recovery_face_exact_20261028.py`: `ebee80375377c8ec404d4e79b46641af94c2afdda14284b6000e750c010d1b5b`
- `general_extremal_recovery_face_exact_20261028.json`: `0fbbb5845e66fd6596bb1bb9a3cf38fb2d68631e650a9ecdc3ca9c918a38c474`
- `general_extremal_recovery_face_independent_check_20261028.py`: `798270e5593fde0ed64e1e1054db939a1890bb64bf2e6ecf50cc3357f9912b00`
- `general_extremal_recovery_face_independent_check_20261028.json`: `997fa442ad02099a247e99b752760f1e61e1d3f87916abfa37c1bab4c012c30a`
