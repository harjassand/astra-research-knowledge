#!/usr/bin/env python3
"""Small exact-rational validation for the cycle-3 Foster witness.

This is finite checking only.  The all-state drift and nonexplosion claims
are proved analytically in REPORT.txt.
"""

from fractions import Fraction as Q


R = Q(6, 5)


def g(m: int) -> Q:
    return R**m * (Q(1, 5) - Q(m, 3)) + m


def value(a: int, b1: int, b2: int) -> Q:
    return Q(a) + R**b1 + R**b2 + 3 * (a == 0)


def formula_drift(a: int, b1: int, b2: int) -> Q:
    return (
        1 - a
        + a * (g(b1) + g(b2))
        - 2 * a * (a - 1) * (b1 + b2)
        - 3 * (a == 0)
        + 3 * (a == 1)
    )


def direct_drift(a: int, b1: int, b2: int) -> Q:
    """Generator applied to V by explicit state changes and propensities."""
    x = (a, b1, b2)
    transitions = [
        (Q(1), (a + 1, b1, b2)),                    # 0 -> A
        (Q(a), (a - 1, b1, b2)),                    # A -> 0
        (Q(a), (a, b1 + 1, b2)),                    # A -> A+B1
        (Q(2 * a * b1), (a, b1 - 1, b2)),           # A+B1 -> A
        (Q(a * b1), (a + 1, b1, b2)),               # A+B1 -> 2A+B1
        (Q(2 * a * (a - 1) * b1), (a - 1, b1, b2)), # 2A+B1 -> A+B1
        (Q(a), (a, b1, b2 + 1)),                    # A -> A+B2
        (Q(2 * a * b2), (a, b1, b2 - 1)),           # A+B2 -> A
        (Q(a * b2), (a + 1, b1, b2)),               # A+B2 -> 2A+B2
        (Q(2 * a * (a - 1) * b2), (a - 1, b1, b2)), # 2A+B2 -> A+B2
    ]
    total = Q(0)
    for rate, y in transitions:
        if rate:
            total += rate * (value(*y) - value(*x))
    return total


def main() -> None:
    values = [g(m) for m in range(10)]
    assert max(values) == Q(5156, 3125)
    assert values.index(max(values)) == 4
    assert g(10) == Q(-459022174, 48828125)
    assert g(10) < -9

    # Verify the exact difference formula over a finite diagnostic range;
    # monotonicity for every m>=10 follows from the displayed coefficient.
    for m in range(101):
        delta = g(m + 1) - g(m)
        exact_delta = 1 - Q(5 * m + 27, 75) * R**m
        assert delta == exact_delta
        if m >= 10:
            bound = 1 - Q(77, 75) * R**m
            assert delta <= bound < 0

    # Independently compare the displayed drift identity to the reaction
    # generator over a finite box, including reaction boundaries.
    for a in range(16):
        for b1 in range(16):
            for b2 in range(16):
                assert direct_drift(a, b1, b2) == formula_drift(a, b1, b2)

    # Exact finite witness: outside F = {1<=a<=3, b1,b2<=9}, the drift is
    # <= -1 on this diagnostic box.  The analytical proof extends globally.
    checked = 0
    max_outside = None
    for a in range(31):
        for b1 in range(26):
            for b2 in range(26):
                inside = 1 <= a <= 3 and b1 <= 9 and b2 <= 9
                if not inside:
                    lv = formula_drift(a, b1, b2)
                    assert lv <= -1, (a, b1, b2, lv)
                    max_outside = lv if max_outside is None else max(max_outside, lv)
                    checked += 1
    assert checked == 31 * 26 * 26 - 3 * 10 * 10
    assert max_outside == Q(-7, 5)

    # LP contradiction is an exact implication, not an optimization result:
    # 2w_i>lambda for both i implies w1+w2>lambda, contrary to lambda>w1+w2.
    print("PASS: Fraction-exact g values, difference identity, LP contradiction")
    print("PASS: direct generator equals formula on 16^3 boundary-inclusive states")
    print(f"PASS: LV<=-1 on {checked} exact grid states outside F; grid maximum={max_outside}")
    print("Scope: these finite checks do not replace the all-state proof in REPORT.txt")


if __name__ == "__main__":
    main()
