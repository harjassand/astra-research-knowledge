# Generic two-design guard: a stronger baseline and an abstraction of the controller
2026-10-29. Root comparison/extension; no uniqueness or advantage claim for symmetry tests.

The sequential proof uses only an actual positive test satisfying e_h≤C q_h for every current source/memory state, plus the complete private-pad service instrument. It is not specific to a singlet code.

Fix logical dimension K=2^k and any known candidate encoder E and CPTP decoder D that return exactly K logical dimensions. On TEST, prepare a uniformly random logical Clifford applied to |0^k>, execute E→N→D, apply the inverse Clifford, and measure whether all bits are zero. The prepared pure states form a state2-design. For the resulting logical channel Λ,
 Favg=(K Fe(Λ)+1)/(K+1),
so the ACTUAL nonnegative failure bit has mean
 q=1−Favg=K/(K+1)(1−Fe),
and therefore e=(K+1)q/K exactly. No protected reference or joint Bell measurement is needed.

The source's averaged input E(I/K) is the same for this test and for the freshly Pauli-padded service. The current random Clifford/state/role must nevertheless not leak through extra pulse/timing/routing controls. This average-state equality is not an excuse to omit the physical same-port requirement.

Substitute C_2design=(K+1)/K≤3/2 into the already proved sequential hazard/NB guard. The same actual outer correction and accepted finite-operation guarantee follow for arbitrary retained source memory. A policy may predictably choose different known E_h,D_h based on previous allowed classical records, provided the logical dimension stays fixed and each current test/service uses the same selected pair of operations and complete boundary. Neither a correct noise model nor a provably successful learner is required for SOUNDNESS. Finding actions with low failure, keeping state/control cost manageable, and maintaining good acceptance/YIELD remain separate problems. Adaptive choices do not turn favorable past data into guaranteed future noise performance.

This is a strong conventional safe-controller baseline. It executes full logical Clifford preparation, actual encoder and decoder, inverse Clifford and logical readout on EVERY test. The local symmetry witness replaces those test controls with signed singlet matching/constant-seed preparation and pair readout, but pays C=O(n) rather than approximately1. Both execute the full code on actual service calls. It is not established that the local route wins overall: qubit Schur transforms can be efficient, random-state preparation has ordinary polynomial circuits, and at n=4 all these test gadgets are small.

For the finite n=4 example, the two-design coefficient is1.5, versus exact weighted-symmetry coefficient3 or declared conservative6. At fixed R=1, expected trial overhead per service is C+1:2.5 for two-design,4 for exact weighted symmetry,7 for the conservative illustrated guard, before source failures and cap effects. The symmetry route must therefore justify its calibration-control savings rather than claim statistical superiority. Quantum authentication plus correction is an additional stronger conceptual competitor.

The controller abstraction does NOT solve efficient, feature-free learning of a good encoder/recovery for every unknown quantum process. It provides a finite accepted-operation safety wrapper around whichever candidate-generation mechanism and physical controls are actually available. No new quantum-authentication concept, fault-tolerance threshold, key-recycling scheme or practical advantage is asserted here.
