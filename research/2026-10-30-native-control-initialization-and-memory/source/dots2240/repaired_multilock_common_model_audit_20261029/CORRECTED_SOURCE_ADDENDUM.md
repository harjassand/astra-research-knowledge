# Narrow corrected-source receipt — 2026-10-29 21:47 UTC

Compared the two revised sources against this audit's preserved pre-correction copies using full textual diffs, and independently recomputed their SHA-256 hashes:

- `no_epoch_healing_20261029/LOCAL_HEALING_CERTIFICATE.md`: `19003a818d742c4dddc0bb28836326665f338e385115efd1edfcd12453b08ce1`
- `no_epoch_healing_20261029/CONDITIONAL_QUANTUM_FLAG_EXTENSION.md`: `15ccfb3fca351b5c0f1e4ecefb730e08d689ee059d448816beaa84ae1876e636`

**Confirmed:** the revised premises now match the actual bundled-instrument proof accepted in SCOPED_REVIEW.md sections 2–3: each resolved gain preserves the good range; the summed complete-instrument loss commutes with the flag; selected clock-transition no-jump loss blocks remain absent. The quantum extension includes the correct bundled operator-order proof. Neither source asserts individual syndrome-loss commutation.

All displayed numerical definitions and inequalities for delta, p0, epsilon, monitor factors, T and c are unchanged. This is justified because the CP-Dyson conditional propagator and local B bound use the summed loss, while selected reset gains retain their complete, separately resolved instrument. The correction does not require changing the physical generator or any numerical estimate.

The added provenance accurately retains the original mismatch and does not relabel the earlier local-healing audit as a corrected-byte audit. No new claims beyond the existing scoped receipt have been accepted.

This addendum closes the pending source-correction item in CORRECTION_STATUS.md for EXACTLY the two hashes above. The original receipt, original SOURCE_SHA256.txt and historical pending-status note are preserved unchanged. Future revisions require their own check. All existing limitations—including no data threshold, no bare-output guarantee, and bad-weight rather than generic first-entry-time interpretation—remain in force.
