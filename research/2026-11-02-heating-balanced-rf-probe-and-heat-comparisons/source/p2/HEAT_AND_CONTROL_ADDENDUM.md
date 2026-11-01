# Final pilot addendum: heat-transport discriminator and full comparator

**Scope:** Executable mathematical/finite-grid discrimination, not an RF-excited gyrokinetic experiment or a reactor-performance result. Previously preserved early analysis remains historical. This document supersedes any statement that only a *particle*-flux proxy was computed: a **passively advected model-temperature flux** was subsequently computed. It is not a self-consistent ion/electron gyrokinetic heat flux.

## 1. Acquired observable, rather than assuming squared shear measures heat

The 2D modified Hasegawa–Wakatani (mHW) numerical model evolves potential and density nonlinearly. The additional Fourier-projected, passive model-temperature perturbation obeys

\[
\partial_t T +\{\phi,T\}=-\kappa_T\partial_y\phi+\chi\nabla^2T-\mu T,\qquad
v_x=-\partial_y\phi,\qquad Q_T=\langle v_x T\rangle.
\]

It does NOT feed back into plasma density, potential, temperature profiles, pressure, neoclassical currents or actual heat deposition. The zonal flow evolves spontaneously in the modified HW model, and the imposed actuator is a specified normalized zonal vorticity force, NOT a wave-propagation-derived plasma source. For the model, periodic boundary conditions give the exact budget

\[
\tfrac12\partial_t\langle T^2\rangle=\kappa_TQ_T-\chi\langle|\nabla T|^2\rangle-\mu\langle T^2\rangle.
\]

`energy_budget_audit.py` evaluated the two sides from the actual numerical state after 60 unforced units at N=32. The residual is `1.11e-16`; the separate zonal-energy equation, including nonlinear transfer, viscous sink, and direct test-force power, has residual `-2.78e-17`. Those are consistency checks on the model's Fourier arithmetic, not fusion-device measurements.

## 2. Actual finite-time response with explicit convergence check

`heat_response_convergence.py` uses a common mature model state after 60 time units. It integrates a `+/- 0.003` normalized force and a zero-force copy, then calculates central response. The full run was repeated for `dt=.025,.0125,.00625` (no silent phase oscillator). At horizon `2` model units the finer-step result is:

| quantity | finite causal derivative with respect to signed forcing |
|---|---:|
| model temperature flux `Q_T` | -0.7497058845 |
| zonal first-harmonic phase, rad | +5.049065140 |
| zonal first-harmonic amplitude | +0.3629177272 |

The `dt=.025` derivative of `Q_T` was `-0.7497060122`, a difference of ~`1.28e-7`; this tests discretization at short horizon, not model or experimental uncertainty. Both amplitude and phase respond. At longer horizons, the phase gain differs strongly among initial conditions and is not a stationary susceptibility.

## 3. Nonlinear equal-power comparison: five independent specified initial states

`mhw_heat_transport.py` ran the zero-torque baseline, two saturated constant torques and three simple heuristic controls with identical nominal absorbed RF energy, one signed normalized force input bounded `|u| <=.003`, and the same measured complex zonal mode and `Q_T`. Every case was restarted from the same state within each seed and advanced with `dt=.0125`, unforced burn `60`, driven horizon `18` model units, using N=32. Mean tail results:

| action | mean model Q_T | change vs no torque |
|---|---:|---:|
| no net torque (equal ±wave powers) | 0.94250154 | — |
| fixed + torque | 0.95466184 | +1.29% |
| fixed - torque | 0.92169951 | -2.21% |
| simple phase-feedback target 0 | 0.93348408 | -0.96% |
| simple phase-feedback target π | 0.94541613 | +0.31% |

The five fixed-seed *descriptive* t intervals for paired changes all include zero. For fixed negative torque, the absolute Q difference is `-0.0208020` with descriptive 95% interval `[-0.0605356,+0.0189315]`. For phase target 0, difference is `-0.00901746` with interval `[-0.05950685,+0.04147192]`. This is NOT a confidence interval for reactor plasma or a statistically adequate turbulence ensemble. No net heat-power or confinement benefit can be inferred. Across-seed variability exceeds the mean effect; best conventional controller is not proved to be fixed negative torque.

The model's zonal-energy budget records negative nonlinear transfer on `~70.2%` of sampled baseline tail records, so the changing phase and amplitude are genuinely embedded in nonlinear dynamics rather than forced into a noisy Adler oscillator. **This is a model sign convention; the number is not a measurement of GENE's back-transfer frequency.**

## 4. Stronger same-information direct-transport comparator

A finite-horizon best-of-three oracle resolves the criticism that a simple phase controller is a weak conventional baseline. `heat_vs_phase_matched.py` gives *both objectives* the same three exact nonlinear branch rollouts `u in {-0.003,0,+0.003}`, the same sensor outputs `Q_T` and complex zonal mode, and identical nominal absorbed wave power. It then selects (i) smallest final model heat flux or (ii) smallest final angular difference from target phase zero. These are **offline calibrated action-oracle upper bounds on attainable finite-choice decisions**, not real-time controllers: the future-response model and three rollouts must be acquired and paid. Their cost is identical here.

This 3-seed test used `N=32`, unforced burn `45`, `dt=.025`, horizon `2` model units.

| seed | heat-minimal u | phase-minimal u | heat-minimizer ΔQ_T | phase-minimizer ΔQ_T |
|---:|---:|---:|---:|---:|
| 19 | -0.003 | +0.003 | -0.000432399 | +0.000419712 |
| 22 | +0.003 | +0.003 | -0.000324316 | -0.000324316 |
| 27 | -0.003 | +0.003 | -0.000358912 | +0.000343436 |

There is no new control algorithm that defeats an ordinary fully informed finite-horizon optimizer. On two states, **picking the phase-optimal action worsens model heat flux while an available equal-cost action reduces it**. The actual reductions are very small and not a transport-performance claim. This is the strongest causal reason here not to treat phase pinning as the north-star objective until a mode-to-heat map is demonstrated.

## 5. Wave reachability and a transfer that fails

For a single symmetric scalar cold O-mode `+ky/-ky` wave pair, the two absorbed local heating profiles are identical and only the odd signed momentum direction changes. This is an exact heating-null direction in the **stated model**, but not in arbitrary magnetized toroidal geometry. The strongly attenuated fifth radial harmonic demonstrates that the sign-reversal operation by itself does not make a phase-addressable actuator.

At `110GHz`, `ne=2e19/m³`, `nu=1e8/s` (phenomenological *collisional* Drude loss), `ky=100/m`, `L=0.5m`:

- Incident absorption in the slab: `0.0235833883` of launched power;
- Mode-5 normalized absorption-profile overlap: `0.00076066293`;
- Formal `(ky/omega)P_abs` mode component: `2.595529e-9 N` per `1MW` launch **only when the phenomenological absorption can legitimately be mapped to momentum; this is NOT Gallaro–Dodin's acquired collisionless resonant source**;
- A *separate illustrative inertial-flow displacement* requires `3.22TW` launch under the same cold O-mode force map. This is not a lower bound for a self-sustained soft-phase plasma mode, and it is not a reactor forecast;
- Under 3% shape asymmetry of the two waves, matching total absorbed watts leaves 2.12% relative L2 local *heating-profile* mismatch.

The exact species-conserving conditional downstream ray arithmetic and the unexecuted BORAY MATLAB source are retained. BORAY uses cold ray propagation and hot kinetic damping, which can be much more suitable for resonant plasma control, but it has not supplied a paired calibrated actual RF deposition and finite reactive dressing map for the selected target.

## 6. Numerical and scientific failures retained

A longer N32 `dt=.025` simulation diverged (overflow in nonlinear advection) and was discarded. A refined `dt=.0125` run finished the 18-unit comparison, but extrapolation to indefinite statistically stationary heat transport is unearned. Time-step convergence of a 2-unit *response* does not certify finite-grid N32 turbulence statistics. The passive scalar can grow dramatically on longer runs. Initial particle-flux-only studies in `PROOF_AND_TRANSFER.md` are historical and do not provide reactor heat transport. Controls are conditioned on a *specified normalized force*; a self-consistent plasma wave field was never coupled to the 2D model.

The stronger physical alternative is measured mode-converted RF flows (Lin et al. 2008, Phys Rev Lett 101, 235002, and Berry–Jaeger–Batchelor 1999, PRL 82, 1871), with negative-triangularity shaping and other known turbulence controls. This work has not shown that a paired heating-null RF intervention improves confinement more effectively than these approaches. The Gkeyll TCV scan provides passive zonal and heat diagnostics, not the causal actuator derivatives. Gallaro–Dodin's stored wave dressing term is a necessary separate transient input.

## Decision

**Retain a precise pilot construction and do not promote reactor performance.** The best earned opening is an *actuator-calibrated, heating-balanced causal test* of whether naturally sustained zonal coherence or its spatial position reduces actual ion/electron heat losses. The next first hard step is to acquire a nonzero, spatially selective and adequately conditioned RF momentum source from a full magnetized resonant wave solve, including time-dependent stored dressing and observed species heat. Then perturb the SAME nonlinear gyrokinetic plasma and compare direct heat-optimizing controller and phase control using the same pulses, power and diagnostics. If no useful spatial force survives, abandon RF phase steering rather than tune an unphysical oscillator model.
