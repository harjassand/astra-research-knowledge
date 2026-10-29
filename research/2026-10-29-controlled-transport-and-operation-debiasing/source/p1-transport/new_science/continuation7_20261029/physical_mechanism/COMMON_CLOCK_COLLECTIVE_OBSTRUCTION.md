# A common Poisson phase does not replace independent local clocks

29 October 2026. Exact companion boundary. This preserves the already pinned deterministic proofs unchanged.

The round5 shared-phase obstruction concerned the full microscopic observable space. Here the requested output is the ordinary empirical magnetization itself, and the failure persists for its entire path from a nonzero initial profile. This is a heat-bath example, not a claimed sharpness theorem for the conserving SSEP ring.

Let \(y_i\in\{-1,+1\}\), \(E_i\) be fair spin heat-bath projections, \(\sigma\in\{-1,+1\}\) one common phase orientation, and

\[
\mathcal L=\sum_{i=1}^N
 \left[1+\alpha\sigma\prod_{j\ne i}y_j\right](E_i-I)
 +\gamma(F_\sigma-I),\qquad0<\alpha<1. \tag{1}
\]

Every native rate multiplier is unchanged by its own heat-bath update. The full process is reversible in uniform visible spins times a fair sign. Its actual native rates are bounded per site, and the phase clock is independent of the spins. Frozen hidden parameters can be added without changing the construction.

Define

\[
m_N=N^{-1}\sum_i y_i,\qquad p_N=\prod_i y_i,
\qquad z_N=\sigma p_N.
\]

The exact closure is

\[
\mathcal L m_N=-m_N-\alpha z_N,
\qquad\mathcal L z_N=-(N+2\gamma)z_N-\alpha N m_N. \tag{2}
\]

Use the small corrector

\[
G_N=m_N-\frac{\alpha}{N+2\gamma}z_N.
\]

Then

\[
\mathcal L G_N=-k_{N,\gamma}m_N,
\qquad k_{N,\gamma}=1-\frac{\alpha^2N}{N+2\gamma},
\qquad |G_N-m_N|\le\alpha/N. \tag{3}
\]

An actual spin flip changes \(G_N\) by at most \(2(1+\alpha)/N\). The total native spin-flip rate is at most \(N(1+\alpha)/2\). A phase flip changes \(G_N\) by at most \(2\alpha/(N+2\gamma)\). Hence the martingale \(M_G\) has

\[
\begin{aligned}
\mathbb E\langle M_G\rangle_T
&\le \frac{2(1+\alpha)^3T}{N}
 +\frac{4\alpha^2\gamma T}{(N+2\gamma)^2}\\
&\le\frac{[2(1+\alpha)^3+\alpha^2/2]T}{N}. \tag{4}
\end{aligned}
\]

The second inequality uses \(\sup_{\gamma\ge0}\gamma/(N+2\gamma)^2=1/(8N)\). It is uniform in the phase rate. Since \(1-\alpha^2\le k_{N,\gamma}\le1\), the integral equation for (3), the corrector bound, and Doob's inequality imply

\[
\sup_{t\le T}|m_N(t)-m_N(0)e^{-k_{N,\gamma}t}|
\xrightarrow{\mathbb P}0 \tag{5}
\]

for every initial spin/sign configuration and every sequence \(\gamma=\gamma_N\). One can use the same factor-two stable Volterra bound as in the main path proof.

If \(m_N(0)\to m_0\ne0\), \(\gamma_N\to\infty\), and \(\gamma_N/N\to r<\infty\), the limiting collective trajectory is therefore

\[
m_0\exp\!\left[-\left(1-\frac{\alpha^2}{1+2r}\right)t\right]. \tag{6}
\]

The mean native generator predicts \(m_0e^{-t}\). A common phase rate which tends to infinity arbitrarily slowly does not supply that prediction. This family needs \(\gamma_N/N\to\infty\) to remove the order-one correction. In contrast, the independent local pi-kick replacement bound in the governing note requires only \(\gamma_N\to\infty\), even for these global context functions.

This is a precise allocation of physical control: one common random clock is different from independent local phase kicks. It does not show that all shared controllers fail, nor that the conserving-ring necessity threshold is the same. It also does not infer energy costs from the rates. The construction is an analytic boundary within the declared reversible heat-bath model; no hardware measurement is asserted.
