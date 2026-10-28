# Direct acquisition of a passive memory module

Research branch, 28 October 2026. This is a conditional construction, not a
claim of a new general theory of system identification or a physical device.
The interpolation ingredients are classical. The actual proposed addition is
an acquired, dimension-independent finite-horizon input/output certificate
which can be attached to a positive finite atomic realization.

## Source and interface

Assume a resettable scalar LTI source with

\[
k(t)=\int_{(0,\Lambda]}\lambda e^{-\lambda t}\nu(d\lambda),\quad
\nu\ge0,\quad \nu((0,\Lambda])\le M,
\]

and step response S(t)=int(1-exp(-lambda*t))dnu. There may be infinitely many
relaxation modes, and no lower rate is supplied. A calibrated unit step can
be applied from known zero state. Point readings of S have absolute error
at most eta. This dynamic interface and source class are supplied, not
established by a finite fit or inherited from static P1.

The object to acquire is the causal convolution kernel in L1[0,T]. If
||k-khat||_1<=epsilon, then every bounded input, of arbitrary switching rate,
satisfies sup_[0,T]|k*u-khat*u|<=epsilon*||u||_infinity. This is the strong
finite-horizon reuse guarantee. The earlier idea of approximating S only
uniformly would instead incur |u(0)|+TV(u), which can be arbitrarily large.

## Dyadic Chebyshev derivative acquisition

Choose t0>0 and B dyadic blocks [a,b], b<=2a, covering [t0,T]. Read S at m+1
Chebyshev-Lobatto nodes per block, sharing endpoints: B*m+1 readings. Set
khat=0 below t0 and equal to the derivative of each interpolant thereafter.

The affine image of the Bernstein ellipse rho=4 lies in Re(t)>0: its
leftmost point is (a+b)/2-(b-a)*(4+1/4)/4 >=7a/16. On it |S(z)|<=2M.
Thus its Chebyshev coefficients obey |c_j|<=4M*4^(-j). For j>m, Chebyshev
interpolation aliases T_j to T_l with 0<=l<=m. Since ||T_j'||<=j^2,

\[
\int_a^b |S'(t)-(I_m S)'(t)|dt
\le16M\sum_{j>m}j^2 4^{-j}.                         \tag{1}
\]

Proof: each aliased derivative discrepancy is at most 2j^2 on [-1,1];
multiplying by 4M*4^(-j), summing, and integrating the x-coordinate interval
of length two gives (1). The change-of-variable scale cancels exactly.

For node errors |e_j|<=eta, the interpolating polynomial p obeys
||p||_infinity<=sqrt(2m)*eta. Discrete cosine orthogonality gives
c0^2+cm^2+(1/2)sum_(j=1)^(m-1)cj^2<=eta^2; weighted Cauchy-Schwarz proves
the bound. A degree-m polynomial has at most m monotone pieces, hence
TV(p)<=2m||p||_infinity. Therefore

\[
\boxed{\|k-\hat k\|_{L^1[0,T]}
\le M\Lambda t_0+B\left[16M A_m+2m\sqrt{2m}\,\eta\right]},
\qquad A_m=\sum_{j>m}j^2 4^{-j}.                  \tag{2}
\]

The sum has an elementary exact expression: with q=1/4, n=m+1,
A_m=q^n[n^2/(1-q)+2nq/(1-q)^2+q(1+q)/(1-q)^3].

Choose t0=epsilon/(3M*Lambda), m large enough that 16MB A_m<=epsilon/3,
and eta<=epsilon/[6B*m*sqrt(2m)]. The certificate is epsilon. Reading count
is O(log(M*Lambda*T/epsilon)*log(M*log(M*Lambda*T/epsilon)/epsilon)).
Required absolute precision is inverse-polynomial in the logarithmic factors
and epsilon; it is not acquired for free. The source must run until T.

## Why an interpolant alone is insufficient for interconnection

The derivative interpolant may violate positivity or positive-realness.
The certificate above controls open-loop convolution but does not by itself
make the approximate module physically passive. To obtain a passive module,
fit any nonnegative finite measure nuhat of total mass at most M on [0,Lambda]
to the same step observations. It yields khat(t)=sum w_j lambda_j exp(-lambda_j*t),
w_j>=0. Its transfer function is positive-real; a zero-rate atom contributes
zero output and can be dropped.

Suppose the model's largest sample residual against the measured data is r.
Then true/model sample discrepancies are at most eta+r. Apply the argument
to S-Shat, whose ellipse bound is 4M. On [0,t0], the two kernels have
combined mass at most 2M*Lambda*t0. Consequently

\[
\boxed{\|k-\hat k\|_1
\le2M\Lambda t_0+B\left[32M A_m+
2m\sqrt{2m}\,(\eta+r)\right]}.                    \tag{3}
\]

This is a computable acquisition certificate, given a validated residual r.
It does not depend on identifying true poles or on hidden mode count.
It is deliberately conservative; a numeric small residual is not itself a
rigorous bound until rounding/measurement/timing error is included.

Caratheodory gives a finite positive atomic exact match to N exact step
values and total mass, with at most N+1 atoms. That is an existence statement,
not a free extraction algorithm. A simple charged construction is an LP over
a finite positive rate grid, minimizing maximal sample residual, with mass
constraint sum w<=M. It has N+1 inequality pairs and as many nonnegative
weights as grid rates. Numerical LP proposals need validated residuals.

## A terminating finite-grid construction

Let z=log(lambda). In the L1[0,infinity) norm,
||d^2 k_(exp z)/dz^2||_1 <= int_0^infinity(1+3x+x^2)e^-x dx=6.
Piecewise linear interpolation of the kernel as a function of z, using
nonnegative barycentric weights on a log-grid of mesh h, therefore incurs
at most 3h^2/4 per unit spectral mass. Modes below lambda_min can be dropped
with finite-horizon error at most lambda_min*T per unit mass. Thus a grid
approximant exists with

\[
\|k-k_{grid}\|_1\le M\max\{\lambda_{min}T,3h^2/4\}. \tag{4}
\]

Its step samples differ by no more than the same bound. To obtain residual
r<=eta+zeta, choose lambda_min=zeta/(M*T), h<=sqrt(4zeta/(3M)), including
Lambda as a final grid endpoint. Grid size is
O(sqrt(M/zeta)*log(M*Lambda*T/zeta)), plus a dummy zero rate if desired.
Combining (3)-(4) gives a terminating dimension-independent LP construction
when the requested tolerance exceeds the instrument floor. Computation is
polynomial in 1/tolerance, not falsely claimed polylogarithmic.

## Full costs and limits

Acquisition is one prepared step trajectory of elapsed duration T, B*m+1
scalar readings, calibrated precision eta, and timing accuracy. A time error
q contributes at most M*Lambda*q to each reading; relative timing can use
|dS/dlog(t)|<=M/e. Reset, preparation, maintenance, actuation, and source
stability are additional. The physical time T cannot be replaced by the
logarithmic reading count.

The finite-grid fit costs a stated LP plus validated evaluation of exponentials.
After fitting K positive modes, evaluating a piecewise constant drive can be
done by K scalar state recurrences per time step. Other planning/feedback
tasks incur their own execution/optimization costs. (3) guarantees input/output
closeness for bounded exogenous drives; a closed-loop feedback guarantee
requires a separate propagation/stability argument. It does not automatically
bound passive network parameters, closed-loop energy, or infinite-horizon DC.

## Obstructions retained

1. Finite port rank does not bound temporal predictive rank. With distinct
   lambda_j>0 and a_j>0, the rank-one-port system A=diag(lambda_j),
   b_j=sqrt(a_j), has k(t)=b^T exp(-At)b. Its d-by-d sampled Hankel is
   V diag(a) V^T with Vandermonde V_ij=(exp(-lambda_j*Delta))^i, hence rank d.
2. Equilibrium laws do not determine kinetics. Positive mobility in
   xdot=-M*grad(E) changes relaxation while preserving equilibrium minima.
3. Even known-DC one-mode sources need time. k_a=a exp(-at) and
   k_(a/2)=(a/2)exp(-at/2) both have DC gain one. For any |u|<=U and t<=tau,
   their outputs differ by at most U*a*tau/2, because
   |d/dlambda[lambda exp(-lambda*s)]|<=1. If a<=4eta/(U*tau), midpoint
   measurements give one common adaptive bounded-error transcript. At
   t*=2log(2)/a, their unit-step responses differ by exactly 1/4. Any number
   of early reset trials cannot guarantee later error below 1/8. Greater
   amplitude, longer time, extra observables, or different noise assumptions
   change the contract.

## Relation to prior Astra work

Current GitHub revision read: 44b7e51f36b6dd4759a0227f23cc6b11671b1583.
N1068 provides matched native dynamic acquisition under separate dimension,
reset and linearity promises. N1069 supplies positive spectral families,
classical principal-measure extrema, task-specific duals, flat-moment stopping
and slow-mode obstructions. Its monotone positive digital feedback is not a
generic passive interconnection theorem. N1070 charges the full shaped-history
readout language and demonstrates why a slow-band bound is not a DC bound.

The new candidate differs in directly acquiring an entire finite-horizon
convolution operator in L1 with no spectral gap or finite dimension, from
logarithmically many step-time locations, and attaching that certificate to
a passive finite atomic LP fit. Its interpolation, positivity and convex
ingredients are established mathematics. Historical novelty is unestablished;
equally informed classical robust identification can adopt this construction.

Primary literature checked: Singh/James/Rudary, UAI 2004 (PSR),
https://arxiv.org/abs/1207.4167 ; Chen/Bai/Mei, ICLR 2023 (B-stable PSR),
https://openreview.net/forum?id=n05upKp02kQ ; Milanese/Vicino, J Complexity
1993, DOI 10.1006/jcom.1993.1028 (bounded-error nonparametric identification);
Hindi/Seong/Boyd, CDC 2002, https://www.web.stanford.edu/~boyd/papers/unc_fdd.html
(data-consistent robust uncertainty models); Lagoa et al., IFAC 2017,
https://pmc.ncbi.nlm.nih.gov/articles/PMC5846195/ (atomic-norm continuous-time
identification from nonuniform observations).
