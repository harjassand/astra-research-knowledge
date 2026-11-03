# An acquired joint operation on arbitrary finite pair-transfer graphs

This records the structural content of HOT_MAJORITY_COMMON_CLEANUP.md,
rather than treating the two-port diagnostic as the destination. It is a
complete stopped operation on the stated faces, not a global recurrence
principle or a theorem for arbitrary weakly reversible lists.

## Raw family

Take m finite ordered C3 blocks on DISJOINT triples (A_i,B_i,C_i), with
complexes 0,A_i+B_i,2A_i+B_i+C_i,3A_i+2B_i+2C_i and arbitrary positive
block constants. Add ANY finite directed pair-transfer graph of reactions

    A_i+A_j+2B_i+2C_i -> A_i+A_j+2B_j+2C_j,

with arbitrary positive fixed constants on present edges. No uniform
mixing, invariant fiber or common complex balance is supplied. Core
reversibility is not needed for this LOCAL operation; full weak
reversibility remains the intended global programme.

For every fixed H there are raw eps>0,n0 such that all inputs with

    A_i<=H,
    n=min_i(B_i-C_i)>=n0,
    sum_i C_i<=eps n                                  (1)

admit an actual stopping episode paying

    E[ sigma+J_nc(sigma)+Z(X_sigma)^2 ]<=Z(x)^2,
    Z=7m+1+M-sum_i mcap(A_i),
    mcap=(0,2,4,7,7,...).                              (2)

All majority ratios can be arbitrary. All m minority inventories can
diverge and exchange packets simultaneously. This is not another fixed
landing controller: each actual source and conservative output is live
and included in the stop or its halo.

## The operation, acquired from the list

Use the explicit one-port progress f in equation(1) of
HOT_MAJORITY_COMMON_CLEANUP.md and sum it over ports. Let

    N=m(3H+4), h=H+N+1.

Continue nonzero block events only when their own terminal is disabled;
continue every terminal, and continue every core transfer from a donor
with anchor<=2. Stop at any other event with its ACTUAL output. Success
means all anchors are zero.

The acquired f table gives:

* each continuing noncore event lowers total f by at least1;
* each continuing core event is nonincreasing, since the low donor is
  packet-periodic and every receiving packet is nonincreasing;
* total f<=N initially and each anchor remains <=h;
* before the stop every majority difference stays >=n/2 for n>=4(N+1).

Thus J_nc<=N+1 and E cleanup_time<=C/n. On every actual failure the mass
overrun is bounded by a raw b_m,H, because only N+1 block events can occur
and all core events conserve M.

For EACH present core edge with high donor,

    core_rate/terminal_rate_i
       =kappa_ij*A_j/[alpha_i3*(A_i-1)*(A_i-2)].

The raw head h and finite edge list therefore acquire

    R_high<=K T,
    K=(h/2)*max_i sum_(i->j) kappa_ij/alpha_i3.           (3)

The complete ready-growth hazards satisfy G_ready<=C/n*T by the same
explicit falling-factorial divisions. Every source0 is a failure with
total constant hazard B0=sum_i alpha_i0.

The bounded success subsolution p^(sum f_i), p=1/(K+2), yields

    P(cleanup success)>=p^N-B0 E cleanup_time
                          >=delta_m,H>0.               (4)

This is the same optional-stopping proof as the two-port construction;
the only extra operation is summing a finite raw directed edge list.
No graph-connectivity, spectral or receiving assumption is hidden in (4).
Local nonexplosion before this stop follows directly from its population
cap, even if a larger unproved network has not yet been shown nonexplosive.

On success all anchors are zero. Execute the acquired isolated activation
trials, stopping immediately when any other port is activated or an own
unexpected source fires. Until that actual interruption all other anchor
catalysts are zero, so EVERY core rate really vanishes. Each full trial
is neutral or deletes one majority molecule, with

    P(good)>=c/(1+sum C_i), P(interrupt)<=C/n,
    E time<=C, J_nc<=4.                                (5)

Run K0(1+sum C_i) trials or the deletion guard/first interruption. Choose
K0 to repay b_m,H even after the success probability (4), then eps small
and n0 large. The exact squared-mass calculation in the governing
two-port proof gives (2). No condition on the largest majority is used.

## The reusable design rule

The enabling step is not a bare path to a finite set. It is a RAW integer
progress with an acquired conservative packet transport law. Conservative
moves that violate progress may be stopped as complete failure outputs
when their actual hazards are bounded by progress-producing terminal
hazards. A bounded p^f subsolution then earns a population-uniform success
chance. Bounded failure cost can be repaid by actual deletion trials at
the SAME globally defined quantity, while physical residence and competing
inputs are retained.

This gives a concrete, checkable structural operation beyond a single
ordered source chain: many simultaneously evolving activation debts on
an arbitrary finite pair-transfer graph. It does NOT assert that every
weakly reversible graph has such an f, packet rule or deletion experiment.
The negative-sign neutral cycle in JOINT_NORMAL_RESOURCE_CAP.md proves
that strict f is not automatic even within this family.

## A second global-coordinate operation from the same raw family

The functions w,v in JOINT_NORMAL_RESOURCE_CAP.md can likewise be summed
over any finite number of these ports. Low-donor transfers conserve both
hidden totals and cannot increase receiver corrections. The actual normal
policy therefore has

    M_t<=M_in+C_m,H

up to EVERY failure output, without any sign/scale premise and without a
bound on the number of neutral noncore cycles. The two-genuine-event
failure path and degree-seven raw rate bound acquire physical and genuine
activity moments O((1+M_in)^(14r)). The complete finite killed operator
exists and can be enumerated per input.

Again, the output can carry a new debt. The finite operator and bounded
population loan do not earn an inward sign or a normalized invariant law.
The full scientific consequence still requires global coverage and
compatibility, especially for neutral negative/mixed faces. These are
live obligations, not assumptions of (2).
