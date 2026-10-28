# A strict ROC obstruction to norm-level-one PC plus closed heat

This is a completed certificate-class no-go, not a non-quasiconvex energy.
The preceding gap and boundary theorem packages remain frozen unchanged.

## The target and theorem

For \(A=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\), set
\(u=a^2+c^2\), \(v=b^2+d^2\), \(w=ab+cd\), \(q=ad-bc\). In the basis
\(\mathcal B=(u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)\), define \(F_p=p\cdot\mathcal B\)
with the exact rational coefficients

\[
10^{10}p=(55220381,55220381,1830880464,-1603523974,
                         0,0,297124543,-297124542,0).       \tag{1}
\]

**Theorem.** \(F_p\) is globally strictly rank-one convex in the acoustic
sense below, but cannot be decomposed as

\[
F_p=G+H,\qquad G\in\mathcal P_1,\quad H\in\mathcal H_I.  \tag{2}
\]

Here \(\mathcal P_1\) is the polynomial minor-support class with the fixed
\(|X|^2\) norm multiplier, and \(\mathcal H_I\) is the identity spatial
Laplacian/closed quadratic two-form/bilinear-SOS heat class. The definitions
below are unrestricted within these precise classes. Nonnegative \(q^2\)
removal is included. The theorem holds throughout the full nine-coefficient
closed box

\[
\|\widetilde p-p\|_\infty\leq1/52800000.                 \tag{3}
\]

Consequently this sum of sufficient QC cones does not contain the full
nine-coefficient ROC cone. True PC, higher norm powers, other flows, and
QC itself are not excluded.

## 1. Precise sufficient classes

Both component energies in these cones are homogeneous quartics.
For a homogeneous quartic \(G\), write
\(B_G(A,X)=G(A+X)-G(A)-DG(A):X\). The class \(\mathcal P_1\) requires a
polynomial \(k(A)\) for which

\[
|X|^2[B_G(A,X)-k(A)\det X]\text{ is SOS jointly in }(A,X). \tag{4}
\]

No selector symmetry or initial degree bound is assumed. Global
nonnegativity after division off \(X=0\), followed by scaling
\((A,X)\mapsto(tA,tX)\), forces \(k\) to be homogeneous quadratic or zero.
A highest component above degree two dominates negatively for an
appropriate determinant sign as \(t\to\infty\); a lowest component below
two does the same as \(t\downarrow0\).

The SOS polynomial is homogeneous of degree six and has minimum degree
four in \(X\). Squares can be taken homogeneous cubic. Their \(A^3\) and
\(A^2X\) terms must vanish, because the lowest \(X\)-degree square terms
cannot cancel. Thus the complete feature space is exactly

\[
Z_{60}=(A_iX_jX_k:\ i=0,\ldots,3,\ j\leq k;\quad
                         X_iX_jX_k:\ i\leq j\leq k).      \tag{5}
\]

It has 40 and 20 entries; \(k\) has all ten \(A_iA_j\), \(i\leq j\).
This includes every polynomial selector degree for the fixed multiplier,
not a guessed selector subspace. Division in (4) supplies a global
minor-affine support; integrating cancels gradient and determinant means,
so \(\mathcal P_1\) is a sufficient QC class. It is not all of PC.

For heat, use the compatible second jet
\(z=(u_{xx},u_{xy},u_{yy},v_{xx},v_{xy},v_{yy})\), and
\(J_1=(z_0,z_1,z_3,z_4)\), \(J_2=(z_1,z_2,z_4,z_5)\). Here \(u,v\) label
potential components, not the quadratic invariants. Define

\[
E_H(A,z)=D^2H(A)[J_1,J_1]+D^2H(A)[J_2,J_2].
\]

The class \(\mathcal H_I\) allows every closed two-form \(\omega\) on
matrix space with homogeneous quadratic coefficients, and requires

\[
E_H(A,z)+\omega_A(J_1,J_2)=(A_i z_j)_{24}^{T}R(A_i z_j)_{24},\quad R\succeq0. \tag{6}
\]

There are 60 coefficient slots, 16 closedness equations of rank 15, and
45 closed directions. All are allowed. A closed quadratic form is exact
with primitive \(\iota_A\omega/4\). Its gradient pullback has zero integral
on affine backgrounds with Schwartz perturbations. Integrating (6)
makes relative quartic energy nonincreasing under componentwise heat flow;
heat decay sends it to zero. Strong \(W^{1,4}\) approximation proves QC on
bounded Lipschitz domains. These are the established heat/null-Lagrangian
arguments; see also the primary
[Bruno–Pasqualotto proof, Lemma 3 and Section 3](https://arxiv.org/html/2608.06367v1#S2).

The class is specifically identity spatial diffusion, closed quadratic
corrections, and bilinear SOS. It does not encompass all nonnegative
corrected densities, arbitrary spatial SPD matrices, or output-coupled
flows. No such enlargement is inferred from the target's approximate
symmetries.

For an invariant target, restricting component energies in (2) to the
nine-basis loses no decomposition in these classes. Average over left
\(SO(2)\): both cones are convex and stable under output rotations; the
norm, closedness, compatible jets, and identity Laplacian are preserved.
The averaged quartics have the nine-invariant representation. This uses
no right/spatial averaging of an unknown diffusion operator.

Finally \(q^2\in\mathcal P_1\). With selector \(2q(A)\), its unweighted
remainder is \([q(A+X)-q(A)]^2\). Thus allowing a nonnegative \(q^2\)
subtraction from the heat component is already included in the sum.

## 2. Exact strict rank-one convexity

`heat_normal_extreme_ROC.json` contains a rational symmetric 8 by 8 matrix
\(Q\) satisfying

\[
D^2F_p(A)[e_1\otimes(s,t),e_1\otimes(s,t)]
 =(s\mathbf a,t\mathbf a)^TQ(s\mathbf a,t\mathbf a),\quad Q-I/200000\succ0, \tag{7}
\]

where \(\mathbf a=(a,b,c,d)^T\). Certificate SHA256:
`9ab66589e89d79379216348ab26de1faba54dd4af96b3f9d62f8564cce7f9413`.
The checker derives (7) from the literal polynomial, checks every
coefficient, and reconstructs all eight exact shifted LDL pivots. Left
\(SO(2)\) invariance reduces every rank-one increment to (7), giving

\[
D^2F_p(A)[\xi\otimes\eta,\xi\otimes\eta]
 \geq |A|^2|\xi|^2|\eta|^2/200000.                       \tag{8}
\]

The quartic Hessian is necessarily zero at the zero background. Equation
(8) states the quantitative strictness used here. It was acquired and
literally verified before any candidate PC/QC inference.

## 3. Exact common separator

`EXACT_COMMON_SEPARATOR.json`, SHA256
`2e812506ed588ec86ea9736a831df69f5eecd8c5d282f226e73e31656360e7b9`,
defines rational functionals \(L_P\) on all 658 Gram monomials from (5)
and \(L_H\) on the 210 monomials \(A_iA_jz_kz_l\), \(i\leq j,k\leq l\).
Their exact facts are

\[
\begin{split}
[L_P((Z_{60})_i(Z_{60})_j)]&\succ0,\\
[L_H((A_i z_j)(A_k z_l))]_{24\times24}&\succ0,\\
L_P(|X|^2 A_iA_j\det X)&=0\quad(i\leq j).               \tag{9}
\end{split}
\]

There are 60 and 24 positive exact pivots, with full matrix
reconstructions. A stored rational vector \(\eta\in\mathbb Q^{16}\) also
obeys, on each of all 60 coefficient basis forms,

\[
L_H(\omega_A(J_1,J_2))=\eta\cdot\operatorname{coeff}(d\omega). \tag{10}
\]

The exterior derivative and compatible pullback are rebuilt literally.
Thus every closed quadratic form is annihilated without trusting an
imported numerical nullspace.

The two functionals agree on every energy basis element:
\(L_P(|X|^2B_{\mathcal B_i})=L_H(E_{\mathcal B_i})=g_i\), where

\[
605000000000g=(717712168314,717681999384,-51187582194,-62459780213,
                         0,0,-144318445546,144307332180,0). \tag{11}
\]

For (1), the exact pairing is

\[
g\cdot p=-28689295580537827/3025000000000000000000<0.       \tag{12}
\]

Every \(G\in\mathcal P_1\) has nonnegative pairing, by (4), the PC moment
matrix, and selector annihilation. Every \(H\in\mathcal H_I\) has
nonnegative pairing, by (6), the heat moment matrix, and (10). Therefore
(2) contradicts (12). This proves the class no-go. As a check, the minor
pairing is \(g_2-g_3=11272198019/605000000000>0\).

`verify_common.py` uses standard-library fractions and literal polynomial
dictionaries only. It imports no producer, interface array, optimizer,
symbolic compiler, nullspace, or prior checker. Schur elimination and a
full LDL reconstruction check positivity. It rechecks (7), every selector,
all 60 exterior-derivative columns, all nine shared pairings, and (12).
The largest pivot numerator/denominator has 1441 bits. The saved literal
replay took 1.515 seconds. The parent's separate SymPy QQ implementation
also passed, without author imports or saved interface arrays, in 2.51
seconds; its receipt is in `../../common_cone_review/`.

## 4. Full nine-dimensional stability

The checker rebuilds the canonical acoustic maps \(Q_i\) from literal
Hessians, keeping the acquired skew parameters fixed, and verifies
\(\sum_i\sum_{j,k}|(Q_i)_{jk}|=132\). A coefficient perturbation bounded by
\(\varepsilon\) changes the acoustic matrix by operator norm at most
\(132\varepsilon\). At (3), this is \(1/400000\), so strict ROC remains.
The common normal has
\(\|g\|_1=1837667307831/605000000000\). The radius (3) is smaller than
\(-g\cdot p/(2\|g\|_1)\), so its pairing remains negative too. This proves
an open set in the full nine-coefficient space outside the combined class.
No extra column or reflection symmetry is required for this conclusion.

## 5. Acquisition, alternatives, and limitations

The matched controls allowed every ten-coefficient PC selector, all 45
closed heat directions, full PSD Grams, and nonnegative minor removal.
The convex norm-four PC control and the known Dacorogna–Marcellini
heat/non-PC control behaved as expected. Nine bounded dual-directed
strict-ROC acquisitions were already handled by heat, so no full-cone
claim was drawn. Pointwise-non-PC/old-heat-normal targets failed already
in the acoustic lift, identifying unsuitable normal pairs rather than a
defect of the combined QC operation.

The successful input minimized the existing exact heat normal over an
independently constrained strict acoustic lift. Numerical pure PC1, heat,
and combined failures suggested a common dual; only (9)–(12) prove it.
The 64 rational constraints have rank 64. Adding a small explicit Gaussian
common-dual interior point made moment matrices strictly positive before
exact reconstruction. Denominator \(10^{10}\) passed on the first attempt
in 1.273 seconds; its exact Gaussian weight was \(1/20000\).

For that anchor, independent standard Gaussian \(A,X\) give PC energy
pairing \(20\mathbb EF(G)\) and moment trace 172. The compatible rank-one
heat jet \(z=\xi\otimes(\eta_0^2,\eta_0\eta_1,\eta_1^2)\), with independent
standard Gaussian output/spatial vectors, has parallel \(J_1,J_2\), so
every form pullback vanishes pointwise. Its energy pairing is
\(16\mathbb EF(G)\). Multiplication by \(5/4\) matches PC, with heat trace
70; dividing both functionals by 242 normalizes them. This construction is
an acquisition aid; final replay proves (9)–(12) without it.

A single pure level-two support attempt returned a negative numerical
margin in 27.23 seconds. This remains an inconclusive failure, not an
infeasibility or non-PC proof. No further multiplier escalation was made.
True-PC support geometry is owned independently by the complementary
peer; an already in-flight local probe is not used as evidence here.

The achieved operation is an exact missing-interface result for the fixed
multiplier and heat class. It does not exclude other norm powers,
nonpolynomial minor supports, different correction/flow classes, or QC.
Historical priority and the full nine-coefficient ROC/QC problem remain
unresolved. Numerical samples, failures, hashes, and replay timings are not
promoted into those broader conclusions.
