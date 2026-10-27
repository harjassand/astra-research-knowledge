# Local pole of the detuned hard-core pair

## Conclusion and provenance

The supplied construction in `../frozen/c74/PROOF.md` already closes the
qualitative full pole target. Its bounded deformation, threshold argument,
hard-core cancellation, physical-response matching and simple-eigenvalue
argument are sufficient. No missing resonance theorem or unproved
noncoincidence of two real energies remains. This integration does not claim
a new theorem from repackaging that construction.

This document gives a source-bound proof chain and an additional exact local
Feshbach equation, including explicit formulas for both continued responses.
The latter equation is a useful independent derivation and check; it is not
a repair needed to make the supplied theorem true. All supplied files remain
unchanged. The independent code and its outputs are in this directory.

The physical model is exactly the connected semi-infinite ladder in
`../packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, restricted to
two excitations, with fixed `g=1/5`. The normalized pair and its dressed
source are constructed in `../review_packet/S62/PROOF.md`; that proof was
read and its load-bearing algebra retained. The new continuation argument
being integrated is `../frozen/c74/PROOF.md`, read together with its full
handoff, result and executed code.

With the convention `(H-z)^{-1}`, there exist `r>0` and `epsilon>0` such
that, for real `|eta|<epsilon`, the physical responses at the bare pair
`p=LR` and the unperturbed normalized pair `psi` have meromorphic outgoing
continuations to `D(E,r)`. Both have one simple visible pole, the same
holomorphic even branch

\[
 \lambda(\eta)=E-\eta^2s(E+i0)+O(\eta^4),\qquad
 s(z)=\langle V\psi,(H_{g,\mathrm{odd}}-z)^{-1}V\psi\rangle,
 \quad V=n_L-n_R.
\]

In particular

\[
 \operatorname{Im}\lambda(\eta)
 =-\pi\rho_g(E)\eta^2+O(\eta^4),\qquad 0<\rho_g(E)<\infty.
\]

This is an infinite-system local resonance theorem at this fixed nonzero
coupling. The coefficient decimal `2.1275067206e-8` is not interval
certified. No evaluated lower bound on `epsilon`, exponential survival law,
physical lifetime or hardware advantage is established.

## Exact microscopic operators

In the one-body memory basis `e_+=(L+R)/sqrt(2)`,
`e_-=(L-R)/sqrt(2)`, the bath sine transform gives

\[
 h_\sigma=\begin{pmatrix}
 3&\sqrt{\kappa_\sigma}v_0^T\\
 \sqrt{\kappa_\sigma}v_0&M_{c_\sigma-\cos k}
 \end{pmatrix},\qquad
 v_0(k)=\sqrt{2/\pi}\sin k,
\]

where `(c_+,kappa_+)=(5,2/25)` and
`(c_-,kappa_-)=(1,1/25)`. The actual one-body detuning mixes the two
memories with matrix `eta [[0,1],[1,0]]`. Let `A_eta=dGamma(h_eta)` on
the symmetric two-boson space. Let `W` have the original normalized
forbidden vectors `LL,RR` as columns, and set `P=1-WW^T`. Then

\[
 H_\eta=PA_\eta P|_{P\mathscr K}=H_0+\eta V.
\]

The hard-core projection commutes with `dGamma(n_L-n_R)` because the
forbidden subspace is invariant. On the allowed space `||V||=1`, while
`V` has infinite rank. Nothing below replaces it by a rank-one operator.

Use the continuous bilinear transpose form `B(f,g)`, the sum/integral of
products without complex conjugation, in this fixed real representation.
All deformed operators are symmetric for `B`; for real physical test
vectors, `B` is exactly the physical bra on a resolvent vector.

The supplied even pair is

\[
 \psi=\frac{(A_+-E)^{-1}q_++(A_--E)^{-1}q_-}{\sqrt D},
 \quad q_\sigma=|e_\sigma e_\sigma\rangle,
\]

\[
 L_+(E)+L_-(E)=0,\qquad D=L_+'(E)+L_-'(E)>0.
\]

Its norm is one, its forbidden overlap is zero, and its nonzero bare-pair
weight is

\[
 Z_p=-2L_+(E)L_-(E)/D>0.
\]

These follow directly by applying the harmonic inverse and differentiating
its scalar matrix elements. They are not assumptions about a bare source.

## Bounded analytic deformation and the outgoing sheet

For complex `|t|<1`, set

\[
 \phi_t(k)=k+t\sin k,\quad
 \omega_{c,t}(k)=c-\cos\phi_t(k),\quad
 v_t(k)=\sqrt{2/\pi}\sin\phi_t(k)\sqrt{1+t\cos k}.
\]

The square root is the branch equal to one at zero. Replace the bath
multipliers and endpoint vectors by these expressions and retain the
memory mixing exactly. Use `v_t^T` in the endpoint functional. This defines
bounded norm-holomorphic `h_eta,t`, `A_eta,t` and

\[
 H_{\eta,t}=PA_{\eta,t}P|_{P\mathscr K}=H_{0,t}+\eta V
\]

on a common fixed Hilbert space. Holomorphy follows from holomorphy into
`L^infinity` for the multiplier and into `L^2` for the endpoint vector.
No complex composition operator on arbitrary `L^2` functions is used.

For real `|t|<1`, the map `phi_t` is a diffeomorphism of `[0,pi]` and
`U_t f=sqrt(phi_t') f(phi_t)` is unitary. It fixes both memories and
therefore both forbidden states. Thus `H_eta,t` is exactly unitarily
equivalent to the physical hard-core `H_eta`, including at nonzero eta.

Fix `theta=1/4` and write `H_theta=H_0,-i theta`. The bath arcs are

\[
 \Gamma_{c,\theta}=
 \{c-\cos(k-i\theta\sin k):0\leq k\leq\pi\}.
\]

Their imaginary part is `-sin(k)sinh(theta sin(k))<0` in the interior.
Their real part is strictly increasing: its derivative is at least
`sin(k)cosh(theta sin(k))(1-theta^2 cos(k)^2)>0`, using `tanh(a)<=a`.
Endpoints stay at the physical band edges. The outgoing sheet is the germ
obtained from the physical upper half-plane by lowering both momentum
contours in this way, with their endpoints fixed. It is an operator
construction of specified scalar continuations, not an asserted bounded
continuation of the physical unweighted resolvent across its spectrum.

## Spectral separation and the threshold at six

The one-body endpoint Schur integral on the deformed contour, denoted
`r_c,theta(z)`, agrees with the physical half-line Weyl function above the
real axis. Analytic continuation on the connected complement of the simple
arc gives

\[
 r^2+4(z-c)r+4=0.
\]

Consequently a zero of `3-z-kappa r` must solve

\[
 (3-z)^2+4\kappa(z-c)(3-z)+4\kappa^2=0.
\]

For the two channels the polynomials are proportional to
`425z^2-2150z+2641` and `525z^2-3350z+5329`. All roots are real outside
the bath bands. Substitution in the original physical branch discards one
root per channel and leaves the simple atoms

\[
 E_+=43/17+4\sqrt{83}/85,\qquad
 E_-=67/21-2\sqrt{79}/105.
\]

The deformed one-body spectra are contained in their arcs plus these atoms.
This follows from the explicit Schur inverse and does not require a
complete nonnormal eigenfunction expansion.

The mixed two-band endpoint at 6 is a real issue; it must be excluded
analytically, not from a floating-point pair energy. The supplied argument
does so. For an upper bath `b` with spectrum `[4,6]`, separate two memory
quanta, one memory plus one bath quantum, and two bath quanta at total
energy 6. The lower-right blocks are

\[
 T=b-3\geq1,\qquad C=d\Gamma(b)-6\geq2,
 \quad D_b=W_b^TC^{-1}W_b\geq0,\quad \|D_b\|\leq1.
\]

The boson creation map obeys `||W_b||<=sqrt(2)`. Thus, for `0<kappa<1`,

\[
 L_+(6;\kappa)=-\frac1{2\kappa s_b(\kappa)},\qquad
 s_b(\kappa)=\langle0,(T-\kappa D_b)^{-1}0\rangle>0.
\]

The function `s_b` is nondecreasing and `kappa s_b(kappa)` is strictly
increasing. Hence `L_+(6;kappa)` is strictly increasing. Spectral
reflection with a memory sign change gives
`L_-(6;kappa)=-L_+(6;kappa)` at equal couplings. The actual unequal
couplings give

\[
 L_+(6;2/25)+L_-(6;1/25)>0.
\]

Since `L_++L_-` is strictly increasing between its two atom poles and
vanishes at the pair energy, this proves

\[
 2E_+<E<6<2E_-.
\]

For bounded one-body operators, a separating-contour resolvent integral
gives spectral inclusion of the tensor sum in the sum of their spectra;
it remains valid on the symmetric tensor subspace. Every sum containing
an interior arc point has negative imaginary part. Real sums containing
arc endpoints cannot equal E: mixed bath endpoint sums are `4,6,8`, and
atom-band endpoints near E are below `E_-+2<5.1` or above `E_++4>6.8`.
The only potentially coincident harmonic atom is `a=E_++E_-` in the odd
sector. No assumption `E != a` is needed.

## Hard-core compression and isolated simplicity

For a real normalized forbidden vector `q`, put `Q=1-qq^T` and
`R(z)=(A-z)^{-1}`, `m(z)=q^TR(z)q`. Where both inverses exist,

\[
 (QAQ-z)^{-1}_{q^\perp}
 =Q\{R-Rq\,m^{-1}q^TR\}Q.
\]

In the even sector `q=(q_++q_-)/sqrt(2)`. Its harmonic operator is
invertible at E, and
`m(E)=0`, `m'(E)=D/2>0`. The formula has a simple rank-one pole.
Its eigenvector is the deformation `psi_theta` of the displayed pair,
with `B(psi_theta,psi_theta)=1`.

In the odd sector `q=|e_+e_->`. If `E != a`, the harmonic operator is
invertible at E. Its forbidden scalar is the complete-measure transform

\[
 M(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z}.
\]

Its deformed value has imaginary part

\[
 \operatorname{Im}M_\theta(E)
 =\pi\int_4^E\varrho_+(x)\varrho_-(E-x)\,dx>0.
\]

The open shell is nonempty and both band densities are positive there.
Thus the odd hard-core inverse exists at E.

If `E=a`, write `d=a-z`,
`R=Pi/d+R0`, `b=q^T Pi q=w_+w_->0`,
`g=R0 q`, and `m0=q^T R0 q`. The rank-one symmetric atom projection
satisfies `(Pi q)(Pi q)^T=b Pi`. Direct substitution gives the following
explicit pole cancellation (an expanded version of the supplied argument):

\[
 R-Rq\,m^{-1}q^TR
 =R_0+
 \frac{m_0\Pi-(\Pi q)g^T-g(\Pi q)^T-dgg^T}{b+dm_0}.
\]

The right side is holomorphic at `d=0`. After the outer Q factors, both
inverse identities extend there from the punctured neighborhood by
continuity. The odd hard-core operator is therefore invertible at E even
in the coincident case. Together these arguments show that E is an
isolated algebraically simple eigenvalue of the **full** deformed H_theta.

## Matching the actual physical responses

For `t=-is`, `0<=s<=theta`, the unperturbed harmonic spectra have no upper
half-plane points. The forbidden compression scalars there equal the
physical Herglotz functions and have positive imaginary parts. Hence the
full unperturbed hard-core resolvent exists there along the whole path.
Choose `z_*=E+ir/2` in the local disk described below. The compact path
has a finite uniform resolvent bound `N_*` at that point.

For `|eta|<1/(2N_*)`, a uniform Neumann series preserves invertibility on
the path and a neighborhood of `z_*`. The pair vector `psi_t` is
holomorphic along this path, since its even harmonic inverses exist at E.
For real t, exact unitary equivalence equates

\[
 B(p,(H_{\eta,t}-z)^{-1}p),\qquad
 B(\psi_t,(H_{\eta,t}-z)^{-1}\psi_t)
\]

to the respective physical responses. Holomorphy and the identity theorem
in t on a connected open neighborhood of the path propagate the equality
to `t=-i theta`. The resulting meromorphic functions thus continue the
actual responses for the full physical detuning. The argument uses the
operator family, rather than assuming scalar Hölder boundary data imply
analytic continuation.

## Local domain and perturbation hypotheses

Choose a closed disk of radius `2r` avoiding all harmonic spectral sums
other than E's even hard-core zero and possibly the odd harmonic atom a.
Shrink it so that

\[
 \left|m_e(z)/(z-E)-D/2\right|<D/4,
\]

and, if `a != E`, `|M_theta(z)-M_theta(E)|<|M_theta(E)|/2`.
In the coincident case instead require
`|(a-z)M_theta(z)-b|<b/2` with the removable value inserted. All are
possible by the holomorphy and nonvanishing established above. The full
unperturbed deformed spectrum in this disk is then exactly the simple E.
Define

\[
 M_r=\sup_{|z-E|=r}\|(H_\theta-z)^{-1}\|<\infty,
 \quad N_*=\sup_{0\leq s\leq\theta}
 \|(H_{0,-is}-z_*)^{-1}\|<\infty.
\]

For `|eta|<1/(2M_r)`, the circle stays in the resolvent set. Its Riesz
projection is norm-holomorphic and has constant rank one. The spectral
part inside is consequently one holomorphic simple eigenvalue lambda.
These are the exact perturbation hypotheses: a bounded holomorphic family,
an isolated algebraically simple eigenvalue and a fixed resolvent contour.
They have all been verified. No many-body resonance theorem is imported.

The contour resolvent identity gives
`||Pi_eta-Pi_0||<=2r |eta| M_r^2`. If, in addition,

\[
 |\eta|<Z_p/(4rM_r^2),\qquad
 |\eta|<1/(4rM_r^2\|\psi_\theta\|^2),
\]

the two pole coefficients remain within half their nonzero values at
zero, `Z_p` and 1. The minimum of these four positive eta bounds gives a
specific positive `epsilon` by resolvent definitions. No numerical value
for those norms or the resulting radius is claimed.

## Additional exact Feshbach derivation

This section is the integrator's added derivation. It is another exact
local form of the construction already completed by the supplied proof.

Let `P0=psi_theta B(psi_theta,.)` be the simple unperturbed Riesz
projection, `Q0=1-P0`, and `f=V psi_theta`. These are transpose symmetric;
`f` is odd and lies in `ran Q0`. On that closed complement define

\[
 D_\eta(z)=Q_0(H_\theta+\eta V-z)Q_0|_{\operatorname{ran}Q_0}.
\]

It is invertible for `(eta,z)` sufficiently near `(0,E)`. Solving the
two block equations exactly gives the scalar denominator

\[
 \boxed{\mathcal F(\eta,z)
 =E-z-\eta^2 B(f,D_\eta(z)^{-1}f).}
\]

Thus `F=0` is the exact local full-detuning pole equation. The dependence
of `D_eta` on eta must be retained; replacing it by the odd unperturbed
resolvent is only a second-order step. This reduction does not assume V
has finite rank. It uses a rank-one projection onto a known isolated
eigenvector, while keeping the entire complementary two-particle space.

More explicitly, put `a_p=B(psi_theta,p)` and `p_Q=Q0 p`. Block inversion
gives

\[
 G_\psi^{\rm out}(\eta,z)=\frac1{\mathcal F(\eta,z)},
\]

\[
 G_p^{\rm out}(\eta,z)
 =B(p_Q,D_\eta(z)^{-1}p_Q)
 +\frac{[a_p-\eta B(f,D_\eta(z)^{-1}p_Q)]^2}
 {\mathcal F(\eta,z)}.
\]

In particular visibility is direct: `F_z(0,E)=-1`, the dressed response
has numerator one, and the bare numerator at zero is `a_p^2=Z_p>0`.
The simple zero of F gives the same branch as the Riesz construction.
These formulas supply an explicit exact local response construction in
addition to the supplied forbidden-state Schur matrix.

For completeness the latter matrix remains the exact full-detuning
criterion wherever the harmonic inverse exists:

\[
 K_\eta(z)=W^T(A_{\eta,-i\theta}-z)^{-1}W,
 \qquad z\in\sigma(H_{\eta,-i\theta})\iff\det K_\eta(z)=0.
\]

At harmonic poles use invertibility of the augmented operator
`[[A_eta,-i theta-z,W],[W^T,0]]`; this is equivalent to hard-core
invertibility by decomposing a vector into its allowed and forbidden
components. Thus neither representation introduces a spurious harmonic
pole into the physical criterion.

## Expansion, coefficient and exact remainder scope

Rail exchange fixes psi_theta and reverses V, and commutes with Q0.
Consequently `F(-eta,z)=F(eta,z)` and the unique branch is even. At zero,
`D_0(E)^{-1}f` is exactly the deformed odd inverse applied to f. Therefore

\[
 \lambda(\eta)=E-\eta^2
 B(f,(H_{\mathrm{odd},\theta}-E)^{-1}f)+O(\eta^4).
\]

The same matching argument identifies this scalar with `s(E+i0)`.
Its holomorphy near E follows from the established odd inverse, including
the coincident-atom case. Hence its boundary value is the actual outgoing
coefficient, with the minus sign dictated by the exact Feshbach equation.

The supplied dressed-source identity is

\[
 (V\psi)(x,y)=\sqrt{2/D}\,u(x,y),\qquad
 u=m_+(E-x)+m_-(E-y),
\]

where the complete endpoint measures include their atoms. Defining
`(M,J,F_s)=int (1,u,u^2)/(x+y-z) dmu_+ dmu_-` gives
`s=(2/D)(F_s-J^2/M)`. The scalar positive identity and its verified
Hölder-density boundary limit give

\[
 \rho_g(E)=\frac2D\int_4^E
 \varrho_+(x)\varrho_-(E-x)
 |m_+(E-x)+m_-(x)-\alpha|^2\,dx,
 \quad \alpha=\lim_{\delta\downarrow0}J(E+i\delta)/M(E+i\delta).
\]

The continuous shell is the only on-shell band piece. In the coincident
case the common atom pole cancels, as in the supplied source proof. To
check strict positivity independently of its small numerical value,
`U(x)=m_+(E-x)+m_-(x)` is real analytic on a connected interval containing
the whole shell and extending to infinity. There
`U(x)=(E-6)/x^2+O(x^-3)`. Since `E<6`, U cannot be constant on the shell.
No constant alpha can annul the positive-density integral almost
everywhere. Boundedness and `D>0` give finiteness. Thus
`Im s(E+i0)=pi rho_g(E)>0` rigorously.

The remainder is `O(eta^4)` by holomorphy and evenness. More precisely,
for any `0<epsilon0<epsilon`, Cauchy's coefficient bound gives

\[
 |\lambda(\eta)-E+\eta^2s(E+i0)|
 \leq\frac{r(|\eta|/\epsilon_0)^4}
 {1-(|\eta|/\epsilon_0)^2},\qquad |\eta|<\epsilon_0.
\]

This is a local complex-parameter eigenvalue remainder. It is not a
uniform-in-time decay estimate.

## Executed checks and remaining work

`supplied_contour_check.py` is an unchanged owned copy of the frozen
script; it writes its results only here. Its replay reproduces the supplied
96–160-node contour response, `s approximately 0.00707837231216 +
6.6837594e-8 i`, including full-eta Schur roots. This is numerical
consistency evidence, not the proof above.

`integration_check.py` independently builds the bosonic Fock operator in
the physical L,R memory basis, deletes exactly LL and RR, and checks the
full two-constraint inverse and the added rank-one Feshbach construction.
It retains the actual diagonal perturbation `n_L-n_R`. At 20 quadrature
nodes per bath (901 allowed states), the direct two-constraint inverse
agrees to about `2.1e-13`; parity identities are exact at displayed
precision and the perturbation norm is one. The full-detuning pole's exact
Feshbach equation has residual below `8.5e-14` across the executed cases.
The final response and evenness errors are recorded in the output.

Low orders are deliberately retained: eight nodes give a spurious
unperturbed imaginary part around `7.3e-7` and a wrong-sign imaginary
coefficient; twelve nodes still do not resolve the width accurately.
Twenty nodes give `Im(s) approximately 6.68387e-8`, close to the much
better supplied contour calculation. Direct dense eigenvalue widths at
small eta also lose relative precision. These failures are discretization
and floating-point limitations and play no role in the analytic theorem.
The initial low-order run is separately preserved in
`integration_check_low_order_results.json`.

There is no remaining load-bearing mathematical obligation for the stated
qualitative local target. Quantitative next work is to validate the contour
distances and resolvent norms determining r and epsilon, and to enclose
the coefficient numerically. An operational decay claim would additionally
require a controlled inverse-transform/threshold analysis; a physical
advantage would require its own device and comparator evidence.
