# Same-input assessment of the ordered-fault-tuple sampler

## Verdict

The tuple method has resolved a concrete modeled design decision. Its individual 99.9% fixed-shot interval for distance 21 and 21 rounds is [1.6876511444865811e-12, 4.18024741599281e-12], excluding the specified failure-probability target of at most 1e-12. The point estimate is 2.742784171599928e-12. This is conditional on the audited model, fixed decoder, arithmetic and ideal IID bits, not a measurement of a quantum device.

The stronger matched challenger implemented here, published subregion MCMC with warm-started splitting and BAR, did not complete its ladder within the predeclared 20-minute cap. It produced no estimate or interval at the target distribution. This establishes an incomplete finite-budget attempt, not the time that an optimized implementation needs to match the tuple result. Cross-method runtime superiority remains unestablished.

The campaign is stopped as directed. No upstream repository was executed. The additional planned Zanella production run was canceled, not executed. Earlier distance-13 code-capacity MCMC measurements are not reused as circuit comparisons.

## Exact matching contract

The input graph hash is 34da7d8ec1a79176a7e5262baa69fafa49d0742639e92a76e5ccaf249107b493. It is the selected detector basis plus original L0 marginal of the acquired Stim rotated_memory_z circuit, distance 21, 21 rounds, physical channel parameter 0.001. After exact projection there are 26,461 independent, nonuniform edge faults and 4,840 interior detectors. This is not the whole joint Pauli logical channel.

All methods use the same CircuitModel constructor, fixed integer costs 4/5, insertion order, PyMatching 2.4.0 tie behavior and logical-failure predicate. The decoder is unchanged across the comparator ladder. The target dyadic probabilities are those in the tuple parameters; the conventional comparator evaluates them in binary64. There are 23 distinct floating edge probabilities, from 0.0005333333 to 0.0051769019, with expected total fault count 41.9870. Uniform-noise binomial density formulas would be incorrect.

## Strong established comparators

- **Circuit splitting with caching:** Mayer et al., Quantum 10, 2237 (2026), already simulate circuit-level failure rates below 1e-20 and cache decoder results. Thus circuit noise and access to the teraquop regime are not new capabilities here. Their convergence conditions are heuristic rather than a finite-time coverage theorem. https://arxiv.org/html/2509.13678v4
- **Subregion MCMC:** Mullan, Weippert and Brown resample part of an error pattern to refresh background faults while changing its malignant core. This directly improves on single-bit movement and is the executed challenger here. Their paper leaves false-convergence and rigorous uncertainty control unresolved. https://arxiv.org/html/2607.27153v1
- **Locally balanced and cluster MCMC:** Haruna and Murakami improve trapping on tested codes. Their principal benchmarks concern conditional mean fault weight; full failure-rate cost is extrapolated under assumptions. The previously inspected public implementation warns that its bootstrap intervals do not include mixing bias. We implemented the mathematical single-bit kernel but did not launch its full circuit run. https://arxiv.org/html/2610.35498v1
- **Multi-seeded splitting and spectrum fitting:** Beverland et al. already cover compressed nonuniform probabilities and warm-start independent chains from high-noise failures. A useful fitted failure spectrum is not an all-weight, fixed-decoder certificate. https://arxiv.org/html/2511.15177v1
- **Independent subset and importance sampling:** Dynamical subset sampling already has explicit omitted-subset bounds and sampling uncertainty for circuit protocols. Fixed-stratum exact binomial intervals can also be combined with a union bound if all unmeasured mass is charged. IID rare-event estimation is therefore not unique to the tuple method. Its same-input efficiency was not measured here. https://arxiv.org/html/2309.12774v1
- **Fault-set counting and extrapolation:** Regev et al. is close prior for removing minimum-path multiplicity, including a measurement-error extension. ScaLER uses stratification plus extrapolation. Neither has been established here as the same all-weight weighted-graph/decoder interval. Unmatched published runtimes cannot supply a numerical speed comparison. https://arxiv.org/html/2605.03054v3 and https://arxiv.org/html/2602.04921v2

Generic rare-union importance sampling and canonical representation are old principles. The candidate contribution is the concrete cover, exact finite supersolution and practical audited instance, not the existence of an unbiased estimator.

## Executed independent baseline

We used the auxiliary product family q_i(t) = logistic(logit(q_i) + t), from t = log(8) to 0. Intermediate points need not correspond to varying the circuit's physical depolarizing parameter; they are valid nonuniform product laws with the same failure set and unchanged target endpoint.

With A(t) = sum_i log(1 - q_i + exp(t) q_i), the density ratio is

    log(P_t2(E) / P_t1(E)) = (t2 - t1) |E| - A(t2) + A(t1).

Only this explicitly chosen tilt makes total fault count sufficient for BAR. Ladder spacing was 0.8 divided by the square root of sum_i q_i(t)(1 - q_i(t)), giving 31 rungs, selected before sampling.

The independent 10,000-shot anchor gave 708 failures: estimate 0.0708, numeric 99.9% CP interval [0.0626360, 0.0796174]. Setup and sampling inside the interpreter cost 18.6001 seconds. Its first 16 failure marks provide independent conditional starts, independent of the indicator count. No tuple-generated failures were supplied to MCMC.

The fixed plan was 16 warm-started chains per rung, 2,000 burn-in steps and 2,000 retained steps. Each edge was selected for resampling with probability 1/11 and resampled at its current nonuniform q_i(t). This is the published heat-bath subregion law. The number 11 is a stated tuning heuristic from ceil(distance/2), not a proof of minimum failure weight for this weighted circuit. A bounded 16,384-entry syndrome/correction-parity cache was included. This is our independent implementation, not upstream software timing or an optimally tuned implementation.

Mathematical sanity checks exhaust all 32 patterns of a heterogeneous five-bit model. Maximum floating detailed-balance residuals were 1.39e-17 for the locally balanced kernel and 8.67e-19 for subregion resampling; exact-enumeration BAR log-ratio error was 8.44e-15. Another 300 actual distance-21 incremental syndrome, weight and failure checks matched full decoder calls. These validate implementation components, not distance-21 mixing.

## Fixed-run outcome and resources

The subregion process was killed at its declared wall-time cap:

- Full process wall time: 1,200.0526 seconds.
- CPU time: 1,197.6461 user plus 0.8658 system seconds.
- Peak RSS: 239,500 KiB; no memory cap was reached.
- Complete rungs: 13 of 31, ending at t = 1.4717679284, not the target t = 0.
- Saved completed work: 832,000 proposals and 416,000 retained fault-count observations. Exact proposal and decoder-call totals including the interrupted rung were not saved and are unavailable.
- Maximum conventional Rhat across complete rungs: 1.0280. Maximum estimated weight IAT: 176.845. Every complete rung failed our conservative requirement of retained length at least 50 times its largest estimated IAT. This screen is ours, not the paper's stopping rule, and neither statistic proves mixing.

There is no target-rate estimate or confidence interval. Full-chain Student-t/delta uncertainty analysis was planned but cannot be performed for the missing ladder. Near-threshold decoder work dominated this attempt. The published method's adaptive Rhat stopping and different tuning could cost less; our fixed-budget cap is not a lower bound on its required runtime.

Known timed stages total 1,218.6527 seconds including the anchor, or 1,234.1932 seconds if the shared graph acquisition is added. Anchor import/interpreter startup was not separately measured, so these are not complete cold-start totals. Development, validation and scientific review also lie outside operational stage timing. The process monitor sampled RSS every 25 ms; it was not a kernel memory cgroup.

## Candidate costs and limitations

The loaded tuple process cost 30.1565 seconds and peaked at 226,492 KiB. It made 10,000 proposals and 2,205 decoder calls, with 55 accepts. The 3,795,606,393 requested pseudorandom bits are not measured physical entropy.

Fresh full-process preprocessing cost 187.0633 seconds: 145.2466 seconds for floating table production and 41.8167 seconds for exact repair/certification. Adding graph acquisition of 15.5405 seconds and the loaded run gives 232.7603 seconds across separately measured stages, not one uninterrupted pipeline. Largest preprocessing RSS was 607,712 KiB. The independent full-denominator certificate/distance audit cost another 45.2891 seconds, and independent fixed-run replay another 28.1411 seconds. Additional arithmetic checks and scientific review should be accounted for separately, not silently charged to only one method.

The largely dense 4,840-by-4,840 distance matrix and shell kernels are material setup costs. A small H table alone does not describe storage. The candidate proves exponential acceptance loss on repetition lines at fixed noise, so no general polynomial scaling follows. It also requires graph geometry and minimum-cost decoder structure, unlike a general black-box failure sampler.

## What this comparison supports

The tuple construction delivered an audited, all-weight modeled decision with fixed-shot coverage that does not require MCMC mixing or spectrum extrapolation. That is a useful specification distinction from this challenger. It is not a blanket advantage over all IID importance sampling, proof that MCMC cannot solve the instance, an upstream-software speedup, or a measured time-to-matched-accuracy result.

## Artifacts

PRECOMMIT.md and STOPPING_UPDATE.md record the plan and explicit campaign stop. compare.py and check_kernels.py are independently written code. kernel_checks.json records checks. anchor.json and anchor_starts.npy preserve the independent anchor. subregion_partial.npz and subregion.log preserve all completed rungs. subregion_process_resources.json records the whole capped process. SUMMARY.json contains complete-rung diagnostics. PRODUCTION_SHA256SUMS and postrun_hashcheck.log confirm the frozen implementation remained unchanged. SHA256SUMS seals this assessment.
