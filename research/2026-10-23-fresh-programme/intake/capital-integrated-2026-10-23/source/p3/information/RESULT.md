# Bounded candidate: acquiring a response without identifying a whole operator

Branch: ASTRA-FRESH-20261023 P3. Internal independent collaborator.
Corpus read: `00_START_HERE.txt` at
`e606bfc587c76bdcae8b8fa3ec33e721efa2fbac`.

## Decision

Do not promote this candidate as a new scientific primitive. The attractive
noiseless construction is established Gauss/Lanczos quadrature, and targeting
experimental designs at quantities of interest is established. No comparative
advantage over those equally informed methods has been demonstrated. The
useful retained material is an explicit acquisition contract and a noise
obstruction that prevents an artificial advantage from being claimed.

## Concrete scientific task

A positive definite self-adjoint linear response operator `A` governs a
discretized stable physical system. A forcing `b` is supplied. Estimate the
compliance/susceptibility `q = b^T A^{-1} b` to prescribed relative accuracy.
The matrix is unknown, and physical directional experiments return `Av` with
error. Such an experiment is not a free exact matrix-vector product.

The concrete oracle considered here returns `y(v) = Av + e(v)` with
`||e(v)|| <= delta ||v||`. The error can be persistent calibration bias.
The experiment can choose `v`; all amplitudes and observations are charged.
An externally justified coercivity bound `A >= mu I` is required by the
certificate below. It is not inferred from Ritz values.

## Retained proposition 1: robust one-action certificate

Let `x` be any proposed solution, let one experiment return `y = Ax + e`,
and suppose `||e|| <= eta`. Write

`F = 2 b^T x - x^T y`, `rhat = b-y`.

Then

`max(0, F - eta ||x||) <= q`

and

`q <= F + eta ||x|| + (||rhat||+eta)^2/mu`.

Proof: completing the square gives

`q = 2 b^T x - x^T A x + (b-Ax)^T A^{-1}(b-Ax)`.

The first two terms equal `F + x^T e`; the final quadratic term is
nonnegative and is at most `||rhat+e||^2/mu`. Cauchy-Schwarz and the triangle
inequality give the stated interval. The positivity lower bound follows from
positive definiteness. No convergence claim about the method that produced
`x` is needed. For the relative oracle, take `eta = delta ||x||`.

This is a straightforward energy-residual bound, not a novelty claim. It
exposes exactly where the independent stability information enters.

## Retained proposition 2: persistent-noise acquisition obstruction

Even in dimension one, no number of adaptive oracle calls removes persistent
operator error. Assume `0 < mu`, `0 < delta`, `mu+2delta <= 1`, `b=1`, and
`a` is known only to lie in `[mu,1]`. Two admissible physical systems are

`a0=mu`, `a1=mu+2delta`.

Both produce the exact same complete adaptive transcript if the oracle
always returns `y(v)=(mu+delta)v`. Its error under each system is bounded by
`delta |v|`. Randomization does not distinguish identical transcript laws.
Their responses are `q0=1/mu`, `q1=1/(mu+2delta)`.

Every estimate therefore has worst-case absolute error at least

`delta / [mu (mu+2delta)]`.

The minimax relative error over these two worlds is exactly

`delta/(mu+delta)`.

Indeed, the optimal common estimate equalizes relative errors and is
`z=2 q0 q1/(q0+q1)=1/(mu+delta)`. Consequently a uniform relative-error
target `eps` requires `delta <= eps*mu/(1-eps)` even before computational
cost is considered. Without a positive lower bound on `mu`, there is no
uniform relative guarantee at fixed nonzero operator error.

This elementary two-world proof should not be described as a new lower bound
in the numerical-analysis literature. Its role here is to rule out the
candidate's uncharged exact-acquisition premise.

## Closest primary predecessors read

1. Chengtao Li, Suvrit Sra, Stefanie Jegelka. *Gaussian quadrature for matrix
   inverse forms with applications*, ICML/PMLR 48 (2016), 1766–1775.
   https://proceedings.mlr.press/v48/lig16.html
   Primary abstract explicitly states Gauss-based retrospective lower and
   upper bounds and monotone geometric tightening. This is the strong
   equally informed baseline, not dense matrix reconstruction.
2. Ahmed Attia, Alen Alexanderian, Arvind K. Saibaba. *Goal-Oriented Optimal
   Design of Experiments for Large-Scale Bayesian Linear Inverse Problems*.
   arXiv:1802.06517v2 (2018).
   https://arxiv.org/abs/1802.06517v2
   Their design optimizes posterior uncertainty of a final quantity of
   interest rather than all inferred parameters. Thus that strategic choice
   alone is established.
3. Gene H. Golub and Zdenek Strakos. *Estimates in quadratic formulas*,
   Numerical Algorithms 8 (1994), 241–268.
   https://doi.org/10.1007/BF02142693
   Retrieved abstract treats Gauss-type bounds for inverse quadratic forms
   and rounding error. Full proof not reviewed here.

## Remaining question and recommendation

A worthwhile extension would need a specific physical acquisition interface
whose noise is reducible and whose experiment-time/precision cost can be
optimized jointly with response computation. It must beat robust inexact
Krylov/Gauss-Radau procedures with the same data and the same coercivity
information. No such advantage is established in this bounded investigation.
This route is lower priority than a construction that actually removes a
verified acquisition or variance bottleneck. Novelty: UNKNOWN for possible
future refinements; the obvious core is established prior art.
