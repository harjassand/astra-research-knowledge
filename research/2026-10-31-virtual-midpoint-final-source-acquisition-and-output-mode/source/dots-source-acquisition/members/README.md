# Executable acquisition checkpoint
31 October 2026

Open clifford_source_acquisition_20261031/README.md for inputs, commands, examples, proofs and exact limitations. The two acquisition programs use only the Python standard library; dense diagnostic tests additionally use NumPy.

What now runs: a known-program certificate finder and verifier, reference/c-state preparation specifications, and exact sparse-Pauli mean/centering acquisition. The fixed state and return horizon are derived from the input gate program rather than supplied. Rejections distinguish persistent quantum information from a mixed reset.

What does not run here: the full downstream quantum simulation circuit. That remains the separate mathematical construction in the previously delivered pure-return checkpoint. This code is not learning a physical source from samples, a new general learning theory, a practical-advantage demonstration or external peer review.

The repaired code passed both supplied and independent checks, including dense small cases, global phases, symbolic 64-qubit source programs, signed Pauli means and malformed inputs. The original verifier failure report is retained as history; the final source-bound review records its correction. Symbolic 64-qubit certificates are not a claim of full non-Clifford 64-qubit simulation.

A nontrivial source-averaged Hamiltonian is preserved and its real action must be paid. The prototype does not silently make an uncentered physical model centered. Scalar system identities are the explicitly noted commutator-zero exception.

MANIFEST.json records exact file hashes. Code, proofs, examples and tests are unchanged from their reviewed local versions, except for the standalone reading guides. The separate pending affine-realization investigation is not included or promoted by this checkpoint. ZIP CRC and every member hash were verified before saving. Earlier research archives remain separate capital.
