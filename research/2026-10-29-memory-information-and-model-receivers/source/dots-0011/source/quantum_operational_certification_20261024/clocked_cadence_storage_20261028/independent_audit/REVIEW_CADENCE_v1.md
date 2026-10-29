# Independent cadence composition and counts-only holdout review

28 October2026. **Accepted at the explicit numerical/model-conditional and implemented-record-law scope below.** No load-bearing defect found. Author originals were not modified.

## Independence and dependencies

This review concerns cadence composition, noncommuting timing order, source/learner separation, sampling, exact-binomial decisions and resource accounting. The review does **not** independently certify the underlying clocked EC primitive again: that is the separately reviewed `clocked_flagged_storage_20261028/independent_audit/RECEIPT_CLOCK.json` dependency. It does not self-review the reviewer's earlier endpoint-oracle derivation. The terminal oracle and all-adaptive single-carrier ceiling remain their separate reviewed dependencies, including mandatory-link/no-quantum-bypass and unmonitored native-channel assumptions.

The independent checker constructs full32×32 Pauli matrices, code operators and terminal decoding matrices, then forms the full five-site native transfer map. It propagates **one mandatory native use at a time**, applying the supplied physical EC map only when the use number is divisible by r. It neither powers decoded logical maps nor calls the author's cadence implementation. The recorded36 grid points agree to3.78×10^-15 in PTM entries, conditional on the same reviewed primitive F.

The same independent per-use stepping reconstructs the single-carrier baseline, inserting the background map after every r uses. Agreement is1.67×10^-15. Replacing this sequence by a single accumulated background map at the end can differ by0.965 in a PTM entry on this grid. Thus the noncommuting ordering in `(D N_site^r)^(T/r)` is material and is correctly retained.

## Time and policy accounting

For every grid row, the checker verifies T/r physical EC windows,5T encoded native carrier exposures,T single-carrier exposures per site, and elapsed trajectory duration2T+201T/r. Cadence comparisons have fixed mandatory-use count but different elapsed time; the single-carrier comparison matches the time **within each policy**, not across policies. No general passive-memory interpretation follows.

The source-informed grid is not learner evidence. It can diagnose why the finite policy set is useful, but its best r is not presented as learned until a separate counts-only experiment chooses it. Version1's serialization failure is preserved. The reviewer verifies that version2 changes only the NumPy-bool cast and results filename, leaving the scientific computation identical.

## Counts-only selection and independent validation

The selector sees a dictionary of ordinary per-policy selection counts. It chooses minimum failures, with the declared larger-r tie rule. It does not receive hidden rates, matrices, oracle scores or source parameters. The generator and post hoc scorer do access those quantities, as explicitly separated in the program. The plan and raw records are hash-bound. Code ordering and the no-overwrite guard support the internal predeclaration claim; this review does not independently establish a historical human-inspection timeline or external preregistration.

The reviewer independently recomputes all quantized CDF thresholds from the supplied floating endpoint maps and replays all61,440 setting/coin draws using the saved seeds. Every raw count agrees exactly; seed streams for selection and validation are distinct. Choices are2,4,8. A fresh validation stream is generated only after each chosen policy is fixed. Therefore there is no need to multiply the validation error budget by six candidate policies: conditional on the selected policy, its fresh outcomes have the stated Bernoulli mixture law. The three-context family bound remains3/3000=1/1000 for that implemented law.

For uniformly sampled±logical-Pauli preparations with matched ideal decoded measurements, the nonunital translation terms cancel and

    p_failure = (3−Tr A)/6 = 2(1−F_e)/3.

Thus p_failure≤4/15 corresponds to F_e≥3/5 under the declared trusted logical preparation/readout interface.

The independent exact-tail implementation evaluates a different integer polynomial, factoring11^(N−k), rather than calling the author's recurrence. Numerator and denominator digests match all three decisions. For8192 trials, the largest accepted failure count at alpha1/3000 is2048;2049 is rejected. The actual counts931,2406,3593 therefore yield **PASS, FAIL, FAIL**. Failed targets are retained without reselection or extra sampling.

The floor-CDF error per draw is below2^-52 relative to the supplied floating Born probability; all inspected probabilities lie within[0,1], so no clipping correction was needed. A union/coupling bound across61440 draws gives the stated61440/2^52 contribution. This does not outward-round the underlying quantum-channel coefficients or certify an experimental quantum fidelity. The exact confidence statement belongs first to the implemented record law; physical interpretation remains conditional on the numerical model and trusted interfaces. No diamond guarantee follows.

## Costs and scope clarification

Independent totals are61440 trajectories and9,830,400 new native carrier exposures. The127,838,208 reference-time total is the **sum of elapsed durations of individual trajectories**, with five data carriers parallel within each trajectory. It is neither summed qubit-time nor laboratory wall-clock time. The separate `ACQUISITION_TIME_SCOPE_ADDENDUM_v1.md` correctly gives639,191,040 data-carrier-time units before endpoint overhead and leaves ancilla live-time uncomputed. Initial preparation, final decoding/readout, available parallelism and inherited frame-learning costs remain separate.

Accepted: actual cadence composition at the supplied clocked primitive, numerical grid replay, counts-only finite-policy selection, fresh exact-binomial validation at its record-law scope, and the explicitly qualified resource bill. Not established: new code/selection novelty, high-fidelity hardware, arbitrary environmental-memory protection, total architecture optimality, external blind preregistration, or a general passive-memory lifetime advantage.
