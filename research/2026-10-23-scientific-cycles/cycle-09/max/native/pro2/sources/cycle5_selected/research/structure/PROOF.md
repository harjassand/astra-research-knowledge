# Removing arbitrarily long triangle strips from the four-color problem

Contributor: `/root/bounded_component_structure`, Cycle5, 22 October 2026
Australia/Brisbane. This is a bounded structural contribution, not a solution
of the full four-versus-five stable-recovery question.

## 1. Precise statement

Let G be a finite simple graph with treewidth at most two and maximum degree
at most four. A **triangle component** is the union of a maximal set of
triangles connected by steps sharing an edge. Isolated edges are not triangle
components. The following statements hold.

1. Every triangle component is a genuine 2-tree. Every connected component of
   the vertices outside such a component has its neighborhood in the component
   contained in a clique of size at most two.
2. By the inherited degree-four 2-tree classification, every triangle component
   is a squared path, the five-vertex three-page book, or the six-vertex
   three-sun. Consequently a triangle component with at least 30 vertices is
   a squared path C=P_n^2. Its only possible external ports are vertices
   0,1,n-2,n-1 in a square-path order, and no connected outside component meets
   both remote end pairs.
3. For every n>=30, and any prescribed ordered distinct colors in {0,1,2,3}
   at each end pair, P_n^2 has a constructive proper acyclic four-coloring
   extending those colors. Every bichromatic component has at most 16 vertices,
   and no such component meets both end pairs.
4. Form G' by deleting vertices 2,...,n-3 in every triangle component of order
   at least 30, keeping each of its two end edges. G' is again in the same
   support class and all its triangle components have order at most 29.
   Any acyclic four-coloring of G' with bichromatic component sizes at most K
   extends to G with sizes at most 65K. The construction takes O(n+m) work
   once such a coloring of G' is supplied.

Thus the *existence* of a uniform bounded-component acyclic four-coloring for
the whole degree-four partial-two-tree class is equivalent to its existence
for the subclass with bounded triangle components (order at most 29 suffices).
One direction is restriction to the subclass. The other is statement4.
The reduced graph still has arbitrary square/long-cycle separator structure;
this result does not assert that its required coloring is known.

## 2. Triangle components and their external attachments

A graph of treewidth at most two is 2-degenerate and has at most 2v-3 edges
when it has v>=2 vertices. These elementary facts also follow from a width-two
elimination order, or from containment in a 2-tree. Such graphs are closed
under vertex/edge deletion and edge contraction.

Let C be a connected-by-edges union of triangles, considered only with those
triangle edges. If it consists of one triangle, it is a 2-tree. Otherwise
2-degeneracy supplies a vertex v of degree at most two in C. Every vertex of
C belongs to a triangle, so deg_C(v)=2. Let its neighbors be a,b. Its unique
triangle is vab, and ab is an edge of C. No other triangle can share va or vb,
because that would give v a third neighbor. Therefore all neighbors of the
triangle vab in the triangle-intersection graph share ab. If there is more
than one such neighbor, those neighbors are mutually adjacent. Removing vab
and v leaves a nonempty edge-connected union of triangles. By induction the
remaining graph is a 2-tree, and restoring v on edge ab is an allowed 2-tree
addition. This proves the claim without any degree-preserving completion of G.

The component C has exactly 2|C|-3 edges. It is induced on its vertex set:
an extra edge between two of its vertices would violate the stated edge bound.
Let U be a connected component of G-V(C). If two neighbors a,b of U in C
were nonadjacent in C, a path from a through U to b has all internal vertices
outside C. Deleting other external vertices and contracting this path yields
the graph C+ab as a minor, with 2|C|-2 edges on |C| vertices, a contradiction.
Thus N(U)∩V(C) is a clique. It has size at most three; if it had three,
contracting U to one vertex together with their triangle would give K4 as a
minor, again a contradiction. The attachment clique has size at most two.

For a *maximal* triangle component, no external vertex is adjacent to both
ends of an internal edge: that vertex would complete another triangle sharing
the edge and would belong to C. A two-port external attachment consequently
begins a cycle of length at least four, not a new triangle.

The classification used in statement2 is preserved source capital, explicitly
proved in the original Cycle4 archive at
`research/degree4_structure/PROOF.md`, Section6. We do not count a replay of
that classification as a new result. In a squared path of order at least six,
vertices2,...,n-3 have internal degree four; the four port vertices have
internal degrees2,3,3,2. The total external degree budget is therefore six.
Saturation excludes external edges at any internal vertex. The two remote
end pairs have no edges between them. The clique-neighborhood statement shows
that a single connected outside component cannot meet both pairs.

## 3. Six-step control of the end colors

A proper coloring of P_n^2 is exactly a color word in which every consecutive
triple has three distinct colors. Let its transition state be the last ordered
pair (a,b), a≠b. There are 12 states. A step appends c∉{a,b}, taking (a,b)
to (b,c).

After **exactly six steps**, every state reaches every state. This is a small
finite assertion with a complete constructive certificate: `RESULT.json`
stores all144 start/end pairs and their six appended colors. The code generates
the table by six breadth expansions; it checks every transition and all144
end states using integer comparisons. Equivalently, color permutation reduces
the assertion to the following12 words from start(0,1), computed by the same
table. The full144 certificate avoids relying on an unspecified symmetry choice.

| End state | Six appended colors from start(0,1) |
|---|---|
| (0,1) | 201201 |
| (0,2) | 302102 |
| (0,3) | 302103 |
| (1,0) | 230210 |
| (1,2) | 320312 |
| (1,3) | 230213 |
| (2,0) | 320120 |
| (2,1) | 321021 |
| (2,3) | 321023 |
| (3,0) | 320130 |
| (3,1) | 321031 |
| (3,2) | 321032 |

For strip order n>=30, define a core of length L=n-12>=18 by repeating the
inherited period-nine word 012031023, starting with(0,1). Given left pair p,
take its six-step transition to(0,1), obtaining an eight-vertex prefix.
Retain only the first six vertices of this prefix and follow them by the
entire length-L core; the omitted last pair agrees with the first core pair.
Finally append the six-step transition from the last core pair to the desired
right pair. The total length is 6+L+6=n. Every interface respects the same
last-two-state transition rule, so all consecutive triples are distinct.
Both prescribed end pairs are realized exactly.

The transition table is used to control boundary conditions only; no floating
solver or empirical all-size extrapolation appears in this construction.

## 4. Bichromatic reset and the uniform local bound

The inherited period-nine lemma proves that every bichromatic component in
its infinite squared-path coloring has at most five vertices. It also gives,
for each color pair, two consecutive positions absent from that pair within
each period window after a suitable cyclic shift. Every core of length at
least18 contains such a two-position gap strictly inside the core for every
pair. Two absent consecutive positions disconnect the bichromatic support:
all graph edges span at most two positions. Thus no bichromatic component
of the completed strip can meet both six-vertex boundary buffers, in
particular it cannot meet both end pairs.

The reset can also be checked directly without a cyclic-window argument:
using zero-based core positions, absent adjacent positions for pairs01,02,03,
12,13,23 are respectively(7,8),(4,5),(1,2),(3,4),(6,7),(9,10).
All lie strictly inside every core of length at least18.

A component entirely within the core has order at most five. A component
meeting the left buffer can meet the core only through its first two vertices.
It therefore intersects at most two of the core's components, each of order
at most five. Adding the six buffer vertices gives the bound6+2*5=16. The
right buffer is identical. This establishes the all-size component bound.

For completeness, the proper coloring is acyclic independently of that bound.
Every induced subgraph of P_n^2 has a vertex of smallest index whose remaining
neighbors are at most the next two positions and hence are mutually adjacent.
This is a perfect elimination order, so P_n^2 is chordal. In a proper coloring,
a bichromatic induced subgraph has no triangles. If it had any cycle, a shortest
one would be a chordless cycle of length at least four, contrary to chordality.

## 5. Simultaneous reduction and global component accounting

Distinct maximal triangle components have no triangle edge in common. Each
one containing a vertex v uses at least two incident edges at v. Hence under
the maximum-degree-four hypothesis a vertex belongs to at most two triangle
components. In particular an internal vertex of a long squared-path component
already uses all four incident edges inside that component and cannot belong
to another. All simultaneous deletions are therefore consistent; every
retained port edge remains present.

Deletion cannot create triangles or join previously distinct triangle
components. Deleting the interiors of all long components removes their
triangles, so every remaining triangle component has order at most29. The
support assumptions survive because G' is an induced subgraph.

Take the supplied proper acyclic four-coloring of G'. Each retained end edge
has distinct endpoint colors. Apply the construction in Section3 separately
to each removed strip. Shared vertices are ports and their colors are held
fixed, so no conflict arises.

Fix a color pair and consider one bichromatic component A in one extended
strip. Its order is at most16. It meets retained vertices at only one end
pair. Its intersection with G' is either empty, a single vertex, or both ends
of a retained edge. In the last case that edge is present both in A and in G',
so this intersection is connected. A is a tree, and attaching a tree to a
forest along a connected subgraph introduces neither a cycle nor a merger of
two previously different components. Repeating this argument for all strips
preserves acyclicity and cannot join different bichromatic components of G'.

Let F be one original bichromatic component of G', with at most K vertices.
Every attached strip component meeting F can be charged to a port incidence
(v,C), with v∈F and C the long triangle component. The safe bound of four
incidences per vertex gives at most4K attached pieces. (The preceding
edge-count argument actually gives at most2K; we do not need that improvement.)
Each piece adds at most16 vertices, so its enlarged component has at most
K+4K*16=65K vertices. Entirely internal components have at most16 vertices,
which is also at most65K for K>=1. This proves statement4.

## 6. Recovery consequence and precise remaining gap

The coordinate theorem in the unchanged Cycle4 source turns a coloring of
G' with uniform K into a four-coordinate operator recovery design on G with
constant at most sqrt(1+3(65K-1)) under the exact total row-energy and absolute
Frobenius-noise contract. This is a deliberately coarse certified bound, not
an optimal condition estimate. The existing incidence decoder and exact
residual accounting apply after the coloring is constructed.
This is a coloring transfer followed by the global decoder for the original
support and its full action block. It does not apply a reduced-graph decoder
to original action cells as though the new strip contributions were absent;
that unsupported blockwise noise-separation premise is not used.

Triangle enumeration and component traversal take O(n+m) work for degree four.
The strip order is recovered from a degree-two endpoint, its degree-three
neighbor, and successive common neighbors; the implementation validates the
entire square-path edge pattern and the absence of external internal edges.
The144 transition table is a fixed finite object. Constructing all extensions
is O(n+m) work and storage. Finding the coloring of G' is an explicit unsolved
input to this theorem and is not charged as free or asserted to be solved.
The implementation checks actual used structural assertions but does not
independently certify treewidth.

No new query lower, arbitrary-real-design obstruction, NIST speed advantage,
molecular reopening, historical priority, or external scientific acceptance
is inferred. The actual advance is a transfer operation that makes arbitrarily
long saturated triangular chains unnecessary in the remaining coordinate
coloring problem. Mixed finite triangle pieces and unbounded square/long-cycle
separator depth are still unresolved.
