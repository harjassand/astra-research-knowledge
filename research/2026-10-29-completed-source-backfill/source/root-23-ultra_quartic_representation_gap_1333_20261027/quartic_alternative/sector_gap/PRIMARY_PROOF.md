# An exact planar quartic gap between polyconvexity and polynomial SOS support

This note proves a global statement, using rational identities and positive
definiteness certificates. No numerical infeasibility is used as a theorem.
The positive certificate was acquired in this folder; the independent negative
dual was acquired by the parent in `../../principal_combined_quartic/`.

## Statement and exact convention

Write

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc.
\]

Throughout, \(|A|\) is the Frobenius norm and \(DF(A):X\) is the ordinary
entrywise derivative pairing. Define

\[
F(A)=u^2+v^2+3w^2+\frac{113}{10}q^2+4q(u-v).                 \tag{1}
\]

**Theorem.** The homogeneous quartic (1) has a finite convex lift in its five
minors \((a,b,c,d,q)\), and hence is polyconvex. For every bounded Lipschitz
domain \(\Omega\subset\mathbb R^2\), every \(A\in\mathbb R^{2\times2}\), and
every \(\varphi\in W^{1,4}_0(\Omega;\mathbb R^2)\),

\[
\int_\Omega\!\big[F(A+D\varphi)-F(A)\big]\,dx
\geq\frac{|A|^2}{400}\int_\Omega|D\varphi|^2\,dx
   +\frac1{1200}\int_\Omega|D\varphi|^4\,dx.               \tag{2}
\]

It is not SOS polyconvex under Definition 2.5 of the pinned primary source
[Fantuzzi et al., *Polyconvexity with Moments and Sums of Squares*,
arXiv:2604.11124v1](https://arxiv.org/html/2604.11124v1#S2.Thmdefinition5).
The exclusion allows a polynomial minor-support map of **any degree**.

More strongly, let
\(G(A)=F(A)+\sum_{|\eta|=4}h_\eta A^\eta\), in the ordinary, unweighted
35-monomial basis of four entries. If

\[
\max_{|\eta|=4}|h_\eta|\leq\frac1{616000},                 \tag{3}
\]

then \(G\) is also polyconvex and not SOS polyconvex under that definition.
Thus the gap contains an open neighborhood in the full 35-dimensional space
of homogeneous quartics, without an invariance assumption. For (3), the
constants in (2) may be replaced by \(1/800\) and \(1/2400\), respectively.

The theorem supplies the planar quartic case left open in the pinned source's
[Remark 2.1](https://arxiv.org/html/2604.11124v1#S2.Thmremark1), at the exact
definition just stated. Historical novelty beyond the checked sources and
external review remain UNKNOWN. This is a polyconvex example, not a
rank-one-convex/non-quasiconvex counterexample or a full classification of the
nine-coefficient cone.

## 1. The positive rational identity

Set

\[
\kappa(A)=\frac{14611}{2500}(u-v)+\frac{110757}{5000}q,
\qquad
P(A,X)=F(A+X)-F(A)-DF(A):X-\kappa(A)\det X.              \tag{4}
\]

In eight variables \((A_0,A_1,A_2,A_3,X_0,X_1,X_2,X_3)\), let \(Z\) list
the following 60 monomials in the indicated order:

1. \(A_iX_jX_k\), with \(i=0,1,2,3\) and lexicographic \(0\leq j\leq k<4\)
   (40 entries).
2. \(X_iX_jX_k\), with lexicographic \(0\leq i\leq j\leq k<4\)
   (20 entries).

The rational 60 by 60 matrix \(R\) in
`EXACT_MULTIPLIER_SUPPORT.json` satisfies

\[
|X|^2P(A,X)=Z(A,X)^T RZ(A,X),\qquad R-\frac1{200}I\succ0. \tag{5}
\]

The certificate SHA256 is
`a7b53759b9ba5576a099ef36b9ffce96c266478a5fbc5594a8b156d5f1576e32`.
`verify_sector.py` reconstructs (1), its derivatives, (4), and the Gram
polynomial directly using only Python's standard library and exact fractions.
It checks equality of every coefficient, then computes an exact LDL
factorization and reconstructs every matrix entry of \(R-I/200\).
All 60 pivots are positive. The largest pivot numerator or denominator is
718 bits. Numerical eigenvalues, tolerances, symbolic generator imports, and
optimizer statuses play no role in this verification.

For \(t_i=X_i^2\geq0\), the sums of the squares of the two feature blocks obey

\[
\begin{split}
\sum_{i,j\leq k}(A_iX_jX_k)^2
 &=|A|^2\sum_{j\leq k}t_jt_k
 \geq\frac12|A|^2|X|^4,\\
\sum_{i\leq j\leq k}(X_iX_jX_k)^2
 &=\sum_{i\leq j\leq k}t_it_jt_k
 \geq\frac16|X|^6.
\end{split}                                                    \tag{6}
\]

The first inequality follows by expanding \((\sum t_i)^2\); the second follows
because every multinomial coefficient of \((\sum t_i)^3\) is at most six.
Divide (5) by \(|X|^2\) when \(X\ne0\). At \(X=0\), both sides below vanish.
Consequently

\[
P(A,X)\geq\frac1{400}|A|^2|X|^2+\frac1{1200}|X|^4.       \tag{7}
\]

The norm multiplier is essential to the method: (5) proves nonnegativity of
\(P\); it does not assert that \(P\) itself is SOS.

## 2. A finite convex lift and the compatible-gradient implication

Let \(m(B)=(B,\det B)\). The two-dimensional determinant identity is

\[
\det B=\det A+\operatorname{cof}A:(B-A)+\det(B-A).
\]

For an independent scalar \(z\), define the affine function of \((B,z)\)

\[
\ell_A(B,z)=F(A)+[DF(A)-\kappa(A)\operatorname{cof}A]:(B-A)
                          +\kappa(A)(z-\det A).          \tag{8}
\]

At \(z=\det B\), inequality (7) implies \(\ell_A(B,z)\leq F(B)\), with
equality for \(A=B\). Therefore the convex function

\[
g(B,z)=\sup_{A\in\mathbb R^{2\times2}}\ell_A(B,z)          \tag{9}
\]

satisfies \(g(B,\det B)=F(B)\). This lift is finite everywhere. Indeed, Euler's
identity and \(\operatorname{cof}A:A=2\det A\) give

\[
\ell_A(B,z)=[DF(A)-\kappa(A)\operatorname{cof}A]:B
                 +\kappa(A)z-3F(A)+\kappa(A)\det A.
\]

Put \(X=-A\) in (7). Since \(F(0)=0\), it yields
\(3F(A)-\kappa(A)\det A\geq|A|^4/300\).
For fixed \((B,z)\), the remaining terms have degree at most three in \(A\),
so the negative quartic term makes the supremum finite and attained. This
constructs a real-valued convex lift; it does not claim that the lift is a
polynomial or provide a new efficient evaluator for (9).

For \(X=D\varphi\), both \(\int D\varphi=0\) and
\(\int\det D\varphi=0\). The latter is the determinant null-Lagrangian
identity, first for smooth zero-boundary functions and then by density in
\(W^{1,4}_0\). Integrating (7) proves (2). The same argument applies to
periodic gradients. For rank-one increments \(X=tH\), \(\det X=0\), so (7)
also directly supplies a strict rank-one-convex support inequality.

## 3. Why all polynomial degrees reduce to 26 quadratic features

This step is needed because failure of one SDP degree is not a general
SOS-polyconvexity obstruction. It holds for any homogeneous quartic
\(H:\mathbb R^{2\times2}\to\mathbb R\), with no symmetry assumption.

Suppose a polynomial minor-support map \(Q(A)=(V(A),k(A))\) makes

\[
H(B)-H(A)-V(A):(B-A)-k(A)(\det B-\det A)                  \tag{10}
\]

an SOS jointly in \((A,B)\). At \(B=A\), (10) is zero and globally
nonnegative, so its derivative in \(B\) is zero. Hence

\[
V(A)=DH(A)-k(A)\operatorname{cof}A.
\]

The invertible linear substitution \(B=A+X\) preserves the SOS property,
and (10) becomes

\[
B_H(A,X)-k(A)\det X,\qquad
B_H(A,X)=H(A+X)-H(A)-DH(A):X.                            \tag{11}
\]

Write \(k=\sum_d k_d\) in homogeneous pieces. If its largest nonzero degree
is \(d>2\), substitute \((tA,tX)\) in (11) and let \(t\to+\infty\).
The leading term is \(-t^{d+2}k_d(A)\det X\). Choose \(A\) with
\(k_d(A)\ne0\) and \(X\) with the same determinant sign; (11) becomes
negative, a contradiction. Thus all pieces above degree two vanish. If a
lowest nonzero piece has degree \(d<2\), the same argument as \(t\downarrow0\)
gives a contradiction. Therefore \(k\) is homogeneous quadratic, or zero.
This argument uses only global nonnegativity; it does not assume a degree
bound on the original minor map.

Now (11) is a homogeneous quartic. In any SOS representation, the highest
degree homogeneous square terms cannot cancel each other; the same is true
of the lowest degree terms. Thus each summand can be taken homogeneous
quadratic. Because (11) vanishes identically at \(X=0\), every such quadratic
also vanishes there. Its only possible monomials are

\[
Z_2=(A_iX_j\ (0\leq i,j<4),\quad X_iX_j\ (0\leq i\leq j<4)), \tag{12}
\]

exactly 26 features. The unrestricted quadratic selector has the ten
monomials \(A_iA_j\), \(i\leq j\). Therefore (10) is possible at any degree
if and only if there are a PSD 26 by 26 Gram matrix and a quadratic selector
for the exact identity (11). No symmetry averaging is needed below.

## 4. The negative exact dual

The parent-owned `EXACT_SUPPORT_SEPARATOR.json`, SHA256
`768f5564a0e9ed66524d3d908626ec4f52f4a24634c4eb3daf50034314d32c19`,
defines a rational linear functional \(L\) on the 215 degree-four monomials
arising in (12). A byte-identical input snapshot is retained as
`external_inputs/PARENT_EXACT_SUPPORT_SEPARATOR.json`, so replay needs no
files outside this folder. Independently rebuilding these monomials in
`verify_sector.py` establishes

\[
\begin{split}
Y_{ij}:=L((Z_2)_i(Z_2)_j)&\quad\text{satisfies }Y\succ0,\\
L(A_iA_j\det X)&=0\quad(0\leq i\leq j<4),\\
L(B_F)&=-\frac{39}{125000}<0.                            \tag{13}
\end{split}
\]

Every entry of the 26 by 26 matrix is rebuilt from the functional. Exact
LDL and full reconstruction verify all 26 positive pivots. The check of all
ten annihilators is stronger than the two directions used to acquire the
dual; it is a direct exact calculation, not a symmetry inference.

For any PSD Gram matrix \(S\), \(L(Z_2^TSZ_2)=\operatorname{tr}(SY)\geq0\).
But every quadratic \(k\) has \(L(k(A)\det X)=0\), so (13) makes (11)
strictly negative under \(L\). This contradicts every possible SOS
representation in (12). Section 3 excludes all remaining polynomial
degrees. This proves the stated failure of SOS polyconvexity.

## 5. Explicit full-dimensional stability

Let \(h=\sum_{|\eta|=4}h_\eta A^\eta\), with 35 coefficients bounded by
\(\varepsilon\). For a single unit-coefficient quartic monomial, the
expansion of its Bregman difference has total coefficient absolute value
\(2^4-1-4=11\). Multiplication by \(|X|^2\) gives total absolute value 44.
Consequently

\[
\big\||X|^2B_h\big\|_{\mathrm{coefficient},1}\leq1540\varepsilon. \tag{14}
\]

Products of the 60 features in Section 1 span every monomial of types
\(A^2X^4\), \(AX^5\), and \(X^6\): respectively
\(10\cdot35=350\), \(4\cdot56=224\), and 84 monomials. There are 658 in
total. To lift a target monomial, choose one feature product giving it; put
its coefficient on the corresponding diagonal Gram entry, or half its
coefficient in each of the symmetric off-diagonal entries. Different
monomials use different entries. This constructs a symmetric \(\Delta R\)
with \(Z^T\Delta RZ=|X|^2B_h\) and

\[
\|\Delta R\|_{\rm op}\leq\sum_{ij}|\Delta R_{ij}|
\leq1540\varepsilon.                                   \tag{15}
\]

At \(\varepsilon=1/616000\), (15) is at most \(1/400\). Thus
\(R+\Delta R\succ I/400\), giving global PC support for \(G=F+h\) with the
**same** quadratic selector (4), and the asserted halved constants in (2).
The finite-lift argument in Section 2 still applies.

The dual coefficient sensitivity is checked exactly over all 35 monomials:

\[
S:=\sum_{|\eta|=4}|L(B_{A^\eta})|=\frac{69749}{25000}.
\]

Hence \(L(B_G)\leq-39/125000+S\varepsilon<0\) whenever
\(\varepsilon<39/697490\). In particular the closed radius (3) satisfies
this condition. All ten annihilators remain zero, independently of \(G\).
Section 3 therefore excludes polynomial SOS polyconvexity for every
quartic in (3). This proves the full-dimensional claim.

## 6. Retained direct-PC alternative and failed assumptions

Before acquiring (5), the direct question was whether the SOS-support
threshold near 11.43955 reflected actual failure of polyconvexity below it.
No such inference is valid. For a positive homogeneous quartic \(H\),
quartic polarization gives a useful exact reduction:

\[
B_H(A,sR)=s^2\left[\tfrac12D^2H(R)[A,A]
                         +s\,DH(R):A+s^2H(R)\right].
\]

Minimizing the bracket over real \(s\) defines

\[
T_H(R)=\tfrac12D^2H(R)-\frac{DH(R)DH(R)^T}{4H(R)}.
\]

A global support scalar at a fixed \(A\) exists exactly when
\(A^TT_H(R)A-k(A)\det R\geq0\) for all nonzero \(R\). Equivalently, zero-determinant
directions must be nonnegative and all positive/negative determinant pairs
must have ordered scalar bounds. Requiring this for every \(A\) is the
matrix pair condition

\[
\frac{T_H(R_+)}{\det R_+}-\frac{T_H(R_-)}{\det R_-}\succeq0
\quad\text{for all }\det R_+>0,\ \det R_-<0,              \tag{16}
\]

together with \(T_H(R)\succeq0\) on \(\det R=0\). The endpoints of each
support interval are finite: any one fixed positive and one fixed negative
determinant direction bound all the other endpoints via pair ordering.
This is a direct support reduction, not an SOS representation restriction.

For (1), positivity follows independently from
\(F=(u-v+2q)^2+5w^2+(93/10)q^2\). Vanishing forces \(w=q=u-v=0\), hence
\(u=v=0\) using \(uv=w^2+q^2\). A negative exact eigenpair in (16) would
have been a genuine non-PC obstruction. The retained random/local searches
found no candidate. That failure was inconclusive. The constructive
multiplied certificate (5) settles this input positively; the numerical
searches are not part of its proof.

## 7. Prior, operations, costs, and remaining destination

The prior tools are ordinary minor-affine support, SOS multipliers, SDP,
rational projection, and exact LDL. The construction does not introduce a
new positivity hierarchy. The primary 2026 source's Definition 2.5 and its
unbounded-degree caveat determine the negative obligation. Its Theorem 2.3
and Remark 2.1 locate the exceptional planar quartic case. Earlier
[Bandeira–Pedregal (2009)](https://doi.org/10.1016/j.anihpc.2008.08.002)
already supply families of rank-one-convex quartics and generalized
eigenvalue constructions; no such construction is rebranded here.
[Gutiérrez (2006)](https://www.heldermann-verlag.de/jca/jca13/jca0514_b.pdf)
does not close the present homogeneous case via its nonzero-cubic-part
criterion. The norm-multiplier strategy belongs to established SOS/rational
positivity machinery, including the denominator literature represented by
[Reznick (1995)](https://doi.org/10.1007/BF02572604); no general sufficiency
of this one multiplier is asserted.

Numerical acquisition used a 60 by 60 PSD matrix, 658 affine coefficient
equations, and two selector coefficients. The saved ordinary Clarabel solve
took 1.194 seconds at one BLAS thread; exact rational reconstruction took
0.601 seconds, and final independent standard-library verification took 0.588
seconds on the current shared host. These are saved run timings, not
end-to-end research-effort or universal complexity claims. The final
positive certificate is approximately 75 KiB. The parent's separate dual
uses a 26 by 26 moment matrix, 215 monomials, and exact rational replay.

The ordinary same-input comparator is the complete unmultiplied SOS-support
test, not an artificially constrained selector. It provably fails here,
even when allowed every polynomial degree. A single norm multiplier proves
PC. This is a strict separation in certificate power; practical speed
advantage over every other polyconvexity method is not claimed.

The earlier acoustic certificate, random support samples, and local
opposite-determinant search remain saved with their original statuses.
Their existence or numerical signs do not establish novelty or the theorem.
The exact global identity, dual, and all-degree reduction establish the theorem.

The broader nine-coefficient rank-one-convex/quasiconvex cone remains
unclassified. This result specifically shows why the unmultiplied
SOS-support boundary cannot be treated as the PC boundary, and supplies a
concrete richer support operation that certifies a neighborhood outside
that boundary. It does not resolve Morrey's conjecture, claim a non-PC
rank-one-convex quartic, or extrapolate the multiplier's success to the
entire unresolved cone.
