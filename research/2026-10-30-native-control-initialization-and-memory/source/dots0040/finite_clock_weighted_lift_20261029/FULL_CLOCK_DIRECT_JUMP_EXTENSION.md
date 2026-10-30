# Full clock Hilbert-space extension for DIRECT fresh-channel reset jumps
2026-10-30. Candidate; audit requested. This is NOT the one-body-reset Stinespring compiler.

## Model and distinction
On FULL clock qubits, including illegal adjacent occupancies, take
H=g sum_h G_h X_h,
L_hs=sqrt(kappa) sigma_h^- tensor K_hs,
where Phi_h is the idempotent local SSF channel. Every reset freshly applies Phi_h on every input sector. This has high-body local jumps containing the actual SSF Kraus operators. The earlier physical compiler instead has one-body resets, and agrees with this fresh-channel action only in its clean invariant range. The distinction is essential.

Use n_h=|1><1|, Y_h=i(sigma_h^--sigma_h^+), G_h=product_{j~h}(1-n_j), m_h=sum_{j~h}n_j. Let nu=g/kappa, f_m=f0 r^m with f0>4 and small r, and set
B_h=n_h+2nu G_hY_h+nu^2 f(m_h).
It is positive on the FULL space: when m=0 the same 2x2 determinant argument applies; when m>=1 the off-diagonal drive vanishes and B_h=n_h+nu^2f_m. Uniform bounds and fixed support persist.

## Exact new terms and their absorption
Idempotence still cancels the own-site reset terms in [L,Z_h]V, leaving -(Lclock B_h)d_h+(D_hB_h)d_h, with D_hB_h=-n_h-nuG_hY_h.
For a neighbor j, B_h commutes with n_j and
sqrt(B_h)n_j sqrt(B_h)=(n_h n_j+nu^2 f(m_h)n_j).
Thus activated-neighbor contributions split into:
- C m_h n_h d_h, paid by the existing -n_hd_h when t is sufficiently small;
- C nu^2 m_h f(m_h)d_h, paid by geometric blocker service exactly as in the legal proof.
The other neighbor reset cross term is bounded by C||B_h||n_jd_j; D_sqrt(B_h)(n_j)=0. Disjoint terms cancel as before.

Pure damping obeys
D(G_hY_h)=-(1/2)G_hY_h+sum_{j~h}n_j G_{h\{j}}Y_h.
The added terms absent in the legal subspace are h-ready/excited off-diagonal. Coherent self-curvature is
 i[G_hX_h,G_hY_h]=2G_h(1-2n_h).
All neighboring Hamiltonian commutators i[G_jX_j,G_hY_h] are also h-off-diagonal; nonneighbor terms commute.
Consequently, after own-site cancellation, the exact clock contribution has:
- desired negative service -nu^2[4G_h+m_h(f_{m_h-1}-f_{m_h})]d_h;
- diagonal +8nu^2G_h n_h d_h, paid by occupation drift;
- boundedly many h-off-diagonal terms of size O(nu), and further such terms O(nu^2);
- O(nu^3) bounded-norm remainder from i[H0,f(m_h)].

For any Hermitian h-off-diagonal R, the block-form bound
±a R <=delta n_h+(a^2||R||^2/delta)(1-n_h)
holds (up to an inessential fixed factor depending on the chosen norm convention). Thus t-times O(nu) terms cost a small fixed part of n_hd_h plus O(t^2nu^2)d_h. The O(nu^2) terms cost O(t^2nu^4)d_h. Both are absorbed by positive tnu^2 service for small fixed t. The O(tnu^3) remainder is absorbed by choosing nu small relative to the finite minimum geometric blocker service.

The same first-order inequality follows on ALL clock sectors:
(L+t sum_h[L,Z_h])V<=-(1/2)sum_h n_hd_h-c tnu^2 sum_h d_h.
No legal-clock projection or stationary-clock restriction enters this extension.

## Finite-depth CP conclusion
Set Z_h to the local Lindblad generator with jumps sqrt(B_h)K_hs and T to the colored product of exp(tZ_h). The exact local similarity remainder from GEOMETRIC_BLOCKER_CP_LIFT_CANDIDATE.md remains valid on the full tensor product. The weighted overlap/orbit bounds and SSF coverage give
L*T(V)<=-c' t kappa nu^2 T(W)+bN
on the selected DATA basin and for arbitrary clock states. The Stinespring perturbation lemma therefore covers arbitrary bounded local data/clock Hamiltonian, Lindblad and shared-bath errors for this DIRECT-jump model.

All rates and local Hilbert-space resources are fixed independently of volume, but may be extremely unfavorable. This is not a native two-site construction and does not replace direct SSF reset jumps by one-body reservoir couplings. The one-body-reset compiler's complementary Stinespring sectors remain an additional physical proof obligation.
