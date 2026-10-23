# Independent focused review of the triangle-strip transfer

Reviewer: `cut_balance_challenge`, Cycle5 PRO2. This review was separately
requested after completion of the cut-balance theorem challenge. It concerns
the new strip transfer, not a duplicate review of the completed period-nine
operation or the full four-versus-five research programme.

## Verdict

The all-size argument in PROOF.md is internally correct with its explicit
dependencies on the inherited genuine degree-four 2-tree classification and
period-nine component bound. The operation genuinely removes arbitrary long
maximal triangle strips while preserving the existence of a uniform
bounded-component acyclic four-coloring, at a proved constant-factor loss.
The reduced graph's coloring remains an unsolved input. No theorem for all
real four-column designs, historical priority, or application performance
follows from this transfer.

## Load-bearing points checked

1. **Triangle unions use actual support.** In a triangle-edge-connected union,
   2-degeneracy supplies a degree-two vertex because every vertex belongs to
   a triangle. Its unique triangle can attach to the remaining triangle graph
   only through its opposite edge; all such neighbors are mutually adjacent.
   Removing it leaves an edge-connected union, so induction proves a genuine
   2-tree without a degree-preserving completion assumption. Extra induced
   edges would violate the 2v-3 edge bound. The external-neighborhood clique
   lemma follows by contracting an external connecting path, with a three-
   vertex attachment producing a K4 minor.

2. **Boundary colors are arbitrary.** The six-step state table covers all
   ordered distinct start/end pairs. The prefix/core overlap has exactly two
   vertices, and the suffix appends six vertices, so the total size is n and
   every length-three window remains proper. The existence argument is finite
   and explicit, not a floating solver status.

3. **A global bichromatic barrier is present.** For every color pair there are
   two consecutive core vertices whose colors both lie outside the pair. No
   edge in P_n^2 jumps this gap. Since the core has length at least18, a strict
   interior such gap is available and no component can connect the two end
   pairs. This is the needed reset property; local rank alone would not do it.

4. **The local component bound is uniform.** A component meeting one six-
   vertex buffer meets at most the first/last two core vertices and therefore
   at most two core components of order five. The stated bound16 is safe.
   Proper coloring of the chordal squared path makes all bichromatic
   components acyclic independently of the size estimate.

5. **Simultaneous pieces do not create hidden cycles or merge old components.**
   A fixed-pair strip component meets the reduced graph in either no vertex,
   one port vertex, or the two endpoints of a retained edge. Its intersection
   is connected. Strip interiors are mutually disjoint by degree saturation.
   Hence adding the strip trees one at a time preserves acyclicity and does
   not merge different reduced bichromatic components. Distinct maximal
   triangle components use disjoint incident edges; at most two can contain
   any vertex of a degree-four graph. Thus the advertised65K bound is safe
   (the same counting already permits33K, which is not needed).

6. **Recovery uses the full original action block.** The result extends a
   coloring, then constructs the global incidence decoder on the original
   support. It does not incorrectly treat original port action entries as
   reduced-graph observations with absent strip contributions.

## Independent finite certificate check

A separate checker at
`../cut_balance_review/check_strip_transition_certificate.py` imports no
producer code. It read the saved144 transition witnesses and checked exact
coverage, length, endpoint states and all proper triples. It also checked the
new strict-interior two-absent-vertex gap obligation for all six color pairs.
The canonical transition data have SHA256

    601806411804e8c5645f07055a9b6f435b65f1b3fc27cc04d4527e9fdce743b2

The first and only run passed. Recorded body wall0.0011410200022510253s,
CPU0.001139071000000002s, peak process RSS9,961,472 bytes. This is a finite
check of a load-bearing transition certificate; the all-size proof above
supplies the generalization. No old scientific fixture or producer mixed-
fixture experiment was replayed.

## Implementation and cost review

An early source read encountered the proof file before its creation; that
failed read did not supply evidence. The final proof and source were then
read. An early union/find traversal and repeated full-edge scan would not
justify an unqualified linear implementation bound. The final code uses
triangle-incidence stack traversal and per-component adjacency scans instead.
At degree four each triangle-edge incidence has bounded multiplicity, so the
claimed O(n+m) preparation/extension work is justified in the stated unit-cost
indexing model. The three producer authoring runs are preserved in
COSTS_AND_SCOPE.md. This review made no extra producer run.

Source reading, proof reasoning, messages, code authoring and service/inference
resources are additional and unmetered. The measured certificate check is not
the cost of mathematical discovery or a matched application benchmark.
