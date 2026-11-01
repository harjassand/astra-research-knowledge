# Finite-dilation resource flow, not a free bath

Root accounting note, 2026-11-01. Applies only to the exact conserved-charge dilation in ANCILLA_CURRENT_HYPOCOERCIVE_LIFT.md, if its assumptions are admitted.

Q=W+sum_alpha d_alpha n_alpha, d_alpha>=d_min>0, commutes with the specified strong controller Hamiltonian. Ideal lowering resets therefore satisfy

 d E[Q]/dt=-gamma sum_alpha d_alpha E[n_alpha].

The expected number of lowering resets through T is gamma integral E[N_aux]dt. If all additional physical mechanisms have a WARRANTED positive-charge injection bound Tr[(L_noise^* Q)rho]<=I_n(t), then

 E[number of lowering resets through T]
 <=[E Q(0)+integral_0^T I_n(t)dt]/d_min.

For bounded-support Pauli Hamiltonian terms, |Delta Q|<=b_Q gives ||i[P,Q]||<=b_Q; their injection contribution is at most b_Q sum||B_P(t)||. Analogous local dissipative terms must be bounded using their actual maps. Thermal upward resets contribute gamma_up sum d_alpha P(ancilla ground), and their OWN event counts/preparation cost are additional. Coherent physical/bath couplings, initialization, and all ancillary registers remain in the ledger.

This shows why an arbitrarily rapid nominal reset rate does not itself imply that arbitrarily many resets are consumed. It is an EXPECTED resource count, not a rare-history certificate. The separate current-corrected exponential Lyapunov proof is essential for the logical-memory claim.

Q is a mathematical conserved charge. It must not automatically be called the complete thermodynamic energy: a physical Hamiltonian E Q+H_int also contains interaction energy, and realizing a local reset can involve work as well as heat. Reservoir preparation, entropy export, monitoring, circuit synthesis and the fixed high-body couplings remain charged. No finite reservoir has been proved to maintain the assumed Markov service for an exponentially long time. The ordinary active competitor receives the same paid services.
