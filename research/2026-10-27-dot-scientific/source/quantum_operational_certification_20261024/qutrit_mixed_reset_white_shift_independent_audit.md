# Independent audit: exact white-shift boundary reduction

**PASS**, 2026-10-26. Governing `qutrit_mixed_reset_white_shift_boundary_theorem.md` and its exact rational certificate. This receives the full-rank reset REDUCTION, not the remaining rank-two edge value.

## Actual source determinant and scaling

For A=3aPhi3+I3 tensor diag(b), the correlated input block is diag(b)+aJ3, with two spectator copies of each b_i. The normalized WH output has three pair blocks diag(b_i,b_j)+(a/2)J2 (up to harmless signs) and one spectator copy of each b_i. Its reference is diag(a+3b_i). Cancelling the actual entropy/normalization constants gives precisely the preceding simplex interface. Applying the rank-one determinant lemma against the zero-main baseline yields the displayed F(m), with m_i=a/(s+b_i), retaining the output factor two and reference factor three.

At infinity F=O(s^-2), and at zero for singular b the finite-rank determinant expression has at worst logarithmic growth; both are integrable. Adding common noise shifts the integral endpoint exactly. For t>0 differentiation gives D'(t)=-F(m(t)); continuity receives t=0 even if a boundary derivative is infinite.

For a>0, rescale s and all b_i by a/6, receiving a=6 without changing any sign statement. When a=0 the entire curve is zero. At a=6, direct denominator cancellation gives exp(F)=Q(s)^2/[A(s)prod_i(d_i+2)^3], exactly the stated polynomial H. The denominator is positive for every s>0 and b_i>=0.

## Exact certificate and Descartes logic

Inspected the coefficient bases and rational JSON data and reran `qutrit_mixed_reset_white_shift_certificate.py`. Degree is exactly10, c10=72, and c10 through c7 are coefficientwise nonnegative. Every N_j has nonnegative rational coefficients and every D_j has constant1 plus nonnegative coefficients. Exact expansion verifies N_j c_j-D_j c_(j-1) coefficientwise nonnegative. Replay remainder counts were52,79,106,180,168,235; all nonzero coefficients were strictly positive. No floating optimizer or sampled root assertion enters this receipt.

For any fixed nonnegative b, D_j>=1. Thus c_j<=0 implies c_(j-1)<=0, including c_j=0 and N_j=0 cases. The upper four coefficients are nonnegative and c10 is strictly positive. Once a nonpositive coefficient occurs at degree<=6, no later lower coefficient can become positive. Consequently the descending list, with zeros omitted, has at most one sign variation. A possible root at s=0 does not count as a positive root and causes no exception.

Descartes' rule bounds positive roots counted with multiplicity by one. The polynomial cannot vanish identically because c10=72. If it has a positive root, that root is simple and the positive leading coefficient forces the crossing from negative to positive. Otherwise H is positive throughout s>0. The same sign alternatives hold for F because sign(F)=sign(exp(F)-1) and its denominator is positive. Tangential double roots and nontrivial zero intervals are excluded.

## From derivative shape to actual rank reduction

The common-noise homogeneous deficit therefore either decreases to zero or first increases and then decreases to zero. Its only possible interior critical point is a maximum. The limit zero follows equally from the integrable F-tail or the entropy expansion. Hence D(a,b+t1)>=min(D(a,b),0), including singular initial b by continuity.

Starting from negative D(a,b), subtract r=min b_i. Applying this bound to b'=b-r1 forces D(a,b')<=D(a,b)<0. At least one noise eigenvalue vanishes. The all-zero b' case would give a pure reversible source with zero deficit, so a negative receiver has reset rank one or two. The physical marginal remains scalar, and source trace drops from3a+3sum b_i to3a+3sum b'_i>0. Dividing the more-negative homogeneous value by this smaller trace cannot increase the normalized negative deficit. The result is an actual TP channel of the same family, with changed p and q.

**Scope:** The reduction is counterexample-preserving over all probabilities. It proves neither fixed-p monotonicity, normalized main-weight monotonicity, noise concavity, nor the boundary value itself. Previously retained twirl/pointwise-integrand obstructions are unaffected. No unrestricted-WH3 conclusion is inferred.
