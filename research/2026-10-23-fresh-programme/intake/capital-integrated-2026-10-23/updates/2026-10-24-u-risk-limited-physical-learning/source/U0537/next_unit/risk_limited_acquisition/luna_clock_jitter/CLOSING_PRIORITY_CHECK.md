# Closing priority check: information before absorption

**Bounded check — 24 October 2026.** This is a focused addendum to the prior audit, not a broader survey or a physical-application claim. I used two focused primary-literature queries and followed the most relevant result to its publisher page; the publisher page returned HTTP 403, so the full paper could not be inspected here.

## Conditional theorem boundary

Under the stated model, let `J_i` indicate that attempt `i` starts while alive and let `B_i` indicate that it survives the exposure and yields an observation. Let `0≤a_i≤1`; the conditional death probability on an attempted exposure is `1−exp(−κ a_i^s)`. Write `ρ` for the probability of death by the policy's stopping time, and `C=E Σ_i J_i B_i` for the expected number of observed successful exposures. The Gaussian likelihood contribution is proportional to

`Eobs = E Σ_i J_i B_i a_i^(2r)`.

Charging only observed, surviving exposures, the pointwise inequality

`κ a^s exp(−κa^s) ≤ 1−exp(−κa^s)`

and the fact that death can occur only once imply `E Σ_i J_i B_i a_i^s ≤ ρ/κ`. Consequently, with `β=2r/s`, for `s>2r` Hölder gives

`Eobs ≤ C^(1−β) (ρ/κ)^β`.

For `s≤2r`, since `a≤1` gives `a^(2r)≤a^s`, the direct bound is `Eobs≤ρ/κ`. These are conditional consequences of the parametric Gaussian-readout and exponential-hazard assumptions. They replace an additive cumulative-dose cap with actual death probability; they do not establish either response law empirically. For constant per-attempt hazard exponent `h=κa^s`, the successful-exposure weighting has the stated sharpness factor `h/(e^h−1)`, tending to one as `h→0`.

## Closest primary overlap found

The closest result surfaced was Greenshtein and Torgersen, “Statistical information and expected number of observations for sequential experiments,” *Journal of Statistical Planning and Inference* 59(2), 1997, [DOI 10.1016/S0378-3758(96)00114-0](https://doi.org/10.1016/S0378-3758(96)00114-0). The publisher search record describes bounds connecting the information in a stopped experiment to its expected observation count. That is genuine overlap with sequential stopping and information accounting. The publisher article page was inaccessible to the browser tool (403), so I did not inspect the full derivation or claim a theorem-by-theorem comparison.

Neither of the two focused queries surfaced a primary theorem matching this particular combination: an absorbing death event, the actual probability `ρ` of that event as the budget, a nonlinear per-attempt hazard `1−e^(−κa^s)`, and KL accumulated only from surviving successful observations. This bounded non-match is not evidence of novelty. Record priority as **UNKNOWN**. Conventional sequential KL/likelihood-chain accounting plus an explicit risk or cost constraint remains the strongest control; the exponent boundary alone is standard information-per-cost reasoning, as recorded in the earlier audit.

## Scope

The theorem is an analytic result for the declared model. No experiment, parameter sweep, or physical application was run. The previous audit's imaging sources do not calibrate fixed Gaussian readout noise together with the exponential hazard law over weak amplitudes or long durations, so no device-level advantage follows.
