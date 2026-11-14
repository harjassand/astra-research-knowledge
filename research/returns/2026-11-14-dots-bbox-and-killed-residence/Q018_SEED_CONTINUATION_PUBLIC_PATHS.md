# Native-clock seed continuation with local importance tilt

## Construction

Use common uniformization rate Λ=n+κ for the original rate-one-per-site heatbath dynamics plus soft source clock. Each tick chooses sitei with probability1/Λ, or a source-clock attempt with probabilityκ/Λ. A source-clock attempt kills only insideA; elsewhere it is a null. Sitei flips with native probabilityc_i=1/(1+exp(Δ_i)). Holding times are independentExp(Λ).

A proposal uses q_i=1/(1+exp(Δ_i+2bσ_i)), adding a fixed positive fieldbiasb but changing neither event-selection probabilities nor source-clock logic. It needs only local spins andA-membership, not a committor. For each selected-site event multiply likelihood byc_i/q_i for a flip, or(1−c_i)/(1−q_i) for a null. Source-clock events have ratio1. Stop only at actual target or source killing.

For terminal likelihoodW, outcomeY, and tick countK, E_proposal[WY]=p_seed and E_proposal[WK/Λ]=m_seed. These are the actual success probability and complete physical duration from the chosen conditional seed law. Holding times have been analytically averaged, not omitted: conditional on the event path, E[sum holding times]=K/Λ. All loops and null proposals remain charged. The likelihood relation is event-resolved, so self-transition events from different sites must not be conflated without aggregating their probabilities consistently.

`exact_seed_path.py` implements exact random-bit event decisions for a concrete3×3 diagnostic with rationalθ6/5,field6/25,κ1/20. Local logistic probabilities use rigorous rational exponential brackets. The initial C1 Gibbs law conditioned on vertex0 being a singleton component is exactly rejection-acquired over its four admissible states; weights areexp[-(228/25)(a−1)]. Likelihood products have outward-rounded rational enclosures. Fifteen paths ran across bias0,.4,1, each likelihood interval width<1e-20. Finite samples do not establish efficient rare success estimation.

## Direct finite-state comparison and cost

`seed_transition.py` explicitly enumerates the256 non-target states of3×3 periodic Ising, A=C1 with uniformNE augmentation, target at least5 plus spins. The floating-point original linear system gives:
- p_seed=0.0010556598057792869.
- m_seed=20.01845962250658 in native physical time.
- native expected uniformized events181.16705958368473.

The local proposal does not read those solutions. They are diagnostic reference calculations only. Executed2000 paths each at bias0,.1,.3,.6, preserving duration rewards. Samples are low-precision Monte Carlo, not theorem certificates. `seed_grid.json` separately compares theoretical finite-state work/variance via linear systems.

At bias.4, proposal success grows to0.00907055, but expected events remain180.39. Success-estimator second moment falls from0.00105566 to0.000275419; second-moment×cost improves only about3.85-fold. This is a modest toy improvement, not evidence of polynomial R200 performance.

## A concrete failure of aggressive drift

For event-resolved importance sampling, the second-moment transient kernel has flip entriesc_i²/(Λq_i), self contributions(1−c_i)²/[Λ(1−q_i)], and the unchanged outside-core source null. If its spectral radius>=1 and the positive success reward is reachable, the success estimator's second moment diverges.

At bias.8 the numerical spectral radius is1.11947. At bias1 there is a stronger EXACT obstruction: at spin mask98 the self-loop second-moment coefficient exceeds1.25, certified with rational exponential intervals in exact_seed_path.py (numerical value1.2591881302). Repeating this same state for arbitrary numbers of null events and then following any positive-probability successful path makes the second-moment sum infinite. The conditional source can reach that state with positive probability. Thus bias1 provably has infinite success-estimator variance despite raising proposal success toabout.1053. Bias3 raises raw success toabout.9527 and dramatically shortens proposal paths, yet its numerical second-moment kernel is vastly supercritical. Raw success frequency and shorter paths alone give a false impression of progress.

## Boundaries

This is standard likelihood-ratio importance sampling specialized with original clocks and full duration. No novelty or breakthrough claimed. It gives a genuine implementable conditional continuation operation but no efficient universal continuation guarantee. Exact event generation costs local updates and core-membership checks per tick; source8's full R200 core membership may require global connectivity work after deletions. That cost has not been replaced with a proven near-constant dynamic data structure. Scaling requires a proposal with controlled likelihood second moments AND computational acquisition/trajectory costs, plus a complete overlap-corrected mixture of seed channels. Pinned equilibrium sampling alone supplies none of those kinetic bounds.
