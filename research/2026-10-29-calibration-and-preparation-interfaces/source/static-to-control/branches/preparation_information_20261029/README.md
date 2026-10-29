# Astra P1: physical information sufficient for controlled prediction

29 October 2026. This continuation preserves the complete physical-information
and hidden-memory predecessor. Its central result is a native principle:
within a specified thermal kinetic class, a sufficiently low baseline entropy
rate and a sufficiently accurate COMPLETE position distribution select one
Gibbs explanation that remains valid across an entire bounded force-control
interface. Exact continuous paths can still distinguish that explanation.
The way memory is ACQUIRED determines whether it can turn that distinction
into a macroscopic intervention response.

## Scientific destination and choice

The intended capability is reusable physical prediction without identifying
every microscopic force or eliminated trajectory. Success must control the
chosen consequences under interventions, not only fit passive means or print
a long timescale. The earlier orientation, entropy-floor and equilibrium-tree
results remain capital at their stated hidden-model interfaces.

A materially different quantum-reference randomization opening was explored
using current Astra N994/N995 and primary material. Its complete-binary result
does not by itself settle the general matrix contraction obstruction. The
native thermal route earned continued depth because its main obstruction
could be attacked constructively: known bath noise regularizes force occupation,
while the stationary entropy identity constrains the remaining force balance.
Current Astra N1220 sharpened the separate baseline/intervention information
question; its abstract model was not presumed to be a native physical system.

## 1. The native source class and the consequence guarantee

Positions q lie on a fixed connected flat torus; momenta p have unit mass.
The baseline is stationary and obeys

    dq=p dt,
    dp=[F(q)-gamma p]dt+sqrt(2gamma tau)dW,
    |F|<=A, gamma,tau>0.

All momenta are directly thermalized by the specified bath. Positions are
even and momenta odd under actual reversal, with no odd external field.
The finite-entropy/Fisher and integration-by-parts domain is explicit.
No uniform derivative bound on F is required. The physical entropy is

    sigma=gamma tau E|grad_p log[rho/(nu M_tau)]|^2.

This is a warranted physical identity, not an arbitrary visible reversal
divergence. Dimension, geometry, bath, source force ceiling and finite time
window stay fixed.

For a smooth periodic potential U with |grad U|<=A, let nu_U be its Gibbs
position law. Suppose sigma<=s and W1(nu,nu_U)<=e. Apply the SAME bounded
Borel Markov force u(t,q,p), |u|<=B, in the momentum equation of source
and candidate, each starting from its own baseline stationary preparation.
The new theorem controls their entire finite-window paths uniformly over u.
The SAME U works for the whole interface; fitting a new model per control
is unnecessary. Controlled work/entropy need not be small.

The qualitative theorem in **BOUNDED_MARKOV_FORCE_INTERVENTIONS.md** has
the order infimum over U BEFORE supremum over controls. Its independently
reviewed static-selection corollary is in **STATIC_INFORMATION_TO_CONTROL.md**.
The later **QUANTITATIVE_CONTROL_FROM_STATIC_INFORMATION.md** supplies
a rate in fixed analytic constants:

    error <= 2 E0 + 2 R_T(h) + 2 C_imp T eta h^(-15/16),
    E0 <= sqrt[s/(4gamma)] + C_pos e^(1/4)/2,
    eta <= C_force (sqrt(s)+e^(1/4))^(1/[12(d+1)]).

Here h=T/m<=h0 is a regular time mesh and R_T is an explicit Brownian/native
interpolation error of order sqrt(h log(T/h)). The bound concerns the bounded
Lipschitz distance for uniform physical paths. Uniform momentum moments give
every finite Wasserstein order, hence appropriate finite-window unbounded
observables as well. It does not integrate survival over infinite time.

The displayed constants are named and their dependencies specified. Numerical
upper bounds for the free-semigroup, product and dyadic-cutoff constants have
NOT been instantiated. The theorem supplies a quantitative mathematical bridge,
not an executed numerical stopping schedule or a practical performance claim.

## 2. Why the passage from information to dynamics is valid

The ordinary proofs identify the native generator, not just a reversible
visible process. Conditional Gaussian logarithmic Sobolev controls deviation
from Maxwell momenta. A common free-path likelihood and compact occupation
operator identify weak limits of bounded forces, including moving controls.
Stationarity then forces the Gibbs relation grad nu=F nu/tau.

For the quantitative extension, free Duhamel smoothing gives a uniform L1
position translation modulus of order |shift|^(1/3), without a force derivative
bound. A weak complete-position fit to a bounded-gradient Gibbs candidate
therefore yields an L1 density fit of order e^(1/4). The stationary momentum
identity controls F nu-tau grad nu by sqrt(sigma) in a negative norm. Dividing
only by the KNOWN candidate Gibbs density gives a weak norm of F+grad U.
Low/high Fourier blocks convert it to the kinetic negative Besov norm eta.

Conventional kinetic Schauder estimates and Bony products then give a uniform
short-time TRANSITION-TV bound C_imp eta h^(1/16), valid for bounded Borel
common feedback and all initial native states. Transition coupling plus
Brownian interpolation yields the path bound above. All these new uses have
ordinary proofs and scoped independent checks. No hidden contraction is fitted
or assumed. The sources and strongest conventional comparison are in
**sources/PRIMARY_SOURCE_INDEX.md** and the frontier comparison notes.

## 3. Memory is determined by its acquisition interface

**FIXED_SENSOR_FINITE_MEMORY_CONTROL.md** proves the qualitative guarantee
for finite scheduled fixed path-sensor kernels, finite reported alphabets
and all bounded branchwise Markov controls. The reference law includes actual
sensor randomness; causal sensor laws survive the feedback change of measure.
The controller retains its acquired report history. It is not assumed to be
a thermally reset hidden variable.

The quantitative transition estimate also composes for current-state snapshot
experiments, retaining arbitrary standard-Borel report histories, even exact
state values. **physical_frontier/CONDITIONAL_SNAPSHOT_CONTROL_COMPOSITION.md**
gives joint record TV at most E0+(m+T/h0)C_imp eta for at most m report-driven
intervals, with no minimum gap. Next times use previous reports; unreported
path-triggered timestamps are excluded. This controls the entire acquired
record and subsequent decisions, not only separate marginals.

The complementary **causal_frontier/ONE_BIT_CAUSAL_CONTROLLER_BOUNDARY.md**
proves that ONE retained bit can defeat a uniform extension to changing
fine-path sensing. The source is a bounded oscillatory thermal shear with
sigma_n tending to zero. A changing path score has a fixed mean gap from
every admitted bounded-force Gibbs model. A clipped randomized test creates
one bit; a known independent free thermal reporter, driven by bounded force,
turns its probability gap into a fixed noisy binary output gap.

The reporter contracts statistical TV and consumes ordinary external work.
One retained bit does not bound the prior path precision, analog accumulation,
temporary memory, computation or preparation. For the specified adaptive
Gaussian position-sensor interface, a fixed useful bit gap requires a gain/
precision budget of order at least 1/sigma_n. That is not a lower bound for
arbitrary force-feature access. The candidate class must retain the reporter's
declared free independent structure. All these qualifications are proved.

## 4. Finite acquisition and strong conventional execution

**alternative_frontier/FINITE_POSITION_SELECTION_BRIDGE.md** gives a finite
selection route from genuinely independent complete native configurations.
An ordinary transport LP fits grid probabilities subject to Gibbs
log-Lipschitz ratio constraints. McShane extension and smoothing return an
exactly bounded-gradient potential. The record includes positional error,
dimension-dependent statistical cost, grid/smoothing error, rational coefficient
intervals, primal/dual gap and integration precision. An exhaustive potential
net is also constructed and is much less attractive on the same information.

The executable **certified_gibbs_grid_selection.py** uses a floating solver
only to propose a candidate, then verifies exact rational constraints and
optimization error. Its eight-point arithmetic fixture certifies total
optimization error at most 5.818852122984356e-11. This is an arithmetic
control, not an acquired native record or a controlled simulation.

The static source approximation can itself be bounded: an explicit Gaussian
bridge gives a stationary POSITION density floor, and smoothed Boltzmann
inversion followed by scaling restores force ceiling A. It yields a
conservative O(sigma^(1/(2d+4))) static fit rate. This floor does not regenerate
momentum or erase controller history. The learned-candidate control theorem
does not need this source-floor lemma.

**physical_frontier/FINITE_PHYSICAL_ENTROPY_UPPER_ACQUISITION.md** supplies
an entropy UPPER certificate from genuinely iid full phase configurations,
using the native energy identity, a proved fourth moment, finite-range
saturated momentum observations and median-of-means. Count, range, momentum
precision, bath calibration and arithmetic are separate costs; no physical
record was acquired. Independent preparations, Gibbs initialization, actual
control descriptions and numerical execution remain additional costs. Arbitrary mathematical Borel
controls need not be computable. No computational speedup over ordinary
equally informed fitting/solving is claimed.

## 5. Reusable constructive capital retained in this tranche

**GENERAL_THERMAL_MEMORY_METRICS.md** solves an important narrower acquisition
interface exactly. For an autonomous equilibrium driver applying a one-way
force f to a thermal receiver, heat is the compressed-resolvent form
<f,H_gamma f>/tau, while the nearest same-bath Gibbs path cost is the ordinary
force norm ||f||^2/(4gamma tau). Actual lag pairs acquire finite matrices H,G
for a whole force family; frozen one-time information does not supply H.
No uniform spectral floor is inferred from positivity alone.

**ACQUISITION_TO_PREPARATION.md** replaces an ideal history oracle by forward
warm preparation, conditional on a genuinely fresh equilibrium driver. Its
initial-state error controls every future common experiment without multiplying
by the future horizon. A finite-bit censored lag clock is constructed and
checked exactly, with timing, feature sensitivity, censor, sensor and arithmetic
errors charged. Waiting does not create a fresh microscopic iid reset.

**THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md** and
**THERMAL_FORCE_INFORMATION_SPECTRUM.md** retain the exact shear failure,
native Gibbs KL/TV floors, negative-half-Sobolev heat form and qualified repairs.
Full-path mismatch persists while physical heat vanishes; finite-resolution
or finite-window consequence guarantees answer a different question.

The native phase and relational-pair constructions show that complete separate
baseline laws can miss actuator-frame alignment. A genuinely simultaneous
quadrature pair resolves the known SO(2) relation with explicit error. Ordinary
phase alignment is the comparator. The static Gibbs-assay quadratic trial
lower bound is not a general dynamical acquisition bound: an exact dynamic
force-feature score supplies a decisive counterexample.

The finite-parity projection/Pythagoras result, local thermalization, earlier
entropy and hidden-memory constructions, and the alternative quantum opening
remain preserved at their actual scopes. **CORRECTIONS_AND_SCOPE.md** records
load-bearing distinctions and the review lineage. **HANDOFF.md** identifies
the live scientific frontier without replacing the user's assignment.
