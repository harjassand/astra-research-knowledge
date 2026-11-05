# Exact entropy control, nonuniform signal limits and a scoped stationary extension

[Return guide](README.md) · [Complete native proof](P1_ORDINARY_CAPACITY_20261106_RETURN.txt) · [Costs and unresolved capacity](reference-costs-and-open-capacity.md)

The weak-label effects are `2^-n product_i(I+y_i r A_i)`, and conditional reference states are formed as `sqrt(tau) F_y sqrt(tau)`. They are collectively normalized positive states. Every nonempty classical Fourier moment vanishes, so the labels are exactly uniform and independent; this does not remove their quantum-reference correlation.

## An exact bounded correction, rather than numerical extrapolation

All B-side conditional states share the spectrum of

```
omega_n,s(r) = 2^-n [tensor_i(I+r Z_i)
                    + s (1-r^2)^(n/2) X^tensor n].
```

For its diagonal part `d_n(r)=tensor_i(I+r Z_i)/2`, define `K_n=D_bits(omega_n,s(r)||d_n(r))`. The exact identity is

```
C_B(n,r) = n J(r)-J(s)+K_n(s,r)
0 <= K_n(s,r) <= J(s) < 1.
```

A measure-X/prepare-qubit channel maps the parity-biased canonical state to `omega` and the uniform state to `d`. Relative-entropy data processing bounds the correction by `J(s)`. The negative finite-signal entropy density therefore has an explicit sub-one-bit correction; it is not inferred from a plotted trend.

The opposite normalized limit values are `a^2-k(s)>0` when the small-signal limit is taken first, and `a^2-1=-0.36` when the large-block limit is taken first. At illustrative `r=0.2`, the source gives positive difference around `0.0020713` bits for `n=1` and negative difference around `-2.23362` bits for `n=256`. Those evaluations illustrate the analytic statement rather than proving it.

## Stationarity and a retained phase record

The original `tau_B,n` family is not the marginal family of one infinite stationary chain: tracing out a qubit erases its global parity term. That limitation is retained.

A separate extension fixes a finite block length `L`, places independent copies along the chain and randomizes their phase. Retaining the phase costs `ceil(log2 L)` storage bits. Conditional on that record, full blocks retain the positive zero-signal Fisher density, with only two boundary blocks charged. The finite-signal density becomes `J(ar)-C_B(L,r)/L`, negative whenever `L>J(s)/(J(r)-J(ar))`.

For the phase-averaged canonical state, the functional differs by at most `log2 L`, so the asymptotic sign remains. This establishes that stationarity with unrestricted finite memory is not itself enough. It does not supply uniform mixing in `L`, preserve every single-block regularity property or realize the particular complementary-channel encoder. The phase and reference records are not free hidden assistance.
