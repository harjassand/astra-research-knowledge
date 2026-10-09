#!/usr/bin/env python3
"""Exact checks for the autonomous sensing-channel counterexample.

Uses only the Python standard library.  Rates are rational, and the stationary
law is solved with Fraction arithmetic.  The time-horizon prediction formula
uses the exact two-state telegraph semigroup.
"""

from fractions import Fraction as F
from math import exp, log


RATIOS = (F(4), F(1), F(1, 4))
ENV_RATE = F(1)
TARGET_UP = (F(2), F(1))     # E=+, E=-: M=0 -> M=1
TARGET_DOWN = (F(1), F(2))   # E=+, E=-: M=1 -> M=0

CHANNEL_SETS = {
    "A": (
        (F(23, 60), F(5, 12), F(1, 5)),
        (F(1, 15), F(1, 3), F(8, 5)),
    ),
    "B": (
        (F(13, 30), F(1, 6), F(2, 5)),
        (F(7, 60), F(1, 12), F(9, 5)),
    ),
}


def solve_linear(matrix, rhs):
    """Solve a square system exactly by Gauss-Jordan elimination."""
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    for col in range(n):
        pivot = next(row for row in range(col, n) if a[row][col] != 0)
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [value / scale for value in a[col]]
        for row in range(n):
            if row == col:
                continue
            scale = a[row][col]
            a[row] = [x - scale * y for x, y in zip(a[row], a[col])]
    return [a[row][-1] for row in range(n)]


def aggregate_rates(d_by_e):
    totals = []
    for d in d_by_e:
        down = sum(d)
        up = sum(r * rate for r, rate in zip(RATIOS, d))
        totals.append((up, down))
    return tuple(totals)


def generator():
    """Row generator, states ordered (+,0),(+,1),(-,0),(-,1)."""
    q = [[F(0) for _ in range(4)] for _ in range(4)]
    for e in range(2):
        for m in range(2):
            i = 2 * e + m
            q[i][2 * (1 - e) + m] += ENV_RATE
            rate = TARGET_UP[e] if m == 0 else TARGET_DOWN[e]
            q[i][2 * e + (1 - m)] += rate
    for i in range(4):
        q[i][i] = -sum(q[i])
    return q


def stationary(q):
    # Solve Q^T p=0 with the last equation replaced by normalization.
    matrix = [[q[j][i] for j in range(4)] for i in range(4)]
    rhs = [F(0) for _ in range(4)]
    matrix[-1] = [F(1) for _ in range(4)]
    rhs[-1] = F(1)
    return solve_linear(matrix, rhs)


def channel_currents(p, d_by_e):
    currents = []
    for e, d in enumerate(d_by_e):
        row = []
        for ratio, down in zip(RATIOS, d):
            up = ratio * down
            row.append(p[2 * e] * up - p[2 * e + 1] * down)
        currents.append(tuple(row))
    return tuple(currents)


def chemical_power_over_kbt(currents):
    # Channel affinities are (ln 4, 0, -ln 4).
    net_fuel_current = sum(
        row[0] - row[2] for row in currents
    )
    return net_fuel_current, float(net_fuel_current) * log(4)


def entropy_production_over_kb(p, currents, d_by_e):
    """Channel-resolved steady EPR, including E jumps, in units k_B/time."""
    e_part = 0.0
    for m in range(2):
        forward = float(p[m] * ENV_RATE)
        reverse = float(p[2 + m] * ENV_RATE)
        e_part += (forward - reverse) * log(forward / reverse)

    m_part = 0.0
    for e, (d, row) in enumerate(zip(d_by_e, currents)):
        for ratio, down, current in zip(RATIOS, d, row):
            up = ratio * down
            forward = float(p[2 * e] * up)
            reverse = float(p[2 * e + 1] * down)
            m_part += float(current) * log(forward / reverse)
    return e_part + m_part


def observed_entropy_production_over_kb(p):
    """EPR of the observed four-state generator after channel lumping."""
    epr = 0.0
    for m in range(2):
        forward = float(p[m] * ENV_RATE)
        reverse = float(p[2 + m] * ENV_RATE)
        epr += (forward - reverse) * log(forward / reverse)
    for e in range(2):
        forward = float(p[2 * e] * TARGET_UP[e])
        reverse = float(p[2 * e + 1] * TARGET_DOWN[e])
        epr += (forward - reverse) * log(forward / reverse)
    return epr


def hidden_channel_entropy_production_over_kb(p, d_by_e):
    """Log-sum gap between labeled channels and the aggregate M edge."""
    gap = 0.0
    for e, d in enumerate(d_by_e):
        x = [float(p[2 * e] * r * rate) for r, rate in zip(RATIOS, d)]
        y = [float(p[2 * e + 1] * rate) for rate in d]
        X, Y = sum(x), sum(y)
        a = [value / X for value in x]
        b = [value / Y for value in y]
        d_ab = sum(ai * log(ai / bi) for ai, bi in zip(a, b) if ai > 0)
        d_ba = sum(bi * log(bi / ai) for ai, bi in zip(a, b) if bi > 0)
        gap += X * d_ab + Y * d_ba
    return gap


def allocation_interval(d):
    """Closed theta interval for d + theta*(1,-5,4) >= 0."""
    lower = max(-d[0], -d[2] / 4)
    upper = d[1] / 5
    return lower, upper


def accuracy(tau):
    # The stationary E,M correlation is 1/5 and E is a rate-1 telegraph.
    corr = 0.2 * exp(-2.0 * tau)
    return (1.0 + corr) / 2.0


def main():
    expected_aggregate = ((F(2), F(1)), (F(1), F(2)))
    q = generator()
    p = stationary(q)
    expected_p = [F(1, 5), F(3, 10), F(3, 10), F(1, 5)]
    assert p == expected_p, p

    print("aggregate rates (u_e,d_e):", expected_aggregate)
    print("stationary p(+0,+1,-0,-1):", tuple(p))
    print("M entropy: 1 bit; conditional response rate: 3 per time unit")
    print("predictive accuracy A(tau)=(1+0.2 exp(-2 tau))/2")
    for tau in (0.0, 0.5, 1.0):
        print(f"  tau={tau:g}: A={accuracy(tau):.12f}")

    for name, d_by_e in CHANNEL_SETS.items():
        aggregates = aggregate_rates(d_by_e)
        assert aggregates == expected_aggregate, (name, aggregates)
        currents = channel_currents(p, d_by_e)
        fuel_current, power = chemical_power_over_kbt(currents)
        epr = entropy_production_over_kb(p, currents, d_by_e)
        assert abs(epr - power) < 1e-12, (name, epr, power)
        hidden = hidden_channel_entropy_production_over_kb(p, d_by_e)
        obs_epr = observed_entropy_production_over_kb(p)
        assert abs((epr - obs_epr) - hidden) < 1e-12, (name, epr, obs_epr, hidden)
        print(f"network {name} down-channel rates:", d_by_e)
        print(f"network {name} channel currents:", currents)
        print(f"network {name} net fuel current:", fuel_current)
        print(f"network {name} chemical power/(kBT): {power:.12f}")
        print(f"network {name} full EPR/kB: {epr:.12f}")
        print(f"network {name} observed-state EPR/kB: {obs_epr:.12f}")
        print(f"network {name} hidden-channel EPR/kB: {hidden:.12f}")

    a = chemical_power_over_kbt(channel_currents(p, CHANNEL_SETS["A"]))[1]
    b = chemical_power_over_kbt(channel_currents(p, CHANNEL_SETS["B"]))[1]
    expected_gap = (3.0 / 20.0) * log(4)
    assert abs((b - a) - expected_gap) < 1e-12
    print(f"same-output power gap/(kBT): {b-a:.12f}")

    # d(theta)=d(A)+theta*(1,-5,4) preserves the aggregate rates.
    # Its strictly positive feasible interval is (-1/20, 1/15).
    for theta in (F(-1, 100), F(0), F(1, 20), F(1, 20) - F(1, 100)):
        vector = (theta, -5 * theta, 4 * theta)
        d_theta = tuple(
            tuple(x + dx for x, dx in zip(row, vector))
            for row in CHANNEL_SETS["A"]
        )
        assert all(rate > 0 for row in d_theta for rate in row)
        assert aggregate_rates(d_theta) == expected_aggregate
    print("continuum direction (1,-5,4) preserves all observed rates")
    print("common-theta subfamily: power/(kBT) = ln(4) * (61/120 + 3 theta)")

    # The full allocation polytope has an independent theta for each input.
    # Its extreme points are obtained by setting one of three channel rates
    # to zero.  Since the work is linear, these endpoint combinations give
    # the sharp closure over all nonnegative allocations.
    intervals = [allocation_interval(row) for row in CHANNEL_SETS["A"]]
    assert intervals == [(F(-1, 20), F(1, 12)), (F(-1, 15), F(1, 15))]
    for theta_values in (
        (intervals[0][0], intervals[1][0]),
        (intervals[0][1], intervals[1][1]),
    ):
        endpoint_allocations = tuple(
            tuple(x + theta * v for x, v in zip(row, (F(1), F(-5), F(4))))
            for row, theta in zip(CHANNEL_SETS["A"], theta_values)
        )
        assert all(rate >= 0 for row in endpoint_allocations for rate in row)
        assert aggregate_rates(endpoint_allocations) == expected_aggregate
    theta_sum_min = sum(lo for lo, _ in intervals)
    theta_sum_max = sum(hi for _, hi in intervals)
    fuel_at_min = F(61, 120) + F(3, 2) * theta_sum_min
    fuel_at_max = F(61, 120) + F(3, 2) * theta_sum_max
    assert (fuel_at_min, fuel_at_max) == (F(1, 3), F(11, 15))
    assert fuel_at_min < F(61, 120) < F(79, 120) < fuel_at_max
    print("independent theta intervals:", tuple(intervals))
    print("full sharp closure fuel-current interval:", fuel_at_min, fuel_at_max)
    print("full sharp closure power/(kBT): ln(4) times that interval")
    assert abs(observed_entropy_production_over_kb(p) - (log(2) / 5)) < 1e-12
    print("observed-state EPR/kB = ln(2)/5; chemical EPR exceeds it")


if __name__ == "__main__":
    main()
