# Independent receipt: arbitrary fixed-qutrit mixed reset

**PASS — 26 October 2026.** Independently received `arbitrary_qutrit_mixed_reset_value_theorem.md`, including both new dependencies `qutrit_mixed_reset_edge_extrema_theorem.md` and `flat_rank_two_qutrit_reset_scalar_value_theorem.md`, their exact Python/JSON certificates, the simplex spectral interface, white-product Stieltjes receiver, and the already-audited white-shift reduction. No mathematical gap was found. This receipt covers value and exact equality for the actual fixed-qutrit-output channel only.

## Physical source, normalization, and endpoints

For A = 3a Phi3 + I3 tensor diag(b), the trace is T = 3a + 3 sum b_i and the physical marginal is (T/3) I3. After normalization, p = 3a/T and q tau_i = 3b_i/T. Thus every reduction stays in the stated actual TP channel class. The homogeneous functional is T times the normalized deficit, not the entropy formula applied naively to an unnormalized state. Its log-scale terms cancel. The reference eigenvalues a+3b_i supply exactly the T log 3 cancellation, giving the stated simplex formula.

The source block is diag(b)+a J3; WH output has the three pair blocks diag(b_i,b_j)+(a/2)J2. This independently yields the scalar formula. Pure-reset positivity uses `arbitrary_logical_success_reset_flag_value_theorem.md`, Sections 1–4, with logical rank one and full supported overlap, as already received in `arbitrary_logical_shared_resolvent_independent_audit.md`. In qutrit output every pure flag lies in the identity success support. Hence this endpoint is strict for a>0 and nonzero reset mass. Reset alone and identity alone have exact zero deficit.

## Rank-two edge

For b=(0,u,v), e=u+v and r=uv, independent determinant expansion gives:

- source determinant = (s+a)r+s^3+(e+3a)s^2+2aes;
- product of the two pair determinants involving the zero coordinate = (s+a/2)^2(r+B);
- remaining pair determinant = r+C;
- the two varying reference factors = r+R.

The entropy determinant signs therefore give exactly K = 2/(r+B)+2/(r+C)-1/(r+A)-3/(r+R). Scaling a to 6 preserves the parameter range and all relevant signs. At interior r>0 the derivatives are integrable at zero and infinity; fixed zero spectators do not enter them.

Replayed `qutrit_mixed_reset_edge_extrema_certificate.py` without modification: **PASS**, 61 coefficient polynomials and 28 exact positive-half-line Sturm counts. The coefficient chain applies to H=-numerator(K): its top coefficients are nonnegative, its leading coefficient is positive, and its constant is strictly negative. Each certified implication propagates nonpositivity downward, including zero coefficients. Descartes therefore gives exactly one positive root counted with multiplicity, necessarily simple. Consequently K is positive before that root and negative afterwards, not the reverse.

The multiplier certificate clears strictly positive denominators. Each exceptional coefficient polynomial has its zero power of s removed, positive constant and leading coefficients, and zero positive roots; it is thus strictly positive for s>0. This establishes K_r+wK<=0 pointwise, rather than from samples. Also r+R <= (s+2+e/2)^2 and R'=2(s+2+e/2), while k'/k <= 1/[75(s+180+e)]. Hence w'<0 strictly. At a stationary edge point, subtracting w(s_*) from w in its integral against K gives a strictly positive integral. Thus D_rr<0 there. Every interior stationary point is a strict maximum, and continuity on the closed edge puts its minimum at pure or flat rank-two noise. No global concavity is needed.

## Scalar receiver

Independently differentiated each two-eigenvalue term using its trace and determinant. The resulting derivative is exactly equation (2), including log(4/27), the log x coefficient, and the -(c_o/2) log 2 term. All affine derivative constants cancel.

The small-x estimates are valid on (0,1/20], including the squared radical comparison and 4x-8x^2-16x^3>=0; their final lower bound is at least 1/25. The large-x rewrite is exact. Rationalizing 3-c_s gives the stated 8y^2 numerator; its denominator is at least 54. Rationalizing 4-c_o gives the stated lower bound for y<=1. The remaining logarithm bounds yield 2y-(13+8/27)y^2>0 on (0,1/10].

Read the interval implementation operation by operation: integer floor/ceiling multiplication and division handle all numerator signs; divisions have positive denominator bounds; integer square roots enclose the exact roots. Endpoint log range reduction preserves arguments in [1,2]. The 60-term atanh sum has nonnegative remainder bounded by the first omitted power divided by 121(1-z^2), evaluated outward. Negative powers-of-two log corrections use signed interval multiplication correctly. The adaptive split is a rigorous covering proof, not sampled positivity.

Executed an unmodified copy of `flat_rank_two_reset_scalar_interval_certificate.py` in /tmp to avoid changing author output: **PASS**, 228 exactly adjoining rational intervals covering [1/20,10]. Reproduced minimum lower bound 508237401513783999573/302231454903657293676544. Together with both endpoint estimates, d'(x)>0 for all x>0; continuity at zero and homogeneity establish strict flat-rank-two positivity.

## White shift and whole strictness

The white-shift hypothesis is precisely the same actual source with arbitrary nonnegative b and a>0. Its numerator has positive leading coefficient and at most one positive root counted with multiplicity, so its integrand has a strictly positive tail and at most one negative-to-positive crossing. This makes D(t) either decreasing to zero or increasing then decreasing to zero. Boundary positivity excludes a negative full-rank value. More strongly, after the crossing D(t) is the integral of a strictly positive tail; before it D(t) strictly increases from its nonnegative boundary value. This also handles b'=0 (boundary identity). Therefore every finite positive common shift is strict.

The complete zero classification is p=0 or p=1. No claim is received for arbitrary correlated logical resets, arbitrary larger-output coherent mixed resets, or unrestricted WH3. No numerical optimizer or floating sample is a premise of this receipt.

The previously audited white-shift exact Python/JSON replay was also rerun: **PASS**, with remainder monomial counts 52, 79, 106, 180, 168, 235. Its hypotheses, root orientation, and normalization agree with the new closure.
