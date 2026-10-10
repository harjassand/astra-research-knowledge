"""Exact and sampled checks for a rare-reset steady-state response identity.

All exact assertions use fractions.  Random sampling is only a diagnostic.
The construction is the N641 four-state family with an optional derivative of
the within-block reset law, beta; beta=0 and a block indicator recover N641.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import sqrt
from random import Random


def solve(a: list[list[F]], b: list[F]) -> list[F]:
    n = len(b)
    aug = [row[:] + [b_i] for row, b_i in zip(a, b)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        c = aug[col][col]
        aug[col] = [v / c for v in aug[col]]
        for i in range(n):
            if i != col:
                c = aug[i][col]
                aug[i] = [v - c * w for v, w in zip(aug[i], aug[col])]
    return [row[-1] for row in aug]


def invariant_and_response(p: list[list[F]], dp: list[list[F]], a: list[F]):
    n = len(p)
    mat = [[(F(i == j) - p[j][i]) for j in range(n)] for i in range(n)]
    mat[-1] = [F(1)] * n
    pi = solve(mat, [F(0)] * (n - 1) + [F(1)])
    rhs = [sum(dp[j][i] * pi[j] for j in range(n)) for i in range(n)]
    dpi = solve(mat, rhs[:-1] + [F(0)])
    assert all(sum(pi[j] * p[j][i] for j in range(n)) == pi[i] for i in range(n))
    assert all(sum(dpi[j] * p[j][i] + pi[j] * dp[j][i] for j in range(n)) == dpi[i] for i in range(n))
    return pi, dpi, sum(a[i] * dpi[i] for i in range(n))


def chain(delta: F, beta: F):
    # B is N641's two-state transition, expressed row-stochastically.
    b = [[F(9, 10), F(1, 10)], [F(2, 5), F(3, 5)]]
    alpha = [F(1, 2), F(1, 2)]
    dalpha = [F(-1, 2), F(1, 2)]
    nu = [[F(1, 2), F(1, 2)] for _ in range(2)]
    dnu = [[F(0), F(0)], [-beta, beta]]
    n = 4
    p = [[F(0) for _ in range(n)] for _ in range(n)]
    dp = [[F(0) for _ in range(n)] for _ in range(n)]
    for mode in range(2):
        for x in range(2):
            s = 2 * mode + x
            for dest_mode in range(2):
                for y in range(2):
                    t = 2 * dest_mode + y
                    p[s][t] = (1 - delta) * F(mode == dest_mode) * b[x][y] + delta * alpha[dest_mode] * nu[dest_mode][y]
                    dp[s][t] = delta * (dalpha[dest_mode] * nu[dest_mode][y] + alpha[dest_mode] * dnu[dest_mode][y])
    assert all(sum(row) == 1 for row in p)
    assert all(sum(row) == 0 for row in dp)
    return p, dp


def coupled_step(x: int, y: int, rng: Random) -> tuple[int, int]:
    """Maximal coupling for B; unequal states meet next step with prob 1/2."""
    u = rng.randrange(10)
    if x == y:
        return (0, 0) if u < (9 if x == 0 else 4) else (1, 1)
    if u < 4:
        return 0, 0
    if u < 5:
        return 1, 1
    return x, y


def local_correction(delta: F, x: int, y: int, rng: Random) -> tuple[F, int]:
    out = F(0)
    discount = F(1)
    steps = 0
    while x != y:
        out += delta * discount * (x - y)  # f(x)=x
        x, y = coupled_step(x, y, rng)
        discount *= 1 - delta
        steps += 1
    return out, steps


def estimate(delta: F, beta: F, rng: Random) -> tuple[F, int]:
    x = int(rng.randrange(2) == 0)  # nu=(1/2,1/2)
    y = int(rng.randrange(5) == 0)  # exact pi_B=(4/5,1/5)
    c0, steps0 = local_correction(delta, x, y, rng)
    c1, steps1 = local_correction(delta, 1, 0, rng)
    # alpha'_0 A_0 + alpha'_1 A_1 = 1/2 times a shared local f.
    # alpha_1 nu'_1 A_1 = beta times a coupled plus/minus local f.
    return F(1, 10) + F(1, 2) * c0 + beta * c1, steps0 + steps1


def exact_estimator_moments(delta: F, beta: F) -> tuple[F, F, F]:
    r = 1 - delta
    eh = 1 - r / (2 - r)  # H=1-r^T, T~Geom(1/2) on {1,2,...}
    eh2 = 1 - 2 * r / (2 - r) + r * r / (2 - r * r)
    ez0 = F(3, 10) * eh
    vz0 = F(1, 2) * eh2 - ez0 * ez0
    vz1 = eh2 - eh * eh
    return F(1, 10) + F(1, 2) * ez0 + beta * eh, F(1, 4) * vz0 + beta * beta * vz1, F(3)


def main() -> None:
    beta = F(1, 4)
    print("nonconstant observable A=(0,1,0,2), beta=1/4")
    for d in [F(1, 10), F(1, 100), F(1, 1000), F(1, 10000)]:
        p, dp = chain(d, beta)
        pi, dpi, exact = invariant_and_response(p, dp, [F(0), F(1), F(0), F(2)])
        coupled_mean, coupled_var, expected_pairs = exact_estimator_moments(d, beta)
        formula = (F(1, 10) + F(9, 10) * d) / (1 + d)
        assert exact == coupled_mean == formula
        assert coupled_var >= 0
        print(f"delta={d}, response={exact}, pair_updates={expected_pairs}, geometric_age_updates={(1-d)/d}, estimator_variance={float(coupled_var):.9g}")
        if d == F(1, 1000):
            rng = Random(641)
            samples = [estimate(d, beta, rng) for _ in range(100_000)]
            avg = float(sum(z for z, _ in samples) / len(samples))
            avg_pairs = sum(c for _, c in samples) / len(samples)
            se = sqrt(float(coupled_var) / len(samples))
            assert abs(avg - float(exact)) < 5 * se
            print(f"  100000-path diagnostic mean={avg:.9g}, exact={float(exact):.9g}, se={se:.3g}, mean_pair_updates={avg_pairs:.5g}")
    # Recover N641's original beta=0 block occupancy response exactly.
    p, dp = chain(F(1, 1000), F(0))
    pi, dpi, response = invariant_and_response(p, dp, [F(0), F(0), F(1), F(1)])
    expected_pi = [F(4001, 10010), F(502, 5005)] * 2
    assert pi == expected_pi
    assert dpi == [-expected_pi[0], -expected_pi[1], expected_pi[0], expected_pi[1]]
    assert response == F(1, 2)
    print("N641 block-occupancy response=1/2 (exact)")


if __name__ == "__main__":
    main()
