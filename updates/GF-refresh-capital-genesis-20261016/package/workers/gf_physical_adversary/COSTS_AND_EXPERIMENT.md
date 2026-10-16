# Paid qualification design and comparison

16 October 2026. Proposed experiment only. No hardware was operated or purchased, no dataset was asserted to be a performed refresh, and no dollar/energy figure is guessed.

## Minimum acceptable pilot

Choose one low-weight physical stabilizer S on an encoded patch. Fix one actual recovery deadline H and its entire controlled region before choosing an estimator. A small controllable sidecar bath is a suitable restricted pilot; an unknown environment is not silently treated as a controllable qubit. The confidence target is either (a) the full joint channel on this complete controlled boundary, with a justified energy truncation; or (b) the finite-horizon initialized-bath operational process and specified endpoint logical output.

The source experiment must include the actual physical I and S branches, common timing, and fixed-reference phase-sensitive preparation/measurement. It must retain emitted waveforms, initializations, counts, circuit and randomizer labels in a secure characterization environment, and delayed return tests. A characterization copy of the seed is permitted only if the baseline cannot access it during the asserted horizon; deploying a record-free randomizer and characterizing a seed-preserving one requires an explicit equivalence argument.

A software-only frame update is a negative control. The positive operation is a physical Pauli endpoint whose randomization is not subsequently canceled. Measure actual simultaneous neighbors, leakage levels, bus states, history dependence, and recovery. Reconstructed model residuals are not hardware observations until held-out interventions and calibration budgets support their stated guarantee.

## All required costs

| Cost | What is measured or supplied |
|---|---|
| Acquisition breadth | Number K of actual tester settings; trusted tester model/rank and allowed continuation effects; shot counts n_k; all additional reference/ancilla preparations. |
| Statistical precision | Simultaneous confidence level alpha and radius from the proof file; coefficient conditioning; no replacement by best-fit fidelity. |
| Systematic precision | SPAM, frequency/phase/angle, timebase, readout, repeatability/drift, transfer-function and model-completeness errors, independently bounded. |
| Control | Peak amplitude, available generators, switching/bandwidth, emitted pulse shapes, branch duty cycle, simultaneous schedule and tail reservation. |
| Harmful pulse action | Every noncommuting baseline/crosstalk/bath/leakage term integrated over the real path, not only the pre-pulse coarse-odd projection. |
| Bath boundary | Retained Hilbert dimension; accessible modes; initial energy/level tail nu; cross-boundary coupling action gamma; reachable-state restriction. |
| Seed | One fresh bit for a fair binary endpoint; bias bound; input independence; physical carrier inventory; no-return time. Measured entropy/bias alone does not certify privacy. |
| Reset | Initialization/recovery/measurement times, bath reinitialization, classical buffer clearing, controller rest time and pulse-tail clearing. Landauer's bound, if quoted, is a thermodynamic lower bound and is not actual measured heat. |
| Geometry | Expanded data footprint until H, hardware couplers and spectator influence, code correctability calculation, external tail residual and all reservation conflicts. |
| Useful output | Encoded logical channel/process at the same horizon and initialization for each competitor, including reference-sensitive tests and actual decoder imperfections. |
| Scaling | Number of local modules, overlap/grouping, total calibration time, added qubits/modes, update cadence and how every residual changes with code size/storage time. |

Most entries are UNKNOWN for a proposed Astra module. All were absent together from the inspected experiments. The proof file makes statistical and finite-model terms computable; it does not replace engineering acquisition of the remaining structural bounds.

## Information-matched incumbent

Give every contender the same measured Hamiltonian confidence region, initialisation knowledge, pulse/energy constraints and endpoint objective. Permit the incumbent its best established Eulerian/DD/DCG and randomized-compiling options allowed by those constraints, including schedules optimized from the same process data. Do not compare only with a square pulse if calibrated corrected implementations are feasible.

For one-qubit arbitrary decoherence, standard Eulerian Pauli memory control uses eight primitive pulses and has a finite-width full-remainder bound in Ng-Lidar-Preskill Eq. (82). A nontrivial endpoint has its own appended/modified gate charge. A first-order nontrivial balance-pair DCG in the cited concatenated construction occupies 20 primitive-duration units with the required inverses/stretching. Those are symbolic construction costs, not measured times or a claim these are the best implementations. Multiply-qubit stabilization requires the actual available group/control algebra; do not apply a one-qubit sequence count without that reduction.

A raw physical I/S primitive can reserve one common window tau. With w parallel single-qubit pi rotations and per-qubit Hamiltonian norm Omega, tau>=pi/(2Omega); the total simultaneous controller norm may be w Omega. The fair random branch averages w/2 active rotations but still pays the whole common window and all idle/bath evolution. Serial gates pay at least w such durations. The waveform, field energy and pulse-tail overhead must be measured.

An upper bound being smaller is not a physical performance result. Report conservative certificates and observed logical outputs separately. If a well-calibrated known static unwanted field can simply be canceled, the equally informed cancellation strategy is admissible. An engineered unknown bounded classical field is a useful demonstrator but is not protection against an acquired arbitrary quantum bath.

## Precision can consume the theoretical gain

The receiver's relevant scale is its actual ideal factor f_i (and, for a proposed refinement, the improvement Delta_i). Its total implementation/qualification charge must be substantially below f_i to preserve leading rare-event scaling and below Delta_i to resolve the claimed improvement. Neither an average physical fidelity nor a fixed absolute epsilon is enough to guarantee that.

For a complete-horizon comparison with M substituted modules, the conservative hybrid error is at most sum_i epsilon_i. A fixed epsilon at every module cannot be ignored over increasing storage times. A sharper product requires a separately valid local causal/independence certificate and the correct actual event. A measured one-horizon logical output does not establish an all-time exponential lifetime.

The finite-sample table below follows the proof's stated sufficient Hoeffding certificate and contains no acquired data:

| Design illustration | epsilon | alpha | Sufficient total binary shots |
|---|---:|---:|---:|
| One directly performed endpoint effect | 0.01 | 0.01 | 26,492 |
| One directly performed endpoint effect | 0.001 | 0.01 | 2,649,159 |
| 324 unit-magnitude dual coefficients, optimized equally here | 0.01 | 0.01 | about 1.88e12 |

The last row is deliberately loose. It shows why a design-specific target/dual and systematic budget must be computed before spending shots; it is not a claimed lower bound or a reanalysis of the 324-setting experimental dataset.

## Decisive pass/fail

First perform the identification-span/rank test on the proposed exact continuation and trusted experiment model. If it fails, add specifically distinguishing interventions or narrow the claim. If it passes, compute the confidence region and costs before hardware execution. Reject an empty region as model/calibration failure. Next require a complete residual below the named target, a correctable footprint, and a no-return horizon. Finally compare useful encoded output and full paid resources against the equally informed incumbent. No present inspected record passes this chain.
