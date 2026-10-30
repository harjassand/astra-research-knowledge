# Clean DATA charging survives animal-local noncommuting activity weights
2026-10-30. New lemma candidate addressing the DATA-weighting gap in the weak-initiation branch. It does not yet compose the useful-service credit or prove a native threshold.

## Circuit choice and bounded-extension comparison
For each animal A let U(A) be the union of fixed-radius anchor neighborhoods of its vertices, and let E(A) be a bounded-degree selected pair set induced by these anchors. Use ONE global coloring/order of the local activity-gate supports. Define

    Y_A=ordered product_{g selected by A} exp(delta X_g),
    G_A=Y_A^dagger Y_A,

where the pair generators have fixed bounded norm and the singleton generators include the prescribed epsilon^2 factor. All gates are strictly positive and invertible. On the clean forest range these are controller-only operators, commuting DATA and the actual activity projections.

If B=A union D and |D|<=k with D in a bounded patch, the selected gate lists differ in O(1) gates. In the quotient Y_B Y_A^{-1}, all common gates outside the finite-depth causal cone of these differences cancel. Only O(1) bounded-norm gates and inverses remain. Thus, uniformly in A and system size,

    ||Y_B Y_A^{-1}||, ||Y_A Y_B^{-1}|| <= exp(C delta),
    exp(-2C delta) G_A <= G_B <= exp(2C delta) G_A.       (1)

This is a relative congruence bound, not the false assertion that products of noncommuting positive factors are order-monotone. The gate-order/color choice must be independent of A. Anchor selection must have bounded change under adjoining one local D; arbitrary animal-dependent gate choices are not covered.

## Exact clean reset-DATA decomposition
On the clean legal forest range, an actual terminal instrument factors into its controller jump J_j and the fixed deterministic-syndrome map Phi_j. Define the scalar controller generator L_c by replacing that DATA channel by identity, retaining every actual clock/lock/monitor operator. For f_A DATA-diagonal,

    L_phys^*(f_A G_A)
      = f_A L_c^*G_A
        +sum_j J_j^dagger G_A J_j (Phi_j^*f_A-f_A).      (2)

Summed workspace outcomes are complete; no independent schedule is inferred. The clean controller-only assertion is NOT extended to malformed masks here.

## Operator-valued full-animal completion
Fix a source raw syndrome s and an accepted j move with changed vertex set D_j. Put W_{j,A}=J_j^dagger G_A J_j>=0. Equation (1) and positivity imply, for B=A union D_j,

    W_{j,A}<=exp(2C delta)W_{j,B}.                      (3)

The original scalar completion proof gives

    f_B(pre)>=R_move f_A(post)

for every increasing animal A, while each B containing D_j loses at least (1-theta)f_B(pre). There are at most 2^k increasing preimages. Hence if

    R_move >= 2^(k+1) exp(2C delta)/(1-theta),

the positive contributions to

    sum_A W_{j,A}[f_A(post)-f_A(pre)]

consume at most half the negative D_j-containing charge, in LOEWNER order. Therefore

    sum_A W_{j,A}(Phi_j^*f_A-f_A)
      <= -(1-theta)/2 sum_{B: D_j subset B} W_{j,B}f_B(pre)
      <=0.                                           (4)

All weights in (3) are controller operators and commute the raw syndrome projectors. Thus the blockwise argument gives a full clean-range operator inequality, not a classicalization of controller states. Idempotence is not needed for this charging lemma; deterministic accepted syndrome moves and the original per-move decrease suffice.

The extra exp(2C delta) is a fixed local factor, absorbed by the same choice of sufficiently small theta and c sufficiently near one. No |A|^2 factor appears.

## DATA-weighted activity drift
Suppose the actual scalar clean-controller calculation earns

    L_c^*G_A <= [-a delta A0 epsilon^2 sum_{h in U(A)}P_h
                 -b delta B0 sum_{e in E(A)}P_e
                 +C delta A0 epsilon^4 |U(A)| I] G_A.

The activity projections commute G_A and DATA. Multiply by f_A, sum, and use (2)-(4). Since |U(A)|<=C_U|A|, the resulting DATA-weighted inequality has negative weighted singleton/pair activity charges, positive idle source at most C' delta epsilon^4 sum_A |A| f_A G_A, and the retained negative DATA-reset charge (4).

This supplies the previously missing justification for DATA-weighting the multiplicative activity hierarchy on the clean range. It does NOT justify multiplying an arbitrary controller inequality by an animal with no circuit-comparison condition, nor does it solve dirty-sector extension or useful recovery service during all-idle phases.
