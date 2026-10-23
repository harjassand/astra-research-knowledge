# Sharp uniform stable query complexity at bounded treewidth

Astra PRO 2, 22 October 2026 (Australia/Brisbane).

## 1. Exact model and principal theorem

For a finite simple graph G, let S_G be the real symmetric matrices supported
on its edges and all diagonal positions. A q-column query block X obeys
||X[i,:]||_2 <= 1 for every vertex. The cap is total row energy across all
queries. Observations are Y=DX+E; E is arbitrary and its norm is the absolute
Frobenius norm. Recovery error is operator norm. Define

    C_2(G,X) = sup_{0 != D in S_G} ||D||_2 / ||DX||_F,

with infinity when there is a nonzero kernel.

For each fixed integer t>=0, put K_t=(t+1)(t+2)/2.

**Theorem.** The minimum fixed query count for a dimension-independent stable
recovery guarantee over all known graphs of treewidth at most t is K_t.
The guarantee allows a constant depending on t but not on graph size, graph,
unknown coefficients, or action noise. More precisely:

1. K_t coordinate queries admit a linear decoder with
   ||Dhat-D||_2 <= ||Dhat-D||_F <= sqrt(2)||E||_F.
2. For every R>=1 there is an explicitly specified finite graph G_t(R), of
   treewidth at most t, for which EVERY capped (K_t-1)-column real X has
   C_2(G_t(R),X)>=R. Thus arbitrary graph-adapted dense designs, and nonlinear
   decoders, cannot lower this uniform budget.
3. The worst-case exact-identification minimum is only t+1.

The upper theorem uses the classical star-color bound of Fertin--Raspaud--Reed,
as proved by Albertson et al. [A, Theorem 6.1], and classical direct symmetric
recovery [B]. The new lower proof is self-contained. Its two operations are
coning with exact apex-action cancellation and covariance-based branching.
It does not depend logically on the previous path or fan obstruction, although
those results and the failed frame construction led to it. Historical priority
of the lower theorem has not been established by the bounded literature search.

The selected trees-of-fans question also has a more economical separate
quantitative negative result in Section 7. That result DOES use the inherited
three-query fan theorem. Do not confuse its family or dependency with the
general induction.

## 2. Uniform decoder necessity and elementary exact identification

Suppose a decoder satisfies ||R_X(DX+E)-D||_2 <= C||E||_F for every D in S_G
and every E. It recovers noiseless data exactly. Evaluating the same observed
DX both as noiseless D and as noise DX at zero implies
||D||_2 <= C||DX||_F. Thus C>=C_2(G,X), without assuming decoder linearity.
Fewer queries can be padded with zero columns without changing the row cap.

A graph of treewidth t is t-degenerate. Choose an n-by-(t+1) block for which
every collection of at most t+1 rows is linearly independent, then scale each
row to meet the cap. At a current vertex of degree at most t,
its action is a linear combination of at most t neighbor rows and its own
row. Solve exactly for those coefficients, use symmetry to subtract the known
column contributions, and delete the vertex. Induction identifies D exactly.
On a clique of size t+1, fewer queries leave a nonzero vector w with w^T X=0;
ww^T is a supported symmetric kernel. This proves the exact count. The
elimination argument carries no uniform conditioning estimate.

## 3. Coning lemma: one extra query and one extra treewidth

Call H (k,epsilon)-bad when, for every capped k-column Z, there exists a
supported B with ||B||_2=1 and ||BZ||_F<=epsilon. This includes epsilon=0.
Finite-dimensional compactness supplies such normalized witnesses from the
corresponding inverse bound; no supremum-attainment gap is hidden.

**Lemma 1.** If H is (k,epsilon)-bad, add a single universal apex to k+1
disjoint copies of H. The resulting cone C is
(k+1,sqrt(k+1) epsilon)-bad, and tw(C)<=tw(H)+1.

**Proof.** Fix ANY capped (k+1)-column X on C. If its apex row is zero, the
apex diagonal is an exact kernel. Otherwise rotate query coordinates
orthogonally to write the apex row as (0,a), a>0, and all other rows as
[Z,V]. Split these rows among the k+1 copies and put R=V/a. Projection keeps
each row of Z capped. Choose on each copy a symmetric B_j of operator norm
one with ||B_j Z_j||_F<=epsilon.

The k-vector sum sum_j c_j R_j^T B_j Z_j imposes at most k homogeneous
linear equations on k+1 coefficients. Choose a nonzero solution c and scale
so max_j|c_j|=1. Set B=diag(c_j B_j). Then ||B||_2=1 and
||BZ||_F^2<= (k+1)epsilon^2. With L=[-R^T; I], form

    D=L B L^T = [[R^T B R, -R^T B],[-B R,B]].

All border entries are allowed because the apex is universal; the bottom
block stays inside the disjoint copies. B is principal, so ||D||_2>=1.
Moreover L^T X=[Z,0] and the chosen coefficients give

    DX = [[0,0],[BZ,0]].

Dividing D by its operator norm proves the lemma. No norm of R, a^{-1},
or L is paid: their action is canceled exactly. k=0 is included: the empty
system on one coefficient produces an edge with a one-query kernel from a
one-vertex zero-query kernel. For treewidth, append the new apex to every
bag of a width-tw(H) decomposition of each copy and connect those trees.
QED.

This is a mathematical construction on exact reals. Finding the coefficients,
normalizing the operator, and certifying arithmetic on a supplied input are
not assumed costless numerical subroutines.

## 4. Branching lemma: covariance either compresses a child or cancels a core

Let a root graph R_0 have n_0 vertices, partitioned into A (unattached vertices)
and P (attachment vertices). For each v in P attach N disjoint copies of the
same cone C by identifying its universal apex with v. All nonapex vertices of
a copy are new. Suppose C is (h,a)-bad, q>=h>=1, and

    dim S_(R_0) > q|A| + (q-h)|P|.                         (1)

For any threshold L>0 and ANY capped q-column X on the assembled graph,

    C_2(G,X) >= min( 1/[a+sqrt((q-h+1)L/N)], sqrt(L/n_0) ). (2)

**Proof.** For v in P let W_v contain all nonapex query rows in its N copies,
and let A_v=W_v^T W_v. Eigenvalues are in decreasing order.

LOW CASE: Some lambda_h(A_v)<=L. Let U be a top-(h-1) eigenspace; when h=1
it is the zero space. The squared Frobenius residual after projection to U
is the sum of q-h+1 trailing eigenvalues, at most (q-h+1)L. One of the N
copies therefore has residual at most sqrt((q-h+1)L/N). Project every row
of that chosen copy onto U+span{x_v}. This is an orthogonal projection into
dimension at most h; it leaves the apex row unchanged, decreases row norms,
and can only reduce the residual compared with projection onto U.

After an orthogonal identification with R^h (padding zeros as needed), the
child hypothesis gives a supported norm-one D with projected action at most
a. The true-action perturbation is bounded by

    ||D(X-Xtilde)||_F <= ||D||_2 ||X-Xtilde||_F.

Embed D into the full graph. Its action outside the chosen child is zero,
because its nonzero matrix columns and rows are confined to that child.
Its apex action is allowed to be nonzero and has been counted. We obtain
action at most a+sqrt((q-h+1)L/N), proving the first alternative. Repeated
eigenvalues and deficient rank cause no problem; any appropriate invariant
subspace works.

HIGH CASE: Every lambda_h(A_v)>L. Let U_v be a top-h eigenspace. Require a
root-supported symmetric B to satisfy (BX_0)_u=0 for u in A and
(BX_0)_v in U_v for v in P. There are at most q|A|+(q-h)|P| linear scalar
constraints. By (1) a nonzero B exists. Normalize ||B||_2=1. Write
b_v=(BX_0)_v and use the least-norm row coefficients

    c_v = -W_v A_v^+ b_v^T.

They satisfy c_v^T W_v=-b_v and
||c_v||_2^2 = b_v A_v^+ b_v^T <= ||b_v||_2^2/L.
Retain B on the root and place these coefficients on the spokes from v to
its child vertices; put zero on every other new matrix entry. These spokes
are all permitted because EACH CHILD APEX IS UNIVERSAL.

Every root action cancels exactly. A new vertex i incident to its assigned
coefficient c_i has action c_i x_v, so total action squared is at most

    sum_v ||c_v||_2^2 <= ||B X_0||_F^2/L <= n_0/L.

The last step uses ||B||_2=1 and ||X_0||_F^2<=n_0. The full D has B as a
principal submatrix, hence operator norm at least one. This proves the high
alternative and (2). All covariance/subspace choices are made after fixing
X; the graph and its parameters are fixed before X. QED.

The cone hypothesis is essential. One cannot reuse an arbitrary rooted bad
graph as this child: cancellation would create edges to nonneighbors. In
particular, naively iterating the fan-tree lower bound without adding a new
universal apex would falsely contradict the six-query upper bound. Lemma 1
creates the missing spokes and explicitly pays one treewidth increase.

## 5. Sharp treewidth induction, with explicit finite graph sizes

It suffices to construct, for every integer R>=1, a graph G_t(R) that is
(K_t-1,1/R)-bad. Start with G_0(R) consisting of one vertex. Zero queries
give zero action, so this base is exact and self-contained.
For a real target R>=1 use the graph G_t(ceil(R)).

For t>=1 assume the construction at t-1. Define

    h=K_(t-1)=t(t+1)/2,   q=h+t=K_t-1,   s=t-1,
    m=q(t-1)-t(t-1)/2+2 = t(t-1)(t+2)/2+2,
    n_0=m+s=1+t^2(t+1)/2.

Take H=G_(t-1)(2hR) and apply Lemma 1 to h disjoint copies, producing a cone
C of treewidth at most t. It is (h,a)-bad with

    a <= sqrt(h)/(2hR) <= 1/(2R).

Use root R_0=K_(t-1) join P_m; A is its (t-1)-vertex clique, and P is its
m path vertices. The root has width t via consecutive bags consisting of
the clique plus a path edge. Its symmetric support dimension is

    d=(t+1)m+t(t-1)/2-1.

The high-case constraints number at most q(t-1)+(q-h)m=q(t-1)+tm. The
difference is exactly one, by the definition of m. This includes t=1:
the root is an edge with three symmetric coefficients and two constraints.

Attach N copies of C at each root path vertex, with

    L=n_0 R^2,     N=4(t+1)n_0 R^4.

All these integers and the entire graph are chosen before X. In (2),
q-h+1=t+1, so the low action is at most 1/(2R)+1/(2R)=1/R and the high
action is at most 1/R. Thus G_t(R) has the claimed all-design obstruction.
Vertex sums at one vertex preserve the maximum treewidth: connect bags
containing the common vertex in the root and child decompositions.

For every fixed t, R can grow without bound; no uniform constant works at
q=K_t-1. The graphs may even be taken chordal: paths, joins with cliques,
cones, disjoint unions and one-vertex sums in this construction preserve
chordality. For t>=2 the assembled graph has diameter at most four, since
all new vertices meet their universal anchor and any two root path vertices
have distance at most two. t=1 gives double stars of diameter at most three.
Degree grows; no bounded-degree lower theorem is claimed.

Let n_t(R)=|V(G_t(R))|. The actual recurrence is

    n_0(R)=1,
    n_t(R)=n_0 + m [4(t+1)n_0 R^4] h n_(t-1)(2hR).

For t>=1, n_t(R)=O_t(R^(4t)). This gives a size-dependent obstruction
of order n^(1/(4t)) along this explicit family, with t-dependent constants;
the exponent and finite-size constants are not asserted optimal. The constants
are very large: n_1(1)=34 and n_2(1)=62,708,695. These huge universal examples
are specified symbolically, not materialized in the computation. Their graph
construction and witness search are not claimed to be practical algorithms.

## 6. Classical matching upper bound

Every graph of treewidth at most t has a star coloring with at most K_t colors
[A]. A star coloring is proper and each two-color induced graph is a disjoint
union of stars. Give vertex v the coordinate vector of its color. All row
norms equal one. Each diagonal appears alone in its own-color reading. Each
edge is isolated at a leaf endpoint of its bichromatic star. Select one such
endpoint per edge; all selected cells are distinct. Copy its reading into
both symmetric output positions and set nonedges to zero. For arbitrary E,

    ||Dhat-D||_F^2 <= 2 ||E||_F^2,

so the operator bound follows. This proves the upper count using an established
construction. Computing a tree decomposition or suitable coloring, generating
the action block, all K_t matrix actions, and subsequent processing are
additional operations; none is free in an implementation comparison.

## 7. The original selected question: a shallow tree of ordinary fans

For the more restrictive fan-tree family, take a root F_6 (one apex joined
to a six-vertex path). At each of its six path vertices attach N ordinary
fans F_M, identifying only the apex. This is an allowed tree of fan blocks,
with just one attachment generation. It is outerplanar, has treewidth two,
and n=7+6NM. Its maximum degree is unbounded.

The inherited all-design three-query fan theorem gives (3,a_M)-bad children,
where a_M<=sqrt(3*pi) M^(-1/4), for M>=4. Root support dimension is18.
For q=5 and h=3 the high constraints number5+6*2=17. Lemma2 yields

    C_2 >= min(1/[a_M+sqrt(3L/N)], sqrt(L/7)).

With N=M=k>=4 and L=sqrt(k),

    C_2 >= k^(1/4)/(sqrt(3*pi)+sqrt(3)),   n=7+6k^2.

The denominator also exceeds sqrt(7), so it bounds both alternatives.
Therefore FIVE directions do not give uniform stable recovery on the selected
family; SIX are necessary and sufficient. Long attachment depth is not needed.
This settles the chosen question by an all-design argument, not a bad palette
or failure of one decoder. The inherited sine bound and its separate weaker
rational tent executable remain distinct.

## 8. Adaptive scope, error, implementation and significance

The lower bound also excludes deterministic adaptive q-query recovery with
the same uniform adversarial-noise guarantee and total row cap. Run it on
noiseless zero and collect X. Choose the adverse D for this realized X.
For input D, at each step feed error -Dx_j; by induction observations and
future queries remain the same zero transcript. The output is zero, and the
same inverse ratio is necessary. This is not a fixed-input randomized minimax
theorem, and it says nothing about algorithms with full-entry access.

The proof's low branch explicitly bridges the projected matrix to the ACTUAL
X by ||D DeltaX||_F<=||D||_2||DeltaX||_F. No theorem for a rounded/low-rank
surrogate is substituted without this allowance. Exact executable examples
use Fraction arithmetic, explicit support and actual DX. Floating arithmetic
would require certified additional error in projections, nullspaces, solves
and recovered coefficients. The old input-error bridge remains unchanged.

The new mathematical consequence is a quadratic-versus-linear separation:
the worst-case exact query requirement is t+1, but a uniform worst-case noise
guarantee costs (t+1)(t+2)/2. Dense real directions and nonlinear recovery do
not improve the classical worst-case color count in this contract. This does
not imply that every individual graph requires its star chromatic number,
that ordinary noisy instances are this difficult, or that any practical
spectral benchmark has been accelerated. No universal optimal divergence rate
is established. The prior NIST and molecular stopping decisions stand.

## References and dependencies

[A] Albertson, Chappell, Kierstead, Kundgen, Ramamurthi, *Coloring with no
2-colored P4's*, EJC11 (2004), R26, Theorem6.1; gives a proof of the
Fertin--Raspaud--Reed treewidth star-color bound.
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/

[B] Gebremedhin, Tarafdar, Pothen, Walther, *Efficient Computation of Sparse
Hessians Using Coloring and Automatic Differentiation*, INFORMS J. Computing
21(2) (2009),209--223. https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

The clique/path/recursive-attachment architecture also has a classical
predecessor in [A, Theorem6.3], which proves sharpness for star coloring.
That coloring obstruction does not itself cover arbitrary dense query rows.
The lower theorem here uses covariance rank and exact action cancellation
to establish the stronger noisy-recovery quantifier; historical priority for
that strengthening remains unestablished.

The exact-query degeneracy proof is supplied above. The general lower theorem
depends on no inherited numerical calculation or old path lower bound. The
special Section7 fan-tree rate depends on the accepted incoming fan proof,
preserved inside the unchanged Cycle2 source. Scoped independent reviews of
the two new load-bearing lemmas are under notes/. Numerical diagnostics are
supplementary and do not supply the universal quantifiers.
