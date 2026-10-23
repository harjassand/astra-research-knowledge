# Two-network elimination audit

Consider a nonzero Fourier mode of the quadratic part of
\[
F=\int\left[\frac a2\phi^2+\frac b4\phi^4+\frac\kappa2\phi_x^2
+\frac C2(u_x-\alpha\phi)^2+\frac D2v_x^2+\frac K2(u-v)^2\right]dx,
\]
with $C,D,K,\kappa,b>0$. Let $q=k^2$, and set $r=ik u$, $s=ikv$. Apart from the $\phi$ terms, the per-mode quadratic energy is
\[
\frac12\left[C|r-\alpha\phi|^2+D|s|^2+\frac Kq|r-s|^2\right].
\]
The last term follows from $u-v=(r-s)/(ik)$. Minimizing over $r,s$ is three springs in series, with compliances $1/C$, $1/D$, and $q/K$; hence the effective coefficient multiplying $|\phi|^2/2$ is
\[
A_{\rm el}(q)=\frac{\alpha^2}{C^{-1}+D^{-1}+q/K}
=\frac{E_0}{1+\xi^2q},\qquad
E_0=\frac{\alpha^2CD}{C+D},\quad \xi^2=\frac{CD}{K(C+D)}.
\]
Thus the quadratic coefficient for nonzero modes is indeed
\[
\lambda(q)=a+\kappa q+\frac{E_0}{1+\xi^2q}.
\]
The displacement block is positive for every $q>0$: when $\phi=0$, its energy is a sum of positive terms and vanishes only at $r=s=0$. In the original variables this leaves only common rigid translation at zero wave number. The elimination therefore does not hide an elastic instability.

For $q\ge0$, $\lambda'(q)=\kappa-E_0\xi^2/(1+\xi^2q)^2$. A strict nonzero minimizing wave number exists exactly when $E_0\xi^2>\kappa$, in which case
\[
q_*=k_*^2=\frac{\sqrt{E_0\xi^2/\kappa}-1}{\xi^2},\qquad
\lambda_{\min}=a+\frac{2\sqrt{E_0\kappa}}{\xi}-\frac{\kappa}{\xi^2}.
\]
The requested separation of long-wave and finite-wave signs is therefore
\[
-E_0<a<\frac{\kappa}{\xi^2}-\frac{2\sqrt{E_0\kappa}}{\xi},
\qquad E_0\xi^2>\kappa.
\]
This interval is nonempty because its width is $(\sqrt{E_0}-\sqrt\kappa/\xi)^2>0$. Here $\lambda(0)=a+E_0$ means the limit $q\downarrow0$ through nonzero modes. The imposed $\langle\phi\rangle=0$ excludes the uniform $\phi$ mode itself. If a uniform mode is admitted, its elastic coefficient depends on the macroscopic strain boundary condition: strict periodic $u,v$ displacements forbid affine strain and give $C\alpha^2$, whereas allowing a common affine strain for both networks gives $E_0$. A clamped-length constraint must be imposed before assigning the uniform-mode coefficient; it cannot be inferred from the $q\downarrow0$ limit. In a finite periodic sample, only discrete nonzero $k$ are available, so a continuum $\lambda_{\min}<0$ is not by itself proof that an allowed sample mode is unstable.

For a matching discrete ladder, take node variables $u_j,v_j$, bond variable $\phi_j$, and Fourier difference symbol $d_h(k)=(e^{ikh}-1)/h$. For example, use the quadratic per-mode energy
\[
\frac12\left[a|\phi|^2+\kappa q_h|\phi|^2
+C|d_hu-\alpha\phi|^2+D|d_hv|^2+K|u-v|^2\right],
\qquad q_h=|d_h|^2=\frac{4\sin^2(kh/2)}{h^2}.
\]
For $q_h>0$, set $r=d_hu$, $s=d_hv$ and use $|u-v|^2=|r-s|^2/q_h$. The same minimization gives the exact discrete coefficient
\[
\lambda_h(k)=a+\kappa q_h+\frac{E_0}{1+\xi^2q_h}.
\]
This substitution is exact for this stated local ladder energy, not for arbitrary discrete couplings. The lattice restricts $q_h\in[0,4/h^2]$ (and a finite ring restricts it further to its allowed modes), so the continuum minimizing $q_*$ is realized only if the available $q_h$ values reach it. The $k=0$ mode again needs its boundary-condition treatment separately.

The positive quartic coefficient bounds the local potential below and can saturate a finite-mode instability, but this dispersion calculation alone does not prove a selected pattern, a global minimizer, or a general microphase theorem.
