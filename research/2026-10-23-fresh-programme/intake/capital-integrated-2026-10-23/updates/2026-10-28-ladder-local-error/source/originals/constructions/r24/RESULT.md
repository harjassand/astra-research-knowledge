# Local parity-breaking spectral response

For the exact infinite ladder in `../packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, with \(g=1/5\), the requested quantity is **finite and strictly positive**. A direct infinite-measure quadrature gives

\[
\boxed{\rho_{1/5}(E_p)\simeq 2.12750672\times10^{-8}}.
\]

The strict sign and finiteness are proved analytically below; the displayed decimal is an ordinary, non-interval-certified numerical approximation. The proof in fact applies to every \(0<g\leq0.4\) for which the source packet's even-sector gap bounds hold. This is a spectral-density statement, not by itself a resonance or lifetime theorem. It is not a claim of external novelty, an experiment, or a device advantage.

## Complete one-particle data and the exact pair

Write \(e_\pm=(L\pm R)/\sqrt2\), and let \(\mu_\pm\) be their **complete** spectral measures for the two one-particle Jacobi matrices. Put \(c_+=5,c_-=1\), \(\lambda_+=2g^2,\lambda_-=g^2\). Let

\[
M_c(z)=2\bigl(z-c-\sqrt{(z-c)^2-1}\bigr),\qquad
s_\sigma(z)=\int\frac{d\mu_\sigma(u)}{u-z}
=-\frac1{z-3-\lambda_\sigma M_{c_\sigma}(z)},
\]

where the square root is chosen asymptotic to \(z-c\) at infinity. For \(x\) in the corresponding band, the density is

\[
u_\sigma(x)=\frac{2\lambda_\sigma\sqrt{1-(x-c_\sigma)^2}}
{\pi\left[(x-3-2\lambda_\sigma(x-c_\sigma))^2+4\lambda_\sigma^2(1-(x-c_\sigma)^2)\right]}.
\tag{1}
\]

Each measure consists of this entire band density plus exactly one atom \(w_\sigma\delta_{e_\sigma}\); no other atom or singular part occurs for \(g\leq0.4\). This follows directly from the monotone outside-band scalar Schur equation: for example the plus determinant is positive throughout \((6,\infty)\), while the minus determinant is negative throughout \(( -\infty,0)\).

The two atoms can be described without numerical root assumptions. Define

\[
h(d)=\frac{2}{2+d+\sqrt{(2+d)^2-1}},\quad
 d_\sigma=\lambda_\sigma h(d_\sigma),\quad
 e_+=3-d_+,\quad e_-=3+d_-,\quad
 w_\sigma=\left(1+\frac{d_\sigma}{\sqrt{(2+d_\sigma)^2-1}}\right)^{-1}.
\tag{2}
\]

For \(g=1/5\), the exact inequalities \(d_+<0.04288\), \(d_-<0.02144\) follow from \(h(d)<h(0)<0.536\). Hence the even atom-band and band-band sums are separated from \((2e_+,2e_-)\). Define, including every atom and continuum piece,

\[
 L_\sigma(z)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-z},\qquad
 L_+(E)+L_-(E)=0,\quad 2e_+<E<2e_-,\quad
 D=L_+'(E)+L_-'(E)>0.
\tag{3}
\]

The sum in (3) is strictly increasing from \(-\infty\) to \(+\infty\); \(E=E_p\) is the unique even hard-core pair energy. For an independent check of normalization, the exact state in the harmonic two-boson even sector is

\[
 \psi_g=\frac{(h_+^{(1)}+h_+^{(2)}-E)^{-1}|2+\rangle+
 (h_-^{(1)}+h_-^{(2)}-E)^{-1}|2-\rangle}{\sqrt D}.
\tag{4}
\]

Here \(|2\sigma\rangle\) means two normalized excitations in memory orbital \(e_\sigma\). Formula (3) makes (4) orthogonal to the forbidden even double-memory state \((|LL\rangle+|RR\rangle)/\sqrt2=(|2+\rangle+|2-\rangle)/\sqrt2\); thus (4) is the physical normalized pair, not a bare-pair approximation.

## Exact odd-sector reduction and shell integral

The harmonic odd two-particle sector is \(\mathcal H_+\otimes\mathcal H_-\), with Hamiltonian \(K=h_+\otimes1+1\otimes h_-\). Its single forbidden physical hard-core direction is
\[
 d=(|LL\rangle-|RR\rangle)/\sqrt2=e_+\otimes e_-.
\]
The actual odd operator is \(P K P\) on \(d^\perp\), \(P=1-|d\rangle\langle d|\). The uncompressed number difference \(\widetilde V\) satisfies \(\widetilde V d=2(|LL\rangle+|RR\rangle)/\sqrt2\). Thus (4) implies \(\widetilde V\psi_g\in d^\perp\), and the physical source \(f=V\psi_g\) equals that vector.

In the cyclic spectral representation of the two endpoint orbitals, the harmonic odd space is \(L^2(d\nu)\), \(d\nu(x,y)=d\mu_+(x)d\mu_-(y)\); \(d\) is the constant function 1. The physical source is the **dressed** function

\[
 f(x,y)=\sqrt{\frac{2}{D}}B(x,y),\qquad
 B(x,y)=s_+(E-x)+s_-(E-y),
\tag{5}
\]

with the Stieltjes transforms in (5) real: all denominators lie outside the even-sector sums. In particular, \(\int B\,d\nu=L_+(E)+L_-(E)=0\), independently confirming \(f\in d^\perp\).

For \(\operatorname{Im}z>0\), define the complete transforms

\[
G(z)=\iint\frac{d\nu}{x+y-z},\quad
J(z)=\iint\frac{B(x,y)\,d\nu}{x+y-z},\quad
K_B(z)=\iint\frac{B(x,y)^2\,d\nu}{x+y-z},\quad
Q(z)=\frac{J(z)}{G(z)}.
\tag{6}
\]

All four combinations of one-body atom and band measures occur in these transforms. The odd hard-core constraint gives the exact bounded-operator block-inverse identity

\[
\langle f,(PKP-z)^{-1}f\rangle
=\frac{2}{D}\left[K_B(z)-\frac{J(z)^2}{G(z)}\right].
\tag{7}
\]

For \(z=E+i\epsilon\), (7) has the equivalent manifestly nonnegative expression

\[
\frac1\pi\operatorname{Im}\langle f,(PKP-E-i\epsilon)^{-1}f\rangle
=\frac{2}{\pi D}\iint\frac{\epsilon\,|B(x,y)-Q(E+i\epsilon)|^2}
{(x+y-E)^2+\epsilon^2}\,d\nu(x,y).
\tag{8}
\]

This identity is exact at every \(\epsilon>0\). At the pair energy the two atom-band channels are off shell: their supports are \([e_+,e_++2]\) and \([e_-+4,e_-+6]\). Only band-band states reach \(E\). Set

\[
 I_E=[\max(4,E-2),\min(6,E)],\qquad
 Q_* =\lim_{\epsilon\downarrow0}Q(E+i\epsilon).
\]

The desired limiting absorption response is therefore the explicit continuum expression

\[
\boxed{\displaystyle
\rho_g(E)=\frac{2}{D}\int_{I_E}u_+(x)u_-(E-x)
\left|s_+(E-x)+s_-(x)-Q_*\right|^2\,dx.}
\tag{9}
\]

Although the on-shell integration in (9) is band-band, \(Q_*\), \(D\), and \(E\) retain all bound and continuous pieces. Dropping the hard-core term is not harmless here: the numerical calculation with \(Q_*=0\) gives approximately \(1.4262\times10^{-11}\), about 1,492 times smaller than (9). Replacing the actual pair by the bare \(|LR\rangle\) is even more drastic, because \(V|LR\rangle=0\) exactly.

## Proof that the limit exists and is strictly positive

The product of the two band densities is strictly positive on the interior of \(I_E\). Their energy-sum convolution and the same convolution weighted by the continuous bounded function \(B\) are locally Hölder continuous. Thus their Cauchy transforms have finite upper-rim values by the elementary Plemelj formula; the atom-band terms are analytic there. If \(E\ne e_++e_-\),
\[
 \operatorname{Im}G(E+i0)=\pi\int_{I_E}u_+(x)u_-(E-x)\,dx>0,
\]
so \(Q_*\) exists and is finite. If instead \(E=e_++e_-\), the common atom-atom pole occurs in both \(J\) and \(G\), and their quotient tends to \(B(e_+,e_-)\). Its contribution to (8) still vanishes in the limit because \(B(e_+,e_-)-Q(E+i\epsilon)=O(\epsilon)\). Consequently (9) exists and is finite in either case; the proof does **not** depend on assuming a nonzero connected shift.

It remains to show the integrand in (9) cannot vanish almost everywhere. In a connected complex domain containing the shell interval, define
\[
 F(z)=s_+(E-z)+s_-(z).
\]
It has isolated possible atom poles at \(z_1=E-e_+\) and \(z_2=e_-\), both above the lower band and the reflected upper band. If they are distinct, their respective residues are \(w_+\) and \(-w_-\), so a pole is nonremovable. If they coincide, the residue is \(w_+-w_-\). It too is nonzero: \(h(d)\) is strictly decreasing, \(d/h(d)\) is strictly increasing, and \(\lambda_+>\lambda_-\) imply \(d_+>d_-\); equation (2) then gives \(w_+<w_-\), since \(d/\sqrt{(2+d)^2-1}\) is strictly increasing. Hence \(F\) has a nonremovable pole in either case. By the identity theorem it cannot be constant on any open shell interval. Since \(u_+(x)u_-(E-x)>0\) there, (9) is **strictly positive**, even if \(Q_*\) happened to be real. This proves the requested sign analytically.

Only standard imports are used: the spectral theorem for the bounded Jacobi operators, block inversion, the identity theorem, and the Plemelj boundary formula for Hölder continuous scalar densities. No global operator-norm limiting-absorption estimate is assumed. The scalar limiting absorption needed for the stated matrix element is established above. Rank-one resolvent identities are standard background; see [Choroszavin, *Notes on Rank-One Perturbed Resolvent*](https://arxiv.org/abs/math-ph/0312016).

## Numerical checks and limits of interpretation

The two independently implemented infinite-measure quadratures give

\[
\begin{aligned}
 e_+&\simeq2.95813805078326,& e_-&\simeq3.02117724919399,\\
 E&\simeq5.97857931516658,& D&\simeq485.98830594769,\\
 Q_*&\simeq -0.18167287066786+6.98181867\times10^{-8}i,&
 \|V\psi_g\|^2&\simeq0.0370447906242.
\end{aligned}
\]

`response.py` uses SciPy one-dimensional continuum quadrature, including atom terms; `high_precision.py` uses separate arbitrary-precision mpmath expressions. Their output files are `response.json` and `high_precision.json`. `finite_fock_audit.py` builds local \(L,R\) hard-core Fock matrices independently and compares the directly computed finite-\(\epsilon\) response and source norm with the reduced formula, for 4, 8, and 12 sites per rail and three regulators. The maximum reported relative response discrepancy is below \(3.1\times10^{-14}\); output is in `finite_fock_audit.json`. This checks factors and the physical hard-core projection, but finite chains and finite regulators do not prove the continuum limit or certify the decimal.

Conditional Fermi-golden-rule interpretation: **if** an applicable resonance theorem establishes the required perturbation and reduced-resolvent regularity for \(H_g+\eta V\), the amplitude pole has the formal expansion \(E_{\rm res}=E+\eta^2\Delta-i\pi\eta^2\rho_g(E)+o(\eta^2)\). With \(\hbar=1\), the amplitude decay exponent/HWHM is \(\pi\eta^2\rho_g(E)\); the probability decay rate and energy FWHM are \(2\pi\eta^2\rho_g(E)\simeq1.33675\times10^{-7}\eta^2\). Such a theorem and uniform-in-time decay bounds have **not** been established here. The rank-one-perturbation resonance results of [Bourget et al.](https://arxiv.org/abs/1707.01597) illustrate the extra hypotheses needed; they are not invoked as a theorem for this non-rank-one perturbation.

The remaining mathematical obligation for a dynamical claim is to prove an applicable resonance/decay theorem for the full bounded perturbation \(V\) and establish its error and time range. For the current fixed-\(g\) density question, the sign and finiteness are closed; interval certification of the displayed decimal would strengthen the numerical evidence but is not needed for those analytic conclusions.
