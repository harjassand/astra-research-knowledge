# Exact spatial minimax for one global ellipsoid

16 October 2026. Independent follow-up requested by the parent after the
v0001 audit. Input `SOURCE_ROOT_THEOREM.v0002.md`, SHA-256
`7f86a62c738c16f7468b4071cf919e425c36ef54dfc03855dce428757b0ef500`.

**Verdict:** v0002's box optimum, ellipsoid cell objective, convexity,
feasibility test, and disjoint-set closed form are correct. For the stated
single global ellipsoid and a common scalar spatial cap, its closed form
extends to **every overlapping incidence family**. The convex feasibility
formulation is valid but unnecessary for computing this optimum.

This statement is strictly about the stated modewise supported-unitary
proposal and diagonal Pauli-floor family. It does not optimize over all
correlated CPTP proposal decompositions or physical interventions.

## 1. Setup and exact per-cell objective

Let the finite modes be `i=1,...,m`, with acquired axes `b_i>0`, and receive
the **one global** uncertainty contract

`sum_i h_i^2/b_i^2 <= 1`.

Let each receiving cell or guard `c` charge a subset `S_c` of modes. Empty
subsets can be ignored, and coordinates charged nowhere have no effect on
this optimization. At fixed positive floors the modewise rate is

`lambda_i=gamma_i+h_i^2/gamma_i`.

Writing `u_i=h_i/b_i`, the exact worst cell rate is

`F_c(gamma)=sum_{i in S_c} gamma_i+max_{i in S_c} b_i^2/gamma_i`.

The maximum follows by allocating all ellipsoid mass to a largest-ratio
coordinate in the cell. The quantity is convex in positive floors: each
reciprocal is convex, the finite maximum preserves convexity, and the other
term is linear. Thus the root's finite convex optimization description is
sound. It need not be interpreted as an exact finite-bit solver.

## 2. The feasibility test is equivalent

For positive `z_c`, define

`gamma_i(z)=max_{c:i in S_c} b_i^2/z_c`.

Suppose floors `gamma` satisfy every `F_c(gamma)<=q`. Choose
`z_c=max_{i in S_c} b_i^2/gamma_i`. For each incident pair `(i,c)`,
`b_i^2/z_c<=gamma_i`, so `gamma_i(z)<=gamma_i`. It follows that

`sum_{i in S_c} gamma_i(z)+z_c<=F_c(gamma)<=q`.

Conversely, if positive `z` obeys these inequalities, then for every
incident pair `gamma_i(z)>=b_i^2/z_c`. Therefore

`b_i^2/gamma_i(z)<=z_c`,

and `F_c(gamma(z))<=sum_{i in S_c} gamma_i(z)+z_c<=q`.

This proves both directions of v0002's feasibility test with all overlaps
retained. Its constraints are themselves convex in `z` because positive
reciprocals, their maxima, and sums are convex.

For a finite nonempty charged catalog the infimum is attained. Any feasible
sublevel with value at most `q` bounds each charged coordinate by

`b_i^2/q <= gamma_i <= q`.

The sublevel is closed inside this compact positive box; a finite feasible
point exists, so the minimum is attained. If no cell is nonempty, the
objective and optimum are zero.

## 3. Closed form for arbitrary overlap

Define

`B_c^2=sum_{i in S_c} b_i^2`,
`B_max=max_c B_c>0`.

The one-cell ellipsoid theorem gives, for every common floor vector,

`F_c(gamma)>=2B_c`.

Taking the maximum proves the lower bound `q_*>=2B_max`. Choose the **single
shared floor vector**

`gamma_i=b_i^2/B_max`

for every charged mode. All ratios are now identical:

`b_i^2/gamma_i=B_max`.

Consequently every nonempty cell has

`F_c(gamma)=B_c^2/B_max+B_max<=2B_max`.

At a cell attaining `B_max`, equality holds. Therefore the exact answer is

```
q_* = 2 max_c sqrt(sum_{i in S_c} b_i^2),
gamma_i = b_i^2 / max_c sqrt(sum_{j in S_c} b_j^2)
```

for arbitrary overlaps, within the stipulated modewise family. The lower
bound and explicit upper-bound construction meet exactly. Overlapping cells
need not all be individually optimized: it is enough that each lies below
the common maximum. This is why unequal cell norms do not obstruct one
shared optimal floor vector.

The same result appears in the root's feasibility variables by setting
every nonempty `z_c=B_max`. Then `gamma_i(z)=b_i^2/B_max`, and the budget
inequalities reduce to `B_c^2/B_max+B_max<=2B_max`.

The root's disjoint formula `2max_c B_c` is thus correct. Its disjoint
per-cell floor choice is one optimizer; the shared vector above is another
optimizer even in that case. The value has no additional overlap penalty
beyond the incidence-weighted norms already present in `B_max`.

As a nontrivial exact overlapping example, take axes `(5,12,9)` and cells
`S_1={1,2}`, `S_2={2,3}`. Their norms are `13` and `15`. The common floors
are `(5/3,48/5,27/5)`. The cell worst rates are respectively `394/15` and
`30`, proving the spatial optimum `30` with a shared mode and unequal cell
norms. The global whole-catalog total-rate optimum is a different objective.

## 4. The box optimum also holds for arbitrary overlaps

For bounds `|h_i|<=epsilon_i`, the worst rate in any cell is

`sum_{i in S_c}(gamma_i+epsilon_i^2/gamma_i)`.

Each summand exceeds or equals `2epsilon_i` independently of all other
coordinates, and `gamma_i=epsilon_i` attains equality at every incident
cell simultaneously. Thus, with zero-uncertainty coordinates omitted,

`inf_gamma max_c sup_h R_c = 2max_c sum_{i in S_c}epsilon_i`.

This is exactly v0002's formula. No disjointness assumption is needed, and
no tradeoff among cell objectives is needed for the box.

## 5. Contract boundaries

The closed form above assumes one global ellipsoid. If instead each anchor
`x` has its own independently variable ellipsoid, the worst rate in a cell
is a sum of block maxima:

`sum_x [sum_{i in S_c intersect block_x}gamma_i
        +max_{i in S_c intersect block_x}b_i^2/gamma_i]`,

with empty block intersections contributing zero. Flattening independent
blocks into one global ellipsoid changes the supplied uncertainty set and
is invalid. The displayed shared-ratio argument does not by itself solve
that different optimization. A general rotated ellipsoid, different
cell-dependent weights/caps, non-diagonal floors, or correlated supported
proposal channels also requires a separate derivation.

The receiver's per-center versus per-touching-cell geometry conversion in
`AUDIT.md` remains necessary. Computing `B_max` only uses known coefficients
and support incidence; it does not acquire them or validate a physical
noise model. The inherited memory probability theorem remains conditional.

`exact_spatial_cases.py` exhausts every incidence family covering three
modes, checks the shared-floor certificates and the feasibility compression
on a rational floor grid, and checks the explicit overlapping example.
`EXACT_SPATIAL_CASES.json` is bounded exact evidence for these algebraic
claims, not an independent proof of an asymptotic memory theorem.
