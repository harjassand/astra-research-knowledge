# Independent four-spin encoder/compiler review
2026-10-29. Accepted at the ideal-control scope in the source README, not as a precision-certified or fault-tolerant hardware implementation.

## Analytic core and exact check
The two supplied columns are orthonormal four-spin singlets in ket order q3 q2 q1 q0, with logical input q0 and the other three signal inputs zero. The total-spin annihilation and normalization identities were independently checked with exact symbolic radical arithmetic. The four-spin spin-zero sector has dimension two, so they span it.

The source Givens matrix maps (x,y) to (sqrt(|x|²+|y|²),0). Exact symbolic QR in the stated elimination order gives nine nontrivial rotations and the reduced matrix equal to the first two identity columns. Reversing and adjointing those rotations gives a full 16-dimensional unitary U with first two columns equal to the intended isometry E. The exact nine radical matrices are preserved in exact_QR_checks.json; they differ from the author's floating matrices by at most 3.6e-16. This makes the analytic target and completion explicit without relying solely on a floating near-zero threshold.

## Addressing and controlled gates
A Gray path flips each differing bit once, so its vertices are distinct. Swapping along all but the last edge moves the first endpoint to the penultimate vertex and leaves the second endpoint fixed. Conjugating the final adjacent two-level action by those swaps therefore realizes the desired ordered two-level gate. If the target bit of its first endpoint is one, conjugating its 2-by-2 matrix by X correctly converts the ordering to target-bit 0,1.

Conjugation by X on open controls turns the selected control pattern into all ones. With work qubit initially zero, Toffoli computes the AND of two controls. The CC-U conditioned on work and the remaining control acts exactly on the desired four-signal basis edge; its target is not either AND input, so uncomputation restores work exactly, including superpositions.

For V²=U, the controlled-V/CNOT/controlled-V†/CNOT/controlled-V sequence gives target exponent d-(d XOR c)+c=2cd. It is identity unless both controls are one, when it gives U. This also shows why an arbitrary square-root branch is harmless if it remains unitary and squares to U. The single-control Euler construction has target products ABC=I and AXBXC=exp(-i alpha)U; the control phase diag(1,exp(i alpha)) restores the determinant/global phase conditionally. Thus no unwanted relative control phase is omitted. The six-CNOT Toffoli is the exact standard H,T,T† construction, not a relative-phase Toffoli substituted into an uncontrolled context.

The exact Gray path counts sum to 25 addressed primitives. Each uses two six-CNOT Toffolis plus a CC-U containing three two-CNOT CU gates and two additional CNOTs: 20 CNOTs. Total 500 CNOTs. Counting the emitted, unoptimized one-qubit list gives 1032. These are executable sufficient costs, not minima; identities and neighbouring rotations have not been optimized away.

## Independent execution
The complete author program was replayed in a separate directory. Independently built tensor-product gate embeddings, rather than the author's row-update simulator, checked:
- 24 general, identity, diagonal and phase-degenerate CU and CC-U inputs;
- the full Toffoli matrix;
- all 64 oriented edges of the four-bit cube with independently sampled unitaries;
- eight nonadjacent Gray routes, including reversed endpoint order;
- the full 32-by-32 compiled matrix and all 16 clean-work columns.

The clean-work physical action differs from the claimed U by Frobenius norm below 5.3e-14 and work leakage below 8.1e-15. Full 16-column agreement, not just the encoded pair, is necessary to justify decoding arbitrary physical outputs. Exact invariance of this subspace also implies the inverse circuit preserves a clean work qubit on arbitrary physical inputs.

## Canonical reset decoder is load-bearing
Plain inverse followed by discarding the three signal ancillas is not the canonical leakage-reset channel. The independent check uses the leakage input U|3>: plain discard returns logical |1>, while canonical reset returns |0>, at trace distance one. The distinction is operational, not a negligible numerical correction.

For the correct implementation, apply U†, measure q1,q2,q3, retain q0 on outcome zero and reset it to |0> otherwise; discard the record. The Kraus family is E† and |0><2a+l|U† for a=1,...,7 and l=0,1. It sums to identity in K†K and realizes D(rho)=E†rho E+|0><0|Tr[(I-EE†)rho]. On a reference-entangled input, the second term is the corresponding reference partial-trace operator, not replacement of the reference. No postselection is required.

Importantly, the independent audit formed the canonical decoder Choi matrix from the ACTUAL compiled five-qubit inverse, not merely the stored ideal U. It agrees with the ideal canonical reset Choi matrix within 1.1e-13, and its trace-preservation residual is below 1.1e-13. These are floating Frobenius diagnostics, not rigorous diamond bounds. The symbolic ideal identities establish the exact mathematical construction.

## Scope, resources and prior art
One encoder plus inverse uses 1000 CNOTs and 2064 one-qubit gates, before preparation, measurement/reset, routing, storage and control errors. Peak footprint is five qubits: four signal qubits plus one restored work qubit excluded from the source port. Sequential reuse and fully parallel allocation have different work-buffer needs. A known tensor-product local frame adds four one-qubit gates per direction; arbitrary unknown/global frame acquisition is not supplied by this construction.

The stored matrices use floating Euler angles/eigendecompositions and numerical zero tests. The ideal circuit is analytically specified, but these particular stored floats are not exact gate-set realizations and lack interval-certified approximation bounds. A physical implementation must supply accurate single-qubit controls, connectivity, trusted measurements/reset and a composable error budget. Neither fault tolerance nor scalability is established by this small circuit.

This removes an assumed isometry in the structured four-spin family and benefits conventional logical tests as well as matching tests. The previous source-memory channel model is preserved only when its required canonical reset completion is actually used. This circuit alone proves no unknown-noise recovery guarantee; that uses the separate acquisition/guard/recovery arguments.

Barenco et al., Elementary gates for quantum computation, Phys. Rev. A 52,3457 (1995), arXiv:quant-ph/9503016, supplies established controlled-unitary and one-qubit/CNOT synthesis. The primary paper's Sections 5–6 were inspected during this review: https://arxiv.org/html/quant-ph/9503016v1 . QR/Givens, Gray addressing and controlled square roots are not claimed as new methods. No optimality or experimental advantage claim is supported.
