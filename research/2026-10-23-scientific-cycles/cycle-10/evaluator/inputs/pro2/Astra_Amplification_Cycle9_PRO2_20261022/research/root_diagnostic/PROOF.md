# A small obstruction to star-four composition at cut vertices

Independent diagnostic contributor: `/root/cycle8_finite_gate`, 22 October
2026. The parent supplied the three-K2,4 candidate and its proposed mechanism.
This note gives a separate argument, complete exact color enumeration, and
original-support checks. It does not claim discovery of the candidate or
historical originality.

## 1. Claim and exact graph

There is a connected simple chordless graph of treewidth at most two and
maximum degree four on **16 vertices and 24 edges** that has no star-four
coloring. Hence the completed star-four theorem for two-connected chordless
atoms cannot extend to all connected chordless graphs under the same degree
cap.

The graph is the union of the following three K2,4 blocks. Within each row
include every edge between its two hubs and four middle vertices, and no
other edge.

| Block | Hubs | Middle vertices |
|---|---|---|
| Central | 0, 1 | 2, 3, 4, 5 |
| Left | 6, 7 | 2, 8, 9, 10 |
| Right | 11, 12 | 3, 13, 14, 15 |

The central block meets the left block only at vertex 2 and the right block
only at vertex 3. The two outer blocks are disjoint. All 16 vertex labels
and 24 original edges are saved in `INPUTS.json`; they are fixed before
any coloring is selected.

A star coloring is proper and has no two-colored simple path on four
distinct vertices. This obstruction concerns four coordinate directions
with a star coloring. It does **not** rule out a four-coordinate coloring
with larger bounded bichromatic trees, other acyclic coordinate designs,
or arbitrary real four-column queries. It is not a lower bound for the full
recovery contract.

## 2. Exact marked-root hazard types

For a root v of a proper star-colored graph write a=c(v), and let N be
the set of neighbor colors. A color b belongs to F when a neighbor u of v
has color b and has another neighbor of color a. The star condition implies
that a neighbor color appearing at least twice cannot belong to F.

A degree-two root has, up to a global permutation of the three colors
other than a, exactly four possible hazard types:

* **A:** both neighbors have the same color, so |N|=1 and F is empty.
* **B0:** the neighbors have distinct colors, with F empty.
* **B1:** the neighbors have distinct colors, with |F|=1.
* **B2:** the neighbors have distinct colors, with F=N.

Suppose two star-colored pieces meet only at such a root and their root
colors agree. The union has degree four there. The new star obstruction is
exactly

\[
N_1\cap N_2\cap(F_1\cup F_2)\ne\varnothing.
\]

Indeed, a common neighbor color occurs at least twice after the merge. A
far-repeat flag on either side then supplies the other half of a
bichromatic length-three path. A color present on only one side retains
its old valid multiplicity/flag relationship. No other vertex acquires a
neighbor at this merge.

At fixed root color, the compatibility table under global relabeling is:

| Left / right | A | B0 | B1 | B2 |
|---|---:|---:|---:|---:|
| A | yes | yes | yes | yes |
| B0 | yes | yes | yes | no |
| B1 | yes | yes | yes | no |
| B2 | yes | no | no | no |

For example, two distinct-neighbor supports are two-element subsets of
three available colors, so they intersect. If one side is B2, every color
in that intersection is flagged on that side. Conversely, two B1 profiles
can put their common color at the unflagged channel and use different
flagged channels. The exact finite support/flag table and witnesses are
also saved in `RESULT.json`.

These are statements about already valid real child colorings. A formal
hazard record alone does not establish its realization in a particular
graph.

## 3. K2,4 has exactly two marked-middle types

Let h1,h2 be the two hubs and let m1,...,m4 be the middle vertices of
K2,4. In a star coloring with at most four colors, the hubs must have
different colors. If both had color a, every middle would use one of the
other three colors. Two middles would share some color b. The four distinct
vertices `mi-h1-mj-h2` would then form a b-a-b-a path, a contradiction.

With the hubs differently colored, every middle uses one of the other
two available colors. At a fixed middle m, the two neighbors are therefore
differently colored. Each hub has another neighbor with color c(m) if and
only if another middle has that color. Thus the root profile at m is

\[
\begin{cases}
\mathrm{B0},&\text{if m is the unique middle of its color},\\
\mathrm{B2},&\text{if its middle color repeats}.
\end{cases}
\]

Types A and B1 are impossible at every middle of every star-four coloring
of K2,4. Both B0 and B2 are realizable at each individually marked middle.
For the central block, examples at middle 2 are respectively

```
hubs 0,1; middles 2,3,3,3
hubs 0,1; middles 2,2,2,2
```

The number of singleton-color middles in one block is at most one: four
middles occupying at most two colors have color-class sizes 4+0, 3+1,
2+2, or their reversals. Only 3+1 has a singleton, and it has exactly one.

This is an elementary all-colorings argument. A separate exhaustive check
of all 4^6=4096 labeled color assignments supplements it: 192 are star
colorings; at a fixed middle, 24 realize B0 and 168 realize B2. It also
checks all four middle vertices in every accepted coloring, including the
at-most-one-singleton statement.

## 4. The three-block contradiction

Assume the fixed 16-vertex graph has a star-four coloring. Its restriction
to any block is a star coloring. At each inter-block cut vertex, the two
restrictions have type B0 or B2 by Section 3. Section 2 rules out a B2
profile on either side of such a merge: each side has two distinct
neighbor colors, and the supports intersect among three available colors.
Therefore each cut vertex must be B0 in each incident block.

In the central block, both vertices 2 and 3 would consequently have to
be singleton-color middles. Section 3 allows at most one. This contradiction
rules out **every** star-four coloring of the actual graph. No fixed
palette or particular construction rule is assumed.

The obstruction can also be read as an exact rooted failure. Two K2,4
blocks joined at one middle admit a star-four coloring; both blocks must
spend their singleton-color middle at that join. Every remaining
degree-two middle of the resulting eleven-vertex graph is therefore
forced to B2 in every star-four coloring. Joining a third K2,4 at any such
root is impossible. The exhaustive enumeration confirms this forced B2
profile at each of the six remaining degree-two middles.

This shows why independently available B0 states at specified roots do
not provide their simultaneous realization: an isolated K2,4 admits B0
at each of its four marked middles separately but can supply it at only
one at a time.

For any tree of K2,4 blocks, where each block edge identifies distinct
middle vertices and no other identifications are made, three or more
blocks contain the same three-block configuration as a subgraph. Hence
none is star-four-colorable. One or two blocks are star-four-colorable,
with explicit witnesses below. This corollary is confined to that
specified block construction; no general five-color optimum is asserted.

## 5. The graph satisfies the promised structural class

Each block is K2,4, hence simple, two-connected and chordless: its simple
cycles have exactly two hubs and two middles and are C4. Blocks meet at
cut vertices in a path, so every simple cycle remains in one block. The
whole graph is chordless and triangle-free, with 18 simple C4 cycles.
The independent checker enumerates all cycles and confirms this count
and the absence of a chord.

Every hub has degree four. Each identified middle has degree four; all
other middles have degree two. The graph is connected and its cut vertices
are exactly 2 and 3.

A width-two tree decomposition has a bag `{h1,h2,m}` for each middle of
each block. Join the four bags of each block into a star, then connect
the two bags that contain each shared middle across its block join. The
result is a tree of 12 bags, each of size three. Every edge is covered,
and the bags containing each vertex form a connected subtree. The exact
bag tree is saved and independently checked in `INPUTS.json`/`RESULT.json`.
It certifies treewidth at most two without relying on a numerical rank
or an unverified graph-class label.

## 6. Complete bounded computation

`check_k24_path.py` constructs the one-, two-, and three-block graphs
before the coloring enumeration. Its DFS uses original-ID vertex order
and first-occurrence canonical color labels. For any coloring with at
most four colors there is a unique global color relabeling into this
form. No vertex permutation, root-type assumption, or hub-color lemma is
used to omit a coloring branch.

A partial branch is rejected only when an already colored edge is
monochromatic or when a fully colored simple P4 is bichromatic. Either
violation persists under every completion. Every complete surviving
assignment is independently tested again. The search has no timeout,
incomplete status, numerical tolerance, or optimization criterion.

| Original graph | n | m | Canonical star-four colorings | Labeled star-four colorings |
|---|---:|---:|---:|---:|
| One K2,4 | 6 | 8 | 8 | 192 |
| Two blocks at one middle | 11 | 16 | 6 | 144 |
| Three-block path | 16 | 24 | 0 | 0 |

The zero count for the third graph follows from a complete search with
142 search nodes and 559 proposed assignments. An example for two blocks,
in the original labels 0,...,10, is

```
[0,1,2,3,3,3,0,1,3,3,3]
```

The saved source has no producer imports and does not invoke any old
closure search or scientific suite. Every actual graph, coloring witness,
profile witness, exact class certificate, count and search statistic is
retained. The independent raw one-block enumeration cross-checks the local
quantifier and the DFS's weighted count by a different enumeration path.

The whole new computation body took 0.016963791999842215 seconds wall and
0.016960407999999996 seconds CPU, with peak RSS 11,665,408 bytes. These are
observed diagnostic costs; proof discovery, reasoning and authoring totals
remain unknown. See `COSTS.md`.

## 7. Decision and remaining recovery question

Universal star-four composition on connected chordless width-two,
degree-four supports is false. A search for an all-nonempty star-four
rooted interface covering that whole class should stop: the stated
target itself contains this fixed obstruction.

The broader stable-recovery question remains open. A useful next
construction must allow larger bounded bichromatic components or a
different real query design, and must pay their actual stability/noise
cost. The existing five-query general control remains relevant. This
negative coloring result neither defeats such a construction nor changes
the completed two-connected atom theorem.

The parent is developing the recovery alternative. This diagnostic does
not duplicate that constructive programme, claim a new receiving action,
or infer practical speedup from the short exhaustive check.
