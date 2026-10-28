# The six even coefficients, the three odd coefficients, and the missing support interface

This records the independent geometric route. It does not prove that the
six-parameter ROC sector is PC. The exact obstruction in `PROOF.md` shows
why a proof through polynomial support selectors cannot cover that whole
sector, regardless of how high its norm-X multiplier degree is taken.

## 1. Exact nine-coefficient coordinates

Let z=(a+ic,b+id), T=u+v and h=(x,y,zeta)=(u-v,2w,2q). Then
T²=|h|², and the Hopf map reaches every h in R3. For example, given h,
set T=|h|, u=(T+x)/2, v=(T-x)/2, w=y/2, q=zeta/2, then reconstruct real
columns with squared norms u,v and dot product/determinant w,q.

Every left-row-SO(2)-invariant homogeneous quartic is uniquely
\[
F(A)=h^TKh+T\ell\cdot h,\qquad K=K^T\in\mathbb R^{3\times3},
\quad\ell\in\mathbb R^3.                                \tag{1}
\]
For coefficient basis
\((u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)\) with coefficients p0,...,p8,
put alpha=(p0+p1+p2)/4. The exact conversion is
\[
\begin{split}
K_{11}&=(p_0+p_1)/2,&K_{22}&=\alpha+p_3/4,&K_{33}&=\alpha,\\
K_{12}&=(p_4-p_5)/8,&K_{13}&=(p_6-p_7)/8,&K_{23}&=p_8/8,\\
\ell_1&=(p_0-p_1)/2,&\ell_2&=(p_4+p_5)/4,&\ell_3&=(p_6+p_7)/4.
\end{split}                                             \tag{2}
\]
The antiunitary spin flip J(z1,z2)=(-conj(z2),conj(z1)), or
\(JA=(-b,a,d,-c)\) in row-major entries, sends h to -h and preserves T.
It is a rank-one-preserving orthogonal transformation and reverses q.
Averaging F with F composed with J projects onto the six even coefficients
K, and preserves ROC, QC, or PC whenever the original energy has the
respective property. It does not transfer a non-PC obstruction through
averaging without further proof.

The Dacorogna–Marcellini odd term T*zeta lies in the other three
coefficients. Known wider DM ROC/non-PC examples therefore do not decide
the even-sector question. Conversely an even-sector theorem would not
classify all nine coefficients.

## 2. Equatorial acoustic criterion and a necessary positivity theorem

The general even-sector ROC matrix is (4)–(5) of `PROOF.md`, with K written
in the equatorial frame (e,m,e3). This is an exact continuum criterion;
the rank-one restriction becomes e3-coordinate zero in Hopf space.

Write K in blocks \(K=\left(\begin{smallmatrix}B&d\\d^T&r\end{smallmatrix}\right)\),
where B is2 by2. ROC implies B is PSD because the acoustic matrix has
entry6 e^T B e for every equatorial unit e. If k=e^TBe=0, positivity
of that matrix forces e·d=0. Thus d belongs to the range of B. Its
principal block in the radial/vertical perturbations gives
\[
r\geq\frac{k}{2}+\frac{3(e\cdot d)^2}{2k}\quad(k>0).
\]
Taking the supremum of the ratio yields
\[
r\geq\frac32d^TB^\dagger d\geq d^TB^\dagger d,
\]
with the B=0 case handled directly. Hence **every even-sector ROC K is
PSD**, and every such energy is pointwise nonnegative. Strict ROC gives
positive definiteness. This is a necessary statement, not a PC support
construction. It explains why importing the negative-value DM obstruction
cannot settle this sector.

For the aligned four-parameter slice, B is diagonal and d lies on an
eigenvector. The acoustic Schur diagonals become affine in cos²theta and
its determinant is quadratic. The new exact symmetric target exploits
this finite analytic ROC reduction. A general five-essential-parameter K
(after one column rotation) still has a genuine equatorial optimization.

## 3. A direct quadratic-support geometry, beyond SOS

Assume K is PD and try a quadratic selector k(A)=c·h(A). Put
\[
M=K-\frac14c e_3^T,\qquad
f(n)=n^TKn,\quad a(n)=n^TMn,\quad v(n)=Mn,
\quad g(n)=f(n)\operatorname{tr}K-n^TK^2n.
\]
For unit n=h(R)/|R|², define the Schur matrix of K in the plane n-perp,
\[
S(n)=K_{n^\perp,n^\perp}
       -\frac{K_{n^\perp,n}K_{n,n^\perp}}{f(n)}.
\]
In the branch a(n)>0, the exact support matrix inequality
\[
T_F(R)-\det R\,C_c\succeq0,\qquad A^TC_cA=c\cdot h(A),
\]
is equivalent to
\[
2S(n)\succeq\frac{|Mn|^2}{n^TMn}I_2.                    \tag{3}
\]
One derivation uses the orthonormal perturbation frame radial/phase/two
Hopf tangents. If l is the tangential part of Kn, and eta that of c,
the top2 by2 block after dividing by2 is aI, its cross block has
Gram |l-n3 eta/4|² I, and the lower Schur block is exactly (3).

The trace and determinant of S are
\(\operatorname{tr}S=g/f\) and \(\det S=\det K/f\) for unit n.
Consequently (3) is equivalent to nonnegativity of two ternary forms:
\[
\begin{split}
L(n)&=a(n)g(n)-f(n)|Mn|^2,\\
D(n)&=4\det K\,a(n)^2|n|^2
       -2|Mn|^2a(n)g(n)+|Mn|^4f(n).
\end{split}                                             \tag{4}
\]
Their degrees are4 and6; the factor |n|² in D is required for homogeneous
degree6. The condition a>0 is a separate hypothesis, not silently inferred
from the two forms. Semidefinite cases with a=0 need direct block checks.
On the equator, c cannot change M n; (3) reduces exactly to the ROC
Schur criterion. The missing polynomial-selector interface is a linear
extension off that equator that satisfies (3) on the whole sphere.
The 24-atom theorem proves that such an extension need not exist, even
with exact strict equatorial positivity. This is a real obstruction to
that proof strategy, not to every nonlinear selector.

## 4. Symmetry determines the first genuinely nonlinear rational selector

For the exact aligned target, average a proposed selector equivariantly
under left row rotations, J, and the column swap S. Under J and S the
selector changes sign, because determinants do; under left rotations it
is invariant. The denominator |A|^(2m-2)=T^(m-1) is invariant under all
these transformations.

A left-invariant numerator p of degree2m is a degree-m polynomial in
(T,h), modulo T²=|h|². J-equivariance forces it odd in h. For m=2 its
only possible terms are T times a linear form in h. The column swap
sends (x,y,zeta) to (-x,y,-zeta), so the linear y term is removed.
Thus p4/T is exactly alpha*x+beta*zeta. A larger SOS matrix cannot make
that degree-four numerator escape the polynomial-selector obstruction.
Without the column-swap restriction, the same argument gives a linear
form in all three h coordinates. Thus the m=2 collapse holds throughout
the six-parameter even sector, not only for this aligned target.

For m=3 the first genuine numerator space is
\[
\{x^3,x^2zeta,xzeta^2,zeta^3,xy^2,y^2zeta\},\qquad
k=p_6/T^2.                                               \tag{5}
\]
Two combinations reproduce the old linear selectors through
T²=x²+y²+zeta², leaving four new nonlinear directions. More generally,
an even m numerator has an overall factor T after J projection and adds
no selector beyond the preceding odd m. New symmetry-compatible rational
degrees occur at m=1,3,5,..., not at every integer.

The parent independently raised the m=2 collapse while implementing the
first rational-selector attempt; I independently confirmed it from the
Hopf/J representation. The parent owns the concrete m=3 180-feature
acquisition. `RATIONAL_SELECTOR_COMPLETENESS.md` concerns an unrestricted
eventual level and does not promise success of this first permitted one.

## 5. Failures and source boundaries

The direct opposite-determinant test is the completed support-interval
criterion in the earlier sector-gap proof. My fixed-line search,100 K
numerical screening run, and targeted exact-energy search found no true-PC
obstruction; all remain diagnostics. The aligned-target strict ROC proof
and all-polynomial-selector obstruction are the exact results.

The quartic Hessian-polarization/generalized-eigenvalue strategy predates
this work. I read the introduction and the fourth-degree reduction and
Examples1–3 in Bandeira–Pedregal2009, DOI10.1016/j.anihpc.2008.08.002,
using the provided primary text and canonical PDF
https://www.numdam.org/item/10.1016/j.anihpc.2008.08.002.pdf . That read
scope gives no six-parameter PC classification. A failed web query does
not establish absence. Historical novelty beyond the actual checked
sources is UNKNOWN.

The fixed trace-free line's exact boundary PC support is an accepted input
from the peer/parent, not a result certified by the numerical searches
here. Its certificate hash is
66901f304531cbc969ccc7f89e5a7e57091e57cefba21133355b0d2cb54be554.
The present exact nonnegative-support obstruction is stronger than an SOS
class separator, but still leaves actual PC and QC of its target open.
