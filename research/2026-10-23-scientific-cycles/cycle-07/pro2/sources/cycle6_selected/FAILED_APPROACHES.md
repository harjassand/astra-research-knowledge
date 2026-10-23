# Failures that changed this checkpoint's decision

## 1. A component cap alone does not close reinsertion

The remote degree-two vertex theorem does not reserve slack in the affected
boundary components. The new C_(2K+1) witness is valid for every K>=2: delete
one vertex, color the two K-vertex runs with disjoint alternating pairs, and
reinsert at endpoints colored 0,1. Colors 2 and 3 each grow a saturated run to
K+1. The deleted vertex is remote from a specified middle edge. Recoloring,
another vertex choice, or a stronger invariant remain possible. The cap-only,
no-recolor rule is retired. See research/chordless/PROOF.md.

## 2. Every boundary color assignment is not extendible

K_(2,4) with equal terminal colors needs four distinct colors on its common
neighbors to avoid a bichromatic C4, but only three remain. This is an actual
admitted atom. An acyclic four-color extension invariant must exclude that
boundary state. It is not a graph-hardness lower: distinct terminal colors give
an ordinary star-three coloring.

## 3. Large atoms need not reset all channels

Theta(2,2,2,L), L>=3, with equal terminal colors forces three distinct transmitting
channels. Its size is unbounded. The source's >12-vertex remote-degree-two
corollary does not remove this obstruction. The general construction must track
allowed transmission rather than demand none for every prescribed boundary.

## 4. The direct even-series extension actually diverges

The positive operation deliberately permits odd series only. Extending it to
S2 by using the third color at the junction exchanges the low/high boundary
slots. The exact Q_h family in PROOF.md has mass 2^h and cut Gamma
2^(h-2)-2^(-h). The actual Q8 source and symmetric cut witness are saved in
results/failed_even_series_rotation.json. Its vertices and actions were
materialized; the all-size conclusion is the recurrence proof. The failure is
scoped to this specified coloring rule. It does not prove that Q_h lacks a
better three- or four-query design.

## 5. Stronger-looking literature premises do not fill the gap

The primary P7^2 obstruction already excludes star-four coloring in the full
target class. Bounded-component acyclic four coloring is a weaker and still
relevant target. Bounded tree-partition bags do not provide the required colors
or interface behavior. The stronger tree-bag theorem inspected has a chordality
restriction. A connected-tree plus independent-set partition of a series-parallel
graph can produce a bichromatic C4 under the naive depth-mod-three/fourth-color
combination; a K_(2,3) example is saved in the literature notes.

The new family shares a first gadget with Laakso graphs but has a different
recursion. No embedding theorem or similarly named fractal coloring result is
used as a substitute for checking the actual graph interface.

## 6. Historical failures remain intact

All native Cycle5 failures are included byte-for-byte under sources/cycle5_selected.
In particular, degree-preserving two-tree completion, uncontrolled unequal-gain
coercivity, arbitrary maximal square-independent recoloring, local rank and local
stable-piece gluing do not prove the full stability target. No completed strip
constant was tuned. The inherited 99-vertex full-action operation retains its
stronger squared constant 20. Closed application campaigns stay closed.

## Authoring and execution status

The root producer's first fixed execution passed. The bounded contributor's
first recorded exact executions and the first independent reset diagnostic
passed. One attempted documentation patch had a context mismatch and made no
file change; the corrected patch succeeded. That is an authoring event, not a
failed numerical experiment. Additional independent receiving verification is
recorded separately, with any repairs and all observed costs retained.
