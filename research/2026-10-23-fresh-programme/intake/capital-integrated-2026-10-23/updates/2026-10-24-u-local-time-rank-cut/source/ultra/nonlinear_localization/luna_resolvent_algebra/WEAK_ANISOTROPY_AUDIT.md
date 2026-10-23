# Independent audit: weak-anisotropy sidebands and internal modes

This checks the algebra and the compact open-channel sector in the frozen note. No source review or parameter search was performed.

## Sideband matrix and open-channel signs

For $z=q_1+iq_2$, the fourfold restoring force decomposes as

\[
(\gamma+3\epsilon/4)|z|^2z+(\epsilon/4)\bar z^3.
\]

Let $\bar\gamma=\gamma+3\epsilon/4$, $B=\bar\gamma A^2$, and linearize about $z_0=Ae^{i\Omega t}$. The isotropic part gives $2B\,w+B e^{2i\Omega t}\bar w$. The anisotropic forcing is $-(\epsilon A^3/4)e^{-3i\Omega t}$ on the equation's right side. The coupled sidebands are therefore $b e^{-3i\Omega t}$ and $d e^{5i\Omega t}$.

With the stated $e^{+i\nu t}$ convention, eliminating the outgoing field puts $-\Sigma(\nu)$ on the oscillator operator. Since $\Sigma(\nu)=-i\,\mathrm{sign}(\nu)\eta_{|\nu|}$, the $-3\Omega$ row has diagonal $a_3-i\eta_3$. The $+5\Omega$ row before conjugation has diagonal $a_5+i\eta_5$; conjugating that row gives the variable $\bar d$ at $-5\Omega$ and diagonal $a_5-i\eta_5$. Thus the stated system

\[
\begin{pmatrix}a_3-i\eta_3&B\\B&a_5-i\eta_5\end{pmatrix}
\begin{pmatrix}b\\\bar d\end{pmatrix}
=\begin{pmatrix}-A^3/4\\0\end{pmatrix}
\]

has consistent signs. For nonzero $x$, $\operatorname{Im}(x^*Mx)=-\eta_3|x_1|^2-\eta_5|x_2|^2<0$, so $M$ is invertible. Since $B>0$ and the forcing is nonzero, neither sideband amplitude can vanish: either zero component, substituted into the other row, forces both components to zero.

## Flux and torque checks

For a circular vector wave with complex amplitude $a$ at signed frequency $\nu$, the two outgoing sides carry energy flux $|\nu|\eta_{|\nu|}|a|^2$, where $\eta_\nu=g^2/(2c^2k)$ and $k=\sqrt{\nu^2-\omega_c^2}/c$. This is twice the scalar cosine-amplitude result because the two real vector components are in quadrature. Its angular-momentum flux is energy flux divided by the signed $\nu$. Hence the two sidebands give the stated $\Gamma_E=3\Omega\eta_3|b|^2+5\Omega\eta_5|d|^2$ and angular flux $\epsilon^2(-\eta_3|b|^2+\eta_5|d|^2)$.

The torque from $V_{\rm aniso}=\epsilon\operatorname{Re}(z^4)/16$ is $\dot L=\epsilon\operatorname{Im}(z^4)/4$. At order $\epsilon^2$, only the $b$ sideband contributes to the cycle average, giving $\langle\dot L\rangle=\epsilon^2A^3\operatorname{Im}b$. From $x^*Mx=x^*(-A^3/4,0)^T$ and the negative imaginary part above,

\[
A^3\operatorname{Im}b=-4(\eta_3|b|^2+\eta_5|d|^2).
\]

Subtracting the radiated angular flux leaves $\dot L_{\rm bound}=-\epsilon^2(3\eta_3|b|^2+5\eta_5|d|^2)$; multiplying by $\Omega$ agrees with the energy loss $-\epsilon^2\Gamma_E$ at this formal order. These identities check the formal response balance; they do not prove modulation over long times.

## Compact-sector internal-mode exclusion

Below cutoff,

\[
f(\nu)=\omega_0^2-\nu^2-\frac{g^2}{2c\sqrt{\omega_c^2-\nu^2}},
\quad f''(\nu)=-2-\frac{g^2(\omega_c^2+2\nu^2)}
{2c(\omega_c^2-\nu^2)^{5/2}}<0.
\]

It is even and strictly decreases with $|\nu|>0$. Also $B=-f(\Omega)>0$. A real gap mode $0<\sigma<\Delta=\omega_c-\Omega$ has both lab sidebands below cutoff and would require

\[
X Y-B^2=0,\quad X=f(\Omega-\sigma)+2B,\quad
Y=f(\Omega+\sigma)+2B.
\]

The sector condition $\Omega>\omega_c/3$ is exactly enough for $\Delta<2\Omega$, so $|\Omega-\sigma|<\Omega$ and therefore $X>B$. Strict concavity at midpoint $\Omega$ gives $X+Y<2B$. If $Y\le0$, then $XY-B^2<0$. If $Y>0$, then $X,Y>0$ and $XY\le((X+Y)/2)^2<B^2$. Thus the determinant is strictly negative throughout the open gap. At $\sigma=0$ it vanishes, as expected for the phase/family neutral subspace; this mode must be projected out separately.

For real $\sigma\ge\Delta$, the upper lab frequency $\Omega+\sigma$ is open (at equality it is at threshold). An $L^2$ eigenstate must have zero oscillator source in that channel, since its half-line field is oscillatory when open and affine at threshold. The nonzero off-diagonal $B$ then forces the other sideband coefficient to zero too. This excludes nonzero real-frequency $L^2$ internal modes, including embedded ones, in the stated sector. The argument is not itself a dispersive estimate and does not exclude resonances; if “internal mode” is meant to include non-real spectral eigenvalues, a separate Hamiltonian spectral-stability argument is needed. No additional real gap resonance or threshold eigenstate is left by the stated inequalities.

The conclusion is conditional on the stated point-coupled KG spectral reduction, real $\sigma$, $\Omega$ in a compact subinterval with $3\Omega>\omega_c$, and $B>0$. It supplies no uniform resolvent estimate or nonlinear lifetime theorem.

