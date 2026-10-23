"""Exact finite-table checks for the weak-live CHSH source and upper witness.

The universal operator lower bound is proved in the companion text, not by
this replay.  No S/R/H, approximation theorem, or optimization is invoked.
"""
from itertools import product
from pathlib import Path
import json
import sympy as sp


def check() -> dict:
    I = sp.eye(2)
    Z = sp.diag(1, -1)
    X = sp.Matrix([[0, 1], [1, 0]])
    psi = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    obs_a = [Z, X]
    obs_b = [(Z + X) / sp.sqrt(2), (Z - X) / sp.sqrt(2)]
    omega = (1 + 1 / sp.sqrt(2)) / 2
    rows = []
    for x, y in product(range(2), repeat=2):
        original = {}
        classical = {}
        for a, b in product(range(2), repeat=2):
            pa = (I + (-1) ** a * obs_a[x]) / 2
            pb = (I + (-1) ** b * obs_b[y]) / 2
            probability = sp.simplify((psi.T * sp.kronecker_product(pa, pb) * psi)[0])
            expected = (1 + (-1) ** (a + b + x * y) / sp.sqrt(2)) / 4
            assert sp.simplify(probability - expected) == 0
            original[a, b] = probability
            classical[a, b] = sp.Rational(0)
        success_a = sp.Rational(0)
        success_b = sp.Rational(0)
        for detector, t, z in product(range(2), repeat=3):
            if detector == 0:
                a = z if x == t else None
                b = z ^ (t * y)
            else:
                a = z ^ (x * t)
                b = z if y == t else None
            success_a += sp.Rational(a is not None, 8)
            success_b += sp.Rational(b is not None, 8)
            if a is not None and b is not None:
                classical[a, b] += sp.Rational(1, 8)
        assert success_a == success_b == sp.Rational(3, 4)
        accepted = sum(p for (a, b), p in original.items() if (a ^ b) == x * y)
        assert sp.simplify(accepted - omega) == 0
        assert sum(classical.values()) == sp.Rational(1, 2)
        lam = 2 * omega
        for a, b in product(range(2), repeat=2):
            old_accepted = original[a, b] if (a ^ b) == x * y else sp.Rational(0)
            assert sp.simplify(lam * classical[a, b] - old_accepted) == 0
        rows.append({
            "x": x, "y": y,
            "source_acceptance": str(accepted),
            "source_conditional_PR": {
                f"{a}{b}": str(sp.simplify(original[a, b] / omega))
                if (a ^ b) == x * y else "0"
                for a, b in product(range(2), repeat=2)
            },
            "upper_witness_both_success": str(sum(classical.values())),
            "upper_witness_each_marginal": str(success_a),
        })
    lower_mass = sp.simplify(sp.sqrt(2) * omega)
    upper_mass = sp.simplify(sp.Rational(3, 2) * omega)
    assert lower_mass > 1
    return {
        "scope": "exact finite source and 3-shared-bit upper-witness table only",
        "universal_lower_bound_proved_in": "WEAK_LIVE_FILTER_CHSH_BOUNDARY.txt",
        "original_event_mass": str(omega),
        "upper_witness_scale": str(sp.simplify(2 * omega)),
        "minimum_max_one_sided_mass_lower_bound": str(lower_mass),
        "explicit_max_one_sided_mass_upper_bound": str(upper_mass),
        "quantum_optimal_mass": "UNKNOWN",
        "source_base_game_value": "1",
        "payoff_only_semantic_repair_obstructed": False,
        "rows": rows,
    }


if __name__ == "__main__":
    result = check()
    path = Path(__file__).with_name("weak_live_filter_exact_replay.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
