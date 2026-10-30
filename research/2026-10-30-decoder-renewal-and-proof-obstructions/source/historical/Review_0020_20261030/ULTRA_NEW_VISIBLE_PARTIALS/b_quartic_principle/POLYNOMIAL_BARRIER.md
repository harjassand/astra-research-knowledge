# Exact polynomial/regularity barrier, without an SOS assumption

Use F* and C(A)[h] from `THEOREM_REDUCTION.md`. The theorem here is:

**There is no closed 2-form Omega with coefficients C² near the
origin such that (5) is nonnegative for every A,h. In particular no
polynomial 1-form of ANY degree supplies such a completion. The same
holds for every constant mean-converging second-order flow.**

This excludes origin-regular closed-form heat proofs, not actual heat
monotonicity by all possible arguments. It does not exclude the full
angular exact-form class (Omega C¹ at zero), and does not prove non-QC.

## 1. Why homogeneous quadratic coefficients suffice for this theorem

Let W(Omega) denote the symmetric 6×6 matrix representing
Omega(B1,B2) on compatible h. Its acoustic symbol vanishes. If
W(Omega)≥0, every rank-one h=eta⊗xi⊗xi belongs to its kernel.
Those h span R²⊗Sym²(R²), which is the whole six-dimensional compatible
Hessian space. Hence W(Omega)=0. The map Omega→W(Omega) is injective:
the six wedge entries have respectively the unique monomials

    h0 h2, h0 h4, h0 h5, −h2 h3, h1 h5, h3 h5.

Thus a pure wedge term cannot be nonnegative unless Omega=0.

For a C² coefficient field, Taylor-expand at zero. Positivity at A=0
forces Omega(0)=0 by this observation. Substituting A=tA0, dividing
by t and passing t↓0 forces the linear coefficient to vanish as well.
Divide the remaining inequality by t²: its limit is

    C_F*(A0)+W(Omega2(A0))≥0,                            (9)

where Omega2 is the quadratic Taylor coefficient. Closedness implies
d Omega2=0. Therefore existence of the original smooth completion
would imply a closed quadratic-coefficient completion. This argument
allows a nonhomogeneous field, not just polynomial primitives.

If alpha is C³, d alpha is C²; any polynomial alpha is therefore
included. An angular homogeneous alpha=P5/T is not included merely
because its coefficients happen to be C² at zero.

## 2. Symmetry and a forced second acoustic null vector

Average (9) over the compact literal symmetries

    A→Rtheta A, A→C A C, A→A S,
    C=diag(1,−1), S=[[0,1],[1,0]].

The last two reverse spatial orientation, so their transported forms
have the minus sign in THEOREM_REDUCTION (6). The averaged quadratic
field remains closed and feasible.

At A=I, take xi=(t,1), eta=(1,−2t/(1+t²)), and let

    r(t)=(eta1 t²,eta1 t,eta1,eta2 t²,eta2 t,eta2).

The correction vanishes on r(t), and literal differentiation gives

    r(t)^T C(I) r(t)=64t⁴.

For a positive semidefinite C(I), the constant and linear coefficients
of C(I)^(1/2) r(t) vanish. Hence its kernel contains

    h0=(0,0,1,0,0,0), h1=(0,1,0,0,0,−2).               (10)

This is a consequence of fourth-order acoustic degeneracy, not an
assumed Gram kernel or a finite-degree heuristic.

## 3. The entire closed equivariant class has one parameter

A general quadratic-coefficient 2-form has 6×10=60 real coefficients.
Impose:

* d Omega=0;
* Lie invariance under JA, with
  J(a,b,c,d)=(−c,−d,a,b);
* anti-invariance under C A C and A S (the spatial signs above);
* C(I) h0=C(I) h1=0.

These are linear coefficient identities. Their exact rank is 59.
Write the remaining parameter z as the coefficient of d² in Omega23.
The full class is the skew matrix determined by

    Omega01=z(a²+b²)−4(z+12)(ad+bc)+3(z+16)(c²+d²),
    Omega02=−4(z+12)T−8(z+18)(ad−bc),
    Omega03=4(z+12)(ab−cd)−2(z+24)(ac+bd),
    Omega12=−Omega03,
    Omega13=4(z+12)T−8(z+18)(ad−bc),
    Omega23=3(z+16)(a²+b²)+4(z+12)(ad+bc)+z(c²+d²).
                                                               (11)

These formulas can be verified by direct substitution. Exhaustiveness
is independently paid twice: `quadratic_completion.py` expands all
identities symbolically; `qualify_quadratic.py` constructs the 60
sparse monomial columns and performs Fraction elimination without
importing that producer or an SDP. Both give rank 59 and (11).

## 4. Two exact evaluations contradict positivity

Use the SAME h1 from (10) and let A(t)=diag(1+t,1). Substitution of
(11) into the literal completed density gives

    C(A(t))[h1]=2zt−(9z+16)t².                            (12)

In particular at t=±1/8,

    C(diag(9/8,1))[h1]=(7z−16)/64,
    C(diag(7/8,1))[h1]=(−25z−16)/64.

Their positive weighted sum, with weights 25 and 7, is exactly −8.
They cannot both be nonnegative, for any real z. This concludes the
no-completion theorem. Equivalently the derivative at t=0 first forces
z=0, and then (12)=−16t² already contradicts positivity.

This is an exact algebraic obstruction to the FULL closed polynomial
class, not a SOS obstruction: C(A) was required positive semidefinite
pointwise, not represented by a global polynomial Gram.

For a general constant mean-converging flow use the exact symmetry and
acoustic rigidity of THEOREM_REDUCTION §5; it reduces any proposed
origin-C² completion to ordinary heat before the preceding argument.

## 5. What must replace this operation

Combining this theorem with the extreme-ray/non-PC proof excludes
finite decompositions into polyconvex quartic polynomials and quartic
heat parts having origin-C² corrections. Polynomial high-degree
escalation does not evade it. A new proof at F* must instead use an
angular correction with an unavoidable origin regularity loss, a
different nonconstant/nonlinear operation, nonpolynomial integrand
summands, or a different QC mechanism.

The result does not contradict ROOT26's no-finite-atomic-obstruction
theorem for the FULL smooth angular class. Our finite-dimensional
field identities prevent arbitrary local values at different angular
points, whereas the admitted smooth angular class has those values.
No exact finite atomic dual for that larger class has been claimed.

No claim of historical priority, nonquasiconvexity, physical response,
or an efficient universal QC algorithm follows from this calculation.
