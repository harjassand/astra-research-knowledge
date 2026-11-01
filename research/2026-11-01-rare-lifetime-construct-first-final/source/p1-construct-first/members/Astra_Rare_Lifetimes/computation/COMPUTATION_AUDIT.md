# Independent mathematical construction and audit

1 November 2026 (Brisbane). Parent task: `/root`; complementary constructor:
`producer-workspace/computation_opening`. This is an internal derivation and finite check,
not an external novelty or physical validation claim.

The prior Astra sources were fetched only at Git revision
`51ce47ce39f976517d60e2f87bbe280b651f6056` of
`harjassand/astra-research-knowledge`. The entry file `00_START_HERE.txt` was
read first. The decisive prior failure is N1213, source
`research/2026-10-29-rare-means-and-finite-width/source/p1-final/HEAT_BATH_COARSE_TARGET_FAILURE.md`.
Its two-spin example has a normalized-indicator estimate whose ratio to the
true coarse-target mean tends to 10/9 despite a full gap at least 1/2.
The present work does not challenge its accepted point-target theorem.

## 1. Exact coarse-target boundary repair

Let Q be an irreducible finite continuous-time reversible generator, let pi
be its invariant probability, and let L=-Q. For a nonempty proper A, put
B=A^c, p=pi(A), b=1-p and

    M = E_{pi(.|B)} tau_A,       mu=b M.

Write G=L^# for the inverse on mean-zero functions and zero on constants.
Then

    mu = min { <g,Gg>_pi : supp(g) subset A, pi(g)=1 }.

Proof: let t=E_x tau_A, zero on A. L t=1 on B. Put g=1-Lt,
so g is supported on A, pi(g)=1, and g>=1 on A (because Q t>=0 there).
As pi(t)=mu, Gg=mu-t, which equals mu on A. Thus this g is stationary
for the strictly convex quadratic restricted to the affine constraint.
For every supported mean-zero perturbation v, <v,Gg>=0 and
<g+v,G(g+v)>=<g,Gg>=mu. Positivity of the minimizer follows from the
displayed g. Dividing by b gives M.

The normalized indicator g=1_A/p is merely a feasible point. Its Green
quadratic is an upper bound, not generally the correct mean. This identifies
the boundary/entrance redistribution that the pinned counterexample misses.
It does not make the minimizing function available computationally.

This repair is ordinary potential theory. Aldous--Fill Proposition 3.41
gives the dual exact stationary hitting-time variational formula.

## 2. A short randomized recrossing operation

Fix s>0 and an independent exponential clock E_s of rate s. Set

    u_s(x)=E_x exp(-s tau_A),       m_s=pi(u_s),
    S_s=s m_s,                     R_s=1/S_s-1/s.

Let the stationary outward flux and exit law be

    J=sum_{x in A,y in B} pi(x) q_xy,
    nu(y)=sum_{x in A} pi(x) q_xy / J.

Starting y~nu, simulate the original process until it hits A or E_s rings.
The Bernoulli success probability is

    q_s=P_nu(E_s<tau_A).

The exact identity, requiring stationarity but not reversibility, is

    S_s=s p+J q_s.

Proof: (L+s)u_s=0 on B and u_s=1 on A. Stationarity gives
sum_A pi(x) [(L+s)u_s](x)=s pi(u_s). The left side is
s p+sum_{x in A,y in B} pi(x)q_xy[1-u_s(y)]. The term
1-u_s(y) is P_y(E_s<tau_A).

Each simulation has expected duration at most 1/s. This is a finite
operation, with a measured Bernoulli probability; it does not assume a
committor function. It requires the exit distribution and a simulator.
Neither is free: they may be constructed after local model acquisition,
but an unknown black-box process with no boundary preparation does not
automatically supply them.

For reversible Q with gap >=g>0,

    R_s/b <= M <= (1+s/g) R_s/b.

The parent independently derived this using a screened Dirichlet principle.
An equivalent check is the operator inequality
g/(g+s) G <= G_s <= G on mean-zero functions, where
G_s=(L+s)^(-1)-Pi/s. Minimizing its compression over supported densities
of pi_A mean one gives the same result.

## 3. Independently checked nonreversible extension

The parent supplied this stronger construction; the steps below were
checked independently. Assume only that the symmetric-part Dirichlet
form has Poincare gap g:

    <f,Lf>_pi >= g ||f||_pi^2 whenever pi(f)=0.

No claim about a nonnormal generator's eigenvalue real parts substitutes
for this assumption. Define

    C_0=1/mu,
    h_0=1-t/mu,
    h_0^*=1-t^*/mu,
    h_s=(u_s-m_s)/(1-m_s),
    C_s=1/R_s=s m_s/(1-m_s).

Here t^* is the mean hitting-time function for Q^*, the stationary adjoint.
Its stationary mean is mu: this follows because the scalar killed inverse
<1_B,L_B^(-1)1_B>_pi equals its adjoint scalar. Every h has pi-mean zero
and equals one on A. On

    W={v : v|A=0, pi(v)=0},

the primal and adjoint weak equations hold. In particular

    <h_0,Lh_0> = <h_0^*,L^*h_0^*> = C_0,
    <h_s,(L+s)h_s> = C_s,
    C_s-C_0 = s <h_0^*,h_s>.

For the last equality replace h_s by h_0 in the L term using the adjoint
weak equation, and replace h_0^* by h_s in the (L+s) term using the primal
weak equation. The Poincare inequality now gives

    |C_s-C_0| <= s sqrt(C_0 C_s / [g(g+s)]).

For x=C_s/C_0, solving this quadratic inequality in sqrt(x) yields exactly

    g/(g+s) <= x <= (g+s)/g.

Therefore

    R_s/[b(1+s/g)] <= M <= (1+s/g) R_s/b.

The reversible lower bound R_s/b<=M cannot be retained generally. The
exact seven-state directed cycle check below supplies a counterexample.
The complete upper/lower interval is multiplicative and independent of
the target rarity once S_s is estimated relatively without cancellation.

The same argument works between screening rates 0<=s<t:

    C_t-C_s=(t-s)<h_s^*,h_t>,
    (g+s)/(g+t) <= C_t/C_s <= (g+t)/(g+s).

Equivalently, where differentiated,
|d log(C_s)/ds|<=1/(g+s). In the reversible case the derivative is
||h_s||^2/C_s>=0, explaining the stronger one-sided interval.

## 4. A useful sharp lower bound on the recrossing probability

Every mean-zero h with h|A=1 has ||h||_pi^2>=p/b. The screened potential
h_s consequently obeys C_s>= (g+s)p/b, even without reversibility.
Since S_s=s C_s/(s+C_s),

    J q_s = S_s-s p >= s g p b/(g p+s).

Thus

    q_s >= s g p b/[J(g p+s)].

If the total outward jump rate is bounded by m on A, J<=mp. In the rare
regime p<=s/g this gives

    q_s >= g b/(2m).

The probability estimated in the short excursion is not exponentially
small in p. The bound is sharp for a two-state chain. This improves the
earlier bound obtained by dropping the s contribution to the mean-zero
energy, which unnecessarily had a factor g-s.

## 5. Source-error transfer without long-path total variation

### 5.1 Reversible weights and conductances

Use unnormalized invariant weights w and symmetric conductances
c_xy=w_x q_xy. The killed weighted Laplacian D_B gives exactly

    M=w_B^T D_B^(-1) w_B / W_B,       W_B=sum_B w.

If a w<=what<=b w and c_lo c<=chat<=c_hi c edgewise, then

    a^2/(b c_hi) <= Mhat/M <= b^2/(a c_lo).

The inverse killed Laplacian is entrywise nonnegative, so replacing the
two w factors costs a^2,b^2. Loewner conductance comparison bounds the
remaining quadratic by 1/c_hi,1/c_lo; the denominator costs b,a.
Uniform logweight error u and logconductance error v thus give factor
exp(3u+v), independent of the huge mean M. For a learned heat-bath law
whose transition rates have logerror r, v<=u+r gives exp(4u+r).

### 5.2 Nonreversible perturbations with common pi

Let Lhat share the same invariant pi and satisfy, for all real f,g,

    |<f,(Lhat-L)g>_pi| <= eps sqrt(E(f)E(g)),  eps<1,
    E(f)=<f,Lf>_pi.

For the normalized hitting potentials of the two chains,

    Chat-C=<h_0^*,(Lhat-L) hhat_0>.

Moreover E(h_0^*)=C and E(hhat_0)<=Chat/(1-eps). Hence
|Chat/C-1|<=eps sqrt[(Chat/C)/(1-eps)], giving

    1-eps <= Mhat/M <= 1/(1-eps).

This requires a bound on the perturbation form, not a sector bound on
the whole original dynamics. It also does not require a spectral gap.

### 5.3 Earning the form bound from short cycles

Suppose a balanced directed stationary flow is represented as a sum of
nonnegative directed cycle flows with coefficients a_c and cycle lengths
ell_c<=K. For one cycle,

    B_c(f,g)=sum_i f_i(g_i-g_(i+1)),
    E_c(f)=1/2 sum_i (f_i-f_(i+1))^2.

Subtract the mean of f on the cycle and use the ordinary cycle Poincare
inequality. This gives

    |B_c(f,g)| <= csc(pi/ell_c) sqrt(E_c(f)E_c(g))
                 <= (ell_c/2) sqrt(E_c(f)E_c(g)).

Relative coefficient errors |ahat_c-a_c|<=eta a_c therefore give the
required form bound with eps=eta K/2, by Cauchy--Schwarz over cycles.
The cycle representation, positive coefficient bounds and actual
coefficient acquisition remain necessary input/construction obligations.

### 5.4 Unknown stationary weights in the directed case

For any balanced directed flow F_xy=w_x q_xy the killed directed
Laplacian D_B is an M-matrix, so D_B^(-1)>=0 entrywise and the same exact
formula M=w_B^T D_B^(-1)w_B/W_B holds. Holding F fixed, a w<=what<=b w
gives a^2/b<=Mhat/M<=b^2/a. Apply the common-pi flow perturbation bound
separately at the original weights. Consequently logweight error u and
flow-form error eps yield

    exp(-3u)(1-eps) <= Mhat/M <= exp(3u)/(1-eps).

This separation lets a learned finite local cycle model retain useful
relative rare-mean guarantees without paying an error proportional to M.

## 6. Executed exact checks and a useful failure

`verify_capacity_stdlib.py` ran successfully using rational arithmetic.
`capacity_checks.json` contains 48 finite checks: 20 reversible complete
graphs, 20 nonreversible graphs obtained by adding a positive directed
circulation, six two-spin heat-bath instances down to epsilon=2^-128,
one sharp two-state instance and one directed-cycle instance. Complete
graph gaps are certified by explicit conductance domination; the directed
cycle uses a safe rational lower gap 1/n^2. No floating eigenvalue is a
premise. The exact primal-adjoint identity is checked in every case.

For the directed seven-cycle of unit forward rate, A={0}, s=1/100:

    p=1/7,       M=7/2,
    R_s/b=25329015075700/7213535210701,
    R_s/(bM)=7236861450200/7213535210701 >1.

The old reversible lower estimate exceeds the true mean by about 0.323%.
The nonreversible two-sided interval passes. A five-cycle trial did not
produce this counterexample; its first derivative at s=0 vanishes. This
was a useful check against assuming every directed cycle has the same
sign of screening error.

The checks support the formulas but establish neither historical novelty
nor fast model acquisition or actual experimental validity.

## 7. Numerical conditioning and a full-target fallback

The formula R_s=1/S_s-1/s is useful only if cancellation is controlled.
Let m bound the total transition rate at every state, so J<=m p. Then

    m_s=S_s/s <= p+J/s <= p(1+m/s).

Consequently p<=s/[2(s+m)] implies m_s<=1/2. In that rare-target
regime, a relative error zeta in S_s produces relative error at most
2 zeta/(1-zeta) in R_s. A relative-error estimate of q_s gives at most
the same relative error in S_s=sp+Jq_s. Taking s proportional to eps g
and zeta proportional to eps therefore gives the desired relative mean
accuracy. The previous lower bound yields, when p<=s/g,

    q_s >= g b/(2m).

Thus O(m/(g b eps^2) log(1/alpha)) independent Bernoulli recrossing
trials suffice, with mean duration at most 1/s per trial. A local-chain
simulator with at most m events per unit time then uses expected
O(m^2/(g^2 b eps^3) log(1/alpha)) events, apart from exit-law acquisition
and sampling costs. This is a deliberately simple sufficient bound,
not an optimal complexity claim. For rare targets with p<=1/2, b>=1/2.

For targets p>=s/[2(s+m)], direct simulation from pi(.|B) is already
polynomially controlled. For every f zero on A,

    Var_pi(f)>=p ||f||_pi^2,
    <f,L f>_pi>=gp ||f||_pi^2.

The killed semigroup therefore has L2 norm at most exp(-gp t), even
without reversibility. Cauchy--Schwarz from initial pi(.|B) gives

    P(tau_A>t)<=exp(-gp t),
    M<=1/(gp),
    E(tau_A^2)<=2/(gp)^2.

Moreover M>=1/m because reaching A requires at least the first state
departure, whose mean is at least 1/m. Independent direct samples thus
have relative second moment at most 2m^2/(g^2p^2). Median-of-means
estimation and an exponential-tail runtime cap yield a fully ordinary
polynomial fallback in this nonrare regime. For p<=1/2, sampling pi(.|B)
by rejection from an actually available pi sampler costs at most two
draws in expectation. Other target classes must earn conditional-start
sampling explicitly; it is not a free oracle.

This fallback preserves the intended rare-target advantage while making
clear that unexamined cancellation is not hidden in the screen estimator.

## 8. Full stationary lifetime law: audit of the parent's extension

The following is the parent's construction, independently checked here.
Retain the nonreversible symmetric-part gap g and put C0=1/mu,
delta=C0/g. Complex inner products conjugate their first argument.
For s=i omega, define u_s=E_x exp(-s tau_A), m_s=pi(u_s),
h_s=(u_s-m_s)/(1-m_s) and C_s=s m_s/(1-m_s). For omega nonzero,
the finite-chain hitting law from B has an absolutely continuous component
and |m_s|<1, so these expressions are well-defined. At omega=0 use the
continuous limit h_0,C0. The complexified affine weak equations imply

    C_s=<h_s,(L+s)h_s>_pi,
    C_s-C0=s<h_0^*,h_s>_pi,
    Re C_s >= g ||h_s||_pi^2.

To verify the first identity, use h_s-1, which vanishes on A, in the
pointwise equation (L+s)h_s=-C_s on B, together with pi(h_s)=0.
For the second, h_0^*-h_s is in the complexified W. Thus
<h_0^*,(L+s)h_s>=C_s, while the adjoint zero-screen weak equation gives
<h_0^*,Lh_s>=C0. No conjugation of C_s is introduced with this convention.
The energy of the real adjoint h_0^* is C0, so its squared norm is at
most C0/g. Consequently z=C_s/C0 obeys

    |z-1|^2 <= (omega/g)^2 Re z.

If |omega|/g<=1/2, this disk inequality implies

    |z-1|<=2|omega|/g,      Re z>=1/2.

Suppose delta<=1/4 and write x=omega/C0. For |x|<=1/(2delta),
the imaginary perturbation satisfies |Im z|<=2delta|x|<=|x|/2,
and hence |z+ix|>=sqrt(1+x^2)/2. Since m_s=z/(z+ix),

    |m_(i C0 x)-1/(1+ix)| <= 4delta x^2/(1+x^2).

Changing x to -x supplies the usual characteristic-function convention
for Y=tau_A/mu from stationary pi. Esseen's standard smoothing inequality,
with comparison density bounded by one, gives for T=1/(2delta)

    sup_y |P_pi(Y<=y)-(1-exp(-y))_+| <= D(delta),

    D(delta) = (4delta/pi) log(1+1/(4delta^2)) + 48delta/pi.

Here (1-exp(-y))_+ means the exponential CDF, zero for y<0.
The constants 1/pi in the Fourier integral and 24/(pi T) for smoothing
are stated in Flajolet--Sedgewick, Analytic Combinatorics, Theorem IX.5,
which cites Feller volume II, p538. The exponential CDF is Lipschitz with
bounded density one; its nondifferentiability at zero is harmless, either
by the bounded-density version or by smooth convolution and a limit.
An atom at zero in the law of Y is allowed by the smoothing inequality.

Since F_pi=p+b F_pi(.|B) on nonnegative times,

    sup_y |P_pi(.|B)(tau_A/mu<=y)-F_Exp1(y)| <= (D(delta)+p)/b.

If the desired exponential uses mean M instead of mu=bM, the exact
additional uniform CDF difference between those two exponentials is
p b^(b/p), bounded by p. The overall bound can always be capped at one.
This gives a uniform additive deadline-risk certificate; it does not
give relative accuracy for an arbitrarily tiny deadline probability.

The finite check `verify_lifetime.py` passed on eight reversible and
nonreversible generators, target mass 10^-2 through 10^-7, with 1120
complex-frequency checks and 1200 phase-type CDF grid checks. Each gap
lower bound is the explicit complete-refresh domination g=1. Results
are in `lifetime_checks.json`. These are floating-point checks, separate
from the exact rational mean checks and the analytic proof.

A useful numerical failure: the initial implementation obtained u_s and
mu by nearly singular killed-generator solves and then subtracted 1-m_s.
At p=10^-7 and x=10^-3, this produced a spurious imaginary capacity error
about 6.6e-7. Rewriting the solve directly for h_s,C_s with the affine
constraint pi(h_s)=0 removed the cancellation. The bordered system is

    [ L_B+sI   1 ] [ h_B ] = [ -L_BA 1 ],
    [ pi_B     0 ] [ C_s ]   [    -p    ].

This is ordinary stable recentering of the potential problem, not evidence
of a novel sparse high-dimensional solver.

The near-exponential phenomenon is established probability theory.
Mathieu (1997), section IV and Theorem 7, explicitly studies non-symmetric
processes, Laplace equilibrium potentials, spectral-gap inequalities and
exponential-law approximation. Reversible Aldous--Brown theory already
gives a stronger uniform error at most delta. The present independent
audit validates this particular sector-free nonreversible certificate,
but does not establish historical priority for it.
