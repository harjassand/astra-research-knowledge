# Finite acquisition and an honest deployment response budget

29 October 2026. Root integration of the chronological supplier in
record_geometry/LOCAL_MOBILITY_MOMENT_ACQUISITION.md. Read that actual
proof for the endpoint identities and serial covariance argument. This
file connects its continuous-rate variant to selective averaging.

## 1. What is acquired, and what must be supplied

The response theorem uses the mean mobility m_i and a bound on
Var(lambda_i)/m_i. Two consecutive actual flips supply these moments
without microscopic sensing, copying, or initial visible equilibrium.
The factorized native generator, independent bath, its gap, rate ceiling
and access to each relevant local context remain separate warranted
properties. Finite data do not establish them or exclude an arbitrarily
rare unmeasured slow hidden mode.

## 2. Native-rate pulses and chronological scores

Supply a binary conditional heat bath K with known probability p,
p_min<=p<=1-p_min. Fix its surrounding context and turn off hidden motion
during two native calls. Under a supplied ceiling 0<=lambda(H)<=Lambda,
an actual independent exponential-clock pulse of rate alpha has kernel

    T=I-g(H)(I-K),        g=lambda/(alpha+lambda).    (1)

The real pulse has mean duration 1/alpha and no asserted hard time cap.
Clock approximation/censoring requires a separate bias budget. For one
chronological path Y0,Y1,Y2 set

    F1=1_(Y1!=Y0), F2=1_(Y2!=Y1),
    Z1=F1/p_opposite(Y0), Z2=F1 F2/[p(1-p)].         (2)

For every starting visible and hidden state,

    E[Z1|H,Y0]=g(H), E[Z2|H,Y0]=g(H)^2.             (3)

Two flips have probability g^2 p(1-p). No second future from a copied
hidden state is used. Score ranges are B1=1/p_min and
B2=1/[p_min(1-p_min)]. The hidden ensemble and fixed-context operation
are necessary even though the starting visible value is arbitrary.

## 3. Persistent-specimen confidence and costs

For each of d declared site/context families start H in stationary nu
and separate n pairs by bath-only intervals b. Suppose the actual
spacing kernel has centered L2 norm rho<1. Pairs leave H unchanged;
bath noise does not use their readouts. The supplier proof gives

    Var(mean Z_a) <= [B_a^2+2rho/(1-rho)]/(4n).       (4)

It uses the exact lag covariance of g or g^2 under that kernel, not
independence of consecutive hidden specimens. Chebyshev and a union
bound give simultaneous moment coverage with failure at most

    beta=sum_i sum_(a=1,2)
      [B_(a,i)^2+2rho_i/(1-rho_i)]/(4 n_i u_(a,i)^2). (5)

Independent actual preparations allow Hoeffding instead. For the phase
bath, conditional on any frozen Z, rho=exp(-kappa_cal b); for telegraph
signs rho=exp(-2gamma_cal b). Z need never reset.

The persistent route costs 2n pulses, n-1 bath intervals and 2n+1 reads
per site/context if unchanged boundary labels can be reused. Expected
pulse time is 2n/alpha and bath time is (n-1)b. Context isolation,
switching, sensing, timing errors, retained data and parallel hardware
are additional costs. Bounded local context structure avoids a full
many-body state table; heterogeneous devices still require calibration.

## 4. Continuous-rate confidence intervals

On the simultaneous event put

    gL=max(0,mean Z1-u1), gU=min(1,mean Z1+u1),
    qU=min(1,mean Z2+u2), vU=max(0,qU-gL^2).

Inconsistent intervals are uninformative. The exact inverse map
lambda=alpha g/(1-g) and its Lipschitz bound give

    m=E lambda in [L,U]=[alpha gL,(alpha+Lambda)gU],
    Var(lambda) <= [(alpha+Lambda)^4/alpha^2] vU.    (6)

For L>0 a valid upper bound on Var(lambda)/m is

    J_i=min(Lambda-L,
             [(alpha+Lambda)^4/alpha^3] vU/gL).      (7)

For L=0 use J_i=Lambda. The first term uses
Var(lambda)<=m(Lambda-m). Take J_U=max_i J_i. Actual independent phase
diffusion then supplies r<=J_U/kappa; a general supplied relevant bath
gap gamma replaces kappa by kappa gamma.

When L>0 choose the harmonic interval center

    mhat=2LU/(L+U), eps_i=(U-L)/(U+L).              (8)

For every m in [L,U], |mhat/m-1|<=eps_i. Multiplying exact local
heat-bath projections by these fitted mobilities preserves pi. With
eps=max_i eps_i<1, the established relative-form receiver adds

    delta_cal=eps/[2sqrt(1-eps)].                    (9)

The memory error r/[2sqrt(1-r)] is separate. Neither budget requires
accuracy proportional to the visible gap. Large alpha reduces inverse
bias but makes observed g smaller and relative estimation more costly.
Near-zero mean channels can also be costly. No favorable practical
sample or precision cost has been established.

## 5. Conditional deployment and retained records

Let D include retained calibration, selector, timing and apparatus data.
A stationary unconditional hidden marginal need not be stationary given
D. If an actual bath-only hold freezes Y, the circle heat kernel obeys

    TV(P_t(theta,.),uniform)<=sum_(n>=1)e^(-kappa n^2 t)
       <=2e^(-kappa t),       kappa t>=log 2.        (10)

For d_phase independent phases, product coupling gives total error at
most 2d_phase exp(-kappa t). Therefore

    t_warm=kappa^(-1)log(2d_phase/zeta)              (11)

supplies a joint zeta approximation to fresh uniform phases with the same
old (D,Y,Z). This uniform row bound survives arbitrary old correlations
and leaves Z untouched. The actual hold must turn off native visible
motion; a diffusion term leaving Y unchanged does not itself isolate Y
from its simultaneously running native generator. Fresh bath innovations
must lie outside the retained record. If its trajectory or keys are
retained, this is not the stronger joint-instrument guarantee.

Fresh fair physical pi kicks offer alternate sign initialization only
when their keys are outside the record. A retained controller bit is not
a hidden randomizer independent of controller memory. The earlier
full-record corrections remain in force. The warm-up can also supply
calibration's initial hidden law within TV zeta_init, added to confidence
failure by coupling. Neither operation prepares the visible Gibbs state.

## 6. Complete finite-confidence receiver

Assume the calibration event fails with probability at most beta and
selected designs enforce r<=r0<1, eps<=eps0<1 on that event. Given the
actual D and frozen Z, suppose the reference initial visible density
g_(D,Z) relative to pi has ||g_(D,Z)-1||_2<=K. Assume the actual initial
joint law is within zeta of this law times fresh stationary phases,
retaining the same (D,Z) marginal. The fitted visible reference uses
the data-selected rates and the same D,Z. At every deterministic time,

    TV(joint (D,Z,Y_t), fitted reference)
     <=min(1,zeta+beta+(K/2)*
           [r0/(2sqrt(1-r0))+eps0/(2sqrt(1-eps0))]). (12)

Apply the two operator bounds conditionally on the good event, integrate
the common D,Z marginal, and charge zeta by data processing and beta by
the failure-event probability. This is frequentist joint coverage, not
posterior success for every rare record. A data-selected external
schedule requires the same instantaneous hypotheses. Later adaptive
feedback is outside this assertion.

The phase warm-up supplies only the hidden part of the initial contract.
It supplies neither a fresh pi nor a useful K. Calibration permits any
starting visible value; an equilibrium-correlation deployment still
needs its warranted equilibrium or local-reweighting preparation. For
an initial readout, retain its actual conditional density or use the
finite-alphabet equilibrium two-time receiver in the main theorem.

## 7. Scope

Finite data select a bath strength and a mean model, not exact population
cancellation. Neither equilibrium weights nor finitely many small
covariances supply the bath energy inequality. The helper preserves the
Green-Kubo extension and its unbounded slow-tail failure. Physical
clocks and endpoint-call programs remain distinct: Poisson opportunities
for finite-duration calls do not alone realize an instantaneous
fixed-wall-time jump generator.

The broad theorem and this factorized acquisition supplier have
different premises. Earlier exact operation, weighted-adjoint,
preparation, retained-record and accepted thermal results keep their
original scope.
