#!/usr/bin/env python3
"""Reproduce the sensing-cost crossover for the M=10 illustrative model.

The exact state-feedback rule lambda_n = M-n is assumed to read the exact
count immediately after every protein birth/death. With gamma=1, its total
state-transition intensity is lambda_n+n=M in every state, so its read rate
is M per unit time. Each read is charged c in protein-completion-equivalent
resource units.

The no-sensor comparator spends the same total resource on constant attempted
protein production. Its stationary law is truncated Poisson. This is a
finite-model accounting calculation, not an experimentally calibrated cost.
"""

from decimal import Decimal, getcontext
from math import comb, factorial

getcontext().prec = 50

M = 10
GAMMA = Decimal(1)
FEEDBACK_TAIL = Decimal(193) / Decimal(512)


def z(q: Decimal, top: int) -> Decimal:
    return sum((q**j / Decimal(factorial(j)) for j in range(top + 1)), Decimal(0))


def truncated_mean(q: Decimal) -> Decimal:
    return q * z(q, M - 1) / z(q, M)


def truncated_tail_below_5(q: Decimal) -> Decimal:
    return z(q, 4) / z(q, M)


def solve_increasing(fn, target: Decimal, lo: Decimal, hi: Decimal) -> Decimal:
    for _ in range(220):
        mid = (lo + hi) / 2
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve_decreasing(fn, target: Decimal, lo: Decimal, hi: Decimal) -> Decimal:
    for _ in range(220):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main() -> None:
    q_same_mean = solve_increasing(truncated_mean, Decimal(5), Decimal(0), Decimal(10))
    q_cross = solve_decreasing(truncated_tail_below_5, FEEDBACK_TAIL, Decimal(5), Decimal(6))
    mean_cross = truncated_mean(q_cross)
    c_cross = (mean_cross - Decimal(5)) / Decimal(M)
    c_example = Decimal("0.03")
    mean_example = Decimal(5) + Decimal(M) * c_example
    q_example = solve_increasing(truncated_mean, mean_example, Decimal(0), Decimal(10))

    feedback_dropout = Decimal(1) / Decimal(2**M)
    feedback_obs_rate = Decimal(M)
    assert sum(Decimal(comb(M, k)) for k in range(5)) / Decimal(2**M) == FEEDBACK_TAIL

    print(f"feedback_mean_births=5")
    print(f"feedback_exact_event_sensor_reads_per_time={feedback_obs_rate}")
    print(f"feedback_P_N_lt_5={FEEDBACK_TAIL}")
    print(f"feedback_P_N_eq_0={feedback_dropout}")
    print(f"constant_same_mean_q={q_same_mean}")
    print(f"constant_same_mean_P_N_lt_5={truncated_tail_below_5(q_same_mean)}")
    print(f"crossing_q={q_cross}")
    print(f"crossing_mean_births={mean_cross}")
    print(f"crossing_sensor_cost_per_read={c_cross}")
    print(f"at_c_0.03_total_resource={mean_example}")
    print(f"at_c_0.03_constant_q={q_example}")
    print(f"at_c_0.03_constant_P_N_lt_5={truncated_tail_below_5(q_example)}")


if __name__ == "__main__":
    main()
