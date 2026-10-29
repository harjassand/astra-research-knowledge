# Every finite Wasserstein order: ordinary finite-window upgrade

29 October 2026. Independent physical-frontier construction.

This is an addition to, not a modification of, the independently reviewed
bounded-force closure proof. The preserved independent proof has SHA256

    964fed77c8f00b9679ace3638711b0b729886286e79019643b1d5aadb8858fc1

and the reviewed root `BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md`
version has SHA256

    c81bcb2e9c36e7eb2e61e63a20364e49b7183b70da6589fb3534f20f9d86e16d

No empirical data or extra preparation is used. All constants below come
from the already specified source amplitude, bath, dimension and finite
observation horizon.

## 1. Statement

Keep the source class of the root theorem: fixed connected flat torus,
unit masses, gamma,tau>0, smooth position-only force ||F||_infinity<=A,
all momenta directly thermalized, specified physical reversal, no odd
external fields, and stationary physical entropy production sigma(F).

On Omega_T=C([0,T],Torus x R^d), use the UNBOUNDED uniform metric

    d_infinity(omega,omega')
      =sup_(0<=t<=T) [d_Torus(q_t,q'_t)+|p_t-p'_t|].       (1)

Write W_p for its Wasserstein distance, 1<=p<infinity. Let E_A be the
stationary smooth Gibbs sources of the same torus, bath and masses whose
potential satisfies ||grad U||_infinity<=A.

**Finite-window all-orders theorem.** For every fixed T<infinity and every
finite p>=1,

    sup_(F smooth, ||F||<=A, sigma(F)<=s)
                       inf_(Q in E_A) W_p(P_F,Q) ->0
                       as s->0.                         (2)

The smooth Gibbs competitors in any sequence can be chosen by the root
bounded-Lipschitz approximation alone. The SAME choices then converge in
every fixed finite W_p; no separate force reconstruction is needed for
each p. This remains a qualitative result as a function of sigma.

The proof has two ingredients: uniform stationary and path-supremum
moments, and a transport interpolation inequality. It does not infer
unbounded hitting-time moments.

## 2. Stationary momentum moments without assuming them in advance

Let B=A/gamma. The mild momentum equation on a stationary realization is

    p_t=exp(-gamma t)p_0+D_t+G_t,
    D_t=int_0^t exp[-gamma(t-s)] F(q_s) ds,
    G_t=sqrt(2gamma tau) int_0^t exp[-gamma(t-s)] dW_s.     (3)

Pathwise |D_t|<=B. The Gaussian random vector G_t has covariance
tau(1-exp(-2gamma t)) I. Neither D_t nor G_t is assumed independent of p_0
for the following estimate.

For any r>0 and finite K, let psi_K(x)=min(x^r,K). Stationarity and (3)
give

    E psi_K(|p_0|)
      <= E psi_K(exp(-gamma t)|p_0|+B+|G_t|).             (4)

The random vector p_0 is finite almost surely, so its exponentially
contracted norm tends to zero in probability, without any initial moment
assumption. Also G_t converges in distribution to a centered Gaussian G
of covariance tau I. Slutsky's theorem, valid without independence of a
vanishing term, and bounded continuity of psi_K yield

    E psi_K(|p_0|)<=E psi_K(B+|G|).

Monotone convergence as K tends to infinity therefore proves the explicit
uniform moment estimate

    E |p_0|^r <= E(B+|G|)^r <infinity.                   (5)

For r>=1, Minkowski gives the useful norm form

    ||p_0||_Lr <= B+sqrt(tau) c_(d,r),
    c_(d,r)=(E|Z|^r)^(1/r), Z~N(0,I_d),
    E|Z|^r=2^(r/2) Gamma[(d+r)/2]/Gamma(d/2).             (6)

This applies uniformly to every stationary bounded-force source,
regardless of its entropy rate, force derivatives or stationary position
law. It also applies to every Gibbs competitor. No stationarity-to-moment
circularity occurs: (4) starts with bounded tests and derives integrability.

## 3. Uniform high moments of the complete finite-window path

Integration by parts against the deterministic exponential kernel gives

    int_0^t exp[-gamma(t-s)]dW_s
       =W_t-gamma int_0^t exp[-gamma(t-s)]W_s ds.

Consequently, on the entire interval [0,T],

    sup_t |p_t|
       <= |p_0|+B+2sqrt(2gamma tau) sup_t |W_t|.          (7)

For any r>1, |W_t| is a nonnegative submartingale. Doob's Lr inequality
and Brownian scaling give

    ||sup_(t<=T)|W_t|||_Lr
       <= [r/(r-1)] sqrt(T) c_(d,r).

Combining with (6)--(7),

    ||sup_(t<=T)|p_t|||_Lr
       <= 2B+sqrt(tau)c_(d,r)
              +2sqrt(2gamma tau T)[r/(r-1)]c_(d,r).      (8)

This simple upper bound need not be sharp in T. It is finite and uniform
over precisely the force class used by the closure theorem.

Fix a constant reference path omega_* with momentum zero and let
R(omega)=d_infinity(omega,omega_*). The torus diameter D is finite, and

    R(omega)<=D+sup_(t<=T)|p_t|.

Hence every stationary bounded-force source and every Gibbs competitor
satisfies

    E R^r <= M_(r,T),                                   (9)

where the completely explicit common bound is

    M_(r,T)=
      [D+2A/gamma+sqrt(tau)c_(d,r)
          +2sqrt(2gamma tau T)[r/(r-1)]c_(d,r)]^r,
      r>1.

The compact position space is used here only to bound its contribution
to the path distance. The momentum estimate supplies every required high
moment. For a different fixed normalization of the state metric the
corresponding fixed conversion factors enter this same bound.

## 4. Transport interpolation on this path space

Let d_0=min(1,d_infinity), the bounded metric used by the root theorem.
The path space is Polish under either metric. With the root convention
that the test function has both supremum norm and d_0-Lipschitz constant
at most one, Kantorovich--Rubinstein duality gives

    d_BL(P,Q)=W_1^(d_0)(P,Q).                            (10)

Indeed any d_0-Lipschitz-one function can be centered at omega_* to have
absolute value at most one, since the diameter of d_0 is at most one.
Thus the dual test classes agree after subtraction of a constant.

Suppose P and Q both obey (9). Choose r>p and a coupling whose expected
d_0 cost is at most delta, where delta can approach d_BL(P,Q) from above.
Put X=d_infinity(omega,omega') under that coupling. The triangle inequality
and convexity imply

    E X^r <=2^(r-1)[E R(omega)^r+E R(omega')^r]
            <=2^r M_(r,T)=:K_(r,T).                    (11)

On X<=1, X^p<=X=d_0 because p>=1. On X>1, Holder's inequality gives

    E[X^p 1_(X>1)]
       <=(E X^r)^(p/r) P(X>1)^(1-p/r)
       <=K_(r,T)^(p/r) delta^(1-p/r),

since P(X>1)<=E min(1,X)<=delta. Therefore

    W_p(P,Q)^p
       <=d_BL(P,Q)
          +K_(r,T)^(p/r) d_BL(P,Q)^(1-p/r).             (12)

This is an ordinary moment-and-coupling interpolation bound; no new
transport theorem is claimed. It exhibits precisely why bounded path
metrics can be upgraded here: the bath and force cap supply uniform tail
control for the unbounded momentum contribution.

For completeness, the sequential weak-convergence formulation is the
same fact. If P_j converges weakly to P and the r-th moments (9) are
uniformly bounded for some r>p, a Skorokhod coupling on the Polish path
space has omega_j tending to omega almost surely. The pair distances
have uniformly bounded r-th moments by (11); their p-th moment tails are
at most K_(r,T)/L^(r-p) beyond distance L. Bounded convergence on the
remaining event gives E d_infinity(omega_j,omega)^p tending to zero.
Taking the infimum over couplings proves W_p(P_j,P) tends to zero.
The limit also has the moment bound by lower semicontinuity.

## 5. Uniform Gibbs closure and a common competitor sequence

Let b(s) denote the supremum/infimum bounded-Lipschitz distance in the
root theorem. Its proved conclusion is b(s)->0. Both a physical source
P_F and every member of E_A obey (9), so (12), followed by the infimum
over smooth Gibbs Q and the supremum over sources, gives

    [sup_(sigma(F)<=s, ||F||<=A) inf_(Q in E_A) W_p(P_F,Q)]^p
       <=b(s)+K_(r,T)^(p/r) b(s)^(1-p/r),
       r>p.                                            (13)

This proves (2). Formula (13) is explicit as an interpolation of the
root qualitative modulus. It does NOT turn b(s) into a computable rate.

For a particular source sequence, choose Q_j in E_A with d_BL(P_Fj,Q_j)
tending to zero. For every fixed finite p, choose any r>p and apply (12).
Thus that same Q_j works for all finite orders p. Equivalently, along an
identified subsequence from the ordinary root proof, the physical paths
converge in every finite W_p to the limiting Lipschitz-potential Gibbs law;
its smooth potential mollifications converge in every such W_p as well.

## 6. Exactly which consequential predictions follow

Every finite-window path functional H with global Lipschitz constant L
satisfies

    |E_P H-E_Q H|<=L W_1(P,Q)<=L W_p(P,Q).               (14)

Its expectations exist because (9) supplies first moments. Examples
include accumulated displacement int_0^T p_t dt and sup_(t<=T)|p_t|,
with their appropriate Lipschitz constants in (1).

Polynomial moments are also controlled. More generally, suppose a fixed
family of functionals obeys, for some fixed m>=1 and L,

    |H(omega)-H(omega')|
       <= L d_infinity(omega,omega')
            [1+R(omega)^(m-1)+R(omega')^(m-1)].          (15)

Apply Cauchy--Schwarz to any coupling and then use (9) at an order greater
than 2(m-1). The expectation difference is bounded by W_2(P,Q) times a
finite constant depending only on that common sensitivity/growth bound
and the fixed source/window parameters. It tends to zero uniformly for
that family. This covers polynomial powers of path-supremum momentum and
finite-window integrated kinetic energy. Along any identified weakly
convergent subsequence, every fixed continuous functional of polynomial
growth has converging expectations as well, by truncation and the higher
moment bound.

The words "fixed" and "common sensitivity" matter. These conclusions
do not cover a sequence of ever finer force-dependent probes whose
Lipschitz constants diverge. They do not infer the full microscopic force
or eliminate the prior full-path TV counterexample. Passive sensors may
use these estimates under their declared finite gain/noise/time budgets;
feedback which changes the source is a separate interface.

## 7. No unbounded hitting-time mean is established

All metrics and moment estimates above concern a specified finite T.
They do not supply a uniform tail estimate for a first-passage time H:

    E H=int_0^infinity P(H>t)dt.

Passing to the limit in this integral requires additional uniform
integrability in the time variable, such as a justified target-specific
tail or regeneration estimate. High moments of sup_(t<=T)|p_t| for every
fixed T are not that estimate. Nor does convergence of every fixed-time
survival probability justify integration over an unbounded horizon.

Accordingly this upgrade establishes finite-window Lipschitz and
polynomial-moment consequences, and includes no theorem about unbounded
mean lifetimes. A separate argument may prove suitable hitting-time tails
for particular targets in this native source class; no counterexample to
such an additional native theorem is asserted here.
