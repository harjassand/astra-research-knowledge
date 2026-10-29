# Actual stronger baseline: the small-instance result favors full logical testing
2026-10-29. Frozen program/data `compare_actual_two_design_v9.py/.json`; pending independent receiving of this comparison fixture. No new mathematical guarantee beyond the generic guard is asserted.

## Controlled comparison
Use EXACTLY the1m no-reset learner's inferred candidate and final bath state from v8. Use the SAME fixed good-source joint unitary U0. Compare actual CP instruments, not a scalar rescaling that ignores memory backaction.

The baseline TEST prepares one of six uniform logical Pauli eigenstates, executes the full physical inner encoder, source and TP logical decoder, and measures survival in the prepared state. Its memory failure effect is checked to equal(2/3) times the service nonidentity effect, including the nonunital joint source and leakage replacement. Thus C=1.5. Choose s=.4, cap500, t=6,b=0, keeping R=1,155 services,35 payload qubits and the SAME0.0078125 subnormalized accepted soundness bound.

The source's Z-burst alternative is NOT compared here: placing the burst at absolute calls500–511 would expose the slower protocol to a disturbance after the faster one normally finishes, which is not an equal disturbance test.

## Results
With exact compressed memory/count propagation:

| Actual test | Acceptance | Expected guard source calls | Cap |
|---|---:|---:|---:|
| Weighted local symmetry, conservative C=6 |0.7757656926|957.4809004|1400|
| Six-state/full logical operation, C=1.5 |0.9290072246|373.4893479|500|

The six-state case's accepted bad-count weight is1.7655e−12. In1000 actual CP-instrument trajectories920 accepted, and50 selected nonzero accepted ledgers were actually outer-decoded correctly. The finite-memory effect equality residual is below1.2e−16 for both supplied source unitaries.

This execution favors the conventional full-logical test in source calls AND acceptance. It provides NO evidence that the local-symmetry witness is a better small-n operating protocol. Use the stronger baseline unless measured/calibrated physical control costs supply a reason not to. The local witness remains a distinct useful theorem/interface: it avoids invoking the full compiler/decoder on test shots, but has a worse statistical coefficient. At n=4 all those gadgets are constant-size, and no total gate-duration/fidelity advantage is demonstrated.

There is also an important robustness distinction. If the actual inner encoder/decoder implementations are part of the SAME complete role-independent tested logical operation, the two-design test can include their noise in that operation; accuracy of their nominal matrices is not needed for guard SOUNDNESS. Trusted logical test preparation/readout and exact private pads outside that boundary, plus outer correction/buffers, remain requirements. The local-symmetry test bypasses the inner compiler/decoder and must independently budget their implementation error. This distinction must be preserved in any fair hardware comparison.

## Why candidate use need not wait for parameter certification
For illustration only, insert n=4, supplied g0=.35, learning failure delta=.05 and target uniform twirled error1/128 into the deliberately loose declared scalar/matrix-rounding confidence bound. It asks for306,027,119,748 acquisition calls. This is NOT a lower bound and not evidence that such a cost is necessary; sharper statistics and direct task tests can be much better.

The executed controller instead freezes a candidate after1m actual no-reset probes and guards the delivered finite operation. Its source-independent accepted soundness does not require correct frame identification, gap certification or the common-algebra promise. The observed good yield is a property of this supplied source fixture, not an unconditional theorem for unknown future environments.

These guarantees differ: parameter certification plus an exact full joint algebra promise supports uniform-horizon passive protection; the guard permits abort and certifies only an actual finite accepted operation. Comparing their numerical budgets is a decision about which guarantee is needed, NOT a like-for-like asymptotic superiority theorem. Quantum authentication plus error correction remains another strong baseline. No historical novelty, hardware experiment, key-recycling or threshold claim is made.
