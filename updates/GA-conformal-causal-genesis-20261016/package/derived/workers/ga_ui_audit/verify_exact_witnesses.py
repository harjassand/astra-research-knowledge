#!/usr/bin/env python3
"""Independent exact rational Fourier checks for the 15-dimensional criterion.

No optimizer, external package, or constructing-worker artifact is imported.
The analytic interpolation and uniform-integrability arguments are in REPORT.md.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


OUT = Path(__file__).resolve().parent
CHECKS = []


def check(name, obtained, expected):
    if obtained != expected:
        raise RuntimeError(f"{name}: obtained {obtained!r}, expected {expected!r}")
    CHECKS.append(name)


def cosine(terms):
    ans = {}
    for x, y, amplitude in terms:
        amplitude = F(amplitude)
        for key in ((x, y), (-x, -y)):
            ans[key] = ans.get(key, F(0)) + amplitude / 2
    return {key: value for key, value in ans.items() if value}


def add(*fields):
    ans = {}
    for field in fields:
        for key, value in field.items():
            ans[key] = ans.get(key, F(0)) + value
    return {key: value for key, value in ans.items() if value}


def scale(field, factor):
    return {key: value * factor for key, value in field.items() if value * factor}


def mul(left, right):
    ans = {}
    for (lx, ly), lv in left.items():
        for (rx, ry), rv in right.items():
            key = (lx + rx, ly + ry)
            ans[key] = ans.get(key, F(0)) + lv * rv
    return {key: value for key, value in ans.items() if value}


def average(*fields):
    ans = {(0, 0): F(1)}
    for field in fields:
        ans = mul(ans, field)
    return ans.get((0, 0), F(0))


def second(field, xx, yy):
    return {key: -value * key[0] ** xx * key[1] ** yy
            for key, value in field.items()
            if value * key[0] ** xx * key[1] ** yy}


def frac(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def cubic_moments(a, b, c, q):
    fields = [a, b, c, q]
    result = []
    for i, j, k, ell in product(range(4), repeat=4):
        if i + j + k + ell != 3:
            continue
        powers = (i, j, k, ell)
        fs = [field for field, exponent in zip(fields, powers)
              for _ in range(exponent)]
        result.append({"powers_a_b_c_q": list(powers),
                       "base_average": frac(average(*fs))})
    check("twenty homogeneous cubic monomials", len(result), 20)
    return result


def stream_record(name, terms, expected):
    psi = cosine(terms)
    x = second(psi, 2, 0)
    a = second(psi, 1, 1)
    b = second(psi, 0, 2)
    observed = {
        "B3": average(b, b, b),
        "AB2": average(a, b, b),
        "XB2": average(x, b, b),
        "A2B": average(a, a, b),
        "X2": average(x, x),
    }
    for key, value in expected.items():
        check(name + ":" + key, observed[key], F(value))

    # At Fourier mode (kx,ky), partial_y(a)=partial_x(b), and
    # partial_y(c)=partial_x(d) after evaluation at (x,Ny).
    keys = set(x) | set(a) | set(b)
    for kx, ky in keys:
        check(name + ":first-row compatibility:" + str((kx, ky)),
              ky * a.get((kx, ky), F(0)), kx * b.get((kx, ky), F(0)))
        check(name + ":second-row compatibility:" + str((kx, ky)),
              ky * x.get((kx, ky), F(0)), kx * a.get((kx, ky), F(0)))

    moments = cubic_moments(a, b, x, {})
    for item in moments:
        i, j, k, ell = item["powers_a_b_c_q"]
        item["actual_average"] = {
            "rational_multiplier": frac(F(item.pop("base_average")) * (-1) ** k),
            "sigma_power": k,
            "N_inverse_power": i + 2 * k,
        }
    return {
        "name": name,
        "psi_cosine_terms": [
            {"frequency": [xx, yy], "amplitude": frac(F(amplitude))}
            for xx, yy, amplitude in terms
        ],
        "map": "f_N=N^-1 psi_y(x,Ny); g_N=-sigma N^-2 psi_x(x,Ny)",
        "coordinates": "a=N^-1 A; b=B; c=-sigma N^-2 X; d=-sigma a; q=0",
        "A_B_X": "A=psi_xy; B=psi_yy; X=psi_xx evaluated at (x,Ny)",
        "base_moments": {key: frac(value) for key, value in observed.items()},
        "T_norm_squared": {"rational_multiplier": frac(observed["X2"]),
                           "sigma_power": 2, "N_inverse_power": 4},
        "all_twenty_cubic_moments": moments,
        "admissibility": "N is any positive integer; fixed finite cosine sum gives uniform Linfinity bound and uniform integrability of fourth powers",
    }


def determinant(matrix):
    a, b, c, d = matrix
    return add(mul(a, d), scale(mul(b, c), -1))


def det4(matrix):
    import itertools
    answer = F(0)
    for perm in itertools.permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i+1, 4))
        value = F((-1) ** inversions)
        for row, column in enumerate(perm):
            value *= matrix[row][column]
        answer += value
    return answer


def main():
    streams = [
        stream_record(
            "ab2_dominant_with_b3_cancelled",
            [(1, 1, -1), (0, 1, -1), (1, 2, F(-1, 2)), (0, 2, 1)],
            {"B3": 0, "AB2": F(3, 2), "XB2": F(5, 4),
             "A2B": F(1, 2), "X2": F(5, 8)}),
        stream_record(
            "cb2_isolated",
            [(1, 0, 1), (0, 1, 1), (1, 1, 1)],
            {"B3": 0, "AB2": 0, "XB2": F(-1, 2), "A2B": 0, "X2": 1}),
        stream_record(
            "a2b_isolated",
            [(1, 1, 1), (1, -1, 1), (0, 2, 1), (0, 4, F(-1, 32)),
             (3, 0, F(-8, 729)), (0, 3, 1), (3, 3, 1)],
            {"B3": 0, "AB2": 0, "XB2": 0, "A2B": 2,
             "X2": F(544627, 13122)}),
        stream_record(
            "simple_cancellation_trap",
            [(1, 1, 1), (1, -1, 1), (0, 2, 1)],
            {"B3": -6, "AB2": 0, "XB2": -4, "A2B": 2, "X2": 1}),
    ]

    zero = {}
    b3_fields = [zero, cosine([(0, 1, 1), (0, 2, 1)]), cosine([(1, 0, 1)]), zero]
    qb2_fields = [zero, cosine([(0, 1, 1)]), zero, cosine([(0, 2, 1)])]
    b3_moments = cubic_moments(*b3_fields)
    qb2_moments = cubic_moments(*qb2_fields)
    for item in b3_moments:
        powers = item["powers_a_b_c_q"]
        check("b3 perturbation isolates " + str(powers), F(item["base_average"]),
              F(3, 4) if powers == [0, 3, 0, 0] else F(0))
        item["epsilon_power"] = powers[2]
    for item in qb2_moments:
        powers = item["powers_a_b_c_q"]
        check("qb2 perturbation isolates " + str(powers), F(item["base_average"]),
              F(1, 4) if powers == [0, 2, 0, 1] else F(0))
        item["epsilon_power"] = powers[3]

    null_rows = []
    for sign in (1, -1):
        gradient = [cosine([(1, 0, 1), (1, sign, 1)]),
                    cosine([(1, sign, sign)]), zero, cosine([(0, 1, 1)])]
        jacobian = determinant(gradient)
        row = [average(entry, jacobian) for entry in gradient]
        check("determinant multiplier row " + str(sign), row,
              [F(1, 2), F(sign, 4), F(0), F(0)])
        null_rows.append(row)
    for original in null_rows[:]:
        null_rows.append([-original[2], -original[3], -original[0], -original[1]])
    check("determinant multiplier witnesses rank four", det4(null_rows), F(1, 16))

    evidence = {
        "status": "EXACT_RATIONAL_FINITE_CHECKS_PASSED",
        "scope": "Exact Fourier moments and compatibility of stated fields only; analytic proof is not machine formalized",
        "normalization": "Mean integral on (R/2pi Z)^2; sigma>0 fixed",
        "b3_witness": {
            "map": "f=sin y+(1/2)sin 2y; g=epsilon sin x",
            "T_norm_squared": "epsilon^2/2",
            "all_twenty_cubic_moments": b3_moments,
            "P_average": "(3/4)*coefficient(b^3) exactly",
        },
        "qb2_witness": {
            "map": "f=sin y; g=(epsilon/2)sin 2y",
            "T_norm_squared": "epsilon^2/2",
            "all_twenty_cubic_moments": qb2_moments,
            "P_average": "(epsilon/4)*coefficient(q*b^2) exactly",
        },
        "stream_witnesses": streams,
        "no_cubic_null_lagrangian_check": {
            "maps": "f=sin x+sin(x+sign*y), g=sin y, sign=+1,-1; then swap outputs",
            "columns": ["<a det>", "<b det>", "<c det>", "<d det>"],
            "rows": [[frac(value) for value in row] for row in null_rows],
            "determinant": "1/16",
        },
    }
    (OUT / "exact_witnesses.json").write_text(json.dumps(evidence, indent=2) + "\n")
    receipt = {"status": "PASS", "exact_checks": len(CHECKS),
               "groups": ["four stream-function moment tables and compatibility",
                          "b3 and qb2 exact isolation",
                          "rank-four determinant-multiplier witnesses"],
               "limits": evidence["scope"]}
    (OUT / "VERIFICATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
