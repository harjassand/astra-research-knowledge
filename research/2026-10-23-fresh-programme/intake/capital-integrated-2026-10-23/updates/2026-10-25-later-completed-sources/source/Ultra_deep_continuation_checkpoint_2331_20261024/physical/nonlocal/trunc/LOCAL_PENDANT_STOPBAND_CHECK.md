# Exact stop-band check: counted local pendant versus N=4 Fejer rods

This is an ideal longitudinal metric-graph comparison at \(K=M_{\rm total}=\theta=\hbar=1\), with \(\theta=k_BT/\hbar\). It certifies a scalar conductance inequality only; no material/device advantage follows.

## Fully counted resources

Take backbone period \(a\), material wave speed \(c\), and \(\tau=a/c=1/\sqrt{101}\). Each cell has backbone point mass \(m_b=1/1000\), pendant mass
\[
m_s=1-m_b-K\tau^2-k(\ell/c)^2,
\quad k=2/5,\quad \ell=(2/5)a.
\]
The backbone axial rod mass is \(K\tau^2=1/101\); the pendant rod mass is
\[
 k(\ell/c)^2=\frac25\left(\frac25\right)^2\frac1{101}
 =\frac{64}{1000\cdot101}=\frac{64}{101000}.
\]
Hence \(m_s=19967/20200\approx0.9884653465>0\), and the per-cell total is exactly
\[
m_b+m_s+\frac1{101}+\frac{64}{101000}=1.
\]
The static long-wave stiffness remains \(K=1\): the pendant follows the backbone under relaxed static translation. Both distributed rods are retained dynamically below.

## Exact dispersion including both rods

Set \(\alpha=\omega a/c=\omega/\sqrt{101}\), \(s=\omega\ell/c=(2/5)\alpha\). The pendant rod's exact two-end dynamic stiffness has entries
\[
A=k s\cot s,\qquad B=k s\csc s.
\]
Eliminating the pendant point mass, away from its discrete poles, gives the backbone's added dynamic load
\[
Z_{\rm eff}=-m_b\omega^2+A-\frac{B^2}{A-m_s\omega^2}.
\]
The backbone is itself a distributed rod: its endpoint dynamic stiffness is retained, giving the exact Bloch equation
\[
\cos q=\cos\alpha+\frac{\sin\alpha}{2K\alpha}Z_{\rm eff}.
\]
Thus this is not a point-spring truncation of either rod. Away from the countable elimination poles, a real Bloch phase exists exactly when the right side lies in \([-1,1]\); there is at most one right-moving channel because there is only one intercell backbone rod. Any extra internal eigenmodes at the discrete poles do not affect the frequency integral.

## Certified stop band \([0.65,5.8]\)

Throughout this interval, \(0<s\le0.231<\pi/2\) and \(0<\alpha\le0.578<\pi/2\). Since \(A\le k=0.4\), while
\[
m_s(0.65)^2
=\frac{3374423}{8080000}>0.4,
\]
we have \(A-m_s\omega^2<0\) on the entire interval. Therefore
\[
Z_{\rm eff}>A-m_b\omega^2.
\]
For \(0\le s<\pi/2\),
\[
s\cot s\ge1-\frac{s^2}{2};
\]
indeed, \(h(s)=s\cos s-(1-s^2/2)\sin s\) has \(h(0)=0\) and \(h'(s)=(s^2/2)\cos s\ge0\). Hence
\[
Z_{\rm eff}>
\frac25\left(1-\frac{s^2}{2}\right)-\frac{\omega^2}{1000}.
\]
The right side decreases with \(\omega\), and at \(\omega=5.8=29/5\) equals
\[
L=\frac{898147}{2525000}\approx0.3557017822.
\]
Meanwhile the condition \(\cos q>1\) is equivalent here to
\[
Z_{\rm eff}>2K\alpha\tan(\alpha/2).
\]
For \(x\in[0,\pi/2)\), \(x\cos x-(1-x^2/2)\sin x\ge0\), so
\(\tan x\le x/(1-x^2/2)\). Thus
\[
2K\alpha\tan(\alpha/2)
\le \frac{\alpha^2}{1-\alpha^2/8}
\le \frac{6728}{19359}\approx0.3475386126,
\]
where the last value uses \(\alpha_{\max}^2=841/2525\). The exact gap is
\[
\frac{898147}{2525000}-\frac{6728}{19359}
=\frac{399027773}{48881475000}>0.
\]
Consequently \(\cos q>1\) at every frequency in \([0.65,5.8]\). There are no propagating modes in this whole interval; it contains no pendant or backbone rod pole.

## Scalar conductance comparison

At \(\theta=1\), the one-channel Bose weight is
\[
g(\omega)=\left(\frac{\omega/2}{\sinh(\omega/2)}\right)^2
=\frac{\omega^2e^{-\omega}}{(1-e^{-\omega})^2}\le1.
\]
The stop band and the a.e. one-channel count imply
\[
J_{\rm pendant}\le0.65+\int_{5.8}^{\infty}g(\omega)d\omega
\le0.65+
\frac{e^{-5.8}(5.8^2+2(5.8)+2)}{(1-e^{-5.8})^2}.
\]
The last tail expression is \(0.14389164693\), so the stated bound is \(0.79389164693<0.8\). For a rational certificate, the positive Taylor sum for \(e^{29/5}\) through order 11 exceeds 325. Therefore \(e^{-5.8}<1/325\), and monotonicity of \(x/(1-x)^2\) gives the tail bound
\[
\int_{5.8}^{\infty}g
<\frac{15353}{104976}<\frac3{20},
\]
which already proves \(J_{\rm pendant}<0.8\).

For the complete N=4 Fejer graph with all three distributed rods, the
full-field estimate in `DISTRIBUTED_FEJER_RODS.md` §2.2, Eq. (6), gives
\(D(0.84,q)>0\) whenever \(\cos(q)\le0\). In particular the acoustic
endpoint at \(q=\pi\) lies above \(0.84\); the continuous acoustic branch
begins at zero at \(q=0\), so it supplies at least one right-moving channel
across every frequency in \([0,0.84]\). This uses the distributed-rod
dispersion, not its point-mass approximation. For \(x=\omega/2\le0.42\),
the power series and \((2j+1)!\ge6^j\) give
\[
\frac{\sinh x}{x}\le\sum_{j\ge0}(x^2/6)^j
=\frac1{1-x^2/6},
\quad
g(\omega)\ge(1-x^2/6)^2\ge1-\frac{\omega^2}{12}.
\]
It follows that
\[
J_{N=4,\,\rm Fejer}\ge\int_0^{0.84}g(\omega)d\omega
\ge0.84-\frac{0.84^3}{36}=0.823536.
\]
Hence the counted local pendant fixture has a strictly lower ideal longitudinal Landauer integral than this N=4 Fejer fixture under the stated scalar parameters. The comparison does not include transverse modes, damping, routing, fabrication, or any device claim.
