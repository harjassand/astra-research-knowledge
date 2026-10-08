#!/usr/bin/env python3
"""Exact symbolic replay for the open-XY anisotropy/detuning exponents.

Requires SymPy. This checks the fixed-mode sine-kernel limit, the (1,2)
coefficient, the adjacent-mode low-q asymptotic, and exponent comparisons.
It does not numerically diagonalize a Gibbs state or prove state convergence
outside the compact regime a>=1,b>=2.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


def main() -> None:
    x, k, ell = sp.symbols("x k ell", positive=True)

    # Since x=pi/L, L*B_{L,k,ell} is exactly this function of x.
    L_times_B = -4 * sp.sin(k * x) * sp.sin(ell * x) / (
        sp.cos(k * x) - sp.cos(ell * x)
    )
    generic_limit = sp.simplify(sp.limit(L_times_B, x, 0))
    expected_generic = -8 * k * ell / (ell**2 - k**2)
    assert sp.simplify(generic_limit - expected_generic) == 0

    L_times_B_12 = sp.simplify(L_times_B.subs({k: 1, ell: 2}))
    limit_12 = sp.simplify(sp.limit(L_times_B_12, x, 0))
    assert limit_12 == sp.Rational(-16, 3)
    # K_12=-2 tau J kappa L^(1-a) * (L B_12).
    K12_prefactor = sp.simplify(-2 * limit_12)
    assert K12_prefactor == sp.Rational(32, 3)

    # For adjacent modes, first take q=pi/L -> 0 at fixed k, then k -> inf.
    L_times_B_adj = -4 * sp.sin(k * x) * sp.sin((k + 1) * x) / (
        sp.cos(k * x) - sp.cos((k + 1) * x)
    )
    fixed_k_adj = sp.simplify(sp.limit(L_times_B_adj, x, 0))
    expected_fixed_k_adj = -8 * k * (k + 1) / (2 * k + 1)
    assert sp.simplify(fixed_k_adj - expected_fixed_k_adj) == 0
    large_k_ratio = sp.simplify(sp.limit(fixed_k_adj / k, k, sp.oo))
    assert large_k_ratio == -4
    # Therefore K_{k,k+1} ~ 8 tau J kappa L^(1-a) k for 1<<k<<L.

    cases = []
    for a_text, b_text in [
        ("3/2", "2"),
        ("1", "2"),
        ("1/2", "2"),
        ("1", "5/2"),
        ("3/4", "3/2"),
        ("1/2", "3/2"),
    ]:
        a = Fraction(a_text)
        b = Fraction(b_text)
        pair_power = 1 - a
        detuning_power = 2 - b
        fixed_pair_over_field_power = b - a - 1
        shell_pair_over_kinetic_power = Fraction(1, 2) * b - a
        cases.append(
            {
                "a": str(a),
                "b": str(b),
                "scaled_pairing_power_fixed_modes": str(pair_power),
                "scaled_detuning_power_fixed_modes": str(detuning_power),
                "fixed_mode_pair_over_detuning_power": str(
                    fixed_pair_over_field_power
                ),
                "moving_shell_pair_over_kinetic_power_0_lt_b_lt_2": str(
                    shell_pair_over_kinetic_power
                ),
            }
        )

    output = {
        "status": "PASS",
        "scope": "exact symbolic coefficient and exponent replay only",
        "identities": {
            "limit_LB_general_fixed_k_ell": str(generic_limit),
            "limit_LB_12": str(limit_12),
            "K12_leading_coefficient_of_tau_J_kappa_L_power": str(
                K12_prefactor
            ),
            "limit_LB_k_kplus1_fixed_k": str(fixed_k_adj),
            "large_k_limit_LB_adjacent_divided_by_k": str(large_k_ratio),
            "adjacent_K_asymptotic": (
                "8*tau*J*kappa*L^(1-a)*k for 1<<k<<L"
            ),
            "critical_effective_parameters": {
                "lambda_eff": "lambda*L^(2-b)",
                "kappa_eff": "kappa*L^(1-a)",
            },
            "moving_shell": {
                "domain": "0<b<2 and lambda>0",
                "k_F_order": "L^(1-b/2)",
                "pair_over_kinetic_order": "L^(b/2-a)",
            },
        },
        "exponent_cases": cases,
        "state_level_limit_checked": False,
    }
    out_path = Path(__file__).with_name("exact_scaling_replay.json")
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
