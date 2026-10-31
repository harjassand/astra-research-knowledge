# Executable source-certificate acquisition
31 October 2026

This research prototype removes several supplied promises from the earlier simulation construction, within a restricted class of KNOWN source programs. It reads a Clifford Stinespring gate list, finds or rejects a pure-return certificate, and emits actual reference-state preparation circuits. A second module acquires exact sparse-Pauli means and centering data for later couplings.

It uses established stabilizer/GF(2) machinery. It is not learning an unknown physical source, a new general learning theory, a complete quantum simulator, or a demonstrated advantage over an equally informed compiler that retains the same tableau.

## What is executed
- acquire_clifford_source.py: standard-library-only finder and certificate verifier. It never builds a density matrix or enumerates all source states.
- acquire_pauli_coupling.py: standard-library-only exact rational, signed-tableau mean acquisition. It emits classical LCU specifications, not synthesized quantum circuits.
- Four test scripts and their JSON results: supplied and independent checks. Dense tests require NumPy; the acquisition programs do not.
- Mathematical specifications and separate independent internal review records. These are not external peer review or a formally verified proof-assistant implementation.

## Run the examples
From this directory, with Python 3.10 or later:

    python acquire_clifford_source.py examples/history_3.json --output certificate.json

The three-bit history program is admitted with horizon 3. Each acquisition call runs the exact verifier before writing. The callable verify(program, certificate) can also check a saved certificate against its source program.

For exact mean acquisition:

    python acquire_pauli_coupling.py examples/reset_zero.json examples/reset_zero.certificate.json examples/mean_preservation.coupling.json --output acquired_coupling.json

That example deliberately contains a nontrivial system mean. It is retained in the output, not silently deleted. The source certificate and its signed tableau can be reused for future sparse term lists. The CLI rechecks certificate integrity on each invocation; within a term list, signed membership is preprocessed once and reused.

To rerun validation:

    python test_acquisition.py
    python test_independent_adversarial.py
    python test_pauli_coupling.py
    python test_pauli_independent_adversarial.py

The final validation run used Python 3.12.14 and NumPy 2.3.5. No package installation is needed for the actual finder or mean module.

## Source input and admitted class
A program is JSON with n source qubits, env fresh zero-initialized environment qubits, and gates. Keep the first n output wires and discard the remaining outputs. Qubit indices start at zero. Allowed gates are H, S, SDG, X, Z, CX and SWAP. Other pure stabilizer ancillary preparations or output-wire conventions must be compiled into this explicit interface, with their gates paid.

For example:

    {"n": 1, "env": 1, "gates": [["H", 1], ["SWAP", 0, 1]]}

This resets the source to |+>. Arbitrary adaptive mixtures of Clifford operations, non-Clifford source gates and postselection are not admitted just because they sound like stabilizer operations.

The raw input does NOT provide the fixed state, return horizon or coefficient-state oracle. The output includes:
- a Pauli-image filtration with at most 2n strict dimension drops;
- the fixed state's signed stabilizers and a preparation circuit, when pure;
- the verified return horizon;
- a phase-safe coefficient-state preparation using the ACTUAL source circuit and clean source work;
- the source-program digest tying that certificate to its input.

## Three outcomes
accepted_pure_return: a source power is exactly a reset to the acquired pure state, including on reference-entangled inputs. The reference, horizon and circuits can enter the earlier theoretical compiler.

mixed_reset: the source forgets its input, but its constant output is mixed. Forgetting alone does not satisfy the pure-return interface.

persistent_pauli: a nonzero Pauli-image subspace persists. This rejects the requested global pure-return certificate for this quantum source. It does NOT prove instability, general simulation hardness, or that no alternative quantum realization of the same CLASSICAL process could work.

The example classical_reset_but_quantum_memory.json demonstrates that classical label mixing can coexist with persistent quantum coherence. The example dephase_z_then_h.json forgets in two steps but resets to I/2, so purity must be checked.

## Coupling input and preserved physical mean
A coupling JSON supplies system_qubits and a list of real rational Pauli terms. Each term has coefficient, system_x, system_z, source_x and source_z. Masks encode Hermitian Paulis with the canonical Y phase; signed stabilizer multiplication supplies exact expectations 0, +1 or -1.

Coefficients are explicit integers or rational strings p/q. Floating-point and executable-expression strings are rejected. Equal terms are combined exactly. The module verifies symbolically that the centered list has zero source mean.

The physical identity is

    Hsys + sqrt(lambda) K
      = [Hsys + sqrt(lambda) Hbar] + sqrt(lambda) K_centered.

Nontrivial mean terms remain physical and their actual simulation cost is paid. A scalar system-identity mean has zero commutator and may be removed under that explicit global-phase convention. The output flag physical_mean_commutator_is_zero refers to this distinction, not to the raw scalar mean being numerically zero.

The reported LCU bounds are accessible upper bounds, not exact operator norms. Empty centered lists represent a zero block; they do not erase source evolution under arbitrary initial source states or joint interventions. The earlier compiler's positive-normalization padding and scope rules remain binding.

This does not compute means of arbitrary succinct nonlinear Boolean operators. Expanding one into exponentially many Pauli terms is not polynomial acquisition.

## Validation and the repaired verifier defect
The source finder was checked against small dense matrices, including all Pauli phases, independent random circuits, and exact relative coefficient-state phases. Larger hidden-coordinate history circuits up to 64 source qubits were processed SYMBOLICALLY. This is not a 64-qubit non-Clifford simulation benchmark.

Independent review found a real defect in the earlier verifier: a list containing only a zero vector could be mistaken for a nonzero persistent subspace. The repaired verifier requires canonical basis lists and checks a nonzero basis. Parser/malformed-input handling was also tightened. The original failure report is retained alongside final regression results; only the repaired source is bound by the final review.

The sparse-Pauli module has separate signed expectation, dense centering, large rational, scalar-mean, cancellation and malformed-input tests. These tests and internal reviews support the prototype, but do not establish a production-hardened service or a complete downstream circuit generator.

## Reading the proofs and scope
INDEPENDENT_ACQUISITION_PROOF.md gives the admission/necessity argument and ordinary prior methods. EXECUTABLE_ACQUISITION_INDEPENDENT_REVIEW.md binds the repaired executable source. ACQUISITION_TO_PAULI_CONSUMER.md and PAULI_CONSUMER_INDEPENDENT_REVIEW.md give the theoretical consumer substitution; PAULI_EXECUTABLE_INDEPENDENT_REVIEW.md separately checks the executable centering module.

The earlier pure-return compiler still pays real source, reflection, coupling, Hamiltonian, control and measurement costs. Its source-rate/precision result is mathematical, not implemented here. Acquisition from observations, device calibration, arbitrary unknown models, novelty and practical superiority remain unestablished.
