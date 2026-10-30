# Full-clock-tensor audit for the DIRECT fresh-K reset model
2026-10-30. This is a direct bounded-body Lindblad architecture, NOT the one-body-reset/Stinespring compiler outside its clean code.

## Model
All clock occupation patterns are allowed. Let a_j=sigma_j^- on ordinary tensor-product qubits, n_j=a_j^*a_j, P_j=1-n_j, G_j=product_{k~j}P_k, Y_j=i(a_j-a_j^*), and H0=sum_j G_j X_j. Physical jumps are a_j tensor K_js, so each completed reset directly performs Phi_j. Time is scaled by kappa; nu=g/kappa.

Use B_h=n_h+2nu G_hY_h+nu^2 f(m_h), m_h=sum_{j~h}n_j, f_m=f0 r^m, f0>4. This is positive on the FULL tensor product: at m=0 the h-qubit determinant is nu^2(f0-4)+nu^4 f0^2>0; at m>0 it is diagonal n_h+nu^2 f_m. No illegal-occupancy projection is used.

Assume the same idempotent data channels and bounded-patch decrement comparisons as in DECREASING_BLOCKER_CREDIT_AUDIT.md.

## Exact neighbor identities and the extra gain term
For j~h, B_h commutes with n_j, so
sqrt(B_h)n_j sqrt(B_h)=(n_h n_j+nu^2 f(m_h)n_j),
D_{sqrt(B_h)}^*(n_j)=0.
However the reset gain has an ADDITIONAL off-diagonal term:
a_j^*B_h a_j=n_j[n_h+2nu G_{h\j}Y_h+nu^2 f(m_h-1)],
where G_{h\j}=product_{k~h,k!=j}P_k.
This whole operator is positive and bounded above by ||B_h||n_j. Therefore its contribution multiplied by -Delta_j d_h is bounded above by C||B_h||n_jd_j and is absorbed by the original occupation drift. The extra off-diagonal gain must not be silently omitted, but it causes no new obstruction.

The activated-neighbor term splits as
(n_hn_j+nu^2 f(m_h)n_j) Delta_h d_j.
The first part is <=C n_hn_j d_h and sums to <=CD n_h d_h, paid by the original occupation drift after multiplying by sufficiently small t. The second part is exactly the decreasing-f term already paid by m_h(f_{m_h-1}-f_{m_h}) service.

## Clock derivatives on the full tensor product
D_h^*(G_hY_h)=-(G_hY_h)/2,
D_j^*(G_hY_h)=n_jG_{h\j}Y_h for j~h,
and other resets contribute zero. Also
i[G_hX_h,G_hY_h]=2G_h(1-2n_h).
For j~h, the commutator i[G_jX_j,G_hY_h] is h-off-diagonal and has norm <=2. For nonneighbors it vanishes. Finally
D^* f(m_h)=m_h(f(m_h-1)-f(m_h)),
and i[H0,f(m_h)] is a bounded local operator with contributions only from neighboring centers.

Thus L_clock*B_h is the sum of:
 -n_h;
 +2nu sum_{j~h}n_jG_{h\j}Y_h;
 +4nu^2 G_h(1-2n_h);
 +2nu^2 sum_{j~h}i[G_jX_j,G_hY_h];
 +nu^2 m_h(f(m_h-1)-f(m_h));
 +nu^3 i[H0,f(m_h)].
The own Hamiltonian nu G_hY_h cancels the own damping -nu G_hY_h, as in the legal model.

Idempotence again makes the self cross terms equal D_h*B_h d_h, with D_h*B_h=-n_h-nu G_hY_h. Hence the first-order commutator contains the extra h-off-diagonal pieces
-t nu G_hY_h d_h-2t nu sum_{j~h}n_jG_{h\j}Y_h d_h,
as well as the h-off-diagonal neighbor-Hamiltonian terms of order t nu^2.

## Absorption and conclusion
Any Hermitian h-off-diagonal operator C_h has a two-block form bound
±s C_h d_h<=a n_h d_h+s^2||C_h||^2 a^{-1}(1-n_h)d_h.
Choose a fixed small degree-dependent a and sum the boundedly many terms. The extra O(t nu) pieces cost only O(t^2 nu^2)d_h after consuming a fixed part of -n_h d_h. The O(t nu^2) pieces cost O(t^2 nu^4)d_h. Both are absorbed by the fixed positive service scale t nu^2 sigma for sufficiently small t. The nu^3 commutator is absorbed by choosing nu sufficiently small. The positive 8t nu^2 G_hn_h term, activated n_hn_j terms, and reset-gain n_jd_j terms are absorbed by the remaining baseline occupation drift.

Therefore the SAME first-order inequality holds on the FULL clock tensor product:
[L*+t sum_h[L*,Z_h]]V<=-(1/2)sum_h n_h d_h-c t nu^2 sum_h d_h,
with Z_h the local Lindblad generators having jumps sqrt(B_h)K_hs. All constants depend only on fixed local geometry and comparison constants, not volume or occupation sector.

The finite-depth local conjugation remainder proof from DECREASING_BLOCKER_CREDIT_AUDIT.md now applies without any clock-code restriction. It yields the exact finite-rate clean drift
L*T(V)<=-c' t nu^2 T(W)+bN
on the relevant data basin and arbitrary clock states. Combined with the independently proved Stinespring-dilation perturbation lemma, this supplies the direct fresh-K architecture's generic local clock/data Hamiltonian/Lindblad perturbation interface, including shared-bath local Hamiltonians.

## Scope
This establishes no native two-site realization. The physical reset jumps a_j tensor K_js directly contain the local correction Kraus operators and are generally bounded-body operations. It also does not extend the original one-body-reset physical compiler's dirty Kraus sectors by relabeling them: that compiler has a different full-Hilbert generator. The direct architecture is a genuine explicit full-tensor intermediate, not an effective-Poisson assumption.
