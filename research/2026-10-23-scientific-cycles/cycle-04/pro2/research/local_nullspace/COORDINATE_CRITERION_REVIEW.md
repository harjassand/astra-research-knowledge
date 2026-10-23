# Independent bounded review: proper coordinate seeds

Reviewer: `local_nullspace`, Cycle4 PRO2. This is a focused challenge of the
root's proposed coordinate-seed theorem, not a universal four-direction lower
bound. No old numerical experiment was replayed.

## Verdict and necessary wording

The proposed lower bound is correct. The exact characterization must say that
**every bichromatic component is a tree, and all those trees have uniformly
bounded order**. Merely saying that the components which happen to be trees are
bounded does not exclude a cyclic component, which gives an exact kernel.

For a chosen cut edge, the flow construction guarantees `|w_e|=1`; its sign
depends on the incidence convention. This is sufficient for the operator-norm
lower bound. Maximum degree must be uniformly bounded for necessity. A star
with its proper two-color coordinate design has unbounded component order but
a uniform inverse bound at most `sqrt(2)`.

## Quantitative theorem

Let `G` be a finite nonempty simple graph, with a proper coloring `c:V -> {1,...,q}`.
Let `X_v=e_{c(v)}`. Let `S_G` contain all real symmetric matrices supported on
the graph, with unrestricted real diagonal. Put

```
C(G,c) = sup_{D in S_G, D != 0} ||D||_2 / ||DX||_F,
```

with infinity when the action has a nonzero kernel. The row-energy cap holds
with equality. Let `Delta` bound the graph's maximum degree, and let `r` be
the maximum number of distinct neighbor colors at a vertex; thus
`r <= min(Delta,q-1)`.

If a bichromatic component contains a cycle, `C(G,c)=infinity`. Otherwise let
`K` be the maximum vertex order of an edge-containing bichromatic component,
or `K=1` if there are no edges. For `Delta >= 1`,

```
max(1,sqrt((K-1)/(2 Delta))) <= C(G,c)
    <= sqrt(1+r(K-1)).
```

The left side is 1 for an edgeless graph, and in that case the exact inverse
constant is 1. Hence in any family with uniformly bounded maximum degree,
uniform operator recovery by these specified proper coordinate seeds holds
if and only if all bichromatic components are trees of uniformly bounded
order. For `q=4, Delta<=4`, the bounds are

```
max(1,sqrt((K-1)/8)) <= C(G,c) <= sqrt(3K-2).
```

This is a quantitative `Theta(sqrt(K))` characterization when maximum degree
and the number of neighbor colors are fixed. It does not imply that every
admitted graph possesses such a coloring with bounded K.

## Orthogonal decomposition of the action

Properness makes `Y[v,c(v)] = D[v,v]` in exact arithmetic. For a color pair
`{a,b}`, the remaining entries `Y[v,b]` at vertices of color `a` and `Y[v,a]`
at vertices of color `b` are exactly the unsigned incidence action `B_T w`
on the edge weights of each bichromatic component `T`.

Different component actions occupy disjoint entries of `Y`. They are also
disjoint from all diagonal channels. Entries for colors having no incident
neighbor carry no exact signal and can be ignored. In particular, no
assumption of independent random noise is used: the Frobenius convention
allows arbitrary correlated noise and provides the required orthogonality
of the coordinate blocks.

## Cycle obstruction

Every bichromatic cycle has even length. Put alternating edge weights `+1,-1`
around any simple such cycle; set all other edges and every diagonal to zero.
At each cycle vertex the two nonzero contributions cancel in its one relevant
coordinate. Thus `DX=0` and `D!=0`. Chords and other incident edges have zero
weight, which is permitted by the linear support class.

## Tree lower bound, signs, and centroid edge

Let a bichromatic tree `T` have `N>=2` vertices. Let `S` be diagonal with `+1`
on one color and `-1` on the other. Orient every edge from the plus color to
the minus color, using incidence `C` with plus sign at the tail. Then
`C=S B_T`. The range of `C` is the mean-zero subspace, and the tree has a
unique edge flow for each mean-zero divergence.

For any edge `e`, deleting it partitions the vertices into `A,B`, of sizes
`a,b`, with `a+b=N`. Define

```
f_v = 1/a on A, and -1/b on B.
```

Solve `Cw=f`. Summing the divergence over `A` shows `|w_e|=1`; no other edge
crosses the cut. The symmetric matrix with these edge weights and zero
diagonal, extended by zero on all other graph entries, satisfies

```
||DX||_F^2 = ||B_T w||_2^2 = ||S f||_2^2 = 1/a+1/b,
||D||_2 >= |D_ij| = |w_e| = 1.
```

Consequently `C(G,c) >= sqrt(ab/N)`.

Choose a centroid vertex of `T`: every branch on deleting it has at most
`N/2` vertices. Its largest branch has size
`a >= (N-1)/deg_T(v) >= (N-1)/Delta`. The edge into that branch has
`a<=N/2`, so `b>=N/2` and

```
ab/N >= a/2 >= (N-1)/(2 Delta).
```

The diagonal-only witness gives the separate lower bound 1. No positivity,
small-entry, or bounded-spectral-radius condition on the unknown matrix is
part of this result.

### Small exact sign check

For the five-vertex path `0-1-2-3-4`, colors alternate plus/minus. Select cut
`A={0,1}`, `B={2,3,4}`. In edge order `01,12,23,34`, the oriented flow is

```
w = (1/2,-1,2/3,-1/3).
B_T w = (1/2,-1/2,-1/3,1/3,-1/3) = S f.
||B_T w||_2^2 = 5/6 = 1/2+1/3.
```

The cut coefficient is `-1`, explaining the harmless absolute-value wording.

## Explicit decoder and operator bound

For each bichromatic tree `T` with `N>=2`, extract the noisy unsigned action
`y`, switch signs to `f=S y`, and project to mean zero:

```
f0 = f - (sum_v f_v)/N * 1.
```

The unique flow solving `C w=f0` is obtained by rooting the tree, taking
subtree sums of `f0`, and applying the incidence orientation sign at each
edge. This is the least-squares inverse of `B_T`. Read the diagonal directly
from its own-color channel. Assemble symmetric edge values.

To bound error, write `e_T` for the component's action noise and consider any
vertex `v` of `T`. Let `A_e`, for incident edges `e`, be the disjoint branches
of `T-v`; their union is `T` without `v`. Let `a_e=|A_e|`, and put

```
q_e = 1_{A_e} - (a_e/N) 1.
```

Up to a sign, the edge error is `<q_e,S e_T>`. For arbitrary signs
`theta_e in {-1,+1}`,

```
||sum_e theta_e q_e||_2^2
  = sum_e a_e - (sum_e theta_e a_e)^2/N
  = N-1 - (sum_e theta_e a_e)^2/N
  <= N-1.
```

The dual formula for the `l1` norm therefore proves

```
sum_{e incident to v in T} |delta w_e|
    <= sqrt(N-1) ||e_T||_2.
```

Now sum over the distinct bichromatic components through `v`, also including
the single diagonal error `E[v,c(v)]`. Their noise blocks are disjoint, so
Cauchy--Schwarz gives

```
sum_j |delta D[v,j]|
 <= sqrt(1 + sum_{T contains v} (|T|-1)) ||E||_F
 <= sqrt(1+r(K-1)) ||E||_F.
```

The decoded error matrix is symmetric. Hence its spectral norm is bounded
by its maximum absolute row sum, proving the stated operator recovery bound.
Applying the same estimate to exact data for arbitrary `D` proves the upper
bound on `C(G,c)`. This is an operator estimate directly under absolute
Frobenius action noise, not a hidden uncharged conversion between matrix
Frobenius and operator norms.

## Arbitrary-input and nonlinear-estimator lower bound

The witness is valid around every `D0 in S_G`, because `S_G` is a linear
space. For any nonzero witness `D` with `DX!=0` and any noise budget
`epsilon>0`, set `lambda=epsilon/||DX||_F`. Both underlying matrices

```
D0 + lambda D,   D0 - lambda D
```

produce the same observation `D0 X`, with noises respectively
`-lambda DX` and `+lambda DX`, each of Frobenius norm `epsilon`. For any
decoder output at this observation, at least one of its operator errors is
at least `lambda ||D||_2`. Thus the lower bound is a true deterministic
minimax noise obstruction, including nonlinear reconstruction methods, for
the specified coordinate seed. With a cycle witness, exact nonidentifiability
holds even at zero action noise.

If the model imposed PSD, fixed norm bounds, exact nonzero patterns, or other
constraints on `D`, this unrestricted perturbation argument would need to be
rechecked. None is imposed in the present support class.

## Cost, arithmetic, and scope

Given the proper coloring, verify it in `O(m)` work. Partition the edges into
unordered color pairs and find their components; each relevant row-channel
appears only once. Test each component for being a tree. For each tree use
one mean and a tree traversal for all cut sums. The total decoder work and
storage are `O(n+m)` once the used action entries are available; reading a
full dense action array costs `O(nq)`. With bounded degree and fixed `q=4`,
both are `O(n)`. Physical acquisition still requires the stated `q` actions.

These are arithmetic-operation counts. Exact rational bit lengths and input
conversion costs are separate. For finite-precision implementation, let
`P Y` be the componentwise projected action and diagonal readout. If a
supported symmetric computed matrix has residual
`r = Dhat X - P Y`, the inverse theorem gives the verifiable allowance

```
||Dhat-D||_2 <= C(G,c) (||E||_F + ||r||_F).
```

Input/query rounding requires its own bound. A success status alone does not
replace this allowance.

This review used mathematical derivation and one hand-checkable rational
five-vertex sign example. It performed no new numerical script run,
optimization, precision sweep, or benchmark. A targeted prior-art lookup used
one search call, one batched opening of two primary sources, and one failed
attempt to fetch the original Cornell PDF (HTTP 405). This was not a complete
historical-priority investigation. Its
first recorded clock was `2026-10-21 20:35:06 UTC`; review/authoring wall and
CPU totals were not instrumented. The theorem is internally assessed here;
historical originality is not assessed.

## Closest primary literature located in the focused check

* Thomas F. Coleman and Jin-Yi Cai, *The Cyclic Coloring Problem and
  Estimation of Sparse Hessian Matrices*, DOI `10.1137/0607026`.
  The author's institutional 1984 report landing page describes the
  graph-theoretic characterization of substitution methods and a roundoff
  error bound; the PDF fetch failed in this check. Therefore a new historical
  claim about stability would require comparison with that bound, not just
  with the acyclic-coloring characterization.
  <https://ecommons.cornell.edu/entities/publication/9e03cca8-ab7d-406d-a78e-314ecd6b897f>
* Assefaw H. Gebremedhin, Arijit Tarafdar, Fredrik Manne and Alex Pothen,
  *New Acyclic and Star Coloring Algorithms with Application to Computing
  Hessians*, SIAM J. Sci. Comput. 29 (2007), 1042--1072, DOI
  `10.1137/050639879`. Its introduction and Table 2.1 identify acyclic
  coloring with substitution recovery and bichromatic forests; this
  coordinate injectivity mechanism is established prior art.
  <https://www.cs.purdue.edu/homes/apothen/Papers/acyclic-SISC.pdf>

The result concerns the supplied coordinate seed and its bichromatic
components. It is not an obstruction against arbitrary graph-adapted dense
four-column designs, and it does not by itself decide whether a graph admits
a coordinate coloring with uniformly bounded bichromatic trees.
