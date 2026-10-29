# Finite local acquisition of the hidden-mobility moments used by averaging

29 October 2026. Complementary supplier for root's new compressed relative-
energy construction. This file supplies actual chronological observations,
finite confidence and their physical premises. It does not infer a hidden
bath or its relaxation rate from the data.

## 1. A bounded endpoint primitive avoids generator inversion

At a binary visible site, hold the surrounding visible context fixed while
calibrating. Its intended conditional Gibbs probability p is known, with

    p_min <= p <= 1-p_min,    p_min>0.

Let K be the heat-bath kernel which refreshes the site to Bernoulli(p).
The actual endpoint call is promised to have the form

    T=I-g(H)(I-K),    0<=g(H)<=1.                      (1)

It leaves H and the context unchanged. The call's actual randomness is
fresh conditional on the current microscopic state. A separate actual
label-preserving bath acts on H, with stationary law nu. Switching to a
calibration pair turns that bath off; H stays fixed during both calls.
These are substantive operation-factorization and isolation premises.

An example is a fixed pulse of a heat-bath generator lambda(H)(K-I):
g=1-exp(-t lambda). An independent exponential-clock pulse gives
g=lambda/(alpha+lambda). The endpoint program uses the **actual bounded
g**; it does not claim to infer E lambda or Var(lambda) exactly by inverting
two moments of g. Fixed-kernel access avoids a hidden-rate cap, while the
duration, clock and execution costs of that actual call remain charged.

For a spatial array, a Poisson-call or randomized endpoint program with
site opportunity rate r_i has visible contribution
r_i g_i(H_i)(K_i-I). Its averaged generator uses r_i m_i(K_i-I), where
m_i=E_nu g_i. For independent hidden modulators and heat-bath projections,
the variance-to-mean quantity in root's energy bound is

    M=max_i r_i Var_nu(g_i)/m_i.                     (2)

If m_i=0 then g_i=0 nu-almost surely and that site's contribution is zero.
Always Var(g_i)/m_i<=1-m_i<=1 when m_i>0. A conservative uncalibrated
bound M<=max_i r_i therefore exists; acquisition can materially improve it.

## 2. Two successive observed flips give unbiased first and second moments

Record Y_0,Y_1,Y_2 from two chronological calls of T. Let

    F1=1_{Y_1 != Y_0},   F2=1_{Y_2 != Y_1},
    p_opposite(0)=p,     p_opposite(1)=1-p,
    Z1=F1/p_opposite(Y_0),
    Z2=F1 F2/[p(1-p)].                               (3)

For **every** initial visible value and hidden value,

    E[Z1 | H,Y_0]=g(H),
    E[Z2 | H,Y_0]=g(H)^2.                            (4)

The first identity is the actual one-call flip probability. Two flips
have probability g(H)^2 p(1-p), because the first flip puts the site in
the opposite visible state before the second call. This is one actual
path, not two independently imagined futures from a copied hidden state.

The bounded ranges are

    0<=Z1<=B1=1/p_min,
    0<=Z2<=B2=1/[p_min(1-p_min)].                     (5)

No initial visible equilibrium is required for (4). In particular,
calibrating the mobility need not first equilibrate a critical visible
many-body target. What must still be supplied is the hidden law nu, or
another explicitly declared hidden ensemble, and the factorization (1).

If the local mobility is context-independent, any fixed known context
can be used. Context dependence requires calibrating the appropriate
contexts and retaining the context-dependent form constants; a label
potential alone does not establish kinetic context-independence.

## 3. Independent local preparations: elementary finite confidence

Suppose n calibration pairs have independently prepared H~nu, with
native randomness as in (1). The initial Y may depend on all past data
and on its current H: (4) still removes that visible-state dependence.
For d declared mobility families, use a union bound over their two
moments. With probability at least 1-beta, simultaneously,

    |Z1_bar_i-m_i| <= u1=B1 sqrt[log(4d/beta)/(2n)],
    |Z2_bar_i-s_i| <= u2=B2 sqrt[log(4d/beta)/(2n)],    (6)

where s_i=E g_i^2. A conditional Hoeffding/martingale argument also
allows adaptive visible starts because the conditional means remain
fixed. This route still pays for each independent hidden preparation.

## 4. One persistent specimen with a known actual hidden bath

Independent hidden preparations are unnecessary if a stronger bath
interface is warranted. Assume the specimen starts with H_1~nu, and
between successive two-call pairs apply an actual bath-only interval b.
Let its transition R be reversible and satisfy

    ||R||_(L2_0(nu)->L2_0(nu)) <= rho<1.              (7)

For a reversible continuous-time bath with supplied gap gamma,
rho=exp(-b gamma). It may have unknown microscopic rates and an unknown
state count. Bath randomness must not depend on the visible readouts or
native call outcomes, and the native pair must leave H unchanged.

The hidden sequence is then a stationary Markov chain with kernel R.
For either score Z_a, put h_1(H)=g(H), h_2(H)=g(H)^2. For j<k,

    Cov(Z_a,j,Z_a,k)
       =<h_a-E h_a, R^(k-j)(h_a-E h_a)>_nu.           (8)

To prove this, condition the second score on H_k and its complete past,
use (4), then propagate the intervening bath transitions back to H_j.
The bath does not use the first score or its native noise. Conditioning
the first score on H_j gives h_a(H_j). The initial visible value and
all visible correlations therefore disappear from this covariance.

Since 0<=h_a<=1 and 0<=Z_a<=B_a,

    Var(Z_a_bar)
       <= [B_a^2+2 rho/(1-rho)]/(4n).                (9)

Indeed each diagonal variance is at most B_a^2/4, and the lag-l
covariance is at most rho^l/4 in absolute value. Sum the geometric tail.

For any chosen positive radii u1,u2, a complete elementary failure bound is

    beta_bound = sum_(i=1)^d sum_(a=1)^2
        [B_a,i^2+2 rho_i/(1-rho_i)]/(4n_i u_a,i^2).   (10)

Chebyshev and a union bound prove simultaneous coverage at least
1-beta_bound. This is deliberately conservative but finite and explicit.
Better Markov-chain concentration can improve the confidence dependence;
it is not required to establish the supplier. No unproved independence
of successive hidden states is used.

The cost per site is exactly 2n native calls, n-1 bath-only intervals,
and 2n+1 endpoint reads if the bath leaves the visible bit unchanged and
boundary reads can be reused. Context sensing, confinement, switching,
native durations, bath time (n-1)b, memory and arithmetic are additional
real costs. Parallel bath operation is available only if physically
warranted. The given gamma is not acquired by observing an invisible
bath in this experiment.

## 5. Turning simultaneous moment intervals into a valid design certificate

On a simultaneous confidence event define

    mL_i=max(0,Z1_bar_i-u1_i),
    sU_i=min(1,Z2_bar_i+u2_i),
    vU_i=max(0,sU_i-mL_i^2).

If a reported interval is inconsistent with [0,1], issue an
uninformative certificate rather than silently trusting it. A valid
upper bound is

    R_i = min(1-mL_i,vU_i/mL_i)   if mL_i>0,
          1                       if mL_i=0,
    M_U=max_i r_i R_i.                               (11)

Then M<=M_U. With root's independently warranted bath gap gamma and
actual speed kappa, its sufficient form parameter obeys

    eta^2 <= M_U/(kappa gamma).                       (12)

Choosing kappa from the confidence set is legitimate **for the operator
certificate** on the simultaneous event. To deploy from the projected
initial condition used by the averaging theorem, the joint initial-law
contract must still be met. Calibration ends with H correlated with its
retained record. An unconditioned stationary hidden marginal does not
make H conditionally nu after a data-selected design. Fresh conditional
hidden preparation, independent deployment, or another proved joint
bound is needed for such a full record guarantee.

The averaged rates m_i can also be fitted. If mL_i>0, a simultaneous
absolute radius u1_i gives a relative mean-rate error at most u1_i/mL_i
for the unmodified empirical estimate (or a clipped estimate within the
same confidence interval). The fitted average generator must retain
the exact Gibbs heat-bath ratios. Its remaining kinetic error can then
be charged with the ordinary relative-form receiver in
GAP_FREE_RELATIVE_KINETIC_RECEIVER.md. This second error is distinct from
the hidden-memory averaging error.

## 6. Only the predictive hidden directions need be fast: a qualified extension

For independent hidden generators H_i, define the centered mobility
xi_i=g_i-m_i and its Green-Kubo energy

    G_i=<xi_i,H_i^dagger xi_i>_nu
       =integral_0^infinity <xi_i,exp(-t H_i)xi_i>_nu dt. (13)

Finiteness requires xi_i to be orthogonal to invariant hidden directions
and the indicated spectral integral to converge. Other hidden modes can
remain frozen. For the total bath H=sum_i H_i and heat-bath projection
operators A_i=I-K_i, orthogonality gives

    <b u,H^dagger b u>
      =sum_i r_i^2 G_i ||A_i u||_pi^2
      <= [max_i r_i G_i/m_i] E_a(u).                 (14)

Since the full omitted block C dominates kappa H, its variational inverse
bound gives the relative off-diagonal form condition with

    eta^2 <= [max_i r_i G_i/m_i]/kappa.              (15)

This states precisely the narrower dynamical information needed; it is
not a finite-sample certificate without further input. The chronological
scores in (3), with a bath interval t between the two native score calls,
measure E[g(H_0)g(H_t)], hence the integrand in (13). Finite observations
at bounded bath lags cannot upper-bound the remaining integral over an
unknown slow tail. A supplied cyclic spectral gap, a justified tail
bound, or an exact closure result on the relevant hidden feature space
would be needed. The elementary supplied-gap bound G_i<=Var(g_i)/gamma
returns (12).

This distinction preserves the original scientific principle: irrelevant
microscopic memory need not reset. It also prevents a finite number of
small observed covariances from being used to certify that no rare,
slow, predictively relevant hidden mode exists.

## 7. Scope of this addition

The moment identities are a finite local supplier for the factorized
heat-bath-modulation class, stronger than general weighted reversible
operation access. They do not establish the factorization, the existence
of a label-preserving independent bath, its gap, or spatial replication
across uncalibrated heterogeneous devices. Their chief advantage is that
they require neither microscopic sensing nor visible Gibbs equilibration
for calibration itself. No favorable practical cost or apparatus result
has been demonstrated.

## 8. Retaining the native continuous-time rate, with a real bias budget

If the desired deployment really uses lambda(H)(K-I), rather than the
endpoint mobility g, suppose the physical interface supplies a rate bound
0<=lambda<=Lambda. Turn off the hidden bath and call an independent
exponential-clock pulse of rate alpha. The same flip scores measure
the first two moments of g=lambda/(alpha+lambda). If m_g=E g and
v_g=Var(g), then

    alpha m_g <= m_lambda <= (alpha+Lambda)m_g,
    Var(lambda) <= [(alpha+Lambda)^4/alpha^2] v_g.      (16)

The first inequality is pointwise. For the second, the inverse map
lambda=alpha g/(1-g) has Lipschitz constant
(alpha+Lambda)^2/alpha on the permitted interval. Apply
Var(f(G))=(1/2)E[(f(G)-f(G'))^2] with an independent *mathematical*
copy only to prove the inequality; no experimental copy is requested.

Thus the actual continuous-rate form quantity has the valid upper bound

    Var(lambda)/m_lambda
       <= [(alpha+Lambda)^4/alpha^3] v_g/m_g.          (17)

It may be intersected with the elementary bound Lambda-m_lambda.
With the confidence values in Section5, use mL in the denominator and
vU in the numerator; if mL=0 use the conservative bound Lambda.

The averaged rate itself lies in the confidence interval

    [L,U]=[alpha mL, (alpha+Lambda)mU],
    mU=min(1,Z1_bar+u1).

When L>0, the fitted rate 2LU/(L+U) minimizes the worst relative error
over that interval and has error at most (U-L)/(U+L). Taking alpha large
reduces the deterministic inverse bias but makes the observed g smaller
and can substantially increase the sampling needed for relative accuracy.
For alpha=Lambda, (17) is simply 16Lambda v_g/m_g.

Clock discretization/censoring, rate-bound validity, bath switching and
sensor errors need their own paid moment bias. They cannot be hidden in
the displayed finite-sample radii. This variant is a bounded-bias supplier
for the native continuous-rate theorem, not an exact extrapolation from
an acquired endpoint kernel to an unmeasured duration.
