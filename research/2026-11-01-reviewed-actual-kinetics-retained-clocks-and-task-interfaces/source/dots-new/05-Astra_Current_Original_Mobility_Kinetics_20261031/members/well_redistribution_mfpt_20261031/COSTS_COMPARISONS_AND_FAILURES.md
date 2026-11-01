# Original unit-mobility MFPT: acquired current, costs and boundaries

## Useful actual consequence

For the SAME ordinary constant-mobility Langevin model, the new current earns
sub-one-percent mean-passage accuracy at513 total dimensions with M_z=I. It does
not increase transverse mobility, change time units or physically redistribute
energy. Redistribution is the choice of a mathematical Poisson-source witness.

The target is EXACT FULL Gibbs conditioned on Y<=-1/2, and target arrival is
Y>=1/2. An angular sampler, fixed-ray initialization, empirical force/mobility
identification, physical parameter accuracy and finite-bit preparation are not
provided. Complete symbolic model receiving is not microscopic physical
reconstruction. Equal output intervals across different models do NOT imply
identical true means or energy-Markov dynamics.

## Hard step and scope of reuse

The earlier conditional current followed the changing fiber law throughout the
rare transition region, incurring an O(1/mu) slab correction. The new A-current
carries the fixed barrier fiber law through that slab and redistributes the
source within the well. Its explicit radial density homotopy has a bounded norm
proved without evaluating a fiber Poisson solution or the unknown angular
normalizer. The longitudinal current is continuous at the patch interfaces;
transverse jumps do not create a hidden divergence source.

The S-current is separately constructed. Q_S<=eta^2 B_new is NOT asserted.
Instead Q_S<=beta M_S^2 R(1+C_s), followed by a valid source Cauchy/AM-GM join.
This is what turns a parallel-slab resistance into an actual full-initial-law
mean. A previous capacity or mean label is not reused as the proof.

## Raw acquisition and all execution costs

The unchanged, hash-pinned accepted constant-SPD parser scans the entire exact
positive quartic energy program and the positive isotropic/diagonal mobility
program. It earns degree, alpha, d_min, coercivity and the actual mobility floor.
The exact model includes unit longitudinal mobility and zero cross mobility.
The theorem permits dense SPD matrices with an acquired floor, but this backend
does not recognize them. Integer alpha>=4 remains an explicit finite-backend
scope, not arbitrary positivity/homogeneity recognition.

M and R use the already reviewed directed dyadic-power/monotone Darboux code.
ONE additional profile R_plus=[vstar^2/(2vstar-v)]^alpha is integrated on the
same finite slab. Its denominator is positive, its monotonicity is proved, and
its points share the SAME cache/total-point and arithmetic budgets. The mass
tail still receives an analytic full-infinity enclosure; a positive seed, cutoff,
grid, precision and all loop budgets remain required. No nested cumulative mass
integral or homotopy integral is numerically supplied as an oracle.

Outward powers of G_b,G_1,a_b^-1 and three positive-root calls receive the
explicit well/moment constants. Root call counts are fixed but operand sizes
and bit complexity can grow with dimension, parameters and chosen precision.
All terms of source-A, source-S and their cross contribution are rounded in the
safe direction before the original TOTAL high/low request is checked. The old
O(1/mu) slab-factor gate is deliberately absent for the NEW A-current; that factor
now belongs only to the separately received S-current. Retaining the old gate
would have falsely refused the actual unit-mobility result.

The source engine reports guarded dyadic product counts and product/root operand
size proxies. They are not all Fraction operations, peak memory, raw storage or
serialization. Additions, division, input generation, hashing and verification
also cost ordinary work. External rational types and every resource type are
strictly validated. Verification redoes all raw and scalar work and strictly
binds the exact separate-source fields/endpoints to the ORIGINAL external task.
No output-provided controls or diagnostic floats decide proof acceptance.

## Why rarity itself does not force rare-path work here

For the fixed kappa=1 profile and integer alpha>=4, elementary near-peak
intervals of length1/(4sqrt(alpha)) give M>=7/(64sqrt(alpha)) and
R,R_plus>=(15/(32sqrt(alpha)))*2^alpha. For M, use
v(1+t)<=1+9t^2 and the binomial/geometric bound at t<=1/(4sqrt(alpha)).
For R and R_plus, the same small y interval gives each integrand at least
(15/16)*2^alpha. These are comparison estimates, not floating asymptotics.
Endpoint Darboux widths on the fixed pieces are therefore relatively
O(sqrt(alpha)/N), while the resistance magnitude grows exponentially. Integer
power output/precision sizes grow only linearly with alpha at fixed profile,
plus the required numerical accuracy bits. Thus these supplied profiles admit
scalar refinement without paying an exponentially long rare-crossing trajectory.
This is not a generic complexity lower bound or a claim that the finite current
implementation always meets arbitrary external tolerances: actual paid endpoint
checks and every finite resource limit still determine PASS versus UNKNOWN.

## Executed unit-mobility examples

At beta=kappa=d_min=mu=1:

| Fiber m | Lower mean | Upper mean | TOTAL ratio |
|---:|---:|---:|---:|
|128|2.146778293e8|2.210284158e8|1.029581940|
|256|4.567286514e17|4.625077471e17|1.012653237|
|512|4.192892844e36|4.221110091e36|1.006729781|

The author suite passes5,520 assertions and replays all four saved actual cases,
including exact density-homotopy/current identities, all separate source terms,
rational R_plus Darboux enclosures and type/model/budget attacks. High-precision
M/R_plus comparisons are diagnostics only; R has an independent exact polynomial
integral check.

The513D result is obtained twice from distinct complete raw inputs: coupling20
with M_z=I, and coupling10^100 with diagonal entries1,2,...,512. Their acquired
floor is the same. Each scans1023 terms and523,776 exponent entries and uses
131,075 scalar points,131,079 power calls and2,228,343 guarded products. The
largest tracked product bound is1154bits; the unit-parameter perfect roots have
small operand bounds, not a general dimension-independent bit cost. Production
was about3.4s here and verification repeats it; no controlled runtime superiority
against an optimized verified PDE/current implementation is claimed. Raw bytes
and fixture-generation time are separately recorded.

The earlier conditional current, at the SAME unit mobility and same large model,
received only ratio1.256975784. The extra paid R_plus profile and explicit source
redistribution tighten this to1.006729781. This is a change of proof/information
use, not a changed actual model. The scalar R_plus building block already existed
in the earlier finite-Jensen conductance receiver; the new source connection,
full-tail resistance and separate S-join are what earn the actual mean.

Numerical quadrature width and the chosen witness's structural width differ.
In particular m256 does not pass a1.01 request in these executions, although it
passes1.03. This is a failure of this sufficient certificate at that task, not a
physical error floor, algorithmic lower bound or claim that a stronger method
cannot do better. As mu decreases enough, well-current costs still grow1/mu;
the earlier zero-mobility latency obstruction is not contradicted.

## Ordinary retaining alternatives and unearned claims

The same ordinary variational/Poisson-current implementation supplied this
explicit witness reproduces all bounds. General exit-time variational principles,
homogeneous scaling, density-ratio estimates and conditional dilation are old
machinery. Historical priority is unresolved. Verified elliptic PDE, barrier,
simulation and averaging methods receive identical raw model, exact initial law
and every newly derived analytic certificate; no universal computational
separation is asserted. Generic conditional mixing and rare trajectories are not
assumed as free inputs merely because a competing method might benefit from them.
The accepted previous construction's primary comparison ledger and the separate
Lu--Vanden-Eijnden coarse-graining note retain stronger alternatives honestly.

All-time survival may be earned later only with the separately source-bound
spectral corollary using B_new and B_S. An older wrapper with the same-current
hypothesis cannot be silently relabeled. This mean receiver does not yet provide
CDF queries, relative tail accuracy, exponential moments, an arbitrary-start
law or a preparation/actuation service.

## Preserved author failures and corrections

The first adapted corruption test wrote mobility_floor='1' into a fixture whose
actual new default is already1; its expected refusal therefore failed correctly.
It now changes the value to2. The first density-ratio symbolic check omitted the
actual s>=v domain, so SymPy retained incompatible possible complex square-root
branches; the corrected check supplies s=v+r with r>0. Neither was a detected
mathematical or executable endpoint error. Both earlier test sources are retained.
The proof's earlier phrase suggesting an 'unavoidable' integral was corrected:
R_plus is required by this chosen witness, not by every algorithm or physical
prediction. Earlier proof bytes are preserved. No filesystem permission denial
or uncertain external operation occurred in this construction.
