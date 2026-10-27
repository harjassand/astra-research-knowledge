# From certified receiving densities to the actual global affinity objective

## Scope

This is a constructive algorithm specification, not an implemented large PDE/optimization run and not an evaluated new affinity gain. It closes the input-model gap between the global Lipschitz reward oracle and a legitimate affinity derivative. Every measure being optimized is an actual complete paid law. Density certificates and finite quadrature are only evaluators, not substitute physical laws.

## 1. Finite nested policies are computable finite Brownian mixtures

For a finite dyadic-helper policy with rational randomization, the internal transition matrix is rational and proper by the uniform variance/visits bound. Its occupation vector is the exact rational solution of(I-P^T)v=delta0. The absorbing Brownian macro weights are rational, nonnegative and sum1. Thus its terminal law is exactly a finite mixture of Brownian exit laws from strict interior helpers.

The invariant smoothing identity also gives

 omega_x K_a=omega_{ax}.

Hence homothetic paid smoothing and rational convex mixtures preserve this finitely representable class. For dyadic a, the scaled interior helpers lie in a later dyadic family. No new abstract law type is required.

## 2. Use a computable reference floor on a truncated ACTUAL target

A finite Brownian mixture need not dominate mu uniformly near every vertex. Do not pretend otherwise. Instead choose integer M>=4, preferably a power of2, and let A_M be the source points on the two sheets with

 pi/M<=a_phase,b_phase<=pi-pi/M.

Its actual source mass is exactly p_M=(1-2/M)^2. Put mu_M=mu|A_M/p_M. All four vertex heights on A_M exceed1/M^2: already the u,v deficits sum to at least2(1-cos(pi/M))>=6/M^2. The audited explicit Brownian lower bound therefore gives

 omega0 >= c_M mu on A_M, c_M=9^(-864M^2)>0.

This is an explicit rational constant, albeit extremely small. It is only asserted on A_M. The target truncation is paid analytically by

 |Phi(mu,eta)-Phi(mu_M,eta)|
 <=sqrt(2-2sqrt(p_M))                                     (1)

uniformly over all eta, by Cauchy-Schwarz on square-root densities.

Fix rational0<theta<1 and a DYADIC rational homothety0<a<1. Optimize over nu in C

 F(nu)=Phi(mu_M, eta_nu),
 eta_nu=theta omega0+(1-theta)nu K_a.

The reference and every update are complete paid laws. Let c=theta c_M and C_a=600(1-a)^(-6). On A_M the actual density r=deta_nu/dmu is at least c; everywhere it is finite and computably bounded above for finite Brownian mixtures.

## 3. An EFFECTIVE continuous gradient, with null-set versions removed

The directional derivative is

 DF(nu)[nu'-nu]=((1-theta)/2) integral G d(nu'-nu),
 G(z)=integral g(y)K_a(z,dy),
 g(y)=1_A_M(y)/[sqrt(p_M)*sqrt(r(y))].                      (2)

The actual receiving kernel is AC relative to mu, so arbitrary mu-null-set versions of g do not affect G. Even an atomic candidate nu' is physically smoothed before contributing; no raw-atomic affinity derivative is used.

The kernel interior harmonic estimate gives the explicit bounds

 |G|<=1/[sqrt(p_M)*sqrt(c)],
 Lip(G)<=12/[(1-a)sqrt(p_M)*sqrt(c)].                        (3)

To COMPUTE G, use the annulus lower-density evaluator for the finite Brownian mixture eta_nu. It gives a simple q<=r with a certified missing mass e=1-integral q dmu. On A_M put qbar=max(q,c)<=r and define

 gbar=1_A_M/[sqrt(p_M)*sqrt(qbar)].

The inverse-square-root derivative bound yields

 ||g-gbar||_{L1(mu)} <=e/[2sqrt(p_M)c^(3/2)].

Using the actual uniform kernel density ceiling,

 sup_z |K_a g(z)-K_a gbar(z)|
 <=C_a e/[2sqrt(p_M)c^(3/2)].                              (4)

The simple gbar is a finite phase-cell function with computable coefficients. Its Brownian expectation K_a gbar is computable to any requested accuracy using continuous phase-cell cutoffs, the uniform K_a<=C_a mu strip payment, and the certified Lipschitz WOS reward evaluator. Thus(4) supplies a certified point-evaluation algorithm for G with the explicit Lipschitz constant(3). This meets the actual input model of the global positive-accuracy reward oracle. Neither mere bounded measurability nor an arbitrary density version was treated as a free oracle input.

## 4. A finite, certified global optimization algorithm for fixed M,a,theta

Along any segment between nu and nu', both smoothed receiving densities lie between0 and C_a, while the mixture density on A_M stays above c. Therefore the absolute second derivative of F is at most

 (1-theta)^2 C_a^2/[4sqrt(p_M)c^(3/2)].

For a simple rational upper bound one may use H=C_a^2/(p_M c^2). This bound is conservative but explicit.

At each step evaluate the continuous reward G from Section3. The global reward oracle returns an actual paid competitor nu' and verified bounds A<=integral G dnu', sup_C integral G<=B, with B-A as small as requested. Compute the current expectation integral G dnu to matching certified accuracy (nu is a finite Brownian mixture). Concavity gives the true GLOBAL gap bound

 max_C F-F(nu) <=((1-theta)/2)[B-integral G dnu].             (5)

If the certified upper side of(5) is below the desired tolerance epsilon, stop. Otherwise make the oracle and expectation errors smaller than epsilon/8 in derivative units and RECHECK the upper-gap stopping test with these refined certificates. If that refined test now passes, stop. Only if the refined upper gap still exceeds epsilon does the summed error budget supply a certified positive directional derivative D_lower>epsilon/2. A coarse failed test alone is not sufficient. Take rational step alpha=min(1,D_lower/H). Curvature gives

 F((1-alpha)nu+alpha nu')-F(nu)
 >=alpha D_lower-H alpha^2/2
 >=min(epsilon/4,epsilon^2/(8H)).

Since0<=F<=1, only finitely many such non-stopping steps are possible. All updates are convex mixtures of COMPLETE laws, and all densities/evaluations remain in the finite Brownian-mixture class. This is a terminating fixed-parameter global optimization specification, not an unsafe residual subtraction scheme.

For an evaluated objective value, a lower density q<=r also gives

 L=(1/sqrt(p_M)) integral_A_M sqrt(q)dmu <=F,
 F<=L+sqrt(1-integral q dmu).

Thus both the objective and its gradient have correctly directed receiving certificates.

## 5. Recovering the unrestricted affinity optimum without inventing a rate

Let Phi_* =max_{eta in C}Phi(mu,eta). The maximum exists by compactness and upper semicontinuity. The invariant paid semigroup proves affinity-optimum density of the nested finite Brownian-mixture family, including singular maximizers. Consequently enumerating its rational policies/mixtures and evaluating their actual affinities gives certified lower bounds increasing to Phi_*.

Alternatively run the fixed-parameter algorithms above with M increasing, a tending to1 and theta tending to0. The uniform target error(1), the invariant source-TV receiving theorem, and the inequality

 Phi(mu_M,(1-theta)eta+theta omega0)>=sqrt(1-theta)Phi(mu_M,eta)

show that these optimized values approach Phi_*. No effective source-TV modulus is presumed; this statement alone supplies no numerical stopping scale.

The audited affinity dual identity supplies the matching upper search:

 Phi_* =inf_{f continuous, f>0} (1/2)[V_f(0)+integral(1/f)dmu].

Positive rational polynomials restricted to Sigma are dense among the positive continuous rewards for this expression. Their positivity and boundary Lipschitz constants are certifiable, the actual source integral1/f is computable by phase quadrature, and the global positive-accuracy reward oracle returns an ACTUAL verified null-concave upper majorant for V_f. Dovetail these actual upper certificates with the actual paid affinity lower evaluations. They converge to the same Phi_*, so an arbitrary positive requested interval width eventually has a certificate.

This is an end-to-end positive-accuracy global affinity optimization specification. It is not a finite decision at Phi_*=1, and no numerical near-unit value or subunit upper gap has been obtained here.

If an evaluated upper certificate is ever strictly below1, its verified f and majorant give a true source gap: f+1/f>=2 implies integral f dmu>V_f(0). The existing audited global2x2 extension and actual-gradient receiving theorem then apply. If Phi_*=1, the actual paid lower laws can approach mu in Hellinger/TV, but no finite run of the abstract procedure alone proves exact membership. These are the actual remaining scientific alternatives.
