# Orientation-preserving, stress-free completion of the accepted aligned energy

This is a new derivation from the accepted literal Hopf theorem, not a new
independent audit of that theorem. The completion is mathematically a stored
energy with conventional elastic constitutive properties. No material,
measurement, quasiconvexity theorem, existence theorem for minimizers, or
physical qualification is acquired by this construction. Historical priority
of either the source family or this completion remains UNKNOWN.

The physical-domain construction below has now passed the independent whole
review in [hopf/physical_review/REVIEW.md](../../hopf/physical_review/REVIEW.md).
That review covers this construction and its own independent algebra replay;
it does not cover the later Young-measure exclusion in
[JENSEN_COMPATIBILITY.md](JENSEN_COMPATIBILITY.md).

## 1. The actual finite Jensen witness is entirely in GL+(2)

Use exactly the A, B_i=A+X_i and weights in hopf/PROOF.md, without importing
producer code. Independent rational reconstruction in verify_completion.py
gives

    det A  = 1260,
    det B0 = 3622910039/2874500,
    det B1 = 630011/500,
    det B2 = 28992/25.

All four determinants exceed 1/2. The same reconstruction verifies the
matrix mean, determinant mean, positive weights, and literal quartic gap

    sum_i lambda_i F(B_i)-F(A)
      = -13534664264487807/296890944920312500 < 0.

Every polyconvex lift on GL+(2) obeys Jensen at these graph points. Therefore
the accepted F is non-polyconvex already on GL+(2), not merely on all matrices
through a witness involving orientation reversal. This argument needs no
statement about differentiability or finiteness of a lift outside the convex
hull of these graph points.

## 2. Exact nonnegative stress-free completion

For the aligned family write

    F(A)=x²+y²+4 beta q x+4r q²,
    q=det A, x=|Ae1|²-|Ae2|², y=2 Ae1 dot Ae2,
    c=r-beta²>0.

The exact algebraic identity is

    F(A)=(x+2 beta q)²+y²+4c q².

Subtract only an affine function of the determinant:

    W_flat(A)=F(A)-8c q+4c
             =(x+2 beta q)²+y²+4c(q-1)².                 (1)

Hence W_flat>=0. On GL+(2), its zero set is exactly SO(2) A0, where

    A0=diag(s,1/s),
    s²=sqrt(1+beta²)-beta.

Indeed q=1, y=0, x=-2 beta force the two columns to be orthogonal with
squared lengths sqrt(1+beta²)-beta and sqrt(1+beta²)+beta, whose product
is one. All these matrices have the indicated form with a proper left
rotation. Since the three squares vanish there, DW_flat=0 there as well.

The shift -8c det A is a null Lagrangian, so it preserves rank-one convexity,
polyconvexity equivalence and quasiconvexity equivalence on the same domain.
In particular the exact finite minors-Jensen gap is unchanged.

For the main accepted example,

    beta=99/100, r=88/25, c=25399/10000,
    W_flat=F-(25399/1250)q+25399/2500.

This is still a polynomial, now of degrees 4, 2 and 0, rather than a homogeneous
quartic. The determinant shift also removes the original even-Hopf symmetry.
These changes of class must not be omitted when describing the completion.

## 3. A smooth convex barrier that is invisible to the witness

Fix delta=1/2 and define on q>0

    k(q)=exp[-1/(delta-q)]/q^4  if 0<q<delta,
         0                    if q>=delta,

    b(q)=integral_q^delta (t-q) k(t) dt  if 0<q<delta,
         0                              if q>=delta.      (2)

Then b''=k>=0, b'<=0 and b>=0. The exponential is flat at delta, so b is
C-infinity on (0,infinity), with every derivative zero at delta and b=0 on
[delta,infinity). No quadrature or floating extrapolation is used here.

For 0<q<delta/4, integration only over 2q<=t<=delta/2 yields

    b(q) >= exp(-2/delta) [1/(16 q²)-1/delta²] -> infinity.

The integrand estimate uses t-q>=t/2 and exp[-1/(delta-t)]>=exp(-2/delta).
Thus b genuinely diverges as q tends to zero from the positive side.
Its extension by +infinity on q<=0 is convex and lower semicontinuous.

Define the completed energy

    W(A)=W_flat(A)+b(det A)  if det A>0,
         +infinity          otherwise.                  (3)

It is objective under left SO(2), smooth on GL+(2), nonnegative, zero and
stress-free exactly on SO(2) A0, and diverges as det A tends to zero from
above. It has quartic coercivity: since K>0, F(A)>=lambda_min(K)|A|^4,
while |det A|<=|A|²/2 and b>=0. Hence W(A)>=c1|A|^4-c2 for suitable
positive constants c1,c2. Its finite sublevel sets are compact in GL+(2).
No connected-sublevel assertion is made.

Along a rank-one direction R, det(A+tR) is affine. Consequently

    D²[b(det A)][R,R]=b''(q)(cof A:R)²>=0.

The accepted strict ROC margin of F therefore survives. For the main energy,

    (1/2)D²W(A)[R,R] >= (7/35200)|A|²|R|²

for all A in GL+(2) and rank-one R. With the extension in (3), every rank-one
line has a convex positivity domain for det, so extended rank-one convexity
also holds. All actual Jensen determinants exceed delta, so b vanishes at
A and every B_i. Their exact negative Jensen gap survives without change.
Therefore W is not polyconvex on its physical orientation-preserving domain.

## 4. Normalizing the stress-free well to the identity

Set

    V(A)=W(A A0).

Because det A0=1, the barrier still uses det A. Right multiplication by A0
preserves rank-one directions, GL+(2), objective left rotations, and
polyconvexity/quasiconvexity under the usual invertible change of variables.
Thus V>=0, DV(I)=0, its zero set is exactly SO(2), and it remains strictly
ROC, globally non-PC and coercive with determinant blowup.

The Jensen matrices become C_i=B_i A0^{-1}, with barycenter A A0^{-1}; their
determinants and the energy gap are unchanged. **That barycenter is not I.**
Since V>=0=V(I), the constant-zero affine-minors support already establishes
polyconvexity *at* I. Likewise V is quasiconvex at I by nonnegativity. The
construction does not yield instability or non-PC at a stress-free minimum.
Global quasiconvexity remains UNKNOWN.

The normalized V remains materially anisotropic. With Q a right rotation
through pi/2, direct evaluation gives

    V(diag(2,1))-V(diag(2,1) Q)
       = -12 beta sqrt(1+beta²) !=0.

Both determinants are 2, so neither the barrier nor the null-Lagrangian
shift contributes to this difference. The right-normalization has not
silently converted the example to the bi-isotropic class.

## 5. The infinite family also survives the physical-domain barrier

For beta=beta_m=(m²-1)/(m²+1), r=4 and every m>=197, use the accepted cuts
at the original base A=I. The positive-determinant increment Rplus satisfies

    det(I+t Rplus)=1+m t²>=1, strictly >1 when t!=0.

The upper support cut U_m follows as t tends to zero, wholly inside GL+(2).
For Rminus=diag(1,-2), the finite scale producing its sharp lower cut is

    tstar=(18 beta-14)/(24 beta+73).

For beta_m in the stated range,

    0<tstar<4/97,
    det(I+tstar Rminus)=(1+tstar)(1-2tstar)
                        >8989/9409>1/2.

Thus the barrier vanishes at the base, throughout the local positive cut and
at the finite negative cut; its first derivative at the base is zero. Any
scalar minor support for W at I would, after undoing the determinant shift,
satisfy the same contradictory U_m and L_m inequalities for F_m. Their
accepted strict gap therefore proves non-PC of W on GL+(2) for every m>=197.
This uses the accepted support inequality, not an unconstructed gradient
Young measure. In fact, [JENSEN_COMPATIBILITY.md](JENSEN_COMPATIBILITY.md)
applies Müller's diagonal-support theorem to exclude a homogeneous bounded
gradient Young measure for the actual main three-atom witness. Global
quasiconvexity is still UNKNOWN.

For completeness, the supporting-affine-minors argument is valid at I even
when the convex lift is specified only on the GL+ graph. The convex hull of
{(A,det A):det A>0} is R^4 times (0,infinity): every (B,d), d>0, is the
average of two graph points (B+Y,det(B+Y)) and (B-Y,det(B-Y)) with both
determinants equal to d. To see this, reduce B by left/right proper rotations
to a signed diagonal matrix and solve cof B:Y=0, det Y=d-det B; for positive
det B choose trace-free diagonal or off-diagonal Y according to the desired
sign, and for negative or zero det B choose an off-diagonal Y of suitable
positive determinant. The lift is therefore finite in an open neighborhood
of the graph point, admits a subgradient there, and differentiating its
touching support gives the usual scalar minor coefficient. The exact main
three-atom proof does not need this auxiliary argument.

## 6. Scope relative to prior science

General objective/isotropic non-PC elastic energies with determinant blowup
already exist: Voss, Ghiba, Martin and Neff, arXiv:2009.09690v1,
Proposition 3.5, gives an explicit nonpolynomial example. Therefore the
completion above must not be presented as the first such elastic phenotype.
Its role is to show explicitly that the new polynomial family's separation
survives these conventional constitutive requirements. The original exact
positive quartic/even-Hopf claim and its priority question remain separate.
The completed model is neither a material identification nor an observed
scientific capability.
