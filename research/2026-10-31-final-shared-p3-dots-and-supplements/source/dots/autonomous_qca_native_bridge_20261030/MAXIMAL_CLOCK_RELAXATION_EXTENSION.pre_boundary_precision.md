# Maximal ordinary relaxation creates an extendible clock boundary

Status: new exact geometric/control lemma, not yet independently reviewed. No quantum causal-cut or bounded unprotected-exposure theorem is inferred.

## 1. Frozen defect boundary and real ordinary updates

Work first with integer clock lifts on a finite graph. Let F be a nonempty set of frozen vertices with values c_v. On a connected component C of the remaining graph, suppose a current height h is1-Lipschitz on every edge in C and every edge joining C to F. Edges entirely inside F need not be valid. Define d_C(x,v) by paths from x through C, with only the final vertex v in F, and

    u(x)=min_(v in boundary F) [c_v+d_C(x,v)].       (1.1)

Then u is the greatest feasible height extending this frozen boundary: h≤u, u is1-Lipschitz on C, and |u(x)−c_v|≤1 on boundary edges. The lower boundary inequality follows from h≤u and h(x)≥c_v−1; the upper follows directly from (1.1).

If h≠u, a legal unit increment exists. Follow strictly decreasing h-values from a vertex with deficit u−h>0. A lower neighbor cannot have zero deficit, since u is1-Lipschitz. The finite descent ends at a local minimum of h, still with positive deficit; incrementing it preserves every incident constraint and h≤u. Hence any sequence that eventually performs eligible updates reaches u after exactly Σ_x[u(x)−h(x)] increments. This is a reachability/progress statement under actual ordinary increments; it is not permission to increment clocks without their associated DATA channels.

For a finite synchronization neighborhood of O(M²) sites and height range O(M), the number of required increments is O(M³). Fresh native service/attempt bounds can price a prescribed sequence or sufficient sweeps, but they do not make those DATA operations semantically harmless near a clock defect.

Modulo clocks require a consistent lift on each component and sufficient alphabet range to prevent an ambiguity along these increments. For a bounded neighborhood one may reserve a fixed constant-factor increase of q. A local phase jump must not simply be assigned a convenient lift without proving the exterior component's consistency.

## 2. Two-dimensional extension from a far boundary

Let F be contained in the L1 ball B_a(0) of Z². Consider the unbounded exterior component, and suppose the accessible frozen boundary heights have range D=c_max−c_min. Let u be (1.1). For x on the sphere S_R, R>a,

    R−a+c_min ≤ u(x) ≤ R+a+c_max.                  (2.1)

For the upper bound, follow a shortest path toward any point of F; stop at its first contact with F. This path has length≤R+a and stays in the exterior until contact. The lower bound is distance to B_a.

If R>D+3a, the restriction u|S_R is1-Lipschitz in the FULL lattice metric, not merely the punctured metric. Indeed, for a pair at distance at least D+2a, use the spread bound (2.1). For a pair at smaller distance, a shortest path stays outside B_a because R−distance>a, so u's exterior Lipschitz property applies.

The integer McShane extension

    U(z)=min_(x∈S_R) [u(x)+|z−x|_1]                (2.2)

therefore agrees with u on S_R and is1-Lipschitz throughout B_R. Thus maximal exterior relaxation supplies a boundary that can be healed by a finite interior replacement.

## 3. Why this is relevant to a single clock root

Ordinary marching updates which test all incident edges never create an invalid edge. Endpoints of a modulo edge whose separation is at least3 cannot advance through that edge by a single legal increment. A corruption from an initially valid field therefore leaves the residual invalid-edge set inside the original corruption's fixed neighborhood, although valid exterior heights can continue evolving.

For a single clock root, a phase far from every neighboring correct value is isolated by the frozen star; the far value is not accessible from the exterior component. Accessible boundary values come from the original neighboring clocks, with O(1) range. If the root is accessible through a still-valid or single-increment-healable neighbor, its lift differs from that neighbor by only O(1), again giving an O(1) accessible range. This observation motivates using (2.2) at fixed radius rather than resetting an entire M-scale synchronization neighborhood. A full case-checked statement for arbitrary native-root footprints and shrinking frozen sets remains to be written.

## 4. Remaining physical and quantum obligations

* A slow repair rate can make an uninterrupted ordinary-relaxation window likely. It does not prove that its DATA/current-old-buffer evolution admits a valid quantum cut, or bound the QEC exposure around the frozen defect.
* The finite native schedule must supply the required ordinary updates and the actual gap between repair attempts, including already active repair owners. A mean waiting-time argument is insufficient.
* A repair that writes all of B_R has that full semantic damage footprint if its controller is corrupted. `READ_ONLY_CLASSICAL_CLOCK_COMPILER.md` reduces read-only amplification but does not make a large write set small.
* For multiple fault roots the radius/range and damage count must scale noncircularly with the number of roots. A one-root extension is not the threshold's cluster theorem.
* The nearby DATA may need an actual local erase/purge and a quantum-safe rejoin. Equation(2.2) repairs clocks, not unknown quantum data.

Thus this is a concrete geometric ingredient for a slow-repair/purge construction, not a completed asynchronous compiler.
