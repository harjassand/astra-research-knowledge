# Astra: measurement-based memory protection and its detector-footprint obstruction

Research checkpoint: 2026-10-15. Conditional mathematics, exact finite-code computations, and acquired experimental evidence. No demonstrated new hardware capability. Internal reconstructions and runnable checks are not independent external validation.

## Decision-relevant result

Repeated stabilizer measurements give a simpler route to the scheduled-memory noise bound than ideal randomizing pulses. The extra outcomes need not be read: a qualified nonselective measurement channel with fresh, non-returning reservoirs supplies a valid latent Kraus decomposition. For M equal weak-noise cells, the proved parent bound is p <= min(1, J^2 tau_noise^2/M), with a product bound for every selected set of clean parents even when their environments are shared. These are conditional full-input operator bounds, not inferred laboratory error probabilities.

However, treating the detectors' entire data footprint as another arbitrary noisy patch does not close the same proof. A general stabilizer-rank argument shows that a self-contained check region satisfying the unchanged zero-good-support condition must be a fixed pure stabilizer factor of the code. That region cannot be a nontrivially coupled memory patch. This defeats a specific proposed repair of the assumptions; it is not a general impossibility of noisy quantum error correction.

## Concrete hardware-code check

For the acquired [[33,1,4]] code matrices used in a published trapped-ion experiment, every weight-4 check footprint needs at least 7 of the existing checks to resolve all local errors modulo stabilizers. Their data support touches at least 14 qubits. A weight-5 footprint needs at least 9 checks touching at least 18 qubits; every sufficient such detector union is uncorrectable as an arbitrary Pauli-error region.

The computation exhausts 61,696 minimum check sets and supplies 25,320 target/union certificates. A separate implementation reconstructs the enumeration and verifies the stored logical witnesses. A connected check-overlap graph also proves that no nonempty region of this code closes under the same fully noisy, zero-good-support certificate. Check counts concern existing generator measurements, not arbitrary new synthesized instruments; data union size excludes extra ancilla and transport costs.

## What was actually established experimentally

Kalb et al. (2016) demonstrated repeated nonselective joint-spin projections that inhibit quasi-static dephasing and protect encoded states. This is the closest acquired physical interface to the unread-measurement refinement. Its nonzero control overhead, imperfect operations, and restricted error model do not establish the full-joint channel assumptions or all-selected-parent bound.

Slichter et al. (2016), on a different device, directly measured suppression of coherently driven transmon transitions under continuous energy measurement. The packet includes 114 reproducibly digitized published figure points. These are figure-level summary estimates, not raw trajectories, author source data, or a uniform noise certificate. The devices and their rates are never combined.

## Closest prior results

Projective and weak-measurement Zeno error protection are established ideas. Dominy et al. already represent an unread weak measurement as a probabilistically skipped projective measurement and analyze finite repetition rates. AGP supplies shared-bath all-location amplitude bounds. The present unresolved novelty question concerns the precise uniform joint-effect / clean-parent / scheduled-memory composition, not the existence of Zeno suppression, weak measurement, or skipped projections.

## Missing operation and decisive next test

A real measurement implementation must include ambient noise during gates, reset, transport and measurement, and a support certificate that handles those faults. Readout-free operation removes one requirement; it does not establish exact QND backaction or isolated reservoirs. A useful repair must either qualify separately charged detector faults, prove a broader space-time support rule, or justify a stable restricted perturbation family. Merely expanding the same noisy footprint fails by the rank obstruction.

The immediate mathematical gate is an actual faulty-instrument model whose effects and support can be bounded without assuming an ideal measurement hidden inside it. The experimental gate is a same-device, full-wall-clock logical-memory comparison with acquired numerical data and an equally informed incumbent. Published mean rates and average infidelities cannot be substituted for arbitrary-bath operator bounds.

## Reading order

1. measurement/UNREAD_MEASUREMENT_REFINEMENT.md and DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md
2. measurement/FULL_DETECTOR_FOOTPRINT_CLOSURE_OBSTRUCTION.md
3. detector_footprints/REPORT.md and its independent audit
4. measurement/MEASUREMENT_COST_CRITERION.md and the partial-dephasing extension
5. experiments/REPORT.md, PROVENANCE.json and README.md
6. foundations/ contains the previously developed deletion-null and scheduled-memory premises used in the composition; their conditional status is retained.

The cost criterion optimizes a conservative bound, not actual observed error. Positive measurement-time cost prevents unlimited subdivision from becoming a free improvement. Partial-dephasing boundaries also retain finite-exposure limits and require their stated sequential channel interface; simultaneous noise during a finite measurement is not automatically that interface.
