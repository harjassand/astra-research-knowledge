#!/usr/bin/env python3
"""Check the occupancy-dependent exact frontier for a binary telegraph sensor.

Rational arithmetic verifies the stationary law and the rate constraints.
The entropy production and mutual informations are evaluated numerically only
after the exact probability formulas have been checked.
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


def model(lam, response, delta, mean_one):
    """Return exact stationary law and conditional rates.

    States are (+,0),(+,1),(-,0),(-,1). Here delta=(u_+-u_-)/2
    and mean_one=(u_++u_-)/(2R)=P(M=1).
    """
    b = response * mean_one
    ups = (b + delta, b - delta)
    downs = (response - b - delta, response - b + delta)
    assert all(x > 0 for x in ups + downs)

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


def entropy(x):
    x = float(x)
    return -x * log(x) - (1 - x) * log(1 - x)


def observed_epr(p, lam, ups, downs):
    total = 0.0
    for m in range(2):
        x, y = float(p[m] * lam), float(p[2 + m] * lam)
        total += (x - y) * log(x / y)
    for e in range(2):
        x = float(p[2 * e] * ups[e])
        y = float(p[2 * e + 1] * downs[e])
        total += (x - y) * log(x / y)
    return total


def bayes_accuracy_at_horizon(p, lam, tau):
    persistence = exp(-2 * float(lam) * tau)
    accuracy = 0.0
    for m in range(2):
        plus = float(p[m]) * (1 + persistence) / 2
        plus += float(p[2 + m]) * (1 - persistence) / 2
        marginal = float(p[m] + p[2 + m])
        minus = marginal - plus
        accuracy += max(plus, minus)
    return accuracy


def formulas(lam, response, delta, mean_one, tau):
    c = 2 * delta / (response + 2 * lam)
    z = c * exp(-2 * float(lam) * tau) / 2
    q = delta / response
    m = mean_one
    cycle_affinity = log(
        ((m + q) * (1 - m + q)) / ((1 - m - q) * (m - q))
    )
    beta_power = float(lam * c / 2) * cycle_affinity
    predictive_information = entropy(m) - 0.5 * (entropy(m + z) + entropy(m - z))
    causal_memory = entropy(m) - 0.5 * (
        entropy(m + float(c) / 2) + entropy(m - float(c) / 2)
    )
    accuracy = 0.5 + float(z)
    return c, z, cycle_affinity, beta_power, predictive_information, causal_memory, accuracy


def main():
    lam, response, delta = F(1), F(3), F(1, 2)
    means = (F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4))
    tau = 1
    rows = []
    for m in means:
        p, ups, downs = model(lam, response, delta, m)
        c, z, cyc, beta_power, pred_i, causal_i, acc = formulas(
            lam, response, delta, m, tau
        )
        assert p == (
            (1 - m) / 2 - c / 4,
            m / 2 + c / 4,
            (1 - m) / 2 + c / 4,
            m / 2 - c / 4,
        )
        assert (ups[0] + downs[0], ups[1] + downs[1]) == (response, response)
        assert (ups[0] - ups[1]) == 2 * delta
        assert abs(observed_epr(p, lam, ups, downs) - beta_power) < 1e-12

        assert abs(bayes_accuracy_at_horizon(p, lam, tau) - acc) < 1e-12
        rows.append((float(m), beta_power, pred_i, causal_i))

    center = rows[2]
    assert all(row[1] > center[1] for row in rows if row[0] != 0.5)
    assert all(row[2] > center[2] for row in rows if row[0] != 0.5)
    assert all(row[3] > center[3] for row in rows if row[0] != 0.5)
    for left, right in zip(rows[:2], reversed(rows[3:])):
        assert abs(left[1] - right[1]) < 1e-12
        assert abs(left[2] - right[2]) < 1e-12
        assert abs(left[3] - right[3]) < 1e-12

    print("R=3, lambda=1, Delta=1, tau=1; all rates and stationary laws exact")
    print("mean occupancy   beta*sigma_obs/kB   I(M;E[t+tau])   I(M;E[t:])")
    for m, power, pred_i, causal_i in rows:
        print(f"{m:14.6f} {power:18.12f} {pred_i:15.12f} {causal_i:13.12f}")
    print("Verified: fixed Bayes accuracy, symmetry, and minima at occupancy 1/2.")


if __name__ == "__main__":
    main()
