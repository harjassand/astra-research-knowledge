# Round 11 result: local contact can control native density, at a different task

The completed construction is SINGLE_FILE_CONTACT_CONTROLS_NATIVE_DENSITY.md.
One driven hard-core tracer in a one-dimensional no-passing ring creates
an order-one native density profile and moves the native population through
actual contact. This is a strong ordinary alternative, directly preceded by
the driven-tracer and local-battery literature. It does not preserve native
density histories, so it does not solve root's strengthened selected task.

## Exact result with hidden frozen rates

Native particle i has unknown fixed symmetric rate c_i between two positive
bounds. The tracer has supplied rates p>q>0 and affinity F=log(p/q).
Writing S_i=sum_{j<=i} 1/c_j,

\[
\mathcal J=(p-q)/(1+qS_M),\qquad
w_i=1+\mathcal J S_i,\qquad
\pi_H(g)\propto\prod_iw_i^{g_i}.
\]

Every particle has the same mean true velocity
v_N=mathcal J Z_{H-1}/Z_H. An exact partition-ratio inequality proves
v_N=Theta(1/N) uniformly over the frozen-rate class at fixed interior
density. Thus one auxiliary drives Theta(1) total native current.
There is no microscopic rate inference or unmeasured intervention.

If the cumulative native resistance homogenizes to bar r times label
distance, the limiting tracer-frame native density is

\[
\rho_F(x)=(1-t)\exp[-(e^F-1)t\,x/\rho],
\quad
\int_0^1[1-t(1+(e^F-1)u)]^{-1}du=1/\rho.
\]

The profile shape depends on F and total density, while the unknown
kinetics enter only the speed through bar r. The proof is a conditioned
geometric-array limit with explicit local-central-limit and concentration
steps. It is a stationary receiver; no cheap finite-time preparation is
asserted for arbitrary frozen arrays.

## Concrete physical target and resources

For F=log 2 and rho=1/[4 log(3/2)], the native profile is
rho_F(x)=(3/4)(2/3)^x. It falls from 3/4 in front of the tracer to 1/2
behind it. Native total mean current tends to 1/(4 bar r).

On physical time N^2 T, true native displacement is order N^2, while
mean ideal signed drive work is
N T log(2) log(3/2)/bar r. The same local-detailed-balance port is
needed for that work formula; hidden futile cycles and nonrecoverable
reverse-step work can increase the apparatus bill.

A canonical equilibrium preparation cannot produce this profile with
o(N) total work plus o(N) supplied excess free energy. The explicit
profile relative-entropy lower bound is at least 0.0103882 N in k_B T
units. Prepared native gradients, controller correlations, and chemical
sources must be included; this is not a universal sparsity prohibition.

The stationary laboratory mean is flat because the profile's origin is
the uniformly positioned tracer. The actual retained tracer position
identifies its nonflat physical density profile. A stationary battery at
one fixed native bond is an ordinary stronger direct actuator producing
a nonflat laboratory-frame profile without the mobile tracer.

## Passive and bandwidth boundaries

Sparse uniformly bounded reciprocal resistances are macroscopically weak
in a homogeneous one-dimensional conductor. Sparse resistances of size
Theta(N/R) are not weak: one critical barrier gives a membrane, and finely
periodic gates can change bulk diffusivity. An Arrhenius realization costs
barriers of order log(N/R), with actual prefactors and assembly still
required. Thus neither sparse mass nor local coupling alone prohibits
collective density control.

Root's later extensive elastic-train option is compatible with a different
resource tradeoff. A closed elastic belt is the strong ordinary comparison.
Large stiffness needs paid force/response range, literal local link
geometry, and a stated bath/friction interface; nearest-label harmonic
coupling does not automatically supply fixed-range mechanical links.
No full elastic-train receiver was constructed by this role.

## Verification and scope

The executable check_driven_tracer.py checks the exact stationary balance,
common marked physical velocities, hole-removal identity, partition bounds
and entropy-production/work identity for 48 finite cases, 1,560 states and
7,896 marked transitions, including nonuniform frozen native rates and
zero drive. All rational residuals are exactly zero; the floating marked
entropy/work residual is below 7.7e-17. DRIVEN_TRACER_CHECK.json preserves
the output and code hash.

This is a population-model verification, not an acquisition-precision,
hardware, hydrodynamic-path or mixing-time experiment. Native labels and
conserved cyclic order, source initialization, arbitrary old-record
conditioning, true displacement, and additional preparation costs are
kept explicit. SOURCE_SCOPE.md records the actual primary sources read.

All earlier continuations are unchanged. This role created no additional
agents, branches, transfers or external messages.

## Subsequent actual receiving review: root elastic carrier layer

The root ideal density proof is accepted with its binding correction.
Exact received hashes:

- ELASTIC_CARRIER_LAYER_AND_DENSITY_LAW.md:
  7f3ecd1fcc7ac70b451fe10a206fd0df17d0bc679dbd90e7f85bc307ea31606a
- ELASTIC_LAYER_CORRECTIONS.md:
  b8b8dcf06013b559b558499aa1428117f22c83516add9440a16e211bc18ca72e

The actual receipt and snapshots are in receiving_review. The prior
RESULT and original MANIFEST were preserved there before this update.
MANIFEST.json remains the historical tracer manifest; the separate
RECEIVING_MANIFEST.json pins the later receiving artifacts.

The proof's local independent unread jitter gives a relative-density
ceiling exp(C N^2): the preparation precision powers cancel the Gibbs
normalization powers. The autonomous relative dynamics preserves that
ceiling despite uniform feedback. The joint Gaussian-proxy determinant
estimate then gives exp[-c epsilon^2 kappa N^2+O(N^2)] concentration for
the true auxiliary density, with no hidden mixing requirement.

Two actual findings were corrected. Continuous-time extension must mesh
the stronger relative-displacement norm event, not only the weaker density
event, because row translations can remove cancellations. Also the original
finite-force bounds require a growth restriction on stiffness. The binding
correction supplies exact all-regime bounds and selects kappa=log(N+2).
Its required worst-case force and derivative ranges are O(N^4 log N) and
O(N^6 log N), with frequency bound O(N^3 sqrt(log N)). These substantial
rare-tail resources are explicitly different from the typical frequency.

The exact horizontal-zero-mean current identity is received. Row-atomic
to step-field interpolation still needs the separate tracking norm bound;
no forthcoming tracking, work or native path-LDP theorem was assumed.
No further load-bearing flaw was found in the scoped density-law review.
The O(N^4) fresh thermal-coordinate count over the physical N^2 horizon
and conditional old-record/future-source requirements remain explicit.

## Later amended source receipt and tracer display correction

The amended ELASTIC_LAYER_CORRECTIONS.md is received at SHA256
35a6d351f969e43d64ca002958bb50a5ce2c6fdfd29cd6a374168766181a62b1.
Its new Section 3 explicitly requires the joint conditional product
thermal source and restricts the quantitative finite-force envelope to
the displayed spring. The earlier correction and receipt remain
preserved. ELASTIC_PRODUCT_SOURCE_SCOPE_RECEIPT.md pins this addition.

Root's actual receiving read also caught a missing plus sign in the
display of the tracer profile's Bernoulli relative entropy. The original
tracer proof remains unchanged. TRACER_FREE_ENERGY_FORMULA_CORRECTION.md,
SHA256 c74a529b5e15e77efe0584182a8f3a301e8bd04501747e57e1e79946ffae1137,
is binding: the two Bernoulli terms in equation (20) are added.
The counting proof and Pinsker bound already use that sum.

## Constructive next connection: downstream emitted-event readout

DOWNSTREAM_EVENT_READOUT_AND_VOLUME_PRECISION.md supplies a distinct
ordinary sensing alternative. At an actual one-way emitted-event port,
downstream detection leaves the native source process unchanged. The
standard cascaded-source commutator cancellation is reconstructed, with
classical-path versus coherent-quantum scope explicit.

For native local event intensity at most C N^2 over physical time N^2,
known detection efficiency eta gives the joint row-error bound

\[
P\{\sup_s N^{-3}\sum_y|\widehat B_y(s)-B_y(s)|>\epsilon\}
\le2^{N+1}
\exp[-c\min\{\epsilon^2N^2/(1-\eta),\epsilon N^3\}].
\]

Thus vanishing loss is sufficient for the volume-speed readout. If the
loss probability is only bounded but is o(1/N), raw counts work without
exact efficiency calibration. Actual delay o(N) is controlled directly
by event counts in recent windows, without asynchronous telescoping.

Fixed loss is a real obstruction at this interface. The explicit
independent-native-walker example has finite detector-error rate
I(e)=eta e^2/[2 lambda T(1-eta)]. Missing Poisson events remain independent
of the entire detected record, so no estimator based only on that record
has superexponentially reliable recovery at fixed nonzero loss.

A finite-rate distributed absorber of length O(log N) realizes the
robust loss bound at the explicit no-unrecorded-loss, linear-unsaturated
counting interface. Competing parasitic absorption creates an efficiency
floor; repeated destructive detectors do not recover a photon already
lost. The proof keeps counter noise, range, sources, clocking and
calibration reliability as actual requirements.

Fixed-energy native emission carries order N^4 energy over the diffusive
horizon at nonvanishing activity. O(N^2 log N) channel material and
additional readout energy may be needed. This can be an attractive
ordinary route when the native stream already exists, but it neither
creates that port for a silent medium nor supplies the elastic layer's
independent thermal preparations. It does not generically supersede the
root compensated continuous-displacement recorder.

## Stronger record escape: fixed-loss tagged-position readout

The fixed-loss obstruction above is specifically for a count-only record.
TAGGED_POSITION_MARKS_REMOVE_FIXED_LOSS_FLOOR.md gives a constructive
escape when the actual outgoing mark additionally identifies the particle
and its wrapped position. For row-confined native particles with unit
steps, shortest-arc reconstruction between detected positions is exact
unless a missed run contains at least N/2 actual steps.

With any fixed detection efficiency bounded below, missed-run lengths
have geometric tails. Across O(N^2) particles and O(N^4) actual events,
the entire reconstructed spatial integrated current has error bound

\[
P\{\sup_t\|Y_N(t)-\widehat Y_N(t)\|_{\rm TV}>\epsilon\}
\le e^{-cN^4}+{\rm poly}(N)e^{-c_\epsilon N^3+C N^2+o(1)}.
\]

Thus fixed loss can suffice at volume speed when the richer actual
record is retained. Initial positions need not be measured: omitting
motion before each particle's first detected position costs one more
geometric run. The proof permits unknown interacting native kinetics;
it conditions on the complete unchanged native path.

This escape is not a general two-dimensional reconstruction theorem.
Small undetected loops can carry spatial current in two dimensions.
Static tags, wrapped-position labels, ordered timestamps, and causal
merging of records are additional physical information and communication
ports. The completed result supplies a causal statistic on that ordered
stream, with data and state requirements explicit; it does not certify a
fixed-bandwidth distributed implementation. The count-only version is
preserved separately and its lower bound is now explicitly labeled by
the actual retained information.

