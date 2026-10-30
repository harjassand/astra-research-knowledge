# A dormant-return edge gains an inverse-A power
Status: personal local derivation, unreviewed. No full boundary-cycle closure is claimed.

Use the triangle and paired reserve profiles of TWO_COORDINATE_BRANCHING_PROFILE_CANDIDATE.md. For s>0, consider the actual subkernel that hits D=0 BEFORE clearing or any connector birth, starting with D>0. Its only exit channel is A'+D->2A' at d=1, so its operational rate is k_back a and it increases physical A by1.

The claim is stronger than an unweighted small return probability:

    E[(1+A_exit)^-s ; hit D=0 first]
       <=C_s (1+A_initial)^-(s+1).                    (GAIN)

## Killed-generator proof
Take a sufficiently large multiple F of the paired profile at exponent s+1:

    F=M[C1 f_(s+1)(A)+C2 f_(s+1)(A+eta C)].

Its linear-in-D generator is nonpositive by the earned reserve construction. Its nonlinear seed contribution is <=C aF. Clearing subtracts k_D(a)_2F. Stop at D=0 and add the boundary reward f_s(A+1). The extra positive forcing is at most

    k_back a 1_{d=1} f_s(A+1).

For large a this is <=C a^2 f_(s+1)(A). Choose M so the clearing's negative term dominates this forcing as well as the lower-order seed contribution. For bounded a and large n, the paired linear drift is negative of order n on active D>0 states, as proved in the preceding profile construction; it dominates the bounded boundary forcing. Thus the killed-generator plus boundary-reward inequality is nonpositive for all sufficiently large n. Small active n are covered by enlarging constants.

Optional stopping gives (GAIN). Restoring the common physical clock multiplies all fast/clearing/D-exit terms by the same positive factor. Connector births merely stop the kernel earlier, so the inequality applies to the actual first-event subkernel without an averaging premise.

## Why this matters for the full operator
Low-phase immigration races already consume one inverse-A power. The dormant-return edge now also consumes one power, rather than costing only a worst-case scalar return probability. Consequently a phase-dependent profile budget can survive a visit to a NON-small dormant block if that block preserves incoming inverse moments. This is more informative than replacing its entire output by p0(N), and is the natural quantity to compose through the whole boundary cycle.

The full exponential-residual Green of the dormant block and its phase-indexed positive drift still require an exact construction. (GAIN) is not that construction, and no full recurrence upgrade is inferred here.
