# Critical review of parity-spider recovery and its coordinate boundary

Focused analytic review, `/root/cycle8_port_lemma`, Cycle9, 22 October 2026.
The principal owner authors the main proof, native recognition/constructor,
full-action receiver and integration. This file independently checks the
new positive mechanism and its lower-bound scope, without a producer replay.

## 1. Intrinsic class and graph facts

Let G be a finite connected graph with at least one block. Require every
block to be K2,k_B with integer k_B>=3. In each block the two hubs are
intrinsically identified by within-block degree k_B>=3, while the k_B middle
vertices have within-block degree two. Require every cut vertex to be a
middle vertex in every incident block and to belong to exactly two blocks.
Equivalently, every middle belongs to at most two blocks, and hubs are never
cut vertices. Bridges are excluded by the block condition. An isolated
vertex, if desired, is a separate trivial diagonal case.

The block-cut incidence graph is a tree. Suppressing its degree-two cut
nodes gives a tree T of blocks; one edge of T corresponds to each actual
shared middle. Distinct edges incident to a block correspond to distinct
middles. Thus degree_T(B)<=k_B. If T has b blocks, then

    n = sum_B k_B + b + 1,
    m = 2 sum_B k_B.

These graphs are simple, chordless and triangle-free. Cycles stay in one
block, and a K2,k block has only induced four-cycles. Treewidth is at most
two by joining the standard bags {hub1,hub2,middle} at the shared middle.
The global maximum degree is max(4,max_B k_B) when a cut vertex is present,
and the evident smaller value otherwise. In particular k_B in {3,4} gives
a class inside the original degree-four target; the general k_B theorem is
a separately stated degree-free operation, not an unchanged degree-four
claim.

## 2. Four-color parity construction

Root T at an arbitrary block. Choose an order of the two hubs of each block
and color them 0 and 1. A middle shared by a parent block at depth d and its
child is colored 2+(d mod 2). An unshared middle of a block at depth d has
that same outgoing color 2+(d mod 2). This assigns one actual color to each
original vertex and leaves every edge untouched. The coloring is proper.

Fix one hub color h in {0,1} and one middle color j in {2,3}. At a block
whose outgoing parity is j, its h-hub is the center of a component. Each
unshared j-middle gives an arm of length one. Each shared j-middle leading
to a child gives an arm of length two, ending at that child's h-hub. The
child hub has no other j-neighbor: its other middles have the opposite
outgoing parity. A nonroot center's upward shared middle has the opposite
color and is not in this component. Other hubs for this pair are isolated
or are these arm ends.

Therefore every edge-containing bichromatic component is a tree consisting
of a center with arbitrarily many arms, each of length at most two. There
are no edges in the pairs {0,1} or {2,3}. These statements do not assume a
bounded number of arms or a bounded block-tree depth. For k_B<=4 the
components have at most nine vertices, but that size bound is unnecessary
for the degree-free theorem.

## 3. Dimension-independent Poincare and inverse bound

Let T0 be any spider whose arms have one or two edges. Let o be its center
and let z be any real vertex function. The variance about the mean is the
least squared deviation from a constant, hence

    sum_v (z_v-mean(z))^2 <= sum_v (z_v-z_o)^2.

For a two-edge arm, write a=z_1-z_o and b=z_2-z_1. Its contribution on the
right is

    a^2+(a+b)^2 = (a,b) [[2,1],[1,1]] (a,b)^T
               <= ((3+sqrt5)/2) (a^2+b^2).

A one-edge arm satisfies the same bound. Summing gives

    variance(z) <= phi^2 sum_(uv edge) (z_u-z_v)^2,
    phi^2=(3+sqrt5)/2.                                  (3)

There is no arm-count or graph-size factor. Thus the smallest positive
Laplacian eigenvalue is at least phi^-2=(3-sqrt5)/2, and the inverse of the
oriented tree incidence on its range has Euclidean norm at most phi. Signing
one bipartition transfers the same result to unsigned incidence.

For the coordinate action X_v=e_color(v), distinct color-pair components and
own-color diagonal cells are disjoint observation blocks. The canonical LS
edge inverse therefore obeys

    sum_edges |edge_error|^2 <= phi^2 ||E_off||F^2.

The symmetric output duplicates each off-diagonal coefficient, while diagonal
errors use separate cells. Consequently

    ||Dhat-D||F^2 <= ||E_diag||F^2 + 2 phi^2 ||E_off||F^2
                  <= (3+sqrt5) ||E||F^2,
    ||Dhat-D||op <= ||Dhat-D||F
                  <= sqrt(3+sqrt5) ||E||F.               (4)

This is exact noiseless recovery on the full original supported symmetric
space, including its free diagonal. Every whole probe row has norm one.
The result uses arbitrary absolute Frobenius noise, not random noise.

The incidence bound (3) is sharp on a five-vertex path viewed as two
length-two arms: take opposite copies of a top eigenvector of the displayed
2x2 matrix, giving mean zero. This does not assert sharpness of the operator
constant in (4), or an optimal inverse among all designs.

## 4. Why the middle-incidence hypothesis is material

If one middle can belong to more than two blocks, a connecting middle in a
fixed color pair can have several child hubs, so an arm may branch. The
spider proof no longer applies. The failure is quantitative, not just a
missing drawing convention.

Take one central K2,3, and attach r new K2,3 blocks at each of two central
middles u,v; all other vertices are distinct. Apply the same depth-parity
rule on the natural block-cut tree. In the {0,2} component there is a central
hub, the three central middles u,v,w, and r child hubs attached at each of
u,v. Its order is N=2r+4. The edge from the central hub to u splits this tree
into r+1 and r+3 vertices. The inherited exact cut certificate gives

    Gamma = (r+1)(r+3)/(2r+4),
    inverse_operator_constant >= sqrt(Gamma).

This diverges although the component has diameter four. It rejects the same
parity design after dropping the at-most-two-blocks-per-middle hypothesis;
it is not a universal four-query graph obstruction. The degree-free positive
claim must retain that incidence restriction.

## 5. Exact three-coordinate lower on the admitted class

Consider a path of b=2m K2,4 blocks, with consecutive blocks sharing distinct
middle vertices. In any exact unit-coordinate design using three colors, the
coloring must first be proper: an edge whose endpoints have the same color
has a kernel obtained by opposite diagonal corrections. It must also be
acyclic, since an alternating supported edge coefficient around a two-colored
cycle gives an exact kernel.

In a K2,4 block, equal hub colors would force its four middles into the other
two colors; some middle color repeats and creates a bichromatic C4. Therefore
the hubs have distinct colors, and all four middles use the third color.
Shared middles propagate this common middle color through the connected block
tree. Each of the other two colors appears on exactly one hub in each block,
regardless of local exchanges of the two hub labels.

For either hub color and the common middle color, the whole induced component
is a tree with one hub per block and every middle. It has

    N=4b+1=8m+1.

Delete the edge between the m-th hub and the middle shared with the next
block. The left side has 4m vertices; the right side has 4m+1. These counts
include the actual shared middle on the right. Thus the inherited cut-balance
witness gives, for every exact unit-coordinate three-color design,

    rho^2 >= Gamma_m = 4m(4m+1)/(8m+1).                   (5)

The witness has a supported edge coefficient of magnitude one and exact
squared action norm 1/(4m)+1/(4m+1). Its operator norm is at least one.
As m grows the lower bound diverges. A nonlinear exact estimator cannot
escape it: a supported matrix and cancelling noise produce the same zero
observation as the zero matrix.

Thus four is the minimum **uniformly stable unit-coordinate query count**
on this intrinsic family. Three unit-coordinate actions still identify every
finite member exactly; the obstruction is uniform stability. Formula (5) is
not an all-dense-design three-query lower.

## 6. Optional strengthened scope: signed/unequal coordinate amplitudes

The lower can also exclude uniform three-query recovery of row-scaled
coordinate form X=W C, where C is a three-color coordinate matrix and W is
real diagonal with |w_v|<=1. If a weight is zero, its free diagonal coefficient
is invisible. Otherwise a supported congruence D=W^-1 D0 W^-1 transfers every
kernel of C to a kernel of X. Consequently the same properness/acyclicity and
K2,4 color classification are necessary.

Let alpha=min_v |w_v|>0. A single free diagonal gives rho>=1/alpha. Let D0 be
the unit-coordinate cut witness for (5), so ||D0||op>=1 and
||D0 C||F=Gamma_m^-1/2. Set D=W^-1 D0 W^-1. Since ||W||op<=1,

    ||D||op >= ||W D W||op = ||D0||op >=1,
    ||D X||F = ||W^-1 D0 C||F <= alpha^-1 Gamma_m^-1/2.

Therefore

    rho >= max(alpha^-1, alpha sqrt(Gamma_m))
         >= Gamma_m^(1/4).                              (6)

This weaker rate still diverges for every choice of signs and amplitudes.
It retains the whole-row budget and the free-diagonal hypothesis. It remains
a coordinate-representation lower, not a lower for arbitrary real dense
three-column matrices. No sharpness of the exponent in (6) is claimed.

## 7. Stronger conditioning control with five actions

A direct five-color star operation is available on the exact same full class.
Color all middles 4. Give hubs in even-depth blocks colors 0,1 and hubs in
odd-depth blocks colors 2,3. At a shared middle the four incident hub colors
are distinct; at an unshared middle the two are distinct. Hence each
bichromatic component is a star. The inherited triangle-free star-LS bounds
are operator sqrt(3/2) and Frobenius sqrt2.

This is a stronger conditioning comparator than (4), at the cost of one extra
full action. On the sixteen-vertex obstruction, it also matches the star-five
lower. Four actions save an action; no runtime or aggregate cost advantage
follows without actual action and precision costs.

## 8. Review status and resources

The parity construction, degree-free extension, Poincare bound, exact
three-coordinate cut and optional amplitude corollary are analytically
consistent. The actual native recognizer must enforce the whole intrinsic
block contract, retain original IDs and edges, and charge its Tarjan/labeling
and any canonical sorting. It must not silently accept bridges, hub cut
vertices or a middle shared by three blocks. The final action/inverse check
must use actual original support and all four columns.

No producer code, finite certificate or receiving experiment was executed by
this reviewer for these claims. The root's implementation and independent
native receiving checks are separate obligations. Inference, source authoring
and mathematical review costs are unknown. Historical novelty, external
acceptance, practical speedup and all-real query optimality are not asserted.
