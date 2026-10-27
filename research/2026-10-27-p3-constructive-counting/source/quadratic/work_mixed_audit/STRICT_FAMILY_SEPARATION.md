# A strict family for the acquired mixed quadratic-core theorem

## Statement and scope

All matrix operations below are over `F_2`. An edge means an unordered pair of
distinct indices. Thus a symmetric matrix with `M` nonzero off-diagonal edges
has `2M` nonzero off-diagonal entries. Diagonal entries are allowed in a
competing symmetric core and are not charged against its edge-error budget.

Fix a constant `0 < alpha < 1`. There is a family of Boolean cubic phases

\[
 p_n(x)=P_n(x)+q_{B_n}(x),\qquad
 q_B(x)=\sum_{i<j}B_{ij}x_ix_j,
\]

with all of the following properties. Here `n` is the original number of
independent input bits, and `r=2 floor(n^alpha/2)`.

1. `P_n` is a sum of `n/3` disjoint cubic monomials, and
   `B_n=A_n+S_n`, where `A_n` is alternating of rank `r` and `S_n` has
   `O(n)` edges. The decomposition is an existence property; the counting
   algorithm is given only the raw coefficients of `p_n`.
2. `B_n` has `Omega(n^2)` nonzero edges and rank `Omega(n)`. Every balanced
   coordinate cut has `F_2` cut rank `Omega(n)`.
3. Across every balanced cut of the original input coordinates, the full phase
   tensor `((-1)^{p_n(x)})` has matrix flattening rank `2^{Omega(n)}` over
   `Q` or `C`. This includes the cubic part, not only its quadratic component.
4. No symmetric core `D_n'` of rank below `r` can approximate the
   off-diagonal matrix `B_n` within `n^{1+o(1)}` edge changes. The competitor
   may use an arbitrary diagonal. In particular the family cannot fall into a
   smaller mixed class requiring core rank `n^{o(1)}` and near-linear sparse
   error through a different hidden decomposition.
5. For the centroid decomposition of the cubic third-derivative tensor, the
   primitive blocks have dimension three, but their quadratic interaction
   graph has `Omega(n^2)` nonzero block pairs. Changing bases within those
   blocks does not remove these interactions.

Consequently the mixed acquisition theorem applies in its new
`r=o(n), M=O(n)` regime, while the direct near-linear local-factor criterion,
the pure small-rank quadratic criterion, the previous near-linear
centroid-block coupling criterion, and small coordinate-cut-rank criteria do
not hold on this family. These are separations between specific
representation conditions. They are not general algorithmic lower bounds.
In particular, a purely quadratic phase is exactly summable by Gaussian
methods even when its cut ranks are large.

The raw coefficient list here has length `Theta(n^2)` bits, or
`Theta(n^2 log n)` under an index-list convention. The mixed theorem's
polynomial dependence on that description length is therefore explicit.
Its exact phase-counting time is `poly(L+n) 2^{o(n)}`; this note does not
execute that asymptotic engine or claim a practical speedup.

## 1. A support-cover lemma, including arbitrary diagonals

**Lemma 1.** Let `T` be a symmetric `n by n` matrix, of rank `q`, with at
most `M` off-diagonal edges. For every positive integer `tau`, one can
construct a set `E` such that

\[
 T_{RR}=0,\qquad R=[n]\setminus E,\qquad
 |E|\le \left\lfloor\frac{2M}{\tau}\right\rfloor+q\tau.
 \tag{1}
\]

If `T` is alternating, the last term can be replaced by `q(tau-1)`.
In particular, for `q>0`,

\[
 |E|\le 2\sqrt{2qM}+q
 \tag{2}
\]

with the usual interpretation `|E| <= q` when `M=0`. The zero matrix
requires no deletion.

**Proof.** Let `H` consist of the vertices of off-diagonal degree at least
`tau`. Since the degree sum is at most `2M`,
`|H| <= floor(2M/tau)`. Put `C=[n] minus H`. Every row of `T_CC` has at most
`tau-1` off-diagonal nonzeros and at most one diagonal nonzero, so its total
support has size at most `tau`.

Choose a row basis of `T_CC`, of size at most `q`, and let `J` be the union
of the supports of these actual basis rows. Then `|J| <= q tau`. Each row
of `T_CC` is a linear combination of the chosen rows, hence every column
outside `J` is zero. In particular `T_(C minus J),(C minus J)=0`. Taking
`E=H union J` proves (1). If the diagonal is zero, the basis rows have
support at most `tau-1`.

For `M>0`, choose `tau=ceil(sqrt(2M/q))`. Then
`2M/tau <= sqrt(2qM)` and `q tau <= sqrt(2qM)+q`, proving (2).
For `M=0`, choose `tau=1`. The argument is constructive using ordinary
Gaussian elimination in polynomial time. QED.

The additive `q` term is needed when diagonal entries are free: a diagonal
matrix of rank `q` has no off-diagonal edges but requires deletion of those
`q` supported vertices to leave a zero principal matrix. No bound in terms
of off-diagonal sparsity alone is being asserted.

## 2. Code distance prevents a hidden rank drop

Let `r` be even, let `J_r` be the standard nonsingular alternating matrix
with `r/2` diagonal blocks `[[0,1],[1,0]]`, and let `U` be an `n by r` binary
matrix. Define

\[
 A=U J_r U^T,\qquad
 d(U)=\min_{0\ne z\in\mathbb F_2^r}\operatorname{wt}(Uz).
\]

Positive distance implies that `U` has full column rank. If fewer than
`d(U)` rows are removed, the remaining matrix `U_R` still has full column
rank: any nonzero vector in its kernel would give a nonzero codeword of
`U` supported on the removed rows. Therefore

\[
 \operatorname{rank}(A_{RR})
 =\operatorname{rank}(U_RJ_rU_R^T)=r.
 \tag{3}
\]

The last equality follows because `U_R` is injective, `J_r` is invertible,
and `U_R^T` is surjective.

**Lemma 2 (finite rigidity certificate).** Suppose `B=A+S`, where `S` is
alternating with at most `M` edges. Let a proposed symmetric core `D'`
have rank at most `r'<r`, arbitrary diagonal, and off-diagonal error at
most `M'` from `B`. If, for some positive integer `tau`,

\[
 \left\lfloor\frac{2(M+M')}{\tau}\right\rfloor
       +(r+r')\tau < d(U),
 \tag{4}
\]

then no such core exists. A sufficient real-valued condition is

\[
 2\sqrt{2(r+r')(M+M')}+(r+r') < d(U).
 \tag{5}
\]

**Proof.** Set `T=A+D'`. It is symmetric of rank at most `r+r'`.
Its off-diagonal support is the sum of the two error matrices, so it has
at most `M+M'` edges, irrespective of the diagonal of `D'`. Apply Lemma 1
to obtain a set `E` satisfying (4), with `T_RR=0`. Its size is below
`d(U)`, so (3) implies

\[
 r=\operatorname{rank}(A_{RR})
   =\operatorname{rank}(D'_{RR})
   \le\operatorname{rank}(D')\le r'<r,
\]

a contradiction. QED.

**Asymptotic consequence.** Suppose `d(U)>=delta n` for a constant
`delta>0`, `r=o(n)`, and `r(M+M')=o(n^2)`. Lemma 2 rules out every
symmetric competitor of rank below `r`, for all sufficiently large `n`.
This includes every fixed error allowance `M'=Cn` when `M=O(n)`.
More strongly, if `r=n^{alpha+o(1)}` with fixed `alpha<1`, it includes
every allowance `M'=n^{1+o(1)}`. Since a rank `n^{o(1)}` competitor is
eventually below `r`, this proves strictness against the earlier smaller
mixed-rank regime even after optimizing over alternative decompositions.

## 3. Simultaneously obtaining distance and density

Sample the rows `u_i` of `U` independently and uniformly from
`F_2^r`, where `r>=2` is even and `r=o(n)`.

For any fixed nonzero `z`, the bits of `Uz` are independent fair bits.
The elementary binomial Chernoff/Hoeffding bound gives

\[
 \Pr[\operatorname{wt}(Uz)<n/4]\le e^{-n/8}.
\]

A union bound over the `2^r-1` nonzero vectors gives

\[
 \Pr[d(U)<n/4]\le (2^r-1)e^{-n/8}=o(1).
 \tag{6}
\]

For completeness, a direct second-moment calculation also gives the
required density, without assuming that the entries of `A` are mutually
independent. Let

\[
 t=2^{-r},\quad N=\binom n2,\quad
 X_{ij}=\mathbf 1[u_i^TJ_ru_j=1],\quad W=\sum_{i<j}X_{ij}.
\]

Conditional on `u_i != 0`, the inner product with `u_j` is fair; when
`u_i=0`, it is zero. Hence

\[
 p=\mathbb E X_{ij}=\frac{1-t}{2},\qquad
 \mathbb E W=N\frac{1-t}{2}.
\]

Disjoint index pairs give independent indicators. For distinct `i,j,k`,
conditional independence given `u_i` gives

\[
 \mathbb E[X_{ij}X_{ik}]=\frac{1-t}{4},\qquad
 \operatorname{Cov}(X_{ij},X_{ik})=\frac{t(1-t)}4.
\]

There are `3 binom(n,3)` unordered pairs of distinct edges sharing a
vertex. Thus

\[
 \operatorname{Var}(W)
 =\frac{N(1-t^2)}4+\frac32\binom n3 t(1-t).
 \tag{7}
\]

Since `r>=2`, the mean is at least `3N/8`. Chebyshev's inequality gives

\[
 \Pr[W<N/4]
 \le\frac{64\operatorname{Var}(W)}{N^2}
 =O(n^{-2}+t/n)=o(1).
 \tag{8}
\]

Combining (6) and (8) by another union bound proves that, with probability
`1-o(1)`, the same `U` has distance at least `n/4` and `A` has at least
`N/4` edges. No independence between those two events is needed. Full
column rank, and hence rank exactly `r` of `A`, follows from distance.

Both properties can be certified: enumerate the `2^r-1` codewords for
the distance and compute the edge count of `U J_r U^T` for density.
Sampling and verification take expected `poly(n) 2^{O(r)}=2^{o(n)}` time.
These certificates concern the witness family; they are not supplied to
the raw-input counting algorithm.

## 4. Expanders force large coordinate cut ranks

Take `S` to be the adjacency matrix of a simple graph of maximum degree
at most a fixed `D`, with edge-expansion constant at least a fixed `h>0`:

\[
 |E_S(X,[n]\setminus X)|\ge h|X|
 \quad\text{for }|X|\le n/2.
\]

Such constant-degree expander families are standard; an explicit primary
construction is Reingold--Vadhan--Wigderson, *Entropy waves, the zig-zag
graph product, and new constant-degree expanders*, Annals of Mathematics
155 (2002), 157--187,
[official article](https://annals.math.princeton.edu/2002/155-1/p04) and
[author manuscript](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/SALIL/EXPANDERS/ANNALS/RVW01.pdf).
If one starts from a bounded-degree multigraph, discard loops and collapse
parallel edges to a single edge, rather than adding them modulo two. The
number of distinct crossing edges decreases by at most the constant
maximum multiplicity, so positive constant edge expansion is retained.

For a balanced cut `n/3 <= |X| <= 2n/3`, let `Y` be its complement. Its
cross graph has at least `hn/3` edges. A bipartite graph of maximum degree
`D` with `m` edges contains an induced matching of size at least
`m/(2D^2)`: choose an edge `uv`, then delete all edges incident to a
neighbor of `u` or a neighbor of `v`, removing at most `2D^2` edges, and
repeat. The selected rows and columns form an identity submatrix of
`S_XY`. Therefore

\[
 \operatorname{rank}(S_{XY})\ge\frac{hn}{6D^2},\qquad
 \operatorname{rank}(B_{XY})\ge\frac{hn}{6D^2}-r=\Omega(n).
 \tag{9}
\]

This also implies `rank(B)=Omega(n)`. Even adding an arbitrary diagonal
to `B` cannot lower its rank below the balanced cross-matrix rank, so
the pure symmetric low-rank criterion fails as well.

Density survives sparse perturbation:
`|E(B)| >= |E(A)|-|E(S)| >= N/4-Dn/2=Omega(n^2)`.

## 5. The full cubic phase also has exponential cut flattenings

The quadratic cut-rank result alone does not automatically apply to the
full cubic phase. The following construction supplies the missing step.
Work on expander sizes divisible by three, and partition the vertices
into triples. A uniform random triple partition puts the endpoints of
any fixed edge in the same triple with probability `2/(n-1)`. Hence the
expected number of within-triple `S` edges is

\[
 |E(S)|\frac{2}{n-1}\le\frac{Dn}{n-1}<2D.
\]

There exists, and rejection sampling finds in expected constant trials,
a partition with at most `4D` such edges. Put

\[
 P(x)=\sum_{T\text{ a triple}}\prod_{i\in T}x_i.
\]

For any balanced cut, discard those at most `4D` within-triple edges
from its crossing graph. Greedily choose an induced matching, with the
additional rule that every selected endpoint must occupy a different
triple from every other selected endpoint. After selecting `uv`, remove
all edges incident to either endpoint's triple (at most `6D` edges),
and all edges incident to the opposite neighborhoods (at most `2D^2`
edges). This produces a matching of size

\[
 t_X\ge\frac{hn/3-4D}{2D^2+6D}=\Omega(n).
 \tag{10}
\]

Let `I` and `J` be its selected vertices on the two sides. Then `S_IJ` is
the identity matrix and `rank(B_IJ)>=t_X-r`. Set every variable outside
`I union J` to zero. Every cubic monomial vanishes, because each triple
contains at most one selected variable. This restriction gives a
submatrix of the full phase flattening equal, up to invertible row and
column signs, to

\[
 H_M=( (-1)^{x^TMy} )_{x,y\in\mathbb F_2^{t_X}},
 \qquad M=B_{IJ}.
\]

Its distinct rows are exactly `2^{rank(M)}` distinct binary characters
of `y`; those characters are linearly independent over `Q` and `C`.
Thus

\[
 \operatorname{rank}_{\mathbb C}(\text{full phase flattening at }X|Y)
 \ge 2^{\operatorname{rank}(B_{IJ})}
 \ge 2^{t_X-r}=2^{\Omega(n)}.
 \tag{11}
\]

Any exact tree tensor representation whose leaves are the original
individual variables has a balanced edge. If one tensor-network edge
alone represents that cut, its bond dimension must therefore be
`2^{Omega(n)}`. This is a precise obstruction to that particular kind
of coordinate-cut compression; it does not forbid arbitrary changes of
variables, non-tree representations, cancellation algorithms, or other
exact counting methods.

## 6. Separation from local scopes and centroid-block coupling

**Fixed scopes in the original variables.** For each nonzero edge
`B_ij`, set every other variable to zero. The multiplicative cross ratio
of the four values of `(-1)^p` on `(x_i,x_j)` is `-1`. A nonzero factor
whose scope does not contain both `i` and `j` has cross ratio `1`.
Therefore any exact product representation of the phase by factors of
scope at most a fixed `k` must include every such pair in at least one
factor scope. Its factor count is at least

\[
 \frac{|E(B)|}{\binom k2}=\Omega(n^2)
\]

for `k>=2`; unary factors cannot represent a nonzero quadratic edge.
This conclusion allows arbitrary nonzero factor values, rather than
only monomial factors. It concerns the original coordinates and does
not assume that every representation after a global substitution is
dense.

**Acquired cubic blocks.** The third-derivative tensor of `P` is a direct
sum of nonzero alternating volume forms on its three-dimensional
triples. Each volume form has zero radical and scalar centroid over
`F_2`: the centroid identity forces all off-diagonal entries of an
endomorphism to vanish and all three diagonal entries to agree.
The centroid of the direct sum is the product of these scalar
centroids. Indeed, an off-block component would pair with two vectors
in its target block to give a nonzero tensor evaluation on one side of
the centroid identity and zero on the other; nondegeneracy excludes
it. The primitive centroid blocks are consequently exactly the
triples, up to ordering.

At most `n` quadratic edges lie within those triples. Since `B` has
`Omega(n^2)` edges, its cross-block quadratic forms have
`Omega(n^2)` nonzero coefficients. Each block pair carries at most
nine coefficients, so the block interaction graph has
`Omega(n^2)` edges. Independent invertible linear changes within the
blocks transform a cross bilinear matrix `C_ij` to
`T_i^T C_ij T_j`; it is zero exactly when the original was zero.
Changes to the cubic term from within-block affine changes create only
within-block quadratic terms. Hence the dense block interaction graph
cannot be repaired by choosing another allowed block basis.

The mixed theorem removes this obstruction by acquiring the dense
quadratic core from its raw matrix and treating the residual sparse
quadratic factors jointly with the local cubic factors. It does not
assume that a block interaction graph was sparse.

## 7. Executed finite verification

The exact runnable implementation is
`strict_family_separation_checks.py`; its complete output is
`strict_family_separation_results.json`. Command:

```sh
python work_mixed_audit/strict_family_separation_checks.py
```

All assertions passed. The execution includes:

- Every symmetric matrix through dimension five, including arbitrary
  diagonals, under every integer threshold from one through its
  dimension: **168,146 support-cover checks**. A separate diagonal-only
  example verifies the necessity of the additive rank term.
- The cube, Petersen graph, and hexagonal prism, with sampled and
  exactly certified distance/density cores: **2,799 balanced cuts**,
  with exact edge expansion, matching submatrices, cut ranks, and the
  rank perturbation inequality checked.
- For the prism's four independent cubic triples, **2,211 full-phase
  restricted flattening checks**. The matching restriction eliminates
  the cubic terms; explicit matrices over `F_3` have the predicted
  rank `2^{rank_F2(B_IJ)}`. This is a check of the exact character-rank
  identity, not a numerical floating-point calculation.
- **8,192 symmetric competitors** in two dimension-twelve fixtures:
  every rank-zero or rank-one symmetric matrix is enumerated as
  `v v^T`. This enumeration allows arbitrary diagonals.
- A larger exact rigidity certificate on **4,098 variables**. The core
  has rank six and code distance **1,993**; its matrix has **4,145,922**
  edges. The sparse perturbation has **16,377** edges and maximum
  degree at most eight. The observed matrix has **4,146,143** edges.
  For a competing symmetric core of rank below six with at most
  `4n=16,392` edge errors, use `q<=11`, `M+M'<=32,769`, and `tau=75`.
  Formula (1) gives a support-cover upper bound of **1,698**, below
  the exact code distance by **295**. Lemma 2 therefore certifies the
  nonexistence of every such competing core. The original rank-six
  core meets the error budget, so the minimum allowable core rank at
  that budget is exactly six.

The large sparse graph is a union of four sampled Hamiltonian cycles.
It is **not** certified here to be an expander and is used only for the
rank-rigidity certificate. The asymptotic expander assertion rests on
the cited expander theorem. The finite cut checks are independent
small examples. None of these executions runs the asymptotic
replacement-form phase counter, establishes a practical runtime
advantage, or supports a priority claim for the component linear
algebra, coding, or expander facts.
