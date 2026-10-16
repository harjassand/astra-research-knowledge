# Strict weighted order characterizes uniformly integrable near-kernel decay

Status: root-derived extension of this round's weighted polynomial theorem. Internal analytic proof; external correctness and historical priority UNKNOWN. This generalizes the separately derived 15-dimensional cubic result. It is a theorem about exact compatible gradients, not a sharp quasiconvexity bound.

Use normalized measure on a fixed planar square torus. For periodic potentials phi=(f,g), write (a,b,c,d)=(f_x,f_y,g_x,g_y), q=sigma a+d, T=(q,c), with fixed sigma>0. Let P be a nonzero homogeneous real polynomial of degree m>=3, and express it in coordinates (a,b,c,q). Give b weight0, a weight1, and c,q weight2. Let j(P) be the least weight of a nonzero monomial after exact coefficient cancellation.

Fix 0<alpha<=m and finite 1<p,s<infinity with alpha/p+(m-alpha)/s=1. Consider all smooth periodic sequences with E_n=||T phi_n||_p>0 tending to zero, bounded M_n=||Dphi_n||_s, and uniformly integrable |Dphi_n|^s.

**Theorem.** The following are equivalent:

1. For every such sequence, |average P(Dphi_n)|/E_n^alpha tends to zero.
2. For every such sequence, ||P(Dphi_n)||_1/E_n^alpha tends to zero.
3. j(P)>2alpha.

In contrast, the all-gradient finite big-O estimate at these same exponents holds exactly when j(P)>=2alpha. Equality is a real compactness boundary; uniform integrability cannot turn every finite bound into a vanishing ratio. The zero polynomial satisfies all three conditions if its least weight is conventionally +infinity.

## Sufficiency with an explicit residual factor

The source's mixed-derivative/Hodge estimate, at finite endpoints p,s, is

    ||a||_t <= C (E M)^(1/2),    1/t=(1/p+1/s)/2.

Thus a_n tends to zero in measure. Likewise c_n,q_n tend to zero in measure by their Lp defect bound. Since |a|^s+|c|^s+|q|^s <= C_sigma |Dphi|^s, uniform integrability implies

    R_n = ||(a_n,c_n,q_n)||_s -> 0.

This uses finite s and Vitali convergence. It needs neither a determinant-product estimate with unjustified dual exponents nor s>=2.

Take a monomial a^u b^v c^w q^z, with degree m, and put beta=u/2+w+z. Strict weighted order gives beta>alpha. Set theta=alpha/beta in (0,1). Interpolate each a factor between its mixed norm t and its own Ls bound R. Interpolate each c,q factor between its Lp bound E and its own Ls bound R. Keep b in Ls with norm at most M. The reciprocal exponents sum to

    theta beta/p+(m-theta beta)/s = 1.

Hölder therefore gives

    ||a^u b^v c^w q^z||_1
      <= C E^alpha M^(v+theta u/2)
                 R^((1-theta)(u+w+z)).

The power of R is strictly positive. Both displayed residual powers add to m-alpha, so the bound has the correct amplitude and measure homogeneity. Bounded M and R->0 prove the absolute little-o result for every monomial, hence for P. In particular, no unjustified L6 acquisition is inserted into a claimed L4 conclusion.

## Necessity: uniformly bounded exact compatible witnesses

This uses the constructive necessity argument from `ga_polynomial_genesis/CORE_THEOREM_v1.md`, independently reconstructed in `ga_weighted_audit/REPORT.md`. Let P_j be the first nonzero weighted part. The planar Hessian null-polynomial lemma implies that, when m>=3, there are smooth periodic psi and mean-zero k with

    I = average P_j(psi_xy,psi_yy,-sigma psi_xx,k) != 0.

Choose smooth periodic F,G with sigma F_x+G_y=k. Set epsilon=1/N for integers N and

    f_N = epsilon psi_y(x,Ny)+epsilon^2 F(x,Ny),
    g_N = -sigma epsilon^2 psi_x(x,Ny)+epsilon^3 G(x,Ny).

Then

    (a,b,c,q) =
    (epsilon psi_xy+epsilon^2 F_x,
     psi_yy+epsilon F_y,
     -sigma epsilon^2 psi_xx+epsilon^3 G_x,
     epsilon^2 k)(x,Ny).

The full gradients are uniformly bounded in Linfinity, so all finite-s powers are uniformly integrable. Their polynomial mean is epsilon^j I+O(epsilon^(j+1)). Their defect is O(epsilon^2) in every finite Lp. It is nonzero for all sufficiently large N: if both psi_xx and k vanished identically, psi_xy would vanish, and a positive leading weight j could not have a nonzero I. For j=0, add an arbitrarily small mean-zero k to create a nonzero defect without changing the leading b-only term.

If j<=2alpha, the signed quotient cannot tend to zero: its magnitude is bounded below by a positive constant times N^(2alpha-j), using the upper bound on E. This includes the equality case. The same signed witness also refutes absolute little-o. Degree two is excluded because the true gradient determinant is an exact signed null Lagrangian. Arbitrary nonzero harmonic matrix fields are excluded because the theorem concerns periodic potentials, not merely row-curl-free matrices.

## Cubic instance and research consequence

For m=3, alpha=1, p=2, s=4, weights<=2 are exactly

    b^3, ab^2, a^2 b, cb^2, qb^2.

Hence the near-kernel little-o space has dimension20-5=15, whereas the finite-bound space has dimension20-2=18. This agrees with two independent cubic derivations in this round. For general degree m at alpha=1, the dimension is binomial(m+3,3)-5.

For the conformal cubic C_r, the lowest weighted term is -kappa a^3 and has weight3, so the strict criterion applies at its L2/L4 balance. Its nonvanishing normalized ratio therefore requires loss of uniform integrability. The quantitative superlevel concentration and diffuse-cloud results give stronger information about that loss. They do not yield Gamma_r<=1 or an acquired physical capability.

The theorem supplies an exact algebraic classification of when near-kernel vanishing is a valid compactness step. It also provides bounded compatible counterexamples whenever it is invalid. Historical priority remains open; interpolation, Hodge theory, Vitali convergence and null-Lagrangian structure are classical.
