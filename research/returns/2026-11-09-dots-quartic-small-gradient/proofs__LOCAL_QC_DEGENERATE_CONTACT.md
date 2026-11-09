# Local quasiconvexity at the original quartic's degenerate contact

Date: 9 November 2026.
Status: hand-derived analytic proof candidate. No numerical optimization, solver, scientific execution, experimental validation, historical-priority claim, or global quasiconvexity claim is made. The mixed-derivative interpolation premise and principal estimate have been discussed analytically with a reviewing reader. The all-mean corollary explicitly imports the original source's strict acoustic statement away from the coordinate axes.

## 1. Exact original density and statement

Let k>1/3, equivalently k=(2r+1)/3 with r>0. Put

    B=(3k-1)/(8(k+1)),  F0=(5k+1)/(2(k+1)),
    m=3k+1,  q=m/(2k),  D=(3k-1)(k+1)/4.

For F=[[a,b],[c,d]], set u=a^2+c^2, v=b^2+d^2, j=ad-bc and

    J(F)=B[k^2 u^2+v^2+2uv+4k u j-4v j]+F0 j^2.

This is the original J_r, not a corrected or restricted density. Let

    A=[[0,k],[1,0]].

THEOREM (local, general compatible perturbations). There exists delta_k>0 such that, on every periodic square T, every periodic Lipschitz vector field phi with ||Dphi||_infinity<=delta_k satisfies

    integral_T [J(A+Dphi)-J(A)]
      >= (1/2) integral_T Q(Dphi) + (c_k/2) integral_T |Dphi|^4,

where

    Q(X)=[m b+2k c]^2/4+D d^2,
    c_k=(3k-1) min(k^2,1)/[4(5k+1)]>0,
    X=[[a,b],[c,d]].

The norm in the smallness condition is the Frobenius norm. The same conclusion holds for compactly supported Lipschitz perturbations after zero extension into a square, including the usual smooth compactly supported quasiconvexity tests. Section 6 gives a positive radius in terms of explicitly declared finite harmonic-analysis constants. Those constants have not been evaluated, so no evaluated numerical radius is claimed.

There is NO constraint m b+2k c=0 in this theorem. This distinction matters: that constraint is a coordinate-transformed previously admitted U-free class for some parameters. The theorem permits arbitrary compatible normal coupling, but only for sufficiently small gradient amplitude at this affine mean.

## 2. Exact algebra and global quartic coercivity

Write s=m b+2k c and lambda=-(3/2)k(k+1). Direct expansion gives

    J(A+X)-J(A)-DJ(A):X-lambda det X
      =Q(X)+T3(X)+J(X),

where

    T3(X) = [(3k-1)b^3+(9k+1)b^2 c+4k b c^2
              +(3k-1)(b+c)d^2]/2 -s a d.

In particular, the cubic contains neither a^2 b nor a^2 c. These cancellations, and not a strict angular quadratic lower bound, are used below.

A useful positive identity valid for every matrix X is

    J(X)=B(ku-v+2j)^2+[(3k-1)/4]uv+j^2.

Indeed, F0-4B=1 and 2B(k+1)=(3k-1)/4. Completing the square in j gives

    B(p+2j)^2+j^2 >= [B/(1+4B)]p^2,
    B/(1+4B)=(3k-1)/[4(5k+1)].

Taking p=ku-v, therefore,

    J(X) >= [(3k-1)/(4(5k+1))]
             [k^2u^2+v^2+(3k+1)uv]
         >= c_k (u+v)^2 = c_k |X|^4.

The last inequality uses 3k+1>2 and min(k^2,1)<=1. This proves the asserted coercivity constant; it does not rely on a claimed sum-of-squares certificate for the Jensen remainder.

For a periodic gradient, the integrals of DJ(A):Dphi and det Dphi vanish. Thus the Jensen gap is exactly the integral of Q+T3+J.

## 3. Finite-exponent mixed-derivative interpolation

LEMMA. There is a finite constant I, independent of the side length of a square torus, such that every smooth periodic scalar psi satisfies

    ||psi_xy||_3 <= I ||psi_xx||_6^(1/2) ||psi_yy||_2^(1/2).       (MI)

All norms here and below use unnormalized Lebesgue measure.

Proof. It suffices first to consider a trigonometric polynomial. Remove its Fourier modes with zero x frequency or zero y frequency, using the product of the two projections I-E_x and I-E_y. This does not change psi_xy, and both projections are bounded on every finite Lp used here. Their endpoint norm costs are absorbed into I.

On the remaining modes define the analytic family

    F(z)=|D_x|^(2z) |D_y|^(2(1-z)) psi,   0<=Re z<=1.

At z=it, this is |D_x|^(2it)|D_y|^(-2it) applied to |D_y|^2 psi. At z=1+it, it is the same imaginary-power multiplier applied to |D_x|^2 psi. Coordinate imaginary powers are bounded on Lp for 1<p<infinity, with at most polynomial growth in |t|, by the one-dimensional Marcinkiewicz multiplier theorem and Fubini. Their product retains such a bound. A Gaussian damping factor in the strip removes this polynomial growth. The vector-valued three-lines/complex-interpolation inequality, with endpoint exponents 2 and 6, consequently gives

    || |D_x| |D_y| psi ||_3
      <= C || |D_y|^2 psi ||_2^(1/2)
             || |D_x|^2 psi ||_6^(1/2),

because 1/3=(1/2)(1/2)+(1/2)(1/6). Normalizing the analytic family by a scalar exponential gives the displayed geometric mean rather than the maximum of the endpoint norms. The product of the two periodic Hilbert transforms converts |D_x||D_y| psi into psi_xy, and is bounded on L3. This proves (MI) for polynomials. Smooth Fourier approximation proves the stated lemma; the same inequality extends whenever the endpoint derivative norms are finite.

There is no L-infinity interpolation endpoint. In particular, no assertion that a Hodge or Riesz projection is bounded on L-infinity is used. Isotropic rescaling of the square preserves the inequality and its constant: the derivative orders and the relation between the three exponents give the same scaling on both sides.

## 4. Hodge projection and quantitative constants

For p in {2,3,6}, fix a finite constant K_p such that, on every square torus, the mean-zero scalar equation Delta eta=f implies

    ||D(nabla_perp eta)||_p <= K_p ||f||_p.

Here nabla_perp eta=(-eta_y,eta_x), and the matrix norm is Frobenius. Standard periodic Calderon-Zygmund estimates supply these order-zero operator bounds, uniformly under isotropic changes of the square's side length. Declare

    H_p=K_p/m,
    ell=m+2k=5k+1,
    L=1/(q sqrt(D))+2H_2,
    h=2^(1/3) ell^(2/3) H_6,
    U=sqrt(2) I^3 L^(3/2),
    P=4(1+q^3)U,
    R=4(1+q^3)[U h^(3/2)+4 ell H_3^3].

These are finite positive constants depending only on k and the declared finite-exponent operator constants.

For X=Dphi, abbreviate

    delta=||X||_infinity,
    M=integral |X|^4,
    mathcal_Q=integral Q(X).

The elementary estimates used below are

    ||s||_2<=2 sqrt(mathcal_Q),
    ||d||_2<=D^(-1/2) sqrt(mathcal_Q),
    ||s||_infinity<=ell delta,
    ||s||_3^3<=4 ell delta mathcal_Q,
    ||s||_6<=2^(1/3)ell^(2/3)delta^(2/3)mathcal_Q^(1/6),
    ||a||_6<=delta^(1/3) M^(1/6).

Set w=(phi_1,-phi_2/q). Its curl is

    curl w=-c/q-b=-s/m.

The periodic Hodge decomposition, retaining an irrelevant constant vector if necessary, is

    w=constant+nabla psi+e,  e=nabla_perp eta.

It follows that

    ||De||_p<=H_p||s||_p,   p=2,3,6.

Comparing components gives

    a=psi_xx+e_1x,       b=psi_xy+e_1y,
    c=-q(psi_xy+e_2x),   d=-q(psi_yy+e_2y).

Hence

    ||psi_yy||_2<=L mathcal_Q^(1/2),
    ||psi_xx||_6
      <=delta^(1/3)M^(1/6)+h delta^(2/3)mathcal_Q^(1/6).

Apply (MI), cube, and use (x+y)^(3/2)<=sqrt(2)(x^(3/2)+y^(3/2)). This yields

    integral |psi_xy|^3
      <=U delta^(1/2)M^(1/4)mathcal_Q^(3/4)
        +U h^(3/2)delta mathcal_Q.

Also

    integral |e_1y|^3, integral |e_2x|^3
      <=4 ell H_3^3 delta mathcal_Q.

Using |x+y|^3<=4(|x|^3+|y|^3) in the two component identities proves

    integral (|b|^3+|c|^3)
      <=P delta^(1/2)M^(1/4)mathcal_Q^(3/4)
        +R delta mathcal_Q.                                  (H)

Only the ORIGINAL gradient is bounded in L-infinity throughout this argument. The projected Hessian is estimated in L6, L3 and L2.

## 5. The cubic bound

The coefficients of the first three monomials in T3 have total absolute value

    (3k-1)/2+(9k+1)/2+2k=8k.

Each corresponding absolute monomial is at most |b|^3+|c|^3. The remaining terms satisfy

    [(3k-1)/2] integral |b+c|d^2
       <=[(3k-1)/D] delta mathcal_Q,

    integral |s a d| <=[2/sqrt(D)] delta mathcal_Q.

Consequently, with the declared constants

    C1=8kP,
    C2=8kR+(3k-1)/D+2/sqrt(D),

one has

    |integral T3(X)|
      <=C1 delta^(1/2)M^(1/4)mathcal_Q^(3/4)
        +C2 delta mathcal_Q.                                 (C)

This direct absolute-cubic estimate avoids any separate difference-of-cubes argument or product of an L-infinity Hodge projection with another factor.

## 6. Explicit unevaluated radius and conclusion

Choose

    delta_k=min{1, (2c_k/C1)^2, 1/(9C1^2), 1/(4C2)}.

This is an explicit positive expression in the declared finite constants, not an evaluated numerical radius.

By the exact expansion, the null-Lagrangian identities, quartic coercivity, and (C),

    Jensen gap >= mathcal_Q+c_k M
                  -C1 sqrt(delta) M^(1/4)mathcal_Q^(3/4)
                  -C2 delta mathcal_Q.

Weighted Young's inequality gives

    M^(1/4)mathcal_Q^(3/4)<=(M+3mathcal_Q)/4.

For delta<=delta_k, the coefficient of M is at least c_k/2. The losses from mathcal_Q are at most 1/4 from the mixed term and 1/4 from C2 delta. Therefore

    Jensen gap >= mathcal_Q/2+c_k M/2,

as claimed. The argument does not divide by M or mathcal_Q, so it includes their zero cases.

For Lipschitz periodic fields, periodic mollification preserves the gradient supremum bound and converges in every finite Lp. The polynomial integrals therefore converge, giving the same inequality. Smooth compactly supported tests can be extended by zero into any containing square. The same reasoning applies to Lipschitz zero extensions where these are admissible, in particular the usual zero-boundary Lipschitz test class on a bounded Lipschitz domain. No boundary constant or square-size dependent radius is introduced.

## 7. All-mean local corollary: imported premise and independently checked parts

The original ROC source, as reported and checked in the source analysis, supplies this additional strict statement:

    D^2J(e1 tensor (1,t)) is positive definite whenever
    t is finite and nonzero, for every k>1/3.

This is stronger than merely saying J is rank-one convex. The corollary below relies on that strict statement; rank-one convexity alone would not establish its classification. Its positive-principal-minor calculation is imported from the original source, not re-executed here.

The axis calculations can be checked independently by differentiating the displayed density. In coordinates (a,b,c,d), D^2J(E11) has no couplings between its (a,d) and (b,c) blocks. The blocks are

    (a,d): [[12Bk^2,12Bk],[12Bk,4B+2F0]],
    (b,c): 4B[[1,-k],[-k,k^2]].

The first has determinant 24Bk^2 because F0-4B=1. Thus this Hessian is positive semidefinite with kernel span{A}.

Likewise, D^2J(E12) has blocks

    (a,d): 4B[[1,-1],[-1,1]],
    (b,c): [[12B,12B],[12B,4B+2F0]].

The second has determinant 24B. Its kernel is span{I}.

For a homogeneous quartic, polarization gives

    D^2J(F)[H,H]=D^2J(H)[F,F].

J is invariant under left multiplication by SO(2). Every nonzero rank-one H can thus be reduced by a proper target rotation and a scalar to either e1 tensor (1,t), with t finite, or E12. The imported strict statement and the two computed axis kernels show that every nonzero affine mean with an acoustic zero is of one of the forms

    F=t O A  or  F=t O I,
    t nonzero, O in SO(2).

There are no other nonzero degenerate means, conditional on the stated source premise. The two classes have opposite determinant signs; neither may silently be omitted.

To transfer the local theorem from A to I, use R=A. Direct substitution gives

    J(FR)=k^2J(F),  R^2=kI.

Indeed, right multiplication changes (u,v,j) to (v,k^2u,-kj), and the displayed density transforms by the factor k^2. Therefore

    J(I+X)=k^(-2)J(A+XR).

For X=Dphi, XR becomes a gradient after the invertible domain change x=Ry. The local theorem is valid for arbitrary compactly supported test domains by zero extension, so no periodic-lattice issue is needed for this transfer. A valid radius at I is delta_k/||R||_op=delta_k/max(k,1). Homogeneity and target SO(2) invariance give positive local radii at tOA and tOI by scaling the perturbation by |t| and rotating its target.

At any remaining nonzero mean F, the acoustic form is strictly positive on the compact product of unit target and frequency vectors. Let its positive minimum be alpha_F. Fourier/Plancherel gives

    (1/2)integral D^2J(F)[Dphi,Dphi]
       >=(alpha_F/2)integral|Dphi|^2.

The cubic Taylor term is bounded by C_F ||Dphi||_infinity integral|Dphi|^2, and the quartic remainder J(Dphi) is nonnegative. A sufficiently small positive radius therefore gives local quasiconvexity at that F. At F=0, quartic coercivity supplies the inequality for every amplitude.

COROLLARY, with the imported strict source premise: every affine mean F has some positive local gradient-supremum radius on which the original J is quasiconvex. No uniform radius relative to |F| over all nonzero means has been proved here. Most importantly, local quasiconvexity at every mean is NOT the unrestricted quasiconvexity inequality: the permitted perturbation amplitude depends on the mean and is bounded.

## 8. Optional anisotropic expansion and overlap qualification

The contact acoustic determinant has fourth-order frequency tilt. The positive local proof above does not replace it by a positive second-order angular coefficient.

For tau=1/N and fixed smooth periodic scalar profiles psi,chi, define

    phi_tau(x,y)=(tau^3 psi_x(Nx,y),
                  -q tau^4 psi_y(Nx,y)+tau^5 chi(Nx,y)).

The gradient is exactly compatible and its normal component is s=2k tau^4 chi_x. Direct use of the Taylor expansion gives the averaged Jensen gap

    tau^8 [Bk^2 <psi_xx^4>+Dq^2 <psi_yy^2>+k^2 <chi_x^2>]
    +tau^9 [-(D/k)<psi_xy^3>-2Dq<psi_yy chi_y>]
    +O_{psi,chi,k}(tau^10).

Thus the first nonzero effective energy is positive, including the first nonzero normal correction; the indefinite coupling occurs one order later. Setting chi=0 imposes s=0, which overlaps the transformed previously admitted U-free class and must not be presented as an independent global result. The main local theorem above is the general-s statement.

## 9. Scope, sources, and work status

The exact original density and the axis/contact conventions are pinned in the companion PROOF_CANDIDATE.md. Its source ledger identifies the original ROC proof as

    research/2026-10-31-coupled-quartic-extension-original-roc-and-fixed-fiber-cost/source/final/outputs/quartic_coupling/PROOF.txt
    Astra pin bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e
    SHA256 948c720458f8e1eafd1da31442603dae912797a5bd1395f7a2156a5274ab9ff1.

The source analysis identified prior fixed-contact cubic compensation and curved-phase work, especially N806 CONTACT_COMPENSATION.md and N812 GLOBAL_COMPATIBILITY.md. Their relationship to this finite-exponent Hodge argument must be checked before asserting novelty. The all-mean classification specifically imports the source's strict finite-nonzero-t Hessian statement and separately checks both axis kernels.

This note is a new analytic deliverable candidate, not a global Morrey solution, not a negative Jensen field, and not a scientific execution record. File creation is documentation only. No solver or numerical optimization was run. Independent final review remains necessary before treating the proof and corollary as established.
