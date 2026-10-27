# Identity-or-arbitrary-qutrit-reset: whole WH3 value theorem

Construction assembled26 October2026. Whole fixed-qutrit theorem, exact-zero classification and all three exact certificates independently received PASS in arbitrary_qutrit_mixed_reset_independent_audit.md; the white-shift receipt is also recorded in qutrit_mixed_reset_white_shift_independent_audit.md. The final aligned-classical-logical extension is an explicit orthogonal-block corollary.

## Statement

For every qutrit density matrix tau and every0<=p<=1, the actual TP channel

 E(rho)=p rho+(1-p)Tr(rho)tau

has nonnegative WH3 Choi deficit

 Delta=2S((W3⊗id)A)-S(A)-S(A_R)-log3,
 A=p Phi3+(1-p)(I3/3)⊗tau.

For0<p<1 its deficit is strictly positive. The exact zero cases in this fixed qutrit output class are p=0 (arbitrary mixed replacement) and p=1 (identity). Unitary reversible success is equivalent by output covariance.

This is the logical-rank-one, qutrit-output mixed-reset theorem. It does NOT cover an arbitrary mixed reset on a larger output space with coherent outside-code components, arbitrary logical sigma with correlated mixed reset, or the unrestricted WH3 entropy conjecture.

## Proof chain

### 1. Actual spectral coordinates

Matched physical/reference unitary covariance diagonalizes tau while preserving Phi3. Work homogeneously with

 A=3a Phi3+I3⊗diag(b0,b1,b2), a,b_i>=0.

The normalized physical marginal is always I3/3. Normalization therefore gives an actual TP channel of the stated form, not merely an arbitrary bipartite state.

### 2. Remove common noise without losing a negative value

qutrit_mixed_reset_white_shift_boundary_theorem.md proves that t->D(a,b+t1) has no interior minimum and tends to zero at infinity. The proof is an exact determinant/Stieltjes formula and a rational degree-ten Descartes sign certificate.

Thus any negative value would yield an equal-or-more-negative unnormalized value after subtracting min_i b_i from all b_i. Renormalization strengthens negativity. It is enough to receive rank-at-most-two reset noise for every success probability.

### 3. Rank-two spectral edge has no off-endpoint minimum

For b=(0,u,v), fix a and e=u+v and use r=uv in[0,e^2/4]. qutrit_mixed_reset_edge_extrema_theorem.md proves that every interior stationary point in r is a strict maximum.

The proof retains the actual determinant factors. Its derivative K(s) has exactly one positive-to-negative crossing in s. An explicitly decreasing rational multiplier w satisfies partial_r K+wK<=0, certified by exact polynomial algebra and28 univariate Sturm checks. Consequently D_rr<0 at D_r=0.

The edge minimum is therefore either pure reset(r=0) or flat-rank-two reset(r=e^2/4). This is not a noise concavity assumption.

### 4. Receive both edge endpoints

Pure qutrit reset is the logical-rank-one, theta=1 specialization of arbitrary_logical_success_reset_flag_value_theorem.md, Sections1–4, received by arbitrary_logical_shared_resolvent_independent_audit.md. It is strictly positive when a>0 and the reset mass is positive. No broader mixed-reset class is imported through this dependency.

flat_rank_two_qutrit_reset_scalar_value_theorem.md proves the flat-rank-two endpoint directly. Its homogeneous value is b d(a/b), with d(0)=0 and d'(x)>0 for every x>0. Elementary small/large parameter estimates and a228-interval exact rational middle certificate cover the entire positive half-line.

Thus every nonzero rank-at-most-two reset has positive value when a>0. The counterexample-preserving reduction in Step2 proves nonnegative value for every full-rank reset as well.

### 5. Strictness for full-rank noise

Write b=b'+t1 with t>0 and min b'_i=0. The actual white-shift integrand has a strictly positive tail, and at most one sign change, from negative to positive. Hence D(a,b'+t1) is strictly positive at and beyond its maximum's location, being the integral of a positive tail. Before that location it is strictly increasing from its boundary value, which is nonnegative by Step4 (zero only when b'=0). Therefore every finite t>0 also gives strict positivity. This proves the stated zero classification.

## Ordinary reproducible sources

- qutrit_mixed_reset_white_shift_boundary_theorem.md
- qutrit_mixed_reset_white_shift_certificate.py and .json
- qutrit_mixed_reset_edge_extrema_theorem.md
- qutrit_mixed_reset_edge_extrema_certificate.py and .json
- flat_rank_two_qutrit_reset_scalar_value_theorem.md
- flat_rank_two_reset_scalar_interval_certificate.py and .json

The certificates use exact rational coefficient checks, exact Sturm root counts, and exact outward-rounded integer interval arithmetic. Discovery diagnostics are not proof premises. No external publication, novelty-priority claim, hardware validation or arbitrary mixed-reset closure beyond the stated scope is claimed.

## Direct orthogonal-block extension: aligned classical logical reset

The new scalar theorem immediately receives actual arbitrary-rank logical channels

 E(rho)=sum_j [p sigma_j rho+q Tr(rho)T_j]⊗|j><j|,

where sigma_j>=0,sum sigma_j=1, T_j>=0 are arbitrary qutrit operators, and sum_j TrT_j=1. Equivalently sigma is diagonal in the displayed logical basis and the reset tau=sum_j T_j⊗|j><j| is classical in that SAME basis. Its physical reset state may depend arbitrarily on the logical label and need not be maximally mixed.

This is an exact orthogonal-reference direct sum, not a convexity inference. Each nonzero block, divided by its trace t_j=p sigma_j+q TrT_j, is an actual identity-or-qutrit-reset channel. Homogeneous deficit additivity therefore gives Delta>=0. Equality holds exactly when every block has p sigma_j=0 or q TrT_j=0.

This extends coverage to arbitrary logical rank and classically correlated physically nonflat mixed reset. Coherent reset off-diagonal logical blocks, or a sigma not diagonal in the same logical basis, are NOT received by this argument.
