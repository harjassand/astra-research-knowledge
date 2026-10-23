# Focused chordless / minimally 2-connected follow-up

## Decision

This bounded primary-source check did **not identify a proved vertex star-four theorem or an admissible counterexample** for all chordless series-parallel graphs of maximum degree at most four. It therefore does not settle the owner's weaker bounded-bichromatic-component acyclic-four question. This is a search result, not a claim that the problem is historically open.

The owner's proposed atom reduction is supported by an explicit published argument. The remaining coloring extension across nonadjacent two-vertex separators is a real obligation; it is not supplied by the structural theorem.

## Exact structural capital

Nicolas Trotignon and Kristina Vušković, *On triangle-free graphs that do not contain a subdivision of the complete graph on four vertices as an induced subgraph*, Sections 4–5:

https://arxiv.org/html/1407.6531v2

The proof of Lemma 5.2, item (8), shows that a series-parallel graph with no clique cutset is chordless: if a cycle has chord ab, the absence of the clique cutset {a,b} supplies a path joining the interiors of its two ab-arcs; together these form a K4 subdivision. The argument itself does not require the surrounding lemma's additional hypotheses.

Theorem 4.2 states that every cycle in a 2-connected chordless graph other than a cycle contains, in cyclic order, degree-two, degree-at-least-three, degree-two, and degree-at-least-three vertices. Its complete induction proof was read. Consequently the vertices of degree at least three induce a forest. Also, a 2-connected chordless graph containing a triangle is that triangle itself. These are structural conclusions, not four-color extension theorems.

Theorem 4.1 gives a proper nonadjacent two-cut unless every edge has a degree-at-most-two endpoint. It does not control bichromatic component size after gluing.

## More refined two-cut theorem; coloring type matters

Manu Basavaraju, Suresh Manjanath Hegde, and Shashanka Kulamarva, *Acyclic Chromatic Index of Chordless Graphs* (2023), Lemma 5:

https://arxiv.org/html/2302.01638v1

For a 2-connected chordless graph that is not 2-sparse, one can choose a proper-two-cut side whose marker-vertex block is 2-sparse, is not K_(2,t) for t≥3, and has a cut vertex of block degree at least three. The other has block degree at least three, or degree two under the stated minimal-side condition. The full Lemma 5 proof was accessed and read, including the removal of redundant common degree-two neighbors and the minimal-side shifts.

This may refine a separator induction. Its coloring theorem is about **edges**: acyclic chromatic index Δ for connected chordless graphs apart from cycles. Pairing edge colors partitions edges into linear forests. That neither assigns four coordinate colors to vertices nor bounds lengths of the resulting paths. No vertex-coloring conclusion was imported. The full edge-coloring proof was not independently checked, since it is not a candidate solution to the owner contract.

## Sparse-density lead does not cover the atom class

The primary arXiv record for Brandt–Ferrara–Kumbhat–Loeb–Stolee–Yancey, *I,F-partitions of Sparse Graphs*, reports a partition into a distance-two-independent set and an induced forest for maximum average degree strictly below 5/2:

https://arxiv.org/abs/1510.03381

This would give star four by the already-established forest-depth construction. Only the primary abstract was accessible in this follow-up; the attempted HTML full text failed. No full-proof verification or new theorem adoption is claimed here.

More importantly, the density premise does not follow from chordless + series-parallel + Δ≤4. The graph K_(2,4) satisfies those conditions and has average degree 8/3. Every cycle uses both vertices on its two-vertex side and exactly two vertices on its other side, hence has length four and no chord. It is series-parallel, with maximum degree four. Thus a density-only invocation at 5/2 (or the older 26/11 threshold) cannot cover even this atom. This is an obstruction to that invocation, not to its I,F-partition or star-four coloring: K_(2,4) is star-three-colorable by giving its two-vertex side distinct colors and its other side one third color.

## Narrow implications for continuation

1. The clique-cutset reduction may safely isolate edges/triangles and 2-connected triangle-free chordless atoms, once the owner supplies the exact decomposition and interface rules.
2. The high-degree induced forest is usable. Suppressing degree-two paths can nonetheless create cycles and parallel edges in the branch graph. A forest proof on the induced high-degree vertices alone cannot ignore those replacement paths.
3. A star-four theorem on these atoms would suffice under Δ≤4 (bichromatic stars then have at most five vertices). It would still require bounded interface propagation when atoms are joined.
4. No lower bound against all admitted four-colorings, and no arbitrary-real four-query lower bound, emerged here. The previously supplied P7-square star-five obstruction has chords and is not a chordless-atom counterexample. Likewise the earlier outerplanar bipartite star-five example has maximum degree five and does not settle this contract.

## Retrieval record and limits

The follow-up made six web calls: thirteen search query entries, two find entries, and six open entries. Source refs for receiving lookup: `turn184view1` (the structural proof), `turn187view0` (complete refined-cut lemma), `turn186academia29` (I,F abstract), `turn187view1` (failed HTML request). Search noise from historical circular “star coloring,” edge coloring, chordal rather than chordless graphs, and unrelated induced-P4 classes was excluded.

Measured awaited web-call time: **23.537 seconds**. Authoring and mathematical assessment time were not separately metered; total discovery cost is unknown. No numerical experiment, old fixture replay, package install, external write, or paid resource was used. Detailed calls are in `CHORDLESS_CALLS.json`.
