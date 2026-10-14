"""Exact arithmetic check of baseline-indistinguishable mass-action networks."""

from fractions import Fraction as F


def rates(a: F, b: F, detailed_balance: bool) -> tuple[F, F]:
    if detailed_balance:
        # 0 <-> A and B <-> A+B, with both directions equal at A=B=1.
        return F(3, 2) + F(3, 2) * b, F(3, 2) * a + F(3, 2) * a * b
    return F(2) + b, a + F(2) * a * b


for balanced in (False, True):
    label = "pairwise balanced" if balanced else "cancelling currents"
    forward, backward = rates(F(1), F(1), balanced)
    print(label, "baseline (+,-,drift,Q_AA):", forward, backward,
          forward-backward, forward+backward)
    forward, backward = rates(F(1), F(2), balanced)
    print(label, "B=2 (+,-,drift):", forward, backward,
          forward-backward)
    forward, backward = rates(F(11, 10), F(1, 4), balanced)
    print(label, "A=11/10,B=1/4 drift:", forward-backward)
