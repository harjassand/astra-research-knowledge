# Accepted: an open strict-ROC family with no polynomial global selector

The exactly symmetric quartic in `EXACT_SYMMETRIC_TARGET.json` is strictly
rank-one convex, but has no polynomial minor-affine global support selector
of any degree. This is a stronger representation obstruction than the
failure of any particular SOS or norm-multiplier level. Root independently
accepts it from the literal actual-atom replay and the complete argument
below. True polyconvexity and quasiconvexity of this target remain open.

Write B_F(A,X)=F(A+X)−F(A)−DF(A):X. The excluded assertion is the existence
of a polynomial k:R4→R such that

    B_F(A,X)−k(A)detX ≥ 0                    for every A,X.       (1)

The peer constructed a positive functional made of 24 actual rational
(A,X) evaluations. Its source certificate is
`quartic_boundary_alternative/EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json`,
SHA256 `e51d9be90ba977c34f5daab4a75901eb6acc377dc53c0004d479425fed945d22`.
Root's `independent_atomic.py` uses a separate SymPy polynomial engine,
imports no producer or peer verifier, and directly differentiates/evaluates
the literal quartic at each atom. The completed replay took 0.225 seconds.
It proves exactly

    all weights > 0,
    sum_atoms weight A_i A_j detX = 0        for all ten i≤j,
    sum_atoms weight B_F(A,X) < −1/100000.                    (2)

The exact large rational pairing and every coefficient sensitivity are
retained in `INDEPENDENT_ATOMIC_REPLAY.json`. There is no pseudo-moment
positivity premise in this argument: the functional is a positive sum of
actual polynomial evaluations.

## Why every polynomial degree is excluded

If (1) holds, fix any A0 and two matrices X+ and X− whose determinants
are respectively +1 and −1. Scale A=t A0 and X=t X± with t>0.
Quartic homogeneity gives

    B_F(A0,X−) + k(t A0)/t² ≥ 0,
    B_F(A0,X+) − k(t A0)/t² ≥ 0.

Thus k(t A0)/t² is bounded both above and below for every t>0. A finite
polynomial in t, divided by t², can be bounded as t→0 and t→infinity
only if all its components except degree two vanish. This holds at every
A0, so k is homogeneous quadratic or zero. In particular no higher degree
polynomial can rescue the support assertion.

Write that remaining quadratic as sum k_ij A_i A_j. Applying the positive
atomic functional to the left side of (1) gives its strictly negative
Bregman pairing, because every k_ij direction is annihilated in (2).
That contradicts the assumed nonnegativity of every evaluated summand.

The usual general polynomial minor-vector formulation is also excluded.
At equality B=A, differentiating a touching nonnegative minor-affine
remainder forces its four entry coefficients to DF(A)−k(A)cofA. Its
remainder is therefore precisely (1). A constant minor contributes no
remainder. No selector symmetry is assumed in this proof.

Any SOS norm-multiplier construction with a polynomial k and a multiplier
positive off an algebraic zero set would imply (1) by division there and
continuity. In particular EVERY finite |X|^(2r) support level using
polynomial selectors is excluded. This does not contradict the accepted
strict-quadratic-support hierarchy: the hypothesis that such a selector
exists fails here. Rational or nonlinear homogeneous selectors remain
possible; the obstruction does not establish true non-PC.

## A full 35-dimensional open family, without exact symmetries

Root additionally evaluated the atomic functional on all 35 ordinary
homogeneous quartic monomials in the four matrix entries. Its exact l1
sensitivity S is in the replay receipt. Under a coefficient sup-norm
perturbation epsilon, the negative pairing changes by at most epsilon S.
For epsilon=1/336000000 it stays strictly negative.

For each ordinary quartic monomial, the sum of the absolute coefficients
of all its second partial derivatives is 4*3=12, independently checked
from the literal polynomials. Since each matrix coordinate is bounded by
|A|, and each direction coordinate by |H|,

    |D²(delta F)(A)[H,H]| ≤ 35*12*epsilon |A|² |H|².

The symmetric target's separately checked exact acoustic certificate gives
the rank-one lower bound |A|² |H|²/400000. Hence every perturbation with
all 35 ordinary coefficients changed by at most 1/336000000 retains the
rank-one lower bound |A|² |H|²/800000. The same 24 actual atoms still
annihilate every quadratic selector and have negative Bregman pairing.
Therefore BOTH strict ROC and the all-polynomial-selector obstruction
persist on this full 35-dimensional closed box. No symmetry requirement
is imposed on its perturbations.

The atoms have different base points A. They are not a gradient law at one
fixed affine background and do not supply a Jensen/quasiconvexity
counterexample. Failed searches for such compatible laws remain distinct.
No world-priority, physical-technology or civilisation-level claim follows.
