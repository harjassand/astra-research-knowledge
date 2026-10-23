# Finite-rate and material-interface check for the passive double chain

24 October 2026. This is a bounded algebra and compatibility audit of the selected local model. No numerical fixture, material, or literature claim is supplied; it is not an assembly or performance result.

## Finite mechanical rates preserve the unstable sign

For periodic fields with fixed conserved mean `integral phi=0`, take

```text
F = integral [a phi^2/2 + b phi^4/4 + kappa phi_x^2/2
              + C(u_x-alpha phi)^2/2 + D v_x^2/2 + K(u-v)^2/2] dx,
```

with `b,kappa,C,D,K>0`. The dynamics are conserved diffusion for composition and finite-rate overdamped mechanics:

```text
phi_dot = M partial_xx mu,   mu = delta F/delta phi,
Gamma_u u_dot = -delta F/delta u,
Gamma_v v_dot = -delta F/delta v,
```

where `M,Gamma_u,Gamma_v>0`. Periodic boundary conditions give

```text
dF/dt = -M integral |mu_x|^2 dx
        -Gamma_u integral |u_dot|^2 dx
        -Gamma_v integral |v_dot|^2 dx <= 0.
```

If `a` or `K` is externally varied while the model remains isothermal, the chain rule instead gives

```text
dF/dt = W_param - M integral |mu_x|^2 dx
                 - Gamma_u integral |u_dot|^2 dx
                 - Gamma_v integral |v_dot|^2 dx,
W_param = (a_dot/2) integral phi^2 dx
         + (K_dot/2) integral (u-v)^2 dx.
```

Thus a closed isothermal coefficient-control cycle has net parameter work equal to the dissipated free energy if the state and coefficients return to their initial values and there are no other fluxes. This is not a free quench. If `a` is changed by varying temperature, the full temperature dependence of the Helmholtz free energy adds its entropy/heat bookkeeping; the displayed `a_dot` term is only one chain-rule contribution, not an energy source exemption.

For a nonzero Fourier mode `k`, the quadratic Hessian in `(phi,u,v)` has the mechanical block

```text
H_m(k) = [[C k^2+K, -K], [-K, D k^2+K]],
det H_m = k^2 [C D k^2 + K(C+D)] > 0,
```

and `H_phi,phi=a+C alpha^2+kappa k^2`, with `|H_phi,u|=C alpha |k|`. Eliminating the positive mechanical block gives

```text
lambda(k) = a+C alpha^2+kappa k^2
            - C^2 alpha^2 (D k^2+K)/(C D k^2+K(C+D)).
```

If this Schur-reduced `lambda(k)<0` for an allowed nonzero mode, the full Hessian `H(k)` has a negative direction: choose `(u,v)` to minimize its quadratic form at fixed nonzero `phi`. The linear dynamics are
`z_dot=-M_k H(k)z`, with `M_k=diag(M k^2,Gamma_u^(-1),Gamma_v^(-1))` positive definite. This matrix is similar to the Hermitian matrix

```text
-M_k^(1/2) H(k) M_k^(1/2).
```

Congruence preserves inertia, so a negative direction of `H` gives a strictly positive real eigenvalue of the finite-rate dynamics. Thus finite positive mechanical drag cannot remove the growing mode. It changes its rate, potentially making growth very slow; the quasistatic scalar rate `-M k^2 lambda(k)` is not the finite-rate eigenvalue in general.

The `k=0` composition mode is excluded by conservation/fixed mean, and the common shift `u=v=constant` is an exact rigid-translation zero mode, not an energy penalty. Fix the displacement gauge or quotient this mode; do not pin the ladder to an unpriced frame. The Schur formula is for `k!=0`, where `H_m` is positive definite.

## What the physical construction would have to contain

The two displacement fields require two distinguishable load-bearing networks with relative motion. A single homogeneous gel does not supply independent `u` and `v` coordinates by definition. In the exact scalar model, `K(u-v)^2/2` is a passive harmonic shear coupling. A compatible small-strain interpretation is two longitudinal bars/networks bonded through a finite shear-compliant layer of width `w` and thickness `h`: for relative displacement `u-v`, layer shear strain is approximately `(u-v)/h`, giving energy per length `G_layer w (u-v)^2/(2h)` and hence `K=G_layer w/h` at leading shear-lag order. This construction counts the second network and the entire interlayer/crosslink material. An unstressed vertical pin-ended central-force rung between longitudinal sliders does not supply this harmonic term: its length change is quadratic in the longitudinal displacement difference, so its axial energy starts at fourth order. The finite layer also has axial, bending, interface, and frame responses omitted from the scalar shear-lag model; those contributions are not calibrated or silently set to zero.

The `C(u_x-alpha phi)^2/2` term assumes a chemoelastic eigenstrain: local composition changes the preferred upper-network bond length by `alpha phi`. `alpha` is a material constitutive coefficient, not an actuated or freely reprogrammable strain. `D v_x^2/2` is the lower-network elasticity. Their values, sign, linear range, relaxation spectrum, and spatial uniformity are unacquired.

The field `phi` must be a conserved composition difference with a controlled mean. `a` is a thermodynamic curvature that would need to be changed by a temperature/composition quench; `b` stabilizes the local mixture and `kappa` prices interfaces. A real finite sample would need a sealed composition inventory, fixed-length boundary condition or a measured clamp, and a reset route that restores the initial homogeneous state and mean strain. Charge the heat removed/added in the quench and reset, clamp/actuator work, mixing or chemical-potential work, and any hysteresis. A one-way quench and spontaneous pattern growth is not a closed operating cycle or a net-work device.

Thermal fluctuations are not optional near a spinodal: conserved composition noise and mechanical Brownian forcing can seed growth, broaden the onset, or dominate the deterministic unstable eigenmode. A continuum prediction is meaningful only for unstable wavelengths above the network/monomer scale and below the finite sample size, with independently measured `a,b,kappa,C,D,K,alpha` and drags. No material or actual two-network gel with this parameter combination has been identified here.

The direct observables are the composition structure factor `S_phi(k,t)=<|phi_hat_k(t)|^2>` and the cross-correlated relative displacement `r=u-v` (or its mode-resolved spectrum). A strain-only readout cannot identify the predicted composition mode. Composition contrast, displacement calibration, temperature and length control, and noise levels would all need matched calibration. No readout modality is acquired by this model note.

This establishes a linear sign result for a specified passive gradient flow and lists its material interface requirements. It does not establish that a realizable gel has `lambda(k)<0`, that the predicted mode beats thermal/finite-size effects, that the nonlinear pattern is selected or repeatable, or that the quench-reset cycle has any practical advantage.
