# An effective bounded-witness port for rational angular heat certificates

30 October2026. Derived for root's `root_angular_receiver/HIERARCHY.md`.
This is a quantitative operation at a stronger, explicit input contract.
It credits Fang–Fawzi's polynomial-kernel proof and ordinary spherical
approximation/SOS machinery. It is not a new general Positivstellensatz,
a practical degree claim, a quasiconvexity decision procedure, or a theorem
that every ROC/QC energy has a smooth coercive heat-form witness.

## 1. What must be acquired

Let F be a rational homogeneous quartic onR4, with its compatible6-jet
dissipation D_nu from the frozen original-target proof. Suppose there
EXISTS an odd homogeneous-degree3 one-form alpha, smooth off0/C2 at0,
such that

    D_nu F+dalpha(B1,B2)>=eta T|h|²,
    |nu|<=Lambda,                                  (1)

for all A,h. The **extra supplied/qualified data** are positive rational
eta, nonnegative rational Lambda, and a rational W bounding, for EACH
coefficient f_s=alpha_s restricted toS3,

    |f_s|, |grad_S f_s|, ||Hess_S f_s|| <= W.        (2)

There is no claim these bounds follow effectively from F alone or can be
extracted from a floating search without qualification. Under this bounded
witness promise, a finite SDP degree and coefficient box can be specified
BEFORE knowing the actual witness alpha. The SDP need not query alpha.

Let H_F=12 times the coefficient-l1 norm of F, which is directly rationally
computable and bounds ||F''|| onS3. Write H_*=max(1,H_F). The construction
below gives a polynomial-size SDP in the NUMERICAL values W, eta^-1,
Lambda,H_*, in fixed physical dimension4 and jet dimension6. It is not
polynomial in their binary bit lengths. The bounds are very conservative.

## 2. Explicit C1 approximation without a hidden modulus

OnS3 with normalized measure, use the zonal polynomial kernel

    K_D f(x)=c_D integral ((1+x.y)/2)^D f(y)d sigma(y),
    c_D=(3)_D/(3/2)_D.                             (3)

This is an ordinary approximate-identity construction. The distribution
of u=(1+x.y)/2 under normalized weight is Beta(D+3/2,3/2), so

    E |x-y|²=6/(D+3).                              (4)

The kernel preserves parity and commutes with every rotation derivative
L_ij=x_i partial_j-x_j partial_i. For a C2 scalar f with the bounds(2),
geodesic distance is at most2 times chordal distance, giving

    ||K_D f-f||inf <=2W sqrt(6/(D+3)),
    ||L_ij(K_D f-f)||inf <=4W sqrt(6/(D+3)).         (5)

The second bound uses ||grad_S(L_ij f)||<=2W. Since
sum_(i<j)|L_ij g|²=|grad_S g|², the tangential derivative error is at most
24W/sqrt(D+3). The value error is at most5W/sqrt(D+3).

For an odd D>=3, K_D f is an odd polynomial of degree<=D. Homogenize it
as a degreeD numerator P with alpha_D=P/T^k, k=(D-3)/2. OnS3 the values
and tangential derivatives are unchanged, and radial derivatives are3
times the values. Thus each full derivative row error is at most
39W/sqrt(D+3); all4 rows have operator error at most78W/sqrt(D+3).
The exterior-derivative error evaluated on the compatible B1,B2 is at most

    156W/sqrt(D+3) T|h|².                          (6)

Take D to be the least odd integer at least3 and at least
(1600W/eta)². Then(6) is less than eta T|h|²/8.

Approximate nu by a rational with error at most
min(1,eta/(16H_*)). Its dissipation error is at most eta T|h|²/8 because
the mixed Hessian bracket is bounded by2H_F T|h|².

Finally round the coefficients of the odd, not-yet-homogenized polynomials
so their TOTAL coefficient-l1 error over all4 coefficients is at most
E=eta/[32(D+3)]. For a degree<=D perturbation, the corresponding
homogeneous-degree3 derivative error evaluated as a two-form is bounded
by4(D+3)E T|h|², hence by eta T|h|²/8. The new rational P,nu therefore
retain a lower bound at least5eta/8, and in particular eta/2.

This step supplies a DEGREE bound for all witnesses satisfying(2), not
only a density assertion or an unspecified modulus. Unknown alpha values
are not an oracle used by the SDP: their existence establishes finite
feasibility under the promised W,eta bound.

## 3. Primitive coefficient and bit box

On a unit sphere point y, sum|y_i|<=2. Also c_D<=2^D by its product
formula. Consequently each polynomial K_D f has coefficient-l1 norm at
most W3^D. Homogenization multiplies the coefficient-l1 norm by at most
2^D. A conservative componentwise numerator box is therefore

    |P_coefficient| <= A_P=(W+eta+1)6^D.            (7)

This bounds real coefficients, not their number by an evaluation oracle.
There are4 binom(D+3,3) homogeneous numerator coefficients. For rounding
before homogenization there are at most4 binom(D+4,4) coefficients.
A common dyadic grid with bits

    b_P >= ceil_log2(64*4*binom(D+4,4)*(D+3)/eta)

suffices for the l1 error above, with nonnegative b_P if the displayed
quantity is<1. Homogenization uses only integer coefficients. Numerator
bit sizes are therefore bounded by O(D+log(W+eta+1)+b_P).

Use a coefficient box twice(7) in the SDP, leaving strict room around the
constructed witness. Use |nu|<=Lambda+2, leaving room around its rational
approximation. This is a bounded same-input coefficient search, not an
assumption of an acquired primitive.

## 4. A fully explicit all-degree matrix Reznick port onS3

Let M(x) be ANY rational symmetric q-by-q homogeneous matrix polynomial
of degree2d, d>=1, with PAID bounds

    mI<=M<=BI onS3,  0<m<=B.                       (8)

The matrix size q is arbitrary. Our heat numerator has q=6 and
d=k+2=(D+1)/2. After the approximation above, one can take m=eta/2 and

    B=2H_F(2+Lambda)+16W+eta+1,                    (9)

because the full homogeneous derivative of alpha onS3 has norm<=8W,
and its exterior derivative evaluation is bounded by16W|h|². The bounded
approximation errors and rounded nu are included in(9). A known rational
coefficient row-l1 bound for M is an alternative computable B; m is not
silently inferred from such an upper bound.

Choose

    ell=d-1+ceil(10*(B/m)*d²(d+1)(d+2)),
    c_ell=4^ell*ell!*(ell+1)!/(2ell)!.              (10)

Let K_ell use normalized kernel c_ell(x.y)^(2ell). On a spherical harmonic
of degree2j its eigenvalue is exactly

    lambda_(2j)=ell!*(ell+1)!/[(ell-j)!*(ell+j+1)!]
               =prod_(i=0)^(j-1) (ell-i)/(ell+2+i).
                                                               (11)

This follows directly by Gaussian Wick contraction: a harmonic tensor has
no internal contractions, and radial moments inR4 divide by
2^(ell+j)(ell+j+1)!. This is also the standard Funk–Hecke kernel calculation
used in the primary Fang–Fawzi construction.

The harmonic degree2j subspace ofS3 has dimension(2j+1)². Its reproducing
kernel has L2 norm2j+1, so its projection satisfies

    ||M_(2j)||inf <=(2j+1)||M||inf,                (12)

also in matrix spectral norm by integrating the absolute scalar kernel.
For ell as above,

    lambda_(2j)^-1-1
      <=2d(d+1)/(ell-d+1),  1<=j<=d.              (13)

Indeed log(lambda^-1)<=j(j+1)/(ell-d+1)<=1/2, and exp(s)-1<=2s there.
Summing(12) gives

    ||K_ell^-1 M-M||inf
      <=2B d²(d+1)(d+2)/(ell-d+1).                (14)

Apply this to M0=M-(m/4)T^dI. It remains positive and has norm<=B.
At(10), (14)<=m/5, so

    H=K_ell^-1 M0 >= (11m/20)I > (m/2)I onS3.     (15)

Fang–Fawzi Theorem6's first/kernel part is the strongest direct primary
predecessor. Its headline O(dim²/ell²) theorem assumes halfdegree<=dim,
which cannot simply be used for arbitrarily large k at fixed dimension4.
Our explicit monomial kernel is weaker but all-degree, rational and has
no unspecified degree constants. The primary optimized Gegenbauer/Toeplitz
kernel operation is granted to the equally informed ordinary comparator.

## 5. Literal rational Gram, weighted Slater margin and coefficient bound

For |alpha|=ell let b_alpha=multinomial(ell;alpha). Homogenize H's harmonic
decomposition back to total degree2d if desired; its values onS3 suffice.
Define the q*binom(ell+3,3) square Gram by

    (Q0)_((alpha,i),(beta,j))
       =c_ell b_alpha b_beta integral y^(alpha+beta) H_ij(y)d sigma(y).
                                                               (16)

It is PSD: its quadratic form is the integral of a vector polynomial's
quadratic form in the positive matrix H(y). The kernel identity and
homogeneity give

    (mon_ell(x) tensor h)^T Q0 (mon_ell(x) tensor h)
        =T^(ell-d) h^T M0(x)h.                   (17)

All entries are rational. For a multi-index r,

    integral y^(2r) d sigma
       =prod_i (2r_i-1)!!/[2^|r|(|r|+1)!],        (18)

and odd moments vanish. Spherical harmonic/Fischer decomposition of a
rational polynomial is rational; explicit Laplacian formulas or rational
linear elimination acquire it, not a spectral-function oracle.

Add the EXACT diagonal Gram for (m/4)T^ell I:

    Q=Q0+(m/4)D_ell,
    D_ell=diag(b_alpha) tensor I_q.

Then Q>= (m/4)D_ell>= (m/4)I. This is a known WEIGHTED Slater margin,
not an unknown minimum Gram eigenvalue. It also avoids an unnecessary
loss of the largest multinomial coefficient in the heat receiver:
z^T D_ell z=T^ell|h|², so the certified corrected dissipation is at least
(m/4)T|h|², independently of ell. A standalone verifier can store a
rational factor/residual for Q-rho D_ell, just as the original certificate
qualified Q-rho I. No irrational square-root basis is required.

Moreover c_ell<=4^ell, b_alpha<=4^ell, ||H||<=2B, so every Gram entry has

    |Qij|<=3B*64^ell.                             (19)

Thus BOTH an interior margin and a finite coefficient box have been paid.
Zheng–Fantuzzi2007.11410v2 Theorem2.3 already proves eventual matrix SOS
existence; (10)–(19) are an explicit quantitative rational operation for
this fixed sphere, composed from their ordinary predecessors. No generic
matrix-SOS or chordal-decomposition priority is claimed.

## 6. Complete cost and what remains unpaid

The Gram dimension is n_G=q*binom(ell+3,3)=O(q ell³); writing its dense
entries costs Omega(q²ell^6). A direct implementation computes the
harmonic decomposition in polynomial rational work in q,d,input bits,
then each Gram entry by O(d³) exact moment terms. Total direct arithmetic
work is O(n_G² d³) after the harmonic decomposition, with cached factorials
and moments. Rational bit lengths are polynomial in the input coefficient
bit length, d and ell: harmonic inverses use O(d²log(ell+d)) bits of common
denominators, and the common moment denominator is
2^(ell+d)(ell+d+1)! with O((ell+d)log(ell+d)) bits. Multiplication by the
binomial coefficients adds O(ell) bits. A coarser polynomial-bit bound
also follows by taking products of all finitely many input denominators.

For the heat search, D=O(1+(W/eta)²), d=(D+1)/2 and (10) specify a finite
level; N=ell-d. Its affine identity matrix has rational coefficients and
can be acquired by sparse monomial differentiation. Bounds(7),(19) and
the weighted Gram floor give explicit finite boxes/interior scales for
ordinary weak-SDP methods on the rational identity affine space. Exact
verification remains required after numerical acquisition. This does not
claim that a particular floating solver is guaranteed to return a proof.

The operation's guarantee needs the actual bounded-witness promise(1),(2).
Without acquired eta,W,Lambda, root's qualitative semidecision theorem is
the honest remaining baseline; the present bounds do not turn it into a
uniform finite cutoff for arbitrary F. Boundary/noncoercive witnesses,
arbitrary QC energies, a priori useful thresholds, practical runtime and
native material qualification remain outside scope. No new source,
optimizer fixture, physical experiment or sample was run for this port.
