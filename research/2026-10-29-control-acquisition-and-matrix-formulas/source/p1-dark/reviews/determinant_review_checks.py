"""Reproduce only the narrow review counterexample and hull branch checks."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]


def read_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    d = read_module("determinant_review_helpers", ROOT / "selection/inference_determinant_tail_checks.py")
    h = read_module("hypograph_review_helpers", ROOT / "code/hypograph_control.py")
    q, k = F(9, 2), 4
    A = q ** k / factorial(k) / (1 - q / (k + 1))
    elo, ehi = d.exponential_interval(q)
    # The uncapped intermediate term in the original Eq. 14 exceeds one.
    # The corrected statement applies min(1,...) before the next inequality.
    assert A / ehi > 1
    rows = []
    for values, costs in [([F(1), F(4)], [F(0), F(1)]),
                          ([F(1), F(1), F(4)], [F(2), F(0), F(-1)]),
                          ([F(1), F(2), F(3)], [F(0), F(1), F(2)])]:
        result = h.optimize_hull(values, costs)
        i, j, t = result["mixture"]
        x = (1 - t) * values[i] + t * values[j]
        cost = (1 - t) * costs[i] + t * costs[j]
        assert F(0) <= t <= 1
        assert -1 / x - cost == result["feasible_hull_value"] <= result["certified_optimum_upper"]
        for i in range(len(values)):
            for j in range(i, len(values)):
                for numerator in (0, 1, 3, 7, 10):
                    t = F(numerator, 10)
                    x = (1 - t) * values[i] + t * values[j]
                    cost = (1 - t) * costs[i] + t * costs[j]
                    assert -1 / x - cost <= result["certified_optimum_upper"]
        rows.append({"values": values, "costs": costs, "result": result})
    u = [F(1, 17), F(1, 19), F(0)]
    actual = h.finite_command(u, 7)
    assert all(F(0) <= a <= b for a, b in zip(actual, u))
    assert sum(actual) <= sum(u) <= F(1, 5)
    receipt = {
        "scope": "Three targeted hull/root branch checks and one exact scalar counterexample; no broad run or whole-proof audit.",
        "eq14_counterexample": {"q": q, "k": k, "rational_A": A,
            "exp_q_interval": (elo, ehi), "middle_quantity_interval": (A / ehi, A / elo),
            "middle_lower_exceeds_one": True},
        "hypograph_cases": rows,
        "finite_command": {"nominal": u, "actual": actual},
        "all_targeted_assertions_passed": True,
    }
    (ROOT / "reviews/DETERMINANT_REVIEW_CHECKS.json").write_text(
        json.dumps(d.jsonable(receipt), indent=2) + "\n")
    print({"eq14_middle_lower": float(A / ehi), "targeted_hull_cases": len(rows),
           "all_targeted_assertions_passed": True})


if __name__ == "__main__":
    main()
