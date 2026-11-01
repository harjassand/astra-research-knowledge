# Independent theorem audit: autonomous Gibbs-conditioned mean hitting time

## Verdict and exact scope

**PASS for the mathematical Poisson-current MFPT construction and formula (9)**, with u=0 understood as the inherited inaccessible no-killing boundary. The scalar source current, zero-resolvent passage, full tail estimates and scalar-only outer formula are sound. This is genuinely a mean-hitting-time statement for the declared autonomous engineered diffusion, not a renaming of capacity/mass and not a clamped-protocol CIR calculation.

The audited source snapshot is `POISSON_CURRENT_MFPT_CANDIDATE.md`, SHA-256 `094fee3f0c6f401f9e15bfab9a16843e1269b45d3fb58f10b6633a039db3b026`. It is preserved as `received_initial_candidate.md`. A later corrected source, if any, is bound separately. No candidate consumer or saved numerical certificate was imported, run or accepted.

One terminology issue was reported: the source calls u=0 “natural inaccessible.” In Feller classification it is entrance, not natural, for alpha>=1. The proof uses the no-killing inaccessible interface already established for the exact lift; its variational/exhaustion argument is correct with that interpretation. No equation depends on a natural-boundary classification.

## 1. Actual process and exactly declared initial law

The radial mobility is multiplied by an ACTUAL finite positive gamma. With the accepted tangent field program and the correct divergence drift, the pointwise quotient is

    dY=-v'(Y)u dt+sqrt(2/beta)dW,
    du=gamma(alpha/beta-v(Y)u)dt+sqrt(2gamma u/beta)dB.

This is neither the old constant-SPD process nor a mere numerical time change: longitudinal mobility remains one. Tangent dynamics annihilate every function of U and may be nonmixing. For the concrete raw program, the previously received positive-coefficient homogeneous grammar, acquired coercivity, and explicit complete-pair smooth tangent noise fields are inherited. An arbitrary unverified positive semidefinite matrix program is not automatically the same received interface.

For c=1+2kappa/gamma,

    GW=[2+(gamma+2kappa)alpha]/beta
          -[2yv'+(gamma+2kappa)v]u
       <=[2+(gamma+2kappa)alpha]/beta-gamma u.

The accepted stopped Lyapunov/coercivity argument therefore still excludes infinity escape. The time change uses A(t)=gamma integral_0^t v(Y_s)ds and s(t)=gamma/beta integral_0^t exp(A(r))dr, yielding the same squared-Bessel dimension 2alpha. It excludes origin hitting for alpha>=1. Thus every fixed positive finite gamma is an actual globally conservative process, even with large admissible tangent coefficients.

The unnormalized projected Gibbs measure is rho=q pi_y, q=v^-alpha, where pi_y is the normalized Gamma law with shape alpha and rate beta v(y). Its total mass is finite. The initial law is EXACTLY rho restricted to A, divided by M_A. The all-start quotient theorem also permits a full-state law singular in angle, such as an exact fixed-ray lift, provided its (Y,U) pushforward is precisely this law. It is not full angular Gibbs sampling, but the y-hitting observable has the same law.

This symbolic initialization is a mathematical assumption, not a finite-bit sampler, experimentally prepared distribution or inferred physical state. A total-variation error by itself does not control an unbounded hitting-time mean. Any approximate-preparation claim needs an independent weighted expectation or density-control argument. For example, a globally verified multiplicative initial-density bound would control every nonnegative expectation, but no such approximate-preparation certificate is supplied here.

## 2. Resolvent, occupation identities, and earned finiteness

Let H be the nonnegative self-adjoint operator of the killed reversible form on Omega={y<b,u>0}, with zero target trace at y=b and no killing at the inaccessible u boundary. For lambda>0, R_lambda=(H+lambda)^-1 is bounded on L2(rho); the sources 1_A,1_S,1_Omega are in that space because rho has finite mass.

The killed Markov/Feynman–Kac identity gives

    <1_A,R_lambda 1_Omega>
      = integral_A rho E_x[integral_0^tau_B exp(-lambda t)dt].

The variational formula

    <f,R_lambda f>
      = sup_h [2<f,h>-E(h,h)-lambda||h||^2]

has the stated sign and normalization. Positive semigroup kernels make each diagonal source quantity and the A/S cross quantity monotone as lambda decreases to zero. Operator Cauchy–Schwarz gives

    0<=<1_A,R_lambda 1_S>
          <=sqrt(<1_A,R_lambda 1_A><1_S,R_lambda 1_S>).

Once the two diagonal limits are bounded by the finite source currents, this inequality bounds the cross limit as well. Since 1_Omega=1_A+1_S almost everywhere, monotone convergence THEN gives

    M_A T_A=Q_A+Q_AS<infinity.

There is no assumed inverse at zero, spectral gap, L2 Poisson solution, finite mean, or global target-hitting theorem hidden in this step. It earns the finite averaged mean at this initialization. It need not prove a finite mean from every deterministic full state.

One may justify all identities first for killed compact-cylinder forms and then exhaust the domain. Killing at intermediate u cutoffs disappears because the actual boundary is inaccessible and the full process is nonexplosive. The generator/domain interface matters; an artificial boundary condition at u=0 would define a different process.

## 3. The explicit source current and its dual cost

For f=1_A or 1_S, define J_f(y)=integral_(-infinity)^y q(s)f(s)ds. With w=-(v'/v)u and j_f=J_f pi_y (1,w), the exact Gamma scaling identity is

    partial_y pi_y+partial_u(w pi_y)=0.

Indeed partial_y log pi_y=alpha v'/v-beta v'u, while partial_u(w pi_y)/pi_y=-alpha v'/v+beta v'u. Thus div j_f=rho f. No unknown conditional sampler, angular density or committor has entered.

For compact zero-target-trace tests, integration by parts gives <f,h>=-integral j_f.grad h. The inverse Dirichlet mobility is diag(1,1/(gamma u)), so weighted Cauchy gives

    |<f,h>|^2 <= D_f E(h,h),
    D_f=beta integral J_f^2/q [1+K]dy,
    K=alpha v'^2/(beta gamma v^3).

The transverse conditional expectation is E_pi[u]=alpha/(beta v). Hence there is exactly one factor beta in the longitudinal cost and no additional beta multiplying the final transverse cost. The u-flux tends to zero at zero and infinity because u pi_y is proportional to u^alpha exp(-beta vu). The target flux is allowed because h vanishes there.

Writing X=E(h,h), the variational expression is at most 2sqrt(D_f X)-X<=D_f, even before subtracting the nonnegative lambda term. Therefore Q_f<=D_f. This upper bound extends from the compact core to the form domain by closure; it does not require knowing a minimizer.

## 4. Scalar lower trial without an invalid L2 assumption

For scalar h, the marginal energy is beta^-1 integral q h'^2. The one-dimensional source trial has

    h'(y)=-beta J_f(y)/q(y),  h(b)=0,
    L_f=beta integral J_f^2/q.

Its energy is L_f and its source pairing is also L_f by integration by parts. For f=1_A, in the left tail J_A=O(|y|^(1-4alpha)), h'=O(|y|), h=O(y^2). Thus the boundary term hJ_A tends to zero when alpha>3/4, and both energy/source integrals are finite under the same condition. The square h^2 need not be integrable when alpha is near one, so inserting this h directly into an L2 resolvent variational formula would be unjustified.

The source correctly avoids that problem. First truncate values h_N=min(h,N), preserving the target trace. These are bounded and hence L2(rho); their source pairings and energies converge monotonically to L_f. Spatial approximation can be made explicit: first cut off y at a large negative distance, then at fixed compact y support cut off large u and small u. Upper-u costs vanish by the Gamma exponential tail. The origin cutoff has arbitrarily small energy for alpha>1 by a power cutoff and at alpha=1 by a logarithmic cutoff, since its local energy weight is proportional to u^alpha. The order of these cutoffs avoids requiring a single uniform origin estimate over the unbounded y tail. Smooth approximation on the remaining compact cylinder is ordinary.

For each finite test take lambda down to zero first, then remove the approximations. This yields Q_f>=L_f in the extended-energy sense without assuming h itself is L2. For f=1_S, J_S is zero to the left of -b, so the corresponding trial is bounded there and easier.

## 5. Cross-source comparison and the exact current sandwich

For y<-b, J_S=0. On the slab [-b,b), J_A=M_A and 0<=J_S<=M_S. Since the common current weight is nonnegative,

    D_S<=(M_S/M_A)^2 D_A.

Thus Q_A+Q_AS<=D_A+sqrt(D_A D_S)<=(1+M_S/M_A)D_A. Positivity gives Q_A+Q_AS>=Q_A>=L_A. Dividing by the SAME unnormalized basin mass proves

    L_A/M_A <= T_A <= (1+M_S/M_A)D_A/M_A.

This is a Poisson occupation-source statement, not a capacity identity. The global Gibbs normalizer cancels, but the A/S occupation cross term is retained and controlled rather than silently omitted.

## 6. General infinite tails

On the left tail y=-x, J_A(-x)=M(x)=integral_x^infinity v(t)^(-alpha)dt. For fixed positive kappa,

    q(x)=Theta(x^-4alpha),
    M(x)=O(x^(1-4alpha)),
    M(x)^2/q(x)=O(x^(2-4alpha)),
    K(x)=O(x^-6).

Therefore L_A and D_A are finite for alpha>3/4. The actual lift imposes the stronger alpha>=1. The compact slab and near-well pieces are harmless. D_S is finite by the pointwise comparison. These are full infinite tails; no reflecting wall or finite-box replacement is used.

The threshold also explains the lower-trial boundary calculation: hJ_A=O(x^(3-4alpha)) vanishes under exactly the same sufficient condition. It is not necessary to assume a global Poincare inequality, which would be problematic for the polynomial longitudinal tails.

## 7. Independent derivation of every constant in formula (9)

Now take integer alpha>=4, b=1/2, d=1/alpha<=1/4, a=v(b)=1+9kappa/16, and c=v(1+d).

**Near basin.** On [b,1], v<=a. On [1,1+d], v<=c<=a, because ((1+d)^2-1)^2<=81/256<9/16. Also |v'|<=4kappa over [b,1+d]: on [b,1] its factor x(1-x^2) is at most one, and on [1,5/4] x(x^2-1)<=45/64<1. With M(x)<=M=M_A,

    integral_b^(1+d) M(x)^2 v^alpha
       <= M^2[(1-b)a^alpha+d c^alpha]=M^2 S0,
    integral_b^(1+d) M(x)^2 v'^2 v^(alpha-3)
       <=M^2(1+d-b)(4kappa)^2 a^(alpha-3)=M^2 S1.

Here alpha>=4 ensures the power alpha-3 is nonnegative; no inequality direction is reversed.

**Far basin.** For x>1, v'>0 and v''=4kappa(3x^2-1)>0. The convex tangent bound yields

    M(x)<=integral_0^infinity[v(x)+v'(x)t]^(-alpha)dt
         =v(x)^(1-alpha)/[(alpha-1)v'(x)].

Since v'(x)=4kappa x(x+1)(x-1)>=8kappa(x-1), v>=1 and alpha>=4,

    M(x)^2 v(x)^alpha
       <=1/[64kappa^2(alpha-1)^2(x-1)^2].

Integrating from 1+d to infinity gives exactly Wfar=1/[64kappa^2(alpha-1)^2 d]. For the transverse tail,

    M(x)^2 v'^2 v^(alpha-3)
       <=v^(-alpha-1)/(alpha-1)^2
       <=q(x)/(alpha-1)^2.

Its integral is at most M/(alpha-1)^2. This deliberately uses the whole basin mass as an upper bound for the smaller far tail; no cumulative-integral oracle is supplied.

**Slab.** Put W=v^alpha on [0,b], where -W'>=0 and v>=a. Then

    K W=[-v'/(beta gamma v^2)](-W')
        <=[4kappa/(beta gamma a^2)] y(-W').

Integration by parts gives integral_0^b y(-W')=integral_0^b W-bW(b)<=integral_0^b W. Evenness therefore gives

    integral_(-b)^b K v^alpha
       <=[4kappa/(beta gamma a^2)]R.

This bound is confined to the slab, not incorrectly applied past the well. Also M_S<=2b a^-alpha=a^-alpha.

**Assembly.** The slab part of D_A is at most

    beta M^2 R[1+4kappa/(beta gamma a^2)].

The near basin adds beta M^2 S0+(alpha/gamma)M^2 S1. The far basin adds beta Wfar+alpha M/[gamma(alpha-1)^2]. Divide their sum by M and multiply by 1+a^-alpha/M. This is EXACTLY the source's T_high in (9). The scalar L_A contains the positive slab term beta M^2 R; dropping its basin contribution gives T_low=beta M R.

There is no missing factor two: R is the full transition slab, M is one basin, and the source tail occurs only once on the left. There is no extra beta in the gamma terms because beta K=alpha v'^2/(gamma v^3). For beta=kappa=1 the slab overhead is exactly 1024/(625gamma), hence 2/625=0.0032 at gamma=512.

Only M and R require numerical quadrature in this sufficient bound. For integer alpha all other terms are rational arithmetic/rational integer powers from rational parameters. A receiver must still enclose M/R, their infinite tails, all propagated arithmetic, and the requested TOTAL ratio. Poor parameters or loose bounds may validly return UNKNOWN. No fixed finite accuracy result is inferred merely from the large-alpha statement.

For fixed positive beta,kappa,gamma, the extra source/basin ratios vanish at large alpha: R concentrates at the barrier v(0)=1+kappa, M concentrates near the well v(1)=1, a<1+kappa, and c=1+O(alpha^-2). Thus the stated qualitative suppression of the retained corrections is consistent. This is not a numerical substitute for a finite certificate.

## 8. Model, computational and preparation costs remain real

Gamma=512 is a declared physical/program kinetic gain. It is not free acceleration of the original process, and its stiffness, bandwidth, noise realization and divergence drift require an actual implementation contract. Tangent kinetics disappear only because the exact lift is pointwise closed and the target depends on Y; their complete input validation is still paid.

The first executable must validate the full positive homogeneous energy program, the tangent/radial mobility program, coercivity/degree/origin conditions, beta/kappa/gamma, the exact Gibbs|A observable initialization, all numerical budgets and M/R enclosures. A previous capacity certificate or clamped-CDF certificate does not authenticate this different mean query. Full sampling/preparation, roots, measurement errors and hardware are not received by a symbolic polynomial alone.

The theorem's initial law is exact. It provides no assertion that finite-bit total-variation approximation preserves this unbounded mean. It also gives no confidence interval for empirically estimated parameters, no claim that all deterministic starts have finite means, no autonomous finite-time CDF, and no independent performance advantage over an equally informed two-dimensional Poisson/variational solver.

## 9. Prior credit, failed retrieval and executed checks

The actual proof uses ordinary killed resolvents, symmetric Dirichlet-form duality, source currents, conditional transport and Cauchy–Schwarz. These are not claimed as new primitives. The accepted kinetic-lift receipt already verifies the Bussi and Lelièvre–Santet–Stoltz comparisons; they are not discarded by changing the observable.

The new cited primary barrier-paper URL was attempted once through the web tool: `https://www.georgejpappas.org/wp-content/uploads/2024/04/CDC04-Barrier.pdf` returned HTTP 404. This is a confirmed retrieval failure, not a pending tool outcome. No retry, alternate source route or inferred successful reading was made. Consequently this reviewer does not independently accept that bibliography item's exact contents or location. The directly checked mathematical proof does not depend on importing a theorem from that paper, so this limited source failure does not block the theorem audit.

The independent second script passed **4,744 exact assertions**, covering transport/dual-weight identities, gamma Lyapunov algebra, current-to-formula-(9) assembly, asymptotic powers, exact overhead constants, and representative rational near/far inequalities for alpha=4 through 24 and three kappa values. Representative tests supplement the all-point inequalities proved above; they are not a global positivity oracle or a numerical MFPT certificate.

The first script stopped on a CAS representation issue: SymPy's rational cancel did not combine arbitrary-alpha powers of an expanded positive quartic. The exact identity was restated in a positive scalar base, with the same mathematics, and the second run passed. Both scripts and a failure explanation are preserved. No author source or implementation was changed by this reviewer.
