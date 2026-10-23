# A single-channel reset composes rooted atom guarantees into stable recovery

Pro2, 23 October 2026. This is a new construction relative to the Cycle9
checkpoint. Historical priority and external acceptance are not established.
The proof uses the accepted Cycle8 atom theorem and Cycle9 one-mark lemma,
whose exact original source is preserved. It does not rerun their closure.

## 1. Model and main consequence

The finite simple support graph G is known before choosing a real n-by-q
matrix X. The unknown D is any real symmetric matrix supported on G, with
an arbitrary free diagonal. Every WHOLE row of X has Euclidean norm at most
one. All original actions Y=DX+E are observed. E is arbitrary absolute
Frobenius noise. The required output is exact when E=0 and has a uniform
operator-norm error bound. No reduced graph actions, known matrix entries,
probabilistic noise or free precision are assumed.

**Theorem A.** Every connected bridgeless chordless graph with at least one
edge, treewidth at most two and maximum degree at most four admits an explicitly constructed
four-coordinate design with canonical least-squares inverse satisfying

    ||Dhat-D||op <= ||Dhat-D||F <= sqrt(3+sqrt(5)) ||E||F.

Here chordless means that no cycle has a chord, not that the graph is
chordal. A single triangle is allowed. Graph size, block depth, block size,
number of attachments and branch-path lengths are unrestricted. All original
vertices, edges and action cells are retained. The implementation takes
native n and an original edge list; it does not request a favorable marked
vertex or a supplied block expression.

The isolated single vertex has the trivial one-query diagonal inverse; the
native block entry point promises the nontrivial class in Theorem A.

The sharper structural assertion is that every bichromatic component is a
spider with arms of length at most two. It may contain a bichromatic P4 or
P5. This is intentionally weaker than star coloring, which Cycle9 proved
impossible with four colors on an admitted 16-vertex support.

The theorem includes the selected theta-block frontier: three or four
internally disjoint hub-to-hub paths of arbitrary lengths at least two,
attached at arbitrary degree-two interiors, each shared by two blocks. It
also includes non-theta atoms and cycles. It does NOT yet cover bridges or
nonchordless blocks. The full arbitrary-real four-query question on all
degree-four partial two-trees remains open.

Within coordinate designs, four is the worst-case uniform stable minimum
on this new class, even allowing signed unequal one-coordinate amplitudes.
Indeed the chains of K_(2,4) in Cycle9 lie in this class and exclude uniform
three-coordinate stability. This is a receiving use of that unchanged
lower proof, not a new all-real lower bound. Exact coordinate identification
alone still does not imply this stability conclusion.

## 2. Abstract gluing theorem

The construction needs less than the graph-class description. Suppose a
connected graph has a tree of nontrivial blocks such that:

1. Every shared vertex belongs to exactly two blocks and has degree two in
   each. Distinct block adjacencies therefore use distinct shared vertices.
2. The root block has a proper star coloring in four colors.
3. For each other block and any ACTUALLY specified shared root r, there is
   a realizable star-four coloring in which the two neighbors of r have
   distinct colors and at most one of their colors is flagged as below.

A star coloring is a proper coloring whose bichromatic components are
stars. For a color assignment c, define the neighbor support and far flags
within one block by

    N(r) = {c(u): u adjacent to r},
    F(r) = {c(u): u adjacent to r and u has another neighbor of color c(r)}.

The root guarantee is |N(r)|=2 and |F(r)|<=1. It is an existential guarantee
for one original root and an actual entire block coloring. It is not an
independent prescription at every cut. Global permutations of a realized
block coloring are allowed.

**Theorem B.** These assumptions suffice for a four-coloring whose every
bichromatic component is a spider with arms at most two. The algorithm
colors each block exactly once, at its actual incoming root, and passes at
most one compulsory forbidden-color message from that block to a child.

No degree bound on noncut vertices is needed for Theorem B or its recovery
bound. The degree-four cap will ensure the incidence assumptions and the
availability of the accepted rooted atom theorem in Theorem A.

## 3. Local transition: a real profile, not a freely assigned boundary

Assume the parent block is already colored and its shared vertex r has
color a. Its neighbor support P has size one or two, because its degree in
that block is two. Optionally the child is required to avoid one color
f in P at its root. This request will have a precise origin in Section 4.

First take an actual coloring of the child supplied by assumption 3. Its
root has two differently colored neighbors and at most one far flag. A
single permutation of all four colors in this child is enough:

* If P={b}, send the child root to a and its two neighbor colors to the two
  colors outside {a,b}. There is no common neighbor color. The optional
  forbidden color is avoided automatically.
* If P={b,d}, let e be the fourth color, outside {a,b,d}. Choose a retained
  color b in P, different from f when f was requested. Send the child root
  to a, one unflagged neighbor color to b, and the other neighbor color to
  e. If there is a flagged color, it is sent to e. Complete the permutation
  using the remaining color d.

Thus every actual admitted parent profile and every one-channel request
has an extension. The parent and child share at most one neighbor color;
when they share b, it is unflagged on the child side. No recoloring of the
parent is needed.

The meaning of the unflagged channel is exact. Since the child's two root
neighbors differ, there is exactly one b-neighbor u of r. Since b is not
flagged, u has no other a-neighbor. Therefore the child's whole component
in the pair {a,b} is the isolated edge r-u. This is stronger than a rank
test or merely saying that the child has a small component at the root.

The finite code may enumerate the 24 color permutations and select the
lexicographically first one satisfying these conditions. This is bounded
per-block work, not a graph-size optimization search. The explicit argument
above proves nonemptiness. The independent 30-case transition diagnostic
is a check of that argument, not the all-depth proof.

## 4. The one-message induction

Root the actual block tree. Color its root block once. Process each child
after its parent, applying Section 3 with the parent's actual neighbor
support at the original shared vertex. Most children have no extra request.

Suppose a pair from the parent enters a child B at r through its unique
shared channel b. In B it is exactly the edge r-u. If u is another cut
vertex, require the child attached to B at u to avoid color c(r) among its
root-neighbor colors. This is a legitimate one-color request because r is
an actual neighbor of u in B, so c(r) belongs to the actual N_B(u).

There is at most one such compulsory outgoing request in B: it has only
one incoming root, there is at most one common channel there, and the
admitted component is exactly one edge. If u is not a cut, no request is
needed. If it is a cut, it has only one other incident block, and Section 3
always accommodates the request. No two messages can target the same child
from distinct parents because the block adjacency is a tree.

The current block is never asked to realize a second rooted profile. Its
other attachment colors and flags are already fixed by its one chosen
coloring. The optional message constrains the NEW coloring of the next
child, not the already colored block. Consequently this induction works
through arbitrary depth and any number of actual outgoing attachment sites,
including adjacent sites. This is the missing simultaneous-attachment
control; independent one-root existence alone would not have supplied it.

## 5. Global component theorem

Fix a pair {a,b} and a nontrivial global component T. Gluing bichromatic
forests at single vertices along a block tree cannot create a cycle, so T
is a tree. The blocks contributing its edges form a connected subtree of
the block tree. There is a unique shallowest such block B. Its intersection
with T is one of its local bichromatic stars. Two disconnected local
components could not reconnect outside B without leaving and returning at
distinct cuts, which would create a cycle in the block adjacency tree.

At each cut of this local star, an outgoing child contributes either no
edge in this pair or exactly one edge from the cut to a new vertex u.
The one-message rule blocks any continuation into the child beyond u.
There is no continuation within the first child either: the component
there is precisely the isolated edge. A cut can supply at most one extra
edge because it belongs to only two blocks.

It follows that T is a local base star with at most one pendant edge added
at each of its vertices. At a leaf, this gives an arm of length two. At
the center, it gives another arm of length one. If the base star is a
single edge and both endpoints are extended, the result is P4, still a
spider with arms of length one and two. Hence every component has the
claimed shape. The argument does not assume that local star centers are
unmarked, or that all components begin at a block root.

The code independently checks the actual resulting components. When there
is a vertex of degree at least three, it must be the unique center; for a
nonbranching component the path has at most five vertices and a valid
center is found directly. This finite shape check supports the implementation,
while Sections 3-5 prove the all-size claim.

## 6. Instantiating the local hypothesis on the intrinsic class

In a connected bridgeless graph, every block is nontrivial and contributes
degree at least two at any of its vertices. Under maximum degree four, a
cut belongs to exactly two blocks and has degree exactly two in each. Thus
the incidence hypotheses in Theorem B are intrinsic, not a chosen input
promise about convenient ports. The native block decomposition recovers them.

Every block of a chordless graph is chordless. Restricting a width-two tree
decomposition to a block preserves width at most two. The degree cap also
persists. For a nontriangle block, Cycle9's accepted one-mark theorem therefore
supplies exactly the hypothesis in Section 2. For C3, three distinct vertex
colors have distinct root neighbors and no far flags; a fourth color can be
unused. These observations prove Theorem A.

For completeness, the exact constructive dependency is as follows. For a
specified degree-two mark r with neighbors s,t, form a TEMPORARY protected
edge st by suppressing r. The auxiliary graph can be chorded. Remove the
formal protected edge from its ordinary TTSP expression and retain ALL
parallel siblings, yielding the exact network H=G-r. Normalize H in the
accepted H8 grammar with original terminals s,t. The active degrees are at
most three. Cycle9's saved projection selects one literal target and a color
for r from the fixed Cycle8 certificate, giving distinct neighbor colors
and at most one far flag after restoring the original path s-r-t.

`src/marked_atom.py` implements that source-bound dependency. It checks the
exact expanded support, actual star coloring and actual marked profile.
It does not add the formal edge to any action. The old unmarked normalizer's
one-sibling rejection is not used on the chorded auxiliary graph. A reusable
fixed certificate bundle is loaded once rather than once per block.

Coverage is proved on the stated intrinsic class. The code is not advertised
as a complete recognizer for chordlessness on every other possible input:
on such inputs it may reject, or accept an actual validated stable design.
Its returned support/color/shape certificate suffices for the recovery claim
on any particular accepted graph, without silently broadening the coverage
theorem.

## 7. The complete inverse and error boundary

Put X_i=e_(c(i)) in R^4. Every whole row has norm exactly one. Properness
isolates D_ii in cell (i,c(i)). For each unordered color pair and each
component, the selected action cells equal B w, where B is its unsigned
vertex-edge incidence and w contains the original edge coefficients.
Different pairs/components and diagonal cells use disjoint input cells.

For a tree, row and column signs transform B to an oriented incidence
matrix without changing singular values. The canonical LS inverse signs
the observations, subtracts their component mean and takes subtree sums.
This is the unchanged inherited exact decoder, now acting on the new
original support and its four-column design.

Set phi^2=(3+sqrt(5))/2. Relative to a spider center, a two-edge arm with
successive values x,y satisfies

    x^2+y^2 <= phi^2 [x^2+(y-x)^2].

The energy matrix [[2,-1],[-1,1]] has smallest eigenvalue
(3-sqrt(5))/2=1/phi^2. A one-edge arm satisfies the same bound. Sum over
disjoint arms, then minimize squared deviation by replacing the center
value with the overall mean. This gives a Laplacian Poincare constant
phi^2 and an incidence inverse norm at most phi, independent of arm count.

Symmetric off-diagonal coefficients occur twice in the matrix Frobenius
norm; diagonals occur once. Summing over the disjoint action cells proves

    ||Dhat-D||F^2 <= 2 phi^2 ||E||F^2 = (3+sqrt(5)) ||E||F^2.

The operator norm is at most the Frobenius norm. This proves the complete
absolute-noise guarantee for all real supported D and all real E. It is not
an empirical error fit or a claim that the sufficient operator constant is
sharp.

Let Pi be the orthogonal projection onto the full supported action range.
For any supported numerical output with verified residual
R=Dhat X-Pi Y, the same inverse gives

    ||Dhat-D||op <= sqrt(3+sqrt(5)) (||E||F+||R||F).

Input conversion, observation acquisition and action assembly errors must
be included in E or bounded separately. Probe error adds D deltaX, which
cannot be bounded from the row budget alone. The new saved receivers use
exact rationals and have projected numerical residual exactly zero. The
raw observation residual is generally nonzero and is saved separately.

## 8. A load-bearing failure: unflagged entry alone does not reset depth

The outgoing message is essential for this construction. For b>=1, take
a chain of b four-cycles. In each block write its cyclic order as r,u,v,w,
identify u with the next block's r, and give colors

    c(r)=c in {0,1}, c(u)=1-c, c(v)=2, c(w)=3.

The shared colors alternate. Each local block is star-four colored with
zero root flags and distinct root neighbors. At each shared vertex, the
parent and child neighbor supports intersect in precisely the alternating
0/1 channel. The child's local component in that channel is an isolated
edge, exactly as in Section 3. Without the outgoing message, however,
the pair {0,1} forms a path through all b blocks, with b+1 vertices.

Let a=floor((b+1)/2) and d=ceil((b+1)/2). Across a middle edge, put constant
signed divergence 1/a on one side and -1/d on the other. Tree incidence
inversion yields an original supported symmetric matrix with a unit cut
coefficient and

    ||DX||F^2=1/a+1/d,  ||D||op>=1,
    inverse_constant^2 >= a*d/(a+d) -> infinity.

The graph is actually chordless, bridgeless, width two and maximum degree
four. This disproves the no-message RULE, not all four-colorings of the
graphs. The complete message rule colors those same supports stably. The
failed rule and an exact finite original-action witness are retained.

## 9. Additional explicit theta construction

A distinct bounded contributor derived a table-free construction for trees
of theta blocks, even allowing arbitrarily many paths per theta. Choose one
unshared hub in each block and give it the fourth color; removing these
hubs leaves a global tree. Choose the removed hub nonadjacent to the incoming
cut whenever possible. In the exceptional length-two incoming branch, color
the forest with a third-color-of-parent-and-grandparent rule, changing only
a terminal leaf when needed to avoid the incoming root's color at every
other neighbor of the removed hub. The changed leaves are nonadjacent and
every vertex has at most one changed child. Both ordinary-color and
special-color components are spiders with arms at most two.

Its complete proof, original inputs, native construction and scoped failure
of the uncorrected depth coloring are preserved separately. It supplies an
explicit alternative without the H8 table on the theta subclass; it is not
needed for Theorem A, nor a second claim of general-class coverage. The
main new receiving operation uses Theorem B and the native marked adapter.

## 10. Cost, comparisons, and remaining boundary

The native reference implementation performs iterative block decomposition,
local original-ID remapping, protected-edge normalization, one witness
realization per block, at most 24 root permutations, and actual global
component preparation/checking. With its canonical sorts it takes
O(n+m log m) comparison work and O(n+m) storage, plus one-time fixed
certificate loading. The expanded expressions have linear size. Coloring,
LS decoding and sparse output cost O(nq+m) arithmetic/storage, q=4.
Exact bit work, observation acquisition and precision/residual validation
are additional; no matrix-action source is made artificially expensive.

Ordinary sparse-Hessian star compression and acyclic substitution already
provide the underlying recovery machinery and earlier error analysis. The
new result is the specific globally stable construction from one actual
marked atom guarantee, under the unchanged absolute-noise norm. No claim
is made to have invented nonstar substitution or established historical
priority for this graph theorem. The source-grounded comparison is in
research/PRIMARY_COMPARISON.md.

The full degree-four class still has its five-action full-spark control.
Star controls can have stronger conditioning when available; forests and
the special A_L family retain their better three-query operations. Four
actions do not by themselves prove lower total cost. Direct assembly or AD
may be preferable when the native application supplies entries cheaply.
No NIST, molecular or physical-performance comparison is reopened.

The selected next boundary is bridge attachment to an atom at an actual
degree-three vertex, with its real residual degree-one budget. Such a root
is not covered by the present degree-two induction. The next question is
whether an unflagged incoming channel can be guaranteed there or a different
paid component invariant is needed. This will determine whether the bridge
restriction can be removed without adding a fifth action. Nonchordless
blocks and the full arbitrary-real four-versus-five question remain separate.
