# Actual noise-reference access, replay, and the residual learning cost

29 October 2026. Focused follow-up after the ordinary score comparison changed
selection. This examines a different physical operation, not a new gradient
estimator. The positive supplier is conventional comparator/DAC metrology.
Its main use here is to identify exactly which added access changes a
learning-cost theorem, and which apparent replay advantages do not survive
complete records or residual noise.

## 1. A concrete device that needs no hidden-state copy or reset

Let an unknown stable analog level theta in [0,1] control a comparator. An
external reference source presents U. At the clock edge, the comparator's
output B=1{U<theta} toggles a visible register X:

    X_next = X xor B.                                 (1)

One reads X before and after the call, hence B is observed regardless of the
initial register value. No register reset is needed. The analog level theta
is unchanged by the readout/control in this declared source model. It can be
an unknown fixed device parameter or a held, stable measurand, not a parameter
we have already measured by another instrument.

With independent uniform U, the native visible kernel is the reversible
binary flip kernel with probability theta. With theta included as frozen
hidden state, every operation preserves uniform X times any law of theta.
The supplied hardware is a reference DAC, comparator, clocked toggle register,
and its readout. These are standard components; no apparatus is built here.
The ideal model first separates their operation from their finite noise and
resolution costs, which Sections 5-7 explicitly reinstate.

There are three genuinely different interfaces:

1. The reference is generated internally; only X is observed.
2. The ACTUAL reference U is also observed/calibrated and retained.
3. A real reference input permits choosing U, not merely replaying an existing
   finite catalog of reference values.

These are source-decision reference controls. They are not the already
available random numbers used to choose which opaque native operation to
call. Exposing an action-selector seed does not expose the random innovation
inside a physical transition.

The threshold architecture is an explicit special supplier. A generic jump
system with rate q(theta) does not thereby acquire a port that makes its
transition equal to a deterministic comparison of a known U with its unknown
flip probability. Replacing an opaque native stochastic operation by this
architecture changes the experiment and its physical resources.

## 2. The statistical interfaces have different precision costs

Take theta in [1/4,3/4] to avoid a boundary rare-event effect.

### Hidden reference: ordinary Bernoulli estimation

The observed increments are iid Bernoulli(theta). Hoeffding gives absolute
error delta with confidence 1-beta using

    n >= log(2/beta)/(2 delta^2).                     (2)

The quadratic precision scaling is necessary. For theta_0,theta_1 in the
stated interval with separation Delta,

    KL(Ber(theta_0),Ber(theta_1))
       <= Delta^2/[theta_1(1-theta_1)]
       <=(16/3)Delta^2.

With n increments, KL is at most n times this value. If a test has error at
most beta in each world, then

    n >= [3/(16 Delta^2)] log[1/(4beta)].             (3)

Here we used the elementary testing inequality alpha+beta>=exp(-KL)/2.
For completeness, Hellinger affinity is at least exp(-KL/2) by Jensen;
TV<=sqrt(1-affinity^2) then gives 1-TV>=exp(-KL)/2. This proves the stated
testing bound without any finite-memory reconstruction argument.

### Recorded reference: a bracket instead of a sample mean

Observe (U_i,B_i). Define

    L=max({0} union {U_i:B_i=1}),
    R=min({1} union {U_i:B_i=0}).

Then theta belongs to [L,R] exactly in the ideal model. If there is a sample
within delta on each available side of theta, R-L<=2delta. The probability
of missing either length-delta interval is at most 2exp(-n delta), so the
midpoint estimate has error at most delta with confidence 1-beta after

    n >= delta^(-1) log(2/beta).                     (4)

This linear precision scaling is also sharp in order. For two thresholds
separated by Delta, records agree exactly when every U avoids the interval
between them. That event has probability (1-Delta)^n; on it the two record
laws are identical. One sample falling in the interval identifies the world.
Thus the optimal equal-prior testing error is exactly

    (1/2)(1-Delta)^n.                                (5)

The information change comes from observing the innovation at the physical
transition, not from a variance-reduction formula imposed on the same data.

### Programmable reference: ordinary successive approximation

Query U at the midpoint of the current bracket. The response chooses one
half. After b calls the interval has width 2^(-b). Absolute error delta needs
only b>=ceil(log_2[1/(2delta)]) comparisons, apart from the trivial small-b
case. This is conventional successive-approximation analog-to-digital
conversion, not a new learning principle.

The DAC must realize those reference levels to the required accuracy; the
comparator must resolve their differences; theta must remain stable; and the
settling, clock, controller bits and sensing costs all remain. A b-bit digital
reference is not an infinitely precise physical voltage. Replaying a finite
set of previously drawn U values cannot locate theta more finely than the
gap in that set containing it; replay alone does not supply arbitrary new
thresholds or the logarithmic query bound.

## 3. Horizon benefit depends on the complete future record

This distinction matters when translating a parameter resolution into a
T-stage prediction guarantee.

If the future service retains only the native visible increments, its law is
Ber(theta)^(tensor T). For theta and an estimate hat_theta in [1/4,3/4],
Pinsker and the preceding KL bound give

    TV <= |theta-hat_theta| sqrt(8T/3).                (6)

Thus delta of order epsilon/sqrt(T) suffices. Under an actual future mode in
which the source-reference values are not retained, the three calibration
interfaces respectively have sufficient call costs of orders

    T/epsilon^2,  sqrt(T)/epsilon,  log(sqrt(T)/epsilon),

with confidence logarithms and real analog precision costs additionally paid.

But if future reference values are retained, the task is stronger. For fresh
independent uniform references drawn after the estimate is chosen, the
complete future record (U_1,B_1,...,U_T,B_T) has exact comparison

    TV = 1-(1-|theta-hat_theta|)^T.                   (7)

Indeed the two laws have identical density when all U values avoid the
inter-threshold interval, and disjoint outputs otherwise. The required
resolution is now of order epsilon/T. An unperformed deletion of the U
record cannot recover (6).

Consequently reference disclosure can improve acquisition AND strengthen the
future prediction task. Comparing the better calibration rate from one
interface with the weaker future record from another is invalid unless the
actual deployment really changes its record interface. For the complete
reference-retained service, active successive approximation still gives a
logarithmic comparison count, but only by supplying reference precision of
order epsilon/T. The passive recorded-reference cost is order T/epsilon.

Old calibration records are preserved in this statement. Conditional on each
good calibration record D, compare the actual future at the same fixed theta
with the reference at hat_theta(D). Averaging this conditional bound under
the SAME actual law of D adds at most the calibration failure mass beta.
It does not regenerate D under the fitted parameter or promise every rare
record-conditioned certificate.

If the future references are already reconstructible from an old retained
seed, they are fixed conditional on that record. Their conditional discrepancy
is the indicator that some recorded reference lies between theta and
hat_theta(D); equation (7) cannot then be applied as a fresh conditional
average. If such early references were themselves drawn iid uniform, the
same-record joint bound is still at most 2Tdelta+beta whenever the estimator
has uniform error delta on its good event: a disagreement requires a reference
within delta of the fixed true theta. This union argument permits the estimate
to depend on the recorded references, but supplies no rare-record guarantee.

## 4. Why recorded randomness does not generally restore a checkpoint

Knowing a random seed does not reconstruct the starting hidden state of an
opaque system. Nor does reversibility of a stochastic kernel make each
noise-conditioned map invertible. The heat-bath kernel P(x,dy)=mu(dy) is
self-adjoint in L2(mu), but its natural realized map is F_u(x)=u. Replaying u
does not recover the discarded x. Recovering it requires extra history
storage, actual state readout, or a different reversible implementation.

There is a sound ordinary checkpoint supplier under stronger physical access.
Suppose the actual noise-conditioned operation F_(j,u) is a bijection and
the apparatus has its actual inverse, using the retained u. For a realized
word F_(j_T,u_T)...F_(j_1,u_1), executing the inverse calls in reverse order
returns the entire represented state exactly. A second controller can then
be run on the same specimen. No microscopic copy is made.

Classical reversible logic implements this on declared logical registers.
One simple primitive is a self-inverse controlled XOR gate, including unknown
fixed wiring or hidden control bits. The same gate and control key undo its
logical action. Ordinary history-preserving reversible simulation extends
the construction to irreversible computations at explicit storage and
recomputation costs. These are Bennett's established mechanisms, not an
operation inferred from detailed balance.

This is not a claim of reversing every microscopic bath degree of freedom.
For a physical logical-register realization, require a conditional per-call
failure probability at most e for the declared map, uniformly over the
relevant histories. A T-call forward trajectory followed by T inverse calls
then fails to restore its checkpoint with probability at most 2Te, by a
sequential coupling/union bound. A long branching experiment pays all its
forward/inverse calls and the corresponding total error budget. Merely
recording an average logical truth table does not supply this uniform premise.

Reusing one checkpoint also does not create independent draws of its hidden
initial state. Coupled comparisons can be legitimate, but an expectation
over unknown initial states still needs its actual baseline sampling source.
There is no demonstrated general removal of the controller-horizon cost by
this conventional checkpoint mechanism.

## 5. Fresh intrinsic noise restores a quadratic precision burden

Now give the programmable reference every adaptive advantage, but suppose
each comparison contains independent unobserved residual noise:

    B_k=1{U_k < theta+sigma Z_k},  Z_k iid N(0,1).      (8)

U_k may depend on the entire previous record, all private controller randomness,
and any replayed external reference. Sigma>0 is fixed. Under two thresholds
separated by Delta, conditional on a common previous record, B_k is obtained
by thresholding a Gaussian whose means differ by Delta. Data processing gives

    KL(one next observation) <= Delta^2/(2sigma^2),

uniformly in the chosen U_k. The adaptive KL chain rule gives

    KL(complete n-call records) <= n Delta^2/(2sigma^2).

The same testing inequality as above therefore requires

    n >= (2sigma^2/Delta^2) log[1/(4beta)]              (9)

to distinguish both worlds with error at most beta. This remains true with
adaptive threshold selection, external-noise replay, unlimited computation,
and all those controller records retained. It concerns the specified fresh
Gaussian residual, not an unconditional law of every possible apparatus.

The logarithmic ideal comparison count is useful only above the actual
residual noise/precision scale or after paying to reduce that residual.
Bounded-error comparisons illustrate the same crossover constructively. If
each combined reference/comparator error has magnitude at most e, preserve
overlapping brackets: for B=1 raise L only to U-e; for B=0 lower R only to
U+e. Each call gives width_new<=width_old/2+e. After b calls,

    width <= 2^(-b)+2e.                              (10)

Thus accurate analog setting and decision precision, not just a small number
of digital comparisons, are load-bearing resources.

## 6. Holding the same noise does not give repeated independent information

An ordinary sample-and-hold has a different noise pattern. During one held
conversion block, let

    V=theta+eta,   eta~N(0,sigma^2),

and permit arbitrarily many adaptive comparator queries or exact readout of V.
The entire block depends on theta only through this single V. Its KL between
two theta values is at most Delta^2/(2sigma^2), regardless of the number of
binary-search or replay calls within the block. The lower bound (9) now
counts fresh independently sampled blocks, not comparator decisions.

Binary search can accurately learn the held noisy voltage; it cannot separate
theta from its one unknown held offset. Replaying the same noise has removed
comparison inconsistency but has not created new information about theta.

A selective noise checkpoint genuinely changes that statement if it is an
ACTUAL additional observation. Suppose the block also supplies

    R=eta+xi,  xi~N(0,nu^2), independent of eta.

With known variances, subtract [sigma^2/(sigma^2+nu^2)]R from V. The remaining
noise is independent of R and has variance

    sigma_eff^2=sigma^2 nu^2/(sigma^2+nu^2).            (11)

The complete joint-record KL is exactly Delta^2/(2sigma_eff^2). A true noise
checkpoint reduces the relevant residual. It is not free information about
an otherwise inaccessible bath, and if nu remains positive the quadratic
small-Delta rate returns. If only contrasts are requested and an identical
additive offset is physically shared between two measurements, ordinary
differential sensing can cancel that common part; independent residuals remain.

## 7. A real selective-checkpoint architecture, and its unremoved noise

Sampling-noise cancellation in switched-capacitor converters is a concrete
ordinary supplier of this kind of extra information. The physical operations
hold an input, freeze a sampling-noise contribution on a capacitor, amplify
that held error into a second storage element, and subtract its correlated
contribution. This is a selective analog memory operation, not copying an
arbitrary microscopic specimen.

Gu et al. (2024), read in full at its sampling-phase discussion, provide a
particularly explicit comparator. Their presampling capacitor C_0 holds the
input fixed while noise on C_1 is measured/cancelled through the amplifier
and C_2. Their model leaves a C_1 noise residue proportional to

    (k_B T/C_1) exp(-2 Delta_t/tau_amp).

They also explicitly retain uncancelled sampling noise on C_0, and their
reported implementation is a circuit simulation. This source prevents an
overclaim that k_B T/C_1 is an immutable bound for every augmented converter,
while also preventing a claim that cancelling one stored noise component
eliminates the full input-referred residual.

For an ordinary passive sample-and-hold, equipartition of the capacitor energy
C(V-theta)^2/2 gives voltage variance k_B T/C. Equivalently it is obtained by
integrating the resistor's thermal spectrum through its RC filter. Larger C,
lower temperature, longer settling, an amplifier/checkpoint circuit, or more
fresh samples can change the implementation budget. The capacitor expression
is NOT a universal energy lower bound for every active sensing architecture.
In particular stored energy is not automatically dissipated energy, and
correlated-noise cancellation must be compared before claiming a capacitance
lower bound for an augmented circuit.

DAC calibration, comparator offset/hysteresis, bandwidth, input loading,
independent amplifier noise, leakage, clock jitter, charge injection and
source drift are part of an actual supplier. A digital record of an intended
reference level is not proof that the realized analog reference was exact.
The construction has not supplied an equivalent noise-observation port for
the inherited hidden jump/diffusion families.

## 8. Consequence for the research direction

An actual source-reference or selective-noise-memory port can change learning
precision exponents without copying hidden state. Ordinary comparator/DAC
metrology and noise-cancellation circuits are strong examples. A theorem for
an opaque native menu should exclude these additional ports explicitly when
its lower bound needs their absence; the existence of those ports in a
different architecture is not a contradiction.

Conversely, common random numbers, recorded selector seeds, detailed balance,
or a held noisy specimen do not by themselves supply microscopic replay or
extra independent information. A universal benefit would require an actual
noise-conditioned inverse/checkpoint or a controlled residual-information
contract. The strongest conventional implementations already exploit those
contracts where available. No new apparatus, exclusive learning mechanism,
or general defeat of a horizon lower bound is established here.

## Primary-source receipts and read scope

- Analog Devices, *Understanding SAR ADCs: Their Architecture and Comparison
  with Other ADCs* (2001),
  https://www.analog.com/en/resources/technical-articles/successive-approximation-registers-sar-and-flash-adcs.html .
  Read the comparator/DAC binary-search construction, capacitive hold, and
  settling/linearity/calibration constraints. The logarithmic comparison
  procedure above is this established ordinary method.
- Analog Devices, *Comparator/DAC Combinations Solve Data-Acquisition Problems*
  (2002), https://www.analog.com/en/resources/technical-articles/comparatordac-combinations-solve-dataacquisition-problems.html .
  Read the actual reference-input architecture and loading, hysteresis and
  settling considerations. No current device-price or performance claim is
  inferred from this historical application article.
- P. Glasserman and D. D. Yao, *Some Guidelines and Guarantees for Common
  Random Numbers*, Management Science 38, 884-908 (1992),
  https://business.columbia.edu/sites/default/files-efs/pubfiles/4261/glasserman_yao_guidelines.pdf .
  Read the construction, synchronization discussion and the role of
  monotonicity/continuity. Deliberate coupling is established; its mathematical
  representation is not itself permission to replay an inaccessible bath.
- Y. Gu et al., *An improved kT/C noise cancellation technique with presampling
  for high-speed SAR ADCs*, Electronics Letters 60, e13298 (2024),
  https://doi.org/10.1049/ell2.13298 . Read the sampling phases, residue model,
  uncancelled C_0 term, and circuit-simulation scope. No fabrication or measured
  apparatus claim is transferred to the present construction.
- H. Nyquist, *Thermal Agitation of Electric Charge in Conductors*, Physical
  Review 32, 110 (1928), https://doi.org/10.1103/PhysRev.32.110 . Publisher
  abstract/metadata read; the primary scan retrieval timed out. The capacitor
  variance is independently derived above and supported by Analog Devices'
  primary engineering discussion of sample-and-hold noise:
  https://www.analog.com/en/resources/technical-articles/2022/07/16/11/45/managing-noise-in-the-signal-chain-part-2-noise-and-distortion-in-data-converters.html .
- C. H. Bennett, *Logical Reversibility of Computation* (1973),
  https://doi.org/10.1147/rd.176.0525 , and *Time/Space Trade-Offs for Reversible
  Computation* (1989), https://doi.org/10.1137/0218053 . Primary indexed
  abstracts and the first theorem's indexed statement were read; direct full
  text retrievals failed. No detailed time/space theorem is imported here.
  The inverse-word identity above is proved directly and is credited as the
  ordinary reversible-computation mechanism.

The preserved Astra mission, current handoff and scientific-acceptance scope
from the completed unit continue to govern. N675 was not reopened. No new
agent, transfer or apparatus operation was performed.
