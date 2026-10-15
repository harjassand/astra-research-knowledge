# Independent proof reconstruction: the ambient invariant ROC cone

Audit date: 2026-10-15. Repository pin:
`b32943eeb62d0d79929a9e572a344219a785ebf9`.

These arguments distinguish universal mathematical implications from the
43 finite symbolic checks in `EXACT_ALGEBRA_RECEIPT.json`. The checker
differentiates polynomials defined in its own source; it does not load a
producer certificate or another worker's module. The absent incoming ZIP and
its verifier were not replayed. This note does not reconstruct the full
negative-branch heat-to-quasiconvexity certificate.

## 1. Exact ambient space and definitions

Let V be the real vector space of homogeneous quartic polynomials on all real
2-by-2 matrices invariant under multiplication on the left by SO(2). Let K
be its rank-one-convex cone. For

    A = [[a,b],[c,d]],
    u=a²+c², v=b²+d², w=ab+cd, j=ad-bc,
    H=(u+v-2j)²=((a-d)²+(b+c)²)²,

a basis of V is

    u², v², uv, w², uw, vw, ju, jv, jw.

For completeness, use complex column coordinates z1=a+ic and z2=b+id.
A degree-four invariant must have two unbarred and two barred factors.
The real-valued expressions are Hermitian forms in
`(z1²,z1 z2,z2²)`, a nine-real-dimensional space. The displayed nine
polynomials are independent by direct coefficient comparison, so they span V.
Equivalently, the ten quadratic products of u,v,w,j have the single relation
`uv=w²+j²`.

For a C² polynomial F, rank-one convexity is equivalent to

    D²F(A)[eta⊗xi,eta⊗xi] >= 0

for every real A,eta,xi: restrict to each rank-one affine line and apply the
one-dimensional second-derivative criterion. Thus K is a closed convex cone.
Left invariance rotates each nonzero eta to a positive multiple of e1.
Only this output rotation is used below; spatial directions are not silently
rotated by a nonexistent right SO(2) symmetry.

Fix throughout

    r>0 or r<-2,
    alpha_r=3r/[8(r+2)], beta_r=r(r-1)/6,
    J_r=alpha_r H+beta_r u²+j²+r uj,
    A_r=[[0,(2r+1)/3],[1,0]].

## 2. Complete acoustic classification, including determinant signs

Define the symmetric matrix M_r(n,m) by

    (1/2)D²J_r(A)[e1⊗(n,m),e1⊗(n,m)] = xᵀ M_r(n,m)x,
    x=(a,b,c,d)ᵀ.

Direct differentiation gives its leading principal minors:

    L1 = r[(2r+1)²n²+3m²]/[4(r+2)],

    L2 = 3r²{[(2r+1)n²-3m²]²+12r(r+2)n²m²}
         /[16(r+2)²],

    L3 = 3m²r²{[(r+1)(2r+1)n²-3m²]²
                +3r(5r+4)n²m²}/[16(r+2)²],

    L4 = det M_r = 9r⁴n⁴m⁴/16.

The factor 1/16 is a normalization convention, not a contradiction to the
incoming report: its acoustic matrix is 2M_r, whose determinant is exactly
`9r⁴n⁴m⁴`. All four identities have been checked symbolically from J_r.

On both allowed branches,

    r/(r+2)>0, r(r+2)>0, r(5r+4)>0, 2r+1 != 0.

If nm!=0, all four minors are strictly positive. Sylvester's criterion
therefore gives positive definiteness, excluding every nonzero background
A from being a contact in a mixed spatial direction.

At n=0,m=1, the (a,d) block is

    3r/[4(r+2)] [[1,-1],[-1,1]],

while the (b,c) block has positive first diagonal and determinant
`9r/[4(r+2)]>0`. This matrix is PSD with kernel precisely span(I).

At n=1,m=0, the (b,c) block is

    r/[12(r+2)] (3,-2r-1)ᵀ(3,-2r-1),

and the (a,d) block has positive first diagonal and determinant
`r(2r+1)²/[4(r+2)]>0`. Its kernel is precisely span(A_r).
Homogeneity handles every nonzero point on these two spatial axes.

Consequently J_r is ROC and all its nontrivial acoustic zeros, up to output
rotation and nonzero scalings of A and R, are exactly

    (I,e12) and (A_r,e11).

Here det(I)=1 and det(A_r)=-(2r+1)/3. Thus det(A_r)>1 on r<-2 and
det(A_r)<-1/3 on r>0. No nonzero singular background is a contact.
The excluded zero-background or zero-direction evaluations are identically
zero functionals and are irrelevant to dual supports. The parameter values
0 and -2 are outside this proof; J_0 degenerates to j² and the displayed
formula is undefined at -2. No argument extends the nonexposure claim to
these values.

For a rank-one R, direct determinant differentiation gives

    D²(j²)(A)[R,R] = 2(cof A:R)².

In target normalization R=e1⊗(n,m), this is `2(dn-cm)²`. It vanishes at
both classified contact families, after every allowed rotation and scaling.

## 3. The two-contact exposed face and extremality

Write a general invariant quartic as `sum(p_i basis_i)` in the basis above.
Let ell0(F)=D²F(I)[e12,e12]. For F in K, ell0>=0. If ell0(F)=0,
nonnegativity of the acoustic polynomial forces all first derivatives in
A,eta,xi to vanish there. The exact linear equations have rank five and give

    p1=-p7/4, p2+p3=-p7/2, p4=p5=p8=0.

The resulting four-dimensional span has the unique parametrization

    F=alpha H+beta u²+gamma j²+delta uj.

Every ROC member of this span necessarily satisfies

    P=[[6beta+delta,delta],[delta,gamma]] >= 0,
    Q=[[8alpha,delta],[delta,2beta+delta]] >= 0.

No sufficient ROC theorem is needed here. To prove necessity, use the exact
acoustic curve `A_t=[[1,-kt],[kt,1]], R_t=e1⊗(t,1)`:

    (1/2)D²F(A_t)[R_t,R_t]
      =t²[6beta+delta+2delta(1-k)+gamma(1-k)²]
         +t⁴k²(2beta+delta).

Divide by t² and let t tend to zero. The quadratic in 1-k is nonnegative
for every k, which gives P>=0, including gamma=0 by continuity in the
test vector. For Q, take `A=[[0,X-Y],[Y,0]], R=e11`. The half-acoustic
value is `(X/2,-Y)Q(X/2,-Y)ᵀ`, so Q>=0 directly.

Let ell_r(F)=D²F(A_r)[e11,e11], also nonnegative on K. The zero set of
ell0+ell_r is an exposed face E_r. After imposing the first contact, the
second gives, with z=(r+2,-3)ᵀ,

    ell_r(F)/2 = zᵀQz/9.

Since Q is PSD, this vanishes exactly when Qz=0, forcing

    alpha=3delta/[8(r+2)], beta=(r-1)delta/6.

Put ell=delta/r. The nonnegative alpha diagonal gives ell>=0, because
alpha_r>0. Then P has entries `(ell r²,ell r;ell r,gamma)`. If ell>0,
PSD forces gamma>=ell; if ell=0 it forces gamma>=0. In both cases
mu=gamma-ell>=0 and

    F=ell J_r+mu j².

Conversely J_r and j² are ROC and meet both contacts. Hence, without
assuming the whole four-dimensional ROC classification,

    E_r = cone{J_r,j²}.

They are independent generators. Thus J_r is an extreme ray of this face
and of K. Extremality here is explicitly in V; no claim is made in the
larger cone of all quartic polynomials or all integrands.

## 4. Closure of the generated dual acoustic cone

Let T consist of acoustic evaluation functionals on V with
`|A|=|eta|=|xi|=1`. It is a compact subset of V*: it is a continuous image
of the product of three finite-dimensional unit spheres. Let Q0(A)=|A|⁴.
For every ell in T,

    ell(Q0)=8[A:(eta⊗xi)]²+4|A|²|eta⊗xi|² >= 4.

Suppose a sequence L_k in cone(T) converges. Write
`L_k=s_k C_k`, where s_k is its total nonnegative coefficient mass and
C_k lies in conv(T), when s_k>0. Then

    0<=s_k<=L_k(Q0)/4.

The right side is bounded. The convex hull of a compact set in a
finite-dimensional space is compact, so a subsequence has
`s_k -> s>=0` and `C_k -> C in conv(T)`. Its limit is sC, still in cone(T).
The zero-mass case is immediate. Thus cone(T) is closed.

By rank-one homogeneity and the second-derivative criterion,
`K=cone(T)*`. Finite-dimensional bipolar duality now gives

    K*=cone(T).

Each functional has a finite positive acoustic decomposition; conic
Caratheodory bounds the number of terms by dim(V)=9. This closure step is
essential. It excludes unaccounted limit supports and does not assume that
derivatives of acoustic evaluations are nonnegative dual functionals.

## 5. Nonexposure and the smallest exposed face

If L in K* vanishes on J_r, express L as a finite sum of acoustic
evaluations with nonnegative weights. Since J_r is ROC, every term with
positive weight must be one of its zeros. Section 2 shows that each such
term also annihilates j². Therefore L(j²)=0.

An exposing functional for the ray R_+J_r would have to exclude j², which
is independent of J_r. None can. The ray is nonexposed in K. Every exposed
face containing it also contains j² and hence E_r; Section 3 already
exposes E_r. Its smallest exposed face is exactly cone{J_r,j²}.

There is no conflict with exposure inside the four-coefficient contact
face. Exposure of a face within another exposed face need not lift to
exposure in the ambient cone.

## 6. Direct-LMI impossibility, with an explicit kernel proof

Suppose K had a direct finite affine real-symmetric LMI representation

    K={p in R⁹:L(p)=L0+sum(p_i L_i)>=0}.

Take y on the nonzero ray J_r and let U=ker L(y). The affine functional
`f(p)=tr(P_U L(p))` is nonnegative on K. For a PSD matrix, zero trace on
U is equivalent to annihilating U. Thus its zero set in K is

    F_y={p in K:U subset ker L(p)}.

For any z in F_y, both L(y) and L(z) annihilate U. On U-perp, L(y) is
positive definite. For sufficiently small epsilon>0,
`L(y)+epsilon(L(y)-L(z))` is PSD, so
`w=y+epsilon(y-z)` lies in K. The point y lies in the open segment from
z to w. The extreme-ray face property therefore forces z onto R_+y.
Conversely every point of that ray lies in F_y: its kernel inclusion
follows by writing y as an interior convex combination of 0 and any
sufficiently large positive multiple of y, and using PSD kernel
intersection. Hence F_y is exactly the ray, and f exposes it. Because
0 belongs to that face, f(0)=0; the relevant support is linear on the
cone even though the proposed pencil was affine.

This contradicts Section 5. Therefore K is not spectrahedral in its
actual nine coefficients. The proof permits arbitrary pencil size and
affine offsets, does not require a strict-feasibility assumption, and
handles finitely many LMIs by taking a block diagonal pencil. The result
also holds after an invertible linear change of the coefficient basis.
It is the classical exposed-face mechanism, applied to the inherited
nonexposure theorem; it is not a new general obstruction method.

## 7. The full cone nevertheless has a finite semidefinite lift

For a general F in V, direct differentiation determines symmetric 4-by-4
matrices M11,M12,M22, linear in its nine coefficients, such that

    D²F(A)[e1⊗(n,m),e1⊗(n,m)]
      =xᵀ(n²M11+2nmM12+m²M22)x.

If this is nonnegative, the univariate matrix polynomial
`M11+2t M12+t² M22` is PSD on the real line. The established univariate
matrix SOS theorem, including degenerate matrices, provides a real
polynomial factor Q(t). Each entry of Q has degree at most one: otherwise
the highest-degree coefficient of some diagonal entry of QᵀQ would be a
nonzero sum of real squares, contradicting degree at most two. Write
`Q(t)=Q0+t Q1` and homogenize, retaining the n=0 direction. Its Gram
matrix yields exactly

    exists K0 in Skew_4(R):
    [[M11,M12+K0],[M12-K0,M22]] >= 0.

The symmetric part of the off-diagonal block is M12, while its six skew
entries are free. Conversely this PSD block immediately proves acoustic
nonnegativity. This is an 8-by-8 LMI with six auxiliary real variables.
It is already present in pinned FV/FX capital, not supplied as a new
result here. No rational-Gram existence assertion is inferred for
rational boundary coefficients.

The independent checker reconstructs all three block matrices and checks
that the six skew entries vanish on `(n x,m x)`. Its finite algebra does
not prove the external SOS theorem. I inspected Hanselka-Sinn,
Corollary 2.8, printed p.9, which explicitly includes the degenerate case.
[Primary paper](https://arxiv.org/abs/1707.08261).

## 8. Additional classical corollary: no hyperbolicity-cone description

Renegar's Theorem 23 states that each boundary face of a closed
hyperbolicity cone is exposed. J_r is a nonexposed boundary face of K,
so K cannot equal a closed hyperbolicity cone of a homogeneous real
polynomial in these nine coefficient variables. This statement is
unchanged under an invertible linear coordinate transformation.
It is an additional audit deduction from the already integrated
nonexposure result and a classical theorem. It supplies no QC result and
does not exclude projections of hyperbolicity cones, since Section 7
already gives a PSD lift. The original theorem and proof were acquired
and inspected on printed pp.14-15.
[Renegar's primary preprint](https://optimization-online.org/wp-content/uploads/2004/03/844.pdf).

## 9. Separate unrestricted-polyconvexity check

For completeness, let
`P_(alpha,r)=alpha H+r(r-1)u²/6+j²+r uj`, with any finite real alpha.
If it is ordinarily polyconvex on all matrices, a convex minor lift can
be taken finite on all `(A,z)`: any point is the midpoint of two graph
points `(A+B,det(A+B))` and `(A-B,det(A-B))` by choosing
`det B=z-det A`. It therefore has a supporting hyperplane at (I,1).
Smoothness of P forces the pulled-back inequality to have the form

    P(I+V)-P(I)-DP(I):V-lambda det V >= 0 for every V.

Its e12 quadratic coefficient is zero. A PSD support Hessian must have
the entire e12 row zero, and its e12/e21 cross entry is
`lambda-r-2`; hence lambda=r+2. The support Hessian then annihilates
`diag(1,-r-1)`. Along that direction the exact residual is

    -r(r+2)t³/3
      +[alpha(r+2)⁴+(r+2)(r+3)/6]t⁴.

If r(r+2)!=0, choose the sign of t so the cubic is negative and then
take |t| sufficiently small. This contradicts the supporting inequality.
Thus every finite alpha is non-PC whenever r(r+2)!=0, including the
source's narrower r(r+2)>0 claim. This stronger quantifier is already
recorded in PR #100. This negative residual is a minor-lift support
residual; it is not a compatible-gradient Jensen violation.
