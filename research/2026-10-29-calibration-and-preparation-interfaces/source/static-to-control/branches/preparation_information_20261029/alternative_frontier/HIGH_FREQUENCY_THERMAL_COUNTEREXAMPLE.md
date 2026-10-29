# Bounded high-frequency forces defeat native equilibrium path stability

29 October 2026. Independent construction developed while reviewing the
root's parity projection. Root independently reached the same family before
receiving this derivation, and supplied the score/TV and Wasserstein extensions
reviewed below. This is ordinary mathematical research under a declared native
stochastic model, not acquired equipment evidence or a priority claim.

## 1. The stronger claim tested

Can the root's low-entropy reversible Markov surrogate always be chosen inside
the original calibrated thermal class? The family below rules out a uniform
full-path KL guarantee of that kind, despite uniformly bounded force amplitude
and fixed positive thermalization of every odd degree of freedom.

Use unit masses, temperature T>0 and friction gamma>0. Positions (x,y) lie on
a flat torus with side 2 pi; momentum lies in R^2. Momentum is odd, position
even, and no odd external field is present. For an integer k>=1 and fixed A!=0:

    dx=p_x dt,
    dp_x=-gamma p_x dt+sqrt(2 gamma T) dW_x,
    dy=p_y dt,
    dp_y=A sin(kx) dt-gamma p_y dt+sqrt(2 gamma T) dW_y.     (1)

The Brownian drivers are independent. Force amplitude |A|, friction and
temperature do not depend on k. Spatial derivatives of the force grow with k.

## 2. Exact stationary construction

Take a two-sided stationary OU p_x with variance T and an independent uniform
phase x_0. Integrate p_x modulo 2 pi. Let Z_y be an independent stationary OU
with the same gamma,T, and define

    S_k(t)=A integral_0^infinity e^(-gamma u) sin(kx_{t-u})du,
    p_y(t)=Z_y(t)+S_k(t).                                 (2)

The integral converges absolutely and |S_k|<=|A|/gamma. Differentiation gives
dS_k/dt=A sin(kx_t)-gamma S_k, yielding (1). Take an independent uniform y_0
and integrate p_y modulo 2 pi.

The resulting process is stationary and its position marginal is exactly
uniform. The y phase remains uniform after conditioning on every base-path
shift. This constructs existence directly. The bounded-force kinetic
diffusion has the usual hypoelliptic regularity; the calculations below require
the stationary construction and the applicable Girsanov conditions.

## 3. Physical entropy tends to zero

Thermal entropy flow, with Boltzmann constant one, is

    sigma_k=(gamma/T)[E(p_x^2)+E(p_y^2)-2T]
           =gamma E(S_k^2)/T.                            (3)

Here p_x and Z_y have variance T, and Z_y is independent of S_k.
Stationarity of S_k^2 gives gamma E(S_k^2)=A E[S_k sin(kx)].

The integrated stationary OU increment has variance

    2T[t/gamma-(1-e^(-gamma t))/gamma^2].

Uniform phase therefore gives the correlation

    E[sin(kx_t)sin(kx_0)]
       =(1/2) exp{-k^2 T[t/gamma-(1-e^(-gamma t))/gamma^2]}.

Thus the entropy is exactly

    sigma_k=(A^2/(2T)) integral_0^infinity
       exp{-gamma t-k^2 T[t/gamma-(1-e^(-gamma t))/gamma^2]}dt. (4)

For 0<=t<=1/gamma, the bracket is at least t^2/3.
For t>=1/gamma, it is at least 1/(e gamma^2). Hence

    sigma_k <= (A^2/(2T))[
        sqrt(3 pi)/(2k sqrt(T))
        + e^(-1)/gamma * exp{-k^2 T/(e gamma^2)} ].         (5)

It tends to zero. Scaling t=s/(k sqrt(T)), with these bounds supplying
domination on the small-time part and an exponentially vanishing tail, gives

    sigma_k ~ A^2 sqrt(pi/2)/(2 T^(3/2) k).                (6)

The odd thermalization gap remains gamma throughout.

## 4. All equilibrium competitors in the same native class

An equilibrium with the same kinematics, bath, linear friction and a
momentum-independent force G(q) has zero irreversible momentum current.
Its density must be r(q) M_T(p). Stationarity then requires

    G(q)=T grad log r(q)=-grad V(q).

Thus smooth periodic potentials V exhaust equilibria in this source class:

    nu_V(q,p)=Z_V^(-1) exp[-V(q)/T] M_T(p).                (7)

This classification fixes physical parity and reservoir. It does not cover
velocity-dependent effective forces, changed bath couplings, odd external
fields or added hidden degrees of freedom.

## 5. Exact full-path KL optimum

Let F_k(q)=(0,A sin(kx)). The stationary forward Girsanov KL rate from (1)
to the native equilibrium with potential V is

    I_k(V)=(1/(4 gamma T)) E_uniform |F_k+grad V|^2.        (8)

The source positional marginal is uniform, div F_k=0, and the domain is
periodic. Integration by parts therefore makes F_k orthogonal to every
gradient, giving

    I_k(V)=A^2/(8 gamma T)
             +(1/(4 gamma T)) E_uniform |grad V|^2.        (9)

The free equilibrium V=constant, with law nu_0=uniform_q M_T(p), is the
exact minimizer. Initial-law KL also decomposes:

    D(rho_k||nu_V)=D(rho_k||nu_0)+D(nu_0||nu_V),           (10)

since both rho_k and nu_0 have uniform position marginals and nu_V/nu_0
depends only on position.

For every observation horizon h>0,

    D(P_k^{rho_k}[0,h] || P_V^{nu_V}[0,h])
      =D(P_k^{rho_k}[0,h] || P_0^{nu_0}[0,h])
         +D(P_0^{nu_0}[0,h] || P_V^{nu_V}[0,h]),          (11)

and exactly

    inf_V D(P_k^{rho_k}[0,h] || P_V^{nu_V}[0,h])
       =D(rho_k||nu_0)+h A^2/(8 gamma T)
       >=h A^2/(8 gamma T).                              (12)

This lower bound is independent of k, although sigma_k tends to zero.
No uniform same-native-class full-path KL bound can therefore tend to zero
solely with sigma_k, keeping gamma,T,A fixed.

## 6. The one-time density does approach free Gibbs

Conditional on the x-history and current p_x, p_y is Gaussian with variance
T and mean S_k. Convexity of KL under this latent mixture yields

    D(rho_k||nu_0)<=E(S_k^2)/(2T)=sigma_k/(2 gamma).        (13)

Thus the same free equilibrium is approached at a single time but not in
full-path KL. The surviving dynamical information lies in fast force increments.
The exact optimum in (12) tends to h A^2/(8 gamma T), not zero.

## 7. Review of root's full-path TV strengthening

Assume the native equilibrium alternatives additionally satisfy
|grad V|<=C, with C fixed. Define the Ito path score

    Z_k=integral_0^h F_k(q_t) dot (dp_t+gamma p_t dt).     (14)

For the source, E Z_k=h A^2/2. For each equilibrium,

    E Z_k=-h integral nu_V(q) F_k dot grad V dq=0,

using grad nu_V=-(nu_V/T)grad V, periodic integration by parts and div F_k=0.
This checks the mean claim independently.

Uniform second-moment bounds follow from Cauchy--Schwarz, Ito isometry and
(a+b)^2<=2a^2+2b^2:

    E_source Z_k^2 <= 2 A^4 h^2+4 gamma T A^2 h,
    E_eq Z_k^2     <= 2 A^2 C^2 h^2+4 gamma T A^2 h.       (15)

The source's actual noise expectation gives a somewhat smaller term; these
uniform bounds suffice. For any two laws P,Q and statistic Z,

    |E_P Z-E_Q Z|^2
       <=2 TV(P,Q)[E_P Z^2+E_Q Z^2],                     (16)

by Cauchy--Schwarz against p+q and
integral(p-q)^2/(p+q)<=integral|p-q|=2TV.

Equations (14)--(16) give a strictly positive lower TV bound, independent
of k, over all native equilibrium alternatives with this fixed force bound.
The restriction |grad V|<=C is needed for this particular uniform moment
argument; (12)'s KL lower bound has no such restriction.

The alternative root score Z'_k=integral F_k dot dp has source mean

    h A^2/2-gamma T sigma_k h

and equilibrium mean zero. This follows from E_source F_k dot p=T sigma_k
and equilibrium momentum centering. Its second moments are likewise
uniformly bounded under the displayed force bound and the thermal moment
identities. The first score gives the simpler nonvanishing mean exactly.

## 8. Review of root's path-Wasserstein contrast

Couple the source to free equilibrium by using identical x,p_x,Z_y,y_0,
with source p_y=Z_y+S_k and free p_y=Z_y. Then

    E integral_0^h |p_source-p_free|^2 dt
         =h T sigma_k/gamma,
    E sup_{0<=t<=h} d_torus(q_source(t),q_free(t))^2
         <=h^2 T sigma_k/gamma.                          (17)

The position inequality is the elementary bound
sup_t |integral_0^t S_k|^2<=h integral_0^h S_k^2.
Both reference marginals are genuinely stationary by the construction.

Therefore the laws converge in a path metric combining momentum L2 and
position uniform distance, even while their full-path KL stays bounded away
from zero and full-path TV stays separated from bounded-force equilibria.
Root's asserted Wasserstein contrast checks.

With ideal continuous position trajectories one can recover momenta by
differentiation, since kinetic positions are C1. This does not make derivative
or Ito-score acquisition stable under finite precision. The oscillatory
scores have growing sensitivity as k grows; (17) is consistent with their
persistent discrimination.

## 9. What this changes, and what remains open

The root's broader reversible projection is not contradicted: it generally
leaves the velocity-independent-force/Maxwell-friction class. This construction
shows why same-native-class approximation is a genuinely different obligation.

It also forces the target guarantee to retain observation topology. A stable
finite-resolution consequence can converge while ideal continuous-path
distinguishability does not. No laboratory acquisition advantage or required
sample complexity has been established here.

A next formulation can retain the broader reversible class, impose warranted
force regularity, or select an observation topology in which the forcing
averages away. This note does not determine the sharp additional premise.

