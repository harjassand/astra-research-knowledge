# Independent audit: local-stochastic correlated-death bridge

2026-10-15 20:31 UTC. Reviewed SUBSET_BOUND_CONTOUR_BRIDGE.md and inspected the named primary statements and proof steps. This audit does not accept the constructor's verdict as a premise.

## Verdict

The classical bridge closes under its explicit uniform microscopic subset-probability hypothesis and the named deterministic contour imports. The coarse coloring estimates, including the weaker clocks-only square-root estimate, are valid. The correlated contour conclusion is a reconstructed extension of the chain proof, not an application of the published iid corollary. Fixed-patch flag copying with zero exterior preserves the required probability class and avoids fictitious iid replay.

No new classical proof gate remains beyond the explicitly imported deterministic contour existence/geometry/counting and the previously established memory support/forcing/homology modules. The new physical subset/instrument hypothesis and the separate restricted-amplitude norm-regrouping theorem remain unproved and cannot be inferred from this result.

## Primary-source contract actually checked

[Swart–Szabó–Toninelli v1](https://arxiv.org/html/2202.10999v1), Definition 2, Theorem 7, and Lemmas 13–14 supply deterministic contour existence, noncolliding sinks, an edge/sink bound, and exponential contour enumeration. The theorem applies to a specified monotone flow, rather than requiring an iid flow. The edge count is per charge; multiplying by the fixed number of charges is harmless.

[Hartarsky–Toninelli v2](https://arxiv.org/html/2212.08437v2), Lemma 9.15 extracts disjoint contour-support chains. Proposition 9.3 as formally stated assumes the decorated-event negative-correlation condition (9.1); local-stochastic noise need not satisfy that condition. Its proof's probability step (9.5) only needs a joint bound for each extracted disjoint family. Replacing that step by the estimate below is valid. Corollary 9.5 itself is not invoked for correlated deaths.

The old theorem numbers refer to SST v1. Later versions have changed numbering and should not be silently substituted.

## 1. Conditional microscopic subset bounds

Precisely, h must canonically index the realized parent starts, and the conditional hypothesis must hold almost surely simultaneously for all their finite subsets. This includes clock-measurable choices of subsets. A statement for a few fixed deterministic time labels would not suffice for random Poisson candidate sets. The report explicitly requires the stronger, appropriate condition.

Let J be a finite set of coarse sites whose complete primitive packets are pairwise disjoint. Its candidate-parent sets I_v are then disjoint, so selecting one parent from each yields |J| DISTINCT starts. Conditional on h, a union bound over these choices gives

    P(all H_v, v in J | h) <= p^|J| product_v K_v.

No assertion of independent marks occurs here. The right side may exceed one on a particular high-count schedule without invalidating the bound. Averaging disjoint Poisson packet counts gives

    E product_v K_v = product_v E K_v <= mu^|J|.

Only first moments are used because each disjoint candidate packet contributes one parent. Repeated points of one stream across disjoint time intervals are still distinct starts. If packets can share a parent, this product argument fails; the packet graph must exclude that sharing, which the report requires.

A deterministic candidate region of N streams and length w has mean kappa N w. For a candidate subset selected using clocks, the same formula remains an upper bound when the subset is contained in that region. Dependence on noise may be avoided by counting every geometrically possible parent in the region; one should not replace this count by an unverified selected completion intensity.

## 2. Combining primitive base failures and marks

Suppose first that the microscopic subset condition holds conditional on all exogenous primitives. On a fixed schedule, A_v is a deterministic binary value. For each partition J=U union V, use base flags on U and marked witnesses on V. The event probability is bounded by

    E[ product_(u in U) A_u product_(v in V) p K_v ].

Complete packet independence factors this expectation across DIFFERENT sites. No independence between A_v and K_v within a site is required, because each site belongs to only one part of the partition. Summing partitions gives

    P(all B_v, v in J) <= (d0+p mu)^|J|.

This also proves the conditional product expression used by the constructor. Arbitrarily long-range mark correlation does not interfere: the conditional subset inequality has already paid for the entire marked family.

If the subset bound is known only after conditioning on clocks, it must not be conditioned further on noise. Instead use the unconditional bounds P(all A_U)<=d0^|U| and P(all H_V)<=(p mu)^|V|. Cauchy–Schwarz applied to these two indicator events gives

    P(all A_U and all H_V) <= d0^(|U|/2) (p mu)^(|V|/2).

There is no need for independence between those two events. Summing partitions produces (sqrt(d0)+sqrt(p mu))^|J| exactly. The resulting loss is conservative but legitimate.

For arbitrary finite W choose a largest class of a fixed Q-coloring, so |J|>=|W|/Q. Dropping the other requirements and using a bracket below one proves the claimed coarse local-stochastic parameter:

    q=(d0+p mu)^(1/Q),

or q=(sqrt(d0)+sqrt(p mu))^(1/Q), respectively. The degree bound and Q must be fixed in coarse units before b. All local terminal/noise windows and candidate supports must be included in the graph. Wrapped torus coloring uses actual distinct vertices; it cannot assign separate independent copies to one periodic variable.

## 3. Exact correlated contour replacement

The sufficient abstract interface can be stated without any stochastic-domination theorem. Each contour gamma has a finite support Z_gamma and a sink set S_gamma inside it, with the following fixed constants:

- bounded contour edge lengths, hence diameter at most a constant times |Z_gamma|;
- |S_gamma|>=|Z_gamma|/C1;
- at most a^r contours/decorations of support size r containing any specified point;
- every zero belongs to a present contour;
- a long connected path covered by present contours yields a chain of pairwise disjoint contour supports whose enlarged sets span that distance.

The named deterministic imports supply these properties. Distinct sink cardinality is essential. Abstract graph vertices may have multiple embeddings elsewhere, but sinks cannot collide. Their images therefore count actual distinct death variables. Disjoint image supports of different chain members imply that their sink sets are also mutually disjoint.

Under coarse LS(q), presence of one specified disjoint family implies all its sink variables are one. Ignoring any additional conditions only enlarges the event. Hence

    P(all contours in family present)
      <= q^|union S_gamma|
      <= q^(sum |Z_gamma|/C1).

This does NOT prove negative correlation relative to the contours' actual marginals. It supplies the exact numerical substitute needed in the chain union bound.

To check summability independently, put r_j=|Z_j| and R=sum r_j. Enlarged-set connectivity implies distance n requires R>=n/J0 for a fixed J0. The first distinguished point has at most a polynomial in r_1 possible positions around the anchor; each subsequent point has at most a fixed-dimensional polynomial in r_j+r_(j+1)+k possible positions. Because all sizes are positive integers, r+s<=2rs and every fixed power of r is bounded by an exponential in r. Thus the full position count is at most K1^R. There are at most 2^R ordered compositions of R and at most a^R shape choices. Enlarging K combines these factors. A union bound now yields

    sum_(R>=ceil(n/J0)) (K q^(1/C1))^R.

For q sufficiently small this is exponentially decaying. A component containing an anchor and having diameter ell contains a point at distance at least ell/2 from the anchor, so the path estimate gives the stated diameter estimate. No stationarity, independence of contour events, iid reference field, or upper-invariant random law enters this argument.

Counting the first distinguished point deserves explicit attention: the anchor need only lie in the enlargement of the first contour, not the contour itself. The constructor's explicit polynomial position count includes this factor, so it does not inherit any shorthand assumption that the anchor is itself a contour vertex.

For the cold process, extend the deterministic flow with the ordinary rule and no deaths before time zero. Its maximal trajectory is all healthy there and agrees with the forward cold process afterward. This places the finite-history process within the deterministic contour-existence theorem. The extension contributes no uncharged sink deaths.

## 4. Native torus to an inhomogeneous infinite field

For each deterministic prospective first-crossing anchor, use the existing closed-zero-ancestor witness inside an injectively liftable spatial patch. Copy the coarse death variables from that deterministic patch and the required finite time interval to the infinite lattice; set all other death variables to zero.

For any finite set of lifted indices, if it contains an outside index, its all-death probability is zero. Otherwise the indices map to distinct native torus spacetime indices and retain their LS(q) bound. Thus the entire lifted field satisfies LS(q), despite potentially arbitrarily long-range dependence inside the copied patch.

The witness is reproduced by induction because every required zero ancestor and death flag lies inside the copied region. Unlike the earlier primitive-Poisson replay, this argument need not reconstruct a valid microscopic model outside the patch. The abstract correlated-death theorem applies directly to the lifted coarse field. Apply the anchored estimate separately for each prospective anchor and union bound over the finite list. No adaptively chosen copy, periodic infinite iid lift, or conditional-law preservation is asserted.

The remaining whole-slab inclusion and accumulated homology statements are deterministic modules. They must still hold for the actual event supports and skipped updates; LS alone does not establish them.

## 5. Quantum and physical boundaries

The report correctly uses actual instrument records to select its CP good subchannel. Uniformity over initial joint states is necessary to upgrade a probability estimate to an operator-effect bound and then a joint-domain diamond bound. A state-specific subset estimate does not suffice. The microscopic bad mark must denote a genuine instrument branch with the claimed support semantics, rather than a signed Pauli-expansion term.

Not established by this bridge:

1. An actual shared-bath finite-duration pulse instrument with the required recordwise support/ordering properties.
2. Uniform joint subset probabilities for its distinct parent starts, conditional on the specified exogenous information.
3. A replacement for a failed serialization step. The classical probability extension cannot repair a wrong quantum channel identity.
4. The restricted-amplitude regrouping theorem needed to pass from cancellation-sensitive inclusive norm bounds to a controlled sum of bad witnesses.
5. Autonomous physical timing, finite controller implementation, arbitrary continuous bath noise, or practical rates.

The separate norm proposal is appropriately conditional. Its scalar cancellation warning is real: an inclusive sum can be small while a selected subsum is large. If an actual U=I_L tensor g+E decomposition with ||E||<=eta<1 is separately supplied and U is an isometry, then g has singular values in [1-eta,1+eta]; polar replacement changes g by at most eta. The resulting isometry differs from U by at most 2eta and the associated channel bound is at most 4eta. This verifies that last implication, not the missing witness regrouping needed to obtain E.

## Final status

Classical probability extension: reconstructed and supported, conditional on the named deterministic imports and established memory geometry.

Physical finite-duration subset/instrument premise: open.

Inclusive coherent norm bound to restricted bad-amplitude witnesses: open.

No iid correlated-noise theorem, physical realization, or broader robustness claim is implied.

## Supplement: embedded support versus abstract graph size

Root requested an explicit check of this possible counting gap after the initial audit. It closes without assuming injectivity of the entire contour embedding.

Let r=|psi(V)|, s=|V_*|, n be the number of edges per charge, sigma the fixed number of charges, and a=1+R/epsilon from the imported edge bound. Sink injectivity and connectedness give, respectively,

    s<=r,             r<=|V|<=sigma n+1.

Combining with n<=a(s-1) proves BOTH directions needed:

    n<=a(r-1),        r<=sigma a(s-1)+1.

Therefore s>=r/max(1,sigma a), while the edge-count enumeration need only be summed up to a(r-1). A polynomial-times-exponential bound in n sums to an exponential bound in r. For contours containing a prescribed point z, the root lies within distance O(r) of z, since the embedded support is connected by bounded-length edges. Summing root positions costs only another polynomial in r. The isolated r=1 contour is handled separately. Hence the decoration bound a_new^r used by the chain argument is justified even though some non-sink abstract vertices coincide under the embedding. The edge/sink inequality rules out unbounded hidden contour complexity on a fixed small support.

The decorations can be contour equivalence classes: their sink sets and embedded charged edge images are retained by the equivalence relation, so the necessary death event is well-defined. Counting more abstract presentations of the same embedded event is unnecessary.

For indexing precision, if theta_(n+1) uses B_(x,n), define the flow's death at output time t>=1 as xi_(x,t)=B_(x,t-1). Set xi=0 for all t<=0 and beyond the finite horizon. Any finite all-death event containing one of those added zero variables has probability zero; otherwise it is exactly an original positive-time LS event. The full flow consequently remains local-stochastic, and its maximal trajectory equals the prescribed cold trajectory. No correlated stationary measure is introduced.
