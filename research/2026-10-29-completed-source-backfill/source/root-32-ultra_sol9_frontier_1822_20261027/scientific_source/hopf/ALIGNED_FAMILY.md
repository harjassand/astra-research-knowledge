# Exact ROC boundary and a strict-ROC/non-PC rational family

For A=[[a,b],[c,d]], use T=|A|², q=detA, x=a²+c²−b²−d²,
y=2(ab+cd), z=2q. Consider the normalized aligned family

    F_(beta,r)=x²+y²+2beta xz+r z²
              =T²+4(r−1)q²+4beta qx.

Changing the sign of beta is a rank-one-preserving orthogonal change of
matrix coordinates. All assertions below are on all real 2 by 2 matrices.

## Exact ROC threshold

The full continuum acoustic calculation in PROOF.md gives

    N11=1−beta²s,
    N22=2r−1−3beta²s,
    detN=3beta⁴s²+2beta²(1−r)s+2r−1−4beta²,
    0<=s<=1.

Therefore ROC holds exactly when b=|beta|<=1 and

    r >= R(b),
    R(b)=1/2+2b²                 for 0<=b<=1/2,
    R(b)=4−2sqrt(3(1−b²))        for 1/2<=b<=1.

For b<1, solve detN>=0 for r. The result is the maximum on [0,1] of

    H_b(s)=[1+3b²s+4b²(1−s)/(1−b²s)]/2.

Its derivative has the sign of 3/2−2(1−b²)/(1−b²s)². If b<=1/2,
the maximum is at s=0. Otherwise its unique interior maximizer is

    s*=[1−(2/sqrt3)sqrt(1−b²)]/b².

These give the displayed formulas. At b=1, direct substitution gives
detN=3(s−1)(s−(2r−5)/3), yielding exactly r>=4. Values b>1 violate
N11 at s=1. Endpoint cases are included. For b<1 and r>R(b), ROC is
strict, since N11 and detN are uniformly positive on the closed interval.

## An infinite explicit family failing PC at the identity

**Theorem.** For every real m>=197, put

    beta_m=(m²−1)/(m²+1), r=4,
    F_m(A)=T²+12q²+4beta_m qx.                       (1)

Every F_m is strictly rank-one convex, positive for A!=0, and not
polyconvex at A=I. Rational m gives rational ordinary quartic coefficients.
No boundedness restriction on A or on support increments is imposed.

Indeed 0<beta_m<1 for every finite m and R(beta_m)<4. The Hopf matrix
has the positive principal block determinant 4−beta_m²>3.

For non-PC, fix A=I and use

    Rplus=[[0,m],[-1,0]], detRplus=m,
    Rminus=diag(1,−2), detRminus=−2.

As in PROOF.md, every scalar global minor support at A must lie below
A^T T_F(Rplus)A/detRplus and above A^T T_F(Rminus)A/detRminus.
Here those bounds are exactly

    U_m=24+16m/(m²+1),
    L_m=2(297beta_m²+603beta_m+268)/(24beta_m+73).

The first is the sharp local upper bound from all off-diagonal R. To
verify it directly, expand F(Rplus+tI); its linear coefficient is zero
and its quadratic coefficient divided by m is the displayed U_m.
For Rminus+tI, the first three coefficients are

    c0=24beta_m+73,
    c1=28−36beta_m,
    c2=−36beta_m−12,

so (c2−c1²/(4c0))/(-2)=L_m. Subtraction gives

    L_m−U_m=
      4(2m⁴−388m³−905m²−196m−313)
       /[(m²+1)(97m²+49)].                         (2)

Writing m=197+t, the numerator polynomial before its factor4 is

    2t⁴+1188t³+235495t²+15632542t+10711168.

All coefficients are strictly positive, so (2)>0 for every t>=0.
Thus the two required support bounds are incompatible at I.

For example m=200 gives beta=39999/40001 and a strict support gap

    L_200−U_200=239041948/155205840049>0.

Unlike the main beta=.99 target, these witnesses place the non-PC base
point exactly at a conformal matrix. This does not contradict the
Guerra–Kristensen automatic-PC theorem, which requires both left and
right rotational isotropy. The term qx fails right rotational isotropy.

The family also shows failure is not caused by a negative energy value
or by lack of smoothness: each F_m is a strictly positive polynomial
away from zero, invariant under all left row rotations and under the
spin flip sending h to −h. Quasiconvexity of this family is UNKNOWN.

## What remains unclassified

The exact PC threshold r_PC(beta) for all beta has not been derived.
For |beta|<=1 it exists as an epigraph threshold if the feasible section
is nonempty, since adding a nonnegative multiple of det² preserves PC.
The derivation above is a necessary support test and a strict family
of failures, not a complete PC classification. No unsupported universal
upper threshold or claim that two selected directions suffice for PC
is made here.
