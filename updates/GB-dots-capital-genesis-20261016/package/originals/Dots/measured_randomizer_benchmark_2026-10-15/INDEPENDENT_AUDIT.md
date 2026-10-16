# Independent measured-randomizer benchmark audit

2026-10-15. Verdict: **PASS for the released aggregate-count, pairing, selection, arithmetic and retained-source interface.** This is not a new hypothesis test, fitted mechanism, causal estimate, or untouched-holdout study. No author software was executed or installed.

## Verified from original retained text
Own independent_audit.py uses a recursive gate-string grammar, an independent count parser, exact rational arithmetic and static source inspection.

- All 14 Ware count files have 3,505 unique nominal keys, in identical order, and two nonnegative integer counts summing to exactly 1,000. Total represented outcomes: 49,070,000. Header order is minus then plus. Pairing is by run number and exact nominal key, not chronology.
- Every 189 paired row (27 keys × 7 runs) exactly matches source counts. All seven-run mean fractions, paired mean differences, extrema and positive/zero/negative pair counts recompute correctly. No extra selection, significance test or fit was added.
- Gx/Gy lengths are 4,16,32,64,128,256,512,1024; Gi lengths are 1,2,4,8,16,32,64,128,256,512,1024. Exact bare length-eight X/Y keys are absent; no padded keys substitute for them. Empty {} is excluded.
- pyGSTi v0.9.3 target source defines preparation |0>, the plus effect |1>, and minus as the remainder. Thus minus is the ideal return label for the selected identity-return powers. This is a source convention, not relabeling whichever outcome performed better.
- Maximum expanded released length is 1,030. The pinned pyGSTi implementation defaults to whole germ powers (total germ-body length bounded by L), with length-as-exponent a distinct option. This supports the released length interpretation. The paper-reported maximum 6,155 remains unreconciled with the acquired subset; the evaluator makes no larger-coverage claim.
- All 24 QGL DiAC angle rows independently agree with the retained 0.5-scaled source table, and the routine has exactly two X90 calls separated/surrounded by virtual Z operations. Zero-duration ZPulse and channel-defined X90 pulse width are visible in retained source. The specific 50 ns width is paper-reported, not inferred from an included calibrated Ware waveform.
- The Randomize notebook says 1,000 compiled variants were each measured once per run, across seven runs; baseline circuits were measured 1,000 times. The example seed is not authenticated as an acquisition seed. Shot/variant mappings and exact physical schedules are absent from this inspected release.
- All 61 previously recorded provenance entries match both byte lengths and SHA256. Retained Ware, EDD and QGL repository licenses are Apache 2.0; pyGSTi source is GPLv3-or-later, with its notice and full license retained. No full primary-paper PDF/HTML/text is redistributed in the packet.

## Descriptive findings and their scope
The saved means are correct: Gx32 return 0.3852857143 baseline versus 0.723 randomized; Gy32 0.378 versus 0.716; Gi128 0.7155714286 versus 0.549. These heterogeneous changes, including worsening Gi, are observed fractions rather than corrected fidelities or universal benefits.

For every nonempty n-Clifford circuit, the **paper-described implementation** uses two 50 ns physical X(pi/2) pulses per Clifford in both arms. Therefore the derived physical pulse budget is 2n per arm and active pulse time 0.1n microseconds. Virtual-Z changes alter the physical pulse phases. Random Paulis are folded into neighboring Cliffords and add no physical pulses. Active duration excludes preparation/readout/scheduling overhead. This dataset cannot estimate added-physical-randomizer pulse cost or a randomizer-rate optimum at fixed task duration.

The 2018 QGL snapshot matches the public implementation description, but the exact acquisition revision remains unidentified. Static source consistency does not authenticate executed waveforms, calibrations or a microscopic control-error model. No physical mechanism is identified by the count differences.

## Separate IBM deterministic-DD condition
An independent bounded parser also verifies the three retained raw-result files: 25 free-evolution circuits and 100 circuits in each of two XY4 jobs, each with two counts totaling 8,192. This check does not pool or compare their outcomes with Ware. The timestamp gaps are real: XY4 at 06:53:04 and 08:04:39, free baseline at 09:59:38 on 2022-04-07, all −07:00. They do not establish drift-free pairing.

The inspected schedule notebook applies residual T_diff padding to a scratch schedule rather than the seq_sched that is submitted. The actual executed schedule cannot be authenticated from that static source alone. Random input states are not randomized control frames. This deterministic-DD condition is an explicitly separate pulse-cost reference with unresolved timing/drift limitations, not a device calibration to combine with Ware.

## Exact boundary for future work
The missing experiment varies **actual added physical randomizer pulse count/rate** at fixed logical task and elapsed duration, with zero-added-control and a strong deterministic-DD comparator, and publishes executed waveforms/pulse timing, shot outcomes/timestamps, frame/seed bookkeeping, interleaving and repeated calibrations. None of the present data establish private fresh bath-independent randomness, a joint system–bath operator bound, a CP fault-process hypothesis, a decoder threshold, or a universal benefit. Additional physical modeling or fitting requires a separately specified task and evaluation design.

Files: independent_audit.py and independent_audit_results.json. The portable replay additionally reruns the original own-code validate_counts.py in a disposable directory and checks the saved exports exactly; retained third-party code is never imported or executed.
