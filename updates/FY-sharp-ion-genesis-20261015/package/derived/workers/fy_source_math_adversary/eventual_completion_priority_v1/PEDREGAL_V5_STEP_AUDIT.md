# Pedregal v5: exact obstruction to the stated fixed point construction

15 October 2026. This is an append-only addition to the earlier source audit.
No source checkout, Git state, or original audit packet was edited. The missing
incoming ZIP is not an input. No author or external party was contacted.

**Finding.** Corollary 7.2 of the acquired v5 is false for a mold expressly
allowed by Section 4. For the periodic piecewise affine maps below,
`T(t)` is empty for every `t in Theta_1`. A single required pair of
decomposition directions has determinant 80, regardless of both weight vectors.
Consequently the proposed application of Kakutani does not establish Theorems
1.1 or 1.2. This finding does not disprove planar rank-one convexity implying
quasiconvexity, and does not exclude other molds or laminate representations.

## 1. Exact acquired claim and its dependencies

Primary source: Pablo Pedregal, [arXiv:1905.06571v5](https://arxiv.org/abs/1905.06571v5),
revision 18 June 2026; [actual PDF](https://arxiv.org/pdf/1905.06571v5), 25 pages.
Local SHA-256:
`e34a534458c37254bf6b09985e26a3947f24b21cb1f38a85b641c12bc845e7bf`.
Acquisition bytes and timestamps are in `sources/ACQUISITION_RECEIPTS.json`.

Theorem 1.1 asserts that each joint gradient measure of a pair of continuous,
periodic, piecewise affine functions on the prescribed triangulation is a
laminate. Theorem 1.2, printed page 4, asserts the equivalence of rank-one
convexity and all-background quasiconvexity for an arbitrary real-valued
function on real 2-by-2 matrices. Its QC tests are all bounded regular planar
domains with boundary of measure zero, all affine backgrounds, and all
zero-boundary Lipschitz vector fields. It is therefore a broader claimed
statement than the eventual finite-H theorem being compared.

The proof uses the following chain.

1. Section 4 fixes a tri-dyadic mold. It groups interfaces with normals
   `(1,0),(0,1)`; `(1,0),(1,1)`; and `(0,1),(1,1)`. Each interface occurs in
   two groups, each triangle in six leaves. Its interface tagging is arbitrary;
   the paragraph on printed page 12 explicitly allows each such tagging.
2. Definition 5.1, printed page 14, fixes a nonnegative leaf-weight polytope
   `Theta_l`: each adjacent leaf pair has mass `1/(3*2^(2l+1))`, and all six
   copies of each triangle have total mass `1/2^(2l+1)`.
3. The initial adjacent-triangle pairs are merged. All later dyadic relative
   weights within each group are 1/2. Decomposition directions are differences
   of the two child barycenters, as in (3.2) and (5.11).
4. Definition 6.1, printed page 16, defines `T(t)` as all `r in Theta_l` for
   which every above-interface decomposition direction for `v,r` is parallel
   to the corresponding direction for `u,t`.
5. Proposition 6.1 makes a fixed point sufficient for the required laminate;
   Theorem 6.2 invokes Kakutani. Nonempty values of `T` are essential.
6. Proposition 7.1 and Corollary 7.2 claim those values are nonempty for every
   prescribed pair of functions, mold, and feasible input weights. The exact
   example below contradicts that conclusion.

The abstract page records a withdrawn v3 in August 2024 and later v4/v5
revisions. That history is provenance only. The conclusion here comes from the
current v5 equations, not from the earlier withdrawal.

## 2. Universal obstruction, rebuilt independently

The parent communicated this fixture, attributed to another independent
Pedregal auditor. This worker did not read that auditor's results or code.
Instead, `verify_pedregal_step_independent.py` independently solved the affine
interpolation equations on every triangle, rebuilt periodic adjacencies from
square indices, checked the mold and weight constraints, and symbolically
reconstructed the decisive merge. The receipt attributes this provenance
explicitly. A separately discovered fixture is recorded in Section 4.

Take `l=1`, with grid nodes at coordinates 0 and 1/2, extended periodically.
In each square, use the diagonal with normal `(1,1)`. Rows in the following
arrays are ordered by `y=0,1/2`; entries are ordered by `x=0,1/2`:

```
u = [[ 0, 2],        v = [[ 2, 0],
     [ 1, 1]]             [-2, 3]].
```

On each square `(i,j)`, number first the triangle with unscaled vertices
`(i,j),(i+1,j),(i,j+1)`, then the triangle with vertices
`(i+1,j+1),(i,j+1),(i+1,j)`. Physical coordinates are these coordinates divided
by 2. Enumerate squares with `i` outermost and `j` innermost. The exact gradients
in zero-based triangle order are:

| triangle | gradient u | gradient v |
|---|---|---|
| 0 | (4,2) | (-4,-8) |
| 1 | (0,-2) | (10,6) |
| 2 | (0,-2) | (10,8) |
| 3 | (4,2) | (-4,-6) |
| 4 | (-4,-2) | (4,6) |
| 5 | (0,2) | (-10,-8) |
| 6 | (0,2) | (-10,-6) |
| 7 | (-4,-2) | (4,8) |

These gradients have zero mean and the correct tangential compatibility on all
three interface types. Thus they are gradients of the continuous periodic P1
functions specified by the nodal data, rather than arbitrary assigned vectors.

For `j=1`, tag the four vertical interfaces first, in row-major `(y,x)` order,
then the four horizontal interfaces, also in row-major order. The last two
horizontal interfaces are at `y=1/2`, with `x` segments `[0,1/2]` and `[1/2,1]`.
Their adjacent triangle pairs are `(1,2)` and `(5,6)`. In the resulting dyadic
mold these are the seventh and eighth bottom pairs, so their barycenters are
required to be merged in the first above-interface level. The other two groups
may be tagged by the same row-major convention; they do not affect this node.

There are 48 leaves in total. Each triangle occurs six times. All leaf weights
equal to `1/48` give an explicit feasible element of `Theta_1`; each pair has
mass `s=1/24`, and each triangle has total mass `1/8`.

For *any* `t,r in Theta_1`, let the two critical u pair barycenters be `P_u,Q_u`
and the corresponding v pair barycenters be `P_v,Q_v`. The pair mass constraints
alone, even without nonnegativity or the other triangle constraints, give

```
P_u = (0,-2),       Q_u = (0,2),
(P_v)_x = 10,       (Q_v)_x = -10.
```

Hence, taking odd child minus even child consistently for both rows,

```
U = P_u - Q_u = (0,-4),
V = P_v - Q_v = (20, 14 - 48*r_a + 48*r_b),
det(U,V) = 80.
```

Here `r_a,r_b` denote one of the two leaf weights in each pair; their partners
are `s-r_a,s-r_b`. Reversing both direction conventions leaves the determinant
unchanged. Both children have positive fixed mass `s`; zero individual leaf
weights cannot remove this merge. The nonzero determinant fails even the
weakest determinant-zero meaning of parallelism. Therefore

```
T(t) = empty for every t in Theta_1.
```

This is a universal algebraic contradiction inside the paper's finite map,
not a numerical optimization result.

## 3. The obstruction persists on an open set

Perturb each of the four periodic nodal values of each scalar function by at
most `epsilon` in absolute value. Solving affine interpolation on triangles of
side 1/2 shows that each gradient component changes by at most `4*epsilon`.
Every normalized pair barycenter is a convex combination, so that bound is
uniform over all feasible weights. Each difference of two such barycenters
therefore changes componentwise by at most `8*epsilon`, again uniformly in
`t,r`.

At the unperturbed fixture `U=(0,-4)` and `V=(20,V_y)` with `12 <= V_y <= 16`.
Writing the perturbations as `dU,dV` and expanding the determinant gives

```
det(U+dU,V+dV)
 >= 80 - 4*(8*epsilon) - 20*(8*epsilon)
          - 16*(8*epsilon) - 2*(8*epsilon)^2
  = 80 - 320*epsilon - 128*epsilon^2.
```

At `epsilon=1/10` this lower bound is `1168/25 > 0`. Thus a full open
neighborhood of the nodal pair retains empty images for every `t`. A proposed
restriction to a dense generic set of nodal functions cannot repair the
nonempty-image claim for this allowed mold.

## 4. Distinct fixture found by this worker

Before receiving the universal construction, this worker independently found
the nodal hat pair

```
u = [[1,0],         v = [[0,1],
     [0,0]]              [0,0]].
```

Use lexicographic interface tagging with vertical interfaces first and the two
vertical interfaces at `x=1/2` consecutive; choose uniform `t=1/48`.
Their adjacent triangle pairs are `(1,4)` and `(3,6)`. For the discovery
direction convention the critical directions obey `U=(-2,0)` and `V_y=4`
for every feasible `r`, so their determinant is `-8`.

Equivalently, in the discovery matrix the two pair equations are
`r5+r6=1/24`, `r7+r8=1/24`, while one parallelism equation is
`-96*(r5+r6+r7+r8)=0`. Multiplying the three equations by `-12,-12,-1/8`
respectively yields the exact contradiction `0=-1`. This concise certificate
is independently rechecked in the script. The earlier random fixture and the
hat fixture remain saved as distinct discovery receipts rather than being
silently replaced by the parent's stronger construction.

## 5. Verification and admission boundary

`verify_pedregal_step_independent.py` passes 33 exact assertions. It imports no
discovery implementation and no other auditor's implementation. It uses
integer/rational affine interpolation and symbolic identities. The two
decisive determinant identities are universal consequences of the critical
pair constraints; a finite assertion count is not being substituted for their
analytic quantifiers.

Printed pages 4, 12, 14, 16 and 19 of the actual PDF were rendered and visually
read to check the theorem, allowed mold, weight polytope, map and disputed
corollary. Receipts retain source hashes and the scope of each read.

**Admissible conclusion:** the stated v5 fixed point argument has an explicit
false required intermediate claim. **Not established here:** the truth or
falsity of its general theorem by another proof, the full planar Morrey
conjecture, the absence of a different successful mold, or any rank-one
convex/non-quasiconvex integrand. The v5 theorem therefore cannot be used as an
established premise to subsume the proposed finite-H completion result.
