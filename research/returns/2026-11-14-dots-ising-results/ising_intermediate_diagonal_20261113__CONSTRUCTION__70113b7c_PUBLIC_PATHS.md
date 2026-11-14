# Native intermediate-diagonal completion with retained actual-wall pins

## Scope and status
Geometric construction for an actual adaptive physical-plus wall gamma with primitive homology(1,±1) and physical length2L<=p<2.5L, L>32. Reflect coordinates to(1,1). The source is outside original B. This is a construction/partition interface, not the full residence theorem. Quantum owns the paid conditional partition and finite occupation receipts.

## 1. Collar and a single unavailable pin band
The inherited physical-plus contour lemma gives a main NN collar trace D with p steps and displacement(L,L). Set b=(p−2L)/2=W+S, the total west/south step count. Keep EVERY visited-plaquette vertex fixed, including fourth-corner plus vertices outside D.

D cannot have an independent-homology NN cycle: it would intersect the actual essential disagreement wall/negative collar. Its lifts therefore form ordered disjoint NN diagonal separators. All outside-D visited pins lie in the essential LEFT8 side of their own lift, by the local adaptive plaquette rule. Their8-connected band is locally attached to that lift. A unit axis/diagonal attachment cannot cross another NN separator in its interior; its endpoints are disjoint from that separator. Thus each pin band lies in the immediately adjacent left strip. In the chosen RIGHT growth strip of D0, only the band of D1=D0+(L,0) occurs. Every such pin is within L-infinity1 of D1. See SINGLE_PIN_BAND.md.

Initial bounded complement pockets have no such essential pin band. KEEP their actual bits unchanged. They lie inside the NW/SE envelope of D, because a ray from any pocket vertex towards NW or SE must meet its enclosing D boundary. They have no NN edge to the processed essential component, so their weights later cancel exactly. They are not filled in an initial native stage.

## 2. Pinned closure forces majority
In the growth strip freeze the unavailable pin band and the initial pockets. Any stable unfilled vertex outside their NW/SE envelope has a pin-free NW or SE quadrant. The intersection of that quadrant with the strip is finite: transverse u=y−x is bounded between the essential plus lifts. At its extreme u vertex, north/west or south/east are outside the unfilled set. Both are physical plus neighbors, contradicting stability. Hence every unfilled vertex is in the pin envelope.

The exact lattice envelope lemma is proved independently in north_compute_20261113/ising_shadow_envelope/RESULT.md. For the NN trace, at most W column-cut residues have a backward crossing. A good cut has vertical envelope gap<=S, a bad cut gap<=L+S; the integrated gap is therefore<=Lb. Lattice indexing and ALL pin offsets give the conservative bound

 number of unfilled physical sites <=Lb+6L <=Lb+8L.

Initial frozen pockets do not enlarge the same projected envelope: adding points already in a monotone envelope leaves its extremal functions unchanged. Copies of this envelope project to the SAME torus set; do not add their areas. Since b<L/4, L>32 gives Lb+8L<n/2. Therefore pinned two-neighbor closure reaches original majority. Actual extra source plus spins only help, and the native path stops at its FIRST original B.

## 3. Deterministic connected-minus order
Choose all tie breaks from gamma/pins only. Work in the essential right complement. If an eligible gate would detach a finite minus pocket, fill that pocket BEFORE the gate, retaining the gate until last. The diagonal finite-pocket lemma uses u=x−y: all periodic copies of a gate have equal u; an extremal pocket site away from that value has two outward plus neighbors. If chosen site is an articulation, recurse into a strictly smaller pocket. This finds an eligible non-articulation removal and eventually clears the pocket without disconnecting the retained essential minus component.

Two essential minus components cannot be detached in this way. The reference perimeter is initially at most2p<5L and never increases. With the retained diagonal gamma, two distinct essential minus components would require at least four parallel diagonal essential walls, each of physical length at least2L, hence total perimeter at least8L, a contradiction. The fixed essential pin band is never deleted and remains in one component. Thus every other detached component is bounded and pin-free. This is NN-plus/8-minus contour separation, not same-connectivity planar separation.

Consequently the connected order reaches the same pinned closure: it never stops while an eligible gate exists, and every intermediate addition is legal. Initial bounded pockets stay frozen. All operations are physical single-site plus births with at least two physical plus neighbors.

## 4. Original-source partition interface
For each gamma the reference order is geometry-only. Actual thermal plus bits cause skips; stop at first B. All visited plaquette bits remain unchanged, so gamma is an actual visible wall at every used edge. The pointwise number of possible essential wall labels is at most2n/L=2L, without summing abstract contour words.

Frozen initial pockets are separated from F by D, so they can be filled plus in BOTH sides of the auxiliary ratio without changing that ratio. Fourth-corner plus pins near the periodic boundary may be adjacent to F: those are instead changed to minus by ferromagnetic boundary monotonicity, which increases w(x_F,b)/w(plus_F,b). This is an upper bound, NOT an exact cancellation. Freeze gamma's local auxiliary triangulation so its retained triangle trace persists after the fourth-bit change.

After these comparisons, plus pins are NN-connected essential and remaining minus pins are8-connected essential. At every prefix, replaying its two-neighbor additions from ANY compatible assignment cannot increase physical perimeter. Thus the all-plus-processed reference is a pinned perimeter minimizer (gap0). Its initial perimeter after filled-pocket cancellation is at most2p and never increases. Removing fixed gamma of length p leaves moving reference length m<=p.

Quantum's connected-pin loop-erasure/diagonal-NB partition can therefore use M>=max(2L,m) for one other essential wall; three-or-more other essential walls are paid separately. Original w,g,v,A,kappa and C_kappa are unchanged. No Gibbs entrance law, surrogate clock, or altered target is introduced.

## Independent checks and limitations
Compute independently formalized the envelope calculation and frozen-pocket containment. Radical independently checked pin padding and the local attachment/single-band separation. Quantum independently identified and repaired the transient-pocket-pin and fourth-plus-boundary issues. Finite pinned-closure tests are diagnostics, not the basis of the proof. Final quantitative promotion requires the independent conditional-partition receipt.

This construction does not cover no-essential-wall configurations. Lengths>=2.5L require another argument, but for the exactly-two-diagonal sector the separate total-perimeter tail removes them: either wall>=2.5L forces total>=4.5L.
