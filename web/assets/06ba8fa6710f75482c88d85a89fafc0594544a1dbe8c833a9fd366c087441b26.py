#!/usr/bin/env python3
"""Finite check for a full-support hybrid code on a non-group Latin square.

The code combines a binary linear syndrome for an embedded 2x2 intercalate
with conditional Slepian-Wolf binning of the rare exception symbols.
"""

from collections import defaultdict
from math import log2


LATIN = (
    (2, 0, 3, 1, 4),
    (3, 1, 4, 0, 2),
    (4, 2, 0, 3, 1),
    (1, 3, 2, 4, 0),
    (0, 4, 1, 2, 3),
)
Q = 5
EPSILON = 0.001
BASE = {
    (0, 1): 0.45,
    (0, 3): 0.05,
    (1, 1): 0.05,
    (1, 3): 0.45,
}


def entropy(probabilities):
    return -sum(p * log2(p) for p in probabilities if p > 0.0)


def main():
    # The selected subtable is the XOR intercalate [[0,1],[1,0]].
    assert ((LATIN[0][1], LATIN[0][3]), (LATIN[1][1], LATIN[1][3])) == ((0, 1), (1, 0))

    epsilon = EPSILON
    joint = {}
    joint_d_tx_ty = defaultdict(float)
    p_d = defaultdict(float)
    p_tx_ty = defaultdict(float)
    for x in range(Q):
        for y in range(Q):
            p = (1.0 - epsilon) * BASE.get((x, y), 0.0) + epsilon / (Q * Q)
            joint[x, y] = p
            alpha = 1 if x == 1 else 0
            beta = 1 if y == 3 else 0
            d = alpha ^ beta
            tx = "*" if x in (0, 1) else str(x)
            ty = "*" if y in (1, 3) else str(y)
            joint_d_tx_ty[d, tx, ty] += p
            p_d[d] += p
            p_tx_ty[tx, ty] += p

    assert all(p > 0.0 for p in joint.values())
    px = [sum(joint[x, y] for y in range(Q)) for x in range(Q)]
    wy = [[joint[x, y] / px[x] for y in range(Q)] for x in range(Q)]
    wz_mass = [[0.0 for _ in range(Q)] for _ in range(Q)]
    for x in range(Q):
        for y in range(Q):
            wz_mass[x][LATIN[x][y]] += joint[x, y]
    wz = [[wz_mass[x][z] / px[x] for z in range(Q)] for x in range(Q)]
    # A common output permutation preserves whether two input rows agree.
    # Here W_Z(.|0)=W_Z(.|1) but W_Y(.|0) != W_Y(.|1).
    assert wz[0] == wz[1] and wy[0] != wy[1]
    h_xy = entropy(joint.values())
    h_d = entropy(p_d.values())
    h_tx_ty = entropy(p_tx_ty.values())
    h_d_tx_ty = entropy(joint_d_tx_ty.values())
    h_tx_ty_given_d = entropy(joint_d_tx_ty.values()) - h_d
    h_d_given_tx_ty = h_d_tx_ty - h_tx_ty
    code_sum_d_first = 2.0 * h_d + h_tx_ty_given_d
    code_sum_flags_first = h_tx_ty + 2.0 * h_d_given_tx_ty

    # Exact one-sided envelope converse: reduce the q=5 posterior to its
    # selected-row mass s, then use convexity of psi on [0,c].
    selected_mass = 1.0 - 3.0 * epsilon / 5.0
    c = (1.0 - epsilon) / selected_mass
    t = c
    u_y = 0.2 + 0.3 * t
    u_z0 = 0.2 + 0.7 * t
    u_z1 = 0.2 - 0.1 * t
    psi_c = entropy((u_y, u_y, 0.2 - 0.2 * t, 0.2 - 0.2 * t, 0.2 - 0.2 * t)) - entropy(
        (u_z0, u_z1, 0.2 - 0.2 * t, 0.2 - 0.2 * t, 0.2 - 0.2 * t)
    )
    envelope = selected_mass * psi_c
    outer_sum = h_xy - envelope

    p_both_selected = sum(joint[x, y] for x in (0, 1) for y in (1, 3))
    p_d_one_both_selected = sum(
        joint[x, y]
        for x, y in ((0, 3), (1, 1))
    )
    q = p_d_one_both_selected / p_both_selected
    gap_from_exception_mass = 12.0 * epsilon / 25.0
    assert abs((code_sum_flags_first - outer_sum) - gap_from_exception_mass) < 1e-12

    # For t in [0,1], ln(2)*psi''(t) is
    # -64/(5*(t-2)*(3*t+2)*(7*t+2)) > 0.
    min_curvature = min(
        -64.0 / (5.0 * (v - 2.0) * (3.0 * v + 2.0) * (7.0 * v + 2.0))
        for v in (0.0, c)
    )
    assert min_curvature > 0

    print("selected 2x2 table:", ((0, 1), (1, 0)))
    print("full support:", all(p > 0.0 for p in joint.values()))
    print("W_Y and W_Z output-permutation equivalent:", False)
    print(f"epsilon={epsilon}")
    print(f"H(D)={h_d:.12f}")
    print(f"H(T_X,T_Y)={h_tx_ty:.12f}")
    print(f"H(T_X,T_Y|D)={h_tx_ty_given_d:.12f}")
    print(f"H(D|T_X,T_Y)={h_d_given_tx_ty:.12f}")
    print(f"D-first hybrid sum rate={code_sum_d_first:.12f}")
    print(f"flags-first hybrid sum rate={code_sum_flags_first:.12f}")
    print(f"Slepian-Wolf sum={h_xy:.12f}")
    print(f"improvement over SW={h_xy-code_sum_flags_first:.12f}")
    print(f"one-sided converse sum lower bound={outer_sum:.12f}")
    print(f"remaining code/converse gap={code_sum_flags_first-outer_sum:.12f}")
    print(f"both-selected mass={p_both_selected:.12f}; q={q:.12f}")
    print(f"one-sided exception mass={gap_from_exception_mass:.12f}")
    print(f"minimum psi curvature factor={min_curvature:.12f}")


if __name__ == "__main__":
    main()
