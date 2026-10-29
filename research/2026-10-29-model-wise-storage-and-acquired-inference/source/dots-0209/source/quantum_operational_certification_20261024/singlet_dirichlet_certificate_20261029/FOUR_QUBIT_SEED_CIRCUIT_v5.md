# Explicit constant-size circuit recipe for the weighted plus-branch seed
2026-10-29. Physical preparation supplement to v4; not a change to its theorem.

Let A=(i,j), B=(a,b), initially all zero. Prepare on A the three-level state (|00>+|01>+|10>)/sqrt(3): apply Ry(2 arccos sqrt(2/3)) to its first qubit, then a Hadamard to the second controlled on the first being0. Copy both computational bits from A to B with two CNOTs. The state is then (|00>|00>+|01>|01>+|10>|10>)/sqrt(3).

Apply a fixed two-qubit unitary U_A to A whose columns in computational order are
[ |00>, −(|01>+|10>)/sqrt(2), |11>, (|01>−|10>)/sqrt(2) ].
Apply U_B=(X tensor X) U_A (I tensor Z) to B. On the three occupied basis states, U_B maps00→|11>,01→|t0>,10→|00>. The resulting four-qubit state is exactly
(|t+>|t−>−|t0>|t0>+|t−>|t+>)/sqrt(3).

U_A is an explicitly specified constant4×4 unitary; it can be implemented using a CNOT that swaps10↔11 followed by an odd-parity-plane rotation taking01→−t0 and10→singlet. This requires a calibrated two-qubit rotation or its ordinary constant-size single-/two-qubit decomposition. Thus the source preparation is not an n-dependent arbitrary-state oracle. The controlled-H, two copying CNOTs, fixed U_A/U_B and one non-Clifford single-qubit angle have fixed size independent of n. Approximation precision and actual pulse errors enter the test-circuit bias budget as in v1/v3/v4.

This construction is deterministic. No success-probability division or postselected source call is hidden in the plus branch.
