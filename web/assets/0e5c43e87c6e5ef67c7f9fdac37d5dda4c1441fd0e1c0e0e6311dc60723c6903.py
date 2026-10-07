"""Exact six-site witness against coefficientwise-square stability closure."""

from fractions import Fraction
from itertools import combinations
import json


F = [
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0],
]
N = len(F)
V = frozenset(range(N))


def det_bareiss(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((r for r in range(k, n) if a[r][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for r in range(k + 1, n):
            for c in range(k + 1, n):
                numerator = a[r][c] * pivot - a[r][k] * a[k][c]
                assert numerator % previous == 0
                a[r][c] = numerator // previous
        for r in range(k + 1, n):
            a[r][k] = 0
        previous = pivot
    return sign * a[n - 1][n - 1]


def hole_coefficients():
    r"""f(U)=sum_{I subset V\U, |I|=|V\U|/2} det(F[I,R\I])^2."""
    out = {}
    for r_size in range(0, N + 1, 2):
        for r_tuple in combinations(range(N), r_size):
            r_set = frozenset(r_tuple)
            total = 0
            for i_tuple in combinations(r_tuple, r_size // 2):
                i_set = frozenset(i_tuple)
                j_tuple = tuple(sorted(r_set - i_set))
                minor = [[F[i][j] for j in j_tuple] for i in i_tuple]
                total += det_bareiss(minor) ** 2
            out[V - r_set] = total
    return out


def support_graph_is_connected():
    adjacency = [set() for _ in range(2 * N)]
    for i in range(N):
        for j in range(N):
            if F[i][j]:
                adjacency[i].add(N + j)
                adjacency[N + j].add(i)
    reached, stack = {0}, [0]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current] - reached:
            reached.add(neighbor)
            stack.append(neighbor)
    return len(reached) == 2 * N


def rayleigh_data(coefficients, i, j, values):
    """Return (A,B,C,D) in A+B*z_i+C*z_j+D*z_i*z_j."""
    grouped = [0, 0, 0, 0]
    for holes, coefficient in coefficients.items():
        degree = len(holes)
        sign = (-1) ** ((N - degree) // 2)
        multiplier = 1
        for k in holes - {i, j}:
            multiplier *= values[k]
        slot = (1 if i in holes else 0) + (2 if j in holes else 0)
        grouped[slot] += sign * coefficient * multiplier
    return tuple(grouped)


def gaussian_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gaussian_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gaussian_div(a, b):
    denominator = b[0] * b[0] + b[1] * b[1]
    return (
        (a[0] * b[0] + a[1] * b[1]) / denominator,
        (a[1] * b[0] - a[0] * b[1]) / denominator,
    )


def exact_upper_half_plane_zero(squared_coefficients):
    """Solve the remaining bivariate affine polynomial at exact inputs."""
    i, j = 0, 4
    epsilon = Fraction(1, 100)
    values = {
        1: (-Fraction(1), epsilon),
        2: (-Fraction(1), epsilon),
        3: (-Fraction(1), epsilon),
        5: (Fraction(1), epsilon),
        4: (Fraction(0), Fraction(1)),
    }
    grouped = [(Fraction(0), Fraction(0)) for _ in range(4)]
    for holes, coefficient in squared_coefficients.items():
        degree = len(holes)
        sign = (-1) ** ((N - degree) // 2)
        term = (Fraction(sign * coefficient), Fraction(0))
        remainder = holes - {i, j}
        for k in remainder:
            term = gaussian_mul(term, values[k])
        slot = (1 if i in holes else 0) + (2 if j in holes else 0)
        grouped[slot] = gaussian_add(grouped[slot], term)
    a, b, c, d = grouped
    z_i = gaussian_mul((-Fraction(1), Fraction(0)), gaussian_div(
        gaussian_add(a, gaussian_mul(c, values[j])),
        gaussian_add(b, gaussian_mul(d, values[j])),
    ))
    assert z_i[1] > 0
    complete_values = dict(values)
    complete_values[i] = z_i
    value = (Fraction(0), Fraction(0))
    for holes, coefficient in squared_coefficients.items():
        degree = len(holes)
        sign = (-1) ** ((N - degree) // 2)
        term = (Fraction(sign * coefficient), Fraction(0))
        for k in holes:
            term = gaussian_mul(term, complete_values[k])
        value = gaussian_add(value, term)
    assert value == (Fraction(0), Fraction(0))
    return z_i, grouped, values


def main():
    f = hole_coefficients()
    assert det_bareiss(F) == -1
    assert support_graph_is_connected()
    assert all(any(row) for row in F)
    assert all(any(F[i][j] for i in range(N)) for j in range(N))
    squared = {holes: value * value for holes, value in f.items()}
    values = [1, -1, -1, -1, 1, 1]
    original_abcd = rayleigh_data(f, 0, 4, values)
    squared_abcd = rayleigh_data(squared, 0, 4, values)
    original_delta = original_abcd[1] * original_abcd[2] - original_abcd[0] * original_abcd[3]
    squared_delta = squared_abcd[1] * squared_abcd[2] - squared_abcd[0] * squared_abcd[3]
    assert original_abcd == (-11, -7, -9, -3)
    assert original_delta == 30
    assert squared_abcd == (-55, -9, -17, -3)
    assert squared_delta == -12
    z0, complex_abcd, complex_values = exact_upper_half_plane_zero(squared)
    assert complex_abcd[1] == (-Fraction(90003, 10000), Fraction(90003, 1000000))
    assert complex_abcd[2] == (-Fraction(170009, 10000), Fraction(150007, 1000000))
    assert complex_abcd[0] == (Fraction(-22001, 400), Fraction(-3, 50))
    assert complex_abcd[3] == (Fraction(-299979999, 100000000), Fraction(30001, 500000))
    result = {
        "matrix": F,
        "matrix_determinant": -1,
        "support_graph_connected": support_graph_is_connected(),
        "nonzero_matrix_entries": sum(sum(row) for row in F),
        "hole_coefficients_by_zero_based_set": {
            "".join(map(str, sorted(holes))): value for holes, value in sorted(f.items(), key=lambda item: (len(item[0]), sorted(item[0])))
        },
        "rayleigh_pair_zero_based": [0, 4],
        "remaining_real_values": values,
        "original_grouped_coefficients_ABCD": original_abcd,
        "original_rayleigh_difference": original_delta,
        "coefficient_squared_grouped_coefficients_ABCD": squared_abcd,
        "coefficient_squared_rayleigh_difference": squared_delta,
        "coefficient_squared_upper_half_plane_zero_z0": [str(z0[0]), str(z0[1])],
        "other_upper_half_plane_coordinates": {
            str(k): [str(value[0]), str(value[1])] for k, value in complex_values.items()
        },
        "determinants_evaluated": 141,
        "arithmetic": "exact integer and rational only",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
