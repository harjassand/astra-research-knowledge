# Proof of the acquired global QC class

## 1. What is certified exactly

Use the conformal coordinates and normalization of the checkpoint: z=(x,y), w=(u,v), r=|z|², t=|w|², F=t²+2rt. Let

    C₊=x(u²-v²)+2yuv, C₋=x(u²-v²)-2yuv,
    κ₊=99/500, κ₋=27/100,
    P₊=F+C₊+κ₊(r+t), P₋=F+C₋+κ₋(r+t).

Both are globally QC. The literal certificates are the files `sos_certificate_99_500.txt` and `sos_minus_certificate_27_100.txt`.

For an actual map U:R²→R² write its compatible Hessian

    h=(U¹_xx,U¹_xy,U¹_yy,U²_xx,U²_xy,U²_yy).

The two derivatives of its conformal gradient coordinates are

    X=(h₀+h₄,h₃-h₁,h₀-h₄,h₃+h₁),
    Y=(h₁+h₅,h₄-h₂,h₁-h₅,h₄+h₂).

The certificate gives a polynomial one-form α on gradient space and eighteen polynomial features L(A,h), each linear in h and of degree at most one in A. Its full identity is

    P''(A)[X,X]+P''(A)[Y,Y]+dα_A(X,Y)=L(A,h)ᵀ G L(A,h),     (1)

where G is a symmetric positive definite rational 18×18 matrix. This is an identity in all ten real variables A,h. In particular it includes every mean, every gradient, all degenerate acoustic directions and zero.

`receive.py` reads only the literal certificate data, reconstructs P'', dα and the actual compatibility maps X,Y, expands the difference of the two sides of (1), and requires every polynomial coefficient to vanish. It then performs exact rational LDL elimination on G and checks every pivot strictly positive. It trusts neither an optimizer status nor any sampled eigenvalue. Both certificates pass this replay.

For a periodic test map U=Mx+φ evolve φ by ordinary componentwise heat. The derivative of its P-energy is minus the integral of the uncorrected part of (1). The pullback of dα has zero integral by Stokes. Thus the energy is nonincreasing and converges to P(M). The usual periodic-to-compact-test argument gives QC. This is precisely the compatible heat mechanism supplied in the frozen primary source, applied here to newly acquired nonhomogeneous primitives.

The first-tranche obstruction concerned λ=3/16. The new certificate at λ=99/500 is a different polynomial. No assertion contradicting that obstruction is needed.

## 2. How the finite lift was constructed

Let R=ξ⊗η, K=U_ξ diag(1/3,1)V_ηᵀ be the actual leading acoustic pair. A plane-wave compatible Hessian has coordinates ξ⊗η⊗η. If a pointwise PSD leading heat density has zero score there, each square in a bilinear SOS must vanish there.

Start with the twenty-four bilinear monomials A_i h_j. Substitute A=K and h=ξ⊗η⊗η, expand in ξ,η, and take the exact kernel of the resulting coefficient matrix. Its dimension is twelve. The twelve literal kernel vectors define the first twelve features of L; the last six features are h itself. This is a syzygy computation on the entire acoustic variety, rather than a grid of its points.

For the plus cubic, compact symmetry averaging permits primitives, modulo exact gauges, of the form

    α₃=(q₁/8+3/2)r az+q₁t az+(6-q₃)r aw+q₃t aw,
    α₂=f(0,0,xu+yv,yu-xv)+g(0,0,xv-yu,xu+yv),
    α₁=(j/2)az+(k/2)aw,

with az=(-y,x,0,0), aw=(0,0,-v,u). For the minus cubic replace the two degree-two vectors by

    (0,0,xu-yv,-xv-yu), (0,0,xv+yu,xu-yv).

The leading coefficient relations come from the actual null columns, as in the checkpoint. For acquisition, coefficient matching of (1) with a free Gram G is an affine linear system. Alternating affine/PSD projection suggested feasible points. The final step selected rational free coordinates, solved the pivot coordinates exactly, symmetrized the Gram, and verified positive rational pivots. The independent replay in Section 1 then certifies the result without relying on this discovery history.

The coefficient systems have 313 polynomial rows and 330 discovery variables when the full 18×18 Gram entries and six primitive coefficients are retained. These finite operation sizes are implementation facts, not a complexity or scientific advantage claim.

Trials at smaller coefficients which did not acquire a strict Gram are not impossibility proofs. In particular the retained numerical failure at 197/1000 cannot be used as a lower bound on QC or on the polynomial-heat class.

## 3. Scaling, proper rotations, and arbitrary M

If F+C+κ(r+t) is QC, then for s≥0

    F+sC+κs²(r+t)

is QC: for s>0 it equals s⁴ P(A/s); for s=0 use the acquired homogeneous QC of F. This is an exact change of variables in the QC inequality.

Independent proper rotations of z and w correspond to actual proper output and domain rotations of the matrix A. Under rotation of w through θ, ν(w) rotates through 2θ. Therefore arbitrary SO(2) rotations on the left and right of the cubic coefficient matrix M can be realized while preserving the isotropic F and r+t. No transposition invariance of QC is assumed.

Every real 2×2 M has a proper signed singular-value decomposition

    M=L diag(m,n) Rᵀ,

with L,R∈SO(2), m=σ₁≥0 and n=sign(det M)σ₂; use n=0 when det M=0. Thus m≥|n|. Put

    a=(m+n)/2≥0, b=(m-n)/2≥0.

In the diagonal coordinates, C_M=aC₊+bC₋. For 0<θ<1, take the convex combination

    θ [F+(a/θ)C₊+κ₊(a/θ)²(r+t)]
      +(1-θ)[F+(b/(1-θ))C₋+κ₋(b/(1-θ))²(r+t)].

Each bracket is QC by scaling, so their sum is QC. The leading part and cubic are exactly F and C_M. Its quadratic coefficient is

    κ₊a²/θ+κ₋b²/(1-θ).

The minimum is

    ρ(M)=(sqrt(κ₊)a+sqrt(κ₋)b)²,

at θ=sqrt(κ₊)a/(sqrt(κ₊)a+sqrt(κ₋)b). The cases a=0 or b=0 use the corresponding single certificate; M=0 uses F. Transport back by the actual rotations.

Finally, a ROC homogeneous quadratic is QC by Fourier decomposition on actual gradients. Consequently **any full quadratic Q with Q-ρ(M)(r+t) ROC can be added**, including equality, degeneracy, cross terms and determinant lineality. This establishes the stated explicit global sufficient class for every M. It does not exhaust the sharp ROC cone.

## 4. Exact progress at conformal means

This separate observation applies to all orthogonal M=σO, regardless of determinant sign, with any Q admitted by the checkpoint's exact ROC criterion.

For every z,w, completing the square in z gives

    H_M(z,w):=F+zᵀMν(w)+(σ²/8)t ≥0.                    (2)

For t>0 this follows from

    H_M=2t |z+Mν(w)/(4t)|²+t²,

because |Mν(w)|²=σ²t². At t=0 the original polynomial is zero, so (2) extends without any singular definition. H_M vanishes at every conformal mean (z₀,0).

The sharp ROC criterion implies, on every normalized rank-one direction,

    Q(a,b)≥σ²/8+(aᵀM Jν(b))²/4≥σ²/8.

Hence Q' = Q-(σ²/8)t is a ROC quadratic and therefore QC. Since P=H_M+Q', for any actual zero-mean gradient G and conformal mean A₀=(z₀,0),

    <P(A₀+G)>-P(A₀)
      =<H_M(A₀+G)>+<Q'(G)>≥0.

This proves QC at every such mean for every admitted Q, including arbitrary cross terms. It proves no inequality at general anticonformal means. After the unique argument translation in the checkpoint, it gives the corresponding translated plane of safe means.

## 5. Failed rational and finite-field attacks

The full invariant one-form numerator of degree at most five divided by D=1+16(r+t) has forty-four real coefficient forms. Removing density gauges leaves thirty-six independent corrections. Enforcing every leading acoustic null and every exact sharp-boundary null column gives a rational linear system of rank twenty-three, leaving thirteen density parameters. These dimension statements are acquired exact linear algebra in `rational_heat.py`.

A numerical least-squares PSD fit on one finite sample obtained a normalized negative eigenvalue of order 10^-5. Fresh points found a defect near

    (x,y,u,v)=(-0.0877823,0.0233513,-0.203231,0),

with normalized eigenvalue about -0.00928872. The candidate is rejected as a global heat certificate. It is not an energy counterexample. No exact infeasibility certificate for this rational class was obtained.

`heat_shape_search.py` tested actual compatible three-wave gradients, not distributions of unrelated matrices. Its best required heat-monotonicity coefficient approached 3/16 from below as the field approached one wave. This finite search proves neither heat monotonicity nor QC and is retained only as a failed discovery attack.

## 6. What remains unresolved

For M=I and Q=λ(r+t), ROC is exactly λ≥3/16, while the acquired QC certificate proves λ≥99/500. The whole intervening interval remains undecided here. The polynomial-heat obstruction at λ=3/16 remains intact. For general M and Q, the sufficient condition in Section 3 is strictly an upper admission construction; it is not asserted equal to the sharp full ROC admission.

The source credits are unchanged: the frozen rotational-face proof provides the exceptional acoustic geometry; the prior tranche gives its full lower quadratic ROC classification and sharp-boundary barrier; the frozen Bruno–Pasqualotto Appendix A supplies the governing compatible heat argument. The new literal nontranslation primitives, rational Grams and global combination theorem are internally reconstructed here. No historical-priority claim or external independent audit is made.
