# Cycle6 focused primary-literature result

Contributor: `/root/bounded_component_literature`, 22 October 2026.

## Decision

**No inspected theorem supplies four proper acyclic colors with uniformly
bounded bichromatic component size for every partial two-tree of maximum
degree four.** This bounded investigation also found no matching obstruction
to that precise property. It is not a literature-wide open-problem or novelty
claim. The full real-design q4 question remains separate.

The useful changes to the owner's comparison boundary are:

1. A general current tree-partition theorem supplies explicit bounded bags,
   but does not remove the four-color compatibility obligation.
2. A primary 2026 obstruction rules out requiring **star four-coloring** even
   on `P7^2`, inside the degree-four class. Bounded bichromatic trees remain
   the appropriate weaker target.
3. A new structural partition theorem provides an alternative interface on
   2-connected partial two-trees, with a concrete gap before it gives recovery.
4. Girth-at-least-five outerplanar graphs already have an established route
   to star four-coloring. This does not cover squares or all partial two-trees.

## 1. Exact tree-partition result and its color-budget limit

Marc Distel, Neel Kaul, Raj Kaul, David R. Wood,
*Tree-Partitions and Small-Spread Tree-Decompositions* (2026), Theorem 2:

https://arxiv.org/html/2604.05690v1

For integers k,d>=1, a graph of treewidth at most k−1 and maximum degree at
most d has a T-partition with bag size at most k(8d−3), quotient-tree degree
at most 4d−1, and at most ceil(n/(kd)) bags. Here k=3,d=4 gives bag size
**87**, quotient degree **15**, and at most ceil(n/12) bags.

Full proof access: yes. Theorem 2, Lemma 10 and its complete inductive proof
in Section 2 were read. The construction groups components behind bounded
separators; it does not require bipartite bags, proper internal palettes,
or four-color bichromatic interface bounds.

Thus its quantitative partition is available, but a four-color conclusion
requires a new argument using the original graph inside/across its bags.
See `PRODUCT_AND_COMPOSITION_GAPS.md` for an explicit conservative 261-color
consequence and why that is not a four-color solution.

## 2. Stronger tree bags apply to chordal input, not every partial two-tree

Vida Dujmović, Pat Morin, David R. Wood,
*Layout of Graphs with Bounded Tree-Width* (2005), Theorem 6.1:

https://cglab.ca/~morin/publications/gd/treewidth-sicomp.pdf

The theorem gives rooted tree-partition bags inducing connected (k−1)-trees,
parent-side attachment sets that are cliques, and bag size at most
max{1,k(Delta−1)}. Crucially, this paper defines a k-tree by successively
adding a vertex on a clique of **at most** k vertices. These are chordal
graphs of clique number at most k+1, including nonmaximal chordal graphs.
They are not all partial k-trees.

For chordal treewidth-two, degree-four input, the theorem therefore supplies
tree bags of size at most six and parent interfaces of size at most two.
Full relevant proof access: yes; Section 6 and the definition preceding
Lemma 2.1 were read. The proof uses chordality to rule out multiple preceding
bags. Arbitrary missing chords invalidate that step. Completing a general
partial two-tree and retaining the original degree bound is not licensed.
This preserves the owner's earlier failed completion premise.

## 3. An exact obstruction to the stronger star-four goal

Germán Benítez-Bobadilla, Fernando Esteban Contreras-Mendoza,
César Hernández-Cruz, Cláudia Linhares Sales, Ana Trujillo-Negrete,
*Star Coloring on Some Subclasses of Chordal Graphs* (2026):

https://arxiv.org/pdf/2606.25168

Proposition 4.4 and Figure 13 give a seven-vertex star-four obstruction H1.
In its labels, the order `(u1,u7,u2,u6,u3,u5,u4)` identifies H1 with `P7^2`.
Hence its treewidth is two and maximum degree four. The complete short
obstruction proof was read and the source figure visually inspected.
The later Theorem 4.6 characterizes star-four-colorable 2-paths, but its full
extension proof was not re-reviewed here and is not needed for this finding.

This is a historical primary-source obstruction to stars, not to the owner's
bounded-component acyclic four-colorings: those already work on bandwidth-two
supports. It says nothing adverse about the triangle-free subclass. A short
independent verification of the seven-vertex obstruction is recorded in
`PRODUCT_AND_COMPOSITION_GAPS.md`.

## 4. Connected-tree plus independent-set partition: a new interface, with a gap

Stijn Cambie, François Dross, Kolja Knauer, Hoang La, Petru Valicov,
*Partitions of planar (oriented) graphs into a connected acyclic and an
independent set*, EJC 33(1), #P1.27 (2026), Theorem 10:

https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i1p27/pdf/

Every **2-vertex-connected simple series-parallel graph** has a partition
V=A union I with G[A] a connected induced tree and I independent. No maximum
degree assumption is required. Full proof access: yes. Section 4, including
the short nested ear decomposition in Lemma 30 and the complete partition
construction in Lemma 31, was read.

Independence of I is weaker than distance-two independence. The result does
not bound the components of the incidence graph between I and a color class
of A. Giving I a fourth color after an arbitrary depth-mod-three coloring
of A can create a two-color cycle even on K2,3. The exact example is in
`PRODUCT_AND_COMPOSITION_GAPS.md`. This source is potentially useful retained
structure, not a four-query guarantee.

## 5. A matched stronger comparator on a narrower triangle-free subclass

Md. Jawaherul Alam, Stephen G. Kobourov, Sergey Pupyrev, Jackson Toeniskoetter,
*Weak Unit Disk and Interval Representation of Planar Graphs* (2014):

https://arxiv.org/html/1408.6928v1

The proof of Lemma 5 decomposes an outerplanar graph of girth at least five
into an induced forest F and a set I whose distinct vertices have distance
greater than two in the original graph. The source calls this “girth 5”;
its proof uses face lengths at least five. That proof was read in full.

Given this partition, color F by forest depth modulo three and I with color
four. Old-color pairs are star forests. Each old-color vertex has at most
one neighbor in I, so every pair involving color four is also a star forest.
For maximum degree four, every such component has at most five vertices.
This is an established structural comparator plus an immediate coloring
consequence, not a newly optimized implementation or a sharp real-query lower.

The paper's triangle-free outerplanar theorem permitting four-cycles uses
unit-interval coordinates directly. It does not establish the same partition
or our coloring guarantee. General chordless partial two-trees are also not
covered by outerplanarity.

## 6. Leads deliberately not promoted to a four-color theorem

The inherited Aravind–Subramanian `(2,K)` definition and general
bounded-degree color bound remain the closest exact terminology. The source
was not re-read: Cycle5 already recorded its insufficient four-color budget.
Ordinary clustered-coloring results control monochromatic components, not
unions of two color classes. The Haxell–Szabó–Tardos primary manuscript
`https://page.mi.fu-berlin.de/szabo/PDF/bounded.pdf` was inspected only for that
scope; its proof was not reviewed or relied on for a new theorem.

Campbell et al., *Product Structure of Graph Classes with Bounded Treewidth*,
`https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/07/Campbell.pdf`,
is an extended abstract explicitly omitting most proofs. Its discussion
agrees with the tree-partition/strong-product equivalence, but no extra
four-color conclusion was found or adopted from it.

No new theorem for all triangle-free or chordless degree-four partial
two-trees was located within these inspected leads. The settled subdivision,
period-nine and prism sources were not reopened, and no old computation was
replayed.

## Source references for a receiving reader

Parent should open the original page before citing source refs in a final answer.

- 2026 tree-partition theorem/proof: `turn172view0`, `turn173view0`,
  `turn176view1`, `turn176view2`.
- 2005 theorem, proof and k-tree convention: `turn173view1`, `turn174view1`,
  `turn174view3`.
- 2026 P7-squared obstruction: `turn177view0`; source figure `turn177view2`.
- 2026 CAI theorem and complete relevant proof: `turn180view3`, `turn181view2`.
- 2014 girth-five partition proof and girth-four scope: `turn181view0`,
  `turn181view1`, `turn181view3`.

Historical priority beyond these explicit sources, full-literature absence,
and the owner's open full-class question are not resolved by this note.
