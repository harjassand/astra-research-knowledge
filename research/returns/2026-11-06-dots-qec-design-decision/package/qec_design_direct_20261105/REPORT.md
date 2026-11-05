# Executed surface-code design decision

## Result

For the predefined set **{19,21,23}**, choose **distance 23** for the specified rotated-memory-Z model and fixed decoder. This is the smallest passing member of that set, not a smallest-over-all-designs claim.

The target is a logical failure probability at most **10^-12 per d-round block**. Joint coverage is at least **99.9%**, conditional on the model, the exact-law sampler/decoder contract and ideal independent random bits.

| Distance | Rounds | Decision | Probability enclosure | Evidence |
|---:|---:|---|---|---|
| 19 | 19 | Reject | [2.19360e-12, 1.03749e-10] | Fresh anytime-valid run, 8/750 accepts |
| 21 | 21 | Reject | [1.60992e-12, 4.32578e-12] | Archived fixed-shot run, 55/10000 accepts; confidence recomputed |
| 23 | 23 | Pass | [6.46021e-15, 9.60582e-13] | Fresh anytime-valid run, 6/3000 accepts |

The d19 and d23 intervals are deliberately decision-oriented and wide. They do not offer a precise rare-event point estimate. All inspected batches and the exact rational endpoints are retained. The d23 upper endpoint includes 5.03684e-16 of circuit-conversion and edge-rounding TV error, so numerical bias is not silently smaller than the design margin.

## Completed operation

1. Freeze circuit family, target, candidate set, decoder and total error budget.
2. Acquire each new circuit's exact selected detector/logical marginal using the supplied symbolic Pauli projection, rather than interpreting printed DEM decimals as exact probabilities.
3. Construct the acquired ordered-fault proposal; verify its finite rational supersolution with exact integer arithmetic.
4. Sample its IID acceptance indicator and use an exact outward mixture-martingale confidence sequence. This supports valid early stopping, including every inspected batch.
5. Expand by the explicit model-conversion bound and assess all candidates without assuming monotonicity.

The fixed error allocation is 1/3000 per candidate. For d21 only, recompute exact fixed-shot Clopper-Pearson using the one archived precommitted 10,000-shot sample. That previous result was known at precommit; it is not presented as a new independent experiment. The two fresh sequences use independent predetermined PRNG seeds and their predetermined stopping rule. See PRECOMMIT.md and THEOREM.md.

## True physical scope

All four generated-circuit channel parameters are exactly 1/1000: after-Clifford depolarization, before-round data depolarization, measurement flips and reset flips. Locations are independent stochastic channels. Symbolic projection may have irrational independent factor probabilities; these are enclosed before exact dyadic rounding. The specified decoder uses the acquired costs {4,5}, fixed graph order and PyMatching tie behavior.

This certifies the original memory-Z observable decoded from one syndrome family, including initialization and final readout. It does not certify an arbitrary-state quantum memory, a full correlated logical Pauli channel, a per-cycle rate, or device reliability. Hardware calibration uncertainty, leakage, coherent errors, crosstalk and time-correlated drift are absent from the model. The executable's deterministic PRNG is reproducible; the theorem assumes ideal IID random bits.

Distance 23 uses **529 data qubits and 1,057 total used qubits**, 23 rounds, 46,552 CNOTs, 12,144 H gates, 12,144 ancilla measurement-reset operations, 529 final data measurements and 1,057 initial resets. Its nominal qubit-round volume is 24,311, excluding the initialization/readout timing. No gate-time assumptions were supplied. The comparable total qubit counts for d19/d21 are 721/881. All counts came from the actual flattened circuits and an independent audit.

## Complete measured cost

Fresh per-distance pipelines include acquisition, numerical table construction, C++ compilation and exact certification, imports, sequential sampling, confidence arithmetic and output:

| Stage | d19 seconds | d23 seconds |
|---|---:|---:|
| Acquisition | 8.5685 | 28.6242 |
| Floating proposal build | 61.9092 | 166.9730 |
| Exact table producer/certificate | 26.1547 | 62.8568 |
| Statistical subprocess | 3.2416 | 12.3923 |
| **Continuous complete pipeline** | **99.8868** | **270.8595** |

The two jobs ran concurrently on a shared host. Adding their pipeline walls gives 370.7451 s of per-job wall time, not elapsed latency or CPU time. The largest observed per-stage process-tree RSS was **865,996,800 bytes (825.88 MiB)** in the d23 floating build. The memory monitor was sampled, not a kernel-enforced bound. Both completed within their precommitted 30-minute/2-GiB individual caps.

The inherited d21 evidence cost 232.7603 s as a sum of separately measured complete stages in its original acquisition, build and fixed-shot operation. Adding this historical cost and the fresh pipelines gives about **603.51 s**, plus the small recorded confidence-recomputation cost. That sum is not one fresh uninterrupted end-to-end benchmark. Cached-table lookup is not represented as free setup. Research/development, independent review, checksum verification and packaging are excluded from operational timings and explicitly disclosed. The exact receipts and cost conventions are in DECISION.json and the pipeline resource files.

Sampling is only a small portion of full cost; the new decision wrapper does not solve the dense-construction scaling problem. The inherited tuple method's exponential acceptance obstruction also remains.

## Strongest alternative and limits

The operation is an application of existing exact circuit acquisition, ordered-fault rare-event sampling, and standard confidence sequences. It makes **no novelty claim for sequential reliability profiling**, including versus ScaLERQEC, and no claim that extremely small logical probabilities are newly accessible.

The strongest relevant incumbents are certified IID/fault-subset profiling where applicable and optimized circuit-level splitting/MCMC, particularly Mayer et al., *Rare Event Simulation of Quantum Error-Correcting Circuits*, Quantum 10, 2237 (2026), arXiv:2509.13678. The inherited same-d21 heat-bath/BAR challenger did not finish its 31-rung ladder within 1,200 s, but that single fixed-budget run is not a tuned time-to-accuracy comparison. **Runtime superiority over an optimized matched incumbent remains unestablished.**

The demonstrated capability is narrower and concrete: an auditable, finite-confidence design decision at the fixed 10^-12 target, with exact numerical error accounting and measured full operation cost. It is not a general efficient surface-code estimator or a hardware-reliability breakthrough.

Sources: supplied surface_code_rare_failure_release_20261105.zip and qec_fault_tuple_20261105; https://arxiv.org/abs/2509.13678 ; https://doi.org/10.22331/q-2026-10-15-2237 ; https://arxiv.org/abs/1308.6270 .

## Independent verification and broader selection

Independent review passed every new d19/d23 table row and distance-potential inequality, each original circuit-channel projection, all inspected confidence-sequence endpoints, and complete deterministic replay including original syndrome/L0 checks on every decode. The d23 review checked 442,368 table rows and 2,569,273,344 gap terms. These reviews do not remove the declared minimum-weight-library and ideal-randomness assumptions.

The 99.9% claim concerns this fixed three-candidate constructor family. Selecting among additional constructor families or historical experiments needs further error allocation. MULTIPLICITY_ADDENDUM.json separately evaluates the unchanged traces at alpha=1/6000 per candidate (total error<=.0005): d23 still passes with upper9.88298e-13. At alpha=1/9000, d23 is inconclusive. Original preregistration, sources and result files are unchanged.

## Latest completed matched challenger

A fresh subregion/BAR implementation subsequently completed all31 d21 rungs: point3.07399e-12, nominal99.9% diagnostic[1.33787e-12,7.06305e-12], recorded main stages920.9314s plus separately timed0.0598s postprocessing. All31 IAT screens remained unresolved. Its intervals exclude mixing and numerical bias and have no guaranteed coverage. Interpreter/import and other stated costs are omitted; no matched-accuracy or speed superiority follows. This terminal run is distinct from the historical partial timeout discussed above. See MATCHED_CHALLENGER_ADDENDUM.md and the included qec_incumbents_sizing_20261105 source/receipts.
