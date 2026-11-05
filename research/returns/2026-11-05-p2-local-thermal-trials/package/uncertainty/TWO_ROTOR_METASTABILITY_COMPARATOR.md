# A structured separation between local preparation and global equilibration

## Scope

This companion proves an exponential lower bound on global Gibbs equilibration
for a concrete two-rotor source while the selected local thermal-intervention
theorem has a preparation bound independent of the barrier. It does **not**
prove an exponential advantage over the best local method. Direct momentum
reset, stronger thermostat access, within-well analysis, or other locally
informed procedures are separate and potentially faster comparators.

The source and its initial family are constructed below. Initial preparation
is a paid source resource: the deployment protocol is not being granted hidden
rotor access merely because a factory or a mathematical example uses it.

## 1. Physical source and invariant law

Let q,y be angles modulo 2 pi, with momenta p,r and masses M,m>0. Set

    U(q,y)=B sin^2(y)+g[1-cos(q-y)], B>0, g>0,
    H=p^2/(2M)+r^2/(2m)+U(q,y).                              (1)

Only p is thermostatted, at inverse temperature beta:

    dq=(p/M)dt,
    dp=-g sin(q-y)dt-gamma p dt+sqrt(2 gamma M/beta)dW,
    dy=(r/m)dt,
    dr=[-B sin(2y)+g sin(q-y)]dt.                            (2)

The Brownian noise is fresh and independent of the initial system and any
retained classical reference. All statements below use this Markov thermal
resource; an observer holding future thermal noise is not an allowed reference.

The Gibbs density pi proportional to exp(-beta H) is invariant: Hamiltonian
flow preserves phase volume and H, while the p Ornstein-Uhlenbeck part preserves
its Maxwell factor. No spectral-gap or ergodicity assertion is needed for the
lower bound. With theta=q-y, the position law factorizes, hence

    pi_y(dy)=exp[-b sin^2(y)]dy/Z_y, b=beta B,
    Z_y=2 pi exp(-b/2) I_0(b/2),                             (3)

and theta has density proportional to exp[-beta g(1-cos theta)]. Momenta are
independent Gaussians with variances M/beta and m/beta. The local force obeys

    |partial_q U|=|g sin(q-y)|<=g,                           (4)

uniformly in the barrier B. The hidden reaction |partial_y U| can be as large
as B+g. The stronger hidden force is part of the manufactured source, not a
free locally available actuator.

## 2. A reference-sensitive initial family with constant entropy

Let L=(-pi/2,pi/2) modulo 2 pi denote the well around zero. Since the barrier
potential is pi-periodic, pi_y(L)=1/2. Let R be a fair independent classical
sign. Draw the remaining variables from pi conditioned on y in L, and replace
p by p+a sigma R, where sigma=sqrt(M/beta), a>=0. This defines a full initial
joint density rho_0(S,R), with R retained outside the source.

Relative to pi(S) times the fair reference law, its density is

    f_R(S)=2 1_L(y) exp[a R p/sigma-a^2/2].                  (5)

Therefore

    D(rho_0 || pi x rho_R)=log(2)+a^2/2,                    (6)
    ||f||_2^2=2 exp(a^2).                                   (7)

Equation (6) includes information in the reference. Using only the source
marginal entropy would omit a real resource. The extra mean kinetic energy of
the shift is a^2/(2 beta). Neither (6) nor (7) grows with B.

The selected entropy/conditional-Gaussian-LSI theorem consequently gives, for
an independent uniform trigger on an interval of length T,

    TV[(tau,p,rest,R), Gamma_p x law(tau,rest,R)]
       <= sqrt[(log 2+a^2/2)/(4 gamma T)].                   (8)

Its finite meter, backaction, clock, assignment and computation errors must be
added according to that theorem. Formula (8) does not turn a finite point-grid
clock into an atomless uniform trigger, and it does not erase those hardware
costs. The exact atomless trigger and zero meter-error point here is the clean
structural comparison.

## 3. Exact stationary barrier-crossing flux

Under stationary pi, y is continuously differentiable with velocity r/m.
An outward crossing of L occurs at y=pi/2 with positive velocity or at
y=-pi/2 with negative velocity. The one-way stationary surface flux is

    lambda_B = 2 exp(-b)/(Z_y sqrt(2 pi beta m)).             (9)

Indeed, each boundary has position density exp(-b)/Z_y, independent Maxwell
velocity, and E[(r/m)_+]=1/sqrt(2 pi beta m). Summing the two oriented boundaries
proves (9). We need only the following endpoint-transfer inequality, so no
level-crossing multiplicity or tangency assertion is required. Let psi_delta
be a smooth approximation to 1_L with one monotone transition at each boundary.
Pathwise,

    [psi_delta(y_0)-psi_delta(y_t)]_+
      <= int_0^t [-psi_delta'(y_s) r_s/m]_+ ds.

Stationarity and the independent Gaussian velocity make the expectation of
the right side converge to lambda_B t. The left side converges to the indicator
of A_t={y_0 in L,y_t outside L}, apart from zero-probability boundary endpoints.
Thus P_pi(A_t)<=lambda_B t. This is an elementary smooth-flux proof of the
part of the usual crossing argument actually needed here.

Because the initial density change is at time zero only and future thermal
noise is unchanged, every path event A satisfies

    P_rho(A)=E_{pi x rho_R}[f_R(S_0) 1_A]
             <=sqrt[2 exp(a^2) P_pi(A)].                    (10)

Since the initial density is supported in L, (9)--(10) and the endpoint-transfer
inequality give

    P_rho(y_t outside L)<=sqrt[2 exp(a^2) lambda_B t].         (11)

Since rho_0 is supported in L,

    TV[rho_S(t),pi] >= rho_t(y in L)-1/2
       >=1/2-sqrt[2 exp(a^2)lambda_B t].                     (12)

In particular the source remains at total variation at least 1/4 from global
Gibbs equilibrium for every

    t <= t_B := 1/[32 exp(a^2)lambda_B]
       = Z_y sqrt(2 pi beta m) exp(b)/[64 exp(a^2)].          (13)

This proof does not assume an Arrhenius rate approximation, a Markov
two-well reduction, a known mixing rate or equilibration inside either well.
It is a direct stationary-flux and change-of-initial-law bound.

For b>=1, the elementary estimates sin u<=u and
sin u>=2u/pi on [0,pi/2] imply

    4 exp(-1)/sqrt(b) <= Z_y <= pi sqrt(pi)/sqrt(b).           (14)

Thus t_B is bounded below by a constant times exp(beta B)/sqrt(B), at fixed
beta,m,a. Its sharper asymptotic is

    t_B ~ pi sqrt(2m/B) exp(beta B)/[32 exp(a^2)].             (15)

The local entropy-based trigger scale in (8) has no B dependence. This shows
that global hidden equilibration is unnecessary for that local operation,
even in a concrete finite-dimensional, smoothly coupled thermal system.

## 4. What initial preparation costs

Equations (5)--(7) specify a source ensemble; they are not a procedure that the
deployment observer can produce from arbitrary unknown states using the p
thermostat alone. In particular, generating pi conditioned on one well by
unrestricted long-time simulation and postselection would not be a legitimate
free initialization in this comparison.

An exact mathematical sampling construction exists without barrier waiting:
sample y uniformly in L and accept with exp[-b sin^2 y]. Its success probability
is Z_y/(2 pi), so its expected number of proposals is 2 pi/Z_y=O(sqrt(b)). Sample
theta independently from its von Mises density by ordinary bounded rejection
(expected cost depends on beta g, fixed here), draw independent Maxwell momenta,
and apply the reference-dependent shift. This is an ordinary classical density
sampler. Converting it into physical loading requires a factory with access to
both rotor angles and momenta, thermal momentum sources, controls and calibrated
continuous loading noise. Those are extra factory resources, not resources
granted to the deployed local observer. The mathematical sampler alone is not
a physical state-preparation proof.

There is also a broader, easier family that avoids precision in the exact
conditional Gibbs density. For b>=1, suppose a factory supplies y with density
g_B supported on |y|<=1/sqrt(b) and ||g_B||_infinity<=C sqrt(b), for a fixed C.
Retain the same theta, momenta and reference-shift factors. Since sin^2 y<=1/b,

    ||rho_0/(pi x rho_R)||_2^2
      <= pi sqrt(pi) e C exp(a^2) =: K_2,                    (16)
    D(rho_0||pi x rho_R)<=log K_2.                           (17)

The inequalities use (14) and integral g_B=1. The same proofs give local error
sqrt[log K_2/(4 gamma T)] and

    TV[rho_S(t),pi]>=1/2-sqrt[K_2 lambda_B t].                (18)

Uniform loading on [-1/sqrt(b),1/sqrt(b)] has C=1/2. This family requires an
angular loading width of order B^(-1/2), with finite density control; the
barrier energy on that support is at most 1/beta. It does not require an
exponentially accurate angular position or an exponentially energetic initial
state. A command resolution proportional to a fixed fraction of this width
uses O(log B) bits. It still requires continuous, calibrated loading noise:
a finitely supported distribution has infinite relative entropy to Gibbs and
does not satisfy (17). The known density/entropy contract must be physically
certified or supplied, not inferred from a few local observations.

If a real factory is only known within initial total variation eta of the
ideal (5), Markov contraction subtracts eta from (12). That alone does not
bound relative entropy for (8). The local preparation theorem separately needs
its actual entropy contract, for example the finite-density class (16).

### Local metrology has a barrier-independent moment budget

The entropy variational inequality applied to p^2/(4 sigma^2) gives

    E p_t^2<=4 sigma^2[D_t+(log 2)/2].

Under the nominal waiting dynamics D_t<=D0. Thus E|p_t|, the local drift bound
g+gamma E|p_t|, and the local Brownian increment moments are independent of B.
For an interval of length h one may use, for example,

    E|p_{t+h}-p_t|
       <=[g+2 gamma sigma sqrt(D0+(log 2)/2)]h
           +sigma sqrt(4 gamma h/pi).

The finite local momentum-estimation budget in the main construction can
therefore have constants independent of the hidden barrier. Added meter
backaction must first update D_t by its actual action/entropy allowance.

Because q is an angle, a position-box implementation must use a locally
unwrapped encoder or equivalent two-quadrature record. An uncharged real-line
position oracle is not part of this rotor model. Over a finite meter window,
E[(integral |p_s|ds/M)^2]<=h^2 sup_s E p_s^2/M^2 bounds the probability of any
finite encoder range overflow by Markov's inequality. A declared finite range,
phase resolution and overflow failure allowance therefore suffice without B
dependence. Their sensor initialization, backaction and bit storage remain
part of the main metrology bill.

## 5. Fair comparator and reuse statements

The strongest ordinary local comparator must receive the same known law,
thermostat, metrology, private randomness, initial ensemble and actuator access.
It may analyze this concrete within-well system, estimate conditional local
readiness, or use exactly the same Gaussian log-Sobolev/entropy bound. It is
not required to wait for global Gibbs mixing. Thus (13) versus (8) proves a
separation of scientific resources, not an optimal-algorithm speedup.

A direct independent Maxwell momentum reset followed by a local tilted-law
sample realizes the desired local intervention without this random waiting,
if the interface permits momentum replacement while retaining the other
coordinates. A finite full momentum swap with a thermal ancilla is another
stronger supplied operation. The present comparison does not grant either
operation. If a factory's hidden-loading access remains available during use,
that stronger access must also be given to the comparator; it cannot be hidden
in initialization and then ignored selectively.

Every reuse that records information or applies treatment must update the
actual history-inclusive entropy/work budget. The retained hidden well remains
part of the source. A local successful intervention does not reset it, make
successive outcomes independent, or give free independent specimens.

## 6. Numerical illustration scope

The companion script evaluates exact formulas (3), (9), (13) in ordinary
floating arithmetic, using the scaled Bessel function to avoid cancellation.
It compares them with the clean theorem scale T=(log 2+a^2/2)/(4 gamma epsilon^2).
It does not simulate exponentially long paths, execute a physical clock or
meter, prove a mixing upper bound, or demonstrate an optimal local speedup.

The smooth-flux argument is derived here. Invariance, Gaussian entropy
identities, stationary-flux bounds and rejection sampling are established
mathematical ingredients, not claims of historical priority.

Primary comparison: Lee, Ramil and Seo, *Eyring--Kramers Law for the Underdamped
Langevin Process* (arXiv:2503.12610, revised February 2026), proves much sharper
low-temperature transition-time asymptotics for its underdamped setting. That
result is not automatically applicable to this partially thermostatted rotor
model. We use the direct bound above rather than importing an unmatched
Arrhenius approximation. Borovkov and Last, *On Rice's formula for stationary
multivariate piecewise smooth processes* (arXiv:1009.3885), is a primary example
of the broader stationary-crossing framework; its particular piecewise-smooth
process hypotheses are likewise not substituted for the smooth-flux proof.

* https://arxiv.org/abs/2503.12610
* https://arxiv.org/abs/1009.3885
