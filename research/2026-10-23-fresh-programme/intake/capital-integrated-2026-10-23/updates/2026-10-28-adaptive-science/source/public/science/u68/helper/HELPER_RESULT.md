# Coupled source derivative: strict obstruction and full-source comparison

2026-10-27. Analytic theorem/counterfamily, followed by an independent audit of the parent's finite five-query correction. The universal polylogarithmic sampler is not proved.

## Results

Under the strict constraint \(\delta_ZJ=u\), every fixed nonzero affine coupling, however small, makes the inverse unbounded on ordinary Gaussian \(L^2\). On total Hermite degree \(n\), its scalar inverse has the sharp order
\[
\|T_n^{-1}\|=\Theta_\lambda((1-\lambda^2)^{-n/2}n^{-2}).
\]
There is no finite-degree resonance. There are bounded smooth periodic residuals for which no square-integrable strict inverse exists. Additional matrix gauge freedom does not remove the obstruction in higher dimensions.

A dimension-free strict inverse exists on a factorially weighted source-Hermite space, or with a precise loss of exponential Hermite radius. Neither regularity bound follows from the universal Lipschitz contract.

The parent-supplied full-source-adjoint gauge is valid and avoids this obstruction while still preserving \(E_Zu=0\). An independent norm calculation below sharpens its bound to
\[
\|J\|_2\le\sqrt3\|R\|_2,\quad
\|D_{(G,Z)}u\|_2\le\|R\|_2,\quad
\|D_Gu\|_2\le\tfrac12\|R\|_2.
\]
This is a larger kernel class than the strict interface, so the two conclusions are consistent.

## 1. Affine reduction and exact inverse

All norms are Gaussian \(L^2\), using Frobenius norms for matrix fields. Gaussian divergence is rowwise; in dimension one \(\delta_Z=Z-\partial_Z\), \(N_Z=\delta_ZD_Z\). Let
\[
0<|\lambda|<1,\quad a=\sqrt{1-\lambda^2},\quad
h(G)=\lambda G,\ K=\lambda I,\ X=\lambda G+aZ,\ J_\psi=aI.
\]
This is globally Lipschitz and conservative. Its actual Stein residual is zero; arbitrary residual tests here concern a proposed general right inverse, not a nonzero defect of this exact affine sampler.

The strict linear operator is
\[
\mathcal L(u,J)=\operatorname{sym}\{\lambda(D_Gu)^T+a(D_Zu)^T+aJ\},
\qquad \delta_ZJ=u.
\tag{1}
\]
In dimension one there is no skew gauge. Substitution gives
\[
TJ=\lambda\delta_ZD_GJ+a(N_Z+2)J,
\tag{2}
\]
because \(D_Z\delta_Z=N_Z+1\).

Let \(e_k=\mathrm{He}_k/\sqrt{k!}\). On total chaos \(n\), use
\(E_q=e_{n-q}(G)e_q(Z)\), \(0\le q\le n\). If \(J=\sum j_qE_q\), \(R=\sum r_qE_q\), equation \(TJ=R\) is
\[
a(q+2)j_q+\lambda\sqrt{(n-q+1)q}\,j_{q-1}=r_q,\qquad j_{-1}=0.
\tag{3}
\]
Every diagonal entry \(a(q+2)>0\): no finite polynomial resonance occurs.

For the unit input \(R=e_n(G)\), the unique solution is exactly
\[
\boxed{j_q=\frac{(-\lambda/a)^q\sqrt{\binom nq}}{a(q+1)(q+2)}.}
\tag{4}
\]
For \(B\sim\operatorname{Bin}(n,\lambda^2)\), this gives
\[
\|J\|_2^2
=a^{-2n-2}E[(B+1)^{-2}(B+2)^{-2}].
\tag{5}
\]
The reciprocal polynomial is convex on \([0,\infty)\). Jensen gives
\[
\boxed{\|T_n^{-1}\|\ge
\frac{a^{-n-1}}{(n\lambda^2+1)(n\lambda^2+2)}.}
\tag{6}
\]
Binomial concentration, including an exponentially small lower tail, gives the exact input asymptotic
\[
\|J\|_2\sim a^{-n-1}/(\lambda^4n^2).
\tag{7}
\]

The correction and both derivatives also grow exponentially:
\[
\begin{aligned}
\|u\|_2^2&=a^{-2n-2}E[(B+1)^{-1}(B+2)^{-2}],\\
\|D_Zu\|_2^2&=a^{-2n-2}E[(B+2)^{-2}],\\
\|D_Gu\|_2^2&=a^{-2n-2}E[(n-B)(B+1)^{-1}(B+2)^{-2}].
\end{aligned}
\tag{8}
\]
Thus, for fixed nonzero \(\lambda\),
\[
\|u\|_2\sim\frac{a^{-n-1}}{|\lambda|^3n^{3/2}},\quad
\|D_Zu\|_2\sim\frac{a^{-n-1}}{\lambda^2n},\quad
\|D_Gu\|_2\sim\frac{a^{-n}}{|\lambda|^3n}.
\tag{9}
\]
The two large derivative terms cancel in (2). Dominant output modes have \(Z\)-degree about \(n\lambda^2\); a small fixed coefficient does not control arbitrarily high source degree.

## 2. Matching upper bound and an inverse between analytic scales

On first-chaos coefficient space, put
\[
B_0=\begin{pmatrix}0&0\\\lambda&a\end{pmatrix},\quad
P=\begin{pmatrix}1&0\\-\lambda/a&0\end{pmatrix},\quad
M_s=sI+(1-s)P.
\]
On total chaos \(n\), (2) is \(d\Gamma(B_0)+2aI\). Direct finite-dimensional exponentiation gives
\[
T_n^{-1}=\frac1a\int_0^1s\,\Gamma_n(M_s)\,ds.
\tag{10}
\]
Here \(\Gamma_n\) is the symmetric tensor power under the normalized Hermite identification. Since \(\|P\|=1/a\),
\[
\|\Gamma_n(M_s)\|=\|M_s\|^n
\le a^{-n}[1-(1-a)s]^n.
\]
Consequently
\[
\boxed{\|T_n^{-1}\|\le a^{-n-1}
\min\{\tfrac12,\ [(1-a)^2(n+1)(n+2)]^{-1}\}.}
\tag{11}
\]
The exact integral factor before relaxation is
\[
\frac{1-(n+2)a^{n+1}+(n+1)a^{n+2}}
{(1-a)^2(n+1)(n+2)}.
\]
Equations (6), (11) prove the sharp \(\Theta_\lambda(a^{-n}n^{-2})\) order.

Define
\[
\|f\|_{\rho,s}^2=\sum_{n\ge0}\rho^{2n}(n+1)^{2s}\|f_n\|_2^2.
\]
Then
\[
\|J\|_{\rho,s+2}\le C_a\|R\|_{\rho/a,s}.
\tag{12}
\]
This is a valid inverse with analytic-radius loss. The exponential rate \(1/a\) is necessary by (6). No common weight depending only on total degree can make the inverse bounded on that same weighted space, because input and output lie in the same block and the weight cancels. Finite Sobolev changes supply only powers of \(n\) and cannot repair the obstruction.

## 3. A bounded smooth residual with no strict \(L^2\) inverse

Take
\[
R(G)=\sum_{k=1}^\infty e^{-k}\cos(kG)
=\operatorname{Re}\frac{e^{-1+iG}}{1-e^{-1+iG}}.
\tag{13}
\]
It is bounded, periodic, real analytic in a strip, and has bounded derivatives of every finite order. Subtracting its Gaussian mean or rescaling to Lipschitz constant one leaves the following conclusion unchanged.

Its even normalized Hermite coefficients are
\[
r_n=\frac{(-1)^{n/2}}{\sqrt{n!}}
\sum_{k\ge1}e^{-k-k^2/2}k^n.
\tag{14}
\]
All summands have the same sign. For even \(k\), let \(n=k^2\); Stirling gives
\[
|r_{k^2}|\ge c e^{-k}(k^2)^{-1/4}.
\]
Projecting any weak solution onto chaos \(n\) forces the unique solution of (3). Even the weaker lower bound with denominator \((n+1)(n+2)\) gives
\[
\|J_{k^2}\|_2\ge c_a a^{-k^2}e^{-k}k^{-9/2}\longrightarrow\infty.
\]
Therefore no strict \(L^2\) solution exists, for every fixed nonzero \(\lambda\). This is stronger than the failure of a uniform bound on finite polynomials.

## 4. Higher-dimensional symmetrization cannot evade the lower bound

For any \(d\), retain \(K=\lambda I\) and choose
\(R=e_n(G_1)e_1e_1^T\). Average the \((1,1)\) equation over all variables except \(G_1,Z_1\). A diagonal entry is unchanged by symmetrization. Gaussian integration kills all auxiliary divergences \(\delta_{Z_k}J_{1k}\), \(k\ne1\). The averaged fields satisfy
\[
\bar u_1=\delta_{Z_1}\bar J_{11},\quad
\lambda D_{G_1}\bar u_1+aD_{Z_1}\bar u_1+a\bar J_{11}=e_n(G_1).
\]
Conditional expectation contracts \(L^2\), so every matrix solution obeys
\(\|J\|_2\ge\|\bar J_{11}\|_2\), with lower bound (6). Matrix skew/divergence-free freedom cannot remove this obstruction.

## 5. A genuine strict inverse in a stronger source space

Decompose into source degree \(p\) and noise degree \(m\), and define
\[
\|f\|_\theta^2=\sum_{p,m\ge0}p!\theta^{2p}\|f_{p,m}\|_2^2.
\tag{15}
\]
For tensor fields use Frobenius norms. Exact Hermite differentiation gives
\(\|D_Gf\|_\theta\le\theta^{-1}\|f\|_\theta\), dimension-independently.

Let \(H=(H_u,H_J)\) be the sign-adjusted frozen S3 §17 baseline inverse:
\[
\delta_ZH_JR=H_uR,\qquad
\operatorname{sym}[H_JR+(D_ZH_uR)^T]=R.
\]
S3 §18 implies
\[
\|H_uR\|_\theta\le\tfrac12\|R\|_\theta,\quad
\|D_ZH_uR\|_\theta\le\|R\|_\theta,\quad
\|H_JR\|_\theta\le(2+\sqrt2)\|R\|_\theta.
\tag{16}
\]
The first constant follows by maximizing \(\sqrt{m+1}/(m+2)\). The map acts only in \(Z\), so it preserves source weights.

Set \(AR=\operatorname{sym}[D_G(H_uR)^T]\), so \(\|A\|\le1/(2\theta)\). If
\[
\eta=|\lambda|/(2a\theta)<1,
\]
then
\[
W=a^{-1}\sum_{k\ge0}(-\lambda A/a)^kR,\quad
u=H_uW,\quad J=H_JW
\tag{17}
\]
solves (1) with right side \(R\), and
\[
\|u\|_\theta\le\frac{\|R\|_\theta}{2a(1-\eta)},\
\|D_Zu\|_\theta\le\frac{\|R\|_\theta}{a(1-\eta)},\
\|J\|_\theta\le\frac{(2+\sqrt2)\|R\|_\theta}{a(1-\eta)}.
\]
Also \(\|D_Gu\|_\theta\le\|R\|_\theta/[2a\theta(1-\eta)]\).
This is a legitimate dimension- and degree-independent strict inverse. For finite source polynomials the series terminates.

This source space is much stronger than the target input contract. The smooth conservative function \(h_b(G)=\sin(bG)/b\) has \(\|h_b'\|_\infty\le1\), but
\[
\|h_b\|_\theta^2=b^{-2}e^{-b^2}
\sum_{p\ {\rm odd}}(\theta^2b^2)^p
\]
diverges when \(\theta|b|\ge1\). A global Lipschitz constant does not supply a fixed \(\theta\).

## 6. Orthogonal re-expansion is not a strict cure

Let \(S=\lambda G+aZ,\ T=aG-\lambda Z\). Then \(S,T\) are independent standard Gaussians and
\[
\lambda D_G+aD_Z=D_S,\qquad
\delta_Z=a\delta_S-\lambda\delta_T.
\]
The strict operator becomes
\[
TJ=a(N_S+2)J-\lambda\delta_TD_SJ.
\tag{18}
\]
The coupling moves to the auxiliary variable. Orthogonal re-expansion is unitary on every chaos and cannot change the singular values in (6).

Allowing a full source-divergence kernel changes this conclusion. An ordinary Hodge inverse along \(S\) preserves the unconditional mean, but generally fails original conditional centering: for \(R=1\), \(u=-S/2\) has \(E_Zu=-\lambda G/2\). The parent-supplied gauge below does better and preserves the conditional mean as well.

## 7. Independent audit of the parent-supplied full-source-adjoint gauge

Now permit \(J=(J_G,J_Z)\) with
\(\delta_GJ_G+\delta_ZJ_Z=u\). For symmetric \(R\) of pure bidegree \((n,m)\), \(N=n+m\), define
\[
s=\delta_Z\delta_ZR,\quad
u=-D_Zs/[(m+2)(N+2)],
\]
\[
w=\delta_ZR-D_Zs/(m+2),\quad
B=[D_Zw-(D_Zw)^T]/(m+2),
\]
\[
J_G=-D_Gu,\qquad J_Z=-R-(D_Zu)^T+B.
\tag{19}
\]
Here \(D_Zu\) is symmetric. Frozen S3's Gaussian identities give
\[
\delta_Zw=0,\quad\delta_ZB=w,\quad
\delta_Zu=-s/(N+2),\quad
\delta_GJ_G=-nu,\quad\delta_ZJ_Z=(n+1)u.
\]
Thus
\[
\delta_{(G,Z)}J=u,\qquad
\operatorname{sym}[J_Z+(D_Zu)^T]=-R.
\tag{20}
\]
Both \(u,J_G\) have \(Z\)-degree \(m+1\), hence \(E_Zu=E_ZJ_G=0\).

### Sharpened norm calculation

Write \(S_2=\|s\|_2^2,D_2=\|\delta_ZR\|_2^2\), \(c=[(m+2)(N+2)]^{-1}\). Then
\[
D_2\le(m+1)\|R\|_2^2,\quad
S_2\le(m+1)(m+2)\|R\|_2^2.
\]
Creation/annihilation gives
\[
\|u\|_2\le\tfrac12\|R\|_2,\quad
\|D_{(G,Z)}u\|_2\le\|R\|_2,\quad
\|D_Gu\|_2\le\tfrac12\|R\|_2.
\tag{21}
\]
For the combined kernel use orthogonality of symmetric \(R+D_Zu\) and skew \(B\), together with
\[
\langle R,D_Zu\rangle=-cS_2,\quad
\|D_Zu\|_2^2=(m+1)(m+2)c^2S_2,\quad
\|J_G\|_2^2=n(m+2)c^2S_2,
\]
\[
\|B\|_2^2=2D_2/(m+2)-2S_2/(m+2)^2.
\]
Combining exactly,
\[
\boxed{\|J\|_2^2=\|R\|_2^2+\frac{2D_2}{m+2}
-\left[\frac2{(m+2)^2}+
\frac{N+3}{(m+2)(N+2)^2}\right]S_2
\le3\|R\|_2^2.}
\tag{22}
\]
The bidegree maps for every output slot are injective, so orthogonality extends these estimates to sums.

For general \(L^2\) residuals, polynomial approximants give \(J_k\to J\), \(u_k\to u\), and \(Du_k\to Du\) in \(L^2\). The single joint divergence \(\delta_{(G,Z)}\) is closed and \(\delta J_k=u_k\), so \(\delta J=u\). This does not assert separate \(L^2\) divergence domains for \(J_G,J_Z\), which may fail after summing. Conditional expectation is bounded and preserves \(E_Zu=E_ZJ_G=0\) in the limit.

### Affine cancellation and a perturbed coefficient gate

At the affine model, the full operator is
\[
\mathcal L_X=\operatorname{sym}\{
\lambda(D_Gu)^T+a(D_Zu)^T+\lambda J_G+aJ_Z\}.
\]
Since \(J_G=-D_Gu\), its source part cancels after symmetrization and
\[
\mathcal L_X(u,J)=-aR.
\tag{23}
\]
Apply (19) to \(R/a\) for a dimension-free full-source inverse of right side \(-R\), for every fixed \(|\lambda|<1\). Unlike the strict inverse, it has no degree-dependent amplification.

For general \(M=(M_G,M_Z)\) with \(\delta M=X-\mu\), the source contribution becomes
\[
\operatorname{sym}[(M_G-D_GX)(D_Gu)^T].
\]
This identity needs no symmetry assumption on \(M_G,D_GX\). Consequently the residual perturbation operator has ordinary \(L^2\) norm at most
\[
\boxed{\theta=
\tfrac12\|M_G-D_GX\|_{\infty,\mathrm{op}}
+\|M_Z-I\|_{\infty,\mathrm{op}}
+\sqrt3\|D_ZX-I\|_{\infty,\mathrm{op}}.}
\tag{24}
\]
If \(\theta<1\), a Neumann series gives the full-source right inverse, with bounds (21)–(22) divided by \(1-\theta\), still conditionally centered.

For raw globally \(\lambda\)-Lipschitz \(h\), \(X=h(G)+Z\), the canonical Stein resolvent has \(\|K\|_{\infty,\mathrm{op}}\le\lambda\) and \(\|Dh\|_{\infty,\mathrm{op}}\le\lambda\) almost everywhere. Thus \(\theta\le\lambda<1\). The parent's claim that the initial linearization admits this full-source \(L^2\) inverse is correct without higher derivatives.

For later nonlinear iterates, coefficient boundedness is an additional hypothesis. A field \(D_G[A(G)Z]\), for example, can be unbounded in \(Z\).

## 8. Audit of the parent's one-step residual and reserve-TV argument

For the exact update \(Y=X+u,M_Y=M+J\), closed joint divergence and the Gaussian Sobolev chain rule give the Stein identity with preconditioned matrix \(M_Y(DY)^T\). If the linear equation is solved, the residual is exactly \(\operatorname{sym}[J(Du)^T]\).

The strengthened bounds above imply the one-step estimate
\[
E\|\operatorname{sym}[J(Du)^T]\|_F
\le\sqrt3\,\|R\|_2^2/(1-\theta)^2.
\tag{25}
\]
This is an \(L^1\) estimate. It does not give another \(L^2\) residual or preserve the next coefficient gate.

The parent's reserve-TV proof is valid. If \(Q\) is an integrable symmetric Stein residual for \(Y\), \(V\) is independent standard Gaussian and \(\eta>0\), then
\[
\operatorname{TV}(\mathcal L(Y+\eta V),N(\mu,(1+\eta^2)I))
\le\frac{\sqrt2}{2}\log(1+\eta^{-2})E\|Q\|_F.
\tag{26}
\]
Indeed \(P_t(P_{\eta^2}1_A)\) has convolution variance \(1-e^{-2t}+\eta^2\). Hermite Bessel gives a dimension-free Frobenius Hessian bound \(\sqrt2 e^{-2t}/(1-e^{-2t}+\eta^2)\); integrating is exactly \((\sqrt2/2)\log(1+\eta^{-2})\). The stated constant is conservative: centering the indicator gives \(\sqrt{\operatorname{Var}(1_A)}\le1/2\), permitting a further factor \(1/2\). No improvement is needed for validity. The reserve variance remains charged to the target.

## 9. Reproducibility

Owned code: affine_hermite_check.py. It uses only the standard library.

~~~
Public script reference (not an executed invocation): research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-28-adaptive-science/source/originals/science/u68/helper/affine_hermite_check.py
~~~

At \(\lambda=3/5,a=4/5\), exact rational checks pass at degrees \(0,1,2,5,10,25,50,100\). They verify (3)–(5) and the scalar full-source-adjoint identities in every bidegree. Log-sums evaluate (5), (8), and test (6), (11), through degree 10000. Full output: affine_hermite_results.json.

The independent owned joint_gauge_check.py additionally passed 180 exact rational two-dimensional checks: source/noise bidegrees \(0,\ldots,5\), with five deterministic coefficient seeds each. It verifies the full divergence and symmetric inverse identities, the exact combined norm formula (22), and each inequality (21). The largest observed \(\|J\|_2^2/\|R\|_2^2\) was 1.275670746587; the theorem uses the proved bound 3, not that finite diagnostic.

| \(\lambda\) | \(n\) | \(\log_{10}\|J\|_2\) | \(\log_{10}\|u\|_2\) | \(\log_{10}\|D_Zu\|_2\) |
|---:|---:|---:|---:|---:|
| 0.1 | 1000 | 0.310390 | 0.708888 | 1.157982 |
| 0.1 | 10000 | 17.834901 | 18.828283 | 19.823940 |
| 0.3 | 1000 | 16.599012 | 17.569562 | 18.542443 |
| 0.6 | 100 | 6.678591 | 7.446627 | 8.219041 |
| 0.6 | 1000 | 91.894567 | 93.171771 | 94.449366 |

## Scope and remaining obligations

The strict source/noise split is decisively obstructed in ordinary \(L^2\). A different full-source kernel validly removes that analytic obstruction. This is not a target lower bound and not a sampler.

Sections 1–8 do not supply a source-value implementation of the joint fields, derivatives, full Hodge inverse or Neumann factors. The subsequent audit in section 10 validates a particular five-query correction at its stated dimension-dependent full-law bound. No reusable product-integrability theorem for Newton iterations, subcritical forest, or every-execution polylog query cap follows.

Frozen scientific sources used: S3_r21_polylog_mean_compiler.txt §§16–18 and, for section 10, S4_r22_polylog_mean_factory.txt §§9–11. Parent science additionally audited: JOINT_GAUGE_THEOREM.md, FIVE_QUERY_POSITIVE_CORRECTION.md and the parent-supplied full-source-adjoint equations. No memory, external research, other trajectory, shared edit, or claimed novelty was used.

## 10. Urgent independent audit: legal five-query positive correction

**Verdict: the parent's five-query program, theorem (1), normalization and exact covariance receipt are valid as written**, under its stated independence and conservative Lipschitz hypotheses. No substantive flaw was found. This is a positive finite value-query program with a valid implemented-law bound. The stated fixed-ratio, unbounded-dimension polylog target remains open.

### Exact program and query count

Write \(0<a<1,b=\sqrt{1-a^2}\), and use
\[
h_b(y)=E g(by+aH),\quad
K_b(y)=\int_0^bE Dg(\rho y+\sqrt{1-\rho^2}H)\,d\rho,\quad
\Gamma_b=\operatorname{sym}[K_b(Dh_b)^T].
\]
Then \(\delta_GK_b=h_b-\mu\), \(\|K_b\|_{\mathrm{op}},\|Dh_b\|_{\mathrm{op}}\le b\lambda\), and \(\|\Gamma_b\|_{\mathrm{op}}\le b^2\lambda^2\).

Frozen S4 §§9–11 supplies exactly the required two-value factories, not a common random matrix. At a conditionally fixed center \(c\), compose independent \(K_b\) and \(Dh_b\) actions in either order with a fresh fair coin. Symmetry of their mean operators, which follows from conservativity, gives
\[
E[W_\Gamma(c;v)\mid c,v]=\Gamma_b(c)v,\qquad
\|W_\Gamma(c;v)\|\le b^2\lambda^2\|v\|.
\]
Two actions cost four original \(g\)-value queries. The source value \(g(bG+aH)\) costs one more. There is no retry or random query-length schedule. Zero-vector/radius branches only reduce this count, so the every-execution cap is five. The arithmetic and Gaussian storage are \(O(d)\).

Draw \(T\) with density \(2t\), let \(C=TG+\sqrt{1-T^2}W\), and return
\[
Y_{\rm impl}=g(bG+aH)+Z-\tfrac12W_\Gamma(C;Z)+\eta V.
\]
All action seeds, the source seed \(H\), and reserve \(V\) must have exactly the independence stated by the parent.

### Conditional mean and the deterministic Stein comparison

With \(F=(N_G+2)^{-1}\Gamma_b=\int_0^1tP_t\Gamma_b\,dt\), the density \(2t\) and factor \(-1/2\) give exactly
\[
E[U_{\rm corr}\mid G,Z]=-F(G)Z=u(G,Z).
\]
There is no missing factor \(2\), \(b\), or \(a\). For a source-only residual of degree \(n\), section 7 gives
\[
u_n=-\Gamma_{b,n}Z/(n+2).
\]
For \(X=h_b(G)+Z\), its initial residual is \(\Gamma_b\), and the deterministic correction has residual
\[
\operatorname{sym}[(K_b-Dh_b)(D_Gu)^T]
+\operatorname{sym}[J(Du)^T].
\]
The parent's bounds
\[
E\|Q_{\rm lin}\|_F\le b^3\lambda^3\sqrt d,\qquad
E\|Q_{\rm quad}\|_F\le\sqrt3\,b^4\lambda^4d
\]
follow from \(\|K_b-Dh_b\|_{\infty,\mathrm{op}}\le2b\lambda\) and
\(\|\Gamma_b\|_2\le b^2\lambda^2\sqrt d\). The reserve-TV theorem applies to their sum. No Neumann solve or smallness hypothesis is required for this single baseline correction.

### Actual random action: conditional Taylor comparison

Set \(\Delta=U_{\rm corr}-u\). Given \(G,Z\), \(X+u\) is fixed and \(E[\Delta\mid G,Z]=0\). Thus Taylor expansion of
\(f_\eta(x)=P(x+\eta V\in A)\) has zero expected linear term. Its uniformly bounded Hessian gives
\[
\left|E f_\eta(X+U_{\rm corr})-E f_\eta(X+u)\right|
\le\frac{\sqrt2}{2\eta^2}E\|\Delta\|^2
\le\frac{\sqrt2\,b^4\lambda^4d}{8\eta^2}.
\]
The final inequality uses conditional expectation as an orthogonal projection and the every-execution action bound. This is a full indicator-test argument and does charge the nonlinear randomization law, including covariance and higher cumulants.

### Actual source value: reserve comparison

For \(E_{\rm src}=g(bG+aH)-h_b(G)\), conditional Gaussian Poincare gives
\[
E\|E_{\rm src}\|^2\le a^2\lambda^2d.
\]
Couple all non-reserve seeds and apply the equal-covariance Gaussian Pinsker bound to the independent \(\eta V\) convolution:
\[
\operatorname{TV}\le E\|E_{\rm src}\|/(2\eta)
\le a\lambda\sqrt d/(2\eta).
\]
Combining these three comparisons is exactly parent theorem (1). The source contribution is not silently removed using its zero conditional mean.

### Covariance cross terms

The mean is exactly \(\mu\): \(bG+aH\) is standard Gaussian and \(E[U_{\rm corr}\mid G]=0\).

Conditionally on \(G\), the source error is centered and independent of all action/noise seeds. Therefore its cross-covariances with \(h_b(G)\), \(Z\), and \(U_{\rm corr}\) vanish. Also \(E[U_{\rm corr}\mid G]=0\) kills its cross term with \(h_b(G)\). Since \(C\) is independent of fresh \(Z\),
\[
E[ZU_{\rm corr}^T]=-\tfrac12E\Gamma_b(C)
=-\tfrac12E\Gamma_b(G).
\]
The Stein identity gives \(\operatorname{Cov}(h_b)=E\Gamma_b\), so these cross terms cancel exactly. Hence
\[
\operatorname{Cov}(Y_{\rm impl})
=(1+\eta^2)I+E\operatorname{Cov}(g(bG+aH)\mid G)
+E[U_{\rm corr}U_{\rm corr}^T].
\]
For every projection \(w\), conditional Poincare gives source covariance at most \(a^2\lambda^2\|w\|^2\). The frozen fixed-center fresh-word convex-order theorem is applicable: condition on \(C\), which is independent of the fresh Gaussian input \(Z\), then compose the fresh actions at that same center. Thus
\[
E[U_{\rm corr}U_{\rm corr}^T]\preceq b^4\lambda^4I/4.
\]
This proves the parent's exact receipt
\[
0\preceq\operatorname{Cov}(Y_{\rm impl})-(1+\eta^2)I
\preceq(a^2\lambda^2+b^4\lambda^4/4)I.
\]
This receipt would not follow from the mere vector norm bound; the fixed-center convex-order input is essential and its independence is satisfied here.

### Normalization and exact affine full-law check

For physical target variance \(\sigma^2\), use normalized source \(g/\tau\), \(\tau=\sigma/\sqrt{1+\eta^2}\), and multiply the output by \(\tau\). Then the target mean and covariance are exactly \(\mu,\sigma^2I\), with normalized Lipschitz constant \(L/\tau\).

For \(g(x)=c+Bx\), \(B=B^T\), both value factories become deterministic matrix actions. Therefore the implemented law is exactly
\[
N\!\left(c,\ (1+\eta^2)I+a^2B^2+\tfrac14b^4B^4\right).
\]
This is a full-law affine sanity check of all signs and normalizations, not an inference from moment matching.

### Optional sharper constants and comparator boundary

For source-only residuals one can sharpen the Hodge constants:
\[
\|D_Gu\|_2\le\|\Gamma_b\|_2/(2\sqrt2),\quad
\|Du\|_2\le\|\Gamma_b\|_2/2,\quad
\|J\|_2\le\|\Gamma_b\|_2.
\]
Indeed the squared multipliers on source chaos \(n\) are respectively
\[
\frac n{(n+2)^2},\quad \frac{n+1}{(n+2)^2},\quad
\frac{n^2+3n+1}{(n+2)^2}.
\]
Thus the deterministic term in parent theorem (1) may be replaced by
\[
C_\eta\left[b^3\lambda^3\sqrt d/\sqrt2
+\tfrac12b^4\lambda^4d\right].
\]
The stated parent bound remains valid without this improvement.

An affine diagnostic does not establish comparator advantage: the ordinary two-query antithetic average \([g(G)+g(-G)]/2\) recovers the exact mean for affine \(g\), followed by fresh target Gaussian noise. The five-query construction's valid claim is a dimension-dependent universal implemented-law bound and improved small-\(\lambda\) powers against the stated independent-average comparison, not a general dominance or completed iteration.
