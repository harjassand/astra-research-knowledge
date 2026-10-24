# Distributed-rod replay of the positive nonlocal kernel

Bounded numerical continuation, 24 October 2026. This tests the specified
kernel after replacing each massless spring by a uniform axial rod. It is an
ideal periodic graph calculation, not a packed specimen or hardware result.

## Construction and normalization

For each N = 2, 4, 8, 16, 32, use positive springs

\[
\kappa_n=K\frac{12(N-n)}{N^2(N^2-1)},\qquad n=1,\ldots,N-1.
\]

The replay checks numerically that `sum(n^2 kappa_n)/K = 1` for every N.
Each n-cell link is an actual distributed axial rod of length `n*a`, with

\[
EA_n=\kappa_n na,\qquad c^2=E/\rho,qquad
m_{\rm rod,cell}=\sum_n\frac{\kappa_n(na)^2}{c^2}=\frac{Ka^2}{c^2}.
\]

The total mass per cell is fixed to `Mtot`, with connector mass
fraction `r=K*a^2/(Mtot*c^2)=0.1` and point mass
`M=0.9*Mtot>0`. Thus all rod cross-sections are positive, their full
longitudinal fields are included, and the connector mass is not silently
discarded.

At `T=100 mK`, I set

\[
\eta=\omega_u a/c=0.08,\quad \omega_u=2k_BT/\hbar,
\quad c=5000\,\mathrm{m/s},
\quad a=15.2765\,\mathrm{nm}.
\]

Only the ratios `r, eta` affect the dimensionless result. This scale puts
long-rod standing-wave poles inside the thermal range: the first pole of the
longest rod is at `u=omega/omega_u=39.27, 13.09, 5.61, 2.618, 1.267` for
N=2, 4, 8, 16, 32 respectively. At cutoff `u=15`, there are 0, 1, 6, 27,
and 117 distinct pole locations below the cutoff.

## Counting all propagating crossings

For each frequency away from the isolated rod poles, I form the degree-
at-most-`N-1` Chebyshev polynomial in `x=cos(q)` from

\[
D(\omega,q)=-M\omega^2+2\sum_{n=1}^{N-1}\kappa_n\theta_n
\frac{\cos\theta_n-\cos(nq)}{\sin\theta_n},
\quad \theta_n=\omega na/c.
\]

At each integration sample the code solves for every polynomial root, counts
each simple real root in `(-1,1)`, and use that as the right-moving channel
count. Each x root corresponds to the `q=+/- arccos(x)` pair, of which one
has positive group velocity. This counts all crossings rather than taking a
union of passbands. The observed maximum count was `N-1` for every N, as the
polynomial-degree bound predicts. Selected root counts agreed with dense direct sign-change checks in q across
25 selected (N, alpha) cases using 65,537 q points each. For N=2, the computed
J matched the separately reduced degree-one local-rod formula exactly on the
same grid.

The infinite integral is truncated at `u=15`, with
`J = integral g(u) N_ch(u) du` and `g(u)=(u/sinh(u))^2`. Since
`Nch<=N-1` away from poles, the remaining tail is at most
`(N-1)*4.5011e-11`. The eliminated-rod equation is singular at exact pole
frequencies. Compatible node-bearing modes can exist there; the pole set is
discrete and has zero measure in the frequency integral, so the off-pole
channel count suffices for this integral.

## Finite numerical comparison

The point-spring reference places all `Mtot` at each site and uses
the same `K, a, c, T` and `Keff=K`, but treats connectors as massless. It is
a same-total-mass reference, not the limit of the distributed-rod family at
fixed point mass `Mpoint`.
The local-rod reference uses only n=1 with stiffness K, the same total mass,
the same `a/c`, and the same 10% connector-mass fraction. The thermal
integrals were computed for the full distributed-rod model using midpoint
frequency grids; the table reports the finest grid and observed refinement
range (not a rigorous error bar).

| N | Distributed rods J, finest grid | Observed grid range | Same-total-mass point-spring Fejér reference J | Max channels observed |
|---:|---:|---:|---:|---:|
| 2 | 1.64492224 | 1.64492224–1.64492224 | 1.64491480 | 1 |
| 4 | 1.63494229 | 1.63494229–1.63494502 | 1.62933646 | 3 |
| 8 | 1.40335784 | 1.40335784–1.40343393 | 1.37190307 | 7 |
| 16 | 0.95670970 | 0.95670970–0.95702280 | 0.85854872 | 15 |
| 32 | 1.00797605 | 1.00551617–1.01119658 | 0.45893876 | 31 |

The local n=1 rod gives `J=1.64492224`, essentially the one-channel
blackbody value `pi^2/6` at this thermal scale. The point-spring sequence
falls strongly with N, but the distributed-rod values do not follow that
monotone trend: N=32 is about 1.008, substantially above its same-total-mass
point-spring reference about 0.459. Even so, the finite N=16 and N=32 rod
fixtures are below the local-rod reference in this selected dimensionless
setting. The (N=32) result is visibly less resolved than the smaller cases;
the finest-grid value is a bounded numerical indication, not a certified
integral or an asymptotic law.

## What this does and does not establish

The replay realizes the spring kernel with distributed connector inertia and
counts the resulting multiple propagating branches through the secular
polynomial. It shows that those branches materially change the finite-N
integral, especially by N=32, while leaving a finite suppression relative to
the local-rod comparator in this one dimensionless parameter setting. It does
not prove a continuum N-limit, robust performance over (r,\eta), a physical
packing/route for all overlapping nonlocal rods, a measured material model, or
a device advantage. The abstract line graph assumes ideal attachment of every
long rod and omits transverse modes, junction scattering, loss, and geometry
constraints.

Replay: `nonlocal_distributed_rods.py`. Full JSON output, including all grid
refinements and per-N mass/stiffness checks: `nonlocal_distributed_rods_results.json`.
