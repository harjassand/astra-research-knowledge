# Root protection/access bound: loading must leave the stationary admission region

1 November 2026. Elementary consequence of the same local logical algebra. Not a no-go for memory loading or a novelty claim.

Let Q be a decoded memory logical Pauli, P_good commute with Q, and every allowed bounded-support memory operator A obey [Q,A]P_good=0. Because Q,A are Hermitian, its commutator is supported on P_bad on both sides. Include arbitrary bath/input/controller coefficients in the local interactions. Let H_c(t) have total norm of memory-touching terms at most h(t)n, and any local jump terms have summed squared norms at most gamma(t)n with the same full logical correctability property.

Then for every joint state, including correlated quantum input and controllers,
 |d <Q>/dt| <= 2n [h(t)+gamma(t)] Pr(P_bad at t).
Terms confined to external controllers or bath contribute zero. The jump claim requires full dissipator correctability, not just a jump commutator alone.

If an intended write changes <Q> by Delta, integrating gives
 Delta <= 2n integral_0^tau [h(t)+gamma(t)] p_bad(t) dt.
Thus a write in polynomial physical time with bounded control density cannot keep p_bad exponentially small throughout. Some phase of loading must exit the protected equilibrium-like syndrome region, change the protected algebra/code, or use interactions outside the admitted bounded-support set.

In particular, suppose reference comparison establishes at every time p_bad(t)<=sqrt(K(t) r_n), where r_n=poly(n)exp(-c n^eta), and total control action A=integral[h+gamma]dt is polynomial in n. For a nonzero Delta, max_t K(t) >= Delta^2/(4 n^2 A^2 r_n). The loading path therefore cannot stay within the sub-stretched-exponential collision-divergence admission region, even if its endpoint can return there.

This explains why keeping the delivered storage certificate invariant during local coherent-SWAP compilation is the wrong target. It does NOT rule out an efficient write followed by a demonstrated return to a protected ensemble. It also does not rule out code deformation, local dissipative cooling with charged entropy export, or a different decoder during the write. The decisive constructive question is this return operation, with faults and input coherence included.

## Endpoint condition, not path condition
The published-to-user theorem is an idle storage theorem. A successful loading extension can allow large transient p_bad and then prove BOTH:
(1) preservation of the arbitrary logical input/reference through the transient;
(2) an endpoint thermal-admission or other exact-dynamics storage guarantee.
Merely demonstrating low final syndrome energy or a correct ideal logical circuit establishes neither jointly under physical faults.
