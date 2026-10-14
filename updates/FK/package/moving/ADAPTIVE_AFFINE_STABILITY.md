# Astra Meta-Genesis: adaptive rank-one regression and full affine stability

Research date: 14 October 2026.

## Status and scope

This note proves an all-affine, Schur-stable Jensen theorem near **transverse acoustic contacts**. The reference rank-one direction is chosen from the actual second moment, and the reference background direction moves with the smallest eigenvector of the rank-one Hessian. A scalar regression removes the complete cubic contribution of the reference line before any matrix inverse is estimated.

The result controls all four affine-background directions simultaneously. It allows unbounded affine backgrounds, arbitrarily small nonzero second moments, and concentration compatible with its two relative norm conditions. It is not the complete nine-coefficient quasiconvexity theorem: tangent contacts and distributions with substantial transverse fourth-moment mass are not covered.

A stronger feature must not be misrepresented: the new positive theorem requires only centeredness and determinant balance, not the entire gradient constraint. It therefore applies to gradients but is not a new characterization of gradient laws. A bounded, noncompatible tangent law shows why this moment argument cannot extend universally. An actual compatible tilted-wave example shows that a fixed-contact Schur denominator can collapse relative to its unreduced entry even without concentration; its variational gaps are positive.

The main theorem uses no rotational invariance. It applies to all 35-coefficient planar quartics satisfying its explicit local spectral assumptions, and more generally to a nondegenerate indefinite quadratic null cone in a finite-dimensional vector space. It does not automatically apply to rank-one cones in higher matrix dimensions, where several minors are required.

The analytic proof below is separate from the finite exact checks. The new standalone verifier passed 11 groups of exact checks in this run. The prior contact-compensation verifier was replayed successfully (nine groups). Its Hodge/interpolation argument was reconstructed, but neither it nor the long prior contact classification is a premise of the new theorem. No external proof review, proof-assistant formalization, historical priority clearance, or repository publication is claimed.

## 1. Definitions and reconstructed identities

Use the Euclidean/Frobenius inner product on V=R^(2x2), identified with R4 in row-major order. Write

    q(X)=det X=X^T J X,
    J_14=J_41=1/2, J_23=J_32=-1/2,

with all other entries zero. In particular J^2=I/4. Let F be a real homogeneous quartic, rank-one convex in the sense

    D^2 F(A)[R,R] >= 0 whenever q(R)=0.

Rotational invariance is not assumed.

For a centered random matrix X of finite fourth moment with E q(X)=0, set

    C=E XX^T, H=E D^2 F(X), b=E DF(X), c=E F(X).

All expectations are probability-normalized. Periodic gradients and zero-boundary W^(1,4) gradients have the required mean and determinant balance by integration by parts and density.

Quartic symmetry gives

    D^2 F(A)[X,X] = D^2 F(X)[A,A],                         (1.1)
    E[F(B+X)-F(B)] = c+b.B+(1/2)B^T H B.                 (1.2)

For fixed A, the indefinite non-strict Finsler lemma gives

    D^2 F(A) = P_A + lambda_A J,    P_A >= 0.             (1.3)

This is the classical indefinite quadratic lemma, not a new result. One short proof compares Q/q on every plane spanned by a positive-q and a negative-q vector. On that plane write q=s^2-t^2 and Q=as^2+2bst+ct^2. The null-line inequalities imply a+c>=2|b|, so Q-(a-c)q/2 is positive semidefinite there. Hence the supremum of Q/q on q<0 is no greater than its infimum on q>0; both are finite by fixing vectors of opposite signs. Any intervening scalar proves (1.3).

Averaging (1.3), and using (1.1), gives H>=0. Whenever H is positive definite,

    Delta_F(X):=inf_B E[F(B+X)-F(B)] = c-(1/2)b^T H^(-1)b. (1.4)

The only singular case needed in the new local theorem will be an exact rank-one law, where the range condition is established directly below. Consequently the new proof does not rely on the prior general nullspace-closure theorem.

## 2. Explicit spectral assumptions

Let R0 be a unit rank-one matrix and assume F(R0)>0. Put M0=D^2 F(R0). Reciprocity makes M0 positive semidefinite.

The substantive case is a **simple transverse contact**:

    ker M0 = span{A0}, |A0|=1,
    P0 = D^2 F(A0)-lambda0 J >= 0,
    ker P0 = span{R0}.                                    (2.1)

Thus both relevant positive quadratic forms have exactly one zero direction. In the previous terminology this is a Type I contact with a simple rank-one Hessian kernel. The hypothesis is explicit and is not asserted to hold at Type II tangent contacts.

The strictly positive case M0>0 has a simpler version of the same theorem, proved in Section 8.

### Main theorem

Under (2.1), there are constants delta0>0 and eta>0 depending on F,R0,A0 such that the following holds. Let X be any centered determinant-balanced law with finite fourth moment. Write

    X=s0 R0+Y0,    s0=X.R0,    Y0 orthogonal to R0.

If X is nonzero and

    ||Y0||_2 <= delta0 ||s0||_2,
    ||Y0||_4 <= delta0 ||s0||_4,                            (2.2)

then

    inf_{B in R^(2x2)} E[F(B+X)-F(B)] >= eta E|X|^4.        (2.3)

There is no restriction on B, no positive lower bound assumed for E|X|^2, and no pointwise support or amplitude bound. The zero law has gap zero. The theorem includes every compatible gradient satisfying (2.2), on arbitrary bounded Lipschitz domains after normalization.

Sections 3-7 prove a sharper quantitative approximation to the fully optimized value.

## 3. Adaptive covariance alignment

Let

    N={R: |R|=1, q(R)=0}.

Choose R maximizing R^T C R on N. This maximum exists because N is compact. Its sign is immaterial; choose the sign close to R0. Define

    s=X.R, Y=X-sR,
    m_j=E s^j, v=E|Y|^2, t=||Y||_4,
    delta2=sqrt(v/m2), delta4=t/m4^(1/4).                  (3.1)

We assume m2,m4>0; the theorem's nonzero cases satisfy this once delta0 is small.

### Lemma 3.1: exact quadratic-normal regression identity

At every stationary R of the constrained maximum,

    z:=E(sY) = -[E q(Y)/(2|JR|^2)] JR.                     (3.2)

Consequently |z|<=C_J v; for the determinant the constant is uniform over all unit rank-one R.

Proof. The gradients of |R|^2 and q(R) are independent because R.JR=0 and JR!=0. Lagrange multipliers give CR=m2 R+theta JR. Hence z=theta JR. Expanding the balanced quadratic moment,

    0=E q(X)=E q(Y)+2 R^T J z=E q(Y)+2theta |JR|^2,

which proves (3.2). This is an exact equality, not an approximation. In coordinates R=e12 it reads

    E(sa)=E(sd)=0,    E(sc)=E(ad).

The potentially first-order covariance correlation is constrained to the normal direction of the determinant cone and is quadratic in the transverse field. QED.

### Lemma 3.2: improvement in the averaged Hessian

Put M_R=D^2 F(R). Since its entries are quadratic polynomials,

    H=m2 M_R + D^3 F(R)[z,.,.] + E D^2 F(Y).               (3.3)

Therefore

    ||H-m2 M_R|| <= L v                                  (3.4)

locally uniformly in R. Without the stationary rank-one fit, the middle term is generally only bounded by a constant times sqrt(m2*v).

### Why the fit stays near the original line

The maximizing line has residual L2 norm no larger than the original line. Let theta be its angle from span R0. Projection onto its orthogonal complement gives

    ||s0||_2 sin(theta) <= ||Y0||_2+||Y||_2 <=2||Y0||_2.

Thus sin(theta)<=2 delta0. Moreover

    ||Y||_4 <= ||Y0||_4+sin(theta)||s0||_4.

The corresponding scalar L2 and L4 norms remain comparable. Hence (2.2) with sufficiently small delta0 ensures that R lies in any prescribed sufficiently small neighborhood of R0 and that delta2,delta4 are both small. No stationarity condition is imposed on the original field; it is obtained by fitting R.

## 4. Transporting the acoustic null direction

Because the zero eigenvalue of M0 is simple and its other eigenvalues are positive, for R near R0 the least eigenvalue epsilon(R) of M_R is simple. Let A_R be its continuously chosen unit eigenvector, with A_R.A0>0. Write epsilon=epsilon(R)>=0. The other eigenvalues are uniformly bounded below by a constant d>0.

A standard finite-dimensional spectral-gap estimate gives

    |A_R-A0| <= L|R-R0|.

Also, since q(R)=0 and P0 R0=0,

    0<=epsilon <= A0^T M_R A0 = R^T P0 R
                                <=L|R-R0|^2.              (4.1)

Choose any feasible Finsler scalar for A_R and put

    P_R=D^2 F(A_R)-lambda_R J >=0.

### Lemma 4.1: the positive remainder stays uniformly transverse

After shrinking the neighborhood,

    P_R(Y)>=nu |Y|^2 whenever Y.R=0,
    ||P_R||<=L,
    R^T P_R R=epsilon,                                    (4.2)

for fixed nu,L>0.

Proof. Feasible lambda_R are uniformly bounded: test P_R on fixed unit positive- and negative-eigenvectors of J. At the reference contact lambda0 is unique, since P0R0=0 and JR0!=0.

There is also a quantitative bound. Since M0A0=0,

    R0^T P_R R0=A_R^T M0 A_R
                =(A_R-A0)^T M0(A_R-A0)<=L|A_R-A0|^2.

Positive semidefiniteness and the uniform operator bound imply

    |P_R R0|<=L|A_R-A0|.

Subtracting P0R0=0 gives

    |lambda_R-lambda0| |JR0|
       <= |[D^2F(A_R)-D^2F(A0)]R0|+|P_RR0|
       <= L|A_R-A0|.

Thus P_R approaches P0 uniformly in the feasible scalar. P0 is positive definite transverse to R0, proving (4.2) after a small rotation of the reference line. The last equality in (4.2) follows from reciprocity and q(R)=0. QED.

## 5. Stability of the actual Schur complement

Take an orthonormal frame of A_R^perp and write

    H=[[h,k^T],[k,D]].

The dimensions are 1+3 in the planar problem. The following statements are in the **moving** frame A_R, not the old fixed contact direction A0.

From (3.4) and the eigenvector equation,

    D >= (d/2)m2 I,    |k|<=L v                            (5.1)

when delta2 is small.

Since determinant balance gives h=E P_R(X), equations (3.2) and (4.2) imply

    h=m2 epsilon+2(P_RR).z+E P_R(Y).

For a positive matrix, |P_RR|^2<=||P_R|| epsilon. Therefore

    h>=m2 epsilon+(nu-L sqrt(epsilon))v
      >=m2 epsilon+(nu/2)v.                               (5.2)

There is also the corresponding upper bound h<=m2 epsilon+L v.

Consequently the true reduced denominator sigma satisfies

    sigma=h-k^T D^(-1)k
          >=m2 epsilon+(nu/2)v-L v^2/m2
          >=c(m2 epsilon+v).                              (5.3)

More precisely,

    sigma >= (1-L delta2^2)h.                              (5.4)

Thus all complementary affine directions can be eliminated without destroying the controlled denominator. This is the missing comparison that was not available in the previous fixed-contact decomposition. It is proved only under the explicit transverse assumptions, not asserted universally.

The same bounds imply

    H >= c diag(m2 epsilon+v, m2 I_3),                     (5.5)

after decreasing c. One way to see this is to complete the square and use |k|^2/[m2(m2 epsilon+v)]<=L delta2^2. Hence, when m2 epsilon+v>0,

    w^T H^(-1)w <= L[w_A^2/(m2 epsilon+v)+|w_D|^2/m2].     (5.6)

The excluded case epsilon=v=0 is an exact rank-one law and will be handled without an inverse.

## 6. Remove the complete pure-line cubic before inversion

Set

    u=m3/(3m2),
    ell=b-u H R.                                           (6.1)

This is a change of affine origin, not a restriction of the optimizing background. For the exact law X=sR, Euler's identity gives

    b=m3 DF(R), H=m2 M_R, M_R R=3DF(R),

so ell=0 **in every background direction**. This cancellation remains true even when M_R is nearly singular.

For general X=sR+Y, let z=E(sY). Quartic expansion gives the exact vector identity

    ell = M_R[E(s^2Y)-2u z]
        +(1/2)E[s D^3F(R)[Y,Y,.]]
        +E DF(Y)-u E[D^2F(Y)R].                            (6.2)

Write S=m4^(1/4), so t=delta4 S and sqrt(v)=delta2 sqrt(m2). For delta2,delta4<=1, Holder gives

    |ell_D| <= L S^2 sqrt(v),                              (6.3)

and the eigenvector equation M_R A_R=epsilon A_R gives the better estimate

    |ell_A| <= L S^2 sqrt(v)(epsilon+delta2+delta4).         (6.4)

For clarity, the four types of term in (6.2) are bounded by

    epsilon S^2 sqrt(v),
    epsilon |u|v,
    S t sqrt(v)+t^2 sqrt(v),
    |u|v,

in its A_R component. Use |u|<=S^2/(3sqrt(m2)) and |z|<=Lv to obtain (6.4).

Combining (5.6), (6.3), and (6.4) proves

    ell^T H^(-1)ell <= L(delta2^2+delta4^2)m4.              (6.5)

Indeed the only apparently troublesome piece obeys

    epsilon^2 m4 v/(m2 epsilon+v)
        <= epsilon m4 v/m2 <=L delta2^2 m4,

because epsilon is bounded in the neighborhood. All other pieces have v/(m2 epsilon+v)<=1.

In particular, writing ell=(ell_A,ell_D) in the moving frame,

    |ell_A-k^T D^(-1)ell_D|
        <= L sqrt(sigma) sqrt(m4)(delta2+delta4),           (6.6)
    ell_D^T D^(-1)ell_D <= L delta2^2 m4.

Equation (6.6) is an estimate of the **actual reduced numerator with its actual reduced denominator**, after the explicit pure-line affine regression. It is not the old bound with sigma replaced by h.

## 7. Complete minimization and the positive margin

Shifting B=-uR+Z in the exact background expansion gives

    Delta_F(X)=Q-(1/2)ell^T H^(-1)ell,
    Q=c-u(b.R)+(1/2)u^2 R^T H R.                           (7.1)

Polynomial expansion and Holder give

    |c-F(R)m4|<=L delta4 m4,
    |b-m3 DF(R)|<=L S^2 sqrt(v),
    ||H-m2 M_R||<=Lv.

Therefore

    |Q-F(R)[m4-(2/3)m3^2/m2]|
        <=L(delta2+delta4+delta2^2)m4.                     (7.2)

Together with (6.5), this proves the stronger approximation theorem

    |Delta_F(X)-F(R)[m4-(2/3)m3^2/m2]|
        <= L(delta2+delta4)m4,                             (7.3)

after delta2,delta4 are restricted to at most one.

Since m3^2<=m2 m4 and F(R) stays uniformly positive,

    F(R)[m4-(2/3)m3^2/m2]>=F(R)m4/3.

For sufficiently small transverse ratios, (7.3) is positive by a fixed multiple of m4. Since

    E|X|^4=m4+2E(s^2|Y|^2)+E|Y|^4
           <=(1+delta4^2)^2 m4,

this proves (2.3).

If epsilon=v=0, then X=sR and H=m2M_R is singular. Euler's identity directly puts b in ran H and gives

    Delta_F(sR)=F(R)[m4-(2/3)m3^2/m2].                      (7.4)

Thus the singular case is included without importing an unproved range condition. Centeredness also gives the sharper scalar inequality m3^2<=m2(m4-m2^2), but the weaker bound suffices.

This completes a proof for all affine B. No minimizing direction was fixed in advance, and no inverse was replaced by a larger denominator.

## 8. Extensions and limit consequences

### 8.1 Strictly positive rank-one Hessian

If M0>0 and F(R0)>0, the same theorem holds with a shorter proof. For the fitted R near R0, M_R>=dI and H>=dm2I/2. The regression identity (6.2) gives |ell|<=LS^2 sqrt(v), so ell^T H^(-1)ell<=Ldelta2^2m4. Equations (7.1)-(7.4) finish the proof. No contact direction is needed.

### 8.2 A uniform statement over all rank-one directions

Suppose F(R)>0 for every unit rank-one R and every singular M_R satisfies the simple transverse conditions (2.1). Compactness of the unit rank-one set supplies a finite cover by the neighborhoods in Sections 2 and 8.1. Consequently there are constants delta_F,eta_F>0 such that (2.3) holds whenever a law is relatively L2- and L4-close to **any** rank-one line by at most delta_F.

This is a spectral hypothesis on the whole rank-one set, not a claimed classification of the nine-coefficient cone. Tangent contacts may be present in that cone and violate the hypothesis.

### 8.3 Full optimized continuity with equiintegrability

Suppose fourth powers |X_n|^4 are equiintegrable and C_n tends to m R0R0^T, m>0, at a reference line satisfying the theorem. Then the transverse projections converge to zero in L2 and, by equiintegrability, in L4. The fitted lines tend to R0 up to sign. Equation (7.3) gives

    Delta_F(X_n)-F(R_n)[m4_n-(2/3)m3_n^2/m2_n] ->0.          (8.1)

If the scalar third and fourth moments converge, this gives the complete limiting optimized value. Unlike the prior directional result, all affine directions have been eliminated. The minimizing matrices themselves need not remain bounded.

This does not assert continuity at tangent contacts, or without equiintegrability. The theorem itself permits concentration when its relative transverse norm conditions hold, and imposes no lower bound on m2.

### 8.4 Generality beyond rotational invariance

The proof only uses quartic reciprocity, the indefinite quadratic lemma, a smooth regular null cone, and the two complementary spectral gaps. With q(x)=x^T Jx for any nondegenerate indefinite J on a finite-dimensional Euclidean space, replace rank-one directions by q-null directions throughout. The same proof holds if M0 and P0 both have one-dimensional kernels and F(R0)>0. Constants depend on J as well.

For ordinary planar gradients this includes all 35 quartic coefficients, whenever the stated assumptions hold. It does not establish those assumptions for every rank-one-convex quartic. In higher matrix dimensions rank-one directions are not generally one quadratic null cone, so no unqualified higher-dimensional Morrey implication follows.

## 9. Nonvacuity: an explicitly checkable transverse contact

The known Dacorogna-Marcellini endpoint

    F_DM(A)=|A|^4-(4/sqrt(3))|A|^2 det A

has a transverse contact. Its global quasiconvexity is prior work, not an output of this note.

Its rank-one convexity can be checked directly using left and right rotations. At the direction e11, the acoustic quadratic in the background (a,b,c,d) is

    12a^2+4(b^2+c^2+d^2)-(4/sqrt(3))(6ad-2bc).

The (a,d) block has determinant zero and is positive semidefinite; the (b,c) block has eigenvalues 4+/-4/sqrt(3)>0. Rotational invariance supplies every rank-one direction.

At R0=e12 a kernel background is the unnormalized

    A0=(0,-sqrt(3)/3,1,0).

The determinant-corrected remainder has rank three with eigenvalues

    0, 8/3-8sqrt(3)/9, 8/3+8sqrt(3)/9, 16/3.

Thus the hypotheses genuinely occur at a non-polyconvex contact. The example is only a check of nonvacuity, not a replacement of the general theorem by another one-parameter classification.

### 9.1 An actual concentrating gradient with an escaping optimal background

The new theorem does not hide a bounded-background assumption. Use the same F_DM and unnormalized A0 above on the unit torus. Let phi0=(h0(y),0), with h0' equal to +1 on (0,1/4), -1 on (1/4,1/2), and zero on the rest of a period. Then

    H0=(1/2)D^2F_DM(e12), ker H0=span A0, b0=0, c0=1/2.

Use the zero-boundary square profile

    psi(s,t)=(f(s)t(1-t), s(1-s)t(1-t)),
    f(s)=2s for s<=1/3, f(s)=1-s for s>=1/3,

and insert rho^(3/4) psi((x-x*)/rho) in a square where Dphi0=0, with x*=(1/4,3/4), 0<rho<1/4. This is a genuine periodic Lipschitz potential for each rho.

Exact profile integration gives

    b_psi.A0=296/25515,
    A0^T H_psi A0=4/15,
    c_psi=E|Dpsi|^4=29023/1071630.

The profile Hessian is positive definite; its leading principal minors are

    88/81, 4561904/4428675, 433077568/1793613375,
    871474623232/19613162255625.

The combined field has exactly

    H_rho=H0+rho^(3/2)H_psi>0,
    b_rho=rho^(5/4)b_psi,
    c_rho=1/2+rho c_psi.

A block inverse on ker H0 and its complement yields

    (1/2)b_rho^T H_rho^(-1)b_rho
        =rho (10952/43401015)+o(rho),
    rho^(1/4)B_opt,rho -> -(74/1701)A0.                    (9.1)

Thus the minimizing background diverges, but its fully optimized cubic loss tends to zero at the displayed exact rate. The gradients have equiintegrable fourth powers: the concentrated fourth-moment mass is O(rho). Their relative transverse L2 and L4 norms are respectively O(rho^(3/4)) and O(rho^(1/4)), so they lie in the theorem's regime for sufficiently small rho. The example illustrates the proved stability through an escaping background; it is not a new claim of quasiconvexity for the already known F_DM.

## 10. A compatible fixed-frame Schur collapse

Use the prior rationally certified tangent quartic

    G=3(u+v-2q)^2+(35/24)u^2+q^2-(5/2)qu.                   (10.1)

The included verifier reconstructs its complete rank-six acoustic Gram certificate; it does not infer global rank-one convexity from angular sampling.

Let R_t=[[t,1],[0,0]] and M(t)=D^2G(R_t). It is positive definite for t!=0. Its determinant is

    det M(t)=15 t^4(563t^4+1296t^2+1248)/16.

Take A0=I and eliminate the complementary background directions K=diag(1,-1), e12, e21. With h=I^TM(t)I and sigma the corresponding Schur complement,

    h=(9/2)t^2,
    sigma=10t^4(563t^4+1296t^2+1248)
          /[3(595t^6+7992t^4+8064t^2+3072)],                (10.2)

so

    sigma/h ~ (65/216)t^2 ->0.                             (10.3)

This is realized by actual periodic gradients. Put

    s(theta)=cos(theta)+(1/2)cos(2theta),
    V(theta)=sin(theta)+(1/4)sin(2theta),
    phi_n(x,y)=(V(x+ny)/n,0).

Then Dphi_n=s(x+ny)R_(1/n). The gradients are uniformly bounded and their fourth powers are equiintegrable. Their averaged Hessians are positive definite. Their covariance has rank one, which is allowed here: this is a positive-gap example, not a putative counterexample.

The scalar moments are

    m2=5/8, m3=3/8, m4=99/128.

Consequently

    B_opt=-(1/5)R_(1/n),
    Delta_G(Dphi_n)=(399/640)G(R_(1/n))>0.                  (10.4)

The reduced cubic numerator in the fixed I frame is exactly (t/10) times the reduced averaged-Hessian denominator. Thus it vanishes fast enough; the apparent denominator singularity is harmless once the complete cubic regression is retained. The example disproves a fixed-frame uniform denominator comparison, not quasiconvexity.

## 11. Why the transverse theorem does not extend by moment algebra to tangency

For G at A0=I,R0=e12,

    D^2G(I)[X,X]=(1/2)(3a-2d)^2+(5/6)c^2-det X.

The positive remainder has rank two, not three. This is precisely the missing spectral gap in Section 4.

The following are bounded determinant-balanced **noncompatible laws**. Fix m=9, let epsilon>0 be small, and put

    w=1-3epsilon/2,
    t=(9/2)m^2 epsilon/w,
    S=diag(1,3/2), Rt=[[0,1],[t,0]].

Give mass w/2 to each of +/-Rt, mass epsilon to mS, and mass epsilon/2 to -2mS. The means of X and det X are zero. The law has transverse L2 and L4 norms tending to zero relative to its e12 component, but

    beta=E DG(X)[I]=(5/4)epsilon m^3,
    h=E D^2G(X)[I,I]=(135/8)m^4epsilon^2/w,
    c-beta^2/(2h) -> 3-5m^2/108 = -3/4.                   (11.1)

The covariance-adapted line is exactly e12 for sufficiently small epsilon. To verify this without an optimizer, for every unit rank-one test matrix R=(a,b,c,d), use ad=bc to rewrite its covariance value as

    R^T C R = w b^2+w t^2 c^2
              +(a,d) [[3,9],[9,27/4]] m^2 epsilon (a,d)^T.

For small epsilon, the 2x2 matrix is strictly below wI and t^2<1. Hence the unique maximizing matrix line is span e12.

Thus even the adaptive fit cannot make determinant balance prove the tangent result. These laws are not gradients; their support lies in a two-dimensional matrix subspace. Negative members contradict the two-phase Jensen inequality satisfied by actual periodic gradients confined to that subspace. Their failure is a boundary of this moment-based proof, not a compatible Morrey counterexample.

At m=9,epsilon=10^-6 the verifier checks centeredness, determinant balance, exact positivity of the averaged Hessian, the optimal fitted line, and an exact negative directional gap. No numerical fit is used for these statements.

## 12. Actual competing compatible search

A separate search used finite Fourier potentials for the exactly rank-one-convex G. It eliminated all affine directions and allowed a constant invertible input transformation, hence deformed periodic cells and nearly aligned input frequencies. The Fourier cutoff was three, the dealiased grid was 13x13, with six starts and 600 Adam iterations per start in double precision. A 10^-9 identity regularizer was used only in the linear solve; saved backgrounds were evaluated in the unregularized polynomial gap.

The smallest directly reevaluated gap was 0.9318892963523981. No negative compatible gap was found. This is not a lower bound, not a certificate of quasiconvexity of G, and not evidence covering the full cone. The script, saved coefficients, transformed cells, backgrounds, eigenvalues and logs are included. Spatial integration of quartic trigonometric polynomials at this bandwidth is dealiased; floating arithmetic, optimization and finite-bandwidth limitations remain.

## 13. What remains and what would constitute further progress

The moving Schur numerator and denominator are controlled in the transverse neighborhoods by (5.3)-(6.6). Repeating a fixed-contact estimate there is unnecessary: all affine directions are already handled.

The proof does not cover a rank-two tangent remainder. The crucial lower bound P_R(Y)>=nu|Y|^2 fails there; the limiting kernel contains a transverse matrix direction. The earlier Hodge/mixed-derivative estimate controls that direction at an exact contact, but no proof here makes it uniform under the simultaneous covariance fit and spectral motion of A_R. The bounded noncompatible laws in Section 11 show that such an extension must use actual differential compatibility, not just another determinant-moment inequality.

Nor does this local law theorem determine the gap for fields with substantial transverse fourth-moment mass. It gives neither a global profile decomposition into the covered laws nor a positive rule for recombining internally resonant pieces. Pure critical concentration can preserve such unresolved profiles.

A substantive next positive step would be a uniform differential estimate for the regressed vector ell=b-[m3/(3m2)]HR in the moving tangent metric, strong enough to replace (6.5), together with a sharp enough quartic remainder bound outside the near-line regime. An actual compatible negative optimized gap remains the competing route. A failed estimate or SDP would not supply one.

## 14. Reconstruction, sources and priority boundary

The prior CONTACT_COMPENSATION.md was read in full. Its exact verifier was replayed (nine groups). Its Hodge correction was checked to preserve both curl equations and its mixed-derivative interpolation has the stated L2/L4 to L^(8/3) exponents. These checks do not provide external validation of that analytic argument, and the new theorem does not depend on it or on completeness of the prior invariant-contact classification.

The classical indefinite Finsler lemma is used with its genuine hypothesis. Gutiérrez's fourth-degree necessary conditions already connect cubic resonances to quadratic and quartic terms. The recent Bruno-Pasqualotto theorem covers the left-and-right rotational quartic class and uses heat/exact forms, not the entire left-invariant class. Kristensen's local-quasiconvexity theorem under strict Legendre-Hadamard positivity is important prior context; it does not by itself assert the present unbounded-background, relative-L4 law inequality. No novelty is claimed for Lagrange multipliers, covariance fitting, spectral perturbation, Schur complements, Euler's identity, or Holder estimates individually.

Primary sources consulted:

1. T. J. Meijer et al., *A General Non-Strict Finsler's Lemma*, arXiv:2403.10306v1 (2024), especially Lemma 2 and the distinction from semidefinite quadratic constraints. https://arxiv.org/html/2403.10306v1
2. S. Gutiérrez, *A Necessary Condition for the Quasiconvexity of Polynomials of Degree Four*, Journal of Convex Analysis 13 (2006), 51-60. The primary PDF and Proposition 4.1 were inspected. https://www.heldermann-verlag.de/jca/jca13/jca0514_b.pdf
3. G. Bruno and F. Pasqualotto, *Quasiconvexity for the Dacorogna-Marcellini Energy*, arXiv:2608.06367v1 (2026). https://arxiv.org/html/2608.06367v1
4. J. Kristensen, *On the non-locality of quasiconvexity*, Ann. Inst. H. Poincare C 16 (1999), 1-13. The primary PDF and Proposition 1 were inspected. https://www.numdam.org/item/AIHPC_1999__16_1_1_0.pdf
5. Prior conversation artifact, *CONTACT_COMPENSATION.md*, 14 October 2026, for the prior two-background-direction result and the precise unreduced-versus-reduced Schur gap.

The targeted search did not establish historical novelty of the adaptive all-affine theorem. Absence of a matching retrieved result is not priority clearance. The finite verifier checks identities and explicit examples; the general inequalities, spectral neighborhoods, regression estimates, compactness and density are proved in this note rather than certified by code. No full quasiconvexity solution or external validation is claimed.
