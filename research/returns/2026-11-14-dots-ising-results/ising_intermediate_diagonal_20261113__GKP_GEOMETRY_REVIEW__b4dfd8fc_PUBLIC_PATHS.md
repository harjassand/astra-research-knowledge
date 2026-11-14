# Independent geometry review: intermediate diagonal front

Reviewed SINGLE_PIN_BAND.md, HULL_MAJORITY_CANDIDATE.md, CONNECTED_MINUS_REPAIR.md and north_compute_20261113/ising_shadow_envelope/RESULT.md. This review concerns geometry, not a new partition or occupation theorem.

## Findings

1. The single-band selection is essential and coherent under the adaptive physical plus4/minus8 wall convention. The NN-connected main collar has diagonal homology and cannot contain an independent essential cycle while disjoint from the actual essential minus8 collar. Its lifts are ordered NN separators. The retained minus endpoints and extra fourth-corner pins form one essential 8-connected band on the left of each copy. Local adjacency to that copy prevents a jump across another NN separator. The chosen right strip therefore has one adjacent pin band, not the union of all torus translates.

2. Compute's discrete envelope proof supplies a particularly direct justification for the area bound. A cut with no west crossing has a unique east crossing and vertical drawdown at most S. For a bad cut, a right-to-left extremal time interval cannot contain a whole period, since its horizontal displacement would be positive when W<L. Its vertical rise is at most L+S. At most W cut residues are bad. Thus the summed envelope width is at most L(W+S). The explicit shifted-index pin thickening costs 6L; the proposed 8L margin is conservative.

3. Frozen initial bounded complement pockets do not enlarge this hull. Their physical neighbor boundary belongs to D, so vertical rays first encounter D. They are not physically adjacent to the processed essential complement: otherwise they would lie in its original 8-component. Their actual thermal bits remain unchanged; filling them in a conditional comparison is algebraic cancellation only.

4. The corner argument proving final bootstrap containment in the pin hull is valid in the selected finite-transverse diagonal strip. A pin-free northwest quadrant intersects the strip in a finite set; a maximal y-x site has north and west plus neighbors. Southeast is symmetric. These are perpendicular-neighbor births, not an assumption about all possible legal births.

5. Hole-first repair works with 8-connectivity and physical neighbor eligibility. A detached component's only exterior minus contacts are copies of its gate. Extremizing x-y avoids all gate copies because that functional is invariant under (L,L). If the eligible site is an articulation, recurse into a smaller component not containing the retained gate. This gives a legal non-articulation deletion. No single finite lift of the component plus its gate is assumed.

6. The global topological premise should be stated explicitly: two essential minus components cannot be newly separated by a birth while the plus set remains NN-connected to the original essential collar and one fixed essential minus band survives. A new plus separator between two essential minus separators would be in a different complementary region from the original plus collar. Physical NN connectivity would require crossing a minus8 separator. This is the NN/8 separation argument, not same-connectivity planar intuition.

## Limits

The majority conclusion follows for p<2.5L and L>32 from |M|<=L(p-2L)/2+8L<n/2. The deterministic schedule and retained label are needed unchanged in every source fiber. Extra actual plus bits can only cause skipped additions; they do not alter the reference geometry.

This review does not independently rederive the conditional contour partition, visible-label multiplicity, capacity upper bound or finite occupation constants. It does not establish arbitrary diagonal-wall completion beyond p<2.5L, or any no-essential-wall occupation bound.
