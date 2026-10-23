# Exact higher-load boundary interface for star coloring

Focused independent obligation, Cycle8 PRO2, 22 October 2026. This lemma is
about exact state composition. It does **not** say that every admissible
uncolored composition has a star-four coloring or a nonempty guaranteed family.
That is a separate constructive obligation owned by the principal investigator.

## 1. Objects and actual boundary data

Fix a finite color set C, with |C|=4 for the current application. A module is a
finite simple graph with two distinct ordered terminals s,t which are
**nonadjacent**. The internal graph and its two terminals are star colored:
the coloring is proper and contains no two-colored path on four distinct
vertices. Terminals may have unequal degrees. In the application every degree
is at most four. Child occurrences used below are disjoint before the declared
identifications; in particular, their interiors are disjoint.

For a terminal v and each color c define

    a_v = color(v),
    n_v(c) = |{u in N(v): color(u)=c}|,
    F_v(c) = 1 iff some u in N(v) of color c has a neighbor w!=v
                         with color(w)=a_v.

The port record is R_v=(a_v,n_v,F_v). The full signature is (R_s,R_t).
The Boolean F_v(c) is an OR over actual incident edges; individual neighbor
identities and the number of flagged incident edges are not required.

Properness implies n_v(a_v)=0. Realizability implies F_v(c)=0 when n_v(c)=0.
Star coloring also implies

    n_v(c)>=2 ==> F_v(c)=0.                         (1)

All these statements concern actual realizable states, not arbitrarily assigned
boundary constraints. No free choice of a_s or a_t is asserted. In particular,
K2,4 still cannot be star-four colored with its two hubs prescribed the same
color. The state retains that infeasibility when complete attainable sets are
used.

## 2. Edge criterion

For an edge uv in a proper coloring, it is the middle edge of a bichromatic
four-vertex path precisely if both

    |{w in N(u): color(w)=color(v)}|>=2,
    |{w in N(v): color(w)=color(u)}|>=2.

Choose a witness neighbor distinct from the other endpoint on each side. The
two selected witnesses are distinct because their required colors differ.
Thus this test is equivalent to the star condition, including in graphs which
contain triangles. Formula (1) is exactly its application to edges incident
to v. Triangle-freeness is not required by the interface lemma.

## 3. The port merge operation

Merge two ports with records R=(a,n,F) and R'=(a',n',F'). Equal colors a=a'
are mandatory. Their neighbor sets remain disjoint under the operations of
Sections 4 and 5. Define

    n''(c)=n(c)+n'(c),
    F''(c)=F(c) OR F'(c).                         (2)

The merge is star-admissible exactly when

    for every c, NOT [n''(c)>=2 AND F''(c)=1].     (3)

In the degree-four application also require sum_c n''(c)<=4. This is an actual
degree budget, not a color count bound. For an arity-b merge use sums and ORs
across all b ports; the same proof applies. Binary processing is sufficient
because a forbidden repetition or degree overflow cannot disappear when more
ports are added.

## 4. Ordinary series composition

Let the two child signatures be (R_s,R_t) and (R_u,R_v). Ordinary series
composition identifies t with u, leaves s and v as the new terminals, and
adds no edge. It is star-admissible exactly when the merge R_t+R_u satisfies
(2)-(3), with matching port colors and the required degree cap. Its signature
is exactly

    (R_s,R_v).                                   (4)

**Proof.** Only the joined vertex gains neighbors. Its neighbor sets from the
two children are disjoint: the original copies are disjoint, and neither
retained terminal is adjacent to the joined terminal in its own child.
Every neighbor of the joined vertex is therefore an internal vertex of one
child. That internal vertex's color-labelled adjacency list is unchanged
except for renaming the joined vertex. Consequently its far-end flag is
unchanged. The edge criterion at every incident edge is precisely (3).
Edges not incident to the joined vertex have unchanged endpoint color lists
and cannot become bad.

The neighbor of a retained outer terminal, of which there may be several, is
not the joined vertex because the child terminals were nonadjacent. Its
color-labelled adjacency list is unchanged. Hence the outer counts and all
outer far-end flags remain exactly those in R_s,R_v. This remains true if an
interior vertex is a common neighbor of the two terminals of one child: the
other terminal is renamed by identification, not deleted or recolored, and
no two neighbors of that interior vertex are identified with one another.
This proves both star-admissibility and (4). QED.

## 5. Ordinary parallel composition

Let two child signatures be (R_s,R_t) and (R_u,R_v). Ordinary parallel
composition identifies s with u and t with v, leaving those two distinct
vertices as the parent terminals. There are no extra stubs. It is
star-admissible exactly when both merges pass (2)-(3), matching both pairs
of colors and paying both degree budgets. Its output signature consists of
the two merged records from (2).

**Proof.** The terminal pairs stay distinct. Because every child has
nonadjacent terminals, there is no direct terminal edge and no edge is
incident to both joined vertices. Every other endpoint of an incident edge
is internal to one child. Different child interiors are disjoint, so the
neighbor sets at each merged terminal are disjoint. For an internal vertex,
its incident endpoints retain their colors and distinctness, even when it
is adjacent to both terminals. Thus its far-end flags relative to either
terminal are unchanged. Both terminal color counts add and their flag
predicates OR as in (2). The edge criterion is exactly (3) at each terminal.
Every other edge retains its endpoint color lists. This proves necessity,
sufficiency and the precise output signature. QED.

## 6. Exactness for attainable state sets

Let S(G) be the set of all signatures from actual star colorings of a module
G. Applying the corresponding merge rule to every compatible pair in S(G1)
x S(G2) produces **exactly** S(G1 S G2) or S(G1 P G2), subject to the graph's
degree cap. One inclusion follows by realizing the selected states in the
disjoint children and gluing. The reverse inclusion follows by restricting
a star coloring of the output graph to each child. Restriction cannot create
a bichromatic P4; the output's local data obey the formulas already proved.

For sufficient guarantee families rather than complete state sets, the
forward inclusion survives, but failure to find a compatible family witness
does not establish graph noncolorability. This distinction must be retained
in any finite synthesis or obstruction claim.

Arbitrary color permutations commute with both transitions. Reversing the
two ordered terminals swaps their records. Thus canonical color-orbit states
and optional reversed modules can be handled without losing realizability,
provided the actual relabeling is restored in a construction.

## 7. Graph contract and limits

Both constructions preserve distinct nonadjacent terminals and simplicity.
Series cannot create an edge between the two retained terminals because
they belong to different disjoint children. Parallel cannot create a direct
terminal edge because neither child has one. No edge becomes a loop and no
parallel edges arise: a duplicated edge between children could only be a
direct terminal edge, which is absent. The degree sums in (2) are exact;
all other vertex degrees are unchanged.

The nonadjacent-port hypothesis is essential to these formulas. A path of
one edge has two degree-one adjacent terminals and both far-end flags zero.
Compose two such paths in series with colors 0,1,0. The resulting two-edge
path is star colored, but each outer port's far-end flag is now one. Formula
(4), if used without the hypothesis, would incorrectly retain zero. Adjacent
ports require extra dependency data and different transition rules.

Disjoint child interiors are also essential. Shared interior vertices could
merge neighbor lists incorrectly, create duplicate edges, or change their
far-end flags. The lemma is not an interface for arbitrary overlapping pieces.

The state does not carry chordlessness, series-parallel recognition or any
original-support isomorphism. Those graph properties must be proved by the
admitted expression grammar, independently of this coloring lemma. Likewise,
the lemma alone supplies neither a nonempty all-depth family nor a recovery
query advantage.

## 8. Finiteness and independent diagnostics

With four colors and terminal degree 1..4, fixing the terminal color leaves
three possible neighbor colors. For each neighbor-color multiplicity, the
number of syntactically valid count/flag records is encoded by

    (1+2z+z^2+z^3+z^4)^3.

The coefficients of z,z^2,z^3,z^4 are respectively 6,15,23,30. Thus there are
at most 74 records for a fixed terminal color, 296 labeled port records, and
87616 labeled two-port signatures before realizability or color symmetry.
This is a finite upper bound, not a practical bound on the number of complete
signature sets or guarantee families needed in a universal theorem.

The independent standard-library diagnostic check_interface.py imports no
producer and directly enumerates actual proper/star graph colorings. Seven
joins, including terminal loads (2,1), (3,2), (3,3), (4,4) and an internal
degree-four series join, passed equality between the directly enumerated
attainable state set and the transition-derived set. It handles shared
terminal neighbors on actual two-edge paths. The largest test is 10 vertices,
12 edges: 35796 labeled proper colorings, 7224 star colorings and 2336 actual
labeled signatures. The complete results and measured body time are in
RESULT.json. These finite diagnostics check the changed implementation;
Sections 2-6 supply the all-size argument.

## 9. Exact one-sided terminal extension

The principal constructor also requests the following operation U_L (and its
symmetric right version). Let a module have nonadjacent terminals s,t and
signature (R_s,R_t). Assume deg(s)<=3. Add one new vertex s' and the sole new
edge s's, use s',t as the new terminals, and prescribe color(s')=A. This is
star-admissible exactly when

    A != a_s  AND  F_s(A)=0.                        (5)

The new left port has color A, exactly one neighbor of color a_s, and its
single possible far-end flag is

    F_(s')(a_s) = [n_s(A)>0].                       (6)

All other new left counts/flags are zero. The right record remains exactly R_t.

**Proof.** Properness of the new edge is A!=a_s. Its new leaf endpoint prevents
that edge from being bad. Only the old terminal s gains a neighbor; its
multiplicity in color A increases by one. An old edge to a neighbor of color
A becomes bad precisely when its far-end repeat flag is one. Such a flagged
edge could not already have multiplicity at least two at s, because the old
coloring was star. Therefore the additional neighbor creates a bad edge iff
F_s(A)=1, proving (5). Other colors and all nonincident edge endpoint lists
are unchanged. The far-end flag at the new leaf asks whether s has an old
neighbor of color A, exactly (6).

A neighbor of t cannot be s because the old terminals were nonadjacent.
Therefore its color-labelled adjacency list is unchanged by adding s's, so
all opposite-port counts and flags remain R_t. An interior vertex adjacent
to both s and t remains harmless: the new edge changes the list of s, not
that interior vertex. The new terminals are nonadjacent, and all degrees
remain at most four because the old s degree was at most three. Simplicity
and distinctness are immediate from freshness of s'. Restricting any output
coloring to the old module proves the reverse direction, so the transition is
exact for complete attainable state sets as in Section 6. QED.

Two one-sided extensions after an ordinary parallel merge recover the original
Cycle7 stubbed parallel operation when the merged terminal degrees are at most
three. The intermediate and final states remain under the nonadjacent-port
contract. This is an actual inclusion of the old grammar in a richer expression
language, not permission to remove stubs from an already supplied graph.
