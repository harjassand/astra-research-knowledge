# Independent check of the coning lemma and its induction interface

Reviewer: `/root/fan_port_lemma`, 22 October 2026 Australia/Brisbane.
Object supplied by root: a coning operation that increases an all-design
unstable query budget by one, followed by a proposed treewidth induction.
This note records a symbolic critical check. It is not a numerical certificate,
historical novelty assessment, or claim of efficient witness computation.

## 1. Accepted coning statement

Let H be a nonempty finite graph with free diagonal. Let k>=0 and epsilon>=0.
Assume that for every row-capped real |V(H)|-by-k query matrix Z there exists
a supported symmetric B with

    ||B||_2=1,  ||BZ||_F<=epsilon.                 (A)

Take k+1 disjoint copies of H and add one universal apex adjacent to every
vertex in every copy. Call the resulting graph Cone_(k+1)(H). Then for every
row-capped query matrix X with k+1 columns on this cone, there is a supported
symmetric D with

    ||D||_2=1,  ||DX||_F<=sqrt(k+1) epsilon.      (B)

The hypothesis (A) follows from an all-design inverse quotient lower bound
1/epsilon: minimize the continuous action norm on the compact unit
operator-norm sphere in the finite-dimensional supported symmetric space.
If a kernel exists, choose a normalized kernel vector. When epsilon=0,
state (A) directly instead of writing its reciprocal.

## 2. Full algebra and exceptional cases

If the apex query row is zero, its unit diagonal is a supported exact kernel,
and (B) holds. Otherwise perform an orthogonal right-coordinate change so
that the apex row is (0,...,0,a), where a>0. Row caps and Frobenius action norms
are preserved by this change. Partition the other rows as [Z,V], with k
columns in Z and one in V. Put R=V/a, a column vector, and split these data
over the k+1 copies of H.

For each copy j use (A) to choose a symmetric B_j supported on that copy,
with operator norm one and ||B_j Z_j||_F<=epsilon. There is a nonzero real
coefficient vector c=(c_1,...,c_(k+1)) satisfying

    sum_j c_j R_j^T B_j Z_j = 0.                 (C)

Indeed the left side is a k-component row vector, so this is a linear
homogeneous system with k equations and k+1 unknowns. No independence or
conditioning assumption is required. Normalize max_j |c_j|=1 and let

    B=blockdiag(c_1 B_1,...,c_(k+1) B_(k+1)).

Then ||B||_2=max_j |c_j|=1, and

    ||BZ||_F^2 = sum_j c_j^2 ||B_j Z_j||_F^2
                <=(k+1)epsilon^2.             (D)

Set L=[-R^T; I] and D_raw=L B L^T. Its lower principal block is B, its apex
diagonal is free, and all its border entries are permitted because the apex
is universal. B has no entries between distinct copies. Thus D_raw is
supported on the cone, including all diagonal positions. Compression to its
lower principal block gives ||D_raw||_2>=||B||_2=1.

Since the full query block has apex row (0,a) and lower block [Z,V],

    L^T X=[Z,V-Ra]=[Z,0],

and therefore

    D_raw X = [-R^T BZ,0; BZ,0]=[0,0; BZ,0].  (E)

The first output row is zero by (C). Combining (D),(E), and normalizing
D=D_raw/||D_raw||_2 proves (B). In particular, normalization cannot enlarge
the action, because the divisor is at least one.

The division by a is legitimate whenever this case is used. Its size can
make R and D_raw large, but no bound on either is invoked: the apex action
cancels exactly, and final operator normalization only helps. Replacing this
exact cancellation by an estimate of ||R|| would invalidate the uniform
bound, but the supplied proof does not do so.

For k=0, Z and the constraint row are empty. There is one copy, one coefficient
c_1=1, and the same algebra gives zero action. Thus this endpoint is valid
and can be used as the induction base below.

**Review decision:** the coning lemma is correct in the stated exact-real,
free-diagonal, absolute-action-noise model.

## 3. Treewidth and quantifiers

If H has treewidth at most w, each copy has a tree decomposition with bags
of size at most w+1. Add the apex to every bag, then join the copy decomposition
trees by arbitrary links between bags. Every such bag contains the apex, so
its running-intersection property is preserved; all other vertices stay in
one copy. The new width is at most w+1. This verifies the coning width bound.

The graph H and the k+1 copies are fixed before X is chosen. Only the local
matrices B_j and scalar coefficients c depend on X. Thus the conclusion
retains the all-design quantifier. No common local witness across distinct
query blocks is needed, and there is no probabilistic selection argument.

The lemma is an existential operation on exact matrices. It does not by
itself give a bit-complexity bound, a certified floating nullspace algorithm,
or a practical sparse-inversion speedup. Those must be stated separately.

## 4. Check of root's proposed induction interface

Let K_t=binom(t+2,2). Suppose the induction hypothesis at treewidth t-1
provides, for any desired accuracy, a finite graph H on which every
(K_(t-1)-1)-column row-capped design admits a unit-operator supported matrix
with action at most that accuracy.

Put

    h=K_(t-1),  q=h+t=K_t-1,  r=t-1.

Coning h copies of such H, using the proved lemma with k=h-1, gives a graph
of treewidth at most t with a universal apex and all-design h-query action
accuracy epsilon, provided the induction input accuracy is epsilon/sqrt(h).
This is the child graph required for the next step. Its universal apex is
essential: all subsequent apex-to-child cancellation coefficients are
permitted support entries.

### General tail estimate

For q-column data on a child, project its nonapex rows W onto the top h-1
right singular directions and retain its apex row. The resulting full query
block has rank at most h and preserves row caps. If the whole graph were to
have inverse constant C, the same perturbation argument as in
fan_spectral_rank_review.md gives

    sum_(i=h)^q lambda_i(W^T W) >= (1/C-epsilon)_+^2.

For N children at one vertex, variational tail superadditivity then gives

    lambda_h(sum_j W_j^T W_j)
       >= N (1/C-epsilon)_+^2/(q-h+1)
       = N (1/C-epsilon)_+^2/(t+1).             (F)

This applies to arbitrary child query blocks; they need not have matching
frames or orientations. Repeated eigenvalues are harmless. Every time the
positive right side of (F) is used, the selected top-h aggregate eigenspace
has strictly positive least eigenvalue.

### Core dimension count

The proposed root core is K_r join P_m, with

    m=q(t-1)-t(t-1)/2+2,  n0=m+r.

Its support-space dimension, including free diagonals, is

    d=n0+binom(r,2)+r m+(m-1)
      =(t+1)m+t(t-1)/2-1.

At each of the m path vertices require the core action to lie in the chosen
h-dimensional aggregate child space. This imposes at most q-h=t scalar
linear conditions per vertex. At each of the r core clique vertices require
the full q-component action to vanish. There are at most

    t m + q(t-1)

conditions in total, and the chosen m makes d minus this count exactly one.
Thus a nonzero supported symmetric core matrix exists for every query design
and every choice of these child subspaces. Dependence among constraints can
only increase the available dimension. Normalize the core matrix to operator
norm one. Its action norm is at most sqrt(n0), since all n0 query rows are
capped by one.

### Spoke cancellation and the target-C quantifier

For each path vertex v, let r_v be its core action row, which lies in the
selected aggregate child space. The aggregate child query matrix W_v has
Gram A_v. A minimum-norm coefficient vector solving

    W_v^T alpha_v=-r_v

has squared norm at most ||r_v||^2/lambda_h(A_v). Place these coefficients
on the permitted spokes between v and the child vertices. Their action at
v cancels its core action exactly. At each child vertex, the remaining
action is its coefficient times x_v. Distinct child vertices are disjoint,
so squared action norms add; ||x_v||<=1. The core clique actions were already
zero. Thus the resulting full supported matrix D has

    ||D||_2>=1,
    ||DX||_F^2 <= n0(t+1)/[N(1/C-epsilon)_+^2]. (G)

The norm lower bound follows from the principal core block, regardless of
the signs or size of the added spokes. No off-support child-to-child entry
is introduced.

For a contradiction to a proposed fixed uniform constant C>0, first choose
the cone-child accuracy epsilon<=1/(2C), and then fix an integer

    N>4 C^4 n0(t+1).

Construct the graph using those choices before considering X. If a design
had inverse constant at most C, every child would inherit the same bound;
(F),(G) would force 1<=C||DX||_F<1. Therefore every design has inverse
constant greater than C. This order of quantifiers avoids choosing graph
parameters after seeing an individual design.

The root core has treewidth at most t, and each child has treewidth at most t.
Identifying one child's universal apex with a core path vertex is a vertex
sum. Connecting decomposition bags containing that vertex preserves width,
so the full graph also has treewidth at most t.

These checks validate the proposed induction interface. Root remains the
author of the combined theorem and is responsible for its final statement,
upper comparator, implementation scope and novelty boundary.

## 5. Optional clean base

The induction can start at t=0 without another quantitative path theorem.
Here K_0=1, and the singleton graph has a supported unit diagonal with zero
action for its unique zero-column query matrix. One query recovers a diagonal
support exactly and stably.

For the step t=1, coning with k=0 gives an edge having an exact one-query
kernel for every query design. The root core has r=0,m=2 and is itself an
edge. Attaching N child edges at each endpoint produces a double star, and
the rank/core argument gives two-query instability as N grows. This supplies
the required forest lower base within the same proof mechanism. It does not
supersede or alter the previously proved sharp path result under unit rows.

## 6. Costs and remaining checks

This note uses elementary exact linear algebra and the root's supplied
construction. No numerical experiment, web search, prior scientific replay,
optimization, or precision sweep was executed. Symbolic review, authoring,
model inference, monetary cost and energy are additional and unmetered.

The resulting lower proof is qualitative all-design instability at one fewer
than K_t queries. It does not establish a sharp divergence exponent in total
vertex count, an optimal inverse constant above the threshold, a practical
algorithm for large recursive witnesses, or historical originality. The
established star-color upper bound must be cited separately for a matching
query-minimum theorem.
