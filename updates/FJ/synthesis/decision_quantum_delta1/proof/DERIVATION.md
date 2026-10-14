# Derivation: Gaussian output sampling

Let `V` be a centered random vector in `R^d`, `Z ~ N(0,sigma^2 I_d)` independent of `V`, and `P=Law(m+V+Z)`, `Q=N(m,sigma^2 I_d)`. All claims below are ideal-real probability statements.

## Gaussian-mixture second moment

For fixed `v`, the density of `N(m+v,sigma^2 I)` relative to `Q` is

```text
ell_v(x) = exp(((x-m)^T v)/sigma^2 - ||v||^2/(2 sigma^2)).
```

If `Y~N(0,sigma^2 I)`, then

```text
E_Q[ell_v(X) ell_v'(X)]
 = exp(-(||v||^2+||v'||^2)/(2 sigma^2))
   E exp(Y^T(v+v')/sigma^2)
 = exp(v^T v'/sigma^2).
```

The mixture likelihood ratio is `E_V ell_V`. Fubini and an independent copy `V'` therefore give

```text
1 + chi^2(P||Q) = E_{V,V'} exp(V^T V'/sigma^2).
```

For independent scalar coordinates `V_i`, the dot-product exponential factors:

```text
chi^2(P||Q) = product_i E exp(V_i V_i'/sigma^2) - 1.
```

The copy `V'` is independent of `V`; coordinate independence is needed only for the last product factorization, not for the vector identity.

For any real `u`, Taylor's integral remainder gives

```text
exp(u) = 1 + u + u^2 integral_0^1 (1-t) exp(tu) dt
       <= 1 + u + (1/2) exp(|u|) u^2.
```

If `E V_i=0`, `|V_i|<=b_i`, and `v_i=Var(V_i)`, put `U_i=V_iV_i'/sigma^2`. Then

```text
E U_i=0, |U_i|<=b_i^2/sigma^2, E U_i^2=v_i^2/sigma^4,
E exp(U_i) <= 1 + delta_i,
delta_i = exp(b_i^2/sigma^2) v_i^2/(2 sigma^4).
```

Thus `product_i (1+delta_i) <= exp(sum_i delta_i)` and

```text
chi^2(P||Q) <= exp(sum_i exp(b_i^2/sigma^2) v_i^2/(2 sigma^4)) - 1.
TV(P,Q) <= (1/2) sqrt(chi^2(P||Q)).
```

For rare coordinates `X_i`, let `|X_i|<=A w`, `Pr(X_i!=0)<=C w`, and `V_i=X_i-E X_i`. Under independence,

```text
|V_i|<=2Aw, v_i<=E X_i^2<=C A^2 w^3, |E X_i|<=C A w^2.
```

For fixed `A,C,sigma` and sufficiently small `w`, each exponential prefactor is bounded by a constant, so the total chi-square exponent is `O(d w^6)`. At `w=d^(-1/4)`, `TV=O(d^(-1/4))` while `||E X||_2<=C A sqrt(d) w^2=O(1)`.

## Vector subGaussian bound

Suppose the centered vector has proxy `S>=0` in the sense

```text
E exp(t^T V) <= exp(t^T S t/2) for every t in R^d.
```

Condition on `V` in the second-moment identity and apply this bound to `V'` at `t=V/sigma^2`:

```text
E_{V'} exp(V^T V'/sigma^2) <= exp(V^T S V/(2 sigma^4)).
```

For an independent `H~N(0,I)`, the Gaussian moment-generating function gives

```text
exp(V^T S V/(2 sigma^4)) = E_H exp(H^T S^(1/2) V/sigma^2).
```

Now apply the proxy inequality to `V` at `t=S^(1/2)H/sigma^2`:

```text
E_V exp(H^T S^(1/2)V/sigma^2)
 <= exp(H^T S^2 H/(2 sigma^4)).
```

The Gaussian quadratic-form integral is finite when `||S||_op<sigma^2`, and equals `det(I-S^2/sigma^4)^(-1/2)`. This proves

```text
1+chi^2(P||Q) <= det(I-S^2/sigma^4)^(-1/2).
```

## Whole-vector Lipschitz oracle algorithm

For `G~N(0,I_d)` and globally Euclidean `L`-Lipschitz `g:R^d->R^d`, every scalar projection `t^T g(G)` is `L||t||`-Lipschitz. Gaussian concentration gives centered proxy `L^2 I` for `X=g(G)`. For `k` independent oracle samples, `bar X=k^(-1) sum_j g(G_j)` has proxy `S=L^2 I/k`. Consequently

```text
chi^2(Law(bar X+Z)||N(E g(G),sigma^2 I))
 <= (1-L^4/(k^2 sigma^4))^(-d/2)-1,
```

provided `k>L^2/sigma^2`. By `TV<=sqrt(chi^2)/2`, a sufficient real threshold is

```text
k >= (L^2/sigma^2) / sqrt(1-exp(-2 log(1+4 epsilon^2)/d)).
```

Take the ceiling and at least one query. For small `epsilon` and large `d`, this is asymptotic to `(L^2/sigma^2) sqrt(d)/(sqrt(8) epsilon)`. Each query returns a full `d`-vector, so the sampler uses `k` oracle calls, reads `kd` real coordinates, uses `O(kd)` arithmetic and can accumulate with `O(d)` storage. It also draws `k` exact standard Gaussian query seeds and one independent exact Gaussian output-noise seed under N687's ideal-real model. It never estimates `E g(G)`.

If the digital result is compared after a common quantizer on both laws, total variation cannot increase by the data-processing inequality. This does not bound finite-bit Gaussian generation or oracle-value arithmetic error. The separate report gives the precise oracle-transcript caveat and the rare-bump gradient construction.
