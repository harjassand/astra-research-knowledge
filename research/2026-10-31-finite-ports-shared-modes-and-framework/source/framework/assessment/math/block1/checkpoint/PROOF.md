# Proofs and exact scope

## 1. Coordinates and the entire cubic space

Use x=a+d, y=c-b, u=a-d, v=c+b. Then

    T=(r+t)/2,  det A=(r-t)/4,
    3F_(1/3)=t²+2rt=:F.

A matrix direction is rank one exactly when its z and w components have the same length. Nonzero such directions can therefore be normalized to R=(a,b) with |a|=|b|=1. Direct differentiation gives

    F''(R) = [[4I, 8abᵀ],
              [8baᵀ, 8I+8bbᵀ]].                         (4)

It is PSD, rank three, with kernel span{(a,-b/2)}. Its positive eigenvalues are 4,8,20. The rank and gap are uniform on the two circles.

For any globally ROC F+C+Q, the supplied acoustic argument requires ∇C(R)·(a,-b/2)=0. This condition also suffices for the range condition at every R, since (4) has precisely this kernel.

Decompose a homogeneous cubic by z-degree, C=C₀+C₁+C₂+C₃. Euler's identity makes the acoustic condition

    -C₀+C₂+2C₃=0 on r=t.

Consequently -C₀+C₂+2C₃=(r-t)ℓ for a linear ℓ. Divisibility follows, for example, by polynomial division in x and evaluating the remainder at both real roots x=±sqrt(t-y²) on the open set t>y². Comparing z-degrees first forces ℓ's z-part to vanish, then gives

    C₃=0, C₂=rℓ(w), C₀=tℓ(w),
    C=C₁(z,w,w)+(r+t)ℓ(w).                            (5)

The unrestricted C₁ has six coefficients. Its two trace components are t times a linear function of z, and its other four are zᵀMν(w). The trace components and the two components of (r+t)ℓ(w) are precisely the four independent derivatives

    F_x=4xt, F_y=4yt, F_u=4u(r+t), F_v=4v(r+t).

Hence uniquely C=DF·V+zᵀMν(w). This identifies the entire eight-dimensional acoustic space in explicit coordinates. Every M is realized by a globally ROC polynomial by the isotropic threshold proved below.

Apply the actual argument translation P(B-V). Its cubic becomes C_M(B)=zᵀMν(w), and its quadratic is

    Qnew=Q-DC·V+(1/2)D²F[V,V].                        (6)

Affine terms are irrelevant. Translation preserves ROC and QC, so no conclusion has been obtained by subtracting a QC function from a ROC function. Formula (6) is implemented and replayed exactly.

## 2. Sharp quadratic membership

Let J be rotation through pi/2. For unit a,b define

    n=ν(b), e=Jn,
    c=aᵀMn, d=(Ja)ᵀMn, e₀=aᵀMe.

For C_M=zᵀMν(w), the components of ∇C_M(R) in the orthonormal directions (a,Ja;b,Jb) are (c,d;2c,2e₀). Formula (4) acts on the (a,b) plane as 4(1,2)(1,2)ᵀ, on Ja by 4, and on Jb by 8. Therefore

    ∇C_M(R)ᵀ F''(R)^+ ∇C_M(R)
       =(c²+d²)/4+e₀²/2
       =|Mn|²/4+(aᵀMe)²/2.                          (7)

The supplied exact rank-one elimination now proves (2). This is a closed evaluated cost, not an unevaluated pseudoinverse condition. Its constant-rank geometry excludes the hidden limiting penalties present in the different Hopf source.

There is also an elementary direct completion. Write a background as z=αa+βJa, w=γb+δJb. Then

    P''(A)[R,R]
       =4(α+2γ+c/4)²+4(β+d/4)²+8(δ+e₀/4)²
        +2Q(R)-|Mn|²/4-e₀²/2.                       (8)

Thus the last scalar is the exact residual, including equality. Arbitrary nonzero R follows by common scaling of its two components.

For Q=αr+βt the left side of (2) is 8(α+β). Maximize first over a to obtain |Mn|²+2|Me|². Since n,e are orthonormal, this equals 2tr(MᵀM)-|Mn|². Its maximum is 2σ₁²+σ₂², attained by taking n in a smallest-singular-value direction. This proves the stated sharp threshold, including singular M and M=0.

## 3. Finite operation for every rational quadratic

Put

    a=(1-h²,2h)/(1+h²), b=(1-k²,2k)/(1+k²).

The two omitted circle points follow by continuity. Multiply the difference in (2) by the strictly positive denominator (1+h²)²(1+k²)⁴. The resulting P(h,k) is a rational polynomial of h-degree ≤4 and k-degree ≤8. Hence the test remains exact at weak boundaries.

Here is a complete finite sign decision, implemented in `classify.py`.

1. Square-free-decompose P over Q[h,k], retaining the multiplicities in P itself.
2. Project to k the leading h-coefficients, h-discriminants, pairwise h-resultants, and any factors depending only on k. Form the square-free least common multiple of all nonconstant nonzero projections.
3. Isolate its finitely many real roots exactly. Choose a rational sample in each open complementary interval.
4. At each sample, decide nonnegativity in h by its leading sign, even degree, and Sturm counts of the factors of odd multiplicity.

On an open projection cell, no degree drop, repeated h-root, crossing between factors, or content zero can occur. The real-root multiplicities and polynomial signs are therefore constant in the sense needed for univariate nonnegativity. All cells passing is sufficient: any strictly negative value on an excluded projection fiber would persist in a neighboring open cell by continuity. This is why the operation need not evaluate algebraic-coefficient boundary fibers, and still handles identically zero and repeated factors honestly. It terminates for every rational input. It is not claimed to be optimal in complexity.

The classifier first applies the exact normalizer (6); a cubic outside (5) is rejected regardless of Q. Its scope is the actual full lower quadratic, with all cross terms and determinant lineality allowed.

## 4. A globally ROC, non-polyconvex boundary member

Let

    P₀=F+x(u²-v²)+2yuv+(3/16)(r+t).

This is M=I, at the exact threshold. Indeed (2)'s residual is

    3-1-2(aᵀJn)²=2(aᵀn)²≥0.

No finite-grid admission is involved.

Set δ=r-t and

    A₀=(-1/4,0,0,-1/4), R=(0,1,1,0),
    B₀=(-11/20,0,0,-1/8).

R is an actual rank-one matrix direction because its conformal and anticonformal components both have norm one. Exact differentiation gives

    RᵀP₀''(A₀)R=0,
    P₀''(A₀)R=(1/16)δ''R=(0,1/8,-1/8,0).

If P₀ were polyconvex, a convex minor lift would give a multiplier λ with

    P₀(B)-P₀(A₀)-DP₀(A₀)·(B-A₀)-λδ(B-A₀)≥0          (9)

for every B. There is no restriction here to polynomial lifts. A convex lift finite on the minors graph is finite everywhere: any (B,s) is the average of graph points B+Y,B-Y after choosing δ(Y)=s-δ(B). It consequently has a subgradient at the graph point under consideration. Restricting this subgradient to the graph gives (9).

The Hessian of (9) at B=A₀ is PSD. Its zero quadratic value on R therefore forces its entire R-column to vanish. The displayed derivative identity uniquely gives λ=1/16. But direct evaluation at B₀ yields

    P₀(B₀)-P₀(A₀)-DP₀(A₀)·(B₀-A₀)
        -(1/16)δ(B₀-A₀)=-3/20480<0.

This proves non-polyconvexity. It does not furnish a gradient Young measure or a compatible energy violation. In the original task normalization p₀=P₀/3 and its quadratic is T/8.

## 5. Exhaustive failure of polynomial differential-form heat corrections

For a compatible Hessian h=(u¹_xx,u¹_xy,u¹_yy,u²_xx,u²_xy,u²_yy), define

    X=(h₀+h₄,h₃-h₁,h₀-h₄,h₃+h₁),
    Y=(h₁+h₅,h₄-h₂,h₁-h₅,h₄+h₂).

These are the x- and y-derivatives of (z,w). A closed two-form Ω gives the corrected heat density

    B(A)[h,h]=P₀''(A)[X,X]+P₀''(A)[Y,Y]+Ω_A(X,Y).     (10)

A globally PSD (10) would prove QC by ordinary heat flow and Stokes. We prove that no polynomial Ω can do so.

P₀ is invariant under z→exp(2iθ)z, w→exp(iθ)w. This is an actual proper output/domain rotation action, so averaging a putative certificate preserves closedness and positivity. Polynomial closed forms have polynomial primitives by radial contraction; averaging commutes with this construction.

Write az=(-y,x,0,0), aw=(0,0,-v,u), rw=(0,0,u,v). Modulo exact one-form gauges, the invariant primitive components of degrees three, two and one are exhaustively

    α₃=q₀r az+q₁t az+q₂r aw+q₃t aw+q₄r rw,
    α₂=f(0,0,xu+yv,yu-xv)+g(0,0,xv-yu,xu+yv),
    α₁=(j/2)az+(k/2)aw.                            (11)

These are coefficient vectors of one-forms. Completeness follows by weights: z has weight two and w weight one. For degree three, the invariant angular terms are r az,t az,r aw,t aw, with one remaining radial cross term after removing differentials of r²,rt,t². At degree two the resonance z-bar times w² gives four real forms and two exact gauges, leaving the two displayed forms. Degree one leaves the two angular forms.

Every leading acoustic null must annihilate the whole leading density matrix if it is PSD. Substitution of the actual acoustic pairs K=U diag(1/3,1)Vᵀ and plane-wave Hessians gives the necessary identities

    q₀=q₁/8+3/2, q₂=6-q₃, q₄=0.                   (12)

Sixteen literal rational pairs suffice for these necessary linear identities; the receiver reconstructs them.

More importantly, P₀ has an actual rank-one Hessian zero at every

    A*(τ)=(-1/4,τ,-τ/2,-1/4),

in the fixed direction R=(0,1,1,0). The compatible plane-wave Hessian h*=(1,-1,1,1,-1,1) has (X,Y) proportional to R and -R. Thus the wedge term vanishes on its quadratic score. Positivity of (10) forces the entire h* column to vanish for all τ. Solving these exact polynomial-in-τ identities yields

    f=0,
    g=16j/3+8k/3+8,
    q₁=-32j/9+32k/9+4,
    q₃=64j/9+8k/9+12.                              (13)

Now only two necessary scalar PSD tests are needed. At A=0, use h=(0,-1,0,1,0,-1). Equations (12)–(13) give

    B(0)[h,h]=4j+3≥0.

In the homogeneous leading density, at (z,w)=(0,1), use h=(-5,0,7,0,1,0). The score is

    -64(24j+19)≥0.

They imply j≥-3/4 and j≤-19/24, a strict contradiction. `heat_obstruction.py` reconstructs (10)–(13) and both scores using exact symbolic arithmetic.

Higher polynomial degrees cannot evade this argument. If a highest-degree corrected density has degree m>2 in A, positivity under A→ρA makes its leading matrix PSD (or identically zero when the parity forces this). Its score on every plane-wave Hessian is zero because it comes only from a two-form evaluated on proportional X,Y. A PSD matrix with zero score on a vector annihilates that vector. Plane-wave Hessians span the entire six-dimensional Hessian space, so this leading matrix is zero. Discard that invisible homogeneous correction and descend to degree at most two in Ω, exactly the primitive class (11).

This proves absence of every polynomial closed-form correction of this type, rather than failure of just the supplied primary primitive. It says nothing against angular/nonpolynomial corrections, a different compatible evolution, or QC itself. The successful primary homogeneous heat certificate remains valid.

## 6. Sources and remaining frontier

The frozen task and `math/rotational_faces/PROOF.txt` supply F_s, the exceptional rank eight, acoustic range necessity, full-space exposure and the nonexceptional translation theorem. `math/quadratic_boundary/PROOF.txt` supplies general Schur elimination and compatible moment reduction; its different eight-mode detector has not been imported. `math/primary_appendix.html`, Bruno–Pasqualotto, arXiv:2608.06367v1, Appendix A, supplies the governing compatible heat mechanism and homogeneous QC certificate. The supporting-minor argument for general finite lifts is also explained in the frozen Hopf proof.

The normal form, evaluated exceptional cost, finite boundary operation, sharp singular-value threshold, explicit admitted non-PC member and exhaustive polynomial-heat obstruction above were derived and exactly checked in this tranche. They are internal mathematical results at their stated scope, with no external priority determination.

The central question remains whether all normal-form polynomials admitted by (2) are QC. P₀ is a concrete sharp-boundary instance for which the standard polynomial heat strategy is provably insufficient. No compatible counterexample has been constructed, and no arbitrary matrix distribution has been treated as a gradient.
