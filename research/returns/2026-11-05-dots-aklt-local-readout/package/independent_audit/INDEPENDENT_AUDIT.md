# Independent audit: square-AKLT classical perfect sampler

## Finding

No correctness defect was found in the finite-open-box birth normalization or reverse marked-ancestor construction. An independently generated 4×4 enumeration verifies all 1,504 routed configurations and 21,288 rooted/oriented encodings of 793 distinct loops, including length 20 and four self-contacts. This is stronger finite testing than the original 3×3 catalog, but the all-size guarantee rests on the telescoping and ancestor arguments, not enumeration.

The result is a classical exact equilibrium sampler. It is not a quantum-state preparation, a measurement-outcome sampler for the AKLT state, a boundary-operator reconstruction, or a quantum gap proof. No speed or practical scientific advantage over the strongest same-target worm method has been established.

## 1. Target and finite-volume normalization

For a finite open rectangular grid, let a configuration be a set of routed, undirected, edge-simple closed trails. Trails may share vertices but never edges. Each cyclic route is identified under cyclic shifts and reversal, not under translations or rotations of the actual box. With L edges and r four-leg self-contacts, its activity is

    w(gamma) = 3^(1-L) (3/5)^r.

Two different loops have interaction delta=0 if they share an edge, and delta=(3/5)^k if they share k vertices. The configuration law is proportional to product w times product delta. No 1/n! belongs in this finite set-of-types expression. Poisson cylinders do have labels and repeated proposed types, but shared-edge exclusion ensures the accepted state has at most one of each type.

Independently enumerating even edge subsets using a plaquette cycle basis, then all three pairings at every four-leg vertex, gives the direct local tensor weight

    3^(number of loops) (1/3)^(number of degree-2 vertices)
      × (1/15)^(number of degree-4 vertices).

Every enumerated configuration agrees exactly with the polymer expression. In particular:

- 3×3: 16 even subgraphs, 20 routed configurations, 17 loop types, Z=2558/2187.
- 4×3: 64 even subgraphs, 104 routed configurations, 72 loop types, Z=224900/177147.
- 4×4: 512 even subgraphs, 1,504 routed configurations, 793 loop types, Z=2581273672/1793613375.

These are the closed-loop scalar Z^emptyset, with the empty diagram assigned weight one. In the standard boundary expansion, this is the identity coefficient, proportional to the trace of the boundary Gram/density operator after conventional scalar factors. It is not the full boundary operator. Open strings are required for the other coefficients.

Primary normalization: Martyn–Kato–Lucia, Eq.16, https://arxiv.org/html/1912.10327 .

## 2. Exact birth oracle

The prefix proposal intensity, continuation probabilities and stopping probability telescope. Each admitted rooted/oriented route has pre-thinning intensity 3^(-L)(3/5)^r_memory. Multiplication by 3/(2L)(3/5)^(r_true-r_memory) yields w/(2L). There are precisely 2L encodings of an edge-simple undirected routed loop, including repeated vertices. Thus the physical loop's total birth intensity is w.

The torus Green array is an integer supersolution, not an approximation used directly as an unverified probability. Each row is checked at construction. Slack is assigned to null proposals. Stopping is restricted to torus displacement zero, and nonzero actual displacement is rejected. The torus therefore guides proposals without changing the finite-box physical target. Repeated edges and box exits are rejected. No imposed physical length cutoff occurs.

Our independently generated 4×4 loop catalog passes all 21,288 exact rational encoding checks. This checks the actual implemented prefix/transition/stop/accept choices, not only the abstract formula. The longest physical loop in this box is 20; maximum four-leg contact count is four. Total physical birth intensity is 3618010841/8968066875.

The fixed torus oracle uses 234,496 integer entries, about 1.79 MiB uncompressed and 556,578 bytes compressed. Its saved build record reports 11.59 seconds. Constructor validation took 0.052–0.093 seconds in our runs. Those costs are separate from per-sample timings. Runtime uses only integer/rational random decisions, assuming an ideal independent random-bit interface; seeded Python PRNG runs are reproducible simulations of that interface.

## 3. Reverse ancestor construction

The dominating marked immigration/death process has immigration rate lambda=0.2653118600343574 times the number of vertices and unit death rate per cylinder. Its stationary population is Poisson(lambda). Null proposal marks must remain in the population count; the implementation does so.

In reverse time, immigration has probability lambda/(lambda+K) and deletion selects a uniform active cylinder. A deletion exposes that cylinder's forward birth. All cylinders remaining active at that moment were older and alive at that birth. The code then queries independent pair marks with conflict probability 1-delta. Spatial indexing omits only pairs with zero conflict probability. Marked parents are recursively required. Resolving births in reverse recorded order gives oldest-first cleaning.

A new accepted loop has rate w times the product of delta over accepted older loops; deletion rate is one. This is detailed balance for the target Gibbs weight. Cleaning keeps a record of whether an older ancestor was accepted, even after its death, which is correct because the parent list already encodes overlap at the child's birth. Deleting a non-required cylinder when its reverse death occurs is safe: it cannot be alive at any still earlier birth.

Finite-volume termination does not require q<1. There are finitely many physical loop types and finite dominating immigration rate. The stationary immigration/death process visits zero almost surely, at which point no required ancestor remains. The q certificate is valuable for volume-uniform complexity and infinite-volume constructions, not mere finite-volume existence.

Poisson draws use alternating rational enclosures of exp(-rate), additive independent Poisson(1) draws, and lazy bit refinement. No fixed precision or unresolved-comparison cutoff was found.

## 4. q certificate: reviewed scope

The documented all-loop inequality is

    sum_eta w(eta)(1-delta(gamma,eta)) L(eta) exp(mu L(eta))
      <= q L(gamma),

where mu=log(1000001/1000000) and the exact saved rational q is below 996411/1000000. The self-proposal term is included. The finite-memory majorant, root prefix/suffix filters, degree-four two-excursion bound, Fourier return projection, and left-weight interval residual argument were reviewed. No lost physical path, extra contact penalty, or normalization error was identified. This audit did not re-run the entire 186-second interval solve; the two recorded certified runs and exact saved scalar bound were inspected. Its numerical implementation relies on IEEE-754 elementary arithmetic and outward mpmath interval functions, not a formal proof assistant.

Two important scope restrictions:

1. The theorem is for finite loops on the infinite planar square lattice and its open subregions. The proof absorbs a simple-loop self term using at least four turns. Noncontractible loops on a physical torus or cylinder need separate treatment; they can have no turns. The auxiliary torus in the Green function is not a physical periodic boundary.
2. The implemented program samples a finite box globally. An infinite-volume local perfect sampler would additionally need an interface generating all proposals that intersect a finite queried region, including loops rooted outside it, together with consistent revelation of overlapping Poisson regions. The current code does not implement that interface. The subcritical certificate supports the standard existence/construction argument, but this distinction should remain explicit.

## 5. Full resource accounting

Let N be the number of sites, R=sum_gamma L(gamma)w(gamma), and q be the certified raw ancestor constant. The stated excursion bounds give R<0.299600N. A Mecke sum over all possible chronological ancestral paths bounds expected total ancestor length by R/(1-q), hence expected ancestor count by R/[4(1-q)]<20.870N. This first-moment argument does not require treating the dependent, merging actual clan as an independent Galton–Watson tree.

Let T be the maximum backward birth age reached by a target's clan. For 0<theta<1-q, exponential lifetime integration along each ancestral path yields

    P(T>t) <= min(1, C exp(-theta t)),
    C = R/[4(1-q-theta)].

This includes the initial target cylinder's age. Choosing theta=(1-q)/2 is valid. These are conservative bounds, not measured practical stopping times.

The current program simulates all global dominant/null events until T, not just actual ancestors. If J is this event count and K_t is the stationary dominant population, the compensator and Cauchy–Schwarz give

    E J = integral E[(lambda+K_t) 1(T>t)] dt
        <= [2 lambda(a+1) + sqrt(lambda)(a+2)]/theta,
    a = max(0, log C).

Here E[(K_t-lambda)1_A] <= sqrt(lambda P(A)); independence between T and K_t is not assumed. The initial Poisson population adds lambda expected proposal draws. Thus this implementation has a justified O(N log N) bound for global event count with fixed model parameters, not an O(N) bound obtained merely from clan size.

At 128×128 the bound is about 70.5 million reverse events versus 137,591 in one independent run. The certified constants are therefore useful for finiteness/scaling but loose as performance predictions. The tiny spatial tilt mu≈10^-6 likewise should not be advertised as a sharp physical correlation length.

Event count is not bit complexity. Proposal generation includes root-coordinate random bits, path generation, repeated-edge checks, and canonicalization that currently materializes O(L^2) coordinate data. Pair testing uses set intersections and integer powers. Finite-memory subcritical path weights have exponential tails, so fixed proposal length moments exist, but a full bit-operation bound or uniform memory-tail bound has not been implemented/tested here. The vertex index reduces irrelevant comparisons substantially. Because every intersecting pair has conflict probability at least 2/5, fresh-mark comparison counts can be related to marked ancestral-edge counts in expectation; this does not remove per-route set and canonicalization costs.

## 6. Independent executions and error

Thirty thousand independent 4×4 samples gave mean loop count 0.3266, compared with exact 0.3305350264; estimated standard error 0.00300227, a 1.31-SE discrepancy. This is a sanity test, not the exactness proof. Sampling took 2.49 seconds, excluding 0.052-second constructor validation.

An independent 128×128 run at seed842156 returned 552 loops, 1,115 ancestors, 786 targets, 137,591 reverse events, 73,142 proposal draws and 799 candidate comparisons. Peak reported RSS was 29.1 MiB. Wall time was 15.19 seconds plus 0.093-second constructor validation. The constructor's separate benchmark averages were about 2.39 seconds on ten 128×128 samples with similar event counts. Shared-host load and per-sample work can differ; the discrepancy was reported rather than replacing either observation. Neither timing is a guaranteed latency or a matched incumbent comparison.

For a bounded observable, independent perfect samples remove finite burn-in and mixing bias, but ordinary Monte Carlo statistical error remains. A finite open box also retains finite-volume/boundary effects when estimating an infinite-volume observable. A perfect sample does not directly return Z, its logarithm, all boundary coefficients, or a rare observable at fixed relative error.

## 7. Strong prior art and practical significance

The strongest directly matched target found is not the 2020 AKLT plaquette-truncation sampler. Silva–Schakel–Vasconcelos, Phys. Rev. E88,021301 (2013), Eq.2, samples routed square-lattice O(N) loops with weight K^b N^loops N^(-v2)[N(N+2)]^(-v4). Setting N=3 and K=1 gives exactly the present local weights, including all three four-leg routings. Its worm and satellite-list method handles the same equilibrium ensemble and open-endpoint correlation observables. It is Markov-chain sampling, not a finite-time perfect sampler. A matched equal-error, equal-boundary-condition runtime benchmark is still missing. Source: https://arxiv.org/pdf/1306.4996 .

The generic reverse-cylinder architecture is also established. Fernandez–Ferrari–Garcia give the ancestor/cleaning method in https://arxiv.org/abs/math/9911162 . Van Lieshout–Stoica's Algorithm2 explicitly implements the global stationary birth/death reverse sweep and incompatibility indexing: https://ir.cwi.nl/pub/11581/11581D.pdf . Those are the appropriate exact-simulation baselines, alongside dominated CFTP, not an assertion that prior methods require arbitrary mixing-time cutoffs.

The potentially distinct result is the explicit certified subcritical regime at the undeformed square-AKLT parameters, an executable exact all-length proposal oracle, and a finite-box exact sample with measured costs. The reduction from about59.376 to0.2653 proposal rate per site compares two new-oracle versions only. It is not a 224-fold improvement over the literature. This audit does not establish priority for the soft pair-mark refinement or the model-specific theorem. Without a consequential observable/decision and a strongest-incumbent comparison, this remains a sound computational-mathematical ingredient rather than a demonstrated transformative capability.

## Reproduction artifacts

- `check_scalar_normalization.py`: independently enumerates finite graphs and pairing weights.
- `scalar_normalization_results.json`: exact finite partition functions and count laws.
- `single_loop_catalog_4x4.json`: independent 793-loop catalog.
- `check_birth_4x4.py`, `birth_4x4_results.json`: exact oracle tests.
- `empirical_4x4.py`, `empirical_4x4_results.json`: 30,000-sample check.
- `measure_128.py`, `independent_128_result.json`: independent resource observation.
- `AUDITED_SHA256.txt`: input versions audited.

All generated audit artifacts are in `/workspace/shared/aklt_independent_full_audit/`.
