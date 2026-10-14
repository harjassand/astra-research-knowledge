#!/usr/bin/env python3
"""Exact algebra/trigonometric checks for FJ contact compensation generalization."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def normalized_average(expr, x, y):
    return sp.simplify(
        sp.integrate(sp.integrate(sp.expand_trig(expr), (x, 0, 2 * sp.pi)), (y, 0, 2 * sp.pi))
        / (4 * sp.pi**2)
    )


def check_polynomial_conditions():
    a, b, c, d = sp.symbols("a b c d", real=True)
    r = d - a

    wave_null = a * (a * d - b * c)
    assert sp.expand(wave_null - (a**3 + a**2 * r - a * b * c)) == 0
    assert sp.diff(wave_null, b, 2) == 0
    assert sp.expand(wave_null.subs({c: 0, d: a}) - a**3) == 0

    bad = b**2 * c
    assert sp.expand(bad.subs({c: 0, d: a})) == 0
    assert sp.diff(bad, b, 2) == 2 * c

    p, q, u, v = sp.symbols("p q u v", real=True)
    rank_one = sp.Matrix([[p * u, p * v], [q * u, q * v]])
    assert sp.expand(wave_null.subs({a: rank_one[0, 0], b: rank_one[0, 1],
                                     c: rank_one[1, 0], d: rank_one[1, 1]})) == 0
    return {
        "wave_null_cubic_restriction": "C|U=a^3",
        "wave_null_cubic_b_second_derivative": "0",
        "bad_cubic_restriction": "C|U=0",
        "bad_cubic_b_second_derivative": "2c",
        "rank_one_substitution": "det(A) A11 vanishes identically",
    }


def check_nonzero_resonance():
    x, y = sp.symbols("x y", real=True)
    phi1 = sp.sin(x) + sp.sin(y)
    phi2 = sp.sin(x + y)
    a = sp.diff(phi1, x)
    b = sp.diff(phi1, y)
    c = sp.diff(phi2, x)
    d = sp.diff(phi2, y)
    cubic = a * (a * d - b * c)
    value = normalized_average(cubic, x, y)
    assert value == -sp.Rational(1, 4), value
    return {"detA_A11_resonant_average": str(value)}


def check_compatible_failure():
    x, y = sp.symbols("x y", real=True)
    values = {}
    for n_value in (1, 2, 5):
        n = sp.Integer(n_value)
        a = 2 * sp.sin(x) * sp.sin(n * y) / n
        b = -2 * sp.cos(x) * sp.cos(n * y) - sp.cos(2 * n * y)
        c = -2 * sp.cos(x) * sp.cos(n * y) / n**2
        d = a
        energy = normalized_average(c**2 + (d - a) ** 2, x, y)
        cubic = normalized_average(b**2 * c, x, y)
        assert energy == sp.Rational(1, n_value**4), (n_value, energy)
        assert cubic == -sp.Rational(1, n_value**2), (n_value, cubic)
        values[str(n_value)] = {"average_energy": str(energy), "average_cubic": str(cubic)}
    return {
        "sequence": "psi_n=n^-2 cos(ny-x)+n^-2 cos(ny+x)+(4n^2)^-1 cos(2ny); phi=(psi_y,psi_x)",
        "exact_integer_frequency_checks": values,
        "analytic_formulas_in_proof": "average Q=n^-4; average b^2 c=-n^-2 for every integer n>=1",
    }


def check_scaling_thresholds():
    p, q = sp.symbols("p q", positive=True)
    field_norm_power = sp.simplify(2 / p - sp.Rational(1, 2))
    rhs_power_lowered_field = sp.simplify(sp.Rational(1, 2) + field_norm_power)
    ratio_power_lowered_field = sp.simplify(sp.Rational(1, 2) - rhs_power_lowered_field)
    defect_norm_power = sp.simplify(2 / q - sp.Rational(1, 2))
    ratio_power_lowered_defect = sp.simplify(sp.Rational(1, 2) - defect_norm_power)
    assert sp.simplify(rhs_power_lowered_field - 2 / p) == 0
    assert sp.simplify(ratio_power_lowered_field - (sp.Rational(1, 2) - 2 / p)) == 0
    assert sp.simplify(ratio_power_lowered_defect - (1 - 2 / q)) == 0
    return {
        "field_Lp_norm_power_under_concentration": str(field_norm_power),
        "field_slot_rhs_power_if_p_replaces_4": str(rhs_power_lowered_field),
        "field_slot_ratio_power": str(ratio_power_lowered_field),
        "defect_Lq_norm_power_under_concentration": str(defect_norm_power),
        "defect_slot_ratio_power": str(ratio_power_lowered_defect),
        "sharp_thresholds": "field p>=4; defect q>=2 for this factorized scaling",
    }


def main():
    result = {
        "status": "PASS",
        "scope": "exact finite algebra and trigonometric diagnostics only; analytic inequalities are proved in PROOF.md",
        "checks": {
            "polynomial_conditions": check_polynomial_conditions(),
            "nonzero_resonance": check_nonzero_resonance(),
            "compatible_failure": check_compatible_failure(),
            "scaling_thresholds": check_scaling_thresholds(),
        },
    }
    out = Path(__file__).with_name("verification.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
