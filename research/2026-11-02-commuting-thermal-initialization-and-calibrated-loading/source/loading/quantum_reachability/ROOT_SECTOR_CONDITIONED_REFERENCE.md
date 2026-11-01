# Root construction: preserve conserved bath charges rather than demand canonical reweighting

1 November2026. Conditional stationary-reference extension, not a preparation algorithm.

Suppose the actual Hamiltonian is block diagonal in conserved classical bath labels b:
 H = direct_sum_b H_b,
with logical Pauli operators acting only on memory and identically in each block. Suppose every conditional H_b satisfies the same static rare-bad-syndrome estimate p_b<=p_n and the same local commutator bound/correctability premises, uniformly in b. Each H_b may include a uniformly weak local noncommuting memory perturbation.

For ANY supplied probability distribution pi_b, define
 sigma = direct_sum_b pi_b exp(-beta H_b)/Z_b.
This is stationary under the ACTUAL Hamiltonian, whether or not pi_b equals the canonical bath weights Z_b/sum Z_b. No operation needs to change a conserved bath charge to make this reference stationary.

For a logical Pauli Q, relative entropy decomposes blockwise:
 D(Q sigma Q || sigma)=sum_b pi_b D(Q rho_b Q || rho_b).
The sector weights and log partition constants cancel. Thus the same 2 beta v n p_n bound holds, followed by the logical twirl and reference-safe exact-H storage estimate. Logical overwrite retains the physical bath-label distribution automatically. A bath-marginal obstruction to the canonical FULL Gibbs state is therefore not by itself an obstruction to the MEMORY CAPABILITY.

This does not erase the central preparation problem: one must prepare the correct conditional memory state for the actual b, or prove a weaker sufficient admission for a reachable state. Reading b may be impossible without an admitted interaction/measurement service; knowing its distribution is not the same as knowing its realization. Coherent superpositions between sectors require a separate argument and are excluded here.

A trivial coupling through stabilizers alone would make the logical algebra commute with H on the full Hilbert space; it is not a consequential substitute for generic damaging interactions. Any proposed conditional sampler or physical preparation must retain nontrivial logical-error mechanisms and charge controls, spectroscopy, cooling and residual faults.

This construction changes the stationary reference to match an actual conservation law. It is a mathematical tool for removing an unnecessary canonical-bath requirement, not a completed local noisy loader, a universal bath result or a claim of new generalized-Gibbs theory.
