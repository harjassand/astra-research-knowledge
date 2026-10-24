# Counted longitudinal intercell rod: exact scalar transfer model

This note replaces the massless intercell spring in the two-mass design by a
distributed, finite-inertia elastic rod. It counts the rod's complete
longitudinal field, its mass, and every propagating band below a stated thermal
tail cutoff. The numbers are an illustrative 1D continuum calculation, not a
named-material data claim or a manufactured-device result.

## Cell and comparison contract

Each period has a point backbone mass `m_b`, a side mass `m_s` attached to it
by a spring `k`, and one uniform axial rod of length `a`, area `A`, density
`rho`, and Young modulus `E` joining this backbone to the next one. The rod is
counted once per period. Its wave speed is `c_L=sqrt(E/rho)`, its static
intercell stiffness is `K=EA/a`, and its mass is `m_r=rho*A*a`. Thus

```text
M_cell = m_b + m_s + m_r,
mu_r = m_r/m_b = K*a^2/(c_L^2*m_b).
```

For a finite `N`-period sample, I use `N` point modules separated by `N-1`
full rods and two half-rods at the ends. The sample has length `N*a`, contains
exactly `N` full rod-lengths, and has mass exactly `N*M_cell`. The comparison
sample has the same rods, same `E,rho,A,a`, same total mass and length, and
replaces each backbone-plus-side module by one rigid point mass
`m_R=M_cell-m_r`. Both samples use the same lead and boundary planes.

Two readouts are kept distinct:

* For the intrinsic ideal-contact periodic readout, semi-infinite matched
  copies of each periodic medium give unit transmission in each Bloch pass
  band. Its dimensionless conductance is `J=integral g(omega) chi(omega)domega`
  with `g=(omega/sinh(omega))^2` at `theta=1/2`.
* For a concrete finite lead check, the `N`-period samples are joined at their
  half-rod boundary planes to semi-infinite *bare rods* of the same
  `E,rho,A`. This has ordinary interface reflection and is evaluated from its
  finite transfer matrix. It is a separate, contact-dependent diagnostic.

Neither readout includes transverse rod polarizations, lateral supports,
anharmonic scattering, disorder, or real contact resistance beyond the
specified bare-rod leads.

## Exact rod and resonator transfer

At angular frequency `omega`, put `kappa=omega/c_L` and use the state
`(u,N)`, where `N=EA*u'` is axial force. Solving the continuum equation inside
one rod gives

```text
T_r(l) = [[cos(kappa*l), sin(kappa*l)/(EA*kappa)],
          [-EA*kappa*sin(kappa*l), cos(kappa*l)]].
```

The local side-mass equation is
`(k-m_s*omega^2)u_s=k*u_b`. Eliminating `u_s` away from its pole makes the
backbone force jump
`N^+ - N^- = -omega^2*m_eff(omega)*u_b`, with

```text
m_eff(omega) = m_b + k*m_s/(k-m_s*omega^2),
P(omega) = [[1,0],[-omega^2*m_eff(omega),1]].
```

Equivalently, the exact rod endpoint dynamic stiffness is
`EA*kappa/sin(theta) * [[cos(theta),-1],[-1,cos(theta)]]`. Bloch assembly of
the left and right rods and the local two-mass module gives

```text
[[2*EA*kappa*(cos(theta)-cos(q))/sin(theta) + k - m_b*omega^2, -k],
 [-k,                                                   k - m_s*omega^2]]
```

and a mode exists when this matrix has zero determinant. Eliminating `u_s`
recovers the transfer discriminant below. The endpoint formula is singular at
`sin(theta)=0`; the rod transfer matrix is regular there, and those frequencies
are included as band edges by continuity rather than discarded as missing
rod modes.

The one-period transfer is `M_cell=T_r(a) P`; its determinant is one and

```text
Delta(omega) = trace(M_cell)/2
              = cos(kappa*a)
                - omega^2*m_eff(omega)*sin(kappa*a)/(2*EA*kappa).
```

A propagating Bloch wave exists precisely when `Delta=cos(q)` is real and in
`[-1,1]`. At the isolated side-resonance pole, the eliminated formula is
understood through the original coupled backbone/side equations; for the
displayed noncoincident parameters it is a stop frequency and has zero measure
in the conductance integral. The rod's standing-wave bands are not discarded.

In dimensionless frequency `Omega=omega/omega_u`, let
`r=omega_u*a/c_L`, `Kbar=K/(m_b*omega_u^2)`, and normalize `m_b=1`. Then
`mu_r=Kbar*r^2` and, at fixed total cell mass `Mbar`,
`m_sbar=Mbar-1-mu_r`. The exact discriminants are

```text
Delta_res(Omega) = cos(r*Omega)
  - Omega^2/(2*Kbar) * [1+kbar*m_sbar/(kbar-m_sbar*Omega^2)]
    * sinc(r*Omega),

Delta_rigid(Omega) = cos(r*Omega)
  - Omega^2*(Mbar-mu_r)/(2*Kbar) * sinc(r*Omega).
```

Here `sinc(x)=sin(x)/x`. At low frequency,
`m_eff(0)+m_r=m_b+m_s+m_r=M_cell`, so both structures keep the same
long-wavelength acoustic speed `sqrt(E*A*a/M_cell)`. The first rod half-wave
scale is `Omega=pi/r=pi*sqrt(Kbar/mu_r)`; higher rod bands move into the
thermally suppressed tail as `mu_r` decreases.

## Finite sample and leads

For the finite comparison, normalize the state to `(u,N/(EA*kappa))`. A rod
segment of phase `phi=kappa*l` is the rotation

```text
R(phi) = [[cos(phi),sin(phi)],[-sin(phi),cos(phi)]],
```

and a point module is `Pbar=[[1,0],[-b,1]]`, where
`b=m_eff*omega^2/(EA*kappa)` (use `m_R` for the rigid sample). For `N` cells,
the symmetric sample transfer is

```text
M_N = R(theta/2) Pbar [R(theta) Pbar]^(N-1) R(theta/2),
theta=kappa*a.
```

In bare-rod leads the right- and left-going wave states are proportional to
`(1,+i)` and `(1,-i)` in this normalized basis. With
`S=P0^-1 M_N P0`, `P0=[[1,1],[i,-i]]`, flux conservation gives
`tau_N=1/|S_22|^2`, equivalently

```text
S_22 = (M_N,11+M_N,22)/2 + i*(M_N,21-M_N,12)/2.
```

This specifies the actual finite scalar chain, its leads, contact planes, and
per-cell mass assignment. It is not the matched-periodic-lead ideal-contact
observable.

## Dependence on counted rod mass

The dimensionless finite-rod parameter is
`mu_r=Kbar*r^2`; it changes both rod phase and the side mass available at fixed
`Mbar`. For `r*Omega << 1`,
`cos(r*Omega)=1-r^2*Omega^2/2+O(r^4*Omega^4)` and
`sinc(r*Omega)=1-r^2*Omega^2/6+O(r^4*Omega^4)`. Thus the low-frequency
discriminant changes at order `mu_r`, while the extra rod standing-wave bands
start at a frequency of order `mu_r^(-1/2)`.

One can make the first-order departure from the proven massless-link optimum
explicit while retaining its `kbar` and subtracting `mu_r` from the side mass.
Write `s0=Mbar-1`,

```text
m0(Omega)=1+kbar*s0/(kbar-s0*Omega^2),
D(Omega,mu)=cos(sqrt(mu/Kbar)*Omega)
  - Omega^2/(2*Kbar) * m_eff(Omega,mu)
    * sinc(sqrt(mu/Kbar)*Omega).
```

At `mu=0`,

```text
D_mu = -Omega^2/(2*Kbar)
        +Omega^2*kbar^2/[2*Kbar*(kbar-s0*Omega^2)^2]
        +m0(Omega)*Omega^4/(12*Kbar^2),
D_Omega = -[2*Omega*m0(Omega)+Omega^2*m0'(Omega)]/(2*Kbar),
m0'(Omega)=2*kbar*s0^2*Omega/(kbar-s0*Omega^2)^2.
```

For an edge `D(Omega_e(mu),mu)=+/-1`,
`Omega_e'(0)=-D_mu/D_Omega`. On the optimal bands the three endpoint
derivatives at `1,2,c` are respectively `+0.209397677`, `-0.572415026`,
`-0.691257666`. Since `g=(Omega/sinh(Omega))^2`, the ideal-contact
conductance slope is `J_res'(0)=+0.315667451` per unit `mu_r`. For the rigid
periodic comparator, `Omega_R=2*sqrt(Kbar/Mbar)` and
`Omega_R'(0)=Omega_R^3/(12*Kbar)`, giving `J_rigid'(0)=+0.056075762`.
Consequently the conductance advantage decreases initially at slope
`-0.259591688` per unit rod/backbone mass ratio. This derivative is local to
the stated retuning convention; it is not a global finite-rod optimization.

## Reproducible illustrative point

Use the exact optimum's dimensionless values
`Kbar=3.786631643761`, `Mbar=3.338716423202`, `kbar=2.801934787812`, and
`c=4.259874009292`. For scale only, set `f_u=1 GHz`, so
`omega_u=2*pi*f_u` and `theta=1/2` corresponds to `T=0.0239962 K`.
Choose an *illustrative* axial rod parameter set
`E=125 GPa`, `rho=5000 kg/m^3`, square `30 nm x 30 nm` area, and `a=300 nm`.
These numbers are a synthetic consistent parameter choice, not sourced
properties of a named material. They give `c_L=5000 m/s`, `r=0.3769911184`,
and `mu_r=0.5381648112`; the retained side mass is still positive,
`m_s/m_b=1.8005516120`. The physical cell masses calculated from `K=EA/a`
are

```text
m_b       = 2.508525217e-18 kg,
m_rod     = 1.350000000e-18 kg,
m_side    = 4.516729123e-18 kg,
M_cell    = 8.375254341e-18 kg.
```

The static intercell spring is `EA/a=375 N/m`; the retained internal spring is
`277.482904 N/m`. No connector mass is hidden in the point masses.

Numerical root isolation of `|Delta|=1` on `0<=Omega<=20` gives:

| Structure | Propagating bands below 20 | `J` below 20 |
|---|---|---:|
| Side resonator | `[0,1.136089003]`, `[1.830731970,3.923708420]`, `[8.333333333,9.869740425]`, `[16.666666667,17.530918744]` | `1.277625400299` |
| Rigid same-mass comparator | `[0,2.253682922]`, `[8.333333333,8.935968160]`, `[16.666666667,16.984713098]` | `1.470633054359` |

The high rod bands are included; their contributions are `8.47e-6` and
`1.58e-12` for the resonator structure, and `5.95e-6` and `8.88e-13` for the
rigid comparison. For either structure the entire omitted ideal-band weight
above `Omega=20` is at most

```text
integral_20^infinity g(Omega)dOmega
 <= 841*exp(-40)/(1-exp(-40))^2 < 3.573e-15.
```

Thus this illustrative counted-rod point remains `0.1930076541` below the
same-mass/same-rod periodic comparator in the specified ideal-contact readout,
a `13.12%` reduction relative to that comparator. It is less than the
massless-link optimum's `21.31%` reduction; the rod consumes a substantial
part of the cell's mass budget.

For a shorter `a=100 nm` rod at the same illustrative wave speed, with the
same dimensionless `Kbar,Mbar,kbar` (and the corresponding backbone mass scale
recomputed from `K=EA/a`), `r=0.1256637061` and `mu_r=0.0597960901`. The
matched-periodic integrals are `J_res=1.1518457030` and
`J_rigid=1.4435337927`, a gap of `0.2916880897`. This provides a second point
on the same counted-mass trend; it is not the same physical-mass sample as the
300 nm example.

For the separate `N=10` sample between the bare-rod leads above, composite
Simpson integration on `[0,20]` gives `J=0.84683041` for the resonator sample
and `J=0.91049603` for the rigid sample at 500,000 panels. The 100,000-panel
values are `0.84685281` and `0.91049603`; the residual numerical grid
sensitivity is stated rather than treated as a theorem. The same Bose tail
bound applies since `0<=tau_N<=1`. This finite sample retains a `6.99%`
model-specific reduction under these bare-rod contacts; changing the leads or
sample length can change this number.

Run `python3 rod_transfer.py` from this directory to reproduce the displayed
transfer and integration diagnostics. The passband roots are numerically
isolated for this fixture; the exact all-frequency dual theorem in
`PHONON_OPTIMUM.md` still concerns the finite-cell massless-intercell-spring
class. This note does not extend that theorem to all distributed-rod networks
or assert a fabricated-material advantage.
