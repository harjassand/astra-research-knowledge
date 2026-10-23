# Cycle5 focused literature and applicability note

PRO 2 contributor `/root/bounded_component_literature`, 22 October 2026
Australia/Brisbane. This is a bounded primary-source investigation, not a
second construction programme. No historical originality or literature-wide
open-problem claim is made.

## Finding

No inspected theorem establishes a uniformly bounded-component acyclic
four-coloring for every graph of treewidth at most two and maximum degree four.
The closer triangle-free question also remains unsettled by this search.
The search did identify established subdivision comparators and a useful
structural reduction for triangle-free atoms. It also rejects a natural
maximal-packing shortcut by a direct counterexample.

## 1. Matched terminology does not supply a matched four-color bound

Aravind and Subramanian, *Bounds on vertex colorings with restrictions on the
union of color classes*, author manuscript, March 25, 2010:
https://people.iith.ac.in/aravind/Files/jgt-gvc.pdf

Definition 1.2 calls a proper coloring a `(j,k)`-coloring when every component
induced by any j color classes has at most k vertices. Theorem 1.3 gives
`C(j,k) Delta^(k/(k+1-j))` colors for general bounded-degree graphs. Section 5
allows simultaneous forbidden-subgraph conditions. These general constants
do not yield four colors here. The target is precisely a four-color
`(2,K)`-coloring that is additionally acyclic.

The relevant older linear-coloring result remains the one in the inherited
Cycle4 note: outerplanar Delta<=4 graphs have four linear colors. A linear
coloring permits arbitrarily long bichromatic paths; outerplanarity is also
strictly narrower than partial-two-tree support. No uniform-length consequence
was established by this contributor.

## 2. Long-bichromatic-path literature

Hou and Wu, *Acyclic coloring of graphs without bichromatic long path*,
Frontiers of Mathematics in China 10 (2015), 1343–1354:
https://doi.org/10.1007/s11464-015-0497-4

The publisher's displayed abstract states that for fixed k>=5 and C4-free G,
there is an acyclic coloring with O(Delta^((k-1)/(k-2))) colors avoiding a
bichromatic k-vertex path. The actual proof was behind subscription access.
It was not purchased or treated as read. This is relevant terminology and a
general comparison, but neither four colors nor the required C4 allowance is
supplied by the inspected statement.

Hou and Zhu, *Coloring Graphs Without Bichromatic Cycles or Paths*, Bulletin
of the Malaysian Mathematical Sciences Society 44 (2021), 1905–1917:
https://doi.org/10.1007/s40840-020-01040-4

The displayed publisher statement gives an explicit P_k-avoiding color bound
`(1+ceil(k/2)^(1/(k-3))) Delta^((k-1)/(k-2)) + Delta + 1`, and an
O(Delta^(4/3)) bound avoiding both cycles and bichromatic P5. The first bound
already exceeds four at Delta=4; the second is not a four-color statement.
The full proof was not available in the inspected publisher access.

Kirtisoglu and Ozkahya, *Coloring of Graphs Avoiding Bicolored Paths*,
arXiv:2012.04560v2 (November 2023), later Graphs and Combinatorics 40 (2024):
https://arxiv.org/pdf/2012.04560

The full primary PDF was read for its definitions, general bound and relevant
grid statements. The bound is `ceil(6 sqrt(10) Delta^((k-1)/(k-2)))`, not a
matched four-color theorem. Its grid results do not cover all partial2trees.

Keskinkilic and Ozkahya, *Coloring Grids Avoiding Bicolored Paths*,
arXiv:2312.12919v7, DMTCS 28:3 (August 2026):
https://arxiv.org/html/2312.12919v7

Theorem 1 establishes that for k>=5 and m,n>=k-2, the P_k-chromatic number of
P_m Cartesian-product P_n is four. This theorem does not assert acyclicity,
and large square grids are outside treewidth two. It cannot replace either
the missing acyclicity condition or the target graph-class argument.

## 3. Triangle-free star-coloring caveat

Ramamurthi and Sanders, *Star Coloring Outerplanar Bipartite Graphs*,
Discussiones Mathematicae Graph Theory 39 (2019), 899–908:
https://www.dmgt.uz.zgora.pl/publish/pdf.php?doi=2109

The publisher's indexed primary text exposes the construction OG_n and
Theorem 4.2, asserting that OG_7^- requires five star colors. Direct retrieval
of the complete PDF repeatedly timed out, so the entire proof was not read.
The graph is a ladder with an extra quadrilateral attached to each rail edge;
the minus version deletes the corner faces. Interior rail vertices still
have two rail neighbors, one rung neighbor, and two added neighbors: degree
five. Therefore this example defeats an unrestricted triangle-free/outerplanar
star-four claim, but it is NOT a counterexample under the owner's Delta<=4
contract. It also does not exclude four colors with larger bounded trees.

No primary counterexample against triangle-free Delta4 partial2tree star-four
coloring was located in the bounded search. This is not a claim that none
exists.

## 4. Established subdivision operations are strong comparators

David R. Wood, *Acyclic, Star and Oriented Colourings of Graph Subdivisions*,
DMTCS 7 (2005), 37–50:
https://dmtcs.episciences.org/articles/344/download

The full primary PDF was inspected, especially Lemma 3 and Section 6.
For exact one-subdivision H' of every edge, Lemma 3 proves
`chi_s(H') <= max(chi(H),3)`: color original vertices properly, then each
division vertex differently from both endpoints. Every four-vertex path
contains a tricolored original-division-original triple. Consequently a
one-subdivision of a partial2tree already admits ordinary THREE-coordinate
star recovery. Lemma 11 gives FOUR star colors when every edge is subdivided
at least twice. Lemma 10 gives three if no replacement path has six vertices.
These are historical constructive results; a new decoder on these unmodified
classes must compare against them, including the star noise constant sqrt2.

Mixed direct edges and short subdivided paths do not satisfy either uniform
subdivision hypothesis automatically. The root's separator problem is still
a distinct obligation.

## 5. Structural input for triangle-free atoms

Nicolas Trotignon and Kristina Vuskovic, *On triangle-free graphs that do not
contain a subdivision of the complete graph on four vertices as an induced
subgraph*, arXiv:1407.6531v2:
https://arxiv.org/html/1407.6531v2

Relevant primary arguments were read in Sections 4–5. A 2-connected
series-parallel graph with no clique cutset is chordless: a cycle chord plus a
connection between its two sides avoiding its endpoints would yield a K4
subdivision. Theorem 4.2 guarantees two degree-two vertices on every cycle of
a chordless 2-connected noncycle. Thus its degree-at-least-three induced core
is a forest. Theorem 4.1 decomposes such graphs into sparse graphs (each edge
has a degree-at-most-two endpoint) or proper nonadjacent two-vertex cutsets.
Lemma 5.2 describes the exceptions to finding a degree-two vertex outside
N[x] union N[y], for adjacent x,y or x=y. The next note derives a quantitative
consequence of that explicit description; it is not a coloring theorem.

See `TRIANGLE_FREE_BOUNDARY.md` for the dependency, all hypotheses and counting
argument. The result is a finite exceptional boundary of at most twelve
vertices under Delta<=4, not an assertion that a coloring extension exists.

## 6. Independent recoloring: precise useful premise and failed shortcut

See `PACKING_COUNTEREXAMPLE.md`. A targeted set independent in G^2 can safely
receive one new color: new-color bichromatic components are stars. But it must
also fragment every old bichromatic tree. Merely choosing a maximal independent
set of G^2 does not ensure that condition, even on a maximum-degree-three tree.
The caterpillar construction in that note is an exact all-size counterexample
to this shortcut, not a lower bound against all recoloring sets or designs.

## 7. Current sparse-matrix implementation literature

Montoison, Dalle and Gebremedhin, *Revisiting sparse matrix coloring and
bicoloring*, arXiv:2505.07308v1:
https://arxiv.org/html/2505.07308v1

The primary table of contents and relevant postprocessing sections were
inspected, not the entire paper. It develops neutral colors, augmented
symmetric reductions of bicoloring, and software decompression. The abstract
and algorithmic scope do not assert the owner's absolute Frobenius-noise to
operator-norm criterion. Neutral rows cannot be imported into the free-diagonal
contract without accounting for their diagonal information. No historical
priority conclusion about the owner's stability theorem is made.

## Source-reference map and scope

Primary tool references available for the parent to open before citing:

- Aravind–Subramanian: turn145view1.
- Hou–Wu and Hou–Zhu publisher statements: turn149view1, turn149view0.
- Kirtisoglu–Ozkahya full PDF: turn149view2.
- Keskinkilic–Ozkahya full primary HTML: turn148view1.
- Ramamurthi–Sanders indexed theorem/construction: turn152search32,
  turn154search46 (complete PDF access failed).
- Wood2005: turn159view0, turn161view1.
- Trotignon–Vuskovic: turn155view2, turn157view0.
- Montoison et al.: turn161view0.

No source search result, abstract, or finite experiment has been promoted to
an all-size four-color theorem. No old operation was replayed.
