# One-mode induction estimator: algebra and physical scope check

**Verdict: the paired-helicity estimator, power split, and reciprocal-port identity are algebraically correct for the literal single-loop induction model.** The estimator is conditional on common rotor parameters and a de-embedded complex stator background; it is not a general materials-state inference. Reversing helicity changes torque, so the two measurements must see effectively the same rotor speed (or be made with a speed-stabilized rotor). This is an electrical/rotordynamic toy model, not evidence about distributed melting, fragmentation, or novelty.

## Paired-helicity inversion

Use RMS phasors with time factor `exp(+iωt)` and spatial field phase `exp(−imθ)`. In rotor coordinates `θ'=θ−Ωt`, the phase is `exp(−imθ') exp(i(ω−mΩ)t)`, so the signed slip is `s_m=ω−mΩ`. The assumption `|Ω|<ω` makes both slips positive. With the task's rotor equation and stator reflected-load convention,

`j_m = −i s_m M I_m/(R+i s_m L)`,

`W_m = iωM j_m/I_m = ωs_m M²/(R+i s_m L)`.

The signs are consistent: the `−i` in the induced-current response cancels the `+i` in the stator reflected voltage, and

`Re W_m = ωs_m M²R/(R²+s_m²L²) > 0`.

Taking the reciprocal gives the key cancellation:

`1/W_m = R/(ωM²s_m) + i L/(ωM²)`,

so with `a_m=Re(1/W_m)` and common `R>0`, `L>0`, `M≠0`,

`a_+ = κ/(ω−Ω)`, `a_- = κ/(ω+Ω)`, `κ=R/(ωM²)>0`,

and therefore

`ω (a_+−a_-)/(a_++a_-) = Ω`.

The sign agrees with the slip convention: positive rotor speed lowers the `+`-helicity slip, raising `a_+`. One helicity alone only supplies a real combination proportional to `R/(M²s_m)` and an imaginary combination `L/M²`; without further known parameters, `R`, `L`, `M`, and `Ω` are not separately identified. The paired formula requires the same `R,L,M` for both readings. If rotor temperature changes `R` between sequential readings, or the two couplings differ, the cancellation fails. It is also poorly conditioned near a synchronous endpoint: as one slip tends to zero, its `W_m` tends to zero and forming `1/W_m` magnifies absolute measurement error.

The `W_m` in this equation must be the rotor-reflected load after subtracting the calibrated common background. If the raw measurement is `Zmeas,m=Zc+Wm`, one must form `Wm=Zmeas,m−Zc` *before* taking reciprocals. A common unknown additive `Zc` does not disappear inside `Re(1/Zmeas,m)`; calibration drift or a helicity-dependent background biases the inversion. The circular comparison also presupposes that the rotor one-loop contribution is diagonal in the two helical channels, as assumed in this model.

## Power, heat, and torque ledger

For RMS current, stator input real power in this reflected branch is

`P_m=|I_m|² Re W_m = ωs_m M²R|I_m|²/(R²+s_m²L²)`.

Rotor Joule heat computed directly from the circuit is

`Q_m=R|j_m|² = Rs_m²M²|I_m|²/(R²+s_m²L²) = (s_m/ω)P_m`.

The remainder is mechanical conversion:

`Pmech,m=P_m−Q_m=(mΩ/ω)P_m = Ω τ_m`,

which fixes the signed torque as `τ_m=mP_m/ω`. Thus the stated signs satisfy conservation for each mode. At `Ω=0`, torque may be nonzero while mechanical power is zero, as for a rotor held at standstill. If both modes are present with *equal real reflected powers* `P_+=P_-=P0`, their torques cancel, but their total Joule heating is positive:

`τtotal=0`, `Qtotal=[(1−Ω/ω)+(1+Ω/ω)]P0=2P0`.

Equal powers are a condition on `|I_m|²ReW_m`, not generally on equal current magnitudes. The electrical source supplies the full `2P0`; there is no free work or thermodynamic advantage here.

`P_m` is only the reflected rotor-branch input: stator copper/core losses in the common background are excluded. Adding the `+` and `−` branch ledgers for a simultaneous field assumes the two helical channels remain decoupled and average cross terms vanish. For a clamped rotor, `Ωτtotal` is work exchanged with the speed controller/load even if `Ω` is held fixed; for a free rotor, its kinetic-energy change and other mechanical losses must be included.

## Reciprocal frozen background and reversal backaction

For any complex 2×2 αβ port matrix `Z` and `e±=(1,±i)/√2`, direct multiplication yields

`e±† Z e± = (Z11+Z22)/2 ± i(Z12−Z21)/2`,

so

`e+†Ze+ − e-†Ze- = i(Z12−Z21)`.

Every stationary reciprocal linear background has `Zᵀ=Z` (not necessarily real or isotropic), and therefore has zero circular self-load difference. Anisotropic conductivity or shape can change the common term and the symmetric off-diagonal entries without creating this handed difference. A nonzero difference indicates an antisymmetric/nonreciprocal contribution under these assumptions; it is not uniquely diagnostic of rotor speed if electronics, active elements, or other moving media contribute such a term.

The rotor itself is not a passive frozen background: `τ_+=+P_+/ω` and `τ_-=−P_-/ω`. Sequential reversal therefore pushes it in opposite directions and can change `Ω` between readings. The estimator applies to paired measurements at one effectively common `Ω`; use a speed clamp/independent speed readout or bound the change during a short, low-energy probe. Simultaneous equal-power helicities cancel ideal mean torque but still heat the rotor. In a freely accelerating rotor, include `d(JΩ²/2)/dt`, bearing/load work, and temperature-driven `R` changes in the time-dependent ledger; the steady phasor formulas do not account for those transients.

## Scope boundary

This model estimates one kinematic parameter, `Ω`, from a reciprocal-subtracted electrical port under known carrier and helicity with a single rotor loop and shared `R,L,M`. It contains no spatially resolved conductivity, temperature, phase, crack, melt-front, or fragment variables; no mapping from `W_m` to a distributed metallurgical state follows. A real induction machine requires winding harmonics, multiple rotor paths, geometry, skin effect, frequency-dependent material properties, losses, and calibrated terminal electronics. The calculation establishes a consistent conditional circuit identity, not a measured capability or a materials/industrial claim.
