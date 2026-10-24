# Fixed-g cyclic control ledger and robust vortex readout

This note audits the revised operation with one fixed `g>=0` throughout;
there is no interaction ramp and no `-g rho_I` counterterm. It supersedes
the variable-g stage ledger in `GP_LEDGER_AND_VORTEX_READOUT.md` for this
protocol. Use `H0=(-Delta+r^2)/2`, and let the controlled one-body term be
`V_c(x,t)=chi_R(x)(W_s(x)-2)`, with the same real potential path for every
`g`. The actual control schedule starts and ends at `V_c=0`, so both endpoint
Hamiltonians are `H0+g|psi|^2` (the constant `+2` sometimes added to all
stages is omitted; it changes only global phase and cancels from a fixed-N
closed-cycle work balance).

## Complete field-work identity

Let `Phi_g` be the normalized radial ground state of the initial harmonic GP
energy

```text
E_g[H0;psi] = integral [ |grad psi|^2/2 + r^2 |psi|^2/2
                         + g |psi|^4/2 ] d^2x.
```

For the Hamiltonian GP equation with real time-dependent `V_c` and fixed `g`,
`N=integral |psi|^2=1` is conserved and the exact work transferred into the
field over the entire forward preparation and smooth release is

```text
W_field = integral_time integral_space |psi(x,t)|^2 partial_t V_c(x,t)
                           d^2x dt
        = E_g[H0;psi_final] - E_g[H0;Phi_g] >= 0.
```

The inequality is the ground-state variational principle because the
Hamiltonian and controls return to their initial values. It does not count
laser/electrode/control-driver losses or stored energy outside the field;
those require an actuator model and a returned-controller state. No free
reset follows from returning the potential profile.

At `g=0`, the full target potential is `Vpre-2`, for which `psi_I` is the
ground state at energy `1`, matching the harmonic ground energy `1`. For a
reversible adiabatic preparation, the ideal preparation work is therefore
zero. A sudden release of that target state to `H0` costs

```text
W_release = Epost0 - 1 = [b^2/2 + 2]/Z > 0,
Epost0 = [(a+1)^2+b^2+3]/Z,
Z = (a+1)^2+1+b^2/2.
```

The winding pair is paid for as post-release excitation energy. An adiabatic
return would instead follow the ground state and erase the desired
nonequilibrium output, so the release must be nonadiabatic. For fixed cutoff
`R`, the real confining `g=0` preparation path has a positive minimum ground
gap when the ground remains simple; sufficiently large finite `T` then
prepares its target to adiabatic accuracy. Taking `R` large controls the
cutoff error in the target on the readout region. The release time `tau` must
be short enough to preserve the sudden-release reference. For the resulting
fixed finite `R,T,tau`, continuous dependence of the smooth GP evolution on
small `g` can preserve a readout with strict topological/density margin.
This is finite-horizon continuity, not a uniform-in-time or lifetime claim.

## Symmetry and local readout margins

The initial `Phi_g` and the stated controls are even under `y -> -y`. The
fixed-g GP evolution preserves that reflection symmetry. Since `Lz` changes
sign under this reflection, `Lz=0` throughout preparation and release; this
does not rely on rotational symmetry during the anisotropic control stage.
After the controls return to radial `H0`, angular momentum is also conserved
by the post-release dynamics. The linear `g=0` pair has opposite local
winding, consistent with zero total angular momentum.

In the sudden `g=0` reference, at time `pi/2` after release,

```text
psi_0(x,y) = c exp(-r^2/2) [ i(r^2-a-2) - b x ],
z_+ = (0,+sqrt(a+2)),  q_+ = -sign(b),
z_- = (0,-sqrt(a+2)),  q_- = +sign(b).
```

Choose disjoint disks about `z_+` and `z_-` with outer radius
`R_d<sqrt(a+2)`. The exact reference has no zero on their boundaries or on
any closed annulus `r_core<=|x-z_±|<=R_d` with `0<r_core<R_d`; hence the
minimum boundary amplitude `eta_b` and annular amplitude `eta_A` are
strictly positive. If the finite-cutoff, finite-`T`, smooth-release, small-g
field differs from `psi_0` in `C^0` on these compact sets by less than
`min(eta_b,eta_A)/2`, then each boundary winding is unchanged and the
annular density is at least `eta_A^2/4`. `C^1` closeness near the simple
zeros, together with `C^0` closeness on the compact remainder of each disk,
preserves exactly one nearby simple zero with the same charge in each disk.
This supplies a conditional robustness margin; it does not supply
numerical values of `R,T,tau,g` or prove the error bound for a particular
control implementation.

For a measured annulus with density lower bound `rho_min(r)>0` and boundary
winding `q`, the phase-flow energy obeys

```text
K_phase = (1/2) integral_annulus rho |grad(arg psi)|^2 d^2x
        >= pi q^2 integral_(r_core)^R_d rho_min(r) dr/r.
```

Thus the observable should include (i) nonzero, resolved density on a closed
contour, (ii) signed phase winding there, and (iii) a positive annular
phase-kinetic lower bound, followed at later finite observation times if
persistence is at issue. A topological zero in an arbitrarily dilute tail
fails the energetic criterion. For `g>0`, disk centers must be tracked from
the actual field; the exact linear positions are only the continuity
reference. No detector, lifetime, or returned-field performance is claimed.
