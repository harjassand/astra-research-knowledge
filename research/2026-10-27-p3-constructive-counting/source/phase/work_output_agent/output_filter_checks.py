#!/usr/bin/env python3
"""Exact checks of output-specific residual degree/precision statements."""
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def parity_chi(e):
    return (-1) ** sum(e)


def run():
    rows = []
    monomial_checks = 0
    for s in range(1, 11):
        cube = list(product((0, 1), repeat=s))
        for d in range(s):
            for subset in combinations(range(s), d):
                val = sum(parity_chi(e) * product_value(e, subset) for e in cube)
                assert val == 0
                monomial_checks += 1
        weights = [Fraction(1 + parity_chi(e), 2**s) for e in cube]
        assert sum(weights) == 1
        assert sum(w * Fraction(1 + parity_chi(e), 2) for w, e in zip(weights, cube)) == 1
        admitted = sum(sum(e) % 2 == 0 for e in cube)
        assert admitted == 2 ** (s - 1)
        n = 3
        t = s - 1
        modulus = 2 ** (t + n)
        assert (2**t * 0) % modulus == (2**t * 2**n) % modulus
        fine_modulus = 2 ** (t + n + 1)
        assert len({2**t * z % fine_modulus for z in range(2**n + 1)}) == 2**n + 1
        rows.append({"states": s, "filter_rank": 1, "admitted_errors": admitted,
                     "selector_mass": "1", "selected_even_parity_mass": "1",
                     "n_plus_multiplicity_bits_ambiguous": True,
                     "one_extra_bit_distinguishes_all_counts": True})
    odd_modulus_checks = []
    for p in [3, 5, 7, 11, 13, 17, 19]:
        for m in range(1, p):
            values = [int(y % 2 == 0) for y in range(m+1)]
            diff = sum((-1)**(m-j) * comb(m, j) * values[j] for j in range(m+1))
            expected = (-2)**m // 2
            assert diff == expected
            assert diff % p != 0
            odd_modulus_checks.append({"prime": p, "m": m, "difference_mod_p": diff % p})
        assert 0 % p == p % p and (0 % 2) != (p % 2)
    return {"all_passed": True, "monomial_orthogonality_checks": monomial_checks,
            "state_fixtures": rows, "odd_modulus_checks": odd_modulus_checks,
            "scope": "Exact identities only; no speed claim."}


def product_value(e, indices):
    value = 1
    for j in indices:
        value *= e[j]
    return value


if __name__ == "__main__":
    result = run()
    path = Path(__file__).with_name("output_filter_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_passed": result["all_passed"],
                      "monomial_orthogonality_checks": result["monomial_orthogonality_checks"],
                      "state_fixtures": len(result["state_fixtures"]),
                      "odd_modulus_checks": len(result["odd_modulus_checks"])}))
