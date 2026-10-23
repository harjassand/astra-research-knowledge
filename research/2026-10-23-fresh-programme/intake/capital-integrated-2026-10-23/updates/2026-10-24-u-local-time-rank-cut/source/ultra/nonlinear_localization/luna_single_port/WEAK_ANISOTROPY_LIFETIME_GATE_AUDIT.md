# Weak-anisotropy lifetime gate

24 October 2026. Bounded audit of
`../WEAK_ANISOTROPY_RESPONSE_AND_MODULATION.md`. No new sources, fixtures,
or device claims.

## What the lifetime statement would have to control

Fix the stated compact sector `K` with positive margins from
`Omega_lin`, `omega_c/3`, and `omega_c`. Let `H_b(Omega)` and `L_b(Omega)` be
the isotropic bound-state branch, with `inf_K H_b'(Omega)=m_K>0`. The
sideband matrix gives the frozen first-order response and the formal
coefficient `Gamma_E(Omega)>0`; it does not control a solution over
`t=O(epsilon^-2)`.

A sufficient modulation target is a phase- and frequency-modulated
decomposition

```
z(t)=z_b(theta(t),Omega(t))
     + epsilon z_1(theta(t),Omega(t)) + r(t),
theta_dot=Omega,
```

where `z_1` is the two outgoing sidebands and the neutral phase/family
directions have been projected into `theta,Omega`. The needed local estimate
is, for every fixed `S`,
`sup_{0<=t<=S epsilon^-2} ||r(t)||_loc=o(epsilon)`; `||.||_loc` must control
the oscillator quadratures and field trace that enter torque and radiation.
For example, a uniform `O(epsilon^2)` stable remainder is more than enough.
This yields an `o(epsilon^2)` pointwise torque error, since
`L_dot=epsilon Im(z^4)/4` and the error enters as
`O(epsilon ||r||_loc)`. Fast zero-mean terms also need a uniform primitive
bound; their phase frequency stays bounded away from zero on `K`.

For the emitted power, the corresponding direct requirement is

```
sup_{t<=S epsilon^-2} | integral_0^t
   [P_rad(s)-epsilon^2 Gamma_E(Omega(s))] ds | = o(1).
```

In a channel-amplitude formulation, it suffices that each outgoing
amplitude be `epsilon a_j(Omega)+rho_j(t)` with
`integral_0^{S epsilon^-2} (epsilon |rho_j|+|rho_j|^2)dt=o(1)`, together
with the same control of any other radiative channels. After separating the
localized part, these estimates must give a modulation residual

```
H_b'(Omega) Omega_dot = -epsilon^2 Gamma_E(Omega)+R_epsilon(t),
sup_{t<=S epsilon^-2} |integral_0^t R_epsilon(s)ds| = o(1).
```

The last condition, rather than pointwise averaging alone, is what survives
on slow time `tau=epsilon^2 t`. It implies the candidate slow ODE uniformly
on fixed `tau` intervals by integration and Gronwall, while the solution
stays in `K`. A uniform `R_epsilon=O(epsilon^3)` is sufficient; an
`O(epsilon^2)` remainder is not sufficient without extra cancellation.

## What an integrable kernel does and does not give

After neutral subtraction, suppose the local stable response has a causal
kernel `K_Omega` with
`sup_{Omega in K} ||K_Omega||_L1 <= C_K`. Young's inequality then controls
local response to a uniformly `O(epsilon^2)` residual source by
`O(epsilon^2)`. This closes the stable-mode part of a bootstrap only if the
nonlinear residual source is already bounded by
`C(epsilon^2+epsilon ||r||_loc+||r||_loc^2)`, the neutral projections are
handled separately, and the homogeneous preparation term is controlled.
None of those source and projection bounds follows from the frozen FGR
calculation.

Moreover, an absolute tail `|K(t)|~t^-3/2` is integrable but has no finite
absolute first moment: `integral t|K(t)|dt` diverges. Thus `K in L1` alone
does not justify replacing a retarded amplitude `B(Omega(t-s))` by its
instantaneous value along a path with `Omega_dot=O(epsilon^2)`. A valid slow
modulation estimate needs a direct bound on that difference, or an
oscillatory first-moment/resolvent-derivative estimate using the fixed
frequency margins in `K`. The exact Bessel memory kernel before spectral
projection is even more delicate; its pointwise tail is oscillatory
`t^-1/2`, not absolutely integrable. The claimed projected `t^-3/2` kernel
must therefore be proved with uniform constants and the neutral modes
removed, not substituted for the raw retarded kernel by assertion.

## Empty-field preparation scale

The finite ramp starts from the empty field and has an exact mismatch
coefficient calculation. At fixed target, its rotating-frame excess obeys
`D_T<=C_F R_T^2`, and the physical field-error norm obeys
`Eerr(T)<=C_E R_T^2`. A clean sufficient target for treating the preparation
error as smaller than the `O(epsilon)` sideband correction is

```
D_T=o(epsilon^2), hence sqrt(D_T)=o(epsilon).
```

By `D_T<=C_F R_T^2`, a sufficient way to ensure this is `R_T=o(epsilon)`.
For the supplied fixed smooth ramp,
`R_T<=||chi''||_1/(T Delta)`, so one sufficient choice is
`epsilon T Delta -> infinity`. Higher fixed-order endpoint-flat estimates
can reduce this ramp-time requirement. A fixed `T` leaves an
epsilon-independent mismatch and cannot be silently inserted into the
epsilon-to-zero lifetime asymptotic. A fixed-duration smooth shutdown
preserves this scale under the earlier isotropic force-port estimate.

This norm condition is sufficient for a crude local-error bootstrap, not a
substitute for the preparation's causal history or local-response estimate.
The actual finite ramp has no incoming field and its coefficients are known;
use those coefficients to control the homogeneous local transient. An
arbitrary energy-small state may contain a remote incoming packet, so the
same energy norm alone is not a no-incoming or local-decay estimate. If the
fourfold perturbation is active during the ramp, the exact residual force
must include its `epsilon conjugate(z)^3/4` term (and the `gamma_bar` shift);
otherwise use an explicit switch-on and count its `O(epsilon)` work and
phase-dependent initial correction. The isotropic shutdown bound should not
be reused unchanged for the perturbed force law.

## Gate

The finite-state preparation can meet an `o(epsilon)` energy-space error at
fixed sub-cutoff target, and the formal FGR sidebands have positive flux.
What remains unproved is the uniform stable-response/nonlinear remainder,
the projected dispersive estimate for the actual prepared history, and the
integrated modulation/flux residual on `O(epsilon^-2)` time. Therefore the
sideband coefficient plus an integrable point kernel is not yet a uniform
lifetime theorem. The conditions above are a sufficient bootstrap target,
not a claim that this model has passed it.
