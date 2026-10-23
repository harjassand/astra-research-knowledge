# One removed hub and a sparse three-color correction

Bounded contributor lemma for Cycle10 Pro2, 23 October 2026. The parent owns
the native recognizer, recovery operation, integration, literature comparison
and final scientific claims. This lemma is a constructive all-depth statement,
not a finite closure or an all-real lower bound.

## Input and construction

The connected original simple graph is a tree of maximal theta blocks. Each
block has two unshared hubs and k>=3 internally disjoint hub-hub paths, all of
length at least two. Every cut vertex is an interior vertex of each of exactly
two blocks. The block adjacency graph is a tree. Arbitrary k and path lengths
are allowed. The k in {3,4} subfamily has maximum degree at most four.

Root the block tree at B0. Every other block B has its actual incoming cut r_B.
Choose one hub h_B for deletion as follows. If r_B is the middle of a length-two
branch, choose either hub. Otherwise choose a hub not adjacent to r_B. Such a
hub exists: on a branch of length at least three no interior vertex is adjacent
to both hubs. For B0 choose either hub. The vertices h_B are unshared and hence
independent. Deleting them leaves a global tree F: each block minus its selected
hub is a tree, and those trees meet only according to the block tree.

Root F at the surviving hub of B0. This orientation enters every child block
at its actual r_B. A block entered through a length-two branch has r_B as a
leaf in its local F-tree; the next vertex is its surviving hub. Call these
blocks *constrained*. For a constrained block B, every neighbor z of h_B other
than r_B is a local F-leaf. Impose the single constraint

    color(z) != color(r_B).

A vertex has at most one such constraint: if it also belongs to a child block,
it is that block's incoming root, which is excluded from its constraint list.
All constraints refer to ancestors in F at distance at least two.

Give every h_B color 3. Color F with {0,1,2} in ancestor-before-descendant order.
Give its root color 0 and its children color 1. For each deeper vertex z, let
p,g be its parent and grandparent. The default color is the unique third color
different from color(p),color(g). If z is constrained and this default equals
the forbidden color color(r_B), give z color(g) instead. Otherwise keep the
default. A vertex at which this replacement occurs is a *flip*.

The replacement is proper because parent and grandparent have distinct colors.
It satisfies the constraint because its old default was distinct from both.
Forced vertices have depth at least two, so the grandparent exists. The actual
original cut has only one color; no boundary colors are chosen independently.

## The two structural flip facts

**Fact A.** A flip cannot lie on a branch of length two. In a constrained block,
the entering root has color c. Let w be the surviving hub and let its color be
b, necessarily different from c. A different length-two branch ends in a leaf
z whose parent is w and grandparent is the entering root. Its default is the
third color different from b,c, and so is not c. It does not flip. Consequently
every flip lies at the end of a branch of length at least three. Its parent is
a nonhub interior vertex in the same block.

**Fact B.** No first vertex after an incoming root in a child block is a flip.
If the child is constrained, that first vertex is the surviving hub, never a
constrained leaf. If the child is unconstrained, it has no flips. Constraints
from a descendant block never apply to its incoming root, so no different
block can create a first-step flip at the same vertex.

These imply two global properties. First, no two flips are adjacent in F. An
edge within a block cannot join its local leaves; Fact A further rules out a
hub-parent flip. An edge from a flipped cut into its child block has a nonflip
other endpoint by Fact B. Second, every vertex has at most one flipped child.
If it has a flipped child within its parent block, Fact A says it is a nonhub
interior path vertex and has only one local forward neighbor. Its additional
child-block neighbors are not flips by Fact B. A hub has no flipped children:
its one-step local leaves lie on length-two branches and Fact A applies.

These statements depend on the original two-block incidence condition and
on the genuine branch lengths. They do not follow merely from small local
diameter, local colorability, or bounded total degree.

## All pairs among the three forest colors are short-arm spiders

Every bichromatic component inside F is a tree. Root one such component at its
vertex closest to the root of F. This vertex is unique because connected
subtrees of a rooted tree have a unique minimum-depth vertex.

For a directed path u-v-w that uses only two colors, properness implies
color(w)=color(u). The default rule would give w the third color, so w is a
flip. A directed bichromatic path of three edges would therefore require two
adjacent flips, which is impossible. Each component has depth at most two.
Moreover each intermediate vertex has at most one child in that component,
because any such child must be a flip and there is at most one flipped child.
Thus every nontrivial component is a spider with arms of length one or two.
The number of arms need not be bounded.

## Pairs involving special color 3 are also short-arm spiders

A non-special vertex has at most two special-color neighbors, one in each of
its at most two incident blocks. A vertex with two such neighbors is their
actual shared cut. After suppressing these degree-two connectors, edges among
special hubs form a subgraph of the block adjacency tree, so there is no cycle.

Fix color c in {0,1,2}. If a (3,c) component enters the hub h_B of a child block
through r_B, then r_B is adjacent to h_B. The hub-choice rule forces B to be a
constrained block, and color(r_B)=c. All other neighbors of h_B were constrained
to avoid c. Therefore h_B has degree one in this component: propagation stops
there. Starting with the least-depth block hub in a component, every arm has
one edge to a non-special neighbor, and possibly one more edge to a terminal
child hub. No internal connector can branch because it belongs to at most two
blocks. Hence this component, too, is a spider with arms of length at most two.

## Recovery consequence

The complete coloring is proper and acyclic. Every bichromatic component has
the exact short-arm form of Cycle9 PROOF.md Section 5.1. Its anchored quadratic
gives incidence inverse norm at most sqrt((3+sqrt(5))/2). Independent selected
action cells, free-diagonal cells and symmetric off-diagonal duplication yield

    ||Dhat-D||op <= ||Dhat-D||F <= sqrt(3+sqrt(5)) ||E||F.

This uses FOUR original coordinate actions and the unchanged canonical LS
decoder, not actions of F or of contracted blocks. The selected hubs and F
are a coloring device only. Every original edge and free diagonal remains in
the action and output. Precision/residual/input-assembly allowances are the
same as in the Cycle9 exact LS theorem.

With a supplied valid block decomposition and path lists, choosing hubs,
building F, its rooted ordering, constraints, coloring and shape checking
take O(n+m) work and storage. Native graph recognition and canonical sorting
are separate obligations owned by the parent. No free recognition is claimed.

## Why the correction is scientifically necessary

The unmodified three-color depth rule can fail on an actual chain of theta
blocks with path lengths (2,3,3). Let each incoming root be the midpoint of
the length-two branch, and attach the next block at the neighbor of h_B on
one length-three branch. In F this outgoing root is distance three from the
incoming root, so the ordinary depth-mod-three colors give every such root
the same color c. Each nonroot special hub then has all its three neighbors
colored c. The (3,c) component spans the entire block chain and has growing cut mass.
Thus deleting one hub and using an ordinary stable forest coloring is not by
itself a stable operation on the original support. The endpoint correction
cuts precisely these transmissions while preserving short-arm components in
the forest colors. This is a scoped failure of that rule, not a graph lower
bound against four-coordinate or arbitrary-real designs.

More exactly, use b=2s blocks, root F at the surviving hub in the first block,
and use its other hub as the selected one in every block. The first block's
two length-three endpoint neighbors have color 2; its length-two midpoint
has color 1. Every later incoming root has color 2, and all three neighbors
of its special hub have color 2. The (3,2) component has 3b=6s vertices. The
edge from the incoming root to the special hub of block s (zero-based) splits
it into 3s and 3s vertices. The exact supported cut witness therefore has
unit cut coefficient and full original action squared norm 2/(3s), giving
inverse squared lower 3s/2. This is an all-size failure mechanism for the
uncorrected rule on maximum-degree-four theta-block supports.

The bounded actual diagnostic uses b=12, hence a=b=18, Gamma=9 and action
squared norm 1/9. Its saved nonzero edge coefficients and all 73-by-4 original
action entries verify this exact identity. The corrected coloring on that
same graph has short-arm components of order at most five. A separate native
57-vertex, 73-edge graph has seven mixed-parity, mixed-arity theta blocks,
three consecutive actual attachment sites in one path, both incoming-root
types and depth three; the complete corrected shape check also passes with
component order at most five. These samples check implementation mechanisms;
the preceding argument supplies the all-size conclusion.

## Scope and cost record

The argument above is new relative to the assigned Cycle9 checkpoint. It does
not establish historical novelty or external acceptance. This contributor's
proof discovery, reasoning and source-reading costs are unknown; they are not
replaced by a short diagnostic time. The parent must integrate and independently
challenge the all-depth argument and supply actual native receiving use before
claiming a completed executable scientific operation.

The new diagnostic body, including both original input constructions, native
recognition/coloring, exact bad-rule witness and JSON serialization, took
0.004001641998911509 seconds wall and 0.003999516000000002 seconds CPU, with
process peak RSS 12,189,696 bytes. This excludes inference, reading, authoring,
review, integration and interpreter startup. The first diagnostic attempt
incorrectly selected one of the two graph-center vertices of an asymmetric
diameter-three spider as its arm center, then falsely rejected an intermediate
branch. The actual component had center35, arms [37,36], [40], [41]. The shape
checker now chooses the unique degree>=3 vertex, if present, otherwise the
path midpoint. Actual failed source and exception diagnosis are preserved in
failed/. That first body was not exception-timed and its cost remains unknown.
No unsuccessful scientific construction was erased by that implementation fix.
