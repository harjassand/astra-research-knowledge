# Constructive thermal initialization and the physical loading gate

1 November2026. Internally reviewed mathematical constructions, reproducible checks, strong conventional comparisons and preserved failures.

## Strongest completed result
An explicit polynomial-time classical sampler for the actual recursive 3D code's COMMUTING Gibbs syndrome distribution, at sufficiently low fixed temperature and fixed construction parameters. Applying matched Pauli corrections to a SUPPLIED encoded logical input produces its thermal logical encoding, with sampling error charged reference-safely.

The key construction is an exact positive polymer representation of valid syndrome configurations using complete deterministic decoder histories. It retains the original couplings, redundant constraints and modified level-2 decoder. Established low-temperature polymer algorithms then supply the sampler. We adopt that stronger existing machinery rather than claim a new general sampling algorithm.

This removes an ideal initialization obstacle caused by non-LDPC metachecks. It is not yet noisy physical writing, generic interacting-bath preparation, or a practical device. Fixed construction constants remain enormous.

## Read first
- ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md and CLARIFICATIONS.md.
- recursive_initialization/actual_decoder_binding.md.
- independent_audit/ACTUAL_RECURSIVE_SAMPLER_BINDING_RECEIPT.md.
- POLYMER_SAMPLER_COMPARATOR_ADDENDUM.md for the stronger established sampler.
- COMPARATOR_GATE.md for equal-resource active fault-tolerant alternatives.

## Additional retained constructions
- Coherent syndrome/sign computation and three controlled decoded-Pauli gates implement logical SWAP without dephasing the interacting thermal gauge/bath state. This is an ideal circuit, not a noisy implementation theorem.
- A weighted second-moment condition admits certain nonstationary loaded states to long exact-H storage. Extensive local faults need not satisfy it; failure of that sufficient condition is not a memory no-go.
- The protection/access bound shows why a polynomial-time local writer must temporarily leave the protected equilibrium region or change the code/algebra. Endpoint restoration remains possible and is the central physical challenge.
- Independent positive construction and obstruction notes test local thermal-preserving repair, rather than assuming it.

## Reproducibility
Python3, NumPy and SciPy suffice; most combinatorial tests use only the standard library. Run scripts from their own directories. Portable helper modules are included.

1. recursive_initialization/actual_rx_recognizer_fixture.py: all4096 syndromes of an actual19-qubit Bell-square RX gadget. Local flags agree exactly with global syndrome-image membership;2071 component replays pass.
2. recursive_initialization/actual_main_seed_recognizer_test.py: actual60-qubit first RX of the source's five-qubit seed,6039 tested inputs and exhaustive local admissibility tables.
3. recursive_initialization/actual_rx_polymer_bijection_test.py: complete finite valid-syndrome/polymer-family bijection and partition equality with nonuniform original couplings.
4. independent_audit/test_abstract_trace_bijection.py:200 deterministic small circuits, complete accepting-input and compatible-family checks.
5. test_trace_polymer_cancellation.py: exact rational cancellation-gate control.
6. test_coherent_overwrite.py: ideal overwrite on a DIFFERENT standard five-qubit perfect code plus an interacting bath qubit. It checks the coherent interface, not the recursive family or physical noisy gates.

Finite tests corroborate but do not replace all-level proofs. The Bell-square fixture is not the full family's modified level-2 terminal. The original code/decoder are imported from Balasubramanian–Davydova–Lin2605.10943v1; conventional polymer sampling is credited to its governing sources. No paper body or source figure is redistributed.

## What is still missing
A local noisy writer and reader with a demonstrated endpoint return into a protected ensemble, under a physically supplied initialization/reset service. The storage-only bath need not cool anything. Generic weak spin-environment Gibbs preparation is not obtained by sampling H0. Active fault tolerance receives the same control and entropy-export resources in the comparison.

No experimental validation, peer review, practical threshold, priority claim or civilisation-level breakthrough is asserted.
