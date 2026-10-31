# Final targeted audit of the quadratic task proof

31 October 2026. Read QUADRATIC_TASK_PROOF.txt and the explicit warm continuation code and saved artifacts. No experiments were rerun. A deterministic check compared the already saved warm prefix, complete batch record, final model, stage numbering, and cumulative bills.

## Verdict

The norm-based Schur yield, constructive finite rational alternatives, and qualified epsilon^(-2) acquisition claim are sound. Three small wording corrections were communicated to root: distinguish an actual coefficient norm from an arbitrary certified upper bound; initialize general matrix-norm bisection with a genuinely valid spectral-norm upper bound; and distinguish selected matrix-entry bit sizes from the longer final error-bound fractions.

The new warm H8-to-H64 artifact supplies the operational continuation that the original independent-run records did not demonstrate. A dated addendum has also been appended to the earlier implementation audit.

## 1. Norm-based Schur yield: the 25z bound is valid

Under exact invariance, empirical least-squares minimality gives

    lambda_max(Rhat) <= (1+sqrt(3))^2 z < 7.465z,

when t<=1/2. The true residual at the empirical coefficient C is positive semidefinite, and the acquired perturbation bound gives

    lambda_min(Rhat) >= -z(1+||C||)^2.

Furthermore,

    ||C|| <= ||B0^(-1)|| ||Atilde||
          <= (1+t+z)/(1-nu) <= 4,

because nu+z=t<=1/2. Thus the negative eigenvalues have magnitude at most 25z, and

    ||Rhat|| <= 25z.

This controls the full matrix norm used by the code, not only its largest eigenvalue. A norm upper bound computed to additive accuracy xi_R is then <=25z+xi_R; choosing xi_R=O(z) preserves the asserted yield.

One notation correction matters: section 6 defines c_a as any certified upper bound on ||C_a||. An arbitrarily conservative upper bound need not itself be <=4. Either write the displayed estimate for ||C_a||, or define c_a as the minimum of its measured certificate and the independently valid analytic bound (1+t+z)/(1-nu). The actual matrix-norm yield is unaffected.

## 2. Constructive rational alternatives

A positive rational Gram estimate admits an exact rational LDL^T factorization with strictly positive diagonal. If Ghat=L D L^T, a whitening proposal can be formed as

    R=L^(-T) Dtilde^(-1/2),

where each positive diagonal inverse square root is approximated rationally by bisection. The resulting B0=R^T Ghat R and nu are checked explicitly. This uses the measured positive pivots, not a supplied favorable Gram floor. Very small pivots can still make the bit and source-precision bill large.

For any finite rational matrix M, the test

    u^2 I-M^T M positive definite

holds exactly when u>||M||_2. Strict positive-definiteness tests therefore give an interval bisection for the norm with no eigenvalue-gap premise. Equality may be treated as a failed strict upper test, placing the tested value on the lower side of the norm bracket. Starting from a strict upper endpoint and halving to a specified positive absolute tolerance terminates after a finite logarithmic number of tests.

Use a rational upper bound on the Frobenius norm, or a rational upper square root of ||M^T M||_infinity, to initialize that bracket, with a positive margin if necessary. A raw maximum row sum of a general nonsymmetric M alone is not a spectral-norm upper bound: [[1,0],[1,0]] has maximum row sum one and spectral norm sqrt(2). For a symmetric matrix, the row-sum norm does provide the needed upper bound. The proof should specify which safe variant it intends.

The radial contraction construction is valid. If u>=||Atilde|| within xi, then

    A=Atilde/max(1,u)

is a rational symmetric contraction and

    ||A-Atilde|| <= max(0,u-1) <= 3t+xi.

The analogous norm-scaling operation for the seed is also finite and rational. Exact rational stored matrices require their stated bit-length execution cost; dyadic output requires its additional checked rounding/shrink step.

## 3. Scope of the epsilon^(-2) claim

Equation (16) has the correct parameter dependence for a sufficient stage bill:

    B^2 p^2 [p+log(1/delta_s)] ||R||^4 H^4 epsilon^(-2).

At a fixed acquired frame, the proof gives z=eta||R||^2, and squared-leakage plus numerical errors of order z produce scalar error O(H^2 z). Therefore eta of order epsilon/(H^2||R||^2) is sufficient, and bounded-report averaging costs eta^(-2). The ||R||^4 factor and H^4 dependence follow directly.

The proof appropriately qualifies this as a local accuracy dependence under closure/yield and proportional numerical budgets. Keep that qualification prominent. Tightening epsilon can change the chosen landmarks, the attained Gram floor, the pool size, return depths, or preceding discovery work; no uniform end-to-end epsilon^(-2) theorem follows for those changes. The statement also is not an optimality lower bound for all learners or an assertion that a first-order vector-analysis route is statistically optimal.

The code's fixed 1e-7 stored-matrix rounding allowance is only adequate for the saved H<=64, epsilon=1/2 tasks. The proof now says this explicitly. Arbitrary tighter tasks must refine that numerical allowance or return failure.

## 4. Bit-size wording

The saved selected-matrix-entry maxima are 386 bits for H8 and 434 bits for H64. The complete exact error-bound fractions have bit lengths 2,698 and 10,148 respectively. Thus a sentence saying checks are 'up to hundreds of rational bits' should not imply an overall maximum. The correct distinction is that selected matrix entries have hundreds of bits, while the longer full certificate fractions are reported separately. Neither field is a complete peak-bit-length or operation-count measurement for all exact-arithmetic intermediates.

## 5. Dated warm-continuation audit: 31 October 2026

The original files quadratic_scalar_baseline_results.json and quadratic_scalar_baseline_models.json remain independent-run diagnostics. The earlier caveat about treating those two runs as an implemented continuation remains true for those records.

The new files quadratic_scalar_warm_results.json and quadratic_scalar_warm_model.json resolve that operational issue. The implementation:

1. Acquires and accepts H8 using stages 1 through 6.
2. Retains the actual landmarks, numerical model, exact latest Gram means, all previous stage records, the original source, and the original global confidence budget.
3. Recomputes the certificate for H64 from the retained data with zero source calls. The resulting bound is about 14.7286174, so it correctly declines to accept epsilon=0.5 from those data alone.
4. Refines through stages 7, 8, and 9, using the continued exact allowances 1/5600, 1/7200, and 1/9000.
5. Returns the H64 certificate about 0.2305919145 under the same shared joint soundness budget delta=0.01.

No new word types or unordered Gram-pair types are introduced; the new stages refine the already acquired experimental family. There are ten word types and 55 unordered Gram-pair types. The records separately identify 60 ordered return-pair spellings because earlier pool orderings produced five orientation variants. All actual reports, including those orientation variants, remain paid.

The marginal bill is:

- 7,075,161,714,672,535 stationary preparations.
- 25,470,582,172,821,126 primitive controls.
- 14,150,323,429,345,070 endpoint readings.
- 165 additional scalar batches.

Adding the retained H8 bill gives the recorded lifetime total:

- 7,076,851,016,432,793 preparations.
- 25,476,663,441,142,005 controls.
- 14,153,702,032,865,586 readings.
- 423 scalar batches.

Return depth remains six. The retained Gram tolerance changes from 0.00015625 to 0.00000244140625. Fresh finer cohorts are charged in full; retaining old data does not silently reduce the new cohort's confidence radius.

A deterministic saved-record check verified that the warm H8 prefix equals the existing H8 raw record, the complete warm batch sequence and final stored model equal the existing H64 record, stage numbers are exactly 1 through 9, and initial plus marginal bills equal the lifetime bill in every additive category. This was an audit of existing records, not a new acquisition execution.

The shared confidence statement is joint soundness: the probability that any returned certificate in this continuation is false is at most delta. It does not assert the same probability conditional on a successful return. Physical episodes remain simulated charges, not laboratory executions.
