# Certified left-eigenvector recovery without coordinate polynomials

This additive result supersedes the earlier statement that an interval left-eigenvector construction was not supplied. The failed binary64 diagnostic remains intact. The modular coordinate numerator candidates remain uncertified as exact identities and are not used by this new route.

## Executed outcome

`left_eigenvector_high_precision.py` uses160-digit numerical arithmetic only to propose three512-bit dyadic matrices: C_Q approximating Q^{-1}, Z approximating M_lambda, and C_A approximating the inverse of a normalized left-eigenvector system. It refines the independently certified least-root interval to width≤2^-100. It imports no coordinate polynomial and runs no local optimizer. Current finder time3.24s.

`verify_left_interval.py` independently checks exact dyadic matrix-ball bounds. It replays the exact root refinement from the received certified least-root interval. Measured runtime0.60s before final rational candidate evaluation. Results:

- ||I−C_Q Q||_infinity ≤3.085e−114;
- normalized eigenvector-system inverse residual uniformly over the entire least-root interval ≤3.634e−11;
- every coordinate of the evaluation vector is within3.634e−11 of the proposed vector;
- coordinates x,y,z are near(1.0000005608256,1.00000033203075,1.00000028459786).

The displayed decimals are summaries of exact rational bounds stored in `left_interval_certificate.json`. Exact stereographic rounding of the coordinate approximation then produces a rational unit quaternion, whose original-objective global gap is1.190011164703136e−5 <1e−4, recorded in `left_feasible_certificate.json`. Its feasibility and upper bound are checked exactly.

## Governing residual proof

All norms are induced infinity norms. A matrix ball is (A0,r), meaning ||A−A0||≤r. Centers are integer matrices divided by S=2^512. Entry rounding loses at most1/S, hence row-sum error at most40/S. The verifier uses:

- addition radius r+s;
- multiplication radius ||A0||s+||B0||r+rs+40/S;
- rational scalar multiplication radius |c|r+40/S.

The original rational coordinate multiplication matrices are rounded with radius40/S. The program evaluates Q=I+Mx²+My²+Mz² and N=f0(Mx,My,Mz) by these rules. All integer matrix products and scalar fractions are arbitrary-precision exact. Numerical precision is not trusted.

If r_Q=||I−C_Q Q||<1, then Q is invertible and ||Q^{-1}||≤||C_Q||/(1−r_Q). For proposed Z, the exact residual yields

||M_lambda−Z|| ≤ ||C_Q||/(1−r_Q) · ||QZ−N/4||.

The verifier bounds transpose error conservatively by40 times this norm error. For λ in the certified interval, form A(λ) from M_lambda^T−λI by replacing its first row with e0^T (normalization w(1)=1), and b=e0. Its center uses Z, the rational interval midpoint, and a dyadic rounded diagonal. The radius includes transpose error, root uncertainty and diagonal rounding. The first row is set exactly. If r_A=||I−C_A A(λ)||<1 uniformly, then

||w−C_A b|| ≤ r_A/(1−r_A) · ||C_A b||.

Existence of the desired evaluation vector is guaranteed by the received reduced40-dimensional quotient with primitive simple value root: evaluation at its unique stationary point is a left eigenvector and has w(1)=1. It solves every original eigenvector row and hence the normalized39-row system. The certified inverse makes that system's solution unique. Consequently the omitted row is automatic; it is not an unchecked extra constraint. The coordinates are basis entries x,y,z at indices3,2,1 respectively.

Thus this certifies the coordinate approximation, rather than merely trusting a numerical eigensolver. The independently exact upper-bound check would remain valid even without the coordinate proximity certificate.

## Scope and rejected implementation

This is an executed fallback on the retained quartic, not a universal condition-number bound. Root isolation may need finer intervals and dyadic precision may need increasing on another input. The simple primitive-root and projective-boundary hypotheses remain essential. The ordinary candidate can be bypassed on this instance, removing that particular heuristic-success dependency. Generic complete runtime and a uniform practical online oracle remain separate obligations.

An attempted fresh direct Sturm count via `count_roots` was interrupted after roughly one minute without completion; it was replaced by exact `refine_root(..., fast=True)` starting from the already independently certified least-root isolating interval. No new least-root ordering assumption is made. This avoids an unnecessary expensive re-audit while preserving exact root enclosure.
