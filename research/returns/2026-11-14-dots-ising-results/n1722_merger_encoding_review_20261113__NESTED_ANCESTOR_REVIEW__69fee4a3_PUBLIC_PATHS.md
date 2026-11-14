# Independent nested-ancestor and source-normalizer review

This reviews MERGER_CLUSTER_CANDIDATE.md. The comparison concerns the physical-small family F and the ORIGINAL fixed-diagonal A and M5; it does not redefine either original set. Standard planar/Jordan properties below refer to the physical-plus4/minus8 outer-disk convention used to define F.

## 1. Laminarity and selection
Filled outer disks of different physical NN plus components are disjoint or nested. Their actual outer boundaries are resolved Jordan curves; two distinct physical plus components cannot have crossing boundary arcs. At an unresolved checkerboard they may touch a dual vertex, but their spin-site interiors are disjoint. Thus every physical component has a unique global outermost filled ancestor, up to coincident selection of the same ancestor.

Choose a bad original augmented plus component K, then take the distinct global ancestors covering its physical NN constituent components. Every selected ancestor intersects K. Solidifying each ancestor gives a physically connected filled disk, so the union U remains original-augmented connected: every original K path lies in U, and every added disk is attached to that path.

For a K step crossing between different selected ancestors, a physical NN step is impossible, since its plus endpoints would be in the same physical component. The step is a permitted original diagonal. If its endpoint were strictly behind an ancestor's outer boundary rather than on that boundary's plus component, the local diagonal would have to cross that Jordan boundary inside its plaquette. The plus corner adjacent to the crossed physical boundary would then be NN-connected to the endpoint, placing it in the ancestor boundary component. Hence a crossing between ancestors produces a genuine diagonal contact of their outer plus boundaries, and their physical dual boundary graphs share the intervening vertex. Contracting the ancestor membership along a path in K proves connectedness of the boundary union. Nested ancestors can belong to a different original augmented component; no such membership is assumed.

## 2. Disjoint physical cut edges and directed reconstruction
Distinct selected outermost filled disks cannot share a physical NN adjacency: their actual plus boundary vertices would then belong to one physical component. Therefore their outer boundary edge sets are disjoint, and their sum is the physical boundary of U. Diagonal contacts create vertices of a connected even graph, not duplicated edges.

Orient each disk boundary with its filled disk on the left. The resulting graph is balanced and connected, so it has a directed Euler circuit. Immediate reversal of a physical edge is impossible because each physical edge occurs only once. The rooted directed word, with at most4n starting directed edges and at most3 subsequent choices, records which side is inside. This resolves the global complement ambiguity of the unoriented edge set. Local edge parity propagated through the connected physical lattice reconstructs U; no separate pairing choice at each checkerboard is required.

Independent diagnostic check.py verified this mechanism in2190 small-component diagonal mergers. These tests did not implement nested filling and therefore do not replace the preceding geometric argument.

## 3. Image family and exact thermal involution
Flip all bits in U. Each source physical outer boundary was plus, so its entire layer becomes minus. New physical plus components inside a flipped disk cannot NN-connect through this minus layer to outside spins; their filled disks remain contained in the old disk. Unselected outside physical components have unchanged vertices and unchanged adjacent spins: otherwise there would have been an NN contact to a selected boundary plus vertex. Their outer disks therefore remain unchanged. This proves image membership in F, including arbitrary nested thermal bits.

Given the directed label U, the flip is an exact involution. Since physical cut edges are disjoint, the weight penalty is the sum over selected disk boundaries. The individual area bound yields the stated exp(-bP) ratio. Injectivity for each label and image containment in F justify comparison with Z_F, not with an invented source law.

## 4. Original failure thresholds
Do NOT identify the filled area of K with the union area of physical disks: a diagonal bay closure can enclose much more area. Instead use the solid synthetic U. Original augmented connectivity is monotone and U contains K, so the original failure persists.

If U is nonwinding, its original filled outer region contains K's filled outer region (or its bounding-box witness). Its outer physical contour uses only physical boundary edges of U, so its physical perimeter is at most P. This gives P>=4sqrt(5)R for M5 failure, or P>=2r for original core box failure.

If U winds, its projection covers all L columns or all L rows. The sum of the finite ancestors' inclusive widths in that coordinate is at least L; each ancestor has physical perimeter at least twice that width. Thus P>=2L. This argument does not incorrectly assign nonzero net homology to the Euler circuit, whose constituent disk boundaries have zero total homology.

In the original fixed planar triangulation, a nonwinding connected component has an injective finite lift. Its resolved outer boundary is contractible and bounds an embedded disk. If the source definition intends any stronger embedding test beyond this usual one, it must be checked separately; no extra failure can simply be deleted by notation.

## 5. Normalizer interface
A subset F follows from physical NN connectivity being contained in original augmented connectivity and monotonicity of filling. The label sum bounds Z_(F\A)<=u Z_F. Therefore ZA>= (1-u) Z_F, and the original normalizer is retained. The M5-failure label tail gives the second stated comparison after this normalizer factor. These are mass bounds; occupation only uses0<=v<=1. No heat-bath clock, soft rate or current law is replaced.

Conclusion: no further flaw found in the directed-label, nested-selection and image-F comparison under the explicit physical filled-disk convention. The original embedded-disk definition should be quoted when closing the remaining source-definition gate. This does not cover a large physical filled domain or a plus-background web with large minus holes.

## 6. Down-set property and an optional proof-basin change
F is decreasing under removal of plus spins. Each new physical NN plus component is contained in an old one, hence in that old component's embedded filled disk. In the finite lift, the complement of the old filled disk is connected to infinity and remains minus for the new component's fill operation. Therefore the new filled outer disk is contained in the old disk. Area, nonwinding and embeddedness persist.

The authorized source's exact residence identity permits ANY down-set M containing A. Thus F may be used as a new comparison basin, keeping the original A, kappa, physical Hamiltonian and native clock unchanged, with its separately paid ZA-normalizer correction. This does not redefine original M5, provide an oracle for the new entrance law, or acquire the remaining physical residence. It legitimately removes an artificial diagonal-merger obligation from the chosen proof decomposition only after paying the displayed F/A comparison.
