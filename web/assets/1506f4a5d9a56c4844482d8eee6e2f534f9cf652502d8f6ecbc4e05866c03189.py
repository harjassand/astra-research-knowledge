#!/usr/bin/env python3
"""Exact four-site dense hard-parity precision-sensitivity fixtures."""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def determinant2(a, rows, cols):
    i, j = rows
    k, l = cols
    return a[i][k] * a[j][l] - a[i][l] * a[j][k]


def law(a):
    w = {}
    for rows in itertools.combinations(range(4), 2):
        cols = tuple(i for i in range(4) if i not in rows)
        value = determinant2(a, rows, cols)
        assert value != 0
        w[rows] = value * value
    z = sum(w.values(), Fraction())
    return z, {rows: value / z for rows, value in w.items()}


def run(precision):
    delta = Fraction(1, 1 << precision)
    h = math.factorial(4) * 65 ** 4
    eta = delta * delta / h
    c = [[0 if i == j else (i + 1) ** j for j in range(4)] for i in range(4)]
    matrices = []
    for i, j in ((0, 2), (2, 0)):
        a = [[Fraction(i0 != j0) + eta * c[i0][j0]
              for j0 in range(4)] for i0 in range(4)]
        a[i][j] += delta
        matrices.append(a)
    z_plus, plus = law(matrices[0])
    z_minus, minus = law(matrices[1])
    tv = sum(abs(plus[x] - minus[x]) for x in plus) / 2
    lower = 1 - 3 * delta * delta / (1 - delta) ** 2
    assert tv >= lower
    a_support = {(0, 1), (0, 3)}
    assert sum(plus[x] for x in a_support) >= 1 - 2 * delta * delta / (1 - delta) ** 2
    assert sum(minus[x] for x in a_support) <= delta * delta / (1 - delta) ** 2
    for z in (z_plus, z_minus):
        assert 2 * delta * delta * (1 - delta) ** 2 <= z
        assert z <= 2 * delta * delta * (1 + delta) ** 2 + 4 * delta ** 4
    for a in matrices:
        assert all(a[i][i] == 0 for i in range(4))
        assert all(a[i][j] > 0 for i in range(4) for j in range(4) if i != j)
    # This rational norm bound certifies condition number <4 without float SVD.
    b = delta + delta * delta
    condition = (3 + b) / (1 - b)
    assert condition < 4
    return {
        "L": precision, "all_six_states_positive": True,
        "delta_operator_distance_exact": str(delta),
        "TV_exact": str(tv), "TV_decimal_diagnostic": float(tv),
        "TV_lower_bound_exact": str(lower),
        "norm_plus_exact": str(z_plus), "norm_minus_exact": str(z_minus),
        "condition_number_certificate": str(condition),
    }


def symmetric_run(precision):
    delta = Fraction(1, 1 << precision)
    matrices = []
    # The three opposite-edge products are exactly x,y,z since edges
    # 23,13,12 stay equal to one. Symmetric entries describe spin-singlet F.
    products = (
        (1 + delta ** 2, 1 + delta + 2 * delta ** 2, 1 - delta + 3 * delta ** 2),
        (1 + delta + delta ** 2, 1 + 2 * delta ** 2, 1 + 3 * delta ** 2),
    )
    for x, y, z in products:
        a = [[Fraction(i != j) for j in range(4)] for i in range(4)]
        for j, entry in ((1, x), (2, y), (3, z)):
            a[0][j] = a[j][0] = entry
        matrices.append(a)
    z_v, v = law(matrices[0])
    z_u, u = law(matrices[1])
    assert z_v == 12 * delta ** 2 * (1 - delta + delta ** 2)
    assert z_u == 4 * delta ** 2 * (1 - 3 * delta + 3 * delta ** 2)
    norm_ratio = z_v / z_u
    assert 3 < norm_ratio < 4
    tv = sum(abs(v[x] - u[x]) for x in v) / 2
    tv_lower = (2 - delta) ** 2 / (6 * (1 - delta + delta ** 2)) - delta ** 2 / (2 * (1 - 3 * delta + 3 * delta ** 2))
    assert tv == tv_lower
    assert tv > Fraction(3, 5)
    # Perturbations are symmetric stars, with norm <= sum of edge magnitudes.
    for a in matrices:
        perturbation_bound = sum(abs(a[0][j] - 1) for j in (1, 2, 3))
        assert perturbation_bound <= 2 * delta
        assert (3 + perturbation_bound) / (1 - perturbation_bound) < 4
    return {
        "L": precision, "symmetric_spin_singlet_F": True,
        "all_six_states_positive": True,
        "operator_distance_exact": "sqrt(3)*" + str(delta),
        "entrywise_relative_distance_upper": str(2 * delta),
        "TV_exact": str(tv), "TV_decimal_diagnostic": float(tv),
        "TV_greater_than_3_over_5": True,
        "norm_v_exact": str(z_v), "norm_u_exact": str(z_u),
        "norm_ratio_exact": str(norm_ratio),
        "condition_number_upper": "25/7",
    }


def main():
    fixtures = [run(precision) for precision in (4, 8, 16, 32)]
    symmetric = [symmetric_run(precision) for precision in (4, 8, 16, 32)]
    result = {"scope": "Exact rational finite checks, not approximate hardness",
              "all_assertions_passed": True, "fixtures": fixtures,
              "symmetric_fixtures": symmetric}
    Path(__file__).with_name("precision_barrier_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"cases": len(fixtures) + len(symmetric), "all_assertions_passed": True,
                      "min_symmetric_TV_decimal_diagnostic": min(x["TV_decimal_diagnostic"] for x in symmetric)}))


if __name__ == "__main__":
    main()
