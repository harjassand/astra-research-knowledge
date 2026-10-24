# Scalar GP release: resource ledger and vortex readout

Bounded audit of the stated two-dimensional Gross-Pitaevskii construction.
Let `r^2=x^2+y^2`, `P=r^2+a+bx`, `a>b^2/4`, and
`rho_I=|psi_I|^2` for `psi_I=c P exp(-r^2/2)`. Define
`Z=(a+1)^2+1+b^2/2` and `I4=int rho_I^2 d^2x`.

## Conserved quantities and preparation/quench work

The norm is `int P^2 exp(-r^2)d^2x = pi Z`, so `c=(pi Z)^(-1/2)` for
unit particle number. The scalar GP equation with real potential conserves
`N=int |psi|^2`; there is no particle source in the proposed ramps or
release. The initial wavefunction is real, hence its angular momentum
`Lz=int psi* (-i partial_theta) psi d^2x` is zero. The released Hamiltonian
is rotationally invariant, including the radial contact term, so `Lz` stays
zero after release. The linear pair has opposite winding charges; it does
not create net angular momentum.

The engineered pre-release one-body potential is
`Vpre^g=r^2/2+[2(a+1)+bx]/P-g rho_I`. With the GP interaction `g rho`, the
`-g rho_I` counterterm cancels it on `psi_I`, leaving the same stationary
equation and chemical potential `3`. At `g=0`, `psi_I` is the positive
ground state of `Vpre^0`; its energy in the *post-release harmonic* trap is

```text
Epost0 = [(a+1)^2+b^2+3]/Z.
```

For the pre-release GP energy functional, the counterterm contributes
`-g I4` and the interaction contributes `+g I4/2`, hence
`Epre^g=3-g I4/2`. Ramping `g:0->g` while adding the counterterm and keeping
`psi_I` stationary does real parameter work
`W_g=-g I4/2`. After the quench to the harmonic trap while retaining `g`,
`EpostGP=Epost0+g I4/2`; therefore the instantaneous quench work is
`W_quench=EpostGP-Epre^g=Epost0-3+g I4`.

An ideal reversible ground-following preparation from the unit harmonic
ground state (energy `1`) to the unit ground state of `Vpre^0` (energy `3`)
has endpoint work `2`. Under that idealized path, the total through the
interaction/counterterm ramp and quench is
`2-g I4/2 + Epost0-3+g I4 = EpostGP-1`, exactly the post-GP energy above the
initial harmonic ground. The `2` is an ideal quasistatic ground-state
endpoint difference, not an acquired work measurement; without a specified
preparation path, its actual work and losses are unknown. The spatially
sculpted `-g rho_I` potential must itself be generated and switched. Returning
the controller and field to their initial states also needs a protocol;
reversing parameter values alone does not restore a state that has evolved.
For a truly closed cycle returning the same state and controls,
`W_net=D_total` with work positive into the system and `D_total` all exported
or dissipated energy. The stated construction supplies no measured cycle
efficiency or free reset.

After the quench, the GP energy
`int[|grad psi|^2/2+r^2 rho/2+g rho^2/2]d^2x` is conserved. The exact
`t=pi/2` opposite-vortex formula below is for `g=0`; for `g>0`, the released
nonlinear dynamics need not keep those centers or the linear pair trajectory.
The anisotropic pre-potential can exchange angular momentum with its
controller during a nonideal preparation, even though the specified exact
initial state has `Lz=0` and the post-release rotationally symmetric
evolution conserves it.

## Readout that excludes tail zeros

For `g=0`, harmonic-oscillator mode phases give, up to a global phase,

```text
psi(x,y,pi/2) = c exp(-r^2/2) [ i(r^2-a-2) - b x ].
```

For `b!=0`, its isolated zeros are at
`z_+=(0,+sqrt(a+2))` and `z_-=(0,-sqrt(a+2))`. The local Jacobian of
`(Re psi,Im psi)` has sign `-sign(b y)`, so their windings are
`q_+=-sign(b)` and `q_-=+sign(b)`.

Choose disjoint compact disks centered at these predicted positions, with
outer radius less than `sqrt(a+2)`. On each measured contour require a
resolved density floor `rho>=rho_boundary>0` and compute

```text
q = (1/(2 pi)) integral_boundary grad(arg psi) . dl.
```

A nonzero boundary density makes this degree well-defined and nonzero degree
forces a zero inside, but this alone can certify a nearly empty tail defect.
For an annulus `r_core<=|x-z|<=R` with measured density lower bound
`rho_min(r)>0` and winding `q`, Cauchy-Schwarz on each circle gives the exact
phase-kinetic lower bound

```text
K_phase(annulus) = (1/2) integral_annulus rho |grad(arg psi)|^2 d^2x
                 >= pi q^2 integral_(r_core)^R rho_min(r) dr/r.
```

Thus a report of an energetic vortex should pair the signed winding with a
resolved nonzero annular density and a positive, uncertainty-resolved
annular kinetic lower bound, as well as persistence at later observation
times. A phase zero in an arbitrarily dilute tail has a vanishing such bound
and does not meet that criterion. For `g>0`, the contours and cores must be
tracked from the actual field; the `g=0` positions are not a prediction of
the nonlinear trajectory. This defines a readout criterion, not a detector
specification or a lifetime claim.
