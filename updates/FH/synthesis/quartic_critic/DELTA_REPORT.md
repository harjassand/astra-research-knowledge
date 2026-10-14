# Independent delta audit: exact deflation and quantitative nullspace bounds

## Verdict and scope

The exact-background calculation in `../FH-root/near_face_deflation.py` checks out. Optimizing over every affine background strengthens the displayed trial-background calculation: for every ε>0 the exact minimum tends to zero, while the attained singular field at ε=0 has minimum 1/4. The minimizing backgrounds escape to infinity, so this is a failure of lower semicontinuity of the optimized value at that singular field. The gaps remain nonnegative; this is not a quasiconvexity counterexample.

The conditional estimates in `../FH-quartic/QUANTITATIVE_NULLSPACE_STABILITY.md` also check out with the stated fixed-decomposition and moment assumptions. They are local bounds for one cubic component of the affine-background load, not a full Schur-remainder estimate or a uniform near-face theorem. The note correctly limits its (1/4)-power reduced-law example: its (C_A,P,q) data do not satisfy quartic integrability, so they do not prove sharpness for actual quartics.

## Exact affine-background minimum

Let

\[
X_\varepsilon=X_0+\varepsilon Y+\varepsilon^2Z,
\quad X_0=D(\sin x\cos y,-\cos x\sin y),
\quad Y=D(-\tfrac14\sin2x,-\tfrac14\sin2y),
\quad Z=D(\sin y,\sin x),
\]
with normalized torus average and row-major vectorization. These are smooth periodic gradients with a fixed finite Fourier support, zero mean, and a uniform (L^\infty) bound for (0<\varepsilon\le1/2). For (q(A)=\det A), set (q_0=q(X_0)). Direct trigonometric moments give

\[
q_0=-\frac{\cos2x+\cos2y}{2},\quad \mathbb E q_0^2=\frac14,
\quad \operatorname{tr}X_\varepsilon=\varepsilon q_0,
\quad \mathbb E X_\varepsilon=0,\quad \mathbb E q(X_\varepsilon)=0.
\]

For (F=q^2), write (C=\mathbb E[\operatorname{vec}X_\varepsilon\operatorname{vec}X_\varepsilon^T]), (b=\mathbb E DF(X_\varepsilon)), (H=\mathbb E D^2F(X_\varepsilon)), and (c=\mathbb E F(X_\varepsilon)). If
\[
K=\begin{pmatrix}0&0&0&1\\0&0&-1&0\\0&-1&0&0\\1&0&0&0\end{pmatrix}
\]
is the Hessian matrix of determinant, the independently reconstructed coefficients are
\[
C=\begin{pmatrix}
\frac14+\frac{\varepsilon^2}{8}&0&0&-\frac14\\
0&\frac14+\frac{\varepsilon^4}{2}&-\frac14&0\\
0&-\frac14&\frac14+\frac{\varepsilon^4}{2}&0\\
-\frac14&0&0&\frac14+\frac{\varepsilon^2}{8}
\end{pmatrix},\qquad H=2KCK,
\]
\[
b=\begin{pmatrix}\varepsilon/4+\varepsilon^4/2\\0\\0\\\varepsilon/4-\varepsilon^4/2\end{pmatrix},\qquad
c=\frac14+\frac{\varepsilon^2}{32}+\frac{9\varepsilon^4}{64}+\frac{\varepsilon^8}{4}.
\]
The eigenvalues of `C` are `ε²/8`, `1/2+ε²/8`, `ε⁴/2`, and `1/2+ε⁴/2`. Thus `H≻0` for `ε>0`. Quartic polarization and `E Xε=0` give the relative energy at background `B` exactly as
\[
J_\varepsilon(B)=\mathbb E[F(B+X_\varepsilon)-F(B)]
=c+b^T B+\frac12B^T H B.
\]
Consequently,
\[
B_\varepsilon^*=-H^{-1}b
=\left(-\frac1\varepsilon-\frac{2\varepsilon^4}{\varepsilon^2+4},\,0,\,0,\,-\frac1\varepsilon+\frac{2\varepsilon^4}{\varepsilon^2+4}\right),
\]
and
\[
\min_B J_\varepsilon(B)
=c-\frac12b^TH^{-1}b
=\frac{\varepsilon^2}{32}+\frac{9\varepsilon^4}{64}
+\frac{\varepsilon^{10}}{4(\varepsilon^2+4)}.
\]
At ε=0, (H_0=2KC_0K\succeq0) has rank two, (b_0=0), and (c_0=1/4), so the exact minimum is (1/4). On the other hand, the trial background (B=-I/\varepsilon) has gap
\[
J_\varepsilon(-I/\varepsilon)=\frac{\varepsilon^2}{32}+\frac{9\varepsilon^4}{64}+\frac{\varepsilon^8}{4},
\]
and the exact difference is
\[
\min_B J_\varepsilon(B)-J_\varepsilon(-I/\varepsilon)
=-\frac{\varepsilon^8}{\varepsilon^2+4}.
\]
Thus the optimized value approaches zero while the fields converge uniformly to the attained ε=0 field, whose optimized value is (1/4). The optimizer diverges like (1/\varepsilon). This distinguishes an attained singular face from a near-singular sequence whose optimizing backgrounds escape; it supplies neither a negative Jensen gap nor a counterexample to quasiconvexity.

## Strict-ROC compactification and residual transfer

For (N(A)=|A|_F^4),
\[
D^2N(A)=8\,\operatorname{vec}(A)\operatorname{vec}(A)^T+4|A|_F^2I.
\]
If (G=F-\delta N) is rank-one convex with (\delta>0), the source one-quadric theorem gives (H_G=\mathbb E D^2G(X)\succeq0) for a determinant-balanced law. Hence, with (C=\mathbb E[\operatorname{vec}X\operatorname{vec}X^T]\),
\[
H_F=H_G+\delta(8C+4m_2I)\succeq4\delta m_2I.
\]
For (m_2>0), this proves strict positive definiteness. If the row-major quartic coefficient vector has ℓ1 norm (K_4), then each degree-four monomial has gradient norm at most (4|x|^3), so
\[
\|b\|\le4K_4\mathbb E|X|^3\le4K_4\sqrt{m_2m_4},\qquad
\|B^*\|\le\|H_F^{-1}\|\|b\|
\le\frac{K_4}{\delta}\sqrt{\frac{m_4}{m_2}}.
\]
These bounds require δ>0, (m_2>0), and finite (m_4); (K_4) is basis-dependent. They deteriorate as the strict ROC margin or (m_2) vanishes and do not compactify the non-strict boundary by themselves.

For the residual bridge, assume `0⪯C⪯H`, `ker C=ker H`, and `b∈ran H`. For arbitrary `v`, set `r=b−Hv`. Then `r∈ran H=ran C`, and direct expansion yields
\[
b^TH^\dagger b=2b^Tv-v^THv+r^TH^\dagger r.
\]
On the common range, `C⪯H` implies `C†⪰H†`: writing `T=H^{-1/2}CH^{-1/2}` there gives `0≺T⪯I`, hence `T^{-1}⪰I` and `C^{-1}=H^{-1/2}T^{-1}H^{-1/2}⪰H^{-1}`. Therefore
\[
c-\frac12\left(2b^Tv-v^THv+r^TC^\dagger r\right)
\le c-\frac12b^TH^\dagger b
\le c-\frac12\left(2b^Tv-v^THv\right).
\]
The inverse-order step is valid only on the shared range; if (b\notin\operatorname{ran}H), the quadratic affine-background objective is unbounded below along a null vector. The lower estimate proves a Jensen inequality only if it is independently shown nonnegative for every gradient under consideration. The assumptions (C\preceq H), common kernel, and that lower-bound sign are not consequences of rank-one convexity alone.

## Fixed-decomposition quantitative bounds

Use the worker note's assumptions: (q(x)=x^TQx) is indefinite on (V); (F) is homogeneous quartic; (D^2F(Z)[R,R]\ge0) for every (Z) whenever (q(R)=0); the law has (\mathbb E q(X)=0), (m_4<\infty); and a fixed direction (A) has one decomposition
\[
Q_A(X)=D^2F(A)[X,X]=P(X)+\lambda q(X),\quad P\succeq0.
\]
Set (U=\ker P), (C_A(X)=DF(X)[A]), and let κ be the operator norm of the symmetric trilinear polarization of (C_A). Quartic reciprocity gives
\[
\delta=A^THA=\mathbb E Q_A(X)=\mathbb E P(X)\ge0.
\]
If (P\ne0) and σ is its least positive eigenvalue, write (\rho=\delta/\sigma). Then
\[
\mathbb E\operatorname{dist}(X,U)^2\le\rho.
\]
The equality-edge argument is sound: for (R\in U\cap\{q=0\}), (t\mapsto D^2F(A+tY)[R,R]\) is nonnegative and zero at (t=0), so its derivative vanishes. This gives (D^2C_A(Y)[R,R]=0). If (q|_U) is indefinite, vanishing on its null cone makes each such restricted quadratic a scalar multiple of (q|_U); symmetry of the cubic tensor forces that scalar to be zero, including when (q|_U) has a radical. Hence (C_A|_U=0). If (q|_U) is semidefinite, the same equality-edge identity holds on its radical (U_0=\ker(q|_U)).

The resulting estimates are:

- If (q|_U) is indefinite,
  \[
  |b\cdot A|\le7\kappa\sqrt{m_4\rho}.
  \]
  The factor 7 follows by expanding the cubic from (u\in U), (v\perp U) and bounding the three terms by (3+3+1). If (P=0), the exact closure gives (C_A\equiv0), stronger than this estimate.
- If (q|_U) is semidefinite and (U_1=U\cap U_0^\perp\ne\{0\}), let (\mu=\min_{u\in U_1,|u|=1}|q(u)|>0) and (s=\mathbb E\operatorname{dist}(X,U_0)^2). Projection, the sign of (q|_{U_1}), and (\mathbb E q(X)=0) yield
  \[
  s\le\rho+\frac{\|Q\|}{\mu}(2\sqrt{m_2\rho}+\rho).
  \]
  If (U_1=0), take (U_0=U) and (s\le\rho). The radical equality identity and cubic expansion give
  \[
  |b\cdot A|\le4\kappa\sqrt{m_4s}.
  \]
  For (0\le\rho\le1), the displayed bound on (s) is at most
  \(\left[1+(\|Q\|/\mu)(1+2\sqrt{m_2})\right]\sqrt\rho\), so the general fourth-moment-only modulus is (O(\rho^{1/4})). If (U_1=0), it improves to (O(\sqrt\rho)).

Under ∞-support bound (|X|\le R_0), the pointwise cubic bounds instead give (7\kappa R_0^2\sqrt\rho) in the indefinite case and (4\kappa R_0s=O(\sqrt\rho)) in the semidefinite case. These estimates control (b\cdot A) for the one fixed decomposition; they do not bound the full Schur remainder, do not give constants uniform as σ or μ degenerates, and do not settle singular limits.

The reduced-law illustration's arithmetic is correct: for (p=\varepsilon^4\le1/16),
\[
m_4-5=p\left[-1+\frac1{2(1-p)}+\frac p{16(1-p)^3}\right].
\]
Both positive terms increase on ((0,1/16]), and their endpoint sum is (1816/3375<1); thus (m_4<5) uniformly. The law has (\delta=\varepsilon^4/[4(1-\varepsilon^4)]), (\mathbb E C_A=\varepsilon), and ratio ( (\mathbb E C_A)^4/\delta=4(1-\varepsilon^4)\to4). But the proposed (C_A=rw^2) has directional derivative (D_A C_A=a_rw^2+2a_wr w), with no (v^2) coefficient, while (P+\lambda q) has (v^2) coefficient 1 for every λ. Thus the tuple cannot be a quartic jet. It is not a sharpness example under full quartic hypotheses, and the law is neither centered nor asserted to be a compatible gradient. The worker note states these scope limits explicitly.

## Reproduction and limits

`DELTA_INDEPENDENT_CHECKS.py` independently expands trigonometric moments from sine/cosine moments, reconstructs (C,b,c,H), checks the exact optimum and trial gap, verifies the quartic-norm Hessian and a symbolic common-range residual identity, and checks the reduced-law arithmetic and its integrability mismatch. It does not import or execute the producer scripts. Its successful output is `DELTA_INDEPENDENT_CHECKS.json`; the run log is `DELTA_CHECKER.log`.

No new prior-literature claim was used in this delta. The existing `PRIMARY_ACCESS_LEDGER.md` remains the literature/access record for the earlier audit. Source hashes and read scope are recorded in `DELTA_READ_LEDGER.md`. External proof review, correctness, and novelty remain UNKNOWN.
