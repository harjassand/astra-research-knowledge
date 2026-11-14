# Independent fixed-diagonal audit of the unrestricted corridor construction

Quantum owns the consolidated occupation theorem and scalar certificate. This file records the geometry/conditioning check, not a second theorem claim.

## Strong source geometry
Fix one full plus column at x=0. All other original spins may be arbitrary. Overwrite columns1,...,L/2 in a fixed cyclic row order, skipping initial plus spins and stopping at B. Completion creates at least L(L/2+1)>n/2 plus sites, hence every non-target source reaches B. Even the last prefix leaves column L-1 untouched and separated from the growing front. A union over2L possible oriented rows/columns is explicit; assign a canonical one or pay the union.

At a fixed native edge, all unprocessed original spins are visible in the endpoint. The fiber varies only in the processed prefix F. For each original assignment, the source-to-endpoint ratio decreases when any exterior neighboring spin is changed from minus to plus. Replace all unknown exterior spins except the fixed plus column by minus to upper-bound that ratio. The retained original exterior need not itself be minus or thermal-equilibrium distributed.

## Wall geometry after the artificial comparison
The all-plus-on-F reference has a straight fixed interface between columns L-1 and0 of physical length L. Its other, moving interface has physical length at most L+2: F is a collection of full columns plus one cyclic interval in the next column. Both endpoints of a physical overwrite edge have this property.

For every binary assignment on F, the fixed interface remains exactly the same. The plus column is a noncontractible pin loop separating it from the right-hand configuration. On the fixed planar SW-NE triangulation, each triangle has zero or two disagreeing sides; dual wall components are closed and nonbranching. The zero-energy diagonals resolve degree-four square-lattice ambiguities rather than adding interaction energy.

The fixed interface has nonzero vertical homology. The entire wall set is a boundary, so its total mod2 homology is zero. After removing the fixed interface, at least one remaining wall has nonzero vertical homology. Its physical length is at least L. All remaining contractible loops have physical length at least4. No winding core hypothesis is used.

A partial first column does not create open walls: the entire configuration is still on the torus with the complete plus pin column and complete untouched minus column in the artificial comparison. Alternatively embed F into the full-height strip through its current column, keeping unused sites fixed minus. Contour-count overcounting may drop those pins, but one should NOT silently replace the spin partition by an enlarged-field partition: positive field on newly freed sites would require an extra factor. The intended proof first drops the nonpositive field contribution on the ORIGINAL F, and only then overcounts contour collections.

## Partition accounting
Relative to the all-plus-F endpoint, the field factor is exp(-2phi Nminus(F))<=1. The fixed interface cancels exactly from the interaction ratio. If P is the total physical length of all remaining walls, the ratio is at most exp[2theta(L+2)]exp(-2theta P).

Mark one noncontractible remaining contour (overcounting configurations with several is harmless). Sum that marked contour over length>=L, then sum arbitrary additional compatible or incompatible contours by the usual nonnegative product bound. A conservative100n4^ell count per length avoids a delicate optimized root count. The contour configuration determines the spins once the plus pin column is specified, so no2^number-of-components or global-spin factor is missing.

## What ran
contours.py constructs the ACTUAL dual graph of the SW-NE triangulation on a4x4 torus and traces every wall for all256 assignments of the two variable columns. Every configuration has one fixed interface of length4 and at least one other noncontractible interface of physical length>=4. Loop-count histogram:171 configurations with2 loops,80 with3,5 with4. No topology exception found.

check.py separately verifies2304 binary-source/prefix pairs and511 endpoint fibers with exact rational Ising weights. All satisfy the termwise outside-boundary comparison and reference moving-wall bound. These small exhaustive checks support the general topological proof but do not independently prove a large-volume occupation estimate.
