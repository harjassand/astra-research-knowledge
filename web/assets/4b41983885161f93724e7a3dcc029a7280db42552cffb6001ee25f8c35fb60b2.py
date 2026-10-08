#!/usr/bin/env python3
"""Reproduce the exact-law comparison used in FINAL_REPORT.md.

The regulated finite-cap birth-death chain has rates
    n -> n+1 at a (M-n), and n -> n-1 at gamma*n.
Its stationary law is Binomial(M, a/(a+gamma)).

The comparator has constant attempted birth rate b when n<M, the same cap M,
and the same per-molecule loss gamma. Choose b so its stationary mean matches
the regulated chain. Its stationary law is a truncated Poisson. Both chains
then have the same mean accepted production rate, gamma*E[N].
"""

from decimal import Decimal, getcontext
from math import comb, factorial


getcontext().prec = 50


def z(q: Decimal, maximum: int) -> Decimal:
    return sum((q**k / Decimal(factorial(k)) for k in range(maximum + 1)), Decimal(0))


def truncated_poisson_mean(q: Decimal, maximum: int) -> Decimal:
    return q * z(q, maximum - 1) / z(q, maximum)


def binomial_cdf_below(m: int, p: Decimal, threshold: int) -> Decimal:
    return sum(
        (Decimal(comb(m, k)) * p**k * (Decimal(1) - p) ** (m - k)
         for k in range(threshold)),
        Decimal(0),
    )


def truncated_poisson_cdf_below(q: Decimal, m: int, threshold: int) -> Decimal:
    return sum((q**k / Decimal(factorial(k)) for k in range(threshold)), Decimal(0)) / z(q, m)


def truncated_poisson_variance(q: Decimal, m: int, mean: Decimal) -> Decimal:
    second = sum(
        (Decimal(k * k) * q**k / Decimal(factorial(k)) for k in range(m + 1)),
        Decimal(0),
    ) / z(q, m)
    return second - mean * mean


def main() -> None:
    m = 10
    a = Decimal(1)
    gamma = Decimal(1)
    p = a / (a + gamma)
    target_mean = Decimal(m) * p

    low, high = Decimal(0), Decimal(100)
    for _ in range(220):
        mid = (low + high) / 2
        if truncated_poisson_mean(mid, m) < target_mean:
            low = mid
        else:
            high = mid
    q = (low + high) / 2

    feedback_dropout = (Decimal(1) - p) ** m
    feedback_low_tail = binomial_cdf_below(m, p, 5)
    constitutive_dropout = Decimal(1) / z(q, m)
    constitutive_low_tail = truncated_poisson_cdf_below(q, m, 5)
    feedback_variance = Decimal(m) * p * (Decimal(1) - p)
    constitutive_variance = truncated_poisson_variance(q, m, target_mean)

    print(f"M={m}, a={a}, gamma={gamma}, p={p}")
    print(f"matched_mean={target_mean}")
    print(f"constant_attempt_rate_b={q * gamma}")
    print(f"constant_mean_check={truncated_poisson_mean(q, m)}")
    print(f"feedback_mean_accepted_births={gamma * target_mean}")
    print(f"constant_mean_accepted_births={gamma * truncated_poisson_mean(q, m)}")
    print(f"feedback_dropout_P_N0={feedback_dropout}")
    print(f"constant_dropout_P_N0={constitutive_dropout}")
    print(f"feedback_P_N_lt_5={feedback_low_tail}")
    print(f"constant_P_N_lt_5={constitutive_low_tail}")
    print(f"feedback_variance={feedback_variance}")
    print(f"constant_variance={constitutive_variance}")


if __name__ == "__main__":
    main()
