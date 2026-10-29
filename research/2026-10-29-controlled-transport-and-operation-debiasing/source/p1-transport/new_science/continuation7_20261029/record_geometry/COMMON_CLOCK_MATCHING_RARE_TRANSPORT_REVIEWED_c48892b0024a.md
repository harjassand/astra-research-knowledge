# Matching rare-transport law for the conserving common-clock family

29 October 2026. Root follow-on receiving theorem. This closes the
scalar lower-bound gap left by the earlier common-clock upper bound,
at an explicitly warranted canonical initial law. It does not prove
the proposed full nonlocal density/current action.

## 1. Result and actual initialization

Use the even-N conserving ring

    r_i=c(1+alpha u delta_i), c=s/2, 0<alpha<1,
    u=sigma p(eta), p=(-1)^(sum_i i eta_i),
    delta_i=eta_i-eta_(i+1), A=sum_i delta_i^2.           (1)

One actual common Poisson clock flips sigma at physical rate gamma_N,
with gamma_N->infinity and gamma_N/N->0. Initialize occupancies from
the uniform canonical law with exactly M_N particles, M_N/N->m in
(0,1), and initialize sigma independently and fairly. Denote this
stationary joint law by mu_N. It is an actual initial-law premise;
this theorem does not supply its preparation or erase its retained
records. Conditional use requires that law, or the explicit additional
initial entropy condition discussed below, and the complete declared
future native-and-clock generator.

For Q_N=J(N^2T)/N^2, the scalar LDP at speed N has rate

    I_T^common(q)=q^2/[2s chi(m)(1-alpha^2)T].            (2)

Its scaled cumulant generating function is

    lim_N N^-1 log E exp[N lambda Q_N]
       =(s/2)chi(m)(1-alpha^2)T lambda^2.                (3)

The existing upper bound holds even for arbitrary deterministic
initial occupancies of the same asymptotic mass. The new lower proof
here is canonical-initial; it does not silently extend that upper
bound to a matching deterministic-initial theorem.

## 2. The corrected-current comparison has an unusually small adjoint source

On active native bonds define d_i=delta_i-alpha u; set d_i=0 on
inactive bonds, which do not produce events. Let M be the sum of d_i
over native events. The preceding exact construction gives

    sum_i r_i d_i=0,
    sum_i r_i d_i^2=c(1-alpha^2)A.                      (4)

Both r_i and the reference law are invariant under their own native
swap, whereas d_i changes sign. For a fixed real lambda define a
mathematical comparison generator by native rates

    r_i^lambda=r_i exp(lambda d_i/N),                   (5)

with the same common clock. No physical actuator for (5) is assumed.
On macroscopic time its adjoint, with respect to mu_N, satisfies

    (L_N^lambda)^*1
       =-2N^2 sum_i r_i sinh(lambda d_i/N).             (6)

The linear term vanishes exactly by (4). Since |d_i|<=2 and the
total native rate is at most cN, the cubic remainder gives

    ||(L_N^lambda)^*1||_infinity<=C_(lambda,c),          (7)

uniformly in N and gamma_N. A generic weak tilt has an O(N) form
cost; this particular corrected-current tilt has an O(1) adjoint
source. That cancellation is the useful additional connection.

## 3. Entropy controls the needed activity under the comparison law

Let f_t be the density of the comparison law relative to mu_N.
It starts at one. The elementary inequality log y-log x<=y/x-1,
applied to the finite-state jump generator, yields

    d/dt H(f_t mu_N | mu_N)
       =int f_t L_N^lambda log f_t dmu_N
       <=int f_t (L_N^lambda)^*1 dmu_N
       <=C_(lambda,c).                                (8)

Thus the entropy is bounded by C_(lambda,c)T on the full macroscopic
interval. Under mu_N the canonical activity satisfies

    E[A/N]=2m_N(1-m_N)N/(N-1), Var(A/N)=O(1/N).         (9)

For a fixed delta>0, Chebyshev gives a reference bad-event probability
O(1/N). The entropy event inequality

    nu(B)<= [H(nu|mu)+log2]/log[1/mu(B)]                (10)

then makes the comparison bad-event probability tend to zero,
uniformly for t<=T. Since 0<=A/N<=1, integration in time gives

    int_0^T A(eta_(N^2t))/N dt -> 2chi(m)T
                                    in P^lambda probability.    (11)

Only canonical finite-space moments and the O(1) entropy source were
needed. No complete common-clock hydrodynamic theorem was imported.
The same proof permits an initial relative entropy o(log N) against
mu_N using (9)--(10), if it is actually warranted. Stronger initial
entropy classes would require a stated stronger concentration bound;
they are not needed for the displayed theorem.

## 4. Typical corrected current and likelihood cost

Under (5), the scaled corrected current M(N^2t)/N^2 has a martingale
part of bracket O(1/N), and its drift is

    sum_i r_i exp(lambda d_i/N)d_i
       =[lambda c(1-alpha^2)/N]A+O_lambda(N^-1).        (12)

The remainder follows from bounded d_i and sum r_i=O(N). Hence (11)
implies

    M(N^2T)/N^2 -> v_alpha lambda,
    v_alpha=s chi(m)(1-alpha^2)T.                      (13)

The exact correction between Q_N and M/N^2 is superexponentially
negligible under the original law, as already proved. The likelihood
for (5) is a bounded weak tilt, |lambda d_i/N|<=2|lambda|/N. Its
second-moment identity therefore transfers that negligible event to
the comparison law. In particular Q_N has the same limit (13).

The likelihood is exactly

    Z_lambda=exp[lambda M/N-B_N(lambda)],
    B_N=int_0^(N^2T)sum_i r_i
          [exp(lambda d_i/N)-1-lambda d_i/N]dv.          (14)

The omitted linear compensator is identically zero by (4). Equations
(4) and (11) give B_N/N -> v_alpha lambda^2/2 in comparison probability.
Together with (13),

    N^-1 log Z_lambda -> v_alpha lambda^2/2.            (15)

Choose lambda=q/v_alpha. On a comparison-typical event with Q_N near
q and likelihood cost near I_T^common(q), restrict
P(B)=E^lambda[Z_lambda^-1 1_B]. This yields the lower exponent
-I_T^common(q). The existing local upper bound and exponential
tightness yield the full scalar LDP (2).

## 5. Exponential moments and the closed-gate limit

The bounded-jump martingale estimate gives a finite O(N) log-moment
bound for M/N at every fixed multiplier. In the exact correction for
Q_N, the common-clock martingale and its occupation integral each
cost only O(gamma_N) in fixed speed-N exponential moments under mu_N.
Holder's inequality therefore gives finite speed-N moment envelopes
at every multiplier for Q_N. Combining those envelopes at 2lambda
with exponential tightness supplies the exponential-integrability
tail condition. The LDP Laplace principle proves (3), not just a
formal Legendre calculation.

If instead alpha_N->1, including alpha_N=1 exactly, the existing
superexponential circulation suppression gives the degenerate rate
zero at q=0 and infinity elsewhere. Under the stated stationary law,
the same moment bounds have divided log costs bounded by
C_lambda[(1-alpha_N^2)+gamma_N/N+1/N], which vanish. The scaled
cumulant generating function is therefore zero; Jensen supplies the
matching lower bound since stationary mean current is zero.

The full shared-clock spatial action and deterministic-initial
matching lower bound remain open. The completed result already shows
that altering joint control correlations, at identical marginal
per-bond clock rates, can change a real rare-transport law within this
constructed reversible family. The independent/grouped fast-control
theorem supplies the reference law, while the present common-clock
regime supplies (2) or the closed-gate limit.
