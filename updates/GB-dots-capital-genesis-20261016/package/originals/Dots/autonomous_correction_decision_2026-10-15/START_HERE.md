# Astra: a measured autonomous-correction evaluator and an exact recovery ceiling

Checkpoint: 2026-10-15. This packet combines acquired published aggregate data, independent sensitivity checks, and a model-specific mathematical optimization. It establishes no new hardware performance or historical novelty.

## Strongest mathematical finding

For the actual four-level spin encoding used by Li et al., under a stipulated single Gaussian dephasing event, the published ideal recovery is globally optimal among every CPTP recovery that preserves every code state exactly, including logical coherences. The proof does not just compare a chosen circuit family.

If exact codespace preservation is relaxed, the unrestricted CPTP optimum can be constructed by a conditional polar-alignment operation. Its improvement over the published ideal recovery is globally bounded by **0.0064661038398026 in entanglement fidelity**, or about **0.647 percentage points**. The maximum is certified analytically, not only by a numerical search. It requires noise-dependent coherent mixing of the code and error spaces before syndrome erasure and deliberately loses exact no-noise code preservation.

This closes a specific tempting route: optimizing only the ideal recovery map for this fixed encoder and noise model cannot supply a large new capability. The original encoding is also optimal within the stated mirror-encoding family if exact codespace preservation is retained. This is not a theorem about every encoder, noise process, multi-cycle protocol, or actual imperfect implementation. The source operation belongs to established channel-adapted quantum recovery; no priority claim is made.

## Actual acquired evaluator

The CC BY 4.0 Zenodo archive 20768851 supplies normalized and unnormalized process-fidelity curves, fifteen interleaved comparisons, fitted coefficients, and real parts of three process matrices. Source bytes and checksum are preserved. These are published aggregate estimates, not raw shots.

At the common measured ambient-storage time 29.0445 ms, QEC exceeds the physical comparator by 0.078 normalized and 0.065 unnormalized fidelity. Eleven of fifteen interleaved pairs favor QEC. The measured ambient advantage is not uniform across all eight time points. All five exactly matched injected-noise times favor QEC. Those comparisons do not require a decay fit.

The June 2026 deposited data differ from the April 2025 manuscript. A 2026 author abstract matches the revised lifetime values, but the corresponding revised full methods were not identified. Their numbers and assumptions remain separately identified.

## Three consequential limits exposed

1. **Lifetime fitting:** ten of twelve deposited fits reconstruct under the stated weighted least-squares objective and a broad bounded-fidelity domain. The two ambient QEC fits reproduce after adding a diagnostic offset restriction a>=0.4. This is consistent with a fitting constraint but does not establish the authors' actual procedure. Lifetime ratios vary with the tested offset assumptions; these alternative fits are sensitivity studies, not equally credible models or confidence intervals. Direct same-time advantages remain separately reported.
2. **Missing channel information:** the three exact central process-matrix arrays each contain a negative diagonal. No omitted imaginary entries can make those central arrays completely positive. They are uncertain reconstructed estimates; this is not evidence of nonphysical experimental dynamics. Raw counts, full complex matrices, covariance and revised reconstruction details are needed before composing them as physical channels.
3. **Missing strong control comparison:** documented optical transitions can synthesize a three-pulse physical-qubit inversion, and a six-pulse identity-memory echo schedule. Calibrated durations and errors for that sequence are unavailable. It is a concrete untested baseline, not a demonstrated improvement. Finite-pulse noise and all control costs must be included in a matched comparison.

## Fault-aware theorem, separately qualified

The measurement CP-coin theorem supplies one mathematical escape from the detector-footprint obstruction: independent, input-independent mixtures of ideal operations and arbitrary local faulty operations can be charged on the entire reserved parent support. The joint parent factor is f+(1-f)p_weak, and correction/controller slots can be included under the same assumptions.

This model must be established rather than inferred from average gate error. An arbitrarily small coherent rotation after ideal pinching has zero positive exact-pinching CP-subchannel weight. Thus closeness alone does not imply the required ideal/faulty mixture. This remains a conditional sufficient interface, not a hardware qualification.

## Decisive next scientific test

A useful physical comparison would retain the same device, input states, noise realization/interleaving, storage clock and acceptance rules, then compare the existing autonomous correction with the explicit optical refocusing baseline at measured pulse costs. The needed existing records are revised methods, complete complex process/shot data and actual control calibration. No outreach or new experiment has been performed.

The exact recovery ceiling argues against spending a large invention campaign on ideal recovery-map optimization in this model. Imperfect implementation, a better justified noise family, or a genuinely different measured control operation must provide the next leverage.

## Navigation and reproduction

- optimal_spin_recovery/RESULT.md and independent_audit.md: global analytic certificates, explicit map, exact ceiling and scope
- autonomous_correction_evaluator/README.md: dataset, timing, version, normalization and CP-completion audits
- autonomous_fit_audit/README.md: nuisance-profile sensitivity and fit-independent comparisons
- autonomous_echo_comparator/README.md: documented controls, exact proposed sequence and conditional models
- faulty_measurement_cp_bridge/THEOREM_AND_LIMITATION.md: qualified faulty-controller/measurement theorem

Run REPLAY.py from a fresh extraction. It executes only our original checking code, not the authors' simulation. The original source archive contains author software; its presence is provenance, not an assertion that it was executed or validated. Primary links and acquisition metadata are included; full manuscript/conference documents are not redistributed in this packet.
