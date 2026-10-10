# Quantum-memory resource, width, and stopping-time family

This family concerns repeated noise on quantum registers that persist between rounds, with postselection and adaptive controls. It preserves the report’s earlier broadcasting and fixed-width results together with its later cumulative-resource and variable-stopping-time extensions in one source record.

## Fast route through the report

Open the [byte-preserved report](RESEARCH_REPORT.txt) at these sections:

| Question | Report lines |
|---|---:|
| Memory model, earlier fixed-deadline probability bound, and failed collective extension | [3126–3428](RESEARCH_REPORT.txt#L3126) |
| Broadcasting-based success bound and its complete-instrument tree argument | [3432–4110](RESEARCH_REPORT.txt#L3432) |
| Sharp-order width claim and fixed-width finite-lifetime result | [4112–4490](RESEARCH_REPORT.txt#L4112) |
| Tensor activation, distillability boundary, evidence and priority limits | [4490–4990](RESEARCH_REPORT.txt#L4490) |
| Cumulative variable-width resource law, proof mechanism, support extensions, and counterexamples | [5001–6773](RESEARCH_REPORT.txt#L5001) |
| Variable stopping-time inequality and exact flagged-erasure region | [6775–7130](RESEARCH_REPORT.txt#L6775) |
| Remaining gaps and final reported verifier scope | [7130–7326](RESEARCH_REPORT.txt#L7130) |

The report states that each persistent quantum register passes through every counted noise round; it allows ideal joint controls, measurements, resets, fresh unentangled ancillas, classical randomness, and feed-forward. It excludes a noiseless quantum bypass, access to environmental labels, operations on the reference, and uncounted entanglement. Success probability includes the encoder and selected events. Its general fidelity statements are conditional Bell-state tests and do not automatically imply worst-case guarantees for input-dependent heralding.

## Results as reported

The report’s memory section begins at line 3126. It combines an earlier fixed-deadline, width-independent success bound with a broadcasting argument. For a fixed CPTP channel with positive-definite Choi matrix, the report states a width classification: `M_Φ(N, ε) = ∞` when `J(Φ)/d` is undistillable, and `M_Φ(N, ε) = Θ_Φ(log(N/ε))` when it is distillable; the constants depend on the fixed channel, and this is not a procedure for deciding high-dimensional distillability. A separate fixed-width argument claims a finite exact lifetime for every adaptive accepted branch under that full-rank noise premise. The report then gives a cumulative accuracy/resource law for variable width and extends the analysis to support-limited noise, including a dual-rail amplitude-damping example that blocks extending the logarithmic-width claim to every rank-deficient non-EB channel.

The later stopping-time theorem uses `q` for reference dimension, `k` for a broadcasting multiplicity, and `p_n,F_n` for success probability and conditional Bell fidelity at completion time `n`. The report claims

\[
\sum_n k^n p_n(qF_n-1)_+\le q-1.
\]

For qubits, if every nonempty success-time bin has `F_n >= 1 - ε`, it derives `E[k^τ 1_success] <= 1/(1 - 2ε)`. It sets `k = 4` for the depolarizing model. For flagged erasure, it claims the full finite-support perfect-fidelity region is `p_n >= 0` and `sum_n k^n p_n <= 1`. These formulas and their hypotheses should be read in the linked source section; this guide does not reconstruct their proofs.

## Evidence and limits

The report says its candidate proofs are complete and its exact integer/rational verifier passed twice with byte-identical output, including checks of serial sandwiches, width profiles, finite-prefix constructions, stopping distributions, and rank-deficient examples. Those are report-reported checks: this intake received only the pasted report text, not the separately referenced verifier, execution receipts, or reproducible package. No checks were rerun and no theorem was independently reconstructed here.

The report leaves the optimal depolarizing reliability exponent, optimal finite-width horizon, and general high-dimensional distillability criterion unresolved. It explicitly does not establish the requested historic-scale breakthrough. Its earlier CP-cone growth-dichotomy material at report lines 31–3110 is preserved in the same raw source file but is a separate mathematical family; no transfer from that theorem is assumed for these memory results.

The repository’s mixed-family approximate-broadcasting package at [`updates/BW`](../../../BW/README.md) is separate evidence with different assumptions and should not be merged into this family’s theorem statements by topic similarity alone.

## Provenance

- [`RESEARCH_REPORT.txt`](RESEARCH_REPORT.txt) is the supplied pasted report, copied byte-for-byte; its SHA-256 and intake limits are in [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json).
- The report pins its initial CP-cone investigation to repository revision `0cc31b6146fed2d0d2cbc20348ab584145ea1b80` at line 39. That pin is not asserted to cover every later memory section.
- The repository revision used for this intake is recorded separately in the manifest and checkpoint.
- This guide is an intake-authored navigation and status summary, not mathematical evidence.
