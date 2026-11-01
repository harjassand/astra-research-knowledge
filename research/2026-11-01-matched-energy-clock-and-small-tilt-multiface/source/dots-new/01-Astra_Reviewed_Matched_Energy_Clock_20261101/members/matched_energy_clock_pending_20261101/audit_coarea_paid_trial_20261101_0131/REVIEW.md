# Independent paid energy-sensitive trial/coarea/source review

## Verdict and exact boundary

**PASS for the exact mathematical identities and source/current bounds below, with the controlling diagnostic scope qualifications in Section 7.** This is not acceptance of a completed matched primal/dual clock receiver or a numerical accuracy improvement.

Exact frozen sources, read in full and unchanged:

- `FROZEN_FIBER_VARIATIONAL_ROOT.md`: `2e04fd5ddb5b2f8742a1f608f81144355d94d71c43c50232b783ef86a9362fa8`.
- `COAREA_DERIVATIVE_PRICE_ROOT.md`: `6e5cc8f88c5b2b38834363d804a003731ef1a6c7aeb635cc60b50393a498c103`.
- `ODD_SLAB_SOURCE_ROOT.md`: `175528f879cbd16aa84a5f4f6c90021a43e994063390b8dd49477cc4a68d465f`.

Use the already received original reversible constant-block-mobility model F(y,z)=v(y)U(z), D_full=diag(1,M_z), v=1+kappa(1-y²)², beta,kappa>0, m=4alpha with admitted integer alpha>=4. The coarea identity itself holds more generally for smooth positive coercive homogeneous quartics and constant SPD transverse matrices. The explicit pair-program coefficient price requires diagonal transverse mobility. These statements do not automatically transfer to nonfactorized uncertain potentials, state-dependent mobility, cross mobility or nonzero processing.

## 1. Coarea, Gauss and the shell conditional identity

For positive energy u, Euler gives z.grad U=4U, so grad U cannot vanish on U=u. Coercivity makes each sublevel bounded, and smoothness makes the positive-level boundary smooth and compact. There is no singular inner boundary at the origin. Let

    C(u)=int_(U=u) |grad U|^-1 dS,
    A(u)=int_(U=u) grad U^T D grad U /|grad U| dS,
    B(u)=int_(U=u) tr(D Hess U)/|grad U| dS.

The normalized geometric shell measure is C(u)^-1 |grad U|^-1 dS. It is also the conditional angular measure under any density that is a function of U alone; no angular equilibration, dynamical Markov closure or sampler is presumed.

Under z=u^(1/4)xi, surface measure scales as u^((m-1)/4), the gradient as u^(3/4), and the Hessian as u^(1/2). Consequently

    C(u)=C(1)u^(alpha-1),
    B(u)=B(1)u^(alpha-1/2),
    A(u)=A(1)u^(alpha+1/2).

The divergence theorem gives A(u)=int_(U<=u) tr(D Hess U) dz. Coarea and the integrability of v^(alpha-1/2) at zero then yield

    A(u)=int_0^u B(v)dv=u B(u)/(alpha+1/2).

For nonconvex U, the pointwise trace need not be positive; the bounded-sublevel coarea step is still justified by absolute integrability, and the resulting B(u) is positive because A(u)>0. Dividing by C(u) proves the stated exact conditional expectation identity. This is a geometric identity, not a replacement of the actual generator by a frozen-fiber process.

## 2. Normalization, beta and Gamma factors

The formulas use the inherited common scale

    w(y,z)=exp[-beta v(y)U(z)]/Z_beta,
    Z_beta=int exp(-beta U(z))dz.

Coarea gives Z_beta=C(1)Gamma(alpha)/beta^alpha. Thus any radial transverse integral divided by Z_beta has prefactor beta^alpha/Gamma(alpha). A Dirichlet factor beta^-1 changes this to **beta^(alpha-1)/Gamma(alpha)**. If one instead uses the fully normalized invariant probability, every energy must additionally be divided by Ztot; mixing the two normalizations is invalid.

For the displayed h_u, partial_y h_u=-exp(beta u v(y))/I(u) on the slab, and the derivative vanishes off it. The exact longitudinal energy is therefore

    C_frozen=beta^(alpha-1)/Gamma(alpha)
             *int_0^infinity u^(alpha-1)/I(u) du.

The integration in y reduces the square to 1/I(u). This verifies all beta/Gamma factors. It is the energy obtained by longitudinal minimization separately at each frozen z, not the full actual energy. In the actual block-mobility model,

    E(h,h)=C_frozen+C_trans,
    C_trans=beta^-1 int_S int |partial_u h_u(y)|²
                    grad U^T M_z grad U w dz dy.

The extra term is nonnegative and fully charged. The model is not altered to freeze z. As an ordinary variational observation, C_frozen<=C0, and indeed it is a lower bound on the full capacity whereas this complete trial energy is an upper bound; neither observation identifies the actual passage mean or a global inverse form.

## 3. Pair-quartic trace coefficients and the correct mobility scope

For the complete pair program U=sum d_i z_i^4+sum_(i,j) g_ij z_i²z_j² and **diagonal** M_z=diag(mu_i), direct differentiation gives

    tr(M_z Hess U)=sum_j c_j z_j²,
    c_j=12mu_j d_j+2 sum_(i:ij edge) mu_i g_ij.

Each literal edge contributes to the opposite coordinate with the stated factor two. Since U>=dmin sum z_j^4, Cauchy gives

    tr(M_z Hess U)<=||c||_2 sqrt(U/dmin).

The c vector depends on actual positive mobility entries and all actual coefficients, not merely a lower mobility floor. For unit pure coefficients, unit mobility and an open path with edge coupling 20, c=52 at each endpoint and 92 at interior sites. At m=512, ||c||²=2*52²+510*92²=4,322,048. This is an exact datum for that declared structure, not a new complete finite receiver.

The shell identity allows arbitrary constant SPD D, but this diagonal coefficient formula cannot silently be used for a full matrix. An off-diagonal D_ij contributes 8D_ij g_ij z_i z_j to the trace. This is a genuine restriction, not cosmetic: with U=(z1²+z2²)²+sum_(3..16) z_i^4, the first 2x2 mobility block [[1,0.9],[0.9,1]], and remaining diagonal entries 0.001, the diagonal-only proposed price at z1=z2=1, others zero is too small. The true trace is 232/5, while the squared omitted-cross bound is 4[2*16²+14*(12/1000)²]<(232/5)². The full matrix is SPD. The exact coarea identity remains true if its full trace is used; only the diagonal shortcut fails.

## 4. Exact transverse scalar price and the earlier integration-by-parts route

Combining the shell identity with the trace bound gives

    E[grad U^T M_z grad U | U=u]
       <=||c||_2 u^(3/2)/[(alpha+1/2)sqrt(dmin)].

The ordinary radial weight u^(alpha-1) then becomes u^(alpha+1/2), proving the complete displayed two-dimensional scalar upper price, including the denominator alpha+1/2 and prefactor beta^(alpha-1)/Gamma(alpha). Unknown angular partition factors cancel exactly.

For fixed y, write g(u)=|partial_u h_u(y)|² and call the auxiliary integral mathcalF(u) to distinguish it from the physical potential. It satisfies beta v mathcalF-mathcalF'=g. Direct divergence gives

    div_z[mathcalF(U) D grad U exp(-beta vU)]
       =[mathcalF(U)tr(D Hess U)-g(U)grad U^T D grad U]
          exp(-beta vU).

The cutoff/tail conditions for this actual trial are earned in Section 5. Integration therefore proves the earlier exact identity, not just a formal integration by parts. For the upper trace price, Tonelli applies to nonnegative factors:

    int_0^infinity u^(alpha-1/2) exp(-a u) mathcalF(u)du
      =int_0^infinity exp(-a s)g(s)
             [int_0^s u^(alpha-1/2)du]ds
      =1/(alpha+1/2) int_0^infinity s^(alpha+1/2)g(s)exp(-a s)ds,

where a=beta v(y). This independently verifies the new denominator and exponent and removes the extra mathcalF integration. Evaluation of h_u and its u derivative still requires its I(u) and weighted cumulative integrals; they are not an uncharged oracle hidden by the phrase “two-dimensional scalar price.”

## 5. Actual trial domain, u=0 and all tails: additional receiving

Define the tilted probability on [-b,b] proportional to exp(beta u v(t)). Differentiating the finite-interval numerator/denominator gives exactly

    partial_u h_u(y)=beta Cov_tilt(1_[y,b](t),v(t)).

For an indicator of probability p and v in [v_b,v_*], the covariance magnitude is at most (v_*-v_b)p(1-p), hence at most (v_*-v_b)/4. Therefore

    |partial_u h_u(y)|<=7 beta kappa/64

for every u>=0 and y in the slab. The derivative is continuous at zero, not singular. In fact h_0(y)=1/2-y and

    partial_u h_u(y)|_(u=0)
      =beta kappa[-37y/240+(2/3)y³-y^5/5].

Both endpoint u derivatives vanish. Since U is smooth at the origin, the full composition h_{U(z)}(y) is locally regular there; grad U vanishes cubically. Its extension by one/zero is continuous at the slab boundaries with the correct Sobolev traces. Piecewise jumps in its longitudinal derivative do not invalidate form membership.

Let L=2b=1, A=v_b and G=(7 beta kappa/64)². Since I(u)>=L exp(beta A u), longitudinal integrability follows at zero from alpha>0 and at infinity from exponential decay. For the transverse upper price, g<=G and v>=A give integrable u^(alpha+1/2)exp(-beta A u). The actual admitted alpha>=4 certainly suffices. Thus the complete full Dirichlet energy is finite, not only a conditional statement pending tails. Bounded h lies in L2(w) because the actual model has finite mass; full-state cutoffs with derivative O(1/R) converge in the form norm because D is fixed finite and the just-proved derivative energy is integrable. Zero target trace then gives the appropriate killed-form membership as well. No operator-domain regularity or actual committor equation is claimed.

For the earlier integration by parts, mathcalF<=G/(beta v) and mathcalF' is bounded. Coercivity and homogeneity make the boundary flux at a transverse sphere vanish as a polynomial times exp(-c R^4); near the origin it is O(R^(m+2)). The volume terms are integrable. These facts justify the exact identity globally for the displayed trial.

Explicit analytic truncation majorants are available. With P=beta^(alpha-1)/Gamma(alpha), H=||c||_2/sqrt(dmin), lower cutoff delta and upper cutoff K, the longitudinal omitted pieces are at most

    P delta^alpha/(L alpha),
    (P/L)(beta A)^-alpha Gamma(alpha,beta A K).

The transverse scalar-upper-price omitted pieces are at most

    P H L G delta^(alpha+3/2)/[(alpha+1/2)(alpha+3/2)],
    P H L G (beta A)^-(alpha+3/2)
          Gamma(alpha+3/2,beta A K)/(alpha+1/2).

Here Gamma(a,x) is the upper incomplete gamma integral; these are analytic bounds, not a claim that its finite-bit evaluation is free. They prove finiteness and provide a receiving route. They can be too coarse to certify the desired gain; exact derivative quadrature and all numerical error still need paid outward bounds.

## 6. New energy-dependent odd residual current

The later odd-slab source is correct and closes this particular previously open source. For each fixed z, wr is odd, so its full slab integral is zero. The y primitive is continuous and has zero traces at both endpoints. Its distributional divergence is wr; no z derivative is involved because j_z=0, even though j_y depends on z.

For y<=0 use the left primitive, whose interval length is at most b; for y>=0 use the negative right-tail primitive. The stated sign/range assumptions then give 0<=j_y<=b exp(-beta v_b U)/Z_beta. Consequently

    beta int j_y²/w
      <=beta b² int_S (2v_b-v(y))^-alpha dy
      <=2 beta b³(2v_b-v_*)^-alpha
       =beta/4 (1+kappa/8)^-alpha.

Both factors and the positive denominator are exact. The full mean is zero pointwise after transverse integration; finite weighted resistance extends the compact-core functional and earns a finite global inverse form by the previously checked positive-resolvent argument. No transverse transport, angular sampler, pointwise infinity flux assumption or unknown source is used.

Evenness of v gives h_u(-y)=1-h_u(y) for each u, so the actual new residual r=(2h_u-1)-(1_A-1_B) has all the required sign/range properties. Its price relative to beta M²R is O(alpha^(3/2)[(1+kappa)(1+kappa/8)]^-alpha), using the accepted scalar whole-basin/barrier estimates. This is a rigorous qualitative asymptotic of the finite bound. It does not construct the shifted barrier-flux current in the wells.

## 7. Controlling diagnostic qualifications, agreed by the root author

Two qualifications control the unchanged diagnostic wording:

1. The quantity approximately 32.5/alpha² is the formal leading estimate of the **scalar upper price** for C_trans/C_frozen, not an identity for the exact angular transverse energy. The trace bound need not be saturated.
2. The claim ||c||_2=O(sqrt(m)) requires bounded graph degree, bounded energy coefficients **and uniformly bounded diagonal mobility entries**. Coefficients/degree alone are insufficient: U=sum z_i^4 and D=mI give c_j=12m and ||c||_2=12m^(3/2). The root explicitly agreed to this controlling clarification while preserving the original bytes. Its current prototype has exact unit mobility, so the qualification does not change that declared example.

The formal coefficient algebra itself is consistent. Writing a=v_*(1-c/alpha), the formal Gaussian calculation gives R_a/R=1+(c²-c+3/4)/alpha+..., minimized at c=1/2 with coefficient 1/2. The frozen longitudinal price formally gives 1-1/(2alpha)+.... Differentiating the Gaussian frozen committor reproduces the displayed transverse scalar-price coefficient ||c||_2 sqrt(beta)v_*^(3/2)/[16kappa sqrt(dmin)alpha^(5/2)]. For the m=512 unit path fixture its corresponding coefficient is ||c||_2/64, about 32.5; the large-dimension bounded-degree value is 23sqrt(2).

These checks verify algebra **conditional on the formal expansion**, not a controlled remainder, finite accuracy, optimality or an actual kinetic error. The 1/alpha cancellation is not admitted as a finite certificate. R_a is a valid scalar resistance when 2a>v_*, but that is not alone a global current with matching well/slab interfaces. The old a=v_* well construction cannot be copied unchanged, and the shifted dual remains open. No new 513-dimensional target precision is claimed here.

## 8. Checks and preservation

The independent script passed **199 exact assertions**, covering shell exponents, Gauss primitive, beta/Gamma normalization, diagonal trace coefficients and scope counterexample, origin derivative, complete-price rational fixtures, odd-current constants, source hashes, and formal coefficient algebra explicitly labeled diagnostic. No candidate numerical receiver was imported or accepted.

The three sources remain immutable. Snapshots, input hashes, this review, the exact check script/results and the source-bound receipt are saved in a unique audit directory and bound by `AUDIT_SHA256.json`. No external retrieval or helper agent was used. Physical acquisition/preparation, model error, actual numerical operation/bit budgets, shifted dual receiving and historical novelty remain outside this acceptance.
