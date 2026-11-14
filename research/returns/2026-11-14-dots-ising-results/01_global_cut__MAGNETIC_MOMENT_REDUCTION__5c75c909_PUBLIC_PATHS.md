# Endpoint-only magnetic moments: a cheaper global-trial implementation

The area-resolved DP in RESULT.md is not necessary to obtain a COMPLETE upper. For any t in[0,2phi] and any actual contour with V<=Vmax=floor(s²R²),

 exp(2phi V) <= exp[(2phi-t)Vmax] exp(tV).

Let M_P(t) sum exp(t*signed_area) over ALL rooted nonbacktracking closed dual words of physical perimeterP, both dual root types, first step physical. Negative-area and zero-area words may now be retained: their weights are positive and only enlarge the upper. Actual positive simple contours are still included. Consequently

 A_P <= n exp(-2theta P) min_(t in chosen grid)
                   exp[(2phi-t)Vmax] M_P(t).

Use this upper for each coefficient in exactly the same8-tuple convolution and paid long-perimeter/source/target formulas. Taking a minimum among valid positive upper coefficients is legitimate. No claim is made that the bound is sharp without evaluating it.

## Local weight and finite-state recurrence

In the coordinates of RESULT.md, put r=exp(t/18). Each dual step from(u,v) by(du,dv) has positive weight r^(u*dv-v*du). The product around a closed word is r^(18*signed_area)=exp(t*signed_area).

Collapse every run between physical edges: after a physical edge, either take the next physical edge directly (not its reversal), or take the unique zero-coupling edge and then a physical edge. Zero edges cannot be consecutive. Store endpoint, dual type and last physical direction. At each physical perimeterP, record a closure either directly at the endpoint or by its optional final zero edge. Root the first edge physically. This enumerates each such word once, including repeated vertices; the previous microstep's nonbacktracking constraint is respected.

There are O(P²) possible endpoint states and constantly many directions/types at perimeterP. Running through Mper therefore costs O(Mper³) positive arithmetic operations and O(Mper²) storage per tilt, rather than tracking signed area explicitly. This is arithmetic complexity, not a claim of negligible bit precision or practical R10000 runtime.

## A rational implementation avoiding unknown tilt exponents

Choose a rational r>=1 with18log r<=2phi, for example r=1+alpha*(2phi/18), rational0<=alpha<=1. Then the coefficient upper can equivalently be written

 n exp(-2theta P+2phi Vmax) * M_P(r)/r^(18Vmax).

Every DP path weight is rational. Signed exponents and the denominator must both be retained; replacing r by an upper approximation without handling negative powers would be invalid. Rational r gives a finite exact algorithm with polynomial bit lengths (potentially O(Mper²) exponent size). Only the final physical exponentials need outward enclosure. Alternatively a positive interval DP can charge all rounding errors. The inequality log(1+x)<=x proves the selected rational tilt is admissible without a transcendental comparison oracle.

## Executed independent small check

magnetic_moment_check.py compares this endpoint-only recurrence with the independently enumerated signed-area DP, for BOTH root types, rational r=1 and101/100, all physical perimeters through8. Every exact rational weighted sum matches. Maximum stored endpoint states220. This tests enumeration, optional zero-edge closure, signs and local area weighting. It does not test a growing critical droplet or establish a better large-instance capacity bound.

## Remaining actual gap

This makes the globally valid upper substantially more accessible, but the complete finite-R convolution has not yet been run. Overcounting self-intersecting words, relaxing compatibility among affected contours, and the field-volume cap can still incur exponential surface entropy. An acquired global energy upper is not an energy-edge proposal for the actual cut; rejection from these overcount walks may be rare. Any near-optimality claim still requires a quantitative comparison with a valid lower, and the original estimator's proposal contract needs a separate acquisition step.

## Exact contraction to a square-lattice nonbacktracking trace

There is a simpler implementation, not just a small-instance coincidence. Collapse each zero-coupling dual edge to its plaquette center. A physical dual crossing then moves that center by one horizontal/vertical square-lattice step. Given the previous physical direction, each of the three non-reversing next directions has exactly one lift: either direct or through the unique zero edge. The first direction chooses the appropriate dual root type, and an optional final zero edge closes its type. Thus all four first physical directions correspond exactly to the sum over both dual root types. We allow reversal between the last and first edge of the closed word, as did the earlier overcount; actual simple contours never need that extra class.

The area equality is exact for EVERY closed word, including self-intersections. In scaled coordinates write each dual vertex as c_i+delta_i, where c_i is its plaquette center and delta_i is one of the opposite vectors(1/2,-1/2),(-1/2,1/2). All deltas are parallel. The difference of closed shoelace sums is

 sum_i cross(delta_i+delta_(i+1), c_(i+1)-c_i).

Each summand vanishes: on a physical edge the deltas are opposite, while on a zero edge the centers coincide. After dividing by18, the signed area is therefore the ordinary square-walk shoelace area. This justifies an ordinary square-lattice endpoint/last-direction DP with local weight exp[(t/2)(x dy-y dx)].

physical_trace_check.py independently compares the exact rational physical-trace moments to the full dual recurrence for both activities throughP8. All match. The compiled magnetic_probe.cpp uses this identity with long-double positive arithmetic and occasional common scaling. It is explicitly a numerical DIAGNOSTIC, not an interval certificate; truncating endpoint distance to min(p,Mper-p) is safe because any trace returning by Mper must satisfy that bound.

## Fixed but nonuniform diagonal resolutions

The primary interface says a fixed diagonal per plaquette; it need not mean one translation-invariant choice. The preferred physical-trace upper does NOT need uniform choices. The centroid-area argument above and its executable small tests used the uniform diagonal and should not alone be cited for mixed diagonals.

For arbitrary fixed choices, use physical square-dual edges between plaquette centers and contract each zero dual edge to its center. An actual simple resolved contour then becomes a closed physical trace, possibly touching a center several times. It cannot immediately reverse a physical edge: that would revisit the same resolved edge, while the only intervening zero step moves to the other triangle where that physical edge is unavailable. With the fixed resolution known, incoming/outgoing physical ports determine whether the zero edge is traversed; thus the physical word and its root reconstruct the original contour and preserve injection.

The filled area is computed COMBINATORIALLY, not from mixed triangle centroids. Regard each primal spin as the center of its unit square Voronoi cell. Physical dual edges are the sides of these cells; augmented diagonal connections are zero-area contacts at cell corners, resolved according to the fixed diagonal. A positively oriented resolved outer contour has winding1 on exactly its filled primal cells and0 elsewhere. Contracting its small resolution near plaquette centers cannot change winding at any primal site. The physical trace's signed shoelace area is therefore the number of filled sites. The statement remains true for vertex-touching traces; the vertex contact has zero area. Fixed resolution removes any ambiguity about which filled domain the trace represents.

Accordingly the ALL physical nonbacktracking square-walk moment is a valid overcount uniformly over the source's fixed choices. No new2^n resolution factor occurs, and the core itself is unchanged. This is the topology interface submitted for independent review, not something established by the uniform-diagonal finite test alone.
