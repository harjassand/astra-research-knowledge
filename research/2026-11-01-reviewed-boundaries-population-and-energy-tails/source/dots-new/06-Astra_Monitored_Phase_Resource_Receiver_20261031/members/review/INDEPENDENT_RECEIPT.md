# Independent monitored-phase / photon-only receiver audit

**Decision:** accept the stated *known-model ordinary environment-assisted operation and finite-model certificates*, with the physical-service and output-time restrictions below. No mathematical or implementation error was found in the frozen candidate. This is not acceptance of apparatus feasibility, a novel correction principle, a hardware advantage, universal computation, or a detached stable output register.

Audit identity: `monitored_phase_receiver_independent_audit_20261031_2135UTC`.
Frozen input: `producer-workspace/monitored_phase_resource_20261031`.
Manifest SHA-256: `20c8f193c616ca7215ad0c63ed79703058567ae7cc4d8ef821ce57e79c8740d5`.
Proof SHA-256: `aa1f21548095e605b88d7d7139ef845ff3ad60e47b615ddb6ff5e824cc910429`.
All eight literal manifest entries were hash/length verified before reading/running copied inputs. Execution occurred only in this unique check directory. Frozen inputs were rechecked unchanged at completion.

## Whole-proof review

1. **Physical trajectory reduction.** For a product of actually known computational source bits, conjugation by the product controlled-Z frame makes each `Xs Zd` term source-only, preserves every data Z/ZZ target, and appends data Z to both raising and lowering jumps. The no-jump anticommutator is source-only. Endpoint projection gives `U_phase Z^(N+qT+q0)` for every resolved trajectory; its probability is data/reference independent. This is a complete-channel statement, not a single-state calculation. Initial source/data correlations and an unrecorded unknown initial bit are outside this proof.
2. **Actual bin instrument.** Independently checked the four-sector positive CQ generator and both Fourier sectors exactly. Captured real jumps leave residual parity unchanged; missed and blind-window real jumps flip it; dark clicks flip it while consuming the remaining active bin. All source Hamiltonian, lowering and raising action continues after the click. No emission reset or replacement effective channel was used. Detector boundary rearm and independent capture are assumptions of the declared instrument, not calibrated services.
3. **Optimal ordinary decoder.** The endpoint signed weights are correct after known click/initial-bit corrections. Taking absolute values is exactly the best terminal binary Pauli policy on the available record; this is not a claim about arbitrary other receiver hardware. The no-record fixed Pauli can be reproduced by a record policy that cancels those frame updates. Thus the optimum cannot be forced below a readout error floor. Online filtering is constant source-state memory and linear in bins; exact risk enumeration is exponential in bins, as disclosed.
4. **No endpoint apparatus.** Tracing the source gives an exact mixture of the two final source-Z sectors. The photon-only score is therefore `D00-D11`; no randomized physical source measurement is performed. Known `q0` is still necessary for this stated correction convention. The cold excitation remainder and dead-time/missed-count upper bounds follow from the stated differential inequality and reset-after-true-loss strong Markov argument. They are upper bounds, not thresholds or optimality claims, and do not extend unchanged to hot/thermal/dark sources.
5. **Entire graph and joint faults.** Conditional source/record independence survives arbitrary entangled data/reference inputs because resolved data actions are commuting unitaries and their probabilities are source-only. Product initial sources, local ports, independent detectors and local policies yield the advertised product joint-Z-error law. Weighted graph Z-error states are orthonormal because `U_phase` commutes with Z, giving the stated fidelity and trace norm. Shared failures, adaptive global postselection, unknown correlated sources and unproved calibration locality do not inherit this law.
6. **Exact numerical enclosure.** The direct-sum source Hilbert dimension is 8 and its 16 density coordinates permit a CPTP semigroup. For nonnegative rates and the positive couplings used by the fixtures, the supplied generator bound is conservative. Entrywise complex rounding error is at most `1/S`; an elementary matrix-entry map has completely bounded trace norm 1, so even summing all 256 coordinate entries costs at most `256/S`, below the supplied `2*8^3/S`. For the echo's Euclidean-contractive 2x2 real generator the corresponding bound is also conservative. The scaled Taylor tail is bounded by `2/4^49`. If one-step error is `tail+rounding`, the squaring recurrence `e_next <= 2e+e^2+rounding`, shifted by rounding, is bounded by `(1+tail+2*rounding)^N-1 <= 2N(tail+2*rounding)` under the asserted smallness condition. Instrument composition and terminal-decision Lipschitz bounds justify the displayed risk radius. Parameter validation outside these physical inputs is not promised by this research code.
7. **Fair ordinary controls.** The telegraph echo equations are exact, including thermal rates; the comparator has ideal instantaneous pulses and is thus optimistic, not an implemented service. An odd number of X pulses leaves a known final X frame for an arbitrary data-channel comparison; that frame must be received by the consumer or corrected. This is an interpretation/clarity caveat, not a numerical error. For pure ZZ graph preparation it also acts trivially on the initial plus product after commuting through the target. Target Z phase scheduling, finite pulses, switching and extra duration remain paid.

## Executed independent evidence

- Author suite replayed: **29 exact + 56 floating** checks. Certificate JSON and 112-row diagnostic sweep replayed **byte-identically**.
- `audit_independent.py`: **423 recorded assertions**, many being branchwise positivity/Pauli-form checks rather than 423 unrelated test cases. It independently constructs physical source+data detector maps, optimizes each record directly from its physical channel (without the candidate signed decoder), and verifies complete local superoperators. Cases include known cold/hot bits, thermal raising, dark counts, zero loss, no collection and endpoint report errors above 1/2. It also checks exact CQ Fourier-lift identities.
- `audit_full_graph.py`: independently constructs the **simultaneous 1024x1024 laboratory source+two-data+detector generator**, including local Z and ZZ targets, thermal raising, dark counts and finite bins. It evolves all 16 data operator-basis inputs, so the comparison covers arbitrary data/reference states, not merely the graph input. Full superoperator error against the predicted product-dephasing target channel: **1.013e-15**. Every complete-record probability was data independent. Recovered graph-state joint probabilities agreed with the product law; in particular the two-error probability was **0.03366908777527064**, predicted **0.03366908777527053**. This floating test supports, but does not replace, the general algebraic proof.
- Actual laboratory-frame echo checks with 3 and 63 pulses, cold/hot initialization and thermal up rates agreed with the telegraph comparator after receiving its known terminal X frame.
- `audit_high_precision.py`: **30 independent 80-digit mpmath evaluations** (noisy optimal/blind, photon optimal/blind, raw, echo at five losses) all lie inside the supplied rational intervals. This is a high-precision diagnostic, not an alternative rigorous interval proof.

### Stronger exact endpoint-omission witness

The author reports equality of photon-only and noisy-endpoint optimal risks for losses 64, 256, 1024, 4096. Matching decimals alone would not establish it. We explicitly checked all 16 complete-record decision signs using Gaussian integers and compared each sign margin against the rigorous process radius:

| loss | minimum decision margin | process radius | endpoint report needed by optimum? |
|---:|---:|---:|---|
|16|5.1251e-9|1.3733e-26|Yes: all 16 branches use it|
|64|8.3571e-12|5.4930e-26|No|
|256|1.9547e-13|2.1972e-25|No|
|1024|8.5495e-16|8.7888e-25|No|
|4096|3.3969e-18|3.5155e-24|No|

For the four larger losses, endpoint signed weights have opposite signs on every branch, and photon-only signed weights are positive. Thus the absolute-value score reduces identically to the photon score and blind photon parity is optimal. This proves equality through a shared optimal policy, not rounding. Loss 16 retains the strict endpoint-benefit interval separation. These are the four stipulated points, **not a proof for every real loss >=64**.

## Actual-instrument and physical-cost receiving

The result is a state/channel at the declared time T while the interaction may continue. It is not a free stopped clock, isolated data register or licensed noncommuting downstream operation. Finite source preparation/readout, detector rearm/reporting, collection transport, controls, switch timing and downstream consumption need their own actual instruments and cost/error bounds. Omission removes the terminal source-readout apparatus only; it does not supply cold preparation or spectral collection. The endpoint `2 c t_ro` Duhamel bound is a conservative disturbance allowance, not a readout construction. Error in a scalar fit does not establish a complete instrument-diamond bound or its spatial independence.

The source decay parameter does not, by itself, determine a necessary detector capture bandwidth or prove constant collection efficiency as loss changes. The independent physical output-port model, spectral response, possible backaction/reflections, source preparation and actual target controls remain unearned inputs.

Primary-source check: [Gregoratti and Werner](https://arxiv.org/html/quant-ph/0209025) already gives environment-assisted correction for convex combinations of isometries; this candidate makes no new correction principle. [Ahn, Wiseman and Milburn](https://arxiv.org/html/quant-ph/0302006) supplies earlier continuously detected-error correction context, not evidence of this hardware. [Besse et al.](https://arxiv.org/html/1912.09896), especially Appendix B, distinguishes its calibrated plotted parity means from roughly 85% raw single-shot assignment. Its 78% transmission, 1 microsecond window and 3.5 microsecond dephasing time are not a calibrated implementation of this source; raw feed-forward cannot be repaired by rescaling an ensemble plot.

## Completion / blockers

- **Completed:** frozen-byte authentication; whole proof review; author replays; independent physical full-channel, full-graph, joint-distribution, decoder, lift-sign, echo and high-precision checks; exact endpoint-policy witness; receipt and evidence hashes.
- **Denied actions:** none. No source-input mutation, equipment, purchases, outreach, experiments, publication, external agents or denied-source retries were attempted.
- **Pending / uncertain physical claims:** feasibility and accuracy of a specified actual local source/collection/preparation/control/receiver stack. Target needed to close this is a concrete apparatus instrument with support/error evidence and full exposure/control costs; the present math package cannot supply it. This is an evidentiary boundary, not a tool failure or an invitation to execute hardware.
- **Recoverable local harness event:** the first full-graph diagnostic run stopped on an audit-only NumPy real/complex in-place cast. It was corrected in the audit harness and rerun successfully. It was not a candidate failure; no physical or external action occurred.

No hidden task remains running. No helper agents were used.
