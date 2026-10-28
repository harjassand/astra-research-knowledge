# A nonvacuous physical family for the joint local logical receiver

28 October 2026. Explanatory exact family, **not a new acquisition experiment**. Zero simulated or hardware source calls. This instantiates the separately reviewed contract in `ordinary_joint_local_logical_swap_recovery_20261028.md`; it does not replace its proof or receipt.

Use q logical input qubits, at least one gauge qubit, and a four-dimensional selector prepared as the known real state |x>. The source measures that selector in an UNKNOWN real orthonormal basis {v_b}_{b=1}^4 and discards the result. On branch b it applies an UNKNOWN distribution p_(alpha,b) of GLOBAL q-qubit Paulis, prepares an UNKNOWN mixed gauge state sigma_b, and applies a fixed UNKNOWN physical U. No branch flag or quantum environment is delivered separately.

Set the identity probabilities to

    p_(I,b)=(1,4/5,3/4,7/10).

The remaining probabilities in each branch can be distributed arbitrarily among the4^q−1 nonidentity strings. In particular they need not factor across logical qubits and may concentrate on high-weight correlated errors. The states sigma_b can be noncommuting, entangled across gauge sites, rank deficient or have arbitrarily tiny positive eigenvalues. The source produces

    G_alpha(x)=sum_b (v_b^T x)^2 p_(alpha,b) sigma_b.

It is a literal positive quadratic gauge instrument, not a synthetic set of state-estimation errors. Since every p_(I,b)>=7/10 and p_(alpha,b)<=1−p_(I,b),

    G_I(x)−G_alpha(x)>=0 for every alpha.

For EVERY nonidentity global Pauli P, its branch contrast is at least2p_(I,b)−1>=2/5. Consequently

    H_P(x)>=(2/5)G(x),

even though the sigma_b do not commute. Thus the supplied acquisition lower bound kappa=2/5 is valid without any gauge eigenvalue floor. The unknown selector x=v_1 is exactly correctable; the other branches have genuinely different nonzero logical losses. A nonzero-optimum family follows by reducing p_(I,1) below1 while leaving it strictly above the other three.

For locality, take U to be an unknown depth-t nearest-neighbor circuit after an unknown assignment of the q input logical factors and gauge factors to physical sites. Each logical generator then lies in its unknown site's width-at-most2t+1 causal interval. These intervals may overlap, and U may contain complex non-Clifford gates. The source's assignment/circuit is not supplied to the receiver; the promised local width is. The source can be globally complicated in its gauge preparation and Pauli error distribution while the receiver's required generator controls remain locally synthesizable.

The source-family description has an exponentially large optional Pauli probability table, but the learner does not receive, reconstruct or enumerate it. It acquires2q local generators by ordinary labeled probes, builds the reversible joint receiver, and learns the four-coordinate encoder from the actual global Clifford-input test. The all-logical Bell reference in the proof is not a transmitted training resource. The same mechanism is available to an equally informed conventional subsystem learner; no advantage, historical priority, hardware feasibility, or generic-noise claim is made.
