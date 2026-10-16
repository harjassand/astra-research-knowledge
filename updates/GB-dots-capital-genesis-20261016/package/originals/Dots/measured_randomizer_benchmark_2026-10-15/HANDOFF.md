# Exact benchmark handoff

## Ware data contract
Use rgst/data/gst_1.gst through gst_7.gst and rgst_1.gst through rgst_7.gst. Pair only by (run number, exact nominal logical circuit key). Each row has nominal key, minus count, plus count; counts sum to 1,000. The key does not identify a compiled randomized waveform. File order is not a shot timestamp.

The reviewed selection is every exact bare Gi power and every exact bare Gx/Gy power divisible by four. All seven runs are retained. No fiducial-padded substitute or empty {} sequence enters the 189 paired rows. Both outcome counts remain visible. Under the pinned pyGSTi target convention, minus is return to |0> for these powers. Seven-run arithmetic means are descriptive observed fractions, not reconstructed process fidelities.

Physical budget is paper-reported: for nonempty n-Clifford circuits, 2n physical X(pi/2) pulses in both arms, each 50 ns; up to three zero-duration frame updates per Clifford. Derived active pulse duration is 0.1n microseconds and excludes reset, readout, scheduling overhead or unknown gaps. Compiled Pauli changes add no physical pulse cost. Changing n changes task depth/duration; it does not independently vary randomizer rate at fixed task time.

## Boundaries that must stay visible
- Maximum verified released length 1,030 versus reported 6,155 remains an unresolved coverage distinction.
- The public QGL revision is a matching source implementation, not a verified acquisition revision.
- The experiment used a finite compiled ensemble reused across seven runs; actual seed/variant-to-shot mappings and timing are absent. The example 0xcafe seed is not an acquisition fact.
- No pristine holdout or newly declared train/test split exists. The selection was exploratory after named examples had been inspected. Any future evaluation must disclose that and separately freeze its protocol before further fitting or selection.
- The authors' GST analysis is the relevant scientific incumbent. Its model fits and confidence-region pipeline were inspected as source, not executed or recreated here. Do not substitute descriptive return fractions for its full scientific claim.
- Gains are heterogeneous and Gi can worsen. Counts alone do not identify pulse-amplitude error, detuning, ambient bath memory or another mechanism. No universal benefit follows.

## IBM deterministic-DD data
Keep edd_subset completely separate. Its free/XY4 jobs are not same-time paired outcomes, and the notebook's residual-padding implementation has an unresolved executed-schedule gap. Random input states are not random control frames. No joint fit, causal timing comparison, cross-device calibration, or pooling with Ware is authorized by this packet.

## Needed next acquisition
Specify a single-device logical task and fixed elapsed duration; vary actual physical randomizer pulse count/rate including zero; compare against strong deterministic DD; publish executed pulse/phase schedules, widths/gaps, shot outcomes/timestamps, frame/seed bookkeeping, interleaved assignments and repeated calibrations. Measure the net response including control errors and potential turnover. State what randomness is visible to the bath. Neither gate infidelity nor aggregate counts alone supplies the joint operator-norm/CP-process assumptions of a memory theorem.

No hardware, outreach, author-code execution, new fit, or held-out inference is part of this handoff.
