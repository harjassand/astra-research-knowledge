# Ordinary constant-SPD MFPT: receiving, costs and limitations

## Actual capability

This is a full-state ordinary Langevin mean hitting-time prediction, not a
capacity label, a clamped CIR terminal law or the previous engineered mobility.
The actual initial law is EXACT FULL Gibbs conditioned on Y<=-1/2. The receiver
neither samples that law nor authenticates physical parameters. A fixed ray with
the same energy distribution is not equivalent; small total-variation error in
finite-bit preparation does not control this unbounded mean. The full initial
law remains a substantive mathematical input.

The predicted interval is common to many admitted models, not a claim that their
actual means coincide. In particular the two 513-dimensional examples with
coupling20/isotropic64 and coupling10^100/diagonal(64,128,...,32768) have identical
exact endpoints because their acquired d_min and mobility floor agree. Their
energy need not be Markov and their angular relaxation need not be identified.

## Acquisition, not a hidden matrix or positivity oracle

Raw input is the complete energy polynomial plus a constant-isotropic or
constant-diagonal mobility program. Every exponent/coefficient and every actual
mobility value is checked. Signs, pure coercive terms, homogeneous degree4,
duplicates and exact canonical rationals are verified. Integer alpha=m/4>=4 is
the first finite backend's scope, not an arbitrary-polynomial recognition claim.
The theorem admits dense SPD matrices if a floor is acquired; this executable
does not. Diagonal mu is the exact minimum, isotropic mu is its supplied positive
value. Unit longitudinal mobility and zero cross mobility are part of the actual
model interface, not inferred from observations.

The prior energy grammar is imported by a checked source-hash chain. A synthetic
zero tangent and e1 witness are used ONLY to reuse its energy/coercivity parser;
all tangent/lift/initial-state claims are removed from the resulting acquisition.
The e1 value is explicitly an algebraic probe, never a physical initialization.
The whole actual raw object, including mobility, is hashed and bound.

The inherited Scalar implementation is source-pinned to the earlier frozen
radial MFPT receiver. Only its ordinary directed arithmetic and M/R integration
are reused; no earlier actual-model or observable certificate is imported. Its
whole review was pending at this construction freeze. Acceptance of either
model requires its own full proof and receiving review.

## All scalar costs and infinite tails paid

The only integrals are M=int_(1/2)^infinity v^-alpha and
R=int_(-1/2)^(1/2) v^alpha. Fixed dyadic outward binary powers take O(log alpha)
guarded products per scalar point. Endpoint Darboux sums are valid after the
known monotonicity splits at1 and0. Cached points are reused across doubled
grids. The ENTIRE mass beyond T is bounded by

    T/(4alpha-1) * [kappa(T^2-1)^2]^(-alpha), T>1,

with its power rounded upward. A resolved positive seed precedes the finite
cutoff search. Grid, total points, fixed products, cutoff, precision and input
sizes all have explicit finite budgets. The analytic Poisson basin bounds
replace an inner cumulative integration; no cumulative oracle is supplied.

Two additional positive square roots bound C_s and D_max. Perfect rational
squares are returned exactly. Otherwise the numerator is scaled by2^(2P),
divided downward, integer square-rooted and incremented, yielding a strict upper
bound divided by2^P. Argument and scaled-integer bit limits are checked before
allocation. Tests compare these roots to exact rational squared inequalities.
The root-call count is fixed, but integer operand sizes depend on P, which
in turn depends on alpha and kappa. Root bit-complexity is paid and is NOT
independent of dimension. The unit-parameter examples happen to use perfect
rational square roots; that does not justify a general dimension-free bit cost.

The producer first enforces the requested NUMERICAL M/R product width, then
substitutes outward M/R/constants into the full mean formula and enforces the
original TOTAL high/low ratio. Structural slack is not numerical quadrature
error. Failure is UNKNOWN, not an impossibility or physical accuracy floor.
A sufficient current factor already larger than the request is refused early;
the actual mobility is never changed to make the request succeed.

All task rationals are exact Fraction and budgets strict positive ints. Input
coefficient-bit accounting includes energy and mobility. `fixed_operations`
counts guarded dyadic products, not all Python additions/divisions. The reported
largest product and root integer bounds are explicit proxies, NOT total peak
memory or every Fraction intermediate. Those remaining operations, raw storage,
fixture generation, hashing, rational serialization and verification still cost
ordinary time/space. Serialization can return UNKNOWN at Python's finite digit
limit; overflowing optional float displays are null and do not determine proof.
Verification repeats the complete acquisition and numerical computation from
the external original task; it does not trust certificate-provided controls.

## Actually executed cases, beta=kappa=d_min=1

| Fiber m | Actual mobility floor | Lower mean | Upper mean | TOTAL ratio |
|---:|---:|---:|---:|---:|
|512|1|4.192892844e36|5.270364770e36|1.256975784|
|64|64|6.654988858e3|6.999720488e3|1.051800482|
|128|64|2.146778293e8|2.160844595e8|1.006552284|
|256|64|4.567286514e17|4.588073011e17|1.004551170|
|512|64|4.192892844e36|4.212934896e36|1.004780006|

The original ordinary unit-mobility case is retained as the first line; no
claim that it has sub-one-percent accuracy is made. Increasing transverse
mobility relative to the fixed longitudinal clock changes the actual model,
not merely numerical accuracy or the overall time unit.

Each 512-fiber example scans1023 terms and523,776 exponent entries. Its producer
uses98,306 scalar points,98,310 power calls,1,671,270 guarded products and two
roots; tracked product bound1154bits. Production was roughly2.5--2.8 seconds
here; verification repeats it. This is a diagnostic timing, not a controlled
benchmark or a claim about an optimized PDE implementation. Serialized raw
bytes and fixture-generation time are recorded separately in each result.

The author suite passed3,678 checks and replayed all six actual cases. It includes
full-z continuity, global Lyapunov/global correction identities, a nonconvex
admitted energy, equal-energy nonclosure witnesses, exact finite-chain
source-to-mean checks, rational root/power/Darboux comparisons, complete exact
polynomial integration of every saved R, corrupted model/task/initialization
rejections, strict type and finite-budget failures. High-precision M integration
is diagnostic only, never a proof premise.

## Retained failures and strongest ordinary alternatives

Unit mobility with requested1.01 returns UNKNOWN from this sufficient bound;
alpha16/m64 with that request also misses. Invalid or absent actual mobility,
zero/negative diagonal entries, the old radial-gain model, degree2/noninteger
alpha/alpha<4, incomplete positivity, resource exhaustion and substituted
initialization are rejected. An initial author build was run from the wrong
working directory and failed with FileNotFoundError before creating its code;
the explicit correct workspace directory fixed that ordinary execution error.
No permissions denial or uncertain external operation occurred here.

The general variational mean-exit machinery already exists; see the primary
comparison ledger. The assembled source current/full-tail/initialization
certificate is the useful local result, not a new generic solver invented by
renaming existing mathematics. Ordinary current/Poisson methods given this same
proof reproduce it. Gaussian radial closure is a strong special case but does
not carry over to generic coupled quartics, as exact nonclosure tests show.
The full elliptic PDE, verified barrier, simulation and averaging alternatives
get identical model/initial-law information; no universal runtime superiority
or historical novelty has been established. Physical membership, parameter
accuracy, full Gibbs preparation and implementation remain unearned.
