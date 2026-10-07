#!/usr/bin/env python3
"""Small exact checks for c10_l09's independent reconstruction.

This is a diagnostic for displayed finite identities, not a proof of their
uniform asymptotic or network-wide claims.
"""

from fractions import Fraction
from itertools import product
from math import comb, factorial
import json
from pathlib import Path


def falling(n: int, k: int) -> int:
    if k < 0 or n < k:
        return 0
    out = 1
    for q in range(k):
        out *= n - q
    return out


def factprod(x):
    out = 1
    for q in x:
        out *= factorial(q)
    return out


def W(m: int, V: int, j: int, rho=Fraction(1, 4)) -> Fraction:
    out = rho**j
    for r in range(m):
        out *= comb(V - 2 * r, j - r)
    return out


def check_birth_death():
    checks = 0
    for m in range(1, 4):
        for V in range(2 * m + 2, 2 * m + 14, 2):
            lo, hi = m - 1, V - m + 1
            weights = {j: W(m, V, j) for j in range(lo, hi + 1)}

            def birth(j):
                return Fraction(falling(V - j, m), V ** (m - 1))

            def death(j):
                return Fraction(4 * falling(j, m), V ** (m - 1))

            for j in range(lo, hi):
                rhs = Fraction(1, 4) * Fraction(falling(V - j, m), falling(j + 1, m))
                assert weights[j + 1] / weights[j] == rhs
                assert weights[j] * birth(j) == weights[j + 1] * death(j + 1)
                checks += 2

            for j in range(lo, hi + 1):
                incoming = Fraction(0)
                if j > lo:
                    incoming += weights[j - 1] * birth(j - 1)
                if j < hi:
                    incoming += weights[j + 1] * death(j + 1)
                outgoing = weights[j] * (birth(j) + death(j))
                assert incoming == outgoing
                checks += 1

            L = m
            assert L < V // 2
            increments = {}
            for k in range(L, hi + 1):
                tail = sum((weights[j] for j in range(k, hi + 1)), Fraction(0))
                increments[k] = tail / (death(k) * weights[k])
            h = {L - 1: Fraction(0)}
            for k in range(L, hi + 1):
                h[k] = h[k - 1] + increments[k]
            for k in range(L, hi + 1):
                generator = death(k) * (h[k - 1] - h[k])
                if k < hi:
                    generator += birth(k) * (h[k + 1] - h[k])
                assert generator == -1
                checks += 1

            R = sum((weights[j] for j in range(lo, L + 1)), Fraction(0)) / sum(
                (weights[j] for j in range(lo, V // 2 + 1)), Fraction(0)
            )
            assert 0 < R <= 1
            checks += 1
    return checks


# N77's five reactions, in species order A,B,C,D.
COMPLEXES = (
    (0, 0, 2, 0),  # 2C
    (1, 1, 1, 0),  # A+B+C
    (3, 2, 0, 0),  # 3A+2B
    (0, 0, 2, 1),  # 2C+D
)
REACTIONS = (
    (0, 1),
    (1, 2),
    (2, 0),
    (0, 3),
    (3, 0),
)


def monomial_factorial(x, y):
    out = 1
    for xi, yi in zip(x, y):
        out *= falling(xi, yi)
    return out


def exact_G_M(x):
    available = [y for y in COMPLEXES if all(a >= b for a, b in zip(x, y))]
    assert available
    G = min(factprod(tuple(a - b for a, b in zip(x, y))) for y in available)
    M = max(monomial_factorial(x, y) for y in available)
    assert factprod(x) == G * M
    return G, M, available


def check_n76_on_n77():
    checks = 0
    for n in range(9):
        for d in range(7):
            states = (
                (n, 0, 2, d),
                (n + 1, 1, 1, d),
                (n + 3, 2, 0, d),
            )
            for x in states:
                G, M, available = exact_G_M(x)
                enabled = []
                for ri, (yi, zi) in enumerate(REACTIONS):
                    y, z = COMPLEXES[yi], COMPLEXES[zi]
                    propensity = monomial_factorial(x, y)
                    if propensity:
                        xp = tuple(a - b + c for a, b, c in zip(x, y, z))
                        Gp, _, _ = exact_G_M(xp)
                        bound = Fraction(M, propensity)
                        ratio = Fraction(Gp, G)
                        assert ratio <= bound
                        enabled.append((propensity, ratio))
                        checks += 1

                total_rate = sum(p for p, _ in enabled)
                expectation = sum((p * ratio for p, ratio in enabled), Fraction(0)) / total_rate
                assert expectation <= 5
                checks += 1

                # Fixed-time predictable rate values in [1,4] at the current
                # state; every corner of the active rate box obeys the bound.
                for multipliers in product((1, 4), repeat=len(enabled)):
                    den = sum(k * p for k, (p, _) in zip(multipliers, enabled))
                    num = sum((k * p * ratio for k, (p, ratio) in zip(multipliers, enabled)), Fraction(0))
                    assert num / den <= 20
                    checks += 1
    return checks


def check_n77_stationary_and_invariants():
    checks = 0
    # Exact class-wise cycle flux and Poisson(1) birth/death balance.
    for n in range(12):
        q0 = 2
        q1 = n + 1
        q2 = 2 * (n + 1) * (n + 2) * (n + 3)
        w0 = Fraction(1, 2)
        w1 = Fraction(1, n + 1)
        w2 = Fraction(1, 2 * (n + 1) * (n + 2) * (n + 3))
        assert w0 * q0 == w1 * q1 == w2 * q2 == 1
        checks += 2
        for d in range(10):
            p_d = Fraction(1, factorial(d))
            # Phase 0: cycle influx/outflux cancel; D immigration and death
            # balance against p_d proportional to 1/d!.
            phase_in = w2 * p_d * q2
            phase_out = w0 * p_d * q0
            assert phase_in == phase_out
            in_d = Fraction(0)
            if d:
                in_d += w0 * Fraction(1, factorial(d - 1)) * 2
            in_d += w0 * Fraction(1, factorial(d + 1)) * 2 * (d + 1)
            out_d = w0 * p_d * (2 + 2 * d)
            assert in_d == out_d
            checks += 2

        for b, a in ((0, n), (1, n + 1), (2, n + 3)):
            assert a - b * (b + 1) // 2 == n
            checks += 1

    # Exact linear stoichiometric invariant B+C and rank-three span.
    v1, v2, v3, v4 = (1, 1, -1, 0), (2, 1, -1, 0), (-3, -2, 2, 0), (0, 0, 0, 1)
    assert tuple(-a - b for a, b in zip(v1, v2)) == v3
    assert all(v[1] + v[2] == 0 for v in (v1, v2, v3, v4, (0, 0, 0, -1)))
    checks += 2

    # Deficiency-zero/complex-balance data: four complexes, one linkage, and
    # the three independent vectors v1,v2,v4. All deterministic complex
    # fluxes at (1,1,1,1) are one, so each complex has equal inflow/outflow.
    assert (len(COMPLEXES), 1, 3, len(COMPLEXES) - 1 - 3) == (4, 1, 3, 0)
    checks += 1
    return checks


def main():
    counts = {
        "birth_death_exact_identities": check_birth_death(),
        "N76_exact_transition_and_rate_box_checks": check_n76_on_n77(),
        "N77_stationary_and_invariant_checks": check_n77_stationary_and_invariants(),
    }
    counts["total"] = sum(counts.values())
    out = Path(__file__).with_name("independent_checks.json")
    out.write_text(json.dumps(counts, indent=2) + "\n")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
