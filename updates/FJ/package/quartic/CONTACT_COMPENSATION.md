# ASTRA Meta-Genesis: quantitative cubic compensation at acoustic contacts

Research date: 14 October 2026.

## Status and exact scope

The full implication from rank-one convexity to quasiconvexity for the nine-coefficient left-SO(2)-invariant homogeneous quartic cone is **not proved here**. No compatible negative quasiconvexity gap is constructed.

The principal result is a quantitative, genuinely differential estimate. At any acoustic contact of a non-polyconvex quartic in the complete invariant cone, its averaged cubic coupling is controlled by the square root of the corresponding averaged Hessian energy, multiplied by the total and transverse L4 norms of the gradient. Unlike determinant balance alone, curl compatibility supplies this estimate. A second estimate controls the coupling between the contact background and the rank-one contact direction.

These estimates prove a uniform positive Jensen inequality in a two-dimensional plane of affine backgrounds, for arbitrary compatible gradients sufficiently close to the contact matrix line in relative L2 and L4 norms. The background coefficients can be arbitrarily large. All Fourier resonances and concentration satisfying those norm conditions are included.

An actual compatible concentrating sequence shows that the transverse L4 factor cannot be replaced by an Lp factor with p<4 while retaining the other factors and a uniform constant. Determinant-balanced, uniformly bounded matrix laws violate the L4 estimate itself: this explicitly distinguishes the differential theorem from moment algebra.

A new algebraic simplification is also proved: at a nonzero rank-one matrix, a rank-at-most-two Hessian of a left-SO(2)-invariant rank-one-convex quartic forces polyconvexity (and, when the value there is positive, an explicit convex decomposition). Consequently every singular rank-one Hessian of a non-polyconvex integrand has a one-dimensional kernel.

Finally, the contact shear is shown to be an exact conjugacy of variational problems. Without a further constraint on the transformed residual it is not a reduction in the admissible class. A stronger spatially frozen Jensen claim fails even for a convex quartic.

The analytic proof below uses standard harmonic-analysis ingredients and the reconstructed algebraic contact classification from the previous note. Neither Hodge projection, complex interpolation, nor change of variables is claimed as a new general method. Historical priority for their combination with the present contact geometry remains unestablished. No external review or proof-assistant validation is claimed.

## 1. Notation and the variational gap

Identify real 2 by 2 matrices with R4 in row-major order. For A=(x|y), write

    u=|x|^2, v=|y|^2, w=x.y, q=det A.

The full invariant quartic is

    F=Ac u^2+Bc v^2+C uv+E w^2+G uw+H vw+L qu+M qv+N qw.       (1.1)

All nine coefficients remain unrestricted, subject only to rank-one convexity. Non-polyconvex means there is no convex function of (A,det A) representing F.

Use probability-normalized averages and Lp norms on a periodic cell. Zero-boundary gradients are included by extension and approximation. For a mean-zero gradient X=Dphi,

    E X=0, E q(X)=0.

Define

    H_X=E D^2F(X), b_X=E DF(X), c_X=E F(X).

Quartic polarization gives

    J_F(B,X):=E[F(B+X)-F(B)]
            =c_X+b_X:B+(1/2)B:H_X B.                          (1.2)

An acoustic contact is a pair A!=0, R!=0 with rank R=1 and

    D^2F(A)[R,R]=0.                                          (1.3)

Normalize |R|=1. For each field set

    s=X:R, Y=X-sR, M=||X||_4, T=||Y||_4,
    h=E D^2F(X)[A,A], beta=E DF(X)[A],
    g=E D^2F(X)[A,R].                                        (1.4)

Y is a pointwise matrix projection. It is **not** assumed to be a gradient. The proof never makes that invalid replacement.

## 2. Reconstructing the algebraic foundation

### 2.1 Reciprocity, positive remainders and cubic closure

Let Jdet be the matrix for q. Homogeneity gives

    D^2F(A)[X,X]=D^2F(X)[A,A].                                (2.1)

The indefinite Finsler lemma says that a quadratic form nonnegative on q=0 has the form

    D^2F(A)[X,X]=P_A(X)+lambda_A q(X), P_A>=0.                 (2.2)

The determinant is indefinite; no semidefinite version is being assumed. One elementary proof compares Q/q on positive and negative q-vectors. On their span, normalize q=s^2-t^2. Positivity on the two null lines implies that Q-(alpha-gamma)q/2 is positive semidefinite on that plane, giving the required global ordering of ratios. A scalar between the supremum of the negative-q ratios and the infimum of the positive-q ratios proves the assertion.

Thus h=E P_A(X)>=0 for every determinant-balanced law. At a contact, P_A(R)=0, hence its symmetric matrix annihilates R. The scalar lambda_A is unique at this contact:

    D^2F(A)R=lambda_A Jdet R,
    lambda_A=((Jdet R).(D^2F(A)R))/|Jdet R|^2.                 (2.3)

This gives the remainder explicitly once F,A,R are given.

Put C_A(X)=DF(X)[A], a homogeneous cubic. Reciprocity makes D^2F(R) positive semidefinite when R is rank one. Contact equality therefore implies D^2F(R)A=0. By quartic tensor symmetry,

    D^2 C_A(X)[R,R]=0 for every X.                            (2.4)

In coordinates X=sR+Y, C_A contains at most one power of s. This is a polynomial identity in all matrix entries, not only on a law's support.

There is a stronger closure on U=ker P_A when q|U is indefinite. For any rank-one Z in U, the nonnegative quadratic t -> D^2F(A+tW)[Z,Z] vanishes at zero, and therefore D^3F(A)[W,Z,Z]=0. Thus D^2 C_A(W)[Z,Z]=0. A quadratic vanishing on an indefinite quadratic null cone is a scalar multiple of that quadratic. Consequently D^2 C_A(W)|U=ell(W)q|U. Diagonalizing q|U and using symmetry of the cubic tensor forces ell=0. Hence C_A|U=0. If q|U is semidefinite, a balanced law supported on U is confined to q=0, which likewise gives C_A=0 almost everywhere.

This reconstructs H_X>=0 and b_X in ran H_X. It does not itself prove the Jensen gap nonnegative.

### 2.2 A new simplification: low rank at a rank-one matrix

**Proposition 2.1.** Let F satisfy (1.1) and be rank-one convex. If rank D^2F(R)<=2 at some nonzero rank-one R, F is polyconvex. If F(R)>0, F is a convex sum of two fourth powers of norms of linear maps.

**Proof.** Normalize R=e11 by a left rotation and an invertible real input change. Put Ac=F(e11). If Ac=0, the convex nonnegative binary rank-one restriction has a zero direction. Its fourth root is a seminorm, so after an input change it is a single fourth power. The full invariant polynomial becomes

    a u^2+gamma q^2+q(Lu+Mv+Nw).

Its positive-semidefinite Hessians at e12 and e11 force M=N=L=0 and gamma>=0. This is polyconvex.

Suppose Ac>0. The Hessian at e11 is

    [12Ac  3G    0    3L]
    [3G  2C+2E  -L    N]
    [0    -L   4Ac    G]
    [3L    N    G    2C].

The (a,c) block is positive definite. Rank at most two forces its lower Schur complement to vanish, giving

    C=(G^2+3L^2)/(8Ac), E=(G^2-L^2)/(4Ac), N=GL/(2Ac).

Let kappa=(G-iL)/(4Ac), using complex output columns. The full polynomial is then

    F=Ac |x_C+kappa y_C|^4+B'v^2+H'vw+M'qv.                  (2.5)

Take any background in x_C+kappa y_C=0. The first summand has zero Hessian there. Test the rank-one direction e1 tensor (1,t). Its acoustic quadratic is nonnegative for all t and vanishes at t=0. Its derivative at zero is

    2[H'(3b^2+d^2)+2M'bd].

This must vanish for every b,d, so H'=M'=0. At a nonzero background in that kernel, a rank-one variation of the second column forces B'>=0. Therefore (2.5) is convex. QED.

In particular, if F is non-polyconvex, F(R)>0 for every nonzero rank-one R and rank D^2F(R)>=3. A singular such Hessian has exactly a one-dimensional kernel.

### 2.3 Contact types needed for the estimate

For completeness, the prior algebraic contact classification was reconstructed as follows. Its two essential implications are:

* If a remainder P_A has rank <=1, or if its rank-two kernel has indefinite or identically zero determinant restriction, F is polyconvex.
* For non-polyconvex F, if rank P_A=2 and A is invertible, the determinant on ker P_A is semidefinite of rank one. Its radical R is a determinant-preserving contact shear: tr(A^{-1}R)=0, and C_A(X+tR)=C_A(X) on ker P_A.

Here are the load-bearing calculations, including the non-generic cases. For invertible A normalize A=I, and write matrices as xi I+jJ+kK+lL. Let z=xi+sqrt(-1)j and w=k+sqrt(-1)l. Here xi,j,k,l are real coordinates. Then q=|z|^2-|w|^2 and the complete invariant polynomial is

    f|z|^4+beta|z|^2|w|^2+g|w|^4
    +Re(delta z^2 conjugate(w)^2
        +epsilon |z|^2 z conjugate(w)
        +eta |w|^2 z conjugate(w)).                           (2.6)

A conjugation by rotations makes epsilon=a>=0 real. Put p=12f-lambda and r=4f-lambda. If p,r>0, rank two of P_A gives

    Im delta=0,
    beta=(9a^2/p+a^2/r-2lambda)/4,
    delta=(9a^2/p-a^2/r)/4,
    ker P_A: xi=-3ak/p, j=-al/r.                        (2.7)

If q|ker P_A is indefinite, cubic closure forces partial_xi F=0 on the kernel. The difference of its k^3 and kl^2 coefficients is

    -4lambda^3 a^3/(r^2 p^3).

Its vanishing forces lambda a=0; each resulting determinant restriction is semidefinite, a contradiction. If q vanishes identically, p=3a,r=a,lambda=0,a=4f, and the full contact equations give

    F=f|z+w|^4+(g-f)|w|^4, g-f>=0,

which is convex.

The cases p=0<r and r=0<p are not discarded. In the former, the indefinite kernel contains I and cubic closure contradicts 4f<0. In the latter, rotation gives a residual

    f q^2+tau(Re z conjugate(w))^2+g0|w|^4+h|w|^2Re(z conjugate(w)).

At z=iZ,w=iW, the rank-one directions (sigma,1), sigma=+/-1, have second derivative

    2[(2tau sigma+h)ZW+(2g0+h sigma)W^2].

Both signs and arbitrary Z force tau=h=0. If p=r=0, the kernel is the conformal plane, with definite determinant, and cannot contain a rank-one contact. The rank-at-most-one remainder cases similarly reduce to gamma q^2 plus a convex fourth power, using the forced first two Hessian rows and the same cubic closure. At rank-one A, Proposition 2.1 permits P_A=D^2F(A), whose rank is at least three for non-polyconvex F.

For a semidefinite rank-one determinant restriction in (2.7), exactly one of p=3a or r=a holds. The first branch has critical contact z=-1,w=1. Writing V=F(-1,1)>0, an explicit joint variation of the rank-one direction and background has minimized second coefficient

    -(p-3r)^4/(324 r^2 V).

If p!=3r this is negative, contradicting actual rank-one convexity, not just an SOS ansatz. If p=3r the polynomial is the convex case already described. The surviving branch r=a has radical z=-il,w=il, or R=e12 in physical coordinates. The full contact equation gives Im eta=0 and

    Re eta=(48f^2-40f lambda+7lambda^2)/p,
    partial_xi F|ker P_A=-4lambda^3 r k^3/p^3.

The last expression is independent of the radical coordinate. This proves the required shear and cubic invariance. The previous standalone verifier was rerun and checks these joint-contact identities. Its full analytic proof is preserved in the prior note; the reconstruction above states every classification branch used here.

Therefore every non-polyconvex contact falls into one of the following two forms:

**Type I:** rank P_A=3, ker P_A=span{R}.

**Type II:** after compatible constant coordinate changes, A=I, R=e12,

    U=ker P_A={c=0,d=lambda a}, lambda!=0,
    P_A >= nu [c^2+(d-lambda a)^2], nu>0,
    C_A|U=kappa a^3,
    partial_b^2 C_A=0 on all matrix space.                   (2.8)

In Type II, trace-free nilpotence puts the radical into e12. Since the determinant's polar form vanishes between R and U, every matrix in U is upper triangular. Subtracting its e12 component puts a second generator into diag(1,lambda), proving the canonical plane description. Norms after these fixed coordinate changes are equivalent; all constants below may depend on them.

## 3. The genuinely differential step

### 3.1 A mixed-derivative interpolation inequality

**Lemma 3.1.** For a scalar potential psi on R2, or on a flat periodic cell, with the displayed derivatives in the indicated spaces,

    ||psi_12||_(8/3)^2 <= C ||psi_11||_2 ||psi_22||_4.         (3.1)

The constant is independent of Fourier bandwidth and frequency aspect ratio.

**Proof.** Begin with a finite Fourier sum, suppressing the frequency axes, which contribute nothing to psi_12. On the strip 0<=Re z<=1 consider

    T(z)=|D1|^(2z)|D2|^(2(1-z)) psi.

On Re z=1 its L2 norm is ||psi_11||_2, because the remaining multipliers are unimodular. On Re z=0, one-dimensional imaginary-power multipliers, applied in each variable, bound its L4 norm by C(1+|Im z|)^N ||psi_22||_4. Those are the usual one-dimensional multiplier estimates; the tensor product acts successively in the two variables.

Multiply the family by a Gaussian factor exp(epsilon(z-1/2)^2) to control the polynomial boundary growth. The vector-valued three-lines/complex interpolation argument gives

    || |D1||D2| psi ||_(8/3)
       <= C ||psi_11||_2^(1/2)||psi_22||_4^(1/2),

since 1/(8/3)=(1/2)(1/2)+(1/2)(1/4). Two directional Hilbert transforms recover psi_12 and are bounded in L^(8/3). Density proves the result. On R2 use the identical Fourier argument. A cutoff on increasingly large boxes transfers the estimate to any periodic lattice without a bandwidth restriction.

This is an application of standard mixed-derivative interpolation, not a claim to have invented complex interpolation or imaginary-power multiplier theory. The proof is included to identify exactly the exponent and endpoint assumptions used: no L-infinity endpoint is imported. QED.

### 3.2 Curl compatibility converts the tangent coordinate into a mixed derivative

Let X=Dphi=[[a,b],[c,d]], lambda!=0, and r=d-lambda a. Define the Riesz-type multipliers

    T_ij=partial_i partial_j Delta^(-1),

on zero-mean functions, and correct the potential by

    phi1^0=phi1+(1/lambda)partial_1 Delta^(-1)r,
    phi2^0=phi2-partial_2 Delta^(-1)r.                        (3.2)

This is a Hodge projection of (lambda phi1,-phi2). Its gradient X0 satisfies

    d0=lambda a0,
    ||X-X0||_p <= C_(p,lambda)||r||_p, p=2,4.                (3.3)

Because it is still a gradient, there is a scalar stream potential psi with

    phi1^0=psi_2/lambda, phi2^0=psi_1,
    a0=psi_12/lambda, b0=psi_22/lambda, c0=psi_11.             (3.4)

Let Y=(a,0;c,d) be the transverse projection away from e12. Equations (3.3)-(3.4) and Lemma 3.1 give

    ||a0||_(8/3)^2 <= C_lambda (||c||_2+||r||_2)||X||_4,
    ||a0||_4 <= C_lambda ||Y||_4.                            (3.5)

Interpolation, or directly Holder with exponents 4/3 and 4, gives

    int |a0|^3 <= ||a0||_(8/3)^2 ||a0||_4.

The difference of the cubes is bounded by

    int |a^3-a0^3|
       <= ||a-a0||_2 (||a||_4+||a0||_4)^2.

Consequently

    |E a^3| <= C_lambda (||c||_2+||r||_2)||X||_4||Y||_4.      (3.6)

This estimate uses both curl equations. It is not obtained by replacing the gradient distribution by a determinant-balanced probability law.

## 4. Main quantitative theorem

**Theorem 4.1 — Cubic contact compensation.** Let F be a non-polyconvex rank-one-convex homogeneous quartic in the complete left-SO(2) cone. Let (A,R) be an acoustic contact with |R|=1. There exists a finite K=K(F,A,R) such that every periodic or zero-boundary W1,4 potential satisfies

    |E DF(X)[A]| <= K (E D^2F(X)[A,A])^(1/2)
                         ||X||_4 ||X-(X:R)R||_4,             (4.1)

and

    |E D^2F(X)[A,R]| <= K (E D^2F(X)[A,A])^(1/2)
                           ||X-(X:R)R||_2.                 (4.2)

The estimates include arbitrary resonances and arbitrarily large amplitudes. No uniform value of K over all integrands or all contact pairs is claimed.

**Proof for Type I.** Since P_A is positive definite transverse to R,

    P_A(X)>=nu|Y|^2.

By (2.4), the cubic C_A has the form s Q2(Y)+Q3(Y), hence

    |C_A(X)|<=C|Y|^2|X|.

Holder gives |E C_A|<=C||Y||_2||Y||_4||X||_4, proving (4.1). Its derivative along R is Q2(Y)=D^2F(X)[A,R], which gives (4.2).

**Proof for Type II.** Work in (2.8). Since C_A|U=kappa a^3, the polynomial C_A-kappa a^3 belongs to the ideal generated by c and r=d-lambda a. Since partial_b^2 C_A=0 globally, these error terms contain no b^2 factor. Thus

    |C_A(X)-kappa a^3|
       <= C (|c|+|r|)|Y|(|b|+|Y|).                          (4.3)

Combining (3.6), Holder, and P_A>=nu(c^2+r^2) proves (4.1). Differentiation along R removes the kappa a^3 term; the remainder is a quadratic bounded by C(|c|+|r|)|Y|. This proves (4.2). Undo the fixed coordinate changes, absorbing their norms in K. The equivalence of transverse norms follows because the transformations map the contact line to the canonical one.

Start with smooth potentials. Hodge multipliers, interpolation and all integrals are continuous in the indicated norms. Density gives the W1,4 versions. Extension by zero and large-box periodic cutoffs give the stated boundary variants. QED.

The analytic implication is not intrinsically rotational: it applies to any homogeneous planar quartic whose contact has Type I or Type II and the indicated cubic null identities. Rotation invariance is used in Section 2 to prove those types exhaust the non-polyconvex contacts in the nine-coefficient class. No exhaustion theorem for all 35 coefficients is asserted.

## 5. Actual global positivity consequences

### 5.1 A uniform Jensen inequality on a contact ray

For h>0, (4.1) gives

    beta^2/(2h) <= (K^2/2)||X||_4^2||Y||_4^2.                (5.1)

When h=0 the numerator is zero; use zero for this quotient.

Because F(R)>0 and F is quartic, there is a coefficient-dependent C_F such that

    |E F(X)-F(R)E s^4| <= C_F ||Y||_4 (||sR||_4+||Y||_4)^3.

Therefore there are delta>0 and eta>0, depending only on F,A,R, for which

    ||Y||_4 <= delta ||X||_4

implies

    E[F(tA+X)-F(tA)] >= eta ||X||_4^4 for every real t.        (5.2)

Indeed c_X>=F(R)||X||_4^4/2 for sufficiently small delta, while the subtracted loss in (5.1) is at most K^2 delta^2||X||_4^4/2. Complete the square in t in (1.2). This controls escaping backgrounds on the entire fixed contact ray; t is not required to be small or bounded.

### 5.2 Two affine-background directions

**Theorem 5.1 — Contact-plane Jensen positivity.** There exist delta,eta>0, depending only on F,A,R, such that for any centered compatible X=sR+Y with

    ||Y||_2 <= delta ||s||_2,
    ||Y||_4 <= delta ||s||_4,                                (5.3)

one has

    E[F(tA+uR+X)-F(tA+uR)]
       >= eta (||s||_4^4+u^2||s||_2^2)
       for every t,u in R.                                 (5.4)

If s=0, the assumptions force X=0 and the non-strict version is immediate. Otherwise the inequality is strict whenever the right side is positive.

**Proof.** Let m_j=E s^j and f0=F(R)>0. Along the pure line,

    J_F(uR,sR)=f0(m4+4u m3+6u^2m2)
              >= (f0/4)(m4+u^2m2),                          (5.5)

because m3^2<=m2 m4 and 4xy<=3y^2/4+16x^2/3.

For delta<=1, polynomial expansion and Holder give

    |c_X-f0m4| <= C delta m4,
    |b_X:R-4f0m3| <= C delta sqrt(m2*m4),
    |R:H_X R-12f0m2| <= C delta m2.                          (5.6)

For example, the linear-transverse term in the cubic uses

    E |s|^2|Y| <= ||s||_4^2||Y||_2,

the quadratic-transverse term uses ||s||_2||Y||_4^2, and the cubic error uses ||Y||_2||Y||_4^2. These are exactly why both relative norm conditions appear.

For B=tA+uR, minimize (1.2) first over t. The loss is

    (beta+u g)^2/(2h)
       <= K^2 [||X||_4^2||Y||_4^2+u^2||Y||_2^2]
       <= 4K^2 delta^2(m4+u^2m2).                           (5.7)

Combine (5.5)-(5.7). Choosing delta so that C delta+4K^2delta^2<f0/8 gives (5.4), with eta=f0/8 after adjusting C. If h=0 then beta=g=0 by (4.1)-(4.2), and the same argument applies without division. QED.

This is a genuine Jensen theorem for all coefficients, not a classification of a new one-parameter integrand family. It is still restricted in perturbation geometry and affine-background directions: (5.4) is not full quasiconvexity of F.

### 5.3 The equiintegrable directional limit

Suppose X_n are compatible gradients with bounded L4 norms, their fourth powers are equiintegrable, and their second moments converge to a nonzero matrix m RR^T. Then Y_n=X_n-(X_n:R)R converges to zero in L2, hence in measure. Equiintegrability implies ||Y_n||_4->0. Thus at every fixed contact (A,R),

    (E DF(X_n)[A])^2/(2 E D^2F(X_n)[A,A]) -> 0.             (5.8)

Zero denominators have zero numerator and contribute zero. This fills a specific gap in the previous continuity analysis. It is a directional statement; it does not imply continuity of the fully optimized inverse-Hessian expression when its minimizing eigenvector rotates.

## 6. Exact examples separating gradients from moments and fixing the exponent

Use the prior exactly certified integrand

    G=3(u+v-2q)^2+(35/24)u^2+q^2-(5/2)qu.                    (6.1)

The new checker reconstructs its positive acoustic Gram matrix with rank six from rational constants, not from numerical eigenvalues. Its leading minors through order six are

    107/2, 642, 1605/8, 8445/16, 2815/8, 26865/4,

and its remaining Schur complement vanishes. Thus G is rank-one convex. Since G(I)=-1/24, the balanced scaling witness described in the previous note proves non-polyconvexity.

At A=I,R=e12, put r=d-3a/2. Then exactly

    h=E[2r^2+(5/6)c^2],
    C_I(X)=-(5/12)a^3+(1/2)a^2r-(5/12)ac^2+2ar^2
             -2bcr-(5/2)c^2r.                              (6.2)

In particular the problematic a^3 is present, and partial_b^2 C_I=0. Formula (3.6) is the missing estimate for that term. A compatible resonant Hessian potential

    psi=cos(x+y)+cos(x+2y)+cos(2x+3y),
    phi=(psi_y/(3/2),psi_x),

has E C_I(Dphi)=85/18, checked exactly. The theorem does not assume cubic resonances cancel.

### 6.1 Uniformly bounded determinant-balanced laws violate (4.1)

Fix m>0 and 0<epsilon<2/3. Set

    S=diag(1,3/2),
    t=(9/2)m^2 epsilon/(1-3epsilon/2),
    Rt=[[0,1],[t,0]].

Put mass (1-3epsilon/2)/2 at each of +/-Rt, mass epsilon at mS, and mass epsilon/2 at -2mS. These laws are centered and determinant-balanced. For fixed m they are uniformly bounded as epsilon->0. Exact integration gives

    beta=(5/4)epsilon m^3,
    h=(135/8)m^4 epsilon^2/(1-3epsilon/2),
    E|Y|^4=(1-3epsilon/2)t^4+(1521/16)epsilon m^4,
    E|X|^4=(1-3epsilon/2)(1+t^2)^2+(1521/16)epsilon m^4.

Hence beta^2/h ->5m^2/54, but ||X||_4^2||Y||_4^2->0. No finite constant in (4.1) works for determinant-balanced laws. More precisely,

    epsilon * [beta^2/(h ||X||_4^2||Y||_4^2)]^2
       ->400/(2916*1521)>0.                                (6.3)

This is an exact distinction between moment balance and the differential theorem. No member of this law family is asserted to be a gradient. The negative-gap members of the earlier construction are already incompatible with the two-phase subspace theorem.

### 6.2 The transverse exponent four is necessary

Take the actual compatible concentration construction from the previous note. Its base is phi0=(h0(y),0), with h0' equal to +1 on (0,1/4), -1 on (1/4,1/2), and zero elsewhere. It is pure R=e12 and has beta0=h0_contact=0. In a region where its gradient is zero insert

    rho^(1/2) psi((x-x*)/rho),

where on the unit square

    psi(s,t)=(f(s)t(1-t),s(1-s)t(1-t)),
    f(s)=2s for s<=1/3 and f(s)=1-s for s>=1/3.

Direct rational integration, repeated by the new verifier, yields

    beta_psi=283/5670,
    h_psi=179/540,
    E|Dpsi|^4=29023/1071630,
    E|Pi_(Rperp)Dpsi|^2=4/45.

Consequently

    beta_rho=sqrt(rho) beta_psi,
    h_rho=rho h_psi,
    beta_rho^2/(2h_rho)=80089/21313530>0,
    ||X_rho||_4^4=1/2+29023/1071630.                         (6.4)

The covariance and averaged Hessian are positive definite for rho>0, as checked in the prior replay. But for every 1<=p<4,

    ||Y_rho||_p=rho^(2/p-1/2)||Y_psi||_p ->0.

Thus no estimate obtained by replacing ||Y||_4 in (4.1) with ||Y||_p, p<4, while retaining the other factors and a uniform constant, can hold. This proves sharpness of the transverse integrability threshold for this form of estimate. It is not a statement about optimal numerical constants, nor a quasiconvexity counterexample.

## 7. What the nonlinear shear does and does not reduce

Let R=a0 tensor b0, A invertible, and b0.A^{-1}a0=0. For a periodic smooth h, set

    Psi(x)=x+A^{-1}a0 h(b0.x),
    Psi^(-1)(x)=x-A^{-1}a0 h(b0.x),
    S_h=I+A^{-1}a0 tensor b0 h'(b0.x).

Both Jacobians have determinant one. The map

    w -> v=w o Psi^(-1)

is a bijection of periodic W1,4 residual potentials for a fixed smooth shear. Since

    A Psi(x)+w(x)=Ax+a0h(b0.x)+w(x),

the chain rule and change of variables give

    int F(A+Rh'+Dw)=int F((A+Dv)S_h).                       (7.1)

For fixed h, w ranges over all periodic residuals, and a0h+w likewise ranges over all periodic potentials. Therefore

    inf_v int[F((A+Dv)S_h)-F(A)]
      =inf_phi int[F(A+Dphi)-F(A)].                         (7.2)

This is an exact conjugacy. It does not discard gradient compatibility, but it does not reduce the unrestricted admissible class either. Additional quantitative information about v or the correlation with S_h must be proved, not assumed.

A tempting stronger inequality with the frozen reference F(AS_h) is false even for F(B)=|B|^4. Set A=I, R=e12, h'=k cos y, and choose v=-e1 h(y). Then

    (I+Dv)S_h=I,
    int[|(I+Dv)S_h|^4-|S_h|^4]
       =-2k^2-(3/8)k^4<0 for k!=0.                        (7.3)

Every frozen integrand B->|B S_h(x)|^4 is convex. The negative difference comes from the spatially varying reference, not from failure of ordinary quasiconvexity. The correct fixed reference F(A) in (7.2) has not been changed.

The present positive theorem instead works on the original compatible field, using its differential Hodge correction and mixed derivative. It does not require a large nonlinear shear to become small in transformed coordinates.

## 8. What is still missing

For a fixed contact with simple kernel, write the averaged Hessian and cubic vector in its background decomposition as

    H=[[h,k^T],[k,D]], b=(beta,gamma), D>0.

The full optimized gap is

    c-(1/2)gamma^T D^(-1)gamma
      -(1/2)(beta-k^T D^(-1)gamma)^2/(h-k^T D^(-1)k).        (8.1)

The new estimate controls beta relative to h, and controls the cross term involving the distinguished rank-one R. It does not give the corresponding estimate for the moving reduced numerator and reduced denominator in (8.1). The latter denominator can be much smaller than h. Replacing it by h would reverse the needed control.

Therefore (5.8) is not promoted to continuity of b^T H^dagger b, and (5.4) is not promoted to unrestricted quasiconvexity. Two affine-background directions and their coupling remain outside its conclusion. Concentrated transverse L4 mass is also not removed by covariance collapse.

A precise remaining operation is a compatibility estimate stable under simultaneous elimination of the positive background block, or a decomposition that separates that coupled residual into genuinely nonnegative profiles with controlled errors. The finite disjoint-profile superadditivity from the previous note is not such a decomposition theorem. The competing route is an actual gradient realizing a negative value of (8.1); determinant-balanced laws are insufficient, as (6.3) demonstrates.

Every putative counterexample can be moved to the acoustic boundary by subtracting the largest nonnegative multiple of |A|^4 preserving rank-one convexity. The multiple is the minimum of a continuous ratio of acoustic forms over unit backgrounds and unit rank-one directions, so it is attained. The subtracted term is quasiconvex; a negative gap remains negative. This elementary boundary reduction explains why contact estimates are relevant even when one starts with a strictly rank-one-convex integrand. It does not align the optimizing background with that contact automatically.

## 9. Literature, verification and priority

The reconstruction uses the classical indefinite Finsler lemma, not a new quadratic S-lemma. Tartar-type cubic and fourth-order resonance conditions have foundational antecedents in Gutiérrez (2006). The Hodge correction and mixed-derivative interpolation are established analytic constructions. The new mathematical claim here is the quantitative contact estimate, its application to the complete invariant contact geometry, the unrestricted-size contact-plane Jensen theorem, and the sharp transverse integrability test.

Bruno and Pasqualotto's August 2026 paper proves the Dacorogna-Marcellini theorem and the class with both left and right rotational invariance using heat flow and exact forms. That theorem does not cover the entire left-invariant cone, and its proof is not imported as a universal flow argument.

Concentration and generalized gradient Young measures have extensive prior theory. In particular, characterizations stated through all quasiconvex test functions cannot be used here to infer Jensen for a function whose quasiconvexity is the unknown conclusion. No such circular import is made.

Sources inspected:

1. T. J. Meijer et al., A General Non-Strict Finsler's Lemma, arXiv:2403.10306v1, especially the established indefinite case in Lemma 2. https://arxiv.org/html/2403.10306v1
2. S. Gutierrez, A Necessary Condition for the Quasiconvexity of Polynomials of Degree Four, Journal of Convex Analysis 13 (2006), 51-60. The primary PDF was read, including the planar cubic-contact discussion. https://www.heldermann-verlag.de/jca/jca13/jca0514_b.pdf
3. D. D. Haroske and H.-J. Schmeisser, Gagliardo-Nirenberg Inequalities for Spaces with Dominating Mixed Derivatives, in Function Spaces and Inequalities (2017), 117-135. The publisher record was inspected for related theory; Lemma 3.1 is proved above rather than asserted to be its verbatim theorem. https://doi.org/10.1007/978-981-10-6119-6_5
4. G. Bruno and F. Pasqualotto, Quasiconvexity for the Dacorogna-Marcellini Energy, arXiv:2608.06367v1. https://arxiv.org/html/2608.06367v1
5. A. Guerra and R. Teixeira da Costa, Numerical evidence towards a positive answer to Morrey's problem, arXiv:2006.09063v1. https://arxiv.org/html/2006.09063v1
6. J. Kristensen and F. Rindler, Characterization of Generalized Gradient Young Measures Generated by Sequences in W1,1 and BV, Archive for Rational Mechanics and Analysis 197 (2010), 539-598, with its published correction. Publisher abstract inspected for scope, not used as an L4 theorem. https://doi.org/10.1007/s00205-009-0287-9
7. Prior conversation artifact: ASTRA_POSITIVE_DEFINITE_BARRIER.md. Its contact classification was reconstructed in Section 2, and its standalone checker was replayed successfully.

A fetch of the older Chen-Ditzian primary PDF failed. No statement is attributed to unread details of that paper. The search did not establish historical novelty of the main combination. Absence of a matching search result is not priority clearance.

Run:

    python verify_contact_compensation.py

The new standalone verifier uses SymPy, with definitions written directly in the script. Nine groups passed: the new low-rank convex reconstruction; the explicit G contact cubic; its full rational acoustic certificate; compatibility of the Hodge correction; a nonzero genuinely resonant cubic; the incompatible-law obstruction; exact concentrated-profile moments and exponent obstruction; shear conjugacy algebra; and the pure-line margin used in Theorem 5.1.

The analytic complex interpolation, multiplier bounds, density, contact classification and variational estimates are proved in this note, not certified by the finite checks. The previous twelve-group verifier was also actually replayed; its log is supplied. No repository publication, external review, formal proof or complete quasiconvexity solution is claimed.
