# A source-smoothed full Stein inverse with a finite random action

This is an internal mathematical construction for the N687 opening in frozen S3 Sections 17–18. It is not the requested g-only polylogarithmic sampler. The sharp scalar inverse was independently derived by the authorised helper; the vector gauge and integration below are the main trajectory's construction. Gaussian second quantization, Hermite calculus, and Gaussian density Taylor bounds are standard instruments. External priority has not been established.

## 1. Statement, with the actual access boundary

Fix any physical dimension d, 0<kappa<1, and a=sqrt(1-kappa²). On independent standard Gaussian G,Z in R^d consider the exact affine Gaussian source

    h(G)=kappa G, K=kappa I, psi=aZ, Jpsi=aI,
    X=kappa G+aZ ~ N(0,I).

For a symmetric matrix field R in L2(gamma_(2d); Frobenius), let P_a^G be source-only Gaussian OU smoothing. There exist u and J such that

    delta_Z J=u,                    E_Z u=0,
    sym[kappa(D_G u)^T+a(D_Z u)^T+aJ] = -P_a^G R.       (1)

The norms ||u||_2, ||D_Zu||_2, ||kappa D_Gu||_2, and ||J||_2 have bounds depending on kappa,a but on neither d nor chaos degree. The smoothing is explicit and cannot be deleted: even in d=1 the unsmoothed inverse is unbounded on L2. Source-only P_rho restores bounded inversion precisely when rho<=a in that scalar problem.

More than an existence inverse is available. One conditional-unbiased action for u uses one value of R applied to a Gaussian vector, a fixed number of Gaussian vectors/scalars, and O(d) surrounding vector arithmetic. If a full R matrix is returned, its multiplication costs O(d²). The program has no random loop or unbounded query count. Its exact second moment is

    E||Uhat||² = pi²/(8a²) E||R(G,Z)||_F².              (2)

If ||R||op<=b everywhere, Uhat is convex-order dominated by N(0,pi² b²/(8a²) I). An unbiased noisy action A(y;v) can replace the R(y)v evaluation: the conditional mean remains u, and the actual action's second moment must replace the right side of (2).

The original oracle supplies g values, not R values or actions. This distinction is load-bearing. In particular, raw Dg at an acquired point is not a free value-query action. Frozen S4 gives exact bounded actions for smoothed heat Hessians and Stein resolvents; obtaining the complete nonlinear residual from those actions is a remaining task.

## 2. The finite positive program

Draw four independent scalar standard Gaussians A1,...,A4 and set

    q=(A1²+A2²+A3²)/(A1²+A2²+A3²+A4²).

Thus q~Beta(3/2,1/2). Draw independent W1,W2~N(0,I_d), independent of outer G,Z and q. Define

    Y_Z=q Z+sqrt(1-q²) W1,
    Y_G=aG-kappa(1-q)Z
          +kappa q sqrt((1-q)/(1+q))W1
          +kappa sqrt(2q/(1+q))W2,
    V=sqrt(2q(1-q))Z
          -sqrt(2)q sqrt(q/(1+q))W1
          +sqrt((1-q)/(1+q))W2.

Return

    Uhat=-pi/(2sqrt(2)a) R(Y_G,Y_Z)V.                  (3)

Assign a fixed value on the zero-probability zero-denominator event. All coefficients are bounded for q in [0,1]; no reciprocal endpoint weight occurs in the executed program.

For every fixed q, (Y_G,Y_Z,V) consists of three independent standard Gaussian d-vectors. This follows by checking the 3-by-3 scalar coefficient Gram matrix, separately on every physical coordinate. Consequently V is independent of the actual residual query point, and (2) follows exactly. This independence is not asserted relative to the original outer G,Z.

Let

    B_q = [[aI,0],[-kappa(1-q)I,qI]],
    [Gamma(B)f](x)=E f(B^T x+(I-B^TB)^(1/2)W).

B_q is a contraction. Define entrywise

    J0=-(1/a) integral_0^1 q Gamma(B_q)R dq,
    u=delta_Z J0.                                     (4)

The conditional Gaussian score in the Z direction, coordinate by coordinate, is

    S=q W1/sqrt(1-q²)-W2/sqrt(2q(1+q)).

Since V=sqrt(2q(1-q))(Z-S), Gaussian integration by parts in the Mehler kernel and importance weighting the q integral prove

    E[Uhat|G,Z]=u.                                     (5)

The first proof is on finite polynomials. The L2 bounds below and (2) extend (5) to every R in the stated space. Conditional expectation in (5) is analysis of the finite program, not runtime oracle data.

## 3. Why this gives the full vector linearization

Write N=N_Z=delta_Z grad_Z and C=delta_Z dot grad_G. The entrywise resolvent in (4) satisfies

    [a(N+2)+kappa C]J0=-P_a^G R.                       (6)

This is second quantization of the two-by-two one-particle matrix. It holds componentwise for an arbitrary matrix field, not just scalar diagonal residuals.

The useful gauge choice is u=delta_Z J0. Requiring u to be a Z-gradient is unnecessary. Commuting Gaussian creation operators gives

    [a(N+1)+kappa C]u=-delta_Z P_a R,
    [aN+kappa C]delta_Zu=-delta_Zdelta_Z P_a R.         (7)

Set

    F=P_a R+sym[kappa(D_Gu)^T+a(D_Zu)^T+aJ0].

Then delta_Zdelta_Z F=0. Indeed

    delta delta (D_Zu)^T=(N-1)delta u,
    delta delta (D_Gu)^T=C delta u,

and (7) cancels the remaining term. For each Z-chaos-m component F_m, put

    w_m=delta_Z F_m,
    B_m=[D_Z w_m-(D_Z w_m)^T]/(m+2),
    Q_m=-F_m+B_m.

Since delta w_m=0, Gaussian Hodge algebra gives delta B_m=w_m. Therefore

    delta Q_m=0,               sym Q_m=-F_m.

Finally set J=J0+(sum_m Q_m)/a. Its divergence remains u and (1) follows pointwise in Gaussian L2. The divergence-free gauge is essential: J0 alone generally fails the matrix equation, although its row divergence is the useful acquired correction.

## 4. Dimension- and degree-independent estimates

Mehler contraction gives ||J0||_2<=||R||_2/(2a). The explicit program gives

    ||u||_2<=pi ||R||_2/(2sqrt(2)a).

Put C0=4+2sqrt(2)/3. The scalar two-by-two covariance inequality

    I-B_q B_q^T >= diag(kappa²q/2, q(1-q)/2) tensor I_d

and Gaussian number-operator estimates imply

    ||D_G Gamma(B_q)|| <= sqrt(2)/(kappa sqrt(q)),
    ||D_ZD_G Gamma(B_q)|| <=2/(kappa q sqrt(1-q)).

These are total Frobenius derivative norms as L2 operators; no sum over physical coordinates is hidden. Gaussian row divergence obeys

    ||delta V||_2²<=||V||_2²+||DV||_2².

Applying this after the displayed derivative bounds and integrating (4) gives

    ||D_Gu||_2 <= C0 ||R||_2/(a kappa),
    ||D_Zu||_2 <= (1/a+C0/a²)||R||_2.                 (8)

For the second estimate, use (6) to bound (N+1)J0, whose norm dominates D_Zdelta_ZJ0. The transfer C J0 is bounded by the same two derivative estimates used in the first line. These arguments apply to tensor-valued fields with the matrix Frobenius norm.

The zero-double-divergence Hodge gauge has ||Q||_2<=(1+sqrt(2))||F||_2. Hence

    ||J||_2 <= ||R||_2/(2a)+(1+sqrt(2))||F||_2/a,
    ||F||_2 <= ||R||_2+kappa||D_Gu||_2
                         +a||D_Zu||_2+a||J0||_2.

This completes a controlled full linear inverse at the affine reference. Separate L2 estimates do not bound the nonlinear Newton product in L2, but they do bound it in L1. Section 8 shows that this is already enough for a full-law estimate after a charged Gaussian reserve.

## 5. Full marginal-law accounting for the random correction

Let X be any R^d-valued measurable function of the outer G,Z. Let u=E[Uhat|G,Z] and add a fresh independent reserve tau N_d, tau>0. Then

    TV(Law(X+Uhat+tau N_d), Law(X+u+tau N_d))
      <= phi(1) E||Uhat-u||²/tau²
      <= phi(1)pi² ||R||_2²/(8a²tau²).                (9)

Here phi(1)=exp(-1/2)/sqrt(2pi). Conditional on the outer variables, Delta=Uhat-u has mean zero. Taylor expansion of the Gaussian density in the direction Delta cancels its first derivative. The directional second derivative has L1 norm 4phi(1)||Delta||²/tau². Taylor's 1/2 and TV's 1/2 give (9). This proof is global in the marginal law and all dimensions.

The positive update X -> X+Uhat+tau N_d therefore has a rigorous quadratic randomization cost. It is not a quadratic correction theorem for the full incoming law: the deterministic inverse must cancel the actual nonlinear residual, its nonlinear products need bounds, and the reserve consumes target variance. Mean preservation holds because E Uhat=E u=0.

## 6. Sharp instability and a genuine conservative counterfamily

In d=1 the unsmoothed affine inverse reduces to

    T J=R,   T=a(N_Z+2)+kappa delta_Z partial_G.

For R=e_n(G), normalized Hermite polynomial, its unique L2 weak solution is

    J=sum_(j=0)^n (-kappa/a)^j sqrt(binomial(n,j))
                   e_(n-j)(G)e_j(Z)/[a(j+1)(j+2)].     (10)

Different total-chaos sectors are orthogonal and each finite sector is invertible. Thus adding a nonpolynomial L2 kernel cannot repair the growth. Formula (10) gives

    ||J||_2>=a^(-n-1)/(n+2)²,
    ||partial_Zu||_2>=a^(-n-1)/(n+2).

Multiplying by source factor rho^n shows unboundedness for every rho>a. Conversely the Mehler contraction above proves boundedness for rho<=a. This establishes the exact scalar source-only smoothing threshold.

The forcing is not restricted to arbitrary synthetic residuals. Fix kappa,delta>0 with kappa+delta<1 and define

    g_k(x)=kappa x+delta sin(kx)/k,
    F_k(x)=kappa x²/2-delta cos(kx)/k².

These are smooth globally (kappa+delta)-Lipschitz conservative fields with Gaussian mean zero. The canonical Stein kernel is

    K_k(x)=kappa+delta Q_k(x),
    Q_k(x)=integral_0^1 exp[-k²(1-t²)/2] cos(ktx)dt.

For the actual positive proposal X_k=g_k(G)+aZ the exact symmetric Stein residual is

    R_k(G)=kappa delta[cos(kG)+Q_k(G)]
                         +delta² Q_k(G)cos(kG).       (11)

The residual norms are uniformly bounded by 2kappa delta+delta². Every even Hermite coefficient in (11) has the same alternating sign: Q_k is a positive cosine mixture and its product with cos(kG) is a positive mixture of cos(k(1+t)G),cos(k(1-t)G). Consequently its coefficient magnitude dominates kappa delta times that of cos(kG).

Let lambda=k²/a²>=16. Applying the unsmoothed affine preconditioner to the actual residual (11) therefore satisfies

    ||J_k||_2 >= (kappa delta/a)
           exp[kappa² k²/(2a²)]/[2(2lambda+2)²].       (12)

Proof: sum (10)'s squared lower bound over even degrees; the resulting series is exp(lambda-k²)/a² times E[1_(N even)/(N+2)^4], N~Poisson(lambda). The event N even and |N-lambda|<=lambda/2 has probability at least 1/2-4/lambda>=1/4. This gives (12).

Thus a family arbitrarily close in source values to an affine field can drive this unsmoothed pointwise preconditioner exponentially large. This is a counterfamily to that preconditioner and its unrestricted L2 certificate. It is not a lower bound for the original active g-value sampling task, nor a proof that the full nonlinear linearization at X_k has the same inverse.

## 7. What this changes and what it leaves open

The source derivative in frozen S3 is a real inverse obstruction, not merely a failed Neumann estimate. An explicit source reserve closes the entire affine analytical inverse; a simpler divergence choice plus a skew gauge makes its correction accessible by a single residual action in every dimension. Randomization has an exact quadratic full-law receipt after a charged reserve.

The next consequential construction is a source-smoothed residual action for the actual nonlinear program, together with a controlled nonlinear inverse or a law-level treatment of the unsmoothed remainder. A formal assumption R=P_a R0 with bounded R0 would put the hard source-acquisition step into an oracle. Repeated reserve losses, Lp products, source retention, all original g-query counts, deterministic caps, and polynomial arithmetic must be proved for the actual compiler. The N687 target remains open.

## 8. A quantitative positive nonlinear step under explicit inputs

The preceding inverse can be integrated with the exact Newton identity, rather than stopping at formal cancellation. This theorem spells out its unsupplied inputs.

Suppose an actual program has X=h(G)+psi(G,Z) in L2, E_Z psi=0, with valid Stein data

    delta_G K=h-mu,       delta_Z Jpsi=psi,
    T_X=K(D_GX)^T+Jpsi(D_ZX)^T.

Assume all identities admit Gaussian integration by parts, and put R_X=sym T_X-I. Suppose one has a declared residual action R0(y)v with

    R_X=P_a^G R0,       r=||R0||_(L2,F)<infinity,       (13)

and the actual coefficient deviations satisfy the L2 operator-norm bound

    max(||K-kappa I||_(L2,op), ||Jpsi-aI||_(L2,op),
                            ||D_ZX-aI||_(L2,op))<=eta. (14)

Apply (3) to R0, and use its deterministic conditional mean u and the full inverse J only for analysis. The implemented positive update is

    Xplus = X+Uhat+tau N_d.                            (15)

It uses one R0 action and fresh Gaussians in addition to the actual X program. No conditional expectation, derivative, J, or mean is evaluated at runtime.

Define the explicit constants

    c=pi/(2sqrt(2)a),
    dG=C0/(a kappa),    dZ=1/a+C0/a²,
    j0=1/(2a),
    j=j0+(1+sqrt(2))[1+kappa dG+a dZ+a j0]/a,
    A=dG+dZ+j,         B=j dZ,
    H(tau)=log(1+tau^(-2))/sqrt(2).

Then the actual implemented marginal satisfies

    TV(Law(Xplus),N(mu,(1+tau²)I))
      <= H(tau)[A eta r+B r²]+phi(1)c²r²/tau².        (16)

In particular, if the coefficient deviations eta are at most C r, the bound is quadratic in r, with no hidden factor d. The dimension still enters r when the residual's Frobenius energy scales with d. The theorem does not supply that smallness relation, the preimage in (13), or its action cost.

Proof. The exact Newton identity from frozen S3 gives, for Y=X+u,

    R_Y=R_X+L_X(u,J)+sym[J(D_Zu)^T].

Equation (1) cancels R_X using (13). The remaining linear terms have the three coefficient differences in (14). Cauchy–Schwarz includes their actual correlations with the correction. Hence

    E||R_Y||F <= eta(||D_Gu||2+||D_Zu||2+||J||2)
                          +||J||2||D_Zu||2
                <= A eta r+B r².                    (17)

There is no need to assert an L2 bound for the product in the last line.

For completeness, a mean-mu vector Y with a valid Stein matrix of symmetric residual S obeys the Gaussian-reserve inequality

    TV(Law(Y+tau N_d),N(mu,(1+tau²)I))
                      <=H(tau) E||S||F.              (18)

To prove it, translate mu to zero and test a bounded |f|<=1. Set f_tau(x)=E f(x+tau N_d). In the standard Gaussian OU Stein-Poisson solution, the Hessian at OU time t has Frobenius norm at most

    sqrt(2) exp(-2t)/(tau²+1-exp(-2t)).

Gaussian degree-two Bessel inequality gives this bound without a dimension factor. Its time integral is H(tau). Apply the scalar Stein identity, and use the TV test convention (or simply the conservative constant in (18)). Combining (17), (18), and the randomization bound (9) proves (16).

All nonlinear correlations involving the new random correction are accounted for in (9). They are not replaced by their means inside a nonlinear Stein calculation. The reserve covariance in (15) is part of the displayed target, not free noise. An iteration targeting a fixed final sigma must allocate that covariance explicitly.

This is a conditional positive nonlinear law-update theorem with finite residual-action access. It is stronger than a formal cubic/Newton identity. It is not an acquired g-only N687 compiler: producing (13) from legal g values and maintaining (14) through actual updates are the decisive missing constructions.

In particular eta need not shrink with the incoming residual r after a first update. Keeping this fixed affine inverse may then yield only an eta*r term, not quadratic convergence in r. A full current-law inverse, a controlled Neumann chain, or a different representation is still required for repeated quadratic updates. No log-log depth claim is made from (16) alone.
