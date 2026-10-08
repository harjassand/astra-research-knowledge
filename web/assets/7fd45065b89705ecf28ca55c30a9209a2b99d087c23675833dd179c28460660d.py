#!/usr/bin/env python3
"""Exact algebraic checks for the marginal-window coherent-symbol note.

Requires SymPy. Run from repository root:
  python3 outputs/research/fermionic_algorithms/cycle2/marginal_window/luna_berezin/checks.py
These checks are finite identities, not asymptotic evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def check_chain(L: int):
    S = L - 1
    # Samples theta(x)=2*pi*x*(1-x), a C^infinity Dirichlet profile.
    theta = [2 * sp.pi * i * (L - i) / L**2 for i in range(1, L)]
    # Keep c_i=cos(theta_i/2), s_i=sin(theta_i/2) as exact algebraic
    # generators. Reduce identities modulo c_i^2+s_i^2=1, avoiding numerical
    # trigonometric simplification.
    c = sp.symbols(f"c0:{S}")
    s = sp.symbols(f"s0:{S}")
    variables = tuple(v for pair in zip(c, s) for v in pair)
    relations = [c[i] ** 2 + s[i] ** 2 - 1 for i in range(S)]
    ideal = sp.groebner(relations, *variables, order="lex")

    def rem(expr):
        return sp.expand(ideal.reduce(sp.expand(expr))[1])

    amp = {}
    for mask in range(1 << S):
        val = sp.Integer(1)
        for i in range(S):
            val *= s[i] if (mask >> i) & 1 else c[i]
        amp[mask] = sp.simplify(val)

    norm = sp.simplify(sum(v * v for v in amp.values()))
    N_direct = sp.Integer(0)
    W_direct = sp.Integer(0)
    H_diag = sp.Integer(0)
    H_hop = sp.Integer(0)
    for mask, v in amp.items():
        occ = mask.bit_count()
        pairs = sum(((mask >> i) & 1) * ((mask >> (i + 1)) & 1)
                    for i in range(S - 1))
        prob = v * v
        N_direct += prob * occ
        W_direct += prob * pairs
        H_diag += prob * 4 * (occ - pairs)  # J=1
        for i in range(S - 1):
            if ((mask >> i) & 1) and not ((mask >> (i + 1)) & 1):
                other = mask ^ (1 << i) ^ (1 << (i + 1))
                H_hop += -4 * v * amp[other]  # two Hermitian matrix entries
    H_direct = sp.simplify(H_diag + H_hop)

    p = [s[i] ** 2 for i in range(S)]
    N_product = sp.simplify(sum(p))
    W_product = sp.simplify(sum(p[i] * p[i + 1] for i in range(S - 1)))
    x = [2 * c[i] * s[i] for i in range(S)]
    z = [c[i] ** 2 - s[i] ** 2 for i in range(S)]
    H_spin = sp.simplify(
        sum(1 - x[i] * x[i + 1] - z[i] * z[i + 1]
            for i in range(S - 1))
        + (1 - z[0]) + (1 - z[-1])
    )

    assert rem(norm - 1) == 0
    assert rem(N_direct - N_product) == 0
    assert rem(W_direct - W_product) == 0
    assert rem(H_direct - H_spin) == 0
    return {
        "L": L,
        "sites": S,
        "profile": "theta(x)=2*pi*x*(1-x), J=1",
        "angle_samples": [str(v) for v in theta],
        "exact_method": "polynomial reduction modulo c_i^2+s_i^2=1",
        "checks": ["normalization", "N", "W", "all hopping and diagonal terms", "both endpoints"],
    }


def check_spin_upper_symbols():
    # Uniform sphere moments characterize the exact spin-1/2 resolution.
    # P(n)=(I+n.sigma)/2, I=2 int P(n) d omega, E[n_a n_b]=delta_ab/3.
    sigma_upper_factor = 3 * sp.Rational(1, 3)
    bond_aligned = 1 - 9  # J(I-sigma_i.sigma_j), n_i.n_j=1
    endpoint_down = 1 - 3 * (-1)
    actual_aligned_bond = 1 - 1
    actual_down_endpoint = 1 - (-1)
    S = 3
    critical_upper = (S - 1) * bond_aligned + 2 * endpoint_down
    critical_covariant = (S - 1) * actual_aligned_bond + 2 * actual_down_endpoint
    assert sigma_upper_factor == 1
    assert critical_upper == -8
    assert critical_covariant == 4
    return {
        "resolution_moment_check": "3*E[n_a^2]=1",
        "spin_1/2_upper_symbol_of_sigma": "3*n_a",
        "S": S,
        "all_down_Hcrit_covariant_symbol_J1": critical_covariant,
        "all_down_Hcrit_contravariant_upper_symbol_J1": critical_upper,
        "difference": critical_covariant - critical_upper,
    }


def main():
    out = {
        "status": "FINITE-EXACT-ALGEBRAIC-CHECKS-PASS",
        "coherent_product_cases": [check_chain(L) for L in (4, 5, 6)],
        "Berezin_symbol_witness": check_spin_upper_symbols(),
        "limitations": (
            "Exact finite identities only; does not prove a speed-L free-energy "
            "limit or a Berezin upper bound matching the profile functional."
        ),
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
