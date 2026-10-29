# Product-block matching and conventional six-state baseline — 2026-10-29

## Consequence and boundary

For a *given* product code Q=P4^⊗h, cheap independent block tests retain dimension-independent fidelity constants even for a correlated/nonunital global channel. No full logical Clifford, global two-design or global physical routing is required. This is a stronger conventional comparison than assuming all full-logical tests require global entangled preparations. It does not supply a learner that discovers a good product-Q code from unweighted global star loss; that acquisition/representation bridge remains open. The earlier full-singlet matching theorem is unchanged. No historical novelty is asserted for tensor-frame arguments or product-state channel certification.

**Test outcome convention:** a global test passes only if ALL h block-survival tests pass. Thus q is the probability that at least one block fails, NOT the mean fraction of failed local tests. The dimension-independent constants do not apply to averaged local failure fraction; a one-factor Pauli can force an h factor for that alternative statistic. Every program here uses the joint all-pass event.

## Exact tensor-frame proof

Let d=2^h, and M=Eψ | |ψ><ψ| >> << |ψ><ψ| | be the Hilbert–Schmidt survival-test frame. The normalized identity vector is i=I/√d. For one four-spin singlet block (logical dimension2), the three matching states have frame eigenvalues (1/2,1/4,1/4,0), with identity eigenvalue1/2. The six Pauli eigenstates have eigenvalues (1/2,1/6,1/6,1/6). Independent product ensembles have tensor frames, up to the harmless vectorization index permutation. Their identity eigenvalue is1/d and their greatest nonidentity eigenvalue is respectively r/d with r=1/2 or1/3: any nonidentity tensor factor incurs at least that ratio, and more factors cannot increase it.

For arbitrary Kraus operators Kα:Q→H, compress Aα=V†Kα to Q. Write Aα=aα I+Aα,0 with Tr Aα,0=0. The average *raw* survival is

p_pass = Σα <<Aα|M|Aα>> ≤ Σα |Tr Aα|²/d² + (r/d) Σα ||Aα,0||²
       ≤ F_raw + r(1−F_raw).

The last inequality uses ΣAα†Aα≤I; no unitality, locality or product-channel assumption is made. Hence 1−F_raw≤q/(1−r), yielding C2 matching and C3/2 six-state. A Pauli acting on just one logical factor in the tested plane saturates matching C2; any one-factor nonidentity Pauli saturates six-state C3/2. Thus the constants cannot be improved uniformly for these ensembles.

The same inequality holds as an operator inequality on an arbitrary memory M: evaluate each memory input density matrix, apply the scalar argument to the resulting channel, and use positivity for all such densities. This produces H_bad≤C F_test, with the correct definition of H_bad for the declared completion below. Entanglement/correlation with payload is handled by the CP split, not by pretending the memory is classical.

## Exact service closure: two consistent interfaces

### A. Raw physical-survival tests and local physical permutations

The S4 representation on P4 is irreducible and occurs once in the physical four-spin space. The product representation of S4^h on Q is therefore irreducible and occurs once in (C²)^⊗4h. For each joint Kraus operator restricted to Q⊗M, let Bα=d⁻¹Tr_Q[(V†⊗I)Kα] and Rα=Kα−V⊗Bα. Uniform independent physical block permutations before the source and their inverses after it average Rα to zero by the unique-intertwiner property. The resulting joint channel splits exactly into identity_Q⊗B_good plus a CP residual. Its bad effect is I_Q⊗H_bad, H_bad=I−ΣBα†Bα. This establishes payload-independent bad probability despite arbitrary joint memory. Raw matching C2 and raw six-state C3/2 bound this H_bad. Permutation keys must be private during use and retired; claimed averaged channel does not retain the key.

### B. Completed decoder tests and cheap logical product Pauli twirl

Let T=D N E be the *complete* logical CPTP channel, including canonical leakage reset. Apply independent logical Paulis before encoding and inverse logical Paulis after decoding. Product Paulis twirl every nonidentity operator to zero and are irreducible on Q. For each completed Kraus Lα, Bα=d⁻¹Tr_Q Lα; the same scalar/residual proof gives an exact CP split with completed H_bad=I−ΣBα†Bα. Product six-state tests implemented through the same E,N,D satisfy C3/2 for this completed H_bad. Only single-logical-qubit Pauli controls and preparation/readout are needed, not a global Clifford. This is the direct extension of the existing conventional comparator.

Raw matching tests can also be paired with the completed logical product-Pauli service twirl: canonical reset retains the raw compressed Kraus branch and adds extra reset Kraus branches. Their scalar-good contributions are positive semidefinite on memory, so H_bad,completed≤H_bad,raw≤2 F_matching. Consequently the strongest fair product-code comparison can use the same cheap logical Pauli service controls for matching and six-state. Physical S4 permutations are an optional valid closure, not a necessary overhead for this completed-decoder comparison.

**Do not mix these interfaces.** A completed decoder can turn leakage into a test pass. For a channel taking the entire code to orthogonal leakage and then canonically resetting to |0>, raw physical-orbit H_bad=1, while a completed six-state single-qubit test has q=1/2. Thus C3/2 q cannot bound raw H_bad. The completed logical channel instead has entanglement fidelity1/4 and H_bad3/4, exactly consistent. Raw six-state tests require leakage to count as failure; this can be done with the inverse encoder's decoded-ancilla code-membership measurement before reset.

## Explicit inner-control budget

The independently checked Bell-label four-spin encoder uses8 CNOT+14 single-qubit gates, no work ancilla, four physical qubits per block. Its inverse has the same count, followed by three ancilla readouts and conditional logical reset for the complete decoder. Therefore a completed logical product-six-state test on h blocks costs16h CNOT+28h encoder/decoder singles, plus h logical preparations/readouts, frame controls and resets. The frozen learned fixture uses logical gauge E=Vhat E_Bell R with R=−X (numerical residual below3e−15); retaining that exact label convention adds one logical X per endpoint direction, as well as four physical local-frame gates per direction. A different known singlet basis is handled by one logical U(2), not a free arbitrary physical unitary. Ordering is load-bearing: encode applies R before E_Bell then Vhat. Decode applies Vhat†, the Bell inverse, then R† to the logical output BEFORE the final conditional leakage reset to logical |0>. Applying R† after an already-completed Bell reset would instead reset leakage to R†|0> (|1> for R=−X), changing the frozen CP maps. Ancilla measurement may precede the logical rotation, but the final reset must follow it on nonzero branches. Product Pauli service keys add no CNOT in the assumed endpoint single-qubit gate model, only local controls. Arbitrary endpoint connectivity and trusted/calibrated gates are assumptions, not hardware performance claims.

A matching raw test prepares2h singlets and measures them: with suitable within-block pair connectivity,2h CNOT for preparation and2h for inverse Bell measurement, totaling4h CNOT and4h Hadamards, plus Pauli signs/readouts/frame controls. No logical encoder is required for that test. Random pairing routing is not free on restricted hardware.

If physical S4^h service twirling is chosen, each block needs at most3 arbitrary-pair SWAPs in each direction, hence at most18h additional CNOT using3-CNOT SWAP decomposition, and independent private keys. All movement stays inside each four-spin block. This is an upper bound, not an optimized implementation. A global full-dimension two-design can yield C=d/(d+1) inverse = (d+1)/d, but its potentially larger controls must be counted; no need to invoke it for constant C3/2.

Neither scalar C nor these raw gate counts by themselves establish yield superiority. Test backaction, source calls, calibration, storage, discarded operations, outer transform cost and control errors remain relevant. Acquisition of a good product code is not obtained by this comparison.

## Executed evidence

`check_tensor_baseline.py`: explicit tensor frames h1,2,3; random correlated joint-memory isometry with true leakage for h1,2; actual24 and576 physical permutation averages; CP Choi split, bad-effect factorization and hazard effects. Leakage is represented by an actual orthogonal fully symmetric physical state, invariant under every local permutation; this compressed output representation is a valid invariant physical subspace, not erased leakage. Completed-decoder product-Pauli variants are checked separately. These fixtures need not model weak noise and make no learned-yield claim.

`check_learned_fixture.py`: frozen learned E, all15 canonical decoder Kraus, Ugood/Uburst and carried bath from the independently reviewed v9 fixture. h2 applies the same joint source successively to two blocks sharing the bath without reset, giving225 completed Kraus operators. Product-six-state hazard inequality passes: Ugood h2 q≈0.0006320044 and bad mass≈0.0009479314; Uburst h2 q≈0.75001175 and bad mass≈0.93750882. No re-learning or controller optimization is inferred.

Run both scripts with Python/NumPy. Results are floating consistency checks, not rigorous numerical intervals, laboratory measurements or a claim of novelty. `received_fixture.npz` is an unchanged dependency copy from `producer-workspace/reviewed_fixture_arrays.npz`. The8-CNOT cost is governed by `producer-workspace/four_spin_bell_encoder_20261029` and its independent review. Governing general service-twirl argument is the previously reviewed full-singlet orbit proof specialized to the product-group representation; this package adds the tensor-test derivation and scoped explicit checks.
