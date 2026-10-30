# Geometric blocker credit and finite-depth CP lift
2026-10-30. NEW candidate proof; independent audit requested. Clean dressed hard-core range only; full physical dirty sectors remain separate.

## Idempotent SSF channel, with fixed finite local resources
For each hub h measure the finite set of syndrome checks affected by subsets of its generator support. Enumerate that finite affine orbit and find the minimum local syndrome Hamming weight. If the measured syndrome already achieves the minimum, apply identity (including tied minima). Otherwise apply a fixed Pauli subset taking it to one chosen minimum. All output states are block diagonal in locally minimal syndrome sectors; repeating the channel measures deterministically and applies identity. Thus Phi_h^2=Phi_h as a FULL CPTP map, not just on classical syndromes.
Every nonidentity correction drops global syndrome weight by at least one, and its changed-check set has bounded size k, giving beta=1/k. Every hub admitting an FGL candidate is active under this local optimizer; the candidate-mass active-hub lower bound is unchanged. Its truth table may be very large but is a fixed local resource, not a global optimization oracle. Rechoose weighted-animal parameters for this beta. The per-move drift, aggregate coverage and bounded-patch overlap estimates apply to the selected moves.

Write d_h=(I-Phi_h^*)V>=0. Idempotence implies Phi_h^*d_h=0 and Delta_h d_h=-d_h. For overlapping hubs establish the bounded-patch estimates
|Delta_j d_h|<=C d_j,   Delta_h d_j<=C d_h.
Absolute value here is pointwise in the common syndrome basis. The original animal completion argument proves both signs with a larger constant: all source differences affected by j complete to a bounded connected patch containing D_j and the h decision footprint; untouched animals cancel. C is independent of volume.

## Exact local clock algebra
Scale kappa=1 temporarily, nu=g/kappa. On the hard-core independent-set clock space let
n_h=a_h^dagger a_h, Y_h=i(a_h-a_h^dagger),
G_h=product_{j~h}(1-n_j), m_h=sum_{j~h}n_j,
H0=sum_h(a_h+a_h^dagger).
For pure reset D and coherent commutator H_ad=i[H0,.],
D n_h=-n_h, D Y_h=-Y_h/2,
H_ad n_h=Y_h,
H_ad Y_h=2G_h-4n_h-sum_{j~h}(a_j^dagger a_h+a_h^dagger a_j).
For a function f(m), Df(m)=m[f(m-1)-f(m)]. Other centers do not change m except its neighbors. These identities follow directly on the legal independent-set space; no stationary clock law is used.

## Positive geometric blocker observable
Choose f0>4 and 0<r<1, then f_m=f0 r^m for m=0,...,D. Set
B_h=n_h+2nu Y_h+nu^2 f(m_h).
This is positive. In a sector with m_h>=1, h cannot be occupied and B_h=nu^2 f_m. In the available h-ready/excited two-dimensional block its matrix has diagonal nu^2f0 and 1+nu^2f0, off-diagonal magnitude2nu; determinant is nu^2(f0-4)+nu^4f0^2>0. Its norm is uniformly bounded for nu<=1.
For every neighbor j, B_h commutes with n_j and
sqrt(B_h)n_j sqrt(B_h)=nu^2 f(m_h)n_j,
D_{sqrt(B_h)}^*(n_j)=0.
This is the key advantage over a constant-shift exact Poisson solution.

The exact clock drift is
L_clock^*B_h=-n_h+nu^2[4G_h-8n_h-2sum_{j~h}(a_j^dagger a_h+a_h^dagger a_j)+m_h(f_{m_h-1}-f_{m_h})]
                  +nu^3 H_ad f(m_h).
The last term has norm bounded by a degree-dependent constant times nu^3. Reset service is strictly positive in EVERY blocked sector, including two or more occupied neighbors.

## CP circuit and exact first-order linked commutator
Define the local unital Lindblad generator
Z_h(O)=sum_s K_hs^dagger sqrt(B_h) O sqrt(B_h) K_hs - {B_h,O}/2.
On data-only V, Z_h(V)=-B_h d_h. Color the enlarged local supports, and define T as the ordered finite-depth circuit of exp(t Z_h), one layer per color. Each factor is unital CP and invertible as a LINEAR map; inverse CP is not required.

For the exact joint generator L (dimensionless resets),
[L,Z_h]V=-(L_clock B_h)d_h
 -sum_j(a_j^dagger B_h a_j)Delta_j d_h
 +sum_j sqrt(B_h)n_j sqrt(B_h)Delta_h d_j
 +sum_j D_{sqrt(B_h)}^*(n_j)d_j.
Disjoint centers cancel exactly. For j=h, idempotence combines the last three terms into (D_h B_h)d_h, where D_hB_h=-n_h-nuY_h. Hence the self-plus-clock contribution is
[-nuY_h -nu^2(4G_h-8n_h-2sum_{j~h}(a_j^dagger a_h+a_h^dagger a_j)+m_h(f_{m_h-1}-f_{m_h}))-nu^3H_ad f(m_h)]d_h.

For neighbors, the last term is zero. The second term is bounded above by C||B_h|| n_jd_j and is paid by a small fraction of the original negative -sum_j n_jd_j after multiplication by t. The third is bounded by
C nu^2 m_h f(m_h)d_h.
Choose r so f_{m-1}-f_m >=2C f_m. Then at least half of the strictly positive blocker service remains. This domination is sectorwise, not a bound using the minimum service prematurely.

The term -t nu Y_h d_h is absorbed using positive 2x2 block/Cauchy estimates:
±t nuY_h <=delta n_h + (t^2 nu^2/delta)G_h,
with harmless fixed constants if desired. The exchange term of size t nu^2 is similarly bounded by delta n_h plus C t^2 nu^4 sum_{j~h}n_j. Multiply by d_h>=0 and sum; each h has boundedly many neighbors. The remaining O(t nu^3)d_h is smaller than the minimum positive t nu^2 service by taking nu sufficiently small.

Parameter order: fix animal/overlap constants C, degree D and f0; choose r<1/(2C+1). The finite minimum
qmin=min(4, min_{1<=m<=D} m(f_{m-1}-f_m)/2)>0
is possibly tiny but volume independent. Choose nu small compared with qmin and the bounded commutator constants; then choose t small. Distribute the Cauchy delta budget across the bounded number of own/exchange terms so it uses at most one quarter of baseline sum n_hd_h. With t sufficiently small, this yields
(L+t sum_h[L,Z_h])V <= -(1/2)sum_h n_hd_h-c t nu^2 sum_h d_h,
for c>0 independent of volume. Restore kappa by multiplying the RHS and generator by kappa.

## Exact finite-depth remainder: no runtime approximation
Set L_eff=T^{-1} L T. A bounded-depth local circuit conjugates each bounded-support local generator into another bounded-support linear map; its inverse factors exp(-tZ_h) are local and uniformly bounded. Taylor expansion in t therefore gives an EXACT decomposition
L_eff=L+t sum_h[L,Z_h]+R_t,
where R_t is a bounded-incidence sum of local HP identity-annihilating maps, each with cb norm <=C_R kappa t^2. Support radius, incidence and constants are independent of volume and uniform for nu<=1. This is a local circuit conjugation statement, not a global-generator-norm estimate.
The ideal local-orbit lemma gives R_t V<=C'_R kappa t^2 W. Actual SSF coverage gives sum_h d_h>=c_V W-b_V N. Choosing t sufficiently small compared with nu^2 c_V/C'_R absorbs this exact remainder:
L_eff V<=-c' t kappa nu^2 W+bN.
Push through the POSITIVE unital T:
L T(V)=T L_eff V<=-c' t kappa nu^2 T(W)+bN.
This is an exact finite-rate inequality, uniform in time and volume. It is NOT an effective Poisson approximation.

## Basin and perturbations
If the ideal inequality is restricted to a low-V basin, each Phi_h move is V-nonincreasing and sqrt(B_h) acts only on clocks. Consequently every CP circuit factor preserves that data basin in the Schrodinger picture, allowing the restricted inequality to be pushed through T. This point must be checked against the exact chosen killed-basin definition; arbitrary small-component sets not closed under correction would not suffice.
The independently verified Stinespring lemma in CP_DRESSING_NOISE_DILATION_LEMMA.md bounds arbitrary bounded-support Hamiltonian/Lindblad/shared-bath perturbations by epsilon C T(W). Thus the CLEAN-RANGE corrected barrier has the correct robustness norm.

## Remaining physical gap
The actual physical implementation has additional illegal occupancy and Kraus-complement sectors. The clean dressed generator used above is exact only on its invariant range. Generic physical perturbations leave that range, so this candidate does NOT yet prove the physical full-Hilbert threshold. A full-space drift with defect credits or a suitable exact extension is still required. The many-body guarded architecture also has not been reduced to native two-site interactions.
