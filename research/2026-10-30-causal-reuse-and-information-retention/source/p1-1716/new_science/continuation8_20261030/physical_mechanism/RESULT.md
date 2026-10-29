# Round8 complementary construction: a programmable activity clock and its obstruction

## Completed answer

A genuine common multiplicative-speed port, driven by a known finite-state controller, programs the full macroscopic transport action without learning the hidden kinetic amplitudes removed by the accepted base operation. The operation is an exact stochastic time change of one persistent specimen. It is a strong ordinary alternative with direct switching-diffusion and slow-fast large-deviation predecessors.

It also answers the comparison question decisively: **autonomous positive common activity noise cannot suppress equilibrium circulation at unchanged mean speed.** It retains mean diffusion and leading equilibrium circulation variance while broadening rare tails. Root's event-updated mechanism is therefore targeting a capability beyond this ordinary global-clock construction.

## Governing proof

`COMMON_ACTIVITY_CLOCK_AND_ITS_LIMIT.md` gives the actual port, full joint generator, initial laws, retained-clock scope, path contraction, scalar rate/SCGF, a separate stationary functional CLT, bandwidth regimes, and a stronger threshold-and-hold feedback comparison.

For base D=s/2, chi(rho)=rho(1-rho), positive speeds g_0<g_1, and a physical two-state gate generator Q/N, define

\[
\ell_Q(a)=\left[\sqrt{r(1-x)}-\sqrt{l x}\right]^2,
\qquad x=(a-g_0)/(g_1-g_0).
\]

The full action is

\[
I_T^{\rm gate}(\rho,j)=\inf_a\int_0^T
\left\{\frac1{2s}\int\frac{[j+aD\rho_x]^2}{a\chi(\rho)}dx
+\ell_Q(a)\right\}dt.
\]

The activity a(t) is common to space. Eliminating it supplies a calculable nonlocal history cost, not just a modified diffusion coefficient. For v=s chi(m), terminal circulation has

\[
I_T(q)=\min_a\{q^2/(2vTa)+T\ell_Q(a)\},\qquad
\Lambda_T(\lambda)=T\lambda_{\max}(Q+(v\lambda^2/2)\operatorname{diag}g).
\]

At stationary mean speed one, choosing the zero-cost clock occupation gives

\[
I_T(q)\le q^2/(2vT),\qquad \Lambda_T(\lambda)\ge vT\lambda^2/2.
\]

Deterministic cycling of the same two levels, with the same duty fractions and order-N controller cycles, achieves the unbroadened mean-speed law. A nontrivial clock occupation cost at speed N requires physical gate bandwidth of order 1/N. A clock whose physical switching rate stays positive or diverges is already too fast to retain this occupation-tail effect. This differs from the physically fast shared-sign mechanism.

## Actual joint-correlation consequence

Two separately supplied specimens may use a shared gate or independent copies of the same gate. Their individual gate and specimen laws are identical across these programs. The shared joint SCGF is

\[
T k_Q((v_1\lambda_1^2+v_2\lambda_2^2)/2),
\]

whereas independent gates give the sum of the two individual SCGFs. The shared mixed fourth derivative is

\[
2T\operatorname{Var}_{\pi_Q}(g)v_1v_2/(r+l)>0,
\]

and the independent one is zero. This is an ordinary way to program correlated rare transport bursts while preserving every individual controller law. It uses separate hardware, not copying of hidden states. Equal total actuation cost for shared and independent sources is not assumed.

## Stronger ordinary suppression route and its price

If an actual global hold and continuous signed-current sensing are additionally supplied, stop the specimen when |J| first reaches h_N=o(N^2). Then every fixed nonzero macroscopic circulation is excluded. For h_N=N^(3/2+e), 0<e<1/2, the stationary maximal second-moment estimate makes the hold trigger with probability O(N^(-2e)); typical paths survive while rare circulation is clipped.

This needs event sensing at order-N physical native intensity, a current counter, timely global actuation and a true hold. It arrests all density dynamics after triggering. It is a valid comparator for terminal circulation suppression, but does not reproduce mode-specific suppression with a prescribed full density evolution. These operations are not inferred from the inherited phase port or positive speed levels.

## Physical scope and costs

The extra premise is a warranted operation g_k B_N on the **whole** supplied physical generator. A native-only multiplier with unscaled evolving hidden dynamics does not supply the exact time change. Frozen hidden sectors pose no issue. A common Arrhenius barrier shift with unchanged prefactors is an illustrative rate-model supplier; no apparatus or precision certificate is established.

On physical horizon N^2T the global gate switches order N times. Its command reaches the native and phase apparatus. The base operation still spends order gamma_N N^3T local sign events and order N^3T native opportunities. Initialization, timing, sensing, calibration, randomization and records retain their real costs. No energy or speedup claim follows from a rate factor.

The full path theorem uses the inherited deterministic flat-profile initial sequence. The actual stationary CLT is separately proved under canonical occupancy and independent fair signs. Conditional old-record claims require the entire future conditional joint law and fresh independent gate innovations to remain stated. The action includes a retained coarse operational clock; conditioning on a rare clock removes its paid occupation cost. No joint LDP for every fine apparatus timestamp is claimed.

## Executed algebra and design comparison

`check_activity_clock.py` produced `ACTIVITY_CLOCK_CHECKS.json`. It independently compares the two-state eigenvalue with its closed formula, occupation minimization with the Legendre transform, finite-N clock-only Feynman--Kac matrices, exact augmented finite SSEP generators, and shared/independent gates with matched marginal laws.

The largest scalar duality discrepancy was 1.78e-15. The largest augmented-generator identity discrepancy was 7.44e-15. These are population algebra checks, not acquired trials or numerical proof of the LDP.

For g_0=0.25, g_1=1.75, r=l=1, v=0.8 and T=1.3, both clock programs have mean speed one. At q=5 the random-gate rate is about 7.90226, versus 12.01923 under the deterministic mean clock. The minimizing occupation spends about 96.2 percent of the interval in the fast state. This illustrates tail broadening without claiming finite-device accuracy of the asymptotic exponents.

## Primary comparisons that changed selection

Huang--Mandjes--Spreij, [Large deviations for Markov-modulated diffusion processes with rapid switching](https://arxiv.org/pdf/1501.03020), supplies the occupation/path framework; its model, rate definition, Theorem 3.1 and Corollary 3.3 were inspected. Kraaij--Schlottke, [A large deviation principle for Markovian slow-fast systems](https://arxiv.org/pdf/2011.05686), supplies the broader variational/eigenvalue predecessor. Gueneau--Majumdar--Schehr, [Large Deviations in Switching Diffusion](https://arxiv.org/pdf/2501.13754), explicitly treats the two-diffusivity spectrum and rare tails. Those concepts and scalar formulas are established.

For root's paired-current target, two inspected primary predecessors are material: Hexner--Levine, [Noise, diffusion, and hyperuniformity](https://arxiv.org/pdf/1611.02386), and Morningstar--O'Dea--Richter, [Hydrodynamics in long-range interacting systems with center-of-mass conservation](https://arxiv.org/pdf/2304.12354). They preempt broad novelty claims about equal/opposite kicks or engineering hydrodynamics through pair-current constraints. The first is nonequilibrium and changes static fluctuations; the second varies pairing distance and includes diffusive regimes. Neither inspected passage supplies root's exact reversible event-gate compiler or its full action. Those narrower claims require their own construction and comparison.

## Unresolved operation

This unit does not implement the global multiplicative-speed port from inherited phase controls. Nor does it prove a physical event-updated directional gate, instantaneous global broadcast, finite-size action accuracy or practical superiority. Its completed contribution is the constructive ordinary comparison and rigorous fixed-mean obstruction, allowing selection to focus on the stronger mode-specific suppression capability.
