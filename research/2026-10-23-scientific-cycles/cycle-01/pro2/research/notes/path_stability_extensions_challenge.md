# Bounded extension challenge: forests and a row-energy cap

This addendum challenges two stated extensions only. It does not start another
matrix experiment. The root owns and has separately checked the forest
recovery implementation; those tests were not duplicated here.

## 1. Three depth colors give stable recovery on every rooted forest

Choose one root per component and set `X_v=e_(depth(v) mod3)` in R^3. Let a_v
denote diagonal entries and b_vw the symmetric coefficients on forest edges.
At a vertex v, the own color, parent color and child color are distinct.
There is at most one parent, while all children have the same color. Thus

    (D X)_v = a_v e_own
              + b_v,parent e_parent
              + (sum_(w child of v) b_vw) e_child,

with absent parent/child terms omitted. Orthogonality yields the exact identity

    ||D X||_F^2 = sum_v a_v^2 + sum_edges b_e^2
                  + sum_v (sum_(w child of v) b_vw)^2.

Since `||D||_F^2=sum a_v^2+2sum b_e^2`, one obtains

    ||D||_F <= sqrt(2) ||D X||_F.

Direct recovery is explicit: read a_v from row v's own-color coordinate, and
read each parent-child edge from the child's parent-color coordinate. Assign
the recovered edge to both symmetric matrix entries. For arbitrary action
noise E, this decoder satisfies

    ||D_hat-D||_F <= sqrt(2) ||E||_F,

because it selects distinct diagonal and edge coordinates, and only the edge
coordinates are counted twice in the reconstructed symmetric Frobenius norm.
No inverse of a growing elimination matrix is needed.

For an endpoint-rooted path, each vertex has at most one child, so the last
sum equals `sum_edges b_e^2` and the map is an exact Frobenius isometry. For
the specified rooted-color construction, sqrt(2) is attained whenever some
vertex has at least two children: give two of those edges coefficients1 and
-1, set all other coefficients and diagonals to zero, and their child-color
sum cancels. This is a statement about that rooted construction. Choosing
an endpoint root avoids this cancellation on path components.

The forest assumptions are essential for this simple formula: every neighbor
must be the unique parent or a child, and diagonal/parent/child colors must
remain distinct. A generic cyclic graph with a depth labeling does not
automatically have the property. Isolated vertices and one-vertex components
are harmless; only their diagonal coordinate is present.

## 2. The sharp unit-row Frobenius constant does not survive a row cap unchanged

The proposed equality between the unit-row optimum and the optimum over rows
of norm AT MOST1 is false. A complete exact counterexample already occurs
at n=4. Take

    X = [[4/5,0], [0,1], [1,0], [0,4/5]].

All row norms are at most1. Their squared norms are16/25,1,1,16/25, and the
total Frobenius energy is82/25, below4.

For symmetric tridiagonal D with diagonal a and off-diagonal b, the diagonal
and neighbor contributions occupy different output coordinates. Hence

    ||D X||_F^2 = (16/25)(a_1^2+a_4^2)+a_2^2+a_3^2 + b^T G b,
    ||D||_F^2 = sum_i a_i^2+2sum_i b_i^2,

where

    G = [[41/25,4/5,0], [4/5,2,4/5], [0,4/5,41/25]].

Its eigenvalues are

    41/25,       lambda_-=(91-sqrt(3281))/50,
                lambda_+=(91+sqrt(3281))/50.

They follow by splitting the first/third antisymmetric vector from the
two-dimensional symmetric subspace. Equivalently the characteristic
polynomial factors as

    (t-41/25)(t^2-(91/25)t+2).

The smallest eigenvalue is lambda_-, and lambda_-*lambda_+=2. Therefore the
EXACT Frobenius inverse constant for this X is

    C_F(X)^2 = max(25/16, 2/lambda_-) = lambda_+.

For a sharp witness, set all diagonals to zero and take

    b = (1, (9-sqrt(3281))/40, 1).

Then `G b=lambda_- b`, so the ratio squared is exactly lambda_+.

The strict improvement is provable without any decimal evaluation:
`57<sqrt(3281)<58` gives

    74/25 < C_F(X)^2 < 149/50 < 3.

But the previously proved unit-row optimum at n=4 has square

    1/[2 sin^2(pi/8)] = 2+sqrt(2) > 3.

Thus shrinking the endpoint amplitudes improves the inverse constant. A
monotone claim that coordinate-wise amplitude reduction can only worsen
the full symmetric-recovery condition number is invalid. The output's
coupling geometry changes; both numerator and denominator weights matter.

This is an exact algebraic counterexample to the stronger mathematical claim,
not a claim of a new practical spectral method or an optimized row-cap design.

## 3. A valid row-cap lower bound still excludes uniform two-query stability

Let every row of a two-column X have norm at most1. A zero row gives an
unobserved diagonal coefficient. Adjacent dependent rows give a supported
rank-one annihilator. In either case the inverse constants are infinite.

Otherwise write `X=R U`, where `R=diag(r_i)`, `0<r_i<=1`, each row of U has
norm1, and `t=min_i r_i`. For any unit-row witness D', set

    D=R^{-1}D'R^{-1}.

This is again symmetric tridiagonal and `D X=R^{-1}D'U`. For either the
operator or Frobenius norm on D,

    ||D'|| = ||R D R|| <= ||D||,
    ||D X||_F <= t^{-1} ||D'U||_F.

Consequently the inverse constant C(X) satisfies `C(X)>=t C(U)`. A single
diagonal coefficient at a minimum-norm row also gives `C(X)>=1/t`. Thus

    C(X) >= max(1/t, t C(U)).

This inequality is valid despite the preceding counterexample: it supplies
only a lower bound, not equality or monotonicity under scaling.

For the Frobenius objective, the sharp unit-row result gives

    C_F(X) >= sqrt(1/[sqrt(2) sin(pi/(2n))]) = Omega(sqrt(n)).

For the operator objective, put `m=floor(n/2)`. The tent construction and a
single diagonal witness give `C_2(U)>=max(1,sqrt(m/2))`, hence

    C_2(X) >= max(1,(m/2)^(1/4)) >= (n/6)^(1/4),  n>=2.

Here `m>=n/3`. Both growth statements are nonsharp bounds for the capped-row
class. They do not reinstate the disproved sharp constant. Their purpose is
to establish that no two-column row-capped design has a dimension-independent
inverse bound along the growing path family.

Combining that fact with the three-column forest decoder gives the stated
uniform stable query-budget distinction for growing forests, under the same
row cap and absolute Frobenius action-error model. It does not require a new
finite-model benchmark or a claim about the actual NIST block's conditioning.

## Exact check and costs

`checks/check_row_cap_counterexample.py` builds the exact n=4 action Gram
matrices with Fraction arithmetic and verifies the extremizing vector and
ratio in the quadratic field Q(sqrt(3281)). It also verifies all rational
root isolators used for the strict comparison. No floating spectrum or
optimization is used. The receipt is
`results/row_cap_counterexample_challenge.json`.

Forest implementation fixtures are owned by the root and were not repeated.
Proof development, the false-extension diagnosis and authoring are additional
costs not fully captured by this small exact checker.
Observed checker body including imports:0.015776333s wall,0.015750594s CPU,
peak RSS9306112 bytes. It made one exact check, with no parameter or precision
sweep and no reconstruction of another finite-model input.
