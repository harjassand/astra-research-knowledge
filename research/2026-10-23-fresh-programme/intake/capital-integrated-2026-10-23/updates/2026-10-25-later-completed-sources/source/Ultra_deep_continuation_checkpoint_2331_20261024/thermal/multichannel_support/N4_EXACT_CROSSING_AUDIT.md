# Exact N=4 nonlocal-kernel crossing audit

For the triangular kernel with range parameter \(N=4\),
\[
c_4=\frac{12K}{4^2(4^2-1)}=\frac K{20},\qquad
(\kappa_1,\kappa_2,\kappa_3)
=\left(\frac{3K}{20},\frac K{10},\frac K{20}\right).
\]
Its weighted stiffness is \(\sum n^2\kappa_n=K\), and
\[
\Omega^2=\frac{4K}{5M},\qquad
u(q)=\frac14\frac{\sin(2q)}{\sin(q/2)}
=\cos(q/2)\cos q,
\qquad \omega(q)=\Omega\sqrt{1-u(q)^2}.
\]

Differentiate:
\[
u'(q)=-\sin(q/2)\left(1+\frac32\cos q\right).
\]
Thus \(u\) decreases from \(1\) to \(0\) on \([0,\pi/2]\), is negative after \(\pi/2\), and reaches its negative minimum at
\(q_m=\arccos(-2/3)\). At that point
\(u(q_m)=-2/(3\sqrt6)\), so the secondary local minimum of frequency is
\[
\omega_m=\Omega\sqrt{1-2/27}=\frac{5\Omega}{3\sqrt3}.
\]
The frequency rises from \(0\) to \(\Omega\), falls to \(\omega_m\), then rises back to \(\Omega\). Counting all regular positive-velocity crossings gives
\[
N_{\rm ch}(\omega)=
\begin{cases}
1,&0<\omega<\omega_m,\\
3,&\omega_m<\omega<\Omega,\\
0,&\omega>\Omega.
\end{cases}
\]
Tangencies at band edges have measure zero. The complete classical channel width is therefore
\[
W_4=\omega_m+3(\Omega-\omega_m)
=3\Omega-2\omega_m
=\Omega\left(3-\frac{10}{3\sqrt3}\right).
\]

The rigid nearest-neighbor chain with the same \(M,K_{\rm eff}=K\) has cutoff
\(\Omega_R=2\sqrt{K/M}=\sqrt5\,\Omega\) and width \(W_R=\Omega_R\). Since
\(3-10/(3\sqrt3)<2<\sqrt5\), the N=4 classical width is strictly smaller.

For Bose weight \(g_\theta\), the exact comparison is
\[
J_4-J_R
=2\int_{\omega_m}^{\Omega}g_\theta(\omega)\,d\omega
-\int_{\Omega}^{\Omega_R}g_\theta(\omega)\,d\omega.
\]
As \(\theta\downarrow0\), for fixed \(0<a<b\),
\[
\int_a^b g_\theta(\omega)\,d\omega
\sim\left(\frac{a^2}{\theta}+2a+2\theta\right)e^{-a/\theta}.
\]
The positive term starts at \(a=\omega_m<\Omega\), whereas the negative term starts at \(\Omega\). Hence
\[
\frac{2\int_{\omega_m}^{\Omega}g_\theta}
{\int_{\Omega}^{\Omega_R}g_\theta}
\sim 2\left(\frac{\omega_m}{\Omega}\right)^2
e^{(\Omega-\omega_m)/\theta}\longrightarrow\infty,
\]
so \(J_4>J_R\) for all sufficiently low positive temperatures. Conversely, as \(\theta\to\infty\), \(g_\theta\to1\) uniformly on these finite frequency intervals and \(J_4\to W_4<W_R\leftarrow J_R\). Thus the N=4 design beats this rigid comparator at low temperature but does not dominate it at all temperatures. This sign change comes from the extra lower-frequency crossings, not from a band union that omits plateau oscillations.
