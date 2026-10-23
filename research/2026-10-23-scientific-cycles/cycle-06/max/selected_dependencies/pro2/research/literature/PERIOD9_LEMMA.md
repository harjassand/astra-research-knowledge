# A stronger elementary comparator: four stable coordinate probes on bandwidth-two supports

Contributor: `/root/bounded_degree_literature`, Cycle4. This finite design arose
during the focused comparator check. Its incidence/substitution recovery
mechanism is classical; historical originality of the period is not claimed.

## Exact statement

Let the vertex order be supplied, and suppose every permitted off-diagonal
entry of a real symmetric matrix D satisfies |i-j|<=2. Every diagonal is free.
There is an explicit four-column matrix X, with every row of Euclidean norm
one, and a linear decoder L such that

    L(DX)=D,
    ||L(DX+E)-D||_2 <= ||L(E)||_F <= sqrt(3+sqrt(5)) ||E||_F.

The construction and decoder use O(n) arithmetic/work, apart from acquiring
the four actions. This resolves the stable query minimum as FOUR on the
full squared-path family when combined with the owner's accepted all-design
three-query obstruction. It does not resolve all treewidth-two maximum-degree-
four graphs, since many such supports have no bandwidth-two ordering.

## The seed and all-size combinatorial proof

Index vertices from zero. Repeat the word

    c = (0,1,2,0,3,1,0,2,3)

and take X_i=e_{c_i} in R^4. Each cyclic consecutive triple has three distinct
colors, so this is a proper coloring of P_n^2. In the infinite periodic word,
the occurrence positions and cyclic gaps for each color pair are:

| Pair | Positions in one period | Cyclic gaps |
|---|---|---|
| 0,1 | 0,1,3,5,6 | 1,2,2,1,3 |
| 0,2 | 0,2,3,6,7 | 2,1,3,1,2 |
| 0,3 | 0,3,4,6,8 | 3,1,2,2,1 |
| 1,2 | 1,2,5,7 | 1,3,2,3 |
| 1,3 | 1,4,5,8 | 3,1,3,2 |
| 2,3 | 2,4,7,8 | 2,3,1,3 |

A gap of at least three separates components because P_n^2 only has edges
of lengths one and two. The first three pairs therefore form repeated paths
on five vertices; the last three form isolated edges. There are no extra
edges: a vertex of one color cannot have two neighbors of the other color
on the same side, because such neighbors would be at distance one or two
and would violate properness. Thus every two-color component is a path.

Restricting to any finite interval, or deleting any permitted edges, only
shortens these paths. This proves the statement for every n and every support
contained in the supplied bandwidth-two order. The exact period checker
confirms the finite data; the periodic-gap argument carries the universal
quantifier.

## Decoder and error proof

Because the coloring is proper, (DX)_{i,c_i}=D_ii, so diagonals are read
directly. For each unordered color pair {a,b}, collect the nontrivial
components of the induced bipartite support. A component is a path on
l<=5 vertices. Order its edges along the path, put their coefficients in d,
and let B_l be the unsigned vertex-edge incidence matrix. The corresponding
action entries, one at each component vertex in the coordinate of the other
color, are exactly B_l d. Decode with

    d_hat=(B_l^T B_l)^(-1) B_l^T y.

There is no cumulative substitution across blocks. All cells selected for
different pair-components and the diagonal cells are disjoint. In particular,
arbitrary correlated action noise is allowed; no stochastic assumption is used.

B_l^T B_l is tridiagonal, with diagonal two and neighboring entries one.
Its eigenvalues are

    2+2 cos(j*pi/l), j=1,...,l-1.

For 2<=l<=5, its least eigenvalue is at least

    alpha=2-2 cos(pi/5)=(3-sqrt(5))/2.

Consequently each edge vector has error squared at most alpha^(-1) times
the squared norm of its component's action-noise vector. Symmetric matrix
Frobenius norm counts each edge coefficient twice and each diagonal once.
Since 2/alpha=3+sqrt(5)>1, summing over disjoint cells proves

    ||D_hat-D||_F^2 <= (3+sqrt(5)) ||E||_F^2.

Operator norm is bounded by Frobenius norm, proving the contract. The bound
is the exact inverse constant for full coefficient Frobenius recovery by this
seed when an entire five-vertex bichromatic component is present. No optimal
operator-norm constant is claimed.

The eigenvalue formula follows from sine eigenvectors of the fixed
tridiagonal matrix. An entirely rational secondary checker certifies
B_l^T B_l-(3/8)I positive definite by leading minors for all l<=5, yielding
the slightly weaker explicit constant 4/sqrt(3). For l=5, the four minors
are 13/8,105/64,533/512,209/4096. These checks are supplied in check_period9.py,
together with exact rational pseudoinverses and exact left-inverse identities.

## Costs and comparison

Constructing the seed costs O(n) writes. The support has at most 2n-3 edges,
so finding all pair-components and decoding them costs O(n) with constant-size
blocks. A supplied valid order suffices; finding a bandwidth-two ordering is
not charged as free and is not solved by this note. For ordinary floating
inputs, arithmetic error in the bounded decoder must be added to action
noise; the theorem does not automatically certify a floating implementation.

Acquiring four actions remains part of any practical cost. No spectral task,
NIST benchmark, physical application, or superiority in total runtime is
claimed. The code is an exact finite witness/check, not a performance decoder.

The five-period coordinate seed is an isometry in Frobenius norm for full
P_n^2 support: each row's five closed-neighborhood coefficients have distinct
coordinates. Thus five queries offer the stronger constant one with full
least-squares averaging, while this four-query seed uses constant
sqrt(3+sqrt(5)), about2.2883. Both construction and decoding are linear.

Classical star coloring requires five colors on P_n^2 for n>=7. The current
four-color seed is deliberately not a star coloring: it has two-color P5
components. It uses established acyclic recovery with an explicit uniform
bound on component size. Hence a comparison only against star-color count
would miss this valid operation. The owner's independent signed seed must
be compared against this four-query comparator when assessed on squared paths.

## Receiving instruction

Run `python research/literature/check_period9.py` from the package root. The
output records all pair gaps, exact small-block inverses, rational positivity
checks, and body time. Use the proof above, not repeated finite instances, for
the all-size assertion. This source is a comparator contribution for integration;
it is not a proof of the general four-versus-five question.
