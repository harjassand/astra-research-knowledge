# Positive subset moments for a coherent constant-depth stabilizer source
30 October 2026. Root working theorem and conditional source receiver. Independent review pending. No classical fault records are attached to arbitrary signed quantum noise.

## 1. Prepared-product defect basis
Let |p>=tensor_i |p_i> be a known product stabilizer state on M finite-dimensional system sites (qubits suffice). Define disjoint commuting defect projectors B_i=I-|p_i><p_i|. A declared depth-D circuit U of bounded-size gates, bounded incidence and bounded per-gate duration prepares a known stabilizer state. D and all lightcone bounds are independent of M. Raw measurement may be deferred into local pointer qubits because no adaptive quantum feedforward is performed yet.

Assume actual dynamics in the ideal circuit interaction picture has centered, normal, bounded-system-body HP perturbation terms, with body size at most q' and per-site incident joint adjoint-cb norm sum <=eta'. The total actual evolution and required normal propagators are CPTP; bath-only dynamics are separated. This follows from the usual fixed-depth bounded-support unitary circuit with residual local generator noise, paying finite lightcone constants. It is NOT automatically established for an arbitrary noisy autonomous classical gate scheduler or an unqualified reset/clock compiler.

The bath may be shared, arbitrarily large and retained. Initial system |p> is pure, so its joint initial state factors from the bath; an explicit warm-source moment generalization is below.

## 2. Actual positive local-stochastic defect statistics
For ANY subset S define F_S(theta)=exp(theta sum_(i in S) B_i), theta>0. Terms whose system support misses S annihilate this observable after identity centering. For a term meeting at most q' of these projectors, the finite-system-leg expansion and relative congruence give

 N_e^*F_S <= C exp(a theta) ||N_e^*||_cb F_S,

where a,C are fixed finite local-dimension/body constants, e.g. a may be chosen conservatively proportional to q'. Sum only incident terms, obtaining

 L_I^*F_S <= C eta' exp(a theta)|S| F_S.                (1)

This is an operator bound with bath identity, uniform over reference amplification. Initial moment equals1. After circuit duration tau,

 Tr F_S rho_I(tau) <= exp[C eta' tau exp(a theta)|S|].

Because product_(i in S)B_i <= exp(-theta|S|) F_S,

 Pr{every site in S defective} <= [exp(-theta+C eta' tau exp(a theta))]^|S|.

For a C eta' tau<1, choose exp(a theta)=1/(a C eta' tau). The resulting parameter is

 p_*=(e a C eta' tau)^(1/a).                           (2)

Thus the ACTUAL joint spectral measurement of the commuting B_i has local-stochastic upper tails at every subset, with no prefactor exp(O(eta' M tau)). The measurement is an analytic tool, not an asserted physical noise unraveling. Coherences between different defect supports remain in the actual source.

The bound uses per-site incident strength. A total O(eta M) bound alone would not give (1) uniformly for every S. Constants can be very poor; no engineering threshold is claimed.

## 3. From positive statistics to retained coherent correctable span
For qubit product eigenstates, each defect pattern e labels a one-dimensional system basis state |p_e>=Z^e|+>^M (with X replacing Z for |0> inputs). Let G be a set of patterns for which the declared ideal source/readout/correction channel sends EVERY coherent linear combination of these basis states, with arbitrary retained coefficients, into one common correctable output module for each actual record. This is a DETERMINISTIC FULL-SPAN premise. Marginal correctness averaged over records does not imply it.

P_G=sum_(e in G)|p_e><p_e| is a positive projector. Equation (2) and an ordinary combinatorial bad-support estimate bound delta=Tr[(I-P_G)rho_I]. Gentle compression gives ||rho_I-P_G rho_I P_G||_1<=2 sqrt(delta), with the usual harmless subnormalization term if a normalized comparison is chosen. Apply the SAME actual later CPTP maps contractively; on the good part the supplied full-span identity gives the desired logical module.

This transfers a deterministic Pauli-support certificate to coherent/common-bath noise via a POSITIVE good-subspace cut, not a triangle sum over exponentially many fault paths. A published stochastic statement can provide the bad-support estimate only after its underlying deterministic certificate and common actual-record output module have been verified.

For ATG specifically, U consists of graph CZ preparation, bulk H and parallel bulk graph-to-pointer CNOT. Graph degree and edge-color depth are fixed by the code check degree. Input Z defects on graph qubits commute all CZ; after raw readout a bulk graph-input defect or its pointer-input X defect becomes a raw outcome flip, while a boundary graph defect becomes boundary Z error. Consequently the effective fault support can be covered by the OR of two input defects per bulk site. This algebra is being checked independently; it is not a grant of the whole ATG decoder's good-span property.

## 4. Noisy raw product preparation, if actually supplied
The exact-pure start can be replaced by a subset moment bound Tr F_S rho0<=exp(beta(theta)|S|). Then replace the exponent in section2 by -theta+beta(theta)+C eta'tau exp(a theta).

For actual onsite complete resets to |p_i> at rate kappa, the nominal adjoint gives exactly

 L_reset^*F_S=-kappa(1-exp(-theta))(sum_(i in S)B_i)F_S.

With the same local noise estimate and scalar spectral Jensen, x_S=Tr F_S rho obeys

 (log x_S)'<=-k log x_S+C eta' exp(a theta)|S|,
 k=kappa(1-exp(-theta))/theta.

From an arbitrary initial correlated state x_S(0)<=exp(theta|S|), a finite burn-in t_R yields

 beta(theta)<=theta exp(-k t_R)+C eta' exp(a theta)/k.

At sufficiently small fixed eta'/kappa, select theta, then a finite t_R independent of M, so this plus the subsequent circuit term is strictly less than theta. This earns a small local-stochastic defect parameter without requiring global product trace fidelity or independent reset successes. The actual onsite resets and their powered reservoirs are resources; a nominal reset operation is not a proof of a laboratory implementation.

## 5. Exclusions
No unknown input encoding, reliable classical record capture/storage, actual baseline programming, noisy final dense correction, autonomous trigger, physical acceptance filter, or universal computation is constructed here. A time-growing circuit depth or growing check weight changes q',tau and constants and cannot be inserted silently. Imperfect measurement record effects must be included in the deferred-readout circuit/model or separately earned. The positive-source method addresses the coherent source seam only if the exact circuit/noise and deterministic decoder interfaces are established.
