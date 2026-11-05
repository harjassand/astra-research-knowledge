# Completed static acquisition checkpoint for root

The requested small-fixture acquisition run is complete. Full data: `next3_gibbs_code/results.json`; execution transcript: `run_stdout.txt`; repeat via `python next3_gibbs_code/run_demo.py`. The engine never receives enumerated probabilities or exact reference partition sums.

- Nonsymmetric graph: 6 vertices, 10 binary edge-failure variables, 31 full cuts, 1024 exact reference states.
- Exact Dobrushin coefficient: 0.37311872909698995 (display only; comparison rational). Exact logarithmic contrast c=3 verified. Ordinary odds contrast approximately 1.8325193796267e12. Transition denominators need at most 98 bits.
- Exact failure probability: 3.7252956888856366e-28. Acquired estimate: 3.800863790182855e-28; relative error +0.020285128378580687.
- Executed local-confidence interval: [2.894287567127758e-28, 4.754035930511187e-28]. This contains the reference. It is wider than 10%; do not call this execution the whole-theorem 10% schedule.
- Generic heavy-prefix engine obtained 32 partition estimates using 32 sampled marginal stages, 12,904 draws/stage, plus exact local-envelope stages and cached prefixes. All 32 partition intervals contain their exact reference. Largest point relative error 0.020088269011979163.
- Partition acquisition: 412,928 independently restarted pinned draws and 27,821,024 heat-bath updates. Union estimation: 8,192 proposals, 2,220,856 updates. Conditional acquisition: 8,192 accepted failed states from 16,384 generated batched proposals (8,192 consumed), 5,038,286 updates.
- Total: 437,504 pinned draws; 35,080,166 heat-bath updates; 70,160,332 heat-bath integer random operations; 97,645,560 PRNG 64-bit words; 32,768 Python integer operations and 41,428,350 Python PRNG bits. Chains use at most 335 steps, fresh unpinned-zero initialization.
- Wall time on this environment: partition 1.060s, union 0.264s, conditional 0.463s; total including exact validation and compilation about 2.992s. Timings are one run, not benchmark claims.
- Conditional empirical histogram TV to exact target: 0.018446281707569366; largest marginal error 0.008565100678779431. Per-output analytic acquired-weight TV bound: 0.14567465682316794; mixing contribution <=6.2e-7. Joint 8,192-output TV union bound is vacuous (1); empirical TV is not an output-law guarantee.
- Independent-edge replacement with the same one-edge marginals gives failure 1.979382140288482e-28, about 47% below the correlated reference; ratio correlated/independent =1.8820497634391604. Correlation therefore materially matters.

Finite randomness is capped and exact-rational, with explicit abort on overflow/cap; no biased fallback. The reproducible experiment uses seeded PRNGs; theorem probability guarantees assume independent fair bits. Native sampler cap-abort union bound <7.05e-14; rejection cap-abort target 1e-6.

**Limitations relevant to Section 11:** all cuts are explicitly enumerated for this small fixture. Root's final theorem calculation places it in the `v<=2a` branch (`h=.1`, `c=3`, `C=6`, `a=15`); maxcut 246.814184699 is below cutoff 520.014094433, so all31 cuts are retained. Scalable contraction is not implemented here. Observed proposals all had multiplicity 1 because intersections require extra extremely rare failures. Inverse multiplicity is nevertheless implemented and its exact identity and `c(x)=2^(components(x)-1)-1` were verified on all 1024 states, including all intersections. This run should not be advertised as an empirical overlap stress test.

The conservative parent heavy-prefix schedule for epsilon=0.1, delta=0.01 and 32 queries is separately reported: 81,920,000 draws/stage, 26,214,400,000 total pinned draws, and upper bound 6,291,456,000,000 heat-bath updates. That schedule was not executed.

Passive route preserved with complete mathematical proof and honest acquisition/comparator limitations in `next3_first_principles/02_PASSIVE_MEMORY_PROOF.md`.

**Final receipt:** README and result status finalized; no extra tests or acquisition reruns were added. Local table construction costs `sum_i 2^d_i`; this fixture has maximum degree3 and46 conditional entries. The parent general theorem assumes certified influences as input. The implementation uses exact rational random scan with capped aborts, distinct from the parent systematic dyadic sampler.
