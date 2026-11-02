# Reusable scientific computation from task-dependent state discovery

**Research note, 2 November 2026.** Reproducible computations in this directory.  This is a new bounded construction and conditional mathematical result **within established stochastic model reduction**, not a priority claim or proof of generally intelligent algorithm invention.

## Executive result

I constructed and ran a task-conditioned abstraction learner for finite-state, locally interacting continuous-time Markov systems. It acquires a structural population-count representation from a native unary/pair-interaction source, retains the compiled sparse generator and supports new observables, new site-specific perturbations, new native rate matrices, and macro-observable feedback interventions. It rejects unsupported named-site outputs, obtains sampled failure evidence, and refines the representation. The mathematical contribution of the study is an explicit **second-order, all-payoff, finite-horizon** certificate under orbit-centering, exchangeable initial preparation, and small native-rule deviations.

For the distributed-heterogeneity 25-site experiment, all 25 sites have distinct native recovery rates and simple exact exchangeable-site lumping produces 2^25 = 33,554,432 states; retained near-exchangeability permits 810 states. Two **outward rational** enclosures, including analytical model discrepancy, are:

| Decision | Extinction probability interval at T = 2.6 |
|---|---|
| No added recovery intervention | [0.064698024927290358..., 0.065137289727290392...] |
| Add +0.08 recovery rate in originally acquired group 0 | [0.078701785882733172..., 0.079141050682733201...] |

Both are strictly separated from the stipulated policy threshold 0.075. These are exact-source-model decisions, not evidence about a real epidemic or an actual device. A strong general near-lumpability solver might also obtain them; no claim of superiority is made without an actual matched execution.

## 1. Selection from strong existing machinery

Astra revision `9cabf2cde4493d50d93bfd5c7a5b18074dabf8ab`, read through the public GitHub fallback rather than the optional private/local semantic retriever:

- N1515: acquisition of a stable signed-operator calculus from noisy scalar word experiments. Its library can require exponentially many atoms; a strong retaining ordinary learner wins the supplied comparison.
- N1521: learned landmark geometry and quadratic return-observable leakage, but expensive geometric conditioning and representation discovery persist.
- N1630 and U1635: later task-fed bounded projection can cost approximately 3e21 calibration reports against ~1.35e6 for an ordinary retainer, on its reported adverse small fixture.

Primary algorithmic competitors: DreamCoder (inductive program/library synthesis, 2021), Stitch (top-down library synthesis, 2023), and Palmarini–Lucas–Siddharth (decompiling amortized knowledge, 2024). They already accomplish substantive compositional program reuse, and should not be described as unable to acquire algorithms. They are not head-to-head methods for explicitly solving CTMC model checking unless a comparable program corpus, semantics and time budget are provided.

For **the selected task family**, the truly relevant ordinary competitors include exact reaction-network species equivalence and target-preserving partition refinement (e.g. ERODE; Cardelli et al., 2021), exact/sound CTMC checking (Storm, PRISM and direct sparse uniformization), rigorous transient aggregation error bounds (Michel & Siegle, 2025), quantitative coarse-graining (Hilder & Sharma, 2024), tensor-network and matrix-free methods, variance-reduced Gillespie sampling, and perturbative model reduction. I implemented a full finite-state generator, exact site-symmetry refinement and a conservative first-order perturbation envelope. I did **not** run or benchmark ERODE, Storm or state-of-the-art near-lumping implementations; therefore no matched best-of-field speedup is established.

Strong literature directly defeats any novelty claim for simple exact symmetry discovery, count aggregation, named-variable partition refinement, learned DSL compression, or generic perturbation/semigroup error estimates. The remaining question is whether the *joined* conditional certificate, task guards and amortization extend to a materially useful regime not already handled as well by such methods.

## 2. Native scientific input, source access and costs

A model has n sites, states in {0,...,q-1}, unary transition coefficients a[j,s,t] and pair-triggered coefficients b[i,j,r,s,t], with i!=j and nonnegative rates. Site j changes from s to t at rate

    lambda_j(s -> t | x) = a[j,s,t] + sum_{i != j} b[i,j,x_i,s,t].

The learner receives the **complete native local rate arrays** as the permitted scientific model. It does **not** receive class labels, symmetry classes, macro coordinates or the later observable. Both competitors receive and may retain precisely the same rate arrays. The *unary/pair reaction grammar and model validity are supplied*; learning this grammar from raw sensor records is NOT achieved. The source is a synthetic mathematical simulator, not an actual physical assay.

A full CTMC has q^n configurations. Its exact sparse generator and its semigroup are the ordinary reference when affordable. There are no hidden feature or verification oracles. Native source coefficient access has cost O(n^2 q^3), and algorithm source-array comparison, generator construction, rational exact checks, 80-bit fixed-integer iterations, training, failures, model storage and deployment are explicitly counted separately. Published research and coding effort are **not** measured as comparable runtime.

## 3. Acquired state variables and exact compilation

For site i and site j, compare all native array entries that are incident to i or j under the transposition i <-> j. Accept the swap only if the complete source arrays are unchanged. Generate the corresponding site exchangeability classes g_1,...,g_G from the accepted swaps. This conservative method has O(n^3 q^3) worst-case comparison work. It is **not** a maximal species-equivalence algorithm like ERODE.

Discover count state k_{g,s} = #{j in g : x_j=s}. Its state space has

    K = product_{g=1}^G binomial(|g|+q-1,q-1)

states. Let a_bar and b_bar be the arithmetically averaged source rules over sites or ordered site pairs of each group. For a change from state s to t in group g, the compiled rate is

    R(k,k-e_{g,s}+e_{g,t})
      = k_{g,s} [ a_bar[g,s,t]
        + sum_{h,r} b_bar[h,g,r,s,t] (k_{h,r}-1_{h=g,r=s}) ].

When all accepted transpositions preserve the actual native rules, this is an **exact** Markov-chain lumping. When the later rules are heterogeneous but close to the old orbit-symmetric class, it is the uniform-orbit projected reference process. The latter does not promise that the microscopic process is Markovian after coarse observation.

A new individual-site query may not factor through the counts. It must be refused or recomputed after the queried site is made a singleton. The code supports that safeguard; its older unguarded prediction is retained solely as a negative test.

## 4. Main theorem: zero-first-order errors for task-conditioned observables

**Theorem (conditional finite-time certificate).** Let Q be the generator of a finite CTMC; let a product of finite site-permutation groups define an orbit partition. Let Q0 be the group average of Q (the full-generator version of averaging a,b), with B lifting macro observables and H uniform averaging within each orbit; thus HB=I, Q0 B = B R and H Q0 = R H. Put E=Q-Q0 and assume an explicit native coefficient bound eta such that

    ||E||_{infinity -> infinity} <= 2 eta,
    ||E B g||_infinity <= eta for all macro payoffs 0<=g<=1.

The exact averaged construction gives H E B=0. If the initial microscopic law is uniformly random within each occupied macro orbit (mu=mu_bar H), then for every terminal orbit-invariant payoff 0<=f<=1,

    |mu exp(T Q) B f - mu_bar exp(T R) f|
      <= min(1, eta^2 T^2).

The same estimate applies to any externally scheduled group-equivariant intervention, with eta*T replaced by integral eta(t) dt. It also applies to count-dependent Markov feedback if the controller state and its observations/actions are group invariant; augment the Markov state with the controller memory. A policy that reads individual labels or produces label-dependent actions invalidates this extension.

**Proof.** The group-averaged generator commutes with every permutation; the uniform orbit projection H intertwines its semigroup with the coarse semigroup. For every t, H E exp(tQ0)B=0. Duhamel and this cancellation yield

    mu [exp(T Q)-exp(T Q0)] B f
      = integral_0^T mu [exp(s Q)-exp(s Q0)]
        E exp((T-s) Q0) B f ds.

Because Markov semigroups are stochastic, Duhamel also bounds the total-variation/L1 distance of the two time-s propagated laws by 2 eta s; and since the propagated payoff remains in [0,1], the supnorm of E acting on it is at most eta. Integration gives integral_0^T (2 eta s)eta ds = eta^2 T^2. Cap the bound by 1. For time-dependent systems, replace eta s by the integral of eta up to s, giving (integral eta)^2. Every step is deterministic; no unproven mixing or asymptotic approximation is invoked.

**Explicit coefficient bound.** Let eta = sum_{j,s,t}|a[j,s,t]-a_bar[group(j),s,t]| + sum_{i!=j,r,s,t}|b[i,j,r,s,t]-b_bar[group(i),group(j),r,s,t]|. Each possible microscopic transition uses a subset of these native coefficients. Hence its aggregate absolute off-diagonal deviation is no greater than eta, the full generator infinity norm deviation no greater than 2 eta, and a [0,1] payoff changes by at most eta under E. This is conservative and potentially dominated by prior more task-specific estimators.

The theorem is also a general group-projection perturbation argument; the present work **does not** establish its historical novelty. Prior near-lumpability and quantitative stochastic model reduction must be compared before any mathematical originality claim.

## 5. Empirical complete-cycle results

Run `python experiments.py`, `python validation.py`, `python failure_acquisition.py`, `python feedback_test.py`, `python verified_uniformization.py`.

- Training: q=2 SIS with n=5, 32 microstates -> 12 count states; q=3 SIRS with n=4, 81 -> 36; exact values numerically matched.
- Held out: q=2 n=7 (128 -> 20, error 1.67e-16), q=2 n=8 (256 -> 48, error 2.78e-17), q=3 n=6 (729 -> 100, error 5.55e-17). These are programmatically generated model fixtures, not external physical validation datasets.
- Failure: a fixed named infected site had a probability 0.3571022 at T=2.8. Substituting group-average occupancy naively predicted 0.1217011 (error 0.2354011). **512 separately simulated SSA episodes** at the actual native transition rules returned mean 0.3613281 and a 99% Hoeffding interval [0.289397,0.433260], rejecting the old prediction; this failure signal does not use the full-generator truth. The repaired 32-state quotient predicted 0.3571022, matching the external full generator to 1.67e-16. The source bill is 512 simulated episodes, 586 reaction events, 46,116 individual pair-rate lookups, 512 terminal readouts, plus re-detection and two model executions. Source access is simulated, not an experiment on a living system.
- Sparse heterogeneity: four irregular source/target sites at n=25 break the original exact grouping; the conventional **exact** site-refinement method nevertheless yields 8,064 states and a 0.0648611 full-exact-under-refinement result in about 0.48 s. This **defeats the case for using approximate reduction there**. The study preserves that negative selection.
- Distributed heterogeneity: every one of the 25 sites has a distinct recovery coefficient. Simple exact site-symmetry grouping now yields 33,554,432 states (not executed). A retained 810-state projected generator still meets the analytic approximation guarantee with eta~0.0057 and T=2.6, i.e. halfwidth eta²T²~0.0002196324. Recovery intervention policy +0.08 changes the projected clearance forecast from 0.0649176573 to 0.0789214183. Both analytic intervals exclude the selected 0.075 threshold on opposite sides.
- q=3 diffuse heterogeneity: eight sites, full 6,561 versus projected 225; observed extinction-event discrepancy 5.29e-7 versus theoretical allowance 1.4161e-4.
- Macro feedback: 15 held-out (threshold, intervention strength) combinations on an eight-site SIS model, all respecting the same certificate, maximum observed discrepancy ~6.36e-7 against 1.871424e-4 bound. This only tests simulated count-triggered policies; continuous observation/actuation costs of a physical implementation remain unacquired.
- Independent checks: 3 exact quotient/intertwining checks and 36 seeded near-lumping random tests; none violated the certificate; maximal observed-error/bound ratio about 0.0717. Finite checks do not establish the general theorem—its algebraic proof does.
- Two minimal falsifiers: with n=2, group-mean recovery rate 0.30 and deviations +/-0.001, a non-exchangeable initial infected site makes a **count-invariant** extinction event have error 0.00074045, violating the *invalidly applied* quadratic bound 0.000004. Conversely, exchangeable initial preparation with **named-site output** also incurs error 0.00074045. These demonstrate why both conditions are essential.

## 6. Rationally outward 25-site decision certificate

`verified_uniformization.py` interprets the finite-decimal string representation of every native input coefficient as an exact rational number. It constructs all averaged coefficients and the uniformized stochastic matrix P=I+R/lambda by rational arithmetic, with lambda the exact ceiling of the maximum row exit rate.

For each intervention, the verifier uses horizon 2.6, Poisson truncation K=155, positive exponential series M=170, and a 2^80 fixed-point integer vector. The matrix is row-stochastic with nonnegative rational entries and 5,128 nonzero transitions. Flooring every positive rational multiply gives a componentwise lower bound on the iterated law. The total missing probability is at most (K * nnz)/2^80. The exponential prefactor e^-lambda T is enclosed using reciprocal positive-series bounds for e^(lambda T); the omitted Poisson mass is bounded by a geometric comparison with the first omitted term. The verifier thus proves an exact-rational bracket around the **projected** expected payoff, not just a floating approximation. Combining it with eta^2 T^2 yields the total true-source-model intervals in the executive result.

Each of the two calls executed 743,133 exact integer floor-multiply updates; measured rational construction plus whole verification about 0.274 seconds each locally. Fraction arithmetic, allocation and source-code development are paid in that wall time, but separate researcher development, real hardware energy, native rate-measurement and physical policy execution are not measured.

## 7. Equal-information lifetime cost and limitations

**Both sides:** obtain the same complete arrays of local native rates, source model type, time horizon, declared outcome, candidate interventions, and prior data. The structured generic solver's human-implemented algorithm is charged as an inherited program, as are the ordinary comparators' standard symmetry and matrix-exponential implementations; we do **not** pretend the generic compiler was learned by an autonomous agent.

**Acquire/compile:** source input is 5,100 scalar entries per n=25 q=2 model (including structural zeros); 300 tested transpositions and no more than 228,000 element comparisons by the code's conservative upper counter; orbit discovery, coefficient projection, 810 macrostate enumeration and sparse generator construction. The user-supplied node groups in the fixture generator are not accessed by the learner. Training examples process 113 full microstates across the two small sources, plus source I/O and generator builds; all training work and failures are included in `experiments.py` runtime. No neural training/algorithm-search cost was incurred because the generic algorithm was engineered by the researcher.

**Failures and calibration:** the failed named-site model, 512 SSA experiments, 46,116 pair-rate lookups, 586 events, repairs, the rejected sparse-perturbation motivation, 36 random validity checks, 15 feedback comparisons, q=3 tests, 2 rational decisions and all native source construction are explicitly executed and reported. Model-verification costs are not treated as zero. Precise energy, programming effort, opportunity cost and external-library CPU costs are not measured.

**Storage and reuse:** the native rate array is retained (5,100 binary64 entries, ~40,800 bytes before Python/array metadata) for each n=25 q=2 model; the acquired coarse generator has 810 rows and 5,128 stored nonzeros plus the class and count mappings. For a later policy, one can retain/reuse the prior grouping, re-evaluate the source deviation eta, rebuild a small projected generator, and run the rational checker. **New physical rates and policy semantics must still be obtained and paid**; past knowledge does not magically provide unknown effects.

**Why the strong baseline is not defeated:** exact symmetry and target-preserving refinement are established, and ordinary near-lumpability and projection theory may reproduce the quadratic correction. A compiled low-rank tensor-network solver, existing rigorous stochastic model checker, strong control variate or existing approximate lumpability tool might match/exceed the full result at equal accuracy and cost. No ERODE/Storm/near-lumping head-to-head or real-data benchmark was executed, so **no general total-computation or scientific impact superiority** is established. The numerical state-count ratio 33,554,432/810 is a representation ratio, NOT a universal runtime lower bound.

**Hard stops:** (i) non-exchangeable preparations and individual-site outputs invalidate cancellation; (ii) long horizons with eta T large yield vacuous bounds (T ~1/eta); (iii) the number of retained groups can grow so the reduced state count remains exponential; (iv) certified source-array uncertainty and higher-order reactions are not learned; (v) a network-specific transition grammar, source stationarity, group-randomized preparation, and intervention response parameters are supplied; (vi) the learned objects do not yet compose arbitrary solvers or invent new program grammars. These are material gaps relative to the requested ambition.

## 8. The real unsolved scientific operation

The strongest opening after this experiment is **learning an experimentally qualified, transferable *structural model language* from partial native event records**, rather than receiving all unary/pair coefficients. A consequential next test would start from raw sparse partial transitions of a real reaction/signal network, acquire not only its rates and symmetry groups but also a testable bound on the unseen interactions, then compile interventions on a genuinely unseen chemistry or network with measured control/observation costs. A predictor that supplies only point estimates would fail. The comparator must implement ERODE-style exact reduction, strong approximate lumpability/validated tensor inference, and task-aware active system identification from the identical raw records; all algorithm-search and calibration must be paid. Positive results under those conditions could be a genuinely cumulative learning contribution. The current work does not meet that standard.

### Sources and executable precedents

1. Astra pinned source: https://github.com/harjassand/astra-research-knowledge/tree/9cabf2cde4493d50d93bfd5c7a5b18074dabf8ab ; N1515, N1521, N1630 and `knowledge/current/packets/U1635-later-adverse-complete-cost-comparison-and-prior-credit.json`.
2. Ellis et al. (2021), *DreamCoder*, https://doi.org/10.1145/3453483.3454080 ; executable work https://github.com/ellisk42/ec .
3. Bowers et al. (2023), *Stitch*, https://doi.org/10.1145/3571234 ; executable code https://github.com/mlb2251/stitch .
4. Palmarini et al. (2024), *Bayesian Program Learning by Decompiling Amortized Knowledge*, https://proceedings.mlr.press/v235/palmarini24a.html .
5. Cardelli et al. (2021), *Exact maximal reduction of stochastic reaction networks by species lumping*, https://academic.oup.com/bioinformatics/article/37/15/2175/6126804 ; executable tool https://www.erode.eu .
6. Michel & Siegle (2025), *Formal error bounds for the state space reduction of Markov chains*, https://www.sciencedirect.com/science/article/pii/S0166531624000695 .
7. Hilder & Sharma (2024), *Quantitative Coarse-Graining of Markov Chains*, https://doi.org/10.1137/22M1473996 .
8. Hensel et al. (2022), *The probabilistic model checker Storm*, https://doi.org/10.1007/s10009-021-00633-z ; https://www.stormchecker.org .

## Reproduce

```bash
cd cumulative_machinery
python experiments.py
python validation.py
python failure_acquisition.py
python feedback_test.py
python verified_uniformization.py
```

Use Python 3 with NumPy and SciPy. Results are serialized into adjacent JSON files. The deterministic network fixtures and source arrays are generated inside the checked scripts. The full 33-million-state model is intentionally **not** evaluated; the proof and formal rational certificate are used instead. The exact arithmetic concerns the rationalized model as specified here; it is not a statement about unmeasured physical transition rates.
