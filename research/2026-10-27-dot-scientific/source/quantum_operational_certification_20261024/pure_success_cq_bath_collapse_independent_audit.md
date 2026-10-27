# Independent audit: pure success and arbitrary physical-CQ reset baths

**PASS — 26 October 2026.** Governing proof: `pure_success_arbitrary_cq_reset_bath_collapse_theorem.md`. Dependency: the independently received arbitrary-weight three-pure-flag theorem and its frozen-kernel zero geometry. This is a whole value/equality result for pure logical success and arbitrary finite logical reset matrices in three fixed physical diagonal blocks. It is not a mixed-success or physically coherent reset theorem.

## Actual source and normalization

The reference blocks have Gram heads `(d,c_i; c_i*,3B_i)` up to the explicitly chosen row/column convention, with `c_i=sqrt(d)sqrt(3B_i)s`. The original input arrow has head `3d`, baths `B_i`, cross `c_i/sqrt(3)`, and two bath spectators per label. The normalized WH output has the three pair arrows with head `d`, cross `c_i/sqrt(6)`, and one bath spectator per label. Consequently the spectators cancel in the stated entropy expression. The normalization is `3d+3 sum Tr B_i=1`. The homogeneous formula and its zero-coherence baseline hold before imposing normalization, which is essential for the eigenvalue derivatives.

The source checker was rerun from the quantum folder: all 18 complex sources (logical dimension 2–4, faithful and singular baths) agree within `2.67e-15`. Both fully saturated tangent checks pass. These numerical checks corroborate, rather than replace, the Gram and tangent derivations.

## Fixed-dimension feasibility and saturated supports

There is no optimization over independent fictitious overlaps. In the original fixed logical dimension, two bath eigenvectors having nonzero projections onto the same success vector can be unitarily rotated within their own two-dimensional span. After choosing their phases, the derivative of the first squared overlap is a nonzero multiple of `2 sqrt(r_a r_b)`; the second changes oppositely. Thus every sufficiently small two-sided redistribution at fixed sum is attainable, with the other blocks unchanged. Eigenvalue transfer at fixed eigenvectors is separately feasible. Both paths preserve bath rank and support, including the case where the success vector lies in every bath support.

For each block,

`u_i(t)/t = d(1-R_i)/t + d sum_a r_ia/(b_ia+t)`

is strictly decreasing and positive. The previously received frozen-kernel zero argument therefore gives either a positive kernel everywhere or one strict negative-to-positive crossing. It does not require a negative small-t sign. The large-t sign is positive.

At any saturated face the worst kernel behavior is `O(1/t)`. Both overlap redistribution and eigenvalue transfer introduce the factor `t`; their differentiated integrands are bounded at zero and decay integrably at infinity. Positive support eigenvalues provide local uniform bounds. The zero eigenvalues of saturated Gram heads stay zero along these paths: this is differentiation on a constant-rank stratum, not an unreceived inward derivative. In particular, all-three-saturated baths need not be pure, and the proof does not assume they are.

## Strict spectral descent

For occupied distinct bath eigenvalues `a<b`, overlap stationarity is exactly

`integral t G_i(t)/((a+t)(b+t)) dt = 0`.

This forces an actual crossing. Relative to this zero integral, the multiplier `(b+t)/(a+t)` is strictly decreasing and `(a+t)/(b+t)` strictly increasing. Centering at the crossing makes the first weighted integral strictly negative and the second strictly positive. Hence `partial_a Delta>0` and `partial_b Delta<0`; decreasing a while increasing b strictly decreases the deficit at fixed bath trace. The factors `d r_a,d r_b` are positive and do not alter these signs. No constrained local minimum can retain two distinct occupied eigenvalues in one block.

## Spectators, compactness, and equality

A positive bath eigenvector orthogonal to success is an actual reference-orthogonal reset summand. It has homogeneous deficit zero. Removing mass w leaves a TP source after division by `1-w`: its success probability becomes `p/(1-w)` and its reset remains physical-CQ. At a negative minimum this makes the deficit strictly more negative. A repeated positive bath eigenvalue always supplies such an orthogonal eigenvector if its multiplicity exceeds one.

With fixed success vector and original finite logical dimension, p and the three PSD baths of total trace one form a compact set. Continuity gives a negative minimum if any negative value exists. The p endpoints have zero deficit. Spectator removal and the strict descent above force each remaining bath to rank at most one, contradicting the received pure-flag theorem. No dimension enlargement or arbitrary-rank compactness is used.

After nonnegativity is established, the same argument applies to a zero: remove all orthogonal spectral directions, preserving zero, and use local minimality on the remaining source. It reduces to rank-one baths, where the received strict pure-flag equality classification excludes any remaining overlap. Therefore for p,q>0 equality is exactly `T_i s=0` for all i; p=0 or q=0 are also zeros.

No correction to the governing proof was required. The checker's relative imports require execution with the quantum folder as working directory; this is an invocation condition, not a mathematical defect.
