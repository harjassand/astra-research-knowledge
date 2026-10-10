# A finite-bit implementation on dense, noncommuting rational input

2026-10-10. This closes a concrete native-acquisition and finite-precision implementation obligation for the homogeneous zero-target sampler. It is a small, reproducible implementation prototype, not a new proof audit, a performance comparison, broad practical validation, or a novelty claim.

## Result

The saved raw input contains two dense 128-by-128 rational matrices. Their integer numerators are independent fixed-seed ±1 perturbations of 4096 I and 4096 X, where X swaps adjacent coordinates; their common denominator is 4096. Every entry is nonzero. The perturbations are arbitrary dense sign matrices, not low-rank perturbations or a recovered orthogonal-coordinate description.

The verifier uses the raw matrices to compute the exact Gram matrix H, its rational inverse, and Mp. An exact symmetric Gershgorin bound gives

    ||Mp||op <= 0.016060661951355255,
    r = 62 >= 4(m+1)^2 = 36.

The ideal acceptance lower bound is 1−2/62=30/31. The commutator is nonzero. Two rational dual vectors with exactly the same H-radius have disjoint certified determinant intervals. Thus the example is dense, noncommuting and angularly nonradial. Acquisition does not use a determinant identity, common diagonalization, hidden normalizer, or numerical eigenvalue estimate.

Three small end-to-end runs are preserved:

- `FINITE_BIT_DRAW.json`: epsilon=1/16, fixed replay seed 17391, T=23, primitive tolerance 2^-280, 388-bit normal-uniform cells, 581-bit precision-factor coordinates. Accepted on trial 1. Exact final residual zero. About 1.72 seconds before JSON serialization in the recorded run.
- `FINITE_BIT_SYSTEM_DRAW.json`: epsilon=1/16, OS-backed random-bit interface; its realized finite tape is preserved and replays exactly. Accepted on trial 1. Exact final residual zero. About 1.87 seconds before serialization.
- `FINITE_BIT_TIGHT_DRAW.json`: epsilon=2^-24, fixed replay seed 17391, T=63, primitive tolerance 2^-553, 757-bit normal-uniform cells, 1128-bit precision-factor coordinates. Accepted on trial 1. Exact final residual zero. About 5.08 seconds before serialization.

These timings are single observations, not benchmark statistics. Three first-trial acceptances do not establish the acceptance rate or distribution. Exact raw-input and interval certificates, rather than those outcomes, support the stated numerical checks.

## Implemented route

1. Load `RAW_INPUT.npz` and recompute the exact input certificate. The driver currently supports two 128-by-128 int64 numerator matrices with common denominator 4096, within the stated safe integer-product bound. It is not an implementation for arbitrary dimensions or all rational encodings. The native theorem threshold must pass. Commutation or density is not required by the sampler; those are demonstrated properties of the included example.
2. Compute all tail, trial-cap, chi-square, conditioning and acceptance-disagreement budgets with rational arithmetic. See `FINITE_PROBABILITY_CONTRACT.md` and `probability_budget.py`.
3. Generate finite Gaussian seeds from uniform cells. A directed integer Taylor/erf calculation and exact Machin bounds for pi certify the whole cell. mpmath proposes an initial quantile only; bounded ambiguity-safe bisection is the fallback. Endpoint and outer-domain seed cells have an explicit zero-output path charged to the normal tail event. The generator constructor also verifies exact a-priori finite-series and roundoff-majorant inequalities; the two exercised precision configurations are saved in `GENERATOR_MAJORANTS.json`.
4. Compute the proposal using a certified dyadic H Cholesky, an exact small rational solve, an integer-square-root interval for sqrt(r/V), and dyadic lambda rounding.
5. Form K=I+A_lambda A_lambda^T exactly. Compute a deterministic dyadic lower factor L, then certify its residual with exact integer products. Bound det(K) using det(LL^T) and that residual. Compute the rational squared-acceptance interval and compare it with a whole independent dyadic uniform cell. Overlap outputs zero; rejection advances to the next capped trial.
6. Solve L^T x=z with certified dyadic rounding. Check the rational separated condition F(x)F(x)^T >= 2tH exactly. Project the fresh finite Gaussian onto the fiber with an exact rational 2-by-2 Gram inverse. The final y is retained as a rational vector, giving F(x)y=0 exactly.
7. Enforce the output norm cap. Every fallback emits (0,0), which exactly satisfies the homogeneous target. The entry point defaults to OS-backed bits; `--seed` is an explicitly pseudorandom reproducibility mode.

The W1 conclusion is conditional on the stated mathematical transport/probability argument and independent-uniform-bit model. It is not inferred from the few saved samples. `FINITE_PROBABILITY_CONTRACT.md` spells out the argument, including the polar Gaussian coupling of approximate Cholesky factors. The code and numerical-majorant arguments have not received independent formal verification or specialist review.

## Deterministic Cholesky termination and precision contract

`rounded_cholesky` uses no floating-point factor proposal. Let K be rational SPD, K>=mu I, and Dmax bound its diagonal. Let u=2^-q. Every recurrence is evaluated exactly from K and the already-rounded dyadic entries.

For column i:

- The diagonal pivot before rounding is d_i=K_ii−sum_{k<i} L_ik^2. Set L_ii to the dyadic floor of sqrt(d_i), using an integer square root of a rational number.
- For j>i, round (K_ji−sum_{k<i} L_jk L_ik)/L_ii to the nearest dyadic multiple of u.

For a positive pivot, d_i<=K_ii<=Dmax and L_ii<=sqrt(Dmax). The completed diagonal residual is at most 2 sqrt(Dmax) u. A completed off-diagonal residual is at most sqrt(Dmax) u/2. Both are bounded by 3(Dmax+1)u.

Choose q so

    c u <= min(target,mu/4),       c=3n(Dmax+1).

The code finds such q by exact integer/rational comparisons. To justify that a pivot cannot fail, define the partially corrected symmetric matrix whose completed entries equal LL^T and whose unprocessed entries remain those of K. Its perturbation from K has operator norm at most n times the entrywise residual bound, hence at most mu/4. It remains at least 3mu I/4. Its already completed factor columns are exactly the computed columns. The next Schur-complement pivot is therefore positive and at least 3mu/4. The selected u is smaller than its square root, so its dyadic floor is also strictly positive. This induction excludes the code's positive-pivot assertions failing on valid inputs.

After all columns, ||K−LL^T||op<=cu<=target. The program separately recomputes the exact maximum absolute row sum of the final residual, so the saved bound does not depend on an assumed library rounding guarantee. Integer lengths and q are polynomial in input bit lengths, dimensions and requested precision.

For K=I+A_lambda A_lambda^T use mu=1 and Dmax=1+s, with s=lambda^T H lambda. For H use its exact rational lower spectral bound det(H)/||H||infinity^(m−1).

### Acceptance interval width

Write delta for the certified K residual. Since K>=I,

    (1−delta)K <= LL^T <= (1+delta)K.

Thus

    det(LL^T)/(1+delta)^n <= det(K)
      <= det(LL^T)/(1−delta)^n.

These are exact rational endpoints. The squared-acceptance interval is their reciprocal, multiplied by (1+s/r)^r, and intersected with [0,1]. The latter intersection is justified by the separately checked stable-rank envelope.

Choose delta<=rho^2/(16n). Then n delta<=1/16, (1−delta)^(-n)<2, and

    (1+delta)^n−(1−delta)^n <=4n delta.

The envelope implies the interval's un-clipped base multiplier is at most 2. Consequently its width is at most 8n delta<=rho^2/2. The code additionally checks the exact returned width is <=rho^2. Taking square roots gives a probability interval of width <=rho. There is no log-determinant/exponential cancellation in this decision.

## Deterministic triangular solve error contract

`solve_transpose` rounds each back-substitution coordinate to a dyadic grid of spacing u_x. Because later coordinates are already fixed, the residual in equation i is exactly the rounding error of that step times L_ii. Hence

    |(L^T xhat−z)_i| <= sqrt(Dmax) u_x/2,
    ||xhat−L^(-T)z|| <= n(Dmax+1)u_x/[2 sqrt(mu_P)],

where P=LL^T>=mu_P I. The chosen grid satisfies

    2n(Dmax+1)u_x/min(1,mu_P) <= rho.

This is more conservative than necessary and implies the distance is <=rho for every input satisfying the factor bounds, not only the saved tape. The implementation independently recomputes the exact squared residual and divides by mu_P; it asserts this rational upper bound is <=rho^2. The 2-by-2 H solve is exact and needs no rounding contract.

The final fiber projection uses exact rational arithmetic. There is no approximate inverse or residual tolerance hidden there. Its integer heights remain polynomial for this fixed small number of constraints; the resulting y may have a larger denominator than the dyadic x.

## Earlier local draw remains separately labelled

`certified_draw.py`, `CERTIFIED_DRAW.json`, `verify_draw.py`, and `SUMMARY.json` preserve the simpler U32/fixed48 local step. It already verifies raw acquisition, acceptance, Gaussian cells, covariance solve and residual, but it does not meet the global probability budget. `PROBABILITY_BUDGET.json` intentionally rejects promoting it to a full W1 draw. This separation is deliberate: the new high-precision capped driver carries its own evidence.

## Tests and reproducibility

No packages were installed. The recorded environment used Python 3.12, NumPy 2.3.5, SciPy 1.17.0 and the existing mpmath package; exact package versions are in `CERTIFIED_DRAW.json` and `ENVIRONMENT.json`.

Run from this directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python certified_draw.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_draw.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_certificates.py
    python test_probability_budget.py
    python certified_normal.py --self-test
    python check_global_contract.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python finite_bit_sampler.py --epsilon 1/16 --seed 17391
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python finite_bit_sampler.py --epsilon 1/16777216 --seed 17391 --output FINITE_BIT_TIGHT_DRAW.json
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_finite_bit_sampler.py FINITE_BIT_DRAW.json FINITE_BIT_SYSTEM_DRAW.json FINITE_BIT_TIGHT_DRAW.json

Omit `--seed` to obtain a fresh OS-backed draw. A saved OS-backed tape can still be reproduced by the verifier. Do not confuse that replay with newly independent randomness.

The tests include raw exact certificate replay, altered-certificate rejection, interval-normal checks, budget/PSD edge cases, endpoint-normal and small-V zero fallbacks, singular-fiber detection, a tiny 100-bit rational Cholesky check, and exact accept/reject/overlap branch checks. They reuse the same arithmetic kernels and are not an independent implementation or a statistical distribution test. A forced full-length cap-exhaustion campaign was not run.

## Honest limits

- The native certificate and local residual conclusions are directly checked by exact arithmetic on the included raw input.
- All finite-budget choices and described runtime guard paths are coded. The full W1 guarantee still rests on the written inequalities and ideal independent-bit abstraction; no finite sample test can prove it.
- The normal evaluator's finite-series/guard-bit majorant and the transport estimates are mathematical implementation contracts, not a machine-checked proof.
- The current parser/kernel is restricted to the dimensions and rational encoding above. General m,p,n, transpose-only certification, affine offsets and nonlinear targets are not implemented.
- There is no practical-speed superiority claim, tail-rate estimate, broad input campaign, parallel/external compute campaign, publication claim, or claim of solving generic dense constraint sampling.
