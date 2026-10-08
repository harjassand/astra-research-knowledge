"""Finite-action robust lineage-risk schedule toy (not clinical data).

Uses uniformization for a birth-death lineage with absorbing extinction (0)
 and establishment threshold (M), then bounds the risk that any Poisson-seeded
lineage reaches M. Run with Python 3; no third-party packages are required.
"""
from __future__ import annotations

from itertools import product
from functools import lru_cache
import math

M = 4
HORIZON = 5
DT = 1.0
S0 = 10.0
EPSILON = 0.04
QUADRATURE_N = 100

# Marginal confidence intervals; the robust calculation uses the adverse
# endpoint combination. These numbers are synthetic, in per-block units.
ROBUST = {
    "H": {"gS": 0.35, "eta": 0.03, "beta": 0.20, "delta": 0.40, "dose": 0.0},
    "D": {"gS": -0.40, "eta": 0.03, "beta": 0.45, "delta": 0.50, "dose": 1.0},
}
NOMINAL = {
    "H": {"gS": 0.30, "eta": 0.025, "beta": 0.175, "delta": 0.425, "dose": 0.0},
    "D": {"gS": -0.45, "eta": 0.025, "beta": 0.425, "delta": 0.525, "dose": 1.0},
}


def lineage_generator(beta: float, delta: float) -> list[list[float]]:
    """Row generator on lineage counts 0,...,M; 0 and M are absorbing."""
    q = [[0.0] * (M + 1) for _ in range(M + 1)]
    for r in range(1, M):
        up = beta * r
        down = delta * r
        q[r][r + 1] = up
        q[r][r - 1] = down
        q[r][r] = -(up + down)
    return q


@lru_cache(maxsize=None)
def transition_matrix(beta: float, delta: float, duration: float) -> tuple[tuple[float, ...], ...]:
    """Compute exp(Q t) by uniformization, truncating a negligible Poisson tail."""
    n = M + 1
    q = lineage_generator(beta, delta)
    rate = max(-q[i][i] for i in range(n))
    if rate == 0.0 or duration == 0.0:
        return tuple(tuple(float(i == j) for j in range(n)) for i in range(n))

    p = [[float(i == j) + q[i][j] / rate for j in range(n)] for i in range(n)]
    mean = rate * duration
    weight = math.exp(-mean)
    term = [[float(i == j) for j in range(n)] for i in range(n)]
    result = [[weight * term[i][j] for j in range(n)] for i in range(n)]

    for k in range(1, 250):
        term = [
            [sum(term[i][ell] * p[ell][j] for ell in range(n)) for j in range(n)]
            for i in range(n)
        ]
        weight *= mean / k
        for i in range(n):
            for j in range(n):
                result[i][j] += weight * term[i][j]
        if k > mean + 15.0 * math.sqrt(mean + 1.0) + 50.0:
            break
    return tuple(tuple(row) for row in result)


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def lineage_hit_probability(
    schedule: str, step: int, elapsed: float, actions: dict[str, dict[str, float]], suffix: list[float]
) -> float:
    """Probability one new cell reaches M from size 1 by horizon end."""
    rem = DT - elapsed
    a = actions[schedule[step]]
    p = transition_matrix(a["beta"], a["delta"], rem)
    return matvec(p, suffix)[1]


def schedule_risk_bound(
    schedule: str,
    actions: dict[str, dict[str, float]],
    quadrature_n: int = QUADRATURE_N,
) -> tuple[float, float, float]:
    """Return (first-moment risk bound, expected-successful-founder upper, final E[S] upper)."""
    # F_j[r] is the chance that a lineage of size r at boundary j reaches M
    # by the horizon, under the fixed suffix schedule. F_H is the indicator of r=M.
    suffix = [0.0] * (M + 1)
    suffix[M] = 1.0
    f_after: list[list[float]] = [[0.0] * (M + 1) for _ in range(HORIZON + 1)]
    f_after[HORIZON] = suffix[:]
    for j in range(HORIZON - 1, -1, -1):
        a = actions[schedule[j]]
        suffix = matvec(transition_matrix(a["beta"], a["delta"], DT), suffix)
        f_after[j] = suffix[:]

    s = S0
    expected_successful_founders_upper = 0.0
    for j, symbol in enumerate(schedule):
        a = actions[symbol]
        for q in range(quadrature_n):
            elapsed = (q + 0.5) * DT / quadrature_n
            p_hit = lineage_hit_probability(schedule, j, elapsed, actions, f_after[j + 1])
            source_rate = a["eta"] * s * math.exp(a["gS"] * elapsed)
            expected_successful_founders_upper += source_rate * p_hit * DT / quadrature_n
        s *= math.exp(a["gS"] * DT)

    # Markov's inequality gives a valid risk upper bound from the expected
    # number of successful founders, even when the sensitive source population
    # is stochastic and its mutation arrivals are not Poisson after averaging.
    risk = min(1.0, expected_successful_founders_upper)
    return risk, expected_successful_founders_upper, s


def dose(schedule: str, actions: dict[str, dict[str, float]]) -> float:
    return sum(actions[a]["dose"] * DT for a in schedule)


def enumerate_schedules(actions: dict[str, dict[str, float]]) -> list[tuple[float, float, str, float]]:
    rows = []
    for symbols in product(actions, repeat=HORIZON):
        schedule = "".join(symbols)
        risk, _, final_s = schedule_risk_bound(schedule, actions)
        rows.append((dose(schedule, actions), risk, schedule, final_s))
    return rows


def main() -> None:
    robust_rows = enumerate_schedules(ROBUST)
    nominal_rows = enumerate_schedules(NOMINAL)

    robust_feasible = sorted(row for row in robust_rows if row[1] <= EPSILON)
    nominal_feasible = sorted(row for row in nominal_rows if row[1] <= EPSILON)
    assert robust_feasible[0][2] == "DHHHH"
    assert robust_feasible[0][0] == 1.0
    assert nominal_feasible[0][2] == "HHHHH"

    robust_by_schedule = {row[2]: row for row in robust_rows}
    nominal_by_schedule = {row[2]: row for row in nominal_rows}
    print(f"risk limit={EPSILON:.3f}; resistant establishment threshold M={M}; horizon={HORIZON}")
    print("schedule  dose  midpoint-first-moment  robust-first-moment  final-E[S]-upper")
    for schedule in ("HHHHH", "DHHHH", "HDHHH", "DDHHH", "DDDDD"):
        rn = nominal_by_schedule[schedule]
        rr = robust_by_schedule[schedule]
        print(f"{schedule:8s} {rr[0]:4.0f} {rn[1]:13.6f} {rr[1]:12.6f} {rr[3]:22.4f}")
    print(f"robust dose-min schedule: {robust_feasible[0][2]} (dose {robust_feasible[0][0]:.0f})")
    print(f"midpoint dose-min schedule: {nominal_feasible[0][2]} (dose {nominal_feasible[0][0]:.0f})")
    print("The midpoint winner fails the union-bound risk limit at the adverse interval endpoints.")


if __name__ == "__main__":
    main()
