"""Exact 4x4 determinant check for a failed local-comparability transfer."""

from fractions import Fraction
import json


def det2(rows, cols, matrix):
    a, b = rows
    c, d = cols
    return matrix[a][c] * matrix[b][d] - matrix[a][d] * matrix[b][c]


def main():
    rows_initial = ((0, 1), (2, 3))
    cols_initial = ((2, 3), (0, 1))
    rows_switched = ((0, 2), (1, 3))
    cols_switched = ((1, 3), (0, 2))
    samples = []
    for bits in (1, 4, 8, 16):
        delta = Fraction(1, 2**bits)
        F = [
            [0, delta, 1, 0],
            [delta, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ]
        initial = [det2(I, J, F) for I, J in zip(rows_initial, cols_initial)]
        switched = [det2(I, J, F) for I, J in zip(rows_switched, cols_switched)]
        ratio = (switched[0] ** 2 * switched[1] ** 2) / (
            initial[0] ** 2 * initial[1] ** 2
        )
        assert initial == [1, 1]
        assert switched == [delta, delta]
        assert ratio == delta**4 == Fraction(1, 2 ** (4 * bits))
        samples.append({
            "delta": f"1/2^{bits}",
            "initial_amplitudes": [str(x) for x in initial],
            "switched_amplitudes": [str(x) for x in switched],
            "pair_weight_ratio": str(ratio),
        })

    print(json.dumps({
        "matrix_family": "[[0,d,1,0],[d,0,0,1],[1,0,0,1],[0,1,1,0]]",
        "initial_partitions": [[0, 1], [2, 3]],
        "switched_partitions": [[0, 2], [1, 3]],
        "union_preserved": True,
        "symbolic_pair_weight_ratio": "delta^4",
        "samples": samples,
    }, indent=2))


if __name__ == "__main__":
    main()
