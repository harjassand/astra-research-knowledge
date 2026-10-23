# Negative bulk energy forces finite-band spectral weight

24 October 2026. Bounded variational audit of the stated periodic mean-zero
phase model. This gives a necessary spectral condition for negative bulk
energy, not a wavelength-selection or dynamics result.

## Mechanical elimination and the negative band

On a periodic cell of length `L`, write Fourier coefficients with
`phi(x)=sum_k phi_hat(k) exp(ikx)` and normalized spatial average. The mean
mode is absent by `phi_hat(0)=0`. For a nonzero mode put `x=ik u_hat`. Minimizing
the `v` terms first reduces the mechanical energy of that mode to

```text
1/2 C |x-alpha phi_hat|^2
 +1/2 [D K/(K+D k^2)] |x|^2.
```

Minimizing over `x` gives exactly

```text
1/2 [E0/(1+xi^2 k^2)] |phi_hat|^2,
E0 = alpha^2 C D/(C+D),
xi^2 = C D/[K(C+D)].
```

Thus, after minimizing over `u,v`,

```text
F_eff/L = 1/2 sum_{k!=0} lambda(k)|phi_hat(k)|^2
          + b/4 <phi^4>,
lambda(k) = a + kappa k^2 + E0/(1+xi^2 k^2).
```

Since `lambda(0)=a+E0>0`, `lambda(k)->+infinity` at large `|k|`, and a
negative value is assumed, the open set `B={k:lambda(k)<0}` is a bounded band
separated from zero. More explicitly, with `y=k^2`, its endpoints are the
positive roots of

```text
kappa xi^2 y^2 + (kappa+a xi^2)y + (a+E0)=0.
```

There is one such interval in `y` because this quadratic is positive at zero
and infinity and negative somewhere. This identifies a finite band, not a
single selected wave number.

For a cosine `phi=A cos(k_* x)` with `lambda(k_*)=-nu<0`, the density is
`lambda(k_*) A^2/4 + 3 b A^4/32`. Its minimizing amplitude is
`A^2=4 nu/(3b)` and its energy density is `-nu^2/(6b)`.

## Explicit lower bound on band power

Let

```text
S = <phi^2>,
m = sum_{k in B} |phi_hat(k)|^2,
mu = -min_{k in R} lambda(k) > 0.
```

All quadratic modes outside `B` are nonnegative, while every mode in `B` has
`lambda(k)>=-mu`. Parseval and Jensen therefore give the exact inequalities

```text
F_eff/L >= -mu m/2 + b <phi^4>/4
          >= -mu m/2 + b S^2/4
          >= -mu m/2 + b m^2/4.
```

Consequently, if a state has bulk energy density `F_eff/L <= -q` for some
fixed `q>0`, then necessarily `q<=mu^2/(4b)` and

```text
m >= [mu - sqrt(mu^2-4bq)]/b > 0.
```

The same argument with `m<=S` gives
`S <= [mu+sqrt(mu^2-4bq)]/b`; hence even the fraction of total squared
Fourier amplitude in the negative band is bounded below:

```text
m/S >= [mu-sqrt(mu^2-4bq)]/[mu+sqrt(mu^2-4bq)] > 0.
```

For any periodic trial wave number `k_*` with `lambda(k_*)=-nu<0`, a global
minimizer on a cell admitting that wave has density no greater than
`-q_*=-nu^2/(6b)`. It must then have

```text
m >= [mu-sqrt(mu^2-(2/3)nu^2)]/b.
```

The bound is deliberately coarse but survives arbitrary mode mixing and
spatial concentration: it uses only the negative spectral minimum, positivity
outside the band, and quartic coercivity. If a sequence's negative density
shrinks to zero, the lower bound also shrinks to zero; there is no uniform
coarsening obstruction from a merely negative `o(1)` density.

## Scope and loopholes

Under a bounded-amplitude, slowly varying macroscopic-domain ansatz, the
Fourier kernel tends to `E0` at `k=0`, so the bulk local density becomes
`(a+E0)phi^2/2+b phi^4/4>=0`; interfaces add the nonnegative gradient term.
The spectral inequality is stronger for periodic states because it does not
assume that ansatz. At fixed negative bulk density, a state cannot move all
its squared spectral weight to wave numbers tending to zero. Quartic
coercivity also prevents high-amplitude spikes from evading the bound.

This does not rule out coexistence: macroscopic domains may contain a
nonvanishing fraction of finite-band structure, and the bound does not fix
its morphology or prove a unique period. The model is periodic, so it has no
physical boundary layer. For open finite samples, a subextensive boundary
term cannot overturn a fixed negative *bulk density*, but it can decide a
finite-size total-energy comparison or dominate when the density gap tends
to zero. Nothing here proves all-time convergence, thermal long-range order,
or a material-scale microphase.
