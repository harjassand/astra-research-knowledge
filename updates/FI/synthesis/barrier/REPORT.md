# Recoverable local-compliance gate: audit and finite-noise qualification

Date: 14 October 2026  
Status: conditional scalar-model derivation and internal replay; no physical
performance, novelty, or device claim.

## Finding

The supplied scalar construction is algebraically sound under its stated
coexistence sextic. Tangent compensation preserves the selected phase as a
global minimum while the gate is present, and eliminating the stated
zero-preload spring produces the claimed local quartic coefficient. At
`U=0.55b`, the exact middle-stage curvature margin is `0.514a`.

Two conditions limit the device interpretation. First, the cited BaTiO3
preprint has an unresolved sign discrepancy between its Table 1 sextic
coefficient and its End Note temperature law, so the resulting field, stress,
stiffness, and work values remain arithmetic targets under the package's
explicit Table 1 choice. Second, in a finite-noise single-coordinate model,
the fully restored zero-field endpoints are degenerate coexistence states.
High-confidence equilibrium selection therefore requires residual control; if
both controls are removed, the device must instead rely on metastable history
and demonstrate its retention time. The finite-time dissipation floor adds a
separate speed cost.

The additional calculation here is a finite-volume selection bound and its link to the
existing finite-time loss formula. It does not establish whether real domains,
interfaces, or nucleation follow this one-coordinate equilibrium model.

## Exact scalar path

For

\[
f_0(q)=\frac a2q^2-\frac b4q^4+\frac c6q^6,\quad
a=\frac{3b^2}{16c},\quad q_B^2=\frac{3b}{4c},\quad b,c>0,
\]

one has `f0(q)=c q^2(q^2-qB^2)^2/6 >= 0`. The minima `0,+qB,-qB` are tied.
Add `u q^4/4-hq`.

1. With `h=0`, raise `u` from `0` to `U`. The selected `q=0` remains a global
   minimum and is unique for every `u>0`.
2. Hold `u=U`, move along `0<=q<=qB`, and choose
   `h=aq+(U-b)q^3+cq^5`. The tilted potential is strongly convex if
   `mu=a-9(b-U)^2/(20c)>0`. For `U=0.55b`, `mu/a=257/500=0.514`.
3. Hold `q=qB`, reduce `u` to zero, and choose `h=u qB^3`. The energy
   difference from `qB` factors as
   `f0(q)+u(q-qB)^2(q^2+2qBq+3qB^2)/4 >= 0`.

The tangent term is the Bregman divergence of the convex gate `G(q)=q^4/4`.
This exact global-minimum certificate is conditional on the scalar `F0` and
on the ability to apply its compensating field. Full factorizations and the
elastic derivation are in [DERIVATIONS.md](DERIVATIONS.md).

## Mechanical work and preload

For `C(e-alpha q^2)^2/2 + K e^2/2`, minimization gives

\[
e_*=\frac{C\alpha q^2}{C+K},\qquad
u(K)=\frac{2\alpha^2CK}{C+K},\qquad
\partial_K f_{el,*}=e_*^2/2=(q^4/4)u'(K).
\]

Thus `u_max=2C alpha^2` and `K/C=U/(u_max-U)`. With an initial shunt
rest-strain `e0`, elimination instead adds

\[
\frac{u}{4}q^4-\frac{ue_0}{2\alpha}q^2
                      +\frac{ue_0^2}{4\alpha^2}.
\]

Preload shifts the quadratic coefficient and creates engagement work at
nominal `q=0`; the quartic-only path requires zero preload or an independently
measured compensation.

Along the ideal isothermal stroke,
`W_field=UqB^4/4` and `W_gate=-UqB^4/4`. This is zero *net reversible work for
one ideal phase-conversion stroke* between equal-free-energy states. It is not
free energy, a complete cycle, a refrigerator COP, or a device energy balance.

For overdamped tracking `zeta qdot=h-[f0'(q)+Uq^3]`, finite-time dissipation is
`zeta integral(qdot^2 dt)`. Any exact path from `0` to `qB` completed in time
`tau` therefore incurs

\[
W_{diss}\geq \frac{\zeta q_B^2}{\tau},\qquad
\frac{W_{diss}}{Uq_B^4/4}\geq
\frac{20}{11}\frac{\tau_{rel}}{\tau}\quad(U=0.55b),
\qquad \tau_{rel}=\zeta/a.
\]

Equality in the first inequality requires constant-speed scalar motion. This
floor is in addition to shunt hysteresis, dielectric loss, leakage, field and
stiffness generation, heat transfer, and other material kinetics. The scalar
friction and its timescale have not been measured for a specimen.

## Finite-noise endpoint qualification

In the one-coordinate finite-volume Gibbs model
`rho(q) proportional exp[-V f(q)/(kBT)]`, the zero-control curvatures are
`a,4a,4a` at `0,+qB,-qB`. Laplace weights are therefore asymptotically
`1/2,1/4,1/4`. Restricting to one basin has coarse-grained surprisal/free-energy
differences `kBT ln(2)` or `kBT ln(4)` relative to the full mixture in this
model; this does not include physical state-preparation or feedback costs. A
pure `q=0` initial state and a pure `+qB` final state are not the equilibrium
distribution at their exactly restored controls.

At the initial gate engagement with `h=0`, the total polar-to-central basin
ratio is asymptotically `exp(-x/4)`, where `x=V u qB^4/(kBT)`. A 99% central
basin target requires `x>=4 ln(99)=18.38...`; selecting the central phase
therefore also requires gate work from an equilibrated zero-control mixture.

For the interior strongly convex stage, Brascamp-Lieb gives
`Var(q)<=kBT/(V mu)`. Near final removal with `h=u qB^3`, define
`x=V u qB^4/(kBT)`. The small-`u` Laplace ratios are
`p_central/p_plus ~ 2 exp(-3x/4)` and
`p_minus/p_plus ~ exp(-2x)`. A 99% `+qB` basin target requires approximately
`x>=7.0511`, i.e.

\[
u\gtrsim 7.0511\frac{k_BT}{Vq_B^4},\qquad
h\gtrsim 7.0511\frac{k_BT}{Vq_B}.
\]

At those residual controls the original landscape is not fully restored. If
both controls are removed, high-confidence occupancy must come from
nonequilibrium retention instead, with finite lifetime and state-preparation
work measured. These are asymptotic results for a uniform scalar coordinate;
they do not substitute for a domain-resolved statistical mechanics model.

The result also means the deterministic statement “unique except at the
ungated coexistence endpoints” is a material limitation, not a technicality.
It does not invalidate a history-selected metastable stroke, but it prevents
the exact endpoint from being described as a unique finite-noise equilibrium.

## Spatial failure retained

A finite-lattice sufficient condition is available if the material architecture
really supplies a local quartic gate at every site. For onsite copies of the
coexistence sextic plus any positive-semidefinite quadratic graph coupling, the
homogeneous traversal Hessian is a diagonal matrix bounded below by `mu I`
plus the positive-semidefinite coupling matrix. The same local tangent
compensation, together with nonnegative gradient energy, certifies the
terminal homogeneous phase globally. This theorem gives a concrete
implementability target; it does not show that an elastic shunt supplies that
local gate or the required uniform bias. The full proof is in
[DERIVATIONS.md](DERIVATIONS.md).

A mean-only clamp
`U(4N)^(-1)(sum_i q_i^2)^2` matches the local gate on homogeneous states, but
its zero-mean-mode curvature is
`a-(3b-U)q^2+5cq^4`. Its minimum is
`a-(3b-U)^2/(20c)`, which equals `-a/15` at `U=b`; the local gate at the
same setting has minimum `a`. At the partial `U=0.55b`, the mean-only minimum
is exactly `-(901/1500)a`, while the local gate retains `0.514a`. The source's
finite four-cell Hessian is a diagnostic for this
specified model, not a spatial-device certificate.

There is a separate compatibility issue. Eliminating a displacement field
normally yields a nonlocal positive-semidefinite kernel in the eigenstrain
source `r_i=q_i^2`. For `G(q)=r^T J r/4`,
`H_G=diag(Jr)+2diag(q)Jdiag(q)`. Positive semidefiniteness of `J` makes
`G>=0` but does not make `H_G` positive: the exact kernel
`J=[[1,-1],[-1,1]]` gives `G=(q1^2-q2^2)^2/4` and
`H_G(1,0)=diag(3,-1)`. Entrywise nonnegative `J` plus `J>=0` is a sufficient
convexity condition for this kernel form. This abstract two-cell example is
not a BaTiO3 kernel; it shows why the actual compatible elastic Green function
and the full order-parameter Hessian must be measured or computed.

The cited primary preprint reaches the same physical caution from its own
multidomain calculation: elastic stresses satisfy mechanical equilibrium,
and the quartic self-energy is computed using nonlocal Fourier-projected
kernels. An ordinary elastic shunt therefore does not automatically realize
the pointwise `integral q^4` gate assumed in the scalar construction.

An independent delta audit also examined a proposed mixed local/mean quartic
ansatz. Within that exact control model, the sharp gate-local fraction for a
global-minimum path uniformly over system size is `theta*=0.167258...`; this
lies above the multi-site homogeneous linear-stability threshold `0.031754...`
but below the full-functional convexity threshold `0.354503...`. At
`theta=0.1`, an exact 32-cell finite-amplitude counterexample has lower energy
than the selected homogeneous state even though every homogeneous Hessian is
positive. The middle-stage theorem is conditional on this mixed ansatz; it neither rescues
the assumed material implementation nor changes the source's coefficient
qualification. The full independent derivation, edge-case qualification, and
checker receipt are in
[DELTA_MIXED_GATE_AUDIT.md](DELTA_MIXED_GATE_AUDIT.md).

## BaTiO3 screen audit

The source's coefficient mapping is conventional for `f0(P)=A P^2+B P^4+D
P^6`: `a=2A`, `b=-4B`, `c=6D`. Using its stated Table 1 choices
`B=-1.69e8`, `D=+2.37e9` gives `P_B=0.1888227 C/m^2` after imposing
coexistence. That choice corresponds to `A=3.0128e6`; with the listed slope
`3.34e5` and `T_c=381 K`, the implied temperature is about `390.02 K`, within
the thick-film Table 1 range. This numerical consistency does not resolve the
sextic sign conflict recorded in
[READ_PRIMARY_LEDGER.md](READ_PRIMARY_LEDGER.md).

For the assumed equibiaxial in-plane strain `e_xx=e_yy=e` and zero out-of-plane
stress, plane-stress elimination gives

\[
D_{bi}=C_{11}+C_{12}-2C_{12}^2/C_{11}=169.9847\,\text{GPa},\quad
C_{eff}=2D_{bi}=339.9694\,\text{GPa}.
\]

The factor two is appropriate because the scalar generalized strain represents
two equal in-plane components and the energy is written `C_eff(e-e_nat)^2/2`.
With `Q12=-0.045` and the source's zero-preload shunt model,
`u_max=2 C_eff Q12^2` (in SI this is `1.3769e9 J m^5 C^-4`). At `U=0.55b`, the
supplied arithmetic gives:

| Quantity | Conditional target |
|---|---:|
| Gate `U` | `3.718e8 J m^5 C^-4` |
| Reference/active effective stiffness `K/C_eff` | `0.3699` |
| Peak field | `2.503 MV/m` |
| Voltage over assumed 500 nm | `1.252 V` |
| Endpoint in-plane active stress | `73.6 MPa` |
| Ideal circulated work density | `0.1182 MJ/m^3` |
| Middle-stage curvature | `0.514a` |

The modulus reduction and factors are internally consistent for the stated
plane-stress idealization. A real patterned shunt, compatible strain field,
preload, domain response, fatigue, leakage, breakdown, and work recovery were
not designed or measured. These numbers are qualification targets under a
frozen coefficient choice, not achieved performance or validated device
predictions.

## Controls and prior art

The supplied package itself preserves established barrier/tilt feedback,
mechanical-boundary control of electrocaloric response, multicaloric hysteresis
cycles, higher-order coupling, and charge-controlled/negative-capacitance
methods. These remain both prior-art boundaries and strong comparators. The
matched constant-quadratic gate in the supplied script is only a narrow model
comparison: at `0.55b` it uses `1/0.5747` times the ideal circulated work of
the quartic gate but a lower peak field. It does not optimize arbitrary
charge-control, feedback, evolving constraints, or a full thermal cycle.

Astra's adjacent N774/N777 capital reinforces the proper boundary: stored
elastic work is not wall work, damping is one loss channel, direct electrical
forces can mimic structural responses, and physical claims require
same-specimen control maps and matched end-to-end energy accounting. Those
records are methodological comparators only; they do not transfer a physical
mechanism to BaTiO3. Exact routes and file hashes are in the read ledger and
manifest.

## Replay and evidence limits

- The supplied verifier was copied, then executed in the owned directory with
  its declared `numpy`, `scipy`, and `sympy` dependencies. Its assertions pass.
- Recomputed JSON matches the supplied results except
  `worst_energy_excess_over_stationary_global_minimum` in the first normalized
  path: the stored run gives `3.552713678800501e-15`; the replay gives
  `1.7763568394002505e-15`. This is a roundoff-level change, not a scientific
  discrepancy.
- The new symbolic checker passes the factorizations, elastic elimination,
  preload expansion, work identity, partial-gate threshold, finite-time ratio,
  mean-only curvature formula, and positive-kernel nonconvex countermodel. It
  reports finite-volume Laplace estimates under their written assumptions.
- The source's 1,203-point stationary-root scans and four-cell eigenvalue
  calculations are finite floating diagnostics. They are not interval
  certification, complete spatial analysis, independent scientific review, or
  physical validation.

Run commands and package versions are in `REPLAY_RECEIPT.json`. The frozen
file-size/hash inventory is `MANIFEST.json` with its own detached digest in
`MANIFEST.sha256`.
