# Why a local large-memory fluctuation construction does not replace the full law

30 October 2026. Root consequence of the complementary elastic-counter
architecture. It uses only its pathwise physical-current relation and capacity,
not a guessed equilibration time or a limiting Gaussian calculation.

Let x be the real harmonic density field, J the complete signed bond current,
and z the actual per-bond elastic counters. The supplied local architecture
obeys, including any reflecting-boundary forces,

    dx=B dJ,   dz=dJ,   |z_i|<=b_N,
    (B j)_i=j_(i-1)-j_i.                                (1)

Thus x-Bz is an exact conserved vector. This is stronger than the total-counter
premise in the general locality theorem; the following conclusion applies to
this per-bond architecture and is not asserted for every local controller.

Set k=2pi/N, d=exp(ik)-1, and define the macroscopic fundamental density mode

    xi_N(t)=N^-1 sum_i exp(iki)x_i(t).

Exact continuity gives, on every path and at every actual time,

    xi_N(t)-xi_N(0)
      =(d/N)sum_i exp(iki)[z_i(t)-z_i(0)],
    |xi_N(t)-xi_N(0)|<=2b_N|d|<=4pi b_N/N.              (2)

For b_N=sqrt(N)(log N)^2, the bound tends to zero uniformly over all time,
although the corresponding fluctuation-mode allowance
sqrt(N)|xi_N(t)-xi_N(0)|<=4pi(log N)^2 diverges. There is consequently no conflict
between ordinary order-one Gaussian fluctuation evolution and a frozen
macroscopic density Fourier mode.

This separates three precision objectives:

| Objective | Consequence of this architecture |
|---|---|
| Stationary one-time visible law | May be exactly the supplied Gaussian marginal |
| Typical density fluctuation paths on N^2 time | May approach the ordinary OU path law when the prepared memory susceptibility grows |
| Order-one density-profile relaxation or complete speed-N history law | Cannot agree with ordinary heat relaxation for b_N=o(N), by (2) |

For example, an actual initial profile with a nonzero order-one fundamental
mode retains that mode up to o(1) for all times. The ordinary harmonic heat
bath changes it by a fixed fraction on physical N^2T. Even with stationary
Gaussian initialization, an event requiring an order-one change between two
specified macroscopic density modes becomes impossible for sufficiently large
N, while the ordinary Gaussian bath assigns a finite rare-history cost.
The one-time marginals can still agree because the controlled process mixes
over conserved initial x-Bz sectors.

The alternative is therefore useful for an explicitly finite-tolerance,
stationary fluctuation objective. It genuinely changes the architecture by
paying growing local capacity and prepared long-wavelength memory correlation.
It does not implement the full exclusion action or replace the shared-bit
construction's nonflat heat receiver. Conversely, the latter is not automatically
preferable when only ordinary typical observables are required. This comparison
must be made at the intended precision and actual initial-law interface.
