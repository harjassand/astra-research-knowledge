# Incremental rectangle construction avoids arbitrary closure denominators

Explore an ORIGINAL augmented-connected component in deterministic connected-prefix order. Stop when either bbox side first reaches400; the other side is then<=400 because each added adjacent vertex changes coordinate spans by at most1. After every newly explored original vertex outside the current bbox, immediately fill the enlarged bbox. Original vertices already inside the bbox need no additions.

Keep explicit overwrite region U: the previously filled rectangle, the newly exposed original witness, and the new sites filled so far. Do NOT include arbitrary untouched original plus sites outside U in its baseline energy. They remain part of the fixed exterior, and the exact exterior-plus comparison makes their effect favorable.

For an axial extension, the new witness lies in a new boundary row/column within the old transverse span. Fill from the witness in both directions. U is old rectangle plus a contiguous interval of length ell in that row. P(U)=P(old)+2 and
 E(U)-E(full enlarged rectangle)=.04*(w-ell)<=15.96.
All added sites have at least two plus neighbors.

For a diagonal extension, U initially is old w-by-h rectangle plus its diagonally adjacent original witness. P(U)=P(old)+4. Add the bridging site in the new row, complete that row, then complete the new column. Each addition has at least two plus neighbors. Ignoring favorable untouched exterior plus spins, every such addition has exactly two neighbors and keeps perimeter constant. Therefore
 E(U)-E(full enlarged rectangle)<=.04*(w+h)<=31.92,
and decreases to zero.

The original explored prefix remains a connected subset of original x intersect U and spans BOTH coordinates of R=bbox(U). Hence x intersect U contains a marked augmented-connected component with bbox R. For each fixed edge and geometric overwrite record, exterior x outside U is unchanged and recoverable, and
 sum_preimages w(x)/w(current) <= e^31.92 * e^{E(full R)} * sum_{A subset R, A contains a component with bbox R} e^{-E(A)}.
The right sum can be bounded by a marked bbox-spanning component activity (filled-hull magnetic bound plus holes), multiplied by the unmarked polymer gas. Restriction A subset U can be dropped conservatively. This is the precise interface to the existing <=400-square K bound; it does NOT assume current original intersections are connected.

Global path/canonical record assignment, exact marked-hull bound invocation and total multiplicities still require integration. This note establishes the construction and conditional energy interface, not the final congestion number.
