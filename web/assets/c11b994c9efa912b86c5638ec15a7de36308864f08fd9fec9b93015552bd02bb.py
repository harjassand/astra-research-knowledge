"""Exact two-cell witness that BMP/inhibitor means do not close pSMAD drift.

This checks only the source-reported local Hill response at h=1, Ki=1,
with g(0, 0)=0. It is a model-level calculation, not biological data.
"""
from fractions import Fraction
import json


def g(b: Fraction, inhibitor: Fraction) -> Fraction:
    if b == 0 and inhibitor == 0:
        return Fraction(0)
    return b / (b + inhibitor)


states = {
    "A": ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
    "B": ((Fraction(1), Fraction(1)), (Fraction(0), Fraction(0))),
}

result = {}
for name, cells in states.items():
    mean_b = sum(cell[0] for cell in cells) / len(cells)
    mean_i = sum(cell[1] for cell in cells) / len(cells)
    mean_signal_drift = sum(g(*cell) for cell in cells) / len(cells)
    result[name] = {
        "mean_b": str(mean_b),
        "mean_i": str(mean_i),
        "mean_pSMAD_drift": str(mean_signal_drift),
        "total_pSMAD_on_rate": str(sum(g(*cell) for cell in cells)),
    }

assert result["A"]["mean_b"] == result["B"]["mean_b"] == "1/2"
assert result["A"]["mean_i"] == result["B"]["mean_i"] == "1/2"
assert result["A"]["mean_pSMAD_drift"] == "1/2"
assert result["B"]["mean_pSMAD_drift"] == "1/4"
assert Fraction(result["A"]["mean_pSMAD_drift"]) - Fraction(
    result["B"]["mean_pSMAD_drift"]
) == Fraction(1, 4)

print(json.dumps(result, indent=2))
