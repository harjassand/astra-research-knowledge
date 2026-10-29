# A physical family which removes kinetic memory from collective response

29 October 2026. Root construction. Positive-generator convention:
evolution is exp(-tA). This document is an explicit mathematical physical
supplier, not a claim that an apparatus has been built.

## 1. The capability

The intended receiver is a many-body visible dynamics whose equilibrium
law is fixed but whose motion is modulated by inaccessible, persistent
microscopic information. A selective operation continually agitates only
the modulation coordinates. A local variance-to-mean budget then controls
the entire visible response operator at every deterministic time, without
an inverse visible-gap or volume factor. Critical slowing down and
conservation-induced slow modes do not by themselves spoil this budget.

The selective operation is an added physical resource. An ordinary
controller given it can use the same procedure. The claim is not an
advantage over a controller supplied with stronger addressability,
resetting or phase-reversal controls.

## 2. Exact native architecture

Let Y have a finite configuration space with a warranted probability pi.
For each update class i, E_i is the conditional heat-bath projection in
L2(pi); put A_i=I-E_i. Thus A_i is an orthogonal projection. Examples
include a single-spin Gibbs refresh and a fair refresh of 10/01 on a
particle-conserving bond. The latter is identity on 00/11.

Each native mobility lambda_i(Y_outside_i,H) is nonnegative and unchanged
within the i-th refresh class. The actual positive generator is

    B=sum_i lambda_i A_i.                           (1)

The common hidden law nu is independent of Y. Because each multiplication
lambda_i commutes with E_i, (1) is self-adjoint and nonnegative in
L2(mu), mu=pi tensor nu. It is an actual reversible jump generator.
Unknown kinetic amplitudes do not change the exact Gibbs ratios. An
additional mu-reversible, visible-preserving hidden generator can be
included when it annihilates visible functions and does not invalidate
the declared bath and common-equilibrium structure.

Let P average the hidden variables. Write

    m_i=E_nu lambda_i,
    a=PBP=sum_i m_i A_i,
    b u=QBPu=sum_i (lambda_i-m_i)A_i u.              (2)

Assume centered local mobilities are orthogonal conditional on Y, and
their variances obey

    Var_nu(lambda_i|Y) <= M m_i(Y).                  (3)

Then, for visible u,

    ||bu||^2=sum_i E_pi[Var(lambda_i|Y)|A_i u|^2]
       <= M sum_i E_pi[m_i|A_i u|^2]
       = M <u,a u>.                                (4)

The last identity uses that m_i is constant within its refresh class
and A_i^2=A_i. No independence of the visible spins is assumed. For a
general reversible endpoint update only A_i^2<=2A_i is automatic; the
projection constant must not be transplanted to that case.

More generally, a conditional covariance matrix bound

    Cov_nu(lambda|Y) <= M diag(m_i(Y))               (5)

in the positive-semidefinite order proves (4). Independent local
modulators are one actual supplier. Bounded overlap can supply a bounded
factor. Local sensing alone does not certify the absence of arbitrary
unmeasured long-range hidden covariance.

## 3. Continuous hidden state with frozen microscopic information

Let Z be an arbitrary frozen hidden variable, possibly shared across all
sites. Conditional on Z, take independent uniform phases theta_i on
[0,2pi). Let

    lambda_i=s_i(Y_outside_i)
       [1+alpha_i(Y_outside_i,Z) cos(theta_i)],
    |alpha_i|<=a0<1,       0<s_i<=smax.              (6)

The mean s_i is independent of Z. The amplitudes may be arbitrary
unknown functions of Z and of the unchanged visible context. The
native jumps leave Z and all phases unchanged.

The supplied added operation is independent phase diffusion,

    L_bath=kappa sum_i d^2/dtheta_i^2,              (7)

which leaves Y,Z unchanged. Its physical coefficient kappa has units
of inverse time. Define H=-sum_i d^2/dtheta_i^2 and A=B+kappa H.
Each phase fiber has gap one in angular units. Z never mixes or resets.

For fixed Z, E_theta lambda_i=s_i and
Var_theta(lambda_i)=s_i^2 alpha_i^2/2. Moreover bu has zero phase mean
conditional on (Y,Z). If R averages only phases, then

    <v,bu>=<(I-R)v,bu>,
    ||(I-R)v||^2 <= <v,Hv>.

Together with (4), this proves the selective energy bound

    |<v,bu>|^2 <= M <u,au><v,Hv>,
    M <= smax a0^2/2.                              (8)

It holds either separately in every frozen Z sector or after any mixture
of sectors. The large kernel containing all functions of (Y,Z) causes
no problem because bu is orthogonal to it. A global hidden mixing gap
is neither supplied nor needed.

By GAP_FREE_SELECTIVE_AVERAGING.md, if r=M/kappa<1,

    sup_t ||P exp(-tA)P-exp(-ta)||_(2->2)
       <= delta_mem=r/[2 sqrt(1-r)].                (9)

The bound is independent of visible volume, visible gap and elapsed
time. It remains valid for externally chosen kinetic contexts/modes
which preserve the same pi and satisfy the same uniform constants.
The actual controls are the native modes and the independently supplied
phase mobility; knowing equilibrium weights does not provide either.

## 4. An alternative supplier from genuine phase-reversal access

If an actual actuator can add pi to each phase separately, fair initial
pi kicks followed by independent Poisson pi kicks of rate gamma give
independent telegraph signs with gap 2gamma. Original phase values and
Z can be absorbed into frozen amplitudes beta_i=alpha_i cos(theta_i),
|beta_i|<=a0. The native mobilities become s_i(1+beta_i sigma_i), with
fair sigma_i. Equations (8)-(9) hold with

    r <= smax a0^2/(2gamma).                        (10)

This supplier need not equilibrate the original phases. It needs the
actual sign-reversal actuator and fresh sign randomization. A diffusion
interface alone does not supply pi kicks. The initial random keys and
subsequent bath history cannot also be retained in the conditioning
record while claiming fair independent signs given that record.

The complementary physical-mechanism role additionally investigates
deterministic mirror cycles. Such controls can be a stronger ordinary
route for a smaller invariant observable sector. See its actual saved
construction and review status; no dominance over that route is claimed.

## 5. A collective diffusive receiver

Consider N sites on a ring, Mpart particles with 0<Mpart<N, and uniform
pi on that conserved occupancy sector. On each bond, E_i refreshes the
arrangement 10/01 fairly. Use (6) with one homogeneous mean s>0 and
arbitrary amplitudes alpha_i(Y_outside_i,Z), bounded by a0. Each amplitude
is unchanged by its own bond refresh. The averaged generator

    a=s sum_i(I-E_i)                                (11)

is symmetric simple exclusion with swap rate s/2. This reference is
known; exclusion and its diffusive scaling are not inventions here.

The actual generator need not preserve linear density observables.
For example an amplitude proportional to (2Y_j-1), at a site j outside
the updated bond, multiplies that bond's linear density difference by
an extra occupation variable. The reference remains exactly (11)
because the independent phase average cancels this modulation. Thus
the receiver does not rely on a closed one-particle equation for the
actual dynamics. Configuration-independent amplitudes form a simpler
subfamily in which the ordinary mirror controller has a stronger
bounded-sector result; see the complementary construction.

For q=2pi m/N, m not zero modulo N, put
F_q(Y)=sum_j Y_j exp(iqj), normalized to L2(pi) norm one. Directly
applying the bond refreshes gives

    a F_q=s(1-cos q) F_q.                           (12)

The actual phase-modulated system therefore satisfies

    |E_mu[conj(F_q(Y_0)) F_q(Y_t)]
       -exp[-s(1-cos q)t]| <= delta_mem             (13)

at every deterministic time, for every N and every allowed frozen Z.
This is an equilibrium density-mode response guarantee. Preparation of
that equilibrium, or a bounded-density perturbation used in its place,
is an explicit separate input.

On the diffusive clock t=N^2 tau with fixed nonzero integer m,
the reference tends to exp(-2pi^2 s m^2 tau). The reference convergence
is uniform in tau>=0: for positive rates c,d,

    sup_tau |exp(-c tau)-exp(-d tau)|
       <= |c-d|/[e min(c,d)],                       (14)

by the mean value theorem. Here their relative difference is O(N^-2).
Consequently any sequence of actual bath strengths kappa_N tending to
infinity, however slowly, makes the error in (13) vanish on the whole
diffusive clock. It does not have to grow like the inverse visible gap
N^2. This statement concerns the specified density-mode correlations;
it is not a full hydrodynamic process theorem or a fixed-kappa claim
about every possible quenched environment.

Even at fixed desired accuracy, one finite local kappa works for all N
and t. Total actuator number, power and calibration still scale with
the physical array. This is not a cost-free thermodynamic limit.

## 6. Broader kinetic design, if an additional multiplier is supplied

For arbitrary interacting pi, (9) covers the full visible L2 operator,
including context-dependent amplitudes in (6). It requires no
high-temperature uniqueness or rapid mixing of the visible dynamics.

Suppose an additional real actuator multiplies each native local clock
by a chosen c_i>=0 while preserving both directions and the bath.
Then the same construction has average rates c_i s_i and
M<=max_(i,context) c_i Var(lambda_i)/s_i. Calibration intervals for s_i permit
c_i to target desired visible mobilities with relative error. The
ordinary relative-form receiver adds delta_cal, uniformly in time and
volume. Hardware ranges and saturation must admit the selected c_i.

This is a conditional kinetic-design corollary, not a free consequence
of endpoint-call access. A finite-duration call inserted at Poisson
opportunities does not automatically implement an instantaneous
physical clock multiplier. The baseline result requires no such extra
multiplier and supplies controlled averaging/prediction of its actual
mean generator.

## 7. Failures which define the mechanism

**Absolute leakage can miss all long-time error.** For one fair visible
bit and frozen fair h=+/-1, let lambda=s(1+alpha h), 0<alpha<1. The
off-diagonal norm s alpha tends to zero as s tends to zero. At t=1/s,
the visible sign correlation is exp(-1)cosh(alpha), whereas the averaged
prediction is exp(-1). The discrepancy is fixed. A smaller absolute
defect is not an adequate long-relaxation-time information objective.

**One shared modulation coordinate destroys the volume-independent
full-operator guarantee.** For N independent fair visible bits, one
shared h modulates every update at rate s(1+alpha h). Their parity u
has a u=Ns u and ||bu||^2/<u,au>=Ns alpha^2. With any fixed-rate bath,
at t=1/(Ns) the probability of a bath change tends to zero; the same
nonzero exp(-1)[cosh(alpha)-1] discrepancy remains. Independent phases
or a supplied covariance bound are load-bearing. A particular smaller
observable sector may still admit a better controller.

**Frozen mean disorder is not removed.** If s_i also depends on Z, phase
agitation leaves that mean dependence. In the one-bit alpha=0 case,
no amount of phase diffusion changes the mixture E_Z exp[-s(Z)t].
Use a sector-specific calibrated target or an additional actual clock
multiplier; do not claim universal averaging of frozen mean disorder.

**A small equilibrium bias is different.** The entire argument shares
one exact pi. Small local errors in Gibbs ratios can move the equilibrium
substantially near a phase transition. The explicit boundary example
from record_geometry is preserved. Symmetric kinetic estimation avoids
that particular error; it does not make Gibbs-ratio acquisition free.

**Records remain physical.** Calibration generally leaves phases
correlated with its transcript. A fresh conditional phase preparation,
an independent deployment specimen or a separately proved joint bound
is required. Retaining the bath's random keys restores hidden
information; the old full-record counterexamples still apply.

## 8. Actual resources and precision

Supply: exact native heat-bath structure, local context/addressability,
known or warranted pi, actual independent phase diffusion or sign
reversal, a bound on modulation amplitude/rate, and the declared
initial conditional law. Increasing temperature is not automatically
an implementation of (7) at fixed pi. Native durations, sensor errors,
phase isolation, actuator errors, calibration and bath time must be
included. Local rate moments can be obtained without microscopic
sensing or initial visible equilibration under the stronger calibration
interface in FINITE_ACQUISITION_AND_RESPONSE.md.

This unit establishes a theorem and an explicit operation family.
Apparatus feasibility, favorable work cost and practical speedup remain
unestablished. Earlier preparation and complete-record results keep
their own interfaces; none is silently strengthened here.
