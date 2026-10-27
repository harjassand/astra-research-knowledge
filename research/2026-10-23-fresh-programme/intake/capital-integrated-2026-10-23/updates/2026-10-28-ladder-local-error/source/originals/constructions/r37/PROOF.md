# Local parity breaking of the embedded hard-core pair

For the exact ladder and dressed pair in the supplied governing packet, with
`g = 1/5` and `V = n_L - n_R`, the requested infinite-volume spectral response is
**finite and strictly positive**. This statement is proved analytically below.
Ordinary continuum quadrature gives

\[
 E_p\simeq5.978579315166579,\qquad
 \rho_{1/5}(E_p)\simeq2.1275067206\times10^{-8}.
\]

The decimal value is a numerical diagnostic, not an interval enclosure. The
classification does not depend on its accuracy, nor on a finite chain limit.
The proof retains both bound atoms, both continuous measures, the exact dressed
pair, and the odd hard-core constraint.

Input: `../packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, especially
sections 2--3. The existing even pair construction is used to obtain its actual
normalized wavefunction; it is not claimed as a new result here.

## 1. Complete one-body measures and the even pair

Write `h_+`, `h_-` for the two one-body Jacobi operators, and `e_+`, `e_-` for
their normalized memory basis vectors. To distinguish vectors from energies,
write their bound energies as `a_+`, `a_-`. Their bath centers and squared
endpoint couplings are

\[
 c_+=5,\quad c_-=1,\qquad \lambda_+^2=2g^2,\quad\lambda_-^2=g^2.
\]

Set

\[
 m_c(z)=\frac{2}{z-c+\sqrt{z-c-1}\sqrt{z-c+1}},\qquad
 r_\sigma(z)=\langle e_\sigma,(h_\sigma-z)^{-1}e_\sigma\rangle
 =\frac1{3-z+\lambda_\sigma^2m_{c_\sigma}(z)}.                 \tag{1}
\]

The square roots are the principal square roots, approached from the upper half
plane. Thus `Im r_sigma(z)>0` there. Each memory vector is cyclic since every
Jacobi off-diagonal is nonzero. Its complete measure is

\[
 d\mu_\sigma(x)=Z_\sigma\delta_{a_\sigma}(dx)
                  +w_\sigma(x)\mathbf1_{(c_\sigma-1,c_\sigma+1)}dx,\tag{2}
\]
\[
 w_\sigma(x)=\frac{2\lambda_\sigma^2\sqrt{1-(x-c_\sigma)^2}}
 {\pi\{[3-x+2\lambda_\sigma^2(x-c_\sigma)]^2
                  +4\lambda_\sigma^4[1-(x-c_\sigma)^2]\}},
 \quad Z_\sigma=[1-\lambda_\sigma^2m'_{c_\sigma}(a_\sigma)]^{-1}.
                                                               \tag{3}
\]

At `g=1/5` the atoms are explicitly

\[
 a_+=\frac{215+4\sqrt{83}}{85}=2.95813805078\ldots,\qquad
 a_-=\frac{335-2\sqrt{79}}{105}=3.02117724919\ldots.              \tag{4}
\]

There are no omitted atoms. Outside a bath band the denominator in (1) is
strictly decreasing because `m_c'(x)<0`. At the plus band endpoints its values
are `-1.16,-2.84`; at the minus endpoints they are `2.92,1.08`.
Consequently the plus problem has exactly one atom below its band, the minus
problem exactly one above its band, and neither has another atom or an edge
atom. Formula (3) is strictly positive inside each band and vanishes like a
square root at the edges. Each measure has total mass one.

Let

\[
 L_\sigma(E)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(u)}{x+u-E}.
\]

Let `E=E_p` be the unique root `L_+(E)+L_-(E)=0` between `2a_+` and `2a_-`.
For completeness, no even continuum meets this interval: the lower even
continua end at `a_-+2<5.022` and the upper ones start at `a_++4>6.958`.
The sum of the `L`s increases strictly, going from minus infinity at the lower
double-atom pole to plus infinity at the upper pole. This verifies the root
and the gap used here directly at fixed coupling.

On the even harmonic two-boson space define

\[
 q_{\sigma\sigma}=|e_\sigma e_\sigma\rangle,\qquad
 R_{\sigma\sigma}(E)=(h_\sigma\otimes1+1\otimes h_\sigma-E)^{-1},
 \quad D=L_+'(E)+L_-'(E)>0.
\]

The normalized physical pair, up to its irrelevant overall sign, is

\[
 \boxed{\displaystyle
 \psi=\frac{R_{++}(E)q_{++}+R_{--}(E)q_{--}}{\sqrt D}.}          \tag{5}
\]

Indeed the forbidden even double-memory vector is
`d_e=(q_+++q_--)/sqrt(2)`; (5) is orthogonal to it by the root condition, has
unit norm by the definition of `D`, and `(H_0-E)psi` is a multiple of `d_e`.
Compression therefore makes it an eigenstate. In particular no bare-pair
substitution is made.

## 2. Exact odd space and actual parity-breaking source

The odd harmonic space is exactly

\[
 \mathcal K=\mathcal H_+\otimes\mathcal H_-,\qquad
 A=h_+\otimes1+1\otimes h_-.
\]

Its one forbidden double-memory vector is

\[
 q=e_+\otimes e_-=\frac{|LL\rangle-|RR\rangle}{\sqrt2}.
\]

Consequently the physical odd Hamiltonian is

\[
 H_{g,\mathrm{odd}}=PAP|_{q^\perp},\qquad P=1-|q\rangle\langle q|.\tag{6}
\]

This is the exact physical hard-core compression, not a scattering approximation.
In the cyclic spectral representation `K=L^2(mu_+ x mu_-)`, the vector `q` is the
constant function one and `A` multiplies by `x+y`.

The physical perturbation is the second quantization of
`v=|e_+><e_-|+|e_-><e_+|`. Contracting one memory coordinate in (5) gives

\[
 A_+(x)=r_+(E-x),\qquad A_-(y)=r_-(E-y),\qquad C=\sqrt{2/D},
\]
\[
 \boxed{\displaystyle f(x,y)=(V\psi)(x,y)=C[A_+(x)+A_-(y)].}     \tag{7}
\]

The factor `sqrt(2)` is the boson creation/annihilation factor from converting
one member of a same-parity pair into the other channel. All functions in (7)
are real and bounded on the complete product support: the same-parity sum
spectra avoid `E`. As a check essential to the odd constraint,

\[
 \langle q,f\rangle=C[L_+(E)+L_-(E)]=0.                         \tag{8}
\]

Thus (7) belongs to the actual physical space (6).

## 3. Exact resolvent and a nonnegative continuum expression

For `Im z>0` define complete-measure integrals

\[
 K(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
 J(z)=\iint\frac{f(x,y)d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
 Q(z)=\iint\frac{f(x,y)^2d\mu_+(x)d\mu_-(y)}{x+y-z}.             \tag{9}
\]

Solving the compressed resolvent equation with its Lagrange multiplier along
`q`, or doing one Schur complement, gives exactly

\[
 \boxed{\displaystyle
 \langle f,(H_{g,\mathrm{odd}}-z)^{-1}f\rangle
                   =Q(z)-\frac{J(z)^2}{K(z)}.}                \tag{10}
\]

The square is the analytic square, not a modulus square. The real source makes
the two off-diagonal resolvent matrix elements equal. Since `Im K(z)>0`, its
denominator is nonzero in the upper half plane.

At energy `E`, bound-plus-continuum odd energies are below `a_++2<4.959` or
above `a_-+4>7.021`, whereas `5.916<E<6.043`. The only on-shell continuous
piece is therefore the *opposite-band continuous-continuous* piece. Define

\[
 I_E=(\max\{4,E-2\},\min\{6,E\}),\quad
 W_E(x)=w_+(x)w_-(E-x),
\]
\[
 f_E(x)=C[r_+(E-x)+r_-(x)],\qquad
 c_E=\frac{J(E+i0)}{K(E+i0)}.                                 \tag{11}
\]

Away from a possible unperturbed double-atom coincidence (treated below), the
answer is the explicit infinite-system expression

\[
 \boxed{\displaystyle
 \rho_g(E)=\int_{I_E}W_E(x)\,|f_E(x)-c_E|^2\,dx.}              \tag{12}
\]

**All off-shell bound and continuous pieces still occur in `c_E`.** They may
not be deleted merely because only the continuous-continuous term is on shell.
For executable one-dimensional evaluation of (9),

\[
 K(z)=\int r_-(z-x)\,d\mu_+(x),
\]
\[
 J(z)=C\left[\int A_+(x)r_-(z-x)d\mu_+(x)
             +\int A_-(y)r_+(z-y)d\mu_-(y)\right].             \tag{13}
\]

Each integral in (13) explicitly includes its atom and its band integral.
Formula (12) follows algebraically from (10): if
`M_j=int W_E f_E^j`, the upper boundary values have imaginary parts
`pi M_0,pi M_1,pi M_2`. For `c=J/K`,

\[
 \operatorname{Im}(J^2/K)
       =2\operatorname{Re}c\operatorname{Im}J-|c|^2\operatorname{Im}K.
\]

This proves (12) with exactly the `1/pi` convention requested in the task.

## 4. Scalar limiting absorption and finiteness

No scattering-completeness or resonance theorem is assumed. The imports are
the bounded self-adjoint spectral theorem and tensor-product functional
calculus, elementary block elimination, and the Sokhotski--Plemelj formula for
a compactly supported locally Hölder continuous density. The hypotheses of
the last import follow directly here, as follows.

Extend the densities (3) by zero. They are globally Hölder continuous with
exponent `1/2`. The source (7) is smooth on a neighborhood of each band
rectangle. Consequently the continuous-continuous densities

\[
 N_j(t)=\int w_+(x)w_-(t-x)f(x,t-x)^jdx,\qquad j=0,1,2,
\]

are locally Hölder continuous. All other continuous pieces are separated from
`E`. For such an `N_j`, the principal value at `E` is finite: subtracting
`N_j(E)` leaves a numerator `O(|t-E|^{1/2})`, whose quotient by `t-E` is locally
integrable. The elementary Plemelj boundary value therefore exists and is
finite. Since `I_E` has positive length and both densities are positive inside
it, `N_0(E)>0`; thus `Im K(E+i0)=pi N_0(E)>0` and `K(E+i0)` cannot vanish.
The functions `f_E`, `W_E`, and the finite constant `c_E` make (12) finite.

There is no numerical assumption hidden in the possible equality
`E=a_++a_-`. It can be removed algebraically as well. Put `p=Z_+Z_->0` and
`b=f(a_+,a_-)`, and split

\[
 K=p/(a_++a_--z)+K_0,\quad J=pb/(a_++a_--z)+J_0,\quad
 Q=pb^2/(a_++a_--z)+Q_0.
\]

Then (10) is exactly

\[
 Q_0-2bJ_0+b^2K_0-
 \frac{(J_0-bK_0)^2}{p/(a_++a_--z)+K_0}.                      \tag{14}
\]

At coincidence the last term tends to zero; the other terms have the finite
boundary values just proved. Formula (12) remains valid with `c_E=b`. This
cancels the forbidden double-atom pole explicitly. In particular finiteness
does not rely on trusting a floating-point nonzero connected shift.

This proves precisely the scalar limiting-absorption statement needed for the
specified vector. An operator norm limiting-absorption principle on the full
unweighted Hilbert space is neither used nor asserted.

## 5. Analytical strict positivity at fixed coupling

It remains possible in a rank-one problem that the source is screened exactly
on shell. Here that possibility is excluded analytically.

Consider

\[
 S_E(x)=r_+(E-x)+r_-(x).
\]

It is real analytic on the connected half line
`x>max{a_-,E-a_+}`, which contains the entire open shell interval `I_E`.
Indeed `E-x<a_+` lies below all plus spectrum and `x>a_-` above all minus
spectrum. If (12) vanished, its positive weight would force `C S_E(x)=c_E`
almost everywhere on `I_E`, and analyticity would force `S_E` to be constant
on that entire half line.

The complete measures have exact first and second moments

\[
 \int u\,d\mu_\pm(u)=3,\qquad
 \int u^2d\mu_+(u)=9+2g^2,\quad
 \int u^2d\mu_-(u)=9+g^2.
\]

Their compact supports give the convergent large-`x` expansion

\[
 S_E(x)=\frac{E-6}{x^2}
          +\frac{E^2-6E+g^2}{x^3}+O(x^{-4}).                  \tag{15}
\]

A constant function with this expansion must be zero. Its first displayed
coefficient would require `E=6`, after which its second displayed coefficient
would require `g^2=0`. This contradicts `g=1/5`. Therefore `S_E` is nonconstant,
so the integral (12) is strictly positive. This also covers the coincidence
case (14), since `b` is merely another constant.

Equivalently, independently of the unknown screening constant,

\[
 \rho_g(E)\ge M_2-M_1^2/M_0>0.                                \tag{16}
\]

The strict inequality in (16) is the weighted variance of a nonconstant
analytic function. It is an analytical positivity certificate at the fixed
coupling, not an asymptotic expansion in `g`.

## 6. Executed numerical checks and scope

`spectral_response.py` evaluates (1)--(3), solves the complete-measure pair
root, evaluates (13), and then integrates (12). The substitution
`x=c+cos(theta)` removes the one-body endpoint square roots; the remaining
branch points are split explicitly. Three tolerances from `2e-10` to `2e-13`
gave the same response to the displayed precision. `results.json` retains
the actual outputs, including

| Quantity | Continuum quadrature |
|---|---:|
| `Z_+`, `Z_-` | `0.9770252706124932`, `0.9880868665784739` |
| `E_p-a_+-a_-` | `-0.0007359848106709421` |
| `D` | `485.9883059476891` |
| bare pair overlap squared | `0.9625769954962954` |
| `||V psi||^2` | `0.03704479062420679` |
| source overlap with forbidden `q` | `1.24e-14` |
| `K(E+i0)` | `1311.698967435640 + 0.000516439643746896 i` |
| `J(E+i0)` | `-15.28714354401377 - 1.43866461379e-7 i` |
| `c_E` | `-0.01165446030189205 + 4.47889265056e-9 i` |
| `rho_g(E)` | `2.1275067206237e-8` |
| weighted variance in (16) | `1.50513922229e-12` |

`high_precision_check.py` independently repeats the continuum calculation with
40-decimal mpmath arithmetic, obtaining
`E_p=5.9785793151665785452365388939752013` and
`rho=2.1275067206158437723596256295547633e-8`. Its root residual is about
`1e-38`; its response agrees with the double-precision implementation to about
`4e-12` relative. This remains a numerical diagnostic, not rigorous interval
arithmetic; its complete output is `high_precision_results.json`.

Both measures integrate to one within floating precision. Independently,
`Im K = pi int W_E` agrees to `2.5e-18` at the tightest tolerance.

`finite_volume_check.py` independently builds the original connected local
rail ladder, its physical two-boson Fock matrix with double-memory states
removed, its actual pair eigenvector, and the diagonal physical operator
`V=n_L-n_R`. For 4, 8 and 12 sites per rail, it compares its resolvent matrix
element with the complete discrete-measure version of (7)--(10). Across
`Im z=0.1,0.03,0.01`, discrepancies are at most `1.9e-15`; pair energies and
source norms agree to floating precision. The complete outputs are in
`finite_volume_results.json`. These are algebra checks; the infinite-system
classification was proved in sections 4--5 without a finite-volume limit.

Two concrete tempting shortcuts fail. First `V|LR>=0`, so replacing the
actual dressed pair by the bare memory pair would incorrectly produce zero.
Second, dropping the odd hard-core correction in (10) gives only `M_2`, about
`1.42621721824e-11`, rather than the actual value about `2.1275e-8`.

## 7. Conditional linewidth interpretation and remaining boundary

The proved result is the spectral-density statement for the unperturbed exact
ladder and the specified local perturbation. If an applicable resonance
perturbation theorem supplies a pole expansion for `H_g+eta V`, its usual
second-order form in the present resolvent convention is

\[
 z_{\rm res}(\eta)=E+\eta^2\Delta
                  -i\pi\eta^2\rho_g(E)+o(\eta^2),
 \qquad \Delta\in\mathbb R.
\]

The amplitude half width is then `gamma=pi eta^2 rho + o(eta^2)`, while the
probability decay rate and Lorentzian full width at half maximum are
`Gamma=2 gamma=2 pi eta^2 rho + o(eta^2)` in units `hbar=1`. The diagnostic
coefficients at fixed `g=1/5` are `6.68375948e-8` and `1.33675190e-7`,
respectively. This document does not prove that resonance expansion, an
exponential survival law over a specified time interval, or a gate-fidelity
bound. Those are separate obligations. No historical priority or device
advantage is claimed.
