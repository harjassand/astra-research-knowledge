# A strict ROC quartic with no polynomial global minor-support selector

All matrix-entry vectors in this note are row-major. Put
\[
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc,
\qquad A=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]
Consider the rational quartic
\[
F=p_0(u^2+v^2)+p_2uv+p_3w^2+Lq(u-v),                 \tag{1}
\]
where
\[
p_0=\frac{55220381}{10^{10}},\quad
p_2=\frac{114430029}{625000000},\quad
p_3=-\frac{801761987}{5000000000},\quad
L=\frac{118849817}{4000000000}.
\]
The energy is the parent's exact symmetric target, not a new independently
selected energy. Its source JSON SHA256 is
`88769c8c3ff995312e7a34967c43959e4e46715b59d3ad781cbba545194ab4f3`.

**Theorem.** Energy (1) is strictly rank-one convex. There is no polynomial
\(k:\mathbb R^4\to\mathbb R\), of any degree, such that
\[
P_k(A,X):=F(A+X)-F(A)-DF(A):X-k(A)\det X\geq0
\quad\text{for every }A,X.                            \tag{2}
\]
Consequently it has no polynomial global minor-affine support map, even when
the support remainder is allowed to be an arbitrary nonnegative polynomial
rather than an SOS. No power of \(|X|^2\), or other multiplier positive away
from the origin, can remedy (2) while retaining a polynomial selector.

This theorem does **not** prove that (1) is non-polyconvex or non-quasiconvex.
A nonlinear homogeneous selector need not be a polynomial. The fixed-line
threshold \(89-12\sqrt{42}\) was independently settled positively elsewhere;
(1) belongs to a different trace-free slice. These facts do not settle (1).

## 1. Exact continuum rank-one convexity

Define
\[
h=(x,y,z)=(u-v,2w,2q),\qquad T=u+v,\qquad T^2=|h|^2.
\]
Using \(uv=w^2+q^2\), (1) is \(h^TKh\), with
\[
K=\begin{pmatrix}k_1&0&d_0\\0&k_2&0\\d_0&0&r\end{pmatrix},
\quad
(k_1,k_2,d_0,r)=
\left(\frac{55220381}{10^{10}},\frac{84449313}{10^{10}},
\frac{118849817}{16000000000},\frac{970660613}{20000000000}\right).
                                                               \tag{3}
\]
Here \(k_1,k_2,k_1r-d_0^2>0\), so \(K\succ0\) and \(F(A)>0\) for
every nonzero \(A\).
For any homogeneous quartic, polarization gives
\(D^2F(A)[R,R]=D^2F(R)[A,A]\). Thus ROC is equivalent to positive
semidefiniteness of \(D^2F(R)\) at every rank-one \(R\). Left row rotations
and homogeneity reduce such \(R\) to a unit real spinor. Its Hopf vector is
\(e=(\cos\theta,\sin\theta,0)\). Write the matrix of \(K\) in the frame
\((e,(-\sin\theta,\cos\theta,0),(0,0,1))\) as
\[
\begin{pmatrix}k&l&m\\l&n&p\\m&p&r\end{pmatrix}.
\]
In an orthonormal real perturbation frame, direct differentiation gives
\[
\frac12D^2F(R)=
\begin{pmatrix}
6k&0&6l&6m\\
0&2k&-2m&2l\\
6l&-2m&4n-2k&4p\\
6m&2l&4p&4r-2k
\end{pmatrix}.                                         \tag{4}
\]
For \(k>0\), its Schur complement is \((2/k)N\), where
\[
N=\begin{pmatrix}
2kn-k^2-3l^2-m^2&2(kp-lm)\\
2(kp-lm)&2kr-k^2-3m^2-l^2
\end{pmatrix}.                                         \tag{5}
\]
For aligned (3), set \(s=\cos^2\theta\). Both diagonal entries are affine:
\[
\begin{split}
N_{11}(s)&=2k_1k_2-k_2^2-(k_1^2-k_2^2+d_0^2)s,\\
N_{22}(s)&=2r[k_2+(k_1-k_2)s]-k_2^2
                         -(k_1^2-k_2^2+3d_0^2)s,\\
N_{12}(s)^2&=4d_0^2k_2^2(1-s).
\end{split}                                             \tag{6}
\]
Hence the continuum test is two endpoint signs and a quadratic minimum on
\([0,1]\), without a sampled-angle approximation. Here \(k_1,k_2>0\),
\[
N_{11}(0)=\frac{2194960011924537}{10^{20}}>0,\qquad
N_{11}(1)=\frac{9723761799317771}{128\cdot10^{19}}>0.
\]
The quadratic \(\det N(s)\) has positive leading coefficient and its
stationary point lies strictly inside \((0,1)\). Its exact minimum is
\[
\frac{205184468993914800287227166151492251477210888930451710201219712027}
{12805781385781164210100480258127516320000000000000000000000000000000000000000}
>0.                                                       \tag{7}
\]
Equations (4)–(7) give positive definiteness at every unit rank-one state,
and compactness gives a positive uniform ROC margin. The independent
standard-library verifier reconstructs (6) and (7) directly from (1).

## 2. Why all polynomial degrees reduce to ten monomials

This is the same homogeneous scaling mechanism used in the completed
quartic gap proof; it applies to global nonnegativity without SOS.
If the largest nonzero homogeneous piece of \(k\) has degree \(j>2\),
simultaneous scaling \((A,X)\mapsto(tA,tX)\), \(t\to\infty\), makes the
leading term of (2) equal \(-t^{j+2}k_j(A)\det X\). Choosing the determinant
sign makes it negative. If the smallest nonzero degree is \(j<2\), use
\(t\downarrow0\) instead. Thus every polynomial solution must be a
homogeneous quadratic, with its ten unrestricted monomials \(A_iA_j\).

More generally, suppose a polynomial map \((V(A),k(A))\) supplies minor
support in variables \((B,\det B)\). At \(B=A\), its nonnegative remainder
vanishes. Its first derivative there forces
\(V=DF-k\operatorname{cof}A\); substitution \(B=A+X\) gives exactly (2).
Thus excluding the ten quadratic monomials excludes every polynomial map.

## 3. Three actual rational support cuts

For positive quartic \(F\), define
\[
T_F(R)=\frac12D^2F(R)-\frac{DF(R)DF(R)^T}{4F(R)}.
\]
Quartic polarization and minimization of one real scale show that (2)
implies
\[
A^TT_F(R)A-k(A)\det R\geq0.                            \tag{8}
\]
Indeed
\[
\frac{P_k(A,tR)}{t^2}
=\frac12D^2F(R)[A,A]+t\,DF(R):A+t^2F(R)-k(A)\det R,
\]
whose minimizing scale is \(t=-DF(R):A/[2F(R)]\). The three cuts below
have strictly positive \(F(R)\) and nonzero minimizing scales. Nothing
requires an optimizer, a pseudo-moment distribution, or an SOS dual for
their exact verification.

| i | row-major R_i | row-major A_i |
|---|---|---|
|1| (967,-167,0,-190)/1000 | (136,675,718,-103)/1000 |
|2| (491,-850,0,-191)/1000 | (-641,-624,240,-377)/1000 |
|3| (872,485,0,63)/1000 | (-663,605,257,359)/1000 |

Their positive weights are
\[
(\lambda_1,\lambda_2,\lambda_3)=
\frac{(3791692271595700368,7689831134150867760,3012134983669509425)}
{14493658389416077553}.
\]
They sum to one. With
\(a_i=\det R_i\,x(A_i)\), \(b_i=\det R_i\,z(A_i)\),
\(c_i=A_i^TT_F(R_i)A_i\), exact arithmetic gives
\[
\sum_i\lambda_i a_i=\sum_i\lambda_i b_i=0,\qquad
\sum_i\lambda_i c_i=E< -\frac1{100000},                 \tag{9}
\]
where the literal value is stored in the certificate (approximately
\(-1.0132159550\cdot10^{-5}\)). Already (9) contradicts every selector
\(k=\alpha x+\beta z\).

## 4. Twenty-four positive atoms annihilate all ten selectors

The symmetry reduction need not be trusted to exclude other quadratics:
the actual certificate symmetrizes the rational evaluation points.
Let
\[
L_0(a,b,c,d)=(-c,-d,a,b),\quad
J(a,b,c,d)=(-b,a,d,-c),\quad
S(a,b,c,d)=(b,a,d,c).
\]
Each is orthogonal and preserves (1); \(L_0\) preserves determinants,
whereas \(J,S\) reverse them. Use the eight representatives
\(G=L_0^eJ^fS^g\), \(e,f,g\in\{0,1\}\). Their projective action is
sufficient because all expressions have even total degree. For each cut,
put \(t_i=-DF(R_i):A_i/[2F(R_i)]\) and create the atom
\[
(A,X)=(GA_i,t_iGR_i),\qquad
\omega=\frac{\lambda_i}{8t_i^2}>0.
\]
These are 24 actual points of \(\mathbb Q^8\) with positive rational
weights. Their evaluation functional \(\mathcal L\) satisfies
\[
\mathcal L(A_jA_k\det X)=0\quad(0\leq j\leq k<4),\qquad
\mathcal L\big(F(A+X)-F(A)-DF(A):X\big)=E<0.             \tag{10}
\]
Every equation in (10) is checked literally. If (2) held for a quadratic
\(k\), positivity of the weights would imply \(\mathcal L(P_k)\geq0\),
while (10) makes it \(E<0\). This proves the theorem using all ten
directions, independently of the informal symmetry argument.

## 5. Reproducible scope and remaining question

`build_polynomial_selector_obstruction.py` acquired the exact certificate
from the numerical necessary cuts and expanded the symmetry atoms in .69s.
`verify_atomic_obstruction.py` independently uses only standard-library
`Fraction`, directly evaluating the nine literal invariant terms and their
directional derivative. It checks all positive weights, all ten zero
annihilators, the negative pairing, and the continuum ROC quadratic in
.0049s on this host. These are replay timings, not a scientific or
computational complexity claim.

Certificate SHA256:
`e51d9be90ba977c34f5daab4a75901eb6acc377dc53c0004d479425fed945d22`.

The ordinary comparator has been strengthened from a finite-degree SOS
test to **every polynomial selector with unrestricted global positivity**.
The obstruction is finite and exact, so it remains strict under sufficiently
small perturbations of all 35 quartic coefficients; strict ROC is also
open. This qualitative neighborhood statement does not rely on exact
symmetry of a perturbed energy. The parent separately owns quantitative
full-35 perturbation reconstruction.

The genuine remaining mathematical question is whether (1) admits a
nonlinear homogeneous global selector, or instead has an exact
opposite-determinant support obstruction. The retained five-parameter
search found no latter witness; it proves no positive statement. The
parent's first rational-selector attempt is also only a numerical failure.
Neither failure determines actual PC or QC. The broader six-parameter
ROC-to-PC question and nine-coefficient ROC/QC question remain open here.
