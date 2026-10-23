# Every two-connected chordless width-two atom admits the loaded grammar

Contributor: `/root/cycle8_structural_scope`, 22 October 2026.
This is a new structural receiving lemma for the owner's already-checked
loaded-port coloring theorem. It is not a theorem about arbitrary graphs with
clique cutsets, and it does not assert historical priority.

## 1. Exact statement

Let G be a finite simple, two-connected graph of treewidth at most two,
maximum degree at most four, and with no chorded cycle. Here two-connected
means at least three vertices and no cut vertex. Treewidth at most two means
there is a tree decomposition whose bags have at most three vertices.

If G is not the triangle C3, there are distinct nonadjacent terminals x,y
for which G has an expression in the loaded grammar of `PROOF.md`: paths of
length at least two, ordinary series and parallel joins, and controlled
one-sided extensions. All intermediate graphs obey the real degree-four
budget, all child interiors are disjoint, and the final graph is exactly G.
The required terminals and expression can be constructed from a supplied
ordinary edge-based TTSP decomposition in linear expression work. A direct
bounded-degree reduction below also constructs such an edge-rooted expression
from the promised graph; it does not require a free graph recognizer.

Thus any uniform star-four/recovery theorem for the complete loaded grammar
applies to every such two-connected chordless atom. C3 is handled separately
by three coordinate queries with the identity design and symmetrization.

The proof has three parts: obtain an ordinary edge-rooted expression, reroot
at an actual nonadjacent parallel split pair, then remove edge leaves without
altering the support.

## 2. Edge-rooted TTSP expression: a self-contained existence proof

Fix any edge uv of G. An ordinary TTSP expression starts from single edges
and uses series and parallel joins with disjoint child interiors. Parallel
intermediate labels may represent several distinct paths, but the expanded
original graph is simple. Reversal of ordered terminals is always allowed.

### 2.1 A degree-two vertex away from the protected edge

Every two-connected graph H of treewidth at most two with at least three
vertices and containing uv has a degree-two vertex w outside {u,v}.

To prove this, root a width-two tree decomposition at a bag containing u,v.
Contract an adjacent pair of bags whenever one is contained in the other;
the surviving bag still covers the removed bag and running intersection is
preserved. Keep a root bag containing u,v. If only one bag remains, H has at
most three vertices, and its third vertex has degree two by two-connectivity.
Otherwise take a leaf bag different from the root. It has a vertex w not in
its neighboring bag. Running intersection implies that w occurs nowhere else,
so all its neighbors lie in that leaf bag and its degree is at most two.
Also w is not u or v, since those occur in the root bag. Two-connectivity
gives minimum degree at least two. Hence its degree is exactly two.

### 2.2 Suppression and expression labels

Suppress such a w with neighbors a,b: remove w and its two incident edges,
and insert ab if it is absent. The resulting simple graph H' is a minor
(contract aw and simplify parallel edges), so its treewidth remains at most
two. For completeness, contraction preserves a width bound by replacing the
two contracted labels with one in every bag; their two occurrence subtrees
meet because a bag contains their edge, so running intersection is retained.

When H' has at least three vertices it remains two-connected. For a vertex
z other than a,b, connectivity of H-z transfers through the suppression.
After deleting a or b, w was a leaf in the connected graph H-a or H-b;
removing that leaf leaves the other vertices connected. Thus no vertex of
H' is a cut vertex. The fixed edge uv is never removed as an edge of the
simple reduction, since w lies outside its endpoints.

Maintain an ordinary TTSP network label on each remaining edge. Initially
each label is that original edge. When w is suppressed, concatenate the
labels on aw and wb in series. If ab already has a label, put the old label
and this new path in parallel; otherwise the concatenation becomes its
label. The label interiors stay disjoint because every suppressed vertex
is removed from the remaining graph exactly once. Induction shows that the
union of the labels is always the unchanged original support.

Continue until only u,v remain. The final edge label is an ordinary TTSP
expression for all of G with terminals u,v. The distinguished original edge
uv has only parallel ancestors in this final label: its endpoints were
protected from suppression. Flattening consecutive parallel nodes therefore
writes the root as parallel(original edge uv, the remaining branches).

This establishes the needed edge-rooted expression without using the external
equivalence between K4-minor-free graphs and treewidth at most two. If one
defines “series-parallel support” as the width-two class, the hypotheses
match directly. If a supplied TTSP expression is used instead, no treewidth
existence lemma is needed.

### 2.3 Preparation cost under the actual degree cap

Suppression never increases a neighbor's degree in the simple reduced graph:
it loses the edge to w and gains at most one edge ab. Thus the degree cap
four is retained. Keep a queue of degree-two vertices other than u,v. Each
suppression inspects at most four neighbors at a,b, so the edge-membership
test and degree updates take bounded work; each vertex enters the queue only
a bounded number of times. The promised class never gets stuck by Section
2.1. There are O(n+m) expression nodes and O(n+m) arithmetic/storage work.

This is a construction on the stated graph class. An arbitrary input can
be rejected if the reduction fails, but that alone is not being asserted to
recognize chordlessness or all support classes. A supplied expression can
instead be validated by expanding its edges and checking the actual support.
Bit costs, actual matrix actions, and downstream decoding are separate.

## 3. Rerooting at a nonadjacent split pair

First consider the edge-rooted expression from Section 2, flattened so that
consecutive series nodes and consecutive parallel nodes are combined.

Since G is simple, there is exactly one direct uv edge branch. There can be
only one other root parallel branch H: if there were two, choose a uv path
in each of them. Their union would be a cycle of length at least four with
the edge uv as a chord. There is at least one other branch because G is
two-connected. Thus G=P(edge uv,H).

If H has no parallel node, it is a single path and G is a cycle. For a cycle
of length at least four, take any two nonadjacent vertices x,y; its two arcs
are paths of length at least two, already giving a loaded-grammar expression.

If G is not a cycle, H has an internal parallel node N with terminals x,y
and at least two nonempty children. Its complement C_N is a nonempty TTSP
network on the same terminals, whose edges are exactly the edges of G not
in N. This follows constructively along the ancestor path, starting with
C_H=edge uv:

* At a series parent with the selected child between prefix A and suffix B,
  the complement of that child is S(reverse(A), C_parent, reverse(B)), with
  empty prefixes/suffixes omitted.
* At a parallel parent, the complement of the selected child is the parallel
  join of C_parent and all other children.

Each formula uses the actual existing vertices and edges. The remaining
children and complement have disjoint interiors. At N the whole graph is

    G=P(children of N, C_N).

There are at least three nonempty x-y branches. Therefore x,y are nonadjacent
in G: if xy were an edge in one branch, paths through two other branches
would form a cycle with xy as a chord. All branches consequently have
terminal distance at least two.

Every simple x-y path in the whole graph lies within one branch, because
the branches meet only at x,y. Choose a path in another branch. Their union
is a cycle. A chord of the first path would be a chord of that cycle, which
is forbidden. Thus **every simple x-y path in G is induced**.

The context formulas create only O(p) nodes from an expression of size p:
each off-path child is used once, and only a bounded number of new nodes is
needed at each ancestor. Terminal reversal is an orientation flag, not a
copy of the expanded subgraph. This is a real rerooting operation, not the
addition of a universal apex or deletion of support edges.

## 4. Normalization into the loaded grammar

Let an ordinary TTSP network have nonadjacent terminals s,t and have every
simple s-t path induced. Reduce its expression by flattening consecutive
series and consecutive parallel nodes. No parallel node has an edge leaf
as a child. Indeed, another child supplies a path between that node's
terminals of length at least two, and that path extends to a simple s-t
path through the outer TTSP expression. The edge child would be a chord of
this extended path, contradicting the assumed terminal-path property.

Every parallel child is therefore a nontrivial series expression. Normalize
recursively. In a series expression, group its edge leaves into consecutive
runs. If all children are edge leaves, the run has length at least two and
becomes one admitted path leaf. Otherwise there is a non-edge child:

* Absorb a leading edge run by successive left extensions of the first
  non-edge child, processing the edges from right to left.
* Concatenate normalized non-edge children by ordinary series joins.
* Absorb each intervening or trailing edge run by successive right
  extensions of the accumulated left network before the next series join.

An edge leaf is never left as an independent module. Every created module
has nonadjacent terminals. No original edge is added, removed, duplicated,
or subdivided: an extension uses exactly its existing edge and endpoint.

All degree checks hold. Each partial module is an actual edge subgraph of
the final G, so an identified or extended vertex has degree no larger than
its final degree. Immediately before extension its degree is at most three,
and at a series/parallel join the sum of actual loads is at most four.
Simplicity and disjoint interiors are inherited from the TTSP expression.

The normalization uses O(p+m) work and output size, where p is the supplied
expression size and m is the expanded edge count. Explicit stacks avoid a
depth-dependent call-stack requirement. This proves exact membership in the
loaded grammar and completes the structural theorem.

For a binary expression, the same normalization can be implemented even more
directly without flattening series nodes. First note that every submodule's
terminal path extends to a global terminal path, so the induced-path property
holds within it too. A nontrivial submodule with an edge between its terminals
would contain a parallel edge child, already excluded. Thus each normalized
child is either one marked edge or an admitted nonadjacent-terminal module.
The four binary series cases are exactly

    edge + edge     -> path of length two,
    edge + module   -> left extension,
    module + edge   -> right extension,
    module + module -> series join.

At every parallel node both children must be modules rather than marked
edges, and ordinary parallel applies. The root is not a marked edge because
its terminals are nonadjacent. These four local rules are a support-preserving
linear-size normalization matching a binary implementation directly.

## 5. The triangle exception and recovery consequence

A two-connected chordless graph containing a triangle is that triangle itself.
Otherwise a connected component outside the triangle has at least two
neighbors on it, because a sole neighbor would be a cut vertex. A path
through that component between two triangle vertices, together with the
two-edge path through the third triangle vertex, forms a cycle whose direct
triangle edge is a chord. This is impossible.

C3 has no nonadjacent terminal pair, so it must not be forced into the loaded
grammar. It has the direct three-coordinate design X=I_3; symmetrization of
Y gives Frobenius and operator error at most ||E||F. Padding with a zero fourth
column also respects the same row-energy budget.

For every other graph in the theorem, an independently proved star-four
coloring closure for the complete loaded grammar now applies to the original
support. Combining that coloring with the received exact full-action LS
inverse gives the owner's stated operator and Frobenius guarantees. The
graph construction is charged O(n+m) work under the bounded-degree promise,
or O(p+n+m) when reading a supplied expression. Four complete original matrix
actions, numerical precision, residual, and output work remain charged.

This moves the structural boundary from a specially supplied recursive family
to **all two-connected chordless width-two degree-four atoms**. It does not
cover arbitrary graphs formed by gluing these atoms at cut vertices or clique
cutsets, triangle-containing nonchordless partial two-trees, or the full
arbitrary-real four-query question. Independently coloring atom interiors
does not prove stable composition at shared vertices.

## 6. Internal status

The argument is self-contained relative to the proved loaded-grammar coloring
theorem and the inherited recovery estimate. The existence/reduction and
rerooting arguments are standard series-parallel mechanisms in substance;
their historical originality is not claimed. The relevant new receiving use
is the removal of the previous grammar-coverage gap, with the exact degree,
noise, support, and action contracts unchanged.
