# Algebraic-logarithm determinant audit: column cutoffs do not remove the 2d wall

Date: 2026-10-09 UTC. Internal research note. No novelty, priority, or external-validation claim.

## Scope and source pin

Target: the rational approximation exponent of x=log(alpha), alpha>0 algebraic, alpha!=1, degree d. The current candidate proves mu(x)<=2d from the moving-center interpolation (MI) input and the family-017 determinant architecture. This note tests a natural improvement: choose the nonzero maximal minor only among lower-degree columns to reduce the algebraic norm cost.

Exact primary source 017 read locally: OpenAI/math commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, path `preprints/The-irrationality-exponent-of-pi-is-2-September-24-2026/build/`; source files are mirrored in `/workspace/shared/astra_programme/number_theory_bridges/sources/017_*`. Local SHA256 values from `SOURCE_MANIFEST.json`: main `957ce6c2cf4b084693273cc4a8987b374de74bc91b25f5b8da8986504811e123`, interpolation `2d921105cd7f8adfba1f1567a14922095678dcde49c5d1cf42c4dd9bbc02fdf`, determinant `b67cef106951b37fbbd901e276cc3772b63ae27e0df395cf12caf1834a6b9921`. Exact primary moving-center input also appears as Theorem 2 in Liu–Jiang–Zhang, arXiv:2610.10192v1, whose local primary text is `/workspace/shared/astra_programme/algebraic_log_audit/2610.10192v1_primary.txt`.

The task indicated Astra commit `99a9d763558c3c7d329d3bdeb64905187cb5429c`; direct web opens for its raw router/start files returned cache misses, so this note does not claim to have independently re-read that latest upstream pin. The local Oct-8 route was only used as context.

## Proposed refinement

Let theta be the transverse row ratio, so row indices satisfy `v0*s + w·beta/theta < H`. Instead of using all polynomial columns of W-degree at most H, restrict columns to degree at most `tH`, where `theta < A < t < 1`, and use MI with

- `W' = W/t`,
- `theta' = theta/t`,
- the same jet weights `V=(v0,w_i/theta)`.

This is a valid rescaling: `W'_i/theta' = w_i/theta`, and MI's volume condition becomes

`K*w0*theta^m/(v0*t^(m+1)) < 1`.

With volume ratio 1/2, take `v0 = 2*K*w0*theta^m/t^(m+1)`. Surjectivity then gives a full-row minor whose columns all have original W-degree at most `tH`. The q-denominator part of the arithmetic lower bound improves from the coarse main cost `d(1-bbar)` to `d(t-bbar)`, where `bbar=(MH)^(-1) sum_rows w·beta`.

For rows indexed by transverse multi-indices `a`, the collision argument still has

`L = eta^2*K*theta^m / ((m+1)*v0*A^m)
  = eta^2*t^(m+1) / (2*(m+1)*w0*A^m)`.

With the standard exponential schedule `K≈C^m`, `w0=B^(-m)`, the collision term can grow while the fixed embedding errors vanish only if one can choose

`A/t < B < min(1/C, C*theta/t)`, with `A/theta < C < t/A`.

Thus a necessary geometric condition is `A^2 < theta*t`. This is the cutoff analogue of the original `A^2<theta` condition.

The high-index analytic branch must beat the norm lower cost, requiring (as `eta→0`)

`nu*(A-theta) > d*(t-theta)`.

But `A^2<theta*t` implies

`(t-theta)/(A-theta) > (A+theta)/theta = 1+A/theta > 2`.

Therefore this rescaled-minor strategy still requires `nu>2d`. The smaller arithmetic cost is exactly offset by the wider degree range needed for a collision saving. This is a mechanism-specific barrier, not a theorem ruling out other determinant constructions.

## Check using the exact row average

A possible finite-dimensional loophole is that the candidate only uses `0<=bbar<=theta`. For fixed m and H→∞, lattice-point averaging actually gives

`bbar -> theta*m/(m+2)`.

For fixed parameters, the high-branch gap is

`g_m = nu*(A*(1-eta)-theta*m/(m+2)) - d*(t-theta*m/(m+2))`.

At eta=0, its limit as m grows is `nu*(A-theta)-d*(t-theta)`, already negative for nu<2d by the cutoff condition above. Allowing parameters to drift with m gives an extra finite-m term `(nu-d)*2*theta/(m+2)`, but only O(1/m).

For schedules drifting to the endpoint with `theta` bounded away from zero, the maximum possible collision base obeys

`L < eta^2*t/(2*(m+1)) * (sqrt(theta*t)/A)^m`.

When `A-theta=O(1/m)`, positivity of the high-branch gap forces `eta=O(1/m)` and `t-theta=O(1/m)`. Beating the arithmetic cost (which is at least order `t-bbar`) then requires polynomial growth of the base, hence `log(sqrt(theta*t)/A) = Omega(log(m)/m)`. Expanding near theta gives `t-theta >= 2*(A-theta) + Omega(log(m)/m)`. The resulting negative `-d*Omega(log(m)/m)` dominates the row-average bonus O(1/m) whenever nu<2d. This closes the tempting exact-average escape for this endpoint schedule; it is not a universal no-go beyond it.

## Status and next mathematical gap

The cutoff-minor approach has not produced a degree-free exponent. It explains, within the present one-parameter Taylor-collision architecture, why lowering the arithmetic column cost recreates the factor two in the collision-volume constraints. A successful route below 2d must change a different interface: e.g. obtain determinant-specific arithmetic savings over the norm, or an analytic mechanism that suppresses high transverse terms at nonmatching embeddings without paying the same height cost. No such mechanism is proved here.

The original candidate's full 2d proof remains a source-dependent research proof already independently audited in `../astra_programme/algebraic_log_audit/COMPARISON_AND_VERDICT.md`; this note neither upgrades its status nor certifies family 017.
