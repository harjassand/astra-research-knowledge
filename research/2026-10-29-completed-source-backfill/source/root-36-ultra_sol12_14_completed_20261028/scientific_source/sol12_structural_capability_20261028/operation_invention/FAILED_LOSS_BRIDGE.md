# A valid material-volume witness and a failed enclosed-void rescue

This file preserves the attempted bridge, its valid portion and two precise restrictions. The calculations concern homogeneous linear Ohmic continuum electrostatics at a fixed nonzero frequency. They do not refute the existing conditional perfect-conductor powder certificate or demonstrate a physically manufacturable bad particle.

## 1. The proposed rescue

The existing powder target needs a response lower bound proportional to the volume filled across shielded closed cavities, V_filled. At finite conductivity, extremely slow shape-dependent charge modes might make a real polarizability too small. A possible response was to add a measured loss quadrature so that the depolarization spectrum need not have a prescribed gap.

Let D be the actual conducting-material region, with volume V_D. The relative electric susceptibility is
\[
 \chi=i b=i/\tau,\qquad b>0,\quad \tau>0,
 \tag{1}
\]
using the exp(-i omega t) convention. This is a loss-only homogeneous contrast in vacuum, with conductivity sigma and tau=epsilon_0 omega/sigma if displacement corrections are neglected. Those material assumptions are model inputs.

The candidate scalar observable is
\[
 W_D(\tau)=\operatorname{tr}\{\Re\alpha_D+6\tau\Im\alpha_D\}.
 \tag{2}
\]
It does obey W_D>=9 epsilon_0 V_D. The right volume is the actual conducting-material volume. Substituting V_filled is false.

## 2. An explicit spectral proof of the valid part

On complex vector fields in L2(R^3), let Gamma be the longitudinal orthogonal projection, whose unitary-Fourier multiplier at nonzero xi is xi xi^T/|xi|^2. Its value at xi=0 is immaterial. Let Gamma_D=1_D Gamma 1_D, acting on fields supported in D. It is self-adjoint with 0<=Gamma_D<=I.

For a uniform incident field e, the polarization P_D solves
\[
 (I+\chi\Gamma_D)P_D=\epsilon_0\chi\,1_D e.
 \tag{3}
\]
Set c_i=1_D e_i. The dipole tensor is
\[
 (\alpha_D)_{ij}=\epsilon_0\chi
       \langle c_i,(I+\chi\Gamma_D)^{-1}c_j\rangle.
 \tag{4}
\]
The spectral theorem gives a positive matrix-valued measure mu on [0,1] with
\[
 \alpha_D=\epsilon_0\int_0^1
       \frac{d\mu(\lambda)}{\lambda-i\tau},\qquad
 \mu([0,1])=V_D I.
 \tag{5}
\]
Write nu=tr mu. Its total mass is 3V_D. Its first moment is exactly V_D, since Parseval gives
\[
 \int\lambda\,d\nu
 =\sum_i\langle c_i,\Gamma_D c_i\rangle
 =\int_{\mathbb R^3}|\widehat{1_D}(\xi)|^2
       \sum_i\frac{\xi_i^2}{|\xi|^2}\,d\xi
 =V_D.
 \tag{6}
\]
This identity uses the material indicator 1_D, not the indicator of a cavity-filled region.

For every lambda>=0,
\[
 \frac{\lambda+6\tau^2}{\lambda^2+\tau^2}-(6-9\lambda)
 =\frac{\lambda\{(3\lambda-1)^2+9\tau^2\}}
        {\lambda^2+\tau^2}\ge0.
 \tag{7}
\]
Integrating(7) with(5)–(6) yields
\[
 W_D\ge\epsilon_0(6\cdot3V_D-9V_D)
       =9\epsilon_0V_D.
 \tag{8}
\]
The code checks the rational identity in(7). No eigenvalue gap is needed. This is a simple consequence of established depolarization spectral machinery; historical novelty is not claimed.

If mass= rho V_D, division by mass only gives W_D/m>=9 epsilon_0/rho. It contains no closed-void fraction. The perfect-conductor filling argument cannot be imported into finite-contrast(3).

## 3. An exact conducting spherical shell

Take a spherical vacuum core of radius a, outer radius R, and homogeneous shell permittivity 1+chi. Set phi=(a/R)^3 and delta=1-phi. In an applied z field, use potentials
\[
 \Phi_{\rm out}=-r\cos\theta+dR^3\cos\theta/r^2,\quad
 \Phi_{\rm shell}=-Br\cos\theta+CR^3\cos\theta/r^2,\quad
 \Phi_{\rm core}=-Dr\cos\theta.
 \tag{9}
\]
Continuity of potential and normal displacement at both boundaries gives
\[
 f(\delta,\chi)
 =\frac{\alpha_{\rm scalar}}{3\epsilon_0V_{\rm outer}}
 =\frac{\delta\chi(3+2\chi)}
        {9+9\chi+2\delta\chi^2}.
 \tag{10}
\]
The code solves these four boundary equations independently before checking(10). Let w=Re f+6 tau Im f. Then W=9 epsilon_0 V_outer w. At each fixed positive tau,
\[
 \lim_{\delta\downarrow0}\frac{w}{\delta}
 =\frac{13+18\tau^2}{9+9\tau^2}<\infty.
 \tag{11}
\]
By contrast, at fixed positive delta the perfect-conductor limit gives w->1. The thin-metal and perfect-conductor limits do not commute.

Two exact rational controls:

| delta | tau | actual void phi | w/delta | invalid value 1-delta/w |
|---:|---:|---:|---:|---:|
| 1/100 | 1/1000 | .99 | 83.46503288 | .9880189348 |
| 1/1000000 | 1/100 | .999999 | 1.444993969 | .3079555893 |

The last column is what incorrectly substituting W for the perfect-conductor trace would assert as an upper void bound. It is less than the actual void in both cases. Thus the global filled-volume inequality is false. These simple shells by themselves do not establish false acceptance at the specific 1% threshold: the second response still exceeds 100/99. That sharper question requires a separate construction.

## 4. A finite-contrast continuity estimate

Let D_0 be a solid ball of volume V_0 and D=D_0 union S, where the added metal S is disjoint from the ball up to a measure-zero interface, of volume V_S. Extend the ball polarization P_0 by zero to D. Subtract(3) for the two domains:
\[
 (I+\chi\Gamma_D)(P_D-P_0)
 =\epsilon_0\chi\,1_S E_0,
 \tag{12}
\]
where E_0=e-Gamma P_0/epsilon_0 is the ball's total background field in S.

For chi=i b and Gamma_D self-adjoint positive, spectral calculus gives
\[
 \|(I+i b\Gamma_D)^{-1}\|\le1.
 \tag{13}
\]
Outside a solid ball of radius a, its field is
\[
 E_0(x)=e+\frac{\chi}{\chi+3}
 \frac{a^3}{|x|^3}(3\widehat x\widehat x^T-I)e.
 \tag{14}
\]
Since |chi/(chi+3)|<=1, this obeys |E_0|<=3|e| outside the ball. Equations(12)–(14) imply
\[
 \|P_D-P_0\|_{L^2(D)}
 \le3\epsilon_0 b\sqrt{V_S}|e|.
 \tag{15}
\]
Integrating the polarization and using Cauchy–Schwarz on D gives the full complex tensor bound
\[
 \|\alpha_D-\alpha_0\|_{\rm op}
 \le3\epsilon_0 b\sqrt{(V_0+V_S)V_S}.
 \tag{16}
\]
No additive independent-sphere approximation is used. The estimate permits strong local interactions near a connecting neck. Only its total added volume and the bounded background field enter.

For the normalized witness Q_D=W_D/[9 epsilon_0(V_0+V_S)], use |tr Re A|,|tr Im A|<=3||A|| to obtain
\[
 Q_D\le Q_0+(1+6\tau)b\sqrt{V_S/V_0},\qquad
 Q_0=\frac{1+18\tau^2}{1+9\tau^2}.
 \tag{17}
\]
The slightly tighter factor sqrt[V_S/(V_0+V_S)] was relaxed in(17). The solid ball term was also bounded upward by Q_0 rather than multiplied by V_0/(V_0+V_S).

### A stronger bound from reciprocity

The square-root bound is not the sharpest available operation. Write E_D^f for the electric field in D induced by a uniform incident vector f. Inside D, E_D^f=A_D^{-1}c_D^f with A_D=I+chi Gamma_D. On S, P_0^f vanishes, so(12) implies
\[
 \|E_D^f\|_{L^2(S)}
 =\frac{\|P_D^f-P_0^f\|_{L^2(S)}}{\epsilon_0 b}
 \le\|E_0^f\|_{L^2(S)}
 \le3\sqrt{V_S}|f|.
 \tag{17a}
\]
The first inequality uses the full-domain contraction before restriction to S. It is not a pointwise field bound.

Reciprocity of the real symmetric Gamma_D makes A_D and its inverse symmetric with respect to the complex bilinear pairing integral(v dot w). This is a transpose identity, not a Hermitian-adjoint identity. Testing(12) with A_D^{-T}c_D^f gives exactly
\[
 f^T(\alpha_D-\alpha_0)e
 =\epsilon_0\chi\int_S E_D^f(x)\cdot E_0^e(x)\,dx.
 \tag{17b}
\]
The fields can be complex; absolute-value Cauchy–Schwarz still applies to this bilinear integral. Using(17a) and the ball background bound yields the stronger estimate
\[
 \|\alpha_D-\alpha_0\|_{\rm op}
 \le9\epsilon_0 b V_S,\qquad
 Q_D\le Q_0+3(1+6\tau)b\,V_S/V_0.
 \tag{17c}
\]
To pass from the bilinear estimate to the operator norm, choose arbitrary unit complex e and f, using the conjugate of a Hermitian dual vector as f. The norm of f is unchanged.

The code independently reconstructs(17b) for a general symmetric two-site matrix and arbitrary incident/test vectors, checking the exact rational-function identity. It also checks A_D^*A_D=I+b^2 Gamma_D^2 for a non-diagonal rational matrix. These finite controls verify algebra and transpose conventions; they do not substitute for the continuum proof.

## 5. A connected smooth continuum counterfamily at the 1% gate

Keep D_0 fixed. Outside it, place a closed spherical metal balloon enclosing a fixed volume comparable to V_0, and connect its outer surface to the ball by a smooth thin metal neck. Its wall and neck can have arbitrarily small total volume V_S while the enclosed vacuum stays macroscopic. The connection need not puncture the inner cavity. Smooth the junctions outward and retain D_0 as a subset. Each member can be connected with C^{1,beta} boundary; no uniform lower wall/neck thickness or uniform boundary regularity constant is asserted.

Choose the balloon's outer enclosed volume V_0 and keep its void at least V_0-V_S. The filled closed-void fraction then obeys
\[
 \phi_D
 =\frac{V_{\rm void}}{V_0+V_S+V_{\rm void}}
 \ge\frac{V_0-V_S}{2V_0}.
 \tag{18}
\]
At tau=1/100, b=100 and V_S/V_0<=10^{-5},(17c) gives
\[
 Q_D\le
 \frac{1+18/10^4}{1+9/10^4}
 +3(1+6/100)100\,10^{-5}
 =\frac{502491431}{500450000}
 =1.004079190728\ldots
 <\frac{100}{99}.
 \tag{19}
\]
Yet (18) gives phi_D>=.499995. Consequently replacing the static PEC trace by this loss-corrected witness in the 1% receiver would falsely accept an admitted member of this unqualified continuum family.

The earlier conservative square-root estimate is retained as a separate completed arithmetic control: at V_S/V_0<=10^{-12},(17) gives 5009530477/5004500000=1.001005190728...<100/99 with phi_D>=.4999999999995. The stronger linear estimate supersedes its necessary small-volume scale.

Equation(16) also shows convergence of every entry of the complex dipole tensor to that of the ball, despite the persistent closed void. It works simultaneously at any fixed finite collection of Ohmic contrasts by choosing V_S small enough for their maximum b. If exact mass matching is desired, rescale D by [V_0/(V_0+V_S)]^{1/3}; its mass becomes exactly the ball's, its dipole tensor still converges to the ball's, and its void fraction is unchanged.

Thus finite-precision, finite-frequency dipole data plus mass cannot give a geometry-uniform robust extension that accepts the ball with a positive tolerance and excludes every such hollow continuum body. This is a stability restriction on the admitted model class, not a claim that exact noiseless data are equal.

## 6. Physical boundary of the counterfamily

The construction deliberately spends small features. At the sharper displayed ratio V_S/V_0=10^{-5} for comparable spheres of radius 15 micrometres, the shell-only thickness scale is about 50 picometres, before paying the neck. This is atomic scale. The older conservative ratio 10^{-12} would imply about 5e-18 metres. Pure local continuum conductivity, connected thin-film material and uniform surface chemistry at either displayed scale are not physically qualified. Moreover b=100 is an abstract contrast, not a value acquired for actual Al at the carrier frequencies. Its relation b=sigma/(epsilon_0 omega), the quasistatic limit and the thin-film constitutive law all need physical admission.

Accordingly this is not a manufacturing recipe, a practical powder false-acceptance demonstration, or a proof that a physically constrained powder device is impossible. It establishes that the proposed spectral shortcut cannot remove the need for a quantitative geometry/material/relaxation admission bound. A lower wall/neck scale, adequate spectral relaxation control, or an independently bounded physical-to-PEC response could remove this continuum sequence and must be paid for by a different operation.

The original T-powder-closed-void receiver explicitly requires such a response premise. It survives this challenge unchanged.

## 7. Controls and what remains unknown

The spherical-shell boundary calculation is the ordinary exact electrostatic comparator and is stronger than applying only the two spectral sum rules. The connected counterfamily is proved by the full volume-integral equation and its contraction estimate; an isolated-sphere sum is retained only as a diagnostic in the JSON output.

The code checks rational identities, shell parameters, the reciprocal perturbation identity, contraction Gram algebra, the arithmetic of(19) and the void lower bound. It does not solve an explicit smoothed balloon boundary mesh or validate continuum material at atomic scale. The analytic estimate, rather than a numerical additive-body approximation, carries the claimed continuum conclusion.

No finite-conductivity enclosed-volume certificate, practical admission rule, improved sensor cost, or advantage over a fully informed spectral/complex-polarizability method has been acquired.
