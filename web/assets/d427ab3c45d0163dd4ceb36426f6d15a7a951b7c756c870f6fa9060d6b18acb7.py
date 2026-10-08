#!/usr/bin/env python3
"""Finite exact check for the reconstructed N77 stationary balance formulas.

This checks only the displayed phase and D birth/death flux identities for
n <= 100 and d <= 100. The proof in OBSTRUCTION.md establishes the identities
symbolically for all n,d; this script is a regression check, not that proof.
"""
from fractions import Fraction
from math import factorial


def phase_weights(n: int) -> tuple[Fraction, Fraction, Fraction]:
    return (
        Fraction(1, 2),
        Fraction(1, n + 1),
        Fraction(1, 2 * (n + 1) * (n + 2) * (n + 3)),
    )


def check(max_n: int = 100, max_d: int = 100) -> None:
    checks = 0
    for n in range(max_n + 1):
        w1, w2, w3 = phase_weights(n)
        r12 = w1 * 2
        r23 = w2 * (n + 1)
        r31 = w3 * 2 * (n + 1) * (n + 2) * (n + 3)
        assert r12 == r23 == r31 == 1
        checks += 3

        for d in range(max_d + 1):
            q_d = Fraction(1, factorial(d))
            q_next = Fraction(1, factorial(d + 1))
            assert q_d * 2 == q_next * 2 * (d + 1)

            # Full local balance at phase 1, after cancelling the common e^-1
            # factor from the Poisson(1) probabilities.
            outgoing = w1 * q_d * (2 + 2 + 2 * d)
            incoming = w3 * q_d * (
                2 * (n + 1) * (n + 2) * (n + 3)
            )
            if d >= 1:
                incoming += w1 * Fraction(1, factorial(d - 1)) * 2
            incoming += w1 * q_next * 2 * (d + 1)
            assert incoming == outgoing

            # The other two phases only have the directed cycle edge.
            assert w1 * q_d * 2 == w2 * q_d * (n + 1)
            assert w2 * q_d * (n + 1) == w3 * q_d * (
                2 * (n + 1) * (n + 2) * (n + 3)
            )
            checks += 4

    print(f"PASS: {checks} exact Fraction identities; n=0..{max_n}, d=0..{max_d}")
    print("Scope: finite balance consistency only; no proof of the all-n claim or external validity.")


if __name__ == "__main__":
    check()

