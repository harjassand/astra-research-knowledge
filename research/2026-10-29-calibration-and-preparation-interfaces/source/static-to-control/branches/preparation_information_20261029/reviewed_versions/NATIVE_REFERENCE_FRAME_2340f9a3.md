# Native reference-frame identifiability in a thermal shear source

29 October 2026. Complementary construction and challenge of the root's new
native phase proposal. Ordinary proofs below. No hardware, field calibration,
Gibbs preparation or experimental record was acquired.

## 1. Complete baseline equivalence, with the observation fixed

Let x,y be angles modulo 2pi and let v,w be momenta. The driver is

    dx=v dt,
    dv=-gamma_d v dt+sqrt(2 gamma_d tau)dW,

and the receiver is

    dy=w dt,
    dw=[a sin(nx+phi)-gamma w]dt+sqrt(2 gamma tau)dB.

All displayed constants except phi are known and positive, and n is a known
positive integer. The common initial preparation has uniform independent
x,y and independent Maxwell v,w of variance tau. Observe the complete y,w
path, optionally also the scalar force feature f=sin(nx+phi), and even v if
desired. The LAB-FRAME x coordinate is not included in this baseline record.

**Exact equivalence.** Every such full baseline path law, on every horizon,
is independent of phi. To couple phases phi and phi', shift the initial x
coordinate by (phi-phi')/n and use identical v,W,B,y,w. The driver dynamics
and uniform preparation are translation invariant, and
n x'(t)+phi'=n x(t)+phi at all times. Thus the entire declared observations
agree pathwise. More baseline samples, longer records, finer timing and
adding the scalar force feature cannot identify phi in this interface.

The same statement holds for record-driven additive receiver controls that
do not act on x/v: equal histories produce equal controls under this coupling.
It does not hold if the calibrated lab-frame x is also observed, or if an
actuator/preparation has already supplied a nontranslation-invariant driver
reference. Those are additional physical information, not counterexamples.

## 2. A physical reference potential changes the experiment

Permit the calibrated driver potential

    U_psi(x)=-u cos(nx-psi),      u>0,
    dv=[-gamma_d v - n u sin(nx-psi)]dt
                                      +sqrt(2 gamma_d tau)dW.       (1)

The driver is autonomous: there is no receiver-to-driver backaction in this
model. Supply an actual Gibbs driver preparation under this potential and
hold the potential during the trial. Its x density is

    p_psi(x)=exp[c cos(nx-psi)]/[2pi I0(c)],
    c=u/tau,
    I_k(c)=(1/(2pi))int_0^(2pi) exp(c cos z)cos(kz)dz.

The velocity remains independent Maxwell. Elementary angle integration gives

    E sin(nx+phi)=r(c) sin(phi+psi),
    r(c)=I1(c)/I0(c)>0.                                  (2)

For a receiver begun independently in its free Maxwell law, the finite-time
mean is EXACTLY

    E w(h)=R_h sin(phi+psi),
    R_h=(a/gamma)r(c)(1-exp(-gamma h)).                    (3)

The stationary receiver formula (a/gamma)r(c)sin(phi+psi) requires the
receiver to have reached its stationary driven mean, or the h->infinity
limit. Gibbs preparation of the DRIVER alone does not remove the finite
receiver factor in (3). This is a necessary qualification to the proposed
operation, not an obstruction to it.

At psi=0 and psi=pi/2, the two means are R_h(sin phi,cos phi). They identify
phi modulo 2pi within this declared source family; atan2 of the first and
second means gives the phase. A single fixed psi retains a reflection
ambiguity: x->2psi/n-x, v->-v transforms phi to pi-2psi-phi while preserving
the potential and the declared y,w,force-feature law. The two settings
remove that particular ambiguity, as the two quadrature means already show.

This does not identify arbitrary hidden models compatible with the record.
The known sinusoidal family, frequency, bath, sensor and actuator semantics
are the structural information supporting the conclusion.

## 3. General symmetry/reference theorem

Let a group G act by measurable invertible transformations on hidden states
and on source parameters. Suppose the uncontrolled generators and starting
laws transform covariantly, while the reported observation is unchanged by
the simultaneous transformation. Then the observable baseline experiment
is constant on each G orbit of parameters. The proof is simply pushforward
of the full hidden path law; it is valid for complete records, not just
equal moments.

Now include preparation and control kernels. If a subgroup H of G fixes
the ACTUAL labeled preparation/control/readout interface and conjugates
each native kernel appropriately, the same induction over causal policies
shows that every allowed experiment is constant on H orbits. An identifiable
consequence must be H-invariant. A consequence that changes along such an
orbit cannot be learned from that interface even with perfect infinite data.

Adding a reference operation can reduce H and therefore change this
identifiability obstruction. Merely reducing H is not a universal sufficient
identification theorem; nongroup ambiguities may remain. In the explicit
sinusoidal family, (2)--(3) additionally prove the sufficient identification
statement.

For the present source, a translation x'=x+delta/n changes the parameter
and action labels as

    phi'=phi-delta,       psi'=psi+delta.

The combination phi+psi is invariant. What is acquired is the RELATIVE
alignment between the native force and the actuator. An unknown constant
phase offset of the actuator can be absorbed into the fitted relative phase
if all future settings use that same reproducible actuator. Absolute phase
in an external laboratory frame requires an additional calibration. Future
response prediction does not require claiming an otherwise meaningless
absolute phase.

These symmetry and reference-frame principles are established ideas in
physics and statistics, not new general discoveries. The contribution under
construction is this explicit native thermal experiment, its full baseline
equivalence and the resource accounting of the new physical reference.

## 4. A complete finite receiver-mean acquisition schedule

Assume independent trials with the supplied Gibbs driver preparation,
independent free receiver Maxwell preparation and fixed duration h. Then

    w(h)=zeta(h)+Y^0(h),
    zeta(h)~Normal(0,tau),
    |Y^0(h)|<=B_h=(a/gamma)(1-exp(-gamma h)),

where zeta is independent of the driver. Thus w(h)-Ew(h) is sub-Gaussian
with variance proxy s_h^2=tau+B_h^2. This charges thermal fluctuations;
the count of mean queries does not provide instrument precision.

With N trials at EACH of psi=0,pi/2, both empirical means deviate by at
most R_h sin(delta)/sqrt(2), with failure probability at most alpha, if

    N >= [4s_h^2/(R_h^2 sin(delta)^2)] log(4/alpha),
    0<delta<pi/2.                                        (4)

The empirical two-dimensional vector is then within R_h sin(delta) of the
true vector of length R_h. Its angle differs by at most delta. Add actual
mean-readout noise to s_h^2 if it is independently Gaussian/sub-Gaussian;
systematic calibration errors require an explicit bias allowance instead.

Equation (4) is an ordinary sufficient sample schedule, not an optimality
or speed claim. It requires 2N complete trial preparations, 2Nh receiver
observation time, actuator switching/calibration and the actual readouts.
If a driven stationary receiver is used instead, its preparation/burn-in
cost must replace the free-receiver start and the finite-horizon factor.

Approximate Gibbs preparation must be warranted independently. A TV error
epsilon in the driver path start changes the bounded Y^0 mean by at most
2B_h epsilon. A known initial receiver-mean error b_0 contributes
exp(-gamma h)|b_0|. These biases must be smaller than the mean-error margin
in (4). A fitted baseline law does not certify this preparation. Standard
Langevin equilibrium theory warrants the target law for each fixed smooth
potential, but no uniform finite-time mixing/preparation certificate is
constructed here. Independent starts or valid dependence-aware statistics
remain actual resources.

## 5. Bounded actuator force and static information per preparation

The actuator force amplitude is n u. Under a known ceiling n u<=A,

    c<=A/(n tau),
    r(c)<=c/2,
    R_h<=a A(1-exp(-gamma h))/(2 gamma tau n).             (5)

The ratio bound follows term by term from the positive I0,I1 series. A
fixed-size mean signal cannot be retained while increasing n at fixed A.
The sufficient mean schedule (4) therefore grows quadratically in n at
fixed other parameters. This does NOT prove a quadratic lower bound for
arbitrary full controlled-path measurements.

There is an exact per-trial information theorem for a narrower static
assay. After one Gibbs driver preparation, observe its phase feature at
one instant, with no subsequent dynamical record. In the stronger
coordinate z=nx+phi mod2pi, its density is the von Mises law

    p_theta(z)=exp[c cos(z-theta)]/[2pi I0(c)],
    theta=phi+psi.

Even this stronger phase readout has

    Fisher_theta = c r(c),
    D(p_theta||p_theta')=c r(c)[1-cos(theta-theta')].       (6)

The Fisher identity follows by integrating the derivative of
sin(z-theta)p_theta(z); the KL identity follows directly from the
exponential-family density. Actual scalar sin(z) observations, detector
noise and postprocessing cannot increase the KL. Therefore N independent
static Gibbs-preparation trials, with adaptive psi and u satisfying
n u<=A, have

    D(transcript_phi||transcript_phi')
        <= N A^2/(n^2 tau^2).                             (7)

The settings are held the same at a common history, so the ordinary KL
chain rule proves (7) even for adaptive phase choices. To distinguish two
phases with transcript TV at least delta requires

    N >= 2delta^2 n^2 tau^2/A^2.                          (8)

This is a rigorous quadratic bound for the declared ONE-TIME PREPARATION
READOUT assay. It is not a limit on native dynamics after preparation.
The companion EXACT_FORCE_FEATURE_DYNAMIC_INFORMATION.md constructs a
decisive counterexample to that overextension.

### Strong equally informed alternative: a paired actuator-feature record

If the baseline can additionally observe the ACTUAL actuator-frame feature
g_psi=cos(nx-psi) jointly with f=sin(nx+phi), then under free uniform phase

    E[f g_psi]=(1/2)sin(phi+psi).

Two quadratures identify the same relative phase without a Gibbs driver
preparation. This is additional paired physical information; separate
marginal laws of f and g_psi are both independent of phi and do not supply
the joint covariance. If x in the actuator frame is observed, g_psi is
already available, so the original baseline ambiguity is absent.

Ordinary equilibrium response theory expresses the first derivative at
u=0 as (1/tau)Cov(f,g_psi). With the known sinusoidal source class, the
same acquired phase and the Bessel formula predict the full prepared mean
for all u,psi,h. This is a strong conventional matched-information route.
The proposed active assay does not outperform it without an actual cost
comparison of the available sensors and preparations.

Measuring g_psi in normalized feature units still demands the spatial
resolution of its n-dependent phase. If a device instead reads the small
potential energy -u g_psi with a fixed absolute noise floor, normalizing by
u amplifies that noise; bounded force u<=A/n does not provide this precision
for free. The scalar native force feature by itself remains insufficient.
With the stronger actually supplied local QUADRATURE pair, the root's
mechanism verified in RELATIONAL_PHASE_PAIRING.md gives a one-pair deterministic
alternative and makes the calibration precision explicit.

## 6. Preparation and calibration costs

Setting psi within phase error delta_psi means locating the spatial field
origin to error of order delta_psi/n. Thus fixed phase accuracy at growing
n still requires increasing spatial calibration resolution. A bounded
force amplitude does not bound the field derivative or hardware bandwidth:
with u=A/n the force derivative has amplitude nA. Creating that field,
calibrating the bath/temperature, and resetting/preparing the driver are
not provided by the Bessel formula.

For a concrete ideal thermodynamic preparation cycle, quench from the free
driver potential to U_psi, equilibrate, perform a noninvasive readout,
quench back to zero and re-equilibrate. The mean quench-on work is zero
from uniform x; the mean quench-off work is u r(c). Thus this specific
driver cycle dissipates u r(c), or c r(c) in units of tau. It equals the
static full-phase Fisher information in (6). The two relaxation entropy
contributions are log I0(c) and c r(c)-log I0(c).

This is an identity for the stated abrupt cycle, NOT a universal minimum
work per bit or per Fisher information. Quasistatic reversible preparation
and return trade additional time for smaller dissipation; readout-record
storage/reset and the receiver's dynamics also have separate costs. No
actual cycle or preparation time bound was acquired.

## 7. Primary antecedents and assessment

Reference-frame absence and symmetry-restricted information are established:
Bartlett, Rudolph and Spekkens, Reviews of Modern Physics 79, 555 (2007),
https://arxiv.org/pdf/quant-ph/0610030, explicitly develops relational frames
and their information role. Marvian and Spekkens, Physical Review A 90,
062110 (2014), https://arxiv.org/pdf/1312.0680, treats symmetric operations
and the asymmetry resources required to implement reference-dependent
operations. These are quantum frameworks, cited as antecedents for the
principle, not as proofs of this classical stochastic construction.

The von Mises integrals, Fisher information and exponential-family KL are
standard. Kitagawa and Rowley, arXiv:2202.05192 (2022), provides a primary
comparison for statistical divergences of von Mises--Fisher distributions.
The formulas used here are proved directly above. No novelty is claimed
for circular statistics or phase-sensitive detection.

The strongest equally informed route is ordinary phase calibration through
the actual actuator, with full force/dynamics inference when the requisite
continuous record and resolution exist. The addition is a physically native
baseline/intervention identifiability separation with the missing reference
made explicit, plus its scoped acquisition costs and the failure of a
static-information ceiling when dynamical information is supplied.
