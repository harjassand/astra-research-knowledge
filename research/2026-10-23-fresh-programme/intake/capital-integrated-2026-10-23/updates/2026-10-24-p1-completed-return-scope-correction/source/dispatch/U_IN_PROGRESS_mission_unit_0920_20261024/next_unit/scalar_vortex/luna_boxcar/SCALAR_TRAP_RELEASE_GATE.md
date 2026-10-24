# Scalar-trap release and finite-aperture gate

24 October 2026. Bounded compatibility check for the specified quasi-2D defocusing Gross–Pitaevskii construction; no apparatus or material parameter is acquired.

## The prepared state and its scalar potential

Write `r^2=x^2+y^2`, `P(r)=r^2+a+bx`, `a>b^2/4`, and

```text
psi_I = c P exp(-r^2/2),  rho_I=|psi_I|^2,
V_pre^g = r^2/2 + [2(a+1)+b x]/P - g rho_I.
```

The denominator is uniformly positive because `P=(x+b/2)^2+y^2+(a-b^2/4)`. Thus the rational term is smooth and bounded everywhere. It is not compactly supported: for generic `b != 0` it has an angular `O(1/r)` tail, and the Gaussian counterterm decays rapidly. In the GP stationary equation the nonlinear term `g rho_I` cancels the trap counterterm at `psi_I`; the remaining one-body operator is

```text
H_0 = -Delta/2 + r^2/2 + [2(a+1)+b x]/P,
H_0 psi_I = 3 psi_I.
```

Since `P>0`, `psi_I` is strictly positive. Harmonic confinement plus a bounded smooth real perturbation gives compact resolvent; the positive eigenfunction is the simple isolated lowest state of `H_0`. This is the exact mathematical preparation state in the stated construction, not evidence that a physical gas can be prepared in it with zero temperature or zero error.

## A finite, norm-conserving trap release

Define the bounded real perturbation

```text
W_g(r) = [2(a+1)+b x]/P - g rho_I(r)
```

and ramp it with a real `lambda(t) in C^infinity([0,T])`, flat at both endpoints, from `lambda(0)=1` to `lambda(T)=0`:

```text
i partial_t psi = [-Delta/2 + r^2/2 + lambda(t) W_g(r) + g |psi|^2] psi,
||psi(0)||_2=1.
```

The initial state is stationary up to its phase at `lambda=1`; at `lambda=0` the trap is radial harmonic. A real scalar potential and real `g` preserve norm. For defocusing (`g>0`) 2D cubic GP with this confining harmonic potential and bounded smooth perturbation, finite-time evolution is well posed in the trapped finite-energy space (including `H^1` and finite second moment). On any fixed interval `[0,T+T_obs]`, continuous dependence bounds the effect of a small initial preparation error and a small potential error, provided the compared trajectories have bounded finite-energy norms. A smooth ramp avoids an impulsive control, but it is not a free or adiabatic ground-state transfer: it produces a generally nonstationary state and the trap work is

```text
W_trap = integral_0^T lambda_dot(t) integral W_g(r)|psi(r,t)|^2 d^2r dt.
```

Taking a short but finite ramp can approximate an abrupt release over a finite observation horizon when `T ||W_g||_infinity` is small; whether an apparatus can deliver the required profile and slew is unmeasured. No complex forcing, spatially resolved phase control, or phase oracle is used in this construction.

The rational tail can be truncated smoothly at a large control radius `R`. Its omitted potential has uniform size `O(|b|/R + R^-2)` (plus a Gaussian tail), so this is a bounded-potential perturbation that tends to zero as `R` grows. Finite-time continuous dependence then justifies convergence of the controlled GP trajectory to the ideal-profile trajectory on a fixed finite horizon, assuming the initial state is also close. For the linear effective operator, its isolated eigenvalue supports perturbative control of a prepared eigenstate under a small potential error; persistence of a nonlinear GP ground-state branch additionally needs a nondegeneracy/stability condition. This is a mathematical truncation argument; it does not establish optical or magnetic field resolution, calibration of the `g rho_I` counterterm, or achievable `R` and ramp time.

## Finite aperture and scope

The initial norm outside radius `R` is the explicit Gaussian tail `c^2 integral_(r>R) P^2 exp(-r^2) d^2r`. After finite evolution, if the second moment remains finite, an aperture loses at most `R^-2 integral r^2 |psi(r,t)|^2 d^2r` of the norm by the elementary tail bound. This can justify large finite apertures for mass or norm observables on a bounded time window. It is not a finite-speed argument: if the aperture truncates the evolving GP domain rather than just the readout, its boundary error needs a separate estimate. The tail bound does not by itself certify a vortex count or phase winding: zeros and phase need a resolved complex-field/density-and-phase readout and an adequate boundary margin.

Physical use still assumes a quasi-2D dilute regime: axial excitation is suppressed relative to the axial level spacing, the effective 2D coupling `g` is calibrated, and mean-field GP remains valid over the ramp and observation time. The construction needs an accurately known `g`, `a`, `b`, normalization, scalar-potential profile, and initial state. Finite temperature, quantum depletion, preparation defects, readout backaction, and trap lifetime are not modeled. Positive isolation and finite-time continuity protect only a specified ideal finite-horizon evolution; they do not supply laboratory preparation, field resolution, long-time stability, or a closed reset cycle.

## Compact-support preparation path from the harmonic ground state

There is a distinct finite-control route that does not start by assuming the target profile is already prepared. Write `H_ho=-Delta/2+r^2/2` for the bare harmonic operator (the earlier `H_0` denoted `H_ho` plus the target rational term) and, for `s in [0,1]`, define

```text
W_s = [2+2 s a+s b x]/[(1-s)+s P],
H_(s,R) = H_ho+chi_R(r)[W_s-2].
```

Here `chi_R` is a smooth cutoff equal to one on a radius-`R` disk and zero outside a larger finite disk. The denominator is positive uniformly in `s`, since `P>=a-b^2/4>0`. At `s=0`, `W_0=2`, so `H_(0,R)=H_ho` has exactly the ordinary Gaussian ground state with energy `1`. At `s=1`, `W_1=[2(a+1)+bx]/P`, and the uncut operator `H_ho+W_1-2` has `psi_I` as its positive eigenfunction at energy `1`, since it is the earlier target `H_0` shifted down by `2`. For fixed `R`, all varying terms and their `s` derivatives are bounded, smooth, and compactly supported. This energy-origin normalization subtracts the same constant `2` from the entire earlier path; states, gaps, and spatial control footprint are unchanged.

For the uncut path `H_ho+W_s-2`, harmonic confinement and bounded real `W_s` give a simple isolated ground state for each `s`; on the compact path the gap has a positive minimum. For finite `R`, the same holds. As `R` grows, the cutoff operator converges in norm resolvent uniformly along this path by harmonic confinement: low-energy resolvent states have uniformly small tails outside the cutoff, even though the potential difference there is not small in the global sup norm. Thus its final ground state approaches `psi_I` in the corresponding graph norms. This is the correct convergence argument for this compact-support route; it is distinct from the earlier direct truncation of a decaying perturbation, which used a small sup-norm tail.

For `g=0`, an ordinary finite-time linear adiabatic preparation with a smooth flat-end schedule `s(t)` can follow the isolated ground state. Choose finite `R` first, then a sufficiently large but finite preparation time `T` for the chosen gap and control derivatives. In the uncut target limit, ideal adiabatic preparation begins and ends at ground energy `1`, so its work is zero. At finite `R`, if the final ground energy is `E_(1,R)`, ideal adiabatic preparation work is `E_(1,R)-1`; it tends to zero as `R` grows. At finite `T`, use the actual work integral `integral dt integral (partial_t V)|psi|^2 d^2r`. Let `phi_R` be the normalized final finite-`R` ground state. A sudden release to `H_ho` costs `<phi_R,H_ho phi_R>-E_(1,R)`. The sum of ideal adiabatic preparation and sudden release work is `<phi_R,H_ho phi_R>-1`, which tends to `E_post,0-1>0`, where `E_post,0=<psi_I,H_ho psi_I>`; strict positivity follows because `psi_I` is not the harmonic Gaussian ground state. By finite-time continuity, sufficiently small but nonzero `tau` preserves positive total work in the `g=0` model when the approximation errors are smaller than this margin. All varying scalar controls have finite support and finite time derivatives, and the potential controls return to their initial setting while the wavefunction generally does not. Do not combine this stage ledger with the earlier direct `V_pre^g` switch, whose energy origin and preparation are different.

For `g>0`, no nonlinear adiabatic theorem, `g` ramp, or state-dependent `-g rho_I` trap counterterm is needed for the bounded claim. Start from the ordinary harmonic GP ground state `Phi_g`, which approaches the Gaussian as fixed `g` tends to zero, and run the same finite `R,T,tau` scalar protocol while keeping `g` fixed. Finite-horizon GP continuous dependence over `T+tau+pi/2` then gives closeness to the `g=0` finite-protocol field for sufficiently small fixed `g`, assuming the initial state is correspondingly close and the finite-energy bounds hold. The scalar-control work integral is continuous under this finite-horizon limit, so a positive `g=0` work margin remains positive for sufficiently small fixed `g`; this statement excludes gas preparation and hardware costs and does not constitute a closed state-return cycle. This is an existence/continuity statement, not an acquired quasi-2D operating window: it does not show that a chosen gas permits sufficiently small `g`, that the scalar controls are physically resolved, or that the finite preparation time fits the trap lifetime. It also does not claim a target-ground-state oracle, zero-temperature preparation, vortex readout resolution, or a field return.

The same finite-aperture tail bound above applies to mass observables during this finite protocol when the second moment is controlled. It does not license replacing the full-plane GP evolution by a finite-domain simulation without a separate boundary-error estimate.
