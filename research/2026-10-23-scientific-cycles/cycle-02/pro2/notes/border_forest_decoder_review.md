# Scoped review: border plus forest decoder and its operator error constant

Contributor `/root/compression_challenge`, 22 October 2026 Brisbane.
This reviews the root's new construction; it does not repeat the incoming
three-query lower bounds or the original NIST benchmark.

## 1. Model and the simple guarantee

Partition the vertices as S disjoint union T, with |S|=s and G[T] a forest.
The induced support on S is arbitrary, as are the permitted S--T edges.
All diagonal coefficients are allowed. Assign S vertices distinct coordinate
rows e_1,...,e_s. Root each forest component and assign T rows one of three
additional orthogonal coordinate vectors, indexed by depth modulo3. Every
query row has norm exactly1. There are q=s+3 actions.

For noisy observed action Y=DX+E, use:

* S diagonal i: Y[i,i].
* Permitted S--S edge {i,j}: the average (Y[i,j]+Y[j,i])/2.
* Permitted S--T edge {i,v}: Y[v,i].
* T diagonal v: Y[v,own_forest_color].
* T--T edge {v,parent(v)}: Y[v,parent_forest_color].

Set every forbidden coefficient to zero and copy recovered edges symmetrically.
All selected cells are distinct, except that averaging intentionally uses two
separate S--S cells for one coefficient. In the forest row, S coordinates,
self color, parent color and child color are different. Thus high boundary
degree, a high-degree forest vertex, or absent S--T edges introduces no
confounding in any selected cell. The S row's three forest-color aggregates
are simply unused, so they cause no noise amplification in this decoder.

The error satisfies

    ||Dhat-D||_F^2 <= 2 ||E||_F^2.

Indeed, for an S--S edge the two symmetric output errors contribute
2*((e_ij+e_ji)/2)^2 <= e_ij^2+e_ji^2. Every one-cell edge contributes2e^2;
every diagonal contributes e^2. This is valid for arbitrary, correlated,
non-symmetric noise E. It does not require E itself to be an action.

It costs q actual matrix actions, O(n+|E(G)|) support traversal and coefficient
reconstruction, and O(n+|E(G)|) sparse output storage; retaining all measured
actions requires an additional O(nq) storage. Explicitly scanning a dense
n-by-q received array costs O(nq); this should be counted if the representation
requires such a scan. The algebraic decoder needs only the selected cells.
A supplied forest/border decomposition can be validated by a union-find or
DFS pass in O(n+|E(G)|). Discovering a small feedback vertex set is a different
problem and is not hidden in this cost statement.

## 2. Stronger operator bound for this particular decoder

The preceding sqrt2 Frobenius bound implies an operator bound, but the latter
can be sharpened without changing the q actions or local decoder:

    ||Dhat-D||_2 <= sqrt(5/3) ||E||_F,  if s>=1,
    ||Dhat-D||_2 <= sqrt(3/2) ||E||_F,  if s=0.

These are sharp as universal bounds for the precise decoder above, which reads
forest and boundary edges from one cell and averages S--S edges. They are NOT
claims about the optimal decoder for every fixed graph. On a small graph,
additional isolated cells can be averaged to give a better decoder.

### Proof

Write H=R(E) for the symmetric error produced by this linear decoder.
For a real unit vector u, the functional u^T R(E)u is linear in the selected
noise cells. Its squared Euclidean coefficient norm is

    sum_i u_i^4
      + 2 sum_{SS edges {i,j}} u_i^2 u_j^2
      + 4 sum_{ST edges {i,j}} u_i^2 u_j^2
      + 4 sum_{TT edges {i,j}} u_i^2 u_j^2.               (1)

The coefficient2 on S--S edges follows because averaging gives each of two
noise cells coefficient u_i u_j. Other edges have one cell with coefficient
2u_i u_j. Set w_i=u_i^2, so w_i>=0 and sum_i w_i=1. The exact operator norm
of R from Frobenius noise to spectral matrix norm is the square root of the
maximum of (1). Interchanging the two suprema is valid: both are suprema of
one bilinear form over their respective compact unit sets.

For any forest F and nonnegative weights of total mass t,

    sum_v w_v^2 + 4 sum_{uv in E(F)} w_u w_v <= (3/2)t^2.  (2)

To prove (2), take two nonadjacent vertices with positive weights and hold
their total weight fixed. The displayed quadratic expression is a convex
quadratic in one of the two weights, so one endpoint of the allowed interval
does not decrease its value. Move all weight to that endpoint. Repeating
reduces the support to a clique; in a forest it has size at most2. On an edge,
with weights a and t-a, the expression is t^2+2a(t-a)<=3t^2/2; on a singleton
it is t^2. This proves (2) for every finite forest.

Put t=sum_{i in T} w_i. Regardless of missing edges, the S part of (1) is
at most (1-t)^2, the S--T part is at most4t(1-t), and the T part is at most
3t^2/2 by (2). Their sum is at most

    (1-t)^2 + 4t(1-t) + (3/2)t^2
      = 1+2t-(3/2)t^2 <= 5/3.

This proves the first bound. If S is empty, (2) directly gives3/2.

### Sharpness for the stated decoder

For s>=1, take a triangle with one vertex in S and an edge in T; any additional
S vertices may be isolated. Root T at one endpoint, so the forest edge is read
only in the child row. Put1/3 in each of the three selected diagonal noise
cells and2/3 in each of the three selected edge cells, and zero in all other
cells. The decoded H has diagonal1/3 and every off-diagonal entry2/3:

    H=(2/3)11^T-(1/3)I_3.

Its eigenvalues are5/3,-1/3,-1/3, while ||E||_F^2=5/3. The ratio is sqrt(5/3).
For s=0, use a single forest edge with selected diagonal noise1/2 and selected
edge noise1. The output has eigenvalues3/2,-1/2 and noise norm squared3/2,
giving sqrt(3/2).

Again, this sharpness is for the explicit one-cell forest/boundary decoder.
For the triangle itself, all pairwise entries happen to be isolated in both
rows, and averaging all of them improves its error constant. Such a graph-
specific improvement does not refute the stated universal algorithm norm.

## 3. Lower-bound lift: inspected obligations, not a duplicate proof

For root's K_s joined to a path lower family, the projected-row mechanism is
consistent with the absolute-noise and row-cap contract. If the s apex rows
are dependent, their complete clique supports an invisible rank-one matrix.
Otherwise an orthogonal query-coordinate rotation puts apex rows in the last
s coordinates with invertible s-by-s block U, and leaf rows become [Z,T],
with Z in R^(m-by-2). For the lift use

    L=[-U^(-T) T^T ; I_m],  so L^T X=[Z,0].

For tridiagonal B, D=L B L^T has precisely permitted clique/path/join support.
Its action's apex part vanishes when T^T BZ=0, which is at most2s scalar
linear constraints. Hence2s+1 slow sine modes suffice when m>=2s+2. The
principal path block gives ||D||_2>=||B||_2 without an uncontrolled ||L||
factor. The small-projected-row rank-one witness must be included separately;
it pays for arbitrarily short projected directions. This scoped inspection
found no structural gap. The root owns the full proof and quantified rate.

## 4. Cost of this scoped review

Analytic work and source writing are unmetered additional research work.
No numerical optimization, graph search or original benchmark was run.
One small exact rational script checks the attaining noise examples and
selected-cell reconstruction. Its body time and peak RSS are recorded in
results/border_decoder_checks.json. Finite checks supplement the all-size
proof; they do not establish its universal quantifiers.
