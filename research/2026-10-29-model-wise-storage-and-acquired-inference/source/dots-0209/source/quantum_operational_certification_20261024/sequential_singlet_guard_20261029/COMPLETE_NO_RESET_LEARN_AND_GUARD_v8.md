# End-to-end retained-memory discovery and guarded finite operation
2026-10-29. Separate extension of the accepted finite v5 example; original files unchanged. Mathematical execution, not hardware evidence. Pending independent review of this composition fixture.

## What is actually joined
Replay the1,000,000-call acquisition in `../nonunital_collective_frame_acquisition_20261029/check_retained_memory_bank_v4.py`. It uses ordinary fresh product-Pauli probes, one never-reset bath qubit, and source unitaries selected by the previous output parity. From the SAME final classical counters, fit each full16×9 pair-adjoint defect, take its smallest right singular vector, and perform the specified ±SO(3) rounding. Compile that inferred relative frame with the known four-qubit singlet encoder.

Then carry the acquisition run's FINAL bath state forward into the guarded operation with NO RESET at the stage boundary. The source uses the first of the acquisition's two known-generator collective joint unitaries during guard calls. This is a declared source fixture, not a prediction that an arbitrary future environment equals an estimated occupation channel. The actual physical learner/guard does not receive the bath state or Kraus operators; only the simulator uses them to evaluate the execution.

The frame is NOT selected using its hidden true-frame error, bath state, future yield, or exact operator baseline. It is a candidate from the1m classical probe bank. Its conservative acquisition-confidence stopping rule has not fired and is not claimed to have fired. Accepted-operation soundness remains the already proved model-free guard property for any fixed candidate frame.

## Unchanged finite design
Keep all prior guard parameters fixed: n=4, one logical qubit per inner service, conservative C=6, service probability1/7, b=0, t=6, grouped [[31,7,13]]_32 outer code,35 payload qubits,155 inner services,1400-call cap, and rigorous subnormalized accepted half-diamond bound0.0078125. Keep the same predeclared alternative lab-frame Z burst at guard calls500–511. No retuning is performed after observing the new learned frame or guard outcome.

## Execution results
`complete_noreset_learn_and_guard_v8.py/.json` reports:

* Collective retained-bath continuation: exact compressed-DP acceptance0.7757656926, expected957.4809004 guard calls, accepted probability of more than6 faulty inner services1.47417e−12. In1000 sampled CP-instrument trajectories773 accepted; the first50 nonzero accepted ledgers were actually passed through the GF(32) decoder and all corrected.
* Predeclared Z burst: acceptance0.01370272747, abort0.9862972725, expected482.3938639 guard calls, accepted bad-count weight1.3731832e−5. Fourteen of1000 trajectories accepted, and all14 nonzero accepted ledgers were actually decoded correctly.

The lower good-source acceptance than v5 is not concealed: this new candidate uses1m no-reset probe calls rather than8.991m replayed finite iid-style banks, and its observed frame error is larger. The setup/source generator also differs, so this is NOT a controlled claim of sample-efficiency superiority. It is an executed continuity check from retained-memory learning to guarded service.

The complete charged data budget is1m acquisition calls plus at most1400 guard calls, each on the same four-qubit native port, together with all ordinary probe preparation/readout, signed test preparation, routing, private pads, outer code gates/classical processing,155-qubit trusted endpoint buffers, and the full durations of those calls. No quantum bath reset was inserted. All ideal control and privacy assumptions remain; no noisy-hardware threshold is acquired.

Source-generator compression, exact logical/bath twirl identity, total outer decoding, and all earlier interpretation cautions remain as in v5. DP probabilities are floating-point mathematical fixture values, not experimental or interval-certified laboratory bounds. Universal soundness is the theorem's0.0078125 subnormalized bound; rare burst acceptance does not inherit that value as its normalized conditional error. No superiority over direct two-design/authentication/QEC alternatives is established.
