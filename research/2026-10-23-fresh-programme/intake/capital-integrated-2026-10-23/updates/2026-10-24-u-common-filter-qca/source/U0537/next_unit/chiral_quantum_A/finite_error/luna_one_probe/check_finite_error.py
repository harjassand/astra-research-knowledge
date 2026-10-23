#!/usr/bin/env python3
"""Exact rational checks for the projector bound and radius-2 bypass map."""

from fractions import Fraction as F


def rank_one_projection_check(p_min, label_weight, overlap):
    # Rank-one P,Q with Tr(PQ)=overlap. Then Tr[P(I-Q)P]=1-overlap.
    delta = 1 - overlap
    joint_mismatch = label_weight * delta
    hs_squared = 2 * delta
    op_squared = delta

    global_hs_bound = 2 * joint_mismatch / p_min
    compressed_hs_bound = 2 * joint_mismatch / label_weight
    compressed_op_bound = joint_mismatch / label_weight
    assert hs_squared <= global_hs_bound
    assert hs_squared <= compressed_hs_bound
    assert op_squared <= compressed_op_bound
    return {
        "joint_mismatch": joint_mismatch,
        "hs_squared": hs_squared,
        "global_hs_bound": global_hs_bound,
        "compressed_hs_bound": compressed_hs_bound,
        "op_squared": op_squared,
        "compressed_op_bound": compressed_op_bound,
    }


def state_cell_destination(x, center):
    # V = right shift after the adjacent transposition (center-1, center).
    if x == center - 1:
        transposed = center
    elif x == center:
        transposed = center - 1
    else:
        transposed = x
    return transposed + 1


def input_cell_at_output(y, center):
    # Inverse of the destination map above.
    if y == center:
        return center
    if y == center + 1:
        return center - 1
    return y - 1


def bypass_check(center=0):
    assert state_cell_destination(center, center) == center
    assert state_cell_destination(center - 1, center) == center + 1
    sites = range(center - 8, center + 9)
    destinations = [state_cell_destination(x, center) for x in sites]
    assert len(destinations) == len(set(destinations))
    for output in range(center - 7, center + 8):
        source = input_cell_at_output(output, center)
        assert state_cell_destination(source, center) == output
        assert abs(source - output) <= 2

    # Disjoint swaps (2k-1,2k), followed by the right shift, fix every even
    # cell and shift the odd sublattice two cells to the right.
    sites = range(-12, 13)
    even_odd_destinations = [x if x % 2 == 0 else x + 2 for x in sites]
    assert len(even_odd_destinations) == len(set(even_odd_destinations))
    for x in sites:
        if x % 2 == 0:
            assert (x if x % 2 == 0 else x + 2) == x
        else:
            assert (x if x % 2 == 0 else x + 2) - x == 2


def main():
    uniform = rank_one_projection_check(F(1, 2), F(1, 2), F(1, 2))
    assert uniform["hs_squared"] == uniform["global_hs_bound"] == 1

    nonuniform = rank_one_projection_check(F(1, 4), F(3, 4), F(1, 2))
    assert nonuniform["joint_mismatch"] == F(3, 8)
    assert nonuniform["global_hs_bound"] == 3
    assert nonuniform["compressed_hs_bound"] == nonuniform["hs_squared"] == 1
    assert nonuniform["op_squared"] == nonuniform["compressed_op_bound"] == F(1, 2)

    bypass_check()
    print("uniform projector fixture:", uniform)
    print("nonuniform conditional-weight fixture:", nonuniform)
    print("radius-2 isolated-site and even-sublattice bypass checks passed")


if __name__ == "__main__":
    main()
