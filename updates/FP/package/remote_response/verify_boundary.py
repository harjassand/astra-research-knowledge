"""Exact rational replay of the remote-row susceptibility boundary.

No external dependencies. Run: python3 verify_boundary.py
"""

from fractions import Fraction as F
import json


def matrix(m, gap):
    """One-excitation matrix of the local frustration-free chain."""
    assert m >= 2 and gap > 0
    terminal = F(m - 1, m) + gap
    j = [[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        j[i][i] = F(2) if i < m - 1 else terminal
        if i + 1 < m:
            j[i][i + 1] = j[i + 1][i] = F(-1)
    return j


def multiply(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def moments(j, end):
    n = len(j)
    power = [[F(i == k) for k in range(n)] for i in range(n)]
    result = []
    for _ in range(end + 1):
        result.append(power[0][0])
        power = multiply(power, j)
    return result


def solve(a, b):
    n = len(a)
    z = [row[:] + [b[i]] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if z[i][k])
        z[k], z[pivot] = z[pivot], z[k]
        scale = z[k][k]
        z[k] = [u / scale for u in z[k]]
        for i in range(n):
            if i != k:
                factor = z[i][k]
                z[i] = [u - factor * v for u, v in zip(z[i], z[k])]
    return [row[-1] for row in z]


def check(m, gap):
    a, b = matrix(m, gap), matrix(m, 2 * gap)
    assert all(a[i][j] == b[i][j] for i in range(m) for j in range(m)
               if (i, j) != (m - 1, m - 1))
    # Positive local rows q_i = sigma_i^- - i/(i+1) sigma_(i+1)^-
    # with weight (i+1)/i, plus gap*n_m, reproduce J exactly.
    reconstructed = [[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(1, m):
        weight = F(i + 1, i)
        q = [F(0) for _ in range(m)]
        q[i - 1], q[i] = F(1), -F(i, i + 1)
        for x in range(m):
            for y in range(m):
                reconstructed[x][y] += weight * q[x] * q[y]
    reconstructed[m - 1][m - 1] += gap
    assert reconstructed == a

    ma, mb = moments(a, 2 * m - 1), moments(b, 2 * m - 1)
    assert ma[:2 * m - 1] == mb[:2 * m - 1]
    assert mb[2 * m - 1] - ma[2 * m - 1] == gap
    chi_a = solve(a, [F(1)] + [F(0)] * (m - 1))[0]
    chi_b = solve(b, [F(1)] + [F(0)] * (m - 1))[0]
    assert chi_a == F(m - 1, m) + 1 / (m * m * gap)
    assert chi_b == F(m - 1, m) + 1 / (2 * m * m * gap)
    return {
        "m": m,
        "gap_parameter": str(gap),
        "identical_moments_through": 2 * m - 2,
        "first_moment_difference": str(mb[-1] - ma[-1]),
        "chi_low_terminal": str(chi_a),
        "chi_high_terminal": str(chi_b),
        "response_ratio": str(chi_a / chi_b),
    }


if __name__ == "__main__":
    print(json.dumps([check(m, F(1, 10**6)) for m in (3, 5, 8)], indent=2))
