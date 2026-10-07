#!/usr/bin/env python3
"""Bounded exact diagnostics for the N77 lattice-class revision.

The infinite classification and limits are proved in DEEPER_ATTACK.txt; this
script only checks the transcription on bounded ranges using integers and
fractions.
"""
from fractions import Fraction
from math import factorial
import json
from pathlib import Path


def rates(x):
    a, b, c, d = x
    fall = lambda z, k: 0 if z < k else factorial(z) // factorial(z - k)
    return [
        fall(c, 2),
        a * b * c,
        fall(a, 3) * fall(b, 2),
        fall(c, 2),
        fall(c, 2) * d,
    ]


DELTAS = [(1, 1, -1, 0), (2, 1, -1, 0), (-3, -2, 2, 0),
          (0, 0, 0, 1), (0, 0, 0, -1)]


def successor(x, delta):
    return tuple(v + dv for v, dv in zip(x, delta))


def class_key(x):
    a, b, c, d = x
    assert b + c == 2 and min(x) >= 0
    n = a - b * (b + 1) // 2
    if n >= 0:
        return ("Gamma", n)
    return ("absorbing-singleton", x)


checked_states = 0
checked_transitions = 0
absorbing_states = 0
for a in range(31):
    for b, c in ((0, 2), (1, 1), (2, 0)):
        for d in range(5):
            x = (a, b, c, d)
            key = class_key(x)
            enabled = 0
            for rate, delta in zip(rates(x), DELTAS):
                if rate == 0:
                    continue
                enabled += 1
                y = successor(x, delta)
                assert min(y) >= 0 and y[1] + y[2] == 2
                assert class_key(y) == key
                checked_transitions += 1
            if key[0] == "absorbing-singleton":
                assert enabled == 0
                absorbing_states += 1
            checked_states += 1


cycle_flux_checks = 0
for n in range(101):
    p = (n + 1) * (n + 2) * (n + 3)
    z = p + 2 * (n + 2) * (n + 3) + 1
    p0 = Fraction(p, z)
    p1 = Fraction(2 * (n + 2) * (n + 3), z)
    p2 = Fraction(1, z)
    assert p0 + p1 + p2 == 1
    assert p0 * 2 == p1 * (n + 1)
    assert p1 * (n + 1) == p2 * 2 * p
    # The D factor is 1/d!; phase-0 birth and death fluxes match exactly.
    for d in range(20):
        mu_d = Fraction(1, factorial(d))
        mu_next = Fraction(1, factorial(d + 1))
        assert p0 * mu_d * 2 == p0 * mu_next * (2 * (d + 1))
        cycle_flux_checks += 1

    # Exact low-degree identities used for the asymptotic boundary mass.
    assert z == n**3 + 8 * n**2 + 21 * n + 19
    assert z - p == 2 * n**2 + 10 * n + 13
    assert p1 * z == 2 * (n**2 + 5 * n + 6)


result = {
    "status": "FINITE_DIAGNOSTIC_PASS; infinite claims are proved symbolically in DEEPER_ATTACK.txt",
    "state_box": {"A": "0..30", "D": "0..4", "(B,C)": [[0, 2], [1, 1], [2, 0]]},
    "plane_states_checked": checked_states,
    "enabled_transitions_checked": checked_transitions,
    "absorbing_singleton_states_checked": absorbing_states,
    "stationary_cycle_flux_n": "0..100",
    "phase_and_D_flux_equalities_checked": cycle_flux_checks,
    "arithmetic": "Python integers and fractions.Fraction; no floating point",
    "scope": "Transcription diagnostics only; no finite check proves all-state classification, stationarity, recurrence, or tightness limits.",
}
out = Path(__file__).with_name("class_partition_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
