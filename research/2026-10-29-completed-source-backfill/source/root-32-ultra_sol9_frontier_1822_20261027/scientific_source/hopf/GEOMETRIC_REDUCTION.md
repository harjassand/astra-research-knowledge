# Selector-free geometry of the even Hopf sector

These statements derive the support geometry used to acquire the exact
counterexample. They use the established scalar minor-support criterion
(see Aubert1988, Theorem1.3); world priority of the specialized geometric
reduction is UNKNOWN. They are not a claim that the underlying general
support criterion or quartic polarization is new.

Let h(A)=(u−v,2w,2detA), |h(A)|=|A|², and F(A)=h(A)^TKh(A), K symmetric.
Write K=[[B,d],[d^T,r]], B symmetric2 by2. Coordinates refer to the fixed
equatorial plane {h3=0}, which is exactly the rank-one locus.

## 1. A complete coercivity dichotomy for ROC even quartics

**Proposition.** If F is rank-one convex, either

1. B=0, d=0 and r>=0, so F=4r(detA)²; or
2. B is positive definite and K is positive definite.

In particular there is no nonzero ROC even Hopf matrix of rank two.
The only singular ROC ray consists of nonnegative multiples of det².

For any equatorial unit e, the acoustic half-Hessian at its unit spinor
has the form recorded in the accepted source and PROOF.md, with
k=e^TBe, n=(Je)^TB(Je), l=(Je)^TBe, m=e dot d, p=Je dot d.
Its diagonal2k forces B>=0. If B has rank one, choose e along its
positive eigenvector: then n=l=0 and k>0. Its Schur diagonal
2kn−k²−3l²−m² is strictly negative, impossible. Hence B is positive
definite or zero. If B=0, the zero acoustic top diagonals force m=0
for every e, so d=0, and the remaining acoustic entry forces r>=0.

When B>0, the other Schur diagonal gives

    r >= k/2+3m²/(2k)+l²/(2k).

Taking the supremum of m²/k implies r>=3d^TB^{-1}d/2. If d!=0,
this strictly exceeds d^TB^{-1}d. If d=0, the term k/2 makes r>0.
The Schur criterion for K therefore gives K>0 in both cases.

## 2. Exact elimination of the relative spinor phase

Assume K>0. For unit n, let

    f(n)=n^TKn,
    Sbar(n)=K−Kn n^TK/f(n),
    sigma(n)=lambda_min(Sbar(n) restricted to n-perp),
    v(n)=Kn−sigma(n)n.

The scalar sigma is strictly positive. It has the closed form

    g(n)=f(n)trK−n^TK²n,
    sigma(n)=2detK/[g(n)+sqrt(g(n)²−4detK f(n))].     (1)

Indeed the two-dimensional tangent Schur complement has trace g/f
and determinant detK/f. Formula(1) is its smaller eigenvalue, expressed
without subtracting close floating-point values. It includes repeated
eigenvalues by continuity.

Let H1,H2,H3 be the real symmetric Clifford matrices satisfying
h_i(A)=A^TH_iA, and let I be the orthogonal complex structure that
implements left row rotation by pi/2. These matrices obey
H_iH_j+H_jH_i=2delta_ij I4 and commute with I.

For unit matrices A,R, put m=h(A), n=h(R), b_i=A^TH_iR.
Literal differentiation gives

    A^TT_F(R)A=2m^TKn+4b^TSbar(n)b,                 (2)

where T_F=(1/2)D²F−DF DF^T/(4F). If b'_i=A^TH_iIR,
the elementary Hopf polar identity is

    bb^T+b'b'^T
       =[(1−m dot n)I3+mn^T+nm^T]/2.               (3)

After orthogonal projection to n-perp, the right side is
[(1−m dot n)/2] times the tangent identity. Thus the two projected
vectors are orthogonal with equal squared norm (1−m dot n)/2.
Replacing R by cos(phi)R+sin(phi)IR rotates them through that entire
tangent circle. Sbar kills n. Minimizing(2) over this phase therefore gives

    min_phase A^TT_F(R)A
       =2m^TKn+2(1−m dot n)sigma(n)
       =2[sigma(n)+m dot v(n)].                    (4)

If m=n the tangent circle has zero radius, and the same equality holds.
For general nonzero A,R, multiply(4) by |A|²|R|² and normalize m,n.

## 3. An exact pairwise criterion for unrestricted PC

**Theorem.** For K>0, F is PC exactly when both conditions hold:

    |v(n)|<=sigma(n)       for all unit n with n3=0; (5)

    |p3 v(n)−n3 v(p)| <=p3 sigma(n)+n3 sigma(p)      (6)

for every pair of unit n,p with n3,p3>0. Condition(5) is exactly ROC.
Consequently a positive even ROC energy is non-PC precisely when some
pair in the open upper hemisphere strictly violates(6).

To prove this, quartic polarization reduces a global support at unit A
to A^TT_F(R)A−k_A detR>=0 for every R. Formula(4), detR=n3/2 and
the symmetry sigma(−n)=sigma(n), v(−n)=−v(n) make this equivalent to
the existence of kappa=k_A/4 satisfying

    |m dot v(n)−kappa n3|<=sigma(n) for every unit n.(7)

At n3=0 this demands |m dot v(n)|<=sigma(n). For n3>0 it requires
kappa to belong to the closed interval

    I_n(m)=[(m dot v(n)−sigma(n))/n3,
            (m dot v(n)+sigma(n))/n3].

Closed bounded intervals on the real line have a common intersection
if and only if they intersect pairwise. For an infinite family, fix
one interval; compactness gives the same conclusion from the finite
intersection property. Thus(7) holds for a fixed unit m exactly when
the equatorial bounds hold and

    |m dot[p3v(n)−n3v(p)]|<=p3sigma(n)+n3sigma(p)

for every upper-hemisphere pair. Requiring this for all unit m yields
(5)–(6) by the Euclidean dual norm. The scalar supports build a finite
convex lift by their supremum, using the same two-graph-point bound
as PROOF.md. This proves sufficiency as well as necessity.

For the ROC assertion, at a rank-one R the full Hessian is PSD exactly
when T_F(R) is PSD. One direction is immediate from its definition.
For the other, quartic homogeneity gives D²F(R)R=3DF(R) and
R^TD²F(R)R=12F(R). Cauchy–Schwarz for the PSD Hessian yields
DF(R)DF(R)^T <=(4/3)F(R)D²F(R), hence T_F(R)>=D²F(R)/6.
Quartic polarization now makes ROC equivalent to T_F(R)>=0 at every
rank-one R. Formula(4) and variation of unit m give exactly(5).

This derivation is important for quantifiers: the theorem concerns
arbitrary scalar supports. It does not assume a polynomial, rational,
continuous, linear, or otherwise prescribed formula for k_A. Failure
of(6) is therefore a genuine non-PC opening. Conversely, a failed
finite search of pairs proves no positive assertion.

## 4. Pairwise ball representation

For upper-hemisphere n=(t,1)/sqrt(1+|t|²), define

    C(t)=K(t,0)−sigma(n)(t,1),
    R(t)=sigma(n)sqrt(1+|t|²).

Condition(6) is equivalently

    |C(t)−C(s)|<=R(t)+R(s) for all t,s in R².

Thus PC corresponds to pairwise intersection of this exact family of
three-dimensional balls, together with the equatorial ROC limits. It
does not assert simultaneous intersection of all balls, which would
be a stronger and generally different requirement.

The numerical acquisition evaluated the ratio in(6) on four angular
variables. Its violating pair identified the aligned K used in PROOF.md;
the final proof replaced that suggestion by small integer cuts and an
independent literal three-atom Jensen evaluation. No asymptotic degree
escalation or numerical positivity premise survives into the certificate.
