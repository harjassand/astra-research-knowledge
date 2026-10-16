# Candidate simplification: stabilizer-refined correction instruments

2026-10-15. Derivation for separate review; not automatically part of a frozen memory packet.

Let the completed correction have Kraus operators Q_j Pi_j, with the Pi_j functions of commuting code-stabilizer checks and Q_j Pauli corrections. Let {R_s} be any finer family of orthogonal stabilizer-syndrome projectors with sum_s R_s=I and Pi_j=sum_{s:j(s)=j} R_s. Implement the refined correction with Kraus Q_{j(s)}R_s, recording or discarding s as specified.

This generally changes the channel on coherent superpositions within one coarse branch. It is not equal to the original completed correction on all inputs.

Nevertheless on every encoded Pauli orbit E V_code, each R_s either annihilates the orbit or is identity on it, because all measured code stabilizers have definite eigenvalues there. The only surviving refined branch applies exactly Q_{j(s)}E V_code, the same correction transition as the coarse instrument. A chronological history expanded in local Pauli factors remains an encoded Pauli orbit term by term. Refinement only removes terms in each refined record; it creates no new memory support or wrong transition.

Therefore a universal support/common-decoder proof that certifies EVERY admitted Pauli term under the original correction also certifies the refined instrument, provided the extra measurement gates/ancillas fit the reserved support, the entire exact implementation remains bath-independent, and its records satisfy the common-dilation/privacy assumptions. The global Fourier subset moment proof depends on deletion stability and unitary dilation, not equality to the unrefined channel, so a frame-independent refined ideal instrument is compatible with that analytic step. Physical outcome indices must still be summed for probability bounds.

The ideal physical primitive can then be ordinary commuting Pauli-check extraction, classical syndrome lookup, and conditional Pauli feedforward, rather than a special coarse inactive-sector measurement preserving every internal coherence. This is an application of standard syndrome measurement, not a new error-correction primitive. Controller/measurement/reset errors are not qualified by this argument. Full measurement support, timing and noise locations must be counted again.

A separate audit is required before extending a stated theorem. In particular one must check that the refinement really refines every Pi_j used by the update and that its local support is bounded in the code family.
