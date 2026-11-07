from pathlib import Path
from fractions import Fraction as Q
import json

ROOT=Path(__file__).resolve().parent
P=ROOT/'results'
read=lambda n:json.loads((P/n).read_text())
e=read('EXECUTION.json');c=read('CRITICAL_NOISE.json');g=read('GAME_CERTIFICATE.json')
a=read('ACQUISITION.json')['certificate'];n=read('NATIVE_TOTAL_COST.json')
v=read('VERIFICATION.json');r=read('RESOURCE_CERTIFICATE.json');tm=read('RUNTIME.json')
num=lambda x:f'{float(Q(x)):.12g}'

report=f'''CERTIFIED CAUSAL PROTOCOLS FROM FINITE EXPERIMENTS
Completed research construction — 7 November 2026

THE CHOSEN FULL QUESTION

Can finite paid port experiments acquire a reusable causal description from
which one can decide and synthesize arbitrary finite-state temporal protocols
for an unlimited future of bounded interventions, including an explicit
robustness converse, without identifying the hidden source?

The answered formulation uses a warranted uniform fading-memory class,
bounded calibrated commands, a numerical acquisition reader, a finite
deployment quantizer and adversarial bounded read errors. It returns a sound
controller, a counterstrategy when justified, and a certified interval for
the best achievable noise tolerance. The gap is priced by the acquired
causal-model error. Exact zero-margin physical classification is a different
question, with an explicit incompatible-source example below.

The general result and its costs are proved in THEOREM.txt. The software
executes a substantial particular member: indefinitely repeated adversarial
requests on a three-port, 256-hidden-state dissipative component with a
first-order actuator, a cooldown constraint and a deadline. It compiles and
audits the entire finite safety game. It does not implement a general parity
solver or demonstrate an actual physical real-time device.

CENTRAL RESULT

Let fhat(s) be the acquired prediction from the last m command symbols.
Suppose every compatible fixed source satisfies, at every future read,

               ||y - fhat(s)||_infinity <= epsilon.

For a reader error bound r and ANY causal feedback policy pi, the complete
finite and infinite trace sets satisfy

   Traces(fhat, r-epsilon, pi)
         subset Traces(actual source, r, pi)
         subset Traces(fhat, r+epsilon, pi),

when r>=epsilon. A nominal channel of radius rho permits exactly the reader
symbols whose calibrated cells intersect the radius-rho prediction cube.

The right inclusion spends epsilon on the actual prediction residual. For
the left inclusion, each nominal observation is reproduced on the same fixed
source by an allowed read error. Identical observations make pi choose
identical commands, so the argument continues forever. Source parameters
never switch. The allowed read-error box, including its ability to vary at
every read, is essential to the converse.

There is no factor proportional to the prediction horizon. This is an exact
inclusion with changed noise radius, not a claim that two uncertain feedback
trajectories remain close or that infinite stochastic path distributions
have small total variation.

A deterministic parity automaton for the requirement can be multiplied by
the finite input-suffix channel. Classical finite-game algorithms then return
a controller or counterstrategy. The report includes a completely explicit
enumeration/transitive-closure algorithm and conservative bit-operation
bound, so there is no hidden synthesis oracle. The chosen execution uses
the more efficient safety greatest fixed point.

If r* is the greatest reader-error radius for which a controller can win,
and rhat* is the optimum in the finite acquired game, then

                         |r* - rhat*| <= epsilon.

The acquired object is independent of the later temporal specification.
Within the linear construction it also supports later finite command
alphabets chosen within the originally declared amplitude cap and fixed
clock/read phase. Source uncertainties, numerical error and initialization
residuals remain in the one error certificate.

WHY THIS CHANGES THE AVAILABLE OPERATION

The previous library could replace unknown components and write/retain
selected ordered states under its stated contracts. The present operation
answers a different class of questions: whether a feedback protocol can
complete requested operations in the required order, repeatedly, within
deadlines, while respecting resource and safety rules for every admitted
future observation history. It produces the finite controller or an
adversarial obstruction and estimates optimal noise tolerance.

The logic can be nonmonotone, hysteretic or oscillatory. The proof needs no
contraction of the entire feedback loop. Individual bounded-drive sources
retain their warranted forgetting property. Independently acquired
components can be combined through bounded sampled digital interconnections;
their error boxes and resource bills compose. Continuous physical assemblies
still need the retained passive-assembly theorem or another justified model.

These are consequences for the specified source/task/access class. They are
not a claim that finite data identifies arbitrary scientific laws, that
formal control is new, or that civilisation-scale novelty has been proved.

ACTUAL ACQUISITION AND USE

The source has 256 distinct hidden relaxation rates and three collocated
ports. Its entire state and actuator persist across experiments. The
learner/controller never reads those hidden values. Three finite coordinate
pulses, with finite zero-command relaxation, acquire four lag matrices.

Acquisition:
  Vector readings:                         {a['vector_reads']}
  Scalar readings:                         {a['scalar_reads']}
  Retained matrix entries:                 {a['coefficient_scalars']}
  Source-time duration:                    {a['acquisition_time']}
  Source-time with nonzero pulse command:  {a['source_input_active_time']}
  Exact resets:                            0
  Acquisition read-error bound:            {num(a['read_error'])}
  Actuator-error L2 bound:                 {num(a['actuator_error'])}
  Complete future prediction residual:     {num(a['epsilon'])}

The dominant error is the certified unretained memory tail; the coefficient
and preparation errors are also included. Fixed adversarial error is never
averaged away. Arbitrary refinement requires a source/instrument that can
actually provide the requested finer precision at a paid cost.

The physical source/actuator model is

             x'=-H x+Bv,  y=B*x,  tau v'=-v+c+e_a.

The execution has a=1, tau=1/8, normalized ports, A0=2 and c0=1/4. A fixed
period h=2 and positive read-to-command window ell=1/4096 are used. Readings
occur at kh-ell; the old command persists while the next command is computed
and communicated. The acquisition uses this same phase. The exact cells of
the 40-bit nearest-even ADC and threshold decoder are used in the game.

The command alphabet is zero and the six signed coordinate unit vectors.
After every nonzero command, the next command must be zero. Requests may
ask for any signed coordinate. Each request must produce the corresponding
reported threshold crossing within four ticks; simultaneous active-port
labels are forbidden. A new arbitrary request follows each completion.

The nominal channel is known from its input suffix, so full ADC codes with
the same monitor label have identical future nominal game states. The proof
therefore justifies the merged 27-symbol observation game even for policies
that retain the full admitted numeric readings. Its converse still concerns
this fixed command alphabet, sampling schedule, error law and task; it does
not exclude more frequent reading or different hardware interfaces.

The cooldown rule reduces 2,401 possible four-command words to
{g['legal_suffixes']} reachable suffixes. Combining them with requests and
deadlines gives {g['winning']['total_states']} game states. The winning
region at the chosen upper radius has {g['winning']['winning_states']}
states. The audit checks {g['winning_audit']['winning_policy_observation_branches']}
winning-policy observation branches and supplies deletion-rank refutations
for every losing state/action. The separate failing-radius game has no
winning states and {g['losing_audit']['losing_state_action_refutations']}
checked state/action refutations.

INFERRED CAPABILITY

Nominal optimum rhat*:               {num(c['critical_radius'])}
Every compatible source optimum:    [{num(c['source_optimal_radius_lower'])},
                                     {num(c['source_optimal_radius_upper'])}]
Executed/certified reader radius:    {num(e['reader_radius'])}
Reader radius with impossibility:   {num(read('MODEL.json')['failing_reader_radius'])}

At the first radius, the returned policy works for every compatible source
and every admitted request/read-error history. At the last radius, no causal
controller using the stated interface can guarantee this protocol under
the full bounded-error law. The intermediate interval is retained honestly.

EXECUTION AND WHAT IT PROVES

The software executed {e['completed_requests']} completed requests over
{e['sampled_intervals']} sampled command periods, with adversarial-direction
read errors. The largest observed request delay was
{e['maximum_request_delay_ticks']} ticks. Every recorded branch belonged to
the certified game, and all {v['model_support_scalar_checks']} scalar
record/prediction checks passed. The finite execution is separate from the
all-future theorem and the exhaustive finite-game certificate.

At each acknowledged read, the true requested signed coordinate is at least
{num(e['certified_true_target_signed_output_at_every_acknowledgement'])}.
At the subsequent command boundary, the derivative/read-age certificate
still gives at least
{num(e['certified_true_target_signed_output_at_command_boundary'])}.
Each request completes within 8 source-time units after it becomes active.

Deployment had {e['vector_reads']} vector readings, {e['scalar_reads']}
scalar readings, {e['online_policy_lookups']} policy lookups and
{v['nonzero_command_intervals']} nonzero command periods. There were
{v['deployment_command_changes']} command changes. Command squared effort
was {v['deployment_command_squared_effort']} in the declared units.
No hidden-state read was used to select a command.

The actual finite record hash is
{e['transcript_sha256']}.

The reported run is a finite prefix of the indefinitely repeatable protocol.
It is not an unpriced shutdown, nor a promise of infinite operation for a
finite resource bill.

TIME, ARITHMETIC AND SUPPLY

Deployment includes 30 source-time units of finite relaxation and 864 units
of operation, for 894 total. Acquisition plus deployment uses
{n['time']} source-time units. The actuator's norm is bounded by 2 and
its slew by 32. Absolute source work is bounded by 3,576 over deployment.

There is also a positive work lower bound derived from the actual service
guarantee. A target event of magnitude c and output derivative bound M costs
at least a*c^3/(3M) of source dissipation on a preceding interval, provided
these intervals do not overlap. Here the proved net source work over the
120-completion prefix is at least
{num(r['executed_prefix_net_source_work_lower'])}.
For perpetual backlog, the limiting average net source supply is at least
{num(r['liminf_net_source_power_lower_for_infinite_backlog'])}.
These are power-conjugate model units. Actual driver, sensor, computation,
communication and clock energies must be added from warranted device
envelopes; no physical watts/joules conversion was supplied.

Native digital source costs for the delivered operation:
  Encoded native coefficient scalars:      {n['source_coefficient_scalars']}
  Source coordinate updates:              {n['state_coordinate_updates']}
  Actuator coordinate updates:            {n['actuator_coordinate_updates']}
  Source update integer multiplications:  {n['state_integer_multiplications']}
  Actuator integer multiplications:       {n['actuator_integer_multiplications']}
  Maximum propagation integer length:     {n['maximum_propagation_integer_bits']} bits
  Exponential enclosures:                 {n['exponential_enclosures']}
  Taylor terms:                           {n['exponential_taylor_terms']}
  Squarings:                              {n['exponential_squarings']}
  Maximum series coefficient length:      {n['series_integer_bits_max']} bits

The exact finite-game compiler performed {g['game_solves']} solves and
{g['fixed_point_rounds']} fixed-point rounds while locating and certifying
the capability boundary. Its dense policy has {g['policy_entries']} entries.
The general parity algorithm's exponential bound remains separate.

The report gives a deliberately conservative sequential-table lookup and
bit-arithmetic bound of {e['sequential_table_bit_operation_bound_per_round']}
bit operations per control round. Completing that bound within ell would
require {e['serial_bit_rate_sufficient_for_this_conservative_bound']}
bit operations per source-time unit, or a justified tighter implementation
bound. Native software took approximately {tm['native_preparation_seconds']:.3f}
seconds to prepare, {tm['acquisition_seconds']:.3f} for acquisition,
{tm['synthesis_and_game_verification_seconds']:.3f} for synthesis/audit,
and {tm['deployment_seconds']:.3f} for the full simulated deployment.
These wall times are not a calibrated physical worst-case deadline proof.

Four native software executions were performed during development; the
earlier three scopes and total costs are retained. Across all four there
were {r['development_totals_including_final_execution']['scalar_reads']}
scalar software readings. No physical experiment, installation, extra
worker or new infrastructure was used.

THE INFORMATION BOUNDARY

For a general nonlinear fading-memory source, one can acquire an m-word
table using a de Bruijn command sequence: K^m readings and K^m+m-1 command
periods, without resetting the hidden state. Its error is the warranted
forgetting modulus plus the actual reading error.

An explicit uniformly contracting shift-register family with a globally
1-Lipschitz nonlinear readout encodes an independent bit at each input
word. Disjoint readout supports let each scalar point reading expose at
most one bit. Consequently uniform later prediction requires 2^m readings
and 2^m retained bits in the binary family. This is an exponential cost in
memory length, even with noiseless observations. The source readout contains
that many independent bits; no lower bound for small parametric source
descriptions is asserted. Linear structure is what permits the p^2m-data
construction used here.

Separately, scalar sources H=1-delta and H=1+delta have uniformly close
bounded-input responses. With a fixed adversarial acquisition-noise floor
they can give the same entire adaptive record, yet only the first can reach
y>1 under unit-bounded commands from zero. This retains the exact-margin
information obstruction while the positive gap operation remains complete.

CREDIT AND RESOLUTION

The architecture draws on classical fading-memory approximation and
input-history abstractions (Boyd-Chua; Zamani-Tkachev-Abate; QUEST), robust
formal control and completeness via robustness (Liu-Ozay; Liu), and parity-
game determinacy. The current 2026 data-driven abstraction literature was
checked under its actual finite-horizon/PAC qualifications. The N736
governing original retains its frozen-policy, finite-horizon assay scope;
it is not used as a universal-transfer premise. N1068-N1070, N997/N1018,
the retained inference machinery and all earlier component/control capital
remain credited, with exact routes and qualifications in SOURCES.txt.

The selected acquisition-to-unlimited-protocol question is resolved at the
stated source, noise and clock contract. The full broader ambition of
certified inference for arbitrary scientific sources remains beyond it.
No historical-priority claim, unrestricted complexity resolution or
physical deployment is inferred from this complete restricted result.
'''
(ROOT/'RESEARCH_REPORT.txt').write_text(report)
print(str(ROOT/'RESEARCH_REPORT.txt'))
