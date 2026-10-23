# Check of finite-rate retention and one-field dilation claims

24 October 2026. Bounded read-only audit of Sections 5 and 7 of
`../LOCAL_NETWORK_AND_FINITE_SCALE_ENERGY.md`.

## Finite-rate retention after a negative sublevel crossing

Under the fixed-parameter periodic/mean-zero contract, the claim is exact.
At each time the relaxed mechanical value is a minimization over admissible
periodic `u,v` at the current `phi`, so

```text
F_eff(phi(t)) <= F_full(phi(t),u(t),v(t)).
```

If the stated finite-rate gradient flow has fixed `a,K` and reaches
`F_full(t0)/L <= -q < 0`, its dissipation identity gives
`F_full(t)/L <= -q` for every later deterministic time. Hence
`F_eff(phi(t))/L <= -q` at every such time, and the same Section 5 bound
`m_B(t) >= [mu-sqrt(mu^2-4bq)]/b` follows. This does not require mechanical
relaxation or convergence. It does require the same admissible constraints,
fixed model parameters, and the stated energy-dissipating flow; parameter
work, thermal noise, or a change in constraints would break this inference.

## One-field dilation at fixed means

For a periodic cell of length `L0`, write `u(x)=e_bar x+u_per(x)` if the
prescribed mean strain `e_bar` is nonzero. The proposed scaling

```text
phi_ell(x)=phi(x/ell),
u_ell(x)=ell u(x/ell)
```

has `u_ell'(x)=u'(x/ell)`, so it preserves the strain field's distribution
and its mean; `phi_ell` preserves the composition distribution and mean.
It is periodic on the larger cell `ell L0` (and a displacement gauge can be
fixed by subtracting a constant). By change of variables, the density of
`f(phi)+W(u_x,phi)` is unchanged for any local nonlinear `W`, while

```text
mean(kappa |(phi_ell)_x|^2/2)
  = ell^(-2) mean(kappa |phi_x|^2/2).
```

Thus any smooth nonconstant finite-period pattern with positive capillarity
is strictly beaten in energy density by its dilated copy in a sufficiently
large commensurate specimen. This is a thermodynamic comparison across
sample sizes; it is not a same-fixed-length competitor. The argument fails
when the functional adds another length-bearing term, e.g. a relative-
displacement penalty, substrate pinning, higher gradients, or nonlocality.
It does not say what pattern a finite system or a kinetic trajectory selects.
