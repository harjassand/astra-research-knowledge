# Moving-face ionic transfer and conductivity-frame audit

## Assumptions and conventions

This checks only Sections 1 and 3 of `deep_continuation/new_opportunity/ELASTIC_INTERFACE.txt`. Let z point from the bottom face to the top face, with undeformed skin occupying `0 <= z <= b`. A Fourier perturbation has lateral wave number `q`. The base electrochemical-potential gradient uses the sign convention `d(phi_bar)/dz = G`, where `G=j0/k_n`. The perturbation potential on the reference slab is `u(z)`, and `j_b,j_t` are incremental normal current densities at the two faces. The stated model uses a fixed Eulerian conductivity tensor `diag(k_t,k_n)` in the flat reference slab and does not add a conductivity response to elastic strain or rotation.

## Moving-face linearization

At the displaced bottom face `z=h`, the first-order physical potential perturbation is the Eulerian perturbation evaluated at the reference face plus the base gradient carried through the displacement:

```text
delta(phi_bottom) = u(0) + G h.
```

The declared linear bottom reaction law is `delta(phi_bottom)=r j_b+chi h`, where `r` is differential charge-transfer resistance and `chi h` is the reaction/mechanical voltage shift. Equating these gives

```text
u(0) = r j_b + (chi-G)h.
```

At the displaced top face `z=b+v`, the same Taylor expansion gives the physical pore-side potential perturbation

```text
W = u(b) + G v.
```

The outer electrolyte and porous layer are a series differential impedance. Linearizing the resistance drop with `R(v)=R+R_v v` around base current `j0` gives

```text
delta(R j) = R j_t + j0 R_v v,
W = -Z_b j_t - delta(R j)
  = -(R+Z_b) j_t - j0 R_v v
  = -L j_t - j0 R_v v.
```

This sign convention and boundary law are model inputs. The `G h` and `G v` terms are geometric evaluations of the base field at moving faces; dropping either changes the linearization. The outer relation assumes `Z_b` itself is fixed and the skeleton enters through `R_v` and the mechanical transfer `v=m h`.

## Exact skin transfer and elimination

The perturbation equation is

```text
k_n u'' - k_t q^2 u = 0.
```

Define `q_s=q sqrt(k_t/k_n)`, `p=k_n q_s=q sqrt(k_n k_t)`, `C=cosh(q_s b)`, and `S=sinh(q_s b)`. Away from `q_s=0`, propagation of `(u,k_n u')` from bottom to top is

```text
u(b)       = C u(0) + (S/p) j_b,
j_t = k_n u'(b) = p S u(0) + C j_b.
```

Substitute the bottom law. Using `W=u(b)+Gv` yields the first transfer identity

```text
W = (r C + S/p) j_b + C(chi-G)h + Gv.
```

The current identity is

```text
j_t = (C + r p S) j_b + p S(chi-G)h.
```

Now impose `v=m h` and `W=-L j_t-j0 R_v v`. Collecting the `j_b` terms gives

```text
D j_b = N h,
D = r C + S/p + L(C+r p S),
N = (G-chi)(C+L p S) - m(G+j0 R_v).
```

Thus `j_b/h=N/D`. For `q>0`, `C,S,p` are positive; with `r>=0` and `L>0`, `D>0`. In particular, the sign of the transfer response is controlled by `N`, not by a zero or sign change in the denominator.

## Long-wave limit and units

As `q -> 0`, `q_s -> 0`, `C -> 1`, `S/p -> b/k_n`, and `pS -> 0`. Directly, the zero-wave-number solution is linear in z, so `j_t=j_b` and `u(b)=u(0)+(b/k_n)j_b`. Therefore

```text
D(0) = r + b/k_n + L(0),
N(0) = G - chi(0) - m0(G+j0 R_v)
     = G(1-m0) - chi(0) - m0 j0 R_v,
```

where `m0=lim_(q->0) m(q)`. This is the q-to-zero limit of the ionic transfer system without needing an additional mechanical relation for `chi`.

The dimensions are consistent when `r,R,Z_b` are area-specific resistances in `ohm m^2`, `R_v` is `ohm m`, `k_n,k_t` are `S/m`, and `q_s` is `1/m`. Then `p` is `S/m^2`; `S/p`, `r`, and `D` are `ohm m^2`; `G` and `chi` are `V/m`; `N` is `V/m`; and `N/D` is `A/m^3`, the derivative of current density with respect to displacement. The quantity `j0 R_v` has units `V/m`, as required.

## What conductivity law this does and does not assume

The transfer identities solve the constant-coefficient Eulerian problem exactly. They include the first-order moving-face evaluation of the base potential, but hold the spatial conductivity tensor fixed as `diag(k_t,k_n)` while the skin deforms. This is a constitutive assumption, not a consequence of elasticity.

If the anisotropic conductivity is attached to material axes, a rotation changes its Eulerian orientation; strain can also change its spatial components. For example, under the conventional push-forward of a reference conductivity tensor `K0` and referential current flux, one would use `K_sp=(1/J) F K0 F^T`, with deformation gradient `F` and volume ratio `J`. Its linearization generally contributes `delta K` terms to `div(K_sp grad(phi))` and to the normal-current boundary condition. Other transport conventions or strain-dependent ionic mobilities give different laws. For isotropic conductivity, pure rigid rotation leaves the tensor unchanged, but strain can still change the spatial tensor or carrier density.

Consequently E4 is valid for a declared constant Eulerian tensor (or an independently justified law that linearizes to it). It is not valid to infer that a crystal-fixed anisotropic tensor remains Eulerian-constant merely because `k_n,k_t` were supplied. The strain/rotation transport law and its measured coefficients are an additional physical input; this audit does not acquire them.
