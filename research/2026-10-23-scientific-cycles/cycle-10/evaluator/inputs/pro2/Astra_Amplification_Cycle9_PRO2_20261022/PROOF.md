# Stable recovery beyond compatible star colorings

Pro2, 22 October 2026. This is an internally proved and independently
challenged checkpoint, with exact executable receiving calculations. No
historical priority, external acceptance, or application speedup is claimed.

## 1. Model and strongest statements

The original finite simple graph G is known before a graph-adapted real design
X is chosen. Every whole row of X has Euclidean norm at most one. The unknown
D is any real symmetric matrix supported on G, with arbitrary free diagonal.
All original actions Y=DX+E are observed; E has arbitrary absolute Frobenius
norm. Exact noiseless recovery and graph-size-independent operator error are
required. There is no reduced-action oracle, prior on coefficients or noise,
free recognition, or uncharged numerical residual.

Fix p>=2. Let C_p consist of connected graphs with at least one block, whose
maximal blocks are complete bipartite graphs K_(p,k_B), k_B>=p+1, such that
every cut vertex is on the k_B-vertex side in each incident block and belongs
to exactly two blocks. There are no bridges or isolated vertices in this
definition. The p-vertex side consists of **hubs** and the other side of
**middles**. The common p and these roles are intrinsically identifiable by
within-block degrees: hubs have degree k_B>p and middles have degree p.
Depth, number of blocks, branching, and the k_B are unbounded.

**Theorem 1 (stable construction).** Every G in C_p admits an explicit
coordinate design X_i=e_(color(i)) with q=p+2, and its canonical least-squares
inverse satisfies, for all admitted D,E,

    ||Dhat-D||op <= ||Dhat-D||F <= sqrt(3+sqrt(5)) ||E||F.

The constant is independent of p, all k_B, and graph size. Native graph
recognition, design, and the original-action inverse are supplied. The
Frobenius constant is a sufficient universal bound; no sharp operator-norm
claim is made.

**Theorem 2 (coordinate count).** The minimum number of coordinate directions
that gives uniform operator stability over C_p is p+2. This remains true if
each coordinate row may have an arbitrary nonzero signed amplitude of
absolute value at most one. The minimum count for exact identification alone
in this representation is p+1. This is NOT a lower bound for arbitrary dense
real designs with p+1 columns.

**Theorem 3 (cost of the star requirement on this class).** Every G in C_p
has a star coloring with 2p+1 colors, giving the stronger canonical LS bounds

    ||Dhat-D||op <= sqrt(3/2)||E||F,
    ||Dhat-D||F  <= sqrt(2)||E||F.

Some G in C_p require 2p+1 star colors. Thus the worst-case star count is
exactly 2p+1, whereas the uniform stable-coordinate count is p+2. The latter
saves p-1 actions while giving a weaker noise bound. Neither dominates total
cost without an actual acquisition/accuracy contract.

For p=2, the subfamily k_B in {3,4} lies inside the original chordless,
treewidth-two, maximum-degree-four target. Three K_(2,4) blocks already
require FIVE star colors, but have a stable FOUR-coordinate inverse by
Theorem 1. The full arbitrary-real four-versus-five question on ALL
treewidth-two, maximum-degree-four supports remains open. For p>=3 the new
blocks are bipartite and triangle-free but generally NOT chordless; this is
an expressly stated generalization, not a claim about chordless atoms.

## 2. What the actual marked-root investigation establishes

### 2.1 Correct structural contexts

The accepted Cycle8 theorem colors every two-connected chordless width-two,
degree-four atom by four star colors. Its native normalizer chooses convenient
ports. It does not automatically qualify an actually specified attachment
vertex. The new source `research/marked_structure/PROOF.md` proves:

* Every specified degree-three vertex v can be an actual H8 terminal. Protect
  an original incident edge vu. In G=P(edge vu,H), the load of v in H is at
  least two. Following the v-side through series nodes reaches a parallel
  node with endpoint v. Reroot at that node with its actual complement.
  Three genuine branches and chordlessness force a nonadjacent other port
  and induced terminal paths. The inherited normalization preserves v and
  every original edge.
* A degree-two vertex cannot always be a terminal: in K_(2,3), a specified
  middle v has only the other middles as nonneighbors. Every choice w admits
  a simple v-w path with a chord. H8 requires every terminal path induced.
* Every nontriangle degree-two mark v, with neighbors a,b, nevertheless has
  the exact original representation G=P(path2(a,v,b),H), where H=G-v has an
  H8 expression and active endpoint loads in {1,2,3}. Suppress v to a formal
  edge ab, protect it, collect ALL other parallel siblings, and then remove
  that formal edge. The original a-v-b path is restored. Every H path closes
  through a-v-b, so it is induced and normalizes into H8. The auxiliary
  suppressed graph may be chorded; the old one-sibling rejection must not be
  applied to that auxiliary graph.

These are exact support-preserving representations, not added stubs or new
matrix entries. C3 is a separate explicit three-color case.

### 2.2 A new finite receiving consequence of the inherited certificate

For an actual H coloring, let its port colors be A,B and its neighbor-color
supports N_a,N_b. Choose color Z for the original midpoint v. After a valid
parallel merge, v has neighbor set {A,B} and far-repeat flags

    F_v = ({A} if Z in N_a else empty) union
          ({B} if Z in N_b else empty).

A far-repeat flag at color c means that a c-colored neighbor of v has another
neighbor of v's color. The inherited targets bound N and F from above at
exact degrees/colors; they do not assert arbitrary rooted choices.

The fixed inherited certificate has exactly 66 families with both loads at
most three. `results/marked_root_projection.json` supplies, for EVERY such
family, one literal target and Z with A!=B, Z different from A,B, Z in neither
port flag set, and Z in at most one of the two port support bounds. This is
the complete NEW finite obligation, not a rerun of the inherited 11,142-row
closure. Each path2 port has flag zero because A!=B. The old merge rule
therefore accepts, and monotonicity preserves the selected bounds for the
actual child realization.

Consequently every specified degree-two atom vertex has a realizable star-four
coloring in which its neighbors differ and at most one root channel is
flagged. This is a genuine use of the completed atom certificate and the
new marked-midpoint representation. It qualifies ONE mark, not independently
chosen profiles at multiple marks of one atom.

### 2.3 Exact one-root compatibility and its global failure

At a degree-two root, up to a permutation fixing its own color, the types are
M (equal neighbor colors, no flags) and D0,D1,D2 (two different neighbor colors,
with zero, one, or two flags). For two blocks meeting only at this root, the
exact star merge condition is

    N1 intersect N2 intersect (F1 union F2) = empty.

The total degree is four. M can meet every type. D0/D0, D0/D1, and D1/D1 can
meet after root-fixing permutations. D2 can meet only M: two two-element
neighbor supports among the three remaining colors must intersect. These
are compatibility statements for ACTUAL colorings, not independent choices
at several vertices of one block.

In K_(2,4), star-four colors force the hubs to differ. Otherwise the four
middles would need four distinct colors different from the common hub color,
but only three are available. With different hubs, the middles use the two
remaining colors. A specified middle has D0 exactly when its color is unique
among the four middles; otherwise it has D2. There is at most one D0 middle,
although any single specified middle can be made D0.

Take three such blocks, with the central block joined at two distinct middles
to one middle in each outer block. The shared vertex requires D0 on both
sides, but the central block cannot supply D0 at both sites. Thus this
16-vertex, 24-edge, chordless width-two degree-four graph has no star-four
coloring. In fact, the two-block rooted compound forces every remaining
degree-two middle to be D2 in every star-four coloring, so it cannot accept
another K_(2,4) there without abandoning the star-four requirement.

The analytic contradiction quantifies over ALL star-four colorings, not one
palette rule. A distinct exact checker finds 0 canonical colorings for the
16-vertex support, after 142 nodes/559 attempted assignments, and verifies its
width-two decomposition and 18 chordless C4 cycles. The one- and two-block
controls have 192 and 144 labeled star-four colorings. These finite checks
support the analytic proof, not replace its quantifiers.

## 3. Intrinsic structure and preparation for C_p

The block-cut incidence graph of a connected graph is a tree. Every cut
vertex here belongs to exactly two blocks, so suppressing the cut-vertex
nodes leaves a tree T on the blocks. Different edges incident to one block
use distinct middle vertices. There is no chosen or free attachment port:
all attachments are recovered from the original graph.

Each block K_(p,k) has a width-p decomposition with bags consisting of its
p hubs and one middle. Connect these bags in a tree. At a shared middle,
join one bag from each incident block containing that original vertex.
The block tree makes the combined decomposition a tree and the running
intersection property holds. Hence every C_p graph has treewidth at most p.
For b blocks,

    n = sum_B k_B + (p-1)b + 1,
    m = p sum_B k_B.

Original hubs have degree k_B. Unshared middles have degree p; shared middles
have degree 2p. When p=2 and k_B<=4 this gives the required maximum degree
four. Every cycle lies within one block. K_(2,k) has only chordless four-cycles,
so this p=2 subfamily is chordless at every block-tree depth.

`src/block_spider_recovery.py` accepts only n and the original edge list.
An iterative low-link traversal computes maximal blocks. Within each block
the minimum degree identifies p; exactly p vertices must have higher degree,
and complete bipartite adjacency is checked. The common p is checked across
blocks. Original-vertex memberships certify the cut roles and multiplicity
two. The resulting block adjacency is checked to be a tree and rooted.

This is a native recognizer and constructor for the stated C_p class, not a
recognition promise for arbitrary chordless graphs. Canonical edge/block
sorting is charged. The implementation uses per-block middle SETS for cut
membership; an earlier unexecuted list-membership version would have had
quadratic cost for large k and was corrected after review.

## 4. The all-depth parity construction

Root T and let d(B) be block depth. In every block, assign its p distinct
hub vertices the colors 0,...,p-1 in original-ID order. Give an unshared
middle of B color p+(d(B) mod 2). Give a shared middle between a parent B
and its child C color p+(d(B) mod 2). The shared vertex has one actual color.
All original edges go from hubs to middles, so this is proper, with p+2 colors.

Fix a hub color h and a middle color c=p+epsilon. A block whose depth has
parity epsilon contributes one h-colored center. Its c-neighbors are all
its outgoing/shared child middles and all its unshared middles. Its possible
incoming middle has the other middle color and is absent from this pair.
An unshared middle is a leaf. An outgoing shared middle leads to the one
h-colored hub of its child block. That child hub has only this one c-neighbor,
because all its outgoing and unshared middles have the opposite middle color.
It is therefore a leaf of the same pair component.

Every nontrivial bichromatic component is consequently a spider: one center,
with internally disjoint arms of length one or two. No arm has intermediate
branching because a shared middle belongs to exactly two blocks. No arm
continues through another generation because the middle parity changes.
This proves the invariant at arbitrary depth and arbitrary branching; a
bounded-diameter assertion alone would not have proved the needed estimate.
Pairs of two hub colors or two middle colors have no edges.

The number of arms and component size can be unbounded when k is unbounded.
Uniform stability follows from the actual arm structure, not bounded size.
The original C_p graph, all its vertices, and all its edges remain in X and Y.

## 5. Canonical LS inverse and uniform absolute-noise bound

The free diagonal D_ii is isolated in action cell (i,color(i)). For a fixed
unordered color pair and a component with edge coefficients w, the selected
original action cells equal B w, where B is the unsigned vertex-edge incidence
matrix of that component. Distinct components/pairs and diagonal cells use
disjoint input coordinates. For a tree, multiplying one bipartition's rows
and suitable edge columns by signs converts B to an oriented incidence
matrix without changing singular values.

The least-squares solution signs the observations, subtracts their component
mean, and takes subtree sums. This is exactly the inherited canonical inverse
in `src/coordinate_decoder.py`, now used on the new original support. It is
linear, exact on noiseless actions, and uses O(nq+m) arithmetic/storage with
q=p+2 after graph preparation. Arithmetic counts do not bound rational bit cost.

### 5.1 The spider estimate

Set phi^2=(3+sqrt(5))/2. For arbitrary real values z on a spider with center o,
subtract z_o. A one-edge arm contributes x^2 to both squared vertex values
and edge energy. A two-edge arm with successive values x,y satisfies

    x^2+y^2 <= phi^2 [x^2+(y-x)^2].

Indeed, the energy quadratic has matrix [[2,-1],[-1,1]], whose smaller
eigenvalue is (3-sqrt(5))/2=1/phi^2. Summing over disjoint arms gives

    sum_v (z_v-z_o)^2 <= phi^2 sum_uv (z_u-z_v)^2.

The mean minimizes squared deviation from a constant, so

    sum_v (z_v-mean(z))^2 <= phi^2 sum_uv (z_u-z_v)^2.

Thus the smallest positive Laplacian eigenvalue is at least 1/phi^2 and the
smallest incidence singular value is at least 1/phi. Every bichromatic tree component's LS
edge error norm is at most phi times its selected observation error norm.
Different bichromatic components/pairs use disjoint selected cells. A symmetric off-diagonal
coefficient occurs twice in matrix Frobenius norm, whereas a diagonal occurs
once. Summing yields

    ||Dhat-D||F^2 <= 2 phi^2 ||E||F^2 = (3+sqrt(5))||E||F^2.

Operator norm is at most Frobenius norm. This proves Theorem 1 for all real
D,E. The estimate does not require a degree cap, a stochastic noise model,
or sampling of graph sizes. The arm Poincare constant itself is sharp on a
five-vertex path with two length-two arms, but we do not claim that this
establishes sharpness of the full operator recovery bound on C_p.

### 5.2 Precision and full original actions

Let Pi be the orthogonal projection onto the range of the full supported
action map L(D)=DX. For any supported symmetric numerical candidate, if
R_num=Dhat X-Pi Y, exact inversion gives

    ||Dhat-D||op <= sqrt(3+sqrt(5)) (||E||F+||R_num||F).

An acquisition, storage, or action-assembly error must be included in E or
bounded separately. Perturbed probes add D deltaX, which is not bounded by
the row budget alone. Saved receiving operations use exact rational inputs,
outputs and normal equations: R_num=0 exactly. The raw Y-Dhat X residual is
generally nonzero; it is the orthogonal discarded noise, not an unpaid error.

## 6. Exact-coordinate and stable-coordinate counts

For unit coordinate designs, properness is necessary: a monochromatic edge
with free diagonals gives a nonzero supported symmetric kernel. In a proper
coloring, each pair's incidence is injective exactly when its components are
trees. A bichromatic cycle has an alternating exact edge kernel. These are
the inherited exact characterization, not new all-real lower bounds.

In K_(p,k), if both bipartition sides repeat colors, two repeated vertices
from each side form a bichromatic C4. Thus one side must be rainbow in any
exact coordinate design. With at most p+1 colors and k>=p+1, the middle side
cannot be rainbow: at least one further hub color would be required. Hence
all p hubs have different colors, and every middle has the one remaining
color. Fewer than p+1 colors are impossible. Conversely, globally color hubs
0,...,p-1 and all middles p. Each color-pair component is a block-incidence
tree, so p+1 is exact-injective on every graph in C_p.

Shared middles force their common color to propagate through the block tree
in EVERY exact p+1-coordinate design. For each other color h, the component
contains exactly one h-hub per block and all middles. Choose a chain of 2s
blocks, each K_(p,2p). That component is a tree on 4ps+1 vertices. A central
edge splits it into a=2ps and b=2ps+1 vertices.

Here is the exact adversarial operation. Give the oriented vertex divergence
the constant 1/a on one side of that cut and -1/b on the other. Its sum is
zero, so it is in the tree-incidence range. Subtree sums recover unique edge
weights with absolute value ONE on the cut edge. Place those weights into
the original symmetric D, with all other coefficients and diagonals zero.
Only this pair's original action cells are nonzero, and

    ||DX||F^2 = 1/a+1/b,
    ||D||op >= 1,
    rho^2 >= Gamma_(p,s) = 2ps(2ps+1)/(4ps+1).

This diverges with s. It applies to every exact decoder, including nonlinear
ones: the same observation is a noiseless action of D and pure noise with
true matrix zero. Exactness fixes the output in the first interpretation.
It is an all-design statement within the coordinate class, not a bad-seed
example.

Allow now X=W C, with coordinate C and signed nonzero amplitudes |w_i|<=1.
Zero amplitudes would already lose a free diagonal. Let alpha=min|w_i|.
Congruence by W converts exact kernels between C and X, so the same proper
acyclic coloring restrictions apply. A diagonal witness gives rho>=1/alpha.
For the unit-coordinate cut witness D0 above, let D=W^(-1)D0W^(-1). Then

    DX=W^(-1)D0 C,
    ||DX||F <= alpha^(-1)||D0 C||F,
    |D_uv|=1/|w_u w_v|>=1 on the cut edge.

Therefore rho>=alpha sqrt(Gamma), and

    rho >= max(1/alpha,alpha sqrt(Gamma)) >= Gamma^(1/4).

This still diverges even when the amplitudes depend arbitrarily on the graph.
Together with Theorem 1, it proves the stable-coordinate minimum p+2. No
restriction or claim is imposed on designs whose rows mix several coordinates;
the full arbitrary-real lower question is explicitly separate.

## 7. Sharp star-color comparison

Use colors 0,...,p-1 for hubs in even-depth blocks and p,...,2p-1 for hubs in
odd-depth blocks. Color every middle 2p. At a shared middle, adjacent blocks'
hub palettes are disjoint. For each pair (hub color,2p), a component is just
one original hub and its adjacent middles: a star. This uses 2p+1 original
coordinate actions and charges the extra p-1 actions over Theorem 1.

For star LS, the edge Gram matrix is I+11^T, so coefficient error squared is
at most the selected observation error squared. Symmetry gives Frobenius
constant sqrt2. The stronger operator bound is the inherited triangle-free
star-LS lemma: a direct exact inverse T selects one isolated leaf cell per
edge plus every own-color diagonal. For unit z, w_i=z_i^2,

    ||E -> z^T T(E) z||^2 = sum_i w_i^2+4 sum_ij_in_edges w_i w_j.

Move mass between nonadjacent positive vertices, keeping their sum fixed.
Convexity makes some endpoint no worse and removes one support vertex.
Repeat to a clique. The graph is bipartite, hence the clique size is at most
two; the expression is at most 1+2a(1-a)<=3/2. Canonical LS is T Pi and Pi is
an orthogonal contraction. Thus its operator constant is at most sqrt(3/2).

For the matching star lower, take one central K_(p,2p) and p disjoint leaf
copies, identifying one middle of each leaf with a different middle of the
central block. This has n=3p^2+2p, m=2p^2(p+1), maximum degree 2p, and
treewidth at most p. It is in C_p.

Suppose a star coloring uses at most 2p colors. In every block the hubs must
be rainbow: a repeated hub color would force all 2p middles distinct, plus
at least one disjoint hub color, exceeding the palette. Thus each root
middle has p different neighbor colors. If its middle color repeats in that
block, every one of these p channels is flagged. At a cut middle, the two
p-element neighbor supports lie among at most 2p-1 other colors and must
intersect. Any repeat on either side gives a bichromatic P4. Therefore a
cut middle's color must be unique within EACH incident block.

The central block would need p distinct unique-colored middles. Its 2p
middles use at most p colors, and at least one color repeats, so at most p-1
middles can be unique. Contradiction. The 2p+1 upper is attained in the
worst case. For p=2 this is exactly the independently checked 16-vertex
counterexample, not a changed graph or an unrelated convenient target.

## 8. Why the remaining incidence hypothesis matters

Dropping the at-most-two-blocks-per-middle condition invalidates this parity
proof even when component diameter stays small. Take a central K_(2,3) and
attach r leaf K_(2,3) blocks at each of two distinct central middles u,v.
Under the same depth-parity rule, pair (0,2) contains the central hub, its
three middles, and r child hubs hanging from each of u,v. It has 2r+4 vertices.
The edge from the center to u separates r+1 from r+3 vertices, giving

    Gamma=(r+1)(r+3)/(2r+4) -> infinity.

The exact cut operation from Section 6 gives a diverging operator inverse
for THIS design. These supports remain width two but have unbounded middle
degree and lie outside C_2. This is not an all-real or all-four-design graph
obstruction. It rejects a specific relaxed incidence invariant and preserves
the distinction between short diameter and controlled branch mass.

## 9. Executable receiving uses and their limits

The actual native receivers are:

| Input | n | m | p | Blocks | Stable queries | Star control queries |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| The original star-four obstruction | 16 | 24 | 2 | 3 | 4 | 5 |
| Unequal, branching complete-bipartite blocks | 27 | 54 | 3 | 4 | 5 | 7 |

Only original n and edge lists are supplied to recognition. The second
receiver exercises the p-parameter, unequal k, branching and another depth;
it is not a larger-size sweep of the first graph and is not called chordless.
Each receiver stores arbitrary rational free diagonals and supported edge
coefficients, every original noiseless action, nonzero rational noise, Y,
output coefficients, projected actions and exact normal equations. The
control uses the SAME D and the SAME absolute noise norm, padding the extra
noise columns with zeros. There is no statistical-performance inference
from these particular noises.

Both noiseless reconstructions are exact. Noisy projected-action residual
is zero exactly and the saved Frobenius errors meet their respective bounds.
A no-producer-import independent gate binds source input hashes, reconstructs
native block structure and color components, and solves independent rational
normal equations rather than importing the producer's subtree decoder.
Its status and costs are recorded separately. This is actual receiving use
of the new theorem; neither receipt nor replay is an application-speedup
claim. The all-size proofs above provide validity beyond the saved examples.

## 10. Cost, prior art, and continuation boundary

For a supplied original edge list, native preparation has O(n+m log m)
comparison work and O(n+m) storage with the current canonical sorts and usual
word-RAM dictionary/set assumptions. Coloring and component certification
are O(nq+m); decoding is O(nq+m) arithmetic/storage. q=p+2 or 2p+1. For a
matrix-action source, all q complete original actions must actually be paid.
The exact explicit-matrix receivers accumulate each edge into its two original
action cells and materialize all nq cells; they do not benchmark a physical
black-box product or claim a one-action speedup. Numerical acquisition,
probe errors, bit complexity and residual verification remain additional.

The first receiver execution failed because a parent-vertex local variable
overwrote p in the shape checker. Its exact failed source and exception are
preserved. Its body costs were not metered and remain unknown; successful
execution does not erase that attempt. All observed bodies, preliminary
projection, independent reviews and other unknown research costs are separated
in COSTS.md. No old closure, scalar-moment calculation, NIST benchmark, or
physical/molecular campaign was rerun.

Star/Hessian direct recovery and acyclic substitution are established prior
machinery. Coleman and Cai's substitution analysis already includes roundoff
bounds; Gebremedhin et al. give recovery algorithms, complexity and stability
analysis. We do not claim that allowing nonstar bichromatic trees, reading
their incidence systems, or saving colors by substitution is new. The
specific new checkpoint claim is the parameterized intrinsic-class separation
between exact-coordinate, uniformly stable-coordinate and star counts, the
degree-independent absolute-noise proof, and the full original-action
operation. A bounded primary comparison has not established historical
priority for this exact theorem. See research/literature/PRIMARY_BOUNDARY.md.

Close universal star-four gluing on the connected chordless target as FALSE,
with the precise 16-vertex witness. Preserve the positive two-connected
Cycle8 theorem and the new one-mark representation/projection. Continue the
owned recovery mission with simultaneous multi-attachment interfaces that
allow controlled nonstar components, rather than seek another star-four
closure contradicted by this support. The next concrete structural question
is whether arbitrary degree-four chordless atoms can be composed with a
bounded weighted branch-mass invariant, analogous to the actual parity reset
proved here. Both cuts and all original actions must remain in that interface.
No theorem about all arbitrary-real four-column designs, the full width-two
class, or the retired NIST/molecular comparison follows from this checkpoint.
