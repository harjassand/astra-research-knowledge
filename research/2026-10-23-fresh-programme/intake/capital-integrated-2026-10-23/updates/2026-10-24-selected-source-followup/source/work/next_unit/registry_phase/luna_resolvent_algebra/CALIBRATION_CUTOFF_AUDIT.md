# Calibration with a local amplitude cutoff

For $V(w)=V_0[1-\cos(2\pi w/d)]$, set $q(w)=\sqrt{2SV(w)}$. Its mean over one period is
\[
\frac1d\int_0^d q(w)\,dw=\frac{E_k}{d}=S m_c,
\]
so $R'(w)=q(w)-S m_c$ has a bounded $d$-periodic primitive $R$. For $|m|\le m_c$, expand the proposed square:
\[
\begin{aligned}
E_m-\frac{Sm^2}{2}-\frac{m}{m_c}R'(w)w_x
&=\frac S2w_x^2-\frac{m}{m_c}q(w)w_x+V(w)\\
&=\frac S2\left[w_x-\frac{m}{m_c}\frac{q(w)}S\right]^2
+\left(1-\frac{m^2}{m_c^2}\right)V(w)\ge0.
\end{aligned}
\]
The cancellation uses $R'=q-Sm_c$; the signs and factors are correct. The bound needs $|m|\le m_c$ because the leftover coefficient of $V$ must be nonnegative.

Let $f(\phi)=a\phi^2/2+b\phi^4/4$, with $a<0$, $b>0$, $a+S\alpha^2>0$, and $|\alpha|\sqrt{-2a/b}<m_c$. Choose a smooth cutoff $0\le\chi\le1$ equal to one on the closure of $\{f<0\}$ and supported strictly inside $\{|\alpha\phi|<m_c\}$. Such a cutoff exists because the negative-$f$ interval has a strict margin from the calibration boundary. Then
\[
f(\phi)+\chi(\phi)\frac{S\alpha^2\phi^2}{2}\ge0:
\]
where $f\ge0$ this follows from $\chi\ge0$, and where $f<0$, $\chi=1$ and the expression is $(a+S\alpha^2)\phi^2/2+b\phi^4/4>0$.

For $m=\alpha\phi(x)$, the relative energy density $E_m$ is nonnegative, hence $E_m\ge\chi E_m$. Apply the calibration only on the support of $\chi$ and drop its nonnegative square/remainder to obtain
\[
f(\phi)+E_{\alpha\phi}(w)
\ge f(\phi)+\chi\frac{S\alpha^2\phi^2}{2}
+\frac{\chi\alpha\phi}{m_c}R'(w)w_x.
\]
Define $\mathcal B(\phi,w)=\chi(\phi)\alpha\phi R(w)/m_c$. Its $w$ derivative is the last coefficient of $w_x$, so
\[
\frac{\chi\alpha\phi}{m_c}R'(w)w_x
=\partial_x\mathcal B(\phi,w)-\mathcal B_\phi(\phi,w)\phi_x.
\]
For periodic $\phi$ and an unwrapped $w$ with any integer winding $w(L)-w(0)=nd$, $R(w(L))=R(w(0))$ and therefore $\mathcal B(L)=\mathcal B(0)$. Integrating the total derivative gives zero, and adding the gradient penalty yields
\[
F_{\rm full}\ge \frac\kappa2\int_0^L\phi_x^2dx
-C_{\rm cal}\int_0^L|\phi_x|dx,
\qquad C_{\rm cal}=\sup_{\phi,w}|\mathcal B_\phi(\phi,w)|<\infty.
\]
The bound is independent of the integer winding number. It does not assume that $w$ stays in one registry well or forbid kink/antikink phase slips. If endpoints have noninteger registry mismatch, or free nonperiodic ends, the total derivative leaves the corresponding boundary term and this exact cancellation must be amended.

At registry minima $q$ has a cusp but is continuous and Lipschitz. Thus $R'=q-Sm_c$ is continuous and $R$ is $C^1$ (indeed $C^{1,1}$); no derivative of $q$ is used. For finite-energy one-dimensional fields $\phi,w\in H^1$, their absolutely continuous representatives obey the chain rule for $\mathcal B\in C^1$, including across those minima. No additional amplitude bound on $\phi$ is used: the strict support condition makes the calibration local, while outside the cutoff region $f\ge0$ supplies the bound. For $a\ge0$, $f\ge0$ outright and the trivial choice $\chi=0$ suffices.
