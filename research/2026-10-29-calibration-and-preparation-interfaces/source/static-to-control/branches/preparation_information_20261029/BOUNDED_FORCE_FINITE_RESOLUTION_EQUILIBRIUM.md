# Bounded-force equilibrium closure at finite observation resolution

29 October 2026. Root construction; ordinary proof independently checked in
physical_frontier/BOUNDED_FORCE_FINITE_RESOLUTION_REVIEW.md and its separate
independent proof. The reviewed version is preserved under reviewed_versions/.
This removes the earlier uniform force-derivative cap for a weaker, operationally
specified conclusion. No physical source or hidden mixing estimate was acquired.

## 1. The theorem and physical interface

Fix a connected flat torus T^d of side 2pi, unit masses, gamma,tau>0 and A<infinity.
Consider stationary native kinetic sources

    dq=p dt,  dp=[F(q)-gamma p]dt+sqrt(2gamma tau)dW,        (1)

with smooth periodic position forces ||F||_infinity<=A (Euclidean norm).
There is NO uniform bound on derivatives of F. All momenta are thermalized
by the specified bath, odd under physical reversal; positions are even and
there is no odd external field. On the usual finite-entropy/Fisher and
integration-by-parts domain the physical entropy rate is

    sigma(F)=gamma*tau int rho_F
                       |grad_p log[rho_F/(nu_F M_tau)]|^2. (2)

Here nu_F is the position marginal, M_tau the centered Maxwell law of
covariance tau I. This calibrated bath identity is a source premise; an
arbitrary path-reversal divergence or visible fit does not establish it.

Write P_F for the full stationary law on
Omega_T=C([0,T],T^d x R^d). Use the bounded uniform path metric
d_path=min(1,sup_t[d_Torus(q,q')+|p-p'|]), and its bounded-Lipschitz distance
d_BL (test functions of absolute value and Lipschitz constant at most one).
Let E_A be stationary Gibbs path laws of the SAME bath and coordinates with
smooth periodic U, force -grad U and ||grad U||_infinity<=A.

**Uniform weak closure theorem.** For every fixed finite T,

    sup_{F smooth, ||F||<=A, sigma(F)<=s}
                    inf_{Q in E_A} d_BL(P_F,Q) ->0 as s->0.              (3)

An empty source class contributes zero. Neither a global hidden mixing
coefficient nor a force Lipschitz cap is used.

The proof supplies a stronger sequential fact: every sequence sigma_j->0
has a subsequence converging SETWISE on each specified finite path window
to a same-bath stationary Gibbs law with a periodic Lipschitz potential
and gradient bound A. Smooth Gibbs laws approximate that limit in path TV.
Setwise convergence concerns each FIXED measurable event; it is not the
uniform-over-events convergence defining TV. The oscillatory shear example
proves that full source-to-native-equilibrium path TV need not tend to zero.

### Observation consequences

For every fixed finite or countable-output noninvasive path-record kernel K,

    sup_{F: ||F||<=A, sigma(F)<=s}
                    inf_{Q in E_A} TV(KP_F,KQ) ->0.                      (4)

A fixed finite decision tree, including its settings/stops, is allowed.
The kernel must be the SAME operation as F varies; increasingly resolving
force-dependent tests are a different interface. The same conclusion holds
for fixed continuous-output kernels with a density k(z|omega), relative
to a fixed output measure, that is bounded in omega for almost every z.
Finite Gaussian report kernels with positive conditional noise and the
stated density bound fit this condition.

Uniformity over sensor families follows when one constant C bounds

    TV(K(omega,.),K(omega',.)) <= C d_path(omega,omega').

Their output-TV error is then at most max(1,C)d_BL. Ordinary finite Gaussian
sensors with a uniform Lipschitz bound on reported state features, a positive
noise floor and finite observation budget supply such families. Fixed electronic
gain alone does not bound a feature's spatial sensitivity.

These are passive kernels of a native path. A physical intervention that
changes the dynamics is not automatically such a kernel. The theorem gives
existence and a qualitative modulus, not a computable rate, an acquired
equilibrium generator, a hidden simulator, or an unbounded-lifetime guarantee.

## 2. Conditional thermalization, with no configurational mixing

Gaussian logarithmic Sobolev applied conditional on q gives

    D(rho_F||nu_F M_tau)<=sigma(F)/(2gamma),
    TV(rho_F,nu_F M_tau)<=sqrt[sigma(F)/(4gamma)].         (5)

The position marginal may have arbitrary slow memory. For sigma_j->0,
rho_j is therefore close to nu_j M_tau, but this alone does not give a
uniform density bound. The next step supplies the needed compactness.

## 3. One mathematical smoothing step supplies bounded densities

Let mu_0=u_Torus M_tau, stationary for FREE Kramers motion F=0.
Start the free process from ANY position probability nu and independent
Maxwell momentum. At a fixed time delta>0, p_delta remains Maxwell.
Conditional on p_delta, the lifted displacement int_0^delta p_s ds is
Gaussian of mean a_delta p_delta and covariance c_delta I, where

    a_delta=(1-exp(-gamma delta))/gamma,
    c_delta=(tau/gamma^2)
         [2gamma delta-3+4exp(-gamma delta)-exp(-2gamma delta)]>0.         (6)

The formula is the Schur complement of the joint Gaussian displacement
and terminal momentum: their covariance is tau a_delta, and displacement
variance is 2tau[delta/gamma-(1-exp(-gamma delta))/gamma^2].
Positive delta leaves a genuinely random displacement after conditioning.
The bracket in (6) equals 2 int_0^(gamma delta)(1-exp(-u))^2 du,
which proves its positivity directly; c_delta is asymptotic to
(2/3)tau gamma delta^3 as delta tends to zero.

The wrapped conditional Gaussian density has a finite maximum C_delta
relative to uniform position. Uniformly over every nu,

    d[(nu M_tau)P_0^delta]/d mu_0 <= C_delta.             (7)

For bounded F, let Z_F be its path likelihood relative to free dynamics
with the same initial law. Its Brownian drift change is
F(q)/sqrt(2gamma tau). The exponential-martingale identity gives

    E_0[Z_F^2 | initial state]
                   <=exp[A^2 delta/(2gamma tau)].         (8)

Write Z_F^2 as the exponential martingale with twice the integrand,
multiplied by exp(int |F|^2/(2gamma tau)); the latter has a deterministic
ceiling. Boundedness makes the former a true martingale.

Let r_F,nu be the forced endpoint density relative to mu_0.
If r_0 is the free endpoint density, then
r_F,nu=r_0 E_0[Z_F|endpoint]. Conditional Jensen and (7)--(8) imply

    ||r_F,nu||_L2(mu0)^2
                    <=C_delta exp[A^2 delta/(2gamma tau)].               (9)

Indeed r_0^2 <=C_delta r_0 before integrating the conditional second moment.

Set r_j=d[(nu_j M_tau)P_Fj^delta]/dmu_0. Stationarity and propagation of (5)
through the SAME transition kernel give

    TV(r_j mu_0,rho_j)<=sqrt[sigma_j/(4gamma)].            (10)

The r_j are uniformly bounded in L2. This delta is a mathematical smoothing
step, not an executed reset or a claim of physical mixing. Its constant
may be large and its operation/preparation are not made free.

## 4. Compact kinetic occupation lemma

For any fixed bounded measurable g(q,p), the linear map

    A_g:L2(u_Torus)->L2(P_0^mu0[0,T]),
    A_g f=int_0^T f(q_t)g(q_t,p_t)dt                     (11)

is COMPACT.

First ||A_g f||_2<=T||g||_infinity||f||_2 by stationary marginals and
Cauchy--Schwarz. The form of A_g* A_g is the double time integral of
E[f(q_s)g(Z_s)h(q_t)g(Z_t)].

On |s-t|<epsilon its absolute bilinear operator norm is at most
2T epsilon ||g||_infinity^2. This uses only uniform q marginals and
Cauchy--Schwarz, not independence of q_s and q_t.

On |s-t|>=epsilon, (q_s,q_t) has bounded joint density on the compact
torus pair. The displacement is wrapped Gaussian with positive variance

    b_|t-s|=2tau[|t-s|/gamma
                    -(1-exp(-gamma|t-s|))/gamma^2].

This density is uniformly bounded for lag in [epsilon,T].
Conditioning bounded g factors on q_s,q_t leaves a bounded integral
kernel. Its operator is Hilbert--Schmidt and hence compact.

Thus A_g* A_g is an operator-norm limit of compact operators as epsilon->0.
It is compact, so A_g is compact. In particular,

    f_j weakly ->f in L2 => ||A_g(f_j-f)||_L2(P0)->0.     (12)

This identifies which rapidly oscillating force information disappears
in finite-time occupation. It is not a bound on full drift likelihoods.

## 5. Identifying the nonlinear native path limit

Choose a subsequence F_j converging weak-* in L_infinity to F, with
||F||<=A. The torus has finite volume, so this also gives weak L2
convergence. Choose a weak L2(mu_0) subsequential limit r of r_j.

On the COMMON free path space P_0^mu0, the law of forced dynamics
started from r_j mu_0 has likelihood

    R_j(omega)=r_j(Z_0) Z_Fj(omega).

The conditional moment bound (8) at horizon T gives

    ||R_j||_L2(P0)^2 <=exp[A^2 T/(2gamma tau)] ||r_j||_L2(mu0)^2.        (13)

Take a weak L2 limit R. Positivity and integral one survive, so Q=R P_0
is a probability law. Every fixed bounded measurable path function lies
in L2(P_0); consequently its expectations converge. This is SETWISE
convergence. The initial law of Q is r mu_0.

It is essential to identify Q as native Kramers dynamics, without silently
discarding memory. Let phi be smooth with compact momentum support. For
every bounded past-measurable chi the j-th martingale identity is

    E_j[chi {phi(Z_t)-phi(Z_s)-int_s^t L_Fj phi(Z_a)da}]=0.

Replace F_j by F. Each resulting error has the form

    E_(R_j P0)[chi int_s^t (F_j,i-F_i)(q_a)
                                     partial_(p_i)phi(Z_a)da].

Its absolute value tends to zero by (13), Cauchy--Schwarz and the compact
occupation lemma for g=partial_(p_i)phi on [s,t]. The remaining identity
with F is a fixed bounded measurable path functional; weak L2 convergence
passes it to Q. Thus Q solves the martingale problem for L_F.

For bounded Borel position force F this martingale problem is well posed
in law. Bounded-drift Girsanov constructs it from the unique free Kramers
law. The inverse change of measure takes any solution back to that free
law. Localization supplies coordinate tests, and bounded drift makes the
required exponential martingales true on every finite horizon. No strong
solution estimate or smoothness of the limiting F is assumed.

Equation (10) makes the forced path law started at r_j mu_0 TV-close to
the TRUE stationary source for the entire window. All bounded finite-
dimensional stationarity identities therefore pass to Q. It is a genuine
stationary native kinetic process with force F, not an unspecified
reversible process or a visible fitted realization.

## 6. Identifying the Gibbs state

Equations (5),(10) imply that the limiting state has product form

    r mu_0=nu(q) M_tau(p).                               (14)

To verify this without an independence assumption, test bounded products
a(q)b(p): the finite-j product approximations factor, and their setwise
limits factor. The position density nu is nonnegative, normalized and L2.

Apply the stationary generator identity to phi(q)p_i with momentum
cutoffs, then remove the cutoffs using the Gaussian moments in (14).
Since F is bounded, this gives

    tau int nu partial_i phi +int F_i nu phi=0,
    grad nu=F nu/tau in distributions.                   (15)

Convolve nu with a positive periodic smoothing kernel. The positive,
normalized result nu_e satisfies |grad nu_e|<=(A/tau)nu_e. Hence log nu_e
has Lipschitz constant A/tau. Compactness and connectedness give uniform
positive upper/lower density bounds, for example exp(plus/minus
A*diam(Torus)/tau). Ordinary gradients are uniformly bounded too.
The limiting nu is positive and Lipschitz, and (15) yields

    U=-tau log nu up to a constant,
    F=-grad U almost everywhere,  ||grad U||<=A.          (16)

This is the genuine Gibbs state and conservative force of the same bath.
Time-reversal invariance of a visible record alone would not give (16).

## 7. Smooth competitors, uniformity and record laws

Mollify the periodic Lipschitz U. The smooth U_e have ||grad U_e||<=A,
converge uniformly to U and have gradients converging strongly in L2.
Their Gibbs position densities converge uniformly and their momenta
retain the same Maxwell law. Girsanov from the limiting stationary law gives

    D(P_U^mu[0,T]||P_Ue^mue[0,T])
      =D(mu||mu_e)+(T/(4gamma tau))
                        int nu |grad U-grad U_e|^2 ->0.                 (17)

The bounded density nu just established justifies the last limit. Thus
smooth same-bath competitors approximate Q in full path TV.

If (3) were false, a sequence sigma_j->0 would stay a fixed positive
d_BL distance from E_A. Steps 2--6 give a subsequence converging setwise,
hence weakly, to Q; d_BL then tends to zero. Approximation (17)
contradicts the separation. This proves the uniform qualitative modulus.

For a fixed finite/countable-output K, setwise path convergence gives
convergence of every output probability. Since probabilities sum to one,
the discrete Scheffe argument gives output TV convergence. For densities
k(z|omega) bounded in omega for almost every z, it instead gives pointwise
convergence of output densities, followed by Scheffe. Equation (17) transfers
both conclusions to smooth competitors. The same contradiction proves (4).

For a uniformly TV-Lipschitz K, every function omega->K(omega,B) lies in
[0,1] and has Lipschitz constant <=C. Applying d_BL uniformly in the output
event B proves the max(1,C) sensor-family bound of Section 1.

## 8. Scope of the advance and the remaining obstruction

The earlier native positive theorem required amplitude AND Lipschitz force
bounds for FULL path TV approximation. This theorem requires only amplitude,
while retaining fixed observational resolution or weak path topology. The
oscillatory shear failure makes the distinction necessary. Its fields can
drive vanishing physical entropy with persistent full-path native mismatch;
they cannot defeat every fixed finite-resolution experiment.

The load-bearing addition is the compact occupation and bounded-likelihood
argument that identifies a native limiting generator. Conditional Maxwell
thermalization and the stationary equation then identify Gibbs equilibrium.
Gaussian LSI, Girsanov, Hilbert--Schmidt compactness, weak martingale limits
and force matching are established machinery, not claimed inventions.

No effective modulus, source reconstruction, general intervention closure,
physical preparation, unbounded-horizon lifetime guarantee or algorithmic
speedup is supplied. The force cap, bath identity, physical reversal and
native source class remain warranted inputs. The time-paired finite-family
record in GENERAL_THERMAL_MEMORY_METRICS.md is the separately effective
acquisition route for its one-way class; this closure theorem is broader
but currently qualitative. Priority for the exact conjunction is unresolved.

