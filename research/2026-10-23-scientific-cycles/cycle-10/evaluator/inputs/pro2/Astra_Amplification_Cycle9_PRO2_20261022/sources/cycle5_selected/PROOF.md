# Cut balance, stable operator recovery, and controlled triangle-strip extension

PRO 2, Cycle5, 22 October 2026 Australia/Brisbane.

The full four-versus-five question on treewidth at most two and maximum degree
at most four is still open in this source. The new results are a degree-free
information criterion for proper coordinate designs and a structural reduction
of the remaining four-color existence problem. No historical priority or
application speedup is asserted.

## 1. Exact model

G is a known finite simple graph, n>=1. S_G is the real vector space of all
symmetric n-by-n matrices whose off-diagonal support is contained in G;
diagonal entries are unrestricted. The graph is known before choosing X.
Each row of X has total Euclidean norm at most one. Observe Y=DX+E, with
arbitrary absolute Frobenius action noise E. The output error is operator norm.

The results below concern proper coordinate designs X_v=e_{c(v)} with q colors.
Their row norm is exactly one. Unless explicitly stated otherwise, a lower
bound is for this specified design, not every graph-adapted real q-column X.
Let r=max_v number of distinct neighbor colors, so r<=q-1. Put

    rho(G,c)=sup_{0!=D in S_G} ||D||op/||DX||F.

## 2. The new degree-free criterion

If a bichromatic component has a cycle, alternating edge coefficients around
that even cycle give a nonzero supported symmetric D with DX=0. Otherwise all
edge-containing bichromatic components T are trees. For an edge e in T, its
deletion splits T into a_e,b_e vertices, N_T=a_e+b_e. Define

    Gamma=max_(T,e) a_e b_e/N_T,
    M=max_(T,e) min(a_e,b_e),

both zero for an edgeless graph. Let L be the exact mean-projected incidence
decoder described below. Then

    max(1,sqrt(Gamma)) <= rho(G,c) = ||L||_(F->op)
        <= sqrt(1+4 r M) <= sqrt(1+8 r Gamma).                 (1)

For families with bounded r, in particular fixed q, uniform coordinate
stability is therefore equivalent to two conditions: all bichromatic
components are trees, and Gamma is uniformly bounded. **No maximum-degree
hypothesis is required.** The criterion permits arbitrarily many small
branches at one centroid; it excludes a large balanced cut. With bounded
degree it recovers the previous bounded-component-size criterion.

### 2.1 Decoder and orthogonal information blocks

Own-color cells give D_vv. For each unordered color pair, its component's
edge weights w act through the unsigned incidence matrix B_T. Distinct tree
components and diagonal channels occupy disjoint action cells. Give one color
sign +1 and the other -1, denoted sigma_v. Signing turns B_T into an oriented
incidence A_T. Its range is exactly the mean-zero subspace.

For signed observations f, subtract the mean. Root T at a centroid. If edge
e has child v and child subtree S_e of size a_e, recover

    w_hat_e=sigma_v [sum_(u in S_e) f_u-(a_e/N_T) sum_(u in T) f_u].       (2)

This is the least-squares incidence inverse. Centroids, subtree sizes and
all sums take linear arithmetic work. The action projection P keeps diagonal
channels, sign/mean-projects tree channels and zeros unused cells. It is the
orthogonal projection onto range(D->DX), and L=A^{-1}P.

Consequently ||L||<=rho. Conversely take E=DX, obtaining L(E)=D; hence
||L||=rho. Any exact decoder, including a nonlinear one, has worst noise
constant at least rho: true D and noise -DX yield the zero observation, whose
exact noiseless output must be zero. Thus the canonical linear decoder is
minimax-optimal for this fixed design. Formula (1) bounds that optimum; it
does not claim the upper expression is its exact numerical value.

### 2.2 Lower bound and geometry

For a cut A,B of sizes a,b, prescribe signed divergence 1/a on A and -1/b
on B. Its sum is zero. The unique tree flow has cut coefficient of absolute
value one, while its squared action norm is 1/a+1/b. Thus ||D||op>=1 and
rho>=sqrt(ab/(a+b)). A single diagonal coefficient supplies rho>=1.
The same two-point argument works about any D0 in the unrestricted linear
space, so this is an information obstruction, not a solver defect.

At a centroid all child subtrees have size at most N/2. These are the smaller
sides of their cuts. The largest such subtree is a centroid branch. Since
a/2<=a(1-a/N)<=a for a<=N/2, Gamma<=M<=2Gamma. In a single component,
Gamma_T=M_T(1-M_T/N_T). Thus bounded Gamma means precisely that every tree
has a centroid whose branches have bounded order. Their number may be unbounded.

### 2.3 Local covariance and the operator upper bound

For a child edge let h_e=1_(S_e)-(a_e/N)1. Its error in (2), up to sign, is
<h_e,f>. Child subtrees at one parent are disjoint, so their Gram matrix is

    ( <h_e,h_f> ) = diag(a)-aa^T/N <= diag(a) <= M_T I.        (3)

Therefore the sum of squared child-edge errors at one vertex in this tree
is at most M_T ||E_T||^2. Across color pairs the selected noise cells are
disjoint. Orient all edges away from their component centroids, and let U
contain the resulting oriented errors. Then

    max_i sum_j |U_ij|^2 <= M ||E_off||F^2.                  (4)

Every column of U has at most r entries: at most one parent for each neighbor
color. By Cauchy-Schwarz, for any z,

    ||U^T z||^2 <= r sum_i |z_i|^2 sum_j |U_ij|^2.

Hence ||U+U^T||op<=2sqrt(rM)||E_off||F. Diagonal errors have norm at most
||E_diag||F and use disjoint channels. A final Cauchy-Schwarz inequality
gives sqrt(1+4rM)||E||F, proving (1). Actual maximum column count r0 of the
chosen orientations can replace r; the executable certifier reports r0.

This is a direct operator estimate. A Frobenius output bound can be much
worse, as Section3 proves on the exact same design. No uncharged dimension
conversion or stochastic-noise assumption occurs.

## 3. An operation and a separation between output norms

Supply a tree consisting of a hub and any number of disjoint arms, each with
at most L edges. Its proper bipartite coordinate design uses two actions.
Every edge cuts off a terminal segment of one arm, so M<=L. Equations(1)-(2)
give

    ||Dhat-D||op <= sqrt(1+4L)||E||F,                        (5)

independently of the number of arms and maximum degree. This is also the
optimal stable query count for every fixed-L class containing an edge:
one query has n outputs for n+m free coefficients, so it cannot be injective.

Two equal arms of length L form P_(2L+1), whose middle cut has Gamma=
L(L+1)/(2L+1). Thus the worst operator inverse constant in this support class
is Theta(sqrt L). The ordinary depth-mod-three forest design uses three
actions with Frobenius/operator constant sqrt2 independent of L; it remains
the better conditioning comparator. Two actions do not imply a runtime win.

There is an exact norm-separation witness. Select two equal arms and order
their joined path vertices 0,...,2L. On edge j (j=1,...,2L), put

    w_j=(-1)^(j-1) min(j,2L+1-j),

all other entries zero, including the diagonal. Internal action entries have
absolute value one except the middle one, which is zero; the two endpoints
also have absolute value one. Hence

    ||DX||F^2=2L,
    ||D||F^2=4 sum_(j=1)^L j^2,
    ||D||F^2/||DX||F^2=(L+1)(2L+1)/3.                       (6)

Any exact decoder's Frobenius-output noise constant is at least the square
root of (6), of order L. But its optimal operator-output constant is of order
sqrt L by (5) and the cut lower. Thus replacing the requested output norm by
Frobenius norm can introduce a provably unnecessary factor sqrt L.

The saved receiving use has 33 arms of length12: n=397, degree33, q=2,
Gamma=4620/397, M=12, and certified operator constant7. On the same graph
and same design, (6) gives a Frobenius inverse lower sqrt(325/3)>10.4.
These exact rational statements demonstrate an actual difference between
the guarantees, not a fitted eigenvalue or new claim about the full Delta4 class.

## 4. Why local stable pieces do not automatically compose

Join two hubs by an edge and give each hub t leaves. Properly two-color this
double-star. Set its central edge to1, every leaf edge to -1/(t+1), and every
diagonal to zero. All action entries have magnitude1/(t+1), giving

    n=2t+2, diameter=3,
    ||DX||F^2=2/(t+1), ||D||op>=1,
    Gamma=(t+1)/2, rho>=sqrt((t+1)/2).                      (7)

The individual star pieces have bounded inverse constants, yet their joined
coordinate system has a large balanced cut. Bounded diameter, a bounded
number of pieces and local conditioning do not imply global conditioning.
The growing family has unbounded degree and is a specified-coordinate
obstruction; it is neither a Delta4 obstruction nor an all-real-design lower.

## 5. A transfer lemma for controlled local replacements

This lemma states the global obligation needed when inserting local pieces.
Fix a proper acyclic coloring of a base graph R. Suppose that, for every
color pair, the final graph is obtained from its base bichromatic forest by
attaching rooted trees at old vertices, and by adding detached trees. Assume:

New vertices of the attached trees are disjoint except for a shared old root.
Equivalently, after deleting old edges, every new-edge component is a tree
containing at most one old vertex. This excludes hidden overlapping pieces.

1. Each old vertex is the root of at most A new vertices in total for this
   color pair (possibly spread over several attached trees).
2. Every detached tree has at most B vertices.

No new edge joins distinct old components; no attachment meets the old forest
at two different vertices. Put W=1+A. Then the final coloring is acyclic and

    Gamma_final <= max(W Gamma_R, A, B/4).                 (8)

For an old edge splitting an old tree into a,b vertices, its new side sizes
a',b' satisfy a<=a'<=Wa and b<=b'<=Wb. The function xy/(x+y) is increasing
in each positive variable, so its new cut mass is at most W ab/(a+b). A new
edge inside an attachment cuts off at most A vertices and hence has cut mass
at most A. For a detached tree, ab/(a+b)<=N/4<=B/4. This proves (8) and
acyclicity is immediate from the stated attachment operation.

This is stronger than bounding final component size: an old component may
have arbitrarily many vertices. Combined with (1), bounded local attachment
mass preserves operator stability under the exact action-noise convention.
Arbitrary local gluing is not covered; the double-star violates the required
uniform bound on attached mass at the root of the new central connection.

## 6. Removing long triangular chains from the selected four-color problem

The bounded structural contribution and focused challenge are preserved in
research/structure/ and research/cut_balance_review/. Its exact lemma is:

For P_n^2 with n>=30, prescribe any distinct colors at the ordered left
endpoint pair (0,1) and independently any distinct colors at the ordered
right pair (n-2,n-1). These extend to a proper acyclic four-coloring whose
bichromatic components have at most16 vertices, with no bichromatic path
connecting the two endpoint pairs. Construction takes O(n) work.

The proof uses the twelve ordered distinct two-color states. Appending a
color different from the previous two is a valid transition. All twelve
states reach all twelve states in exactly six transitions; a finite exact
table is supplied, with a color-symmetry proof/replay. Six-vertex boundary
buffers surround a period-nine core of at least eighteen vertices. For
every color pair, the core contains two consecutive vertices of the
complementary pair. Their absence from that induced subgraph blocks every
edge of length at most two across the gap. Thus the buffers cannot create
a bichromatic path between the ends. A proper coloring of this chordal
graph is acyclic. The constant16 is a safe component-size bound from the
buffers plus the inherited core bound; the core operation itself is not
claimed as new in this cycle.

In a K4-minor-free graph, a maximal edge-connected union of triangles is a
genuine2-tree, and a connected outside piece has a clique neighborhood of
size at most two in it. The inherited classification of genuine2-trees
with Delta<=4 makes every such long component P_n^2; book3 and three-sun
are finite exceptions. Its interior vertices are already degree four, so
external edges can touch only its two endpoint pairs.

Delete the internal vertices of all such components of order at least30,
keeping both endpoint edges. Call the reduced graph R. It remains in the
original class and all its triangle components have order at most29. Any
proper acyclic four-coloring of R extends independently by the lemma.
Within a color pair, an inserted tree meets R at one vertex or at the two
ends of an already retained edge. In the latter case, deleting that edge
splits it into trees attached separately to its endpoints: acyclicity within
the strip forbids a second path. It meets no opposite-end vertex. Thus no
old bichromatic components merge and no new bichromatic cycle arises.

A Delta4 vertex belongs to at most four strip incidences, a deliberately
loose bound (the focused reviewer gives two). At most16 new vertices per
incidence can attach to it in a given color pair. Therefore Section5 applies
with A=64, B=16, W=65:

    Gamma_G <= max(65 Gamma_R,64),                         (9)

and, if all base components have order<=K, all final components have order
at most max(65K,16)=65K for K>=1. Consequently a uniform bounded-component
acyclic four-color theorem for the reduced class would imply one for the
entire original class. The converse holds by restriction to a subclass.

This is a reduction, not a full four-query construction on arbitrary input:
the coloring of R is still needed. The reducer/extension validates supplied
strip representations; discovering and proving the missing global coloring
is not treated as free preprocessing. Extraction of maximal triangle unions
is linear at fixed degree by local triangle enumeration and edge-component
traversal; the source separates this from general treewidth recognition.

## 7. Remaining scientific boundary and primary comparisons

Unbounded triangular chain length is no longer the unresolved obstruction to
this coordinate route. The remaining task is a closed size-two-separator
state invariant through bounded triangular atoms and square/chordless pieces
of unbounded branching depth. Acyclicity alone still permits arbitrary growth.
Neither Section2 nor Section6 supplies an all-dense-design four-query lower.
The original full-class query interval is unchanged: four necessary, five
sufficient. Six is not substituted for the stronger current comparator.

Classical acyclic/star sparse-Hessian compression and substitution are
established: Gebremedhin, Pothen, Tarafdar, Walther, Efficient Computation of
Sparse Hessians using Coloring and Automatic Differentiation (2009),
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf,
especially Section3 and Theorem3.1. That theorem treats entrywise substitution
error through subtree sizes. We do not claim discovery of that mechanism or
historical originality of the present optimality/cut formulation.

Wood, Acyclic, Star and Oriented Colourings of Graph Subdivisions (2005),
https://dmtcs.episciences.org/articles/344/download, Lemma3, gives three star
colors for an exact one-subdivision of a three-colorable graph. Lemma11
gives four for sufficiently subdivided edges. Such subdivision-only cases
are already stronger ordinary comparators, not an unclaimed new opportunity.

Trotignon and Vuskovic, arXiv:1407.6531v2, Section5, Lemma5.2,
https://arxiv.org/html/1407.6531v2, describes bad adjacent-boundary triples in
triangle-free clique-cutset-free series-parallel graphs. The source review
derives a useful finite exception: under Delta<=4, every such graph of more
than12 vertices has a degree-two vertex outside the closed neighborhoods of
any specified adjacent pair. The counting derivation is preserved, but a
low-degree reinsertion does not automatically preserve component size. It is
an input to the next construction, not a solved extension theorem.

## 8. Error, cost and verification obligations

Preprocessing and decoding of a supplied coloring take O(nq+m) arithmetic
operations and storage; for fixed q this is O(n+m). The new centroid/cut
certifier has the same order. Rational bit cost depends on input lengths.
Finding the coloring or structural representation, q actual matrix actions,
input conversion and any downstream spectral calculation are additional.

For a supported symmetric computed answer and rigorously bounded residual
R=Dhat X-PY, the guarantee is ||Dhat-D||op<=C(||E||F+||R||F).
Physical query error deltaX contributes D deltaX and requires a bound, e.g.
||D||op||deltaX||F. The saved coordinate seeds are exact0/1 and all saved
numerical data use Fraction arithmetic. No solver success flag is a proof.

Internal analytic reviews and independent exact fixture checking are separate
from historical novelty, external acceptance and implementation performance.
COSTS.md records the actual executions and unmetered discovery/authoring.
The original NIST dense incumbent and the closed molecular and other campaigns
are not rerun or claimed beaten. Their native sources remain unchanged.
