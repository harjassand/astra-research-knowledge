# Positive sharp cores: a non-heat calibration and its remaining boundary

Research date: 16 October 2026 (Australia/Brisbane).
Repository inspected: `harjassand/astra-research-knowledge`, commit
`3dde9ce74d829a93388e64032d27351b36dd2221`.

**Status.** This investigation does not prove all-background quasiconvexity of the positive sharp cores and does not produce a compatible negative Jensen map. It supplies a new exact, parameter-wide supporting identity, quasiconvexity on an explicit cone of affine backgrounds, quantitative coercivity at every singular background, and a precise surviving obstruction. All coefficients of the integrand remain unchanged. The standalone symbolic verifier passes 24 groups. Analytic arguments are supplied below; this is not external review, formal proof verification, or historical-priority clearance.

## 1. Definitions and scope

For real planar matrices write
\[
 A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\quad
 u_A=a^2+c^2,\quad v_A=b^2+d^2,\quad w_A=ab+cd,\quad j_A=ad-bc.
\]
Then \(u_Av_A=w_A^2+j_A^2\). Set
\[
 H(A)=(u_A+v_A-2j_A)^2,\quad
 \alpha=\frac{3r}{8(r+2)},\quad\beta=\frac{r(r-1)}6,
 \quad t=\frac{2r+1}{3},\qquad r>0,
\]
\[
 J_r=\alpha H+\beta u^2+j^2+ruj.
\]
The relation \(\beta=\alpha(t^2-1)\) is used repeatedly. Norms of matrices are Frobenius norms.

Quasiconvexity **at a background B** means
\[
 \int_\Omega [J_r(B+D\phi)-J_r(B)]\ge0                 \tag{1}
\]
for every bounded Lipschitz planar domain and every \(\phi\in W^{1,4}_0(\Omega;\mathbb R^2)\). The results also hold for periodic \(W^{1,4}\) perturbations. Proving (1) for some backgrounds does not make the integrand quasiconvex, which requires all backgrounds.

### Theorem 1: an explicit background cone, with no heat operation

Define
\[
 k_*(r)=\frac{4(r+2)}{3(\sqrt{r^2+8r+4}+r+2)}.
                                                        \tag{2}
\]
For a constant background B, let
\[
 L_{r,k}(B)=
 \begin{pmatrix}
 t^2u_B+(1-k)v_B+2t j_B&k w_B\\
 k w_B&(1-k)u_B+v_B-2j_B
 \end{pmatrix}.                                         \tag{3}
\]
For every r>0,
\[
 \boxed{L_{r,k_*}(B)\succeq0\quad\Longrightarrow\quad
 J_r\text{ satisfies (1) at B}.}                         \tag{4}
\]
The supporting inequality proved below is pointwise for **every** matrix A. Thus (4) allows arbitrary compatible perturbations, not merely small perturbations, finite waves, orientation-preserving maps, or rank-one-valued gradients.

All nonzero singular backgrounds are in the strict region \(L_{r,k_*}(B)\succ0\). The zero background also satisfies (1). Consequently (4) includes an open conical neighbourhood of the entire nonzero rank-one background cone.

This is a sufficient background criterion. Failure of (3) does not imply failure of quasiconvexity, or even failure of every possible supporting inequality.

### Theorem 2: the full singular-background stratum and coercivity

For each r>0 there is \(c_r>0\) such that for every singular B and every admissible perturbation,
\[
 \int_\Omega[J_r(B+D\phi)-J_r(B)]
 \ge c_r\left(|B|^2\int_\Omega|D\phi|^2+
                       \int_\Omega|D\phi|^4\right).      \tag{5}
\]
The constants can be uniform when r ranges over a compact subset of (0,infinity). They are independent of the domain and affine-background scale. No sharp general-r value is asserted.

For r=1 there are the explicit bounds
\[
 \boxed{\int[J_1(B+D\phi)-J_1(B)]\ge\frac1{32}\int|D\phi|^4,}
                                                        \tag{6}
\]
and separately
\[
 \boxed{\int[J_1(B+D\phi)-J_1(B)]
 \ge\frac1{44}\left(|B|^2\int|D\phi|^2+\int|D\phi|^4\right).}
                                                        \tag{7}
\]
These constants are not claimed optimal.

### Theorem 3: a concrete full-rank region for r=1

Here \(k_*=\sqrt{13}-3\). A sufficient condition is
\[
 \boxed{
 (1-k_*)(u_B+v_B)^2-2k_*(u_B-v_B)j_B
                    -(4-k_*^2)j_B^2\ge0.}              \tag{8}
\]
For B nonzero, the trace of (3) is positive, so this determinant condition is exactly (3).

In particular, with singular values \(\sigma_1\ge\sigma_2\ge0\), every background satisfying
\[
 \boxed{\frac{\sigma_2}{\sigma_1}\le
       1-\sqrt{\sqrt{13}-3}=0.221828248094\ldots}        \tag{9}
\]
satisfies (1), for either determinant sign and every column orientation.
The orientation-uniform threshold (9) is sharp for criterion (8), not asserted sharp for quasiconvexity. Criterion (8) also covers additional backgrounds outside (9).

At B=I, the lower-right entry of (3) is \(-k_*<0\) for every r>0. The decisive conformal-background problem survives.

## 2. Independent reconstruction of the incoming claims

The supplied sharp-frontier archive was extracted without modifying its mathematical input. Its `verify_frontier.py` was executed. All ten exact groups pass, including the universal negative-branch identity and its positive minors, the sharp acoustic Schur complement on both parameter components, contact equations, face LMIs, the cubic nonpolyconvexity residual, and the G subtraction arithmetic. The replay log and file hashes are preserved.

The new standalone verifier also reconstructs the positive-branch rank-one convexity directly from J_r. It does not import an inherited heat Gram. For direction \(e_1\otimes(1,z)\), change background coordinates by
\[
 (a,b,c,d)=\tfrac12(P+X,Y-Q,Y+Q,P-X).
\]
The conformal acoustic block is
\[
 A_c=\begin{pmatrix}
 (r+1)^2/2&-z(r+1)/2\\
 -z(r+1)/2&(3z^2+r(r+2))/6
 \end{pmatrix},
 \quad \det A_c=\frac{r(r+1)^2(r+2)}{12}>0.
\]
Put \(b_r=r(5r+4)/(24(r+1)^2)\), \(c_r'=\alpha/(r+1)^2\).
Its Schur complement at the unchanged sharp coefficient is
\[
 4\begin{pmatrix}
 (\alpha-c_r')z^2+3(\alpha-b_r)&(2\alpha-\alpha/(r+1))z\\
 (2\alpha-\alpha/(r+1))z&3\alpha z^2
 \end{pmatrix}.
\]
Its determinant is \(48\alpha(\alpha-c_r')z^4\), and its diagonal entries are nonnegative. Indeed \(\alpha>c_r'\) and
\[
 \alpha-b_r=\frac{r(2r+1)^2}{24(r+1)^2(r+2)}>0.
\]
This proves rank-one convexity for every r>0. The missing input direction follows by continuity. The full acoustic determinant is \(9r^4n^4m^4\). This independent ROC proof is essential if a later compatible negative Jensen field is found.

The negative theorem, general finite completion, and peer operation obstructions are not needed to prove Theorems 1-3 above. Only the corollary to the full shear-contact family below imports the existing negative theorem for its negative sector.

## 3. The new identity

For arbitrary A,B, put \(V=A-B\),
\[
 \Delta u=u_A-u_B,\quad\Delta v=v_A-v_B,\quad
 \Delta w=w_A-w_B,\quad\Delta j=j_A-j_B,
 \quad z=(\Delta u,\Delta v,\Delta j)^T.
\]
For any real k define
\[
 M_{r,k}=\begin{pmatrix}
 t^2&1-k&2t\\
 1-k&1&-2\\
 2t&-2&4+2k+1/\alpha
 \end{pmatrix},                                        \tag{10}
\]
\[
 \lambda_{r,k}(B)=
 (2+8\alpha+4\alpha k)j_B+(r-4\alpha)u_B-4\alpha v_B.
                                                        \tag{11}
\]
Then the universal identity is
\[
\begin{split}
 R_{r,k}(A,B):={}&J_r(A)-J_r(B)-DJ_r(B):V
                          -\lambda_{r,k}(B)\det V\\
 ={}&\alpha z^TM_{r,k}z+2\alpha k(\Delta w)^2
       +2\alpha\sum_{i=1}^2 V_{i,:}L_{r,k}(B)V_{i,:}^T.
\end{split}                                             \tag{12}
\]
No compatibility or rank assumption is required for this polynomial identity. Both A and B are arbitrary matrices.

### Derivation from a quadratic constraint on Gram differences

Write \(g=A^TA\), \(g_B=B^TB\), and \(\mathcal C X=(X_{11}-X_{22},X_{12}+X_{21})\). The exact identity
\[
 \boxed{\det(g-g_B)-(j_A-j_B)^2
                  =-|\mathcal C(V\operatorname{adj}B)|^2}            \tag{13}
\]
holds for all A,B, including singular B. To verify it, use
\[
 \det(g-g_B)=j_A^2+j_B^2-|A\operatorname{adj}B|^2,
\]
and \(B\operatorname{adj}B=j_BI\). The conformal defect of this last matrix is zero. Also \(|X|^2-2\det X=|\mathcal CX|^2\).

Expand J as a quadratic in u,v,j:
\[
 J_r=\alpha(u+v)^2+\beta u^2+(4\alpha+1)j^2
                     +(r-4\alpha)uj-4\alpha vj.
\]
Subtract its first-order Taylor expansion at B. The quadratic remainder in the invariant differences can be translated by
\(-2\alpha k[\det(g-g_B)-(\Delta j)^2]\).
Identity (13) converts that translation into a quadratic expression in V. Separating its determinant term yields exactly (10)-(12).

This is a minor/Gram-difference translation and a polyconvex supporting-plane operation at the selected background. It does not require pointwise positive heat dissipation or a flow. The underlying determinant identities and supporting-plane principle are classical algebra/variational tools; historical originality is not claimed for those tools.

## 4. Positivity for the entire positive parameter range

The leading principal minors of (10) are
\[
 t^2,\qquad (1+t-k)(t+k-1),
\]
\[
 \det M_{r,k}=
 \frac{2(-3k+2r+4)}{27r}
 \underbrace{[9rk^2+6(r+2)^2k-4(r+2)^2]}_{D_r(k)}.       \tag{14}
\]
The positive root of \(D_r\) is precisely (2). Since \(D_r\) is strictly increasing for k>=0,
\[
 D_r(0)<0,\quad D_r(1)=2r^2+17r+8>0,
\]
\[
 D_r((r+2)/3)=3r(r+2)^2>0,
 \qquad D_r(1-t)=-12r(2r+1)<0.
\]
It follows that
\[
 \max(0,1-t)<k_*<\min(1,(t+1)/2).
                                                        \tag{15}
\]
Therefore the first two principal minors are positive and the third is zero at k_*. A Schur complement proves \(M_{r,k_*}\succeq0\), of rank two. Moreover \(k_*>0\).

These observations prove Theorem 1 from (12): every term on its right is nonnegative when (3) is positive semidefinite.

The correction coefficient \(\lambda_{r,k}(B)\) is constant in space. For a zero-boundary or periodic perturbation,
\[
 \int D\phi=0,\qquad \int\det D\phi=0.
\]
Thus the linear and determinant terms in (12) integrate to zero. Smooth approximation and quartic growth pass the identity and inequality to W^{1,4}. No orientation, injectivity, invertibility, small-amplitude, or Fourier-cutoff restriction is imposed on B+Dphi.

### Exact boundary of the separated-block construction

Within the construction requiring k>=0, \(M_{r,k}\succeq0\), and \(L_{r,k}(B)\succeq0\) separately, the admissible M interval is
\[
 k_*\le k\le1+t.
\]
At the upper endpoint positivity follows by continuity from the interior; outside that interval a principal minor or determinant fails. Also
\[
 \frac{d}{dk}L_{r,k}(B)=-\operatorname{cof}(B^TB)\preceq0.
\]
Hence the most permissive choice for backgrounds in this specific separated-block construction is k=k_*. Theorem 1 is its exact background criterion.

This does not classify every nonnegative quartic support residual: negative quadratic and invariant blocks might compensate without being separately positive. It certainly does not classify the full QC background set.

## 5. All singular backgrounds, strictness, and the general-r margin

By left rotational invariance, write a nonzero singular B as \(e_1\otimes\xi\), \(\xi=(p,q)\), without loss. Then j_B=0 and
\[
 L_{r,k}(B)=\begin{pmatrix}
 t^2p^2+(1-k)q^2&kpq\\kpq&(1-k)p^2+q^2
 \end{pmatrix}.
\]
Its determinant is
\[
 (1-k)(tp^2-q^2)^2+(t+1)(t+1-2k)p^2q^2.                 \tag{16}
\]
At k=k_* the two coefficients are strictly positive by (15). If p or q is zero, the first term is strictly positive. Otherwise the second is strictly positive. Thus L is positive definite for every nonzero singular B, proving the claimed open neighbourhood property by continuity.

There is an especially simple **single rational choice for the entire parameter range**:
\[
 k=\frac23.
\]
The three leading principal minors of M are
\[
 \boxed{t^2,\quad\frac{4r(r+1)}9,\quad\frac{16(r+1)}{27},}
\]
all strictly positive for every r>0. Moreover
\[
 \det L_{r,2/3}(B)=\tfrac13(tp^2-q^2)^2
                  +(t+1)(t-1/3)p^2q^2>0
\]
for every nonzero singular B, since t>1/3. Thus both positive blocks admit a uniform rational construction without parameter sampling, a bounded interval, or an algebraic root. The root k_* is needed only to enlarge the full-rank background cone optimally within the separated-block construction.

For j_B=0 the slope (11), and hence the residual, is independent of k. Compactness on |B|=1 gives a uniform \(\eta_r>0\) with
\[
 R_r(A,B)\ge\eta_r |B|^2|A-B|^2.                        \tag{17}
\]
At B=0, (12) with k=2/3 and M positive definite gives \(J_r(A)\ge c_r^0|A|^4\) for some positive constant; one explicit choice is
\(c_r^0=\alpha/(2\operatorname{tr}(M_{r,2/3}^{-1}))\).
For V nonzero normalize |V|=1 using homogeneity. For singular |B|>=1, (17) bounds R/(1+|B|^2) below by eta_r/2. For singular |B|<=1, this quotient is continuous on a compact set and strictly positive: for B nonzero use (17), and for B=0 use the pointwise lower bound. Its minimum is positive. This proves (5).

The same compactness argument is uniform over compact parameter subintervals of (0,infinity). It is not an algorithm for optimal constants, and no uniform constant as r tends to zero or infinity is asserted.

## 6. Explicit r=1 inequalities

Let B be singular and V=A-B. Define \(\Delta u,\Delta v,\Delta w\) as before and j=j_A. Then (12), at k=1, becomes
\[
\begin{split}
 &J_1(A)-J_1(B)-DJ_1(B):V-\tfrac12(u_B-v_B)\det V\\
 &\quad=\tfrac18(\Delta u+2j)^2+\tfrac18(\Delta v-2j)^2
 +\tfrac14(\Delta w)^2+\tfrac34j^2+\tfrac14|VB^T|^2.     \tag{18}
\end{split}
\]
This formula is invariant under simultaneous left rotations of A and B; it does not require keeping B in a special coordinate form.

Put \(S=|V|^2\), \(X=B:V\). Since B is rank one,
\(|VB^T|^2\ge X^2\), and \(\Delta u+\Delta v=S+2X\).
Discarding nonnegative terms in (18) gives
\[
 R\ge\frac{(S+2X)^2}{16}+\frac{X^2}{4}
   =\frac{S^2}{32}+\frac{(S+4X)^2}{32}
   \ge\frac{|V|^4}{32}.                               \tag{19}
\]
At k=2/3 the matrix M has positive principal minors \(1,8/9,32/27\), while
\[
 L_{1,2/3}(B)=\tfrac13|B|^2I+\tfrac23B^TB.
\]
Therefore (12) also gives \(R\ge |B|^2|V|^2/12\). Combining this with \(|V|^4\le32R\) yields
\[
 |B|^2|V|^2+|V|^4\le44R.
\]
Integration proves (6)-(7). Both hold at the original coefficient \(\alpha=1/8\).

### Full-rank backgrounds at r=1

The matrix L has trace \((2-k)(u_B+v_B)\). On the constraint \(u_Bv_B=w_B^2+j_B^2\), its determinant is exactly the left side of (8). Thus (8) proves Theorem 3.

For the singular-value implication, normalize sigma_1=1 and put e=sigma_2/sigma_1. Then s=u_B+v_B=1+e^2, |j_B|=e, and
\((u_B-v_B)^2+4w_B^2=(1-e^2)^2\).
The smaller eigenvalue of L is bounded below by
\[
 \frac{(2-k)(1+e^2)-k(1-e^2)-4e}{2}
       =(1-e)^2-k.
\]
At k=k_* this is nonnegative precisely on the interval (9). Equality in this orientation-uniform estimate is attained at B=diag(1,e), so increasing that universal ratio threshold loses the particular calibration. It does not prove a QC violation above it.

An example included by (8) but not (9) is B=diag(1,-1/2): the two diagonal entries of L are positive at k_*. At I, however, L has a negative entry. This separates genuine coverage from the remaining obstruction.

## 7. Consequence for the four-dimensional shear-contact family

For \(F=\alpha_0H+\beta_0u^2+\gamma_0j^2+\delta_0uj\) in the positive-coupling ROC sector, the inherited exact acoustic conditions give
\[
 \begin{pmatrix}6\beta_0+\delta_0&\delta_0\\\delta_0&\gamma_0\end{pmatrix}\succeq0,
 \qquad
 \begin{pmatrix}8\alpha_0&\delta_0\\\delta_0&2\beta_0+\delta_0\end{pmatrix}\succeq0.
\]
With \(\delta_0>0\), put
\[
 r_0=(6\beta_0+\delta_0)/\delta_0>0,
 \qquad \eta_0=\delta_0^2/(6\beta_0+\delta_0)>0.
\]
Then
\[
 F=\eta_0J_{r_0}+(\gamma_0-\eta_0)j^2+
 \left[\alpha_0-\frac{\delta_0^2}{8(2\beta_0+\delta_0)}\right]H.
\]
All coefficients of the last two terms are nonnegative. Their determinant-Jensen and convex inequalities transfer Theorems 1-2 to F. Together with the already supplied negative-sector theorem and the elementary zero-coupling case, **every ROC member of this four-dimensional family is now proved QC at every singular affine background**. The qualifier on the background remains indispensable.

## 8. Why this operation still cannot solve the contact background

At B=I, \(L_{r,k}(I)_{22}=-k\). Every admissible k in the separated positive construction is positive. Hence no such certificate reaches I.

A stronger limitation is already inherited and was rechecked directly. A polyconvex supporting plane at I for J_r would have to use determinant slope r+2. This follows because the quadratic residual has a zero in direction e12, whose mixed terms must vanish for a positive semidefinite residual Hessian. On
\[
 V=s\operatorname{diag}(1,-r-1)
\]
the residual is
\[
 -\frac{r(r+2)}3s^3+
 \left[\alpha(r+2)^4+\frac{(r+2)(r+3)}6\right]s^4.
                                                        \tag{20}
\]
It is negative for sufficiently small positive s. Thus no ordinary global supporting plane in the minors exists at I. Merely enlarging the positive blocks of a pointwise minor-support representation cannot fix the actual contact obstruction.

This is not a negative compatible-gradient Jensen construction. A constant full-rank perturbation V does not have the required zero boundary or zero gradient mean. The negative cubic is a polyconvexity obstruction, not a QC counterexample.

### A precise remaining nonlocal inequality

The existing repository already contains the general quartic moment/Schur reformulation of all-background QC. It is not a new discovery here. At r=1 and the conformal background B=I it specializes as follows. Write a=phi1_x, b=phi1_y, c=phi2_x, d=phi2_y and normalized periodic averages. Put
\[
 A_4=\langle J_1(D\phi)\rangle,
 \quad Q_2=\langle(2a+d)^2+c^2\rangle,
\]
\[
 C_3=\langle a^3+5a^2d-4abc+ac^2+2ad^2-2bcd+c^2d\rangle.
\]
The determinant-null identity gives
\[
 \langle J_1(sI+D\phi)-J_1(sI)\rangle
                 =A_4+sC_3+s^2Q_2.                    \tag{21}
\]
In particular all real scalar conformal backgrounds are controlled exactly if
\[
 \boxed{C_3^2\le4A_4Q_2\quad\text{for every compatible periodic }\phi.} \tag{22}
\]
When Q2=0 the condition includes C3=0. This is an infinite-dimensional all-gradient inequality, not a finite SDP test. Neither (22) nor its full four-coordinate background version has been proved in this investigation.

The new background calibration removes singular and a significant collection of full-rank backgrounds as counterexample targets. It does not establish (22). A continuation should attack that missing compatible cubic compensation or its full background version, rather than search for another pointwise minor support at I, which (20) excludes.

## 9. Counterexample attempts and exact scope

Two actual-compatible search spaces were investigated at the unchanged coefficients: finite Fourier maps and continuous periodic piecewise-affine nodal maps. The affine background was minimized analytically through the known quartic moment matrix for each map, rather than fixed before optimization. The numerical implementation uses a small regularization in the inverse of that moment matrix; it is exploratory, not rigorous optimization or certification.

For Fourier bandwidth m, the grid has 4m+1 points per dimension, avoiding quartic aliasing in exact arithmetic. The finite element maps are genuine nodal interpolants on a periodic triangulation, with exact elementwise gradient formulas and equal triangle weights. Both constructions enforce compatibility by construction.

The supplied `SEARCH_SUMMARY.json` records 200 completed local searches and their numerical minima. The saved best candidates were independently re-evaluated using the actual unregularized moment energy at their saved backgrounds. The three P1 candidates were additionally rounded to rational nodal/background data and checked exactly: their means and determinant means are zero and their Jensen energies are positive. These are audits of specified candidates, not lower bounds for any search class. No negative optimized Jensen energy was obtained. The minima are results of local searches, not lower bounds over their finite-dimensional spaces, and certainly not a proof over all gradients. Ill-conditioned affine minimization, discretization restrictions, high-frequency concentration, and local optimization traps remain limitations.

Exploratory positive rational SOS matrices at r=1, r=1/10 and r=4 helped reveal the family identity. They are not premises of the universal proof and do not substitute for it. The certificate used in Theorems 1-3 is the universal identity (12), with algebraic sign proofs for all r>0.

Linear equivalence to the negative branch cannot be inferred from continuation: its two contact backgrounds have equal determinant signs, while the positive branch has opposite signs. Common invertible input/output transformations preserve this relative sign. Partial hodograph or inverse-map arguments require additional orientation/injectivity hypotheses and were not promoted to a theorem for the unrestricted test class.

## 10. Prior work and concurrent research

The reference pin is stated at the top. N877 explicitly retains the distinction between finite H-completion and unchanged-coefficient QC. N874 retains failures of scalar-potential projection and positive Burkholder superposition, along with the known moment inequality. These are not imported as certified premises of the new identity, and their searches were not repeated.

Bruno-Pasqualotto, arXiv:2608.06367v1, Theorem 2 has both left and right SO(2) invariance. It does not directly apply to J_r. Their heat/exact-two-form method is a predecessor of the incoming negative theorem; the present argument instead constructs a supporting plane in the minors at a restricted set of backgrounds. No claim to invent determinant null Lagrangians, translation arguments, or convex supporting-plane logic is made.

Kirchheim-Kristensen's rank-one-background convexity theorem concerns degree-one homogeneous rank-one convex functions, not the present degree-four J_r. Raising or taking a fourth root does not automatically transfer its hypotheses. Guerra-Kristensen's automatic polyconvexity theorem uses isotropy and concerns conformal matrices; those hypotheses differ, and J_r is demonstrably not polyconvex at I. These primary comparisons delimit apparent similarity; they do not establish historical novelty of the exact calibration.

Pedregal's arXiv:1905.06571v5, revised 18 June 2026, claims the full planar equivalence. The primary Section 4 permits arbitrary interface labels; Definition 6.1 and Corollary 7.2 require nonempty images for every permitted fixed mold. I read those primary statements and Sol's exact permitted-mold counterexample. The small independent reconstruction in `verify_peer_obstruction.py` checks the nodal gradients and the determinant separation on the whole weight box. For its required subtree,
\[
 U=(4,-6-2a+2b),\quad V=(8,6-2c+2d),\quad a,b,c,d\in[0,1],
\]
\[
 \det(U,V)=72+16a-16b-8c+8d\ge48.
\]
Consequently the requisite parallelism fails for that allowed mold. The failure is of the stated nonempty-image proof route; it is not a refutation of the conjectured implication, nor of every function-dependent or differently chosen mold. This is Sol's construction, rechecked here, not a new discovery of this run.

A contemporaneous 8 October 2026 Warwick analysis seminar describes the 2x2 case as remaining open. This is contextual evidence, not mathematical validation of any proof. No general claimed solution or sharp external constant is assumed here.

## 11. Exact next obligation and preservation

The achieved result is fixed-coefficient, family-wide in r, and all-gradient within its stated background cone. It does **not** close the positive family, not even the single r=1 integrand at every background.

The next decisive obligation is to prove the compatible cubic estimate (22), then its full background version, or to produce a compatible field violating one of them. Any negative candidate must be re-evaluated with exact/interval arithmetic, including the optimized background and every spatial integral, against the independent ROC proof. Failure of the background cone test or of any Gram search is not such a candidate.

Files: `CALIBRATION.json` contains all compact coefficient formulas; `verify_calibration.py` is the standalone symbolic reconstruction; `VERIFICATION_RECEIPT.json` records its 24 passing groups; `evidence/` records the incoming replay and peer calculation; `exploration/` preserves compatible searches and discovery checks; `SOURCES.json` records source pins and primary URLs. The mathematical status and unresolved gate are also in `RESEARCH_STATE.json`.
