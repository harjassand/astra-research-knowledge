# Autonomous mean passage time from a conditional-transport Poisson current

Status: new construction candidate, not accepted. Earlier freezes are unchanged.
This is an actual hitting-time calculation for a specified engineered diffusion,
NOT a relabeling of capacity/mass. No physical actuation or empirical model
membership is acquired. All parameter/control/computation costs remain explicit.

## 1. Actual model and initialization

Let U:R^m->R be a positive homogeneous coercive polynomial of even degree p,
alpha=m/p>=1. Put v(y)=1+kappa(1-y^2)^2, kappa,beta>0 and b=1/2.
The actual full diffusion has potential F=v(y)U(z), unit longitudinal mobility,
zero cross mobility, and transverse mobility

    M(z)=gamma z z^T/(p^2 U(z))+T(z), gamma>0,

where T is a finite smooth positive semidefinite tangent diffusion, T grad U=0,
with the correct divergence drift. The received concrete raw program later uses
the positive-coefficient degree2/4 energy grammar and complete-pair tangent
matrix from the accepted kinetic lift. If its tangent weight is positive, this
M is SPD at every z!=0. Gamma is part of the ACTUAL model, not a numerical time
rescaling or a free operation. Large gamma can impose real control/stiffness costs.

The exact projected process is

    dY=-v'(Y)u dt+sqrt(2/beta)dW,
    du=gamma(alpha/beta-v(Y)u)dt+sqrt(2gamma u/beta)dB.       (1)

This is the prior accepted pointwise Ito closure with the radial terms multiplied
by gamma; tangent dynamics still annihilate every function of U. The global
Lyapunov W=1+y^2+(1+2kappa/gamma)u satisfies

    G W <= [2+(gamma+2kappa)alpha]/beta-gamma u,

because yv'>=-kappa and v>=1. Squared-Bessel time change still excludes u=0
when alpha>=1. Coercivity controls z on bounded u, so even large polynomial
tangent coefficients cannot cause finite-time explosion. The conservative
reversible law has projected density, up to one irrelevant global constant,

    rho(y,u)=q(y) pi_y(u),
    q(y)=v(y)^(-alpha),
    pi_y(u)=(beta v(y))^alpha u^(alpha-1) exp(-beta v(y)u)/Gamma(alpha).

No angular partition appears. Define A={y<=-b}, B={y>=b}, Omega={y<b},
S={-b<y<b}, M_A=int_A q, M_S=int_S q. The requested observable is

    T_A = E_{mu(.|A)} tau_B,

or equivalently the same observable expectation from ANY full-state initial law
whose (Y,U) pushforward equals rho restricted to A and normalized by M_A.
A fixed-ray lift of that pushforward does not sample the full angular Gibbs law;
it is enough only because of the separately proved exact all-start projection.
Scalar/Gamma sampling, energy evaluation, roots and physical preparation are
not silently supplied by this theorem or its numerical certificate.

## 2. Zero-resolvent quantities: the actual hitting-time join

Use the unnormalized inner product with density rho on Omega and the killed
Dirichlet form

    E(f,f)=beta^-1 int_Omega rho [f_y^2+gamma u f_u^2],

with zero trace at y=b and the inaccessible, no-killing u=0 boundary (entrance
in Feller classification). Let R_lambda
be the killed resolvent for lambda>0. Positivity and the Markov/Dynkin resolvent
identity give

    <1_A,R_lambda 1_Omega>
      = int_A rho E_x[int_0^tau_B exp(-lambda t)dt].        (2)

For nonnegative f let Q_f(lambda)=<f,R_lambda f>. Its ordinary Hilbert-space
variational formula is

    Q_f(lambda)=sup_h [2<f,h>-E(h,h)-lambda||h||^2].        (3)

As lambda decreases to zero these nonnegative quantities increase. No bounded
inverse at zero, spectral gap, finite mean, or L2 Poisson solution is assumed.
We first prove finite bounds on Q_A=lim Q_1A(lambda) and Q_S similarly. Positive
resolvent Cauchy--Schwarz gives

    0<=Q_AS(lambda)<=sqrt(Q_A(lambda)Q_S(lambda)).          (4)

Therefore their finite limits also bound the cross term. Monotone convergence
in (2), after adding A and S, earns the ACTUAL finite hitting mean

    M_A T_A = Q_A+Q_AS.                                  (5)

Thus the construction itself proves finiteness at this initialization; it does
not begin by assuming the desired mean exists. Absence of a global spectral gap
in the polynomial y tails is not concealed by a bounded-domain replacement.

The variational/source identities can be obtained first on compact cylinders
with killing and then by monotone exhaustion. Smooth compactly supported test
functions with zero target trace suffice for upper bounds. Extended finite-energy
scalar trials for lower bounds are approximated by truncation/cutoff; their
energy and source pairings converge by the integrability estimates below. This
avoids treating an unbounded quadratic-growth trial as an L2 vector when its
square need not be integrable at alpha near one.

## 3. Constructed source current, not an assumed committor or solver

For f(y) equal to 1_A or 1_S, put

    J_f(y)=int_{-infinity}^y q(s) f(s)ds,
    w(y,u)=-(v'(y)/v(y))u,
    j_f(y,u)=J_f(y) pi_y(u) (1,w(y,u)).

The exact Gamma scaling identity is

    partial_y pi_y + partial_u(w pi_y)=0.

Consequently div j_f=q pi_y f=rho f. The sign may be reversed for the source
integration-by-parts convention; it does not change the resistance. The u-flux
vanishes at u=0 and infinity since u*pi_y is proportional to u^alpha exp(-beta v u).
For every compact zero-target-trace test, integration by parts and weighted
Cauchy give <f,h>^2<=D_f E(h,h), where

    D_f=beta int_{-infinity}^b J_f(y)^2/q(y) [1+K(y)]dy,
    K(y)=alpha v'(y)^2/[beta gamma v(y)^3].                (6)

Here the transverse resistance is 1/(gamma u), and E_pi_y[u]=alpha/(beta v).
These factors matter: replacing gamma u by Euclidean mobility gives a different
model and invalidates the finite mean guarantee. Equations (3),(6) yield Q_f<=D_f.

Conversely restrict (3) to scalar trials h(y). The one-dimensional Poisson trial
has h'(y)=-beta J_f(y)/q(y) and h(b)=0. Its source pairing and Dirichlet energy
both equal

    L_f=beta int_{-infinity}^b J_f(y)^2/q(y)dy.             (7)

Hence Q_f>=L_f after finite-energy approximation. This is the ordinary scalar
variational restriction, not an identification of the actual process with an
averaged one-dimensional diffusion.

For y<-b, J_S=0; for -b<=y<b, J_A=M_A and 0<=J_S<=M_S. Therefore

    D_S <= (M_S/M_A)^2 D_A.

Combining (4)--(7) proves the full autonomous mean sandwich

    L_A/M_A <= T_A <= (1+M_S/M_A) D_A/M_A.                (8)

The unknown normalizer cancels between source energy and basin mass. Arbitrarily
slow/fast nonmixing tangent dynamics do not enter this result; the declared
radial mobility does. A fixed-fiber current with j_u=0 would instead recover the
frozen-energy divergence obstruction and does not supply this bound.

## 4. Infinite tails really are finite

On the left tail y=-x, x>=b, write M(x)=int_x^infinity v(t)^(-alpha)dt.
Then J_A(-x)=M(x). As x tends to infinity,

    M(x)=O(x^(1-4alpha)),
    M(x)^2/q(x)=O(x^(2-4alpha)),
    K(x)=O(x^-6).

Thus L_A,D_A are finite when alpha>3/4; the actual lifted process interface uses
alpha>=1. On the finite slab all coefficients and integrals are finite. Q_S is
then finite by the pointwise current comparison. These estimates justify the
zero-resolvent/hitting-time limit in Section2 without rare-path simulation.

## 5. Explicit scalar-only outer certificate, alpha>=4

The first consumer uses integer alpha>=4, b=1/2, and the following acquired
quantities (the theorem's exact sandwich (8) is more general):

    M=M_A=int_b^infinity v^-alpha,
    R=int_-b^b v^alpha,
    a=v(b)=1+9kappa/16,
    d=1/alpha, c=v(1+d),
    S0=(1-b)a^alpha+d*c^alpha,
    S1=(1+d-b)(4kappa)^2 a^(alpha-3),
    Wfar=1/[64kappa^2(alpha-1)^2 d].

Only M and R require numerical integration. All other quantities are exact
rational powers for the integer-alpha backend. The inner cumulative M(x) is not
silently assumed as an oracle; it is bounded analytically as follows.

For b<=x<=1+d, M(x)<=M, v(x)<=a, and |v'(x)|<=4kappa. Since d<=1/4,
((1+d)^2-1)^2<=81/256<9/16, justifying v<=a on that full interval.
Splitting at x=1 gives

    int_b^(1+d) M(x)^2 v(x)^alpha dx <= M^2 S0,
    int_b^(1+d) M(x)^2 v'(x)^2 v(x)^(alpha-3)dx <= M^2 S1.

For x>1 the profile v is convex with v'>0, so its tangent line bounds the entire
remaining tail:

    M(x) <= v(x)^(1-alpha)/[(alpha-1)v'(x)].

Also v'(x)=4kappa x(x+1)(x-1)>=8kappa(x-1). Since alpha>=4 and v>=1,

    int_(1+d)^infinity M(x)^2 v(x)^alpha dx <= Wfar,
    int_(1+d)^infinity M(x)^2 v'(x)^2 v(x)^(alpha-3)dx
      <= M/(alpha-1)^2.

These are full infinite-domain bounds, not a fixed numerical cutoff or an
assumed first-hitting-time asymptotic.

On the transition half slab set W(y)=v(y)^alpha. Then -W'>=0 and

    K(y)W(y)=[-v'(y)/(beta gamma v(y)^2)] [-W'(y)]
      <= [4kappa/(beta gamma a^2)] y[-W'(y)].

Integrate by parts: int_0^b y(-W')=int_0^b W-bW(b)<=int_0^b W. Evenness yields

    int_-b^b K W <= [4kappa/(beta gamma a^2)] R.

This estimate is ONLY for the slab. It is not applied to the left-basin tail.
Finally M_S<=2b a^-alpha=a^-alpha. Formula (8) therefore receives

    T_low = beta M R,
    T_high = (1+a^-alpha/M) * {
       beta M R [1+4kappa/(beta gamma a^2)]
       + beta M S0 + beta Wfar/M
       + (alpha/gamma) M S1 + alpha/[gamma(alpha-1)^2] } .  (9)

Every term has the correct time scaling; in particular the gamma terms are not
multiplied by an extra beta. There is no missing factor2: M is one basin mass,
R is the complete transition slab, and the left-basin contribution is counted
once. The lower endpoint discards a positive left-basin Poisson energy; no
claim that T equals reciprocal conductance is made.

For beta=kappa=1, the slab overhead is 1024/(625gamma). A finite declared radial
gain gamma=512 gives overhead0.0032. For sufficiently large alpha the explicitly
retained basin/source corrections are much smaller. Whether a particular finite
raw input meets a requested TOTAL ratio is decided by exact outward arithmetic;
a sufficient-bound miss returns UNKNOWN, not a physical accuracy floor.

## 6. Ordinary alternatives and acquisition burden

The proof uses ordinary killed-resolvent variational duality, Poisson current
bounds, conditional transport, Cauchy--Schwarz and scalar integration. The new
construction is the actual source current and its full initialization/tail join,
not those primitives. No historical priority or proprietary separation is claimed.
A conventional two-dimensional PDE solver, verified barrier-certificate program,
fast/slow averaging method or variational method gets the SAME raw model,
initialization, radial gain and all analytic certificates. A comparator augmented
with this very current is not an independent pre-existing result supplying it.

The Gaussian U=||z||^2/2 ordinary radial reduction already gives the same scalar
observable generator when its actual mobility is matched; it is a strong retained
special case. Bussi--Donadio--Parrinello's existing CIR thermostat and Lelièvre--
Santet--Stoltz's metric design remain the kinetic-lift priors recorded in the
accepted lift. Prajna--Jadbabaie--Pappas (2004), Stochastic Safety Verification Using Barrier
Certificates, is retained as a bibliographic comparator for polynomial stochastic
barriers/convex search, not a newly invented general mechanism. The author's
primary indexed excerpt supplied that abstract-level description; the exact PDF
URL below returned404 to the independent reviewer and is NOT independently
received full text. The direct current proof does not depend on that reference.
https://www.georgejpappas.org/wp-content/uploads/2024/04/CDC04-Barrier.pdf

The first raw receiver must read the complete exact homogeneous energy program,
its tangent program and the actual radial gain, verify coercivity/degree/origin
conditions, bind the Gibbs|A observable initial law, acquire M/R intervals with
all infinite tails and arithmetic costs, and recompute formula (9). It cannot
reuse a previous capacity certificate's label as proof of this mean. No physical
kinetic interface, control bandwidth or initialization apparatus is inferred
from having a symbolic tensor formula.
