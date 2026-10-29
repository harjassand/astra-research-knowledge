# Independent review of explicit noisy code boundaries, version 2

28 October 2026. Accepted at the declared finite-dimensional channel-model scope, conditional on the separately reviewed bulk EC primitive and acquired-frame data. This is standard stabilizer encoding and syndrome-conditioned decoding with explicit noisy operations, not a new code or hardware claim. Version 1 remains a preserved failed source and is not used.

## Exact all-operator target

The reviewer reconstructed the listed Clifford circuit using independent computational-basis gate embedding and exact SymPy arithmetic. Its two canonical code columns map to the input-qubit/zero-syndrome columns, with the same global phase. More importantly, the sixteen terminal syndrome-projector rows followed by the declared Pauli correction are exactly a phase/permutation of the sixteen previous recovery Kraus operators. The permutation is saved in the checker. This proves equality to the old recovery-and-decode map on every physical 32-dimensional operator and hence every entangled reference input; it is not merely a codeword or single-error performance test.

The syndrome lookup is derived from the actual synthesized Clifford and is complete on all sixteen outcomes. There is no discarded failure record or postselection. A bare inverse Clifford without these physical measurements and conditional Paulis would not establish this equality. The new circuit implements the missing recovery operation rather than re-labelling its metric.

## Independent noisy representation and normalization

The reviewer separately implemented density matrices with computational-basis gate embedding, entrywise dephasing determined by Hamming distance on live qubits, immediate projective measurements and explicit outcome-conditioned physical corrections. The author instead uses real Pauli coordinates and postpones the measured-ancilla contraction. For four noise settings, including negative coherent error and background strength .3, random arbitrary non-Hermitian physical operator tests agree to less than 4e-16. Complex tests were split into real and imaginary Hermitian coordinate parts because the author routine is intentionally a real transfer-matrix implementation. Prepared-input encoder tests agree to less than 2e-16. These are floating diagnostics supplementing the inspected CPTP composition, not outward-rounded bounds.

Raw coordinates are Tr(P O), not normalized state coefficients. Reconstructing a five-qubit operator divides by 32. Logical PTM entries divide the output Pauli trace by 2. The terminal measurement's factor 1/32 is therefore correct: four binary projections supply 1/16 and the logical PTM convention supplies the further 1/2. The zero-noise round-trip check catches the preliminary version's incorrect normalization.

## Clock and liveness

Each Clifford direction has six H, eight CX and one X: 23 reference units. Sequential four-ancilla initialization costs 8. Four destructive syndrome measurements cost 16; common classical feedback costs 1 and the correction window costs 1 even for identity. Total boundary duration is exactly 72.

The unknown input is live throughout initialization; each ancilla becomes live at its own preparation. All five qubits receive background noise during encoding/decoding gates, including active supports. Measured syndrome qubits are retired while the output and remaining syndrome qubits continue to dephase. The output alone is live for final feedback and correction. Postponing already measured qubit contraction is valid here because no later gate couples to it. No raw measurement outcome is free: basis misalignment, duration and physical correction are included. Classical dispatch is trusted.

The model still separates effective native-channel phases from background controller time. It does not prove physically absent background during native phases. Inverse-frame gate synthesis remains in its earlier declared scope. External qubit test preparation/readout is not included in the 72 units and is explicitly still trusted/calibrated.

## Complete channel replay

The independent replay uses its own density-matrix initialization, boundary gates, measurement branches and native Kraus application, carrying the actual five-qubit state between cycles. Only the previously reviewed bulk EC transfer map is reused as a dependency. It reproduces all four saved endpoint PTMs, including both zero-storage tests and the two T=32 storage cases. Exact differences and endpoint fidelities are saved in `replay_full_channel_v1.json`.

This is a deterministic model evaluation. No new acquisition records, hardware measurements, six-state acceptance decision or confidence statement are asserted. The original selected frame is reused, and its acquisition cost remains inherited. The previous cadence holdout tested a different channel with trusted ideal boundaries; its acceptance cannot be transferred automatically to this new executed boundary channel.

## Consequences and limits

The construction now has a genuine single-qubit quantum input/output interface in the declared model, including a finite gate-level implementation of terminal recovery. An inaccessible reference can be retained throughout the CPTP map. The remaining trusted external tester can in principle test that full channel directly; imperfect preparation/readout needs independently justified error bounds.

Early unencoded input errors and final output errors are not fault-tolerantly suppressed merely by the bulk code. Same-time single-carrier comparisons must also account for these additional 72 units and their permitted ideal controls, not silently recycle old endpoints. The seven-versus-one quantum-resource difference remains. An equally informed conventional implementation can use exactly these standard circuits. No new-code advantage, general passive-memory lifetime, scalability threshold, physical device performance, arbitrary environmental-memory guarantee or historical novelty is received by this review.
