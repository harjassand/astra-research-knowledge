# Independent full theorem derivation review

## A. Verdict and fixed boundary

**PASS, theorem-only**, for `WELL_REDISTRIBUTION_CURRENT.md` SHA `207d9ee314c2c3f4638d0a3c45eaa7e23fd85246010ef799fd538201a0278ab7` and `UNIFORM_ANGULAR_UNIVERSALITY_CANDIDATE.md` SHA `7b21a27ccb6cfd0b73f987ba4683a9bda7e163b556dfd8cc2a4ea525b2e50e78`. Both were read completely. Their quoted freeze hashes also match: current freeze `c8b611cb33803a972c10efc1abe35a883c7d92ce240871e3e4f292cf241bc3fb`, universality freeze `37f68ba0c99c3a7ad0a301184ec29489f9f64703d11c7b158520874527f2299d`.

The freeze manifests are provenance boundaries, not acceptance of their executable contents. This review does not inspect or accept the candidate implementation, finite numerical result, paid work budget or physical preparation. No source correction was required. Original and revised historical sources remain untouched. The later exponentially small mobility note is outside this review.

## B. Actual model, normalization, and global process

The potential is v(y)U(z), v=1+kappa(1-y^2)^2; the mobility is diag(1,M_z), with fixed finite SPD M_z>=mu I and no cross block. The current constructed below is a dual witness, not a force or mobility inserted into this SDE. The generator remains

    L = beta^-1 (partial_yy + M_z : Hess_z)
        - v' U partial_y - v M_z grad U . grad_z.

For any smooth coercive homogeneous quartic, Euler's identity z.grad U=4U gives, for K0=1+kappa/4,

    L[1+y^2+K0 z^T M_z^-1 z]
      = 2(1+K0 m)/beta - 2[yv'+4K0 v]U
      <= 2(1+K0 m)/beta - 8U.

Here yv'+kappa=kappa(2y^2-1)^2>=0 and v>=1. The Lyapunov function is proper for each fixed SPD matrix. Local smoothness, stopping and this upper drift bound give a global nonexplosive solution. Its conservative reversible gradient-diffusion form has finite Gibbs reference measure because the y marginal is q=v^-alpha, alpha=m/4>=4. There is no singular origin, projected Markov closure, angular relaxation or uniform coefficient-upper-bound assumption. Constants in this Lyapunov receiving may depend on the model; the final numerical bounds do not. No uniform-in-model path convergence is being invoked.

Homogeneity gives Z(s)=int exp(-beta s U)=(beta s)^-alpha Z_U. Thus pi_s=(beta s)^alpha exp(-beta sU)/Z_U integrates to one, and rho=q pi_v is one constant multiple of the actual Gibbs density. Scaling the reference density/current by any common constant scales Q_A, Q_S, energies and basin mass together, leaving the mean and spectral conclusions invariant. The uncomputed Z_U is used only in exact analytic identities and cancels; its numerical value is not an input oracle.

The virial identity E_pi_s U=alpha/(beta s), coercivity U>=d_min||z||^4/m, M_z^-1<=mu^-1 I and Jensen give

    E_pi_s z^T M_z^-1 z
      <= mu^-1 sqrt[m alpha/(beta d_min s)]
      = 2 alpha/[mu sqrt(beta d_min s)].

This is the stated equation (1). It holds for nonconvex angular quartics as well as the admitted positive-coefficient grammar. It requires no upper coefficient or condition-number bound.

## C. Current identity, interfaces, and full inverse-mobility norm

Write V=1+kappa. Direct differentiation yields

    partial_s pi_s=(alpha/s-beta U)pi_s
                 = div_z(z pi_s/(4s)).

On the well segment with v<V, j_y=J pi_V and F_v=-(z/4)int_v^V pi_s/s ds. Hence div_z F_v=pi_v-pi_V, partial_y j_y=q pi_V, and div j=q pi_v. The y dependence of F_v is irrelevant to this divergence: j_z is differentiated in z, not y. On the far left v>=V, the ordinary conditional-dilation formula cancels the J partial_y pi_v term and leaves J'pi_v=q pi_v. On the slab, J=M and pi_V are constant in y and j_z=0.

The switching locations are y=-sqrt(2) and y=-b. J and pi_(max(v,V)) have matching traces there, so the normal component j_y matches. The jump in j_z is tangential to these hyperplanes; it creates no distributional surface source. The current is smooth in z, including z=0. This proves the source identity on compactly supported smooth tests in the killed domain. A target-boundary flux is allowed: killed tests have zero trace at y=b. There is no additional source at a mathematical origin or interface.

For D=diag(1,M_z), the dual resistance is

    beta int j^T D^-1 j/rho.

There are no cross terms. This uses the actual inverse mobility and its actual lower floor; replacing it by Euclidean norm without mu would be invalid.

For 2s-v>0 the normalized density identity is

    pi_s^2/pi_v=[s^2/(v(2s-v))]^alpha pi_(2s-v).

Multiplication by q^-1 cancels the v factor in the longitudinal norm. In particular the slab resistance is exactly beta M^2 R_plus, R_plus=int [V^2/(2V-v)]^alpha. Its denominator is at least V on the slab. The identity

    V^2/(2V-v)-v=(V-v)^2/(2V-v)>=0

proves R_plus>=R.

For F_v, integral Cauchy in s supplies the factor (V-v)/16. The moment estimate at 2s-v then supplies 2alpha/[mu sqrt(beta d_min(2s-v))]. Their product is precisely K(V-v), K=alpha/[8mu sqrt(beta d_min)]. The remaining q factor yields the stated integrand

    [s^2 sqrt(2s-v)]^-1 [s^2/(v^2(2s-v))]^alpha.

For 1<=v<=s<=V, s^2/(2s-v) increases in s, and V^2/[v^2(2V-v)] decreases in v: its logarithmic derivative is (3v-4V)/[v(2V-v)]<0. Thus the ratio is at most G_1=V^2/(2V-1). Also s^2 sqrt(2s-v)>=1 and both s-interval factors are at most kappa. This gives exactly K kappa^2 G_1^alpha. The redistribution interval has length sqrt(2)-1/2<1, proving the whole transverse cost in (8). No homotopy quadrature or fiber PDE is needed to pay this norm.

## D. All constants and infinite basin tails

The global conditional-dilation correction is K v'^2/v^(5/2). With r=sqrt(kappa)|y^2-1| and y^2<=1+|y^2-1|,

    v'^2/v^(5/2)
      <=16[kappa r^2+sqrt(kappa)r^3]/(1+r^2)^(5/2)
      <=16(kappa+sqrt(kappa))<=32 max(kappa,1).

Hence D_max=32K max(kappa,1)=4alpha max(kappa,1)/[mu sqrt(beta d_min)], as stated.

On the half slab W=v^alpha is decreasing, -v'<=4kappa y and v>=a_b. Thus

    K v'^2 v^(alpha-5/2)
      <=4kappa K/[alpha a_b^(3/2)] y(-W').

Integration by parts gives int_0^b y(-W')=int_0^b W-bW(b)<=int_0^b W. Evenness yields C_s=kappa/[2mu sqrt(beta d_min)a_b^(3/2)]. This is an integrated slab correction, not a global pointwise replacement.

For x=-y in [b,1+delta], delta=1/alpha<=1/4, the maximum v is at b because v(5/4)<=v(b); their exact difference is 63kappa/256. J<=M and V^2/(2V-v) is increasing in v. This gives (9), with length 1+delta-b.

For x>1, v is convex increasing. Its tangent lower bound gives directly

    int_x^infinity v(t)^-alpha dt
      <= v(x)^(1-alpha)/[(alpha-1)v'(x)].

Moreover v'(x)-8kappa(x-1)=4kappa(x-1)^2(x+2)>=0. On [1+delta,sqrt(2)], after squaring the cumulative bound, the longitudinal integrand is at most

    V^2 G_1^alpha/[64kappa^2(alpha-1)^2 delta^2].

The interval length is below 1/2, giving exactly the **128** denominator in (10). On [sqrt(2),infinity), the current is conditional dilation, so its longitudinal norm is at most

    1/[64kappa^2(alpha-1)^2(x-1)^2],

using v^(2-alpha)<=1. Multiplication by 1+D_max pays the entire transverse norm. Extending the lower limit down to 5/4 enlarges the integral, and int_(5/4)^infinity (x-1)^-2 dx=4. This gives exactly the **16** denominator in (11). These estimates cover the whole basin; no cutoff is silently discarded. Combining all disjoint regions and both norm components yields (12), with all beta factors present.

## E. Form core, infinity and zero-resolvent receiving

A rigorous route avoids any need to smooth the current globally or assert that it vanishes pointwise at infinity. The current is locally regular piecewise with matching normal traces, and its proved weighted resistance D_j is finite. For g in C_c^infinity({y<b}), distributional integration by parts and Cauchy give

    |<f,g>_rho| = |int j.grad g|
                <=sqrt(D_j) sqrt(E(g,g)).

The actual killed form is the closure of this local smooth core, with zero target trace. The coefficients and reference density are smooth and locally elliptic; the conservative unique diffusion above supplies the process realization. Approximation in E+r||.||² extends the pairing identity and bound to the form domain. This is a weighted dual-energy statement; it does not require j to belong to a global unweighted H(div) space.

For g=(K+r)^-1 f, r>0, let Q_f(r)=<f,g>. The resolvent identity gives Q_f(r)=E(g,g)+r||g||². Therefore Q_f(r)<=sqrt(D_j Q_f(r)), hence Q_f(r)<=D_j. Monotone convergence as r decreases to zero yields a finite inverse form Q_f<=D_j before any zero-inverse operator, spectral gap or finite hitting mean is presumed. This argument controls infinity entirely by the proved resistance and core closure. In fact the conditional current's pointwise value near z=0 need not vanish in the far y tail; requiring that would be unnecessary and unjustified.

The bounded scalar transition trial h=1 on A, h(y)=R^-1 int_y^b q^-1 on S, and h=0 on B has E(h,h)=1/(beta R). It belongs to the killed form domain. To check noncompactness explicitly, multiply by smooth full-state radius cutoffs with derivative O(1/L). The cutoff-gradient energy is bounded by a fixed-model constant times L^-2 int rho, while the omitted h-gradient tail vanishes by integrability. L2 convergence follows from finite mass. The matching h trace is continuous at -b, and its zero trace at b permits the usual boundary-layer approximation; its linear vanishing there makes that layer's energy error vanish. No angular tail is omitted.

This bounded trial already yields Q_A>=<1_A,h>²/E(h,h)=beta M²R. Thus the required lower mean does not even need an unbounded Poisson trial or an extra infinity assumption. At the admitted alpha>=4, the older quadratic-growth scalar Poisson trial is also L2 and finite energy, but is unnecessary for this lower bound.

## F. Separate S current and actual mean/survival join

The retained S current has zero longitudinal cumulative J_S left of the slab, J_S<=M_S on the slab, and the ordinary conditional-dilation divergence identity. It is zero outside the slab within the killed domain and has no normal source jump at -b. Its norm is at most B_S=beta M_S² R(1+C_s). This is proved independently of B_new; Q_S<=eta² B_new has not been assumed.

For each r>0, semigroup positivity gives Q_AS(r)>=0 and inverse-form Cauchy gives Q_AS(r)<=sqrt(Q_A(r)Q_S(r)). The killed-process identity is

    M E_A int_0^tau_B exp(-rt)dt = Q_A(r)+Q_AS(r).

Only after the two finite current energies have been proved does monotone convergence give finite actual mean and

    beta M R <= E_A tau_B <= [B_new+sqrt(B_new B_S)]/M.

Since B_S=eta² M T0(1+C_s), ordinary AM-GM yields (15) exactly. Positivity, the bounded h trial, and the separately reviewed inverse-form spectral theorem similarly yield the defect `(sqrt(b_new)+eta sqrt(1+C_s))²-1`. Its conservative upper (16) is valid because the difference is eta(sqrt(b_new)-sqrt(1+C_s))²>=0. The full exact Gibbs|A initialization comparison is still required and unchanged. The old wrapper's shared-source formula cannot be reused silently.

## G. Uniform arbitrary-angular theorem

The extended class permits any finite homogeneous quartic polynomial satisfying U>=d_0||z||^4/m, not just positive mixed coefficients. Every argument above uses only smoothness, Euler homogeneity, that coercivity floor and M_z>=mu I. The process for each member is globally received. Its finite inequalities share constants depending only on fixed beta,kappa,d_0,mu and alpha. No uniform upper bound on coefficients, angular Hessian, condition number, partition or pathwise convergence is needed. The inverse-mobility norm is favorable to matrices above the floor even if their largest eigenvalue is arbitrarily large.

The whole-basin Laplace limit is valid, not just local heuristic. With x=sqrt(alpha)(y-1), the pointwise integrand tends to exp(-4kappa x²). For y>=1/2,

    v(y)>=1+(9kappa/4)(y-1)².

For alpha>=4, monotonicity of (1+t/alpha)^alpha yields the integrable global majorant [1+(9kappa/16)x²]^-4. Thus sqrt(alpha)M_alpha tends to sqrt(pi)/(2sqrt(kappa)) over the entire infinite basin.

On the slab write u=(kappa/V)(2y²-y⁴). Then 0<=u<=7kappa/(16V)<7/16 and u>=[7kappa/(4V)]y². For R/V^alpha, (1-u)^alpha has a fixed Gaussian majorant after x=sqrt(alpha)y. For R_plus/V^alpha, (1+u)^-alpha has another one using log(1+u)>=u/(1+u_max). Both converge to exp[-(2kappa/V)x²]. Dominated convergence gives both remaining limits (2), their ratio tending to one, and the stated leading scalar time constant beta*pi*sqrt(V)/(2sqrt(2)kappa).

The residual terms in B_new/(beta M_alpha²R_alpha) are nonnegative. The near-well term is O(sqrt(alpha)(G_b/V)^alpha). The combined middle/vertical term is O(alpha^(5/2)(G_1/V)^alpha): the middle coefficient is O(1), the transverse coefficient O(alpha), and 1/(M²R)=O(alpha^(3/2)V^-alpha). The far term is O(sqrt(alpha)V^-alpha). Here G_b/V<1, G_1/V<1, V>1 for every fixed kappa>0. The constants depend only on the fixed floors. Also eta<=a_b^-alpha/M=O(sqrt(alpha)a_b^-alpha). Thus the mean upper and lower squeeze gives the first uniform supremum limit, and the independent spectral/current error plus initial-law comparison gives the second, uniformly for all scaled times s>=0.

This is not an inference of mean convergence from uniform CDF convergence: the actual means were separately bounded. It is not uniform in mu down to zero at a fixed alpha; fixed positive mu is part of the theorem. It is not a claim that different finite-dimensional models have identical exact laws.

For each fixed alpha, scalar tail test functions psi(-y/L) have full-state norm of order L^(1-4alpha) and energy of order L^(-1-4alpha). They are admitted by the same cutoff argument. The killed Rayleigh quotient therefore vanishes like L^-2. For the global Poincare quotient, subtracting the mean changes the norm only by a vanishing relative term O(L^(1-4alpha)). Both gaps are zero. This is compatible with source-specific finite inverse forms and the task-specific spectral approximation.

## H. Optional first correction is a witness upper bound only

Set c=2kappa/V and d=kappa/V. The local logarithms have quartic coefficients A_minus=d-c²/2 for R and A_plus=d+c²/2 for R_plus. After y=x/sqrt(alpha), on |x|<=alpha^(1/12), analyticity and exponential Taylor remainder give an error bounded by C_kappa alpha^-2(x^6+x^8)exp(-cx²). The scaled correction is uniformly small there. Outside this growing interval, the previously proved Gaussian dominators make both integrals, and the approximation's Gaussian polynomial tails, smaller than every inverse power of alpha.

The Gaussian fourth-moment ratio is 3/(4c²). Consequently the two rescaled integrals have relative correction 3A_minus/(4c²alpha) and 3A_plus/(4c²alpha), respectively. Division yields R_plus/R=1+3/(4alpha)+O_kappa(alpha^-2). Adding the exponentially small positive current/initialization corrections supplies a uniform upper error with limsup alpha times the error no greater than 3/4. It does not identify the true kinetic error or prove current optimality, and no effective finite remainder constant has been acquired by this asymptotic argument.

## I. Preservation, checks and limits

The independent script here passed 850 exact assertions: homogeneous/density/divergence identities, inverse-mobility constant, profile/cumulative-tail/128/16 constants, separate-source and normalization algebra, Gaussian coefficients and dominant-function identities, rational parameter fixtures, and all four source/freeze hashes. Fixtures supplement the global proofs; they do not replace them. No candidate code was imported.

The conclusions are mathematical predictions for the declared complete model and exact full Gibbs|A law. They do not supply physical parameter inference, finite-bit or fixed-ray initialization, hardware control, empirical model membership, relative extreme-tail accuracy, exponential moments, or arbitrary-start laws. The optional scalar asymptotic is not a finite-tolerance certificate. Ordinary homogeneous scaling, variational currents, Laplace asymptotics and spectral-mixture principles remain strong prior methods; no historical priority or generic algorithmic separation is accepted.
