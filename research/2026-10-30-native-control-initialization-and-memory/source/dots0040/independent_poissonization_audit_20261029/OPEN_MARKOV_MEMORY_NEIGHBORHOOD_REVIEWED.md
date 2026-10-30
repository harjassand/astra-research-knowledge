# An open Markovian memory neighbourhood from deliberately added local mixing
2026-10-29 23:16 UTC. Root synthesis of the reviewed transactional CPTP-kick memory construction and the new Choi-interior reduction. The reduction's independent review is in progress at this writing. No practical performance advantage or historical priority is claimed.

## Consequence
The previous memory theorem was restricted to genuine bounded-rate stochastic CPTP faults. This construction gives an OPEN SET of continuously perturbed Markov generators around a modified, time-independent autonomous memory. The modification is real, deliberately added full local mixing. The new guarantee does not require identifying the unknown perturbing channels.

Let L0,N be the fixed transactional memory generator on a bounded-degree physical graph, with uniformly bounded site dimensions. Its independent proof supplies a nonzero admissible local CPTP-kick intensity epsilon_star and decoded memory error O(poly(N,t) exp(-c sqrt(N))) from the declared encoded-input / ready-controller initialization. Its exact decoder and resource qualifications are unchanged.

Fix a family of bounded-size physical patches Z with bounded incidence and bounded Hilbert dimensions d_Z<=D. The family includes every perturbation support that is to be protected. For each patch install the ACTUAL complete replacement channel

 R_Z(X) = (I_Z/d_Z) tensor Tr_Z X

as Markov mixing at rate delta_Z. Choose all these rates below the kick threshold, with their patch incidence charged. Define

 Lbar,N = L0,N + sum_Z delta_Z (R_Z-id).

For arbitrary measurable time-dependent local perturbations N_Z(t) which preserve Hermiticity, annihilate trace, and obey

 ||N_Z(t)||_diamond <= delta_Z/d_Z^2,

set Phi_Z(t)=R_Z+N_Z(t)/delta_Z. Using normalized Choi matrices,

 J(R_Z)=I/d_Z^2,
 ||J(N_Z)||_infinity <= ||J(N_Z)||_1 <= ||N_Z||_diamond.

Hence Phi_Z(t) is completely positive and trace preserving. EXACTLY, with no short-time or weak-coupling approximation,

 Lbar,N+sum_Z N_Z(t)
   = L0,N+sum_Z delta_Z [Phi_Z(t)-id].

The right-hand side is the already controlled Poisson-CPTP fault model at the same fixed rates delta_Z. The full autonomous memory guarantee therefore holds throughout the indicated local generator neighbourhood. Strict inequalities give a genuine positive margin. The perturbations may include local coherent Hamiltonian drift and signed differences between ideal and actually deformed reset generators. No covariance, Pauli mixture, known noise basis or total-variation bound in time is imposed.

The small constant depends on fixed local dimension/patch incidence and the existing memory threshold, not total system size. If a uniform norm budget eta is known, the sufficient choice delta=D^2 eta is explicit, subject to delta remaining below the memory's local intensity budget. Alternatively fix a small delta once and certify the bound eta<delta/D^2; knowing the detailed N_Z is unnecessary.

## Native onsite corollary
When every unknown perturbation is supported on ONE physical site (the complete declared controller or data-resource qudit), install only onsite R_i. The architecture still has two-site coherent Hamiltonian terms and onsite dissipative channels. Full onsite replacement has one-site Kraus operators |a><b|/sqrt(d_i), so it is within the same locality form as the existing reset apparatus. It acts on controller/workspace and data sites alike. This covers onsite controller drift and onsite reset deformation, not just DATA noise.

The local dimension may be very large. The factor d_i^2, the number of mixing channels, and the already poor analytical threshold are genuine costs. This is a uniform-in-N existence result, not a numerically useful hardware threshold.

For multi-site perturbations, the proof requires full JOINT patch replacement. Independent onsite depolarizing GENERATORS do not furnish its Choi interior; in particular they need not cover a two-site coherent operator direction. A general bounded-patch theorem is valid only with that extra engineered primitive. The native onsite result must not be marketed as robustness to arbitrary two-site coupling calibration errors.

## Records and imperfect apparatus
The added mixing changes the real generator. It is not fictitious twirling or a relabeling of the original unmodified dynamics. The equality above supplies an exact positive quantum-trajectory representation of the modified unconditional evolution, including the nominal clean reset channels. Thus the previous killed-instrument proof may be used in this mathematically equivalent unraveling even if the original physical reset operators were deformed. The architecture makes no external decisions from those records, so the unconditional memory channel is unchanged by this choice of analysis representation.

This does NOT identify the chosen analysis records with an actual laboratory detector's original records. An operational record-output claim or feedback protocol would require separate instrument equivalence. The theorem here concerns the unconditional stored information and its stated final decoder.

Added mixing need not be asserted perfectly calibrated without qualification. Any implementation error belongs in the total local perturbation budget. For example, if its error is bounded by chi delta plus a native error eta, the sufficient margin is delta/d^2 >= eta+chi delta; this requires chi<1/d^2. All pump/reset and noise-source resources are real and remain extensive at fixed per-site rates.

## What remains outside this result
- Arbitrary uncontrolled retained system-bath couplings are not finite-dimensional system-local N_Z. Depolarizing only the system does not supply a Choi cushion in unrestricted bath directions.
- No improvement of the actual lifetime over the unmodified apparatus is proved. Added mixing buys a robust guarantee, and may reduce practical performance.
- This does not remove clean encoded initialization, final decoding, finite-rate control calibration, or graph-routing requirements. The onsite corollary leaves coupling errors outside its stated support class.
- High encoding rate is with respect to bounded-dimension graph sites; no fixed-dimensional geometric layout or translation invariance is supplied.
- Choi positivity via added isotropic noise is elementary/established machinery. The proposed consequence is its composition with the explicit autonomous memory construction; historical novelty still requires comparison.
