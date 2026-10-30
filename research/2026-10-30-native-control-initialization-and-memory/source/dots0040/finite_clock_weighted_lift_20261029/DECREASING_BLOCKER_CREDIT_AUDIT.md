# Independent audit: decreasing-blocker CP credit closes the legal-range signed overlap estimate
2026-10-30. Audit of parent's new construction. This replaces the scalar-shifted Poisson credit; the earlier finite-t scalar-Poisson counterexample does not apply.

## Inputs and conventions
Scale time so kappa=1, put nu=g/kappa. Let a_h be hard-core lowering, n_h=a_h^*a_h, Y_h=i(a_h-a_h^*), X_h=a_h+a_h^*, G_h=product_{j~h}(1-n_j), and m_h=sum_{j~h}n_j. The overlap graph includes complete data-channel decision supports. Assume Phi_h is an idempotent CPTP map, d_h=V-Phi_h^*V>=0, and the bounded-patch estimates
|Delta_j d_h|<=C d_j, Delta_h d_j<=C d_h
for adjacent pairs (the first is a two-sided diagonal operator inequality). Channels at nonadjacent sites commute. All these conditions concern syndrome-diagonal V and its local update images.

Choose f_m=f0 r^m, f0>4, 0<r<1/(2C+1), and define
B_h=n_h+2nu Y_h+nu^2 f(m_h).
On legal clock configurations with m_h>=1, B_h=nu^2 f(m_h) is scalar in h. On m_h=0, its h-qubit matrix has diagonal (nu^2 f0,1+nu^2 f0), off-diagonal magnitude2nu, and determinant nu^2(f0-4)+nu^4 f0^2>0. Thus B_h>0. It has a bounded local full-qubit extension obtained by using guarded Y_h=G_h i(sigma_h^- -sigma_h^+) and the same diagonal terms.

## Exact hard-core identities
With D* the summed clock damping adjoint and H0=sum X_h,
D*Y_h=-Y_h/2,
i[H0,Y_h]=2G_h-4n_h-sum_{j~h} E_hj,
E_hj=a_j^*a_h+a_h^*a_j.
Neighbor resets give zero on Y_h: both their anticommutator and gain vanish on the legal space. Nonneighbor terms commute. The exchange sign is MINUS.

Consequently
L_clock*B_h=-n_h+nu^2[4G_h-8n_h-2sum_j E_hj+m_h(f_{m_h-1}-f_{m_h})]
             +nu^3 i[H0,f(m_h)].
The final commutator is bounded and local: only neighboring centers contribute, with their own local guards.

## Exact first-order CP commutator
Let Z_h be the local Lindblad generator with jumps sqrt(B_h)K_hs; equivalently
Z_h(O)=sqrt(B_h)Phi_h^*(O)sqrt(B_h)-{B_h,O}/2.
The exact general identity in CP_OVERLAP_AUDIT.md applies. Idempotence gives Delta_h d_h=-d_h. Therefore the j=h cross terms combine to D_h*B_h d_h, where
D_h*B_h=-n_h-nu Y_h.
This cancels the n_h Poisson-scale term and leaves
-(L_clock*B_h-D_h*B_h)d_h
=[-nu Y_h-nu^2(4G_h-8n_h-2sum_j E_hj+m_h(f_{m_h-1}-f_{m_h}))
  -nu^3 i[H0,f(m_h)]]d_h.

For j~h, [B_h,n_j]=0 exactly, and
sqrt(B_h)n_j sqrt(B_h)=nu^2 f(m_h)n_j,
a_j^*B_h a_j=nu^2 f(m_h-1)n_j.
Thus their cross contribution is EXACTLY
nu^2 n_j[f(m_h) Delta_h d_j-f(m_h-1) Delta_j d_h].
All nonneighbor terms cancel by channel commutation and clock commutation, even when their data decrements involve the same large animal.

## Signed absorption
The potentially activated-neighbor term obeys
sum_{j~h} nu^2 f(m_h)n_j Delta_h d_j
 <=C nu^2 m_h f(m_h)d_h
 <=(nu^2/2)m_h(f(m_h-1)-f(m_h))d_h
by the choice of r. This is the key missing sign control in the scalar-Poisson construction.
The other neighbor term is bounded above by C nu^2 f0 n_jd_j and is absorbed into the ORIGINAL -sum_j n_jd_j drift after summing boundedly many neighbors and taking t small.

Let sigma=min(4,min_{1<=m<=D} m(f_{m-1}-f_m)/2)>0. Ignoring absorbable positive n_h terms, the diagonal service contribution is at most -t nu^2 sigma d_h.
The coherence is controlled by the two-block form bound
±t nu Y_h d_h<=a n_h d_h+(t nu)^2 a^{-1}(G_h-n_h)d_h.
The exchange contribution satisfies similarly
±2t nu^2 E_hj d_h<=a n_h d_h+4t^2 nu^4 a^{-1}n_j d_h.
Choose a small fixed degree-dependent constant so all n_h costs consume less than a fixed fraction of the original occupation drift. The residuals are O(t^2 nu^2)d_h and O(t^2 nu^4)d_h, hence are absorbed by t nu^2 sigma d_h for small t. The last Hamiltonian commutator costs O(t nu^3)d_h; choose nu small compared with sigma and its fixed local coefficient norm. The positive 8t nu^2 n_h term and the neighbor n_jd_j costs are also absorbed for small t.

It follows that for sufficiently small positive nu,t, independent of volume,
[L*+t sum_h [L*,Z_h]]V
 <=-(1/2)sum_h n_h d_h-c t nu^2 sum_h d_h
for some c>0 depending only on the fixed local geometry and f. All clock/data form inequalities commute between the clock and syndrome factors, so no state factorization is assumed.

## Finite-depth product and exact remainder
Color the enlarged local supports of Z_h with a fixed number of colors and set T to the corresponding finite-depth ordered product of exp(tZ_h). Each factor is unital CP; its inverse exp(-tZ_h) is local, Hermiticity-preserving and unital, though not CP.
The conjugated generator T^{-1}L*T is an exact sum of uniformly bounded-support local superoperators. Conjugating each original local term through the fixed number of layers enlarges its support through only a fixed causal neighborhood; only boundedly many gates per layer meet it. Its Taylor expansion is
T^{-1}L*T=L*+t sum_h[L*,Z_h]+R_t,
with R_t decomposed into local HP/I-annihilating terms of norm <=C_R t^2 per original center, uniformly in volume. This does NOT require incorrectly factoring the whole circuit into one near/far product.
The established local syndrome-orbit estimate gives R_t(V)<=C'_R t^2 W. Combining weighted coverage sum_h d_h>=c_0 W-b_0 N and choosing t sufficiently smaller than nu^2 c c_0/C'_R yields
(T^{-1}L*T)V<=-c_1 t nu^2 W+b_1 N.
Apply the positive unital T to obtain the EXACT finite-rate legal-range inequality
L*T(V)<=-c_1 t nu^2 T(W)+b_1 N.
There is no runtime-growing approximation: the finite Taylor remainder is absorbed pointwise in the observable drift.

## Remaining boundary
This audit supports the legal independent-set, idempotent-channel construction, conditional on the stated bounded-patch decrement estimates and the already accepted ideal weighted coverage/orbit lemmas. It does not show that the actual physical full-Hilbert dressed generator equals this legal clock model outside the clean invariant range. Illegal occupancies and Kraus-complement sectors need a further physical extension or defect-weighted barrier. The local full-qubit extension of B and Z supplies a local CP dressing, but alone does not resolve that generator mismatch.
