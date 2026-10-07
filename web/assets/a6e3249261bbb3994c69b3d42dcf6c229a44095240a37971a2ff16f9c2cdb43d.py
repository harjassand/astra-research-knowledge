"""Exact check that legal coordinate-pair stability closure does not fix squaring."""

import json

from check_coefficient_square import (
    exact_upper_half_plane_zero,
    hole_coefficients,
    rayleigh_data,
)


def main():
    f = hole_coefficients()
    auxiliary_pair = frozenset((0, 1))
    # Adding (e_0,e_1) with activity one: determinant expansion gives this.
    g = {
        holes: (value + f.get(holes | auxiliary_pair, 0)
                if holes.isdisjoint(auxiliary_pair) else value)
        for holes, value in f.items()
    }
    assert g[frozenset()] == 7
    assert g[frozenset((2, 5))] == 4
    assert g[frozenset((3, 4))] == 3
    assert g[frozenset((3, 5))] == 3
    assert g[frozenset((2, 3, 4, 5))] == 2

    values = [1, -1, -1, -1, 1, 1]
    original = rayleigh_data(g, 0, 4, values)
    squared = {holes: value * value for holes, value in g.items()}
    square = rayleigh_data(squared, 0, 4, values)
    original_delta = original[1] * original[2] - original[0] * original[3]
    square_delta = square[1] * square[2] - square[0] * square[3]
    assert original == (-14, -7, -11, -3)
    assert original_delta == 35
    assert square == (-80, -9, -25, -3)
    assert square_delta == -15
    z0, grouped, hp_coordinates = exact_upper_half_plane_zero(squared)

    print(json.dumps({
        "auxiliary_pair_zero_based": [0, 1],
        "activity": 1,
        "coefficient_update": "g(U)=f(U)+f(U union {0,1}) if U avoids {0,1}; otherwise f(U)",
        "rayleigh_pair_zero_based": [0, 4],
        "remaining_real_values": values,
        "stable_auxiliary_grouped_ABCD": original,
        "stable_auxiliary_rayleigh_difference": original_delta,
        "squared_grouped_ABCD": square,
        "squared_rayleigh_difference": square_delta,
        "squared_upper_half_plane_zero_z0": [str(z0[0]), str(z0[1])],
        "complex_grouped_ABCD": [[str(x[0]), str(x[1])] for x in grouped],
        "other_upper_half_plane_coordinates": {
            str(k): [str(v[0]), str(v[1])] for k, v in hp_coordinates.items()
        },
        "result": "legal auxiliary preserves stability; coefficientwise square does not",
    }, indent=2))


if __name__ == "__main__":
    main()
