# Sharing one learned compressed decoder across a joint payload batch

2026-10-29. Root extension, unreviewed. Does not turn a batch decoder into a reusable original-D classical decoder.

Store N training Choi outputs and M later encoded payload registers before one compression operation on ALL N+M D-level outputs. The M logical inputs may be arbitrarily entangled with each other and an external reference. The same reference-joint compression identity produces one common latent Haar U(d) acting on every training and payload factor, with independent junk sigma on each source call.

Conditional on U and the complete training measurement record, the N training data determine one classical learned Petz recovery R_t in the common small-d frame. The M payload outputs then pass through (R_t A_U)^tensorM, with their original arbitrary joint logical input. On the good training event the single-use half-diamond error is at most e0=k sqrt(3delta), so the joint batch error is at most M e0. The ONE shared tomography-failure event contributes beta once, not M beta. Joint compression/synthesis error contributes its actual complete-instrument budget gamma. Thus a direct global identity bound is M e0+beta+gamma.

No new training queries are required for each payload WITHIN this one jointly compressed batch. Training cost is N; service uses M calls; protected storage is at least(N+M)logD output qubits plus references/work. Independent compression of a later batch creates another latent frame, so the old classical matrix is not a decoder for future original-D payloads. No streaming/reusable-frame theorem is asserted.

## Error correction and the conditioning distinction
If known logical Pauli/Weyl randomization before the source and matching post-decoder correction is supplied, then conditional on the same U and training record, the M effective logical channels are independent Pauli/Weyl channels. This conditional product structure can support ordinary outer coding. The unconditional channels need not be independent: shared calibration randomness correlates their errors. One must bound a single bad-calibration event separately and prove a uniform conditional error bound before invoking independent-noise code estimates.

For example, a decoder that is correct with probability1-beta and applies Z to EVERY payload with probabilitybeta has individual errorbeta but two-error probabilitybeta, not beta². This invalidates replacing a shared random decoder by independent copies of its average channel. The current good-event certificate avoids that shortcut, but a quantitative outer-code/rate construction for this batch architecture is not supplied in this note.
