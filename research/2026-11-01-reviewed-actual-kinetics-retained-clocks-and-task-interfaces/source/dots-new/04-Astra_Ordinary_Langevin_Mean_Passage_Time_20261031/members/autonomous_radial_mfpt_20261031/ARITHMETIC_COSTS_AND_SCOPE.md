# Autonomous MFPT consumer: arithmetic, acquisition, comparison and boundaries

## What the finite operation actually predicts

The output is an exact interval for the autonomous mean time to Y>=1/2, from the
EXACT declared Gibbs law conditioned on Y<=-1/2 (or an exactly matching (Y,U)
initial pushforward), under the ACTUAL declared radial-gain tensor. It is not a
clamped experiment, a capacity/mass value, an arbitrary-start mean, or a claim
about the original constant-mobility model.

The mean is unbounded as a function of initial state. Small total-variation error
in an approximate sampler therefore does NOT automatically control mean error.
A future physical fixed-ray preparation service would need weighted initial-law
error or a Poisson-envelope/moment guarantee, in addition to scalar/Gamma/root
sampling and actuation costs. Nothing here implements such preparation. Computing
an exactly specified symbolic initial-law observable is legitimate without
physically sampling it; this distinction is part of the receiving contract.

## Raw input and inherited components

The raw input contains a complete rational homogeneous energy polynomial, a
complete-pair tangent generator program, and a canonical positive `radial_gain`.
The energy/tangent acquisition helper is imported only after checking its exact
accepted source hash. It checks all coefficients, exponents, dimensions, signs,
duplicates, pure coercive terms and resource limits. Its e1 energy evaluation is
explicitly renamed an ALGEBRAIC PROBE, not the physical initial state. The new
receiver binds the full raw hash INCLUDING the actual radial gain.

The backend requires p2 or4, integer alpha=m/p>=4, beta,kappa>0, and b=1/2.
These are sufficient receiving premises, not recognition of arbitrary positive
polynomials or arbitrary supplied mobility matrices. The tangent program is a
succinct exact formula, not an uncharged reconstruction of an m-by-m matrix.
All 523,776 exponent entries in each 512-fiber-dimensional example are scanned;
the full raw program is hashed. Neither an angular sampler, angular partition,
committor, planner nor cumulative tail-integral oracle is assumed.

## Two paid scalar integrals and finite infinite-tail control

Only M=int_(1/2)^infinity v^-alpha and R=int_(-1/2)^(1/2) v^alpha are numerically
integrated. The proof derives the full Poisson-current and basin-source corrections
analytically. In particular, using M/R does not inherit a capacity certificate's
observable label or silently assert T=1/k.

Positive rational bases are rounded outward at scale 2^P. Integer powers use
binary exponentiation, with every multiply rounded downward/upward. Work is
O(log alpha) guarded integer multiplications per distinct scalar point. The
integrator splits at the known turning point1: q increases on[1/2,1], decreases
on[1,infinity], and v^alpha decreases on[0,1/2]. Left/right endpoint Darboux sums
are therefore exact enclosures. Adjacent doubled grids share cached evaluations.

For T>1 the ENTIRE remaining mass satisfies

    int_T^infinity v^-alpha
      <= T/(4alpha-1) * [kappa(T^2-1)^2]^(-alpha).

Its integer-power evaluation is rounded upward. A positive seed on[1,5/4] must
be resolved before cutoff search. Cutoff doubling, grid doubling, total scalar
points, total fixed arithmetic operations, precision and product sizes all have
finite external budgets. Unresolved precision/tail/width yields UNKNOWN.

The numerical product Mhi*Rhi/(Mlo*Rlo) must first meet1+quad_relative. The extra
positive constants a^alpha,v(1+d)^alpha,a^(alpha-3),a^-alpha are independently
rounded outward. The new Poisson formula then evaluates each upper correction
with Mhi or Mlo in the appropriate direction. Only after that does the verifier
check the externally requested TOTAL high/low ratio. Numerical width and the
sufficient current's structural width are distinct. A miss is not a theorem that
the physical mean cannot be more accurately predicted by a stronger method.

A known radial gain that fails even the sufficient slab-factor gate can be
refused before quadrature. Gamma is not optimized or changed behind the user's
back. It remains part of the original actual raw model in every replay.

## Exact resource semantics

All task rationals are Fraction values and all budget integers are strict ints;
bool/float aliases are rejected. Resource types are validated before they are
used in comparisons, allocation or input acquisition. Raw rational bit/string
limits, dimension/term/exponent-entry limits and total energy-coefficient bits
are inherited and enforced. Initial e1-probe Fraction products/additions use
conservative bit prechecks. The energy coefficient-bit counter does not include
every other input field; radial-gain and tangent-weight parsing are additionally
paid and capped by the individual coefficient budget.

`fixed_operations` counts the guarded fixed-point products, including constants
and tail evaluations. `largest_guarded_product_bits` is a product-operand bound
proxy, NOT total peak memory, every rational intermediate, input storage or
serialization. Monotone sum additions and other bounded Fraction operations are
also ordinary computational work. Exact rational serialization can return an
explicit UNKNOWN at Python's finite digit limit; optional float displays may be
null. Display conversion never determines an endpoint or acceptance.

The receiver recomputes every raw and scalar step from the external ORIGINAL
task, and strictly binds all proof fields, the actual generator, exact initial
law, scope/exclusions, correction terms and rational endpoints. Work/timing and
floating displays remain explicitly non-proof diagnostics.

## Executed cases and strongest alternatives

At beta=kappa1 and DECLARED gamma512, the accepted-candidate calculations give:

| Fiber dimension | alpha | Lower mean | Upper mean | Total ratio |
|---:|---:|---:|---:|---:|
|64|16|6.654988858e3|6.870103838e3|1.032323868|
|128|32|2.146778293e8|2.156937488e8|1.004732298|
|256|64|4.567286514e17|4.584412274e17|1.003749657|
|512|128|4.192892844e36|4.209577975e36|1.003979384|

The full autonomous physical state also has the longitudinal coordinate, so the
last line is513-dimensional. The two 512-fiber-dimensional raw models with
interaction/tangent strengths(20,1) and(10^100,10^80) produce identical exact
mean intervals, not only similar rounded displays. Each uses98,306 scalar
points,98,311 power calls and1,671,295 guarded products, about2.8s per producer
run in this workspace. Complete verification executes the work again. Timing
is diagnostic, not a controlled benchmark; input fixture generation and test
construction are separate paid work, not hidden in a dimension-free oracle.

The scalar integral acquisition is straightforward ordinary interval quadrature.
The enabling mathematical step is the constructed finite-resistance Poisson
source current and its actual initial-law/hitting-time join. Conventional
variational/current methods supplied this same current reproduce every bound.
Do not count that as an independently located prior construction, and do not
claim a proprietary algorithmic separation. Historical priority is unresolved.

Ordinary Gaussian radial/CIR reduction gets the same information and scalar
engine; a matched-alpha Gaussian/quartic pair is explicitly tested. An ordinary
2D Poisson solver gets the same exact generator and initialization. No numerical
claim that it loses is made: the current construction avoids having to assume
such a solved PDE as an input and gives a separate rigorous outer certificate.
Direct ordinary scalar Poisson averaging supplies the lower variational trial,
not an exact full mean unless its receiving conditions are separately proved.

Actual radial control, state-dependent noise, the mandatory divergence drift,
large-gamma bandwidth/stiffness, energy readout, physical model identification,
and initialization apparatus are not implemented or free. The formula predicts
a declared mathematical generator; it does not demonstrate that real matter
has been made to implement it.

## Preserved construction failures, not erased successes

Before freezing, a resource-validation ordering issue was noticed by the author:
`max_coefficient_bits` was used in a comparison before its strict type check.
It was repaired before any accepted receiver freeze; all resource aliases,
including None, are now tested. A first symbolic test compared expanded and
factored SymPy expressions structurally rather than comparing their expanded
difference to zero; that test assertion failed and was corrected. Neither was
a mathematical counterexample to the Poisson-current proof. The first production
cases were subsequently fully replayed against the final source.

True retained UNKNOWN cases include gamma1 with a requested1.01 sufficient bound,
alpha16 with a requested1.01 full interval, noninteger or alpha<4 backend scope,
unresolved precision, explicit numerical budgets and malformed raw controls.
No operation was denied or left uncertain in this construction. Earlier accepted
sources/archives remain unchanged. Broader radial-compliance ideas are outside
this freeze and cannot be inferred accepted from these tests.
