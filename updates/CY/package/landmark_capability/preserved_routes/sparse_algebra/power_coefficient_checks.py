"""Exhaustive and large-index finite checks for power_coefficient.py."""

from __future__ import annotations

import json
import random

from power_coefficient import coefficient_of_power


def multiply(a, b, p):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = ea + eb
            out[e] = (out.get(e, 0) + ca * cb) % p
    return {e: c for e, c in out.items() if c}


def direct_power_coefficient(terms, p, K, N):
    P = {}
    for e, c in terms:
        P[e] = (P.get(e, 0) + c) % p
    P = {e: c for e, c in P.items() if c}
    result = {0: 1}
    for _ in range(K):
        result = multiply(result, P, p)
    return result.get(N, 0)


def lucas_binomial(n, k, p):
    if k < 0 or k > n:
        return 0
    factorial = [1] * p
    for i in range(1, p):
        factorial[i] = factorial[i - 1] * i % p
    answer = 1
    while n or k:
        nd, kd = n % p, k % p
        if kd > nd:
            return 0
        answer = answer * factorial[nd] % p
        answer = answer * pow(factorial[kd], -1, p) % p
        answer = answer * pow(factorial[nd - kd], -1, p) % p
        n //= p
        k //= p
    return answer


def lucas_multinomial(n, parts, p):
    factorial = [1] * p
    for i in range(1, p):
        factorial[i] = factorial[i - 1] * i % p
    answer = 1
    parts = list(parts)
    while n or any(parts):
        nd = n % p
        digits = [part % p for part in parts]
        if sum(digits) != nd:
            return 0
        answer = answer * factorial[nd] % p
        for digit in digits:
            answer = answer * pow(factorial[digit], -1, p) % p
        n //= p
        parts = [part // p for part in parts]
    return answer


def main():
    exhaustive = 0
    # Every polynomial of degree at most two over F_3, including the zero
    # polynomial and leading-term cancellations, for small powers and indices.
    for c0 in range(3):
        for c1 in range(3):
            for c2 in range(3):
                terms = [(0, c0), (1, c1), (2, c2)]
                for K in range(9):
                    for N in range(0, 2 * K + 3):
                        got, _ = coefficient_of_power(terms, 3, K, N)
                        expected = direct_power_coefficient(terms, 3, K, N)
                        assert got == expected, (terms, K, N, got, expected)
                        exhaustive += 1

    # Random sparse polynomials over several small prime fields, checked by
    # explicit repeated multiplication (the expansion remains modest).
    rng = random.Random(20261010)
    random_cases = 0
    for p in (2, 3, 5, 7):
        for _ in range(150):
            degree = rng.randrange(1, 9)
            terms = [(e, rng.randrange(p)) for e in range(degree + 1) if rng.random() < 0.4]
            K = rng.randrange(0, 18)
            N = rng.randrange(0, degree * K + 3)
            got, _ = coefficient_of_power(terms, p, K, N)
            expected = direct_power_coefficient(terms, p, K, N)
            assert got == expected, (p, terms, K, N, got, expected)
            random_cases += 1

    # Huge-index binomial coefficients are independently checked by Lucas'
    # digit formula, including zero residues caused by carries.
    huge_cases = 0
    huge_multinomial_cases = 0
    p = 101
    for _ in range(500):
        K = rng.getrandbits(250)
        N = rng.getrandbits(260)
        got, _ = coefficient_of_power([(0, 1), (1, 1)], p, K, N)
        expected = lucas_binomial(K, N, p)
        assert got == expected, (K, N, got, expected)
        huge_cases += 1

    # Independent multinomial/Lucas expansion for a non-binomial polynomial
    # at huge K and small N.  The bounded N leaves only O(N^2) count vectors.
    terms = [(0, 2), (1, 5), (2, 7)]
    for _ in range(200):
        K = rng.getrandbits(250)
        N = rng.randrange(41)
        expected = 0
        for count_x2 in range(N // 2 + 1):
            count_x = N - 2 * count_x2
            count_x0 = K - count_x - count_x2
            if count_x0 < 0:
                continue
            multinomial = lucas_multinomial(
                K, [count_x0, count_x, count_x2], p
            )
            term = (
                multinomial
                * pow(2, count_x0, p)
                * pow(5, count_x, p)
                * pow(7, count_x2, p)
            ) % p
            expected = (expected + term) % p
        got, _ = coefficient_of_power(terms, p, K, N)
        assert got == expected, (K, N, got, expected)
        huge_multinomial_cases += 1

    # Frobenius cancellation: P(x)^(p^m) has only p^m-scaled exponents.
    frobenius_cases = 0
    for p, polynomial, m in (
        (2, [(0, 1), (1, 1), (2, 1)], 60),
        (3, [(0, 2), (1, 1), (2, 2)], 45),
        (5, [(0, 1), (1, 2), (3, 4)], 35),
    ):
        K = p**m
        for exponent, coefficient in polynomial:
            target = exponent * K
            got, _ = coefficient_of_power(polynomial, p, K, target)
            assert got == coefficient % p
            frobenius_cases += 1
        got, _ = coefficient_of_power(polynomial, p, K, K // p)
        assert got == 0
        frobenius_cases += 1

    print(
        json.dumps(
            {
                "exhaustive_small_cases": exhaustive,
                "random_sparse_cases": random_cases,
                "huge_lucas_cases": huge_cases,
                "huge_nonbinomial_lucas_expansion_cases": huge_multinomial_cases,
                "frobenius_cancellation_cases": frobenius_cases,
                "huge_K_bits": 250,
                "huge_N_bits": 260,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

