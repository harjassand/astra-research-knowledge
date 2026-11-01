# Acquisition, paid computation, retaining alternatives, failures

## 1. Actual information access and physical task

The receiving input is a finite raw program for

    U(z)=sum_i d_i z_i^4 + sum_{i<j} g_ij z_i^2 z_j^2,
    F(y,z)=[1+kappa(1-y^2)^2]U(z),

and constant positive isotropic/diagonal transverse mobility. Literal energy
coefficients must be nonnegative; every aggregated pure coefficient must be
strictly positive. m is a multiple of four, alpha=m/4>=4. beta,kappa>0 are
external exact task parameters. The shifted-current choice additionally requires
v_b <= (1+kappa)(1-1/(2alpha)); tiny kappa may therefore be refused.

The actual dynamics, full-fiber basins A={y<=-1/2}, B={y>=1/2}, and once-only
exact full Gibbs|A initial law are those of the earlier accepted construction.
The law is a mathematical input, not a physically prepared finite-bit sample.
Every subsequent label refers to the same continuing process, not iid draws.
The literal physical spacing is externally supplied as a Fraction. The new
reference chain's rate is allowed to differ, but observation times are NOT
silently redefined in new mean-time units.

For the production case, canonical raw bytes are **1,079,871**, SHA
`e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff`.
There are 1,023 literal monomials and 523,776 literal exponent entries. This is
not a free sparse-vector oracle: the current grammar really supplies and reads
full exponent vectors. Total coefficient bits read including mobility: 4,092.
A future sparse parser could reduce this representation cost but is not assumed.
The physical spacing is approximately 4.19452093699e36; exact bytes are in
`original_physical_task.json`. Predicting this event analytically is not evidence
of simulating or physically exposing the system for that duration.

## 2. Raw derivative acquisition is new and explicitly paid

`acquire_derivative.py` checks the complete schema, dimensions, positive actual
mobility, all literal exponent vectors and rational coefficient encodings.
It sums **all duplicate terms** exactly, reads zero terms before dropping them,
and verifies all aggregated pure terms. It then forms

    c_j = 12 mu_j d_j + 2 sum_i mu_i g_ij,
    H = sum_j c_j^2,
    tr(M Hess U) = sum_j c_j z_j^2 <= sqrt(H U/d_min).

The d_j here are actual aggregate coefficients, not the coercivity lower bound
misused as an upper bound. Pair contributions use both actual mobility entries.
The original and normalized raw hashes are distinct receiving fields; a split
coefficient can represent the same model but is not confused with identical
input bytes. The accepted downstream parser receives the fully verified
canonical program, and reads it again. Both passes are paid.

Production coefficients are 52 at the two endpoints and 92 at all 510 interior
vertices: H=4,322,048. The new rational aggregation/derivative counter is 5,114;
its maximum stored rational operand is 23 bits. Complete SPD mobility is valid
for parts of the abstract theorem but NOT for this diagonal derivative shortcut.
Negative coefficients, absent pure terms, general rotations, SOS membership and
unknown/noisy coefficient acquisition do not inherit acceptance.

## 3. Scalar finite computation; no angular sampler or rare-event oracle

The complete full-energy price is an upper bound, not an uncontrolled floating
quadrature. Gamma-bin probabilities, positive cross-cell D bounds, trapezoid
remainders, finite positive-Taylor lower-J bounds, and both omitted energy tails
are all evaluated outward. The auxiliary Taylor order is literally K0=3, not an
unpaid variable loop. t=0 takes the exact J(0)=1/2 branch. Roots, exponentials,
rational powers and all normalizing factors are explicit.

Production: Nt=1024, Ny=256, L=32, T=400, 512-bit fixed-point arithmetic.
There are 263,425 tensor nodes and 1,025 spatial rows. Only two rows and shared
one-dimensional coefficient/prefix/suffix arrays are retained at once. Cost is
O(Nt Ny + alpha Nt) fixed-size arithmetic operations, with the actual operand
lengths and scalar setup separately paid. This is not dimension-free bit cost:
alpha, raw coefficients, normalization powers and exact physical-time operands
all affect arithmetic lengths. Fixed K0 contributes O(Nt), and integer-Gamma
sums contribute O(alpha Nt). The coefficient acquisition is O(literal terms*m)
under this actual full-vector grammar, plus exact rational bit work.

Actual new primal counters:

- 8,989,844 guarded fixed-product operations;
- 1,443,199 named interval additions and 263,168 interval divisions;
- 2,572 exponential calls / 194,546 Taylor terms;
- 1,033 Gamma-survival calls; 2,051 roots;
- 4,102 separately guarded rational-power calls;
- fixed-product maximum precheck 1,073 bits; root-operand maximum 1,759 bits.

The complete producer additionally recomputes the accepted mass/resistance and
well-source engine (8,913,015 fixed operations) and shifted resistance
(2,228,241), then pays 804 query operations. **Total fixed-product counter:
20,131,904**. Shared inherited+shifted points: 655,364. Five extra query roots
have largest prechecked operand bound 7,532 bits. Their count is fixed here,
not their bit cost. Exact normalization powers are separately guarded/counted.

`max_operations` bounds the specifically counted guarded fixed products. It is
NOT a claim that every Python addition, rational construction, loop, comparison,
JSON read or output operation is individually counted. Prefix/suffix sums and
other linear arithmetic obey the explicit finite loop bounds above. Rational
counters/maximum fields are named proxies, not a total-memory or every-temporary
bit instrumentation. No hidden oracle is required for these conventional
operations. Separate input/tree/grid/precision/exponent/root budgets prevent
unbounded search; this producer does not automatically refine forever.

The full producer completed in 35.45 seconds in this environment; a fresh whole
raw verification was also executed in the author suite. Timings are diagnostics,
not proofs or portable performance guarantees. Raw acquisition, scalar source
recomputation, the transverse price, complete well current, physical grid,
finite-state event DP and exact comparison are all included. The output is
54,190 bytes. The count-event DP has eight states and 52 actual updates; no
arbitrary-predicate free oracle is claimed.

## 4. Same-input retaining alternatives

`same_task_comparison.json` binds one physical model, one initial law, the same
ten physical observation times, and the same count4..6 event. It explicitly
reuses the *already paid and reverified* scalar certificate. It is not a fresh
raw replay, and does not pretend its inexpensive comparison time includes the
production costs already incurred.

- The earlier accepted coarse certificate gives 0.1398728551 whole-record TV.
- Give its older witness the SAME newly paid, finer scalar enclosures: 0.1329399049.
- Use new U-dependent trial but old unshifted barrier-current source: 0.1233275225.
- Use old scalar trial but new shifted-current source: 0.1100556695.
- Use the matched pair: 0.09660695295.

The two ablations are conservative variational choices, not estimates of actual
error. For the new-trial/old-current choice replace b_f by
(Mh/Ml)^2 Rplus_hi/v_*^alpha + 2 Erest/(Ml^2 v_*^alpha), retaining the received
new residual. For the scalar-trial/new-current choice take P=v_*^alpha/Rlo and
b_r=eta^2 Rhi C_s/(4 v_*^alpha), from the original scalar odd-residual current.
The same Cu/Ml moment/count argument and the same physical spacing then apply.
Thus both halves matter for this particular requested 10% operation. This is
not a lower bound against better old-witness analysis or other ordinary methods.

Ordinary Dirichlet/Thomson duality, coarea, conditional homogeneous scaling,
frozen-fiber trial functions, interval arithmetic and finite-state Markov event
computation supply all the machinery. A comparably informed ordinary variational
implementation gets these inputs and can implement this exact construction.
An ordinary energy-coordinate solver or higher-order validated quadrature might
be faster/tighter; no separation against those unimplemented retaining
alternatives is claimed. The existing free-energy approximation already proposes
a two-state clock. The earned addition is an explicit full-model error certificate
for the actual finite record without assuming hidden angular equilibration.

Located primary metastability results already give repeated Markov limits and
resolvent methods, sometimes for stronger initial laws: Beltran–Landim
[2009](https://arxiv.org/pdf/0910.4088),
[2013](https://arxiv.org/pdf/1305.5987), and Lee–Seo
[2020](https://arxiv.org/pdf/2008.08295v3). The bound prior-scope notes distinguish
their stated regimes from this growing-dimensional flat/unbounded critical-set
family. This is not historical novelty clearance or a claim those methods cannot
adapt. The coarea identity and finite-grid constructive theorem are newly derived
here from ordinary primitives; they must not be double-counted as an independent
pre-existing method already supplying the same certificate.

## 5. Honest failures and narrower promise

`boundary_checks.json` contains actual, non-mocked complete runs:

- Same original task, Nt=128/Ny=64: UNKNOWN after about25.35s because the full
  unchanged-grid error misses 10%, despite valid mathematics at that resolution.
- Actual path coupling increased from20 to200, all other supplied tasks unchanged:
  UNKNOWN after about35.97s for the same accuracy gate. The raw derivative price
  is reacquired; the new certificate does not inherit arbitrary-coupling
  insensitivity from the older homogeneous rate envelope.

The author suite additionally pays real small-model missed path/event-width/
jitter gates, source budgets and exact L=0 receiving. It tests literal duplicate
aggregation, actual diagonal Hessians, strict types, negative/noncanonical
coefficients, missing coercivity, depth/cycles and allocation preflights.
Schema-only mutation tests are explicitly stubbed to avoid mislabeling thousands
of repeated expensive productions; the literal original production and small
case are also genuinely recomputed by `verify`.

A primitive auditor found the initial preallocation order could construct
S=1<<precision_bits before its bit-budget check. The one-line check was moved
before construction; no scalar formula changed. The auditor preserves the exact
original source and nonallocating sentinel failure. This correction is separate
from the earlier retained-clock incident/guard repair history; accepted older
files were not altered.

The finite error remains a sufficient certificate width, not a physical or
algorithmic floor. Increasing precision alone need not meet a requested accuracy.
No exact finite-alpha iid renewal law, continuous timestamp-TV, uncontrolled
neutral stirring (the new trial depends on U), adaptive stopping-time schedule,
rare-event relative error or unbounded moment guarantee is received here.
