# The normal variable must enter a global lift nonpolynomially

This is a target-specific consequence of the already accepted absence of
every polynomial global determinant-support selector for the old quartic
`sol8_opportunity_selection_20261027/rational_selector/PROOF.md`. It concerns
that PC/QC quartic, not the newer ROC/non-PC Hopf quartic.

Let F be that homogeneous quartic and let W(A)=F(A)+epsilon |A|^2, with
epsilon>=0. A convex representative means a finite convex function
g:R^4 x R -> R such that g(A,det A)=W(A) for EVERY real A.

**Theorem.** No C^2 convex representative of W is polynomial in the last
variable s, even allowing arbitrary C^2 coefficient functions of B and
arbitrary finite degree. Consequently there is no such rational
representative whose denominator is everywhere nonzero and depends only
on B. In particular the explicit local formula

    h(B,s)=W(B)+k_sigma(B)(s-det B)+M(s-det B)^2

cannot itself be a global convex representative, regardless of the choice
of smooth nonlinear k_sigma and constant M. Convexification is substantive.

## 1. A universal quadratic upper bound in s

Choose C with |F(A)|<=C|A|^4. For the literal target one may use the
ordinary quartic coefficient l1 norm

    C=2535570311/2500000000.

For any B,s choose Y with det Y=s-det B and |Y|^2=2|s-det B|. For example
Y=diag(r,sign(s-det B)r), r=sqrt(|s-det B|). The determinant identity gives

    (B,s)=1/2 (B+Y,det(B+Y))+1/2 (B-Y,det(B-Y)).

Convexity and graph equality therefore give

    g(B,s)<=1/2[W(B+Y)+W(B-Y)]
           <=24C|B|^4+64C s^2+2epsilon|B|^2+2epsilon|s|.       (1)

Here |B+/-Y|^4<=8(|B|^4+|Y|^4),
(s-det B)^2<=2s^2+|B|^4/2, and
|s-det B|<=|s|+|B|^2/2. These estimates are deliberately conservative.

For each fixed B, a convex univariate polynomial with the upper growth
bound (1) has degree at most two. Thus a putative representative has form

    g(B,s)=a(B)s^2+b(B)s+c(B),     a(B)>=0.                    (2)

## 2. Joint convexity removes all nonlinear coefficient freedom

For r>0, g(B,rs)/r^2 is convex in (B,s). Its finite pointwise limit

    f(B,s)=a(B)s^2

is convex. It is zero on the entire hyperplane s=0. Fix B1,B2,s!=0 and
0<theta<1, and put B3=(B1-theta B2)/(1-theta). Then

    f(B1,s)<=theta f(B2,s/theta)+(1-theta)f(B3,0)
           =a(B2)s^2/theta.

Letting theta increase to 1 gives a(B1)<=a(B2), and reversing B1,B2 proves
that a is a constant a0. This argument also covers zero coefficients.

If a0>0, positivity of the Hessian of (2) and its Schur complement give

    D^2c(B)+s D^2b(B) - Db(B)Db(B)^T/(2a0) >= 0

for every real s. Testing each direction and both signs of unbounded s
forces D^2b=0, so b is affine. If a0=0, a PSD Hessian with zero ss entry
has a zero Bs block; hence Db=0 and b is constant. In both cases

    k_g(A)=partial_s g(A,det A)=2a0 det A+b(A)                 (3)

is a polynomial of degree at most two in A.

## 3. Contradiction with the accepted support obstruction

Differentiating the graph equality identifies the B component of the
gradient of g as DW(A)-k_g(A)cof A. The global convex tangent inequality
then implies

    B_F(A,X)+epsilon|X|^2-k_g(A)det X>=0                     (4)

for every A,X. Replace A,X by tA,tX, divide by t^4 and let t tend to
infinity. Since b is affine, (3)-(4) imply

    B_F(A,X)-2a0 det A det X>=0

globally. This is a polynomial global determinant-support selector for F,
contradicting the accepted exact 24-evaluation obstruction. No appeal to
finite numerical tests enters this argument.

If g=N(B,s)/D(B) is rational with D(B)!=0 everywhere, polynomial division
in s expresses it in form (2) after the growth reduction, with smooth
coefficient functions. The same contradiction applies. A denominator
depending on s, or another nonpolynomial normal operation, is necessary
within rational constructions.

This excludes a precisely specified architecture. It does not exclude a
rational/algebraic smooth lift with s-dependent denominator, or a finite
semidefinite operation; the latter is acquired separately and has corners.
