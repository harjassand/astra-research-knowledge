# A global contour-cut energy upper with acquired area-resolved walk counts

Status: explicit finite positive algorithm and exact small geometry checks. This replaces a crude count in the EXISTING globally defined cut potential. It is not a restricted-family capacity claim, not an acquired actual energy-edge law, and not a demonstrated numerical improvement at the retained large tuples.

## 1. Original global trial and its inherited interfaces

Keep the original fixed-diagonal augmented core A, heatbath clock, reservoir kappa, majority target B, and theta4 (the formula below also works when the stated tail contraction holds). For1<=s<=2 let M=M_(s²) be the source's nonwinding embedded-filled-component area cutoff s²R². Use f(star)=1, f=1 on M\B and f=0 elsewhere.

Import exactly the geometry/normalizer lemmas of n1722_optimized_cut_capacity_20261113/RESULT.md: A subset M, Z_M/ZA<=1/(1-u4), u4<1, and any structural exit joins at most8 disjoint old outer filled domains, each area<=s²R², whose total physical perimeter is at least S0=ceil(4sR-4). Simultaneously flipping those filled domains is injective and remains in M, paying exp[-2theta sum P+2phi sum V]. Hole closure, mergers and first winding are covered by that inherited perimeter statement; no new claim that filled area equals actual plus count is made.

The original proof then discarded V and used6n4^P. The operation here retains V in a complete overcount.

## 2. Exact physical-perimeter / filled-area walk representation

Take the fixed diagonal (x,y)--(x+1,y+1) in every plaquette; the other convention is a reflected copy. In coordinates multiplied by3, triangle dual vertices are

 A_xy=(3x+2,3y+1), B_xy=(3x+1,3y+2).

From A the dual steps (du,dv; physical cost) are (-1,1;0),(-1,-2;1),(2,1;1); from B they are their opposites. Zero cost crosses the zero-coupling diagonal. A nonbacktracking walk cannot take two zero edges successively, since each dual vertex has exactly one zero edge. Root the first step at a physical edge; a closed walk with physical perimeter P then has at most2P dual steps.

For any lifted actual simple outer contour, orient it positively. The shoelace sum in these scaled coordinates is18V, where V is its filled spin-site count. One way to see this precisely is to use the translation-periodic dual cell around each primal site: each has area1, their straight dual sides meet at the edge midpoints, and filling the contour is a union of exactly V such cells. This is a statement about actual simple resolved contours. For a self-intersecting overcount walk the signed area is not called a physical domain; it is only an integer bookkeeping statistic.

Every actual contour has a canonical physical root and positive orientation. Lifting it, translating the root to its type-A or type-B origin, and recording its step word is injective. There are n translates of each type. Counting ALL nonbacktracking closed words, including repeated vertices and self-intersections, therefore overcounts the actual contour family. Discarding words with negative or nonintegral area does not discard a positively oriented actual contour.

## 3. Positive DP, including overhangs

For a chosen cutoff Mper, propagate states

 (dual step count, physical perimeter, displacement u,v,
  accumulated shoelace sum, previous step).

For a next step, update area by u*dv-v*du and prohibit immediate reversal. Root first step physically. Record every return to the origin with positive area18V and perimeterP<=Mper. Sum both root types, obtaining exact integer c_(P,V). Coordinates are O(Mper), shoelace range O(Mper²), step count and physical perimeter O(Mper), and the previous direction has constant size. A direct rolling-step implementation takes polynomial O(Mper^6) arithmetic work and O(Mper^5) state storage by a crude dense upper count. Sparse implementation can be much smaller, but no cheap large-R runtime is asserted. Count integers have O(Mper) bits before the subsequent positive weighted operations.

Define acquired truncated contour activities

 A_P = n sum_(1<=V<=floor(s²R²)) c_(P,V) exp(-2theta P+2phi V),
     4<=P<=Mper.

Compute the ordinary positive polynomial A(z)=sum A_P z^P. Then

 T_short = sum_(j=1)^8 sum_(S>=S0) [z^S] A(z)^j

overcounts all relevant tuples whose individual perimeters are<=Mper. Roots, labels and compatibility have all been PAID, not sampled conditionally. The convolution is polynomial in Mper and uses at most8 factors.

## 4. Fully paid omitted tail and complete global upper

Let a_s=theta(2-s/2), q=4exp(-a_s)<1. The inherited contour bound gives total one-contour activity at most

 Aall=6n q^4/(1-q),
 Atail=6n q^(Mper+1)/(1-q).

Every tuple with a contour above Mper has at least one marked tail member. Summing all1<=j<=8 and dropping its total-perimeter requirement safely gives

 T_tail <=36 Atail max(1,Aall)^7.

Therefore T=T_short+T_tail is a COMPLETE structural predecessor bound. Retain the original modest field tilt rho=1/500000 for target crossings. The same globally valid potential has

 W/ZA <= [nT+n exp(-phi n(1/2-rho)+phi)
                 +kappa exp(-phi n(1/2-rho))]/(1-u4).

This includes structural exits, many-small-droplet majority crossings, and source-target overlap. No state outside the corner/Ferrers family is silently assigned zero energy. Take the minimum with the previous crude global upper if this new bound is worse.

At fixed theta and s<=2, a_s-log4 is bounded away from0. Thus choosing Mper=O(R+log n+log(1/delta)) makes the tail smaller than a requested exp(-bR)delta after paying the polynomial prefactor. All finite normalizers and sums above are acquired by positive arithmetic. This does NOT prove polynomial W/C: the non-simple walk overcount, tuple rooting, and field-volume relaxation may still lose exponential surface-scale factors.

## 5. Cheaper complete-upper implementation

MAGNETIC_MOMENT_REDUCTION.md replaces explicit area storage by admissible exponential area tilts and local shoelace-step weights. Its endpoint-only recurrence takes O(Mper³) arithmetic work/O(Mper²) storage per tilt, while retaining a complete upper via the same area-cap, tuple and tail inequalities. A rational-tilt implementation is explicit. This is the preferred next implementation; the area-resolved DP above remains a transparent exact reference.

## 6. Executed checks and precise remaining task

walk_area_check.py enumerates every nonempty3x3 primal spin pattern (511 total), builds its exact fixed-triangulation dual walls, and verifies closed degree2 geometry, integer area, and dual length<=2P. For all280 one-loop patterns, enclosed dual area equals actual plus count. It also executes both-root positive closed-walk DPs through physical perimeter8; all actual one-loop examples within that perimeter occur in the overcount. Root types agree. It includes non-simple extra words explicitly.

No retained R80 or larger capacity sum was executed. The dense polynomial bound is steep, and even a sharper theoretical acquisition representation is not automatically practical. Nor is a sample from these overcount walks an actual energy edge: rejection to compatible simple source contours could be rare. The next test is whether a better compressed DP or a controlled saddle evaluation makes this complete upper both sharp and usable. Until then this is a global acquired-upper construction with a clear cost and bottleneck, not a solved rate algorithm.
