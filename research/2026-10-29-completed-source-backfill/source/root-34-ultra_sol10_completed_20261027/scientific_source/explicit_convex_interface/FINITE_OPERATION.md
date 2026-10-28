# A fixed finite convex operation, with rational query certificates

The target here is the accepted old rational-selector quartic F from
`sol8_opportunity_selection_20261027/rational_selector/PROOF.md`, with
W_epsilon=F+epsilon|A|^2. It is already PC/QC and has no polynomial global
minor-support selector. The newer ROC/non-PC Hopf quartic is a different
target. This operation gives no new PC or QC conclusion for that target.

For y the 70 moments through degree four in four real variables, let
M2(y) be the 15 by 15 moment matrix indexed by monomials of degree at most
two. The finite convex representative is the standard moment program

    G(B,s)=min L_y W_epsilon
       subject to M2(y)>=0, y_0=1, L_y A=B, L_y det A=s.       (1)

The use of moment/SOS semidefinite programming is established machinery,
not a new general optimization algorithm. Root's independent analytic
proof and primary-source comparison are in
`../parent/finite_moment_interface/PROOF.md`. It proves target graph
equality for (1), finiteness, attainment, and the corners described below.
Those conclusions do not depend on the numerical query acquisition.

## Exactness, compactness, and an explicit interior Gram

For each FIXED nonzero base A, the accepted R180 certificate divided by
the constant |A|^4 is an SOS in X for the support remainder

    F(A+X)-F(A)-DF(A):X-k(A)det X.

Its rational dependence on the parameter A is immaterial to fixed-A
moment dual feasibility. At (A,det A), this support gives the lower bound
W_epsilon(A); the Dirac moments give the matching upper bound. Zero is
covered by F itself being SOS. Every (B,s) is feasible using two actual
graph atoms B+/-Y, det Y=s-det B. Coercive quartic SOS domination bounds
all 70 moments on an objective sublevel set by PSD Cauchy-Schwarz, so the
minimum is attained. No flatness/atomic-recovery assertion is required.

There is also a small literal interior Gram. In the old feature ordering,
the ten features A_0^2 X_i X_j occupy indices80:90. Fix A=e_0 and take the
degree-four-in-X part. The corresponding 10 by 10 principal Gram G_F
satisfies exactly

    F(X)=z_2(X)^T G_F z_2(X),       G_F>I/400000.             (2)

The code independently reconstructs every quartic coefficient from this
principal block and verifies positivity of G_F-I/400000 with exact
Fraction LDL. Consequently F-|X|^4/800000 is SOS: the sum of squares of
the ten degree-two monomials is at least |X|^4/2. This strengthens the
uniform-in-base floor1/1600000 used in the generic proof. For epsilon>0,

    diag(1,epsilon I_4,G_F)

is an explicit positive-definite Gram for W_epsilon+1 in the full
15-feature basis. It supplies the interior dual point used in recovery.

## Exact rational certificates after a numerical suggestion

`acquire_moment_interface.py` solves (1) with CLARABEL, but retains no
floating PSD premise. It rounds the 70 primal moments and the dual Gram
and multipliers to denominator2^40, then corrects all affine identities
exactly. To move into the interiors it uses:

- Primal: a Gaussian with the same mean and determinant expectation.
  Writing delta=s-det B, its rational covariance has diagonal
  |delta|+1, cov(a,d)=delta/2, cov(b,c)=-delta/2, and all other off-diagonal
  entries zero. It is positive definite and has full support. Isserlis
  moments through degree four are reconstructed exactly.
- Dual: the explicit interior Gram above, corresponding to constant
  affine lower bound-1.

The code tries rational mixing weights, and accepts one only if all
exact Fraction LDL pivots are positive. The corrected dual identity is
checked coefficient by coefficient for all 70 monomials. For a rational
query this yields exact rational lower and upper objective bounds by
ordinary weak duality. It does not turn a solver status into a theorem.

`certificates/` contains all moment vectors, Gram matrices, multipliers,
and rational rescalings. `verify_moment_brackets.py` is a separate
standard-library-only consumer. It imports neither the acquirer nor a
solver, NumPy, or SymPy; it reconstructs the literal target, all affine
equations, all polynomial identities, PSD tests and endpoints.

Root separately consumed all 22 certificates using literal SymPy
coefficients and integer Bareiss Sylvester tests in
`../parent/finite_moment_interface/independent_consumer.py`. This is a
substantive independent acceptance of the saved rational query bounds,
in addition to root's analytic exactness proof.

## An ordinary control in all five variables

For the ordinary target W_0(A)=|A|^4+epsilon|A|^2, the same moment program
has the exact closed form

    tau(B,s)=|B|^2+2|s-det B|,
    G_0(B,s)=tau(B,s)^2+epsilon tau(B,s).                    (3)

Indeed the centered covariance is PSD and its trace is at least
2|L det(A-B)|=2|s-det B|. Thus L|A|^2>=tau, and moment PSD also implies
L|A|^4>=(L|A|^2)^2. These give the lower bound. For the upper bound,
choose Y in the conformal two-dimensional subspace if s-det B>=0, or
the anticonformal subspace otherwise, with det Y=s-det B and B:Y=0.
Such a Y exists because one linear orthogonality condition leaves a line
in either subspace. It has |Y|^2=2|s-det B|. The two atoms B+/-Y have
constant |A|^2=tau, correct mean, and correct determinant expectation.
They attain both lower bounds. Thus (3) holds even though general
truncated feasible moment vectors need not represent measures.

All 11 saved ordinary-control cases enclose (3) exactly, testing mean,
determinant, sign, physical scaling and quartic coefficients together.

For the actual old F, four nonzero zero-mean slice cases enclose an
independently reconstructed rational bisection interval for

    min_x[p0 x^2+Lsx+(2p0+p2)s^2
                         +epsilon sqrt(x^2+4s^2)].           (4)

The other three formula controls are graph equality. The four generic
nonzero-mean off-graph cases have exact primal/dual bounds, without a
separate closed-form value formula.

## Measured values, conditioning, and cost scope

For epsilon=1/100, representative old-F values are

| B, row-major | s | exact certified interval, decimal display |
| --- | --- | --- |
| (0,0,0,0) | 1 | [0.18506766443719525,0.1850676765651496] |
| (1,0,0,3/4) | 5/4 | [0.33248233790550596,0.3324824730824276] |
| (1,0,0,3/4) | 1/4 | [0.06725477478690621,0.06725478564378033] |
| (3/5,-1/5,3/10,9/10) | -2/5 | [0.11378912254170159,0.11378914118694647] |

The exact rational endpoints, rather than the decimal renderings, are in
`MOMENT_EVALUATIONS.json`. All22 brackets passed the independent consumer;
18 have the formula controls above. The widest old-F bracket is about
1.36e-7. Floating moment/Gram eigenvalue ratios reach about1.11e13 and
4.83e12 respectively; these are conditioning diagnostics, not proof
premises. Several solver statuses are `optimal_inaccurate`; the rational
certificates establish the reported intervals independently.

The first saved 22-query acquisition took0.657603s after imports, symbolic
coefficient setup and the interior-Gram check. This includes0.140212s in
solver calls and0.488026s in exact repair, with the remainder in query
construction, serialization and loop overhead. The saved JSON field
`full_acquisition_seconds` refers to this query cycle; it excludes startup
and should not be interpreted as a full fresh-process cost. Our separate
standard-library consumer took0.0885795s after imports. Root's independent
Bareiss consumer reported0.039s after imports. Shared-host timings are
acquisition records, not an efficiency advantage or a hardware benchmark.
The acquisition of the old R180 certificate is a charged prior input,
documented in its original files; it is not free work erased by (1).

## What this completes and what remains open

This is a fixed finite SDP operation with explicit coefficient data and
reviewable rational query certificates. It acquires a global convex
representative beyond every scalar polynomial lift. Generic moment/SOS
machinery retains prior credit; a semidefinite solver remains part of the
operation and its cost is charged. This is not an elementary closed
formula or a universal efficient evaluator theorem.

It does not meet the smooth-interface target. For epsilon>0 the value has
corners at EVERY graph point: the accepted strict SOS support remains
dual-feasible for an interval of determinant slopes

    k(A)+zeta,       |zeta|<=2(epsilon+|A|^2/2400000).

Distinct slopes yield distinct touching subgradients. At zero the simpler
bound G(0,s)>=2epsilon|s|+4s^2/800000 already proves a vertical cusp.
Unique primal Dirac moments at graph points do not imply differentiable
value dependence. The smaller `conv(h)` construction is smooth on a
graph neighborhood but retains an unevaluated convexification. A directly
evaluable globally convex smooth representative remains NOT_ACQUIRED.
