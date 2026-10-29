# Input/output boundary requirements for the clocked code construction

28 October 2026. Independent derivation supplied to the boundary authors. These are standard channel-composition facts and an explicit perfect-code synthesis target, not a claimed new code or received review of an unbuilt circuit.

## 1. The old terminal map contains recovery

Let V: C^2 -> C^32 be the five-code isometry. Let E_a, a=0,...,15 be identity and the fifteen weight-one Pauli representatives. The perfect code has

    V† E_a† E_b V = delta_ab I_2.

Consequently the square matrix W=[E_0 V | E_1 V | ... | E_15 V] is unitary. Under the coordinate convention |a>_syndrome tensor |l>_logical,

    W† E_a V |l> = |a> tensor |l>.

Thus the completely positive trace-preserving map

    D(X)=Tr_syndrome(W† X W)
        =sum_a V† E_a† X E_a V

is exactly the previously used ideal recovery followed by logical decoding, on ALL physical input operators, including code/syndrome coherences. The equality follows by the partial-trace Kraus rows of W†, not just correctable inputs. The initial isometry V is realized by W acting on |0000> tensor |psi>.

This provides an explicit finite unitary synthesis target. It does not grant a free 32-dimensional gate. Its actual decomposition, gate scheduling, preparation of four clean qubits, control errors and live-qubit background must be supplied. W is a specific extension of V; the inverse of another arbitrary extension of V need not implement D. Merely executing inverse encoding and discarding four qubits can leave syndrome-dependent logical byproducts.

The target matrix is independent of the unknown native noise. That fact does not remove control calibration, noisy initialization or input injection costs.

## 2. Complete boundary composition

Let C be the actually implemented five-carrier storage/recovery channel, including every noisy time interval. Let E and D be ideal encoding and syndrome recovery/decoding. Let E_tilde and D_tilde be physical boundary channels. For half-diamond errors

    alpha = ||E_tilde-E||_diamond/2,
    beta = ||D_tilde-D||_diamond/2,

contractivity and a two-term telescoping identity give

    ||D_tilde C E_tilde - D C E||_diamond/2 <= alpha+beta.

The beta bound must hold on the full physical input space reached by C, or on a separately justified restricted interface including its reference correlations. Codespace-only calibration is insufficient when the actual repeated channel retains syndrome leakage. Similarly, a boundary map reconstructed only on physical single-qubit marginals need not satisfy this complete-channel premise.

For normalized Bell entanglement fidelity, the same trace-distance bound implies

    F_e(D_tilde C E_tilde) >= F_e(D C E)-alpha-beta.

No factor-two change is needed with this half-diamond convention. This is a sufficient bound, often pessimistic; direct evaluation or testing of the entire implemented input-qubit to output-qubit channel avoids summing separate boundary norm bounds.

A declared coherent gate exp(-i eta P/2) differs from the ideal gate by half-diamond |sin(eta/2)| for a nontrivial Pauli P, and a Z-dephasing interval with coherence exp(-lambda d) has half-diamond (1-exp(-lambda d))/2. These elementary bounds can be telescoped only over the operations actually scheduled, with every live-qubit exposure and preparation/readout cost charged. They are not inferred from infidelity alone.

## 3. Six-state full-channel test with external SPAM

Let L be the full implemented qubit channel, including physical encoding, storage and physical decoding, with Pauli transfer matrix entries M_jk. For uniform j in {X,Y,Z} and sign s in {+1,-1}, prepare rho_js=(I+s sigma_j)/2 and measure whether the same eigenvalue is returned. Averaging the six failure probabilities cancels translation, giving

    p_fail=(3-sum_j M_jj)/6=2(1-F_e(L))/3.

This identity requires only a qubit-to-qubit CPTP channel, not unitality, knowledge of its environment, or ideal internal code operations. If source and controls are stationary/frozen over validation, fresh binary outcomes support the ordinary binomial test. Otherwise an appropriate martingale/confidence formulation is needed, not an unqualified binomial claim.

If each external prepared state rho_tilde_js has trace distance at most alpha_js from rho_js, and each actual failure effect differs from its target effect by operator norm at most beta_js, contractivity and the effect norm give

    |p_fail_observed-p_fail| <= mean_js(alpha_js+beta_js) = delta_SPAM.

Thus a valid one-sided observed-failure upper bound p_U implies

    F_e(L) >= 1 - (3/2)(p_U+delta_SPAM).

This certifies the channel between the selected input/output reference planes, conditional on independently justified SPAM bounds. Treating noisy SPAM as part of the retained quantum channel is legitimate only when those operations are really included before/after service on arbitrary unknown inputs; an artificially matched preparation/measurement error can otherwise hide a bad channel. No diamond or retained-history guarantee follows from this entanglement-fidelity statement without additional conversion and resource conditions.

## 4. Scope needed in the next construction

- Expose a true quantum output qubit, not only a destructively measured logical observable.
- Include actual initial encoder and final syndrome-decoder circuits, or clearly label them trusted interface assumptions.
- Carry the physical state through all cycles and the output circuit without a free intermediate ideal projection.
- Record elapsed time, data/ancilla live time, actual gate count and inherited frame-acquisition bill separately.
- Any matched comparator needs the same task/reference planes; conventional coding with the same hardware can run the same construction.
- This architecture is still a mandatory-native-link task, not unrestricted passive storage with noiseless ancilla bypass.
