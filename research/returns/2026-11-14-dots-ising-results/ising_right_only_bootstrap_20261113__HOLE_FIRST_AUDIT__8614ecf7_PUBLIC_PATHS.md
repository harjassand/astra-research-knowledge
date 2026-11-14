# Hole-first bootstrap with periodic gate images

This is a constructive topology lemma for the cylinder, not yet an occupation theorem.

## Assumptions
Current plus K is physically NN-connected and contains a fixed vertical winding seed. Start from its essential right8-minus component R0. Freeze every other initial minus component (the essential left component and bounded pockets). Only sites in R0 may be added. Retain the far-right half-cylinder minus; additions are restricted to x<=xmax of the initial seed. Every actual addition must have at least two NN-plus neighbors.

Initial frozen minus components are not8-adjacent to R0, and subsequent deletions from R0 cannot create such adjacency. Hence every NN neighbor of a remaining right component that is neither in that component nor at the designated gate is plus.

## No separated essential pocket
Suppose deleting one eligible gate a separates a component C from the far-right component. C has bounded horizontal extent. If C is essential, choose an essential8-minus loop in it. The fixed plus seed is on its left. At the rightmost edge of C there is a NN-plus neighbor on its right: otherwise an8-adjacent minus site would belong to C, and frozen minus components cannot be adjacent to R0. Thus the new NN-connected plus set would have sites on both sides of an essential8-minus separator, impossible by digital planar separation. Therefore all components cut off from the far right are contractible.

The far-right component remains the unique essential component. A cutoff pocket cannot contain x>xmax, since that entire untouched half-cylinder is connected to the far right.

## Periodic escape complication, explicitly retained
A contractible pocket C may become essential after its gate a is restored. Its finite lift can therefore touch several periodic images of a. One must NOT silently apply a finite-plane rooted-pocket lemma to C union a with only one lift of the gate.

All lifted images of a lie on the same vertical line x=a_x. To find an eligible cell of C:
- If C has any x<a_x, choose its leftmost such column and the topmost cell in that column. Its west and north neighbors are outside C and are not any gate image.
- Otherwise, if C has any x>a_x, use the rightmost/topmost cell. Its east and north neighbors have the same property.
- If C lies wholly on x=a_x, both west and east neighbors are outside C and are not gate images.

These two neighbors are plus, so the chosen cell is eligible. This argument tolerates arbitrarily many periodic images of the gate.

## Safe recursive order
If the eligible cell v is not an articulation of the current right8 component, add it safely. If deleting it cuts off pockets, recurse on one not containing the old gate a. Such pockets are strictly smaller subsets of C, are contractible by the preceding separator argument, and have only periodic copies of v as possible minus escape neighbors. Apply the same corner rule. The recursion terminates on a strictly smaller finite vertex set, producing an eligible non-articulation cell.

Repeat until the original pocket is filled, then the original gate becomes safe. Its eligibility cannot be lost when more neighbors become plus. Thus every eligible but unsafe gate can be replaced by a finite sequence of safe eligible additions. The remaining right-minus component stays8-connected and essential at EVERY actual prefix.

Combined with the earlier right-boundary turning argument, this gives a connectivity-preserving right-only flattening: a stalled configuration with any eligible unsafe gate would admit a safe eligible replacement, so genuine termination still forces a straight right boundary.

## Limits
The proof requires the proper lifted cylinder and a physically NN-connected essential plus seed. It does not apply directly to diagonal-only augmented seeds, arbitrary torus-spanning geometry, or frozen components that were initially adjacent to the chosen right component. It also does not automatically supply an improved Gibbs partition bound; that is a separate source-weight calculation.
