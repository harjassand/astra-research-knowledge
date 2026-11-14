# Fixed-diagonal filled-contour decoder with full vertex-touch support

`filled_trace.py` exports `filled_domain_from_steps(steps,diag,start=(0,0))`. Physical directions areE0,N1,W2,S3. Primal site(x,y) is represented by unitcell[x,x+1]×[y,y+1]; the walk lives on cell-boundary vertices. `diag(x,y)=True` chooses the SW-to-NE zero-coupling diagonal in the plaquette with southwest site(x,y). Caller must apply the global placement to this oracle for nonuniform graphs.

The decoder accepts repeated VERTICES. It does not accept repeated directed physical EDGES, inconsistent orientation, winding values other than0/1, a disconnected augmented plus domain, unfilled minus-component holes, or a boundary traversal with the wrong fixed-diagonal pairing. It returns the filled setD, not its thermal interior spin pattern. Temperature, rates, field, target and source are not changed.

## Checkerboard pairing rule

At a dual vertex with two incoming and two outgoing physical boundary edges, its four primal cells alternate plus/minus. If the supplied diagonal connects the plus pair, incoming directiond is followed by right turnd−1(mod4). If the supplied diagonal connects the minus pair, use left turnd+1(mod4). Every other boundary vertex has a unique outgoing continuation. These are exactly the two planar resolutions; in particular a permitted plus diagonal produces a vertex-touching figure-eight outer trace rather than two independent contours. The opposite diagonal produces separate positive components.

The derived domain must have one positive outer boundary cycle with this successor rule. Matching every successor is stronger than checking only the same boundary-edge set. Its cyclic starting position is arbitrary; no rooted-word multiplicity is silently changed by this validator.

## Relation to the recovered source

The archived `01_global_cut/MAGNETIC_MOMENT_REDUCTION.md` specifies physical dual edges as boundaries of unit primal cells, zero-area diagonal contacts resolved by the fixed augmentation, and winding1 on precisely the filled primal sites. It explicitly permits vertex-touching contracted traces. The archived bridge review imports the disjoint outermost filled-domain/collar convention. This decoder implements those physical-trace and fixed-triangulation conditions; it is not a substitute for the broader original topology/collar theorem.

Filling bounded components of the complement on the SAME supplied augmented graph matches the planar resolution: at a checkerboard only the chosen diagonal pair connects locally, and the other pair is separated. In particular treating both diagonals as allowed would give the wrong holes and wrong component law. `fill_holes(C,diag)` blocks onlyC, retaining all bounded interior cells regardless of their original thermal spins. This is suitable for deriving the filled domain of one actual plus component. For a full configuration, compute such domains for its actual augmented plus components and keep outermost domains; unexpected nonnested overlap should trigger a technical error or the explicit topology handling, not silent null filtering.

## Executed checks

All connected subsets of a3×3 window under uniformNE, uniformNW and alternating diagonals were checked:881 accepted connected masks, including233 vertex-touching outer traces. Each was filled, traversed under the supplied pairing and reconstructed exactly. A two-cell diagonal figure-eight is explicitly accepted under its correct diagonal and rejected under the opposite one. Receipt:filled_trace_tests.json.

This is exact finite validation, not proof that an upper-only DP receipt implements backward word sampling, nor an R200 acceptance/runtime guarantee. Filling, connectivity, provenance and successor checks have explicit costs proportional to the represented domain/word sizes. No nonempty-thermal-background auto-rejection or universal repeated-vertex rejection is permitted by this interface.
