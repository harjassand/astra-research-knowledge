# Exact sampling of the square-AKLT classical loop gas

## Outcome and boundaries

The supplied program samples the complete routed-loop Gibbs distribution in any finite open rectangular box of the square lattice. It has no loop-length cutoff, no burn-in period, and no time or ancestor cutoff. Every sampling decision uses integer or rational arithmetic and random bits. The finite-state Green function is a proved majorant, not a truncation of physical loops. Its auxiliary torus does not impose periodic boundary conditions on the physical box.

This is a classical norm-loop sample. It is not a prepared quantum AKLT state, a measurement-based computer, a spectral-gap proof, or a proved speed advantage over approximate Monte Carlo. Those claims require separate work. The sampled partition function is the trace/identity component of the open-boundary Gram operator, not the full boundary density matrix. Any physical-observable statement must name the corresponding virtual-identity-boundary AKLT mixture. Infinite-volume local perfect sampling would require a separate local proposal interface and is not implemented here.

The exactness theorem is stated in the ideal independent-random-bit model. The executable uses Python's pseudorandom generator as the practical source, as conventional Monte Carlo implementations do; a fixed pseudorandom seed is not itself a mathematical random-bit source.

## Target measure

A polymer γ is one unoriented cyclically routed, edge-simple closed trail in the box. Its routing at a degree-four vertex is part of its identity. Let Lγ be its edge count and rγ its number of degree-four vertices. Set

wγ = 3^(1−Lγ)(3/5)^rγ.

For two polymers, δγη is zero if they share an edge, and otherwise is (3/5)^k, where k is their number of shared vertices. Set δγγ=0. The target law on finite sets C of polymers is

π(C) = Z^−1 ∏γ∈C wγ ∏{γ,η}⊂C δγη.

The exact same routed gas is already represented in Silva–Schakel–Vasconcelos, Physical Review E88,021301(R)(2013), arXiv:1306.4996, Eq.2, at N=3,K=1. Their worm/satellite-list method handles arbitrary positive N and loop crossings. Thus this is not the first scalable simulation of the model or its open-path correlations. The distinct contribution being assessed is a verified physical-parameter subcriticality regime with exact output and an executable all-length rational oracle, not the loop representation itself.

## Exact unbounded-length birth oracle

The memory-six weighted-trail automaton remembers the last six edges, forbids their reuse, and assigns factor3/5 to remembered second visits of an internal vertex. Forgetting older constraints only increases weights. A rational positive Green supersolution on a16×16 spatial torus obeys

g(s,p) ≥ 1_{p=0} + Σ(s→s′) [a(s,s′)/3] g(s′,p+d),

where a is1 or3/5. build_torus_green.py obtains it by descending, outward-rounded integer iteration from an exact Perron supersolution. torus_loop_birth_sampler.py independently checks every final row and the rotational symmetry used at initialization.

For an initial six-edge prefix, choose weight3^−6 times its remembered contact weight times g at its state and endpoint displacement. Shorter closed loops are included separately. Given state(s,p), use these rational probabilities:

- Stop with probability1/g(s,p), only if p is the torus origin.
- Follow a transition with probability[a(s,s′)/3]g(s′,p+d)/g(s,p).
- Reject with the remaining nonnegative probability.

Every ratio telescopes. A stopped trajectory therefore has precisely its remembered weighted-trail mass, up to the known initial normalization. Reject trajectories that leave the physical box, reuse any physical edge, or end at a nonzero actual displacement. The last rejection removes torus aliases without altering any genuine closed trail.

For a true loop of lengthL and actual contact count r, multiply by3/(2L) and by(3/5)^(r−r_remembered). This is a valid acceptance probability. Each placed loop has exactly2L rooted oriented encodings, including self-touching routed loops. Their total birth intensity is therefore exactlywγ.

The resulting proposal rate per lattice vertex is the exact rational

66455976045001 / 250482492702720 ≈0.2653118600343574.

The original all-endpoint oracle is retained as an independent implementation; its rate is about59.376 per vertex. The closure-aware oracle reduces this overhead by about224 times.

## Marked loss-network construction

Give each proposed cylinder an independent mean-one exponential lifetime. For every earlier/later pair of nonnull cylinders, assign an independent conflict mark with probability1−δγη. A later birth is accepted exactly when none of its accepted, still-alive predecessors has a conflict mark with it.

Fresh birth marks are independent of all prior acceptance decisions. Thus the accepted birth rate ofγ iswγ∏η∈Cδγη, while each accepted polymer dies at rateone. Detailed balance with the target measure is immediate. Multiple proposed copies of a loop are permitted, but their conflict probability isone, so accepted configurations contain at most one copy.

Generic loss-network perfect simulation is prior work, for example Ferrari–Fernández–Garcia, Stochastic Processes and their Applications102(2002),63–88, https://doi.org/10.1016/S0304-4149(02)00180-1 and https://arxiv.org/abs/math/9911162. The global reverse birth/death-clan skeleton is also prior work: van Lieshout–Stoica, Computational Statistics & Data Analysis51(2006),679–698, Algorithm2, https://doi.org/10.1016/j.csda.2006.02.023 and https://ir.cwi.nl/pub/11581/11581D.pdf. The soft factor1−δ in the ancestor bound is justified here by independent pair marks, not by silently applying a dependence-indicator bound that chargesone for every nontrivial interaction.

## Exact backwards algorithm without continuous-time arithmetic

Let λ be the known proposal rate times the number of lattice vertices. Null proposals are retained as cylinders in the dominating process.

At timezero, initialize the dominating population from its stationary Poisson(λ) law and independently attach the birth-oracle marks. All nonnull candidates alive at timezero are the target roots of the ancestor search.

The stationary immigration/death process is reversible. Moving backwards, at population sizeK:

- Add an independent candidate with probabilityλ/(λ+K).
- Otherwise remove a uniformly chosen active candidate.

A backwards removal reveals that cylinder's forward birth. If the cylinder is needed, all active candidates remaining at that moment are exactly the older cylinders overlapping its birth. Query their independent conflict marks, record conflicting predecessors, and mark them as needed. Unneeded removed cylinders can be discarded.

Stop when the births of all needed cylinders have been revealed. Process the recorded graph from oldest to newest, accepting a cylinder if none of its accepted predecessors conflicts. Return the accepted target cylinders alive at timezero.

Only event ordering matters; continuous holding times are integrated out exactly. Poisson(λ) is sampled by splittingλ into integer and fractional parts, then using exact alternating-series bounds for exp(−r), r≤1, together with lazy uniform bits. There are no floating-point Poisson parameters or event-time comparisons.

The implementation's vertex index changes only how potentially overlapping active parents are found. Null cylinders remain inK and uniform removal. Thus the index does not alter the dominating process or its law.

For every finite box, the dominant finite-rate immigration/death process visits its empty state almost surely, so the backwards search terminates almost surely even without the quantitative contraction theorem. The contraction below supplies useful size-dependent bounds instead of relying on this very weak recurrence argument.

## Quantitative ancestor bound

The independently certified tilted raw condition is

Ση wη(1−δγη)e^(μLη)Lη ≤ q Lγ,

with q<0.996411 and μ=log(1000001/1000000)>0. The separate theorem/certificate in square_aklt_operator_bridge_20261105 documents all loop, contact, coverage, and spatial-return bounds.

Consider any backwards ancestral path. Birth times strictly decrease, so all its cylinders are distinct. The Poisson factorial-moment formula and independent pair marks give a product of wη(1−δγη). Integrating each required lifetime over its positive time gap givesone. Therefore expected weighted generationn is at mostq^n times its root weight. This argument does not incorrectly assume that different branches or repeated parent discoveries are independent.

For R=Σγ⊂box Lγwγ, the expected total clan weight is at mostR/(1−q), and its expected cardinality is at mostR/[4(1−q)]. The certificate's excursion bounds imply R<0.299600N for N lattice vertices. Consequently expected clan size is less than20.870N. This is a conservative certified bound, not the measured constant.

For0<θ<1−q, integrating exp(θ·age) over each temporal gap gives the tail bound

P(backwards physical-time depth>t) ≤ R/[4(1−q−θ)] exp(−θt).

For θ=(1−q)/2 this has decay rate0.0017945 and prefactor below41.739N. The small margin makes this worst-case certificate loose. Actual code also pays for null proposals, the stationary Poisson seed, birth-oracle trajectories, and parent queries; clan size alone is not an operation count. Those costs and empirical scaling are reported separately and are under independent audit.

## Exact and empirical checks

The complete3×3box has12physical edges and17 routed loop types. All224 rooted oriented encodings were independently checked as exact Fractions for both birth oracles. Total physical birth intensity is1837/10935. Exhaustive configuration summation gives

Z=2558/2187,

E[number of loops]=1873/12790.

The original full sampler produced mean0.1465 in2,000 independent samples, matching the exact mean within sampling error. This empirical check is a diagnostic; exactness rests on the construction and rational normalization checks.

Meaningful-size benchmarks use the full physical loop model, not the17-type catalog or a cutoff. The catalog is used only for the complete tiny-box comparator.

## Total dominant-event work

Let θ=(1−q)/2, C=R/[4(1−q−θ)], and λ be the proposal rate for the whole box. Stationarity gives K_t~Poisson(λ). For the backwards stopping depthT, Cauchy–Schwarz bounds

E[(λ+K_t)1_{T>t}]≤2λP(T>t)+sqrt(λP(T>t)).

Integrating the established tail gives

E[number of reverse events]≤{2λ[log_+ C+1]+sqrt(λ)[log_+ C+2]}/θ.

This charges null candidates and is O(N logN), with a loose constant set by1−q. Initial Poisson proposals have meanλ and are additional. check_work_bounds.py supplies conservative exact-rational event-count bounds by replacing the logarithm and square root with explicit integer upper bounds. For256×256 it gives an expected-event bound below447,473,944, versus495,113 events per sample in three measured runs. The gap between proved and observed costs must not be concealed.

This is not a bit-operation bound: variable-length trajectories, set operations, canonicalization, exact rational/random-bit arithmetic and Poisson initialization cost more than one operation per event. Physical paths in an open finite box cannot exceed its edge count, so those costs have finite polynomial worst-case bounds per successful path; the implementation rejects edge reuse immediately. A sharper total bit-complexity bound is not claimed.
