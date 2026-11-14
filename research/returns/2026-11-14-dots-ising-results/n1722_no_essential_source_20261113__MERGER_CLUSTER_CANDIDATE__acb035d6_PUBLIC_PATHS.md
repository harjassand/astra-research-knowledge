# Physical-small / original-augmented-large merger comparison

Candidate proof for independent review. This does NOT address a genuinely large physical NN plus filled domain or the plus-background/no-wall sector. Original core A and original fixed-diagonal M5 are unchanged.

## Enlarged physical basin
Let F contain configurations for which every physical nearest-neighbor plus component has a nonwinding embedded filled outer disk of area<=5R², using the adaptive plus4/minus8 physical convention. Thus A subset M5_original subset F. Nested thermal spins are retained. F is a down-set: deleting plus sites only splits physical NN components; each resulting component lies within an old component, and its filled disk is contained in the old filled disk because the accessible8-connected exterior can only enlarge. A subset cannot gain winding. This uses physical plus4/minus8 filling, not a new core definition. Define b=theta(2-sqrt(5)/2), q=3exp(-b).

Proposed bounds, when u=100n q^(2r)/(1-q)<1:

 Z_F/ZA <=1/(1-u),
 Z_(F\M5_original)/ZA <=100n q^ceil(4sqrt(5)R)/[(1-u)(1-q)].

The second bound also bounds its non-target occupation becausev<=1. These are direct mass comparisons, not current-source replacements.

## Choosing a connected witness without losing nesting
Choose an original augmented plus component K that fails the desired core or M5 test. For every physical NN component meeting K, take its GLOBAL outermost physical filled-domain ancestor. Retain the distinct ancestors D1,...,Ds. Their filled interiors are pairwise disjoint; they cover K. This may select an ancestor whose physical plus component is not itself K. That is allowed: it is a flip witness, not an assertion about original-component membership.

The selected domains form an8-connected union. A contact of K across two different ancestors reaches their outer boundaries, so their physical outer boundary cycles meet at a square-dual vertex. After replacing each domain by a solid plus disk, distinct domains cannot be physical NN-adjacent: their original outer boundary plus spins would already have belonged to one physical component. Thus their boundary edge sets are disjoint, and their union is a connected even physical-dual graph.

## One oriented Euler word pays the entire cluster
Orient each outer boundary with its filled disk on the left. The union is balanced and connected, so has a directed Euler traversal. Every physical edge is used once, so the traversal cannot immediately reverse a physical edge. There are at most4n choices of the initial directed edge and at most3 choices at every subsequent step. The conservative100n3^P count therefore pays all cluster labels of total physical perimeter P.

The DIRECTED word retains the side choice. Its oriented edge set reconstructs the filled-domain union, including checkerboard contacts; no extra independent component-pairing labels are assumed. An unoriented word would instead require an explicit global-side bit. This distinction was flagged in independent review.

## Thermal-preserving flip and normalizer comparison
Flip EVERY spin in all selected filled domains. Given the label, this is an involution, preserving all complementary thermal bits. Each old physical boundary plus layer becomes minus, so newly created plus components inside a flipped domain cannot NN-connect to the exterior. Their filled areas remain bounded by that domain's area. The image remains in F, including nested configurations.

Since the selected domains are disjoint,
 w(x)/w(flip_union x) <=exp[-2theta P+2phi sum_j |Dj|]
 <=exp[-bP],
using |Dj|/Pj<=sqrt(5)R/4. For every fixed label, injectivity bounds its conditional F probability byexp(-bP). Summing the Euler labels gives the displayed geometric series.

A failed ORIGINAL r-box core test requires witness totalP>=2r. The ancestor union covers the failing component and hence its transverse range; if it winds, the stronger2L bound applies. This yields mu_F(Ac)<=u and the normalizer comparison without a separate sampler for F.

## Original M5 failure threshold: do not replace augmented geometry
A single physical C-shaped component can have small physical filled area but close a huge bay under the original diagonal convention. Therefore one must NOT claim that a component contained in one small physical filled domain automatically belongs to M5_original.

Instead solidify the selected witness union U. It contains K, so original augmented monotonicity preserves K's failure. Every physical edge of an original outer contour of this solid union belongs to its physical boundary edge set; zero diagonal edges cost no physical perimeter. Thus the relevant augmented outer perimeter is at mostP. If it bounds filled area>5R², the inherited physical isoperimetric inequality givesP>=4sqrt(5)R.

If original augmented connectivity winds, the connected solid witness union projects onto every column or every row. The sum of the inclusive widths (or heights) of its constituent contractible domains is at leastL, while each physical outer perimeter is at least twice that width. Hence their total physical perimeter is at least2L. This projection argument does not falsely assign nonzero homology to the Euler word, whose net homology is zero. AtL8R this exceeds4sqrt(5)R. The original fixed triangulation resolves planar contacts; any additional alleged nonembedded/nonwinding failure mode must be checked against that definition rather than silently omitted.

## Review gates before promotion
- Prove the global-ancestor witness remains connected at every original diagonal contact, including nested thermal cases.
- Check the original augmented contour perimeter domination for pinched bay closure.
- Check image membership in F and directed Euler reconstruction.
- Verify the original source's embedded-disk definition has no unhandled failure mode.

Bridge independently found the Euler/flip mechanism plausible and specifically required the directed-side encoding and careful nested-ancestor choice. No general no-essential occupation theorem is asserted by this candidate.

## Potential use as an alternative mesoscopic basin
The recovered source identity is valid for ANY down-set M containing the original core A. Therefore, if the above normalizer proof is validated, F may be used as a new mesoscopic basin while preserving A, kappa, all physical dynamics and the actual target. Its occupation outside A is at mostZA*u/(1-u) directly. This does not acquire capacity or resolve the physical-large/plus-background exterior; it removes the need to treat artificial original-diagonal merger topology as a distinct dynamical bottleneck. The original M5 is not silently redefined.

## Executed diagnostics and conditional receipts
`check.py/json`:512 exhaustive padded3x3 states,6000 seeded4x4 states andone explicit nested5x5 state. Among5168 physical-small states,5044 ancestor-cluster witnesses passed domain disjointness, cluster8-connectivity, exact perimeter removal, flip-image basin membership, synthetic augmented-hull containment and isoperimetric bounds;397 witnesses had original augmented filled area beyond the physical cutoff. This is planar support, not a torus winding proof. Bridge independently tested2190 directed Euler mergers.

`scalar.py/json` uses exact q<1/11 and log11>239/100. At the four existing(R,r) pairs the proposed F-minus-original-M5 mass bounds are exp(-1693),exp(-4255),exp(-21355),exp(-213740). They remain conditional on the general geometric/injection proof.
