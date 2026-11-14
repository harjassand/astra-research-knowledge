# Separating actual visible pins from the conditional partition pins

This clarifies the adaptive-label construction. The actual path preserves every visited-plaquette bit, but the auxiliary partition proof need not carry irrelevant disconnected pins.

## Extra checkerboard plus on the frozen side
Let D be the main plus endpoint collar of gamma. Under the minus-biased encoding D is NN-connected and essential. Treat its complement geometrically as minus and let L0 be the artificial left8 component. A fourth plus corner in a visited checkerboard, not in D, shares a plaquette with gamma's true minus collar. It therefore belongs to L0 when treated geometrically as minus.

Every processed site F lies in the initial right8 component R0, distinct from L0. No R0 site can be8-adjacent to any L0 site, or the components would coincide. Thus there is NO physical interaction edge between F and this extra plus pin, including at later prefixes because F only shrinks the same initial R0.

All energy terms involving that extra pin are identical in numerator and denominator of every source/reference ratio. We may set the extra pin to MINUS on both sides of the comparison without changing the ratio. This is not a physical flip. The actual path leaves its original plus value unchanged, which is why the adaptive label stays visible.

Keep gamma's original local auxiliary diagonal choice fixed during this algebraic substitution. The extra vertex belongs to the other triangle if it is not already in D, so all triangles actually traversed by gamma retain their spin pattern. Recomputing the adaptive rule after the substitution is unnecessary and would be an invalid shortcut.

## Initial bounded pockets
Any initial bounded component of the artificial complement of D is likewise not8-adjacent to R0. If it is never processed, all its interaction terms cancel in the ratio. Set its entire interior to PLUS on both sides of the auxiliary comparison and include it in D'. This fills holes behind the fixed plus boundary, so D' remains NN-connected and essential and its perimeter cannot increase. Again no actual source bit is changed by this proof operation.

The operation removes disconnected bounded minus pins that would otherwise invalidate contractible-loop erasure. The actual path still retains their original arbitrary spins.

## Remaining minus connectivity and auxiliary triangulation
Hole-first ordering keeps the remaining right component8-connected and essential at every prefix. On the actual torus it joins the frozen left exterior through the untouched opposite band, because the short-span construction stays in a proper strip with sufficient unused width. Thus the relevant remaining minus pins form an essential8-connected set after the preceding cancellations.

Choose an auxiliary triangulation that joins minus diagonal neighbors at checkerboards, while preserving gamma's local choices. An absent minus-minus diagonal has a two-step all-minus physical alternative unless both opposite vertices are plus; in that case the minus-biased rule selects the needed minus diagonal. Therefore the minus pins are connected in this triangulation. D' is physically NN-connected and needs no diagonals.

At a visited gamma plaquette these choices are compatible with the original label. If an extra left plus was replaced by minus, it lies in the nontraversed triangle and is physically connected to the preexisting minus collar. No new incompatible connection across gamma is required.

These observations provide the connected-essential-pin hypotheses for quantum's conditional partition lemma in the SHORT-SPAN regime. They do not prove majority completion for arbitrary walls with span approaching L, and do not change the original core triangulation or Hamiltonian.
