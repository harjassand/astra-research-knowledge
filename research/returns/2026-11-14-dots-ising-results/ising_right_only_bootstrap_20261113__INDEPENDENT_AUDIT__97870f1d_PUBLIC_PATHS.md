# Independent proof audit: right-only bootstrap preserves the fixed wall

GKP owns the construction and numerical checks. This note supplies a precise version of the turning argument rather than duplicating those experiments.

## Setting
Work on the infinite horizontal cylinder Z x (Z/LZ). Let D be a finite-width connected plus set containing a nearest-neighbor vertical winding cycle. In the intended application D is the vertex set of a short simple winding cycle. Let L0 be the component of initially minus sites reachable from the far left using8-neighbor steps. The nearest-neighbor plus winding cycle separates L0 from the far-right minus component: an8-neighbor minus edge cannot cross a nearest-neighbor plus polygon without meeting a plus vertex.

Freeze every site in L0 minus. Keep D plus. Repeatedly add any remaining minus site with at least two plus nearest neighbors, restricting x<=xmax=max{x:(x,y) in D}. The rule is deterministic after fixing a tie-breaking order. All candidate sites lie in a finite-width cylinder because x<xmin already belongs to L0.

## Exactly fixed left wall
No initially minus site outside L0 shares a plaquette with a site in L0: all sites of a plaquette are8-neighbors. Thus every allowed new plus site has no nearest-neighbor OR diagonal adjacency to L0. Every physical and fixed-triangulation boundary edge of L0 remains unchanged throughout the operation. The complete left wall set, including any attached finite complications, is fixed; its physical length is at least L because it contains an essential winding component.

This is stronger and more precise than assuming an arbitrarily selected left contour is visibly fixed.

## Why termination forces a straight right boundary
Suppose the finite process has stopped. Examine the interface with the unbounded RIGHT minus component. A plaquette with three plus sites and one right-minus site makes that minus site eligible (two plus nearest neighbors). A checkerboard plaquette with two diagonal plus sites also makes its minus sites eligible. Neither pattern can occur at a stopped right interface. Frozen-left minus sites cannot be substituted into this argument, because they cannot share a plaquette with right-side allowed minus sites.

The restriction x<=xmax does not hide an eligible right corner: all sites with x>xmax are minus, and each has at most one plus nearest neighbor. Hence any eligible corner would lie in the permitted strip.

With checkerboards excluded, the right outer interface is an unambiguous simple polygonal essential cycle. Plus connectivity excludes an isolated plus island as its explanation. The only possible nonstraight corners left are convex-plus corners (one plus and three minus sites). Concave-plus corners would be the forbidden three-plus plaquette.

An essential simple polygon on this flat cylinder has total signed turning zero: the region between it and a far-right straight vertical line is an annulus, so the polygonal Gauss-Bonnet turn sum is zero. A polygon with turns of only one sign must therefore have no turns. The right interface is a straight vertical line. Since the connected plus set contains a site at xmax and no sites to its right, the rightmost column xmax must be entirely plus.

Finite unfilled holes on the right cannot obstruct this conclusion. Their closed contractible boundaries require the opposite total turn and hence an eligible concave-plus corner; alternatively apply the same plaquette argument to each hole.

## Physical accounting
Each added site has at least two plus nearest neighbors, so total physical perimeter never increases. For a seed cycle of length ell, P(D)<=2ell. Removing the fixed left wall length>=L leaves remaining reference wall length<=2ell-L=L+2(ell-L). Subsequent straight-column growth adds at most2 transient perimeter edges and preserves the original left wall.

This supplies the geometry needed by GKP's one-fixed-wall pointwise contour argument. It does not by itself bound label multiplicity, thermal partition pressure, or original occupation; those must still be paid in the full theorem. Initial digital checkerboards are allowed. Their exclusion is only used at a STALLED boundary, where the bootstrap rule itself excludes them.

## Remaining review requirement
The argument uses the ordinary planar cylinder embedding and a fixed single-diagonal triangulation only for contour encoding. It must not be transplanted to a graph with both crossing diagonal interactions, nonlocal bonds, or a seed lacking a physical nearest-neighbor winding cycle. GKP's reported500-cycle tests are diagnostic support, not the topological proof.

## Independent exhaustive diagnostic
check.py enumerated all4096 subsets of a three-column by four-period cylinder. It retained664 nearest-neighbor-connected winding seeds, froze the initial left8-minus component, and executed1184 native two-neighbor additions. Every run preserved the full physical left-wall edge set and completed the rightmost seed column. This is a broader exhaustive local diagnostic than testing only randomly generated simple cycles, while the turning proof remains the general justification.

## Actual-wall labels: exact visibility and its limitations
If an anchor is an ACTUAL wall cycle gamma in the fixed triangulation, pin both spin endpoints of every crossed augmented edge, on both phases. Every dual triangle visited by gamma has two crossed edges whose endpoints together are all three primal vertices. Thus its spin pattern is permanently fixed, and gamma remains exactly the same closed dual component at every path endpoint. A fixed state has onlyO(n) such components. This can replace exponential unobserved seed-word counting by actual visible-wall multiplicity, provided the constructed path never changes those pins.

This observation does NOT prove a small reference-perimeter cost. The plus-side collar may be connected only through the selected zero-coupling diagonals, not through physical nearest-neighbor edges. The left/right digital topology must then use the actual planar augmented graph, not all8-neighbor minus links. Nor may one assume without proof that the canonical plus collar's opposite perimeter is at most the original wall length. These are the outstanding geometric interfaces for that proposed stronger construction.
