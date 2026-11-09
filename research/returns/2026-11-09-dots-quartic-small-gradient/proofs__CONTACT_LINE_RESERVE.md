# Contact-line reserve: extension without global quartic positivity

9 November 2026. Analytic addendum candidate, no numerical run. This leaves TYPE_II_SMALL_GRADIENT_LEMMA.md (SHA256 f19819dfa7a09ff5d564d07b852c93acd02a266843d0e47740f399aa7875ecc9) and the original-J_r proof unchanged. Independent review is pending.

## 1. Contract and precise additional claim

Retain the fixed nonzero affine mean, calibrated quadratic Q, cubic C, compatible coordinates, and Type-II hypotheses (1) from TYPE_II_SMALL_GRADIENT_LEMMA.md. Replace its pointwise reserve F(X)>=c_*|X|^4 by the weaker hypothesis

    F(R)>0,   R=e12.

This is the rank-one contact direction in those canonical coordinates. Then the SAME kind of small-gradient Jensen inequality still follows:

    int[F(A+Dphi)-F(A)] >= (1/2) int Q(Dphi)
                              +(c/2)int|Dphi|^4

for a sufficiently small positive gradient-supremum radius depending on the fixed polynomial and coordinates.

This statement is about the fixed nonzero mean A. It makes NO claim at A=0 without a separate positive integral reserve. For a homogeneous quartic, small-gradient Jensen stability at zero is equivalent by scaling to the unrestricted arbitrary-amplitude zero-mean inequality; that operation is not supplied by this addendum.

## 2. A positive line supplies a reserve with a transverse debit

Write X=bR+Y, with Y=(a,0;c,d), so the decomposition is orthogonal in the canonical Frobenius norm. Put f0=F(R)>0. By homogeneity and continuity, there exists eta in (0,1] such that

    |Y|<=eta |b|  implies  F(bR+Y)>= (f0/2)b^4.

A computable eta is obtained by expanding the finitely many coefficients of F(bR+Y)-f0b^4 and bounding each term by a coefficient sum times eta b^4. There is no minimization oracle in this choice. Since |X|^4<=4b^4 on this cone, c=f0/8 is valid there.

Choose a finite coefficient bound K with |F(X)|<=K|X|^4. Outside the cone, |X|^4<=(1+eta^(-2))^2|Y|^4. Therefore, globally,

    F(X)>= c|X|^4-C_Y|Y|^4,
    C_Y=(K+c)(1+eta^(-2))^2.                              (R)

The inequality permits F to be negative away from the contact line. No positivity at arbitrary matrices is inferred.

## 3. Compatible small gradients pay the entire transverse debit

Use the notation of the frozen generic lemma:

    epsilon=||Dphi||_infinity, M=int|Dphi|^4,
    Qbar=int Q(Dphi), r=d-lambda a,
    Aeps=epsilon^(1/2)M^(1/4)Qbar^(3/4),
    Beps=epsilon Qbar.

Equation (10) of that lemma is independent of any positivity assumption on F; it uses only the fixed quadratic normal control and compatibility. Thus

    int|a|^3 <= 4 A1^3 Aeps+4 A2^3 Beps.

Because a is an ORIGINAL gradient entry, |a|<=epsilon, and therefore

    int|a|^4 <= 4 A1^3 epsilon Aeps
                 +4 A2^3 epsilon Beps.                    (A)

Also |c|<=epsilon and |r|<=(1+|lambda|)epsilon, while
int(c^2+r^2)<=Qbar/nu_*. Hence

    int(c^4+r^4)
       <=[1+(1+|lambda|)^2]epsilon^2 Qbar/nu_*.            (N)

Finally, d=lambda a+r and elementary fourth-power inequalities give

    |Y|^4=(a^2+c^2+d^2)^2
       <=3[(1+8|lambda|^4)a^4+c^4+8r^4].

Combining (A) and (N), there are explicit finite D1,D2 such that

    int|Y|^4 <= D1 epsilon Aeps+D2 epsilon Beps.            (Y)

For example, one can choose

    D1=12(1+8|lambda|^4)A1^3,
    D2=12(1+8|lambda|^4)A2^3
          +3[1+8(1+|lambda|)^2]/nu_*.

No L-infinity bound is imposed on a projected Hessian. The only supremum used in (A) is that of the original entry a.

## 4. Absorption

The frozen generic cubic proof supplies

    |int C(Dphi)|<=C1 Aeps+C2 Beps.

Together with (R) and (Y),

    Jensen gap >=Qbar+cM
       -(C1+C_YD1 epsilon)Aeps
       -(C2+C_YD2 epsilon)Beps.

Restrict epsilon<=1, set

    C1'=C1+C_YD1, C2'=C2+C_YD2,

and use exactly the same positive radius construction as before with c,C1',C2'. This proves the displayed claim. Periodic mollification, zero extension, and fixed compatible-coordinate changes are those already paid in the generic lemma.

## 5. Type I

For a Type-I contact, write X=sR+Y with |R|=1,
Q>=nu_*|Y|^2, and |C(X)|<=K_C|X||Y|^2. If F(R)>0, the same positive-line argument gives (R). Since Y is an orthogonal projection of the ORIGINAL gradient,

    int|Y|^4<=epsilon^2 Qbar/nu_*.

Consequently the quadratic energy pays the cubic and quartic transverse debits for sufficiently small epsilon, leaving Qbar/2+cM. Again, no global pointwise quartic positivity is needed.

## 6. Conditional class consequence and remaining origin

N806 CONTACT_COMPENSATION.md states two algebraic facts for non-polyconvex, rank-one-convex homogeneous quartics invariant under left SO(2):

1. F(R)>0 for every nonzero rank-one R (Section 2.2).
2. Every nonzero acoustic contact has Type I or Type II with the exact cubic identities used here (Section 2.3).

CONDITIONAL ON THOSE CLASSIFICATION FACTS, the present proof gives small-gradient Jensen stability at every NONZERO affine mean in the full left-SO(2) rank-one-convex homogeneous quartic cone. Noncontact means use the classical strict Legendre-Hadamard argument, and polyconvex members already satisfy global Jensen.

The zero mean is NOT included in that general consequence. If an integrand additionally has a known positive compatible-gradient quartic reserve, the zero-mean conclusion follows separately. Original J_r does have the independently checked pointwise reserve for all r>0, so its earlier all-mean result is unchanged.

This distinction avoids the invalid inference that all members of the cone are pointwise positive. It also prevents the nonzero-contact argument from silently solving the arbitrary-amplitude zero-mean problem.

## 7. Prior and status

The Type-II algebraic geometry and Hodge method are inherited from N806 at Astra pin bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e:
updates/FJ/package/quartic/CONTACT_COMPENSATION.md,
SHA256 f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28.

The new analytic implication is the finite-p small-gradient estimate and its use to pay a quartic transverse debit. The estimate is a standard interpolation/Holder argument specialized to the inherited contact structure, not a new general harmonic-analysis method. This addendum does not independently re-audit the entire nine-coefficient classification.

Use the term small-gradient Jensen stability or Morrey weak quasiconvexity, not existence of a nearby globally quasiconvex extension. No arbitrary-amplitude QC, uniform moving-background radius, numerical radius, priority claim, or scientific execution is asserted.
