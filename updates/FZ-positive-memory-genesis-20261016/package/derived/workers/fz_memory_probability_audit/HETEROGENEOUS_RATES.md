# Uniformity under bounded spatial rate variation

This is a directly derived stronger conditional theorem, not a claim about
general local-generator perturbations or historical novelty. It uses the same
LSS and HT imports, support envelope, stopped replay and decoder as `AUDIT.md`.

Fix `K>=1`. Suppose every canonical primal/dual vertex proposal rate is a fixed
number `kappa_v` satisfying

```
0<kappa_min <= kappa_v <= kappa_max <= K*kappa_min.
```

The rates may vary arbitrarily in space and between sectors. Each active
pattern at a given vertex uses that vertex's rate, preserving the single
state-independent proposal-clock representation. Allow spatially varying
independent Pauli face proposal rates with

```
max_f max(lambda_(f,X)+lambda_(f,Y),
          lambda_(f,Z)+lambda_(f,Y)) <= epsilon(K)*kappa_min.
```

Then there are fixed `b`, `epsilon(K)>0`, `A(K),c(K)>0` such that for all
sufficiently large `L=bM` and every such rate arrangement, the same fixed
component-local decoder satisfies

```
||Dec_L exp(T L_total) Enc_L-Id||_diamond
 <= min(2, A(K) L^4 (1+kappa_min*T) exp(-c(K)L)), all T>=0,
```

assuming the exact Pauli trajectory reduction. Constants are independent of
the particular arrangement, size and storage horizon.

To prove this, set `Delta=Cb/kappa_min` with `C>10 log(8)`, then fix
`R>=ceil(280 e C K)+10`. The deterministic envelope, healthy halfspaces,
coarse DNF, eroder proof and component-local decoder are unchanged.

In the predecessor certificate, `E_x` has independent law Exp(`kappa_x`).
At exponential parameter `kappa_min/2`, its moment is

```
E exp(kappa_min E_x/2)
 = kappa_x/(kappa_x-kappa_min/2) <= 2.
```

Thus the slow failure probability remains bounded by
`2b^4 exp((5 log(8)-C/2)b)`.

For a structural word using stream `v` with multiplicity `r_v`, the expected
number of ordered arrival tuples is exactly

```
Delta^m product_v(kappa_v^r_v)/m!
 <= (kappa_max Delta)^m/m!.
```

With `m=floor(Rb/2)` and `b>=4`,
`35 e kappa_max Delta/m <= 140 e C K/R < 1/2`.
The fast contribution is therefore at most `b^4 2^(-m)`. The birth contribution
is bounded by the same full-guard face count with the maximum sector face rate.

All flags still depend on independent packets within the same fixed coarse
radius. They need not be identically distributed: their marginals obey one
uniform bound. LSS requires no spatial homogeneity for this conclusion. For
a fixed prospective torus anchor, copy its deterministic local rate field
together with its ordinary independent primitive streams, and extend outside
with arbitrary rates in the same interval. The infinite field has independent
inhomogeneous streams and the same uniform good-flag estimate. Its flags are
dominated by homogeneous iid deaths, so the HT comparator is the same
translation-invariant CA as before.

Choose `p,delta_*`, then fixed `b`, then the noise tolerance in that order.
The stopped witness and historical-homology arguments are unchanged.
`N=ceil(T/Delta)+1<=2(1+kappa_min T)` completes the estimate. This shows that
strictly equal correction rates are unnecessary; a fixed lower rate and fixed
ratio bound suffice.

This does not allow `kappa_min=0`, time-dependent/adaptively correlated clocks,
non-Pauli jump components, changes to the accepted syndrome pattern, or coherent
Hamiltonian perturbations. Those modifications need different premises.
