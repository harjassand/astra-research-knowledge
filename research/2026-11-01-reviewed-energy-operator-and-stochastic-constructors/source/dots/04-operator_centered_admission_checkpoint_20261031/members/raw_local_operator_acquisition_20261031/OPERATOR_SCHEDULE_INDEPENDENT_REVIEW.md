# Independent review: raw operator certificate to scheduled admission

31 October 2026. Reviewer: challenge_graph_profile_compiler.

**PASS for the separate known-model composition.** This receipt closes Section 8 of `RAW_OPERATOR_ACQUISITION_AND_RECEIVING.md`, SHA-256 `5fdd5bf94326e4715a4dc486a35bfe8bb939a456e44588c324ef491d0b9ba534`. It receives, and does not replace, the core receipt `RAW_OPERATOR_INDEPENDENT_REVIEW.md`, SHA-256 `cbfe146631e62e5b29b78bc6ff1033c80153be537b0e056e0881102c741282e0`.

## Exact sources and execution

I read the entire wrapper and its test suite and reran the non-writing `run()` entry point: all 20 supplied checks pass. I added 73 independently executed checks. The author's saved input/certificate/result JSON was not rewritten.

- `receive_operator_schedule.py`: `7a2ce2907cb894e0e9aeec2778cf7ffca684de914ea7e815c642f3ea4af4b71f`.
- `test_operator_schedule.py`: `71c67f22bd342a9718adfb3dd8b5cf639a7b827de16143462c0d2babd0e540e3`.
- Repaired raw checker: `35acdcdcc533f523cc78c558153f97fcb800711bbd4ff0f57b8a2ea50d60ee35`.
- Reused, hash-checked `local_energy_fault_admission_20261031/acquire_local_admission.py`: `a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8`.
- `check_schedule_independent.py`: `43338ad5cd633c9984cc7b9022ce90bde4caf779d9d80f2254d92838bccce262`.
- `schedule_independent_checks.json`: `1fecc2a0c13a6afd63b3589a4451ce5fd065029c35a1ec25fa2f734f3f513767`.
- Saved `qutrit_complete_schedule_input.json`: `2136995d6979d272776bed3dfcf820c35d9c45a663ad7db9ea413fe83209fab9`.
- Saved `qutrit_complete_schedule_certificate.json`: `6161e009a93842b2aeb2f4d066d9f36ad342a7508db8e91d57542f0e907c8c9a`.

## Mathematical and executable join

The wrapper first independently verifies the raw drift certificate against the externally supplied raw model. It then reconstructs the global allocation matrix and activation totals. The minimum of the negatives of every row and column sum is a valid physical kappa; the largest total activation is a valid a. These may be sharper than the originally requested margins, because the actual checked allocations, not their proposed objective value, are used.

Every supplied matrix-times-system-Pauli coupling is mapped to its acquired NONNEGATIVE matrix norm upper bound, keeping its source-cell index and full system Pauli support. Summing these scalar bounds is a valid bound on the actual grouped source/system operator, including noncommuting source matrices. Positive norm coefficients cannot accidentally cancel oppositely signed actual matrices; my independent test verifies this conservative behavior.

The constructed independent-loss scalar model is ONLY an input format for the frozen schedule checker and rational contour arithmetic. It is not a channel, a replacement physical generator, or a proof that a mixed-transparent qutrit source is a qubit. Section 5's general-projector product-weight proof depends on exactly kappa, a, c, g, tau and epsilon_ctl; that proof, rather than any asserted equality of physical dynamics, licenses the substitution. The scalar envelope has gamma=1, so its optimized contour cap is consistent with the general-charge cap. The zero-coupling control-only branch avoids division by zero.

The reused checker checks full explicit gate/idle coverage, actual Pauli support containment, source/location assignment and simultaneous nonoverlap, supported intended targets, and integrated control-error data. The wrapper enforces matching task identifiers and consumer contract hashes and binds the entire externally supplied model, raw certificate and schedule. It records actual source dimensions and does not expose the envelope as a physical source-qubit claim.

Its full-record verifier recomputes the deterministic acquisition result with strict recursive type equality. A truthful NOT_ADMITTED record can verify consistently but cannot pass `verify_admitted`; CLI verification requires actual admission. The 73 independent checks include all integer-output bool/float substitutions, conservative opposite-matrix norm grouping, a valid zero-coupling control-only case, and rejection of a full-rank coupling introduced under an old raw certificate. The supplied tests cover changed models, tasks and intended targets, missing idle coverage, schedule gaps, unsupported reset targets, forged raw drift, simultaneous source fanout, and a valid NOT_ADMITTED large-control-error record.

The complete qutrit fixture reproduces the claimed conservative amplitude `303/2916666431`, below `1/10^6`. This is a sufficient exact mathematical bound under its specified model and zero-control-residual evidence premise, not an observed error rate or experimental result. Large harmless internal Hamiltonians are removed by exact commutation in the raw drift computation, not waived by a norm oracle.

## Boundaries

The externally supplied physical operators and control evidence remain assumptions. Hash matching does not inspect or authenticate an evidence document or prove the consumer threshold contract. Full input inspection, exact raw verification, explicit schedule inspection and ordinary arithmetic are paid; there is no compressed unknown-device acquisition claim or gate backend.

This wrapper still requires the raw common-transparent-sector certificate. It does NOT implement the separate clamped-weight PP-zero source-creation theorem, and no such upgrade is inferred here. It is a sound composition of the reviewed raw drift and schedule receivers, not a new noise theorem, a new threshold, or evidence of practical superiority.
