# Independent receiving audit: positive-cost gated rounding on a binary decoder cube

**RECEIVED in the stated product-cube scope.** 28 October 2026.

Source: `ordinary_classical_positive_cost_gated_rounding_20261028.md`, SHA-256
`d30bebfe86d4abc4154482d9b3a435de247c09e9dbc2ecf164dcabafbfa99e01`.

This reviewer independently checked the Gaussian group covariance, affine-offset repair, truncation/grouping inequalities, and capped finite implementation. No correction to the source is required. A separate constructive companion improves the logarithmic square by simultaneously rounding all groups; that improvement is not needed to receive the frozen source.

## 1. Feasible moment relaxation and group lemma

The perspective constraints are exactly the positive-denominator homogenization. The original binary vertices are feasible, and a strictly positive independent-Bernoulli moment point lies in the relative interior of the affine moment constraints. Supplied rational bit bounds and a finite Slater witness remain part of any actual SDP implementation; the rounding statement itself only needs a feasible moment matrix.

For a group with p_i in(p/2,p], Y=M_I/p+diag(1-p_i/p) is a correlation matrix. The Gaussian sign identity and the absolutely convergent arcsine series imply E ss^T >=(2/pi)Y in Loewner order: each higher odd Hadamard power is PSD, including singular-correlation cases by continuity. With one common Bernoulli(p) gate, E z_i=p/2<=p_i and E zz^T=(p/4)(11^T+E ss^T)>=M_I/(2pi). Consequently the numerator bound is valid for every PSD A_II, including negative off-diagonal entries. Independent gates per coordinate would not suffice.

For the affine offset, N(z)+A_00>=||sum a_i z_i||^2/2. If both the baseline ratio and EN/Eu were smaller than S_I/(8pi c_I), this inequality would be contradicted after expectation. Thus the baseline repair is necessary and its constant is correct.

## 2. Tail and offset cases

Write d=m+sum w_i p_i. The discarded principal block satisfies S_tail<=a sum_tail p_i<=m/64; this uses the supplied operator bound a, not entrywise positivity of A. Two PSD Cauchy inequalities give S<=2A_00+4S_keep+m/16. When F=S/d>=1 and A_00/m<F/4, this actually gives S_keep/d>=7F/64, stronger than the stated F/16.

The further bounds S_keep<=L sum S_I and sum c_I<=L d prove the displayed group choice. If L=0, the same inequality makes the small-baseline case impossible, so returning the baseline covers that corner. F<1 permits additive-one loss rather than an unsupported multiplicative guarantee. Coordinate flipping to a minimizing cube vertex preserves a PSD affine-quadratic representation and produces nonnegative cost coefficients.

## 3. The fixed trial cap and finite arithmetic

For the chosen group, t=F/(4096L^2), and R_0<t,

    E[N-2t u] >= (64/pi-2)t c_I-t m
               >= (64/pi-3)t m >13t m.

The source only requires t m. Since N-2tu<=N<=a(n+1), the success probability is at least 13t m/[a(n+1)] in the ideal sampler. There is therefore ample slack to approximate each complete gate/sign record in coupling probability, e.g. by at most t m/[4a(n+1)], and still retain the stated conservative trial cap. No potentially huge negative value of N-2tu needs a bounded-range expectation comparison: couple the success EVENT instead. Large rational w_i affect exact objective evaluation and input bit complexity, not the sign-distribution bound.

The finite Gaussian implementation does not need a correlation spectral floor. Approximate a PSD square root in Frobenius norm; couple a finitely truncated/quantized standard Gaussian to its ideal draw; then all sign differences are contained in the Gaussian truncation event or in a union of marginal intervals around zero. Every ideal marginal has variance one, so that union has probability at most sqrt(2/pi) times the sum of interval widths. Required precisions and caps are polynomial in the numerical parameters n,a,1/m and logarithmic failure precision, as claimed. This is not a claim of polynomial dependence on log a when a itself is exponentially large.

All returned vectors remain exactly binary. Baseline inclusion covers failed histories; the approximation guarantee is probabilistic with a predeclared finite cap. The source's SDP and finite sampler are mathematical finite algorithms, not production implementations or executed hardware.

## 4. Diagnostic evidence and boundary

The separate `_independent_check.py/.json` uses feasible PSD moment matrices not restricted to actual Bernoulli moment matrices, signed PSD quadratic forms, rare groups, tail-empty cases, exact rational affine-offset/tail budgets, and exhaustive small binary menus. Numerical arcsine eigenvalues supplement, rather than replace, the analytic Loewner proof.

No full-CPTP Choi rounding, cost-preserving quantum matrix gate, improved generic source exponent, or historical priority claim is received here. Product feasibility is essential; the strongest equally informed conventional learner receives the same classical optimization tool.
