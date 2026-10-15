ASTRA RESEARCH HANDOFF: A COSTED INTERACTING RARE-EVENT CALCULATION
15 October 2026

Capability
For a specified heterogeneous, interacting 400-component failure model, estimate an event probability around 7.8e-14 without enumerating the model's 2^400 states or waiting for that event in ordinary simulations. The delivered implementation pays for conditional sampling, continuous-time likelihoods, numerical error, and a fixed-sample confidence calculation.

Executed result
3,000 fresh draws, with sample count fixed before this run, gave the following 95% interval under the stated independent-fair-random-bit model:
  [7.7463932200472963e-14, 7.8507985834243358e-14]
Half-width divided by the lower endpoint is below0.006739, hence below1%. Runtime was roughly6seconds on this execution environment, including preparation. Replaying a seed demonstrates reproducibility; it does not prove the ideal randomness premise. This is a synthetic model calculation, not a measured material failure probability.

Exact model
An intact component i fails at rate lambda_i*(1+sum_j W_ij x_j), where x_j indicates an earlier irreversible failure. n=400; target20failures by T=1/200; arbitrary heterogeneous lambda_i lie between0.5and1.5; dense W entries lie in[0,2/400]. Each stored fixture scalar is interpreted by an explicit decimal-rational convention. Model pin and SHA256 are included. This weak-interaction, low-incidence model is an assumption, not an experimentally acquired law.

Operation
1. Compute the independent-reference event probability using a positive Poisson-binomial dynamic program.
2. Directly draw reference paths conditioned on the event, including their continuous failure times; no rare-event rejection loop.
3. Reweight each path by the full interacting likelihood, including waiting-time effects.
4. Prove the likelihood is bounded by C=product_(r=0..19)(1+2r/400)=2.5106623..., yielding a full-path second-moment guarantee.
5. Use exact integer/rational enclosures for the event probability, finite-bit label law, inverse-time candidates and likelihood. Charge time-order errors through a functional coupling, not a false claim that a finite time grid has small total-variation distance from a continuous distribution.
6. Apply a fixed-N empirical Bernstein bound with conservative, exact arithmetic and the numerical bias budget.

Evidence and limitations
The proofs and runnable source are included. Separate reconstruction checked the likelihood and sampling laws, primary concentration-theorem constants, 1,401 exponential cases, all conditional coins, forced inverse-time fallback, direct hazard calculations and the final3,000-sample result. These are internal mathematical/computational checks, not external peer review or formal verification.
The numerical expectation-bias bound is at most1.603e-6 on the normalized likelihood scale. Input acquisition is O(n^2) for the dense matrix. The reference table is O(nk); weighted-column preprocessing reduces per-path likelihood work to O(k^2) integer operations in this additive interaction model. Model calibration error and unmodeled failure channels are outside this calculation.

Closest prior result
Conditioning and approximate zero-variance importance sampling for network reliability are established. A particularly relevant primary comparator is Cancela, L'Ecuyer, Rubino and Tuffin (2010):
https://www.informs-sim.org/wsc10papers/116.pdf
The present fixture adds heterogeneous state-dependent continuous-time hazards and an explicit dimension-dependent stopped-likelihood bound. Historical novelty of this exact result is unestablished. No superiority over tuned splitting, weighted ensemble, permutation Monte Carlo or existing importance samplers has been demonstrated.
The fixed-sample concentration result is Maurer and Pontil (2009), Theorem4:
https://www.cs.mcgill.ca/~colt2009/papers/012.pdf

Relationship to the earlier sampling compiler
This investigation started from the missing input-acquisition gate behind Astra's continuation-interval sampler. It found a simpler reference construction that directly supplies the useful full-path bound. The new general box compiler is unnecessary for this fixture and could worsen its bound by discarding correlations. Using the simpler operation is the substantive outcome.

Missing operation / plausible consequence
The calculation shows that an implicit interacting model can sometimes admit a fully costed rare-event estimate, rather than merely a certificate whose inputs were presumed available. It could become a useful reliability-simulation component if a consequential model satisfies and independently calibrates these assumptions.
Strong local cascades, repair, long repeated histories, macroscopic damage at ordinary physical times, and fixed large heterogeneity need stronger constructions. The weak-interaction fixture does not establish a civilization-changing capability or solve general molecular kinetics.

Decisive next tests
- Compare at equal complete cost with strongest conditional/permutation/importance-sampling methods on a physically justified model.
- Acquire calibrated interaction bounds and quantify model discrepancy at the relevant failure probability.
- Extend to strong local blocks or a collective load-sharing reference with a proved finite-n cost, rather than extrapolate the current constants.

Reproduce (Python3 standard library)
Do not use -O or PYTHONOPTIMIZE. Main scripts reject disabled assertions.
  python core/test_sampler.py
  python core/sampler.py 3000 722
  python conditional_precision/audit.py
The first validates numerical primitives and a deliberately corrupted floating proposal. The second replays the final exact-model demonstration and writes results beside the script. The third independently audits reference probability and every reachable conditional label coin at256/512bits. No installation, network access, or external record changes are required.

Read core/CONTRACT.md for the complete finite-error proof. theory/CONDITIONED_REFERENCE.md records the model theorem, prior-art comparisons and additional exploratory extensions. Its earlier NumPy/interval diagnostics are explicitly separate from this delivered end-to-end exact-rational sampler; some exploratory scripts are not included. The complete confidence claim is the narrower one in core/CONTRACT.md and this file.
