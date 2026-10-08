#!/usr/bin/env python3
"""Exact finite generator check for the multiplicative boundary corrector.

This is a scoped formula check only. The theorem's uniform drift is proved
analytically in leaves/geometric_rate_box.txt.
"""

from fractions import Fraction as F


R = F(6, 5)
KAPPA = F(1)
ALPHA = DELTA = P = U = F(1)
Q = VREV = F(2)
K = 1


def falling(n, order):
    out = 1
    for z in range(order):
        out *= n - z
    return max(0, out)


def psi(b1, b2):
    return R**b1 + R**b2


def potential(a, b1, b2):
    return F(a) + (1 + KAPPA * (a == 0)) * psi(b1, b2)


def actual_generator(a, b1, b2):
    x = (a, b1, b2)
    terms = []

    def add(rate, y):
        if rate:
            terms.append(rate * (potential(*y) - potential(*x)))

    # 0 <-> A
    add(ALPHA, (a + 1, b1, b2))
    add(DELTA * a, (a - 1, b1, b2))

    for i, b in enumerate((b1, b2)):
        def shifted(db):
            bs = [b1, b2]
            bs[i] += db
            return (a, bs[0], bs[1])

        # A <-> A+B_i
        add(P * a, shifted(1))
        add(Q * a * b, shifted(-1))
        # A+B_i <-> 2A+B_i
        add(U * a * b, (a + K, b1, b2))
        add(VREV * falling(a, K + 1) * b, (a - K, b1, b2))

    return sum(terms, F(0))


def formula_generator(a, b1, b2):
    ps = psi(b1, b2)
    if a == 0:
        return ALPHA - DELTA * ps
    c = R - 1
    d = 1 - 1 / R

    def g(m):
        return P * c * R**m - Q * d * m * R**m + K * U * m

    return (
        ALPHA
        - DELTA * a
        + a * (g(b1) + g(b2))
        - K * VREV * falling(a, K + 1) * (b1 + b2)
        + (DELTA * ps if a == 1 else 0)
    )


def main():
    states = 0
    max_abs_error = F(0)
    for a in range(16):
        for b1 in range(16):
            for b2 in range(16):
                states += 1
                exact = actual_generator(a, b1, b2)
                claimed = formula_generator(a, b1, b2)
                max_abs_error = max(max_abs_error, abs(exact - claimed))
                assert exact == claimed, (a, b1, b2, exact, claimed)
    print({
        "status": "PASS",
        "scope": "exact rational generator identity on finite fixture grid",
        "states": states,
        "max_abs_error": str(max_abs_error),
        "rates": "alpha=delta=p=u=1, q=v=2, k=1, R=6/5, kappa=1",
        "not_checked": [
            "all-state drift inequality",
            "uniformity over the rate box",
            "nonexplosion or recurrence",
            "novelty or external proof validity",
        ],
    })


if __name__ == "__main__":
    main()
