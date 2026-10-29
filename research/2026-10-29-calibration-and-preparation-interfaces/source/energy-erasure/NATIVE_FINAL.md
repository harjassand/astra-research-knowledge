**I constructed and internally reviewed a finite, energy-conserving loss-erasure operation.** It restores lost excitations while erasing the information carried by the captured loss field, using a quantum energy carrier sent forward and a classical result returned afterward. The construction preserves arbitrary inputs—including reference entanglement—within its declared joint data–battery encoding.

This opening earned sustained work because it turns the purification-flow results into an explicit operation: the replacement energy itself can carry the quantum correlations needed for recovery.

## The constructed operation

Write the encoding as
\[
V_N|x\rangle=|x\rangle|N-q(x)\rangle_B.
\]
After loss, a fresh Fock-state carrier restores the missing battery excitations. A local quantum register temporarily retains the loss label. The carrier then travels to the receiver holding the captured field.

The crucial feature is energy balance. If the total loss is \(\ell\), of which \(j\) excitations were captured, the restored carrier and captured field together have energy corresponding to
\[
M-\ell+j=M-r,
\]
where \(r=\ell-j\) is the uncaptured loss. Consequently, different captured-loss histories lie in the **same total-energy sector**. A joint measurement can erase their distinction while conserving energy. Its classical result then controls recovery of the local register.

For attenuation survival \(\eta\) and coherent capture fraction \(\xi\), define \(u=(1-\eta)(1-\xi)\). The complete corrected instrument is exactly
\[
K_{r,k}
=\frac{\sqrt{p_r(N-Q)}}{\sqrt{d_r}},
\qquad
p_r(m)=\binom mr u^r(1-u)^{m-r},
\qquad d_r=N-r+1.
\]

The result \(k\) is uniform conditional on \(r\); only the uncaptured-loss count retains information about the input. **At complete capture, the encoded input factors from every retained record and apparatus output.** The theorem includes multiple losses without an infinitesimal collision approximation.

The proof constructs the conserving restoration, fixed-energy measurement and conditional local recovery. See :chatgpt-content-reference{index="2"}[ENERGY_BALANCED_ERASURE.md](producer-workspace/ENERGY_BALANCED_ERASURE.md).

## A finite pump and an exact complete-record error theorem

I then connected a finite coherent pump to the eraser, including its failed transfers and their actual records.

After calibrated polar feedback, the successful branches have Kraus operators
\[
K_\pm=\frac{\sqrt{I-F}}{\sqrt2},
\]
where \(F\) is the failure effect. The failed-output channel can retain arbitrary quantum information.

For comparison with the ideal identity operation carrying a uniform success bit and no failures, the **exact** complete classical-record error is
\[
\frac12\|\Phi-\Psi\|_\diamond=\|F\|.
\]

If the purification remains coherent across success and failure, the matched complete-output distance is instead \(\sqrt{\|F\|}\). Both calculations include failed runs. The distinction depends on the physical record boundary: an omitted purification that can return invalidates the classical-record contract.

This positive-filter theorem applies beyond the particular pump. It gives an exact operation-level error for a useful class of flagged recoveries, including arbitrary input references and quantum failure outputs.

A further construction removes the separate local flag measurement: one remote joint carrier–field detector produces the same completed instrument. It pays transport and storage on failed runs and provides later failure notification. This simplification was independently checked.

See :chatgpt-content-reference{index="3"}[finite_binary_integration.md](producer-workspace/finite_binary_integration.md).

## Calibration and decisive failures

The calibration construction compares the **complete physical mode dilations before applying the same nominal recovery**. This remains valid even when a nominal detector outcome has zero probability; it avoids differentiating a normalized rare-branch state.

Several failures materially shaped the result:

- **Transfer populations do not certify the operation.** An independent exact example has perfect transfer population and zero nominal failure, yet an uncalibrated phase changes a nominally uniform detector bit to probabilities \(1/50\) and \(49/50\).
- **An inaccessible copy of the old loss count defeats erasure.** A harmless-looking public record is insufficient.
- **Passive two-mode optics does not implement the general required mixer.** The multi-photon construction needs additional selective control.
- **Small coherent memory does not imply cheap processing.** The local register has logarithmic width, while its control complexity, holding time and fault exposure remain substantial resources.

The calibration proof and executable checks are in :chatgpt-content-reference{index="4"}[CALIBRATION_BRIDGE.md](producer-workspace/CALIBRATION_BRIDGE.md).

## What this adds—and the comparison it must survive

A governing ancestry correction is preserved: normalized photon replacement and its square-root-number phase diffusion were already derived by Vitali, Tombesi and Milburn in 1998. Those mechanisms are established starting material. The contribution here is the explicit finite conserving interface and its complete-record integration; historical priority for that specific bridge remains unestablished. :chatgpt-content-reference{index="0"}

Strong conventional alternatives remain competitive. Coherent return of the captured field permits simpler passive recombination. With the necessary transduction and Bell-measurement interfaces, entanglement distribution and teleportation can provide comparable access. Fixed-charge direct coupling may avoid battery exposure altogether.

The constructed route requires matched physical gaps, coherent capture, a forward quantum carrier, charge-selective control, local coherent storage through the return delay, and qualified readout and reuse. It establishes neither a hardware advantage nor a total workload threshold. Its exact multi-loss theorem concerns an idle attenuation interval; arbitrary noncommuting computation during that interval remains a different decoding problem.

**The substantive gain is a constructive connection between conserving energy replacement, purification flow and the actual classical record.** It identifies an operation that is possible under explicit interfaces, and provides an exact way to carry finite pump failure into the intended computation’s channel error.

The main eraser passed two distinct internal reviews. Calibration and finite-pump integration received separate independent reviews, including exact reference-entangled checks and isolated executable replays. These are internal research reviews, not external peer review.

The proofs, executable work, source corrections, useful failures and precise review scopes are indexed in :chatgpt-content-reference{index="5"}[CONTROL_SUCCESSOR.md](producer-workspace/CONTROL_SUCCESSOR.md). The completed predecessors remain unchanged.