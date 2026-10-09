#!/usr/bin/env python3
"""Exact finite checks for the T17 parity/short-interval note.

Only Python's standard library is used.  These checks validate finite
identities and exhibit finite counterexamples; they do not test an
asymptotic prime-distribution claim.
"""

from __future__ import annotations

import json
import math


def arithmetic_sieve(n: int):
    """Return SPF, primes, Mobius, Liouville, and von Mangoldt arrays."""
    spf = [0] * (n + 1)
    primes: list[int] = []
    for value in range(2, n + 1):
        if spf[value] == 0:
            spf[value] = value
            primes.append(value)
        for prime in primes:
            if prime > spf[value] or value * prime > n:
                break
            spf[value * prime] = prime

    mobius = [0] * (n + 1)
    liouville = [0] * (n + 1)
    von_mangoldt = [0.0] * (n + 1)
    mobius[1] = 1
    liouville[1] = 1
    for value in range(2, n + 1):
        prime = spf[value]
        quotient = value // prime
        liouville[value] = -liouville[quotient]
        if quotient % prime == 0:
            mobius[value] = 0
        else:
            mobius[value] = -mobius[quotient]

        residual = value
        while residual % prime == 0:
            residual //= prime
        if residual == 1:
            von_mangoldt[value] = math.log(prime)
    return spf, primes, mobius, liouville, von_mangoldt


def dirichlet_convolution(left, right, n: int):
    result = [0.0] * (n + 1)
    for a in range(1, n + 1):
        if left[a] == 0:
            continue
        for b in range(1, n // a + 1):
            if right[b] != 0:
                result[a * b] += left[a] * right[b]
    return result


def check_vaughan_identity(n: int, cutoff_mu: int, cutoff_lambda: int):
    """Check one exact Vaughan decomposition numerically through n."""
    spf, _, mobius, _, von_mangoldt = arithmetic_sieve(n)
    log_values = [0.0] * (n + 1)
    for value in range(1, n + 1):
        if value >= 2:
            log_values[value] = math.log(value)

    mu_small = [0.0] * (n + 1)
    mu_large = [0.0] * (n + 1)
    for value in range(1, n + 1):
        if value <= cutoff_mu:
            mu_small[value] = float(mobius[value])
        else:
            mu_large[value] = float(mobius[value])

    one = [0.0] * (n + 1)
    one[1:] = [1.0] * n
    lambda_small = [0.0] * (n + 1)
    lambda_large = [0.0] * (n + 1)
    for value in range(1, n + 1):
        if value <= cutoff_lambda:
            lambda_small[value] = von_mangoldt[value]
        else:
            lambda_large[value] = von_mangoldt[value]

    mu_small_times_one = dirichlet_convolution(mu_small, one, n)
    mu_large_times_one = dirichlet_convolution(mu_large, one, n)
    mu_small_times_log = dirichlet_convolution(mu_small, log_values, n)
    small_product = dirichlet_convolution(mu_small_times_one, lambda_small, n)
    large_product = dirichlet_convolution(mu_large_times_one, lambda_large, n)

    maximum_error = 0.0
    for value in range(1, n + 1):
        rhs = (
            lambda_small[value]
            + mu_small_times_log[value]
            - small_product[value]
            + large_product[value]
        )
        maximum_error = max(maximum_error, abs(rhs - von_mangoldt[value]))
    assert maximum_error < 2e-9
    return maximum_error


def main():
    x = 100_000
    nmax = 2 * x
    spf, primes, mobius, liouville, von_mangoldt = arithmetic_sieve(nmax)
    prime_set = set(primes)

    # Selberg's sequence: it is nonnegative and vanishes at every prime.
    prime_model_nonzero = [p for p in primes if 1 + liouville[p] != 0]
    assert not prime_model_nonzero
    assert all((1 + liouville[value]) in (0, 2) for value in range(2, nmax + 1))

    # Verify the exact divisor-class formula and compare finite local densities.
    prefix_lambda = [0] * (nmax + 1)
    for value in range(1, nmax + 1):
        prefix_lambda[value] = prefix_lambda[value - 1] + liouville[value]
    divisibility_samples = []
    for divisor in (1, 2, 3, 5, 6, 10, 30, 97, 210, 1000):
        quotient = x // divisor
        direct = sum(1 + liouville[divisor * k] for k in range(1, quotient + 1))
        formula = quotient + liouville[divisor] * prefix_lambda[quotient]
        assert direct == formula
        divisibility_samples.append(
            {
                "d": divisor,
                "multiples": quotient,
                "model_mass": direct,
                "uniform_mass": quotient,
                "relative_error": direct / quotient - 1.0,
                "exact_lambda_remainder": liouville[divisor]
                * prefix_lambda[quotient],
            }
        )

    # At this cutoff a rough integer <=2x has at most two prime factors
    # with multiplicity.  The parity character then isolates primes exactly.
    z = math.floor(nmax ** (1 / 3)) + 1
    assert z**3 > nmax
    interval_checks = []
    for left, right in ((x, 2 * x), (x, x + 5_000), (x + 25_000, x + 35_000)):
        rough_count = 0
        rough_liouville = 0
        parity_detector = 0
        actual_primes = 0
        for value in range(left + 1, right + 1):
            if spf[value] <= z:
                continue
            rough_count += 1
            rough_liouville += liouville[value]
            parity_detector += (1 - liouville[value]) // 2
            actual_primes += int(value in prime_set)
        assert parity_detector == actual_primes
        interval_checks.append(
            {
                "interval": [left, right],
                "cutoff_z": z,
                "rough_count": rough_count,
                "rough_liouville_sum": rough_liouville,
                "half_difference": (rough_count - rough_liouville) // 2,
                "prime_count": actual_primes,
                "exact_identity_holds": True,
            }
        )

    # Check Lambda = mu * log and one Vaughan decomposition on a smaller range.
    convolution_errors = []
    for value in range(1, 5_001):
        rhs = sum(
            mobius[d] * math.log(value // d)
            for d in range(1, value + 1)
            if value % d == 0 and value // d >= 1
        )
        assert abs(rhs - von_mangoldt[value]) < 2e-9
        convolution_errors.append(abs(rhs - von_mangoldt[value]))

    vaughan_error = check_vaughan_identity(2_000, 17, 23)
    global_lambda_sum = prefix_lambda[nmax]
    global_uniform_sum = nmax
    output = {
        "status": "finite_identity_checks_only_not_asymptotic_evidence",
        "range": {"N": x, "maximum_n": nmax},
        "selberg_model": {
            "a_n": "1 + lambda(n)",
            "prime_count_checked": len(primes),
            "nonzero_prime_weights": len(prime_model_nonzero),
            "weight_values_for_n_ge_2": [0, 2],
        },
        "divisibility_samples": divisibility_samples,
        "global_liouville": {
            "sum_lambda": global_lambda_sum,
            "sum_uniform_weight": global_uniform_sum,
            "relative_lambda_sum": global_lambda_sum / nmax,
        },
        "rough_parity_detector": {
            "criterion": "spf(n) > z and n <= 2N, where z^3 > 2N",
            "cutoff_z": z,
            "intervals": interval_checks,
        },
        "mu_log_identity": {
            "range": 5_000,
            "maximum_absolute_error": max(convolution_errors),
        },
        "vaughan_identity": {
            "range": 2_000,
            "U": 17,
            "V": 23,
            "maximum_absolute_error": vaughan_error,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
