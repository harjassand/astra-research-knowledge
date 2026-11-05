# Passive output-only Hamiltonian calibration with finite classical photon counts

This construction learns a static local Hamiltonian from one continually evolving source through classical photon records. Calibration needs no direct source preparation/control/readout, coherent output collector or receiver quantum memory. It uses the **actual calibrated vacuum Pauli ports**, a finite coherent local oscillator, a finite correlation response and a nonlinear inverse. The separate quantum archive remains necessary if this learner is used to recover an earlier arbitrary input.

Read the complete [report](package/Astra_Passive_Hamiltonian_Calibration.pdf), [editable proof](package/next2_root/passive_calibration_report.tex), [response/inverse/compiler theorem](package/next2_continuous_quantum/OUTPUT_ONLY_CLASSICAL_CALIBRATION.md), and [independent finite-LO/response review](package/next2_alternatives/finite_lo_implementation_review.txt).

| Distinct result | Direct route |
|---|---|
| Finite classical response, Hamiltonian inverse and exposure law | This page |
| Actual optical measurement, counters, detector service and timing | [Finite photon-count interface](finite-photon-count-interface.md) |
| Completed independent whole reliability-curve certificate | [Equilibrium-safe curve and changing-law uncertainty](reliability-curve-certificate.md) |
| Separate all-working initialization extension | [Chosen-deadline point-query construction](all-working-point-query.md) |
| Original material | [ZIP](original/Astra_Passive_Calibration_Research_Package.zip), [complete captured return](P3_PASSIVE_CALIBRATION_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

These are conditional constructive theorems with declared acquisition costs and limited recorded implementations. They do not establish historical firstness, universal practical superiority or a deployed civilisation-scale capability. Capital performs no scientific rerun or new audit.

A subsequent [declared correlated-Gibbs extension](../2026-11-05-p3-correlated-reliability/README.md) constructs rare static counting and failure-conditioned sampling from pinned Gibbs operations, then joins them to this finite curve machinery. Its fixed logarithmic contrast, all-pinning mixing and reversible operating-gap premises replace the product-law static interface; the original result and source artifacts here retain their own scope.

A separate [controlled-source quantum export companion](../2026-11-05-p3-direct-prevention/quantum-export-control.md) adds actual calibrated source rotations and pure coherent three-axis Weyl ports. Its full-output construction retains paid receiver/control costs and discards the correction key. This stronger physical access is distinct from the output-only calibration setting here. Original source files remain unchanged.

## Static model and actual observations

The known complete nonidentity Pauli list has maximum weight k and candidate degree d. Unknown static coefficients obey a supplied **per-site sum bound** `max_i sum_(P contains i)|theta_P|<=J`. Bounded arity alone does not imply bounded candidate degree. The source has actual ports `L_i,a=sqrt(r)sigma_i,a/2`, independent vacuum inputs, known positive r, calibrated axes/phases/gains and known positive collection efficiency kappa. The full source/port model, stable dynamics throughout exposure and absence of omitted couplings are premises; photon flux alone cannot certify them.

All `3n` ports are measured concurrently. A matched finite local oscillator gives two signed projector jumps `J_+=sqrt(kappa r/2)Pi_+`, `J_-=-sqrt(kappa r/2)Pi_-`, total detected rate `R=kappa r/2` per port. Window count differences are ordinary classical data. Empty windows and counter overflows are included through the stated estimator, not removed by normalized postselection. [Finite physical construction](finite-photon-count-interface.md).

Adjacent-window products minus their time reversals cancel all even Hamiltonian orders. For a weight-b candidate, a `(b+1)`-point response has a positive diagonal linear kernel. In the stationary hard family `H=theta P`, moments of order at most b are exactly sign-blind; this is a moment-order limitation, not a no-go against arbitrary full-record processing. The finite window is chosen from dynamical bounds and **does not shrink with target coefficient accuracy**.

## Certified inverse and finite forward computation

Damping-aware and all-positive-r finite-time bounds control the nonlinear odd remainder. The preferred certified inverse uses a nearest sup-norm feasible projection implemented as a finite linear program. Its possible factor-two distance increase is included rather than assuming a nonexpansive projection. Under the supplied contraction certificate, response accuracy `delta=lambda_* eta/32` and logarithmically many iterations acquire coefficient accuracy eta, with diagonal-normalization, LP and arithmetic errors allocated. The inverse corrects the full response; it does not discard cubic terms as zero.

A rooted **connected-set**, cached Möbius forward compiler supplies the response without an exponentially large full-source density matrix or quasipolynomial word enumeration. Fixed k, candidate degree and local/access ratios govern its polynomial bounds; weak coupling, low efficiency and poor conditioning retain their costs. Finite truncation, local support and numerical precision are specified in the proof. The displayed implementation uses floating exponential actions as a diagnostic, not the theorem's certified arithmetic backend.

The source can start arbitrarily, including with an inaccessible reference. Paid passive forgetting before retained blocks controls the conditional mean bias; martingale concentration handles prior records. One shared front/back acquisition record informs all candidate coefficients, with simultaneous-confidence and `O(M)` product-processing costs rather than a free independent run for each coefficient. Calibrated optical loss can be nonzero during this **classical learning** operation.

## Exposure comparison and full physical bill

For admitted hard coefficients `+-2eta`, with `2eta<=J` and `eta<=r/8`, the supplied lower bound gives exposure of order `(r/eta^2)log(n/confidence_failure)` even to a more generous receiver with all fields, final source and initial purifiers. The match concerns coefficient precision and simultaneous learning at fixed local/access ratios, up to stated logs/constants. It is not an optimality theorem for all weak-port/loss factors, runtime, detector arrays, timestamp service or total hardware.

The [finite interface](finite-photon-count-interface.md) pays local-oscillator photons, port routing, counter range, source discard/burn-in, fixed detector deadtime, phase/gain/loss calibration and growing timestamp precision. More detector rails mitigate busy-time loss but do not remove a fixed timing-jitter floor. No fixed aggregate hard optical passband, fixed complete hardware at arbitrary accuracy or microscopic finite-band Markov realization is established.

This learner can replace calibration inside the preserved [correlated-calibration first-input recovery theorem](../2026-11-05-p3-deferred-calibration/README.md). It does **not** replace its coherent archive, lossless initial ingress, protected waiting through calibration and computation, or accepted recovery margin. The earlier no-burn-in neighborhood construction stays separate. No full pipeline becomes practical merely because calibration uses classical records.

## Recorded computation and its limits

Two million raw event-driven blocks were simulated for **each** of two finite-oscillator settings on one two-qubit Hamiltonian with collection efficiency `.6`. The stronger setting used 29,992,217 source-plus-LO events and maximum coefficient error `.0307006`; the matched setting used 9,596,361 events and error `.0594418`. Both are retained: [stronger-LO results](package/next2_root/passive_photocount_results.json), [matched results](package/next2_root/matched_photocount_results.json), [program](package/next2_root/passive_photocount_demo.py). Exact-model stationary initialization was supplied. Physical burn-in, deadtime, clock errors, dark counts, clipping and spectral detector response were not simulated.

The floating regression inverse reached `3.0631e-11` after eight iterations at useful `w=.25`, **outside** the conservative uniform inverse certificate. Sampled iterations omit the feasible-set projection. They exercise response correction, not the complete certified theorem.

The [connected-set diagnostic](package/next2_continuous_quantum/connected_set_demo.json) ran one three-qubit five-term case at cutoff three. Two responses differed from a separate density-matrix calculation by `7.33e-8` and `1.37e-7`, below loose analytic tails `.0548` and `.00863`, using 26/20 rooted sets and 196 sparse exponential actions. This is limited floating-point evidence, not a generic certified compiler execution.

At the preceding coefficient target `1.4526409921e-5`, the [different certified resource allocation](package/next2_root/passive_resource_bounds.json) uses `w=.006`, matched `mu=.0036`, response accuracy about `4.92445e-9`, counter cap nine and approximately `10^26.1731` shared raw blocks, or `10^27.2162` model time units before extra service. Its improvement over the old `10^39.12` sufficient bound compares upper allocations with different observations/access bills, not a demonstrated device speedup or a lower bound. No theorem-scale trials were executed.

The substantive [independent review](package/next2_alternatives/finite_lo_implementation_review.txt) covers the stated matched-LO, timing/deadtime and focused response/connected-set checks. Other source statuses remain historical at their checkpoints; no new blanket audit is inferred. [Source register](package/SOURCE_REGISTER.txt), [earlier 47-file preservation receipt](package/PRESERVATION_RECEIPT.json), original programs and diagnostics are retained. The [new reliability completion](reliability-curve-certificate.md) supersedes the old computational gap only by this new proof, without rewriting the old artifact as already completed. An [independent thermodynamic route remains incomplete](package/next2_alternatives/INCOMPLETE_INDEPENDENT_ROUTE.txt). Generated current retrieval is unchanged; complete proofs and scoped entries are public directly on GitHub.
