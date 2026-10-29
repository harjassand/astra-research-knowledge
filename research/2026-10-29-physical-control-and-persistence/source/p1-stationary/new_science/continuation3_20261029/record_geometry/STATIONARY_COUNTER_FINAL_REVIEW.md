# Independent review: bounded stationary change of measure

29 October 2026. Reviewer: the existing Astra P1 record-geometry helper.
This is an internal mathematical and executable review within the continuing
research role. It is not external peer review, apparatus validation, a
priority determination, or formal verification.

## Verdict and reviewed inputs

**Accepted at the stated interface.** I found no remaining load-bearing
mathematical error in the governing proof or its executable examples. The
construction preserves the desired full microscopic law at macro completion
indices. Its universal native-call cap is sharp, and its stationary mean is
optimal when the native stationary probability is unique. These conclusions
do not imply convergence from an arbitrary start, rapid mixing, independence
from retained records, or a change of native physical-time occupation.

The final proof was read in full. Its changes from the earlier inspected
revision were also compared explicitly. The actual reviewed files are:

| File | SHA256 |
|---|---|
| BOUNDED_STATIONARY_CHANGE_OF_MEASURE.md | `79947c769db47b6b5cd56b5afb535f58e7f26fdb9dd0afd76ec54db8c015ac51` |
| check_stationary_counter.py | `e81cfe51ee42c9756538c7e9e010c357a124d17c43c9a63750fe700e43b85578` |
| STATIONARY_COUNTER_CHECKS.json | `2a23bf847adbe41c2ab6d5d3f4ead2f8f9e36eace934af0a0f3b08557eb2b1b3` |
| BOUNDED_REVERSIBLE_EXCURSION_COMPILER.md | `c3d09b270d0df1802b74c6bbdeb66f00ffe73142892ab3907527ee40d8b4d749` |
| check_reversible_excursion_compiler.py | `74b7db9125b61779b93038dea6653afa856f6c0d8283406b5b9f54129584d544` |
| REVERSIBLE_EXCURSION_CHECKS.json | `d51a0182a154faf3d5e94b0676bce41de0f70eafc3fd8fce98ae0798ce092461` |

The accompanying JSON pins these hashes, saved input snapshots and the
independent replay receipts. The earlier governing proof snapshot beginning
`b557f957ea9f` is preserved. The later proof correctly qualifies reducible
sources, ordinary thinning's tail, and the separate iid binary bounded-bit
fallback.

## Mathematical attacks and resolutions

### 1. The counter really returns within the claimed cap

Write m=min W, M=max W and L=ceil(M/m). For positive direction, the first
forward wrap of any phase lands in the universally accepted interval
{0,...,m-1} within L calls. For negative direction, subtracting m reaches
that interval within L calls, possibly after one initial wrap. The argument
is independent of the state path, including evolving hidden memory. It also
works from phases outside the accepted set. Consequently the killed outside
block is nilpotent, and the finite return-kernel formula is legitimate.

The conditional phase draw is essential: the initial phase is uniform in
the current state's accepted interval, not uniform in all M phases. This
matches the conditional phase law under the tilted augmented stationary
measure. The executable counterexample for unconditional phase selection
confirms that the distinction is substantive.

### 2. Stationarity needs no reversibility

The product kernel P times a counter permutation preserves mu times the
uniform phase law whenever mu P=mu. Restricting this product law to the
accepted subgraph gives microscopic marginal nu=W mu/mu(W). The finite
positive-return kernel preserves that restriction, by the stationary block
equations. Conditional phase refresh and projection therefore define a
physical endpoint kernel preserving nu on the full state space.

No step requires a finite predictive representation, conditional iid visible
increments, microscopic copying, or simulation of a hidden adjoint. The
finite-dimensional code illustrates the statement; the measure/kernel proof
is not restricted to those finite examples.

### 3. Reversal and generalized parity are correctly scoped

For reversible P, the two lifted counter directions are adjoints. Reversal
of each finite return path, followed by conditional lift and projection,
gives K_plus adjoint equal to K_minus. Their equal mixture is reversible.
For an involution Theta with P*=Theta P Theta and Theta-even W, the same
**direction-symmetrized** K has K*=Theta K Theta. In the governing text,
K already denotes this equal mixture. A single direction instead generally
relates to the opposite direction under Theta. No physical Theta operation
is inferred or needed.

An irreversible native kernel retains invariance after counter compilation;
averaging directions need not remove its native currents. The directed
circulation fixture explicitly exercises this case.

### 4. Occupation and mean cost do not hide a preparation theorem

The accepted subgraph is visited initially and not again before stopping.
The outside occupation is the initial restricted law times the finite
resolvent. Stationary block balance identifies the total augmented occupation
as the original product measure divided by accepted mass mu(W)/M. Projection
gives native occupation (M/mu(W))mu and mean length M/mu(W).

This is a stationary-start identity. With a single repeated P, it agrees
with the fact that stopping and restarting have not altered the underlying
native path. It does not establish the tilted law at physical-time samples.
All-start guarantees here concern the hard count cap alone.

The mean lower bound follows from the classical stopped-occupation identity:
if start and endpoint both have law nu, the finite occupation measure Lambda
satisfies Lambda P=Lambda. Under uniqueness, Lambda=c mu. The mandatory
initial visit implies Lambda>=nu, hence c>=ess sup(dnu/dmu)=M/mu(W).
The proof correctly retains uniqueness. The added P=I example demonstrates
why global optimality cannot be inferred from an arbitrary invariant mixture
of conserved sectors.

### 5. The universal cap lower bound covers the stated controller class

For P_p=(1-p)I+pQ and a fixed capped controller whose seeds do not supply p,
every terminal path weight is polynomial in p. At first order, one Q event
occurs before the unchanged-path stopping decision; after it, remaining
identity steps leave the actual terminal state unchanged. Thus
K'_0=diag(t_x)(Q-I), with 1<=t_x<=L. Q self transitions are already included
by this generator expression.

Invariance on an open physical p interval is a polynomial identity, so
differentiating at zero is valid. Uniqueness of Q's stationary left vector
forces nu(x)t_x=c mu(x), and therefore L>=max W/min W. Taking the integer
ceiling gives the claimed sharp universal cap. The statement concerns the
same unknown-kernel interface, not a p-dependent externally supplied
calibration law, an additional actuator, or continuous observations between
native calls.

### 6. Composition, sectors, calibration and finite precision

Each local native operation must preserve the common full microscopic
baseline law and all nonselected visible coordinates. Disintegrating by its
fixed visible context then justifies the local tilt. Prescribed compositions
and state-independent random scans preserve the resulting common target;
unrestricted history-selected schedules are not covered.

Frozen sector weights cannot be changed by a controller using only a
sector-preserving native operation. The preserved 7/10-versus-3/4 example
correctly rules out inferring preparation from aggregate stationarity. A
common baseline visible law in every sector is a meaningful sufficient
condition for a common tilted visible law, conditional on the separate
convergence premise.

Finite kinetic calibration can choose among operations already warranted
to have the required stationary law; it cannot certify unrestricted hidden
stationarity exactly. Selection and old records may change the conditional
initial state. Retaining intermediate phases, labels and clocks does not
make the endpoint independent of those records.

The implementation-error statement now requires a coupling bound uniform
on the full operational state and actual history. The union/first-error
bound Le is then valid for one macro. It does not imply a stationary phase
observable bound. The companion excursion proof now uses U=-log W for
coherent energy perturbations and identifies conservative field errors as
sufficient to select phases. These corrections are accepted.

## Executable audit and replay

Both scripts were read, including the imported exact matrix/controller
helpers. The main checker uses rational arithmetic and literal branch
enumeration; it does not substitute fitted rates for the unknown native
operation. I independently ran both final scripts successfully.

Main replay: **16 exact source/weight cases and four exact binary reductions
passed.** The cases cover reversible and circulating irreversible native
sources, arbitrary integer weights with minimum above one, both directions,
full microscopic invariant laws, the sharp cap, exact native occupation,
and stationary mean. Endpoint/count adjoint identities are checked for
reversible sources. The ordinary Bernoulli thinning comparator is evaluated
with an exact inverse, preserving the same target and mean while exhibiting
a positive beyond-cap tail in the nonconstant test cases. Constant weights
correctly give no such tail.

The binary reductions compare endpoint kernels, occupation and the full
joint count/endpoint distribution with the independently expressed excursion
controller. Wrong unconditional phase selection is retained as a failing
implementation. The main output's code hash matches the inspected main
source; the imported dependency is separately pinned above.

Dependency replay: **12 general hidden-state cases and 25 iid binary cases
passed.** The preserved checks include independently computed block
formulas, detailed balance, count-resolved reversal, exact occupation, local
composition with shared evolving hidden memory, an observed-label memory
witness, and an exact positive finite Hankel-moment sanity check. The proof,
not that finite matrix check, establishes the all-order rank conclusion.

These are exact synthetic model checks. They do not validate an apparatus,
an acquired calibration confidence budget, or performance in a mixing-limited
physical program. No further broad testing is required to close the concrete
generalization risks addressed by this review.

## Prior mechanisms and acceptance boundary

Watched chains, stopped occupation, auxiliary slice coordinates, wrapped
uniform translations and importance thinning are established mechanisms.
PRIMARY_COMPARISON.md records inspected primary sources, including Pitman's
occupation work and Neal's auxiliary-coordinate constructions. Root's
additional direct comparison with the Importance Markov Chain remains part
of its own source assessment. This review establishes internal correctness
and declared resources, not historical novelty.

The accepted addition is the supplied bounded actual implementation with
its exact target, optimal stationary mean under uniqueness, sharp universal
call cap, evolving hidden-state scope and explicitly limited composition.
No remaining blocking correction is requested for the versions pinned here.
