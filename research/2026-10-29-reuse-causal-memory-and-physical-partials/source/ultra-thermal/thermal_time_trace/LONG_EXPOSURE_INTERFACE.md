# Supporting temporal interface handed to C

C owns the physical exposure/retention receiver, its budget and its
comparison. These are two supporting lemmas and a finite exact scalar
packet, not a second classification implementation. The source is the
same one-hidden-quartic M-matrix diffusion. All claims are mathematical
conditional on its stationary bath/detector/access contract.

## 1. Travel survival retains a distant covariance signal

C's exact covariance identity already gives, for stationary a>=Delta,

    D_pp(t):=C_0,pp(t)-C_a,pp(t)
         >=s_a (exp(-Kt)R)_pv/g,  s_a>=s_Delta>0.

For endpoint K=3I-A_path define the probability density

    f_L(t)=(exp(-Kt))_pv/g, t>=0.

It is nonnegative and integrates to1. Its survival function is exactly

    L(t)=(exp(-Kt)R)_pv/g.

The endpoint resolvent identity gives its Laplace transform

    E exp(-z Ltime)=D_N(3)/D_N(3+z)
                  =product_j lambda_j/(lambda_j+z).

Hence Ltime is distributed as a sum of N independent exponential
variables with the positive eigenvalue rates of K. This is the
ordinary birth-death/hypoexponential mechanism (Karlin–McGregor /
Keilson, with a primary modern proof by Fill). Here the equality is
also proved directly by finite determinants; no native hitting-time
oracle or hidden trajectory is measured.

Let mu=Tr K^-1, v=Tr K^-2. For an exposure average over duration delta,
the covariance difference is at least s_Delta times

    B_L(delta)=2/delta^2 int_0^delta (delta-t)L(t)dt
             =1-E[(1-Ltime/delta)_+^2].

Since positive-part squared is at most the corresponding square,

    B_L(delta)>=2mu/delta-(mu^2+v)/delta^2.             (1)

One closed scalar choice, **not a claimed optimal exposure**, is

    delta=3(mu^2+v)/(2mu),
    B_L(delta)>=8mu^2/[9(mu^2+v)].                     (2)

All these scalars follow from two derivatives of the continuant,
with no spectral root finding, matrix exponential, quadrature, or
thermal data. At N32 the exact packet gives delta22.12012148867 and
retention>=.853403911532. For K3, eigenvalues lie in(1,5), so mu=Theta(N),
v=O(N); (2) is a constant retention at exposureTheta(N).

## 2. A qualified small variance for LONG exposures

The old Jensen bound E(barY)^4<=3(theta R_pp)^2 does not shrink with
exposure and would miss this opportunity. The needed replacement
follows from the ordinary Brascamp–Lieb variance inequality and
Gaussian/Wiener Poincare, using the actual cooperative derivative.

Let J(t,s) be the derivative of the nonlinear flow with respect to its
state at s, along any sample path. It solves

    dJ/dt=-[K+3a X_v(t)^2 e_v e_v^T]J, J(s,s)=I.

Positivity of this cooperative fundamental matrix and Duhamel give

    0<=J(t,s)<=exp[-K(t-s)] ENTRYWISE.                  (3)

For F=delta^-1 int_0^delta X_p(t)dt, initial-coordinate derivatives
and Brownian Cameron derivatives are integrals of rows of J, and
are therefore entrywise nonnegative and bounded by their harmonic
values. Initially X(0) has pi_a, independently of future Brownian
increments. Its Hessian satisfies Hess(-log pi_a)>=K/theta, so
Brascamp–Lieb gives its variance Dirichlet form bounded by theta R.
Tensorize with the ordinary Gaussian Poincare inequality for the
Brownian path. For a smooth path functional G the combined form is

    Ecal(G)=theta grad_0(G)^T R grad_0(G)
                         +int_0^delta |D_s G|^2 ds,
    Var G<=E Ecal(G).

One obtains the same statement by Gaussian cylinder approximation
and closing the derivative form; no time-grid simulator is an input.
R is entrywise nonnegative. Thus (3) bounds Ecal(F) **pointwise** by
the harmonic value, which equals the actual harmonic exposure
variance V_delta. This is a bound on the variance Dirichlet form,
not a claim that the nonlinear exposure is Gaussian. Consequently

    E F=0, E F^2<=V_delta,
    Var(F^2)<=4 V_delta E F^2<=4 V_delta^2.             (4)

Adding independent centered Gaussian electronics eta with warranted
variance sigma_delta^2=Sdet/delta adds that variance to the Dirichlet
bound. For Z=F+eta and S_delta=V_delta+sigma_delta^2,

    Var(Z^2)<=4 S_delta^2.                             (5)

For two nonoverlapping exposures separated by r, the stationary
semigroup gap and endpoint conditioning give covariance of their
squared exposure means bounded in absolute value by
4 V_delta^2 exp(-kappa r). Independent electronics contribute no
cross-read term. At start spacing h=delta+1/kappa, the correlated
raw-score variance therefore satisfies

    Var[Q^-1 sum_j(Z_j^2-sigma_delta^2)]
      <=[4S_delta^2+8V_delta^2 exp(kappa delta)
                                  /(exp(kappa h)-1)]/Q
      <9 S_delta^2/Q.                                 (6)

This is the same useful constant9, with the SMALL exposure variance,
not the unblurred point variance. No IID snapshots are assumed.

The harmonic covariance is theta exp(-K|t|)R, hence

    V_delta<=min(theta R_pp, 2theta(K^-2)_pp/delta).     (7)

The first bound follows by averaging positive covariance bounded
by its value at0; the second follows by replacing the triangular
weight by delta and integrating to infinity. Exact harmonic
integration can tighten (7) and is equally available to an ordinary
source-aware procedure.

For the locked N32 source, (7) gives V_delta<=.015444797022244;
Sdet/delta=.000452077083081; S_delta<=.015896874105325 and
9S_delta^2<=.002274395456885. The exact fractions, recurrence counts,
and actual input specification are in `INTERFACE.json`. No scalar
Gibbs contrast was reacquired; C consumes its own qualified s_Delta.

C's existing zero-start synchronous burn-in and calibration/risk
allocation can use (1),(6) directly. The long-window implementation
still needs the warranted integration time, stationary bath, white
electronics PSD, calibrated gain/reference, and stability across the
long observation. Low-frequency drift/colored detector noise would
change the packet. Longer integration is not a free measurement.

With fixed theta,Delta,Sdet and fixed-gap K3, these lemmas admit the
sufficient scaling Q=O(g^-4/N^2), duration Qh=O(g^-4/N), before burn-in
and calibration cost, instead of the fixed-short-exposure sufficient
O(g^-4) duration. This is a polynomial refinement of a conservative
receiver, not an exponential-depth cure or an optimum over all
time-series statistics. A strongest ordinary Gaussian/nonlinear
likelihood receives the SAME covariance/retention information. C owns
the actual finite-budget comparison and any scientific acceptance.
