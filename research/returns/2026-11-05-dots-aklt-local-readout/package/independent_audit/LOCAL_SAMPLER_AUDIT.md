# Independent adversarial audit of the query-local sampler

## Current verdict

No flaw was found in the all-length local birth normalization, residual marked-Poisson exploration, shared-ancestor handling, lazy-real ordering, or finite-box/infinite-lattice coupling. The mathematical construction passes this audit under the separately certified raw-kernel contraction and ideal independent fair bits.

Implementation statistical validation is a separate check. A rare3x3 category was low in two pilot batches. The fresh preregistered two-million-draw main-engine check then gave770 against781.861 expected, exact two-sided binomial p=.693942, with unchanged source hashes (focused_main_check.json). The pilot results remain preserved rather than discarded. All three independent high-activity finite-support stress tests below also passed their distribution screens. These tests are not substitutes for the mathematical proof.

Audited source hashes are in LOCAL_AUDITED_SHA256.txt. The implementation remains the constructor's unchanged code under square_aklt_local_sampler_20261105.

## 1. Exact local loop measure

For query K, the rate is lambda|K| with lambda=66455976045001/166988328468480. A routed loop has2k_K oriented rooted encodings, where k_K counts cyclic visits to query vertices, including both visits at a four-leg vertex. The final1/k_K correction and the3/2 rate factor cancel exactly to give w_gamma. Replacing cyclic visits by distinct query vertices would be wrong; the implementation uses the correct multiplicity.

The auxiliary16x16 torus is only a positive proposal majorant. Actual closure, globally unused physical edges and finite-box membership are checked in ordinary lattice coordinates. Memory-forgotten contact penalties are restored by the rational correction. The local oracle has no path-length cutoff. Its substochastic continuation chain has a certified geometric survival bound, so proposal generation terminates almost surely with all fixed path-length moments.

The previous independent complete4x4 normalization audit covered793 loop types and21,288 rooted oriented encodings. The all-size guarantee is the telescoping/counting proof, not extrapolation from that enumeration.

## 2. Poisson exposure and shared ancestors

At time0, loop candidates meeting K form a finite PPP with type intensity w. Conditional on being alive at the queried time, backward age and forward residual lifetime are independent Exp(1) variables.

After earlier queried children, the unseen-cylinder intensity equals the original cylinder intensity, outside the seed region, times the product of prior-child delta factors for each old birth time covered. This is a conditional Poisson law. The next child can be selected adaptively from revealed data. Independent thinning against its new pair mark exposes precisely its remaining conflict parents.

The implementation realizes this by generating a fresh dominating parent PPP, rejecting seed-region and prior-region candidates, and remembering false marks against older queries for every retained candidate. These rejected candidates are auxiliary thinning points, not actual old atoms. Existing actual atoms are separately reused by identity. A successful mark is never independently redrawn for a known pair. Strictly decreasing parent birth times preclude cycles; oldest-first topological cleaning is equivalent to sorting all birth times.

This avoids the common incorrect shortcut of independently resampling an entire parent set for each child. Shared ancestors are one cylinder with one acceptance decision, even when they have multiple descendants.

## 3. Infinite-lattice and physical scope

The tilted kernel bound makes every finite query's ancestor clan finite almost surely. Every realized loop and every realized clan has finite spatial support. Coupling finite boxes by restriction of a single infinite marked process therefore gives eventual exact equality of the queried configuration once the whole infinite clan is inside the box. This proves the selected finite-box limit without a guessed boundary distance.

The sampler returns all accepted loops meeting K jointly. Separate calls are independent fresh marginals, not compatible extensions of a previously returned infinite configuration.

The physical consequence is the thermodynamic pair-correlation limit of expanding virtual-identity-boundary spin2 AKLT mixtures, using the already audited factor9 open-path estimator. This does not establish arbitrary-boundary quantum-state uniqueness, a quantum gap, quantum preparation, or a Kubo susceptibility.

## 4. Costs now actually charged

The exact rational certificate in certify_local_resources.py establishes, per query vertex:

- expected retained clan length <34.481635;
- expected retained cylinders <6.539013;
- expected all local birth-oracle calls <14.120548, including nulls and rejected parents.

An implementation-specific discovery forest, completed with phantom offspring, is dominated by the raw Poisson multitype branching process. Known shared ancestors add edges but no new discovered vertices. This yields the joint MGF

E exp(10^-8 A+10^-8 P) <= exp(0.000002039 |K|),

where A is total retained type weight and P counts all proposals. Consequently known-pair and previous-region scans, bounded by M² and MP, have finite expected cost and all fixed counting moments. This argument does not depend on the separate all-order connected-derivative proof.

The constructor's sharper integer resolvent H>=g+QH was independently rerun and audited. Prefix averaging correctly gives E(continuation length)<=H/g-1, then cancels g. Certified mean attempted walk steps are <12.145771 per loop proposal and <5.801433 per nearest-neighbor open-path proposal. Hence loop walk steps are <172|K| in expectation. A full nearest-neighbor physical attempt makes fewer than97 local birth proposals in expectation. The older geometric-tail proof separately pays quadratic-length canonicalization proxies.

LAZY_TIME_COST_PROOF.md gives a qualitative finite-expected-bit-cost argument. Sequentially created timestamps have conditional density at most1, giving control of the smallest separation even under adaptive comparisons. Combined with the proposal-count exponential moment, required log precision has finite moments. The atanh enclosure arithmetic is polynomial in this precision and expression size. The Poisson primitive is separately charged with a concrete coarse arithmetic bound and sufficient first/second moments. Averaging over an unbounded source-path query is justified by the exact rate comparison H<1-rho, where H<.000002039 and rho=709007/750000. No useful numerical bit-cost constant, linear query-size bit theorem, or guaranteed latency follows.

## 5. Independent artificial-gas stress tests

stress_local_poisson_engine.py replaces only the loop birth oracle by an exactly enumerable finite-support oracle; the exposure engine is unchanged. Activities are deliberately much larger than the physical AKLT loop activities, producing many shared ancestors, old-region exclusions and exact-time comparisons.

Completed results are saved in stress_local_poisson_engine.json:

- Mixed hard/soft three-loop gas, activities2/3,3/4,4/5, partial query:3000 samples, all four exact marginal categories within0.85 standard deviations; maximum clan41.
- Soft-contact three-loop chain, unit activities:3000 samples, all four exact marginal categories within1.53 standard deviations; maximum clan73;187.4 time comparisons per sample on average.
- Four-plaquette gas with activity1/2 each, full query:3000 samples, all seven exact marginal categories within1.66 standard deviations; maximum clan62;144.8 time comparisons per sample on average.

An initial overlarge30,000-per-case diagnostic was stopped before output; no result from it is included or claimed. The smaller run was selected for stress coverage, not for a prescribed hypothesis test.

## 6. Strongest same-access comparison and prior work

Silva, Schakel and Vasconcelos2013, https://arxiv.org/pdf/1306.4996, has this exact crossing gas at N=3,K=1 and an open-endpoint correlation observable. Its algorithm is a finite periodic-lattice Metropolis worm. Its numerical study is principally N<=2, not a rigorous iid N=3,K=1 error certificate. Wierschem and Beach2016, https://arxiv.org/abs/1603.03444, directly evaluates AKLT loop observables and explicitly qualifies its Monte Carlo exactness as asymptotic.

Generic exact finite-window infinite-volume ancestor simulation already appears in Fernandez, Ferrari and Garcia2002, https://arxiv.org/abs/math/9911162. Therefore neither ancestor sampling, infinite-volume local sampling, the loop representation nor physical loop observables should be presented as newly invented here.

The scoped capability is an executable exact all-length intersecting-loop oracle plus verified parameter-specific subcriticality and bounded iid physical readout. The targeted primary-source search did not locate the same pointwise finite-sample infinite-volume guarantee, but absence from this search is not a proof of priority. No performance comparison against an implemented2013 worm or2016 AKLT loop code was performed. Any measured speedup over this project's earlier full-box exact code must be labeled as such.
