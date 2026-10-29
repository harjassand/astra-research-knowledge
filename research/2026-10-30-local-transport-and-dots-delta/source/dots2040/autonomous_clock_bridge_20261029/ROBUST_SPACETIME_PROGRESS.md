# Robust simultaneous progress in physical time

2026-10-29. Root extension of the independently constructed local-observability / polynomial-Lyapunov theorem. Pending review of this extension. This is a joint clock-stall theorem, not a quantum data-correction threshold.

## Required proved local certificate

For each update location x, let J_x be its recorded downward-reset CP map and K_x=L_clean*−J_x*. The local-clock derivation constructs a positive finite-support operator F_x with

    a0 I <= F_x <= b0 I,
    K_x F_x <= -r0 F_x.

The constants are explicit, positive, independent of volume, and fixed once g,kappa and overlap degree are fixed. One construction truncates the small-time integral of the no-emission effect:

    F_x = sum_{j=0}^m delta^(j+1)/(j+1)! K_x^j(I).

Its support is inside an overlap-graph ball of radius R=2m. The certified constants from the companion are a0=a/2, b0=3delta/2, r0=c/(3delta), with a=(1−exp(-kappa delta))/kappa and c the uniform single-site emission minorization at time delta. Thus C=b0/a0=3delta/a. Exact local Taylor estimates control both F and K_x F; no global-generator norm or favorable mixing promise is used.

The general physical guarded-Kraus model, not merely its legal clock subspace, is used here. Its arbitrary-state local observability proof includes illegal occupancies and dark Kraus labels; see FULL_GUARDED_KRAUS_EXTENSION.md in producer-workspace/clock_high_reset_joint_20261029. Its physical-support packing buffer is one graph unit larger than the clock-only case: centers are separated by more than4m+3 before any additional noise-range buffer.

## Local perturbations and retained environments

Let the actual generator contain additional local terms N_e(t) with N_e*(I)=0 and adjoint operator norm <=nu_e(t). The full dynamics is assumed CPTP. These may include extra nonunitary Lindblad jumps and bounded system–bath Hamiltonian interactions. Bath-only dynamics commutes with the F's and needs no norm bound. The bath may be retained and correlated; no bath tomography, Markov approximation for this additional noise, or reset of that bath is assumed.

The intended downward-reset channels J_x remain actual recorded channels of the model. Additional thermal upward jumps are noise terms; replacing the downward channels by arbitrary unknown instruments is not silently covered.

Assume finite noise interaction range and a per-box norm budget eta. State the noise budget directly as eta_R = sup_x sum_{e: physical support(e) intersects physical support(F_x)} nu_e. If converting a per-cell norm budget eta into eta_R<=eta M_R, M_R must bound the ACTUAL physical support size including data-box size and overlap multiplicity, not merely count abstract clock centers. Choose a subset S' of a marked set S with buffered F supports separated sufficiently that each clean or noise local term touches at most one F factor. Bounded-degree packing gives

    |S'| >= |S|/P,

where P is a fixed ball-volume bound at radius 2R plus the declared interaction range. This constant can be enormous; it does not grow with total system size or runtime.

## Product Lyapunov inequality

Put F=product_{x in S'} F_x. The factors have disjoint buffered supports, so they commute. Each local clean term acts on at most one factor. Consequently the no-event generator for S' satisfies

    (L_clean*−sum_{x in S'}J_x*) F <= -r0 |S'| F.

For a perturbation term touching F_x,

    N_e*(F)=(product_{y!=x}F_y) N_e*(F_x)
             <=nu_e b0 (product_{y!=x}F_y)
             <=nu_e C F.

Terms touching no factor vanish since N_e*(I)=0. Hence if

    eta_R C <= r0/2,

then the ACTUAL generator killed on S' obeys

    K_actual,S'* F <= -(r0/2)|S'| F.

Killing the additional marked channels S\S' only subtracts positive CP images of the positive operator F, so the inequality remains valid for all S. Positivity of the killed propagator and a0^|S'| I<=F<=b0^|S'| I imply

    sup_initial Pr(no recorded downward events at every x in S during t)
      <= C^|S| exp[-gamma |S| t],
    gamma = r0/(2P).

This holds for arbitrary initial system–bath states, including clock defects, under the uniform local norm budget. The time-dependent case uses the same fixed F and the positive two-parameter propagator comparison.

## Genuine space-time stall law

Fix a physical-time slab length T with p=C exp(-gamma T)<1. Call a site/slab pair stalled if there is no recorded downward event at that site during the slab. For any finite chronological collection of marked sets S_j in disjoint slabs,

    Pr(every specified site/slab pair is stalled) <= p^(sum_j |S_j|).

Reason: the one-slab effect bound holds for every conditional state, including retained bath correlations. Apply it backwards through the actual no-event record instruments. This is not multiplication of marginal probabilities and does not assume independent clock histories.

The record is the downward-emission unraveling of the specified open-system model. It need not be measured by an external observer, but the underlying reset channels are part of the physical contract. The statement differs from the earlier hypothetical repeated measurement of B_x defects: here the clock-event record already defines the implemented channel sequence.

## What is still absent

A recorded event can be a faulty channel completion if physical noise corrupted data or a lease. The theorem bounds starvation, not successful error correction. Combined with sparse bad-box bounds it removes two ideal-controller premises, but a full space-time DATA fault-path theorem and a fault-tolerant architecture using it are still required. The two-site leasing compiler is a separate construction with different clock states and must receive its own progress/defect proof; this theorem is not transferred to it by name.

Constants are deliberately conservative. This is a structural scalability result at fixed local parameters, not a practical threshold estimate or a device claim.
