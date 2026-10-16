# A homogeneous nonseparable tube around the separated first-potential space

Date: 2026-10-16. Status: internally derived, unreviewed. The unchanged integrand is retained. Historical originality, external correctness, and hardware implications are UNKNOWN. The theorem below is restricted; unrestricted conformal quasiconvexity remains open.

## 1. Contract and statement

All functions are real and periodic on the square torus, with normalized averages and norms. Write

\[
V=D(f,g)=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
u=a^2+c^2,\quad v=b^2+d^2,\quad j=ad-bc,
\]
\[
J_r(V)=\frac{3r}{8(r+2)}(u+v-2j)^2+
\frac{r(r-1)}6u^2+j^2+ruj,\qquad r>0.
\]

The canonical separated part of a scalar potential is

\[
\Pi f(x,y)=\langle f(x,\cdot)\rangle_y+
\langle f(\cdot,y)\rangle_x-\langle f\rangle.
\]

Put \(f_0=\Pi f=F(x)+H(y)\), \(\eta=f-f_0\),
\(R=\|Df_0\|_4\), and \(\varepsilon=\|D\eta\|_4\).
Thus both coordinate averages of \(\eta\) vanish; its Fourier support has \(mn\ne0\).

**Theorem.** For each \(r>0\), the explicit constant \(\delta_r>0\) in Section 2 has the following property. If \(R>0\) and

\[
\varepsilon\le\delta_r R,
\tag{1}
\]

then, for every periodic \(g\in W^{1,4}\) and every real \(s\),

\[
E_r(f,g,s):=\langle J_r(sI+D(f,g))\rangle-J_r(sI)
\ge\frac\alpha2(R^4+\|Dg_0\|_4^4)+\frac\mu2s^2\mathcal A(f,g)>0,
\tag{2}
\]

where \(g_0=g+p\), the compatible scalar correction \(p\) is defined in Section 4, and

\[
\mathcal A(f,g)=\langle((r+1)f_x+g_y)^2+\kappa g_x^2\rangle.
\]

The strict sign in (2) uses \(R>0\). No condition \(\|F'\|_2>0\) is needed. In particular, every nonconstant \(H(y)\) has a nonseparable all-background neighborhood. The constant depends only on \(r\), not on the profiles, their concentration, amplitudes, Fourier bandwidth, or \(g,s\).

**Actual open-ball corollary.** Let \(h_0=F(x)+H(y)\) be any nonconstant separated potential. Every \(f\) satisfying

\[
\|D(f-h_0)\|_4\le\frac{\delta_r}{5}\|Dh_0\|_4
\tag{3}
\]

satisfies the theorem. Indeed, \(\|D\Pi\zeta\|_4\le2\|D\zeta\|_4\) by coordinate Jensen and the triangle inequality. Hence \(\|D(I-\Pi)\zeta\|_4\le3\|D\zeta\|_4\), and \(\|D\Pi f\|_4\ge\|Dh_0\|_4-2\|D\zeta\|_4\). Since \(\delta_r\le1\), (3) implies (1).

The center \(h_0\) cannot be constant in this argument: then its quartic reserve vanishes. No neighborhood of the zero potential is asserted.

## 2. Explicit, deliberately conservative constants

Set

\[
\kappa=\frac{r(r+2)}3,\quad
\alpha=\frac{5r}{4096(r+2)},\quad
\beta=\frac r{512(r+2)},\quad
K_0=\max\{2(r+1)^2,\kappa\},\quad \mu=\beta/K_0.
\]
\[
L=3(r+1)\left(1+\frac1{2\sqrt\kappa}\right),\quad
D=1+L,\quad L_c=L,\quad L_e=r+1+L,\quad
C_a=\frac{\max\{1,\kappa^{-1/2}\}}{r+1}.
\]
\[
C_t=4+\sqrt\kappa+2rL_c+\frac{rL_e}{\sqrt\kappa},
\]
\[
C_R=2(r+1)+4L_e+2(r+2)+2L_c+
\frac{2L_e}{\sqrt\kappa}+2\sqrt\kappa L_c,
\]
\[
C_\varepsilon=2L_e+(r+2)+rL_c^2+2L_c+
\kappa\left(\frac3{r+1}+11C_a\right)+\sqrt\kappa L_c,
\qquad C_P=\max\{C_t,C_R,C_\varepsilon\},
\]
\[
L_J=\frac{6r}{r+2}+\frac23r(r+1)+1+2r,
\]
\[
\boxed{\delta_r=\min\left\{1,\frac1D,
\frac\alpha{256L_JD},\frac{\sqrt{\alpha\mu}}{8C_P}\right\}.}
\tag{4}
\]

All constants are strictly positive and finite for every fixed \(r>0\). They are not optimized. On any compact interval of positive \(r\), they give a uniform positive radius. At \(r=1\), the simpler rational choice \(\delta=1/40{,}000{,}000\) satisfies every condition in (4); its verification is exact.

## 3. The inherited separated reserve and exact acoustic expansion

The all-positive-parameter separated theorem at the assigned Astra pin proves

\[
E_r(F+H,g,s)\ge\alpha\langle|D(F+H,g)|^4\rangle+
\beta s^2\langle|F'|^2+|Dg|^2\rangle.
\tag{5}
\]

Its independent rational Gram certificate is supplied in `originals/stability/certificate.json`. The new checker reconstructs the polynomial identity and positive pivots from that data; it executes no producer program.

Compatibility gives \(\langle j\rangle=0\), so the exact conformal expansion is

\[
E_r(f,g,s)=s^2\mathcal A(f,g)+s\mathcal P(f,g)+\mathcal Q(f,g),
\tag{6}
\]
\[
\mathcal Q=\langle J_r(V)\rangle,\qquad
\mathcal P=\langle P(V)\rangle,
\]
\[
P(V)=r\left[d+\frac{2r+1}{3}a\right](a^2+c^2)+2j((r+1)a+d).
\]

With \(U=(r+1)a+d\), this is equivalently

\[
\boxed{P=2aU^2-(r+2)a^2U+rc^2U-2bcU-\kappa a^3-\kappa ac^2.}
\tag{7}
\]

Every term in (7) except \(a^3\) has an acoustic factor \(U\) or \(c\). The following lemma controls the remaining term with a finite explicit constant. It is an explicit receiving proof of a qualitative estimate already implied by Astra N885 at \(m=3,p=2,s=4,\alpha=1\); no new generic compensation theorem is claimed.

## 4. Compatible acoustic projection, without loss in the quadratic form

Define the mean-zero real scalar \(p\) by its Fourier coefficients

\[
\widehat p(m,n)=\frac{(r+1)mn}{n^2+\kappa m^2}\widehat\eta(m,n)
\quad ((m,n)\ne(0,0));\qquad \widehat p(0,0)=0.
\tag{8}
\]

Let \(g_0=g+p\), \(a_0=F'(x)\), \(b_0=H'(y)\),
\(A=\eta_x\), \(B=\eta_y\), \(c_0=(g_0)_x\),
\(d_0=(g_0)_y\), \(U_0=(r+1)a_0+d_0\), and

\[
k=p_x,\qquad e=(r+1)A-p_y.
\]

Then \(a=a_0+A\), \(b=b_0+B\), \(c=c_0-k\), and \(U=U_0+e\).
The identity \(\partial_y e-\kappa\partial_x k=0\) gives
\(\langle d_0e-\kappa c_0k\rangle=0\). Also
\(\langle a_0e\rangle=0\), because \(e\) has zero average in \(y\).
Consequently

\[
\boxed{\mathcal A(f,g)=\mathcal A(f_0,g_0)+\mathcal R(\eta)},
\qquad \mathcal R=\langle e^2+\kappa k^2\rangle\ge0.
\tag{9}
\]

In Fourier form,

\[
\mathcal R=(r+1)^2\sum_{m,n}
\frac{\kappa m^2}{n^2+\kappa m^2}|\widehat A(m,n)|^2.
\tag{10}
\]

Let \(R_x\) denote the multiplier \(im/\sqrt{m^2+n^2}\), with value zero at the origin. Then

\[
\|R_xA\|_2\le C_a\sqrt{\mathcal R}.
\tag{11}
\]

The only external analytic input is the classical second-order Riesz bound on a flat torus with any positive constant metric: at \(p=4\), the operator with multiplier \(\xi^TM\xi/|\xi|^2\) has norm at most \(3\|M\|\). This is Theorem 4.1(i) of [Bañuelos–Baudoin, arXiv:1109.5751](https://arxiv.org/pdf/1109.5751), applied to the abelian compact Lie group with vector fields \(\sqrt\kappa\partial_x,\partial_y\). Diagonal and cross choices give, respectively,

\[
\|p_y\|_4\le3(r+1)\varepsilon,\qquad
\|p_x\|_4\le\frac{3(r+1)}{2\sqrt\kappa}\varepsilon.
\]

Thus \(\|Dp\|_4\le L\varepsilon\), \(\|k\|_4\le L_c\varepsilon\), \(\|e\|_4\le L_e\varepsilon\), and \(p,g_0\in W^{1,4}\).

Write \(q=\sqrt{\mathcal A(f,g)}\), \(t=\|Dg_0\|_4\). The projection gives

\[
\|U\|_2,\|U_0\|_2\le q,\qquad
\|c\|_2,\|c_0\|_2\le q/\sqrt\kappa,\qquad
\|a_0\|_2\le q/(r+1).
\tag{12}
\]

For the last inequality, the horizontal Fourier modes of \(U_0\) equal \((r+1)a_0\), because \(d_0\) has none; (9) then applies. Also

\[
\|U\|_4\le(r+1)R+t+L_e\varepsilon,\qquad
\|c\|_4\le t+L_c\varepsilon.
\tag{13}
\]

## 5. An explicit cubic estimate, with all frequencies admitted

For every periodic scalar \(\eta\in W^{1,4}\),

\[
\boxed{\langle|\eta_x|^3\rangle\le
11\|R_x\eta_x\|_2\|D\eta\|_4^2.}
\tag{14}
\]

Here is a full proof. Put \(A=\eta_x\), \(B=\eta_y\), \(q_*=\|R_xA\|_2\), and for \(0<\tau\le1\) define

\[
\widehat A_\tau(m,n)=\frac{\tau^2n^2}{m^2+\tau^2n^2}\widehat A(m,n).
\]

The gradient identity gives \(A_\tau=\tau T_\tau B\), where \(T_\tau\) has multiplier \(\tau mn/(m^2+\tau^2n^2)\). The same classical Riesz bound, now with vector fields \(\partial_x,\tau\partial_y\) and the cross matrix of norm \(1/2\), gives

\[
\|A_\tau\|_4\le K\tau\|B\|_4,\qquad K=3/2.
\tag{15}
\]

Plancherel gives \(\|A-A_1\|_2\le q_*\). It also gives

\[
\|A_\tau-A_{\tau/2}\|_2\le\frac{3}{4\tau}q_*.
\tag{16}
\]

To verify (16), put \(v=|m|/(\tau|n|)\). The ratio of the difference multiplier to \(|m|/\sqrt{m^2+n^2}\) is

\[
\frac{3v\sqrt{1+\tau^2v^2}}{\tau(v^2+1)(4v^2+1)}
\le\frac{3v}{\tau\sqrt{v^2+1}(4v^2+1)}
\le\frac3{4\tau},
\]

using \(4v/(4v^2+1)\le1\). Coordinate-axis modes are checked by continuity or directly; the difference is zero there.

For real \(X,Y\),
\(\big||X|^3-|Y|^3\big|\le|X-Y|(X^2+|X||Y|+Y^2)\).
Apply Hölder to telescope from \(A\) to \(A_1\) and then through \(A_{2^{-j}}\). The first difference is at most
\((1+K+K^2)q_*\|D\eta\|_4^2\).
The difference at scale \(\tau=2^{-j}\) is at most
\((21K^2/16)\tau q_*\|D\eta\|_4^2\).
The terminal term tends to zero by (15), and \(\sum_{j\ge0}2^{-j}=2\). Therefore the total constant is

\[
1+K+K^2+\frac{21K^2}8=\frac{341}{32}<11.
\]

This proves (14), including absolute values, without a frequency cutoff.

For the present canonical split, \(\langle a_0^2A\rangle=0\). Thus

\[
|\langle a^3-a_0^3\rangle|
\le3\|a_0\|_2\|A\|_4^2+\langle|A|^3\rangle
\le\left(\frac3{r+1}+11C_a\right)q\varepsilon^2.
\tag{17}
\]

## 6. Cubic and quartic perturbation estimates

Put \(\mathcal P_0=\mathcal P(f_0,g_0)\), \(\mathcal Q_0=\mathcal Q(f_0,g_0)\). From (7), (12)–(13), Hölder, and (17),

\[
\boxed{|\mathcal P-\mathcal P_0|\le
C_P\varepsilon q(R+t+\varepsilon).}
\tag{18}
\]

For explicit reproducibility, the six terms in (7), in order, contribute at most the following coefficients to \(\varepsilon q(R,t,\varepsilon)\):

| term | coefficient of R | coefficient of t | coefficient of epsilon |
|---|---:|---:|---:|
| \(2aU^2\) | \(2(r+1)+4L_e\) | 2 | \(2L_e\) |
| \(-(r+2)a^2U\) | \(2(r+2)\) | 0 | \(r+2\) |
| \(rc^2U\) | 0 | \(2rL_c+rL_e/\sqrt\kappa\) | \(rL_c^2\) |
| \(-2bcU\) | \(2L_c+2L_e/\sqrt\kappa\) | 2 | \(2L_c\) |
| \(-\kappa a^3\) | 0 | 0 | \(\kappa(3/(r+1)+11C_a)\) |
| \(-\kappa ac^2\) | \(2\sqrt\kappa L_c\) | \(\sqrt\kappa\) | \(\sqrt\kappa L_c\) |

For the second row of the table, expand
\(a^2U-a_0^2U_0=A(a+a_0)U+a_0^2e\).
The integral of \(a_0^2e\) vanishes by its zero \(y\)-average. No derivative of a rough coefficient is multiplied by a distribution.

The pointwise derivative bound

\[
|DJ_r(V)|\le L_J|V|^3
\tag{19}
\]

follows directly from \(|j|\le|V|^2/2\), \(|Dj|=|V|\), \(|Du|\le2|V|\), \(0\le u+v-2j\le2|V|^2\), and \(|D(u+v-2j)|\le4|V|\); use \(|r-1|\le r+1\).
Since \(\|V-V_0\|_4\le D\varepsilon\), integration along the line segment gives

\[
|\mathcal Q-\mathcal Q_0|\le L_JD\varepsilon(R+t+D\varepsilon)^3.
\tag{20}
\]

If \(\varepsilon\le\delta R\), \(\delta\le1/D\), then, with \(Z=R^4+t^4\),

\[
|\mathcal Q-\mathcal Q_0|\le64L_JD\delta Z,
\qquad
|\mathcal P-\mathcal P_0|\le2C_P\varepsilon q(R+t).
\tag{21}
\]

## 7. Absorption and discriminant margin

The separated reserve (5) gives

\[
E_r(f_0,g_0,s)\ge\alpha Z+\beta s^2
(\|a_0\|_2^2+\|Dg_0\|_2^2)
\ge\alpha Z+\mu s^2\mathcal A(f_0,g_0),
\]

because \(\mathcal A(f_0,g_0)\le K_0(\|a_0\|_2^2+\|Dg_0\|_2^2)\).
Equations (6) and (9) now give

\[
E_r(f,g,s)\ge\alpha Z+\mu s^2q^2
-2C_P\varepsilon|s|q(R+t)-64L_JD\delta Z.
\]

Here \(\mu<1\), so the full residual \(s^2\mathcal R\) can indeed be bounded below by \(\mu s^2\mathcal R\). Young's inequality bounds the mixed term by

\[
\frac\mu2s^2q^2+\frac{2C_P^2}{\mu}\varepsilon^2(R+t)^2
\le\frac\mu2s^2q^2+\frac{16C_P^2}{\mu}\delta^2 Z.
\]

Therefore

\[
E_r(f,g,s)\ge
\left(\alpha-64L_JD\delta-\frac{16C_P^2}{\mu}\delta^2\right)Z
+\frac\mu2s^2\mathcal A(f,g).
\tag{22}
\]

The two final conditions in (4) make each loss at most \(\alpha/4\). This proves (2).

It also proves the following quantitative cubic discriminant estimate on exactly this class:

\[
\boxed{\mathcal P^2\le
4(1-\mu/2)\mathcal A\left(\mathcal Q-\frac\alpha2Z\right).}
\tag{23}
\]

If \(\mathcal A>0\), minimize the quadratic obtained by subtracting the right side of (2) from (6). If \(\mathcal A=0\), that quadratic is affine and nonnegative for every real \(s\), so \(\mathcal P=0\); (23) remains valid. No quotient is taken in the degenerate case.

All arguments first apply to smooth periodic functions. Coordinate averaging and the Fourier multipliers used above are bounded on the stated Sobolev spaces. Strong periodic convolution, Hölder, and quartic continuity extend the identities and the unabsorbed estimates to \(W^{1,4}\); apply the norm condition and absorption after taking that limit. Equivalently the algebra and projection hold directly in the Sobolev class. No higher derivative assumption or orientation restriction enters.

## 8. Exact example and boundaries

At \(r=1\), take \(f=\sin y+10^{-8}\sin(x+y)\). Its canonical separated part is \(\sin y\), and
\(\varepsilon^4/R^4=4\cdot10^{-32}<1/40{,}000{,}000^4\).
It is nonseparated and is admitted for every real background and every compatible \(W^{1,4}\) second potential. This example is illustrative; the theorem concerns all profiles and all admitted perturbations, including arbitrarily fine scales.

The result proves a homogeneous tube, not a radius of order one. It does not prove the unrestricted mixed-source inequality, remove all first-potential restrictions, or construct a negative compatible map. It does not change \(J_r\) by a completion coefficient. The generic weighted estimate, Riesz bounds, and acoustic projection tools are prior capital/classical tools; the new transfer here is their use with the separated quartic reserve and the zero-slice-average cancellations to remove the \(A>0\) requirement and obtain a shape-independent relative tube.

Primary comparison: the triangular-gradient-measure theorem of [Harris–Kirchheim–Lin, Theorem 2.4](https://arxiv.org/pdf/1708.07849v2) already covers qualitative one-profile cases. A generic mixed perturbation has no triangular support promise. This note makes no exhaustive prior-art or historical novelty claim.

The exact input pin, source hashes, algebra checks, and verification scope are in `SOURCES.json`, `check_exact.py`, and `CHECK_RECEIPT.json`.

