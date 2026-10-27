# Local memory detuning opens a strictly positive pair spectral response

The Hamiltonian and units are those of the supplied
`../packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, sections 2–3:
\(\hbar=1\), memory energy 3, bath centers 5 and 1, bath hopping magnitude
\(1/2\), and endpoint couplings \(\sqrt2g\) and \(g\). This note addresses
the actual perturbation \(V=n_L-n_R\), not the packet's additional
parity-preserving wrong-band source. No device or historical-priority claim
is made.

**Result.** For the normalized exact hard-core even pair \(\psi_g\),
\[
 0<\rho_g(E_p)<\infty\qquad(0<g\leq0.4).
\]
In particular this settles the requested fixed value \(g=1/5\). The
classification follows analytically below, independently of numerical
error estimates. Continuum quadrature gives
\[
 E_p(1/5)\simeq5.978579315166578,\qquad
 \rho_{1/5}(E_p)\simeq2.12750672152\,10^{-8}.
\]
These displayed decimal values are ordinary floating-point continuum
quadratures, not certified decimal enclosures.

## 1. Complete one-body measures

Write \(a_+=2g^2\), \(a_-=g^2\), \(c_+=5\), \(c_-=1\). Use the
resolvent convention
\[
 M_\sigma(z)=\langle e_\sigma,(h_\sigma-z)^{-1}e_\sigma\rangle.
\]
The half-line Schur recursion is
\(s_c(z)=\{c-z-\tfrac14s_c(z)\}^{-1}\). Choosing the solution
asymptotic to \(-1/z\), and then taking the memory Schur complement, gives
\[
 s_c(z)=2\{c-z+\sqrt{(z-c)^2-1}\},\qquad
 M_\sigma(z)=\frac1{3-z-a_\sigma s_{c_\sigma}(z)}. \tag{1}
\]
The square root is the branch asymptotic to \(z-c\) at infinity; its
imaginary part is positive in the upper half-plane. Consequently
\[
 d\mu_\sigma(x)=w_\sigma\delta_{b_\sigma}(dx)+r_\sigma(x)\,dx, \tag{2}
\]
where
\[
 \begin{split}
 3-b_\sigma-a_\sigma s_{c_\sigma}(b_\sigma)&=0,\\
 w_\sigma&=\{1+a_\sigma s'_{c_\sigma}(b_\sigma)\}^{-1},\\
 r_\sigma(x)&=
 \frac{2a_\sigma\sqrt{1-(x-c_\sigma)^2}}
 {\pi\{[3-x+2a_\sigma(x-c_\sigma)]^2
       +4a_\sigma^2[1-(x-c_\sigma)^2]\}}
 \mathbf1_{|x-c_\sigma|<1}. \tag{3}
 \end{split}
\]
In particular both densities are strictly positive in their band interiors.

These are the complete measures. To see that no other bound atoms were
deleted, the denominator in (1) decreases strictly on each interval
outside the band. For the plus channel it has one zero below 4 and no
zero above 6, since its value at \(6+\) is \(-3+2a_+<0\).
For the minus channel it has no zero below 0, since its value at \(0-\)
is \(3-2a_->0\), and one zero above 2. There are no edge zeros.
The explicit square-root function (1) has no other singular spectral
piece. Direct endpoint bounds give
\[
 2.8<b_+<3<b_-<3.1\quad(0<g\leq0.4).
\]
All Jacobi off-diagonal entries are nonzero, so the memory endpoint is
cyclic in each one-body channel, and multiplication on \(L^2(\mu_\sigma)\)
represents the entire one-body space.

## 2. Exact dressed pair and its detuning source

Let \(K_\sigma=h_\sigma\otimes1+1\otimes h_\sigma\) on the symmetric
same-channel two-boson space, and let \(|\sigma\sigma\rangle\) be the
normalized double-memory harmonic state. The even forbidden vector is
\[
 q_e=\frac{|++\rangle+|--\rangle}{\sqrt2},
\]
whereas the allowed bare memory pair is
\(p=(|++\rangle-|--\rangle)/\sqrt2\).
Set
\[
 L_\sigma(E)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(t)}{x+t-E}.
\]
Between \(2b_+\) and \(2b_-\), the sum \(L_++L_-\) increases strictly
from \(-\infty\) to \(+\infty\). Its unique root is the exact pair
energy \(E=E_p\). All same-parity continuous supports avoid
\((5.6,6.2)\): the closest bound-plus-continuum bands end below 5.1 or
start above 6.8. Thus the integrals below are real and have no hidden
principal-value prescription. In particular \(5.6<E<6.2\).

Define
\[
 C=\left[\frac{2}{L'_+(E)+L'_-(E)}\right]^{1/2}>0.
\]
The normalized even eigenvector, including its complete bath dressing,
has spectral wavefunctions
\[
 \psi_\sigma(x,t)=\frac{C}{\sqrt2}\frac1{x+t-E}. \tag{4}
\]
Indeed this is the harmonic resolvent applied to \(q_e\), normalized by
its squared norm \((L'_++L'_-)/2\); the hard-core constraint is precisely
\(L_+(E)+L_-(E)=0\). Since \((K_+\oplus K_--E)\psi=Cq_e\),
compression to \(q_e^\perp\) makes (4) an exact eigenvector.
Its bare-pair weight is
\(C^2L_+(E)^2\), agreeing with the packet's residue.

The odd harmonic space contains one plus and one minus boson and is
\(L^2(\mu_+\otimes\mu_-)\). Its only forbidden memory vector is
\[
 q_o=|+ -\rangle
     =\frac{|LL\rangle-|RR\rangle}{\sqrt2}.
\]
It is represented by the constant function 1. The physical odd space
is \(Q=q_o^\perp\), and the exact odd hard-core Hamiltonian is
\[
 H_{g,\mathrm{odd}}=QKQ\big|_Q,\qquad
 (Ku)(x,y)=(x+y)u(x,y). \tag{5}
\]

In parity coordinates
\(V=d_+^\dagger d_-+d_-^\dagger d_+\), where \(d_\pm\) annihilate
only the memory modes (distinct from the coupling squares \(a_\sigma\)).
Applying it to (4), including the bosonic \(\sqrt2\) factor, yields
\[
 f(x,y):=(V\psi_g)(x,y)
  =C\{M_+(E-x)+M_-(E-y)\}. \tag{6}
\]
Here both functions in braces are real and bounded on their respective
one-body supports because \(E\) is in the even-sector gap. Moreover
\[
 \langle q_o,f\rangle
  =C\{L_+(E)+L_-(E)\}=0,
\]
so (6) is already in the exact physical odd space. Replacing (4) by
the bare pair would be fatal: \(Vp=0\) exactly and would incorrectly
produce zero response.

## 3. Exact odd hard-core resolvent and continuum expression

Put \(d\nu(x,y)=d\mu_+(x)d\mu_-(y)\), and for \(\operatorname{Im}z>0\)
define
\[
 D(z)=\int\frac{d\nu}{x+y-z},\quad
 B(z)=\int\frac{f\,d\nu}{x+y-z},\quad
 A(z)=\int\frac{f^2\,d\nu}{x+y-z}.
\]
The block inverse relative to \(\operatorname{span}\{q_o\}\oplus Q\)
gives the exact compression identity
\[
 \langle f,(H_{g,\mathrm{odd}}-z)^{-1}f\rangle
  =A(z)-\frac{B(z)^2}{D(z)}. \tag{7}
\]
It is \(B^2\), not \(|B|^2\), in this analytic resolvent formula.
The positivity of \(\operatorname{Im}D\) ensures the division is valid
in the upper half-plane.

Let \(\alpha(z)=B(z)/D(z)\). Directly taking imaginary parts in (7)
gives the useful exact identity, for \(z=E+i\epsilon\),
\[
 \frac1\pi\operatorname{Im}\langle f,(H_{g,\mathrm{odd}}-z)^{-1}f\rangle
  =\iint\frac{\epsilon\,|f(x,y)-\alpha(z)|^2}
                 {\pi[(x+y-E)^2+\epsilon^2]}\,d\nu(x,y). \tag{8}
\]
This is a positive formula at every \(\epsilon>0\), not an interference
ansatz or a projected-pair approximation.

The scalar boundary quantities needed in (8) have one-dimensional
complete-measure formulas:
\[
 \begin{split}
 D(E+i0)&=\int d\mu_+(x)\,M_-(E-x+i0),\\
 B(E+i0)&=C\left\{
 \int d\mu_+(x) M_+(E-x)M_-(E-x+i0)
 +\int d\mu_-(y) M_-(E-y)M_+(E-y+i0)
 \right\}. \tag{9}
 \end{split}
\]
In (9), **each integral includes its bound atom** from (2).

Except for the harmless exceptional case treated below, put
\(\alpha_E=B(E+i0)/D(E+i0)\). Then the requested continuum expression is
\[
 \boxed{
 \rho_g(E)=\int_{I_E}r_+(x)r_-(E-x)
  \left|C\{M_+(E-x)+M_-(x)\}-\alpha_E\right|^2\,dx,
 } \tag{10}
\]
where
\[
 I_E=(\max(4,E-2),\min(6,E)).
\]
This interval is nonempty. Only the continuous-continuous piece is
on shell. The bound-continuous and bound-bound pieces still affect
\(E,C,f,D,B,\alpha_E\); deleting them changes (10). In particular the
large real value of \(D\) in the numerical result below comes mainly
from the nearby odd harmonic bound-bound pole.

## 4. Boundary limit exists and is finite

No many-body limiting-absorption theorem is assumed. Here is a direct
proof of the specific scalar limit requested.

For \(x\in[4,6]\), the arguments \(E-x\) in (9) belong to
\([-0.4,2.2]\), away from the minus atom \(b_->3\). Likewise, for
\(y\in[0,2]\), \(E-y\in[3.6,6.2]\), away from the plus atom
\(b_+<3\). The explicit functions (1) are bounded up to the band edges
on these compact intervals. The continuous integrals in (9) therefore
have finite limits by dominated convergence. If
\(E\ne e_{bb}:=b_++b_-\), their atomic terms are also finite, and
\[
 \operatorname{Im}D(E+i0)
   =\pi\int_{I_E}r_+(x)r_-(E-x)\,dx>0. \tag{11}
\]
Thus \(\alpha_E\) is a finite number.

The complete product measure has four types of contributions: one atom
at \(e_{bb}\), two bound-continuous bands below 5.1 or above 6.8, and
the continuous-continuous band \([4,8]\). The first three are off shell
when \(E\ne e_{bb}\), so their contributions in (8) vanish as
\(\epsilon\downarrow0\). The weighted continuous-continuous density
is continuous at \(E\): it is an integral of bounded smooth source
factors against two continuous compactly supported densities with
square-root edge behavior. The elementary Poisson approximate-identity
limit in (8) is therefore exactly (10). Its integrand is bounded and
integrable, proving finiteness.

For completeness the classification does not need a numerical
assumption that the connected shift is nonzero. If \(E=e_{bb}\), then
\[
 D(E+i\epsilon)=\frac{i w_+w_-}{\epsilon}+O(1),\qquad
 B(E+i\epsilon)=\frac{i w_+w_- f(b_+,b_-)}{\epsilon}+O(1).
\]
Set \(\alpha_E=f(b_+,b_-)\) in (10). The ratio \(\alpha(E+i\epsilon)\)
converges to this finite value with error \(O(\epsilon)\), so the
atom's term in (8) is \(O(\epsilon)\), not singular. The same
continuous integral (10) remains the limit. Hence the possible free
bound-bound coincidence cannot obstruct the result.

The only general mathematical ingredients in this argument are the
spectral theorem, elementary block inversion, dominated convergence,
and the Poisson approximate identity for continuous compactly supported
densities. The half-line Weyl function and all scalar boundary estimates
used here are explicitly derived/evaluated rather than imported from a
resonance theorem. This proves the requested scalar boundary limit;
it does not assert an operator-norm limiting-absorption principle.

## 5. Strict positivity is analytical

Define the real on-shell source
\[
 S(x)=C\{M_+(E-x)+M_-(x)\}.
\]
The weight \(r_+(x)r_-(E-x)\) is strictly positive in \(I_E\). Thus
(10) could vanish only if \(S\) were equal to the constant
\(\alpha_E\) almost everywhere on that interval, hence everywhere
there by continuity. We now rule this out without a small-\(g\)
expansion of the pair or a numerical sign check.

Both terms of \(S(x)\) are analytic on a connected complex neighborhood
of the real half-line \(x>\max(b_-,E-b_+,2,E-4)\), whose endpoint is
less than 4. This domain includes \(I_E\) and arbitrarily large
positive \(x\). If \(S\) were constant on \(I_E\), the identity theorem
would make it constant along that half-line. Its large-\(x\) limit is
zero, so it would vanish identically there.

The first three endpoint moments are exact:
\[
 \int d\mu_\sigma=1,\quad
 \int t\,d\mu_\sigma(t)=3,\quad
 \int t^2\,d\mu_\sigma(t)=9+a_\sigma.
\]
Expanding the Stieltjes transforms at large \(x\) therefore gives
\[
 \frac{S(x)}C
 =\frac{E-6}{x^2}
  +\frac{(E-3)^2-9+a_+-a_-}{x^3}+O(x^{-4}). \tag{12}
\]
Identical vanishing would first require \(E=6\), then
\(a_+=a_-\). But \(a_+-a_-=g^2>0\). This contradiction proves that
\(S\) is nonconstant. A nonconstant continuous real function cannot
agree almost everywhere with any complex constant under a strictly
positive interval weight. Consequently (10) is **strictly positive**.

This proof also covers the exceptional bound-bound coincidence in section 4,
since it rules out equality with every constant, including
\(f(b_+,b_-)\). Together with finiteness it establishes the asserted
classification at fixed \(g=1/5\), and in fact throughout the stated
parent gap regime.

## 6. Executed calculations and checks

`continuum_response.py` implements (1)–(3), the complete-measure
integrals for the pair root and normalization, (9), and (10). It uses
\(x=c+\cos\theta\) to regularize one-body endpoint square roots and
splits at the remaining band thresholds. Three continuum quadrature
tolerances \(2\,10^{-10},2\,10^{-12},2\,10^{-13}\) agree on the
reported response. The finest run yields:

| Quantity | Numerical value |
|---|---:|
| \(b_+\) | 2.9581380507832593 |
| \(b_-\) | 3.021177249193989 |
| \(w_+\) | 0.9770252706124932 |
| \(w_-\) | 0.9880868665784739 |
| \(E\) | 5.978579315166578 |
| \(E-b_+-b_-\) | -0.000735984810670054 |
| \(C\) | 0.06415080170763802 |
| Bare-pair weight | 0.9625769954963075 |
| \(D(E+i0)\) | 1311.6989674372342 + 0.0005164396437468961 i |
| \(B(E+i0)\) | -15.287143547188174 - 0.00000014386646137944212 i |
| \(\alpha_E\) | -0.011654460304297955 + 0.0000000044788926514998245 i |
| \(\rho_g(E)\) | 0.0000000212750672152351 |

Both complete one-body measures integrate to 1 to floating-point
precision. The exact optical checks
\(\operatorname{Im}D=\pi\int r_+r_-\) and
\(\operatorname{Im}B=\pi\int r_+r_-S\) have numerical residuals below
\(3\,10^{-18}\) and \(5\,10^{-20}\), respectively.

As an independent algebra check, `check_fock.py` constructs the full
physical two-boson Fock Hamiltonian with actual hard-core \(L,R\)
memories and finite bath lengths 4, 6, 10, applies the diagonal physical
operator \(n_L-n_R\) to its pair eigenvector, and compares its complex
resolvent to (7). Pair energies, source norms, and scalar resolvents
agree within \(4\,10^{-15}\). The source norm squared tends to
0.0370447906. These finite Fock checks test normalization and compression;
the infinite-system sign classification comes from sections 4–5, not from
finite-chain crossings or extrapolated broadening.

The numerical response is dominated by the hard-core scattering
correction \(\alpha_E\). Omitting that correction would instead give
\(\int r_+r_-S^2\), a different and much smaller number. The weighted
variance \(\int r_+r_-(S-\overline S)^2\simeq1.50514\,10^{-12}\)
also provides a numerical positive lower bound independent of the
constant \(\alpha_E\); it is supplementary, not a rigorous interval
bound.

## 7. Scope of a possible lifetime interpretation

The result proved here is the exact unperturbed spectral-density limit
for the actual local detuning source. It does not by itself establish
resonance existence, an exponential survival law, a finite-\(\eta\)
error bound, or a gate fidelity.

Conditionally, if a valid second-order resonance continuation or
Fermi-golden-rule theorem applies to this embedded eigenvalue under
\(H_g+\eta V\), the pole convention
\(z_\eta=E+\Delta E_\eta-i\gamma_\eta\) would give
\[
 \gamma_\eta=\pi\eta^2\rho_g(E)+o(\eta^2),\qquad
 \Gamma_{\rm population}=2\gamma_\eta
          =2\pi\eta^2\rho_g(E)+o(\eta^2).
\]
Here \(\gamma\) is the amplitude-decay rate / Lorentzian half width,
and \(\Gamma_{\rm population}\) is the probability-decay rate /
Lorentzian full width, with \(\hbar=1\). Those resonance hypotheses
have not been proved in this note. In particular they are logically
separate from the completed finite-positive spectral-density result.
