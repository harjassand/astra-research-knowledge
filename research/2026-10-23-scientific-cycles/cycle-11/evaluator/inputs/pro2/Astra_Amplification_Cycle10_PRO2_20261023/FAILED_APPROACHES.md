# Failures, corrections, and the preserved scope

## Local unflagged entry without a depth reset is insufficient

An incoming bichromatic component can be an isolated edge in every child
block and still concatenate through arbitrarily many blocks. A chain of
four-cycles with literal local colors (c,1-c,2,3) has this property. Every
child root has distinct neighbors, no flags, and only one common parent
channel, yet pair 0/1 forms an unbounded path. PROOF.md Section 8 gives
the all-size cut witness. The saved eight-block graph has 25 vertices,
32 edges, cut 4/5 and inverse squared lower bound 20/9, using the full
original actions with norm squared 9/20 and a unit original edge coefficient.

The new compulsory message stops that very channel at the next cut.
The same graph's complete-rule components have order at most three. This
rejects the local-condition-only premise, not other four-color designs or
the graph's recoverability. A small saved bound is not the asymptotic proof.

## A stable coloring of a deleted-hub forest need not transfer

In the alternate theta representation, merely deleting one hub per block,
using ordinary three-level forest colors, and restoring all hubs in color
four is unstable on a chain of theta(2,3,3) blocks. The special-color
component retains a growing balanced cut. For 2s blocks it has 6s vertices
and inverse squared lower bound 3s/2. The actual 12-block witness has
action norm squared 1/9 and unit cut coefficient, hence lower bound 9.
Original support and actions are saved in research/theta_explicit/.

The endpoint color correction fixes this specific transmission mechanism
while preserving short-arm components in the forest colors. No actions
of the deleted forest are substituted for original observations.

## Failed first shape checker, not a failed coloring theorem

The explicit theta contributor's first native check rejected an asymmetric
diameter-three spider after choosing the wrong one of its two graph centers.
The actual valid center was vertex 35 with arms [37,36], [40], [41]. The
correct checker uses the unique vertex of degree at least three when one
exists, otherwise a path midpoint. The exact first checker, diagnostic and
failure receipt are preserved. Its uninstrumented body costs remain unknown.
Successful execution does not replace that unsuccessful attempt's cost.

## Scope and wording correction

Independent review noticed that the phrase 'connected bridgeless graph'
also includes an isolated singleton under standard definitions. The native
block entry point handles nontrivial blocks. Theorem A now explicitly says
'with at least one edge'; the isolated singleton has the trivial one-query
diagonal inverse. This corrects coverage wording, with no change to any
calculation or nontrivial theorem.

Before the first main receiver run, a read-only complexity check replaced a
quadratic metadata degree count by one edge pass. No execution of that
unneeded O(nm) metadata loop is claimed or hidden in the preparation bound.

## Historical exclusions remain in force

Universal star-four gluing is false on the original 16-vertex three-K2,4
graph. The present theorem permits P4/P5 bichromatic components and does
not reverse that obstruction. The Cycle9 coordinate lower remains distinct
from arbitrary-real designs. One root is qualified per atom; independent
simultaneous root assignments are still not granted.

Bridges are not silently treated as degree-two atom incidences. A bridge
may meet an atom at degree three or create more pieces at a cut; the present
proof does not supply that new interface. Nonchordless partial two-trees
remain outside the positive class. More components, larger fixtures or a
precision sweep would not settle these missing hypotheses.

The Cycle5 99-vertex squared constant stays 20. No prior closure, spectral
benchmark, molecular target or retired thermal/TPV/half-cell/GUIDE method
was rerun. Protected scientific ownership remains unchanged.
