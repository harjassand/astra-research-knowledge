# Focused review of the owner's new graph-property assertions

Reviewer: `/root/cycle7_structural_boundary`, Cycle7, 22 October 2026.
Scope: owner `PROOF.md` Section 2 and the structural use of A_L in Section 10.
No coloring-transition, recovery-norm or full-programme review is claimed here.

Reviewed source sections, including their headings and trailing whitespace:

- Section 2: 1,428 UTF-8 bytes, SHA256
  `7f755be4a36f46599df1bde53dbd3cba47c5bde4b11ff6ba11617760788e390f`.
- Section 10: 2,000 UTF-8 bytes, SHA256
  `a65de4c633d381b355486ed9f70f6a7ac6a610612ba637f33ce3b02c8cade59f`.

## Verdict

Both reviewed sections are sound under the stated grammar. No correction is
required. In particular, the added invariant that **every simple path between
the two terminals is induced** is sufficient and is correctly preserved.

## Section 2: induced paths and chordlessness

1. A path leaf has degree-one nonadjacent terminals and the unique terminal
   path is induced. It has no cycle.

2. In a series production, each consecutive identification is an articulation
   between two disjoint sides. A simple outer terminal path must traverse the
   children in order, using a simple terminal path in each. Each such child
   path is induced by induction. There are no cross-edges between children,
   so their concatenation is induced. Any cycle lies entirely in one child.
   Identified terminal leaves have degree two; old internal degrees do not
   change. Allowing either series parity does not affect these arguments.

3. At a parallel production, a simple outer terminal path first uses the new
   stub s-a and ends with z-t. Between a and z it must remain in one child:
   switching children would require a repeated a or z, violating simplicity.
   Its child portion is induced by induction. There are no cross-interior
   edges, no a-z edge, and no additional edges incident to the new leaves.
   Hence the complete terminal path is induced.

4. A cycle crossing child copies in a parallel production visits a and z
   exactly once each and consists of one terminal path in each of two distinct
   children. Both paths are induced; no cross-interior edge or a-z edge exists.
   Thus the cycle has no chord. Its two portions each have at least two edges,
   giving length at least four. Cycles contained in a child remain chordless
   and triangle-free by induction. Child chordlessness alone would not have
   justified this step for arbitrary terminals; the new invariant resolves
   that precise obligation.

5. Simplicity, connectivity, distinct nonadjacent degree-one outer terminals,
   and the maximum-degree-four bound are preserved as stated. The productions
   are explicit ordinary two-terminal series/parallel operations, including
   two series stub edges at a parallel node, and therefore preserve the
   asserted series-parallel/width-two support class.

No hidden assumption of two-connectivity of the full network is introduced:
the exterior terminals remain leaves, and series joins remain articulations.

## Section 10: scope obstruction and ordinary control

The owner correctly uses the paired-degree invariant of the supplied grammar.
The top production of a generated network with a two-connected cyclic core
must be parallel. In a top series production, child terminal distance at
least two ensures surviving vertices on both sides of a join even after
the two outer leaves are deleted, so the articulation persists. The top
parallel core join vertices have degree two or three; all degree-four core
vertices are inherited from children and occur in an even total number.

The A_L construction has exactly one degree-four vertex, independently of L.
Its two-connectivity, chordlessness, triangle-freeness, clique-cutset absence
and explicit width-two decomposition are proved in the native scope note.
Consequently its exclusion holds for every choice of the two exterior-leaf
attachments, with the exact core/grammar contract retained. The owner does
not incorrectly infer coloring or query hardness. A_2's supplied star-three
coloring is a valid ordinary control.

The inclusion formula for Theta(2,2,2,L), L>=4, is also exact: the top path
child has length L-2, and the other child is the P3 construction with its
two stubs. Removing the top exterior leaves produces the stated four-path
theta graph. This does not prescribe colors at its original degree-four
hubs, so the known equal-terminal transmission restriction remains intact.

## Evidence and costs

This is a mathematical source review of newly explicit assertions, with no
new graph experiment, no old replay, and no additional numerical test. Reading,
reasoning and writing costs were not separately timed and remain unknown.
The earlier exact scope-check cost remains in COSTS_AND_RECEIVING.md and is
not charged again as a new calculation. This verdict establishes internal
consistency within its scope, not historical priority or external acceptance.
