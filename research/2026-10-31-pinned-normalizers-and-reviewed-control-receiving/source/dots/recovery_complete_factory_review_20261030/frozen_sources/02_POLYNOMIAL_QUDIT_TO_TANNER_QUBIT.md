# Polynomial-code realization and an actual qudit-to-qubit terminal port
30 October2026. Addendum to reviewed TOP_DOWN_QUANTUM_OUTPUT_DECODER.md. Avoids making the optional degenerate Steane realization load-bearing.

## 1. Actual exact decoder core
Use the fixed prime-p polynomial computation code already admitted by the scheduled-FT receipt. Its actual G2 list in ABO §5.1 contains field shifts, SUM, SWAP, multiplication by nonzero constants, phase w^(ca), Fourier transforms and generalized Toffoli (a,b,c)->(a,b,c+ab). The corresponding fixed-size FT gadgets and arbitrary-input correction contract remain received from the frozen review.

The quantum inverse encoder need not be ABO's classical decoder. For a degree-d polynomial code on distinct nonzero evaluation points alpha_i, the desired unitary encoding is

 |a>|0...0> -> p^(-d/2) sum_(b1..bd) |a+sum_j b_j alpha_i^j>_(i=1..m).

Prepare d coefficient ancillas in uniform states by Fourier. The Vandermonde evaluation columns for coefficients (a,b1,..,bd) are linearly independent. Complete them to an invertible m-by-m matrix over Fp and implement that matrix using Gaussian elimination, SUM, nonzero multiplication and SWAP. This is an EXACT finite G2 unitary E0. Its inverse uses inverse linear operations and inverse Fourier, also in G2.

A full coherent Pauli-syndrome recovery is likewise an exact finite G2 circuit. Linear syndrome extraction uses Fourier/SUM arithmetic. Each finite syndrome-to-representative lookup can be reversibly evaluated with addition and multiplication: equality indicators over Fp are products of 1-(s_i-t_i)^(p-1), and every function on the fixed finite syndrome space has a corresponding interpolation polynomial. Compute the representative in scratch, apply its controlled Pauli, and retain/uncompute work as appropriate. Controlled phases w^(za) are obtained by computing za into a clean scratch pit, applying a linear phase and uncomputing. All clean scratch targets are the actual finite-reset resources already charged by the cavity theorem.

Thus the entire constant shrinking-stage target D0 is EXACT in the fixed supplied gate set. There is no fixed logical approximation delta repeated at each shrink. Such an unbudgeted delta would otherwise accumulate with the number of levels and invalidate the uniform O(x0) floor. The top-down proof carries over with qupits replacing qubits and the same finite constants appropriately enlarged.

## 2. Preparing the desired Tanner target inside qudit logical symbols
Represent each desired target qubit by the subspace span{|0>,|1>} of one logical qudit. Extend each gate of the known polynomial-size qubit stabilizer encoder to a unitary on its one/two logical qudits. Compile this fixed target circuit into G2 to total diamond error epsilon_synth, using the supplied universal approximation theorem. This compilation is counted in L, and its approximation error is paid once in the global computation/source budget—not once per decoding level.

For epsilon_synth=exp(-cN) and L0=poly(N) target gates, polylogarithmic approximation overhead per gate is polynomial in N. The resulting L is still polynomial in N. Ideal compiled dynamics may slightly leave the embedded qubit subspace; this is part of the global synthesis error, not a clean-output assumption.

## 3. Literal two-site transfer to a Tanner DATA qubit
At the final physical output qudit Q, introduce the actual Tanner DATA qubit b and reset it to |0> using the received finite-reset primitive. Apply the fixed two-site unitary W that exchanges

 |1>_Q|0>_b <-> |0>_Q|1>_b

and fixes all other computational basis states (including |0,0>). For every unknown embedded qubit state,

 W[(alpha|0>+beta|1>)_Q |0>_b]
      = |0>_Q (alpha|0>+beta|1>)_b.

This preserves entanglement with arbitrary references and leaves no logical label in Q. Outside-subspace amplitudes are not promised a faithful qubit image; their effects are charged to bad output/synthesis terms. W is a constant-dimensional, bounded-body physical operation whose actual implementation and target-reset discrepancy are included in the FINAL constant decoder stage. If the declared hardware lacks this mixed-dimension gate or an equivalent finite synthesis, it is an explicit extra hardware interface, not a free decoder.

All outputs perform this transfer in parallel. The good-path actual output is now a literal physical qubit in the Tanner DATA register. The joint O(x0) decoder bad law and outer-code cardinality sieve remain as in the main note, with the final-stage constant B enlarged. Global synthesis error requires the common syndrome interface, not contraction of an arbitrary signed-history replacement. Let b_c bound the bad computation map. In the fixed coherent common-decoder isometry D, the good computation output has the form |psi_synth><psi_synth| tensor K, with K supported on the common hierarchical-sparse syndrome subspace S and ||K||_1<=1+b_c. The latter bound follows by comparing with the actual decoded positive trace-one state and the bad map of norm<=b_c. The all-logical common sparse-error identity guarantees that logical-space tensor S lies in the image of D. Therefore a fixed CP trace-preserving inverse extension of D can reembed BOTH logical targets with the SAME K.

Replace only |psi_synth><psi_synth| by the exact target density |psi><psi| in this chart. Their physical comparison changes by at most(1+b_c) epsilon_synth, although K and the resulting comparator may be signed. Propagate through the SAME actual output-decoder CPTP channel. Its decoder bad-cardinality map costs at most(1+b_c)b_out on this target-plus-admissible-syndrome comparator, while its good part is in the desired target Pauli span. Hence the positive actual output's bad-span population is bounded by

 b_c+(1+b_c)(b_out+epsilon_synth).

A final gentle projection supplies the corresponding warm-support trace-distance bound. This argument needs the full common sparse syndrome image, not just a reduced logical-channel estimate. The analysis chart/inverse is not a physical output decoder, and synthesis error is not assumed to be a sparse physical Pauli pattern.

## Costs and unchanged boundary
Temporary concatenated space is N polylog(L/epsilon_comp), hence polynomial N when epsilon_comp and epsilon_synth are exponentially small in N. The exact output decoder has a fixed small physical noise floor. Native warm clock/ancilla reception remains a separate actual apparatus theorem. Nothing here supplies autonomous scheduling, ideal detectors, arbitrary-accuracy physical single-qubit output, or FT novelty.

Primary gate-list and polynomial-code source already checked: https://arxiv.org/html/quant-ph/9906129 , §5.1/Theorem5. The explicit coherent inverse encoder and two-site transfer above are the receiving construction, not a reuse of that paper's classical de-encoding as a quantum port.
