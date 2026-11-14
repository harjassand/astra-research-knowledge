# Geometric completion and pin accounting for p <= 2L-8

This is the geometric interface requested by quantum's CONNECTED_PIN_PARTITION.md and short_conditional_scalar.py. It deliberately does NOT claim the larger p<2.45L range.

## Exact width bound
Contract the selected zero-cost dual edges to physical square-dual steps. A lifted axial wall of physical length p and vertical displacement L has H horizontal steps with H<=p-L and zero net horizontal displacement. Its horizontal center range is at most H/2. Every main plus-collar vertex is a corner of a visited plaquette, at most1/2 horizontally from its center. Hence the collar's inclusive integer column width satisfies

 w=max_x(D)-min_x(D)+1 <= (p-L)/2+2.

For p<=2L-8, w<=L/2-2. The side pins of visited plaquettes extend at most one column to the left of min_x(D). A minus pin cannot lie to the right of max_x(D): it would then be connected to the far-right minus half-cylinder, whereas the connected essential minus collar lies on the left side of the NN-connected winding plus collar.

## Right-only bootstrap and majority
Lift the collar into this proper horizontal strip. The independent right-only bootstrap proof completes column xmax(D), using only sites to its right side with x<=xmax(D); hole-first ordering retains connected essential unprocessed minus pins at every prefix. Actual source plus bits only cause skips. Stop immediately if actual B is reached during this stage.

Once column xmax(D) is full, the remaining essential right-minus component cannot retain any site on its left: that full plus column separates the cylinder, and hole-first ordering has kept the right component connected. Thus its moving front is genuinely straight.

At most L/2-1 additional FULL columns are needed: together with the existing full column, they contain n/2 plus sites and force B, regardless of every other spin. The last possible column is xmax(D)+L/2-1.

The earliest periodic image of any retained left collar pin is at least min_x(D)-1+L. Their difference is

 [min_x(D)-1+L] - [xmax(D)+L/2-1] = L/2-w+1 >=3.

Therefore neither endpoint of any used edge reaches a protected periodic collar image. All actual visited-plaquette pins remain unchanged. This proves majority completion with a three-column safety margin under the stated conservative bound.

## Conditional pins and cancellation
Use PIN_CANCELLATION.md: extra left checkerboard plus pins and initially bounded pockets are not physically adjacent to the processed right component, so their terms cancel in every source/reference ratio. Set the former minus and fill the latter plus in the AUXILIARY comparison only. This produces a physically NN-connected essential plus pin set, while hole-first right growth and the untouched opposite torus band give an essential8-connected minus pin set.

Choose a prefix-specific auxiliary triangulation connecting those minus pins, extend gamma's retained local choices, then freeze that triangulation for the entire conditional sum. The physical Hamiltonian, actual core and clocks are unchanged.

Every bootstrap prefix is an exact pinned perimeter minimizer: replay its prescribed two-neighbor additions from any compatible source subset, skipping existing plus spins. No perimeter can increase. Therefore the minimum-cut gap is0. After the straight front forms, its length is L or L+2; a retained fixed essential gamma plus essential opposite pins imply a minimum remaining wall length L, giving gap<=2. All relevant contractible pinned pockets have been removed by the exact cancellation, not discarded from the probability model.

## Label count
At an actual edge every source anchor gamma remains an actual closed component under the deterministic physical-plus resolution. Its local plaquette spins remain readable. At most2n/L=2L noncontractible physical wall cycles can coexist, because physical disagreement edges total at most2n. This is a POINTWISE label count, not an unweighted sum over all abstract contour words.

These statements close the geometric/visibility premises for the quantitative p<=2L-8 application. They do not imply arbitrary axial-wall coverage, diagonal homology, or completion for nearly full transverse span. Quantum's separately paid scalar receipt must still be used, including its >=3-essential-cycle remainder and ordinary wall pressure.
