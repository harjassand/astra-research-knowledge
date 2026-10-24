# Local complete-flip rigidity: bounded audit

Independent check of Section 3 of the lead candidate
`ALL_TIME_LAX_BUDGET_GATE.md`. Result: the lemma is valid under the literal
hypotheses below. The proof uses the L2 Cauchy-boundary theorem on an open
interval and analytic continuation across an interval where the density
vanishes. It needs no Hardy-space positive-measure boundary theorem.

Let
`L_j(z) = integral_I v D_j(v)/(z-v) dv`,
`ell(z) = integral_I v G(v)/(z-v) dv`, and
`M(z) = L_z(z)+ell(z)`. Since I has finite measure, D is in L-infinity,
and G is continuous, every density `v D_j`, `v G`, and
`f(v)=v(D_z(v)+G(v))` belongs to L2(I). The bilinear invariant is exactly

```text
L_x(z)^2 + L_y(z)^2 + M(z)^2 - 2 M(z) ell(z) = 0,   z outside I.
```

For an L2 density f, its Cauchy transform
`C_f(z)=integral_I f(v)/(z-v) dv` has nontangential upper and lower
boundary values in L2, with

```text
C_{f,+}(x)-C_{f,-}(x) = -2 pi i f(x)   a.e.
```

The vertical boundary approximants converge in L2. Therefore products of
any two such approximants converge in L1: if a_y -> a and b_y -> b in L2,
then

```text
||a_y b_y - ab||_1
 <= ||a_y-a||_2 ||b_y||_2 + ||a||_2 ||b_y-b||_2.
```

Taking upper and lower limits of the invariant, which holds off I, gives
the boundary invariant in L1 on each side. No pointwise multiplication of
merely weak boundary limits is being assumed.

Choose a nonempty open subinterval J' compactly contained in J and away
from v=0. On J', D_x=D_y=0 and D_z+G=0 a.e. Hence L_x, L_y, and M all
have zero jump there. But

```text
ell_+(x)-ell_-(x) = -2 pi i x G(x)
```

is nonzero a.e.; after shrinking J', its magnitude is bounded away from
zero. The upper and lower boundary versions of the displayed invariant
have identical L_x^2, L_y^2, and M^2 terms. Their difference is therefore

```text
-2 M(x) [ell_+(x)-ell_-(x)] = 0   a.e. on J'.
```

Thus both traces of M vanish a.e. on J'.

Now M is the Cauchy transform of f(v)=v(D_z+G), and f=0 a.e. on J'. For
any smaller compact interval K inside J', the support of f is separated
from K, so the integral defining M is holomorphic through K and agrees
there with its boundary traces. That holomorphic extension is zero a.e.
on K; continuity makes it zero on K, and the identity theorem makes it
zero on a neighborhood. The complement of the support of f, a subset of
the real axis, is connected. Hence M is zero throughout its
Cauchy-transform domain. Its L2 jump then gives f=0 a.e. Injectivity yields
`v(D_z(v)+G(v))=0` a.e.; the singleton v=0 has zero Lebesgue measure, so
D_z=-G a.e. The pointwise ball |D|<=|G| forces D_x=D_y=0 a.e. This makes
`integral_I D_z=-q`, contradicting the fiber constraint
`integral_I D_z=q` when q!=0.

Literal needed hypotheses: the invariant holds for every complex z off the
interval (so both vertical boundary limits are available); the Cauchy
densities are L2 (ensured by the finite interval, L-infinity bound, and
continuous G); there is a nonempty open flipped interval on which xG(x)
is nonzero a.e.; and the relaxed fiber has charge `integral_I D=q zhat`
with q!=0. The interval can be shrunk to avoid x=0. No regularity of D
beyond L-infinity, no boundary values outside that interval, and no
dynamical reachability of the whole fiber are used.

