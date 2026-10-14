# Adaptive covariance regression beyond one quadratic cone

## Result

The covariance-regression step does extend beyond one indefinite quadratic form. For a regular, constant-rank intersection of finitely many quadratic null constraints, the scalar normal identity becomes a Moore–Penrose normal regression. Its exact consequence is still

\[
  z:=\mathbb E[sY]\in\operatorname{ran}\mathcal J_R^*,\qquad
  \mathcal J_R z=-\mathbb E\Phi(Y),\qquad
  |z|\le C_\Phi\,\gamma^{-1}\mathbb E|Y|^2,
\]

where \(R\) is the covariance-maximizing null direction, \(s=X:R\), \(Y=X-sR\), and \(\gamma\) is the smallest nonzero singular value of the constraint Jacobian on the unit-sphere tangent space. The estimate is an exact balance identity followed by a finite-dimensional pseudoinverse bound.

I prove below a complete all-affine fourth-moment law theorem under this geometric condition, a simple acoustic kernel, and a locally stable multi-Finsler positive remainder. The fully minimized gap is within \(C(\delta_2+\delta_4)\mathbb E s^4\) of

\[
  F(R)\left(\mathbb E s^4-\frac{2(\mathbb E s^3)^2}{3\mathbb E s^2}\right).
\]

The error includes the Schur elimination of every affine direction. For sufficiently small relative transverse \(L^2\) and \(L^4\) mass, the gap is bounded below by a fixed positive multiple of \(\mathbb E|X|^4\), with no bound on amplitudes and no lower bound on \(\mathbb E|X|^2\).

For higher-dimensional rank-one cones, the geometric part does apply: all 2-by-2 minors have differential rank equal to the normal codimension at every nonzero rank-one matrix. Periodic gradients balance each minor. The theorem then applies to an individual rank-one-convex quartic if its contact has the stated simple spectral geometry and a stable local positive-remainder certificate. Those conditions do not follow automatically from rank-one convexity in general dimensions. A primary 3-by-3 quadratic example is rank-one convex but not polyconvex, so positivity on the rank-one cone does not force the PSD-plus-minors representation needed for a quartic Hessian. Constant rank of a differential operator alone also does not supply the needed quadratic moments.

This is a conditional extension of the incoming theorem’s proof mechanism, not a full quasiconvexity result or a novelty claim. The local theorem is derived in this report; the tangent counterexample and the N797/N800/N806 results below are source results with their original evidence status retained.

## Exact assumptions and theorem

Let \(V\) be a finite-dimensional real Hilbert space. Let

\[
  q_j(x)=\langle J_jx,x\rangle,\quad J_j=J_j^*,\quad
  \Phi=(q_1,\ldots,q_k),\quad
  \Lambda=\{x:\Phi(x)=0\},\quad
  \Sigma=\Lambda\cap S(V).
\]

Fix \(R_0\in\Sigma\). For \(R\in\Sigma\), set

\[
  \mathcal J_R=D\Phi(R)|_{R^\perp}:R^\perp\to\mathbb R^k.
\]

Assume the spherical common zero set \(\Sigma\) is an embedded \(C^2\) submanifold near \(R_0\), with \(T_R\Sigma=\ker\mathcal J_R\) for \(R\) in a relative neighborhood \(U\). On \(U\), assume \(\mathcal J_R\) has constant rank \(r\ge1\), its nonzero singular values lie in \([\gamma,\Gamma]\) for some \(0<\gamma\le\Gamma<\infty\), and \(\|D\Phi(R)\|\le\Gamma\). This includes a regular-level presentation after locally removing redundant constraints; the explicit embeddedness/tangent condition also covers a redundant full list such as all matrix minors. Its normal space in \(R^\perp\) is \(\operatorname{ran}\mathcal J_R^*\).

Let \(F:V\to\mathbb R\) be a homogeneous quartic. Write \(D^2F(A)\) for its Hessian as a self-adjoint operator. Assume:

1. **Cone convexity:** for every \(A\in V\) and \(R\in\Lambda\),
   \(D^2F(A)[R,R]\ge0\).
2. **Simple acoustic kernel:** \(F(R_0)>0\), and for some unit \(A_0\),
   \(M_0:=D^2F(R_0)\succeq0\), \(\ker M_0=\operatorname{span}\{A_0\}\), and
   \(M_0|_{A_0^\perp}\succeq dI\) for some \(d>0\).
3. **Stable local remainder:** on a neighborhood \(W\) of \(A_0\), there are continuous \(P(A)\succeq0\) and \(\lambda_j(A)\in\mathbb R\) such that
   \[
     D^2F(A)=P(A)+\sum_{j=1}^k\lambda_j(A)J_j,
   \]
   and \(P(A_0)\) has kernel exactly \(\operatorname{span}\{R_0\}\).

The third item is an explicit local multi-Finsler hypothesis. By continuity, after shrinking \(U,W\), there is \(\nu>0\) such that \(P(A)[Y,Y]\ge\nu|Y|^2\) for every \(R\in U\), \(A\in W\), and \(Y\perp R\). The certificate need only hold near \(A_0\); cone convexity is the global assumption.

For a centered probability law \(X\) with \(\mathbb E|X|^4<\infty\) and \(\mathbb E\Phi(X)=0\), let \(R\) maximize \(\langle CR,R\rangle\) over \(\Sigma\), where \(C=\mathbb E[X\otimes X]\). Choose the sign with \(R:R_0\ge0\), and define

\[
 s=X:R,\quad Y=X-sR,\quad m_j=\mathbb E s^j,\quad
 v=\mathbb E|Y|^2,\quad t=\|Y\|_4,\quad
 \delta_2=\sqrt{v/m_2},\quad\delta_4=t/m_4^{1/4}.
\]

There are constants \(\delta_*>0\), \(C<\infty\), and \(\eta>0\), depending only on the fixed data above, such that whenever the law is nonzero and initially satisfies

\[
  \|Y_0\|_2\le\delta_*\|s_0\|_2,\qquad
  \|Y_0\|_4\le\delta_*\|s_0\|_4,
  \quad s_0=X:R_0,\quad Y_0=X-s_0R_0,
\]

the adaptive \(R\) lies in \(U\), its least-eigenvalue unit vector \(a_R\) lies in \(W\), and

\[
 \left|\Delta_F(X)-F(R)\left(m_4-\frac{2m_3^2}{3m_2}\right)\right|
       \le C(\delta_2+\delta_4)m_4, \tag{T1}
\]

where

\[
 \Delta_F(X)=\inf_{B\in V}\mathbb E\,[F(B+X)-F(B)].
\]

In particular, after decreasing \(\delta_*\) if needed,

\[
  \Delta_F(X)\ge\eta\,\mathbb E|X|^4. \tag{T2}
\]

The statement quantifies over all centered balanced probability laws with finite fourth moment satisfying these relative conditions. It therefore includes any compatible periodic or zero-boundary field whose normalized law has the same moment balances. No pointwise support restriction, amplitude cap, or positive lower bound on \(m_2\) is imposed.

## Proof

### Normal regression for several quadratic constraints

At the maximizing \(R\), first-order optimality on \(\Sigma\) gives

\[
  CR-m_2R=z\in\operatorname{ran}\mathcal J_R^*,\qquad z=\mathbb E[sY].
\]

Indeed, \(CR-m_2R\perp R\), and its inner product with every tangent vector \(V\in R^\perp\) satisfying \(\mathcal J_RV=0\) is zero. The orthogonal complement of that tangent space is \(\operatorname{ran}\mathcal J_R^*\).

Since each \(q_j\) is quadratic and \(q_j(R)=0\),

\[
  0=\mathbb E q_j(X)
   =\mathbb E q_j(Y)+2\mathbb E[s\langle J_jR,Y\rangle].
\]

The second term is the \(j\)-th component of \(\mathcal J_Rz\), so

\[
  \mathcal J_Rz=-\mathbb E\Phi(Y).
\]

The restriction of \(\mathcal J_R\) to \(\operatorname{ran}\mathcal J_R^*\) has inverse norm at most \(\gamma^{-1}\). Also

\[
 |\mathbb E\Phi(Y)|\le
 \left(\sum_j\|J_j\|^2\right)^{1/2}\mathbb E|Y|^2.
\]

Therefore

\[
  |z|\le C_\Phi\gamma^{-1}v. \tag{1}
\]

For a nonzero law, each initial scalar norm \(\|s_0\|_p\), \(p=2,4\), is positive: if it were zero, the corresponding relative closeness condition would force \(Y_0=0\) and hence \(X=0\) almost surely. The fit argument below gives \(\cos\theta\) close to one. Since \(s=s_0\cos\theta+R:Y_0\), we then have \((\cos\theta-\delta_*)\|s_0\|_p\le\|s\|_p\le(1+\delta_*)\|s_0\|_p\), so the fitted moments are positive and the ratios are well-defined.

This is the scalar normal regression identity in its constant-rank form. Redundancy among the \(q_j\) is harmless once it is removed by the Moore–Penrose inverse; loss of rank is not.

The maximizing line remains close to \(R_0\). Its residual second moment is no greater than the residual at \(R_0\), so if \(\theta\) is the angle between the fitted lines,

\[
 \|s_0\|_2\sin\theta\le\|Y_0\|_2+\|Y\|_2\le2\|Y_0\|_2.
\]

Moreover \(Y=P_{R^\perp}(s_0R_0+Y_0)\), hence

\[
 \|Y\|_4\le\|Y_0\|_4+\sin\theta\|s_0\|_4.
\]

Thus sufficiently small initial relative norms put \(R\) in \(U\) and make both fitted ratios \(\delta_2,\delta_4\) small. No stationarity assumption is made about the original \(R_0\); it is obtained by fitting.

### Moving contact and the averaged Hessian

Quartic reciprocity gives

\[
 D^2F(A)[X,X]=D^2F(X)[A,A],\qquad
 \mathbb E D^2F(X)=m_2M_R+D^3F(R)[z]+\mathbb E D^2F(Y).
\]

By (1),

\[
 H:=\mathbb E D^2F(X)=m_2M_R+O(v). \tag{2}
\]

Cone convexity and reciprocity imply \(M_R\succeq0\) for every \(R\in\Sigma\). Since \(M_0\) has a simple kernel, the least eigenpair of \(M_R\) is a continuous simple pair \((\epsilon,a_R)\) near \((0,A_0)\), with \(\epsilon\ge0\), while the remaining eigenvalues stay at least \(d/2\). The eigenvector perturbation bound gives \(|a_R-A_0|\le C|R-R_0|\). The local certificate at \(A_0\) also gives

\[
 0\le\epsilon\le A_0^TM_RA_0
   =D^2F(A_0)[R,R]
   =P(A_0)[R,R]\le C|R-R_0|^2. \tag{3}
\]

Set \(P_R=P(a_R)\). Reciprocity, \(q_j(R)=0\), and the eigenvalue equation imply

\[
  P_R[R,R]=D^2F(a_R)[R,R]=D^2F(R)[a_R,a_R]=\epsilon.
\]

In the moving frame \(a_R\oplus a_R^\perp\), write

\[
 H=\begin{bmatrix}h&k^T\\k&D\end{bmatrix}.
\]

Equation (2), after shrinking the fitted neighborhood, yields \(D\succeq c_Dm_2I\) for some fixed \(c_D>0\), and \(|k|\le Cv\). Balance and the local certificate yield

\[
 h=\mathbb E P_R[X,X]
   =m_2\epsilon+2\langle P_RR,z\rangle+\mathbb E P_R[Y,Y].
\]

For a positive operator, \(|P_RR|^2\le\|P_R\|P_R[R,R]\le C\epsilon\). The transverse gap and (1) then give, for small enough \(\epsilon\),

\[
  m_2\epsilon+\frac{\nu}{2}v\le h\le m_2\epsilon+Cv. \tag{4}
\]

The true reduced denominator after eliminating every complementary background component is

\[
 \sigma=h-k^TD^{-1}k\ge c(m_2\epsilon+v),\qquad
 \sigma\ge(1-C\delta_2^2)h. \tag{5}
\]

Thus the normal regression controls the actual Schur denominator. A fixed-frame estimate for \(h\) alone would not imply (5).

### Full affine elimination

Let \(b=\mathbb E DF(X)\), \(c=\mathbb E F(X)\), and \(u=m_3/(3m_2)\). Centeredness and quartic homogeneity give the exact background polynomial

\[
 \mathbb E[F(B+X)-F(B)]=c+\langle b,B\rangle+\tfrac12\langle HB,B\rangle.
\]

Set \(\ell=b-uHR\). For a pure line \(X=sR\), Euler’s identity makes \(\ell=0\) in every background direction, not just along \(R\). For general \(X=sR+Y\), polarization gives the exact identity

\[
\begin{aligned}
\ell={}&M_R\big(\mathbb E[s^2Y]-2uz\big)
 +\tfrac12\mathbb E\big[sD^3F(R)[Y,Y,\cdot]\big]\\
 &+\mathbb E DF(Y)-u\,\mathbb E[D^2F(Y)R].
\end{aligned} \tag{6}
\]

Hölder’s inequality, (1), and the eigenvector relation \(M_Ra_R=\epsilon a_R\) imply, for \(\delta_2,\delta_4\le1\),

\[
 |\ell_{a_R^\perp}|\le C m_4^{1/2}\sqrt v,
 \qquad
 |\ell_{a_R}|\le C m_4^{1/2}\sqrt v(\epsilon+\delta_2+\delta_4).
\]
In the \(a_R\) component, the four types of terms in (6) are bounded respectively by
\[
 C\epsilon m_4^{1/2}\sqrt v,\quad
 C\epsilon|u|v,\quad
 C(m_4^{1/4}t+t^2)\sqrt v,\quad
 C|u|v.
\]
Here \(|u|\le m_4^{1/2}/(3\sqrt{m_2})\), and \(t=\delta_4m_4^{1/4}\), \(\sqrt v=\delta_2\sqrt{m_2}\); these give the displayed estimate. The transverse component uses the same bounds without the eigenvalue factor \(\epsilon\).

Together with (4)–(5), block inversion now uses the actual reduced numerator and denominator and yields

\[
 \ell^TH^{-1}\ell\le C(\delta_2^2+\delta_4^2)m_4,
 \quad
|\ell_{a_R}-k^TD^{-1}\ell_{a_R^\perp}|
     \le C\sqrt{\sigma m_4}(\delta_2+\delta_4). \tag{7}
\]

Minimizing first over the shifted background \(B=-uR+Z\) gives

\[
 \Delta_F(X)=Q_{\rm fit}-\tfrac12\ell^TH^{-1}\ell,
 \quad
 Q_{\rm fit}=c-u\langle b,R\rangle+\tfrac12u^2\langle HR,R\rangle.
\]

Direct quartic expansion and Hölder bounds give

\[
\left|Q_{\rm fit}-F(R)\left(m_4-\frac{2m_3^2}{3m_2}\right)\right|
       \le C(\delta_2+\delta_4)m_4. \tag{8}
\]

Combining (7) and (8) proves (T1). Since \(m_3^2\le m_2m_4\), the scalar bracket is at least \(m_4/3\). Near \(R_0\), \(F(R)\ge F(R_0)/2\). Finally,

\[
 \mathbb E|X|^4=m_4+2\mathbb E[s^2|Y|^2]+\mathbb E|Y|^4
 \le(1+\delta_4^2)^2m_4.
\]

Shrinking \(\delta_*\) proves (T2). If \(v=0\), then \(X=sR\), \(b=(m_3/(3m_2))HR\), and direct minimization, including the singular case, gives

\[
 \Delta_F(sR)=F(R)\left(m_4-\frac{2m_3^2}{3m_2}\right).
\]

This covers every affine direction and closes the proof.

## Rank-one and constant-rank differential systems

### Higher-dimensional rank-one cones

For \(V=\mathbb R^{m\times n}\), take \(\Phi\) to list all 2-by-2 minors. Its common zero cone is the rank-at-most-one cone. At a nonzero rank-one matrix, orthogonal changes of coordinates reduce the point to \(e_{11}\). The differentials of the minors using row 1 and column 1 independently detect the \((m-1)(n-1)\) entries in the lower-right block; all other first-order directions are tangent to the rank-one manifold. Thus \(D\Phi_R\) has constant rank \((m-1)(n-1)\), equal to the normal codimension. The normalized rank-one set is compact and the nonzero singular values of this differential are uniformly separated from zero.

Each 2-minor is a quadratic null Lagrangian. For periodic or zero-boundary \(W^{1,4}\) gradients \(X=D\varphi\) of mean zero, \(\mathbb E\Phi(X)=0\). Hence the normal-regression estimate (1) applies to rank-one covariance fitting in every matrix size. This resolves the geometric warning in the incoming note: higher-dimensional rank-one cones need several minor constraints, but they do not defeat the covariance-normal estimate itself.

The remaining issue is the local positive remainder. For a fixed quartic satisfying cone convexity, the theorem applies only if the reference acoustic kernel is simple and its Hessian at \(A_0\) admits a continuous local decomposition into a PSD remainder plus a linear combination of the minor Hessians, with the PSD remainder coercive transverse to \(R_0\). Neither property is automatic in 3-by-3 matrices. Harutyunyan–Milton give a 3-by-3 rank-one-convex quadratic form that is not polyconvex; such a quadratic form cannot be represented as a PSD quadratic form plus a linear combination of 2-minors. Thus rank-one convexity supplies cone nonnegativity but not the certificate this proof needs.

### Constant-rank systems

Let \(\mathcal A\) be a homogeneous constant-rank differential operator with wave cone \(\Lambda_{\mathcal A}=\bigcup_{\xi\ne0}\ker\mathcal A(\xi)\). A conditional transfer holds if, near the reference direction, this cone is the common zero set of finitely many homogeneous quadratic \(\mathcal A\)-quasiaffine null Lagrangians \(q_j\), their common constraint map has constant rank with a positive singular-value gap, and the integrand satisfies the cone-convexity and local remainder hypotheses above. Mean-zero periodic \(\mathcal A\)-free fields then balance each \(q_j\) and inherit (T1)–(T2).

The qualifications are substantive. Constant rank alone does not give quadratic conservation laws or an algebraic description by quadrics. Guerra–Raiţă’s constant-rank theory gives an effective characterization of \(\mathcal A\)-quasiaffine null Lagrangians, but their Example 5.15 proves that three-dimensional divergence-free matrix fields have no nontrivial homogeneous quadratic null Lagrangians. In such a system there is no \(\Phi\) of the required kind. Nor does the fact that some quadratics vanish on a wave cone by itself imply they are null Lagrangians; the exact integral identity is needed.

## Failure examples and exact boundaries

### Degenerate constraint Jacobian: regression loses one power

In \(V=\mathbb R^3\), write \(x=(x_0,y_1,y_2)\), and take

\[
 q_1(x)=y_1^2-y_2^2,\qquad q_2(x)=y_1y_2.
\]

Their common null cone is just the \(x_0\)-axis, so its unit slice is \(\{\pm e_0\}\), but \(D\Phi(e_0)=0\): the defining equations are singular at the only admissible line. Let \(U\in\{e_1,-e_1,e_2,-e_2\}\) have probabilities \(3/8,1/8,1/4,1/4\), and let an independent \(s\) be uniform on \(\{-1,1\}\). Then

\[
 X=s(e_0+\varepsilon U),\quad
 \mathbb EX=0,\quad \mathbb Eq_1(X)=\mathbb Eq_2(X)=0,
 \quad \mathbb E|Y|^2=\varepsilon^2,
 \quad z=\mathbb E[sY]=\frac{\varepsilon}{4}e_1.
\]

Both relative transverse norms are exactly \(\varepsilon\), but \(|z|/\mathbb E|Y|^2=1/(4\varepsilon)\to\infty\). Thus no uniform \(O(v)\) normal regression survives if the constraint Jacobian loses rank, even though the fitted null line is unambiguous. The exact check is in `check_results.json`.

### Multiple Finsler multipliers are not automatic

Here is an exact five-variable example. Let \(q_j(x)=x_j^2-x_1^2\), \(j=2,3,4,5\), so their common null cone consists of sign vectors times a scalar. On this cone,

\[
  Q_*(x)=\frac35\sum_{i=1}^5x_i^2+\sum_{i=1}^5x_ix_{i+1},\qquad x_6=x_1,
\]

is nonnegative: after setting \(x_i=\sigma_i t\), the five-cycle edge sum has minimum \(-3t^2\), so \(Q_*\ge0\).

If \(Q_*=P+\sum_{j=2}^5\lambda_jq_j\) with \(P\succeq0\), then \(P\) has off-diagonal entries \(1/2\) on the five-cycle, zero on the nonedges, and trace 3. Average P over the dihedral symmetries of the cycle. The averaged matrix is still PSD, with diagonal \(3/5\) and cycle adjacency contribution \(A(C_5)/2\). Its least eigenvalue is

\[
 \frac35+\cos(4\pi/5)=\frac{7-5\sqrt5}{20}<0,
\]

a contradiction. Thus cone nonnegativity on the common zero set does not imply the multi-Finsler representation. This is an independently derived counterexample to automatic multi-constraint exactness.

There are two relevant primary precedents. Meijer et al. show that even the non-strict one-constraint Finsler implication can fail for a semidefinite constraint: with \(N=\begin{psmallmatrix}1&1\\1&1\end{psmallmatrix}\) and \(M=\operatorname{diag}(1,-1)\), \(x^TMx=0\) on \(x^TNx=0\), yet no scalar \(\alpha\) makes \(M+\alpha N\succeq0\). Their non-strict equivalence is restored for an indefinite N. Separately, Harutyunyan–Milton’s explicit 3-by-3 example is rank-one convex and not polyconvex. For quadratic forms, a PSD-plus-null-Lagrangian decomposition is exactly the relevant polyconvex representation, so that example refutes automatic multi-minor Finsler closure in the matrix setting.

### Failure of the simple transverse remainder

The incoming source gives an exact balanced-law counterexample at its tangent quartic

\[
 G=3(u+v-2q)^2+\frac{35}{24}u^2+q^2-\frac52qu,
 \quad u=|x|^2,\ v=|y|^2,\ q=\det A.
\]

At contact \(A_0=I, R_0=e_{12}\), the positive Finsler remainder is

\[
 P_0(a,b,c,d)=\tfrac12(3a-2d)^2+\tfrac56c^2,
\]

of rank two, rather than rank three with kernel only \(R_0\). For fixed \(m=9\), small \(\varepsilon>0\), set

\[
 w=1-\tfrac32\varepsilon,\quad
 t=\frac{(9/2)m^2\varepsilon}{w},\quad
 R_t=\begin{pmatrix}0&1\\t&0\end{pmatrix},\quad
 S=\operatorname{diag}(1,3/2).
\]

Put probability \(w/2\) on each of \(\pm R_t\), probability \(\varepsilon\) on \(mS\), and probability \(\varepsilon/2\) on \(-2mS\). This law is centered and determinant-balanced. Its unique covariance-maximizing rank-one line is \(e_{12}\) for small \(\varepsilon\), and its relative transverse \(L^2,L^4\) norms tend to zero. Along the affine direction \(I\), its optimized one-dimensional gap is

\[
 c-\frac{\beta^2}{2h},\quad
 \beta=\frac54\varepsilon m^3,\quad
 h=\frac{135}{8}\frac{m^4\varepsilon^2}{w},\quad
 \lim_{\varepsilon\downarrow0}\left(c-\frac{\beta^2}{2h}\right)
 =3-\frac{5m^2}{108}=-\frac34.
\]

It is already negative at \(\varepsilon=10^{-6}\); the full averaged Hessian is positive definite there, so the full affine infimum is no larger. This is a genuine counterexample to deleting the simple transverse-kernel hypothesis from the balanced-law theorem. It is **not** a gradient law and hence is not a counterexample to quasiconvexity. The local source independently gives the exact construction, and my SymPy check recomputes the law, balances, Hessian positivity, adaptive line, and negative directional gap from its stated atoms.

### What multiple null moments do not give for gradients

N800 gives a compatible 3-by-2 gradient

\[
 G(x,y)=\begin{pmatrix}
 \cos x&0\\0&\cos y\\\cos(x+y)&\cos(x+y)
\end{pmatrix}
=D(\sin x,\sin y,\sin(x+y)).
\]

In its three-dimensional matrix subspace the three 2-minors are \(st,sr,-tr\); all have mean zero. Yet the resonant cubic \(str\) has mean \(1/4\), while its second derivative vanishes on each of the three rank-one coordinate axes. Thus the single-quadric cubic-integrability/nullspace-closure step in N800 does not transfer to several minors by moment balance alone. This does not refute the local all-affine theorem above, which uses a simple contact and positive transverse remainder; it blocks a broader attempt to replace those assumptions by several balanced moments.

## What the capital results supply

**N800** supplies a source theorem for one indefinite quadric: the planar determinant case has nullspace closure and full-affine background range control. It also supplies full-nine-coefficient Jensen results on exact singular averaged-Hessian faces. The explicit 3-by-2 resonant cubic above shows why its one-quadric closure argument does not transport directly to multiple minors. N800 does not control the positive-definite Hessian sector for every compatible field, nor does it supply the moving multi-constraint local certificate or (T1) in higher rank.

**N806** supplies compatible fixed-contact cubic compensation for the left-rotation-invariant planar quartic class, including a differential Hodge correction and a mixed-derivative interpolation estimate. Its all-background calculation still leaves the Schur quotient

\[
 h^*=h-k^TD^{-1}k,\qquad
 \beta^*=\beta-k^TD^{-1}\gamma,
\]

and the open gate asks for a compatible bound on \(|\beta^*|^2/h^*\). Its source records examples with \(h^*/h\to0\) and positive gaps, so the denominator collapse alone is not a counterexample. N806 does not establish the moving reduced-numerator estimate needed at tangent contacts.

**N797** supplies exact sharp quartic slices and heat/exact-form certificates in specified planar symmetry sectors. It does not supply a general multi-null regression or the local Finsler/Schur operation above; its full nine-coefficient and general Morrey gates remain open.

The incoming adaptive note itself already proves the scalar determinant case, the formula (T1), and full affine elimination near a simple transverse contact. The result here isolates the precise geometric replacement for its scalar identity and proves the corresponding conditional multi-constraint theorem. It does not close N800’s general compatible positive-definite sector, N806’s tangent moving-Schur gate, or N797’s universal representation gate.

## What must be added beyond one quadratic, and prior art

The multi-constraint analogue has two separate steps. First, replace scalar normal regression by a **joint normal lift**: stationarity places \(z=\mathbb E[sY]\) in the row space of the full constraint Jacobian, while balance prescribes its image as \(-\mathbb E\Phi(Y)\); a uniformly bounded Moore–Penrose inverse then gives the \(O(v)\) estimate. Second, to carry that estimate through quartic affine minimization, one needs a **moving local multi-Finsler certificate** \(D^2F(A)=P(A)+\sum_j\lambda_j(A)J_j\), with a PSD remainder that stays coercive transverse to the fitted null direction, plus the simple acoustic eigengap. The first step follows from regular geometry; the second is a genuine extra algebraic hypothesis. Several moment balances alone do not supply it, as the five-cycle example and N800 resonant gradient demonstrate.

The indefinite one-quadratic non-strict Finsler lemma is established prior work. Meijer et al., *A General Non-Strict Finsler’s Lemma*, arXiv:2403.10306v1 (15 March 2024), Lemma 2 and Example 1, record the exact indefinite case and a semidefinite failure ([arXiv version](https://arxiv.org/abs/2403.10306v1); [Eindhoven-hosted primary PDF](https://pure.tue.nl/ws/portalfiles/portal/358730225/2403.10306v1.pdf)). This report does not claim the one-constraint result.

Harutyunyan and Milton, *Explicit examples of extremal quasiconvex quadratic forms that are not polyconvex*, arXiv:1403.3718v3, Theorem 1.5, give an explicit 3-by-3 quadratic form that is quasiconvex (equivalently rank-one convex in this quadratic setting) but not polyconvex ([arXiv HTML, v3](https://arxiv.org/html/1403.3718v3)). Their introduction explains that for quadratic forms polyconvexity is precisely a sum of a convex quadratic form and a quadratic null Lagrangian. This is prior evidence that cone positivity need not imply the PSD-plus-minors certificate assumed here.

Guerra and Raiţă, *Quasiconvexity, null Lagrangians, and Hardy space integrability under constant rank constraints*, arXiv:1909.03923v3 (1 July 2020), Theorem A, Proposition 5.3, and Example 5.15, develop the constant-rank null-Lagrangian framework and prove there are no non-affine quadratic null Lagrangians for three-dimensional divergence-free matrix fields ([arXiv HTML, v3](https://arxiv.org/html/1909.03923v3)). This supports the conditional PDE interface and its limits; it does not establish the fourth-moment theorem here.

Rapoport, *Extension of S-procedure in the Analysis of Multivariable Control Systems*, IFAC Proceedings Volumes 38(1), 203–208 (2005), is related context on loss of exactness for several quadratic inequality constraints ([publisher page](https://www.sciencedirect.com/science/article/pii/S1474667016369907); [NTNU-hosted primary PDF](https://skoge.folk.ntnu.no/prost/proceedings/ifac2005/Fullpapers/01573.pdf)). It concerns an inequality S-procedure, not this equality-constrained local decomposition, so it is not used as proof of the five-cycle result.

Covariance normal-space stationarity, the Moore–Penrose bound, and Schur complementation are standard finite-dimensional tools. The report’s analytic combination is derived here conditionally; no historical priority or external correctness claim is made for it.

The incoming, N797, N800, and N806 claims retain their source labels: internally derived and unreviewed externally. Exact symbolic checks establish only the finite identities listed below. They do not validate the analytic theorem, external correctness, priority, full quasiconvexity, or laboratory capability.

## Checks and limitations

`verify_examples.py` is an independent exact SymPy implementation written in this assigned folder; it imports no producer verifier. It passes three groups: (i) singular-constraint regression failure, (ii) the five-cycle multi-Finsler counterexample, and (iii) the tangent balanced-law construction including balance, covariance-fit certificate, Hessian positivity, and negative directional affine gap. The output is `check_results.json`.

The analytic theorem’s estimates are proved above and are not formalized by the script. The generic multi-Finsler condition, regularity constants, local certificate continuity, and simple-kernel assumptions must be verified for each proposed integrand and constraint system. General Morrey/quasiconvexity, non-simple tangent contacts, high transverse fourth-moment mass, external review, and historical priority remain unresolved.
