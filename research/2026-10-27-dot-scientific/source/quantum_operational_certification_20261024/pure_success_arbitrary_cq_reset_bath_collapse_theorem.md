# Pure logical success with arbitrary physical-CQ mixed reset: spectral bath collapse

Status: independently received PASS in `pure_success_cq_bath_collapse_independent_audit.md` (26 October 2026). Depends on the new pure-flag whole theorem and its scalar zero-geometry lemma in `arbitrary_weight_three_block_pure_success_value_theorem.md`. No arbitrary matrix-valued success or physical-reset coherence is claimed.

## Statement

Let s be a unit logical vector and let T_1,T_2,T_3 be arbitrary positive semidefinite logical operators with sum_i Tr T_i=1. The actual TP channel

E(rho)=p rho tensor P_s+q Tr(rho) sum_i |i><i| tensor T_i, p+q=1,

has nonnegative WH3 Choi deficit. The T_i need not commute with each other or with P_s. For p,q>0, equality holds exactly when T_i s=0 for every i.

The arbitrary fixed physical basis may be changed by matched covariance. The theorem is a physical-CQ reset theorem, not arbitrary physically coherent reset.

## 1. Exact mixed-bath source spectra

Put d=p/3, X_i=q T_i, B_i=X_i/3, and c_i=sqrt(d) sqrt(X_i) s. Work on the positive support of X_i. The normalization is

3d+3 sum_i Tr B_i=1.

The original reference state has, for each physical label, the nonzero Gram spectrum of

T_i^G=[[d,c_i*],[c_i,X_i]].

The original input has one changing Gram arrowhead R with center 3d, bath diag(B_1,B_2,B_3) and cross vectors c_i/sqrt3, plus two scalar-matrix spectators B_i for each i. The normalized WH output has, for each physical pair i<j, a changing Gram arrowhead O_ij with center d, baths B_i,B_j and cross vectors c_i/sqrt6,c_j/sqrt6, plus one spectator B_i for each i. These statements follow directly by forming Gram matrices of the success vector and the eigenvectors of each physical reset block; distinct physical labels are orthogonal, so mutual logical eigenvector inner products never enter.

Consequently the exact homogeneous deficit is

Delta=sum_i f(T_i^G)+f(R)-2 sum_{i<j} f(O_ij)
      -(3d+3 sum_i Tr B_i)log3,

where f(X)=Tr XlogX. This is an actual source identity, not an abstract enlargement of admissible matrices.

Schur complements and the same input-resolvent substitution as in the pure-flag theorem give

Delta=integral_0^infinity G_t(u(t);d)dt,                 (1)

with exactly the scalar function G from that theorem and

u_i(t)=d-(1/3)c_i*(B_i+tI)^(-1)c_i.

In an eigenbasis of B_i, write b_iα>0 and

r_iα=|<e_iα,s>|^2=|c_iα|^2/(3d b_iα),
R_i=sum_α r_iα<=1.

Then

u_i(t)=d-d sum_α r_iα b_iα/(b_iα+t),
u_i(t)/t=d(1-R_i)/t+d sum_α r_iα/(b_iα+t).               (2)

These ratios are positive and strictly decreasing for t>0, including every saturated face R_i=1.

Source replay: `pure_success_cq_bath_collapse_source_check.py` compares 18 actual complex sources in logical dimensions 2–4, with full-rank and singular baths; maximum discrepancy is below 2.67e-15. It also checks both tangent derivatives on a fully saturated three-cap source.

## 2. The scalar crossing persists on all bath faces

Let G_i(t)=partial_{u_i}G_t as in the pure-flag theorem. Its zero-geometry proof uses only positivity and strict decrease of each u_j(t)/t. It therefore applies verbatim to (2): every zero of G_i is a strict negative-to-positive crossing. Since G_i(t)=4d/(3t^2)+O(t^-3)>0 at infinity, G_i is either positive everywhere or has a unique negative-to-positive crossing.

No negative sign at t=0 is assumed. On fully saturated faces G_i may have an O(1/t) singularity with either sign. The tangent derivatives below all contain an additional factor t and remain integrable. This is why the previously disproved all-saturated inward-sign shortcut is not used.

## 3. Actual overlap redistribution and eigenvalue derivatives

Fix one physical block i. Suppose it has two distinct positive eigenvalues a<b with nonzero overlaps r_a,r_b. Rotate only their eigenvectors relative to s, preserving the sum r_a+r_b. This realizes arbitrary sufficiently small redistribution r_a -> r_a+epsilon, r_b -> r_b-epsilon, with all other spectral data fixed. It is an actual logical unitary variation of this reset block alone, allowed even when its support contains s and R_i=1.

At a constrained local minimum this tangent derivative must vanish. From (2), it gives

integral_0^infinity [t G_i(t)]/[(a+t)(b+t)]dt=0.          (3)

Thus G_i cannot be positive everywhere, and must have its unique negative-to-positive crossing theta_i.

Now vary the two eigenvalues, keeping their eigenvectors and overlaps fixed. The exact partial derivatives are

partial_a Delta=-d r_a integral t G_i(t)/(a+t)^2 dt,
partial_b Delta=-d r_b integral t G_i(t)/(b+t)^2 dt.       (4)

Relative to the zero-weight integral (3), the first multiplier (b+t)/(a+t) is strictly decreasing, and the second multiplier (a+t)/(b+t) is strictly increasing. Centering each multiplier at theta_i gives the strict signs

integral t G_i(t)/(a+t)^2 dt<0,
integral t G_i(t)/(b+t)^2 dt>0.

Therefore

partial_a Delta>0, partial_b Delta<0.                    (5)

Decrease a and increase b by the same small amount. This preserves the physical reset trace, p, all overlaps, rank and support, and it strictly decreases Delta by (5). Thus no constrained local minimum can have two distinct occupied eigenvalues in any physical reset block.

The variations stay on the same constant-rank entropy stratum, including saturated heads. Their derivative integrals converge near zero because G_i=O(1/t) at worst and both weights in (3)-(4) are O(t); at infinity G_i=O(t^-2). Positivity of the support eigenvalues gives local uniform domination. No derivative in a singular off-face direction is invoked.

## 4. Zero-overlap spectators and degeneracies

A positive reset eigenvector e with <e,s>=0 gives a reference sector |i> tensor e orthogonal to success and all other reset eigenvectors. Its homogeneous deficit is zero. Removing it leaves an actual source; normalizing the remainder divides its homogeneous deficit by a number smaller than one.

Therefore a negative global minimum cannot contain any such spectator: removal and renormalization would make the negative value strictly more negative. A degenerate positive reset eigenspace of dimension at least two always contains a vector orthogonal to s. Accordingly, at a negative minimum all positive bath eigenvalues are simple and all corresponding overlaps are nonzero.

Combining this with Section 3, every reset block at a negative global minimum has rank at most one.

## 5. Compact minimum and whole value

Fix any finite logical dimension. The parameters p in [0,1] and positive reset blocks T_i of total trace one form a compact domain; the deficit is continuous. Endpoints p=0 or p=1 have zero value. If a negative value existed, a negative global minimum would exist with p,q>0.

Sections 3-4 force every reset block at that minimum to have rank at most one. This is exactly the received pure-flag class of `arbitrary_weight_three_block_pure_success_value_theorem.md`, including missing physical labels. Its value is nonnegative, a contradiction. This proves (1)'s nonnegativity for arbitrary mixed baths without any inward assumption on fully saturated faces.

## 6. Equality

Orthogonality T_i s=0 for all i gives an actual orthogonal success/reset split and zero deficit.

Conversely suppose p,q>0 and Delta=0. Remove all zero-overlap reset eigenvectors, including the directions orthogonal to s in each degenerate eigenspace. The homogeneous deficit remains zero, and normalization preserves zero. If no reset block remains, the original reset was orthogonal and the desired condition holds. Otherwise the resulting source is still in the theorem's class and is a global minimum by nonnegativity. Section 3 again rules out two distinct occupied eigenvalues within a block. Thus every remaining block has rank one. If any remaining reset vector overlaps s, the strict equality classification of the pure-flag theorem gives positive deficit, a contradiction. Hence no occupied nonorthogonal reset support was possible.

## Scope

The proof handles arbitrary noncommuting logical reset matrices because only their separate spectral measures against the one pure success vector enter the actual Gram matrices. Mixed logical success produces matrix-valued Schur complements and is not covered. No physically coherent reset terms between different physical labels are introduced or removed by this proof.
