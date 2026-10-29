# Adaptive single-carrier upper bound, version 1

28 October 2026. Author derivation; independent review pending. This is an application of established concurrence theory, not a new entanglement law. It strengthens the comparator class, not the encoded hardware claim.

## Interface and statement

An inaccessible reference qubit R begins maximally entangled with a stored qubit B. At every compulsory noisy interval exactly one two-dimensional quantum carrier B holds all retained quantum information on the controller side. Arbitrary genuinely classical (block-diagonal, not coherent quantum pointer) records may persist. Before/between/after intervals, arbitrary local instruments may act on B, using fresh uncorrelated ancillas that are discarded or measured before the next interval. Instruments may adapt to the entire classical history. All outcomes count: no success-only conditioning. Pre-shared entanglement, retained quantum ancillas, noiseless bypasses, access to R, and measurement of the noise environment are excluded.

At step j, every history undergoes the same declared CPTP qubit channel N_j, independently of prior environment memory, or a conditional channel with a history-uniform Choi-concurrence upper bound c_j. The channel is compulsory. Let J_N=(id⊗N)(Phi) be normalized Bell Choi state and c_j=C(J_Nj). Then the total protocol's entanglement fidelity satisfies

    F_e <= (1 + product_j c_j)/2.

Source knowledge, calibration and ideal controls are freely granted to this upper bound. Hence it does not weaken the comparator through estimation error, gate error, or fitting budget. It does NOT bound arbitrary continuously driven noise whose generator or exposure is changed by the controls. Subdividing fixed dephasing intervals into arbitrarily many positive-duration fixed-generator segments and inserting ideal controls is permitted. Native phase N is an indivisible declared channel, not a derived continuous generator.

## Proof, including classical histories

Use homogeneous concurrence C(w rho)=w C(rho), and define branch resource A=sum_h p_h C(rho_RB|h). Konrad et al., arXiv:0708.0180v3 Eq (9), gives C((id⊗N)rho)<=C(J_N) C(rho). Therefore a compulsory noise step sends A to at most c_j A. This also applies to history-dependent channels bounded uniformly by c_j.

Here is a direct local-instrument argument. For a pure two-qubit vector, one-qubit Kraus K multiplies unnormalized concurrence by |det K|. Refining every instrument outcome to individual Kraus outcomes can only increase the displayed average concurrence, by convexity. For a trace-preserving instrument with Kraus operators K_a,

    sum_a |det K_a| <= sum_a Tr(K_a† K_a)/2 = 1,

by arithmetic-geometric mean on the two singular values. Apply an optimal convex-roof decomposition to mixed input and use convexity again. Thus any allowed local instrument cannot increase A. This applies separately to each history, including a final record-conditioned decoder. Initially A=1, so finally A<=product c_j.

For every pure two-qubit state psi, its overlap with any fixed maximally entangled state is at most (1+C(psi))/2, by its two Schmidt coefficients. Applying this to an optimal concurrence decomposition proves Tr(Phi rho)<=(1+C(rho))/2 for mixed rho. Summing terminal histories proves the stated bound. No assumption that the classical record is discarded before final decoding is made.

A classical measure-store-reprepare channel has at most F_e=1/2; the bound respects this floor. A weak-measurement success branch can have higher conditional fidelity without violating this all-outcomes theorem. A noisy-channel unraveling supplied by a monitored environment is a different resource and cannot be smuggled in as a free local instrument.

## Application to the actual clock model

Read `clocked_channel_v1.py` and `GOVERNING_CLOCK_MODEL_v1.md`, and the frozen source generator `../five_qubit_acquired_frame_pilot_20261028/code_and_channels.py`. Each round has a compulsory native source plus learned inverse (declared duration 2) and an additional controller window of tau=201 default time units. The native channel is unitary-pre/post-processed amplitude damping with gamma_i; therefore its Choi concurrence is sqrt(1-gamma_i), unchanged by unknown frames or the learned inverse. The dephasing channel multiplies X,Y by exp(-lambda*d), so its Choi concurrence is exp(-lambda*d), NOT exp(-2lambda*d). Total background time per round is tau. Native-phase background is already excluded by the original declared two-mode model and is not added here.

For T rounds, granting arbitrary free adaptive local instruments between all fixed segments gives

    F_e <= [1 + (1-gamma_i)^(T/2) exp(-T lambda tau)]/2.

Allowing choice of any source site per round still gives the uniform bound with gamma_min. No simultaneous redundant storage is allowed. This is a stronger comparator than an optimized final decoder on one fixed uncontrolled trajectory. It remains a one-carrier versus redundant-code comparison, NOT equal hardware cost or superiority to conventional quantum error correction.

The source parameterization uses m=20,19,18,17,16, gamma=(2m/(m²+1))²; hence sqrt(1-gamma)=(m²-1)/(m²+1) exactly. For dephasing q=exp(-lambda*d), Choi spin-flip eigenvalues are ((1+q)/2)², ((1-q)/2)²,0,0. For amplitude damping with survival amplitude c=sqrt(1-gamma), they are c²,0,0,0. These give the multipliers above directly.

`adaptive_single_carrier_bound_check_v1.py` records exact rational identities, random numerical mixed-state/instrument checks, source hashes and comparisons with frozen clocked outcomes. Numerical encoded performance remains simulation of an independently declared model, not hardware evidence or outward-certified interval arithmetic. The upper-bound theorem is analytic; floating comparisons are not presented as experimental acquisition.

## Sources and dependency scope

- Konrad et al., *A Factorization Law for Entanglement Decay*, arXiv:0708.0180v3, Eq (8) pure-state factorization and Eq (9) mixed-state contraction; primary full text inspected 2026-10-28: https://arxiv.org/html/0708.0180v3 (published as *Evolution equation for quantum entanglement*, Nature Physics 4, 99 (2008), DOI 10.1038/nphys885). This paragraph and the citation identify the established theorem; the adaptive controller derivation above is independently supplied.
- Wootters convex-roof concurrence is the definition used here; its closed spin-flip formula is used only for numerical checks, not as a new result.
- No earlier result superseded. This adds a stronger allowed-controls comparator; it does not certify the encoded simulation or resolve the native compulsory-channel physical interface.

## Heralding and negative controls

If only a declared subset of outcomes is called successful, with total probability p_s and conditional Bell fidelity F_s, the same proof gives p_s F_s <= (p_s + product c_j)/2. It does NOT give F_s <= (1+product c_j)/2. Rare high-fidelity successes must not be compared to the unconditional code without charging their yield.

Two explicit excluded-resource counterexamples explain the interface. Swapping the unknown state into a noiseless auxiliary qubit across every required noisy interval would retain F_e=1. Monitoring the classical Z-flip outcome of the dephasing environment and undoing it would also give F_e=1 for that segment although the unmonitored channel has c=exp(-lambda*d)<1. Neither is an allowed record from a local instrument before/after the declared unmonitored channel.

There is also an attainable negative comparator within the allowed class: measure the initial carrier in the Z basis, keep the bit classically throughout all compulsory channel uses, and reprepare the bit at final output. The resulting complete dephasing channel has F_e=1/2. Thus at integrated strength .1 and T=32, the simulated encoded F_e=.368335 is not merely below an upper bound: it is below this feasible classical-storage strategy. The same holds at .3 and1. This does not imply the classical strategy preserves entanglement; it marks failure of this unoptimized encoded controller in that regime.
