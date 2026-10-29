# Phase replacement under weak current tilts

**Date:** 2026-10-29.  
**Scope:** a proved constructive connection for continuation 7. This file proves the needed phase replacement and its initial-law scope. It does not assert a full density/current large-deviation principle. Mathematical tilted laws are comparison measures, not an additional supplied physical actuator.

Use the model, reference measure, and Dirichlet forms in `ORDINARY_ENTROPY_HYDRODYNAMICS.md`: `V=N^d`, actual macroscopic generator

\[
L_N=N^2\sum_b c_b(\eta,\theta,z)(T_b-I)
   +N^2\kappa_N\sum_b\partial_{\theta_b}^2,
\qquad
c_b=\frac s2(1+\alpha_b\cos\theta_b),
\]

with bounded phase-independent amplitudes invariant under their own swap. The bounds below are uniform in the frozen parameter `z`, with `c_max=s(1+a_0)/2`.

## 1. A direct form estimate, retaining visible dissipation

Consider a time-dependent mathematical comparison generator

\[
L_N^{q}(t)f
=N^2\sum_b c_b e^{q_b(t,\eta,\theta)}(f^b-f)
 +N^2\kappa_N\sum_b\partial_{\theta_b}^2f,
\qquad |q_b|\le K/N.
\tag{1}
\]

The current tilts needed for exclusion have

\[
q_{(x,x+e_j)}=
N^{-1}(\eta_x-\eta_{x+e_j})E_j(t,x/N)
\tag{2}
\]

for a fixed smooth bounded field `E`. The form estimate allows the larger class (1). No reversibility of `L_N^q` is assumed.

For a complex form-domain function `f`, Cauchy–Schwarz gives

\[
|\langle f,(L_N^q-L_N)f\rangle|
\le N^2
\left[\int\sum_b c_b|e^{q_b}-1|^2|f|^2d\mu_N\right]^{1/2}
\sqrt{2D_{\rm vis}(f)}.
\tag{3}
\]

Since `|e^q-1|<=K e^K/N` and there are `dV` bonds, Young's inequality yields

\[
\operatorname{Re}\langle f,L_N^q(t)f\rangle
\le-\frac{N^2}{2}D_{\rm vis}(f)
-N^2\kappa_ND_\theta(f)+C_KV\|f\|_2^2,
\tag{4}
\]

where one valid uniform constant is

\[
C_K=c_{\max}dK^2e^{2K}.
\tag{5}
\]

This calculation differentiates neither the modulation amplitudes nor the tilt. Its important feature for subsequent occupation estimates is that half of the original visible Dirichlet form remains available.

## 2. Centered phase potentials

Let

\[
F_{N,t}(\eta,\theta,z)=\sum_bu_{b,t}(\eta,z)\cos\theta_b,
\qquad
\sup_{t,\eta,z}\sum_bu_{b,t}^2\le C_F N^2/V,
\tag{6}
\]

where all coefficients are independent of the phases. They may depend on the entire visible configuration. Phase integration by parts gives

\[
\left|\int F_{N,t}|f|^2d\mu_N\right|
\le 2\sqrt{C_F}\frac N{\sqrt V}\|f\|_2\sqrt{D_\theta(f)}.
\tag{7}
\]

Combining (4) and (7), and completing the square, proves

\[
\operatorname{Re}\langle f,(L_N^q(t)+\gamma VF_{N,t})f\rangle
\le V\left(C_K+\frac{C_F\gamma^2}{\kappa_N}\right)\|f\|_2^2.
\tag{8}
\]

This holds for every real `gamma`. The bound is also valid for time-dependent coefficients: the corresponding backward Feynman–Kac equation, with time reversed to make it an initial-value equation, has the same `L2(mu_N)` energy inequality at each time. Gronwall and Cauchy–Schwarz against the constant function one give

\[
\mathbb E_{\mu_N}^{q}
\exp\left\{\gamma V\int_0^TF_{N,t}(X_t)dt\right\}
\le\exp\left\{VT\left(C_K+\frac{C_F\gamma^2}{\kappa_N}\right)\right\}.
\tag{9}
\]

The bounded state-dependent jump rates and compact phase diffusion give the ordinary evolution/Feynman–Kac construction. Measurable time dependence can be obtained from bounded step approximations. In (9), the tilt is a specified function of time and state; a separate likelihood argument below covers general bounded predictable tilts.

If an initial density satisfies `d nu_N/d mu_N <= exp(hV)`, Chernoff's inequality gives, when `C_F>0`,

\[
\frac1V\log\mathbb P_{\nu_N}^q
\left(\left|\int_0^TF_{N,t}dt\right|>\epsilon\right)
\le h+\frac{\log2}{V}+C_KT
-\frac{\kappa_N\epsilon^2}{4C_FT}.
\tag{10}
\]

In particular, for `kappa_N -> infinity`, the probability is superexponentially small at speed `V`. If `C_F=0`, the phase potential is identically zero and the assertion is exact. From (6), `||F_{N,t}||_infinity <= sqrt(d C_F)N`; a deterministic time grid therefore gives the same conclusion for the supremum of the accumulated integral over `[0,T]`.

The leading phase term in the density or current drift has the scaling in (6). Phase terms in the quadratic weak-tilt compensator have smaller coefficients, usually `sum_b u_b^2=O(1/V)`, and hence also satisfy this lemma. This observation is a scale check, not a substitute for writing the actual current likelihood expansion.

## 3. A simpler likelihood transfer supplied independently by the root role

The root role independently supplied the following shorter route for transferring already-proved superexponential events. It is recorded here to make the relationship explicit; the direct form bound (4) remains useful when visible dissipation must be retained.

Let `q_b(t)` be any bounded predictable tilt with `|q_b|<=K/N`, and let `J_b` count the corresponding native transitions. Starting from the same arbitrary initial law, the likelihood of the tilted jump law relative to the untilted law is

\[
Z_q(T)=\exp\left\{
\sum_b\int_0^T q_b\,dJ_b
-\int_0^TN^2\sum_bc_b(e^{q_b}-1)dt
\right\}.
\tag{11}
\]

The diffusion law of the phases is unchanged. Zero-rate transitions cause no division problem: both laws have the same support, and the expression is the standard counting-process exponential. Bounded rates on a finite horizon make these exponentials true martingales. The exact identity

\[
Z_q(T)^2=Z_{2q}(T)
\exp\left\{\int_0^TN^2\sum_bc_b(e^{q_b}-1)^2dt\right\}
\tag{12}
\]

implies

\[
\mathbb E[Z_q(T)^2]\le e^{C_KVT}.
\tag{13}
\]

Consequently every path event satisfies

\[
\mathbb P^q(E)\le
e^{C_KVT/2}\mathbb P(E)^{1/2}.
\tag{14}
\]

Thus a superexponential event at speed `V` remains superexponential under any such weak predictable tilt. This requires neither stationarity of the tilted law nor phase equilibrium at initialization. Its use presupposes a valid untilted estimate for the event in question; it cannot manufacture an occupation-replacement estimate from the phase estimate alone.

## 4. Active initialization and retained information

Let the initial law be arbitrary, even singular in all phase coordinates and correlated with the visible configuration. Fix `u>0`. Run the actual dynamics for physical time `u/kappa_N`, equivalently macroscopic time

\[
\delta_N=u/(\kappa_NN^2).
\]

The phases evolve autonomously even under (1), because only the visible jump rates were changed. Their joint marginal at that time has density at most `K_u^(dV)` relative to product Haar measure, where `K_u` is the supremum of the single-circle heat kernel. A conditional visible configuration has probability at most one. The joint law therefore obeys

\[
\frac{d\nu_N'}{d\mu_N}\le
2^VK_u^{dV}=e^{h_uV},\qquad h_u=\log2+d\log K_u.
\tag{15}
\]

For a potential in (6), its accumulated integral over this layer is deterministically bounded by

\[
\sqrt{dC_F}\,u/(\kappa_NN).
\tag{16}
\]

It follows by applying (10) after the layer that the phase-replacement assertion holds from arbitrary initial laws. No isolation of the visible dynamics was used. The same layer changes a smooth empirical-density test by expected total variation `O(1/(kappa_N N))`.

These assertions hold conditionally on any pre-existing record `D` and frozen parameter `z` only if the complete future native-and-actuator process retains the declared conditional generator law, including native jump innovations and fresh actuator inputs. Fresh bath noise alone is insufficient if the record exposes future native innovations. The number of retained record values is irrelevant to these pointwise bounds. They do not imply that a confidence statement about an estimated parameter becomes a posterior statement after conditioning on arbitrary calibration data.

For a weak current tilt, the number of native jumps during this layer is dominated by a Poisson variable of mean `C V/kappa_N`. A smooth integrated empirical-current test changes by at most `||H||_infinity/(NV)` per jump. A change of fixed size therefore requires order `NV` jumps. The Poisson Chernoff bound makes this initial current contribution superexponentially small at speed `V`; its exponent divided by `V` is of order `-N log(N kappa_N)` for fixed nonzero threshold. This is stronger than a mean estimate and is the relevant initialization statement for a current large-deviation argument.

## 5. What remains before an action theorem follows

The preceding statements close the phase replacement and initialization connection, including weak comparison tilts. They leave distinct tasks:

1. **Occupation replacement.** The nonlinear mobility contains `(eta_x-eta_y)^2`. Replacing it by `2 rho(1-rho)` requires local-equilibrium estimates. If `a_0<1`, then `c_min=s(1-a_0)/2>0` and the visible Dirichlet form dominates the SSEP exchange form. That supplies the ordinary one-block/two-block route even when the coefficients themselves depend nonlocally on `eta`. At `a_0=1`, this particular domination argument is unavailable; another lemma is needed.

2. **Path topology and tightness.** The phase drift is bounded pointwise only by `O(N)`. A current-compensator proof that blindly imports the unmodulated pointwise `O(V)` estimate loses a factor `N`. Use superexponential phase replacement before the short-time exponential-martingale estimate. Control of every fixed smooth test is not automatically a compact-containment theorem in an unstated path topology.

3. **Upper bounds.** An exponential martingale yields a local or compact-set bound only after its compensator is replaced and the test functional is continuous in the chosen topology. Extending it to arbitrary closed sets requires exponential tightness. Identifying the supremum over smooth tests with the proposed action requires the continuity equation and the appropriate finite-energy representation.

4. **Lower bounds.** Tilted empirical-density and current laws must converge to the controlled macroscopic equation. Occupation replacement, uniqueness of that equation, and the likelihood cost are all needed. Extending a lower bound from smooth positive-density paths to every finite-action path requires an action-preserving approximation argument.

5. **Initial law.** Mere convergence in probability of the initial empirical density is sufficient for the mean theorem, but not for a dynamical LDP with a fixed initial condition. Use deterministic configurations approaching the specified profile, superexponential initial concentration, or an explicitly stated initial LDP and its added rate. The phase regularization does not repair a wrong rare-event law of the conserved initial occupations.

6. **Confidence and records.** A fixed acquisition failure probability `beta` added to an `exp(-V I)` bound erases its exponent. An unconditional speed-volume assertion needs a sufficiently small failure budget (superexponential if transferring superexponential events), an explicitly conditional-on-coverage result, or a robust action interval valid on every admitted parameter. A fixed-confidence population statement does not supply that budget.

7. **No action transfer from a coarse density ceiling alone.** The factor `exp(hV)` in (15) is harmless when transferring a superexponential replacement event. It is not harmless for a finite rate `I`: multiplying `exp(-V I)` by it shifts the exponent. The actual action must be obtained from the process's own exponential martingales and tilted lower bound.

## 6. A precise continuous-path convention

At finite `N`, empirical density and integrated current have jumps. The event that such a path is literally continuous generally has probability less than one and often tends to zero. Statements that only continuous limiting paths matter must not be rewritten as a literal claim that discontinuous finite-system paths have superexponentially small probability.

A clean convention is to use the usual Skorokhod space and prove exponential continuous tightness. Alternatively, linearly interpolate between successive visible jump times. A density jump has total variation at most `2/V`, and a current jump at most `1/(NV)`. The interpolated path is therefore deterministically within these respective uniform weak bounds of the original path. For each fixed positive tolerance, the two versions are exponentially equivalent with error probability exactly zero for all sufficiently large `N`. The interpolation is a mathematical representation, not an added physical operation.

## 7. Primary comparison

The closest inspected classical target is Bertini–De Sole–Gabrielli–Jona-Lasinio–Landim, [Large deviations of the empirical current in interacting particle systems](https://arxiv.org/pdf/math/0512394), especially Section 3: weak tilts, superexponential occupation replacement, compact-set upper bounds, current tightness, and smooth-path lower bounds. The present phase lemma supplies an extra replacement input; it does not make those remaining steps disappear.

General fast-environment path large deviations are also established. Kraaij–Schlottke, [A large deviation principle for Markovian slow-fast systems](https://arxiv.org/pdf/2011.05686), express the effective action through fast occupation measures or an eigenvalue problem. Their fixed compact fast space and finite-dimensional slow-state framework do not directly include the growing `dV`-phase conservative spatial system here. The relevant distinction is a uniform-in-volume supplier, not the generic idea that sufficiently fast dynamics can average rare-event behavior.

