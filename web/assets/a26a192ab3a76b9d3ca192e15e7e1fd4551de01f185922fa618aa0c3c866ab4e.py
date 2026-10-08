#!/usr/bin/env python3
"""Exact small-size checks for the negative scaled-coupling trial state.

Requires SymPy.  These checks verify the product-state norm, N, W, and the
full occupation-basis Hcrit expectation for two nontrivial ramp profiles.
They are finite algebraic diagnostics, not a proof of the asymptotic result.
Run from the repository root:
  python3 outputs/research/fermionic_algorithms/cycle2/negative_scaled_coupling/checks.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def profile(L: int, w: int):
    S = L - 1
    assert 2 * w + 1 <= S
    out = []
    for i in range(1, S + 1):
        if i <= w + 1:
            q = sp.Rational(i - 1, w)
        elif i <= S - w:
            q = sp.Integer(1)
        else:
            q = sp.Rational(S - i, w)
        out.append(sp.pi * q)
    return out


def simplify_zero(x):
    return sp.simplify(sp.trigsimp(sp.expand_trig(x))) == 0


def check_case(L: int, w: int):
    S = L - 1
    theta = profile(L, w)
    c = [sp.cos(t / 2) for t in theta]
    s = [sp.sin(t / 2) for t in theta]
    amplitudes = {}
    for mask in range(1 << S):
        a = sp.Integer(1)
        for i in range(S):
            a *= s[i] if (mask >> i) & 1 else c[i]
        amplitudes[mask] = sp.simplify(a)

    norm = sp.simplify(sum(a * a for a in amplitudes.values()))
    n_expect = sp.simplify(
        sum(a * a * mask.bit_count() for mask, a in amplitudes.items())
    )
    w_expect = sp.Integer(0)
    diagonal = sp.Integer(0)
    hopping = sp.Integer(0)
    for mask, a in amplitudes.items():
        occ = mask.bit_count()
        pairs = sum(((mask >> i) & 1) * ((mask >> (i + 1)) & 1)
                    for i in range(S - 1))
        diagonal += a * a * 4 * (occ - pairs)  # J=1
        for i in range(S - 1):
            if ((mask >> i) & 1) and not ((mask >> (i + 1)) & 1):
                other = mask ^ (1 << i) ^ (1 << (i + 1))
                hopping += -4 * a * amplitudes[other]  # both Hermitian entries
        w_expect += a * a * pairs
    hcrit = sp.simplify(diagonal + hopping)

    # Independent single-site product identities, including the open ends.
    hcrit_spin = sp.simplify(
        sum(1 - sp.cos(theta[i + 1] - theta[i]) for i in range(S - 1))
        + (1 - sp.cos(theta[0])) + (1 - sp.cos(theta[-1]))
    )
    hcrit_expected = sp.simplify(2 * w * (1 - sp.cos(sp.pi / w)))
    n_expected = L - w - 2
    w_expected = sp.simplify(
        L - sp.Rational(3, 2) * w - 2 + sp.Rational(w, 4) * sp.cos(sp.pi / w)
    )

    assert simplify_zero(norm - 1)
    assert simplify_zero(n_expect - n_expected)
    assert simplify_zero(w_expect - w_expected)
    assert simplify_zero(hcrit - hcrit_spin)
    assert simplify_zero(hcrit - hcrit_expected)
    return {
        "L": L,
        "sites": S,
        "w": w,
        "norm_exact": str(norm),
        "N_exact": str(sp.simplify(n_expect)),
        "W_exact": str(sp.simplify(w_expect)),
        "Hcrit_exact_J1": str(hcrit),
        "checks": ["norm", "N", "W", "hopping+diagonal Hcrit", "spin-form endpoints"],
    }


def main():
    cases = [check_case(6, 2), check_case(8, 3), check_case(10, 4)]
    out = {
        "status": "FINITE-EXACT-ALGEBRAIC-CHECKS-PASS",
        "cases": cases,
        "limitations": (
            "Small-size exact identities only; no asymptotic theorem, partition "
            "function computation, or external review is established by this script."
        ),
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
