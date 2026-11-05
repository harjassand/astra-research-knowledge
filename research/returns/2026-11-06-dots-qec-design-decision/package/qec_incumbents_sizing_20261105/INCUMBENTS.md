# Circuit-level surface-code incumbents and matched sizing scope

Research checked 2026-11-05. This note separates applicable methods from published unmatched numerical claims. It does not claim an exhaustive impossibility theorem or a globally fastest solver.

## Frozen task

Stim 1.16.0 `surface_code:rotated_memory_z`, d in {19,21,23}, T=d; all four noise arguments equal exact 1/1000: after_clifford_depolarization, before_round_data_depolarization, before_measure_flip_probability, after_reset_flip_probability. The fixed single-basis MWPM decoder uses quantized costs 4/5, specified insertion order, PyMatching 2.4.0 and the audited logical gauge. Need choose the smallest admitted distance with block failure at most 1e-12, simultaneous 99.9% confidence, without assuming monotonicity. This is a stochastic Pauli circuit model including noisy preparation/readout, not measured quantum hardware or the whole joint Pauli logical channel.

## Principal applicable incumbent families

### Circuit splitting with cached decoder calls

[Mayer et al., Quantum 10,2237 (2026)](https://arxiv.org/html/2509.13678v4), extends Bravyi–Vargo/Bennett splitting to gate-fault categorical states. It reports modeled errors below 1e-20, uses a 10-million-event cache, and an Intel Xeon server with 96 CPUs at 2.7 GHz and 384 GB RAM. Its experiment is NOT the frozen Stim memory experiment: it uses 2d noisy rounds and corrections in only the first d. Setup includes independent Monte Carlo at the initial noise rate; published cumulative-runtime figures explicitly separate/include it. Convergence/confidence remain open in §6.1.1. No directly executable public code/data link was found in the inspected article. The printed very-low probabilities are not matched sizing certificates.

### Subregion MCMC with warm starts

[Mullan, Weippert and Brown (2026)](https://arxiv.org/html/2607.27153v1) resamples random subsets, refreshing benign background faults as well as a failure core. It uses QVM and 50 independently seeded chains, discards the first half and terminates around Rhat≤1.05. Reported 2–10× decoder-count gains versus one-bit MCMC are for bit-flip circuit noise, not equal-coverage time on this target. Full Pauli-circuit results are separate. Rhat and sampling standard errors do not exclude false convergence or mixing bias. Public executable QVM source was not supplied in the article inspected. The independent matched implementation here uses the published law, not vendor software timing.

### Improved locally balanced/cluster splitting

[Haruna and Murakami (2026)](https://arxiv.org/html/2610.35498v1) improve trapping using locally balanced flips and weight-preserving exchange. Their core benchmark is mean failing-pattern weight under code-capacity bit flips; full logical-error cost is inferred under assumptions. Circuit-level support is not established by those benchmarks. Public [mcmc4qec](https://github.com/junichiharuna/mcmc4qec), pinned in the earlier local comparison to v0.1.0.dev6, commit f6726d0628c84ed7ec837bfa6ac4907981671cfd, was read but never executed. Its interval warnings explicitly exclude mixing bias. The earlier d13 code-capacity run must not be counted as a circuit-level comparison.

### Multi-seeded splitting and failure-spectrum fitting

[Beverland et al., Fail fast (2025)](https://arxiv.org/html/2511.15177v1) combines a failure-spectrum ansatz, low-weight failure counting and multiple high-noise failure seeds carried down a ladder. The framework handles nonuniform fault probabilities. Ansatz agreement and low-weight information are useful cross-checks, but do not certify the omitted all-weight failure mass for an arbitrary fixed decoder. A code distance alone must not be substituted for the circuit/decoder onset weight.

### IID subset/stratified sampling

[Heußen et al., PRR 6,013177 (2024)](https://arxiv.org/html/2309.12774v1), with public Apache-2.0 [qsample](https://github.com/dpwinter/qsample), supplies circuit/protocol subset sampling, explicit omitted-subset mass and sampling-uncertainty propagation. This is prior art against any claim that independent conditional sampling and explicit omitted mass are new. No matched d19/21/23, 4/5-decoder result was found. The paper's ordinary propagated uncertainty bars are not automatically an exact finite-sample familywise 99.9% guarantee; one can separately use conservative per-stratum exact/bounded intervals with a union bound when fixed allocation and all missing mass are accounted for.

### ScaLER original fitted method and newer confidence controller

The [ScaLER paper](https://arxiv.org/html/2602.04921v2) reports d17 at p=.0005 with estimate 1.51e-11 in 7200 seconds on an i9-13900F (24 cores/32 threads), 32 GB desktop. Its original uniform independent single-qubit depolarizing model, S-curve extrapolation and five-run standard deviation are not this circuit/noise/decoder/coverage task. The paper also documents substantial fit errors on smaller accessible cases. These numbers cannot be used as a matched runtime.

The newer MIT-licensed [ScaLERQEC development code](https://github.com/yezhuoyang/ScaLERQEC/tree/0babdb7a7171009e8079f68f80ae9ae8eb4c259b) does supply general linear Pauli noise, independent full-support uniformization, a fixed polynomial estimator, and sequential finite-grid KL/empirical-Bernstein bounds without fitting or MCMC. Its pinned [validation report](https://github.com/yezhuoyang/ScaLERQEC/blob/0babdb7a7171009e8079f68f80ae9ae8eb4c259b/experiment_results/uniformized_final_validation/results.md) explicitly says low-p d13 remains uncertified. The public d13 Z, T=13 nonuniform case took 36.386s compilation plus 60.203s profile for 162,303 shots (123.505s reported total), and returned [0,3.44905e-4] at p=.001. Its minuscule point estimate was not considered reliable. This is stronger relevant finite-confidence prior art, but still not the matched task. Sources and result JSON are retained as inert text.

For the pinned uniformized controller alone, `BERNSTEIN_BUDGET_FLOOR.md` proves a necessary shot floor of 10.0858 trillion times the number of proposal components to ever return U≤1e-12 with per-design alpha=.001/3. The independent audit confirmed the mathematical derivation. This does not apply to its conditional-stratified variant or other structure-aware importance samplers.

### Exact small-code enumeration/transform

The public [certify Part K](https://github.com/05oz/certify#part-k--the-exact-logical-error-probability-v0110) reports exact rational probabilities for d3/d5, one-round independent DEM noise and a lookup/coset-leader decoder, using a syndrome-space Walsh transform. This is exact-computation prior art, not a scalable d19–23, T=d MWPM result. Claims were read, not independently replayed; no source was executed. Similarly [Regev et al.](https://arxiv.org/html/2605.03054v3) give closed-form approximations and remove path-overcounting in their specified regimes, not the present all-weight fixed-decoder certificate.

## Recovered matched baseline and fresh attempt

The existing qec_fault_tuple_comparison_20261105 run used this d21 graph, 23 nonuniform edge probabilities and unchanged decoder. It stopped at its declared 1,200s cap after 13/31 subregion rungs, giving no target estimate. Its known stages sum to 1,234.1932s with graph acquisition, excluding some startup/review. It is not a time-to-matched-accuracy measurement or proof MCMC cannot solve the instance.

A fresh optimized subregion attempt ran under `OPTIMIZED_PRECOMMIT.md`. It uses sparse Bernoulli envelope sampling, packed incremental syndromes, parity-only decoder output, and batches independent chains. Random output-equivalence tests covered 4,000 patterns; fresh component tests cover packed syndrome updates and a small-space sparse-Bernoulli distribution. The exact small-kernel detailed-balance/BAR checks from the prior comparison still apply to the unchanged mathematical proposal.

No claim of benchmark victory is made before a full endpoint result, diagnostics and complete cost reconciliation. A conventional nominal interval remains distinct from guaranteed familywise coverage. See `d21_optimized_result.json` and the completed-result section below.

## Scope of an eventual comparison

Appropriate supported distinction: a specific geometry-aware method can meet a finite-confidence modeled sizing decision with audited arithmetic where the measured conventional attempt has not met that same specification.

Unsupported: new access to the teraquop regime; new existence of IID rare-event estimation; quantum hardware fidelity or engineering readiness; globally optimal code size; speedup against all prior art; nominal MCMC interval relabeled as a mixing-free certificate; code-capacity numbers reused as circuit results; per-round and per-block rates interchanged; differences of decoder or noise model hidden.

## Completed fresh conventional endpoint (2026-11-05)

All 31 rungs completed, without the cooperative cap binding. The d21 BAR point is **3.0739900352e-12**. Its nominal 99.9% Student-t/delta interval is [1.3378651823e-12,7.0630545300e-12]; adjusting the nominal per-design budget to .001/3 gives [1.1963154872e-12,7.8987648638e-12]. These diagnostic intervals agree with the audited tuple rejection, but neither is a finite-time coverage certificate: every rung fails the predeclared conservative retained-length≥50×largest-IAT screen. Maximum ordinary Rhat is 1.04438 and maximum estimated IAT 235.19. Rhat below 1.05 alone is not enough. Forward-only ratio estimation gives 3.10400e-12; backward-only gives 2.59809e-12, a useful sensitivity check, not independent validation.

The run used 1,488,000 MCMC proposals and 1,508,373 total decoder calls (including the 20,000-shot anchor and 384 additional start trials). Recorded model loading, anchor, starts, rungs and trace saves totaled 920.9314 s. This includes 0.2518 s model setup, 18.9014 s anchor/start acquisition and 899.6241 s in rung loops. It excludes interpreter/import startup and the final BAR-histogram analysis, because the frozen program recorded its timer immediately before that analysis. Thus it is not a complete cold-process time-to-accuracy. The stored 175,420 KiB RSS is also captured before the final histogram analysis and is not whole-process peak. Fresh separate summary postprocessing took 0.0598 s inside the interpreter and 94,944 KiB peak. Prior graph acquisition, development, mathematical checks and optimization validation are separate costs, not silently free.

The frozen source and precommit hashes still match. A final independent state replay confirms all 16 terminal states fail under the original full-correction decoder, and all terminal weights match saved traces. Probability inputs use conventional binary64 arithmetic: the actual terminal expit/logit values have product-law TV distance at most 9.022e-15 from the exact 64-bit dyadic endpoint. This small numerical bound does not cover MCMC bias or finite-state pseudorandomness. It is retained in `binary64_endpoint_bias.json`.

This completed attempt replaces the earlier blanket statement that no conventional target estimate was obtained in the current pilot. It does not alter the archival 20-minute incomplete run, establish matching finite-confidence precision, or prove a speedup of either approach. The completed result and all rung diagnostics are in `SUMMARY.json` and `d21_optimized_result.json`; all retained traces are in `d21_optimized_partial.npz` (the historical filename is retained although complete).
