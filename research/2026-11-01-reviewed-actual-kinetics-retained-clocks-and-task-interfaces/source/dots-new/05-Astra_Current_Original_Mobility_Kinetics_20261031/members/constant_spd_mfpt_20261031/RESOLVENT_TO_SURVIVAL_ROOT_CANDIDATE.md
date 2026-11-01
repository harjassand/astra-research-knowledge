# From current bounds to an all-time survival approximation, without a gap

Status: new root construction, independent review pending. Ordinary spectral,
variational and Cauchy--Schwarz machinery is used. No historical novelty claim.
This is separate from the frozen MFPT theorem/code and has no executable receipt.

## 1. A scalar spectral lemma

Let X>0 be a random variable with EX<=1 and E(1/X)<=1+epsilon, epsilon>=0.
Then for EVERY s>=0,

  exp(-s) <= E exp(-sX) <= exp(-s)+epsilon.                 (1)

Proof. Jensen gives the lower bound. Set
R_s(x)=exp(-sx)-exp(-s)+s exp(-s)(x-1). Convexity makes R_s>=0. Taylor's
integral remainder and sup_{s>=0} s^2 exp(-su)=4/(e^2 u^2) give

 R_s(x) <= (4/e^2)(x-1-log x),                       x>=1,
 R_s(x) <= (4/e^2)(-log x-1+x),                      0<x<=1.

For x>=1, log x>=1-1/x implies x-1-log x<=(x-1)^2/x.
For x<=1 the same logarithm inequality implies
-log x-1+x<=(x-1)^2/x. Therefore R_s(x)<=(4/e^2)(x-1)^2/x everywhere.
Furthermore 1-EX<=epsilon/(1+epsilon), by EX E(1/X)>=1, and
E[(X-1)^2/X]=EX+E(1/X)-2<=epsilon. Thus

 E exp(-sX)-exp(-s)
   <=epsilon/[e(1+epsilon)]+4epsilon/e^2 <=epsilon,

since 1/e+4/e^2<1. This proves (1). No spectral support gap, upper eigenvalue
bound, finite variance of X, or exponential moment of 1/X is assumed.

## 2. Abstract killed-process receiving theorem

Let P_t=exp(-tK) be the positivity-preserving self-adjoint killed semigroup of
an actually received reversible Markov process, killed on B. Work with any
finite invariant reference measure m; normalization is irrelevant. The surviving
domain D splits into A and S. Write M=m(A)>0, S0=m(S), rho=S0/M.
Let h be the actual equilibrium committor, h=1 on A, h=0 on B, 0<=h<=1, with
finite Dirichlet energy cap(A,B)=<h,Kh> (in the quadratic-form sense).
Suppose ordinary source-current/variational certificates earn

 cap(A,B)<=C0,
 Q_A=<1_A,K^(-1)1_A><=B_A,
 Q_S=<1_S,K^(-1)1_S><=rho^2 B_A.                       (2)

Inverse forms are the monotone zero-resolvent limits; their finiteness, actual
killed-process interpretation, and form-domain approximation must already be
proved, not supplied by a positive spectral-gap assumption. Define

 k0=C0/M,
 epsilon=C0 B_A (1+rho)^2/M^2 - 1.                    (3)

The hypotheses imply epsilon>=0. Then the survival probability from the EXACT
initial law m(.|A) obeys, for all t>=0,

 exp(-k0 t)-d_init <= P_{m(.|A)}(tau_B>t)
                    <=exp(-k0 t)+epsilon+d_init,     (4)
 d_init=rho+sqrt(rho(1+rho)),

with probabilities capped to[0,1]. In particular its uniform absolute CDF error
from this exponential law is at most epsilon+d_init.

Proof. Put N=<h,h>, so M<=N<=M+S0. Positivity of the resolvent and 0<=h<=1_D,
followed by the source Cauchy--Schwarz bound, give

 <h,K^(-1)h> <= <1_D,K^(-1)1_D>
              <=(sqrt(Q_A)+sqrt(Q_S))^2
              <=B_A(1+rho)^2.

The normalized spectral measure of h has X=lambda/k0, with
EX=cap/(Nk0)<=1 and E(1/X)=k0<h,K^(-1)h>/N<=1+epsilon.
Finiteness excludes mass at lambda=0, but the spectrum may accumulate there.
By (1), C_h(t)=<h,P_t h>/N lies between exp(-k0t) and exp(-k0t)+epsilon.

For the actual initial law, M times survival is <1_A,P_t1_D>. Put
e=h-1_A and d=1_D-h, both nonnegative, supported in S and at most1.
The exact difference from <h,P_th> is

  <1_A,P_t d> - <e,P_t h>.

Both terms are nonnegative. By L2 contraction their magnitudes are at most
sqrt(M S0) and sqrt(N S0), respectively. Thus the absolute difference is at
most sqrt(N S0), not a bound requiring a pointwise density ratio. After dividing
by M and accounting for N/M in[1,1+rho],
|survival-C_h(t)|<=rho+sqrt(rho(1+rho)). Combine with (1).

## 3. Application interface for the present MFPT constructions

For the fiber models divide the unnormalized Gibbs measure by the common
unknown transverse normalizer. This makes its y marginal q(y), with
M=int_A q and S0=int_S q. The scalar committor trial gives C0=1/(beta R),
R=int_slab 1/q, hence k0=1/(beta M R). The already constructed A-current gives
B_A. The same transport field with J_S instead of J_A gives (2), because
J_S(y)<=rho J_A(y) throughout the killed domain. This is a new use of the
Poisson source bound, not an identification of mean passage time with capacity.

If the existing finite receiving gives T_upper>=(1+rho)B_A/M and
T0_lower<=beta M R, then a safe spectral parameter is

 epsilon_upper=(1+rho_upper) T_upper/T0_lower - 1.

An explicit slab-mass upper bound and basin-mass lower bound give rho_upper.
Finite intervals for M,R must also enclose the exponential reference rate:
use exp(-t/T0_lower) in the lower survival envelope and exp(-t/T0_upper)
in the upper envelope, together with the proved additive errors. An arbitrary
midpoint is not an exact reference rate. Any numerical exp evaluation and
external time query still require their own outward arithmetic/cost receiving.

No assertion is made here that the existing code already computes or receives
this new output. Its full future-time statement follows only after all new
parameters/inequalities are independently bound to the actual input.

## 4. Limits that remain important

This is UNIFORM ABSOLUTE survival/CDF accuracy, not relative accuracy in the
extreme tail, exact exponential waiting times, an exponential moment bound,
or a promise that all quantiles have small relative error. Polynomial far tails
and zero killed spectral gap can coexist with (4). Probabilities far below
epsilon+d_init are not resolved by this certificate.

The initialization is the exact full m(.|A) law. Small TV preparation error does
not control an unbounded mean; (4) is not a hardware preparation certificate.
For bounded survival probabilities a separately earned TV input error can be
added, but that does not retroactively certify the MFPT. Time-homogeneous model
validity throughout the queried horizon, actual mobility/noise/calibration and
any physical control remain premises. No angular sampler, whole-space gap or
rare-crossing experiment is supplied or needed by the mathematical current
computation; none is thereby implemented physically.
