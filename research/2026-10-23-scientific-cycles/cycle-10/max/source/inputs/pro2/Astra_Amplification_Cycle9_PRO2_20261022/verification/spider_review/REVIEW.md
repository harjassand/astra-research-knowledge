# Independent review of the block-spider recovery operation

Reviewer: `/root/cycle8_structural_scope`, Cycle9, 22 October 2026.
Root owns the construction and native implementation. This review targets the
new global component shape, action-noise bound, and scope hypotheses. No old
closure gate or completed scientific suite was run.

## 1. Reviewed contract and verdict

The reviewed nontrivial class consists of finite connected simple graphs with
no bridges, every maximal two-connected block is K_(2,k) for some k>=3, every
cut vertex is a middle (degree-two within-block) vertex in every incident
block, and every vertex belongs to at most two blocks. All edges and diagonal
coefficients of the arbitrary symmetric matrix remain unknown. The graph is
known before selecting unit-row coordinate probes; observations are all
original actions with arbitrary absolute Frobenius noise.

**Verdict:** the proposed four-coordinate coloring, exact incidence-LS inverse,
and uniform squared Frobenius/operator bound 3+sqrt(5) are valid for this whole
class. The stronger five-coordinate star control is valid on the same class.
Neither statement relies on finite depth, bounded block size, or a small
sample. The argument allows unbounded hub degree. For k in {3,4}, the supports
lie inside the owner's original maximum-degree-four width-two class.

The one-vertex edgeless graph is a vacuous edge case if the intrinsic class
is not required to contain a block. It has a trivial one-coordinate diagonal
inverse. The native implementation explicitly treats the nontrivial class
with n>=5; the theorem statement should make the same convention or mention
this isolated exception.

## 2. Exact all-depth component classification

The ordinary block-cut incidence graph is a tree. Each cut vertex belongs to
exactly two blocks, so contract its degree-two incidence node to obtain a tree
T whose vertices are the original blocks. Root T and let d(B) be block depth.
Each block has two intrinsic hubs, given colors 0 and 1 in either consistent
within-block order. Hubs are never shared under the stated hypotheses.

Every unshared middle of B receives 2+(d(B) mod 2). A middle shared between a
parent B and child C receives 2+(d(B) mod 2). This is a well-defined coloring
of actual original vertices. It is proper because edges always join hubs
to middles, and their color sets are disjoint.

Fix h in {0,1} and c in {2,3}. The only potentially nontrivial bichromatic
components use such a pair. In each block of depth parity c-2, its h-colored
hub is a component center. Its incident c-colored middles are precisely all
middles except an incoming shared middle, if one exists:

* An unshared middle terminates an arm of length one.
* A shared outgoing middle connects to the h-colored hub of one child block,
  giving an arm of length two.

That child block has the opposite depth parity. Its sole middle of color c
is the incoming shared middle; all its other middles use the opposite middle
color. Hence the child hub is a leaf of this bichromatic component and cannot
propagate it to a grandchild. A shared middle meets only the two blocks in
question, so it cannot branch into several child hubs.

Thus every edge-containing component is a spider with a unique hub center
and arms of length one or two. Components of pairs {0,1} or {2,3} have no
edges. This is an all-depth reset proved from the actual block tree and
vertex memberships, not a bounded-diameter assertion applied without mass
control. In particular all bichromatic edge components are trees, so the
coordinate action map is injective on supported symmetric matrices with a
free diagonal.

## 3. Uniform incidence bound, including the mean projection

Let T be one such spider, with center o, and let f be any real-valued function
on its vertices. Write its variance as

    Var(f)=sum_v (f(v)-mean(f))^2.

The mean minimizes squared distance to a constant, so

    Var(f) <= sum_v (f(v)-f(o))^2.

Set t=(3+sqrt(5))/2. For a length-two arm, put
x=f(first)-f(o), y=f(leaf)-f(o). Then

    x^2+y^2 <= t [x^2+(y-x)^2].                         (1)

The energy matrix is [[2,-1],[-1,1]], whose eigenvalues are
(3-sqrt(5))/2 and (3+sqrt(5))/2. Alternatively, the quadratic difference
t[x^2+(y-x)^2]-(x^2+y^2) has positive leading coefficient and determinant
t^2-3t+1=0, so it is positive semidefinite. For a length-one arm the same
bound follows from x^2<=t x^2. Summing the disjoint arms proves

    Var(f) <= t sum_edges (f(u)-f(v))^2.                 (2)

Thus the nonzero vertex-Laplacian eigenvalues are at least 1/t. For an
oriented incidence A of this tree, the positive eigenvalues of AA^T and
A^T A agree. Since A has full column rank, its Euclidean least-squares
inverse has squared norm at most t. Signing one color transforms unsigned
incidence to oriented incidence without changing noise norm. Projection
onto mean-zero divergence is orthogonal and contractive.

This is the actual canonical LS decoder's estimate. It does not authorize
discarding the center observation or substituting an unproved anchored
decoder merely because an anchored inequality was used in the proof.

## 4. Original matrix and arbitrary action noise

Own-color action cells contain the arbitrary diagonal coefficients separately.
For each unordered color pair, the off-diagonal coefficients on an edge
component act through its unsigned incidence matrix. These component cells
and the diagonal cells are disjoint. Unused cells may be orthogonally projected
to zero.

For noise E, let e_diag be the resulting diagonal error and w_T the edge-error
vector on component T. Equation (2) gives

    ||w_T||_2^2 <= t ||E_T||_2^2.

The symmetric output duplicates each edge coefficient, so

    ||Dhat-D||F^2
      = ||e_diag||_2^2 + 2 sum_T ||w_T||_2^2
      <= max(1,2t) ||E||F^2
      = (3+sqrt(5)) ||E||F^2.

Operator norm is at most Frobenius norm, establishing the stated uniform
operator bound as well. Every row of X is one coordinate vector, so its
total Euclidean energy is exactly one. All four original actions are used.
The inverse is exact for every noiseless supported real D. No bounded D,
noise distribution, known off-diagonal entry, or smaller action oracle is
introduced.

The Frobenius bound is the appropriate direct estimate here; no optimality
of the resulting operator constant is being claimed. An inexact computed
inverse must still pay its supported projected-action residual, acquisition
and assembly error, and errors in the design itself. Row normalization alone
does not bound D times a design perturbation.

## 5. Matched five-coordinate ordinary control

Give all middle vertices color 4. Give the hubs of even-depth blocks colors
0,1, and the hubs of odd-depth blocks colors 2,3. At a shared middle the four
hub neighbors have four distinct colors. At an unshared middle its two hub
neighbors have two distinct colors. Therefore every middle has at most one
neighbor of any hub color, and every bichromatic edge component is a star
centered at a hub.

The support is triangle-free. The received star-LS inverse therefore gives
operator constant sqrt(3/2) and Frobenius constant sqrt(2), uniformly in the
same graph family and with the same absolute noise convention. The extra
query is charged. The four-coordinate theorem saves one action but has a
weaker uniform noise bound; neither automatically dominates total physical
or computational cost.

## 6. Which hypotheses do real work

### 6.1 At most two blocks at a shared middle

This condition is essential to the proposed rule's uniform guarantee, not
merely to a convenient proof drawing. To see the failure of its natural
extension, take a root K_(2,t), t>=3, and choose one of its middles v. Identify
v with one middle of each of t-1 child K_(2,3) blocks. All other vertices are
distinct. Root the block-cut tree at the root block and assign v its parent
block's middle color, with all other vertices colored by the same parity
rule. Only the block-membership-at-most-two hypothesis has been dropped.

For either hub color h, the (h,2) component is a balanced double-star: one
center is the root h-hub and the other is v; each has t-1 leaf neighbors.
Deleting the central edge splits the component into t vertices on each side.
Put coefficient 1 on that central edge, -1/t on every leaf edge of this
component, and zero elsewhere in the original supported matrix. Then

    ||DX||F^2 = 2/t,     ||D||op >= 1.

Indeed every one of the 2t component action cells has absolute value 1/t,
and the central matrix entry has absolute value one. Any exact inverse for
this specified design has operator noise constant at least sqrt(t/2).
The divergence is real and dimension-dependent. It does not prove that
these larger graphs defeat every other four-query design.

### 6.2 Middle-only shared vertices

This makes the hub/middle roles globally disjoint and makes each shared
middle contribute exactly one hub neighbor of each hub color in each of
its two blocks. Without it, even well-definedness can fail: identifying a
hub of one K_(2,3) with a middle of another would require that same vertex
to have both a hub color and a middle color under the literal rule. Some
more restricted hub-sharing variants might admit another proof; they are
not covered or ruled out here.

### 6.3 k>=3, no bridges, and actual maximal blocks

k>=3 makes the two hubs intrinsically identifiable by their within-block
degrees. The component argument itself would also work with supplied valid
roles for some k=2 cases, but the current intrinsic theorem does not assert
that extension. Bridge attachments require an additional coloring rule and
cannot be silently treated as already proved. Finally the input objects must
be the actual maximal blocks with their real intersections, not overlapping
local pieces whose claimed tree misses other graph edges.

## 7. Implementation inspection and one required cost correction

Read `src/block_spider_recovery.py` and the inherited `src/coordinate_decoder.py`.
The iterative low-link extraction, actual K_(2,k) adjacency validation,
membership checks, native graph coloring, whole-component shape certification,
and mean-projected incidence decoder match the mathematical construction.

The first inspected version checked membership with

    v not in blocks[i]['middles']

where `middles` was a list, once for every cut vertex. For a block with k
shared middles, this can cost Theta(k^2), contradicting the claimed
O(n+m log m) work in the unbounded-degree theorem. Root was notified to cache
a middle set per block (or record roles during extraction). The subsequently
inspected generalized implementation now constructs `middle_sets` once and
uses those sets at both sides of every shared vertex. That correction is
present and the stated sorting-dominated cost is accepted for this step.
It must be preserved. This correction concerns actual total preparation cost,
not the proof of the uniform inverse. Exact inspected bytes are pinned in
`SOURCE_BINDINGS.json`.

The following independent diagnostic uses no producer imports and checks
newly built block-tree colors/components and the lost-hypothesis witness.
Its finite outputs supplement this proof; they do not prove all-depth closure
or replace the root's full-action receiving calculations.

## 8. Parameterized receiving theorem: K_(p,k) blocks

The root subsequently proposed the following direct generalization. Fix an
integer p>=2. Every actual block is K_(p,k_B), where k_B>=p+1; its p hubs
have within-block degree k_B and its k_B middles have degree p. Only middles
are shared, and each belongs to at most two blocks. The common p, role
partition, and degree inequalities must be validated from the native input.

**Parameterized verdict: accepted.** Give the p hubs of each block the p
distinct colors 0,...,p-1. Give middles the parent/own depth-parity colors
p,p+1 as before. For each hub color h and middle color c the entire proof in
Sections 2-4 is unchanged: one hub of color h per block, length-one/two arms,
and no further propagation. There are more disjoint information components,
but their uniform inverse bound does not add across noise channels. Therefore

    q=p+2,
    ||error||F <= sqrt(3+sqrt(5)) ||E||F,
    ||error||op <= sqrt(3+sqrt(5)) ||E||F,

with a constant independent of p, every k_B, depth, and graph size.

The matched star control uses q=2p+1: even-depth hubs get colors 0,...,p-1,
odd-depth hubs p,...,2p-1, and every middle gets 2p. Every middle then has
at most one neighbor of each hub color, so the control remains star with
operator constant sqrt(3/2) and Frobenius constant sqrt(2).

Every block has a width-p decomposition with bags consisting of all p hubs
and one middle; joining block decompositions through their actual shared
middle gives treewidth at most p. For p=2 and k_B in {3,4}, the original
treewidth-two degree-four recovery contract is retained exactly. Larger p
is an explicitly stated structural generalization, not a hidden change to
that original target. For p>=3 these supports need not be chordless: a
K_(3,3) subgraph has a six-cycle with chords. Triangle-freeness, sufficient
for the star-control operator bound, is preserved. Do not inherit the word
“chordless” into the general-p theorem.

## 9. Exact worst-case star requirement in the parameterized class

Take a central K_(p,2p), and attach p further K_(p,2p) blocks at p distinct
middle vertices of the central block. Each attachment identifies only that
one middle; all other vertices are disjoint. The graph has

    n=3p^2+2p,  m=2p^2(p+1),  maximum degree=2p,  treewidth<=p.

It belongs to the parameterized class. Suppose it has a star coloring with
at most 2p colors. In any one block, if two hubs share a color, every pair
of equally colored middles would give a bichromatic four-cycle and hence
a bichromatic P4. Its 2p middles would all need distinct colors, plus at
least one different hub color. That requires 2p+1 colors, a contradiction.
Thus all p hubs have distinct colors in every block. Each block's middles
use at most the p remaining colors.

At a middle v, its neighbor support N consists of those p hub colors. If
its middle color is repeated anywhere else in the block, every hub has
another neighbor of color c(v), so F=N. If its color is unique, F is empty.
For a shared middle, the two incident p-element neighbor supports lie in
the universe of at most 2p-1 colors different from c(v). They must intersect.
If either side's middle color is repeated, the intersection is flagged and
creates a bichromatic P4 across the join. Both sides must therefore give
this shared middle a unique middle color within their block.

All p marked middles of the central block would consequently have to have
unique colors there. But among 2p vertices colored with at most p colors,
at most p-1 vertices have a color occurring only once: at least one used
color must be repeated, and there are at most p used colors. Contradiction.

The star control in Section 8 uses 2p+1 colors on every graph in the class,
so this finite graph has star chromatic number exactly 2p+1 and the
worst-case star requirement of the entire class is exactly 2p+1. This is
an all-coloring statement, not a counterexample to one chosen palette.

## 10. Uniform unit-coordinate stable minimum is exactly p+2

The lower claim must explicitly mean **unit-coordinate designs** X_v=e_c(v).
It does not apply automatically to signed/scaled coordinate rows or general
real-valued designs. Under that exact representation, the proposed sharpness
argument is valid.

First, exactness with free diagonal requires properness. A monochromatic
edge uv has the nonzero action kernel D_uv=D_vu=1, D_uu=D_vv=-1, with all
other coefficients zero. Exactness also excludes a bichromatic cycle: put
alternating edge weights around that even cycle and zero elsewhere.

In a proper coloring of K_(p,k), the hub and middle color sets are disjoint.
If both sides repeat a color, they form a bichromatic four-cycle. Therefore
one side must have all vertices differently colored. With q=p+1 and
k>=p+1, it cannot be the middle side, which would already use at least p+1
colors in addition to a hub color. Hence the p hubs have all distinct colors
and every middle uses the one remaining color. For q<=p even exact recovery
is impossible by the same argument.

In a connected block tree, the shared middle's color identifies that one
remaining color in both incident blocks. Thus all middles of the whole
graph have a single common color c, and each block has one hub of every
other color. Palette permutations within blocks cannot avoid this conclusion.

Now choose, before any design, a path of N=2r K_(p,2p) blocks, joined at
distinct middle vertices. For every exact q=p+1 unit-coordinate design and
every hub color h, the (h,c) component has 4pr+1 vertices. It consists of
one h-hub per block, shared middles linking successive hubs, and the other
middles as leaves. An edge adjacent to the central shared middle splits
it into

    a=2pr,  b=2pr+1.

The inherited exact cut-flow witness therefore gives

    inverse_operator_constant^2 >= ab/(a+b)
        = (2pr)(2pr+1)/(4pr+1) >= pr.

Equivalently, choose signed divergence 1/a and -1/b on the two sides,
recover the unique tree flow, and set all other supported coefficients to
zero. The cut coefficient has absolute value one and the full action norm
squared is 1/a+1/b, so the operator-norm ratio has the displayed lower bound.
This grows without bound for each fixed p. The graph is chosen before the
coloring, and the forced-color proof covers every admitted exact unit-
coordinate design; this is not a single-seed failure.

Together with Section 8, the worst-case dimension-independent stable
unit-coordinate query minimum for this class is exactly p+2. The full
arbitrary-real question remains distinct. In particular, this result does
not replace the original all-real upper/lower comparison for all width-two
degree-four supports.

### 10.1 Received extension to signed, unequal coordinate row amplitudes

The focused port contributor subsequently supplied a congruence argument
extending this lower beyond unit rows. This reviewer read and independently
checked the actual source
`research/root_gluing/PARAMETERIZED_SEPARATION_REVIEW.md` and the corresponding
section of `PARITY_AND_CUT_REVIEW.md`. The following is the complete argument.

Let X=W C, where C is a unit-coordinate design and W is diagonal with real
entries w_v satisfying |w_v|<=1. If any w_v=0, the free diagonal coefficient
D_vv is invisible, so exact recovery already fails. Otherwise W is invertible
and alpha=min_v |w_v| is positive. Exact properness and acyclicity requirements
still hold: any unit-coordinate kernel H transforms into the supported
symmetric kernel D=W^{-1} H W^{-1}, since DX=W^{-1}HC.

Thus with p+1 columns the same forced unit-color topology applies. Let H
be its exact cut witness on the block path, normalized to have cut entry
H_ab=1 and ||HC||F=1/sqrt(Gamma). Set D=W^{-1} H W^{-1}. Then

    ||DX||F = ||W^{-1}HC||F <= alpha^{-1}/sqrt(Gamma),
    ||D||op >= |D_ab| = 1/|w_a w_b| >= 1.

This gives inverse constant rho>=alpha sqrt(Gamma). Independently, a unit
diagonal coefficient at a minimum-amplitude row gives rho>=alpha^{-1}.
Consequently

    rho >= max(alpha^{-1}, alpha sqrt(Gamma)) >= Gamma^(1/4).

The lower diverges with the block-path length for every admitted choice of
amplitudes, even when those amplitudes depend on the whole graph. The p+2
upper uses unit amplitudes and therefore remains in this larger class.
Accordingly the uniformly stable minimum is exactly p+2 for **single-nonzero-
coordinate-per-row designs, including real signs and unequal row amplitudes**.
The unit-row lower sqrt(Gamma) and weighted-row lower Gamma^(1/4) must remain
distinct. Neither is an all-dense-real-design lower.

## 11. Parameter-dependent costs and interpretation

The q=p+2 construction saves p-1 actions relative to the exact worst-case
star control q=2p+1, while paying the weaker uniform noise constant. All
q original matrix actions and all nq observation cells are charged. In this
particular class every vertex has degree at least p, so pn<=2m; consequently
n(p+2)=O(m) for p>=2, but this does not make the action acquisition free.
Arithmetic and bit costs, sparse output, canonical sorting, and residual
verification remain separate.

The parameterized claims follow from the same all-size component and
counting arguments. No larger benchmark, numerical parameter sweep, or old
gate is needed to prove them. Historical priority, external acceptance, and
physical performance are not established by these internal arguments.
