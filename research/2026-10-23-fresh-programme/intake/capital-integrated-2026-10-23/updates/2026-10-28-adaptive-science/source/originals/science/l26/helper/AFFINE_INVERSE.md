# Scalar affine Newton inverse: sharp source reserve and acquired random action

Derived independently for the authorised l26 helper. The governing Newton identity is frozen S3 Sections 17–18. All mathematical statements below concern that scalar affine interface; they do not assume a residual-value oracle is supplied by the original g-value model.

Let 0<|kappa|<1, a=sqrt(1-kappa²), and let G,Z be independent standard Gaussians. Set h(G)=kappa G, K=kappa, psi=aZ, Jpsi=a. Then X=kappa G+aZ is exactly standard Gaussian. Write delta_Z=Z-partial_Z and use the normalized probabilists' Hermite basis e_n=He_n/sqrt(n!). We seek u,J with delta_Z J=u and

    L(u,J)=kappa partial_G u+a partial_Z u+aJ=R.

The requested correction for residual R has the opposite sign. Conditional centering E_Z u=0 is automatic for an L2 divergence.

## 1. Exact inversion and genuine unboundedness

Eliminating u gives

    T J = R,       T=a(N_Z+2)+kappa a_Z^dagger a_G,

where a_G=partial_G, a_Z=partial_Z, a_Z^dagger=delta_Z and N_Z=delta_Z partial_Z. Both terms preserve total (G,Z) Hermite degree. On total degree n, in the ordered basis e_(n-j)(G)e_j(Z), 0<=j<=n, T has diagonal a(j+2) and subdiagonal kappa sqrt((n-j+1)j). Every sector is therefore invertible.

For R=e_n(G), the unique polynomial solution has coefficients

    J=sum_(j=0)^n [(-kappa/a)^j sqrt(binomial(n,j)) /
                  (a(j+1)(j+2))] e_(n-j)(G)e_j(Z).       (1)

This is also the unique Gaussian L2 weak solution. Indeed, pairing a weak solution with finite Hermite tests determines its projection onto each total-degree sector, and every sector matrix is invertible. A nonpolynomial L2 homogeneous solution cannot be added.

Since 1+(kappa/a)²=a^(-2), formula (1) gives the exact bounds

    ||J||_2 >= a^(-n-1)/(n+2)²,
    ||partial_Z u||_2 >= a^(-n-1)/(n+2).                (2)

Thus no uniformly bounded L2 right inverse exists for arbitrary residuals, even though the underlying source is a globally Lipschitz conservative affine field and the baseline output is already an exact Gaussian. This rejects an unrestricted residual-inverse claim, not the Gaussian-mean sampling target: the actual residual of this affine baseline is zero.

## 2. Sharp source-only smoothing threshold

Let P_rho^G multiply source Hermite degree k by rho^k, leaving the Z degree unchanged. Put r=kappa/a. On finite polynomials,

    T^(-1) P_rho^G
      = integral_0^infinity exp(-2at) Gamma(S_t diag(rho,1)) dt,
    S_t=[[1,0],[-r(1-exp(-at)),exp(-at)]].               (3)

Here Gamma(B) is Gaussian second quantization: if ||B||<=1,

    [Gamma(B)f](x)=E f(B^T x+(I-B^TB)^(1/2)W).           (4)

The matrix orientation in (4) is important: on linear coefficients v, this sends v to Bv. For q=exp(-at), direct 2x2 algebra shows S_t diag(rho,1) is a contraction for every t>=0 exactly when rho<=a. Therefore

    ||T^(-1)P_rho^G R||_2 <= ||R||_2/(2a),   rho<=a.   (5)

Finite polynomials are dense; (5) gives a bounded extension. The equation T J=P_rho R holds in the closure of the differential operator on Gaussian L2, since both the solutions and right sides of polynomial approximations converge. Conversely (2), multiplied by rho^n, proves unboundedness for every rho>a. Hence a is the exact source-only smoothing threshold for J.

At the critical value rho=a, define

    B_q=[[a,0],[-kappa(1-q),q]],  0<q<1.

Then

    J=(1/a) integral_0^1 q Gamma(B_q)R dq.              (6)

This consumes one explicit source smoothing P_a: it solves T J=P_a^G R, not T J=R.

## 3. Derivative bounds at the critical threshold

Let C0=4+2sqrt(2)/3. The following rough constants are degree independent:

    ||J||_2 <= ||R||_2/(2a),
    ||partial_G u||_2 <= C0 ||R||_2/(a |kappa|),
    ||partial_Z u||_2 <= (1/a+C0/a²)||R||_2.           (7)

In particular the coupled derivative kappa partial_G u is bounded even as kappa decreases to zero. At kappa=0 one uses the ordinary diagonal inverse directly.

Proof. One has

    I-B_q B_q^T >= diag(kappa² q/2, q(1-q)/2).          (8)

To verify (8), the remaining matrix has first diagonal kappa²(1-q/2), second diagonal (1-q)[a²+(kappa²+1/2)q], and determinant

    kappa²(1-q)q [a²/2+(kappa²+1/2)(1-q/2)] >=0.

Factor B_q=D_q C_q with C_q a contraction and D_q the diagonal Gaussian damping supplied by (8). The Hermite bounds ||partial Gamma(s)||<=1/sqrt(1-s²) give

    ||a_G Gamma(B_q)|| <= sqrt(2)/(|kappa|sqrt(q)),
    ||a_Z a_G Gamma(B_q)|| <=2/(|kappa|q sqrt(1-q)).

Since ||a_Z^dagger v||²=||a_Zv||²+||v||², integrating (6) yields the second line of (7). Finally T J=P_a R implies

    (N_Z+1)J = [(N_Z+1)/(N_Z+2)]
                  [P_a R-kappa a_Z^dagger a_G J]/a.

The multiplier has norm at most one, partial_Z u=(N_Z+1)J, and partial_Gu=a_Z^dagger a_GJ. This proves the final bound. Also ||u||_2<=||partial_Zu||_2 because every component of u has Z degree at least one.

## 4. One residual-value implementation of the correction action

Formula (6) is not confined to a derivative oracle. Let q have Beta(3/2,1/2) density

    p(q)=(2/pi)sqrt(q/(1-q)),   0<q<1.

It is generated exactly by q=(A1²+A2²+A3²)/(A1²+A2²+A3²+A4²) with independent scalar Gaussian A_i. Draw independent W1,W2 and define

    Y_Z=q Z+sqrt(1-q²) W1,
    Y_G=aG-kappa(1-q)Z
          +kappa q sqrt((1-q)/(1+q)) W1
          +kappa sqrt(2q/(1+q)) W2,
    V=sqrt(2q(1-q)) Z
          -sqrt(2)q sqrt(q/(1+q)) W1
          +sqrt((1-q)/(1+q)) W2.

Return the actual random correction

    Uhat=pi/(2sqrt(2)a) V R(Y_G,Y_Z).                  (9)

This uses one evaluation of R and Gaussian seeds/arithmetic. No endpoint-singular numerical weight appears. For each fixed q, the vector (Y_G,Y_Z,V) is exactly three independent standard Gaussians: direct covariance calculation gives identity covariance. Thus q is independent of this product marginal. For every finite p>=1,

    ||Uhat||_p = pi/(2sqrt(2)a) ||N(0,1)||_p ||R||_p.  (10)

In particular

    E[Uhat|G,Z]=u,
    E Uhat²=pi² ||R||_2²/(8a²).                       (11)

Proof of conditional unbiasedness. In the Mehler kernel (4), conditional on G,Z the residual query Y has mean B_q^T(G,Z) and covariance I-B_q^TB_q. Its Gaussian score for differentiation with respect to Z is

    S=q/sqrt(1-q²) W1 -1/sqrt(2q(1+q)) W2.

Therefore delta_Z Gamma(B_q)R=E[(Z-S)R(Y)|G,Z]. This is first valid for smooth polynomials and extends to L2 by the bounds above. Since V=sqrt(2q(1-q))(Z-S), importance weighting the q integral in (6) with p(q) gives (9). The product-Gaussian covariance calculation proves (10) without any unjustified independence from the original outer G,Z.

The conditional mean in (11) is analysis of the actual finite program (9); it is not supplied runtime data. The implemented correction has nonzero randomness, and a nonlinear law update must charge it.

## 5. Quadratic full-law cost of randomizing the correction

Let X be any random variable measurable in the outer G,Z. Let u=E[Uhat|G,Z], and let N be a fresh independent standard Gaussian. For every tau>0,

    TV(Law(X+Uhat+tau N), Law(X+u+tau N))
      <= phi(1) E[(Uhat-u)²]/tau²
      <= phi(1)pi² ||R||_2²/(8a²tau²).               (12)

Here phi(1)=exp(-1/2)/sqrt(2pi). This is a full marginal-law bound, not a moment or KS diagnostic.

Proof. Conditional on the outer variables, Delta=Uhat-u has mean zero. The first derivative of the Gaussian density in the shift therefore cancels. Taylor's integral remainder and translation invariance give

    ||E phi_tau(. -Delta)-phi_tau||_1
      <= E Delta² ||phi_tau''||_1/2.

Since ||phi_tau''||_1=E|N²-1|/tau²=4phi(1)/tau², the TV factor 1/2 proves (12). The same argument in any dimension gives this constant times E||Delta||²/tau² by using the directional Gaussian Hessian. The independent reserve consumes actual target variance.

## 6. Scientific boundary

The unsmoothed full linearization genuinely has no bounded L2 inverse on arbitrary residuals. Explicit source smoothing restores the scalar inverse at a sharp threshold and supports a finite one-residual-value random correction with an exact second-moment receipt. A charged fresh Gaussian reserve makes the randomization error quadratic in the residual L2 norm.

This does not construct the original N687 sampler. The supplied value access is to g, not R. The actual nonlinear residual need not have an acquired representation P_a R with controlled R norm. The nonlinear inverse, repeated smoothing reserves, common-source correlations, query-tree costs and target-noise allocation are still load-bearing. No priority or practical-advantage claim is made. The result strengthens the affine analytical/acquisition interface beyond merely noting an unbounded source derivative; it does not reject adaptive g-value algorithms or establish a target lower bound.

Finite Hermite-sector checks and covariance tests are in check_affine_inverse.py and affine_inverse_checks.csv. They verify the displayed finite formulas and implementation algebra; the proofs above establish the infinite-dimensional claims.
