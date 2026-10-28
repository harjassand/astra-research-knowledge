# Strict PC support with rational homogeneous selectors: a complete finite hierarchy

This is a construction from standard compact approximation and the
Scherer–Hol matrix Positivstellensatz. It is not claimed as a new general
positivity hierarchy, an efficient algorithm, or a proof that the symmetric
target is PC. Its purpose is to remove a genuine selector restriction exposed
by `PROOF.md`: arbitrarily high norm multipliers in X cannot repair a failed
polynomial selector.

## Statement

Let \(F:\mathbb R^{2\times2}\to\mathbb R\) be a homogeneous quartic, and
write \(B_F(A,X)=F(A+X)-F(A)-DF(A):X\). The following conditions are
equivalent.

**(S)** There are constants \(a,b>0\) such that, for every A, there exists a
real scalar \(k_A\) satisfying
\[
B_F(A,X)-k_A\det X
\geq a|A|^2|X|^2+b|X|^4\qquad\hbox{for every X}.          \tag{1}
\]
No regularity, polynomial form, or common formula for the scalars is assumed.

**(R)** There are an integer \(m\geq1\), a homogeneous polynomial
\(p\) of degree \(2m\) in the four entries of A, and \(\delta>0\), such
that
\[
k(A)=\frac{p(A)}{|A|^{2m-2}}\ (A\ne0),\qquad k(0)=0,     \tag{2}
\]
satisfies (1) with \(a=b=\delta\).

**(C)** For some m,p as above and \(\delta>0\), there are an SOS polynomial
matrix \(Q(A,R)\) of size2 and arbitrary symmetric polynomial matrices
\(U(A,R),V(A,R)\) such that the literal polynomial identity
\[
M_p(A,R)-\delta I_2
=Q(A,R)+(1-|A|^2)U(A,R)+(1-|R|^2)V(A,R)                 \tag{3}
\]
holds, where
\[
M_p(A,R)=
\begin{pmatrix}
\frac12D^2F(R)[A,A]-p(A)\det R & \frac12DF(R):A\\
\frac12DF(R):A & F(R)
\end{pmatrix}.                                         \tag{4}
\]
If F has rational coefficients, p, delta, the ideal multipliers and an SOS
Gram matrix in (3) can all be taken rational, with the Gram matrix positive
definite on a complete finite monomial feature set.

Every finite certificate (3) proves a finite real-valued convex lift of F
in \((A,\det A)\), a uniform compatible-gradient energy inequality, and
strict ROC. The theorem asserts no degree, bit, runtime or negative-decision
bound. It does not assert finite termination at every boundary PC quartic.

## 1. The two-by-two matrix reduction

Quartic polarization gives
\[
B_F(A,tR)=t^2\left[\frac12D^2F(R)[A,A]
                          +t\,DF(R):A+t^2F(R)\right].   \tag{5}
\]
For \(|A|=|R|=1\), condition (1) is equivalent to
\[
M_k(A,R)\succeq\operatorname{diag}(a,b),                 \tag{6}
\]
where \(M_k\) is (4) with p(A) replaced by k_A. To see the equivalence,
divide (1) by t² and use every real t. A quadratic nonnegative for all t
is exactly a PSD two-by-two matrix; the case with vanishing first coordinate
follows by its leading coefficient. This is a global support condition,
not a finite subset of sampled increments.

If (4) is at least delta I on the product of unit spheres, use (2), write
\(A=\rho A_0\), \(X=\eta R_0\), and apply (5):
\[
B_F(A,X)-k(A)\det X
=\eta^2(\rho,\eta)M_p(A_0,R_0)(\rho,\eta)^T
\geq\delta(\rho^2\eta^2+\eta^4).                        \tag{7}
\]
At A=0 the assertion follows from the bottom-right entry F(R). There is
no division by a zero A and no cancelled-origin claim.

For completeness the finite lift is explicit. Put
\[
\ell_A(B,t)=F(A)+[DF(A)-k(A)\operatorname{cof}A]:(B-A)
                         +k(A)(t-\det A),\qquad
g(B,t)=\sup_A\ell_A(B,t).
\]
Equation (7) makes these minor-affine functions lower supports, with
equality on the graph at B=A. Euler's identity writes their constant
term as -3F(A)+k(A)detA. Taking X=-A in (7) bounds this term above by
-2delta|A|⁴. The other terms grow at most cubically or quadratically in A,
since k is degree-two homogeneous and bounded on the unit sphere. Thus
g is finite everywhere and equals F on the minors graph. Integrating (7)
against compatible gradients removes the derivative and determinant terms
by the usual zero-boundary null-Lagrangian identities.

## 2. From arbitrary pointwise scalars to a continuous even sphere selector

Only unit A are considered initially. At a fixed A0, choose a scalar k0
from (S). The matrix \(M_{k_0}(A_0,R)\) is uniformly positive on the compact
unit R sphere, by (6). Since its entries are continuous in A and R, the
same constant scalar k0 remains feasible with half the positive matrix
margin in a neighborhood of A0. A finite such cover and a continuous
partition of unity produce a continuous feasible scalar function on the
unit A sphere: the matrix is affine in its selector entry, so convex
averaging preserves the reduced uniform margin.

The function may be made even by averaging its values at A and -A.
Indeed \(M_k(-A,R)\) is congruent to \(M_k(A,R)\) by
\(\operatorname{diag}(1,-1)\), apart from the chosen scalar. Feasibility
therefore transfers with the same scalar and margin. The averaged selector
is continuous and even. This step does not assert that it is polynomial.

## 3. Polynomial approximation on the sphere and homogeneous extension

Polynomials are uniformly dense in the continuous functions on the unit
sphere. Approximate the continuous even selector, average away odd total
degrees, and homogenize all remaining monomials to one even degree2m by
multiplication with powers of \(|A|^2\). The polynomial on the sphere is
unchanged by homogenization. If necessary raise the degree to at least2.

An error of epsilon in the sphere selector changes only the upper-left
entry of (4), by at most epsilon/2, because \(|\det R|\leq1/2\) on the
unit R sphere. Thus a sufficiently accurate approximation retains a
uniform positive matrix margin. Formula (2) extends it to a continuous
degree-two homogeneous function on all matrices, even when m>1. This
proves (S) implies (R). When F is rational, choose the approximating
polynomial coefficients rational, with the same strict margin.

For m=1 this is a polynomial quadratic selector. For m>1 it is generally
rational and lies outside the polynomial-selector obstruction. There is
no claim that m=2 suffices for the target or for the class.

## 4. Finite matrix-SOS certificates on the product spheres

Use the scalar equality ideal generated by
\(g_A=1-|A|^2\) and \(g_R=1-|R|^2\). The SOS-plus-ideal matrix module is
Archimedean: \((2-|A|^2-|R|^2)I_2=(g_A+g_R)I_2\) belongs to it.
Its positivity set is exactly the product of the two unit spheres. The
established matrix Scherer–Hol theorem therefore supplies (3), after
subtracting a smaller positive delta I from a matrix that remains positive
definite there. In the module generated by both signs of the two equalities,
the non-SOS terms may be collected into the arbitrary symmetric U,V in
(3); conversely any ideal multiple is permitted in that module.

The primary theorem actually used is Theorem1.1, with the Archimedean
criteria in Lemmas2.2–2.3, of Dinh–Ho–Le,
[*Some applications of Scherer-Hol's theorem for polynomial matrices*,
arXiv:1904.00206v1](https://arxiv.org/html/1904.00206v1). This theorem and
the underlying Scherer–Hol2006 machinery are prior results. The new role
here is the explicit compact two-sphere support interface (4), with an
unrestricted sphere selector, rather than the supplied quadratic-selector
premise of the existing norm-X hierarchy.

Evaluating (3) on the spheres proves (7), so (C) implies (R) and (S).
All three conditions are equivalent.

## 5. Rational exact certificates, without a numerical feasibility assumption

Suppose F and p are rational. Subtract a small rational margin eta I
before applying the matrix theorem. Let D bound the degrees of the acquired
SOS factors. The constant matrix eta I has a Gram representation, modulo
the sphere ideal, that is positive definite on the complete feature list
of monomials of total degree at most D, tensored with the two matrix output
coordinates. To construct it, for each pair i,j with i+j<=D use the positive
diagonal multinomial identity
\[
(|A|^2)^i(|R|^2)^j
=\sum_{|\alpha|=i,|\beta|=j}
  {i\choose\alpha}{j\choose\beta}(A^\alpha R^\beta)^2.
\]
Each left side equals1 modulo the ideal. Average these identities with
positive rational weights summing to eta. Every complete-list monomial
receives a positive diagonal coefficient. Adding this Gram to the PSD
Gram for the margin-subtracted matrix makes the total Gram PD. The
corresponding ideal multipliers absorb the difference from eta I.

Coefficient matching is a rational affine system. A nonempty rational
affine system has a rational particular solution and rational nullspace
basis; rational points are dense in its real solution space. Therefore
one can choose a rational solution close enough to preserve the PD Gram.
The polynomial identity and positive definiteness then have exact rational
replays. No bounded denominator, degree or rational search time follows.

## 6. Consequence for the PC cone and the ordinary comparator

A finite polynomial F that is polyconvex has a finite convex lift in the
five minors: the convex hull of the minors graph is all R5, so a convex
lift finite on that graph has full domain. A subgradient of the lift at
each graph point gives a global scalar support k_A. These supports need
not be polynomial or continuous as initially selected.

For every epsilon>0, the quartic
\(F_\epsilon=F+\epsilon|A|^4\) satisfies (S). In fact the Bregman remainder
of \(|A|^4\) obeys
\[
B_{|\cdot|^4}(A,X)\geq\frac14\big(|A|^2|X|^2+|X|^4\big).
\]
One exact check decomposes A into its component along X and its orthogonal
component. The relevant two-by-two quadratic matrix is
\(\left(\begin{smallmatrix}6&2\\2&1\end{smallmatrix}\right)\), whose
difference from I/4 is positive definite; the perpendicular coefficient
is2. Hence rational F and rational epsilon>0 admit some finite rational
certificate (3). Conversely every such certificate proves PC. Equivalently,
every interior rational PC quartic is certified at some finite level, and
the boundary cone is approached through these strict certificates. The
closure statement also uses closedness of the PC support inequalities (or
the usual minors-Jensen characterization).

At fixed m,D, coefficient matching in (3) is finite and affine in the
selector, Gram and ideal coefficients. A complete unstructured Gram has
size \(2{8+D\choose D}\), with at most \(3{8+2D\choose2D}\) scalar
coefficient equations; p has \({2m+3\choose3}\) coefficients. This is an
explicit cost description, not an efficiency claim. Numerical SDP followed
by exact reconstruction is one acquisition method; dovetailed rational
enumeration is an in-principle one-sided procedure. Nothing guarantees a
negative answer, a modest level, or a useful practical runtime.

The parent's 80-feature rational-selector attempt is a smaller first-level
test of the same representation change, not a replay of this full
two-sphere hierarchy. Its failure on the symmetric target has no negative
logical implication. The target's actual PC and QC status remain UNKNOWN.
