# Independent review: common-seed support via sampled core events

**Accepted at the frozen scope below.** The whole ordinary proof, raw/scalar
construction, independent receiving and paid finite-fiber comparator have passed
review. The final boundary includes both additive cycle-flow corollaries and the
explicit decimal-serialization correction. No mathematical blocker remains.

## Mathematical verdict and exact scope

The reconstructed argument is sound for its stated raw family: one open coordinate
A with `0 <-> A`, every other nonnull channel count-conservative and retaining A at
both endpoints, weak reversibility, and top-order support access to shifted A after
stripping one common A. The stripped maximum order is finite `p>=2`. This proves
positive recurrence of every communicating class and all finite exponential
total-count moments of every stationary probability, for arbitrary positive rates.
The executable exact API uses positive rational rates.

This is a sufficient structural theorem, not a classification of stable seeded
networks or a solution of general weak reversibility. The sampled criterion is
compatible with the previous physical one-step `F(A,N)` no-go. No invariant internal
fiber law, supplied good weight/corrector, stationary mixing bound, or numerical ODE
solution is assumed. The proof earns finite-time activation directly from raw support.

This receipt is ordinary independent mathematical/code review, not formal
proof-assistant verification or hardened hostile-input service approval. Exact finite
tests are supplementary evidence, not the infinite-tail argument.

## 1. Proof reconstruction

### Seed stripping and clocks

The identity `(A)_(u_A+1)=A(A-1)_(u_A)` makes the seeded internal generator exactly
`A Q`, where `r=A-1` and the fixed stripped mass is `M=N-1`. Internal jumps retain
A>=1. Time change `d tau=A dt` leaves Q, makes death a constant-rate independent
Exp(mu) clock, and makes immigration hazard `lambda/(1+r)`. The unrestricted Q
chain is used counterfactually only until the first core event. Its later evolution
does not incorrectly describe the actual process after immigration or death.

### Raw support and uniform finite-time concentration

The proposed `C=max(1,p^3 sum_Q rates)` safely bounds the coordinate depletion and
row-sum Jacobian norm of the top-order simplex ODE. Each support-adding reaction
produces a previously absent coordinate with integer increment at least one. The
support recursion must maintain every acquired lower bound throughout the entire
remaining time interval, not just at a block endpoint. The retained proof does so:
the two survival factors of at least 3/4 leave at least 9/16, safely above the
recursion's factor 1/4. At most n-1 additions reach shifted A; padding to n stages
only reduces the valid uniform activation level delta.

The finite-fiber scaling is `Z_s=Y_(s/M^(p-1))/M`. The normalized drift is exactly
`sum kappa nu (Mz)_u/M^p`. Top falling-factorial errors are at most
`p(p-1)/(2M)` before the jump-vector factor. Disabled reactions are covered too:
either use the proof's absolute-factor telescoping with M>=p, or telescope factors
`max(z_i-j/M,0)`. Lower-order drift is O(1/M), and the stated C bounds their sum.
The coordinate bracket rate is at most `p^2 sum_Q rates/M<=C/M`.

Thus the stated Doob/union probability `64 n C T/(M delta^2)` is conservative.
For `M>=ceil(8CT/delta)`, the Gronwall error on the good event is at most
`(delta/4+CT/M)*(4/3)<=delta/2`. These estimates hold uniformly over every starting
state, including simplex boundary states. Conditioning on the last window of
length `T/M^(p-1)` consequently gives the reciprocal-A and zero-r bounds at every
later operational time. It does not union-bound infinitely many windows or assume
convergence to a fiber equilibrium.

### Both bad core outcomes and the sampled Foster estimate

Dropping the no-immigration indicator enlarges the integrals for both immigration
before the independent death clock and death while r=0. Integrating the uniform
last-window bounds gives the claimed constants divided by M. The initial window
has length at most T/M specifically because p>=2; no order-one extension is hidden.

A last-seed death is followed by its actual A-zero waiting interval and one restoring
immigration. The bundled count increment is zero, not minus one. The three exact
increments are +1,-1,0. Their exponential ratio is

```
t^-1+(t-t^-1)p_up+(1-t^-1)p_loss.
```

The acquired cutoff `M_cut>=2a(t+1)` pays this by
`rho=(1+t^-1)/2`. At the remaining seeded head, count increases by at most one.
This gives the stated Foster bound with `B=(t-rho)t^M_cut`. The head consists of
`binomial(M_cut+n-1,n)` seeded lattice states; this is a symbolic count, not an
enumerated set or a hidden finite-state optimization.

### Classes and physical stationary occupation

The ordinary immigration-Poisson comparison proves nonexplosion independently of
the fluid or Foster argument. Weak reversibility closes full state classes. A finite
path between seeded states becomes a sampled path by bundling visits to A=0; if its
last segment is internal, append immigration and death to record the desired endpoint.
All those finite prescribed paths have positive probability. Thus each full class
has one closed irreducible sampled class.

Discrete Foster gives its stationary law nu and
`nu(t^N)<=L_t=(2t+1)t^M_cut`. Tight Cesaro occupation laws and Fatou justify this
without assuming stationary integrability in advance. The sampled kernel is the
same for all t, so uniqueness makes the repeated moment arguments apply to the same
classwise law.

Physical occupation transfer includes the seed-free waiting time. Before the terminal
endpoint, N never exceeds its starting value; a terminal immigration has zero
occupation duration at its new count. Conditional holding means and polynomial
rate integrability justify cycle Dynkin identities and the invariant occupation
probability. The resulting full-class law is unique, hence positive recurrence.
Uniform bounds across classes also apply to stationary mixtures. The finite-sublevel
argument establishes that only finitely many full classes can occur under this
criterion.

### The additive cycle-flow normalization

The sharper normalization was checked independently, rather than inherited from the
earlier Jensen bound. Let T be the bundled cycle and J the next physical immigration.
On up, T=J; on ordinary down, T<J; on seed loss the chain waits at A=0 until J.
Therefore `T<=J` pathwise and `E_x T<=1/lambda` pointwise.

Counting immigrations through the endpoint gives exactly
`lambda E_x T=p_up(x)+p_loss(x)`. This follows either from the bounded-stopping
immigration compensator followed by monotone convergence, or from the exact killed
fiber equations. Under nu, the already-proved finite N moment and stationarity give
`nu(p_up)=nu(p_down)`. Consequently

```
lambda E_nu T=(1+nu(p_loss))/2,
1/(2lambda)<=E_nu T<=1/lambda,
pi_cont(t^N)<=2 nu(t^N)<=2(2t+1)t^M_cut.
```

The lower holding bound is stationary-average only. It fails pointwise at large
A-only states; the independent exact controls retain such counterexamples. Including
an endpoint immigration in the count while excluding its zero-duration occupation
is essential and consistent. No unknown normalization or stationary fiber law is
used. The earlier H-bound, Jensen expression and `2lambda H L_t` remain valid
conservative comparators, not proof failures.

## 2. Independent receiver and adversarial controls

`independent_audit/independent_time_change_receiver.py` imports no candidate module.
It independently validates exact raw domains, aggregates channels, acquires the open
coordinate, strips A, checks conservation and graph return reachability, and computes
graph work using separate reachability sets. It finds support additions by eligible
sets, then reconstructs the declared first-enabled scan's source/product-coordinate
work from each tested prefix. Closed-face meaning is checked independently on a
failed support scan.

The numerical receiver independently reconstructs every support level, power preflight,
scalar constant, threshold, factored power, symbolic head size, interpretation and
work field. It verifies the sharper and relaxed occupation expressions symbolically,
without materializing `t^M_cut`. The author's receivers are correctly described as
semantic recomputation using their constructor; they are not themselves independent
implementations.

The eight independently received numerical cases comprise the author's seven and
an extra stripped order-five network with genuine lower-order channels. These cover
the opposing pure-ray obstruction, the prior mediated `F(A,N)` no-go family, cubic
catalytic lift, five species with the open role last, heterogeneous rates, near-one
and large bases. All six coordinate permutations with reordered raw input, split
rates and a validated null channel pass.

Every primitive leaf of the qualitative and numerical receipts was independently
mutated: **52 qualitative-interface mutations and 115 full numerical-interface
mutations** were rejected by both receivers. Six receipt omissions/extra-field
mutations were also rejected. Sixteen malformed raw cases and nine scalar-domain
cases are checked by both implementations, including bool/float distinctions,
validation before null removal, lack of a common seed, non-WR input, extra open
channels, nonpositive bases and invalid caps. Forty small exact binomial identities
check the head-count formula independently of the main enormous expression.

Cap-boundary tests show zero, one and two completed support powers before numerical
UNKNOWN, and acceptance at the first sufficient bound. The qualitative theorem is
retained throughout. With `p=10^50`, the qualitative and capped numerical paths both
run while every Fraction power is forbidden: the latter declines before its first
support power. The ordinary opposing numerical run makes exactly three powers, all
of degree two, never of the Foster exponent. Failed support and stripped order one
remain stability UNKNOWN, not rejected stability claims.

## 3. Paid finite-fiber comparator

Original mechanism notes and uncharged finite-fiber results are preserved byte-for-byte
under `independent_audit/mechanism/`, still marked as their original pending-stage
notes. The separate paid control records actual rational Gaussian work. It solves
the killed matrix

```
diag(mu+lambda/(1+r))-Q
```

jointly for four right-hand sides: birth probability, seed-loss probability,
ordinary-down probability, and physical seeded duration. These are conditional
first-core quantities, not stationary laws on a fiber.

For the opposing quadratic and catalyzed cubic stripped examples, the controls cover
17 fibers and 285 states, with matrix dimensions between 1 and 45. They verify 3,150
exact seed-factorization identities, 813 scaled-drift and 813 bracket bounds, 1,140
killed-equation rows, and 2,670 catalytic generator multiplier identities. All 285
states satisfy the exact birth-compensator holding identity. In 249 states the
conditional holding mean is below `1/(2lambda)`, guarding against falsely turning
the stationary lower bound into a pointwise assertion.

The joint Gaussian eliminations used 285 pivot nonzero tests, zero row swaps, 8,949
rational divisions, 3,427 eliminated rows, and 128,377 multiplications plus 128,377
subtractions. This accounting excludes matrix assembly, other proof/test checks,
gcd/bit costs, memory and output; it is not a total resource budget. These small
fibers do not numerically reach the astronomical asymptotic threshold and do not
prove the infinite-tail estimate. That estimate is supplied by the ordinary proof.

## 4. Honest costs, comparisons and limits

For the opposing fixture at t=2, the acquired cutoff is

```
2543267526313950623496479133068309573484172804713259814879233.
```

It has 61 decimal digits. The head is a binomial expression and stationary bounds
contain a power of two with this exponent. No head, large fiber, or such power is
expanded. Broader structural coverage does not imply quantitatively superior bounds:
the earlier inverse-mass package is far sharper on its recognized family.

The power-bit cap bounds only the declared upper size of support-level power-product
outputs. It does not bound validation, graph work, all rational arithmetic, transient
bit sizes, memory or wall time. The retained-record bit peak has its literal scope.
Qualitative recognition spends the retained structural theorem, with no per-instance
ODE solution, stationary fiber, polynomial expansion or scalar support-power oracle.

A genuine wire-domain defect was found before final binding: CPython's default
4,300-decimal-digit conversion guard can stop serialization of a mathematically
accepted scalar receipt even under the declared support-power cap. The final trusted
research module, and the independent receiver, explicitly disable that guard **for
the interpreter process on import**. This is documented, is not a resource limit,
and is not appropriate as an implicit hardened-service security policy.

Fresh-process tests reset the guard to 4,300 before importing each implementation,
so one module cannot mask a missing setting in the other. The original constructor's
failure is reproduced. The final four-species/order-six receipt has 15,561-bit
retained scalar records and 61,202 canonical wire bytes; both implementations
independently produce the same hash and receive its roundtrip. A separate admitted
network with immigration rate `10^5000` gives a 5,022-digit cutoff and a 98,063-byte
receipt, again identical across implementations. Only compact metadata and receipt
hashes are saved, not those large wires. No Foster power is expanded. These local
stress controls demonstrate the stated domain repair, not a global memory/time bound.

The non-complex-balanced opposing fixture satisfies the new support test while every
inverse-linear profile has contradictory pure-source signs. Conversely the all-unit
lower-order-restoration fixture is complex balanced and stable despite failed top
support, establishing incompleteness of this structural condition. These facts do
not exclude other conventional representations or sampled criteria.

Time change, finite-time density-dependent martingale comparison, support propagation,
Foster theory and occupation laws are ordinary tools. `SOURCE_SCOPE.md` records the
parent's primary inspections and specifically credits Darling's finite-time
approximation and earlier reaction-network sampled-chain methods. This review
reconstructs the needed estimates directly; no unavailable theorem is assumed.
No priority or general weak-reversibility claim follows from parser failures or
finite tests. The Kurtz DOI reported inaccessible and historically denied/gated
sources were not retried by this review.

Earlier accepted packages, including the delivered inverse-mass archive and its
manifest, are unchanged. The preliminary `CANDIDATE_NOT_REVIEWED.md` is excluded
from the final allowlist. Use ordinary Python with assertions enabled, not `-O`.

## 5. Frozen binding and replay

The final proof `SEEDED_TIME_CHANGE_THEOREM.md` has SHA256
`8cb39cfc1d3f4b39a1140ed861fc240ae390bdaf2d3928109d4d0d2ef75aefb9`.
The final constructor `seeded_time_change.py` has SHA256
`ffa0ac3f1741e89916290a74aa5201d0b1582a072fa29e5f015f5a778a9298d9`.
The final exercise script/output hashes are respectively
`25b9991aa066ae1c4d752e854beadc4f7e6fc72b18f6a4ee59dd5c18d107e48e` and
`7268a849133b2ae1f9e92257b52fb8c658599ac090b7867f786fd9540e80984d`.
The final opposing demo hash is
`1675149efc02c011800851dab05ecb96e7bb49bbee4dedfbeac1c88461c04691`.
`SOURCE_SCOPE.md` remains
`c9f93d8c77142f5c7b4aec45ec0ed676c077aa0dd0229d6b43e18eb1e460cc23`.

For historical precision, the original supplied proof/constructor hashes were
`dc365ede8c866cf4c1043d59666f1b53a55dff1cad7df0457871d56fe8d867a4` /
`07a01d555532e7c809d190085e6bc57085a399934f420159427aa28208d646bf`.
The first additive flow-normalization revision was
`72e6b0fc139e37c24831f85450b986b0230bbc6e051c6eaaef6c075fb400ac69` /
`38d2ce2a92181dbe223ea79c535c30a1fe2dd5f58034979381997fa3cbad7d2a`.
Those weaker bounds remain mathematically valid. The final revision adds the
first-immigration-time corollary and repairs actual serialization. The old frozen
bytes and replay outputs are retained with `original_<hash-prefix>_` names; they are
historical evidence, not the final receiver target.

Both final main outputs replayed byte-identically. The final independent driver,
fresh-process wire controls and paid fiber controls completed with exit status zero.
The author's final exercise includes seven cases, six permutations, 40 selected
semantic tamper controls and 12 domain controls; these are kept distinct from the
independent counts rather than added as disjoint evidence.

The package-relative exact allowlist is `independent_audit/AUDIT_MANIFEST.json`,
excluding itself, caches and the preliminary candidate note. It binds this receipt,
final core and README/source scope, frozen copies, replay outputs, independent
receiver/driver/results, paid comparator and historical mechanism notes. Original
pending mechanism files were copied byte-identically. No earlier accepted package
was edited.

From this package directory, ordinary Python 3 replays are:

```sh
python seeded_time_change.py > producer-workspace/time_change_demo.json
cmp opposing_demo.json producer-workspace/time_change_demo.json
python exercise_time_change.py > producer-workspace/time_change_exercise.json
cmp exercise_results.json producer-workspace/time_change_exercise.json
python independent_audit/run_independent_audit.py > producer-workspace/time_change_independent.json
cmp independent_audit/independent_results.json producer-workspace/time_change_independent.json
python independent_audit/wire_stress_fresh_process.py > producer-workspace/time_change_wire.json
cmp independent_audit/wire_stress_results.json producer-workspace/time_change_wire.json
python independent_audit/mechanism/exact_fiber_controls.py > producer-workspace/time_change_fibers.json
cmp independent_audit/mechanism/exact_fiber_results.json producer-workspace/time_change_fibers.json
python independent_audit/mechanism/exact_fiber_paid_controls.py > producer-workspace/time_change_paid.json
cmp independent_audit/mechanism/exact_fiber_paid_results.json producer-workspace/time_change_paid.json
```
