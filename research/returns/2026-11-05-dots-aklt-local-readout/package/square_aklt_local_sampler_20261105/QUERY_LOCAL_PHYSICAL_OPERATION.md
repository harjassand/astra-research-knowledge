# A query-local AKLT prediction with no equilibration or finite-box cutoff

## Acquired operation

The open-path physical readout is now joined to a query-local perfect sampler. Instead of constructing a full stationary loop configuration over an entire physical box, it explores precisely the marked ancestors needed to determine the loops touching one proposed source path. It can operate directly on Z².

This changes the task from repeatedly sampling the whole system to answering a specified local physical question. The sampler, local birth primitive, exact event-time ordering and physical source insertion have separate implementation and mathematical audits. No truncation radius, maximum path length, ancestor-depth cutoff, floating-time ordering or burn-in is introduced.

The end task is the equal-time nearest-neighbor spin dot product in the thermodynamic limit of expanding open spin-2 AKLT regions with virtual-identity boundary mixtures. The output is a bounded unbiased random variable and an outward rational confidence interval. A separate theorem in `THERMODYNAMIC_PAIR_JOIN.md` identifies this precise limit. It does not claim arbitrary-boundary/full-state uniqueness, a spectral gap, quantum-state preparation or dynamical response.

## Decisive computational steps

1. Acquire an all-length rational path proposal with output probability a_p/C. For nearest neighbors, C=301805115576299/500964985405440.
2. For a finite vertex query K, acquire the exact birth measure of every closed routed loop meeting K. Rate is (3/2)Lambda0|K|; the rooted proposal is corrected by the reciprocal number of cyclic visits to K. Every4×4 loop type is checked exactly against the actual oracle probabilities.
3. Explore the residual marked Poisson field consistently. Previously revealed cylinders and pair marks are reused, while new candidates are thinned by all earlier revealed-region exclusions. The exposure proof and full implementation audits belong to the local sampler constructor and independent reviewers.
4. Order all event times exactly using symbolic sums of independent exponential atoms with refining rational logarithm bounds.
5. Return9(-1)^parity C times the exact path-loop suppression product. A null path costs no loop query. Each attempt uses a fresh independent local process.

The physical identity and path proposal are unchanged from `../square_aklt_observable_join_20261105/PHYSICAL_OBSERVABLE_OPERATION.md`. Only the amount of stationary loop information acquired per query changes. All loops outside the path query are irrelevant to the readout once the complete necessary ancestor clan has been resolved.

## Actual end-to-end measurements

All runs include path generation, null paths, rejected local birth proposals, exact time comparisons, ancestor exploration/cleaning and rational readout. Table setup is charged separately. Shared-host load varies.

| Physical target | Attempts | Independent local queries | Setup | Full elapsed | Estimate |95% outward halfwidth |
|---|---:|---:|---:|---:|---:|---:|
|3×3 center→neighbor |10,000 |7,108 |0.099s |0.978s |-3.412060 |0.073636640719 |
|32×32 center→neighbor |10,000 |8,563 |0.116s |12.361s |-3.578595 |0.073636640719 |
|256×256 center→neighbor |10,000 |8,565 |0.125s |13.679s |-3.570723 |0.073636640719 |
|Z² thermodynamic pair limit |10,000 |8,565 |0.107s |11.228s |-3.570723 |0.073636640719 |

The 256×256 and Z² runs happened to agree pathwise for their shared seed, including all recorded work counts. That is a coupling diagnostic, not a proof that the finite and infinite correlations are identical. The theoretical limit is proved separately without relying on this observation.

The 3×3 exact physical answer is -22071/6395≈-3.451290 and is inside the reported interval. Its empirical variance 6.5138 agrees with independently enumerated exact variance 6.4633.

In the infinite 10,000-attempt run, each non-null path query used on average:

- 1.468 dominating seed proposals and 2.583 parent proposals;
- 2.538 exact event-time comparisons;
- 1.053 retained ancestor cylinders and 6.655 retained loop edges.

The largest observed clan contained 28 cylinders; the largest observed loop had 56 edges. These observed maxima are not algorithmic cutoffs.

The former whole-box 32×32 physical run took 42.21 s for 512 attempts. Its per-attempt cost was about 67 times the new 32×32 cost on these runs. This comparison is ONLY against our earlier full-box exact implementation. It is not a speed comparison with established worm or AKLT Monte Carlo.

## Fixed-confidence high-precision run

The exact radius formula requires 542236 independent attempts for nearest-neighbor additive error 0.01 with failure probability at most 1/20. Its outward rational radius is

    4999997629 / 500000000000 = 0.009999995258.

The actual fixed-budget run is complete. With fresh seed 2026110501 and 542236 attempts, the nearest-neighbor thermodynamic spin dot product estimate is

    -3.559889191,

with the outward 95% confidence interval

    [-3.569889186, -3.549889195].

The exact rational interval and mean are preserved in `physical_local_infinite_precision001.json`; the displayed endpoints are rounded outward. The displayed nine-decimal point estimate plus/minus 0.01 also contains the exact rational interval.

The run used 463946 independent local queries. Actual compute time was 722.901041 seconds plus 0.105724 seconds initialization, totaling 723.006765 seconds, or 12 minutes 3 seconds. Components include 20.447801 seconds of path generation, 693.165422 seconds in local loop sampling, and 9.287818 seconds of remaining readout/accumulation work. It generated 687693 seed proposals and 1223355 parent proposals, including null outcomes, performed 1160591 exact time comparisons, and retained 490116 clan cylinders. The largest observed clan contained 35 cylinders, and the largest observed loop had 104 edges. There was no restart, finite cutoff, optional stopping, or omitted burn-in.

The budget was fixed from the deterministic range bound before sampling, not selected by looking at sample means. All pilot runs remain separate and preserved. `production_manifest.json` records the seed, precommitted budget and frozen code/table hashes; all hashes remained unchanged. `production_progress.json` records progress counters without using intermediate means for stopping. `production_summary.json` provides final wall time and outward decimal display.

A rare route was low in two earlier small-box diagnostics. That discrepancy was retained, not silently discarded. Independent geometric-exposure and raw-birth comparisons found no defect. A fresh pre-registered main-engine test then observed 770 outcomes against 781.861 expected in 2 million draws, two-sided exact binomial p=.693942. Nonrejection is a diagnostic, not the correctness proof. Final implementation signoff combines the mathematical exposure/code audit, exact local-oracle/time tests, physical-state checks and these independent empirical screens. The production run began provisionally while the targeted diagnostic was running; its fixed budget and code were not changed afterward.

## What is and is not established about cost

The query engine does not scan, store or equilibrate the full physical area. Its cylinders, spatial routes and exact arithmetic are generated on demand, and it is also defined with no finite physical box at all. Independent resource proofs now establish qualitative finite expected arithmetic work for each fixed finite query K, including adaptive exact-time comparisons and Poisson generation. Section 7 of the independent lazy-time proof also averages this bound over the geometric source-path tail, proving finite expected arithmetic for the full physical attempt. This is stronger than almost-sure termination alone. It does not supply a useful small bit-cost constant, a linear-in-|K| arithmetic theorem, or a deterministic wall-time guarantee.

The sharper certified mean bounds are fewer than 14.120548 local birth proposals per query vertex, fewer than 171.505 attempted loop-walk steps per query vertex, and fewer than 97 local birth proposals per full nearest-neighbor physical attempt. They count rejected proposals. See `LOCAL_SAMPLING_THEOREM.md`, `oracle_work_sharp_certificate.json`, and the independent `LOCAL_RESOURCE_PROOF.md` / `LAZY_TIME_COST_PROOF.md` audit documents. The measured 723-second run includes all actual costs rather than substituting these combinatorial bounds for arithmetic timing.

The same rare-event warning remains for distant tiny correlations. A fixed 16×16 torus proposal majorant has a long-distance alias floor, and additive accuracy is not relative accuracy. The all-endpoint equal-time correlation sum has a large proposal constant 65.8844 and is not automatically an efficient precision operation.

## Strongest incumbent and novelty boundary

The 2013 Silva–Schakel–Vasconcelos crossing O(N) worm algorithm treats the same routed loop gas and includes correlation observables. The 2016 Wierschem–Beach AKLT valence-bond loop work already computes physical observables. Martyn–Kato–Lucia studies the square-AKLT boundary loop representation. Thus neither a classical AKLT loop mapping nor physical spin readout is new by itself.

The candidate differentiator here is acquired exact local sampling at this parameter point, with independent infinite-volume readouts and finite-sample confidence free of an unquantified mixing or finite-box bias. The targeted primary-source check found no same-point rigorous iid infinite-volume confidence guarantee, but that search is not a proof of priority. [Silva–Schakel–Vasconcelos2013, pp3–4](https://arxiv.org/pdf/1306.4996) uses a periodic finite-lattice Metropolis worm for the same gas at N=3,K=1 and measures correlations using open endpoints; its numerical study is N≤2, not a certified error theorem at our parameter point. [Wierschem–Beach2016](https://arxiv.org/abs/1603.03444) explicitly qualifies exactness as asymptotic Monte Carlo exactness. [Fernandez–Ferrari–Garcia2002](https://arxiv.org/abs/math/9911162) already supplies generic exact finite-window infinite-volume ancestor sampling. Thus this is an executable, parameter-certified application with physical readout, not invention of the sampling framework and not an established QMC speed record.

Mathematical exactness and interval coverage use an ideal independent-fair-bit model. Python PRNG seeds make these runs reproducible numerical diagnostics, not physical-randomness certificates. All confidence endpoints are nevertheless computed outward using exact rational arithmetic, avoiding an additional floating-point rounding qualification.

## Files

- `local_birth_oracle.py`, `exact_lazy_time.py`, `PRIMITIVE_PROOFS.md`: acquired exact primitives.
- `local_perfect_sampler.py`: consistent local marked-ancestor engine.
- `estimate_local_spin.py`: complete physical readout, finite or infinite box.
- `exact_confidence.py`: outward rational fixed-confidence arithmetic.
- `THERMODYNAMIC_PAIR_JOIN.md`: scoped physical limiting argument.
- `primitive_checks.json`: complete 3×3/4×4 oracle audit and exact-time checks.
- `physical_local_*json`: actual physical benchmark outputs and work counters.
- `production_manifest.json`, `production_progress.json`, `production_summary.json`: frozen implementation, fixed-budget monitoring and final cost/display checks.
