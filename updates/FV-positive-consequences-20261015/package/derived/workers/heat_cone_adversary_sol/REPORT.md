# Exact ROC lift and a sharp compatible-heat boundary

15 October 2026. Independent adversarial worker `heat_cone_adversary_sol`.
Input capital pin: `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`.

## Findings and scope

The full nine-coefficient left-SO(2)-invariant rank-one-convex (ROC) quartic
cone has an exact **8 by 8 semidefinite lift with six skew parameters**.
This is a direct specialization of established Calderón / matrix
Fejér–Riesz theory, not a new general positivity theorem. The explicit
coefficient matrices and proof are in `ROC_CLASSIFIER.md`.

An additional exact boundary consequence for the supplied G is
`G-tau(det A)^2` fails ROC for every tau>0. An explicit rank-one family has
acoustic values `15t^4/8` for G and `25t^2/2` for determinant squared. Thus
the known determinant-squared polyconvex ray cannot be removed at any positive
scale, although N860's distinct convex elliptic-defect subtraction is valid.
This is proved at the end of `ROC_CLASSIFIER.md`.

A sharper internally derived result concerns the compatible-heat cone itself.
For

\[
 F_{\alpha,\beta}(A)=\alpha |A|^4+\beta(\det A)^2,
 \qquad b_* = 12+8\sqrt3,
\]

there exists a **closed homogeneous-quadratic two-form correction making the
compatible second-jet heat density pointwise nonnegative for some positive
constant scalar input-diffusion matrix** if and only if

\[
 \boxed{\alpha\ge0,\qquad -2\alpha\le\beta\le b_*\alpha.} \tag{R1}
\]

The same interval admits bilinear sum-of-squares certificates. Thus allowing
pointwise positivity beyond a Gram ansatz does not enlarge this particular
two-dimensional section. The proof includes an explicit four-square
algebraic endpoint certificate and a three-evaluation exact dual obstruction.
It is given in `SHARP_HEAT_BOUNDARY.md`.

Two rational checkpoints make the distinction concrete:

* `F25 = |A|^4+25(det A)^2` has the portable rational rank-eight certificate
  `F25_EXACT_HEAT_CERTIFICATE.json`, reconstructed exactly without a numerical
  eigenvalue premise.
* `F26 = |A|^4+26(det A)^2` has no correction in the entire quadratic
  closed-two-form class, for any positive constant scalar input metric.
  The exact obstruction is `b_*-26=8sqrt(3)-14<0`.

Both forms are already polyconvex. This does **not** refute heat-plus-polyconvex
universality, supply a non-QC example, determine the full heat cone, or show
that F26 actually increases along a heat flow. It is a sharp certificate-class
boundary inside a previously known QC class.

For isotropic heat, the same proof supplies an explicit linear separating
functional on the entire nine-dimensional invariant coefficient space:

\[
 \boxed{L(F)=(5+3\sqrt3)(p_0+p_1)+(1+\sqrt3)p_2
                      +(2+\sqrt3)p_3\ge0.}                \tag{R2}
\]

Here the coefficient order is defined in `ROC_CLASSIFIER.md`. This functional
is necessary for an isotropic quadratic closed-form heat certificate. It
does not remain a proved necessary condition for arbitrary anisotropic F
with an adaptively chosen input metric. F26 is bi-isotropic, which is why its
metric-independent exclusion follows.

Finally, `HEAT_PLUS_POLYCONVEX_DECISION.md` gives an exact first-order
real-algebraic formulation of **unrestricted** polynomial polyconvexity and of
the heat-plus-polyconvex inclusion question. It avoids identifying
polyconvexity with existence of a convex polynomial lift. This establishes
decidability in principle, without claiming a practical quantifier-elimination
run or an answer to the inclusion question.

## Inherited obstruction, not a rediscovery claim

Capital already refutes heat-only universality much more broadly at the
integrated-flow level. Read

`W/updates/FH/package/quartic/ASTRA_FULL_CONE_RIGIDITY.md:400-456`.

Its exact compatible periodic field is at lines 421-444; its symmetry argument
excluding all fixed real strongly parabolic constant-coefficient output-matrix
operators is at lines 446-450. The integrand is
`(det A)^2+10^-4|A|^4`, which is strictly coercive and polyconvex. This inherited
result cannot be promoted as a new contribution of this worker. It also does
not refute a sum of separately certified heat and polyconvex components.

## Supplied data reconstructed

I read the current N850 and N860 dossiers, the N850 all-background heat proof,
the N860 certificate-subtraction / output-average / elliptic argument relevant
to the cone question, and the final heat-cone suggestion in
`sources/mathematics_pasted.txt`. The pasted suggestion was treated as data.
No other current worker's mathematical outputs were read.

`verify_source_G.py` independently reads the immutable N850 JSON, checks its
SHA256 `4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000`,
reconstructs `Q=C S C^T`, all eighteen positive rational LDL pivots, closedness,
the Euler primitive, and the full compatible polynomial identity.
`SOURCE_G_EXACT_RECEIPT.json` records the six passing groups. Those checks do
not replace the separately read heat limit / density argument, and do not
independently audit N860's full critical-storage proof.

## Numerical discovery versus exact proof

`explore_isotropic.py` performed one finite sampled-jet SDP. Its reported
`optimal_inaccurate` status and value approximately 25.856404 were used only
to guess the algebraic endpoint. `ISOTROPIC_EXPLORATION.json` preserves that
unproved discovery status.

A separate floating scalar-extraction SDP for G reported
`optimal_inaccurate`, with a small positive value about `6.1e-5`.
`G_EXTRACTION_EXPLORATION.json` preserves that diagnostic. The exact acoustic
family above proves that the true value is zero.

The accepted claims use no finite grid or solver status: the endpoint identity,
positive diagonal Gram, rational F25 LDL, complete averaged correction space,
and three-evaluation dual are exact. `verify.py` checks them from explicit
formulas and the rational portable certificate. `exact_endpoint.py` and
`invariant_space.py` additionally preserve the symbolic construction and
complete linear-space calculation. The independent verifier can run with
plain Python and SymPy; CVXPY is only needed for the dispensable exploratory
script.

## Primary comparisons and remaining question

[Calderón, A note on biquadratic forms (1973)](https://doi.org/10.1016/0024-3795(73)90052-9)
proves the two-by-n nonnegative-biquadratic SOS theorem. The univariate matrix
formulation is also established in
[Hanselka and Sinn (2017)](https://arxiv.org/abs/1707.08261).
The exact eight-dimensional ROC lift is an application of that prior theory.

[Bruno and Pasqualotto, v1 (2026)](https://arxiv.org/html/2608.06367v1),
Sections 2-3, supplies the heat / exact-two-form strategy and the left-and-right
rotation-invariant QC theorem. The sharper section (R1) concerns the correction
cone rather than a new quasiconvex family; the forms in it were already QC by
elementary convexity and polyconvexity.

[Fantuzzi, Henrion, Kružík, Murali and Weis (2026)](https://arxiv.org/abs/2604.11124)
studies SOS sufficient conditions and moment methods for polynomial
polyconvexity. Proposition 2.3 already supplies the unrestricted support
characterization used here, and Proposition 2.4 exhibits a quartic without a
convex polynomial lift. Remark 2.1 leaves planar quartic PC versus SOS-PC
completeness open. The decision formulation is a standard corollary, not a
new polyconvexity characterization.

The targeted primary-source search did not establish priority for the exact
number `12+8sqrt(3)` or this three-jet dual. This is not a historical clearance.
External correctness, formal verification and novelty remain UNKNOWN.

The mathematically consequential unresolved target is still whether every
full left-SO(2)-invariant ROC quartic admits an admissible decomposition
`F=P+H`, with P genuinely polyconvex and H admitting a compatible-heat
certificate (or a specified positive sum of such components). The present
work supplies exact classifiers and a sharp calibration example; it does not
answer that target.
