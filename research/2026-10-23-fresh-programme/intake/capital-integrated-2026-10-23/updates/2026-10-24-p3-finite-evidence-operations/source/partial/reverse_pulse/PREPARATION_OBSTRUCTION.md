# Hidden preparation memory defeats visible short-stationarity checks

Private Astra P3 bounded applicability counterexample, 2026-10-23. No
benchmark or external scientific implementation is asserted. The source
below does not contradict the reverse-pulse theorem: it violates its full
stationary-preparation contract. Its pulse operator can nevertheless be
exactly reversible, irreducible, and a finite-rate CTMC propagator.

## 1. Exact six-state reversible discrete construction

Let h in {-1,+1} be a hidden preparation sign. For each h there are three
states F_+, F_-, M. The signs on F denote the visible sign relative to h.
The readout is

    f(h,F_+)=h,    f(h,F_-)=-h,    f(h,M)=h.

Within each h block, the unit-action transition is

    P_block =
      [[(1-d)(1+lambda)/2, (1-d)(1-lambda)/2, d],
       [(1-d)(1-lambda)/2, (1-d)(1+lambda)/2, d],
       [rho/2,             rho/2,             1-rho]],

with lambda=1/2, d>0, rho>0 and d+rho<1. The block equilibrium weights are

    pi_block=(rho/[2(d+rho)], rho/[2(d+rho)], d/[d+rho]).

Detailed balance holds: the fast transitions are symmetric and each edge
from F to M has equilibrium flow rho*d/[2(d+rho)] in either direction.
Give the two h blocks equal equilibrium weight and call the resulting
six-state equilibrium pi. Let Pi=1 pi^T. For gamma in (0,1), replace the
block-diagonal source by

    P_gamma=(1-gamma)P+gamma Pi.                                  (1)

This has strictly positive entries, is irreducible, and is exactly
self-adjoint on L2(pi). All its eigenvalues are nonnegative under the
parameter conditions above. It is a contraction in the correct equilibrium
Hilbert space.

### Preparation is the missing warrant

Prepare h uniformly and place the source at (h,F_+). Thus the visible
initial sign is f_0=h, and the hidden h stores it. Call this preparation mu.
It is not pi. The visible one-point marginal is nevertheless exactly uniform
at every later time, by the source's global sign-flip symmetry.

Starting from F_+, the probability of occupying M after n actions under P
is

    d/(d+rho) * [1-(1-d-rho)^n].

The signed difference between the two fast-state probabilities is
[(1-d)lambda]^n. A global Pi reset erases the correlation with the original
sign. Hence the exact endpoint correlation under the actual preparation is

    C_n^mu=E_mu[f_0 f_n]
      =(1-gamma)^n {
          d/(d+rho) [1-(1-d-rho)^n]
          +[(1-d)lambda]^n
       }.                                                        (2)

This is a decay followed by recovery of the initially stored sign.

### What the first two apparent moments say

Put r=1-gamma and lambda=1/2. Equation (2) gives

    H=C_1^mu=r(1+d)/2,
    J=C_2^mu=r^2[1/4+3d/2-3d^2/4-d rho],
    v_app=J-H^2=r^2 d(1-d-rho)>0.                                (3)

For sufficiently small d,rho,gamma these look like feasible positive
spectral moments of a stable binary observable with lambda approximately
one half and residual variance O(d). Naively treating them as equilibrium
Gram moments would give

    |C_n^mu-H^n| <= v_app/(1-H)^2=O(d)

uniformly in n. Formula (2) instead gives an order-one recovery at n of
order 1/d if rho and gamma are of order d^2. The executable rational
witness d=1/64, rho=gamma=d^2 verifies this failure without rounding.

The mistaken identification is precise. Two-pulse endpoint correlation
under mu is not the residual-norm Gram entry required by self-adjointness
on L2(pi). In fact, on the two states in the support of mu,
(P_gamma f)(x)=H f(x), so E_mu[(P_gamma f)^2]=H^2, while
E_mu[f P_gamma^2 f]=J>H^2. Moving the pulse between the two factors of an
inner product is justified for pi, not for this preparation.

## 2. Every bounded short visible history is close to the stationary model

Compare against the ordinary stationary binary Markov chain with one-step
correlation lambda=1/2. Couple its initial sign to h and its successive
fast flips to those of the six-state source. Before either a leakage F->M
or a global Pi reset, the complete observed boundary histories agree.

Thus for all histories through L actions,

    TV(Law_mu(f_0,...,f_L), Law_stationary_binary(f_0,...,f_L))
       <=1-[(1-d)(1-gamma)]^L
       <=L(d+gamma).                                             (4)

This controls every statistic of the retained short histories, not just
the first two correlations. One-point marginal checks pass exactly. The
conditional return rate rho is irrelevant to this coupling before the
first leakage event.

For any prescribed finite L and observational tolerance eta, d can be
chosen small enough that (4) is below eta. A protocol using independent
preparations and at most B total actions has transcript TV at most
B(d+gamma), even if its short experiments and stopping decisions are
adaptively chosen from earlier observations. Couple each fresh preparation
and continue until the first bad action. Any such fixed-budget test can be
made arbitrarily unable to distinguish the models, while (2) differs by
order one at a longer horizon.

This is an approximate finite-evidence obstruction. It does not assert
that the complete exact short distributions are identical: sufficiently
precise acquisition can detect their O(d) deviations. Nor does it turn
short visible stationarity into a quantitative bound on hidden preparation.

## 3. The failure persists with finite irreducible reversible kinetics

The same mechanism has an exact continuous-time realization, so lack of
CTMC embeddability is not responsible. In each h block use rates

    F_+ <-> F_- : k=log(2)/2,
    each F -> M : d,
    M -> each F : rho/2.

The block generator is

    Q_block=[[-k-d, k,     d],
             [k,    -k-d, d],
             [rho/2,rho/2,-rho]].

It is reversible with the same pi_block. Add gamma(Pi-I) to the full
block-diagonal generator Q. This adds strictly positive inter-state rates
and makes the six-state process irreducible while preserving detailed
balance. Q commutes with Pi, so its unit pulse and every repeated pulse
are exactly self-adjoint contractions on one common L2(pi).

Prepare mu as before. At real elapsed time t, the exact correlation is

    C_t^mu=e^(-gamma t) {
        d/(d+rho) [1-e^(-(d+rho)t)]
        +2^(-t)e^(-d t)
    }.                                                           (5)

The fast antisymmetric mode has rate log(2)+d. The mass exchange between
the combined F states and M has rate d+rho. Their two contributions give
(5); equilibrium mixing supplies the factor e^(-gamma t).

Before the first leak or global reset, the observed fast process is the
stationary binary CTMC with pulse correlation 1/2. The total-variation
bound for all pulse-boundary histories through L unit pulses is

    1-e^(-(d+gamma)L) <=L(d+gamma).                               (6)

Choose rho=gamma=d^2, 0<d<=1/64, and T=ceil(1/d). Then

    C_T^mu
      >= e^(-(d+d^2))/(1+d) * (1-e^(-1))
      >3/5.                                                      (7)

For an elementary constant check, the first factor is at least 4031/4160
and 1-e^(-1)>5/8; their product exceeds 3/5. The unperturbed stationary
binary model predicts 2^(-T), which tends to zero.

The apparent two-moment residual is also positive and O(d) in this finite
CTMC example. Write

    c=e^(-gamma),    l=e^(-(d+rho)),
    s=(1/2)e^(-d),  p=d/(d+rho).

Then

    H=c[p(1-l)+s],
    J=c^2[p(1-l^2)+s^2],
    J-H^2=c^2 p(1-l)[(1-p)+(1+p)l-2s].                           (8)

With rho=gamma=d^2 and d<=1/64 the bracket is positive. As d tends to
zero, H tends to 1/2 and J-H^2=O(d), so the naively imported uniform
radius tends to zero even though (7) holds at T. No source, operator or
readout is time-dependent; the sole invalid theorem premise is equilibrium
preparation.

## 4. Why this does not contradict the certificate

The genuine reverse-pulse theorem uses correlations under a common invariant
measure and the corresponding adjoint identities. Here the pulse operator
really has those properties for pi, but the experiment samples mu. The
full preparation discrepancy is large:

    TV(mu,pi)=1-rho/[2(d+rho)].                                   (9)

For rho=d^2 this tends to one, despite the small leakage and nearly
stationary visible short records. The counterexample therefore makes no
claim that a small full-state stationarity error causes an order-one
pointwise error.

An independently warranted TV(mu,pi)<=zeta would control every bounded
endpoint correlation discrepancy by at most 2zeta, uniformly in word length:
the conditional endpoint product is a function of the initial state in
[-1,1]. Such a warrant is useful evidence. For a reverse-pulse certificate,
the same systematic allowance must also enter the acquired Gram moments.
Visible short-history agreement alone does not provide that full-state
warrant.

This failure concerns applicability recognition, not the algebra of the
certificate. An equally informed retaining method that admits preparation
memory must retain this uncertainty. Reusing a valid operation requires the
preparation and adjoint contracts to remain warranted; passing finite short
visible stationarity checks is insufficient for an unqualified all-horizon
claim.

## 5. Addendum: finite visible checks and independent-copy centering

### Independent copies center the observable, not the preparation

Apply the proposed construction to two independent copies of this same
six-state source, both prepared from mu, and define

    F_t=(f_t-f'_t)/2.

For any identically prepared independent copies, writing
m_t=E_mu[f_t], independence gives exactly

    E[F_t]=0,
    E[F_0 F_n]=(C_n^mu-m_0 m_n)/2.                              (10)

Thus centering is valid even when the original mean varies with time;
stationarity of the resulting covariance does not follow. In the present
witness m_t=0 at every time already. Consequently every centered-copy
endpoint correlation is precisely half the existing correlation, and

    G_F=E[F_0^2]=1/2,    H_F=H/2,    J_F=J/2.

The scalar coefficient obtained by the naive Gram calculation is still
T_F=H_F/G_F=H. Its apparent squared residual and uniform radius become

    R_F=J_F-2H H_F+H^2 G_F=v_app/2,
    E_F,infinity=v_app/[2(1-H)^2],

with forecast H^n/2. The true correlation is C_n^mu/2, so the previously
proved violation is halved on both sides and remains a violation. In the
continuous-time family, (7) gives E[F_0 F_T]>3/10, while the false forecast
and radius tend to zero as d tends to zero. These are algebraic consequences
of the preserved witness, not a new test case.

The invalid adjoint step is likewise explicit. Let A=P_gamma for the
discrete source. On the support of mu, Af=Hf. For the independent product
source, therefore,

    E_(mu x mu)[((A x A)F)^2]=H^2/2,
    E_(mu x mu)[F (A x A)^2 F]=J/2>H^2/2.                       (11)

The product pulse is self-adjoint in L2(pi x pi), but the acquired inner
product uses mu x mu. Independent copying does not supply its invariance
or justify moving the pulse between the two inner-product factors. Even
the complete one-time distribution of F is constant here: its probabilities
at -1, 0, +1 are 1/4, 1/2, 1/4.

### Finite-word visible stationarity is still an approximate obstruction

The TV distance between two product laws is at most the sum of their
individual TV distances, and applying the map (f,f')->F cannot increase
TV. Hence (4), or its continuous-time analogue (6), gives

    TV(Law_mu(F_0,...,F_L), Law_stationary_copied(F_0,...,F_L))
        <=2L(d+gamma).                                         (12)

For continuous-time pulses the coupling also gives the tighter upper bound
1-exp[-2(d+gamma)L]. Thus every statistic of any tested word or window
within these short histories is close to that of a stationary reference.
Two equal-length windows within the record differ in TV by at most
4L(d+gamma). For any finite tested horizon and positive tolerance, d can
make all these checks arbitrarily convincing while long covariance
recovery remains of order one.

This claim concerns finite evidence with nonzero tolerance. It does not
assert exact equality of all tested visible laws, or rule out detecting
their small deviations with sufficient precision. Visible centering and
short approximate stationarity do not by themselves warrant stationary
preparation in the full future-relevant state space.

### An independent preparation warrant is charged at two distinct stages

Suppose instead that TV(mu,pi)<=zeta is independently justified. For every
word w and |f|<=1, the endpoint product conditional on the initial state
lies in [-1,1], so

    |C_mu(w)-C_pi(w)|<=2zeta.                                   (13)

If an acquired raw endpoint moment has statistical error eta_w around
C_mu(w), its input interval for the stationary theorem must therefore have
radius eta_w+2zeta around the acquired estimate. These enlarged input
intervals must be propagated through the Gram matrices, residuals,
coefficient choices, and certificate calculation.

After a valid stationary target interval I_pi(w*) has been calculated,
prediction for a future experiment prepared from mu requires the separate
target conversion

    I_mu(w*)=I_pi(w*)+[-2zeta,2zeta].                            (14)

A single allowance of 2zeta does not pay for both stages. Nor is the total
effect generally just 4zeta: the acquisition uncertainty can be amplified
by the certificate calculation before the final target allowance is added.

For the independent-copy procedure, apply the same rule to the actual
product-preparation discrepancy zeta_copy=TV(mu x mu,pi x pi). If only
the single-copy bound is known, a coupling gives

    zeta_copy<=1-(1-zeta)^2=2zeta-zeta^2.

Use 2zeta_copy at acquisition and separately at the future product-source
target. Copying is not an exemption from either requirement.
