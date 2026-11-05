# Independent audit of query-local perfect sampling

## Mathematical construction

The proposed algorithm is valid under the ideal independent-fair-bit specification, subject to the established finite-clan certificate. It does not sample parents independently for each child. Its conditional residual-Poisson construction is the essential coupling.

Let a cylinder d consist of a routed loop, birth time b_d and death time e_d. The free intensity is w_gamma db exp(-l) dl, l=e_d-b_d>0. At any fixed time t, cylinders alive at t have loop intensity w_gamma and independent age/residual lifetime Exp(1). This follows by the change of variables a=t-b, r=e-t, whose density is exp(-a-r).

Seed every free cylinder alive at0 whose loop meets the finite query K. Let B0 be this entire seed region. After querying children c1,...,ck, the unrevealed cylinders form a conditionally Poisson process with intensity

mu(d) * 1_(d outside B0) * product_r delta(c_r,d)^(1_(b_d < b_cr < e_d)).

At a new child c, split this residual process by its independent conflict mark, whose probability is1-delta(c,d). The retained part is the newly revealed parent process; the complementary intensity acquires the additional delta factor. These are disjoint marked-Poisson classes. A retained new parent necessarily has false conflict marks against every earlier queried child it covers, and these marks must be cached. Existing revealed atoms are tested separately using their already exposed or fresh pair marks.

Thus different child queries share actual cylinder objects rather than independently redrawing shared ancestors. Rejected fresh candidates are auxiliary proposals, not exposed background cylinders retained in the conditioning history. Forgetting them is correct for this splitting construction. In contrast, a geometric-region algorithm that reveals all cylinders must retain its soft-nonconflicting cylinders; the independently coded reference does so.

A cylinder with the same loop route but a different birth/death time is a distinct Poisson atom. Route-based deduplication would be wrong. Exact equality of separately generated continuous birth times has probability zero. Every true parent is strictly older than its child, so the final dependency graph is acyclic. Topological oldest-parent-first cleaning gives the same result as sorting every continuous time.

## Code checks

Reviewed files: local_birth_oracle.py, exact_lazy_time.py, local_perfect_sampler.py.

- Seed exclusion is correct: all discovered parents have negative birth times, so meeting K and having positive death time is exactly membership in B0.
- The queried-history list excludes the current child until its fresh-parent generation is finished.
- New retained parents cache false prior marks and the true current-child mark. The unordered pair key is appropriate because each overlapping pair has only one older-to-newer birth direction.
- Known atoms are filtered by strict lifetime coverage before their cached marks are used. FIFO exploration is valid; it need not follow chronological birth order.
- All retained new ancestors are queued exactly once. Existing shared ancestors are reused. Cleaning uses only actual conflict edges and checks acyclicity.
- The spatial index includes all retained known cylinders, not merely those alive at time0. This is required for queries at past birth times.
- No physical-box, path-length, time or ancestor cutoff was found. A box argument changes the requested ensemble by excluding loops not wholly contained in that box; box=None uses the infinite lattice.

## Local birth measure

The raw closure-aware rooted proposal has rate Lambda0 per vertex. For finite K, the local oracle uses rate(3/2)Lambda0|K|. A loop gamma has exactly2k_K rooted/oriented encodings with roots in K, where k_K=sum_(v in K)m_v counts visits, not distinct vertices. Final thinning by(3/5)^(r_true-r_mem)/k_K therefore yields exactly3^(1-L)(3/5)^r_true=w_gamma.

The implementation counts k_K with multiplicity. Finite-box rejection preserves the same normalizer. The torus Green table is only a proposal device; nonzero actual return displacements are rejected. Previously audited exact integer supersolution rows make every transition and killing probability valid. Primitive checks cover every local loop intensity on3x3 and4x4 graphs for four query sets, including diagonal two-corner queries.

## Exact times and termination

Lazy exponential atoms use -log(U), with U revealed in fair-bit blocks. Rational range reduction and a positive atanh series with a geometric tail enclose logarithms. ExactTime keeps rational linear combinations of shared atoms, cancels identical terms symbolically, and refines until an ordering is proved. Nontrivial comparisons terminate almost surely because distinct continuous linear combinations tie with probability zero. No floating-point value determines an ordering.

The certified raw ancestor contraction below1 gives an almost surely finite complete clan for each finite query. Each loop route is finite almost surely, and each local Poisson proposal count is finite. Thus the sampler terminates without truncation. Bounds on expected logical ancestor/oracle counts are not automatically bounds on every rational bit-operation cost; benchmark timing and complexity claims should distinguish them.

## Finite/infinite physical join

Use one master marked Poisson cylinder field. The full infinite ancestor clan of any fixed finite query is almost surely finite and has finite spatial support. Every sufficiently large open box contains that support. Restricting the field to loops contained in the box then leaves the query output unchanged. Hence finite-open loop marginals eventually agree under this coupling and converge in total variation.

For a source-path correlator, first draw one finite all-lattice path proposal with the same fixed normalizer C in every volume. Couple finite boxes by rejecting a path outside the box. Eventually both the path and its independent query clan fit. The readout bounded by9C is then eventually identical, and bounded convergence proves the thermodynamic pair-correlation limit selected by virtual-identity boundaries. This does not establish uniqueness of arbitrary quantum ground states, a gap or a Kubo response.

Each sample() returns a joint marginal on its complete specified query. Separate calls are independent marginals, not consistent pieces of one stored infinite configuration. A pair observable must query both sites together; a path suppression must query all vertices of that path. Adaptive extension of an already returned sample is not implemented.

## Independent checks and prior art

An independent full-geometric-exposure reference sampler is in geometric_reference_sampler.py. It reveals every cylinder in each geometric parent region, reuses known atoms, excludes previously revealed regions, and queues only true marked ancestors. This is a deliberately different exposure implementation for comparison with the soft-complement method.

The exact3x3 finite loop law has20 configurations. Its two-corner projection has15 categories. Independent statistical screens and their raw outcomes are retained, including an initially unusual rare-category deficit. They are diagnostic checks, not the proof of exactness; final status is recorded with the completed results.

Local infinite-volume ancestor sampling is established prior art. Ferrari, Fernandez and Garcia, Stochastic Processes and their Applications102(2002),63–88, present finite-window perfect simulation from marked Poisson ancestors and subsequent cleaning: https://arxiv.org/abs/math/9911162 . Marked-point-process extensions and other perfect samplers also predate this work. The specific acquired contribution is the all-length square-AKLT loop birth oracle, verified subcritical regime, exact arithmetic and implemented observable interface, not a new generic principle of local perfect sampling.

## Completed diagnostic record and signoff

The first main-engine run had100,000 samples. The exact two-corner marginal has15 categories; its empirical total variation was0.001145. A selected rare length-eight route occurred18 times against39.093 expected. A second independent-seed500,000-sample run had160 against195.465 expected for that route, with total variation0.000524. Both runs are retained. Selection across categories matters: these exploratory deviations were not a pre-registered single-hypothesis test.

A separately implemented geometric-exposure engine then generated500,000 samples. Its full marginal total variation was0.000339, every category was within1.61 marginal standard deviations, and the flagged route had179 against195.465 expected. An independent1,000,000-proposal birth test had568 against574.478 expected for the route. These checks support the primitive/reference consistency, but alone do not rule out a main-engine bias.

Therefore a fresh main-engine check was pre-registered before drawing:2,000,000 samples, seed1168304679, the fixed target route, exact probability1/2558, and a two-sided binomial diagnostic at alpha0.01. It produced770 events against781.861 expected, with p=0.693942. The exploratory deficit was not reproduced at the pre-specified diagnostic threshold. The99% Clopper-Pearson interval for this one probability is approximately[0.0003502073,0.0004221921]; it does not exclude arbitrarily small bias or establish other marginals.

The first execution of this fixed batch completed but failed while serializing a library boolean, before any count or p-value was displayed. The same frozen code/seed/random sequence was replayed with only serialization repaired and a raw-count checkpoint added. This was not a newly selected random batch. The failed runner and replay metadata are retained.

Implementation signoff rests on the mathematical residual-Poisson invariant, code review, exact primitive identities, independent exposure implementation, and these diagnostic tests together. Nonrejection is not proof of exactness. The finite probability precision claim remains conditional on the proved algorithm and ideal independent-fair-bit specification. The reviewed main sampler SHA256 is6e6e4c0e7fb7c2d366a47effbbbb4c53257bbb0ec8ac5421b88b2d23840baf5d.
