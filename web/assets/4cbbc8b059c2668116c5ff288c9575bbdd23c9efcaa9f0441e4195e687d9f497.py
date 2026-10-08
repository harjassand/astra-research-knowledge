#!/usr/bin/env python3
"""Exact symbolic replay of the matched-port thermal reciprocity witness."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def main() -> None:
    t, s = sp.symbols("t s", positive=True, real=True)
    C = sp.diag(1, 4)
    K = sp.Matrix([[1, -1], [-1, 1]])
    A = C.inv() * K
    q = sp.exp(-sp.Rational(5, 4) * t)
    E = sp.Matrix(
        [
            [(1 + 4 * q) / 5, 4 * (1 - q) / 5],
            [(1 - q) / 5, (4 + q) / 5],
        ]
    )
    H = sp.simplify(E * C.inv())
    H_resolvent = (K + s * C).inv()

    assert sp.simplify(A**2 - sp.Rational(5, 4) * A) == sp.zeros(2)
    assert sp.simplify(E[0, 1] - 4 * E[1, 0]) == 0
    assert sp.simplify(H[0, 1] - H[1, 0]) == 0
    assert sp.simplify(H_resolvent[0, 1] - H_resolvent[1, 0]) == 0
    assert sp.simplify((E[0, 1] - E[1, 0]) / (E[0, 1] + E[1, 0])) == sp.Rational(3, 5)

    q1 = sp.exp(-sp.Rational(5, 4))
    numeric = {
        "time": 1.0,
        "q": float(q1),
        "same_initial_deltaT": {
            "T2_response_from_node1": float(E[1, 0].subs(t, 1)),
            "T1_response_from_node2": float(E[0, 1].subs(t, 1)),
            "ratio": 4.0,
            "symmetric_contrast": 0.6,
        },
        "unit_energy_power_impulses": {
            "T2_response_from_node1": float(H[1, 0].subs(t, 1)),
            "T1_response_from_node2": float(H[0, 1].subs(t, 1)),
            "difference": 0.0,
        },
        "exact_checks": [
            "A^2=(5/4)A",
            "E_12=4 E_21",
            "(E C^-1)_12=(E C^-1)_21",
            "((K+sC)^-1)_12=((K+sC)^-1)_21",
        ],
        "scope": "exact 2-node reciprocal RC fixture only; not a physical-material validation",
    }
    out = Path(__file__).with_name("two_node_replay_output.json")
    out.write_text(json.dumps(numeric, indent=2) + "\n")
    print(json.dumps(numeric, indent=2))


if __name__ == "__main__":
    main()
