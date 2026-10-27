# Spectral response to local parity breaking

## Result

For the precise ladder and hard-core memories in
`packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, let
\(g=1/5\), \(V=n_L-n_R\), and let \(E=E_p(g)\) and \(\psi\) denote the
normalized even bound-pair branch defined there. The limit in the question
exists and satisfies

\[
  0<\rho_g(E)<\infty.
\]

An exact one-dimensional shell integral is given in (9) below; the scalar in
its integrand is defined using the **complete** one-body spectral measures,
including their atoms.  Its floating-point evaluation is
\(\rho_{1/5}(E_p)\simeq 2.1275067206\times10^{-8}\) in the units of the
packet. The classification is analytical; the displayed decimal is an
uncertified numerical diagnostic, not an interval bound.

The argument uses the packet's isolated even-pair root and one-body band
locations. The only general imports are the spectral theorem for bounded
self-adjoint operators and the scalar Poisson-kernel / Sokhotski–Plemelj
boundary formula for Hölder densities. The needed boundary regularity is
verified below; no global two-particle limiting-absorption theorem, resonance
theorem, finite-chain extrapolation, or replacement of the pair by \(|LR\rangle\)
is used.

## Complete one-body data and the dressed source

Write \(e_\pm=(|L\rangle\pm|R\rangle)/\sqrt2\). Let \(h_\pm\) be the
one-particle parity-channel operators and \(\mu_\pm\) their spectral measures
at \(e_\pm\). Set
\[
  m_\sigma(z)=\int\frac{d\mu_\sigma(t)}{t-z},\qquad
  L_\sigma(E)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-E}.
\]
The packet establishes the unique pair root \(L_+(E)+L_-(E)=0\) between
\(2E_+\) and \(2E_-\), with \(5.6<E<6.2\), and
\(2.8<E_+<3<E_-<3.1\). Define the positive finite normalization
\[
  D=L_+'(E)+L_-'(E),\qquad C=\sqrt{2/D}. \tag{1}
\]

The following expressions make the complete measures explicit. For
\(c_+=5,c_-=1\) and \(k_+=2/25,k_-=1/25\), let
\[
 r_c(z)=2\{c-z+\sqrt{(z-c)^2-1}\},\qquad
 m_\sigma(z)=\frac{1}{3-z-k_\sigma r_{c_\sigma}(z)}, \tag{2}
\]
where the square root is analytic off \([c-1,c+1]\) and behaves as \(z-c\)
at infinity. For real \(z<c-1\), it is the negative square root; for real
\(z>c+1\), it is the positive square root. At the upper edge of the cut it
has positive imaginary part. Each complete measure consists of one atom and
one band:
\[
 d\mu_\sigma(x)=w_\sigma\,\delta_{E_\sigma}(dx)
                   +\varrho_\sigma(x)\,dx,\qquad
 w_\sigma=\frac1{1+k_\sigma r'_{c_\sigma}(E_\sigma)}, \tag{3}
\]
\[
 \varrho_\sigma(x)=\frac{2k_\sigma\sqrt{1-(x-c_\sigma)^2}}
 {\pi[(3-x-2k_\sigma(c_\sigma-x))^2
       +4k_\sigma^2(1-(x-c_\sigma)^2)]}
\quad (|x-c_\sigma|<1), \tag{4}
\]
and zero off the band. Here \(E_\sigma\) is the unique zero of the denominator
of (2) in the gap. There are no additional atoms: the denominator is strictly
decreasing on each real gap, its signs at the exterior bath edges exclude
exterior roots for these \(k_\sigma\), and the gap root is unique. Thus (3)
is complete, not a continuum-only approximation.

To construct the actual source, begin temporarily in the harmonic two-boson
space and put \(q_\sigma=|e_\sigma e_\sigma\rangle\) with unit norm,
\(A_\sigma=h_\sigma\otimes 1+1\otimes h_\sigma\) on the symmetric
two-boson sector, and \(\phi_\sigma=(A_\sigma-E)^{-1}q_\sigma\). The even
forbidden double-memory vector is \((q_++q_-)/\sqrt2\). Therefore the exact
physical eigenvector is
\[
 \psi=\frac{\phi_++\phi_-}{\sqrt D}. \tag{5}
\]
Indeed its forbidden overlap is \((L_++L_-)/\sqrt{2D}=0\), its norm is
one because \(\|\phi_\sigma\|^2=L_\sigma'(E)\), and
\((A-E)\psi\) is proportional to the forbidden vector. Its bare-pair
overlap is nonzero, so it is the pair branch in the packet.

In the odd sector the free harmonic operator is
\(A=h_+\otimes1+1\otimes h_-\). Identifying this sector with
\(L^2(\mu_+)\otimes L^2(\mu_-)\), the forbidden double-memory vector is
the constant function \(q(x,y)=1\). Since
\(V=d\Gamma(|e_+\rangle\langle e_-|+|e_-\rangle\langle e_+|)\), applying
it to (5) gives exactly
\[
 (V\psi)(x,y)=C\,u(x,y),\qquad
 u(x,y)=m_+(E-x)+m_-(E-y). \tag{6}
\]
This includes the complete dressing of \(\psi\). Also
\(\langle q,u\rangle=L_+(E)+L_-(E)=0\), so the source lies in the allowed
odd hard-core subspace \(q^\perp\).

## Rank-one hard-core resolvent and continuum formula

Put \(Q=1-|q\rangle\langle q|\). The physical odd Hamiltonian is
\(H_{g,\mathrm{odd}}=QAQ|_{q^\perp}\). For \(\Im z>0\), set
\[
 M(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
 J(z)=\iint\frac{u(x,y)d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
 F(z)=\iint\frac{u(x,y)^2d\mu_+(x)d\mu_-(y)}{x+y-z}. \tag{7}
\]
Here the real-valued \(u\) is fixed at the pair energy \(E\); it does not
depend on \(z\). The rank-one compression identity yields
\[
 \langle V\psi,(H_{g,\mathrm{odd}}-z)^{-1}V\psi\rangle
 = C^2\left[F(z)-\frac{J(z)^2}{M(z)}\right]. \tag{8}
\]
It follows by solving \((A-z)w=f+\lambda q\) with \(w\perp q\). All
atom–atom, atom–band and band–band terms in (7) are retained.

Let
\[
 \alpha=\lim_{\epsilon\downarrow0}\frac{J(E+i\epsilon)}{M(E+i\epsilon)},
 \qquad I=[\max(4,E-2),\min(6,E)].
\]
Then the requested density is the explicit infinite-volume expression
\[
 \boxed{\displaystyle
 \rho_g(E)=\frac{2}{D}\int_I\!
  \varrho_+(x)\varrho_-(E-x)
  \left|m_+(E-x)+m_-(x)-\alpha\right|^2\,dx.} \tag{9}
\]
The integral is over the actual opposite-band two-particle shell. The scalar
\(\alpha\) includes all bound and continuum pieces in (7); dropping them
changes the answer.

For any \(z=E+i\epsilon\), direct algebra gives the positive identity
\[
 \Im\left(F-\frac{J^2}{M}\right)
 =\iint\frac{\epsilon\,|u(x,y)-J/M|^2}
 {(x+y-E)^2+\epsilon^2}\,d\mu_+(x)d\mu_-(y). \tag{10}
\]
The atom–band thresholds lie below 5.1 or above 6.8, whereas
\(5.6<E<6.2\); hence only the band–band part is continuously on shell.
The one-body density (4) has square-root edge behavior and no in-band poles,
and \(u\) is smooth on each support component because \(E\) is in the even
spectral gap. Thus the weighted band–band convolution is Hölder at \(E\),
and the imported scalar boundary formula applies. Its integral on the open
shell is strictly positive for \(M\), so \(M(E+i0)\ne0\) whenever the
bound–bound sum is not exactly \(E\).

For completeness, the proof does not need to assume that the bound–bound sum
differs from \(E\). If they coincide, the atom gives \(M\sim w_+w_-/(E-z)\)
and \(J\sim u(E_+,E_-)w_+w_-/(E-z)\), so
\(\alpha=u(E_+,E_-)\); the remaining terms have finite boundary values. In
(10), the atom's contribution then vanishes in the limit. This also rules out
an uncancelled delta contribution at the coincident atom in this source
response. Consequently (9) is valid in either case. In the numerical
calculation the difference is approximately \(7.36\times10^{-4}\).

## Strict positivity, without a numerical sign test

On the open shell write
\[
 U(x)=m_+(E-x)+m_-(x).
\]
The band densities are strictly positive on its interior, which is a
nonempty interval since \(4<E<8\). The analytic function \(U\) extends from
that interval to every real \(x>\max(E-E_+,E_-)\): the arguments \(E-x\) and
\(x\) lie respectively below the complete spectrum of \(h_+\) and above the
complete spectrum of \(h_-\). This interval contains the entire shell.

The endpoint measures have first moment 3 and second moments \(9+k_+\) and
\(9+k_-\). Their resolvent expansion at infinity is therefore
\[
 U(x)=\frac{E-6}{x^2}
       +\frac{E^2-6E+k_+-k_-}{x^3}+O(x^{-4}). \tag{11}
\]
If \(U\) were constant on an open shell interval, analyticity and
\(U(x)\to0\) would make it identically zero on the whole connected interval.
For \(E\ne6\), the coefficient of \(x^{-2}\) contradicts this. For \(E=6\),
the coefficient of \(x^{-3}\) is \(k_+-k_-=1/25\ne0\). Hence \(U\) is
not constant on the open shell. No scalar \(\alpha\), real or complex, can
make the integrand in (9) vanish almost everywhere. The integral is therefore
strictly positive. Boundedness of the shell integrand and \(D>0\) prove
finiteness.

## Numerical check and interpretation

`spectral_response.py` computes the boundary through explicit Cauchy principal
values and also performs a finite local hard-core Fock-space check. The
independent `high_precision.py` uses one-dimensional endpoint resolvent
integrals, retaining all atoms, and 45-digit `mpmath` arithmetic. Both give
\(E\simeq5.97857931516658\), \(D\simeq485.98830594769\),
\(\alpha\simeq-0.181672870668+6.98182\times10^{-8}i\), and the response
quoted above. The approximately \(1.3\times10^3\) real part of \(M\) is
dominated by the nearby bound–bound term, illustrating why it cannot be
discarded. The direct local Fock check, at four bath sites per rail, verifies
the exact finite-chain pair energy, source norm, and complex odd resolvent
against the reduction to about \(2\times10^{-15}\); it is a normalization
check, not the continuum argument. Numerical outputs and reproducible
commands are in `RESULT.md`.

If one separately establishes a suitable weak-\(\eta\) resonance/Fermi
golden rule expansion for \(H_g+\eta V\), the formal energy pole has imaginary
part \(-\pi\eta^2\rho_g(E)+o(\eta^2)\). With \(\hbar=1\), the formal
population decay rate and energy full width at half maximum are both
\(\Gamma=2\pi\eta^2\rho_g(E)+o(\eta^2)\); the amplitude decay rate and
energy half width at half maximum are \(\Gamma/2\). Numerically the formal
coefficient of \(\eta^2\) in \(\Gamma\) is about
\(1.3367518968\times10^{-7}\). This work does not prove a resonance pole,
an exponential survival law, a physical-device lifetime, or a practical gate
advantage.
