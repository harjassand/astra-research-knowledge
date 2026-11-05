# Exact query-local sampling of the square-AKLT routed-loop gas

## Claim and scope

For any finite nonempty vertex set K in the square lattice, the construction below returns the **joint collection of all accepted loops meeting K**, with the stationary infinite-volume routed-loop-gas law. It also works in any finite open rectangular box containing K, by suppressing every loop leaving that box. There is no spatial, time, ancestor, or loop-length cutoff, and no burn-in. All choices that affect the output law use integer/rational probabilities or almost-sure exact comparisons of lazy real variables.

The mathematical exactness statement uses independent ideal fair bits. The included seeded pseudorandom implementation is reproducible, not a claim that a finite seed is an ideal source of independent randomness. Each `sample()` call constructs a fresh joint marginal. Different calls are independent draws, **not consistent pieces of one already sampled infinite configuration**. Extending an already returned sample adaptively is not implemented.

This samples a classical norm-loop gas. It does not prepare an AKLT quantum state, prove a quantum gap, certify uniqueness of all quantum ground states, or sample the continuous O(3) spins. The physical pair-correlation consequence below is a specified thermodynamic limit of virtual-identity-boundary AKLT mixtures.

Implementation: `local_perfect_sampler.py`, `local_birth_oracle.py`, `exact_lazy_time.py`. Exact local-oracle and lazy-time tests: `primitive_checks.json`. The residual-Poisson induction, implementation and exact primitives have passed independent review. A retained early finite-law screen had a selected rare-category deficit; the pre-registered fresh2,000,000-draw main-engine check found770 events versus781.861 expected, exact two-sided p=.693942, so the selected deficit was not reproduced. Independent geometric-exposure and birth-frequency checks also pass. These statistical checks supplement the proof and code audit; nonrejection is not itself a correctness proof. Further stress-test receipts are recorded in the independent audit bundle.

## 1. Model and acquired certificates

A polymer gamma is an unoriented cyclically routed, edge-simple closed square-lattice trail. Vertices can be visited twice. The route, not merely its edge set, records the pairing at each four-valent vertex. Its length is L_gamma and the number of four-valent vertices is r_gamma. Its activity is

    w_gamma = 3^(1-L_gamma) (3/5)^r_gamma.

Two loops have pair factor delta_gamma,eta = 0 if they share an edge, and otherwise (3/5)^c, where c is their number of common vertices. In particular a loop excludes another simultaneous copy of itself. In finite volume the probability of a configuration C is proportional to

    product_gamma w_gamma product_{unordered pairs} delta_gamma,eta.

The scalar partition function is the identity/trace component of the square-AKLT boundary Gram operator, not the full boundary operator.

The separately checked exact-arithmetic certificate in `../square_aklt_operator_bridge_20261105/RAW_LOOP_CONTRACTION_THEOREM.md` proves, with mu=log(1000001/1000000)>0,

    sum_eta w_eta (1-delta_gamma,eta) exp(mu L_eta) L_eta
        <= 0.996411 L_gamma.

The raw kernel includes the identical-loop self-exclusion. The later `SHORT_TAIL_GREEN_THEOREM.md` proves the stronger type-weighted contraction q_A <= 453903/500000 = 0.907806, with a_gamma=L_gamma v_type, v_type>=0.711122124 for short loops and v_type=1 for loops of length at least14. These are all-length statements, not truncations of the loop catalog.

The same certificates bound the total rooted length intensity:

    sum_{gamma meeting K} L_gamma w_gamma
      <= |K| (S_2+T_2+M_4) < 2.260657079 |K|.

These bounds imply almost-sure finite backward ancestor clans by the Mecke ancestor-path first-moment argument. This argument does not assert an unjustified independent branching-process domination of the full explored clan.

## 2. Exact local birth oracle

The oracle of `local_birth_oracle.py` has rational proposal rate

    lambda_local |K|,
    lambda_local = 66455976045001/166988328468480 < 0.397967791.

Its null outcomes are retained in this proposal rate. For every routed loop gamma meeting K, its non-null output intensity is exactly w_gamma.

The oracle is a killed Doob transform of an exact rational Green supersolution on a memory-six trail automaton and an auxiliary16x16 spatial torus. The torus is a **proposal majorant only**. Nonzero actual displacement is rejected, as are globally repeated edges and exits from the requested physical open box. The memory relaxes forgotten restrictions and counts only remembered self-contacts; a final rational correction restores the missing contact factors. No unbounded path is truncated.

For a loop gamma, let k_K(gamma) be its number of cyclic visits to K, counting a twice-visited vertex twice. There are exactly 2k_K rooted oriented encodings based in K. Multiplying the original raw rooted rate by3/2 and accepting the final proposal with

    (1/k_K) (3/5)^(r_true-r_remembered)

therefore gives intensity w_gamma. All793 routed loops in the complete4x4 box, all21,288 rooted oriented encodings, and four different query sets were checked as exact fractions. This includes crossed routes, root revisits and long encodings.

## 3. Stationary marked cylinder construction

For every loop eta, put births on the real time line at rate w_eta. Each birth has an independent exponential mean-one lifetime. A cylinder d consists of its loop eta_d, birth b_d, and death e_d. The base Poisson intensity is

    mu(d) = w_eta db exp(-s) ds,  s=e_d-b_d>0.

An older cylinder d is a potential parent of a newer cylinder c if b_d < b_c < e_d. For every overlapping unordered cylinder pair, expose one independent conflict mark with success probability1-delta(eta_d,eta_c). The older cylinder is a conflict parent precisely when this mark succeeds. Marks belong to cylinder pairs, not loop types, and are reused whenever the same pair is encountered again.

Process a finite ancestor clan from older to newer births. Accept c if none of its accepted conflict parents is present at its birth. Conditional on the currently accepted configuration, the accepted birth rate of eta is w_eta times the product of all its pair factors with active accepted loops; death rate is1. The finite-volume detailed-balance ratio is exactly that of the loop gas above. The subcritical ancestor construction defines the consistent infinite-volume stationary law.

A local query at time0 asks for all accepted cylinders alive at0 whose loops meet K. The number of such **candidate** roots is finite; they are not necessarily accepted after cleaning.

## 4. Conditional unexplored-Poisson invariant

This is the essential overlap/deduplication step. It must not be replaced by independent parent draws for each child.

Let B0 be the set of cylinders alive at0 with loops meeting K. First expose all of B0 using the exact local oracle and independent backward/forward exponential ages. All of these roots are stored, including those later rejected by cleaning.

After querying the stored children c_1,...,c_m, the as-yet-unrevealed cylinder process, conditional on the exposed history, remains Poisson with intensity

    mu(d) 1_{d not in B0}
      product_{j: b_d < b_cj < e_d} delta(eta_d,eta_cj).

For a fresh child c, split this residual intensity into its marked conflict-parent part by multiplying by

    1_{b_d < b_c < e_d} (1-delta(eta_d,eta_c)),

and the new residual by the complementary factor. Independent marked-Poisson thinning proves the invariant inductively, including adaptive selection of each next child from the revealed queue.

The implementation realizes this split as follows.

1. Reuse every already stored older cylinder covering b_c. Query a fresh pair mark only if that pair's mark has not already been exposed. Store the resulting parent edge if the mark succeeds.
2. Generate an independent dominating alive-at-b_c cylinder process from the local oracle queried on V(c), with birth b_c-Exp(1) and death b_c+Exp(1). Thin by the current conflict probability1-delta.
3. Reject any fresh proposal lying in B0.
4. For each previously queried child whose birth the proposal covers, thin by its delta factor. Retain only proposals that pass all these tests. Their already tested conflict marks against the previous children are stored as false; the current child's mark is stored as true.
5. Append each retained fresh cylinder with a new identity, and append c to the queried history.

Rejected fresh proposals are **auxiliary samples used to generate the residual process**, not newly exposed atoms of the original process. They are forgotten. Existing actual atoms are handled separately in step1. In particular, a proposal rejected by a prior-region test must not be matched to an old object or retained as an additional old atom.

The disjoint marked classes, not comparison of floating timestamps, prevent duplicates. Distinct births of the same geometric loop remain distinct cylinders. The strict birth order makes the dependency graph acyclic even when the queue is queried FIFO. Topological cleaning is therefore sufficient and avoids sorting additional real times.

## 5. Exact times and termination

An exponential variable is represented as -log(U), with U an independent uniform variable whose binary digits are exposed only as needed. Times are rational linear combinations of these atoms. Rational logarithm enclosures use range reduction to[1,2] and the positive atanh series with a rigorous geometric remainder.

To compare two times, cancel shared symbolic atoms first. If the difference is a rational constant, compare it directly. Otherwise refine the rational enclosures until strict separation. Every nonzero fixed rational combination of independent continuous atoms is nonzero almost surely. There are countably many comparisons, so all comparisons terminate almost surely. This remains valid under adaptive exposure of the independent bit streams. No finite-precision tolerance or guessed ordering affects the sample law.

The all-loop ancestor contraction gives a finite clan almost surely. Every cylinder has finite length almost surely under the local oracle, and every lazy-time comparison terminates almost surely. Thus the entire local algorithm terminates almost surely. There is no finite deterministic worst-case running time.

## 6. Complete resource scope

The type-weighted first-moment calculation, using the exact quantities above, gives the conservative per-query bounds

    E total retained clan length <34.481635 |K|,
    E retained clan cylinders <6.539013 |K|,
    E all oracle calls, including null proposals <14.120548 |K|.

The last line includes seed proposals and all parent proposals, not just accepted cylinders. It follows by charging lambda_local |K| at seeding and lambda_local |V(gamma)| <=lambda_local L_gamma at each queried cylinder.

The exact checker `certify_oracle_work.py` separately bounds every oracle call. Let rho=709007/750000 and

    D=554813895823645700970207/43738339027847429295092.

If T is its number of continuation transitions after the prefix of at most6 edges, then

    P(T>=n) <= min(1,D rho^n).

This follows from the memory-six Collatz vector lifted constantly over spatial/orientation states, and cancellation of Green factors in the prefix mixture. The bound drops below1 at n=46. Exact rational summation gives

    E(6+T) <68.489,
    E(6+T)^2 <5007.216.

Thus the geometric certificate alone bounds expected attempted walk steps, including proposals ultimately rejected, by968|K|. A sharper exact spatial resolvent certificate in `certify_oracle_work_sharp.py` verifies H>=g+QH by integer arithmetic and averages the actual prefix mixture. It gives fewer than12.145771 expected walk steps per loop proposal, hence fewer than172|K| total expected loop-walk steps. The nearest-neighbor source-path proposal has expected walk length below5.801433, so the entire physical attempt requires fewer than97 local birth-oracle proposals on average. One final continuation decision per call is additional. The geometric second moment remains available to pay the quadratic-length route-canonicalization proxy in the current implementation. The sharper resolvent and prefix-averaging constants were independently re-executed and audited.

These statements **do not yet equal an O(|K|) bit-complexity or wall-time theorem**. Costs also include query sorting, geometry/set intersections, scans through previously queried children, pair-mark caching, symbolic time expressions, arbitrary-precision rational arithmetic and random-bit generation. Previous-region scans can be quadratic in the realized clan size. The independent discovery-forest resource proof now gives the explicit joint MGF bound E exp(10^(-8) A +10^(-8) P) <= exp(0.000002039 |K|), where A is total retained type weight and P counts all proposals, including nulls. Its proof charges a fresh independent parent-proposal PPP before any previous-region exclusions, completes rejected offspring by phantom subtrees, and uses the tilted type-kernel supersolution. Known atoms add edges but no discovery-forest nodes. Consequently known-pair, previous-region, geometry and sorting work have finite polynomial moments; this is not based on an assumed independent full ancestor DAG. The independent proof and exact arithmetic are in LOCAL_RESOURCE_PROOF.md and certify_local_resources.json in the separate audit bundle. The separate LAZY_TIME_COST_PROOF.md also gives qualitative finite expected lazy-time arithmetic for this implementation: newly created timestamps have conditional densities at most1, giving a union bound on close pairs; the proposal MGF controls how many timestamps exist. Consequently the required precision and symbolic/rational arithmetic have finite moments. The Poisson primitive is charged separately with an explicit polynomial arithmetic degree and finite first/second cost moments. This closes finite expected arithmetic for each fixed finite query, but does not give a useful small constant or linear bit complexity in query size. Coordinate bit length also matters even though enclosing volume and distances do not appear in the proposal-count bounds.

Measured diagnostics are recorded in `local_query_benchmarks.json`. On one shared-host run,2000 one-vertex Z² queries averaged0.56ms,2000 adjacent-pair queries1.20ms,2000 queries at two vertices a million lattice units apart1.54ms, and100 queries of an8x8 vertex set11.4ms. These are measurements, not latency guarantees. A same-seed translation test verified100 samples exactly under a billion-unit translation.

## 7. Finite-volume coupling and physical pair limit

Use one master marked Poisson process for the infinite lattice and restrict its births to loops inside each expanding open box. For a fixed finite query K, its full infinite ancestor clan is almost surely finite, with finite spatial support. Every sufficiently large box contains that whole clan. Removing all births outside such a box therefore changes neither the queried candidates nor their cleaning. The finite-box queried loop configuration eventually equals the infinite one almost surely under this coupling, hence converges in total variation.

For distinct spin-2 sites i,j, the separately audited finite-box virtual-identity-boundary state satisfies

    <S_i dot S_j> = 9 (-1)^parity(i,j)
      sum_{routed open paths p:i to j} 3^(-L_p)(3/5)^(r_p)
      E_loop[product_gamma delta(p,gamma)].

The exact all-lattice open-path oracle has a finite rational majorant C. Draw a path first; invalid or out-of-box paths return0. For a valid path query all its vertices together using this local sampler, then evaluate the exact product of its contact factors with the returned loops. The resulting signed estimator is bounded in magnitude by9C and has exactly the finite-box expectation above. No estimate of a partition-function denominator is divided into another estimate: the normalized perfect loop draw handles that denominator exactly.

Use the same all-lattice path proposal and the same independent master cylinder process for every finite box. The sampled path and its entire queried ancestor clan are finite almost surely, so the bounded estimator is eventually identical as the boxes expand. Bounded convergence proves that the box=None estimator computes the **thermodynamic pair-correlation limit selected by expanding virtual-identity-boundary AKLT mixtures**. It does not prove uniqueness under arbitrary quantum boundary states. Quadrupole observables depending directly on finitely many queried loop incidences converge by the local coupling without the path argument.

For nearest neighbors, the current path majorant is

    C=301805115576299/500964985405440.

Independent complete attempts give Hoeffding confidence intervals of half-width

    9C sqrt(log(2/delta)/(2n)).

`exact_confidence.py` rounds the displayed endpoints outward using rational arithmetic. At95% confidence and additive precision0.01, the rigorous bound requires542236 independent attempts. This is an equal-time spin correlation; sums of such correlations give an equal-time structure factor, **not** a Kubo/static susceptibility.

## 8. Strongest comparison and attribution

The routed O(3) gas itself, including crossings and open-path correlations, is exactly the N=3,K=1 case of Silva, Schakel and Vasconcelos, Physical Review E88,021301(R)(2013), arXiv:1306.4996. Their worm/satellite-list simulation is a directly relevant incumbent. Generic backwards ancestor perfect simulation is due to Ferrari, Fernandez and Garcia, Stochastic Processes and their Applications102(2002)63-88, arXiv:math/9911162. The global reverse birth/death-clan skeleton and incompatibility indexing also appear in van Lieshout and Stoica, Computational Statistics & Data Analysis51(2006)679-698.

The scoped operation here is the **verified square-AKLT-parameter contraction together with an executable exact all-length local loop oracle and local physical readout**. It is not a claim of inventing ancestor sampling, the loop representation, worm observables, or the first scalable classical simulation. No speed advantage over the2013 worm has been established. The measured advantage over our own global exact sampler is the removal of enclosing-volume work and finite-box bias for the specified local limit, at the cost of exact local exploration. Generic exact local samplers require a realizable intersecting-object oracle and a certified subcriticality regime; those inputs are supplied here for this particular model.
