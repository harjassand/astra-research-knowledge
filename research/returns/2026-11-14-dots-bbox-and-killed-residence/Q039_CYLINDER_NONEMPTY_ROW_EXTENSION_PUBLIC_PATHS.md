# Cylinder reconstruction extension below the critical strip width

Creative's full cylinder bound uses widthw, vertical periodL1600, minus horizontal exterior, and relative energy against the completely filled strip. For row subset S, let r(S) be its number of occupied intervals and
D_S=exp[−16(r(S)−1)−.04(w−|S|)].
The vertical kernel K_ST=exp[−8|SΔT|] is the restriction of the tensor product of [[1,t],[t,1]], t=e^-8. It is positive semidefinite, with norm at most(1+t)^w.

For unrestricted rows, D_empty≤1 requiresw≥400. But if EVERY ROW IS NONEMPTY, then r(S)≥1 and D_S≤1 for everyw≥1. Restricting the kernel to nonempty rowstates preserves positive semidefiniteness and cannot increase its norm. Therefore the same transfer-matrix trace argument yields
Z_nonempty-rows / w(full strip) ≤e16(1+e^-8)^(wL+1).
Forw≤800 this has logarithm below446.

This class permits arbitrarily many intervals per row, separated neighboring intervals, internal holes and all patterns satisfying the nonempty-row condition. No single-interval approximation is made. A vertically winding component contained inside the strip necessarily occupies every row, so its configurations belong to this class. The bound can consequently support weighted preimages below width400 when that winding condition is genuinely preserved by the reconstruction.

This does NOT cover an arbitrary winding component that cannot be contained in the strip (for example a diagonally winding path spanning the whole horizontal torus), nor does it prove a native growth time or a complete path-congestion assignment. The horizontal minus boundary, vertical periodicity, and standalone Gibbs reconstruction interpretation must be maintained.
