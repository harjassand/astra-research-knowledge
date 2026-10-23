# Marked-root star hazards and a genuine star-four gluing obstruction

Focused contributor: `/root/cycle8_port_lemma`, Cycle9, 22 October 2026.
The principal owner retains the programme and authors the native operation.
The actual Cycle8 proof/continuation and Cycle9 scope read for this obligation
are pinned in SOURCE_READS.json. No Cycle8 search or certificate suite is rerun.

## 1. Exact one-vertex gluing, with the marked vertex retained

Let two already star-colored simple graphs meet only at an actually specified
root v, with common color 0. Their other vertices and edges are disjoint.
For each side i and color c in {1,2,3}, define its actual root-neighbor count
n_i(c), neighbor support N_i, and far-end flag

    c in F_i iff some neighbor u of v of color c has another neighbor
    of color 0 within that side.

The true degree d_i=sum n_i(c) is retained. The joined graph is star colored
exactly when its degree budget is met and

    N_1 intersect N_2 intersect (F_1 union F_2) is empty.       (1)

Proof: only v gains neighbors. All of its old neighbors retain their
color-labelled adjacency lists. A color on only one side inherits its
already-valid count/flag configuration. A color on both sides creates a
repetition at v and is dangerous exactly when an incident far-end flag is
present. This is the original bad-edge criterion. No remote connectivity
or free recoloring assumption is involved.

The result applies to actual marked vertices, not merely convenient
terminals selected by the Cycle8 atom normalizer. Any relabeling of a child
must be one permutation of its whole coloring, fixing color 0 at the root.
The data at different marked vertices in one atom are correlated and cannot
be selected independently.

## 2. All degree-two root types

Up to permutations of the three colors other than the root, the complete
list of star-valid local count/flag types at degree two is:

| Type | Positive neighbor counts | Flag set | Interpretation |
| --- | --- | --- | --- |
| M | 2 | empty | Both neighbors have the same color |
| D0 | 1,1 | empty | Distinct neighbor colors, neither flagged |
| D1 | 1,1 | One of the two colors | Distinct neighbors, one flagged |
| D2 | 1,1 | Both colors | Distinct neighbors, both flagged |

A repeated neighbor color cannot be flagged in an already star-valid
coloring, so these are exhaustive. After independent whole-child palette
permutations fixing the root, two such degree-two roots can be joined
precisely according to the symmetric table below:

| First / second | M | D0 | D1 | D2 |
| --- | --- | --- | --- | --- |
| M | yes | yes | yes | yes |
| D0 | yes | yes | yes | no |
| D1 | yes | yes | yes | no |
| D2 | yes | no | no | no |

For M, select its sole neighbor color outside the other side's flag set,
which has size at most two. Two D0 sides are safe automatically. For D0/D1,
choose their unique overlap to be the unflagged color of D1. For D1/D1,
make their overlap the color unflagged on both sides, with their flagged
colors distinct. Conversely, two size-two supports in a three-color universe
must intersect. If either side is D2, that intersection is flagged and
violates (1). Thus D2 needs an M partner; this is a necessity, not a choice
of a bad palette.

## 3. Degree-three roots and actual bridge constraints

Degree three has seven local types up to root-fixing palette permutations:

| Positive neighbor counts | Permitted flag patterns up to symmetry |
| --- | --- |
| 3 | empty |
| 2,1 | empty, or only the singleton-count color |
| 1,1,1 | Zero, one, two, or three flagged colors |

Only one additional incident edge fits the degree-four budget. For a bridge
branch attached at v, let its first neighbor u have color c!=0, and let
f indicate whether u has another neighbor of color 0 in that branch. The
exact compatibility condition is

    c outside N, OR [c in N minus F AND f=0].               (2)

Thus a branch with f=0 is permitted exactly when c is outside F; a branch
with f=1 requires c outside N. The remote branch is not entitled to set f=0
without its own realizing coloring. For a new leaf f=0 automatically.

The only degree-three local type which rejects every possible new leaf color
is the rainbow, fully flagged type N=F={1,2,3}. It is a real star-valid
configuration: color both hubs of K2,3 by 0 and its three middle vertices by
1,2,3. Either hub has that type, and adding any leaf at that hub without
recoloring creates a bichromatic four-vertex path. This is a failure of that
rooted coloring, not graph hardness: K2,3 also has other star colorings.

For several bridges at an available degree-two root, counts and flags must
be merged cumulatively. Separate compatibility with the original atom does
not, by itself, check interactions between the branches. In particular,
all chosen branch flags and overlaps enter (1).

## 4. What a one-root guarantee can and cannot buy

A sufficiently strong guarantee would compose: suppose every admitted atom,
when one actual degree-two vertex is marked, has a star-four realization of
type M at that vertex. In a tree of such blocks joined only in degree-two
vertices, take the upward attachment as the marked root of each nonroot
block. Decorated children of type M can be attached one at a time using the
first row of the table. The already colored parent remains star. If its own
marked upward root has type M, its neighbor colors do not change when
children attach at other vertices; star validity forces its repeated-color
flag to remain zero. Thus its M guarantee survives arbitrary depth and
multiple attachment sites. This is a conditional theorem, not an available
hypothesis for all Cycle8 atoms. Bridges and degree-three attachment sites
need the additional actual compatibility in (2).

A weaker guarantee of realizable D0 at each individually marked vertex is
insufficient. The next explicit atom realizes D0 at any one marked degree-two
vertex but cannot realize it at two specified such vertices simultaneously.
This identifies the exact missing joint information rather than treating
one-port feasibility as an independent choice at each attachment.

## 5. K2,4 root theorem

Let B=K2,4, with hubs a,b and middle vertices m1,...,m4. In every star coloring
with at most four colors, a and b have different colors. If they had the
same color, any repeated middle color would form a bichromatic P4; four
middles would therefore need four distinct colors, all different from the
common hub color. Only three colors are available, a contradiction.

With different hub colors, every middle uses one of the remaining two colors.
At a marked middle v, the two neighbor colors are distinct. Both far-end
flags are present exactly when v's color occurs at another middle, because
both hubs have the same set of four middle neighbors. Hence its type is
D0 if its middle color is unique, and D2 otherwise. Types M and D1 are
impossible at a middle in a star-four realization of B.

At most one middle can have a unique color among four vertices using only
two colors. Yet any *one* specified middle can be unique: give it one of
the available colors and all three others the other. Thus every individually
marked middle admits D0, while two simultaneously marked middles cannot
both admit D0. This is an intrinsic joint-root obstruction.

## 6. Sixteen-vertex graph with star chromatic number five

Take a central K2,4 with middle vertices x,y,z,w. Identify x with one middle
of a second K2,4, and y with one middle of a third K2,4. All other vertices
are distinct. The graph has 16 vertices, 24 edges, maximum degree four and
three blocks. Its two cut vertices x,y have degree four.

It is simple, connected, triangle-free and chordless: every cycle lies
inside one K2,4 block, whose cycles are chordless four-cycles. It has treewidth
at most two: a block has bags {a,b,mi}, and those decompositions can be joined
at bags containing the shared middle. Original vertices and edges are not
modified in this assertion.

Assume a star-four coloring of the whole graph. Restricting it to each block
gives the realizations described in Section 5. At each cut vertex, both
incident block roots are of type D0 or D2, never M. The compatibility table
therefore forces D0 on both sides. In particular, the two distinct marked
middles x,y of the central block would both have to be unique among its four
middles. Section 5 proves this impossible. Thus the graph has no star-four
coloring, for any palette choice or relabeling.

Five star colors suffice explicitly: color the two central hubs 0,1, the
hubs in either outer block 2,3, and all middle vertices 4. At a shared middle
its four neighbors have distinct colors; at an unshared middle its two
neighbors have distinct colors. Every hub/middle color-pair component is a
star. Hence the graph's star chromatic number is exactly five.

This closes universal star-four gluing of the completed atoms. It does not
exclude acyclic four-coordinate recovery, unequal/signed coordinate probes,
or arbitrary-real four-column designs. The principal owner's new parity
operation in fact recovers this same graph with four stable coordinate
actions, using bounded larger bichromatic trees.

## 7. Scientific and cost scope

The root-hazard table and the K2,4 obstruction are analytic all-coloring
statements, not conclusions from one failed palette. The independent finite
validator and actual native receiving operation belong to separate owners
within this turn and are not claimed as performed here. Historical priority
is not asserted. These results do not reopen any completed physical or
molecular programme.

No numerical search, old certificate replay or new benchmark was executed
for this contributor obligation. Actual source intake and deductive authoring
were performed; their full inference/review costs are unknown. The separate
PARITY_AND_CUT_REVIEW.md checks the principal owner's positive replacement
and the precise coordinate lower bound.
