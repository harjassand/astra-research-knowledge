"""Exact algebra for an adaptive, costed scalar-experiment lower bound."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json


def run():
    checks = 0
    rows = []
    for m in [4, 8, 16, 64, 256, 1024]:
        e = F(1, m)
        lengths = sorted(set([0, 1, 2, 3, 4, m//2, m, 2*m, 5*m, 8*m]))
        for k in lengths:
            fa = (1+(1-2*e)**k)/2
            fb = (1-e)**k
            d = fa-fb
            assert 0 <= d <= min(e*e*k*(k-1)/2, F(1, 2))
            qa, qb = F(1, 4)+fa/2, F(1, 4)+fb/2
            assert F(1, 4) <= qa <= F(3, 4)
            assert F(1, 4) <= qb <= F(3, 4)
            chi_square = (qa-qb)**2/(qb*(1-qb))
            assert chi_square <= e*k/3
            checks += 1
        h = 5*m
        gap = (1+(1-2*e)**h)/2-(1-e)**h
        assert gap > F(49, 100)
        rows.append({"e": str(e), "future_length": h,
                     "future_amplitude_gap": float(gap),
                     "any_adaptive_expected_A_operations_lower": str(2/(3*e)),
                     "direct_test_samples": 64,
                     "direct_test_operations": 64*h})
    assert sum((F(5**n, factorial(n)) for n in range(20)), F(0)) > 100
    z = 64*F(49, 100)**2/8
    assert sum((z**n/factorial(n) for n in range(10)), F(0)) > 3
    result = {"exact_finite_checks": checks, "all_checks_passed": True,
              "proof_scope": "Arbitrary adaptive finite-word Bernoulli queries; cost is primitive applications, not computation or elapsed readout.",
              "lower_bound_expected_cost": "2/(3e) under source A for both testing errors at most 1/3",
              "matching_order_upper_bound_cost": "320/e for e=1/m, using 64 length-5m trials",
              "fixtures": rows}
    p = Path(__file__).resolve().parents[1]/"results"/"ADAPTIVE_COST_OBSTRUCTION.json"
    p.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
