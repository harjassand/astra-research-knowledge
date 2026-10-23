# Focused independent review: cut balance and coordinate operator stability

Reviewer: `cut_balance_challenge`, Cycle5 PRO2. This is a challenge of the
owner's proposed degree-free theorem, not a second investigation of four
queries on maximum-degree-four partial two-trees. The original Cycle4 proof
was read in full through its norm/decoder sections; no old fixture was rerun.

## Verdict

The proposed proof is correct under the stated proper-coordinate,
free-diagonal, absolute Frobenius action-noise contract. A useful refinement
replaces the factor `8 r Gamma` by `4 r M`, with `Gamma <= M <= 2 Gamma`.
The canonical mean-projected decoder has norm exactly equal to the
information inverse constant, although the displayed computable bounds need
not equal that norm. The conclusion is representation-specific. It does not
settle the four-versus-five question for all admitted real designs.

## Definitions and exact statement

Let G be a nonempty finite simple graph. Let c be a proper coloring with q
colors, X_i=e_{c(i)}, and let S_G be all real symmetric matrices supported on
G, including arbitrary diagonal entries. Let

    A(D)=DX,   rho=sup_{D != 0} ||D||op/||A(D)||F,
    r=max_i |{c(j): ij is an edge}| <= q-1.

Every bichromatic edge-containing component must be a tree. A bichromatic
cycle yields the inherited alternating-edge nonzero exact kernel. For each
edge e of such a tree T, let a_e,b_e be its two cut sizes, N_T=a_e+b_e. Define

    Gamma = max_{T,e} a_e b_e / N_T,
    M = max_{T,e} min(a_e,b_e),

with both maxima zero if G is edgeless. Then the exact mean-projected
incidence decoder L satisfies

    max(1,sqrt(Gamma)) <= rho = ||L||_(F->op)
        <= sqrt(1+4 r M) <= sqrt(1+8 r Gamma).                 (1)

For a family with bounded r (in particular fixed q), stable recovery by these
specified proper-coordinate designs is therefore possible uniformly if and
only if every bichromatic component is a tree and Gamma is uniformly bounded.
No graph-degree hypothesis is needed. If q or r is allowed to grow, bounded
Gamma alone is not established as sufficient by (1).

## The lower bound and estimator scope

For a cut A,B of sizes a,b, choose signed divergence f_i=1/a on A and -1/b
on B. Sign the unsigned incidence to an oriented incidence C. The unique
flow Cw=f on a tree has absolute coefficient one at the cut edge. Extending
this edge-weight matrix by zero gives

    ||D||op >= 1,   ||DX||F^2 = 1/a+1/b = N/(ab).

The free diagonal supplies the separate lower bound one. These are
information lower bounds, not shortcomings of a particular decoder. If an
exact estimator is applied to true D with noise -DX, it sees the same zero
observation as the zero matrix; a two-point construction about arbitrary
D0 gives the same minimax lower even for nonlinear estimators.

## Tree geometry and centroids

Root a tree at a centroid o. Every component of T-o has order at most N/2.
Every child subtree S_e in the resulting orientation is contained in one of
these branches, so its size a_e is at most N/2. Hence

    a_e = min(original cut sizes),
    a_e b_e/N = a_e(1-a_e/N),
    a_e/2 <= a_e b_e/N <= a_e.

The largest oriented child subtree is one of the branches at o. Consequently
M_T is precisely the largest centroid branch, and

    Gamma_T = M_T (1-M_T/N_T),   Gamma_T <= M_T <= 2 Gamma_T.

Taking maxima over trees gives the inequalities in (1). This also supplies
the geometry behind the degree-free condition: each bichromatic tree has a
single centroid from which every branch has uniformly bounded order. The
number of branches is unrestricted. The condition is not bounded diameter:
a double-star can have diameter three and arbitrarily large balanced cut.

A centroid and all subtree sizes can be found in O(N) work. No optimization
or spectral solve is hidden in the certificate M or Gamma.

## The local squared-row estimate

Write the observed error in the cells assigned to T as E_T. Color-sign it
to f; this preserves its Euclidean norm. For a child edge e with subtree S_e,
the decoder's edge error has the form

    delta w_e = sigma_child <q_e,f>,
    q_e = 1_{S_e} - (a_e/N) 1.

Fix one vertex v. The subtrees for its children are disjoint. If their sizes
form the vector a, their Gram matrix is exactly

    (<q_e,q_f>)_(e,f) = diag(a) - aa^T/N <= diag(a) <= M_T I.

The signs sigma_child only conjugate this Gram matrix by a diagonal
orthogonal matrix. It follows that

    sum_{e from v to a child in T} |delta w_e|^2
        <= M_T ||E_T||_2^2.                                  (2)

This is the crucial difference from an absolute row-sum bound: it allows an
unbounded number of short branches without charging their number as degree.
All action-noise cell sets from different color-pair components are disjoint.
Thus, after orienting every component away from its own centroid, the sum of
squared outgoing edge errors at any graph vertex is at most

    M ||E_off||F^2,                                          (3)

where E_off contains only the non-diagonal signal cells. The choice of
component roots need not be globally consistent and does not need to be.

## From oriented rows to the operator norm

Let U_ij equal the recovered edge error when edge ij is oriented from parent
 i to child j, and zero otherwise. The supported symmetric off-diagonal
error is U+U^T. A vertex belongs to at most one tree for each of its neighbor
colors, and has at most one parent within each such tree. Therefore every
column of U has at most r nonzero entries.

For arbitrary z, Cauchy--Schwarz in each column gives

    ||U^T z||_2^2
      <= r sum_j sum_i |U_ij|^2 |z_i|^2
      <= r (max_i sum_j |U_ij|^2) ||z||_2^2.

Combining this with (3),

    ||U+U^T||op <= 2 ||U||op
                 <= 2 sqrt(r M) ||E_off||F.                  (4)

The diagonal recovery error is taken from disjoint own-color cells and has
operator norm at most ||E_diag||F. Combining (4) with this independent norm
budget by two-dimensional Cauchy--Schwarz proves

    ||L(E)||op <= sqrt(1+4 r M) ||E||F.

Unused noise cells may be discarded. No independence or probability
assumption on E was used. No conversion from matrix Frobenius error to
operator error with an omitted dimension factor was used either.

## Exact decoder norm and optimality for a fixed design

Let H be the range of A in the action space with its Frobenius inner product.
The componentwise sign/mean projection, together with keeping diagonal cells
and zeroing unused cells, is the orthogonal projection P onto H. The
canonical decoder is L=A^{-1}P. Therefore

    ||L(E)||op <= rho ||PE||F <= rho ||E||F.

Conversely, choosing E=A(D) in the definition of the decoder norm gives
||L|| >= rho. Thus equality holds. An arbitrary exact decoder cannot have a
smaller worst-case deterministic noise constant, by the zero-observation
lower bound above. Equation (1) bounds this optimum; it does not calculate
its exact numerical value in general.

The residual allowance is inherited unchanged: for a supported symmetric
computed answer Dhat and a rigorously bounded R=Dhat X-PY,

    ||Dhat-D||op <= C (||E||F+||R||F),

with C=sqrt(1+4rM), or any stronger independently certified constant. Query
implementation error still contributes D deltaX and must be charged.

## Exact local-gluing failure: balanced double-stars

Take two adjacent hubs u,v, each with t leaves, t>=1. Properly two-color the
resulting tree. Set the central edge coefficient to 1, every leaf coefficient
to -1/(t+1), and the entire diagonal to zero. Both hub action entries equal
1/(t+1); every leaf action entry equals -1/(t+1). Consequently

    n=2t+2,   diameter=3,
    ||DX||F^2=2/(t+1),   ||D||op>=1,
    Gamma=(t+1)/2,   rho>=sqrt((t+1)/2).

Each individual star has a uniformly stable two-color coordinate inverse.
Joining two such pieces by one edge can nevertheless create an unstable
balanced global cut. Bounded piece diameter, bounded number of joined pieces,
and good separate local inverse constants do not establish a global inverse.
This example has unbounded maximum degree t+1. It must not be presented as
an all-design lower bound, or as an obstruction within the maximum-degree-four
class when t grows.

## A concrete useful support class

Suppose a tree is supplied as a hub with any number of disjoint arms, each
having at most L edges. Rooting at the hub need not give a centroid, but a
centroid exists and no smaller cut side can exceed L: every edge cuts off a
terminal portion of one arm, or has that portion as its complement. Thus
M<=L. The proper bipartite coordinate design uses exactly two actions and
has

    ||Dhat-D||op <= sqrt(1+4L) ||E||F.

This is uniform in the number of arms. If an edge is allowed, one query is
not injective (n+m free symmetric coefficients, only n scalar outputs), so
two is the exact and stable query minimum on this supplied fixed-L class.
Two equal arms of length L give a path of order 2L+1; its middle cut gives
Gamma=L(L+1)/(2L+1). Thus the worst operator constant has order sqrt(L), up
to absolute factors. The inherited three-query forest design has constant
sqrt(2) and remains the stronger conditioning comparator; a query saving is
not an overall computational speedup.

## Limits and scientific status

For uniformly bounded maximum degree, bounded Gamma is equivalent to the
old bounded-component-size condition, so this theorem alone does not solve
the remaining four-coordinate existence problem. Its substantive extension
is a degree-free information criterion and a correct global composition
quantity, with an exact instability witness when it fails.

This review establishes internal mathematical correctness. Historical
originality, external acceptance and practical application speedup were not
assessed. The construction does not reopen the preserved molecular/NIST or
other closed operations and does not change the all-dense-design quantifiers.
