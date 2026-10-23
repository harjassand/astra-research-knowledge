# Structural scope of the loaded-port grammar

Contributor: `/root/cycle8_structural_scope`, 22 October 2026.
This is a bounded structural lemma for the owner's Cycle8 construction. It
does not assert a coloring theorem or a graph-recognition algorithm.

## 1. Exact grammar

A network is a finite simple graph with two distinct ordered terminals s,t.
All child occurrences are vertex-disjoint before the declared identifications.
The following productions are admitted, subject to maximum degree at most four.

* A path of edge length at least two, with its endpoints as terminals.
* Series: identify the right terminal of one child with the left terminal of
  the next child. Binary series suffices. The sum of the two identified
  terminal loads must be at most four.
* Ordinary parallel: identify all left terminals and all right terminals of
  two or more children. The respective sums of terminal loads must each be at
  most four. No exterior stubs are inserted by this production.
* Left or right extension: add a fresh terminal joined by one new edge to the
  old terminal on that side. The old terminal's load must be at most three.

Terminals of every generated network are nonadjacent. The supplied expression
and the degree checks are part of the operation's input/preparation cost.
No arbitrary boundary colors or edge values are supplied by this grammar.

## 2. Global structural invariants

**Theorem.** Every generated network is simple, triangle-free, chordless,
two-terminal series-parallel, has maximum degree at most four, and has the
following additional property:

> Every simple path between the two terminals is induced.

Its terminals are distinct and nonadjacent, and every edge lies on some simple
terminal-to-terminal path. These claims hold at arbitrary expression depth.

**Proof.** They hold for a path leaf. For a series join, the joined vertex is
a cut vertex separating the two child interiors. Each simple terminal path
is the concatenation of one terminal path in each child; there are no edges
between child interiors. Thus inducedness is preserved. Every cycle remains
within one child, so chordlessness and triangle-freeness are preserved. Outer
terminals remain distinct and nonadjacent. All edges remain on terminal paths.
The joined vertex alone changes degree, to the sum of its child degrees.

For a parallel join, every simple terminal path lies in one child: switching
children would revisit an endpoint, since the only common vertices are the
two terminals. A cycle either lies wholly in one child, or consists of one
terminal path from each of two distinct children. In the latter case both
paths are induced, their interiors are disjoint, there are no cross-edges,
and there is no edge between the common terminals. Consequently the cycle
has no chord. Its length is at least four. Distinct child edges cannot become
parallel edges: such an edge would have to join the two terminals, which is
excluded. All other simplicity and degree claims follow from disjointness and
the two load sums. Every edge is on a retained terminal path.

A one-sided extension adds a pendant edge. It creates no cycle. Every new
terminal path consists of that edge followed by an old terminal path, and is
induced because the new vertex has no other neighbor. The old terminal's
degree increases by one and no other existing degree changes. The new two
terminals are nonadjacent. These arguments also give a usual two-terminal
series-parallel expression: a one-sided extension is a series join with an
edge. Induction proves all assertions. QED.

This proof must retain the terminal-path invariant. Chordlessness of the
children alone would not justify ordinary parallel closure: a noninduced
terminal path could acquire its missing closing path through another child,
turning its chord into a chord of a cycle.

## 3. Why one-sided extensions matter

If the extension productions are omitted, every edge has an endpoint that was
an internal vertex of a path leaf. That vertex is never identified later and
has degree exactly two in the final graph. In particular, vertices of degree
at least three form an independent set.

There is also a boundary invariant: any degree-one terminal has a degree-two
neighbor. This is true at path leaves, is preserved at series joins because
the two endpoints of each child are nonadjacent, and cannot be newly created
by a nontrivial parallel join.

Therefore the unstubbed grammar by itself does not contain the completed
Cycle7 grammar. A Cycle7 stubbed parallel root has a degree-one terminal whose
neighbor has degree three or four. Treating the unstubbed grammar as a strict
enlargement without adding an operation would be a false scope claim.

With both one-sided extensions present, every Cycle7 expression is translated
without changing its graph. Keep path leaves and series joins. Replace each
Cycle7 P_b node by ordinary parallel on its b children, followed by one left
and one right extension. Each child has terminal load one, so the parallel
core has load b on each side. Here b is two or three, hence each extension is
admitted and produces final load one at its new terminal and degree b+1 at
the old terminal. The exact exterior stubs are retained, not deleted.

Thus the augmented grammar genuinely contains the completed Cycle7 grammar.
Its structural upper scope is still stated by the supplied expression; no
recognition or coverage theorem for all chordless SP atoms is being assumed.

## 4. New unequal-load atoms A_L

Let T_k denote a path of length k. For every L>=2, set

    B = P(T_2,T_2),
    C_L = S(B,T_L),
    A_L = P(T_2,T_2,C_L).

The two terminals of B have load (2,2). The series join forming C_L has
combined degree 2+1=3; its external loads are (2,1). The last parallel join
therefore has total loads (1+1+2, 1+1+1)=(4,3). Every identification meets
the actual degree-four budget. No extension is made at the degree-four port.

Naming the final terminals a,c and the series junction b gives exactly two
internally disjoint length-two paths a-b, two such paths a-c, and one path
of length L from b to c. Thus this is the owner's original excluded family,
not a modified graph or an action oracle for a smaller graph. Its counts are

    n=L+6, m=L+8, deg(a)=4, deg(b)=deg(c)=3,

with every other vertex of degree two. The previous source's direct proof
of two-connectivity and absence of clique cutsets applies unchanged; it is
also repeated below so that the new structural consequence is self-contained.

Deleting an internal path vertex leaves two path remnants attached to their
branch endpoints, while the remaining four paths still connect a,b,c. Deleting
one branch vertex leaves the other two joined by an existing path or paths,
and all remnants of incident paths attach to those surviving branches. Hence
deleting any one vertex leaves a connected graph. The graph is two-connected.

In a triangle-free graph, a clique cutset has size at most two. A one-vertex
cutset is excluded by two-connectivity. If an adjacent pair x,y were a cutset,
each resulting connected component would meet both x and y, again by
two-connectivity. Two components would then supply internally disjoint x-y
paths of length at least two. Their union is a cycle having xy as a chord,
contradicting chordlessness. Therefore A_L has no clique cutset.

It is not a Cycle7 cyclic two-connected core for any choice of exterior
ports. Every such Cycle7 core has an even number of degree-four vertices:
each old P_3 production creates a pair, series joins create only degree-two
vertices, and deleting the two outer leaves of a cyclic two-connected root
leaves its new top join vertices of degree two or three. In contrast A_L has
exactly one degree-four vertex. This is the earlier structural exclusion,
now paired with an exact admitted unequal-load expression.

Consequently the augmented grammar is a strict extension at the level of
represented supports/atoms, not just an alternative coloring of an old graph.
The inclusion alone says nothing about colorability or query hardness. In
particular A_2 already has a star-three coloring, as the predecessor records.

## 5. A real remaining scope limitation

The induced-terminal-path property excludes some chordless triangle-free
degree-three series-parallel supports even before coloring is considered.
Take a four-cycle a-b-c-d-a and add leaves s at a and t at b. The only degree-one
vertices are s,t. Every generated grammar network has all its degree-one
vertices among its two terminals: path interiors have degree two, joining
ports only increases their degrees, and a replaced terminal under extension
becomes degree at least two. Thus any representation of this support must
use s,t as its two terminals. But

    s-a-d-c-b-t

is a simple terminal path with the chord a-b. The support therefore cannot be
represented by the augmented grammar with any choice of its terminals.

This example has a clique cutset and is not an obstruction to coverage of
two-connected atoms. We make no complete-coverage claim in either direction
for chordless two-connected SP atoms. The statement that has been proved is
the exact supplied-expression closure and its strict inclusion of Cycle7.

## 6. Recovery relevance and boundary of this contribution

If the owner constructs a nonempty realizable star-four signature family for
every degree-admitted production of this augmented grammar, this structural
lemma supplies actual simple triangle-free supports and strict new receiving
atoms. The inherited full-action inverse and triangle-free operator bound can
then be applied to those supports. The structural lemma itself neither proves
such a coloring closure nor grants it as an assumption without a checker.

All statements here are elementary proofs relative to the explicitly given
grammar. No historical priority, full-class four-query theorem, graph
recognizer, practical runtime advantage, or molecular/NIST consequence is
asserted.
