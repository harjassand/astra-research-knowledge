# From ordinary frame calibration to validated encoded preservation

28 October 2026. **Author result; independent full-pipeline audit pending.**

The frozen two-pipeline experiment completed without retries or discarded banks. Both actual learned receivers passed the predeclared logical entanglement-fidelity target **F_e >= 0.999**. The selected receiver used **4,096 calibration transmissions per physical site**, not an exact supplied frame. This is a small, complete acquisition-to-protection software instance, rather than a uniform inverse-error estimate.

| Calibration shots/site | Fresh logical failures / 131,072 | Fixed acceptance threshold | Post hoc exact logical infidelity |
|---|---:|---:|---:|
| 4,096 (selected) | 44 | <=52 | 0.0005180078319230905 |
| 16,384 | 48 | <=52 | 0.0004084269816334440 |

The exact-channel scores are diagnostics unavailable to the learner and are not the certificate. The certificate uses actual independent randomized six-state input/readout records after the receiver is frozen. The nominal failure probability is `(2/3)(1-F_e)`. Exact integer binomial tests, selection among both receivers, and all ten unencoded comparisons are protected by a twelve-test allocation of `3/5000`, plus sampling-record total variation `249/1099511627776` (about 2.27e-10). This is below the declared overall allowance 0.001. It is simultaneous frequentist coverage, not posterior certainty about these accepted records.

All five unencoded SAME-learned-inverse receivers in each bank separately confirmed **F_e <= 0.997**. Their failure counts were `[238,250,283,367,448]` and `[202,287,271,301,330]`, each out of 65,536; the predeclared threshold was >=179. This comparison does not upper-bound arbitrary unencoded CPTP recovery or compare equal transmission rates: one encoded qubit uses five physical channels and trusted encoding/recovery resources. The equally informed conventional procedure—ordinary Bloch-response fitting, polar frame calibration and the standard five-qubit code—is exactly this pipeline. No new code, optimizer advantage or conventional-method separation is claimed.

## What was actually acquired and executed

Five stationary independent physical channels apply unknown-axis amplitude damping (rates about 0.00995–0.01550) followed by unknown fixed rotations. The learner receives only six-state input/random-Pauli output counts, forms the response matrix, extracts a proper polar rotation and rounds stereographic coordinates to an exactly rational SU(2) receiver. It never receives source frames, damping axes or rates. The generator knows those quantities solely to implement exact Born probabilities and later score diagnostics.

The actual standard [[5,1,3]] encoder, all five local noise channels and learned inverses, and the actual sixteen-syndrome decoder define the logical channel. Exact rational Pauli-transfer polynomials retain nonunital, coherent and non-Pauli terms. An independent direct 32-dimensional channel implementation agrees to below 5e-16 in this run. No Pauli approximation is substituted. The ideal exact-frame code infidelity is 0.0003839814889742225; that is only a post hoc source-informed benchmark.

Input setting and final outcome draws are individually generated and retained as sufficient counts with fixed seeds/CDFs for full replay. Physical damping trajectories and syndrome outcomes are analytically summed; they are not individually sampled. All data are simulated, not acquired from hardware.

## Complete executed cost

- Calibration: 102,400 physical noisy transmissions across both banks and all five sites.
- Coded holdout: 262,144 logical blocks, hence 1,310,720 physical noisy transmissions.
- Unencoded holdout: 655,360 physical noisy transmissions.
- **Total: 2,068,480 physical noisy exposures; 1,019,904 individually drawn setting/readout blocks and final binary readouts.**
- 262,144 trusted code encodings and recoveries; 1,310,720 encoded and 655,360 unencoded local inverse calls.
- 1,048,576 clean zero ancilla preparations and the same number of discarded syndrome qubits across coded holdouts.

This is the full executed two-pipeline ledger, not a claim that only the selected bank was paid. Per future logical transmission the nominal interface still requires five physical transmissions, four clean encoding ancillas, five local inverse unitaries, and known recovery/disposal. Actual control compilation, timing, reset, SPAM and control noise are unqualified; a nonzero implementation error budget must be established separately.

## Scientific scope and remaining obligation

The result closes a narrow acquisition-to-protection gap: a uniform inverse certificate need not be small before a known code protects the actual learned channel, and the complete receiver can be validated directly with an independent logical holdout. Here modest frame calibration followed by a standard code passes a high-fidelity target. It does not establish broad unknown-noise discovery, scalable calibration, nonstationary/memory robustness or superior adaptive decoding. It also does not demonstrate positive unassisted quantum capacity, a fault-tolerance threshold, or hardware operation. Trusted stationary CPTP testing is load-bearing; uncalibrated preparation/readout can invalidate the conclusion.

Earlier operator-block/convex acquisition and native-oracle-regret results remain separate. This small stationary product-channel instance does not upgrade their failed uniform-inverse guards or transfer their guarantees to unseen arbitrary channels. Nothing here supersedes those results.

## Reproduction and provenance

`FROZEN_PROTOCOL_HASHES.json` binds the protocol, source utilities and driver before the draws. `PREDECLARATION.json` fixes budgets, seeds, thresholds and selection. `raw_counts.npz`, `models.npz`, `sampling_cdfs.json`, `exact_channels_N4096.json`, `exact_channels_N16384.json`, `threshold_certificates.json` and `results.json` retain the evidence. `run_pipeline.py` refuses to redraw over existing counts; reproduce in a separate empty output directory rather than overwriting evidence. `code_and_channels.py` cites and hashes the governing five-qubit construction. `independent_code_check.*` checks its exact encoding/recovery algebra; the full sampled audit remains separately identified.
