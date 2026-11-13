# Exact contextual coherence elimination via binary linear constraints

This is a direct generalization of the proved bridge-output identity, not a new universal simulation theorem. Priority/novelty has not been assessed.

Consider basis-state input, arbitrary diagonal unitaries, fixed classical-reversible affine gates (X,CNOT,SWAP), computational-basis measurements/resets, final Z output, and non-Clifford Pauli rotations U_j=a_j I+b_j P_j. Fix any independent sampled noise categories and reset preparation bits. P_j is a Pauli product, so each chosen branch flips a fixed binary subset and contributes a basis-dependent phase.

Introduce a binary ket path variable z_j choosing the P_j branch. Propagate each wire's computational-basis value as an affine function of z, using ordinary binary linear algebra through X,CNOT,SWAP. At every reset/measurement append its measured old-bit expression as a row; after a reset replace the wire by its fixed fresh bit. Append final Z outputs. The resulting complete-record constraint has form H z=h(record,input,preparations).

For ket/bra histories contributing to the SAME complete record, H(z xor z')=0. If column j is a COLOOP of the binary matroid of H, meaning no kernel vector has its j-th coordinate nonzero (equivalently removing column j lowers rank), then every contributing pair has z_j=z'_j. Thus U_j may be replaced, for the final classical record law, by

|a_j|² Id + |b_j|² Ad(P_j),

provided the rotation has |a_j|²+|b_j|²=1. This is a classical mixture of product-Pauli operations. Its branch phases remain in P_j; no non-Pauli entangling operation is introduced. All coloops can be removed simultaneously. An arbitrary diagonal reference and Pauli Z/Y phase factors do not affect the linear flip constraint.

For the actual pair-XX/reset model, H is the reset-segment graph incidence matrix, and its coloops are exactly graph bridges. Parallel edges are distinct columns. In the broader affine-gate setting, H is not necessarily a graph incidence matrix; find coloops by a kernel basis or rank-revealing GF(2) elimination, charging polynomial bit-matrix cost.

Scope restrictions:
- Final classical-output equality, not full-channel equality or arbitrary-basis measurement equality.
- Intermediate measurement records must be included before marginalizing them away.
- Arbitrary nonlinear reversible permutations do not preserve this affine construction.
- Outcome-adaptive gate choices require a separate branch-dependent argument and cannot be silently inserted into the fixed H theorem.
- Columns that are not coloops can still sometimes be removed for special angles/states, but this criterion makes no such claim.
- Retained columns can have extensive coupled interference; the theorem alone gives no polynomial full-output sampler.

This supplies a reusable exact preprocessing mechanism for certain non-Clifford circuits. It is conceptually related to established path-sum, binary-code, and Pauli-rotation simulation methods. Absence of a matching result in an initial search is not a novelty demonstration.
