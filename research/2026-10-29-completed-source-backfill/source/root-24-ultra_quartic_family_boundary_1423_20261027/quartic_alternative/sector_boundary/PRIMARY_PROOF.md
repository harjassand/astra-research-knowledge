# Sharp ROC, PC, and QC threshold on an oriented planar quartic line

This branch follows the frozen `../sector_gap/` theorem without changing
its certificates or strict margin. The exact boundary support, a
standard-library replay, and the parent's independently implemented
quadratic-field replay and complete proof review have passed. Analytic
quantifiers and the parameter classification are proved below; numerical
optimizer statuses are not premises.

## The theorem

For \(A=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\), put

\[
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc,
\qquad F_\tau(A)=u^2+v^2+3w^2+\tau q^2+4q(u-v).
\]

Write ROC for rank-one convexity, PC for polyconvexity in the five minors,
and QC for Morrey quasiconvexity. For **every real** \(\tau\),

\[
\boxed{F_\tau\text{ is ROC}\ \Longleftrightarrow\
F_\tau\text{ is PC}\ \Longleftrightarrow\
F_\tau\text{ is QC}\ \Longleftrightarrow\
\tau\geq\tau_c:=89-12\sqrt{42}.}                         \tag{1}
\]

In the nine-coefficient basis
\((u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)\), the classified line is
\((1,1,\tau,3-\tau,0,0,4,-4,0)\), using \(uv=w^2+q^2\).
The edge is approximately 11.231111619105677; this decimal is not used in
the proof. The theorem includes the degenerate edge. It classifies this
fixed \(r=3/2,L=4\) line, not the full nine-coefficient cone.

## 1. The exact boundary support

Work in \(K=\mathbb Q(\sqrt{42})\) with its positive real embedding. Set

\[
\alpha=\frac{59629}{10000},\qquad
\delta=\frac{3418887}{20000}-\frac{689629}{30000}\sqrt{42},\qquad
\kappa(A)=\alpha(u-v)+\delta q,
\]

and define

\[
P_c(A,X)=F_{\tau_c}(A+X)-F_{\tau_c}(A)-DF_{\tau_c}(A):X
                                             -\kappa(A)\det X.         \tag{2}
\]

Here \(DF(A):X\) is the derivative pairing in row-major entry order and
\(|X|\) is the Frobenius norm. We specify all features, so replay needs no
symbolic or numerical producer. Write

\[
A_0^\mathbb C=a+\mathrm i c,\quad A_1^\mathbb C=b+\mathrm i d,\qquad
Z_0=X_0+\mathrm i X_2,\quad Z_1=X_1+\mathrm i X_3.
\]

For each three-factor expression below, multiply it by
\(\mathrm i^{i+j+k}\). Indices are 0 or 1, and a barred factor's index is
counted in the same way as an unbarred factor's. The spin-one list \(W_1\)
has the following order:

1. \(A_i^\mathbb C Z_j\overline Z_k\), all \(i,j,k\) (8 terms).
2. \(\overline{A_i^\mathbb C}Z_jZ_k\), \(i=0,1\), \(j\leq k\) (6 terms).
3. \(Z_iZ_j\overline Z_k\), \(i\leq j\), \(k=0,1\) (6 terms).

The spin-three list \(W_3\) has the order:

1. \(A_i^\mathbb C Z_jZ_k\), \(i=0,1\), \(j\leq k\) (6 terms).
2. \(Z_iZ_jZ_k\), \(i\leq j\leq k\) (4 terms).

Within each line, use lexicographic index order. The names describe the
lists' rotation weights; their explicit expressions suffice for the proof.
Let \(V_1\in K^{20\times16}\), \(V_3\in K^{10\times6}\) be the stored
`basis_matrices` in `EXACT_BOUNDARY_SUPPORT.json`, and put
\(\chi_j=V_j^TW_j\). The stored real symmetric matrices
\(S_1\in K^{16\times16}\), \(S_3\in K^{6\times6}\) satisfy

\[
\begin{split}
|X|^2P_c(A,X)
 &=\sum_{j\in\{1,3\}}\Big[
 (\operatorname{Re}\chi_j)^TS_j\operatorname{Re}\chi_j
 +(\operatorname{Im}\chi_j)^TS_j\operatorname{Im}\chi_j\Big],\\
S_1-I/200&\succ0,\qquad S_3-I/200\succ0.                 \tag{3}
\end{split}
\]

Certificate SHA256:
`66901f304531cbc969ccc7f89e5a7e57091e57cefba21133355b0d2cb54be554`.
Each entry is stored as two rational strings \((r,s)\), meaning
\(r+s\sqrt{42}\). Producer projection verifies its 334 nontrivial affine
rows exactly over \(K\); the exact affine rank is 65.

The independent `verify_boundary.py` instead constructs (2) from the literal
energy and rebuilds the complete polynomial in (3), including zero
coefficients outside the producer's row list. It imports only the Python
standard library; no producer, face map, symbolic algebra, numerical array,
solver, or previous checker is imported. For both shifted matrices it
computes and reconstructs complete exact LDL factorizations. All 22 pivots
are positive; the largest pivot component numerator or denominator has
1098 bits. Field signs are decided by rational comparisons, including
comparison of \(r^2\) with \(42s^2\) when the components have opposite
signs. Floating-point square roots and eigenvalues are not used.

Divide (3) by \(|X|^2\) for \(X\ne0\); at \(X=0\), (2) is explicitly zero.
It follows that \(P_c\geq0\) globally. A singular acoustic edge is therefore
consistent with a positive definite Gram after removing its forced kernels.
This is a minor-affine support, not a claim that \(P_c\) is unmultiplied SOS.

## 2. Finite convex lift and all larger parameters

For each \(A\), define an affine function of the independent variables
\((B,t)\in\mathbb R^{2\times2}\times\mathbb R\):

\[
\ell_A(B,t)=F_{\tau_c}(A)+
 [DF_{\tau_c}(A)-\kappa(A)\operatorname{cof}A]:(B-A)
 +\kappa(A)(t-\det A).
\]

The determinant expansion and (2) imply
\(\ell_A(B,\det B)\leq F_{\tau_c}(B)\), with equality when \(A=B\).
Consequently \(g(B,t)=\sup_A\ell_A(B,t)\) is convex and equals \(F_{\tau_c}\)
on the graph of the minors. It is finite everywhere. Choose a real matrix
\(Y\) with \(\det Y=t-\det B\). The point \((B,t)\) is the average of
\((B+Y,\det(B+Y))\) and \((B-Y,\det(B-Y))\). Affinity bounds every
\(\ell_A(B,t)\) above by
\([F_{\tau_c}(B+Y)+F_{\tau_c}(B-Y)]/2\), and any one \(\ell_A\) supplies a
finite lower bound. This proves PC in the usual finite-valued sense.

For \(\varepsilon=\tau-\tau_c\geq0\), set
\(\kappa_\tau(A)=\kappa(A)+2\varepsilon q(A)\). The corresponding support
remainder is exactly

\[
P_\tau(A,X)=P_c(A,X)+\varepsilon\,[q(A+X)-q(A)]^2\geq0.  \tag{4}
\]

To verify (4), expand \(q(A+X)=q(A)+\operatorname{cof}A:X+q(X)\).
After the derivative term and \(2q(A)q(X)\) are removed from the Bregman
difference of \(q^2\), precisely the displayed square remains. Thus every
larger parameter has a global support and a finite convex lift. Its norm-
multiplied certificate adds four nonnegative weighted squares
\(\varepsilon X_i^2[q(A+X)-q(A)]^2\) to (3). No further SDP is needed.

Integrating \(P_\tau(A,D\varphi)\geq0\) cancels the gradient mean and
determinant mean. For every bounded Lipschitz planar domain and
\(\varphi\in W^{1,4}_0(\Omega;\mathbb R^2)\), this gives

\[
\int_\Omega F_\tau(A+D\varphi)\,dx\geq|\Omega|F_\tau(A). \tag{5}
\]

The determinant identity holds first for smooth potentials and passes by
strong \(W^{1,4}\) approximation. In particular this includes the usual
\(W^{1,\infty}_0\) QC tests and periodic gradients. Rank-one increments
have zero determinant, so the same global support also directly implies
ROC. We do not transfer the strict constants from `../sector_gap/` to this
degenerate boundary.

## 3. One exact critical pair excludes every lower parameter

This shorter necessity argument was proposed independently by the parent.
It avoids making a separate all-parameter acoustic sufficiency test a
premise of (1). Define

\[
m_c=-\frac{39}{58}+\frac{15}{29}\sqrt{42}>\frac52,
\qquad z>\sqrt2,\qquad z^4-m_cz^2+1=0.                 \tag{6}
\]

Such a real \(z\) exists uniquely: \(y=z^2>1\) satisfies
\(y+y^{-1}=m_c\), and \(m_c>5/2\) makes its larger root exceed 2.
Let \(H=e_1\otimes(1,z)\), which has rank one. The four components of the
background \(A_0(z)\), in row-major order, are the degree-at-most-three
polynomials stored in `CRITICAL_PAIR.json` as
`A_polynomial_coefficients`. The coefficient convention is increasing
powers of \(z\), with the same rational-pair field representation as (3).
Its SHA256 is
`c57502de52215737c319374669a32b8e31983fbd7bc89c0fe6b8315aa0b36aa3`.

For transparency the matrix defining the critical pair is explicit:

\[
Q_\tau(z)=
\begin{pmatrix}12&0&0&12\\0&6&-4&0\\0&-4&4&0\\12&0&0&2\tau\end{pmatrix}
+2z\begin{pmatrix}0&6&-4&0\\6&0&0&-4\\-4&0&0&3-\tau\\0&-4&3-\tau&0\end{pmatrix}
+z^2\begin{pmatrix}6&0&0&-4\\0&12&12&0\\0&12&2\tau&0\\-4&0&0&4\end{pmatrix}.
\]

Literal differentiation gives
\(D^2F_\tau(A)[H,H]=\operatorname{vec}(A)^TQ_\tau(z)\operatorname{vec}(A)\).
The stored pair satisfies the exact polynomial identities

\[
Q_{\tau_c}(z)\operatorname{vec}(A_0(z))=0
       \pmod {z^4-m_cz^2+1},                            \tag{7}
\]

and, writing \(A_0=\left(\begin{smallmatrix}a_0&b_0\\c_0&d_0\end{smallmatrix}\right)\),

\[
\begin{split}
\operatorname{cof}A_0:H=d_0-zc_0&=g_0+g_2z^2,\\
g_0&=\frac{-38880+12240\sqrt{42}}{29},\\
g_2&=\frac{-6464880+863640\sqrt{42}}{841}.               \tag{8}
\end{split}
\]

Exact field sign checks give \(g_2<0\) and \(g_0+2g_2<0\). Since \(z^2>2\),
(8) is strictly negative, so in particular \(A_0\ne0\). Equation (7) gives
zero acoustic curvature at \(\tau_c\). Along a rank-one line the determinant
is affine; hence \(D^2(q^2)(A_0)[H,H]=2(\operatorname{cof}A_0:H)^2\).
For **every** \(\tau<\tau_c\), the same exact pair therefore satisfies

\[
D^2F_\tau(A_0)[H,H]
=2(\tau-\tau_c)(g_0+g_2z^2)^2<0.                       \tag{9}
\]

This violates ROC. QC and PC imply ROC, so both are excluded too. Together
with Section 2, this completes (1). The critical pair, its nonzero factor,
and the rank-one update are checked using exact field polynomial arithmetic.
No limiting numerical eigenvector is a premise.

## 4. Construction, ordinary alternatives, and costs

At the acoustic edge, exact null directions force a quadratic selector to
satisfy
\(\delta=162-21\sqrt{42}-\alpha(-3/2+\sqrt{42}/3)\).
This is derived in `critical_selector.py`. The ordinary 60-feature norm
multiplier search approached a singular Gram at the edge and did not
certify positivity. A 115-feature higher-multiplier search at 11.232 was
positive but cost 30.20 seconds; numerical positivity there did not settle
the boundary.

The surviving operation uses exact symmetry and the known acoustic orbit
to remove forced Gram kernels. Rotation weights one and three give complex
blocks of sizes 20 and 10. Rephasing by the second-column count makes the
combined reflection act by conjugation, so averaging permits real blocks.
The exact orbit kernel removes four directions from each block. The
resulting PSD blocks have sizes 16 and 6. Direct identity (3), not this
search derivation or a completeness claim for it, establishes the theorem.

The final ordinary SDP has 158 variables and 334 affine rows of exact rank
65. A redundant-row Clarabel failure is retained in `SOLVER_FAILURES.json`;
it was not interpreted as infeasibility. After removing the redundant
numerical row space, the solve reached a robust face margin near 0.00917
in 2.86 seconds including face-map loading. Exact quadratic-field projection
and full producer LDL took 24.74 seconds at one BLAS thread. The saved
standard-library replay took 0.4533 seconds including the critical pair;
the parent's separate field-engine replay took 3.066 seconds. Bit costs and
matrix storage are charged, including the 1098-bit pivot components.

The materially different direct-PC alternative used
\(T(R)=D^2F(R)/2-DF(R)DF(R)^T/(4F(R))\) and a forced support at an acoustic
singular background. Three bounded numerical global searches found only
the known rank-one zero. Their lack of a negative witness is not a PC
proof. No failed SDP, random sample, or numerical non-witness is used in
(1). Those failures and exact supporting algebra remain saved.

For rational input \(\tau\), `classify_tau.py` compares it with the exact
edge, then supplies either (4) or the common negative-curvature witness
(9). All matrix dimensions are fixed for this line. Input bit lengths
affect the exact integer arithmetic; no unit-cost algebraic oracle or
efficient arbitrary-quartic classification is assumed.

The methods are established SOS multipliers, exact SDP reconstruction,
symmetry/facial reduction, and polynomial minor-affine support. The new
supplied mathematical content is the exact support at this anisotropic
edge and the resulting whole-line classification. General hierarchy
completeness, superiority over every PC method, and historical priority
beyond bounded primary-source checks remain UNKNOWN.

Known wider counterexamples are preserved. In particular,
[Bruno–Pasqualotto, arXiv:2608.06367v1, Introduction and Theorem 1](https://arxiv.org/html/2608.06367v1#S1)
record a larger ROC/QC range than PC for the trace-coupled
Dacorogna–Marcellini family \(|A|^4-2\gamma|A|^2\det A\).
Its right-rotation invariance differs from the present trace-free coupling.
Thus (1) cannot be extrapolated to all invariant quartics or all nine
coefficients. No full Morrey theorem, physical device, or civilisation-level
capability is established.
