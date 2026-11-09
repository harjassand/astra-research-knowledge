# P2 complete visible return

Source: https://chatgpt.com/c/6af1715f-dbc4-83ec-a58c-3bca5bb0fe65
Actual prompt: P2_FULL_BODY_FORCE_AFTER_A873_XI_20261110.txt; followed by exact recovery message `please continue.`
Model: GPT-6 standard, Extra High, per dispatch receipt. Response c44d708a-3022-4f43-a677-13b858451da5. No ZIP visible.

## Complete response (native copy)

# P2 — Further research on universal additive-force control

Status: the full common-force, all-\\(H^1\\), all-Leray–Hopf compiler remains open. This continuation produces a new exact nonlinear actuator obstruction and examines a previously untreated quadratic resonance in the balanced-shear construction.

## 1. New obstruction: triangular multidirectional actuator families

The earlier obstructions exclude collinear forcing, single Fourier lines, Beltrami eigenspaces and planar monochromatic spaces. There is another invariant class that need not satisfy any of those restrictions.

Consider the infinite-dimensional space

\\[ \mathcal T= \left\\{ U(x)= \begin{pmatrix} v(x_2,x_3)\\\ w(x_3)\\\ 0 \end{pmatrix}: \int\_{\mathbb T^3}U\\,dx=0 \right\\}. \\]

Suppose every actuator belongs to \\(\mathcal T\\). The actuators may contain arbitrarily many fixed Fourier modes, both \\(e_1\\) and \\(e_2\\) velocity components, and two independent spatial wavevector directions.

### Theorem — Triangular-force obstruction

For every prescribed additive force \\(f(t)\in\mathcal T\\), every \\(\nu>0\\) and every \\(\tau>0\\), there is an initial condition of \\(H^1\\) norm \\(M\\) producing an exact smooth solution with

\\[ \boxed{ \\|U(\tau)\\|\_2\ge \frac{M}{\sqrt{1+4\pi^2}} e^{-4\pi^2\nu\tau}. } \tag{1} \\]

Therefore no actuator family contained in \\(\mathcal T\\) satisfies the full universal compiler assertion.

Proof. The nonlinear equation preserves the triangular structure. Indeed,

\\[ (U\cdot\nabla)U= \begin{pmatrix} w(x_3)\partial_2v(x_2,x_3)\\\ 0\\\ 0 \end{pmatrix}. \\]

This vector is already divergence-free, so its Leray projection is unchanged.

Writing \\(f=(f_1(x_2,x_3),f_2(x_3),0)\\), the exact nonlinear equations reduce to

\\[ \begin{aligned} w_t&=\nu\partial_3^2w+f_2,\\\ v_t&=\nu(\partial_2^2+\partial_3^2)v -w\partial_2v+f_1. \end{aligned} \tag{2} \\]

The second velocity component is an autonomous forced heat equation, even though the first velocity component experiences genuine nonlinear advection.

Choose two initial conditions

\\[ U_0^\pm= \pm\frac{\sqrt2 M}{\sqrt{1+4\pi^2}} e_2\cos(2\pi x_3). \\]

Both have \\(H^1\\) norm \\(M\\). Their second components retain the exact difference

\\[ w^+(\tau)-w^-(\tau)= \frac{2\sqrt2M}{\sqrt{1+4\pi^2}} e^{-4\pi^2\nu\tau}\cos(2\pi x_3). \\]

At least one complete velocity therefore has the lower bound (1). The reduced system has global smooth solutions for these smooth forcing coefficients, so the counterexample applies to the admitted weak-solution class without invoking nonuniqueness.

For example, the actuator family

\\[ \begin{aligned} G_1&=e_1\sin(2\pi x_2),\\\ G_2&=e_1\cos(4\pi x_3),\\\ G_3&=e_2\sin(2\pi x_3) \end{aligned} \\]

is excluded. Its members are not confined to one Fourier line, one Laplacian eigenspace or a common Beltrami eigenspace.

The underlying obstruction is an autonomous quotient of the full nonlinear dynamics, rather than an Euler-null invariant space.

This remains a restricted-family negative result. It does not exclude actuator families containing sufficiently coupled modes in all three directions.

## 2. An amplitude-independent nonlinear estimate for a genuinely infinite-dimensional sector

The next result is constructive. It addresses the central difficulty with the previous balanced-shear strategy: the available relative-energy estimate grows like \\(\exp(CAT)\\), which overwhelms enhanced dissipation.

There is a nonlinear sector where that exponential dependence can be eliminated exactly, even for arbitrarily large prescribed shear amplitudes.

### Theorem — Nonlinear scalar response under an unknown planar perturbation

Let \\(\kappa=2\pi\\), and define the four-dimensional space

\\[ \mathcal E= \operatorname{span}\\{ e_1\sin(\kappa x_2),e_1\cos(\kappa x_2), e_2\sin(\kappa x_1),e_2\cos(\kappa x_1) \\}. \\]

Choose any prescribed time-dependent \\(b(t)\in\mathcal E\\), with \\(b(0)=0\\), and temporarily take the exact force

\\[ f=b_t+\nu\kappa^2b. \\]

The unknown initial condition is

\\[ U_0=V_0+e_3\phi, \\]

where \\(V_0\in\mathcal E\\), while \\(\phi\\) is an arbitrary mean-zero scalar in \\(L^2(\mathbb T^2)\\). There is no Fourier cutoff on \\(\phi\\).

The full nonlinear 2.5-dimensional solution has the exact representation

\\[ \boxed{ U(t)=b(t)+e^{-\nu\kappa^2t}V_0+ e_3 S\_{V_0}(t). } \tag{3} \\]

Here \\(S\_{V_0}\\) solves the passive advection–diffusion equation driven by the actual planar velocity \\(b(t)+e^{-\nu\kappa^2t}V_0\\).

Let \\(S_0^b\\) instead solve the scalar equation driven only by the prescribed \\(b(t)\\), with the same scalar initial condition \\(\phi\\).

Then

\\[ \boxed{ \\|S\_{V_0}(t)-S_0^b(t)\\|\_2 \le \\|V_0\\|\_2\\|\phi\\|\_2 \sqrt{\frac{t}{\nu}}. } \tag{4} \\]

This holds for every \\(t\ge0\\), independently of the amplitude, frequency of temporal switching and spatial gradients of \\(b\\).

### Proof

Because every element of \\(\mathcal E\\) is a planar monochromatic Euler-null field, the projected quadratic nonlinearity of its planar component vanishes. Consequently, its full nonlinear evolution is exactly the forced heat equation:

\\[ U\_\parallel(t)=b(t)+e^{-\nu\kappa^2t}V_0. \\]

The third velocity component has no feedback on the planar equation, so it satisfies scalar advection–diffusion.

Set \\(D=S\_{V_0}-S_0^b\\). Subtracting the two scalar equations gives

\\[ D_t+U\_\parallel\cdot\nabla D =\nu\Delta D-e^{-\nu\kappa^2t}V_0\cdot\nabla S_0^b, \qquad D(0)=0. \\]

The prescribed and unknown planar advection cancels from the \\(L^2\\) energy estimate:

\\[ \\|D(t)\\|\_2 \le\\|V_0\\|\_\infty \int_0^t\\|\nabla S_0^b(s)\\|\_2\\,ds. \\]

Meanwhile scalar dissipation gives

\\[ 2\nu\int_0^t\\|\nabla S_0^b(s)\\|\_2^2ds \le\\|\phi\\|\_2^2. \\]

Finally, the explicit four-mode space satisfies

\\[ \\|V_0\\|\_\infty\le\sqrt2\\|V_0\\|\_2. \\]

Cauchy–Schwarz proves (4).

The bound applies to arbitrary finite perturbation sizes, not merely to a Taylor coefficient or linearization. In particular, on \\(\\|V_0\\|\_2,\\|\phi\\|\_2\le M\\),

\\[ \sup\\|S\_{V_0}(t)-S_0^b(t)\\|\_2 \le M^2\sqrt{\frac{t}{\nu}}. \\]

Thus an arbitrarily strong prescribed planar shear can act on an entire infinite-dimensional scalar preparation class with a nonlinear error that tends to zero as the pulse duration tends to zero.

### Exact rational force realization

The preceding theorem uses \\(\nu\kappa^2\\), which is generally irrational. This can be fixed without destroying the result.

Choose a rational \\(\lambda\\) with

\\[ |\lambda-\nu\kappa^2|\le\zeta \\]

and output the admissible rational force

\\[ f=b_t+\lambda b. \\]

The actual planar background is now \\(b+r\\), where

\\[ r(t)=(\lambda-\nu\kappa^2) \int_0^t e^{-\nu\kappa^2(t-s)}b(s)\\,ds. \\]

It remains exactly in \\(\mathcal E\\), and

\\[ \\|r(t)\\|\_\infty \le\sqrt2\zeta\int_0^t\\|b(s)\\|\_2\\,ds. \\]

Comparing the actual scalar flow to the ideal flow driven by \\(b\\) gives the explicit fully rational-control error estimate

\\[ \boxed{ \\|S\_{\mathrm{actual}}(t)-S_0^b(t)\\|\_2 \le \left( \sqrt2\\|V_0\\|\_2+ \sqrt2\zeta\int_0^t\\|b(s)\\|\_2ds \right) \\|\phi\\|\_2\sqrt{\frac{t}{2\nu}}. } \tag{5} \\]

Every term is computable from the control and preparation bounds. The exact force uses only the four fixed rational trigonometric fields.

Scope: (4)–(5) concern exact 2.5-dimensional dynamics with no off-sector disturbance. They do not control general three-dimensional perturbations. They also do not suppress the surviving planar component \\(e^{-\nu\kappa^2t}V_0\\). Indeed, the accepted monochromatic obstruction proves that a force confined to \\(\mathcal E\\) cannot solve the full problem.

Nevertheless, this supplies an amplitude-independent, nonperturbative nonlinear comparison for infinitely many initial scalar degrees of freedom. It is stronger than a bound for finitely many selected Fourier interactions.

## 3. A sharp nonlinear resonance calculation for the balanced loop

The accepted earlier calculation showed that one quadratic interaction decays like \\(T/\sqrt{AT}\\) as the shear impulse grows. It would be incorrect to extrapolate that rate to every quadratic interaction.

A different pair has a larger resonant response. Its exact asymptotic can be calculated.

### Set-up

Work first with the smooth inviscid forced Euler equation, using the accepted balanced background

\\[ a(t)=\alpha(t)e_1\sin(\kappa x_2), \quad \alpha(t)=A g(t/T), \quad L=AT. \\]

Let

\\[ G(z)=\int_0^z g(r)\\,dr,\qquad \Theta(t)=L G(t/T). \\]

Then \\(\Theta(5T)=0\\).

Choose the real initial perturbation

\\[ w_0=e_2\cos(\kappa x_1)+e_3\cos(\kappa x_1). \\]

Expand the exact smooth solution for small \\(\rho\\):

\\[ U^\rho(t) =a(t)+\rho w_1(t)+\rho^2w_2(t)+O(\rho^3). \\]

The planar part of \\(w_1\\) remains \\(e_2\cos(\kappa x_1)\\), while its vertical part is

\\[ (w_1)\_3 =\cos\left( \kappa x_1-\kappa\Theta(t)\sin(\kappa x_2) \right). \\]

The planar mode is a critical neutral mode, and the vertical mode is transported as a scalar.

The mean-in-\\(x_1\\) part of the second-order vertical response at the endpoint is therefore exactly

\\[ \boxed{ P\_{k_1=0}(w_2)\_3(5T,x_2) = \frac{\kappa^2TL}{2}\cos(\kappa x_2) \int_0^5 G(z) \sin\bigl(\kappa L G(z)\sin(\kappa x_2)\bigr)\\,dz. } \tag{6} \\]

This is a genuinely nonlinear interaction between a critical planar velocity mode and a transported vertical mode. Its output has zero streamwise frequency, so it is not removed by streamwise mixing.

### Exact large-impulse asymptotic

Define

\\[ J(\xi)=\int_0^5G(z)e^{-i\xi G(z)}\\,dz. \\]

The balanced trapezoid has four interior stationary points, at \\(z=1,2,3,4\\), with

\\[ (G(1),G(2),G(3),G(4)) = \left(\frac34,-\frac94,\frac94,-\frac34\right). \\]

On either side of each stationary point, \\(G\\) is exactly quadratic. Applying the elementary one-sided Fresnel integral to those eight quadratic pieces gives

\\[ J(\xi)=\xi^{-1/2} \sum\_{r=1}^4 c_r e^{-i\xi G(r)} +O(\xi^{-1}), \qquad \xi\to+\infty, \\]

with explicit nonzero coefficients \\(c_r\\).

The four values \\(G(r)\\) are distinct. Consequently, all cross-frequency terms have bounded logarithmic integrals, while the diagonal terms contribute a positive logarithmic mean:

\\[ \boxed{ \int_1^X|J(\xi)|^2d\xi =C\_\*\log X+O(1), } \tag{7} \\]

where

\\[ \boxed{ C\_\*= \frac{27\pi}{64} \left(2+\frac3{\sqrt6}\right)>0. } \\]

Substituting (7) into (6) and integrating over the normalized torus gives

\\[ \boxed{ \left\\|P\_{k_1=0}(w_2)\_3(5T)\right\\|\_2^2 = \kappa^2C\_\*T^2L\log L +O(T^2L). } \tag{8} \\]

In particular,

\\[ \boxed{ \left\\|P\_{k_1=0}(w_2)\_3(5T)\right\\|\_2 \sim \kappa\sqrt{C\_\*}\\, T\sqrt{L\log L}. } \tag{9} \\]

This is a sharp asymptotic for the specified nonlinear quadratic coefficient, not just an upper bound.

It demonstrates that the accepted \\(T/\sqrt L\\) suppression rate for the earlier special interaction cannot be a uniform estimate for the entire inviscid quadratic operator.

### A precise amplitude–duration window

Suppose

\\[ A=T^{-q},\qquad T\downarrow0. \\]

Then \\(L=AT=T^{1-q}\\). The resonant quadratic response behaves as

\\[ T\sqrt{L\log L} \asymp T^{(3-q)/2}\sqrt{\log(1/T)}. \\]

Thus this interaction vanishes when \\(q<3\\), but not when \\(q\ge3\\).

Meanwhile the accepted noncritical constant-shear enhanced-dissipation mechanism requires, for fixed positive viscosity,

\\[ \sqrt{\nu A}\\,T\longrightarrow\infty, \\]

which holds when \\(q>2\\).

The two requirements therefore admit the common window

\\[ \boxed{2\<q<3.} \tag{10} \\]

The preceding balanced-loop choice,

\\[ A=2^{8n},\qquad T=2^{-3n}, \\]

corresponds to \\(q=8/3\\), strictly inside that window. For this choice, the new resonant quadratic coefficient is

\\[ O(\sqrt n\\,2^{-n/2}). \\]

This gives an analytical explanation for why that particular scaling can simultaneously provide strong noncritical linear decay and suppress this more difficult nonlinear resonance.

The limit calculation is inviscid. It is not, by itself, a necessary amplitude scaling for the viscous full-control problem.

## 4. Physical viscosity suppresses the same resonance uniformly in shear amplitude

The inviscid asymptotic (9) might suggest that a sufficiently large impulse necessarily produces a large nonlinear response.

For the actual viscous equation, that inference is false.

In fact, the exact viscous quadratic response associated with the same initial pair satisfies an estimate independent of \\(A\\).

Let \\(S\\) solve

\\[ S_t+\alpha(t)\sin(\kappa x_2)\partial_1S =\nu\Delta S,\qquad S(0)=\cos(\kappa x_1). \\]

The planar first-order perturbation remains exactly

\\[ V(t)=e^{-\nu\kappa^2t} e_2\cos(\kappa x_1). \\]

The complete vertical second-order coefficient \\(W_2\\), not merely its streamwise average, satisfies

\\[ (W_2)\_t+ \alpha(t)\sin(\kappa x_2)\partial_1W_2 =\nu\Delta W_2-V\cdot\nabla S, \qquad W_2(0)=0. \\]

Divergence-free advection cancels from both energy estimates. Since

\\[ 2\nu\int_0^t\\|\nabla S(s)\\|\_2^2ds \le\\|S(0)\\|\_2^2=\frac12, \\]

and \\(\\|V(t)\\|\_\infty\le1\\), we obtain

\\[ \begin{aligned} \\|W_2(t)\\|\_2 &\le\int_0^t\\|\partial_2S(s)\\|\_2ds\\\ &\le\sqrt{\frac{t}{4\nu}}. \end{aligned} \\]

Therefore,

\\[ \boxed{ \\|W_2(5T)\\|\_2 \le\sqrt{\frac{5T}{4\nu}}, \qquad\text{for every amplitude }A. } \tag{11} \\]

This is a different type of estimate from the accepted oscillatory cancellation: it uses dissipation of the actual scalar gradient, rather than decay of an oscillatory time integral.

For fixed positive \\(\nu\\), it converges to zero as \\(T\to0\\), even when \\(A\\) increases arbitrarily rapidly.

The conclusion is stronger than an estimate for one projected Fourier mode. It controls the complete mixed quadratic response for this planar–vertical interaction.

Together, (9) and (11) establish a useful distinction:

- The inviscid quadratic response can grow with the shear impulse.
- The corresponding viscous response is uniformly bounded by \\(O(\sqrt{T/\nu})\\), regardless of that impulse.

Thus a universal inviscid bilinear estimate is not necessarily the right intermediate theorem for the additive-force problem. A formulation that preserves viscous dissipation throughout the nonlinear calculation can be substantially stronger.

### Disturbance-robust extension of Section 2

The amplitude-independent comparison also survives additive disturbances within the exact 2.5-dimensional invariant class.

Suppose

\\[ h(t)=h\_\parallel(t)+e_3h_3(t,x_1,x_2), \\]

where \\(h\_\parallel(t)\in\mathcal E\\), and \\(\\|h\\|\_{L^\infty_tL^2_x}\le\eta\\).

For the rational force in Section 2, compare the actual vertical scalar solution against the scalar equation driven by the prescribed \\(b(t)\\), with the same vertical disturbance \\(h_3\\). The energy argument gives

\\[ \boxed{ \begin{aligned} \\|S\_{\mathrm{actual}}(t)-S_b(t)\\|\_2 \le{}& \left( \\|V_0\\|\_2+\eta t+ \zeta\int_0^t\\|b(s)\\|\_2ds \right)\\\ &\times (\\|\phi\\|\_2+\eta t)\sqrt{\frac{t}{\nu}}. \end{aligned} } \tag{12} \\]

It holds uniformly over all initial conditions and disturbances in the stated invariant class. The amplitude of the prescribed \\(b\\) enters only through its rational-calibration error, which can be chosen arbitrarily small.

This is a genuine nonlinear, disturbance-robust comparison, but the restriction on the disturbance is essential. Arbitrary three-dimensional disturbances may leave the invariant class, and (12) does not control their subsequent interactions.

## 5. A polynomial energy envelope for every three-dimensional weak realization

There is also an unconditional estimate applicable to the full three-dimensional equation, rather than an invariant subsystem.

For the rational balanced-loop force

\\[ f=(\alpha'+\lambda\alpha) \sin(\kappa x_2)e_1, \\]

the accepted profile has the exact total-variation and integral identities

\\[ \int_0^5|g'(z)|\\,dz=32, \qquad \int_0^5|g(z)|\\,dz=12. \\]

Consequently,

\\[ \int_0^{5T}\\|f(t)\\|\_2dt \le \frac{32A+12|\lambda|AT}{\sqrt2}. \\]

For every admitted three-dimensional Leray–Hopf solution and every allowed additive disturbance, the ordinary energy inequality implies

\\[ \boxed{ \\|U(t)\\|\_2 \le M+ \frac{32A+12|\lambda|AT}{\sqrt2} +t\eta,\qquad 0\le t\le5T. } \tag{13} \\]

Since the comparison background satisfies \\(\\|a(t)\\|\_2\le6A/\sqrt2\\),

\\[ \boxed{ \sup\_{0\le t\le5T}\\|U(t)-a(t)\\|\_2 \le M+\frac{38A+12|\lambda|AT}{\sqrt2} +5T\eta. } \tag{14} \\]

These estimates are unconditional: no strong regularity, uniqueness, selected initial condition or Fourier truncation is used.

They show that the previously available factor \\(\exp(CAT)\\) is not an unavoidable bound on the actual absolute departure from the background. Every admitted weak realization has at most the displayed algebraic-in-\\(A\\) energy envelope.

However, (14) remains too weak to establish terminal contraction. Under the accepted amplitude scaling, an \\(O(A)\\) error is still enormous. Converting that global energy envelope into a small terminal error requires additional dissipation-sensitive estimates for the genuinely three-dimensional nonlinear interactions.

## 6. Where the full problem stands

RESULTS OF THIS CONTINUATION

| Result                                                           | Status and scope                                             |
| ---------------------------------------------------------------- | ------------------------------------------------------------ |
| Triangular multidirectional actuator obstruction                 | Exact nonlinear no-go for that entire family                 |
| Amplitude-independent nonlinear scalar comparison (4)            | Entire infinite-dimensional vertical-scalar class            |
| Rational realization and restricted disturbance robustness (12)  | Constructive, with explicit error                            |
| Sharp balanced-loop quadratic resonance (8)                      | Complete inviscid second-variation asymptotic                |
| Uniform viscous suppression (11)                                 | Exact mixed quadratic coefficient, arbitrary shear amplitude |
| Polynomial full-3D weak-solution energy envelope (14)            | Entire preparation class and all allowed disturbances        |
| Common additive-force contraction of the whole 3D \\(H^1\\) ball | Open                                                         |
| Full deterministic compiler and uniform complete-bit bounds      | Open                                                         |

The relevant existing controllability results remain distinct. Finite-dimensional additive control can achieve approximate controllability or exact control of specified projections, but these are not common controls guaranteeing a terminal bound simultaneously for every unknown initial condition. Local stabilization results likewise generally involve feedback or neighborhood restrictions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://epubs.siam.org\&sz=32)

epubs.siam.org+2



### The resulting research direction

The strongest positive result here is (4), especially its rational and disturbance-controlled form (12). It proves that nonlinear interactions involving an arbitrary infinite-dimensional scalar component can be handled without paying exponential-in-shear amplification.

The sharp calculation (8) then shows why the next theorem should retain viscosity from the outset: inviscid resonances can have much larger scaling, even where the corresponding viscous interaction is uniformly suppressible.

The remaining central problem is to extend this dissipation-based nonlinear control to interactions between all three velocity components, including pressure-projected stretching, without relying on an invariant 2.5-dimensional reduction. Such an extension must then be paired with a fixed multidirectional additive-force schedule that removes its own background and contracts the surviving low modes.

Until that genuinely three-dimensional estimate and a common-control construction exist, neither an unrestricted positive compiler nor a general negative theorem is justified. The full question remains open, but this continuation provides an amplitude-independent nonlinear mechanism that was absent from the preceding shear analysis.

## Available visible activity

Worked for 30m 34s.

Assessed the obstruction and developed the mechanism
Refined strategy, estimated errors, and tested cycle limits
Explored and refined averaged control cycles beyond the no-go
Strengthened obstruction analysis and estimated nonlinear echo effects
Searched the web
Analyzed and identified nonlinear resonance
Computed nonlinear echo suppression thresholds
Analyzed nonlinear effects and resonant interactions
Analyzed resonant interactions, scaling, and viscous effects
Searched the web
The resonance calculation has produced a useful distinction. In the inviscid equation, one mixed quadratic interaction can be much larger than the previously studied example. With physical viscosity restored, an energy estimate bounds that same interaction independently of the shear amplitude. I’m checking the exact asymptotics and the scope of the viscous estimate.
Assessed viscous mixing and sharpened nonlinear interaction bounds
Refined theorem, derived robust sector, and compared viscous effects
Sharpened the conclusion

### Visible Python analysis

```python
import sympy as s
z=s.symbols('z')
phi=[
(4*z,0,s.Rational(1,4)),(s.Integer(1),s.Rational(1,4),s.Rational(3,4)),(4*(1-z),s.Rational(3,4),1)
]
fareas=[s.integrate(p,(z,a,b)) for p,a,b in phi]
fareas

```
