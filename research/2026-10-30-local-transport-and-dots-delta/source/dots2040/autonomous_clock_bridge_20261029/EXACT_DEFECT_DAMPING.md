# Exact local damping of clock-exclusion and Kraus-complement defects

2026-10-29. Root derivation, pending independent review. Uses exactly the guarded channel-clock Hamiltonian and one-body reset generator in GUARDED_CHANNEL_CLOCK.md. This is stronger than assuming arbitrary physical errors remain in the clean image; they need not.

## Local positive defect operators

Recall V_x*V_x=P_x and V_x V_x* is a projector in the excited auxiliary sector Q_x. Define

    R_x = Q_x - V_x V_x* >=0,
    E_xy = Q_x Q_y    for every overlap edge xy.

R_x projects onto excited states outside the intended Stinespring image. E_xy detects forbidden simultaneous occupancy of overlapping update boxes. Both are bounded local projectors. R_x and R_y need not commute on illegal doubly occupied sectors; do not treat all defects as a joint classical record.

## Exact adjoint-generator identities

For the CLEAN finite-rate generator L:

    L*(R_x) = -kappa_x R_x,
    L*(E_xy) = -(kappa_x+kappa_y) E_xy.

Proof for R_x: its product with V_x or V_x* on either side is zero. A neighboring term H_y carries P_x in its guard, and R_x P_x=P_x R_x=0, so both H_y R_x and R_x H_y vanish. Nonneighbor terms act on disjoint data and only commuting auxiliary guards. Therefore [H,R_x]=0. Reset x sends the auxiliary to |0>, so its gain term on R_x vanishes; its total anticommutator is -kappa_x R_x. Resets elsewhere commute with R_x and cancel in gain-minus-loss.

For E_xy: H_x and H_y annihilate it because their guards require the other endpoint ready; every other H_z commutes with Q_x Q_y. Endpoint resets remove the occupancy with their respective rates, and all other resets cancel. Hence the second identity.

These are operator identities valid on the entire physical Hilbert space, including arbitrary entanglement and illegal occupancy. Thus

    Tr[R_x rho(t)] = exp(-kappa_x t) Tr[R_x rho(0)],
    Tr[E_xy rho(t)] = exp(-(kappa_x+kappa_y)t) Tr[E_xy rho(0)].

No fast-reset limit, global spectral gap, independent trajectory assumption or state-dependent condition number is used.

## Meaning and limitations

A physical error can create clock exclusion violations or complementary Kraus-label excitations, but the clean dynamics never creates these defects and damps their local weights at a size-independent rate. This supplies a real finite-memory relaxation mechanism. Data corruption caused while a defect is present is NOT undone by this identity and must count as an error in the intended correction computation. The result does not establish a joint fault-tail law or a quantum threshold.

Under an additional generator perturbation N, the exact balance is

    d Tr[R_x rho]/dt = -kappa_x Tr[R_x rho] + Tr[N*(R_x) rho],

and similarly for E_xy. A bound on the local perturbation terms touching the defect support gives a local expected defect floor. Hamiltonian/noise terms disjoint from that support contribute zero. A mean defect floor must not be misreported as a product probability bound for many fault locations.

The construction's remaining hard obligations are a threshold-compatible joint physical-noise/scheduling contract, fixed-resource two-body synthesis, and an actual finite-temperature reset/work interface. The simple expectation identities are supporting structure for those obligations, not replacements for them.
