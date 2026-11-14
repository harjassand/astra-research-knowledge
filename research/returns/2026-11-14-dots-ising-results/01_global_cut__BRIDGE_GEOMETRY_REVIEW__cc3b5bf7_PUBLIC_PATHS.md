# Independent bridge review: global walk-cut geometry and completeness

Reviewed RESULT.md, MAGNETIC_MOMENT_REDUCTION.md and the inherited optimized-cut RESULT.md on 2026-11-13. This review concerns the proof interfaces, not the directed-arithmetic implementation or a new numerical run.

1. The trial is genuinely global: it is the indicator of M_(s²) outside the actual majority target, with reservoir value1. Since original A is contained in M, only A intersect B contributes source energy; target crossings inside M and structural exits are separately included. It is not the energy of a restricted Ferrers channel.

2. The new counting step legitimately inherits the at-most-eight disjoint OUTERMOST old filled-domain interface from the original fixed-augmentation cut proof. The statement that a gate inside an existing filled domain cannot create a new area/topology violation uses the complete augmented collar convention. Under that inherited convention, simultaneous whole-domain flips retain all interior thermal bits, are injective given the domains and preserve M. No conditional equilibrium or pure-interior assumption is added.

3. For an actual contractible resolved outer contour, contraction of the zero diagonal crossings to plaquette centers gives a closed physical square-dual trace. It cannot immediately reverse a physical edge: the same physical port cannot be reached from the other triangle after its sole zero crossing. Given the FIXED diagonal resolution, each incoming/outgoing port pair determines the lift, so there is no independent resolution label or factor2 per vertex. Canonical root and orientation make the injection into rooted traces valid. The all-walk overcount can include invalid/repeated traces harmlessly.

4. The mixed-diagonal area extension should rely on winding numbers of unit primal cells, not on the uniform-centroid calculation. Contracting/resolving within a plaquette does not cross a primal site; it preserves winding there. A positively oriented actual resolved outer contour has winding1 on precisely the filled cells. Its contracted trace therefore has signed shoelace area equal to the filled-site count, including vertex touches. This argument applies to the fixed source embedding without identifying actual plus count with filled area.

5. The area tilt is one-sided only on ACTUAL domains: V<=Vp=min(floor(s²R²),floor(P²/16)). For admissible 0<=t<=2phi, exp(2phi V)<=exp[(2phi-t)Vp]exp(tV). Summing all signed-area walks with positive weights then overcounts. Retaining negative/zero-area words is safe. Taking a coefficientwise minimum of valid upper bounds remains safe. Rational powers with negative shoelace increments must be kept exactly or outward enclosed; replacing their base by a one-sided approximation is not automatically safe.

6. The tuple convolution pays all ordered roots/labels through A(z)^j, j<=8. Terms beyond the individual-perimeter cutoff are covered by marking one tail member; sum j<=36 and max(1,Aall)^7 justify the stated tail. Dropping total-perimeter requirements on that tail enlarges it. Native gate-site rates are separately bounded by n. The inherited target tilt and reservoir overlap retain their original clocks.

No flaw found in these interfaces under the explicitly inherited cut/topology hypotheses. This does not certify actual energy-edge sampling from the walk overcount: simplicity/compatibility rejection could be exponentially costly. It also does not supply an actual-count canonical G_k: nested thermal contours require alternating areas and cannot simply be replaced by filled-area statistics. The original global count-trial acquisition remains distinct.

## Reviewed root/order/gate refinements

The following sharper counts are valid without changing the source family.

- Divide the rooted physical-perimeter-P moment activity by P. Every actual positively oriented resolved-simple contour has exactly P choices of physical first edge. A rooted physical word together with its plaquette basepoint reconstructs the contour under the fixed resolution. A nontrivial cyclic word period would repeat a physical edge, which an actual simple resolved contour cannot do. Touches created by contracting zero edges do not invalidate this argument. All invalid walk terms remain nonnegative overcount after division.

- Divide the ordered j-contour convolution by j!. The actual affected domains are distinct and disjoint; each unordered tuple has exactly j! orderings with identical product activity. Repeated/invalid overcount labels only add nonnegative mass. This does not assert independence of physical contours.

- The actual structural gate is outside every affected filled domain and is an augmented neighbor, hence a Chebyshev-distance-one neighbor. The outside Chebyshev collar of any D has size at most3P(D). For a diagonal neighbor z of a site a in D, inspect the horizontal intermediate site: if it is outside, z is a tangential neighbor of that physical boundary edge's outside endpoint; if it is inside, z itself is the outside endpoint of a physical boundary edge. A direct nearest neighbor is already an endpoint. Thus every gate is among the outside endpoint and two tangential neighbors of some boundary edge. Summing domains gives at most3S gate labels. Native site rates remain at most1, so truncated tuple weights may be multiplied by3S instead of n.

One may keep the prior n-weighted complete perimeter tail unchanged. This pays all omitted long tuples and avoids assuming the truncated3S sum covers them. These are structural-count improvements, not a new physical clock or an actual crossing sampler by themselves.
