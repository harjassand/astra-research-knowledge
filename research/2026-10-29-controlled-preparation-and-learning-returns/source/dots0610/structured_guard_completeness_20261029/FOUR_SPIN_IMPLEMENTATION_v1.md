# Explicit constant-size inner encoder
2026-10-29. Exact finite isometry/completion, not a checked elementary-gate netlist.

In computational order |q0 q1 q2 q3>, define

 E|0>=(|0101>-|0110>-|1001>+|1010>)/2,
 E|1>=(2|0011>+2|1100>-|0101>-|0110>-|1001>-|1010>)/(2sqrt(3)).

The executable `check_construction.py` verifies EXACTLY with symbolic algebra that E†E=I2 and each of the three total spin generators annihilates E. Tensoring h such blocks therefore embeds h logical qubits into the full 4h-spin singlet sector. No assertion that this tiny subcode is permutation invariant is made; orbit randomization is essential in the governing theorem.

The same script explicitly completes E to a real16x16 unitary U by exact Gram-Schmidt on E's two columns followed by the16 computational basis vectors. `four_spin_unitary_exact.txt` stores that exact matrix. This convention implements E by applying U to |000>_ancillas tensor |logical>. Apply U†, measure the first three (ancilla) wires, retain the logical wire only on syndrome000, and otherwise reset that logical wire to |0>. This implements the CANONICAL total reset decoder D(rho)=E†rho E+Tr[(I-EE†)rho]|0><0|. Merely tracing ancillas would give a different total decoder and is not the stipulated interface. No outcome is postselected away.

A16-dimensional unitary has a finite two-level Givens/diagonal decomposition. Each two-level rotation can be mapped along a four-bit Gray path to a multiply controlled one-qubit operation, and decomposed into elementary controls using standard finite synthesis. Since the block size is fixed, this establishes a constant-size ideal local construction per logical qubit, hence O(h) block encoder/decoder work. This packet does NOT supply or claim a verified CNOT/one-qubit netlist. Approximate local compilation errors, storage and feedforward must be budgeted; no hardware noise threshold is claimed. The earlier three-qubit control compiler is not silently treated as a checked four-qubit compiler.

For the outer code, nested generalized Reed-Solomon spaces C2 subset C1 of dimensions2t and B-2t on all B distinct GF(B) points give a CSS code with B-4t logical field symbols and distance2t+1. This nesting, rather than a self-dual square-root-multiplier ansatz, avoids an invalid characteristic-two restriction. We use the existing received finite-field compiler as dependency, not a new unchecked gate-count advantage.
