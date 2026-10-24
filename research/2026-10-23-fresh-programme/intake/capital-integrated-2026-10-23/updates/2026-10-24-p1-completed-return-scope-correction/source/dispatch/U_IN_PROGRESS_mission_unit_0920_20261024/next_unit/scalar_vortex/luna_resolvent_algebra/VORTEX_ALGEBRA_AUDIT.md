# Exact oscillator vortex-pair algebra audit

Take $H_0=(-\Delta+r^2)/2$ on $\mathbb R^2$, $P=r^2+a+bx$, $a>b^2/4$, $b>0$, and
\[
\psi_I=cP e^{-r^2/2},\qquad c=(\pi Z)^{-1/2}>0,\qquad
Z=(a+1)^2+1+b^2/2.
\]
The polynomial is strictly positive:
\[
P=(x+b/2)^2+y^2+a-b^2/4>0.
\]
Using $\int e^{-r^2}=\pi$, $\int r^2e^{-r^2}=\pi$, $\int r^4e^{-r^2}=2\pi$, and $\int x^2e^{-r^2}=\pi/2$ gives $\int P^2e^{-r^2}=\pi Z$, so $\psi_I$ is normalized and strictly positive.

For a polynomial $Q$ in two dimensions,
\[
H_0(Qe^{-r^2/2})=e^{-r^2/2}\left(-\frac12\Delta Q+(x,y)\cdot\nabla Q+Q\right).
\]
Here $\Delta P=4$ and $(x,y)\cdot\nabla P=2r^2+bx$, hence
\[
H_0\psi_I=c e^{-r^2/2}(3r^2+2bx+a-2).
\]
With $V_{\rm pre}=r^2/2+[2(a+1)+bx]/P$, the pre-quench Hamiltonian is
$H_{\rm pre}=-\Delta/2+V_{\rm pre}=H_0+[2(a+1)+bx]/P$. Acting on $\psi_I$, the added numerator completes the displayed $H_0\psi_I$ polynomial to $3P$, so $H_{\rm pre}\psi_I=3\psi_I$. Positivity of $P$ makes the rational term nonsingular.

Decompose $P=(a+1)+bx+(r^2-1)$. The three Gaussian polynomials have $H_0$ energies $1,2,3$, respectively, so the exact quench evolution is
\[
\psi(t)=c e^{-r^2/2-it}\left[(a+1)+bx e^{-it}+(r^2-1)e^{-2it}\right].
\]
This matches the proposed expression. For zeros, set $G=e^{it}[(a+1)+bx e^{-it}+(r^2-1)e^{-2it}]$. Then
\[
\operatorname{Re}G=(a+r^2)\cos t+bx,\qquad
\operatorname{Im}G=(a+2-r^2)\sin t.
\]
When $\sin t\ne0$, every zero must satisfy
\[
r^2=a+2,\qquad x=-\frac{2(a+1)}b\cos t,
\]
with $y=\pm\sqrt{a+2-4(a+1)^2\cos^2t/b^2}$ when the radicand is nonnegative. Thus the formula describes a pair only at times when those points exist; at $t=\pi/2$ they always exist. At that time the field, up to a nonzero scalar phase and positive Gaussian, is $-bx-i(a+2-r^2)$. The Jacobian of $(\operatorname{Re}\psi,\operatorname{Im}\psi)$ at either zero has sign $\operatorname{sgn}(-2by)$; more generally the sign is $\operatorname{sgn}(-2by\sin t)$ for simple zeros. The two roots $y=\pm\sqrt{a+2}$ therefore have opposite charges. Initially $P>0$, so the field has no zeros. There is no contradiction with this later pair under the linear quench.

The normalized post-quench harmonic energy is the weighted average of the three mode energies. Their squared norms before multiplying by $c^2$ are $\pi(a+1)^2$, $\pi b^2/2$, and $\pi$, respectively; consequently
\[
E_{\rm post,0}=\langle\psi_I,H_0\psi_I\rangle
=\frac{(a+1)^2+b^2+3}{Z}.
\]
The initial state is real, hence $\langle L_z\rangle=0$ (equivalently, its angular derivative integrates to zero). Isotropic $H_0$ commutes with $L_z$, so the expectation remains zero during the quench evolution.

For the nonlinear extension, define
\[
E_g[V;\psi]=\int_{\mathbb R^2}\left(\frac12|\nabla\psi|^2+V|\psi|^2+\frac g2|\psi|^4\right)dx,
\qquad V_{\rm pre}^g=V_{\rm pre}-g\rho_I,\quad \rho_I=|\psi_I|^2.
\]
Assume $g\ge0$, $\|\psi\|_2=\|\psi_I\|_2=1$, and finite-energy states for which the ground-state transform is justified (first for smooth decaying states, then by form-domain closure). Since $V_{\rm pre}^g+g\rho_I=V_{\rm pre}$, $\psi_I$ is also the stationary nonlinear profile at frequency $3$. Since $H_{\rm pre}\psi_I=3\psi_I$ and $\psi_I>0$,
\[
\langle\psi,H_{\rm pre}\psi\rangle-3
=\frac12\int\rho_I\left|\nabla\left(\frac{\psi}{\psi_I}\right)\right|^2dx.
\]
The extra density terms in $E_g[V_{\rm pre}^g;\cdot]$ differ by $\frac g2\int(|\psi|^2-\rho_I)^2dx$. Therefore the proposed identity holds exactly:
\[
E_g[V_{\rm pre}^g;\psi]-E_g[V_{\rm pre}^g;\psi_I]
=\frac12\int\rho_I\left|\nabla\left(\frac{\psi}{\psi_I}\right)\right|^2dx
+\frac g2\int(|\psi|^2-\rho_I)^2dx\ge0.
\]
The norm-one premise is essential for canceling the eigenvalue term $3(\|\psi\|_2^2-1)$. This certifies the constrained energy comparison for the specified potential; it is not a dynamical vortex-pair lifetime or novelty claim.
