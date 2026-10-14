# FK tangent-contact compatibility result

Research date: 14 October 2026. This note is a new exact compatible stress test for the open N806 moving-Schur gate. It is not a proof of the concentration-stable estimate for every compatible gradient, and it is not a negative Jensen example.

The main result is an explicit periodic resonant gradient family for the tangent quartic

\[
G=3(u+v-2q)^2+\frac{35}{24}u^2+q^2-\frac52qu,
\qquad u=a^2+c^2,\quad v=b^2+d^2,\quad q=ad-bc.
\]

This is the candidate \(G\) in the incoming moving note. That source reports an exact acoustic Gram certificate for its rank-one convexity; I did not independently reconstruct that global certificate here. The new exact checks concern the compatible family and its affine optimization.

Its covariance-fitted rank-one line is certified exactly. Its averaged Hessian is positive definite, its true resonant cubic survives complete complementary-block elimination, and its optimizing affine background escapes to infinity. The exact reduced metric ratio stays finite and has limit \(8000/567021\). A rational output rotation makes the stale fixed-frame ratio \(h_*/h\) tend to zero while preserving the covariance-fitted moving calculation. Thus the old fixed-frame collapse is compatible with the desired scaling after the acoustic direction moves. The full gap remains positive and tends to \(219/4\).

## Exact compatible field

Let \(N\ge4\) be an integer and \(\varepsilon=1/N\). On the unit torus use phases

\[
\theta_1=2\pi(x+Ny),\quad
\theta_2=2\pi(-3x+Ny),\quad
\theta_3=2\pi(-2x+2Ny)=\theta_1+\theta_2.
\]

For \(j=1,2,3\), set \((p_j,q_j)=((1,1),(-3,1),(-2,2))\), \(s_j=(2,1,1)\), and

\[
a_j=\varepsilon(p_j/q_j)s_j,\qquad d_j=\tfrac32a_j,
\qquad c_j=\varepsilon(p_j/q_j)d_j.
\]

Then

\[
X_N=\sum_{j=1}^3
\begin{pmatrix}a_j&s_j\\c_j&d_j\end{pmatrix}\cos\theta_j
=D\Phi_N,
\]

where the smooth periodic potential is

\[
\Phi_N(x,y)=\frac1{2\pi}\sum_{j=1}^3
\begin{pmatrix}\varepsilon s_j/q_j\\\varepsilon d_j/q_j\end{pmatrix}
\sin\theta_j.
\]

Each mode matrix is the rank-one tensor \(v_j\otimes(p_j,Nq_j)\), so this is an actual compatible periodic gradient. The relation \(\theta_1+\theta_2=\theta_3\) gives a genuine three-wave resonance; exact integration gives \(\mathbb E a^3=9\varepsilon^3\ne0\). No determinant-balanced abstract law is used.

## Covariance fit and Hessian positivity

For the row-major vector \((a,b,c,d)\), the covariance is exactly

\[
C_N=\begin{pmatrix}
7\varepsilon^2&0&-18\varepsilon^3&\frac{21}{2}\varepsilon^2\\
0&3&\frac{21}{2}\varepsilon^2&0\\
-18\varepsilon^3&\frac{21}{2}\varepsilon^2&\frac{387}{4}\varepsilon^4&-27\varepsilon^3\\
\frac{21}{2}\varepsilon^2&0&-27\varepsilon^3&\frac{63}{4}\varepsilon^2
\end{pmatrix}.
\]

Let \(J\) represent the determinant, so \(J_{14}=J_{41}=1/2\) and \(J_{23}=J_{32}=-1/2\). The matrix

\[
K_N=3I-C_N-21\varepsilon^2J
\]

has a zero row and column in the \(e_{12}\) coordinate. Its remaining \(3\times3\) block is positive definite for \(0<\varepsilon\le1/4\). An exact certificate is in [exact_moving_metric_certificate.json](exact_moving_metric_certificate.json): every principal minor of that block, after writing \(x=\varepsilon^2\) and \(x=y/16\), has strictly positive Bernstein coefficients on \(0\le y\le1\). Therefore \(K_N\succeq0\), and every rank-one \(R\) satisfies

\[
R^TC_NR\le3|R|^2-21\varepsilon^2\det R=3|R|^2.
\]

Equality holds only on \(\mathbb Re_{12}\). Thus the covariance-fitted line is exactly \(R=e_{12}\), without a numerical fit. Also \(D^2G(e_{12})\) has rank three and kernel \(\mathbb RI\), so the acoustic direction is exactly \(A=I\). The tangent contact remainder is

\[
P_I(X)=\frac12(3a-2d)^2+\frac56c^2,
\]

of rank two, as required for this obstruction.

The exact leading principal minors of \(H_N=\mathbb E D^2G(X_N)\) are recorded in the certificate. They are positive for every \(\varepsilon>0\), so \(H_N\succ0\). This includes the nonzero determinant, which is \(15\varepsilon^4/4096\) times a polynomial with positive coefficients.

## Fully reduced cubic and optimized gap

Use the complete background decomposition \(A=I\), \(W=\operatorname{span}\{\operatorname{diag}(1,-1),e_{12},e_{21}\}\),

\[
H_N=\begin{pmatrix}h&k^T\\k&D\end{pmatrix},\quad
h_*=h-k^TD^{-1}k,
\quad u=\frac{m_3}{3m_2},\quad
\ell=b-uH_NR,
\quad r_*=\ell_A-k^TD^{-1}\ell_W.
\]

Constant-term Laurent integration gives exactly

\[
m_2=3,\qquad m_3=3,\qquad m_4=\frac{81}{4},\qquad u=\frac13,
\]

and

\[
h=\frac{645}{8}\varepsilon^4,\quad
h_* = \frac{10385}{144}\varepsilon^4+O(\varepsilon^6),\quad
r_*=-\frac{25}{2}\varepsilon^3+O(\varepsilon^5).
\]

The relative transverse ratios about the fitted line obey

\[
\delta_2^2:=\frac{\mathbb E|Y|^2}{m_2}
=\frac{91}{12}\varepsilon^2+O(\varepsilon^4),\qquad
\delta_4^2:=\left(\frac{\mathbb E|Y|^4}{m_4}\right)^{1/2}
=\frac{91}{12}\varepsilon^2+O(\varepsilon^4).
\]

Hence for \(\delta=\max(\delta_2,\delta_4)\),

\[
\frac{r_*^2}{h_*m_4\delta^2}\longrightarrow\frac{8000}{567021},
\qquad
\frac{r_*^2}{2h_*}=\frac{2250}{2077}\varepsilon^2+O(\varepsilon^4).
\]

The full affine optimization is exact, not a bounded-background scan. The optimizer \(B_N^*=-H_N^{-1}b_N\) satisfies

\[
\varepsilon(B_N^*)_{11}\to\frac{360}{2077},\quad
(B_N^*)_{12}\to-\frac13,\quad
\varepsilon(B_N^*)_{22}\to\frac{360}{2077},
\]

so \(|B_N^*|\asymp\varepsilon^{-1}\). Meanwhile

\[
\Delta_G(X_N)=\mathbb E G(X_N)-\frac12 b_N^TH_N^{-1}b_N
=\frac{219}{4}+O(\varepsilon^2)>0
\]

for all sufficiently large \(N\). The positive limit is exactly the pure-line margin
\(G(e_{12})[m_4-2m_3^2/(3m_2)]\). Thus this profile tests a nonzero resonance, complete Schur elimination, and an escaping optimizer without producing a negative gap.

## Angular motion and fixed-frame collapse

Let

\[
U_\varepsilon=\begin{pmatrix}
\frac{1-\varepsilon^2}{1+\varepsilon^2}&-\frac{2\varepsilon}{1+\varepsilon^2}\\
\frac{2\varepsilon}{1+\varepsilon^2}&\frac{1-\varepsilon^2}{1+\varepsilon^2}
\end{pmatrix}\in SO(2),\qquad \widetilde X_N=U_\varepsilon X_N.
\]

The integrand is left-rotation invariant, so \(\widetilde X_N=D(U_\varepsilon\Phi_N)\) has the same optimized gap and the same moving-frame Schur quantities. Its covariance-fitted rank-one line and acoustic direction are exactly
\(\widetilde R_N=U_\varepsilon e_{12}\) and \(\widetilde A_N=U_\varepsilon I\).

If one keeps the old contact frame \(A=I\) while eliminating its full complement, exact rotation of the Hessian gives

\[
h_{\rm old}=24\varepsilon^2+O(\varepsilon^4),\qquad
h_{*,\rm old}=\frac{10385}{144}\varepsilon^4+O(\varepsilon^6),\qquad
\frac{h_{*,\rm old}}{h_{\rm old}}=\frac{10385}{3456}\varepsilon^2+O(\varepsilon^4).
\]

The old-frame reduced numerator remains \(-25\varepsilon^3/2+O(\varepsilon^5)\), so the normalized quotient still tends to \(8000/567021\). This is an exact compatible example with \(H\succ0\), angular motion, a resonant cubic, and \(h_*/h\to0\) in the stale frame; following the covariance-fitted acoustic direction removes that frame artifact. The calculation uses a rational Pythagorean rotation, not a floating-angle approximation.

## Concentration and affine escape

For each fixed \(N\), the periodic potential \(\Phi_N\) is smooth and bounded. On a large square \(Q_L\), multiply it by a smooth cutoff equal to one except in a boundary strip of fixed width and zero on the boundary. The normalized polynomial moments through degree four of the resulting zero-boundary gradient converge to those of \(X_N\), because the boundary strip has relative area \(O(L^{-1})\). Since \(H_N\succ0\) and \(\Delta_G(X_N)>0\) for sufficiently large \(N\), choose the cutoff size large enough at each \(N\) to preserve positive definiteness, the fitted frame to the needed accuracy, and the positive optimized gap.

Now rescale this compactly supported potential into a square of area \(\rho\) by \(\psi_\rho(x)=r\psi((x-x_0)/r)\), with \(r=\sqrt{\rho}/L\). Its gradient values are unchanged inside the support and are zero outside. This gives an actual zero-boundary-compatible gradient on the unit torus. The averaged \(b,H,c\), covariance, \(h_*\), and \(r_*\) all scale by \(\rho\); \(m_4\) also scales by \(\rho\), so both relative transverse ratios and the normalized reduced metric quotient are unchanged, while the optimized gap scales by \(\rho\) and stays positive. The optimizer is unchanged by this spatial dilution. Taking \(\rho=\varepsilon^2\) along the diagonal sequence retains \(|B_N^*|\asymp\rho^{-1/2}\), so concentration, resonance, and escaping backgrounds coexist in actual zero-boundary gradients. The cutoff step is an approximation argument; the exact rational identities above belong to the periodic parent family.

## Scope and remaining obstruction

The incoming transverse proof controls its moving Schur quotient under rank-three remainder hypotheses. The original N806 contact theorem controls the fixed contact cubic and its cross-Hessian through Hodge compatibility. Its determinant-balanced negative laws are explicitly noncompatible and cannot be transferred to gradients. The old compatible controls (rotated line, positive-definite \(h_*/h\to0\) family, resonant anisotropic family, and concentration with an escaping optimizer) likewise stay positive.

The new exact family extends those controls by balancing the first covariance tilt, certifying the fitted line rather than estimating it, and combining nonzero resonance with an exact rotating-frame collapse. It supports the requested scaling for this one family but supplies no constant uniform over all periodic or zero-boundary gradients. The open gate remains: control the reduced cubic for arbitrary compatible fields when the fitted tangent direction moves, while its remainder has only rank two and the field can concentrate. A useful next operation is a vector-valued Hodge estimate for \(\ell[B]\) uniform over constant \(B\) near the moving contact, with the same \(H[B,B]\) metric and concentration quantifiers; the decisive stress test should couple a localized resonant \(b^2a\) profile to a soft moving background. If that estimate fails, the failure still needs to be converted into an exact compatible negative optimized gap before it refutes the Jensen claim.

A separate seeded scan tested 280 compatible three-wave resonances at \(N=32\). It found no negative gap; the largest computed normalized reduced ratio was \(0.01824\), and the smallest computed full gap was \(4.42336\). The 64-by-64 trapezoidal grid integrates these degree-four fields exactly by bandwidth, but rank-one frame fitting used multistart floating-point optimization. This scan is only a finite search and supplies no global lower bound.

The exact arithmetic and bounded search are internal evidence only. The original N806 and moving-note claims remain source-derived and externally unreviewed; no novelty, all-integrand theorem, full quasiconvexity implication, or external validation is claimed.
