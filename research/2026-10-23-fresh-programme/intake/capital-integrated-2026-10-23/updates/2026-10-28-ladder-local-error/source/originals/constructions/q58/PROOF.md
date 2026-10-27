# Local parity-breaking response of the hard-core ladder

## Statement and scope

For the semi-infinite ladder in the supplied source, at **exactly** \(g=1/5\), let \(\psi_g\) be the normalized dressed even hard-core pair and let \(V=n_L-n_R\). Then

\[
\rho(E_p)=\frac1\pi\lim_{\epsilon\downarrow0}
\operatorname{Im}\langle V\psi_g,(H_{\rm odd}-E_p-i\epsilon)^{-1}V\psi_g\rangle
\]

exists and satisfies

\[
\boxed{0<\rho(E_p)<\infty.}
\]

An explicit continuum expression is (14) below. Its evaluation gives
\(\rho(E_p)\simeq2.12750672\times10^{-8}\) in the declared units. This decimal is a numerical quadrature result. Separately, an outward-rounded interval computation using only algebraic atoms, support bounds and two continuum intervals proves
\(\rho(E_p)>4\times10^{-16}\); it does not assume accuracy of that quadrature.

The consequence is a nonzero local symmetry-breaking transition coefficient for the actual protected pair at fixed nonzero coupling. The exact available machinery is the source's even pair resolvent together with the explicit half-line Jacobi measures. The missing link addressed here is the *dressed source and complete odd hard-core compression*. The strongest operational alternative already in the source is exact preservation of the exchange parity; a parity-preserving wrong-band source is a different perturbation and supplies no coefficient for this \(V\).

Only the supplied `ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md` and its two supplied Python constructions are used as scientific input, frozen under source revision `c1b8ac1516457a88b383a6350680e3be865fbffd`. No novelty or physical-device claim is made.

## Complete one-body measures

Use the convention
\(r_\sigma(z)=\langle e_\sigma,(h_\sigma-z)^{-1}e_\sigma\rangle\), so its upper boundary value has nonnegative imaginary part. Write

\[
 c_+=5,\quad c_-=1,\qquad k_+=2g^2,\quad k_-=g^2,
\]

where \(k_\sigma\) is the **square** of the endpoint coupling. Define

\[
 q_c(z)=2[-(z-c)+\sqrt{z-c-1}\sqrt{z-c+1}],\qquad
 r_\sigma(z)=\frac1{3-z-k_\sigma q_{c_\sigma}(z)}. \tag{1}
\]

Both square roots are principal for \(\operatorname{Im}z>0\); their product is asymptotic to \(z-c\). This fixes all signs and branches. The memory endpoint is cyclic for each irreducible Jacobi matrix, so its spectral representation is the complete one-body space, not a selected bath mode.

At the present couplings each measure consists of exactly one atom and one absolutely continuous band:

\[
 d\mu_\sigma(u)=Z_\sigma\delta_{E_\sigma}(du)+a_\sigma(u)\,du, \tag{2}
\]

\[
 a_\sigma(u)=
 \frac{2k_\sigma\sqrt{1-(u-c_\sigma)^2}}
 {\pi\{[3-u+2k_\sigma(u-c_\sigma)]^2
       +4k_\sigma^2[1-(u-c_\sigma)^2]\}}
 \mathbf1_{|u-c_\sigma|<1}. \tag{3}
\]

There is no omitted singular continuous or threshold component: (1) is a rational function of the square root, its band denominator is nonzero, and its only real poles outside the bands are the roots below. Monotonicity of \(3-z-kq_c(z)\) on each complementary interval excludes additional poles. In particular the plus denominator is negative at both sides of the upper edge, and the minus denominator is positive at both sides of the lower edge.

The atoms are explicitly algebraic:

\[
 E_+=3-\frac{2k_+}{2+\sqrt{3+4k_+}},\qquad
 E_-=3+\frac{2k_-}{2+\sqrt{3+4k_-}},\qquad
 Z_\sigma=[1+k_\sigma q'_{c_\sigma}(E_\sigma)]^{-1}. \tag{4}
\]

Here \(q'_c(E)=2[-1+|E-c|/\sqrt{(E-c)^2-1}]>0\). Numerically,

\[
\begin{split}
 E_+&\simeq2.958138050783261,& Z_+&\simeq0.9770252706124933,\\
 E_-&\simeq3.021177249193989,& Z_-&\simeq0.9880868665784739.
\end{split}
\]

## The normalized dressed pair and its actual perturbation source

Let \(u_\sigma=|e_\sigma e_\sigma\rangle\) be a normalized equal-parity two-boson memory state. The two forbidden double-memory states resolve into

\[
 q_e=\frac{|LL\rangle+|RR\rangle}{\sqrt2}
     =\frac{u_++u_-}{\sqrt2},\qquad
 q_o=\frac{|LL\rangle-|RR\rangle}{\sqrt2}
     =|e_+e_-\rangle. \tag{5}
\]

The physical pair is \(p=|LR\rangle=(u_+-u_-)/\sqrt2\). The uncompressed even operator is
\(A_e=d\Gamma_2(h_+)\oplus d\Gamma_2(h_-)\). Put

\[
 L_\sigma(z)=\iint\frac{d\mu_\sigma(u)d\mu_\sigma(v)}{u+v-z},\qquad
 L_+(E_p)+L_-(E_p)=0,
\]

\[
 \mathcal N^2=\frac{2}{L_+'(E_p)+L_-'(E_p)},\qquad
 \psi_g=\mathcal N(A_e-E_p)^{-1}q_e. \tag{6}
\]

The normalization in (6) includes the complete one-body atoms and continua. In the two symmetric spectral sectors the kernels are
\(\psi_\sigma(u,v)=\mathcal N/[\sqrt2(u+v-E_p)]\). Equation (6) solves the compressed hard-core eigenvalue equation because its forbidden component is zero at the root; its norm is one.

The physical operator \(V=n_L-n_R\) is the restriction of
\(d\Gamma(|e_+\rangle\langle e_-|+|e_-\rangle\langle e_+|)\).
It preserves the allowed hard-core subspace. Applying it to the two kernels in (6), with the normalized bosonic contraction factor \(\sqrt2\), gives the *exact* odd source

\[
 b(x,y):=(V\psi_g)(x,y)=\mathcal N W(x,y),\qquad
 W(x,y)=r_+(E_p-x)+r_-(E_p-y), \tag{7}
\]

in \(L^2(d\mu_+(x)d\mu_-(y))\). Every resolvent in (7) is evaluated off its own spectrum on the indicated supports and is real and bounded. Its forbidden overlap is exactly

\[
 \langle q_o,b\rangle=\mathcal N[L_+(E_p)+L_-(E_p)]=0. \tag{8}
\]

A bare-pair replacement would instead give \(Vp=0\) and incorrectly return zero response.

## The complete odd hard-core continuum

The uncompressed odd operator is multiplication by \(s=x+y\) on the full product measure. The physical odd operator is its compression to \(q_o^\perp\), with \(q_o(x,y)=1\). Denote the uncompressed resolvent by \(R_0(z)\), and set

\[
 D(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z},\qquad
 A(z)=\iint\frac{W(x,y)d\mu_+(x)d\mu_-(y)}{x+y-z},
\]

\[
 B(z)=\iint\frac{W(x,y)^2d\mu_+(x)d\mu_-(y)}{x+y-z}. \tag{9}
\]

Direct multiplication on \(q_o^\perp\), or a one-dimensional Schur complement, gives

\[
 (H_{\rm odd}-z)^{-1}
 =R_0(z)-R_0(z)|q_o\rangle D(z)^{-1}\langle q_o|R_0(z)
 \quad\text{on }q_o^\perp.
\]

Consequently the exact requested scalar resolvent is

\[
 \boxed{\langle b,(H_{\rm odd}-z)^{-1}b\rangle
       =\mathcal N^2\left[B(z)-\frac{A(z)^2}{D(z)}\right].} \tag{10}
\]

The square in (10) is the analytic square, not \(|A|^2\). This distinction is required by the resolvent identity.

For clarity, the full product measure in every integral (9) has all four pieces:

\[
\begin{split}
 D(z)={}&\frac{Z_+Z_-}{E_++E_--z}
 +Z_+\int_0^2\frac{a_-(y)}{E_++y-z}\,dy\\
 &+Z_-\int_4^6\frac{a_+(x)}{x+E_--z}\,dx
 +\int_4^6\int_0^2\frac{a_+(x)a_-(y)}{x+y-z}\,dy\,dx. \tag{11}
\end{split}
\]

The corresponding terms of \(A,B\) have the same weights multiplied by \(W,W^2\). Neither the nearby product atom nor the bound-plus-continuum channels have been deleted. The compression in (10), rather than removal of an atom from (11), imposes the odd hard-core condition. Possible odd discrete poles elsewhere are retained by the same expression.

## Existence and explicit on-shell density

The interval certificate below gives

\[
 5.9785<E_p<5.9787<E_++E_-,\qquad
 E_++E_-\simeq5.979315299977250. \tag{12}
\]

Thus the product atom is near the shell but is not on it. The two bound-plus-continuum channels have supports
\([E_+,E_++2]\) and \([E_-+4,E_-+6]\), both separated from \(E_p\). Only the continuum-continuum product contributes an imaginary part at the shell. Define

\[
 I=(\max(4,E_p-2),\min(6,E_p))=(4,E_p),\quad
 \nu(x)=a_+(x)a_-(E_p-x),
\]

\[
 W_s(x)=r_+(E_p-x)+r_-(x),\qquad
 \alpha=\frac{A(E_p+i0)}{D(E_p+i0)}. \tag{13}
\]

Each density in (3) is bounded, vanishes as a square root at its edges, and has integrable derivative. The functions \(W,W^2\) are smooth on the continuum product. Their sum-energy convolutions are locally Lipschitz. Therefore the three principal values in (9) exist and are finite at (12), by subtracting the value at the shell before taking the Hilbert transform. The atom and the other two channels have ordinary finite real values there. Moreover
\(\operatorname{Im}D(E_p+i0)=\pi\int_I\nu(x)dx>0\), so \(D\) cannot vanish.

Taking imaginary parts of (10) and using
\(\operatorname{Im}A=\pi\int_I\nu W_s\),
\(\operatorname{Im}B=\pi\int_I\nu W_s^2\), gives the actual continuum expression

\[
 \boxed{\displaystyle
 \rho(E_p)=\mathcal N^2\int_I a_+(x)a_-(E_p-x)
            \left|r_+(E_p-x)+r_-(x)-\alpha\right|^2dx.} \tag{14}
\]

The algebraic identity behind (14) is
\(\operatorname{Im}(A^2/D)=2\operatorname{Re}(A/D)\operatorname{Im}A
-|A/D|^2\operatorname{Im}D\). All factors in (14) are finite, proving finiteness of the requested limit. It is a continuum integral with an explicit odd-scattering correction, rather than a formal delta operator or a finite-chain peak.

The correction constant is itself obtained from one-dimensional complete-measure integrals:

\[
\begin{split}
 D(E_p+i0)&=\int r_-(E_p-x+i0)d\mu_+(x),\\
 A(E_p+i0)&=\int r_+(E_p-x)r_-(E_p-x+i0)d\mu_+(x)\\
 &\quad+\int r_-(E_p-y)r_+(E_p-y+i0)d\mu_-(y).
\end{split} \tag{15}
\]

Equations (1)–(6), (13)–(15) specify every object without an unknown continuum state or scattering oracle.

## Strict positivity: analytic proof

The function \(\nu\) is strictly positive in \(I\). If (14) vanished, its real analytic function \(W_s\) would equal the constant \(\alpha\) throughout \(I\). Both resolvents defining \(W_s\) are analytic on a real half-line containing \(I\) and extending to infinity: the transformed plus band and both bound poles lie below \(4\). Analytic continuation would make \(W_s\) constant on that half-line.

The complete one-body moments are
\(m_{0,\sigma}=1\), \(m_{1,\sigma}=3\), \(m_{2,\sigma}=9+k_\sigma\). Hence

\[
 W_s(x)=\frac{E_p-6}{x^2}
       +\frac{E_p(E_p-6)+(k_+-k_-)}{x^3}+O(x^{-4}). \tag{16}
\]

Its constant limit is zero, while (12) makes the first coefficient nonzero. Even without (12), if \(E_p=6\), the next coefficient would be \(k_+-k_-=g^2\ne0\). Thus \(W_s\) cannot be constant. The integral in (14) is strictly positive for **every** value of the scattering correction \(\alpha\).

Equivalently, if \(M=\int_I\nu\) and \(\overline W=M^{-1}\int_I\nu W_s\), then

\[
 \rho(E_p)=\mathcal N^2\left[
 \int_I\nu(W_s-\overline W)^2dx+M|\overline W-\alpha|^2\right], \tag{17}
\]

and the first term is positive. This proof does not depend on a numerically resolved peak or a numerically nonzero imaginary part.

## A quadrature-independent positive lower bound

`certify_positive.py` uses `mpmath.iv` at 50 decimal digits. The atom formulas (4) are evaluated with outward rounding. To enclose the root, split
\(F=L_++L_-=F_{aa}+C_++C_-\), where

\[
 F_{aa}(z)=\frac{Z_+^2}{2E_+-z}+\frac{Z_-^2}{2E_--z},
\]

\[
 0<C_+(z)\le\frac{2Z_+(1-Z_+)}{E_++4-z}
                  +\frac{(1-Z_+)^2}{8-z},
\]

\[
 0<-C_-(z)\le\frac{2Z_-(1-Z_-)}{z-E_--2}
                  +\frac{(1-Z_-)^2}{z-4}.
\]

The upper bound for \(F(5.9785)\) is below \(-0.00524427\); the lower bound for \(F(5.9787)\) exceeds \(0.02119993\). Strict monotonicity of \(F\) proves (12) with no quadrature assumption.

Take \(J_1=[4.1995,4.2005]\), \(J_2=[5.7995,5.8005]\). The same interval arithmetic certifies

\[
\begin{split}
 W_s(J_1)&\subset[-0.006948,-0.005389],\\
 W_s(J_2)&\subset[-0.001808,-0.001526],\\
 m_1:=\int_{J_1}\nu&>1.6619\times10^{-7},\quad
 m_2:=\int_{J_2}\nu>8.1443\times10^{-9},\\
 \mathcal N^2&>0.0041019.
\end{split}
\]

For the last inequality the derivative integrals in (6) are bounded above by atom contributions plus the same continuum masses divided by the squares of their minimum spectral distances. This is implemented explicitly in the certificate.

For any complex constant \(\alpha\), the contribution of these two intervals is at least

\[
 \int_{J_1\cup J_2}\nu|W_s-\alpha|^2dx
 \ge\frac{m_1m_2}{m_1+m_2}\,d^2,
\qquad d=\inf W_s(J_2)-\sup W_s(J_1)>0.
\]

This follows by minimizing over the two weighted means; within-interval variance is nonnegative. The expression increases with each positive mass, so their lower bounds suffice. The resulting lower bound for \(\rho\) exceeds \(4.0853\times10^{-16}\), and the program checks the simpler statement

\[
 \boxed{\rho(E_p)>4\times10^{-16}.} \tag{18}
\]

The bound is deliberately loose; its role is to certify positivity independently of the continuum quadrature and of \(\alpha\).

## Executed continuum evaluation

`continuum_response.py` computes the complete measures by Gauss-Chebyshev quadrature for the even pair and uses the exact analytic resolvents with adaptive one-dimensional continuum integration for (15) and (14). Endpoint substitutions remove square roots, and each internal threshold is split explicitly. There is no finite chain in this continuum calculation. Runs at 48/96/128 continuum nodes and 35/45/55 decimal digits agree at the reported precision; this convergence check is not a rigorous error enclosure for all displayed digits.

Representative values are

| Quantity | Continuum quadrature |
|---|---:|
| \(E_p\) | 5.978579315166579 |
| \(E_p-E_+-E_-\) | -0.0007359848106713624 |
| \(\mathcal N^2\) | 0.004115325359732575 |
| \(|\langle p,\psi_g\rangle|^2\) | 0.9625769954963076 |
| \(\|V\psi_g\|^2\) | 0.03704479062420688 |
| \(D(E_p+i0)\) | \(1311.698967434905+0.0005164396437468984i\) |
| \(A(E_p+i0)\) | \(-238.3001168660034-0.000002242629204153110i\) |
| \(\alpha\) | \(-0.1816728706678602+6.981818669959253\times10^{-8}i\) |
| \(\rho(E_p)\) | \(2.127506720615844\times10^{-8}\) |
| first term of (17) | \(1.505139222276562\times10^{-12}\) |

`check_operator_identities.py` separately builds the connected physical ladder at 4, 6 and 8 rungs per rail. At a nonreal spectral parameter it compares the physical Fock resolvent and source norm with (7) and (10); the largest scalar-resolvent discrepancy is below \(8\times10^{-16}\). This checks bosonic factors and the compression identity only; it is not evidence for an infinite on-shell peak.

The large real part of \(D\) comes principally from the *retained* nearby bound-bound atom in (11). The code checks the Plemelj imaginary parts of both \(D\) and \(A\) against their independent on-shell integrals, and checks (14) against the imaginary-part algebra of (10).

A discarded shortcut is worth recording: replacing the squares of the contracted resolvents in \(\|V\psi_g\|^2\) by \(L_+'+L_-'\) is invalid. The correct norm is
\(\mathcal N^2[\int r_+(E_p-x)^2d\mu_+(x)+\int r_-(E_p-y)^2d\mu_-(y)+2L_+(E_p)L_-(E_p)]\), used in the code. An initially attempted certificate \(\rho>10^{-15}\) was also too strong for the chosen tiny intervals; the interval computation yields the valid (18). Neither failed shortcut enters the conclusion.

## Coefficient, conditional decay law and remaining obligations

The result proved here is the exact positive finite **spectral coefficient** (14). For a static perturbation \(H+\eta V\), the first-order pair energy shift vanishes by parity. If an appropriate resonance expansion is established, the second-order imaginary energy shift is \(-\pi\eta^2\rho(E_p)\), and the corresponding probability linewidth would be
\(\Gamma=2\pi\eta^2\rho(E_p)+o(\eta^2)\). This is a conditional convention-dependent interpretation, not a proved finite-time survival law. A temporal noise process needs its actual power spectrum and generally the response away from \(E_p\) as well.

There is no remaining gap in the finite/positive/zero/singular classification for the declared model and \(g=1/5\). A rigorous tight numerical enclosure of the decimal coefficient would require a validated quadrature for (15) and (14). A resonance theorem, controlled finite-time errors, fabrication mapping, noise spectrum, control costs and an experimental gate advantage have not been acquired. The next mathematical attack is a weighted limiting-absorption/analytic-continuation argument for the full \(H+\eta V\) family, with the already explicit coefficient as input.
