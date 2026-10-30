# Independent audit: universal half-factorial extension and exact halo

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review, no external novelty certification.

## Verdict

The growing-tilt finite-phase proof PASSES on projected phase components having a nonzero residual increment. The finite-halo construction and exact adjoint identity PASS. The halo note's final blanket application DOES NOT follow as written: inactive phases and all-zero-increment projected components require separate treatment. A single-linkage, full-rank example below shows the neutral case cannot simply be discarded by referring to finite halo classes. A direct local neutral-block repair is supplied; incorporating it changes the final assertion to a valid classwise corner-tail statement. No global overlap/feedback closure follows.

## 1. Universal alpha interval: pass

For an upward edge of source height h and increment delta>0, a weakly reversible return path must eventually descend. Before its FIRST descending edge, every source height is at least h+delta. The retained energy has fixed-coefficient Dirichlet terms on all preceding up/horizontal edges and a fixed-coefficient sink at the source of that first descending edge. Telescoping the phase values therefore controls the upward target value by energy terms whose fluxes have order at least r^(h+delta). The burden has order r^(h+2alpha delta). Their ratio is O(r^(-(1−2alpha)delta)), which tends to zero for every fixed alpha<1/2. This estimate does not depend on the number of phases or the reaction orders through the allowable alpha interval; constants and thresholds still do.

Dropping the vanishing downward Dirichlet terms is legitimate because the downward endpoint sinks remain at least F_e/4 eventually. Upward Young bounds retain fixed F_e/4 Dirichlet terms. Summing finitely many burdens leaves a positive fraction of the energy. In a connected projected component with at least one nonhorizontal edge, E=0 forces zero at downward endpoints and equality across every remaining edge, hence zero everywhere. Thus the weighted quadratic form is strictly negative and G is Hurwitz. Components with all delta=0 have no sink and are explicitly outside this argument.

For rational alpha=p/q and rational rates, G is Laurent-polynomial in r^(1/q). The positive inverse-vector entries are rational functions with a positive leading asymptotic coefficient, so their fixed-shift ratios are 1+O(1/r). The ordinary rate ratios have the same property. The Gamma ratio has precisely r^(alpha delta)(1+O(1/r)); the factor 2^|delta| absorbs the finitely many nonzero-shift errors. Horizontal shifts are exactly zero, including phase changes. The dual inequality is consequently valid outside a finite set on the nonneutral components. Polynomial factors do not change the claimed stationary exp[s n log(n+2)] moment range s<alpha under the accepted dual/regeneration argument.

## 2. Immediate primal counterpart: pass

Let w(r)=(-G(r))^−1 1 and V_j(r)=Gamma(r+1)^alpha w_j(r). For an actual outgoing transition with residual jump delta,

    Gamma(r+delta+1)^alpha/Gamma(r+1)^alpha
      =r^(alpha delta)(1+O(1/r)),
    w_k(r+delta)/w_k(r)=1+O(1/r).

The same inflated tilt dominates each nonhorizontal positive jump term; horizontal ones are exact. Hence LV≤−Gamma(r+1)^alpha eventually. V is norm-like because its positive rational/Puiseux factor has polynomial upper/lower growth. This is a direct primal Foster certificate on each nonneutral projected component, with finite-head extension understood. It does not fix neutral components automatically.

## 3. Finite halo and exact interface: pass

Every actual outgoing channel from j in J has unique bounded residual z=j−b_y≥0 and therefore appears. Every incoming channel has target complex y' with j≥b_y', hence residual z=j−b_y' in Z and predecessor phase z+b_y in H. Its bounded falling-factorial coefficient is exact. Two different residuals cannot duplicate the same original channel at the same source phase; coincidences between distinct original channels are correctly added. Each retained translated linkage is complete, so identifying repeated lifted vertices preserves weak reversibility. Thus the physical adjoint at j in J depends only on halo values and equals the halo adjoint there, wherever j belongs to H.

If j is not in H, no original complex's bounded coordinate can be enabled at j. There are neither outgoing nor incoming physical reactions there; its adjoint is zero, not strictly negative. Such inactive states must be treated as absorbing exceptions, not claimed to receive a strict certificate.

## 4. Substantive application gap: neutral halos occur on an infinite physical class

Consider the strongly connected single-linkage full-rank network

    0→A+B→3A+2B→0,

with A unbounded and J={B=0}. The construction has Z={0} and H={0,1,2}. Its residual offsets beta=(0,−1,−3) make every halo increment delta zero. The accepted theorem only says its residual classes are finite; it supplies no strict adjoint negativity on all halo phases for all large residuals.

Nevertheless every (n,0) lies in the SAME physical communicating class as zero. Starting from any (n,0), the sequence immigration, connector, connector, clearing, connector, clearing visits

    (n+1,1),(n+3,2),(n+5,3),(n+2,1),(n+4,2),(n+1,0).

All firings are enabled, and weak reversibility supplies return paths. Iteration reaches every n. The physical trajectory uses B=3, outside this halo. Therefore restricting to a fixed physical class does not by itself make the neutral halo tail finite. The halo note needs an additional argument.

## 5. Exact local repair for neutral projected components

On an all-delta-zero projected component, each transition preserves r exactly. For all sufficiently large r, let Q(r) be its ordinary finite phase generator. It is irreducible on that projected component; its entries are polynomials in r. Split the phases into I=component intersect J and O=component minus J.

If both I and O are nonempty, Q_II is transient because every phase in I reaches O. Set

    v_O(r)=1,
    v_I(r)=(-Q_II(r)^T)^−1 [1+Q_OI(r)^T 1].

This is positive and rational in r, and (Q(r)^T v(r))_I=-1 EXACTLY. Multiplication by Gamma(r+1)^(-alpha) preserves this equality since r never shifts. Thus any already chosen alpha>0 works, with polynomial prefactors and no new alpha/width circularity. This repairs the corner-interior adjoint while allowing positive defect on O; global matching still remains open.

If O is empty, all phases of the component lie in J. Outgoing completeness of the halo then makes each fixed-r finite halo class a closed finite PHYSICAL class. Such states do not occur in a fixed infinite physical irreducible class. A fixed finite physical class contributes no tail. Inactive j not in H are likewise absorbing. Empty I needs no certificate.

Consequently, after adding this neutral-block lemma and stating the conclusion classwise, the exact halo method yields negative corner adjoint for sufficiently large n on each fixed infinite physical class, using the same prechosen alpha<1/2. It still does not match halo values across different corners or with bulk profiles and does not establish global recurrence.

## Repaired-version addendum: accepted after reread

The author revised FINITE_HALO_EXACT_CORNER_INTERFACE.md to include exactly the neutral killed-block solve and the inactive/closed-finite-class exclusions above. Re-read this version: its resulting classwise receiving statement now PASSES. The earlier failure description records the defect in the prior blanket application, not a defect in the repaired statement. For clarity, its polynomial incoming vector g is the normalized forcing Q_OI^T 1 after division by the common Gamma(r+1)^(-alpha) factor.

Also reviewed PRIMAL_AND_EXACT_CORNER_TRANSFER.md. The primal bulk ratio has the correct mixed-power orientation: its ratio to the ideal term is

    [((x+nu)!(x−y')!)/(x!(x−y)!)]^alpha=1+O(1/min x).

The primal finite-phase right inverse and the neutral right killed-resolvent counterpart are valid. A fixed polynomial multiplier has fixed-shift ratio 1+O(1/r), so it can be absorbed by reserved fixed inflation without changing alpha.

The physical and halo generators agree on every outgoing channel from J, so their stopped paths through the first exit of J genuinely agree. On an auxiliary halo communicating class that meets the exterior, positive recurrence gives finite expected hitting time of a chosen exterior state, hence finite expected corner exit time. This uses the already established auxiliary recurrence, not physical-network recurrence.

For the earned primal function, positive drift is confined to a finite head F. By the strong Markov property at first entry to F before exit, its expected occupation time before exit is bounded by the maximum expected exit time from F in the relevant communicating class. This maximum is finite. Stopped Dynkin followed by localization and Fatou therefore yields the exit V-moment bound. The negative drift integrand is bounded below away from zero outside F, which also yields E[tau]≤C'(V+1). In neutral components the large-r killed equation is exact; finitely many lower residuals can be handled separately within the exiting classes. Closed physical classes must remain excluded, as the revised note does.

A nonnegative boundary datum g≤cV consequently has a finite NONNEGATIVE harmonic extension. Replace “positive” by “nonnegative” unless g is positive on a reachable portion of the exit boundary; g identically zero is the elementary exception. The finite Poisson extension for a running cost bounded by the proved negative drift integrand is likewise justified. No claim of uniform constants over increasing corner width, nor of feedback contraction, has been proved.

Reviewed final artifact hashes follow (captured after rereading the repair):
91715aa2464aef682dbc4978f2f7fc18a7047def6cc919584c9d2fcc0f177d16  producer-workspace/UNIVERSAL_HALF_FACTORIAL_PHASE_EXTENSION.md
be78063cb296f411bd6816ce205b2c59811be59894389c6f4d4bd18578f0ee8e  producer-workspace/FINITE_HALO_EXACT_CORNER_INTERFACE.md
07b73bc0e7fe8323288987c5a5bda2d41469a06cfeecb8d115b404aa2a91aba2  producer-workspace/PRIMAL_AND_EXACT_CORNER_TRANSFER.md
