"""Finite arithmetic diagnostics for the coprime-mass exactifier.

The report contains the proof. These checks are only finite consistency evidence.
"""
from fractions import Fraction
from math import gcd
import json
from pathlib import Path


def adjustment(a: int, b: int, denominator_bits: int):
    d = gcd(a, b)
    if d & (d - 1):
        raise ValueError("The numerator gcd has an odd divisor.")
    r = denominator_bits + 1
    target = 1 << (denominator_bits + r - 1)
    reduced_a, reduced_b = a // d, b // d
    residue = 0 if reduced_b == 1 else (
        (target // d) * pow(reduced_a, -1, reduced_b)
    ) % reduced_b
    maximum_k = target // a
    k = residue + ((maximum_k - residue) // reduced_b) * reduced_b
    ell = (target - a * k) // b
    return r, k, ell


checked = 0
excluded = 0
examples = []
for D in range(1, 9):
    denominator = 1 << D
    for a in range(denominator // 2, denominator + 1):
        for b in range(1, denominator + 1):
            d = gcd(a, b)
            if d & (d - 1):
                excluded += 1
                continue
            r, k, ell = adjustment(a, b, D)
            assert 0 <= k <= 1 << r
            assert 0 <= ell < a // d
            assert ell <= 1 << r
            assert a * k + b * ell == 1 << (D + r - 1)
            mass = (
                Fraction(1, 2) * Fraction(a, denominator) * Fraction(k, 1 << r)
                + Fraction(1, 2) * Fraction(b, denominator) * Fraction(ell, 1 << r)
            )
            assert mass == Fraction(1, 4)
            checked += 1
            if (D, a, b) in {(3, 5, 3), (3, 6, 2), (3, 4, 8)}:
                examples.append({"D": D, "a": a, "b": b, "r": r,
                                 "k": k, "ell": ell, "mass": str(mass)})

result = {"status": "passed", "scope": "finite arithmetic only",
          "D_range": [1, 8], "admissible_pairs_checked": checked,
          "odd_gcd_pairs_excluded": excluded, "examples": examples}
output = Path(__file__).with_name("logic_algorithms_check_results.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
