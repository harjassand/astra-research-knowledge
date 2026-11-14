# Independent integration review: actual-wall p <= 2L-8

Reviewer: north_bridge. This review covers the present coordinated mathematical construction, not source-sector completeness or novelty. No new large-system trajectory experiment was performed.

## Documents inspected
- INTEGRATION_CANDIDATE.md and CONNECTED_PIN_PARTITION.md in this directory.
- ising_physical_phase_boundary_20261113/{CONSTRUCTION,SHORT_SPAN_COMPLETION,PIN_CANCELLATION}.md.
- ising_right_only_bootstrap_20261113/HOLE_FIRST_AUDIT.md.

## Pin topology and cancellation
The distinction between the ACTUAL preserved plaquette bits and the AUXILIARY conditional boundary is essential and is respected in the current notes. The reference geometry defines D and its artificial8-complement before reading arbitrary extra source spins. The initial right component R0 is different from the left component and every bounded complement component. Different8-components have no physical adjacency. Since the erased prefix F is a subset of R0, none of those frozen components interacts physically with F. Their contributions cancel identically in each ratio, not approximately.

Filling a bounded component plus attaches it to D through its boundary and removes an enclosed hole; setting extra frozen-left plus bits minus is also a ratio-preserving operation. Keep gamma's original local triangulation choices rather than recomputing the adaptive rule after those algebraic changes. The traversed triangles keep their endpoint signs, so gamma survives. Elsewhere minus-biased auxiliary diagonals can connect8-neighbor minus pins; if a missing minus diagonal is not selected, a two-step minus physical path exists unless opposite corners are both plus, in which case selecting the minus diagonal is compatible. Main plus pins are already physically connected.

In contrast, unprocessed arbitrary source plus bits in R0 MAY interact with F. They are not canceled. Their replacement by minus is justified by ferromagnetic boundary monotonicity of w(source_F)/w(allplus_F), keeping the mandatory plus pins. This gives an upper bound and must not be described as an equality.

## Completion and periodicity
The axial physical wall has horizontal step count H<=p-L and zero horizontal displacement, so horizontal range<=H/2. Including collar corners gives inclusive width<= (p-L)/2+2. With p<=2L-8 the width is<=L/2-2. The last required straight column is xmax+L/2-1, while the earliest protected periodic collar image is at least xmin-1+L; the difference is at least3. Thus the proof does not encounter a retained periodic label bit before majority.

The hole-first lemma explicitly handles a contractible pocket touching multiple periodic images of its gate, rather than incorrectly invoking a one-gate planar argument. Its corner choice avoids the gate's entire vertical line when possible. Its recursive subpocket size decreases. The reference plus set remains physically connected; the remaining right minus set stays essential and8-connected. Once the rightmost full column forms, this maintained right component cannot have sites on the column's left. This is the point needed for the claimed straight front.

## Native edge reconstruction
For a given visible gamma, fix the root, lift, axis convention, and all hole-first/eligible-site tie choices canonically, as functions of gamma only. These choices should be explicitly retained in any eventual algorithm specification; they require no probability or extra label count. The resulting reference order does not depend on arbitrary source plus spins. Actual plus sites cause skips, but at an actual flip the site identifies a unique position in this fixed order. All earlier geometric sites belong to F, including skipped ones. Unprocessed source spins are read at the edge; erased spins are summed by the partition ratio.

All visited-plaquette bits remain physically unchanged. Therefore gamma is an actual component of the same deterministic resolution at BOTH native endpoints. There are at most2n/L such essential components because they use disjoint physical disagreement edges. No enumeration of abstract wall words or hidden root factor is needed. If source assignment chooses one of several anchors, select a canonical anchor or positively overcount them; the pointwise component bound still pays this choice.

## Partition and constants
The connected-pin contractible-loop deletion is valid: a connected essential pinned set cannot enter a contractible disk without crossing its boundary, and cannot be contained in that disk. After deleting contractible loops, the remaining spin assignment is still pin-compatible, so its perimeter obeys the stated minimum-cut bound. The ONE versus >=THREE remaining essential-cycle split correctly retains the possible multi-cycle sector.

Bootstrap replay from every compatible assignment proves g=0, not merely a low barrier from one reference state. During the straight phase the retained essential gamma plus another essential interface forces Pmin>=p+L, while the reference moving boundary has length at mostL+2; thus g<=2.

I reran short_conditional_scalar.py. Its exact rational certificates reproduce the negative exponents94,567,3858,41368. The two native heat-bath endpoint ratios, <=2L visible labels, n coordinate-current cuts, >=3-cycle remainder, and ordinary loop pressure are retained. The original core, kappa, capacity, target and clock are unchanged.

## Conclusion and limits
I found no additional mathematical gap in the SHORT-SPAN integration as currently written, with canonical geometry-dependent tie choices made explicit. This does not validate the rejected wider p<2.45L completion, diagonal-only original-core winding, all longer interfaces, no-winding-wall sectors, or a full exit/residence theorem. The pressure factor remains finite-volume and must not be silently promoted to an asymptotic uniform result.
