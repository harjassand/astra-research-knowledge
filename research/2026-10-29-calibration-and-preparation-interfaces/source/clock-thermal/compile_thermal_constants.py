#!/usr/bin/env python3
"""Compile the GENERAL rational sufficient gate; no Hamiltonian is sampled.

This pays integer size and inequality checks for the source's admitted
q,d,L bounds. It does not numerically verify the analytic cylinder theorem,
qualify the old literal clock recipe, or acquire physical data.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from time import perf_counter


def compile_gate(q: int, d: int, L: int) -> dict:
    if min(q, d) < 1 or L < 3:
        raise ValueError("q,d>=1 and L>=3 are required")
    start = perf_counter()
    degree = d * (q - 1) + 2
    K = degree + 1
    eps_den = 16 * (K + 1) * K**2
    A0 = L * 2**d * eps_den
    delta0 = A0.bit_length()
    power_two = 8 * q * delta0
    Dthermal = 4 * delta0 * A0**q * 2**power_two

    # The old KT choice uses J=d and rho=(64*q*d*L**q)^(-1).
    rho_den = 64 * q * d * L**q
    Dground = 12 * rho_den**L
    Dchosen = max(Dthermal, Dground)
    Delta = Dchosen**L // 4
    assert 4 * Delta == Dchosen**L
    BDelta = Delta.bit_length()
    Mcrit = 2 * (BDelta + 4)

    assert 2**delta0 >= A0
    assert Dchosen >= Dthermal
    assert Dchosen >= Dground
    assert 4 * delta0 * A0**q * 2**power_two <= Dchosen
    # x<=eta**q/2, then exp(x)-1<=2*x<=eta**q.
    assert 2 * delta0 * 2**power_two * 2 * A0**q <= Dchosen
    epsilon = Fraction(L * 2**d, A0)
    assert epsilon == Fraction(1, eps_den)
    b_upper = 8 * K**2 * epsilon  # exp(2)<8
    assert b_upper == Fraction(1, 2 * (K + 1))
    Bstar = b_upper / (1 - b_upper)
    assert Bstar == Fraction(1, 2 * K + 1)
    assert K * Bstar < 1
    # At beta>=1, this ensures floor(beta*Delta/delta0)>=Mcrit.
    beta_one_height_gate = Delta >= delta0 * (Mcrit + 1)

    return {
        "q": q,
        "d_incident_native_hops": d,
        "L_clock_dimension": L,
        "spacetime_degree_bound": degree,
        "K": K,
        "epsilon_upper_exact": f"1/{eps_den}",
        "A0_exact": str(A0),
        "delta0_integer": delta0,
        "lambda_T_exact_factorization": {
            "numerator": 1,
            "denominator": "4*delta0*A0**q*2**power_two",
            "power_two": power_two,
        },
        "lambda_T_denominator_bits": Dthermal.bit_length(),
        "lambda_ground_denominator_bits": Dground.bit_length(),
        "chosen_lambda": "min(lambda_T,lambda_ground)",
        "chosen_is_thermal_gate": Dthermal >= Dground,
        "chosen_lambda_denominator_bits": Dchosen.bit_length(),
        "Delta_exact_factorization": "chosen_lambda_denominator**L/4",
        "Delta_integer_bits": BDelta,
        "Delta_times_lambda_integer_bits": (Dchosen ** (L - 1) // 4).bit_length(),
        "Bstar_exact": f"1/{2*K+1}",
        "Mcrit_integer": Mcrit,
        "beta_at_least_one_meets_height_gate": beta_one_height_gate,
        "physical_beta_sufficient": (
            "beta>=1 and beta>2*beta_c" if beta_one_height_gate
            else "beta>2*beta_c and floor(beta*Delta/delta0)>=max(3,Mcrit)"
        ),
        "large_integer_decimal_output": "OMITTED; factorization and exact bit bounds retained",
        "scope": "general rational gate composition only; no Hamiltonian model or physical run",
        "ordinary_analytic_inequalities_used": [
            "exp(1)<4", "exp(2)<8", "exp(x)-1<=2*x for 0<=x<=1/2", "exp(1)>2"
        ],
        "arbitrary_physical_Hamiltonian_errors": "NOT_INCLUDED",
        "old_literal_recipe_thermal_qualification": "NOT_ACQUIRED",
        "wall_seconds_after_imports": perf_counter() - start,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=43)
    ap.add_argument("--d", type=int, default=344)
    ap.add_argument("--L", type=int, default=8)
    ap.add_argument("--output", type=Path, default=Path(__file__).with_name("THERMAL_CONSTANTS.json"))
    ns = ap.parse_args()
    result = compile_gate(ns.q, ns.d, ns.L)
    ns.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
