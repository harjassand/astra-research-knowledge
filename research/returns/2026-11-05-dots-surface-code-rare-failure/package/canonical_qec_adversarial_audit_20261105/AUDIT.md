# Independent adversarial audit of canonical QEC witness sampling

## Scope and verdict

The code-capacity and repeated-measurement constructions pass the checks below. No counterexample was found within the stated independent, equal-probability graph-fault model and minimum-weight decoder contract. This is an audit of mathematical/model validity and executable arithmetic, not proof of real-device noise assumptions, general polynomial efficiency, novel statistics, or superiority over the strongest splitting implementation.

The repeated-measurement model is specifically T data-Z noise rounds, T−1 independently noisy syndrome observations, perfect initial syndrome and perfect final observation. Its returned probability is failure over that complete block, not a directly measured steady-state per-cycle rate. It does not model gate faults, propagation, leakage, correlated faults, or imperfect final closure.

## Core argument checked independently

1. Let e be the graph-error edge set, c an exact minimum-cardinality correction with the same detector syndrome, and r=e XOR c. All interior vertices of r have even degree. Odd total parity across the left rough boundary implies at least one connected component touches both rough boundaries.
2. The deterministic breadth-first selector produces a simple left-to-right path P in r. Because toggling c along P preserves the detector syndrome, minimum cardinality gives |c∩P|≤|P|/2. Since e and c are complementary on P, |e∩P|≥|P|/2.
3. The nonbacktracking proposal contains every such simple path up to the chosen length budget. If B_L is the binomial majority probability on a length-L path, each individual length-L walk has probability B_L/Z under the exact length/start/suffix proposal. Nonsimple walks are deliberately rejected.
4. Conditional sampling of errors on a simple P has density Pr(e)/B_L when P contains a majority of errors. Thus the joint proposal probability is Pr(e)/Z. Exactly one canonical path accepts for each included failing e. Acceptance is therefore an iid Bernoulli variable with mean P_truncated/Z under independent ideal random bits.
5. If the maximum interior degree is Δ, there are at most |left|(Δ−1)^(L−1) candidate length-L paths. For 0<p≤1/2, B_L≤[2√(p(1−p))]^L. The implemented upward rational square-root envelope and geometric tail therefore bound every omitted canonical witness. The 3D graph has Δ=6, not 4.
6. Outward dyadic Clopper–Pearson endpoints for the Bernoulli acceptance probability, multiplied by exact Z and with the omitted tail added only to the upper endpoint, cover the full modeled failure probability. Fixed sample size matters; no stopping based on observed acceptance was used.

## Independent executable checks

Run these from the workspace root with the existing decoder interpreter:

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python canonical_qec_adversarial_audit_20261105/audit.py

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python canonical_qec_adversarial_audit_20261105/audit_phenomenological.py

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python canonical_qec_adversarial_audit_20261105/audit_d21_normalizer.py

### Code-capacity audit

- All 8,192 distance-3 error patterns and all 64 detector syndromes checked; decoder correction weight compared with exhaustive optimum, and residual-component parity checked separately.
- Reconstructed the actual length/start/continuation choice probabilities, conditional binomial count, uniform error subset, and outside-path error probability. This avoids the original test's tautological check that merely summed Pr(e)/Z.
- Exhaustive likelihood and omitted-mass checks at p=1/1000 with length budgets 3 through 7; also p=1/10 and p=1/2 at full length.
- 17,850 integer CDF values compared against independent direct binomial sums.
- 2,144 CP intervals checked against exact root inequalities, one-grid-unit sharpness, and independent numerical beta quantiles. All 1,216 rational coverage-grid cases had at least 0.999 coverage; minimum observed was 0.9990234375.
- 500 larger detector syndromes at distances 5,9,13,25,41, each with at most 14 defects, checked against an independent exact Manhattan-distance/boundary T-join dynamic program.
- Original d13 result arithmetic matches its 2,752 accepted of 10,000 trials and exact rational confidence endpoints.

### Repeated-measurement transfer

- Independently built cumulative physical data-error trajectories, noisy syndrome observations, and consecutive-observation differences. Compared every single-edge fault and 100 random traces at each of d3/T1, d3/T2, d3/T3, d5/T5, d9/T7. All 1,828 edge-basis comparisons and 500 random traces match the graph syndrome and final logical parity.
- For d3/T2, an independent breadth-first search over all 4,096 syndrome masks gives the exact minimum fault weight. Every PyMatching correction matches it and satisfies its syndrome.
- All 41,449 fault patterns of weight 0 through 4 on that 32-edge graph satisfy the canonical-cover and majority property. This is not an exhaustive check of all 2^32 error patterns.
- Independent depth-first enumeration of length≤9 nonbacktracking paths gives counts [0,0,0,6,28,74,152,302,708,1822], matching the production backward DP.
- The vectorized Bernoulli primitive was checked on its complete 16-bit input domain for 16 parameter cases, including denominators 1,000, 32,769, 65,535 and 65,536. Uniform accepted residues are exact; independence still assumes independent ideal input bits.
- Separate d21 audit recomputes the whole normalizer using a forward directed-walk recurrence with O(E) state, independently recomputes the degree-6 tail, checks CP root inequalities using a reverse integer-binomial sum, and replays the fixed 10,000-trial stream. See d21_independent_results.json for its completed result and hashes.

## Findings and limitations

- The initial sampler omitted a p≤1/2 input guard. At p=.999 the small Chernoff factor is not a majority upper bound. Current code rejects this out-of-domain input. This did not affect either p=.001 result.
- Python Random is deterministic pseudorandomness. The interval has its stated finite-sample interpretation under the explicitly declared ideal-iid-bit model; the code is not a physical entropy certificate.
- Exact minimum-weight decoding remains a trusted library contract, supported by independent small and sampled larger checks, not a formally verified proof of all PyMatching executions.
- A separately reported serial-diamond family shows exponential rejection is possible. No general graph polynomial-time claim follows from these experiments.
- The method's integer/rational arithmetic does not make its physical assumptions exact. For example, Q=(1−ε)P+εδ_L adds a rare undetectable logical-string event to the assumed iid model. It raises logical failure to (1−ε)P(failure)+ε while changing any affected physical error marginal by at most ε. A common-mode rate ε=10^−12 can therefore dominate a modeled 10^−23 failure rate despite a negligible marginal change. This is a counterexample to unrestricted hardware transfer, not to the stated simulation.

## Relevant prior-work boundary

The unique-representative acceptance construction is the classical coverage algorithm of Karp, Luby and Madras, *Monte-Carlo Approximation Algorithms for Enumeration Problems*, Journal of Algorithms 10 (1989), §3 and §5. The specialization here is an implicit nonbacktracking cover, a decoder-derived path selector, and a rigorous omitted-witness tail, not a new general acceptance identity. https://www.math.cmu.edu/~af1p/Teaching/MCC17/Papers/KLM.pdf

Bravyi–Vargo splitting predates this construction by over a decade. Mayer et al., *Rare Event Simulation of Quantum Error-Correcting Circuits* (Quantum, 2026), demonstrates circuit-noise rates below 10^−20; §6.1.1 explicitly leaves rigorous convergence/confidence quantification open. This gives a meaningful distinction for the iid finite-sample intervals in the restricted graph model, but not proof of overall computational superiority. https://arxiv.org/html/2509.13678

Beverland et al., *Fail fast* (2025), studies failure-spectrum fitting, exact minimum-weight failure analysis, and multiseed splitting; it documents mixing difficulties and improvements. Any performance comparison must include strong multiseed/optimized splitting, not merely naive Monte Carlo or an intentionally weak single-chain implementation. https://arxiv.org/html/2511.15177
