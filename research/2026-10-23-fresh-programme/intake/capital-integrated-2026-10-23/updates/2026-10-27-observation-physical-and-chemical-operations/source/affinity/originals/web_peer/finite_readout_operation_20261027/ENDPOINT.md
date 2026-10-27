# Positive finite-readout continuation: completed conditional operation

Completed27 October2026 in the same retained SolMax slot, with no descendants or physical actions. Latest Astra task-first entry was read at commit `f9558b967f5014eced96f229cf89cc4aa7f3490b`; the older query helper was not silently relabelled current. All work here stayed in this continuation folder.

The consequential replacement question is: **what minimum driving force per microscopic cycle is required by non-Gaussian observations when separate sensor responses are unknown?** The answer can remain positive even when the old rate counterfamily makes every covariance-only entropy-production-rate floor vanish.

## Finished mathematics

For stationary finite-state all-even Markov sources with bidirectional rates, the established Ohga–Ito–Kolchinsky sector bound gives `kappa<=Amax/(2pi)`. The new bridge proves that every physical spectral covariance, real observable projection and common finite-window average has canonical imaginary radius at most `kappa/sqrt(1+kappa^2)`. Appropriate real noise contracts preserve this cone.

For three measured channels with separate unknown response phases and allowed noise,

**`Amax >= pi sqrt(F(C))`**,

where F is the exact three-channel phase-minimized covariance SDP from the preceding unit. No Gaussian physical path law is required. This bounds maximum microscopic cycle affinity, not dissipation rate. Local detailed balance is additionally needed to interpret the rate-ratio affinity thermodynamically.

The finite shutter must occur **before** all unknown individual temporal responses, and their complete response or an acquired tail budget must be observed. A common gate then makes the physical finite-record covariance a positive window average **before** the unknown H factors. This is different from smoothing already filtered records, which failed in the previous unit.

`SPECTRAL_AFFINITY_THEOREM.md` contains the full source/sector/precision/cone/window/sensor proof. Root independently reconstructed the bridge and checked it exactly on a noncommuting sector example, then whole-read and accepted the stated mathematical scope. Final file:8114bytes, SHA256 `8334d1121be4d34b28492d9789daa7e4654f448ac3f5aae1bd197c776efd5e18`.

## A concrete positive photon/readout operation

The photon contract is a common passive readout shutter, nonnegative Markov-state-dependent intensity, separate fixed causal detector kernels, conditionally independent Poisson counting, deterministic repeatable dark intensity, and paid capture/initial-memory bounds. It is a model/record contract, not an acquired real detector. It tolerates non-Gaussian photon paths without requiring a full detector-noise time-reversal law. Generic correlated noise after the separate filters is not allowed.

The shutter gives an ordinary calibration control which cannot be withheld from a comparator:

`E Y_i,on - E Y_i,dark = mu_i H_i W`, with `mu_i>0`.

Thus the source's own stationary mean provides relative detector phases without known source brightness or a conjugate-force probe. Nonzero W and finite phase precision are paid. A two-channel mean-referenced covariance gives the positive floor

`Amax >= 2pi q/sqrt(1-q^2)`

with `q=|Im(C12 conj(m1)m2)|/[|m1m2|sqrt(C11C22)]`.

Two bright records per block supply an unbiased covariance through their difference; one dark record supplies the mean reference. The eight shared-data real coordinates receive a simultaneous confidence budget. Explicit Poisson dominators, predeclared whole-block clipping and exact tail-bias transport handle unbounded counts. Established empirical-Bernstein intervals use observed variances. Detector saturation is not confused with that statistical clipping.

`PHOTON_CONFIDENCE_AND_MEAN_REFERENCE.md` gives the complete conditional count, mean, covariance, timing, tail, initial, coupling and confidence proof. Root whole-read, requested an explicit deterministic-background restriction and N>=2 guard, verified those corrections, and recorded completed substantive independent mathematical acceptance in `parent/PHOTON_REVIEW.md`. Final file:14548bytes, SHA256 `25bfdb4e5ccab5499fe568491d1a5d2f77c833e2623ec7c355dfd35be49d15ba`. No remaining proof error was found at that stated scope.

## Executed resource calculation, not acquired data

`cox_acquisition_planning.py` uses the already accepted rare-active-cycle family as a declared population model. A state-resolved Feynman–Kac ODE computes photon moments through order4; an independent analytic two-pulse covariance checks it. The code generates **no random records**. Private population moments are used only for power planning, never supplied to an observed-data confidence estimator.

The common readout uses two short windows of width .01, separation .18 and analysis frequency pi/(2*.18). Maximum intensity gives20 expected photons per maximally bright open window. Exact rational Poisson tail bounds set cutoff144. Pure unknown latencies bounded by .12, unit efficiency and zero dark background are the planning response class; arbitrary attenuation can erase the positive floor.

For a displayed .05 affinity target, numerical planning yields:

| Active fraction | Statistical blocks | Bright / dark records | Source-time units | Expected signal photons |
|---|---:|---:|---:|---:|
| .5 | 1.37million | 2.74M /1.37M | 55.2million | 36.5million |
| .1 | 4.68million | 9.36M /4.68M | 200million | 25.0million |
| .01 | 44.2million | 88.3M /44.2M | 2.09billion | 23.6million |

Source mixing gaps and initial stationary preparation are charged. Dark readout may occupy an already paid sufficiently long mixing gap. The model's stat=.01, source coupling=.005 and initial preparation=.005 budgets give98% confidence under its operational promises. The separate beta=.1 event concerns the population-power calculation. Numbers in this table are **numerical power/resource diagnostics**, not outward-rounded power certificates, physical seconds, generated experimental evidence or acquired-photon confidence statements.

The point affinity floor stays positive as activity becomes rare, but acquisition does not become free. No cheap discovery-multiplier conclusion is supported by these large bills.

## Strong ordinary methods receive everything

* Ohga–Ito–Kolchinsky2023 already infer maximum cycle affinity from calibrated short-lag state-observable correlations. Their theorem is the established sector input; neither affinity inference itself nor their cycle bound is claimed new.
* Liang–Pigolotti2023, arXiv2308.14497v2, provide finite-lag bounds for positive observables in terms of a **sum of cycle affinities**. The relevant definitions/proof/application were read. This is an important adjacent operation; with an unknown number of hidden cycles, a lower bound on that sum is not a quantitative lower bound on Amax. Their visible-state/coarse-graining inputs are retained, not silently identified with arbitrary sensor-filtered photons.
* Unknown-axis circular-reflection tests and invariant polyspectra are established alternatives to the initial full-law closure idea. That candidate is preserved in `FINITE_GATE_BRIDGE.md` but is not advertised as a new statistical method.
* Ordinary mean-response calibration receives the same shutter, dark records and first moments. An ordinary implementation may use the **same empirical-Bernstein method** as our finite compiler. The worst-cap MOM illustration is more conservative and has a stronger power receipt in the present code; no matched-power speedup over it is asserted.

Historical priority for the complete spectral-cone/finite-gate/mean-reference source-affinity composition remains UNKNOWN. Familiar implementation primitives alone do not disprove a new input/output composition, and the composition alone does not prove practical advantage.

## Exact remaining limitations

The displayed conditional mathematics is finished and internally accepted. The resource code was read at its numerical-planning scope; it was not independently rerun or rigorously rounded. No real gated photon record has been run through a certified numerical inference implementation.

Still unacquired are an actual nonperturbing common shutter/readout chain; conditional linear/Poisson response with controlled dead time and saturation; initial and response-tail bounds; intensity/clock/linearity envelopes; actual stationary/independent or quantitatively mixing source preparation; and a hardware- and task-matched advantage over the strongest ordinary method. These are acquisition/usefulness obligations, not unnamed missing algebra. No more ideal generators or solver tuning are needed to finish this unit.
