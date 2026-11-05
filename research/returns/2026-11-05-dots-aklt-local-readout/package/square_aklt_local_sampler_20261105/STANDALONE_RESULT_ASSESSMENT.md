# Independent assessment of the local physical-prediction operation

Status: proof and implementation signoff reviewed; the fixed-budget production run completed and its source hashes, budget, exact interval and runtime were independently checked. This assessment is separate from the construction and does not claim external peer review or an exhaustive priority search.

## Verdict

This is a complete, specialized computational capability rather than only a formal intermediate lemma. It joins a certified parameter regime, an implementable all-length proposal, a consistent local infinite-volume sampler, and an independently checked physical observable. The distinctive output is a finite-sample confidence interval for a precisely specified thermodynamic spin correlation without an unquantified burn-in or finite-box bias.

It is not presently a demonstrated speed breakthrough over the strongest established simulation methods, a new physical phenomenon, or a result close to delivering quantum hardware or fault-tolerant computation. A defensible characterization is a candidate advance in rigorously controlled many-body simulation, useful as a verification/reference instrument. Calling it a civilization-changing breakthrough would be unjustified.

## What is actually computed

For distinct sites i,j, the target is the limit of Tr(sigma_R S_i dot S_j) as open rectangles R exhaust the square lattice, where sigma_R = V_R I_boundary V_R* / Tr(V_R I_boundary V_R*). These are spin-2 AKLT virtual-identity-boundary mixtures. The construction proves this selected pair limit by coupling, without claiming uniqueness under arbitrary quantum boundary states.

One complete attempt draws an all-length open path and then independently queries precisely the stationary loops needed for its suppression factor. Its signed output lies in an interval of width 9 C_ij. The physical factor 9, sublattice sign, source-path normalization, endpoint revisits, and normalized-loop denominator have been checked against independent exact sphere moments and small quantum VBS amplitudes. No estimated ratio of partition functions is taken.

For nearest neighbors, C = 301805115576299 / 500964985405440. A fixed 542236 attempts gives an outward rational Hoeffding radius 4999997629 / 500000000000, less than 0.01, at failure probability at most 1/20. This is a probabilistic error guarantee under the specified ideal independent-bit algorithm, not a deterministic exact value or an experimental uncertainty interval. Seeded Python runs are reproducible numerical realizations, not proofs that a finite PRNG seed supplies ideal randomness.

## Completed production result

The 542236-attempt, fresh-seed run returned nearest-neighbor dot correlation -3.559889190566645 with outward 95% interval [-3.569889186, -3.549889195]. It required 463946 independent local loop queries and 723.006765 seconds including setup, approximately 12 minutes 3 seconds. The interval shown here rounds both endpoints outward again. The exact rational endpoints are retained in the production JSON.

A separate 100-digit arithmetic check confirmed the outward radius and minimum sample budget, and a fresh execution of the independent physical spin-2 tensor test reproduced the exact small-box values to below 9e-16. These are cross-checks of the joins, not a replacement for the algorithm proof.

## Comparison with the strongest relevant prior approaches

1. Silva, Schakel and Vasconcelos, Physical Review E 88, 021301(R) (2013), https://arxiv.org/abs/1306.4996. Their crossing O(N) worm method includes the same routed gas at N=3, K=1 and open-source correlation measurements. Neither the model mapping nor the ability to measure correlations is new. Their reported numerical study concerns finite periodic lattices and mainly N below 2. No matched implementation of this worm has been run here, so no speed or variance advantage over it has been established.

2. Wierschem and Beach, Physical Review B 93, 245141 (2016), https://arxiv.org/abs/1603.03444. This already evaluates ordinary and strange AKLT correlators using valence-bond loop Monte Carlo, including square lattices. It explicitly uses asymptotic Monte Carlo exactness. The present distinction is the acquired finite-confidence, no-equilibration and no-finite-box guarantee for the selected local limit, not first physical AKLT readout or superior observed precision.

3. Fernandez, Ferrari and Garcia, Stochastic Processes and their Applications 102 (2002), https://arxiv.org/abs/math/9911162. Finite-window infinite-volume perfect simulation by backward marked ancestors and forward cleaning is established. The current work supplies model-specific quantitative subcriticality, the realizable intersecting-loop birth oracle, exact event handling, and the physical estimator. It does not invent local perfect sampling.

4. Feng, Guo and Yin, Random Structures & Algorithms 61 (2022), https://doi.org/10.1002/rsa.21079. General conversion of strong spatial mixing into perfect sampling is prior art. Applying such generic results at this particular crossed-loop parameter point still requires verifying the relevant hypotheses and implementing the sampling primitives. A possible alternative implementation is not automatically an existing equally certified implementation.

Targeted searches and these primary-source checks did not identify an earlier identical parameter-certified iid infinite-volume physical readout. That supports a novelty candidate, not a publication-level first-result claim. Wierschem and Beach already present ordinary square-AKLT correlations on a 512 by 512 periodic lattice. I did not verify a tabulated nearest-neighbor number with enough precision and the same limiting convention to make a pointwise numerical benchmark claim. The new value is therefore not presented as a newly discovered correlation or precision record. Strong tensor-network methods are also relevant practical incumbents for this low-entanglement state; no matched numerical precision/runtime contest against them has been conducted.

## Resource assessment

The enclosing lattice area is absent from the local engine's work-count bounds; it does not first construct or equilibrate a finite approximation to the whole system. For a fixed finite query K, independently checked bounds include fewer than 14.120548 |K| expected loop-oracle calls, including null and rejected proposals, and fewer than 172 |K| expected loop-walk steps. These are not wall-time bounds.

The proof separately charges retained geometry, old-region and pair scans, exact Poisson generation, and adaptive exact timestamp comparisons. These costs have finite expectation for each fixed finite query. The random source-path join also closes: its continuation tail has rate rho=709007/750000, while the local-query proposal MGF has exponent H<2039/10^9. Since H<1-rho, exp(H)rho<1. An exact checker also bounds E_path exp(H|K|) by 1.014858962. Averaging the query MGF over the unbounded path therefore retains a positive exponential moment, so the full physical attempt has finite expected exact arithmetic, not merely almost-sure termination.

No useful small bit-complexity constant or linear-in-|K| total arithmetic theorem is established. Coordinate bit lengths and query geometry matter. Accumulating many rational outputs also has a precision cost. The correct accuracy statement is an explicit O(epsilon^-2 log(1/alpha)) count of independent attempts for a fixed pair, with volume-independent finite expected sampling cost per attempt; it is not a demonstrated optimal end-to-end bit complexity.

Nearest-neighbor pilots completed 10000 full attempts in 11.228 seconds on the infinite lattice and 12.361 seconds in a 32 by 32 box, with approximately 0.1 seconds of table setup. These include path nulls, local proposals, exact comparisons and readout. The approximately 67-fold per-attempt gain over our former whole-box exact 32 by 32 implementation is an internal architectural comparison only. Older same-oracle MCMC was faster than the global exact sampler per empirical loop-count ESS; that neither measures the new local physical estimator nor settles the worm comparison.

For distant tiny correlations, the fixed auxiliary torus proposal has an alias floor. Additive error does not imply useful relative error, and rare-event cost remains. The all-endpoint summed observable has a large proposal constant. A local two-point demonstration is not an efficient general measurement interface, a dynamical response solver, or full quantum-state simulation.

## Audit evidence and remaining qualification

The independent local audit checks the residual-Poisson exposure invariant, reuse of previously revealed cylinders and pair marks, exact primitive probabilities, exact lazy-time comparisons, and finite/infinite coupling. A separate geometric-exposure implementation and small exact distributions were used as checks. An early selected rare-category deficit was preserved. A fresh preregistered two-million-draw main-engine test observed 770 events against 781.861 expected, with two-sided binomial p approximately 0.694; this did not reproduce the deficit. Statistical nonrejection is not the correctness proof.

All 12 production-manifest source/table hashes matched when independently checked on 5 November 2026. No claim is made that this is a formal proof-assistant verification or external peer review. The final production run completed without a restart, cutoff or data-dependent stopping decision. The frozen hashes were rechecked afterwards. See standalone_assessment_checks.json for the independent receipt checks.

## Relevance to the original high-return objective

The work has cleared the important access-and-operation hurdle: the inputs and controls are acquired, code runs at a useful local scale, all required stages are charged, and the output answers a physical question. This is a meaningful improvement over earlier disconnected theoretical ingredients.

The remaining distance to the north-star is substantial. Reliable error bars for an already tractable model do not by themselves unlock a new industry, a new quantum-computational capability, or the square-AKLT spectral gap. Its best present use is as an independently reproducible benchmark and exact sampling instrument, and possibly as a reusable ingredient in a genuinely consequential later theorem. The latter is an opportunity, not an earned consequence.

Recommended presentation: report the completed numerical interval, the specific guarantee it adds, the strongest prior methods, and the absence of a speed or gap claim. Preserve the sampler as a completed research output. Continue the quantum boundary route only through a clearly defined quantitative gate, rather than relabeling sampler correctness as the sought quantum breakthrough.
