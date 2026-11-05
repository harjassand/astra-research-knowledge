# Runtime and matched baseline

## Exact sampler

These are completed wall-time measurements on the shared execution computer, using the indexed reverse-clan implementation and the exact torus-return birth oracle. They are not guaranteed runtimes or dedicated-machine benchmarks.

| Open box | Sites | Independent draws | Mean seconds/draw | Mean reverse events | Mean clan size |
|---|---:|---:|---:|---:|---:|
|32×32|1,024|50|0.0672|3,553|69.76|
|64×64|4,096|20|0.4807|24,106|299.55|
|128×128|16,384|10|2.3897|109,662|1,203.2|
|256×256|65,536|3|11.8262|495,113|4,994|

The256² maximum among these three runs was12.826s. The small number of large-box draws does not establish a runtime percentile. An independent128² run took15.19s for137,591reverse events and1,115clan cylinders, with peakRSS29.1MiB; it demonstrates substantial host/seed/runtime variability. A profiled reproduction of that seed took8.58CPU seconds, including profiler overhead. Prefer exact operation counts when comparing these runs.

The new birth oracle's exact proposal intensity is0.2653118600 per site, versus59.376 for the first all-endpoint oracle. The224-fold reduction concerns this internal oracle comparison, not a speedup over published Monte Carlo methods.

## Same-oracle approximate MCMC

`compare_same_oracle_mcmc.py` uses the identical rational all-length birth oracle and the identical target measure. A constant-rate uniformized birth/death chain is recorded after30 heuristic burn-in sweeps. Empty and packed-plaquette initializations are separate runs. Effective sample size is estimated from the initial-positive paired autocorrelation sequence of **loop count only**.

| Box | Recorded sweeps per initialization | Seconds/estimated ESS, empty | Seconds/estimated ESS, packed |
|---|---:|---:|---:|
|32×32|1,000|0.01474|0.01929|
|128×128|300|0.30012|0.38161|

At128² the additional burn-in time was about5s per run. Empirical mean loop counts were585.87 and590.42, with standard deviations20.03 and20.66. The exact-sampler ten-draw mean was584; this small comparison is not a convergence proof for MCMC.

Approximate MCMC is faster per empirical loop-count ESS in these tests, by roughly6–8times at128². The exact sampler's earned distinction is independent stationary output and explicit error accounting without burn-in assumptions, not speed.

## Stronger published comparator

Silva–Schakel–Vasconcelos, PRE88,021301(R)(2013), https://arxiv.org/abs/1306.4996, gives a worm/satellite-list algorithm for the same routed O(N) gas. Its Eq.2 atN=3,K=1 matches this physical model, including degree-four routing and crossings. Open-path correlation measurements are also established prior work.

We have not implemented and run their optimized worm method on the same hardware. Therefore the same-oracle birth/death control above is not a performance comparison against the strongest published implementation, and no claimed speed advantage over worm or quantum Monte Carlo follows.

Generic perfect-simulation and reverse-clan skeletons are also prior work, including Ferrari–Fernández–Garcia(2002) and vanLieshout–Stoica(2006). The proposed distinct result is the verified all-loop subcriticality regime plus a concrete all-length exact-output implementation at the AKLT parameter point.

## Proved costs are much looser

With q<0.996411, expected clan cardinality is bounded by20.870times the site count. Charging the stationary proposal population and its null cylinders gives an O(NlogN) bound on expected dominant reverse events. At256², the conservative exact-rational checker bounds this expectation by447,473,944events, versus495,113observed. Variable trajectory, indexing, canonicalization and random-bit costs are additional.

No finite worst-case runtime is claimed: exact random sampling has unbounded stochastic tails. The temporal ancestor tail and all included null work are documented in `SAMPLING_THEOREM.md` and `certified_work_bounds.json`.
