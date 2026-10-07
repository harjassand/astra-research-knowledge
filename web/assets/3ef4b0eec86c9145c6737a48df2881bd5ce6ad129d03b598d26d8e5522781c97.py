#!/usr/bin/env python3
"""Exact, bounded reconstruction checks for the N77 reaction example.

This is finite algebra evidence only; the report contains the uniform derivation.
Uses Python standard-library exact integers and Fractions.
"""
from fractions import Fraction
from math import factorial
import json
from pathlib import Path

REACTIONS = [
    ((0, 0, 2, 0), (1, 1, 1, 0)),  # 2C -> A+B+C
    ((1, 1, 1, 0), (3, 2, 0, 0)),  # A+B+C -> 3A+2B
    ((3, 2, 0, 0), (0, 0, 2, 0)),  # 3A+2B -> 2C
    ((0, 0, 2, 0), (0, 0, 2, 1)),  # 2C -> 2C+D
    ((0, 0, 2, 1), (0, 0, 2, 0)),  # 2C+D -> 2C
]


def falling(x, k):
    out = 1
    for j in range(k):
        out *= x - j
    return out if x >= k else 0


def propensity(x, reactants):
    out = 1
    for xi, yi in zip(x, reactants):
        out *= falling(xi, yi)
    return out


def invariant(x):
    a, b, _, _ = x
    return a - b * (b + 1) // 2


# Check the alleged nonlinear invariant against every enabled reaction in a
# bounded slice of the integer plane B+C=2.
invariant_transitions = 0
for a in range(13):
    for b in range(3):
        c = 2 - b
        for d in range(4):
            x = (a, b, c, d)
            for reactants, products in REACTIONS:
                rate = propensity(x, reactants)
                if rate:
                    y = tuple(xi - ri + pi for xi, ri, pi in zip(x, reactants, products))
                    assert y[1] + y[2] == 2
                    assert invariant(y) == invariant(x)
                    invariant_transitions += 1

# Outside the plane the same state function is not a stochastic invariant.
x = (2, 1, 2, 0)  # 2C reaction is enabled; B+C=3.
reactants, products = REACTIONS[0]
y = tuple(xi - ri + pi for xi, ri, pi in zip(x, reactants, products))
assert invariant(y) - invariant(x) == -1

# The continuous extension N(a,b)=a-b(b+1)/2 is not a first integral of
# the deterministic mass-action ODE, even on B+C=2.
a, b, c = Fraction(2), Fraction(1, 2), Fraction(3, 2)
dot_a = c**2 + 2*a*b*c - 3*a**3*b**2
dot_b = c**2 + a*b*c - 2*a**3*b**2
dot_n = dot_a - (b + Fraction(1, 2)) * dot_b
assert b + c == 2 and dot_n == Fraction(-1, 2)

# Exact stationary-balance checks on the three-phase class Gamma_n x Z_+.
stationary_states_checked = 0
for n in range(13):
    p = (n + 1) * (n + 2) * (n + 3)
    phase_rates = (2, n + 1, 2 * p)
    phase_weights = (Fraction(1, 2), Fraction(1, n + 1), Fraction(1, 2 * p))
    for phase in range(3):
        prev = (phase - 1) % 3
        for d in range(10):
            qd = Fraction(1, factorial(d))  # common e^-1 factor omitted
            incoming = phase_weights[prev] * phase_rates[prev] * qd
            outgoing = phase_weights[phase] * phase_rates[phase] * qd
            if phase == 0:
                if d:
                    incoming += phase_weights[0] * Fraction(1, factorial(d - 1)) * 2
                incoming += phase_weights[0] * Fraction(1, factorial(d + 1)) * 2 * (d + 1)
                outgoing += phase_weights[0] * qd * (2 + 2 * d)
            assert incoming == outgoing
            stationary_states_checked += 1

# Exact phase-probability formula and escaping observables.
phase_formulas = []
for n in range(13):
    P = (n + 1) * (n + 2) * (n + 3)
    z = P + 2 * (n + 2) * (n + 3) + 1
    p0 = Fraction(P, z)
    p1 = Fraction(2 * (n + 2) * (n + 3), z)
    p2 = Fraction(1, z)
    assert p0 + p1 + p2 == 1
    ea = n * p0 + (n + 1) * p1 + (n + 3) * p2
    assert ea == Fraction(n) + Fraction(2*n*n + 10*n + 15, z)
    assert p0 > Fraction(1, 1) - Fraction(3, n + 1) if n else True
    phase_formulas.append({"n": n, "p_phase0": str(p0), "p_phase1": str(p1), "p_phase2": str(p2), "E_A": str(ea)})

result = {
    "scope": "bounded exact checks; not proof certification",
    "method": "Python standard-library integer/Fraction arithmetic; no simulation",
    "plane_invariant_transitions_checked": invariant_transitions,
    "outside_plane_witness": {"source": x, "target": y, "delta_invariant": invariant(y) - invariant(x)},
    "deterministic_derivative_witness": {"a": "2", "b": "1/2", "c": "3/2", "B_plus_C": "2", "dN_dt": str(dot_n)},
    "stationary_balance_states_checked": stationary_states_checked,
    "phase_probabilities_and_EA": phase_formulas,
    "formula": "p0=P/Z, p1=2(n+2)(n+3)/Z, p2=1/Z; Z=n^3+8n^2+21n+19; E[A]=n+(2n^2+10n+15)/Z",
}
out = Path(__file__).with_name("exact_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("plane_invariant_transitions_checked", "outside_plane_witness", "deterministic_derivative_witness", "stationary_balance_states_checked")}, indent=2))
