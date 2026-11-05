# A certified finite improvement to rare surface-code failure estimation

## Decision obtained

For the frozen distance 21, 21-round circuit model at physical channel parameter p=0.001, with its specified integer-cost minimum-weight decoder, the precommitted 10,000-trial experiment gives

    1.6876511444865811e-12 <= block logical-failure probability
                             <= 4.18024741599281e-12

at individual 99.9% fixed-shot confidence under the ideal-independent-bit assumptions of the algorithm. The lower endpoint exceeds the unchanged 10^-12 target. The earlier path-cover experiment on the same input had been inconclusive. This rules out that modeled decoder/design against that target; it is not a hardware reliability measurement.

Independent verification replayed every trial and checked the original selected detector/L0 identities, all outcome and random-bit counters, and exact outward confidence inequalities. Python's reproducible PRNG is not ideal physical randomness; the exact-law and confidence statements are conditional mathematical guarantees.

## What changed

Instead of proposing every clean-and-faulty path, the sampler proposes only an ordered oriented tuple of faulty edges. Certified shortest-gap lower bounds replace the omitted clean routes. A positive rational supersolution normalizes all tuple lengths; exact score filters and canonical decoding restore the intended law. There is no fixed path-length cutoff or uncharged tail.

Exact normalizers on the same rounded graph laws fell by factors 6.0271453 (d13) and 8.3215834 (d21). This guarantees larger expected acceptance per trial, not automatically faster execution. The new individual trials are slower because they scan a dense vertex-distance kernel. The executed precision and sampling-time differences are stated below; complete dense preprocessing must be included separately.

## Frozen results

Distance 13 / 13 rounds:
- 20,000 trials, 1,578 accepts, seed 202611051913.
- Individual 99.9% interval [2.5595549148433986e-8,3.002621635589656e-8].
- Sampling 23.4619s; loading+sampling+confidence 25.1240 s; entire Python subprocess 27.6564 s.
- Peak  process memory 138,940 KiB; listed static arrays 3,949,864 bytes.
- 5,928,265,458 requested random bits, including background noise and rejected integer draws.

Distance 21 / 21 rounds:
- 10,000 trials, 55 accepts, seed 202611052921.
- Individual 99.9% interval [1.6876511444865811e-12,4.18024741599281e-12].
- Sampling 28.0527s; loading+sampling+confidence 28.4400 s; entire Python subprocess 30.1565 s.
- Peak  process memory 226,492 KiB; listed static arrays 33,836,136 bytes.
- 3,795,606,393 requested random bits.

Every interval includes the explicit conversion-TV error from the exact projected circuit model to the dyadic graph probabilities. Two individually 99.9% intervals have joint coverage at least 99.8% by union bound, not joint 99.9%. No optional stopping or post-count parameter adjustment occurred. All frozen sources and input arrays passed postrun hash checks.

## Matched comparison with the previous acquired operation

The same d13 path-cover implementation used 100,000 trials and 1,249 accepts, sampling 48.6885 s, for interval [2.409810660133688e-8,2.902079702096728e-8]. The tuple run used one-fifth as many trials and produced a 10% narrower interval with 48% of its sampling time. This is an executed finite comparison between two implementations, not an optimized cross-language benchmark.

The same d21 path cover used 10,000 trials and 7 accepts, sampling 16.568 s, and produced [5.591279015181958e-13,8.565926177314925e-12], straddling the target. The tuple run took 69% more sampling time for the same trial count, but reduced interval width by a factor 3.21 and decided the fixed threshold. The new dense preprocessing is more expensive and must also be charged. Saved-table loading is not complete setup.

## Complete measured costs

Fresh byte-identical copies of the producer and numerical table builder were run in an isolated directory, with process startup, imports, compilation and output included. All six resulting arrays matched the frozen data byte-for-byte; exact normalizers, conversion bounds and certificate fields also matched.

- d13: complete floating build 10.9151 s; exact producer 8.2250 s. Adding independently measured acquisition 3.1965 s and full statistical process 27.6564 s gives 49.9929 s.
- d21: complete floating build 145.2466 s; exact producer 41.8167 s. Adding acquisition 15.5405 s and the statistical process 30.1565 s gives 232.7603 s, about 3.9 minutes.

These totals are sums of separately measured full subprocess stages, not a single uninterrupted end-to-end run. The fresh preprocessing itself was timed continuously: 19.1411 s and 187.0658 s. Shared-host timings are observations, not guaranteed runtimes or a controlled comparison against a simultaneously executed baseline.

The largest d21 construction process used 607,712 KiB (593.5 MiB), versus 226,492 KiB during sampling. d13 construction's sampled aggregate process-group peak was 173,672 KiB (including Python and compiler); the sampling process used 138,940 KiB. Sampled aggregate memory is not the same as a kernel-enforced memory bound. All observed stages remained below 2 GiB and 20 minutes. The statistical runs separately obeyed their precommitted resource limits.

File-copy setup, development, independent scientific review, equivalence comparisons and hash checks are excluded from these operational stage sums and are not represented as free research. Source acquisition and operational table certification are included. See fresh_preprocessing/COMPLETE_COST_ACCOUNTING.json for every receipt and exclusion.

In particular, the d21 result does NOT establish a fresh-input speed advantage over a sufficiently longer previous path-cover run. Its new contribution is a demonstrated finite cover improvement and a verified decision at the fixed test budget; the dense setup limits the amortized benefit.

## Why this is not a general solution

THEOREM.md proves exponential loss on a simple 2m-edge repetition line: acceptance is at most (1-p)^(m+1)/(1-2p), even with unique clean routes, exact uncapped gaps, and no score aliasing. Omitting clean-edge conditions still costs an exponential factor. Dense distances and fixed gap caps are additional scaling limits.

Fault-set counting, union importance sampling, splitting and subset sampling are established prior methods. In particular Regev–Dilley–Bennink 2605.03054 already avoids minimum-path multiplicity by counting physical error configurations. Our current comparison does not establish superiority over optimized published splitting/MCMC on this same full circuit graph. See PRIOR_ART_AND_SCOPE.md and the terminal matched-comparator result below.

## Terminal matched-comparator result

The independently implemented published subregion heat-bath/BAR challenger used the same nonuniform d21 graph probabilities and fixed integer-cost decoder, with a predeclared 31-rung odds-tilt ladder, 16 chains, 2,000 burn-in and 2,000 retained steps per rung. It hit its fixed 1,200-second process cap after 13 of 31 rungs, so it produced no complete target probability or uncertainty interval. The process used 239,500 KiB peak RSS; its independent high-noise anchor was also charged. Partial traces and all sources are preserved in ../qec_fault_tuple_comparison_20261105/.

This is one executed, fixed-budget challenger, not a proof that splitting is slower or less accurate, an optimized time-to-accuracy measurement, or a result for every prior method. The subsequently canceled Zanella run was not executed. No partial ladder was extrapolated to the target and no favorable post-result schedule was substituted. Superiority over the strongest published circuit splitting/subset methods remains unresolved. The tuple result remains a verified finite cover/decision improvement over its own earlier path-cover implementation, not a general rare-event breakthrough.

## Verification and reproduction

- THEOREM.md: coverage, exact probability identity and exponential limitation.
- SAMPLER.md: actual integer categories, exact terminal/boundary shifts, certified floating-prefix acceleration and model scope.
- PRECOMMIT.md/PRECOMMIT_SHA256SUMS: fixed budgets, seeds, target and frozen implementation.
- SAMPLER_RESULTS.md: runtime details, tests and artifact map.
- production_d13_20000.json / production_d21_10000.json: exact interval fractions, all counts, bit costs and dependencies.
- Corresponding process_resources.json files: full process timing and memory.
- ../qec_fault_tuple_audit_20261105/: independent full-denominator table checks, finite exact tests, adversarial prefix checks and production replay.

This is a concrete, audited improvement for a modeled reliability decision. It does not establish arbitrary-distance efficient rare-event estimation, quantum fault-tolerance itself, or a general physical capability beyond the stated computational model.
