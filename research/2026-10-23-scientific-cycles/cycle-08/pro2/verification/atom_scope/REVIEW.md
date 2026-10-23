# Independent challenge of the all-chordless-atom representation theorem

Reviewer: `/root/cycle8_port_lemma`, 22 October 2026. Requested bounded
obligation: challenge the structural theorem in
research/structural_scope/ALL_CHORDLESS_ATOMS.md. The precise read source is
pinned in REVIEWED_SOURCE.json. This is a new coverage obligation, not a
repeat of the earlier exact star-interface gates.

## Verdict

**The all-size structural argument is valid under its stated hypotheses.**
No graph-theoretic counterexample or missing boundary dependency was found.
The conclusion established here is exact membership in the loaded S/P/U
expression language, with the original edges and the actual degree-four
budget. The star-four theorem for that language remains a separate input;
this review does not re-audit its finite family closure. Likewise it does
not verify the native normalizer implementation, which the principal owner
is constructing separately.

The hypotheses are essential: finite simple two-connected G, treewidth at
most two, maximum degree at most four, and every cycle chordless. C3 must
be handled separately. No result for all partial two-trees, independently
glued blocks, or arbitrary-real four-column recovery is inferred.

## 1. Protected-edge degree-two elimination

Fix an actual edge uv. The key claim is that every current two-connected
width-two graph H with at least three vertices has a degree-two vertex
outside {u,v}. Here is a direct proof check.

Root a width-two decomposition at a bag containing uv. Remove adjacent
bag containment by contraction, preserving a root containing uv. For a
nonroot leaf bag B with neighbor B', noncontainment gives w in B minus B'.
Running intersection implies w appears in no other bag; otherwise its
occurrence path would pass through B'. Therefore every neighbor of w lies
in B, giving degree at most two. Neither u nor v can be w because each
occurs in the root bag. Two-connectivity gives degree at least two. If
only one bag remains, H has at most three vertices; the stated case is
exactly three, and its vertex outside the protected edge has degree two.
This covers the small case as well as arbitrarily large decompositions.

Suppression of such w, with neighbors a,b, preserves simplicity by inserting
ab only when absent. It is a minor operation: contract aw, then simplify a
possible parallel ab pair. Width at most two is preserved. The bag proof
in the source is sufficient and does not require an unproved equivalence
with another definition of series-parallel graphs.

If the reduced graph has at least three vertices, it remains two-connected.
For z distinct from a,b, suppressing the still-degree-two w in the connected
H-z preserves connectivity. For z=a or b, w was a leaf in the connected
H-z; removing that leaf preserves connectivity of the remaining vertices.
The removed vertex w is not a candidate deletion vertex in the new graph.
Thus no cut vertex is introduced. The protected endpoints are never
suppressed, so their actual protected edge persists until the two-vertex
base case. Reduced graphs need not remain chordless; importantly, the
source never assumes that they do.

## 2. Edge labels and disjointness

The reduction's label invariant is strong enough for actual TTSP composition.
Each current simple edge ab has a network on a,b. Its interior consists of
vertices already suppressed from the current graph. Interiors belonging to
distinct edge labels are disjoint. The union of expanded labels is precisely
the original edge set, and labels meet only at their current edge endpoints.

Suppressing w concatenates labels aw and wb, introducing w as an interior
vertex of the new network. If an ab label already exists, putting it in
parallel with that path preserves disjoint interiors. The new parallel join
does not create duplicate original edges: its two branches consist of
disjoint old edge labels. This proves the invariant inductively and yields
an ordinary TTSP expression for the exact original graph when only u,v
remain.

Because u and v are protected, the distinguished original edge uv is never
inside a series concatenation. Its ancestors are exclusively parallel
compositions. Flattening those ancestors exposes the original edge as one
root parallel branch. This fact is necessary for the rerooting argument;
it is correctly justified by the chosen elimination rule.

The degree cap is retained by suppression in the *simple reduced graph*:
a neighbor loses its edge to w and gains at most one replacement edge.
All expression subgraphs also obey the final graph's degree cap because
they consist of actual subsets of its edges. These are different degree
facts and both are valid.

## 3. Rerooting and nonadjacent terminals

After root parallel flattening, G consists of the direct original uv edge
and one or more other TTSP branches. Simplicity permits only one direct uv
edge. Two other branches would supply two internally disjoint uv paths;
their union is a cycle with uv as a chord. Hence chordlessness leaves
exactly one other branch H. Two-connectivity ensures H is present.

If H has no parallel node after flattening, it is a path. Then G is a
cycle; any cycle of length at least four admits two nonadjacent terminals
whose two arcs both have length at least two. The triangle is the separately
excluded case.

Otherwise choose an internal parallel node N in H. Its complement network
is constructible with the same terminals. The source's orientation is
correct: if a series parent is S(A,N,B), with prefix A and suffix B,
then the complement of N is

    S(reverse(A), complement(parent), reverse(B)).

Empty prefix or suffix is omitted. At a parallel parent, add its sibling
branches to the parent's complement in parallel. Starting from complement(H)
equal to the actual edge uv, induction proves that the complement is
nonempty, has exactly the edges outside the selected module, and meets that
module only at its terminals. All ingredients retain disjoint interiors;
no extra edge, apex, or vertex identification is introduced.

At N, the whole original graph is a parallel union of N's at least two
children and the nonempty complement. It therefore has at least three
nonempty branches between the new terminals x,y. If xy were an actual edge,
it would belong to one branch; paths through two other branches would form
a cycle for which xy is a chord. Simplicity ensures those two other paths
cannot themselves be additional direct xy edges. Thus x,y are nonadjacent.

Every simple x-y path lies in one branch: a simple path cannot switch
branches without revisiting x or passing through its final vertex y before
termination. A path through a different branch is internally disjoint.
Their union is a cycle. Any chord of the first path would be a chord of
that cycle. Therefore *every* simple x-y path in G is induced. This is an
all-path statement, not merely existence of one convenient induced path.
It is exactly the invariant required for normalization below.

## 4. Edge-leaf normalization

In an ordinary TTSP expression, every terminal-to-terminal path of a
submodule extends to a simple terminal-to-terminal path of the whole
network. This follows inductively through series prefix/suffix paths and
by choosing that branch at a parallel ancestor; disjoint interiors prevent
repeated vertices. Consequently the all-path-induced property is inherited
by every submodule.

A parallel node cannot have a direct edge child. Another child provides a
path between the same terminals. Because the expanded graph is simple,
that other path has at least two edges. It extends to a global terminal
path, and the omitted direct edge would be a chord of that path. This
contradicts the invariant. Nor can a nontrivial series network have a
terminal edge: such an edge would bypass its required articulation join
and is not present in a disjoint-child series expression. Thus any
submodule is either one marked edge or a network with nonadjacent terminals.

The binary normalization rules are consequently exhaustive and valid:

    edge + edge       -> a path of length two;
    edge + module     -> one left terminal extension;
    module + edge     -> one right terminal extension;
    module + module   -> ordinary series.

At a parallel node both children are modules, so ordinary parallel applies.
The root cannot be a marked edge because x,y are nonadjacent. This avoids
any implicit use of a forbidden one-edge leaf in the loaded language.

Every intermediate normalized module is an actual edge subgraph of G.
Before a terminal extension, its old port has degree at most three because
one of that vertex's final incident edges has not yet been included. At a
series or parallel identification, the actual child neighbor sets are
disjoint and their degree sum is the degree in the resulting subgraph,
which is at most four. All simplicity and nonadjacency hypotheses of the
loaded coloring interface are therefore retained. There is no reduced-action
oracle or support alteration in this conversion.

## 5. Triangle exception

A two-connected chordless graph containing a triangle must equal that
triangle. If a nonempty component outside a triangle were present, it
would have at least two triangle neighbors, since a unique attachment
vertex would be a cut vertex. Connect two such triangle vertices through
that component. This outside path and the two-edge route through the
third triangle vertex form a cycle whose direct triangle edge is a chord.
Contradiction.

Thus the exception is precisely C3, not a larger unexamined triangle class.
It has no nonadjacent terminals. The direct three-column identity design
and symmetrization handle it under the stated row-energy/noise contract;
padding by a zero fourth column does not change that guarantee.

## 6. Cost and implementation obligations

The O(n+m) graph preparation claim is justified under the degree-four
promise. Suppression never increases simple degrees, so a vertex's degree
can change only a bounded number of times. A degree-two queue excluding
u,v and constant-size adjacency scans therefore incur linear total work.
Each suppression creates only a constant number of expression nodes.
The process never gets stuck on the promised class by Section 1.

Rerooting along one ancestor path uses each off-path subtree once. It must
move/reference those subtrees, not copy their expanded contents at every
ancestor. Orientation can be stored as a flag. Binary normalization makes
one constant-size replacement per expression node. Explicit stacks avoid
an artificial depth-dependent recursion limit. These conditions support
linear expression work and output size; an implementation that repeatedly
copies large prefixes or reverses full child graphs would not inherit that
bound automatically.

A successful degree-two reduction by itself is not claimed to recognize
chordlessness. The theorem assumes that property. A native checker should
validate the produced exact expression, original edge/vertex identity,
actual degree budgets and star coloring; if a non-promised input passes
all of those constructive checks, the checked construction is still usable.
If a promised graph cannot be normalized in the implementation, that is an
implementation defect or missing validation step, not a counterexample to
the proved representation theorem.

The receiving recovery consequence is conditional on the independent
loaded-grammar coloring closure and inherited full-action LS theorem. It
uses all four original actions, arbitrary free diagonal and absolute
Frobenius noise. No graph acquisition, action cost, arithmetic precision,
residual or output cost is removed by this structural lemma.

## 7. Boundaries of the review

No proof flaw was found and no correction to the mathematical statement is
requested. The implementation obligations above are material. In particular,
the exact-child disjointness invariant, protected uv ancestry, all-terminal-
paths-induced property and C3 exclusion must not be dropped in code or in a
shortened statement.

The theorem genuinely broadens the prior supplied grammar's receiving
scope to all two-connected chordless width-two degree-four graphs. It does
not establish a universal construction after arbitrary articulation or
clique-cutset gluing, and it does not settle the full four-versus-five
question with triangles. Historical originality, external acceptance,
application efficiency and physical usefulness are not established by this
internal structural review.
