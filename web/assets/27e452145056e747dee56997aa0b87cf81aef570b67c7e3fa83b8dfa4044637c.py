#!/usr/bin/env python3
"""Exact finite-time error/work curve for an autonomous binary sensor.

Only standard-library modules are used.  Fractions verify the stationary
law and currents; logarithms enter only when converting chemical affinity to
power and evaluating path irreversibility.
"""

from fractions import Fraction as F
from math import exp, log


def solve_linear(matrix, rhs):
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    for col in range(n):
        pivot = next(row for row in range(col, n) if a[row][col] != 0)
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row == col:
                continue
            scale = a[row][col]
            a[row] = [x - scale * y for x, y in zip(a[row], a[col])]
    return [a[row][-1] for row in range(n)]


def stationary(lam, response, bias):
    ups = (response * (1 + bias) / 2, response * (1 - bias) / 2)
    downs = (response * (1 - bias) / 2, response * (1 + bias) / 2)
    q = [[F(0) for _ in range(4)] for _ in range(4)]
    for e in range(2):
        for m in range(2):
            i = 2 * e + m
            q[i][2 * (1 - e) + m] = lam
            q[i][2 * e + (1 - m)] = ups[e] if m == 0 else downs[e]
    for i in range(4):
        q[i][i] = -sum(q[i])
    matrix = [[q[j][i] for j in range(4)] for i in range(4)]
    rhs = [F(0)] * 4
    matrix[-1] = [F(1)] * 4
    rhs[-1] = F(1)
    p = tuple(solve_linear(matrix, rhs))
    return p, ups, downs


def observed_epr_over_kb(p, lam, ups, downs):
    epr = 0.0
    for m in range(2):
        i, j = m, 2 + m
        x, y = float(p[i] * lam), float(p[j] * lam)
        epr += (x - y) * log(x / y)
    for e in range(2):
        x = float(p[2 * e] * ups[e])
        y = float(p[2 * e + 1] * downs[e])
        epr += (x - y) * log(x / y)
    return epr


def chemical_power_over_kbt(p, ups, downs, bias):
    affinity = log((1 + float(bias)) / (1 - float(bias)))
    currents = [
        p[0] * ups[0] - p[1] * downs[0],
        p[2] * ups[1] - p[3] * downs[1],
    ]
    return float(currents[0]) * affinity + float(currents[1]) * (-affinity)


def main():
    lam, response = F(1), F(3)
    for bias in (F(1, 3), F(1, 2), F(2, 3), F(9, 10)):
        p, ups, downs = stationary(lam, response, bias)
        corr = 2 * (p[1] - p[3])
        expected_corr = response * bias / (response + 2 * lam)
        assert corr == expected_corr
        assert p == (
            (1 - corr) / 4, (1 + corr) / 4,
            (1 + corr) / 4, (1 - corr) / 4,
        )

        power = chemical_power_over_kbt(p, ups, downs, bias)
        observed = observed_epr_over_kb(p, lam, ups, downs)
        affinity = log((1 + float(bias)) / (1 - float(bias)))
        sharp_formula = float(lam * corr) * affinity
        assert abs(power - observed) < 1e-12
        assert abs(power - sharp_formula) < 1e-12

        print(f"bias a={float(bias):.6g}, stationary correlation c={float(corr):.12f}")
        print(f"  response rate R={float(response):g}, input flip rate lambda={float(lam):g}")
        print(f"  sharp beta*P = sigma_obs/kB = {power:.12f}")
        for tau in (0.0, 0.25, 1.0):
            acc = (1 + float(corr) * exp(-2 * float(lam) * tau)) / 2
            err = 1 - acc
            inferred_c = exp(2 * float(lam) * tau) * (1 - 2 * err)
            inferred_a = inferred_c * (float(response) + 2 * float(lam)) / float(response)
            inferred_power = float(lam) * inferred_c * log((1 + inferred_a) / (1 - inferred_a))
            assert abs(inferred_power - power) < 1e-12
            print(f"  tau={tau:g}: accuracy={acc:.12f}, error={err:.12f}, bound={inferred_power:.12f}")

    # At the base construction used in the channel-allocation witness, the
    # three-channel networks have the same score but strictly greater power
    # than the one-channel sharp-attainment network.
    base_p, base_u, base_d = stationary(F(1), F(3), F(1, 3))
    p_base = chemical_power_over_kbt(base_p, base_u, base_d, F(1, 3))
    p_a = float(F(61, 120)) * log(4)
    p_b = float(F(79, 120)) * log(4)
    assert p_base < p_a < p_b
    print("matched-output three-channel powers:", f"A={p_a:.12f}", f"B={p_b:.12f}")
    print("single-channel sharp-attainment power:", f"C={p_base:.12f}")


if __name__ == "__main__":
    main()
