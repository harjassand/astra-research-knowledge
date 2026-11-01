# Nearly universal conductance does not provide mean deployment latency

Status: new root construction, independent review pending. This is a sharpened
scope obstruction using ordinary diffusion/potential theory, not a novelty claim.

For m>=3, beta=1, set u=||z||^2/2, v(y)=1+(1-y^2)^2 and F(y,z)=u v(y).
The basins are the original full fibers A={y<=-1/2}, B={y>=1/2}.
For every gamma>0 use the ACTUAL global reversible diffusion with mobility
diag(1,gamma I_m). Its invariant Gibbs law mu is independent of gamma. Define

  k_gamma=cap_mu,gamma(A,B)/mu(A),
  T_gamma=E_{mu(.|A)} tau_B.

The previously proved homogeneous parallel/free sandwich gives
0<k_parallel<=k_gamma<=k_free<infinity. Its scalar Jensen improvement satisfies
k_free/k_parallel<=Rplus/R0 ->1 as m->infinity. Thus for any epsilon>0 one can
choose ONE fixed sufficiently large m such that ALL positive gamma have rates
within one common multiplicative interval of width1+epsilon.

Nevertheless liminf_{gamma down to0} T_gamma=infinity. No finite factor or
finite upper bound on this mean latency follows from that common conductance
interval and the equilibrium law alone. T_gamma is allowed to be an extended
expectation; this note does not assert finiteness for every fixed gamma.

## 1. A frozen-fiber process used only to prove a limit

At gamma=0, z is constant and y is the one-dimensional nonexplosive diffusion
dy=-u v'(y)dt+sqrt(2)dW. For u>0 its mean hitting time of b=1/2 from y<b is

  t_u(y)=int_y^b exp(u v(s)) [int_{-infinity}^s exp(-u v(r))dr] ds.

This follows by integrating t''-u v't'=-1 with the no-exit entrance boundary at
minus infinity and absorbing right endpoint, or by finite-interval exhaustion. All integrals are
nonnegative, so exhaustion/Tonelli is legitimate even for extended means.

For u>=16 and y<=-3/4, restrict s to [-1/sqrt(u),1/sqrt(u)] and r to
[-1-1/sqrt(u),-1+1/sqrt(u)]. These intervals are ordered and inside the outer
integration range. On the s interval, v(s)>=2-2/u. On the r interval,
v(r)<=1+6/u, since r=-1+x and (1-r^2)^2=x^2(2-x)^2<=6/u.
Therefore

  t_u(y)>=4 exp(-8) exp(u)/u.

The initial Gibbs mass at fixed u in y<=-3/4 has the lower bound

  int_{-infinity}^{-3/4} exp(-u v(y))dy
       >=2 exp(-6) exp(-u)/sqrt(u),

using the same interval around -1 (its right endpoint is at most -3/4).
Radial Lebesgue measure is c_m u^(m/2-1)du. Consequently the unnormalized
mu(.|A) mean hitting time is bounded below by a positive constant times

  int_16^infinity u^(m/2-5/2) du = infinity   for m>=3.

The Gibbs normalizer and basin mass are finite: integrating z gives a constant
times v(y)^(-m/2), whose tails are proportional to |y|^(-2m).
Thus T_0=infinity is not caused by an invalid initial law or divergent mass.

## 2. Transfer to strictly positive actual transverse mobilities

Start every gamma process from the SAME mu(.|A) draw and use common Brownian
motions. The coefficients are smooth and converge locally uniformly to those
of the gamma0 process, including noise coefficient sqrt(gamma). The limit
process is nonexplosive for almost every initial draw (u>0 almost surely).
Standard stopped local Lipschitz/Gronwall estimates, followed by localization
on the limit's compact finite-time paths, give uniform-on-compact-time
convergence in probability to gamma0. This argument does not need a uniform
mixing time or a gamma-independent inverse-mobility Lyapunov constant.

For any fixed time horizon, an almost-sure uniformly convergent subsequence
preserves survival whenever the limit remains strictly below b throughout that
compact time interval. Hence Fatou, first for survival and then integrated
over finite times, gives

  liminf_{gamma down to0} E(tau_B^gamma wedge H)
     >= E(tau_B^0 wedge H).

One can justify this for the full liminf by selecting a sequence realizing it
and then the almost-sure convergent subsequence. Let H tend to infinity and use
the previous divergent expectation. Every member gamma>0 remains a finite SPD
mobility in the actual previously received global family; gamma0 is only a
proof device, not a claimed admitted implementation.

## 3. What this does and does not establish

The same known energy and Gibbs law can have a tightly confined equilibrium
conductance but arbitrarily large Gibbs-conditioned mean time to the other
basin. This is a mean-tail statement, not a claim that median or every finite
quantile diverges. Indeed those are different tasks and require separate proof.
It does not invalidate any earlier capacity certificate, which explicitly did
not promise arbitrary-start passage times. It shows why a useful latency
consumer needs an additional kinetic/initialization ingredient, rather than
renaming conductance as a transition rate for every deployment.

Strong ordinary prior: Bovier, Eckhoff, Gayrard and Klein, JEMS6(2004),
doi10.4171/JEMS/14, Section2, equations2.24--2.28, relates mean hitting times
to Green functions and equilibrium-measure-weighted starting laws; subsequent
regularity estimates matter when converting this to point-start means.
Those identities already warn against an arbitrary starting-law substitution.
Their global coercivity/nondegenerate-minima hypotheses are not imported into
this flat-valley example. The one-dimensional formula and limit are proved
directly above. Primary PDF inspected:
https://ems.press/content/serial-article-files/31525?nt=1
Article: https://ems.press/journals/jems/articles/172
