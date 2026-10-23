# Failures and corrections that affect continuation

## Universal arbitrary marked terminal

False for an actual degree-two mark in K_(2,3). Every nonadjacent second
terminal admits a chorded terminal path. The correct replacement is the
original marked-midpoint path2 context. Actual degree-three marks do qualify
as terminals. See research/marked_structure/PROOF.md and its exact checker.

## Independently realizable rooted profiles compose at all cuts

False. A single K_(2,4) can make any specified middle D0 (no far-repeat flags),
but cannot do so simultaneously at two middles. The 16-vertex three-block
path has no star-four coloring. The 11-vertex two-block compound is star-four
colorable but forces each remaining middle to D2. This retires universal
star-four gluing on the connected chordless class, not arbitrary-real or
stable-coordinate four-action recovery. The positive replacement operates
on the SAME obstruction support.

## Remove the two-block incidence cap from the parity construction

False for this rule. A shared middle joining many children branches inside
one color pair. Central K_(2,3), with r child K_(2,3) blocks at each of two
middles, gives cut balance (r+1)(r+3)/(2r+4), which diverges while the pair
component has diameter four. The proof needs each intermediate arm vertex
to have degree at most two. This is a design failure, not a universal
four-query impossibility on the relaxed graph class.

## Implementation corrections

1. A read-only review found that checking shared-middle membership in lists
   would be quadratic for unbounded k. The implementation now caches sets.
   This changed the justified cost bound; no timing of the erroneous large-k
   path was run. The first archived executable version already contains this
   fix but still had the independent error below.
2. The first new receiver failed with StopIteration because the local parent
   vertex variable p overwrote the common hub-side dimension p in the spider
   checker. Exact failed source and receipt are retained in failed/. The
   corrected name is pv. No first-attempt result was written. That unmetered
   failed body has unknown time/CPU/RSS; the successful 0.016832031-second
   body does not replace it.

## Abandoned diagnostic and alternate construction

The finite contributor planned a small atom-library scan, then canceled it
before execution when the analytical three-K_(2,4) obstruction was found.
No nonexistent computation is charged or claimed.

Root also derived a compatible two-by-two incident-pair assignment for trees
of K_(2,4), balancing the four middles two per color and producing P3/P5
bichromatic components. It was not implemented or used: the depth-parity
spider rule has a simpler proof and extends to arbitrary k and general p.
This was a valid alternative representation sketch, not a falsified theorem
or an independent application result. Its unknown inference cost remains part
of research. The supplied operation and claims use only the documented parity
algorithm, with exact actual source.

## Preserved historical exclusions

No failed predecessor approach is repaired by relabeling it. The Cycle8 H8
closure is accepted and was not rerun; the exact-count closure had already
succeeded before occupancy compression. Current evaluator timing is not
this branch's discovery cost or another science task. Cycle5's stronger
99-vertex squared constant20 stays20. Closed molecular, thermal, TPV,
half-cell, GUIDE, and original NIST comparison records remain unchanged.
