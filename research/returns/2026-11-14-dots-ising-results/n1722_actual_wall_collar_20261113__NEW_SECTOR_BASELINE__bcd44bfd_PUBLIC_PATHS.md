# A nonrare new sector beyond short-plus-seed constructions

This is a Gibbs-weight lower baseline, NOT an occupation lower bound.

Let L be divisible by8 and at least24. Put

    a=floor(L/3), b=floor(L/6), c=floor(5L/6).

If L is divisible by6, reduce c by1. Define row intervals of plus spins:
- For rows y>=L/2, use [a,c).
- For L/8<=y<3L/8, use [0,b).
- For all remaining rows, use [0,c).

The two wide buffers on either side of the narrow [0,b) quarter are essential: without them a periodic transition to [a,c) would disconnect the band. With these buffers the plus set is a connected vertical winding band with two disjoint axial phase interfaces.

## Exact geometry and weight
Its volume and physical perimeter are

    V=Lb/4+3Lc/4-La/2,
    P=2L+2a+2(c-b).

The actual deterministic physical-plus-resolution wall lengths are

    p_left=L+2a,   p_right=L+2(c-b).

The left wall satisfies p_left<=2L-8 for L>=24. There are no checkerboard ambiguities in the macroscopic step geometry that change these lengths; direct actual-encoding checks at L24,32,40,48,64,80 confirm the two axial cycles and formulas.

The rounding gives V<n/2. At L=8R, theta4, phi4/R,

    log[w(x)/w_minus]=2phi V-8P >= -32.

For the four actual finite instances R80,200,1000,10000 this logarithm is respectively -16,-16,0,0. The source is non-target in every case.

The existing core pressure receipt gives ZA/w_minus<=2exp(S0), with

    S0=6n(1/450)^4/(1-1/450)<1

at all four instances. Therefore even this single new-sector state has

    w(x)/ZA > exp(-34).

The universal constant is deliberately conservative. This is not an exponentially rare-in-R Gibbs sector, whereas the proposed actual-wall occupation bounds are exp(-94),exp(-567),exp(-3858),exp(-41368).

## Why this is outside the earlier simple covered seed families
There is no full plus row since c<L, and no full plus column since a>=b. All plus sites lie in the proper horizontal slab 0<=x<c, so no plus cycle can have nonzero horizontal homology; in particular there is no diagonal digital anchor.

Any vertical winding plus path must visit a row of the narrow quarter, where x<=b-1, and a row of the high-a half, where x>=a. In a proper horizontal lift its total horizontal variation is at least2(a-b+1). Its vertical variation is at leastL. Consequently EVERY plus winding path has length at least

    L+2(a-b+1) ~ 4L/3.

This exceeds both the earlier L+floor(R/16) short-cycle cutoff and the relevant small-total-variation seed cutoffs. Thus the new actual-wall theorem is not merely rediscovering the previous short-cycle coverage. This argument does not claim exclusion from every possible historical specialized source family; it explicitly separates the full-line, digital-diagonal and short/low-roughness winding-seed routes.

The total winding-wall perimeter is near4L, below the independent >=5L (or >=4.9L) direct Gibbs-tail regime. The example therefore also lies in the important low-winding-perimeter sector that the tail estimate does not remove.

## Executed receipt
`new_sector_baseline.py/json` verifies six actual finite-grid wall encodings, absence of full rows/columns, exact V and P, and the four large-instance formulas using integer/rational arithmetic. The large instances are formula checks, not allocations of billions of spins. The shortest-winding-path statement is the geometric lower bound above, not an unperformed large-grid path search.

## Translation amplification, with no hidden multiplicity
All n=L^2 translations are distinct. The rows of length b form one unique proper consecutive block of length L/4; because b,c,c-a are distinct, preserving the configuration fixes the vertical translation. Then any narrow row is a nonempty proper consecutive interval [0,b), which has no nonzero horizontal translation stabilizer. Hence the orbit has exactly n configurations, each with the same weight and all the same coverage exclusions.

The code now includes exact upper-exponential receipts e^16<9,000,000 and e<3. For R80 and R200, e^S0<=1/(1-S0) yields orbit mass relative to ZA greater than respectively

    8728035712/383579296875 > .022,
    87252832/613726875 > .14.

For R1000 and R10000, the exact w=wminus and S0<1 imply orbit mass relative to ZA greater than respectively

    32,000,000/3,  3,200,000,000/3.

These quantities are masses normalized by the CORE partition ZA, not probabilities under the full Gibbs distribution, so values above one are expected and legitimate. No extra orbit factor is inserted into the occupation upper bound: the entire translated family is already included in H and its pointwise visible-label counting.
