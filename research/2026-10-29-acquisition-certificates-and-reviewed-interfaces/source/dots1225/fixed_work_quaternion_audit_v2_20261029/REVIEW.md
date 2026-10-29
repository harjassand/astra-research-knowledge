# Independent mathematical receiving review: bounded quaternion kernel v2

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler` is not a construction author. **Accept the corrected mathematical certificate contract and declared finite-work arithmetic model, with the restrictions below.** The original v1 standalone verifier remains superseded and must not be described as valid for arbitrary supplied certificates. Original source files were not changed.

## Governing correction and exact lower-bound proof

The authoritative verification modules are `bounded_sos_oracle_v2.py` and `fixed_work_oracle_v2.py`, governed by `VERIFIER_CORRECTION_v2.md`. Both enforce canonical scale max(1,sum|F_e|)>0, four quaternion entries, ten-by-ten matrices, symmetry where needed, and valid integer degree-four exponent tuples. Checks use assertions: this acceptance requires Python assertions enabled, not `python -O`.

The 10 quadratic monomials have 55 symmetric Gram coordinates and span all 35 quartic monomials. The source grouping has exactly the diagonal/off-diagonal factors 1/2 required by z^T G z; its construction supplies 20 independent nullspace directions by assigning each redundant coordinate against a leading coordinate in the same monomial group. I independently checked all 35 basis polynomials and all 20 null directions exactly.

In the full certificate, exact coefficient identities give F/scale-lambda Q^2=z^T Gz. With D=diag(1 for squares,2 for cross-products), z^T Dz=Q^2. For arbitrary rational V, B=V^T D V. Strict row diagonal dominance with positive diagonal makes B positive definite by the symmetric Gershgorin bound. Thus V is invertible. Writing A0=V^T G V and b_i=B_ii-sum_off|B_ij|>0, the chosen nonnegative delta ensures

(A0+delta B)_ii-sum_off|(A0+delta B)_ij| >= A0_ii-sum_off|A0_ij|+delta b_i >=0.

Symmetry and weak diagonal dominance with nonnegative diagonal imply PSD. Invertible congruence then gives G+delta D PSD. Hence F >= scale(lambda-delta) on Q=1. If B fails its strict test, V=I provides b_i=D_ii>0, so the one-pass repair always has a finite exact denominator. No floating eigensolver output is trusted as a PSD proof.

The weak-DD certificate checks the analogous identity scale*z^T Gz=F-dd_lower*Q^2 with G symmetric DD. Both additionally check the unit quaternion, exact upper value, lower=max(certificate lower,-sum|F_e|), and exact nonnegative gap. On the sphere every quartic monomial has magnitude at most one, so |F|<=A=sum|F_e|. Therefore the fallback is sound and 0<=gap<=2A. The candidate is separately feasible; this does not round a relaxed Gram solution into a quantum code.

## Previous defects and corrected admissibility

The preserved negative-scale arithmetic example for F=q0^4 passes the old assumptions incorrectly: multiplication by negative scale reverses a lower-bound inequality. V2 rejects it at canonical scale validation. The retained extra-coordinate normalization example is likewise rejected by exact length four. Reviewer checks additionally rejected noncanonical positive scale, short Gram/basis matrices, floating or wrong-length exponent tuples, and a negative exponent. These are mathematical input-admissibility checks only, not evaluation of any external service.

The v2 full solver imports `fixed_work_oracle.py` for unchanged Gram/monomial/evaluation helpers. Its old `verify` function is not used by the v2 full verifier. The receipt binds that helper dependency but does not reinstate the old standalone validator. The weaker solver's valid-input domain is rational homogeneous quartics; strict malformed-exponent checks reside in its v2 verifier. No claim is made that all solver argument-validation paths provide a general external API.

## Finite work and always-output scope

For declared defaults, candidate construction uses 31 starts, 32 tangent iterations, eight line-search slots per iteration, exact 24-bit stereographic rounding, and fixed-dimensional solves. The Gram proposal has 9*16*16=2,304 trial Cholesky slots plus bounded current-matrix/reset factorizations; it is not a claim of exactly 2,304 total factorizations. Jacobi proposes 12*45=540 pair updates. Full Gram coordinates use 40-bit rounding, bases 32-bit rounding. The pure rational baseline uses 28+9*8=100 objective evaluations and 1+60*9=541 Gram scores.

Normalization bounds the coefficient l1 norm by one. The canonical G0 has absolute row sum at most one (an off-diagonal assigned coefficient is split equally across symmetric entries), so G0+2D has exact strict positive margin at least one. This justifies the reset point. Bounded proposals and exact repair do not require convergence. Rounding uses a rational stereographic parametrization with strictly positive denominator, so the produced quaternion is exactly feasible. Generated certificate bit lengths are bounded in terms of the public input-bit bound and declared precision budgets. The checker applied to arbitrary external-size rationals is not constant-work irrespective of their size.

Within the manuscript's fixed-dimensional floating-primitive model and absent computational faults, there is no abort merely because a requested accuracy is missed: a visible possibly poor gap is returned. This is not an unconditional hardware/language runtime-totality guarantee under floating-library failure, allocation failure or arbitrary custom arguments. No uniform small gap, SOS exactness for every quartic, or certified optimality of the DSOS search is inferred.

## Dyadic reporting

For an integral cap in 2^-b units and 0<=e<=Bcap, the ceiling report has e<=e_report<=e+2^-b and e_report<=Bcap. The minimum with Bcap does not break upward validity because the cap is already on the grid. N reports have excess at most N*2^-b. Storing integer units requires at most b+ceil(log2(N Bcap+1))+O(1) bits, rather than accumulating heterogeneous exact denominators. This upper report may replace a raw error in an upper-error theorem, but its realized sum is not its conditional expectation and does not certify future readiness.

## Executed independent evidence and limits

All frozen core/v2/counter manifests verified. On copies, all 1,096 retained certificates pass v2: six full-SOS banks, seven weak-DD cases, 360 full offline, 360 weak offline, 360 live-query certificates and three retrospective certificates. The old inadmissible-scale regression is rejected. This checks arithmetic on retained actual/offline query data; it does not independently reproduce or accept the quantum trajectory or service protocol.

Independent additions: 35 monomial Gram identities with nullspace checks; 40 rational congruence/repair cases including singular and arbitrary proposed bases; four fresh full and four weak solver cases (zero, q0^4, a tiny negative coefficient and a dense rational polynomial); invalid-input rejection fixtures; and 1,200 exact dyadic report tests at four precisions and three caps. Defaults' operation metadata agrees with loop inspection. Copied retained counter replay agrees with exact raw sums. No physical timing or noise measurement was performed.

Primary prior-art page checked directly 2026-10-29: Ahmadi and Majumdar, *DSOS and SDSOS Optimization*, https://arxiv.org/abs/1706.02586. Diagonal-dominance sufficient Gram certificates are established machinery. This review establishes no historical novelty or practical advantage over equally informed conventional SOS/control methods.

Acceptance covers corrected mathematical soundness, visible conservative gap, declared finite-budget arithmetic construction and dyadic reporting. Excluded: universal tightness, physical clock isolation, measured worst-case timing, source/key privacy, calibrated hardware controls, integrated recovery/service/outer-code yield, and independent acceptance of the retained live quantum simulation. A release/padding architecture is still needed wherever the source can observe candidate-dependent computation. The correction preserves existing generated values, not the old validator's soundness.
