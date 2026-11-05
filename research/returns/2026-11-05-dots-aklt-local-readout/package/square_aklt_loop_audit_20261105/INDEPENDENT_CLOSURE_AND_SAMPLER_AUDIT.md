# Independent audit of closure bounds and exact loop sampling

This audit concerns the positive routed classical square-AKLT loop representation. It does not establish the quantum spectral gap or a noncommutative boundary response theorem.

## 1. All-loop closure certificate

The implementation reviewed is `../square_aklt_operator_bridge_20261105/certify_geometry_return.py`, with the transfer setup in `fourier_loop_return.py` and the local charge/coverage proof in `ALL_LOOP_CONTRACTION_CERTIFICATE.md`.

The mapping passes the following independent checks.

- Initialization is an actual first-East prefix, not a stationary cyclic trace. Contacts are penalized on arrival at most once for a physical degree-four vertex. Forgetting old contacts and excluding the oldest remembered vertex omit penalties, hence enlarge physical weights. There is no cyclic double-counting problem at lengths between m and 2m.
- A true degree-two-root loop never revisits its root before the final step. It therefore passes both the prefix no-return filter and the terminal memory endpoint-uniqueness filter. Nonphysical long histories passing these filters add only positive mass.
- State orientation is updated by the old history's second direction, after calculating the current displacement in the old orientation. Fourier phases therefore add to the actual endpoint displacement. Modulo-torus closures include all true closures and add nonnegative aliases.
- First-East initialization is invariant under reflection in the horizontal axis. Combining that symmetry with complex conjugation makes the real Fourier output separately even in both Fourier coordinates. The quarter-grid multiplicities are valid despite the fixed first direction.
- The coefficient of a continuation of length k in `(m-1)R+R^2` is m+k. The factor six for degree-two roots is four initial directions times color factor three divided by two rooted orientations at the vertex. Exact lengths at most m do not overlap the resolvent part: the prefix excludes a root return, and the torus side exceeds 2m.
- The resolvent supersolution is a backward one, correctly used as a left weight for the forward transfer. Thus q-weighted residual controls unweighted l1 error. The second-resolvent error bound by its own residual plus max(q) times the first error has the correct orientation and norm.
- The implementation independently checks the actual binary64 supersolution as exact dyadic rationals. Residual coefficient rectangles and arithmetic are outward rounded. This is a computer-assisted interval certificate using IEEE-754 and mpmath interval assumptions, not a proof-assistant verification.

The local interaction constants also pass. D4 averaging gives straight charge S2/5+T2/2 and turn charge S2/2+7T2/20. Coverage of a nonsimple root forces a degree-four target at a selected root contact; coverage of a distinct simple root forces one somewhere on that root. A simple identical-loop term is absorbed by four turning visits when the stated cap gap is at least 3x^4. Artificial upper caps can be used consistently here; subtraction of unknown exact moments is unnecessary.

Cutting a degree-four-root loop gives two first-return excursions. For straight first excursions the second has two starting orientations. For turns those two choices cancel the fixed-final-direction half of the turning class. This gives coefficientwise G4 <= (3/5)(2Gs^2+Gt^2). Root multiplicity four for degree-four roots versus two for degree-two roots yields M4 <= (6/5)Gs S2+(3/5)Gt T2. Extra mutual exclusions and contact penalties between excursions only reduce physical weight.

No conceptual missing multiplicity/contact factor was found in the reported q < 0.996411 all-loop contraction certificate. The separate quantum join remains unproved.

## 2. Exact all-length birth oracle

Reviewed implementations: `exact_loop_birth_sampler.py`, `torus_loop_birth_sampler.py`, and `build_torus_green.py` in the boundary-operation directory.

For the nonspatial oracle, prefix selection has intensity 3^(-m)(3/5)^r q(state). Transition probabilities multiply by weight*q(next)/(3q(current)), and stopping contributes 1/q(final). These telescope to 3^(-L)(3/5)^r_mem for every admitted rooted path. Killing, box exits and repeated-edge rejection remove nonphysical proposals only.

The thinning factor is 3/(2L)*(3/5)^(r_true-r_mem). Prefix root penalties are deliberately omitted. Every other remembered repeat is a true second arrival at a degree-four vertex, so r_mem<=r_true. An edge-simple routed loop has exactly 2L distinct rooted/oriented encodings, including when a vertex is visited twice. Thus summing accepted rooted intensities gives exactly w(gamma)=3^(1-L)(3/5)^r_true.

The torus version replaces q(state) by q(state, displacement modulo L). Its constructor verifies every integer supersolution row and the exact rotational invariance needed by uniform initial orientation. The same telescoping holds. Stopping occurs only at torus origin; rejecting nonzero actual displacement removes aliases and does not change any true loop's intensity. There is no physical loop-length cutoff.

`audit_exact_sampler.py` independently evaluates actual rational prefix, transition, stopping and thinning probabilities for every rooted/oriented encoding in the complete 3x3 box. Both oracles pass all 224 encodings of all 17 routed loops, including crossed length-eight routings. Each encoding equals w(gamma)/(2L), and the exact total birth intensity is 1837/10935. These are exact checks, not Monte Carlo confidence claims.

The ordinary proposal rate is 32439356957172712/546339971648709 per vertex. The closure-aware rate is 66455976045001/250482492702720 per vertex, about 224 times lower. This is proposal-rate improvement against the first oracle, not a claim against every known equilibrium algorithm.

## 3. Full finite-box equilibrium sampler

Reviewed implementation: `perfect_loop_sampler.py`.

The dominant process has constant proposal immigration rate Lambda and independent unit-rate deaths. At time zero its stationary population is Poisson(Lambda), with iid proposal marks, including null marks. Its reversibility means that the past jump chain adds a mark with probability Lambda/(Lambda+K), otherwise deletes a uniform active mark. Continuous waiting times can be integrated out because only overlap and temporal order matter.

A reverse deletion reveals that cylinder's forward birth. Every remaining active cylinder was alive at that birth and was born earlier. Querying independent pair marks with conflict probability 1-delta and recursively including conflicting parents therefore constructs the correct ancestor clan. Null marks stay in K but are never ancestors. An unneeded object can safely be deleted from storage at its reverse deletion because it cannot parent a still-earlier birth. Reversing the list of resolved needed births is oldest-first cleaning.

Conditional on an accepted older configuration, a new physical loop is accepted with probability product delta. Combined with its exact birth activity and unit death rate, this satisfies detailed balance for the desired repulsive loop Gibbs measure. Same-loop proposals are excluded by shared edges.

The Poisson routine uses rational alternating-series bounds for exp(-rate), exact Poisson additivity, and lazy uniform bits. Its comparisons refine rather than truncate when undecided. No length, time, or ancestor cutoff was found.

For every fixed finite box, almost-sure termination already follows because the finite-rate dominant immigration/death chain visits zero, by which point all needed births are resolved. The subcritical all-loop bound is needed for useful uniform complexity and infinite-volume local constructions, not for finite-box correctness. The current implementation still performs global bookkeeping and requires honest scaling benchmarks.

As usual, mathematical exactness assumes ideal independent random bits; the supplied Python seeded PRNG is a reproducible implementation of that interface, not a literal source of infinite random entropy. The 3x3 empirical test is a sanity check, not the proof of stationarity.
