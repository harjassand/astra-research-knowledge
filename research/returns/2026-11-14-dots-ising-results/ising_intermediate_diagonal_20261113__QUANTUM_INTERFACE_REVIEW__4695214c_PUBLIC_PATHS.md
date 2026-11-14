# Independent intermediate-hull and thermal-partition interface review

This is a review of HULL_MAJORITY_CANDIDATE, not a completed occupation theorem.

## Count and majority algebra
For one lifted periodic NN trace with displacement(L,L), W west and S south steps, W+S=b. There are at most W bad unit-cut residues. A good cut has exactly one east crossing, because its net horizontal crossing number is one and it has no west crossing. Taking a good cut as period boundary makes the segment between successive copies stay within that width-L strip: leaving through either boundary would require an impermissible west crossing. Over this segment total north variation is L+S. This validates the stated good-cut vertical drawdown bound S and bad-cut bound L+S, hence integrated hull area at most L(W+S).

The envelopes U=max past height and V=min future height are monotone and satisfy U(x+L)=U(x)+L, likewise V. Their Minkowski thickening by radius r adds exactly4rL to the integrated upper-minus-lower bound (or less if the hull has empty slices). Thus trace-to-pin radius1 and pin-site-to-unit-cell radius1/2 cost at most6L;8L is conservative. With b<L/4 and L>32, the candidate residual bound Lb+8L is below half the torus.

This count applies to ONE translated pin band. Including unavailable vertices from both collar copies would invalidate its use: even a straight diagonal strip then has pins on opposite sides and its entire area belongs to the quadrant hull. The required premise is that the left copy's outside-D pins all lie outside the chosen right growth strip, while only the next copy's left-side pin band lies inside. This must be established for the full possibly self-touching main collar, not merely for a selected simple subcycle. The inherited statement that every extra visited-plaquette corner lies in the essential LEFT complement is the relevant geometry, but a proper-strip argument is still needed.

## Initial bounded pockets are a separate partition obligation
Filling unpinned bounded components of the initial D-complement is legitimate as native bootstrap geometry. It is NOT automatically covered by the connected-essential-minus thermal partition. During a partial fill, unprocessed sites in that pocket are temporary fixed-minus boundary sites in the auxiliary erased-prefix sum. A contractible contour can contain these pins, so it cannot simply be erased before invoking the essential-wall mincut lower bound.

Even if all additions have two plus neighbors, replay proves a total-perimeter mincut floor only. It does not put that floor entirely into ESSENTIAL wall length. The previously derived intermediate one-loop/three-loop formula needs pin-free contractible-loop erasure. Therefore either:
- show the actual collar class has no bounded D-complement pockets;
- leave all such pockets and their source bits unchanged and prove that the majority hull bound still holds with their paid area;
- or supply a separate full conditional partition for the initial pocket-filling stage, paying forced contractible contours rather than treating them as ordinary unmarked pressure.

After all initial pockets are addressed, the diagonal-cylinder hole-first repair is appropriate for pockets CREATED by an eligible gate: it delays the gate until the prospective pocket is filled, so the remaining minus set stays essential-connected at every actual prefix. This does not retroactively solve initial disconnected components.

## Reference versus actual source
All actual visited-plaquette bits remain fixed. Extra frozen plus corners that interact with the growing prefix can be lowered only by ferromagnetic ratio monotonicity, not falsely canceled. The auxiliary triangulation must retain gamma's local choices while the source bits are summed. The physical source/core/clock and first-majority target remain unchanged.

Conclusion: the stated single-band hull count is mathematically plausible and quantitatively sufficient; its digital pin-band premise and the initial-pocket thermal stage remain explicit obligations. No unconditional intermediate-wall occupation bound is asserted here.

## Constructive repair agreed with fluid: freeze initial pockets
The temporary-pin objection above is resolved without a new pocket partition IF initial bounded D-complement components are left unchanged throughout the actual path. Every point in a contractible component has a finite lift. Its upward and downward vertical rays first leave the component at D (another complement vertex would be adjacent and in the same component). Thus it has a D vertex in each of its NW and SE quadrants and belongs to H(D).

The remaining right-strip sites are bounded by the thickened hull of the next translated copy D+(L,0). Modulo the torus this is the same projected hull as H(D). Therefore untouched bounded pockets and residual right-strip sites are contained in ONE common thickened hull, not two separately added area budgets. Freeze these pockets; apply closure only in the essential right component. The hull-majority estimate remains sufficient.

No grown site is physically adjacent to a frozen pocket, because D separates distinct complement components. Their physical weight factors therefore cancel exactly from source/endpoint ratios. They may be filled plus on both sides of the auxiliary comparison, joining the essential plus set and eliminating disconnected minus pins, without performing those changes in the actual source path. This is distinct from lowering adjacent fourth-corner plus pins by monotonicity.

The still-open premise is the globally consistent single unavailable pin band for the full collar trace. Hole-first repair then applies to new pockets generated within the essential right component, with initial pockets frozen as above.
