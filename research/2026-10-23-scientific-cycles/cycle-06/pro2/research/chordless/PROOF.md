# Chordless boundary states: exact transmission, mass, and extension obstructions

Contributor: `/root/bounded_component_structure`, Cycle6, 22 October2026 UTC.
This is a bounded interface contribution. The owner retains the global
four-versus-five stable-recovery programme. The full class is not resolved here.

## 1. Contract and the distinction that matters

The support is a known finite simple graph of treewidth at most two and maximum
degree at most four. The owned recovery problem concerns arbitrary real symmetric
matrices with free diagonal, total probe-row norm at most one, absolute
Frobenius action noise, and operator recovery error. This note studies only
proper coordinate designs arising from acyclic four-colorings.

A graph with a good existential coloring need not permit every prescribed
boundary coloring. Likewise, exact injectivity or finite-state connectivity
does not bound the mass of a bichromatic component after repeated gluing.
The new results identify precise allowed and forbidden terminal states and
give their exact mass update. They do not claim that all actual separator
states in the general graph class can be chosen with bounded mass.

The preserved Cycle5 long-triangle-strip theorem is unchanged and not replayed.
Its endpoint-reset operation is not assumed to apply to nonadjacent separator
vertices in chordless atoms.

## 2. Exact nonadjacent-separator join rule

Let G1,G2 share exactly two vertices u,v, with no edge uv and no other common
vertices or edges. Let their proper acyclic colorings agree on u,v. Their
union is properly colored. For a fixed pair of colors P, retain only vertices
whose colors lie in P; each retained graph Fi is a forest.

**Join theorem.** The union coloring is acyclic if and only if there is no
color pair P for which both F1 and F2 contain a u-v path.

Proof. Any cycle wholly in one side is excluded. A cycle using both sides
must enter and leave through distinct shared vertices, so it contains a u-v
path from each side. Conversely, if both forests contain such a path, their
internals are disjoint and their union is a cycle. This argument is separate
for each pair of colors and proves both directions.

This criterion applies to *nonadjacent* two-vertex separators. It is different
from the adjacent-edge boundary in the received remote-degree-two corollary.
For adjacent boundary vertices a bichromatic boundary edge is already shared;
the intersection and cycle accounting must include that shared edge instead.

### Exact vertex-mass update

For every color pair record the partition induced on the boundary vertices
present in that pair, the size of each corresponding component, and the
largest component that does not meet the boundary. There are only the following
boundary-connectivity types, but the positive integer masses are unbounded.

| Boundary present / connectivity | Parallel-join update |
|---|---|
| No boundary vertex | Closed components remain separate; take the larger closed maximum. |
| Exactly one boundary vertex | Its new mass is m1+m2-1. |
| Both vertices, separate on both sides | New masses are m1,u+m2,u-1 and m1,v+m2,v-1. |
| Connected on one side, separate on the other | New connected mass is m_connected+m_other,u+m_other,v-2. |
| Connected on both sides | Forbidden: a bichromatic cycle. |

The subtracted integers count the shared boundary vertices exactly. Closed
components from either piece stay closed and are not merged by the join.
These formulas follow directly by taking unions of the actual vertex sets.

Consequently these profiles form an **exact invariant through arbitrary depth
of admissible parallel composition**: induction on the composition expression
shows that the propagated partition and masses equal the actual ones. This
does not prove a uniform cap. A bounded-state construction must establish that
its allowed mass inequalities are closed under every required transition, or
must include a verified resetting/recoloring step. Erasing the masses and
retaining only the finite connectivity partition loses precisely that obligation.

`separator_profile.py` implements the profile and join operations, rejecting
the two-connected-states case. It assumes the stated graph overlap and matching
boundary colors; an abstract profile alone does not certify those structural
input assumptions.

## 3. A complete interface theorem for parallel paths

Let Theta(l1,...,lr) be the graph consisting of r internally vertex-disjoint
u-v paths, where2<=r<=4 and every edge-length li>=2. Call a length-two path
**short**, and let s be the number of short paths. The graph has maximum
degree r at its two terminals and degree two elsewhere.

These are actual triangle-free, 2-connected, clique-cutset-free series-parallel
atoms. Every cycle consists of two whole terminal paths and has no chord.
Deleting one vertex leaves the remaining graph connected. Deleting an adjacent
pair also leaves it connected: a deleted pair belongs to one path, whose
remaining pieces attach to one or both terminals, and at least one other
terminal path remains to connect the two sides. There are no triangles, so
there is no larger clique to consider. They have treewidth at most two because
parallel paths are series-parallel networks; alternatively each path can be
introduced as a subdivided parallel edge in a width-two decomposition.

Fix prescribed terminal colors a,b in a palette of four colors.

**Theta interface theorem.**

1. If a!=b, every such network admits a proper acyclic four-color extension
   with no bichromatic u-v path and with component order at most r+1<=5.
2. If a=b, an acyclic four-color extension exists **if and only if s<=3**.
   In any such extension, the s short-path internal vertices have distinct
   colors other than a. Each produces a compulsory transmitting color pair.
   There is an explicit extension with exactly those s transmitting pairs,
   no others, and component order at most2r+1<=9.

The stated caps are uniform in all path lengths. They are conservative and
not asserted to be optimal. This is a theorem for this atom subclass, not for
every chordless atom admitting a proper two-vertex-cutset decomposition.

### Four-color path lemma

For a path of edge-length l>=3, any two prescribed endpoint colors extend
to four colors with every consecutive triple having three distinct colors.
For l=2 the same is possible precisely when the endpoint colors differ.

For l>=3, color from the left, leaving the last two internal positions for
the right endpoint. Greedily choose each earlier color different from the
preceding at most two colors. Choose each of the final two internal colors
different from the preceding at most two colors and the prescribed right
endpoint color. At most three colors are forbidden at each of these steps,
so a fourth is available. This makes all consecutive triples distinct,
including the last triple. For l=3 no earlier internal choices are needed.
For l=2 and distinct endpoints, choose a third color for the internal vertex.

In any coloring satisfying this triple condition, a fixed bichromatic
component within that path contains at most one edge. In particular a whole
path of length at least two cannot transmit between distinct terminal colors,
and a whole path of length at least three cannot transmit between equal ones.

### Proof of the theta theorem

If a!=b, use the path lemma on every path. No whole terminal path is bichromatic.
Every component therefore contains at most one terminal. At that terminal it
contains at most the first vertex of each of its r paths; continuing one more
edge would violate the triple condition. The component is a star of order at
most r+1. Components meeting neither terminal are isolated vertices or edges.
Thus the coloring is in fact a star coloring, and has no transmitted pair.

Suppose a=b. Properness forbids color a on a short-path internal vertex. If
two short paths use the same other color c, their four vertices form a
bichromatic C4. Therefore all s such internal colors must be distinct. Only
three other colors are available, proving the necessity s<=3.

Conversely, when s<=3 assign distinct colors other than a to those s vertices.
Use the path lemma on each longer path. For a color pair {a,c}, a terminal
connection exists exactly when a short internal vertex has color c; there is
at most one such path. No longer path is bichromatic, so no pair has two
terminal paths and no bichromatic cycle occurs. Pairs not containing a have
no terminal connection.

Without a transmitting short path, a boundary component has at most r+1
vertices. With such a path, the component contains its two terminals and
one internal vertex. Each of the other r-1 paths can add at most one adjacent
vertex at each terminal, giving3+2(r-1)=2r+1. Nonboundary components contain
at most an edge. This proves the stated bound and the exact transmission rule.

### Consequential boundary exclusions

For K_(2,4)=Theta(2,2,2,2), equal prescribed terminal colors admit **no** acyclic
four-color extension. No larger permitted component size repairs that state.
Yet distinct terminal colors0,1 and common-neighbor color2 give an ordinary
three-star-coloring. Thus this is an obstruction to an arbitrary-boundary
extension claim, not a graph requiring five coordinate queries existentially.

For Theta(2,2,2,L), L>=3, equal terminal colors force **all three** available
color pairs involving that terminal color to transmit through the three short
branches. This is an unbounded-size family of the same admitted atoms. Hence
even excluding small atoms or using the source's order-greater-than-twelve
remote-degree-two property cannot justify an all-pairs terminal-reset invariant.
The long fourth path can be reset; the three unavoidable channels cannot.

In a nonadjacent-separator join, any neighboring piece paired with these equal
terminal colors must transmit none of these three channels. The profile rule
states exactly why: another transmitted channel creates a bichromatic cycle.

## 4. The stronger existential comparator must be kept separate

The theta family also has a simple **three-color** bounded-component operation
when it may choose terminal colors0,1. Thus the four-color interface theorem
is not a new existential query saving on this subclass.

On a length-two path use0,2,1. On a length-three path use0,2,0,1. For length
l>=4, color positions0,...,l-2 by the periodic word012, then choose position
l-1 different from positionl-2 and the final endpoint color1; append endpoint1.
There are three colors, so such a choice always exists. The length-at-least-four
prefix contains all three colors, so the whole path is not bichromatic.
The two smaller cases are also not bichromatic from terminal to terminal.

Inside the periodic prefix, a bichromatic component has at most one edge.
The two-vertex suffix can add at most two vertices to that component, so any
bichromatic component within a single path has at most four vertices. A whole
theta component contains at most one terminal and can acquire at most three
additional vertices from each incident path. Therefore K<=1+3r<=13 is a valid
uniform bound. It is not optimized. Acyclicity follows because two whole
bichromatic terminal paths would be necessary for a cycle, and there are none.

The executable `free_three_color_theta` supplies this comparator. On the exact
one-subdivision special case the established Wood subdivision operation already
gives three star colors, a stronger noise comparator. The general source is
listed below. Neither this simple comparator nor the boundary theorem claims
historical originality or an optimal query count for theta networks.

Under the retained coordinate criterion, q=4,K<=9 gives the conservative
operator-error constant5; the free q=3,K<=13 comparator also gives constant5.
The shared norm convention is absolute Frobenius action noise with unit
coordinate rows. These equal coarse constants do not establish matched
efficiency because the allowed boundary conditions differ and the bounds are
not optimal.

## 5. A cap alone cannot support the remote-degree-two induction

For every integer K>=2, construct a path on2K vertices. Color its first K
vertices alternately0,2, beginning with0. Color its last K vertices alternately
1,3, ending with1. The two runs use disjoint color pairs. Join them by the
existing middle path edge. This is a proper acyclic four-coloring with maximum
bichromatic component order exactly K: its two runs attain K and the crossing
edge creates only a two-vertex component.

Add a new vertex z adjacent to the two path endpoints, obtaining C_(2K+1).
Its endpoint neighbors have colors0 and1, so z can receive only2 or3. Color2
extends the first alternating component to K+1 vertices; color3 extends the
second to K+1. Either extension is still proper and acyclic, but neither
preserves the saved cap K.

Take the designated boundary edge to be the middle edge between positions
K-1 and K. Vertex z is outside the closed neighborhoods of both its endpoints.
The whole graph is triangle-free, 2-connected, clique-cutset-free, has maximum
degree two, and is series-parallel. For K>=6 it also has more than twelve
vertices. Thus the received remote-degree-two existence statement is fully
compatible with failure of this cap-preserving extension step.

This is an all-K obstruction to the following *stated inductive invariant*:
"Any saved proper acyclic four-coloring with maximum component size K extends
without recoloring when a remote degree-two vertex is reinserted, keeping K."
It does not rule out choosing a different vertex, reserving boundary mass,
recoloring, tracking more state, or an entirely different coloring of the cycle.
It is not a lower bound against all designs of a graph.

## 6. Sources, dependencies and exact remaining gap

The received structural note was read in full:
`cycle5_pro2/research/literature/TRIANGLE_FREE_BOUNDARY.md`.
Its primary dependency, Trotignon and Vuskovic, arXiv:1407.6531v2, Sections4–5,
was opened and inspected directly:
https://arxiv.org/html/1407.6531v2
It supplies the chordless/proper-two-cutset setting and the adjacent-edge
remote-degree-two corollary used as motivation. It does not supply the new
coloring extensions. The elementary theta and cycle proofs above are given
in full and do not depend on numerical enumeration of general atoms.

The established subdivision comparator is David R. Wood, *Acyclic, Star and
Oriented Colourings of Graph Subdivisions*, DMTCS7 (2005),37–50:
https://dmtcs.episciences.org/articles/344/download
The original Cycle5 source preserves its matched one-subdivision comparison;
the new unrestricted-theta three-color construction is proved above directly.

A focused search also located Basavaraju–Hegde–Kulamarva's2023 theorem on
acyclic **edge** coloring of chordless graphs. Its four edge colors are not
four vertex-coordinate directions and do not settle this contract. No such
conversion or unsupported novelty claim is made here.

The precise remaining gap is now explicit: for arbitrary chordless atoms and
their proper nonadjacent separators, choose realizable terminal connectivity
states and bounded boundary masses that remain closed under the necessary
series/parallel/forget transitions. The present profile calculus is exact for
parallel joins but does not prove such a bounded invariant exists. The theta
state obstruction rules out universal arbitrary-boundary resetting, and the
cycle family rules out cap-only reinsertion. Those failed premises must not
be reused in a general proof.
