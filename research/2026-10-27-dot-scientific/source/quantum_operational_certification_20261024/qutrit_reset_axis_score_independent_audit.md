# Independent audit: exceptional-axis reference score and overlap-power guard

**PASS — 26 October 2026.** Governing axis note: `qutrit_reset_axis_reference_score_theorem.md`, with actual interface `qutrit_reset_anchored_reference_score_interface.md`.

The reference-filter derivative is the stated diagonal entropy score. In the actual source, the correlated input block is diag(a_i)+dJ3, the WH pair blocks are diag(a_i,a_j)+(d/2)J2 up to a fixed sign unitary, and the reference contribution after its log3 subtraction is `3f(a_i+d/3)`. Scalar spectators cancel. The signed masses and first moments cancel, so the resolvent entropy representation is legitimate. Sherman–Morrison yields exactly `d integral s/(a_i+s)^2 g_i ds`, including all factors.

For A=diag(a,b,b), the displayed factorization of g is correct. After scaling d to one, b>=1 is pointwise positive. For b<1 the transformation theta=1-b and the ratio to q0 are acquired from that same actual kernel by the exact checker, not merely asserted from a hand-copied rational expression.

The 177-monomial polynomial certificate was independently rerun. Its denominator is strictly positive at z>0; every listed coefficient is positive. At v=w=0 the polynomial vanishes, while its v-only and w-only monomials establish strict positivity whenever v+w>0. The ratio is therefore increasing, with the pure exception R=1. Its finite large-z limit and the integrable baseline receive subtraction of R(1). The centered ratio and baseline have matching signs on both sides of one, giving the claimed nonnegative integral, strictly positive with nonzero noise. Zero a or b is also received directly by the rational positive-z expressions; no unavailable singular off-support derivative is used.

This proves only the infinitesimal exceptional-axis score at an unfiltered axisymmetric seed. It does not receive repeated-axis coordinate scores, general anisotropy, finite reference-filter order, or accepted-only GLS monotonicity.

## Separate simultaneous-overlap curvature guard

The note `coherent_reset_overlap_power_curvature_obstruction.md` was also checked. The actual input has one changing 2x2 block and eight b spectators; the reference has three 2x2 blocks; normalized WH output has three 2x2 blocks and six b spectators. The entropy coefficients and constant source mass are correct.

Their small eigenvalues have the displayed determinant/trace coefficients. Expanding x log x yields the exact `C epsilon log epsilon` term and, from analytic eigenvalue expansions, the differentiated remainder `Delta''(r)=C/(1-r)+O(|log(1-r)|)`. The algebraic simplification of C has sign d-b. With d=p/3,b=q/9 the input opening coefficient is `pq/(q+9p)`, reference total is pq, and output contribution is `-2pq/(q+3p)`. Thus C=-1/100 at p=1/10 and C=1/20 at p=1/2. The first overlap derivative has the corresponding sign near one as well.

This exact already-paid source family rules out universal increasing/decreasing and convex/concave overlap-power behavior. It gives neither a negative actual value nor a failure of conditional coupled stationarity or homogeneous mass monotonicity.
