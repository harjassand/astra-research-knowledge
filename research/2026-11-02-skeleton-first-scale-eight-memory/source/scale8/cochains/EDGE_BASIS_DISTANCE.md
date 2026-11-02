# Edge-local physical bases and the X-logical distance readout

This supplies the basis part of the distance gate for the constructed completion. It is a direct physical degree-one statement; no uncontrolled basis mixing over a growing parent region is needed.

## Par4 resolution in fixed edge-local bases
Suppose the ordered split is (f1,f2 | f3,f4), with auxiliary strip a. Choose the old Par4 basis

 b1=f1+f2, b2=f3+f2, b3=f4+f2.

The degree-two projection fixes old faces and maps a to f2. On the left Par3 stalk choose basis l1=f1+f2, l2=f2+a; on the right Par3 stalk choose r1=f3+a, r2=f4+a. The degree-one projection is

 l1 -> b1, l2 -> 0, r1 -> b2, r2 -> b3.

Thus every fine physical basis qubit maps to either zero or ONE old physical basis qubit. Both cochain identities follow by the tree-resolution cancellation, and the degree-one identity can be verified by applying d to these four displayed columns. This uses only basis changes within each individual edge stalk, not across the two resolved edges.

For Rep4, choose left Rep3 scalar to map to the old scalar, right scalar to zero; P2(a)=f3+f4. Again P1 columns have weight at most one, although P2 does not.

## Consistency through generations
A newly created red degree-four cylinder edge chooses its old parity-star anchor according to its deterministic split in the next refinement. This is a bounded forward choice in the construction, not a retroactive global basis change. Its current sheet readout is zero, so this anchor is unconstrained by the current X-step distance map. The resulting new degree-three bases are thereafter inherited identically on descendants and vertical T seams. Ordinary inherited edge subdivisions use exactly the inherited old edge basis. Newly created red degree-three attaching edges have zero old projection; their basis is free. Thus the requirements do not conflict across generations.

## Disjoint X-step readouts
Let PA^1,PB^1 be old-level refinement projections applied to the two actual sheet restrictions. Every physical column belongs to at most one sheet readout. Cylinder-only columns belong to neither; an attaching qubit belongs to its own sheet edge stalk, not to the other sheet. The edge-local basis choices above and ordinary interval projection imply

 |PA^1 e| + |PB^1 e| <= |e|.

Both PA and PB induce H1 isomorphisms by the unequal-restriction mapping-cylinder proof and relative normalization. Hence if e is a nontrivial fine 1-cocycle, both projected cocycles are nontrivial and

 d_X(new) >= 2 d_X(old)  for an X/blue step.

For a red step, the direct red projection sums inherited edge-code labels on the entire seam network, including both sheet copies and inherited vertical T seams. Its degree-one columns again have weight zero or one in these bases. Once its H1 isomorphism is established by the red fiber transfer, it gives d_X(new)>=d_X(old).

This yields exponential-in-number-of-blue-steps X-logical distance for this basis-specified completion, WITHOUT a recurring constant loss in the recurrence.

## Limitation
This note does not claim the corresponding Z-distance recurrence merely from an abstract sheaf Poincare-duality isomorphism. Such a claim requires controlled physical chain readouts, or a duality construction with the required distance constants accounted for globally. A bounded local Clifford equivalence at each step cannot simply be charged once if it is used recursively; that would risk a multiplicative loss at every generation. The X-distance argument above avoids that error by making the physical basis convention explicit from the start.

## Safe once-at-final-level use of distance duality
There is a way to use distance duality without paying a constant each iteration. Apply the entire X-distance argument independently to the orthogonal-sheaf family F-perp, with its own compatible edge-local basis convention. Its blue steps are the primal red steps. This gives d_X(F-perp,k)>=2^(number of primal red steps) times its seed distance. Only AFTER proving that recurrence, apply the uniform final-level distance comparison in source Theorem2.2 (or explicitly constructed bounded-star duality maps):

 d_Z(F,k) >= c d_X(F-perp,k),

where c depends only on the bounded local stars and edge-basis sizes, not k. A different edge basis on F-perp only costs another bounded per-stalk comparison at this final step. This proves the desired exponential-in-depth Z-distance when the theorem's distance comparison is available with those uniform local constants. It is not a memory-lifetime duality claim. If relying solely on the theorem's displayed cohomology isomorphism, the distance inequality still needs the bounded-star chain-map proof; an abstract H1 isomorphism alone is insufficient.
