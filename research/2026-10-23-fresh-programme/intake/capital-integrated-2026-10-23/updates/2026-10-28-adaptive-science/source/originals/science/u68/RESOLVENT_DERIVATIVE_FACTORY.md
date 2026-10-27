# Exact finite-value action for the first derivative of the full resolvent

The analytical joint gauge needs source derivatives. This note acquires one precise derivative interface from legal values, including raw C1,1 conservative sources. It does not acquire the entire gauge or Gaussian law.

Let g be globally L-Lipschitz and let

```
K_b(y) = ∫_0^b E Dg(ρy+sqrt(1-ρ²)Z) dρ,   0<b<=1.
a = sqrt(1-b²),   m_b=1-a.
```

The full b=1 kernel is C1 for the conservative source class, as proved in frozen S4 section 11. For supplied y,v,w, this exact THREE-query random vector has mean D K_b(y)[v] w.

If v=0 or w=0 return zero. Otherwise put u=w/||w|| and independently draw

```
S ~ Uniform[a,1],    ρ=sqrt(1-S²),    c=ρy,
Zperp ~ N(0,I-uu^T), R ~ chi_3, T ~ Uniform[-1,1].
```

Uniforms can be produced from scalar Gaussian sphere coordinates as in the frozen sources. S>0 and R>0 almost surely; define an arbitrary value on null endpoints. Query

```
x+ = c+S Zperp+S R u,
x- = c+S Zperp-S R u,
xT = c+S Zperp+S R T u.
```

Set

```
D = [g(x+)-g(x-)]/(2 S R),
Q = [g(x+)+g(x-)-2g(xT)]/(2 S),
J_DK(y;v,w) = m_b ||w|| [(v·Zperp) D + (v·u) Q].
```

## Unbiasedness

Conditional on Zperp,R, absolute continuity on the chord gives

```
D = E_T Dg(c+S Zperp+S R T u) u,
E_T Q = E_T [(RT) Dg(c+S Zperp+S R T u) u].
```

The second identity follows by scalar integration by parts. Since RT is standard normal under the chi3 mixture, the expectation at fixed S is

```
E J_DK / m_b = E_Z [Dg(c+SZ) w (v·Z)].
```

Gaussian integration by parts gives

```
D K_b(y)[v]w
 = ∫_0^b [ρ/sqrt(1-ρ²)]
       E[Dg(ρy+sqrt(1-ρ²)Z)w (v·Z)] dρ.
```

Changing variables S=sqrt(1-ρ²) turns the positive measure into Lebesgue measure on [a,1], proving the claim. Dg appears only in analysis. The finite program evaluates exactly three g values.

## Dimension-free moments and query count

Lipschitzness gives pointwise

```
||D|| <= L,       ||Q|| <= LR,
||J_DK|| <= m_b L||w|| [|v·Zperp| + |v·u|R].
```

In particular

```
(E||J_DK||²)^(1/2) <= 2 m_b L||v||||w||.
```

For p>=2 the bound is at most C sqrt(p) m_b L||v||||w|| with an absolute C. Only a scalar Gaussian projection and chi3 radius appear. The sample is not uniformly bounded; its Gaussian tail and deterministic query count are separate receipts. Fresh seeds make the theorem conditional on arbitrary previously acquired y,v,w.

## Affine-annihilating antithetic version

The three-query estimator has nonzero variance even on affine g. Pair T with -T, replacing Q by

```
Q_even = [g(x+)+g(x-)-g(xT)-g(x(-T))]/(2S).
```

This costs four queries. Also average the entire estimator at Zperp and -Zperp with the same R,T. The resulting version costs at most EIGHT queries, has the same expectation and no greater second moment by conditional Jensen, and is exactly zero on **every execution for every affine g(x)=Ax+c**. In d=1 the perpendicular pairing is redundant, so four queries suffice. Only deterministic g values and vector arithmetic are used.

## Remaining boundary

This is a first full-resolvent tensor action, not a common realized derivative tensor. Adaptive composition needs fresh seeds and the appropriate conditional input. The Newton coefficient K-Dh still includes a raw derivative at a fixed point; a small operator norm does not supply that coefficient as a value oracle. Coupled products, Hermite/OU inverses, and the law of randomized corrections remain unresolved. A random unbiased correction changes the law through conditional second moments and higher terms. No Gaussianity, full-law quadratic update, subcritical query forest, universal polylog bound or novelty claim follows from this action factory alone.
