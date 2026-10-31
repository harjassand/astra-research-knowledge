# Finite full-diffusion accuracy from one extra scalar resistance

Status: constructed and author-tested; separate whole review pending. The
accepted fixed-factor wrapper and all earlier sources remain unchanged.

## 1. Exact target and accepted mathematical premise

The input grammar, physical process, acquired full-fiber basins, global
nonexplosion/Gibbs law, exact raw receiving and q/MA/R0 integration are precisely
those of the source-bound accepted coupled-quartic consumer. The accepted
parallel theorem additionally gives, for alpha=m/4, a=1+kappa and
Delta(y)=a-v(y)>=0 on[-1/2,1/2],

  I_minus/I_plus <= k_full/k_free <=1,
  I_minus=int_-b^b (1-Delta/a)^alpha dy,
  I_plus =int_-b^b (1+Delta/a)^(-alpha)dy,
  k_free=1/(beta MA R0), R0=int_-b^b v^alpha,
  MA=int_b^infinity v^(-alpha).

This intermediate finite Jensen inequality is BEFORE the uniform slab-contraction
bound. It is not an appeal to the optional asymptotic theorem. It follows from
fiberwise weighted Cauchy, exact homogeneous energy pushforward, the Gamma
Laplace identity and Jensen; those proof operations do not need to be simulated.

## 2. Absorb all normalizing powers into one monotone scalar function

Since R0=a^alpha I_minus and
I_plus=a^alpha int_-b^b(2a-v)^(-alpha)dy, define

  R_plus = int_-b^b [a^2/(2a-v(y))]^alpha dy.

Cancellation gives the executable finite sandwich

  1/(beta MA R_plus) <= k_full <=1/(beta MA R0).           (F)

No unknown partition, Gamma function/integral, angular moment, conditional
sampler or PDE appears in(F). Both normalizations and the intermediate I_minus
cancel. The actual conditional process is not replaced by a Markov process.

On the half slab, v decreases from a and 2a-v increases. Thus the positive new
integrand is decreasing, just like v^alpha. Moreover

  a^2 - v(2a-v)=(a-v)^2>=0,

so R_plus>=R0. The additional structural width is the exactly defined scalar
ratio R_plus/R0. It is finite for every admitted finite m/kappa. It tends to1
under the separately stated fixed-profile large-alpha limit, but that limit is
not a premise of the finite computed result.

## 3. Outward exact operation and admission

At rational y the number r(y)=a^2/(2a-v(y)) is rational and positive. Since
alpha=m/4, r(y)^m followed by an outward fourth root gives an enclosure of the
new integrand. The accepted standard-library power/root algorithm is used under
the same precision and power/root-shift bit guard. There is no separate large
a^(2alpha) factor or uncharged transcendental evaluation.

An additional N-cell monotone Darboux sum on[0,1/2], doubled by evenness, gives
[L_plus,U_plus]. The original [L_M,U_M] and [L_0,U_0] are retained. The exact
full-rate output is

  [1/(beta U_M U_plus), 1/(beta L_M L_0)].                 (G)

All interval directions are outward. The supplied positivity checks make the
reciprocals legal. The optional requested_full_ratio is a strict Fraction>1.
If supplied, admission additionally requires the exact ratio of(G)'s upper to
lower endpoint <=requested_full_ratio. Failure is UNKNOWN, not a statement that
the true capacity is wide. It may reflect numerical resolution or inherent slack
in this finite Jensen lower bound; this method need not achieve every requested
accuracy. No claimed asymptotic limit silently replaces this exact check.

The caller supplies the external quadrature tolerance/budgets. The producer does
not secretly refine an unbounded computation to force the requested full ratio.
Its single additional sum uses the already acquired N and precision; if these
are insufficient it returns UNKNOWN. A new explicit request with finer tolerance
is a separately paid construction.

## 4. Work and strict receiving

The inherited producer is first rerun from ORIGINAL raw coefficients and the
external task. It pays axis/kappa/graph/coercivity/full-identity acquisition, all
mass and R0 arithmetic, tail/cutoff/grid search, and its unused old radial factor.
The new operation pays N+1 additional function evaluations and high-degree
powers/roots. Even though those coordinates coincide with existing R0 points,
they are conservatively charged as separate scalar evaluations: their budget is
max_points minus the inherited count. Refinement history remains included in
the inherited count. If the combined total exceeds max_points, it is UNKNOWN.

New diagnostic counters report added evaluations/power calls and the largest
new powered rational numerator/denominator. These are not whole-program peak
arithmetic or authenticated performance counters. The source-bound arithmetic
and all explicit budgets, not a claimed unit-cost real operation, underwrite(G).

The new verifier recomputes the entire inherited plus extra construction. It
strictly binds the source hash, method/schema, requested full ratio, external
original task/budgets, observable/basins, acquired raw model except timing,
cutoff/grid/precision/tail, exact full-ratio value and EVERY endpoint of all six
intervals. A stale radial factor field is rejected. Optional float displays,
timings and diagnostic work counts remain non-proof fields. The declaration is
finite-Jensen capacity/mass receiving, not signing arbitrary extra metadata.

No new raw grammar, arbitrary-coordinate recognition, physical calibration,
angular kinetics, sampler or first-hit-time assertion is added. The accepted
underlying model and the accepted parallel inequality are the exact join points.
