# Area-admissible clean completion: geometric interface

This extends only the geometric schedule, not its quantitative partition receipt. It is a candidate interface for the two-axis residual decomposition and retains the original source weights, voltage and soft clock.

## Hypotheses
There are exactly two resolved physical axial essential walls. Fix an oriented actual wall gamma with plus on its right. Its main plus collar D is the NN-connected essential collar in CONSTRUCTION.md. Use a proper horizontal lift with span sufficiently below L that the cut described below lies strictly beyond the full rightmost collar column. Let xmin and xbar be the minimum and signed-area mean of the PHYSICAL cell-boundary wall (infinitesimal checkerboard resolution, not a finite-area triangular polygon). Put a=xbar−xmin. Let h be the number of actual minus sites in the erased plus annulus between the two essential walls.

Use the same retained visited-plaquette pins, right-only connected-front bootstrap and hole-first deterministic tie breaks as the short-span theorem. They depend on gamma and its retained local encoding only, not on additional thermal bits. Freeze all initial bounded components of the artificial complement of D. After obtaining the full rightmost column, sweep complete columns towards the periodic copy of gamma, stopping at the vertical cell boundary xmin+L−4. Physical square-dual extrema and vertical cell boundaries have the same half-integer coordinate convention, so this cut requires no additional rounding. Take the zero-resolution limit for checkerboard contacts. The geometric area loss relative to xmin+L is exactly4L.

## Count of guaranteed actual plus sites
The oriented region between gamma and this straight boundary has area at least

 n−L(a+4).

This is Stokes' signed-area identity, valid with overhangs. In the proper lift this is an actual right-hand region, not an algebraic overlap count. Every site in it is either in the retained plus collar, in the initial essential right complement which the template fills, or in an initial bounded complement pocket which the template retains.

A bounded pocket on this right side cannot contain or cross the opposite essential wall: that wall would have to cross the boundary D to enter or leave, and D consists entirely of actual plus sites. The opposite wall cannot lie wholly in a bounded pocket because it is essential. Thus every such right pocket lies in the ERASED plus annulus. Its retained minus sites are among the h defects. Nested contours do not change this conclusion; all actual minus sites are counted in h. The guaranteed actual plus count at the terminal template is therefore at least

 n−L(a+4)−h.                                         (A)

If (A)>=n/2, the actual monotone path reaches B by this terminal template; stop at its FIRST visit. Retained extra plus sites can only advance that stopping time. The analogous construction from the other wall gives n−L(b+4)−h.

## Pins, labels, conditional fibers
The four-column reservation keeps the sweep away from all periodic visited-plaquette pins; these extend at most a constant one-column offset from gamma. The initial right-complement pockets and left component remain frozen exactly as in PIN_CANCELLATION.md. Hence actual gamma remains visible. The full reference template is fixed by the label, while individual sources merely skip already-plus sites and stop at B. Restricting to sources satisfying (A) does not introduce an equilibrium conditional law: their fixed-edge overwrite fiber is a SUBSET of the same positive conditional partition sum, so relaxing this restriction is an upper bound.

All original weights w, conductances g, voltage v and clock kappa remain unchanged. Once an appropriate pointwise fiber bound is proved, the original site-cut current inequality applies. This note is NOT itself that bound.

## Applicability and remaining gaps
If p<2.6L+8, transverse wall span is at most(p−L)/2<.8L+4. At L>=640 the rightmost collar is well before the reserved terminal cut, so the proper-lift/sweep requirement is available. This alone does NOT guarantee (A); failed cases are exactly the specified area-inequality class, not a general path failure claim.

Independent review is requested for (i) the right-pocket/erased-annulus inclusion and (ii) the precise cell-boundary rounding margin. The conditional partition estimate must still be paid at this wider wall length. Large filled contractible contours, non-axis walls, four essential walls and no-essential-wall sectors are NOT addressed by this geometric interface.

## Independent review received
GKP independently checked the physical half-integer cut and signed-area formula, the proper-lift clearance (at least .2L−8.5 beyond the main collar for p<=2.6L+8), and the bounded-pocket argument: essential walls cannot enter a contractible pocket with actual plus boundary, and erasing all contractible loops makes the entire pocket plus. This uses the previously proved selected-left-boundary plus4/minus8 interface, not an arbitrary unresolved contour convention. Quantum independently checked the restricted-source/overcounted-fiber logic and is deriving the wider-length partition receipt.
