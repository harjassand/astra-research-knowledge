# Actual-current exclusion of two disjoint macroscopic predecessor droplets

## Status and purpose

This is an internally derived finite theorem/certificate using the thermal-core capacity lower bound from the preceding package and standard Peierls/Thomson machinery. It is not an independently reviewed scientific novelty claim. It removes a specified family of genuine dense-merger entrances; it does not prove full entrance coverage or physical growth.

## Definitions and hypotheses

Use the actual periodic heatbath model and source conventions of N1722: n=L², θ≥4, φ=θ/R, R≥1, one proposal clock per site, B={M≥0}, acquired thermal core A=C_r, soft source clock κ>0. Assume

    1≤r, r+2≤R/3, r<L/4,
    5R²<L²/4,
    u_r<1, Z_M5/Z_A≤1/(1−u_r).

The core-size +2 conservatively pays lattice box-width conventions. The capacity lower theorem supplies, with a=49999/50000,

    Cκ≥Z_A/Dκ,
    Dκ=κ^(-1)+2n exp(8θR/a+8θ).

Let E2 be the set of configurations x∈M5\B that contain two DISTINCT augmented plus components whose FILLED outer domains D1,D2 are disjoint and satisfy

    R²≤|D_i|≤5R²,  i=1,2.

Define J2 to be the actual outgoing current over boundary EDGES with predecessor in E2:

    J2=sum_{x∈E2,y∈D} g(x,y)[v(x)−v(y)],
    D=outside(M5∪B).

This is an edge-labelled entrance-current fraction. It does not require every predecessor of the same destination y to belong to E2. It includes in particular mergers of two disjoint macroscopic precursor droplets, but the components need not both be adjacent to the added spin for the upper bound to apply.

## Finite theorem

Set

    cθ=6θ−4log4,
    B_R=ceil(9R)+3,
    A_R=6n B_R exp(−cθR).

Then

    J2/Cκ ≤ min{1, [n A_R²/(1−u_r)] Dκ}.             (1)

The only exponential-in-volume factor from the earlier bare-allminus normalization is ABSENT. All labels, physical clock rates, source κ and thermal interiors are paid.

## Proof: the two-domain map

For each x∈E2 select a canonical ordered pair of qualifying domains, for example by lexicographic rooted-contour encodings. For a FIXED selected pair, flip EVERY spin in D1∪D2.

The domains are disjoint and belong to distinct augmented plus components. No physical edge can directly join the two filled domains: its endpoints would belong to their plus outer boundaries and would connect the components. Consequently their boundary energy changes add.

The map is an involution for the recorded pair and therefore injective. It preserves M5:

* Each outer plus boundary becomes minus.
* Every new plus component created inside D_i stays inside that embedded nonwinding domain of area≤5R².
* The flipped boundaries separate these new components from the unchanged exterior.
* Every other component is unchanged.

All thermal holes, islands and exterior spins are retained, merely complemented inside the two recorded domains. No perfect droplet is imposed and no hidden resampling occurs.

For physical outer perimeters P_i and volumes V_i,

    w(x)/w(Fx)
      ≤ exp[−2θ(P1+P2)+2φ(V1+V2)].                  (2)

Fixed diagonal contact resolution is inherited from the actual source. Nested filled domains are excluded precisely because the disjoint-map proof would otherwise require different accounting.

## Proof: pay the full contour sum

The source's diagonal-resolved count gives at most6n4^P possible rooted/located contours of physical perimeterP. For a qualifying domain, lattice isoperimetry and the area cap give

    P≥4R,    V≤min(5R²,P²/16).

Let t=2θ−log4>0. The entropy-included exponent is bounded by

    −tP+2φ min(5R²,P²/16).

For4R≤P≤4sqrt(5)R this is a convex quadratic inP, so its maximum lies at an endpoint. At P=4R it equals−cθR. At the other endpoint its negative coefficient exceeds cθ because

    [(8sqrt5−10)θ−4sqrt5 log4]−cθ
       =(8sqrt5−16)θ−4(sqrt5−1)log4>0

for θ≥4. For example, using sqrt5≥20/9 and log4<7/5, its value at θ4 is at least4/15.

There are at mostceil(4sqrt5R)+1 integer perimeter terms up to the second endpoint. Above it the bound has geometric ratioq=4exp(−2θ)<1/2. The remaining sum is at most1/(1−q)<2 times the endpoint bound. Since4sqrt5<9,

    sum_{qualifying contours γ}
       exp[−2θP(γ)+2φV(γ)]
       ≤6n[ceil(4sqrt5R)+1+1/(1−q)]exp(−cθR)
       ≤A_R.                                        (3)

For the canonical labelled pair, (2) maps its source weight into Z_M5. Summing all possible ordered pairs, including incompatible pairs only to upper-bound the positive sum, gives

    sum_{x∈E2}w(x)≤Z_M5 A_R².                       (4)

There is no uncharged assertion of independence. The product is a union/counting upper bound. A canonical pair makes the source label unique; summing all candidate pairs can only overcount.

## Proof: actual current and clock

The soft voltage satisfies0≤v≤1. Across the upward M5 boundary its current is nonnegative. Thus

    J2≤sum_{x∈E2,y∈D}w(x)c(x,y)
       ≤n sum_{x∈E2}w(x),

because there are n rate-one site clocks and each accepted heatbath rate≤1. Combine this with (4), the acquired Z_M5/Z_A ratio and the thermal-core capacity lower bound to obtain (1).

No Gibbs law for the incoming current, physical-time simulation, or unknown committor value is used.

## Strength and limits

When n and κ^(-1) are polynomial inR, the main exponent in(1) is

    −[12θ−8log4−8θ/a]R,

which has positive suppression margin already at θ4 (about4.909R before polynomial factors). This does not mean the bound is useful at every finite parameter choice; κ is important and must not be replaced by1 without saying so.

The following remain OUTSIDE this certificate:

* A single dense critical/rough predecessor component.
* A dominant nearcritical component merging only with sub-R² components.
* Two large components whose filled domains are nested/overlap rather than disjoint.
* Hole-closing or winding entrances without two qualifying disjoint precursor domains.
* Physical growth duration or residence from the retained entrances.

If a winding destination DOES have a predecessor in E2, its corresponding edge current is covered. This is not a general winding exclusion.

## Clock-aware exact numerical certificates

`certify.py` uses EXACT rational arithmetic, integer roots and elementary Taylor bounds. It evaluates the new theorem and the earlier sparse-component theorem with the actual source prescription

    κ=ε/(64D0), ε=1/100,
    D0=2γ0^(-1)[n(log2+6θ)+log2],
    γ0=q*/[384(r+2)^8] exp[−(8log2+88θ)(r+2)],
    q*=(1+exp(10θ))^(-1).

It conservatively bounds logκ^(-1) rather than treating the source clock as1. For θ4,L8R and r chosen so the acquired core/basin error bound≤.01:

    R20,r4: both coarse bounds uninformative with this clock.
    R40,r5: sparse current≤exp(−1260); two-macro bound uninformative.
    R80,r5: J2/Cκ≤exp(−278); sparse current≤exp(−5257).
    R1000,r6: J2/Cκ≤exp(−4669); sparse current≤exp(−68841).

These are scalar consequences of the mathematical theorem, not simulated dynamics. The script does not independently verify the contour/flow proof. Earlier examples with κ1 remain mathematically valid for that clock but are not substitutes for these source-clock-aware evaluations.

## Prior-art distinction

Multiple-droplet Peierls suppression is classical. GMV already gives asymptotically sharp normalized soft-capacity bounds in its own finite-box setting. The reusable addition here is the finite actual-source edge-current certificate with all displayed factors and the bulk-free thermal-core flow normalization. No broad novelty claim or full predictor is made.

# Extension: pure mergers below a 4R² precursor area cut

The area4R² below is an explicit geometric threshold, NOT a claim that every domain above it is a thermally supercritical Wulff seed.

## Witness family

Let K=floor5R². Consider predecessor configurations in M5 containing a collection of2≤k≤8 distinct components with disjoint filled domains, such that

    sum_i V_i≥K,
    max_i V_i≤4R²,
    all but at most one V_i≤R².

Let J4 be actual outgoing M5 boundary current whose predecessor admits such a witness. A canonical witness collection and canonical contour ordering can be chosen for each predecessor; summing all possible collections gives a positive upper bound.

Every pure merger whose old filled domains are disjoint, whose new filled area is1+sum_iV_i, and whose largest precursor has area≤4R² is covered by EITHER J2 OR J4:

* If two precursors have area≥R², it is in the earlier two-domain family.
* Otherwise all but at most one have area≤R², and the M5 exit implies sum_iV_i≥K, so it is in the present family.

The one-site update merges at most8 old augmented components, as stated by the governing source. A hole-closing update with a positive extra enclosed-area jump does not satisfy the assumed pure-merger area identity merely because the destination crosses M5.

## Explicit bound

Set

    s0=2θ−29/20,
    E4(R)=(4s0−2θ)K/R−8s0R,
    Dκ=κ^(-1)+2n exp(8θR/a+8θ), a=49999/50000.

Then

    J4/Cκ ≤ min{1,
      [7n(126n)^8/(1−u_r)] Dκ exp[−E4(R)]
    }.                                               (5)

For integer R, E4(R)=(14θ−87/5)R. At θ4 its coefficient is38.6, exceeding the thermal-flow capacity coefficient32/a.

## Proof with every label paid

For each fixed disjoint witness collection, flip all its filled domains simultaneously. The same injective map and M5-preservation proof used above applies, preserving all thermal spins and adding the boundary energy changes.

Reserve η=1/20 of each physical perimeter exponent. After the contour count4^P has been included, put

    s=2θ−log4−η ≥s0.

Let domain1 be the largest. For every other domain Vi≤R², isoperimetry gives sqrt(V_i)≥V_i/R. Since P_i≥4sqrt(V_i),

    sum_i[sP_i−2φV_i]
      ≥4s[√V1−V1/R]+(4s−2θ)(sum_iVi)/R
      ≥−8sR+(4s−2θ)K/R
      ≥E4(R).

The second line uses V1≤4R², so sqrt(V1)−V1/R≥−2R. The last line uses4K/R−8R>0 forR≥1, making replacement s→s0 valid.

For each contour the reserved summable factor obeys

    6n sum_{P≥4} exp(−ηP)
       ≤6n/(1−exp(−η))
       ≤6n(1+1/η)=126n.

Here exp(η)≥1+η proves the last step. Sum over2≤k≤8 ordered contour collections:

    sum_{witness predecessors}w
       ≤Z_M5 exp[−E4(R)] sum_{k=2}^8(126n)^k
       ≤7Z_M5(126n)^8 exp[−E4(R)].

There is no independent-contour assumption; after applying a bound valid for all qualifying collections, compatibility constraints are dropped only to upper-bound a positive sum. Canonical witness selection avoids an uncounted source label. The factor n for the actual outgoing site clocks, the normalizer ratio, and the capacity lower bound give(5).

## Exact source-clock consequences and retained cases

The same exact rational script, usingκ=ε/(64D0),ε.01, certifies

    θ4,R80,L640,r5:   J4/Cκ≤exp(−320), J2/Cκ≤exp(−278).
    θ4,R1000,L8000,r6: J4/Cκ≤exp(−6341), J2/Cκ≤exp(−4669).

Their union is bounded by the sum, without claiming disjointness. At R20 and R40 the coarse J4 bound is uninformative with that source clock; the script reports this rather than asserting exclusion.

Consequently, within the stated pure-merger/disjoint-domain class, an entrance not removed by these estimates must have a precursor of area>4R² and no second precursor of area≥R². That is a narrowing of the retained source family, not proof of its physical growth. Dense single-component area-addition entrances, nested configurations, new-hole area jumps, and unclassified winding events remain open.
